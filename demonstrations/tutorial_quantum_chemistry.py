r"""
Building molecular Hamiltonians
===============================


.. meta::
    :property="og:description": Learn how to build electronic Hamiltonians of molecules.

    :property="og:image": https://pennylane.ai/qml/_images/water_structure.png

.. related::
   tutorial_vqe Variational quantum eigensolver

*Author: PennyLane dev team. Last updated: 17 June 2021*

The ultimate goal of computational quantum chemistry is to unravel the
quantum effects that determine the structure and properties of molecules. Reaching
this goal is challenging since the characteristic energies associated with
these effects, e.g., the electronic correlation energy, are typically a tiny fraction
of the total energy of the molecule.

Accurate molecular properties can be computed from the wave function describing the
interacting electrons in a molecule. The **electronic** wave function
:math:`\Psi(r)` satisfies the `Schrödinger equation
<https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation>`_

.. math::
    H_e \Psi(r) = E \Psi(r),

where :math:`H_e` and :math:`E` denote the electronic Hamiltonian and the
total energy of the molecule, respectively. When solving the latter equation,
the nuclei of the molecule can be treated as point particles whose coordinates
are fixed [#BornOpp1927]_. In this approximation, both the total energy and
the electronic Hamiltonian depend parametrically on the nuclear coordinates.


In this tutorial, you will learn how to use PennyLane to build a
representation of the electronic Hamiltonian :math:`H_e` that can be used to perform
**quantum** simulations of molecules [#yudong2019]_. First, we show how to define
the structure of the molecule in terms of the symbols and the coordinates of
the atoms. Next, we describe how to solve the `Hartree-Fock
equations <https://en.wikipedia.org/wiki/Hartree%E2%80%93Fock_method>`_ for the target
molecule by interfacing with classical quantum chemistry packages. Then, we
outline how to decompose the fermionic Hamiltonian into a set of Pauli operators
whose expectation values can be measured in a quantum computer to estimate the total energy
of the molecule. Finally, we discuss some advanced features that can be used to simulate
more complicated systems.

Let's get started!

Defining the molecular structure
--------------------------------
In this example we construct the electronic Hamiltonian of the water molecule.


.. figure:: ../demonstrations/quantum_chemistry/water_structure.png
    :width: 30%
    :align: center

The structure of a molecule is defined by the symbols and the nuclear coordinates of
its constituent atoms. It can be specified using different `chemical file formats
<https://en.wikipedia.org/wiki/Chemical_file_format>`_. Within PennyLane, the molecular
structure is defined by providing a list with the atomic symbols and a one-dimensional
array with the nuclear coordinates in
`atomic units <https://en.wikipedia.org/wiki/Hartree_atomic_units>`_.
"""
import numpy as np

symbols = ["H", "O", "H"]
coordinates = np.array([-0.0399, -0.0038, 0.0, 1.5780, 0.8540, 0.0, 2.7909, -0.5159, 0.0])

##############################################################################
# The :func:`~.pennylane_qchem.qchem.read_structure` function can also be used to read the
# molecular geometry from an external file.


from pennylane import qchem

symbols, coordinates = qchem.read_structure("h2o.xyz")

##############################################################################
# The xyz format is supported out of the box. If
# `Open Babel <http://openbabel.org/wiki/Main_Page>`_ is installed, any
# format recognized by Open Babel is also supported by PennyLane.
#
# Solving the Hartree-Fock equations
# ----------------------------------
# The molecule's electronic Hamiltonian is commonly represented using the
# `second-quantization <https://en.wikipedia.org/wiki/Second_quantization>`_ formalism,
# which we will explore in more detail in the
# next section. To that aim, a basis of **single-particle** states needs to be chosen.
# In quantum chemistry these states are the
# `molecular orbitals <https://en.wikipedia.org/wiki/Molecular_orbital>`_
# which describe the wave function of a single electron in the molecule.
#
# Molecular orbitals are typically represented as a linear combination of **atomic orbitals**.
# The expansion coefficients in the atomic basis are calculated using the
# `Hartree-Fock (HF) method <https://en.wikipedia.org/wiki/Hartree%E2%80%93Fock_method>`_.
# In the HF approximation, each electron in the molecule is treated as an **independent**
# particle that moves under the influence of the Coulomb potential due to the nuclei, and a mean
# field generated by all other electrons [#pople1977]_. The optimized coefficients are precisely
# what we need to build the second-quantized Hamiltonian.
#
# We can call the function :func:`~.pennylane_qchem.qchem.meanfield` to perform
# the Hartree-Fock calculation using either the quantum chemistry package `PySCF
# <https://sunqm.github.io/pyscf/>`_, or `Psi4 <http://www.psicode.org/>`_. Here
# we use PySCF, which is the default option.

