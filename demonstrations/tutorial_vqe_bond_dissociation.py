r"""
Modeling bond dissociations and chemical reactions using VQE
=======================

.. meta::
    :property="og:description": Construct Potential energy surface for a simple bond dissociation and general chemical     reactions  using the variational quantum eigensolver algorithm in PennyLane.
    :property="og:image": https://pennylane.ai/qml/_images/pes_h2.png

.. related::

   tutorial_vqe
   tutorial_vqe_parallel VQE with parallel QPUs
   tutorial_vqe_qng Accelerating VQE with the QNG

*Author: PennyLane dev team. Last updated: 25 Apr 2021.*

Chemical reaction is another name for transformation of molecules - breaking and forming of bonds - accompanied with energy cost. This energy cost determines the feasibility of a particular transformation amongst many different alternate possibilities.  

## A + B -> C + D

Wouldn't it be nice to use theoretical tools to model chemical reactions? This is indeed the case and the field of quantum chemistry has several methods to do that. In this tutorial, we will learn how Pennylane could be used to do exactly the same albeit on a quantum computer or a classical simulator. 

Quantum computing aims to revolutionalize this exploration of chemical reactions. We could possibly build the exact energy landscapes and thus unearth the most feasible routes for any general chemical reaction. This could enable us to find new routes for a chemical reaction to occur (i.e reaction mechanism), develop and design new catalysts and create molecules and materials with tailored properties.

In a previous tutorial, we looked at how a hybrid quantum-classical algorithm, Variational Quantum Eigensolver (VQE), [#peruzzo2014]_ is used to compute molecular energies which are the expectation value of the molecular Hamiltonian. Here, we show how VQE can be used as a tool to construct potential energy surfaces(PES) for any general molecular transformation and how this lends way to the calculation of important quantities such as activation energy barrier, reaction energy and reaction rates. As illustrative examples, we use VQE and other tools implemented in Pennylane library to study a simple diatomic bond dissociation and reactions involving exchange of hydrogen atoms. Let's get started! ⚛️


##############################################################################
# An illustration of potential energy surface of H-H bond dissociation for hydrogen molecule. The y-axis is the total imolecular energy and x-axis is the H-H bond distance. By looking at this curve, we could estimate the H-H equilibrium bond distance and the energy required to break the H-H bond.   
#
# |
#
# .. figure::  /demonstrations/vqe_bond_dissociation/h2_pes_pictorial.png
#     :width: 50%
#     :align: center
#
# |
#

##############################################################################


Potential Energy Surfaces: Hills to die and be reborn for molecules
---------------------------------------------------------------------

Potential energy surfaces (PES) are, in simple words, energy landscapes on which any chemical reaction or any transformation occurs. But what is it? The concept originates with the idea that "nuclies are heavier than electron" aka Born-Oppenheimer approximation and that we can solve for the electronic wavefunction with nucleis clamped to their respective positions. This results in separation of nuclear and electronic parts of the Schrodinger equation and we only solve the electronic part:  $  H_{el}|\Psi \rangle =  E_{el}|\Psi\rangle  $
        
From here arises the concept of electronic energy of the molecule, a quantum mechanical system, as a function of interatomic coordinates and angles, and potential energy surface is a n-dimensional plot of E with the respective degrees of freedom. It gives us a visual tool to undertstand chemical reactions where stable molecules are the local minimas in the valleys and transition states the *hill peaks* to climb.

This is to say that we solve the electronic Schrodinger equation for a given fixed positions of nucleis, and then we move nucleis in incremental step. The obtained set of energies are then plotted against nuclear positions.

We will begin by showing how this works for a simple diatomic molecule such as H2.  H$_2$ is the simplest of the molecules and the formation (or breaking) of the H-H bond is the simplest of all reactions. 

H${_2}$ $\rightarrow$ H $+$ H  

In terms of quantum computing terms, this is a 4 qubit problem if considered in a minimal basis set i.e. 2 electron in 4 spin orbitals. And as discussed in the previous tutorial, the states involved are |1100> (also the Hartree-Fock ground state), |1010>, |0101> and |0011>, these are the only states out of 2^4 (=16) states that matter for this problem and are obtained by single and double particle-hole excitation out of the HF state. Below we show how to set upthe problem to generate a PES for such a reaction. 

The first step is to import the required libraries and packages:
"""

import pennylane as qml
from pennylane import qchem
from pennylane import numpy as np
import time

##############################################################################
# The second step is to specify the geometry and charge of the molecule,
# and the spin multiplicity of the electronic configuration. To construct the potential energy surface,
# we need to vary the geometry. So, we keep one H atom fixed at origin and vary the x-coordinate of the other
# H atom such that the bond distance varies from 1.0 to 4.0 Bohrs in steps of 0.25 Bohrs.

charge = 0
multiplicity = 1
basis_set = "sto-3g"

electrons = 2

active_electrons = 2
active_orbitals = 2

vqe_energy = []

