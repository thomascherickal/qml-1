 .. role:: html(raw)
   :format: html

Research
============

.. meta::
   :property="og:description": Implementations of the latest cutting-edge ideas and research from quantum machine learning using PennyLane.
   :property="og:image": https://pennylane.ai/qml/_static/demos_card.png


Explore cutting-edge research using PennyLane. The demonstrations below implement
ideas from inspiring papers that investigate the training of quantum circuits.
You can find research that targets quantum machine learning in the `Quantum machine learning`_ section,
or discover other variational quantum optimization algorithms under `Optimization`_.

.. raw:: html

    <link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.8.10/css/mdb.min.css" rel="stylesheet">


Quantum machine learning
------------------------
Delve into the latest exciting research and cutting-edge ideas in
quantum machine learning. Implement and run a vast array of different QML
applications on your own computer—using simulators from Xanadu,
IBM, Google, Rigetti, and many more—or on real hardware devices.

:html:`<div class="gallery-grid row">`

.. customgalleryitem::
    :tooltip: Create a simple QGAN with Cirq and TensorFlow.
    :figure: demonstrations/QGAN/qgan3.png
    :description: :doc:`demos/tutorial_QGAN`
    :tags: cirq tensorflow

.. customgalleryitem::
    :tooltip: Fit one-dimensional noisy data with a quantum neural network.
    :figure: demonstrations/quantum_neural_net/qnn_output_28_0.png
    :description: :doc:`demos/quantum_neural_net`
    :tags: autograd strawberryfields photonics

.. customgalleryitem::
    :tooltip: Universal Quantum Classifier with data-reuploading.
    :figure: demonstrations/data_reuploading/universal_dnn.png
    :description: :doc:`demos/tutorial_data_reuploading_classifier`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Quantum transfer learning.
    :figure: demonstrations/quantum_transfer_learning/transfer_images.png
    :description: :doc:`demos/tutorial_quantum_transfer_learning`
    :tags: autograd pytorch

.. customgalleryitem::
    :tooltip: Training an embedding to perform metric learning.
    :figure: demonstrations/embedding_metric_learning/training.png
    :description: :doc:`demos/tutorial_embeddings_metric_learning`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Pre-process images with a quantum convolution.
    :figure: demonstrations/quanvolution/zoom.png
    :description: :doc:`demos/tutorial_quanvolution`
    :tags: tensorflow

.. customgalleryitem::
    :tooltip: Variational Quantum Linear Solver.
    :figure: demonstrations/vqls/vqls_zoom.png
    :description: :doc:`demos/tutorial_vqls`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Coherent implementation of a variational quantum linear solver.
    :figure: demonstrations/coherent_vqls/cvqls_zoom.png
    :description: :doc:`demos/tutorial_coherent_vqls`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Implement a multiclass variational classifier using PyTorch, PennyLane, and the iris dataset.
    :figure: demonstrations/multiclass_classification/margin_2.png
    :description: :doc:`demos/tutorial_multiclass_classification`
    :tags: pytorch

.. customgalleryitem::
    :tooltip: Differentiate any qubit gate with the stochastic parameter-shift rule.
    :figure: demonstrations/stochastic_parameter_shift/stochastic_parameter_shift_thumbnail.png
    :description: :doc:`demos/tutorial_stochastic_parameter_shift`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Using a quantum graph recurrent neural network to learn quantum dynamics.
    :figure: demonstrations/qgrnn/qgrnn_thumbnail.png
    :description: :doc:`demos/tutorial_qgrnn`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Optimize a Quantum Optical Neural Network using NLopt.
    :figure: demonstrations/qonn/qonn_thumbnail.png
    :description: :doc:`demos/qonn`
    :tags: autograd photonics

.. customgalleryitem::
    :tooltip: Understand the link between variational quantum models and Fourier series.
    :figure: demonstrations/expressivity_fourier_series/expressivity_thumbnail.png
    :description: :doc:`demos/tutorial_expressivity_fourier_series`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Making a quantum machine learning model using neutral atoms
    :figure: demonstrations/pasqal/pasqal_thumbnail.png
    :description: :doc:`demos/tutorial_pasqal`
    :tags: cirq tensorflow

.. customgalleryitem::
    :tooltip: Kernel-based training with scikit-learn.
    :figure: demonstrations/kernel_based_training/scaling.png
    :description: :doc:`demos/tutorial_kernel_based_training`
    :tags: pytorch sklearn kernels

.. customgalleryitem::
    :tooltip: Meta-learning technique for variational quantum algorithms.
    :figure: demonstrations/learning2learn/l2l_thumbnail.png
    :description: :doc:`demos/learning2learn`
    :tags: tensorflow

.. customgalleryitem::
    :tooltip: Kernels and alignment training with PennyLane.
    :figure: demonstrations/kernels_module/QEK_thumbnail.png
    :description: :doc:`demos/tutorial_kernels_module`
    :tags: kernels alignment classification 

:html:`</div></div><div style='clear:both'>`

Optimization
------------
Here you will find demonstrations showcasing quantum optimization. Explore
various topics and ideas, such as the shots-frugal Rosalin
optimizer, the variational quantum thermalizer, or the issue of barren
plateaus in quantum neural networks.

:html:`<div class="gallery-grid row">`