hf_file = qchem.meanfield(symbols, coordinates)

##############################################################################
# This function creates a local file that will later be used to compute the Hamiltonian.
#
# .. _hamiltonian:
#
# Building the Hamiltonian
# ------------------------
# In the second quantization formalism, the electronic wave function of the molecule
# is represented in the occupation number basis. For :math:`M` *spin* molecular
# orbitals, the elements of this basis are labelled as
# :math:`\vert n_0, n_1, \dots, n_{M-1} \rangle`, where :math:`n_i = 0,1`
# indicates the occupation of each orbital. In this representation, the electronic
# Hamiltonian is given by
#
# .. math::
#     H = \sum_{p,q} h_{pq} c_p^\dagger c_q +
#     \frac{1}{2} \sum_{p,q,r,s} h_{pqrs} c_p^\dagger c_q^\dagger c_r c_s,
#
# where :math:`c^\dagger` and :math:`c` are the electron creation
# and annihilation operators, respectively, and the coefficients
# :math:`h_{pq}` and :math:`h_{pqrs}` denote the one- and two-electron
# Coulomb integrals [#ref_integrals]_ evaluated using the Hartree-Fock
# orbitals.
#
# We can use the states of :math:`M` qubits to encode any element
# of the occupation number basis
#
# .. math::
#     \vert n_0, n_1, \dots, n_{M-1} \rangle \rightarrow \vert q_0 q_1 \cdots q_{M-1} \rangle.
#
# This implies that we need to map the fermionic operators onto operators
# that act on qubits. This can be done by using the
# `Jordan-Wigner <https://en.wikipedia.org/wiki/Jordan-Wigner_transformation>`_
# transformation [#seeley2012]_ which allows us to decompose the fermionic Hamiltonian
# into a linear combination of the tensor product of Pauli operators
#
# .. math::
#     \sum_j C_j \otimes_i \sigma_i^{(j)},
#
# where :math:`C_j` is a scalar coefficient and :math:`\sigma_i` represents an
# element of the Pauli group :math:`\{ I, X, Y, Z \}`.
#
# This fermionic-to-qubit transformation is done using
# the :func:`~.pennylane_qchem.qchem.decompose` function, which
# uses `OpenFermion <https://github.com/quantumlib/OpenFermion>`_
# to compute the electron integrals using the previously generated
# results of the mean field calculation. Then, it builds the fermionic Hamiltonian and
# maps it to the qubit representation.

qubit_hamiltonian = qchem.decompose(hf_file, mapping="jordan_wigner")
print("Qubit Hamiltonian of the water molecule")
print(qubit_hamiltonian)

##############################################################################
# It is often convenient to use the :func:`~.pennylane_qchem.qchem.molecular_hamiltonian`
# function which encapsulates all the steps explained above. It simplifies the process of building
# the electronic Hamiltonian to a single line of code. We just need to input the
# symbols and the nuclear coordinates of the molecule, as shown below:

H, qubits = qchem.molecular_hamiltonian(symbols, coordinates)
print("Number of qubits: {:}".format(qubits))
print("Qubit Hamiltonian")
print(H)

##############################################################################
# Additionally, if you have built your electronic Hamiltonian independently using
# `OpenFermion <https://github.com/quantumlib/OpenFermion>`_ tools, it can
# be readily converted to a PennyLane observable using the
# :func:`~.pennylane_qchem.qchem.convert_observable` function.
#
# Advanced features
# -----------------
# The :func:`~.pennylane_qchem.qchem.meanfield` function allows us to define additional keyword
# arguments to solve the Hartree-Fock equations of more complicated systems.
# The net charge of the molecule may be specified to simulate positively or negatively
# charged molecules. For a neutral system we choose

charge = 0

##############################################################################
# We can also specify the
# `spin multiplicity <https://en.wikipedia.org/wiki/Multiplicity_(chemistry)>`_. For the
# water molecule, which contains ten electrons, the `Slater determinant
# <https://en.wikipedia.org/wiki/Slater_determinant>`_ resulting from occupying the five
# lowest-energy orbitals with two *paired* electrons per orbital has spin multiplicity one.
# Alternatively, if we define an occupation where the first four orbitals are doubly occupied
# and the next two are singly occupied by *unpaired* electrons, the HF state will have
# multiplicity three.
#
# |
#
# .. figure:: ../demonstrations/quantum_chemistry/hf_references.png
#     :width: 50%
#     :align: center
#
# |
#
# For the neutral water molecule we have,

multiplicity = 1