# set up a loop to change internuclear distance
for r_HH in np.arange(0.5, 4.0, 0.1):

    symbols, coordinates = (["H", "H"], np.array([0.0, 0.0, 0.0, 0.0, 0.0, r_HH]))

    # Do a meanfield calculation -> Define a fermionic Hamiltonian -> turn into a qubit Hamiltonian
    H, qubits = qchem.molecular_hamiltonian(
        symbols,
        coordinates,
        charge=charge,
        mult=multiplicity,
        basis=basis_set,
        package="pyscf",
        active_electrons=active_electrons,
        active_orbitals=active_orbitals,
        mapping="jordan_wigner",
    )

    print("Number of qubits = ", qubits)
    print("Hamiltonian is ", H)

    ##############################################################################
    # Now to build the circuit for a general molecular system. We begin by preparing the
    # qubit version of HF state, :math:`|1100\rangle.
    # We then identify and add all possible single and double excitations. In this case, there is only one
    # double excitationi(:math:`|0011\rangle) and two single excitations(:math:`|0110\rangle and :math:`|1001\rangle))

    # get all the singles and doubles excitations

    singles, doubles = qchem.excitations(active_electrons, active_orbitals * 2)
    print("Single excitations", singles)
    print("Double excitations", doubles)

    # define the circuit
    def circuit(params, wires):
        # Prepare the HF state |1100> by flipping the qubits 0 and 1
        qml.PauliX(0)
        qml.PauliX(1)
        # Add double excitation
        qml.DoubleExcitation(params[0], wires=[0, 1, 2, 3])
        # Add single excitations too
        qml.SingleExcitation(params[1], wires=[0, 2])
        qml.SingleExcitation(params[2], wires=[1, 3])

    ##############################################################################
    # From here on, we can use optimizers in PennyLane
    #
    # PennyLane contains the :class:`~.ExpvalCost` class, specifically
    # that we use to obtain the cost function central to the idea of variational optimization
    # of parameters in VQE algorithm. We define the device which is a classical qubit simulator,
    # a cost function which calculates the expectation value of Hamiltonian operator for the
    # given trial wavefunction and also the gradient descent optimizer that will be used to optimize
    # the gate parameters:

    dev = qml.device("default.qubit", wires=qubits)
    cost_fn = qml.ExpvalCost(circuit, H, dev)
    opt = qml.GradientDescentOptimizer(stepsize=0.4)

    ##############################################################################
    # A related question is what are gate parameters that we seek to optimize?
    # These could be thought of as rotation variables in the gates used which
    # can then be translated into determinant coefficients in the wavefunction expansion.

    # define and initialize the gate parameters
    params = np.zeros(3)
    dcircuit = qml.grad(cost_fn, argnum=0)
    dcircuit(params)

    ##############################################################################
    # We then define the VQE optimization iteration and the convergence criteria :math:`\sim 10^{
    # -6}`
    prev_energy = 0.0

    for n in range(40):

        t1 = time.time()

        params, energy = opt.step_and_cost(cost_fn, params)

        t2 = time.time()

        print("Iteration = {:},  E = {:.8f} Ha, t = {:.2f} S".format(n, energy, t2 - t1))

        # define your convergence criteria, we choose modest value of 1E-6 Ha
        if np.abs(energy - prev_energy) < 1e-6:
            break

        prev_energy = energy

    print("At bond distance \n", r_HH)
    print("The VQE energy is", energy)

    vqe_energy.append(energy)

##############################################################################
# Once we have the Energy as a function of H-H bond distance, we could the plot it

# Plot the Potential energy surface
# Energy as a function of internuclear distance

r = np.arange(0.5, 4.0, 0.1)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(r, vqe_energy, label="VQE(S+D)")

ax.set(
    xlabel="Distance (H-H, in Angstrom)", ylabel="Total energy", title="PES for H$_2$ dissociation"
)
ax.grid()
ax.legend()

# fig.savefig("test.png")
plt.show()


##############################################################################
#  This was a simple 1D PES for Hydrogen molecule. It gives an estimate of H-H bond distance to be ~ 1.4 Bohrs
#  H-H bond dissociation energy (the difference in energy at equilibrium and energy at dissociation limit)
#  around 0.194 Hartrees (121.8 Kcal/mol). Can these estimates be improved? Yes, by using bigger basis sets and
#  extrapolating to the complete basis set (CBS) limit.
#
# .. _vqe_references:
#
# References
# ----------
#
# .. [#peruzzo2014]
#
#     Alberto Peruzzo, Jarrod McClean *et al.*, "A variational eigenvalue solver on a photonic
#     quantum processor". `Nature Communications 5, 4213 (2014).
#     <https://www.nature.com/articles/ncomms5213?origin=ppub>`__
#
# .. [#yudong2019]
#
#     Yudong Cao, Jonathan Romero, *et al.*, "Quantum Chemistry in the Age of Quantum Computing".
#     `Chem. Rev. 2019, 119, 19, 10856-10915.
#     <https://pubs.acs.org/doi/10.1021/acs.chemrev.8b00803>`__