.. customgalleryitem::
    :tooltip: Faster optimization convergence using quantum natural gradient.
    :figure: demonstrations/quantum_natural_gradient/qng_optimization.png
    :description: :doc:`demos/tutorial_quantum_natural_gradient`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Barren plateaus in quantum neural networks.
    :figure: demonstrations/barren_plateaus/surface.png
    :description: :doc:`demos/tutorial_barren_plateaus`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Rotoselect algorithm.
    :figure: demonstrations/rotoselect/rotoselect_structure.png
    :description: :doc:`demos/tutorial_rotoselect`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Doubly stochastic gradient descent.
    :figure: demonstrations/doubly_stochastic/single_shot.png
    :description: :doc:`Doubly stochastic gradient descent <demos/tutorial_doubly_stochastic>`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Frugal shot optimization with the Rosalin optimizer.
    :figure: demonstrations/rosalin/rosalin_thumb.png
    :description: :doc:`demos/tutorial_rosalin`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Understand the difference between local and global cost functions.
    :figure: demonstrations/local_cost_functions/Local_Thumbnail.png
    :description: :doc:`demos/tutorial_local_cost_functions`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Optimizing measurement protocols with variational methods.
    :figure: demonstrations/quantum_metrology/illustration.png
    :description: :doc:`demos/tutorial_quantum_metrology`
    :tags: cirq metrology autograd

.. customgalleryitem::
    :tooltip: Learn about the variational quantum thermalizer algorithm, an extension of VQE.
    :figure: demonstrations/vqt/thumbnail.png
    :description: :doc:`demos/tutorial_vqt`
    :tags: chemistry

.. customgalleryitem::
    :tooltip: VQE optimization using quantum natural gradient.
    :figure: demonstrations/vqe_qng/vqe_qng_thumbnail.png
    :description: :doc:`demos/tutorial_vqe_qng`
    :tags: chemistry

.. customgalleryitem::
    :tooltip: Optimize and reduce the number of measurements required to evaluate a variational algorithm cost function.
    :figure: demonstrations/measurement_optimize/meas_optimize_thumbnail.png
    :description: :doc:`demos/tutorial_measurement_optimize`
    :tags: chemistry

.. customgalleryitem::
    :tooltip: Reduce the number of device executions by using a stochastic approximation optimization.
    :figure: demonstrations/spsa/spsa_mntn.png
    :description: :doc:`demos/spsa`
    :tags: qiskit

.. customgalleryitem::
    :tooltip: Solve combinatorial problems without a classical optimizer.
    :figure: demonstrations/falqon/falqon_thumbnail.png
    :description: :doc:`demos/tutorial_falqon`
    :tags: autograd

.. customgalleryitem::
    :tooltip: Optimizing the geometry of molecules.
    :figure: demonstrations/mol_geo_opt/fig_thumbnail.png
    :description: :doc:`demos/tutorial_mol_geo_opt`
    :tags: chemistry

:html:`</div></div><div style='clear:both'>`


Quantum computing
-----------------

Explore the applications of PennyLane to more general quantum computing tasks
such as benchmarking and characterizing quantum processors.

:html:`<div class="gallery-grid row">`

.. customgalleryitem::
    :tooltip: Beyond classical computing with qsim.
    :figure: demonstrations/qsim_beyond_classical/sycamore.png
    :description: :doc:`demos/qsim_beyond_classical`
    :tags: cirq qsim

.. customgalleryitem::
   :tooltip: Construct and simulate a Gaussian Boson Sampler.
   :figure: demonstrations/tutorial_gbs_thumbnail.png
   :description: :doc:`demos/tutorial_gbs`
   :tags: photonics strawberryfields

.. customgalleryitem::
   :tooltip: Learn how to compute the quantum volume of a quantum processor.
   :figure: demonstrations/quantum_volume/quantum_volume_thumbnail.png
   :description: :doc:`demos/quantum_volume`
   :tags: characterization qiskit

.. customgalleryitem::
   :tooltip: Learn how to sample quantum states uniformly at random
   :figure: demonstrations/haar_measure/spherical_int_dtheta.png
   :description: :doc:`demos/tutorial_haar_measure`
   :tags: quantumcomputing

.. customgalleryitem::
    :tooltip: Approximate quantum states with classical shadows.
    :figure: demonstrations/classical_shadows/atom_shadow.png
    :description: :doc:`demos/tutorial_classical_shadows`
    :tags: quantumcomputing characterization

:html:`</div></div><div style='clear:both'>`


.. toctree::
    :maxdepth: 2
    :hidden:

    demos/tutorial_quantum_natural_gradient
    demos/tutorial_barren_plateaus
    demos/tutorial_rotoselect
    demos/tutorial_doubly_stochastic
    demos/tutorial_rosalin
    demos/tutorial_local_cost_functions
    demos/tutorial_vqls
    demos/tutorial_coherent_vqls
    demos/tutorial_quantum_metrology
    demos/tutorial_vqt
    demos/tutorial_vqe_qng
    demos/tutorial_measurement_optimize
    demos/spsa
    demos/tutorial_QGAN
    demos/quantum_neural_net
    demos/tutorial_data_reuploading_classifier
    demos/tutorial_quantum_transfer_learning
    demos/tutorial_embeddings_metric_learning
    demos/tutorial_quanvolution
    demos/tutorial_multiclass_classification
    demos/tutorial_stochastic_parameter_shift
    demos/tutorial_pasqal
    demos/tutorial_qgrnn
    demos/qonn
    demos/tutorial_expressivity_fourier_series
    demos/qsim_beyond_classical
    demos/quantum_volume
    demos/tutorial_haar_measure
    demos/tutorial_gbs
    demos/learning2learn
    demos/tutorial_mol_geo_opt
    demos/tutorial_classical_shadows