##############################################################################
# As mentioned above, molecular orbitals are represented as a linear combination
# of atomic orbitals which are typically modeled as `Gaussian-type orbitals
# <https://en.wikipedia.org/wiki/Gaussian_orbital>`_. We can specify different types
# of `Gaussian atomic basis <https://www.basissetexchange.org/>`_. In this example we
# choose a `minimal basis set
# <https://en.wikipedia.org/wiki/Basis_set_(chemistry)#Minimal_basis_sets>`_.

basis_set = "sto-3g"

##############################################################################
# PennyLane also allows us to define an active space [#truhlar2018]_ to perform quantum
# simulations with a reduced number of qubits. This is done by classifying the molecular
# orbitals as core, active, and external orbitals:
#
# * Core orbitals are always occupied by two electrons.
# * Active orbitals can be occupied by zero, one, or two electrons.
# * The external orbitals are never occupied.
#
# Within this approximation, a certain number of **active electrons** are allowed to
# populate a finite set of **active orbitals**.
#
# .. figure:: ../demonstrations/quantum_chemistry/sketch_active_space.png
#     :width: 40%
#     :align: center
#
# .. note::
#     The number of active **spin-orbitals** determines the **number of qubits** required
#     to perform the quantum simulations.
#
# For the water molecule in a minimal basis set we have a total of ten electrons
# and seven molecular orbitals. In this example we define an symmetric active space with
# four electrons and four active orbitals using
# the :func:`~.pennylane_qchem.qchem.active_space` function:

electrons = 10
orbitals = 7
core, active = qchem.active_space(electrons, orbitals, active_electrons=4, active_orbitals=4)

##############################################################################
# Viewing the results:

print("List of core orbitals: {:}".format(core))
print("List of active orbitals: {:}".format(active))
print("Number of qubits: {:}".format(2 * len(active)))

##############################################################################
# Finally, we use the :func:`~.pennylane_qchem.qchem.molecular_hamiltonian` function to
# build the resulting Hamiltonian of the water molecule:

H, qubits = qchem.molecular_hamiltonian(
    symbols,
    coordinates,
    charge=charge,
    mult=multiplicity,
    basis=basis_set,
    active_electrons=4,
    active_orbitals=4,
)

print("Number of qubits required to perform quantum simulations: {:}".format(qubits))
print("Hamiltonian of the water molecule")
print(H)

##############################################################################
# In this case, since we have truncated the basis of molecular orbitals, the resulting
# observable is an approximation of the Hamiltonian generated in the
# section :ref:`hamiltonian`.
#
# You have completed the tutorial! Now, select your favorite molecule and build its electronic
# Hamiltonian.
# To see how simple it is to implement the VQE algorithm to compute the ground-state energy of
# your molecule using PennyLane, take a look at the tutorial :doc:`tutorial_vqe`.
#
# References
# ----------
#
# .. [#yudong2019]
#
#     Yudong Cao, Jonathan Romero, *et al.*, "Quantum Chemistry in the Age of Quantum Computing".
#     `Chem. Rev. 2019, 119, 19, 10856-10915.
#     <https://pubs.acs.org/doi/10.1021/acs.chemrev.8b00803>`_
#
# .. [#BornOpp1927]
#
#     M. Born, J.R. Oppenheimer, "Quantum Theory of the Molecules".
#     `Annalen der Physik 84, 457-484 (1927)
#     <https://onlinelibrary.wiley.com/doi/abs/10.1002/andp.19273892002>`_
#
# .. [#pople1977]
#
#     Rolf Seeger, John Pople. "Self‐consistent molecular orbital methods. XVIII. Constraints and
#     stability in Hartree–Fock theory". `Journal of Chemical Physics 66,
#     3045 (1977). <https://aip.scitation.org/doi/abs/10.1063/1.434318>`_
#
# .. [#ref_integrals]
#
#     J.T. Fermann, E.F. Valeev, "Fundamentals of Molecular Integrals Evaluation".
#     `arXiv:2007.12057 <https://arxiv.org/abs/2007.12057>`_
#
# .. [#seeley2012]
#
#     Jacob T. Seeley, Martin J. Richard, Peter J. Love. "The Bravyi-Kitaev transformation for
#     quantum computation of electronic structure". `Journal of Chemical Physics 137, 224109 (2012).
#     <https://aip.scitation.org/doi/abs/10.1063/1.4768229>`_
#
# .. [#truhlar2018]
#
#     J.J. Bao, S.S. Dong, L. Gagliardi, D.G. Truhlar. "Automatic Selection of an
#     Active Space for Calculating Electronic Excitation Spectra by MS-CASPT2 or MC-PDFT".
#     `Journal of Chemical Theory and Computation 14, 2017 (2018). 
#     <https://pubs.acs.org/doi/abs/10.1021/acs.jctc.8b00032>`_
