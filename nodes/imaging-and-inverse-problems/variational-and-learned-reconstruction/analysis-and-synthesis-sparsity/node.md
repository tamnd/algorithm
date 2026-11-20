---
tag: 6V9TP3
kind: concept
slug: analysis-and-synthesis-sparsity
name: Analysis and synthesis sparsity
aliases:
- analysis prior
- synthesis prior
- cosparsity
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: A synthesis model writes the image as a sparse sum of atoms, while an analysis model asks that an operator such as a gradient map the image to a sparse vector.
prereqs: [sparse-signal-recovery, variational-regularization, discrete-wavelet-transform]
see_also: [compressed-sensing, total-variation-denoising, total-generalized-variation, dictionary-learning, basis-pursuit, haar-wavelet, split-bregman-method, iterative-shrinkage-thresholding]
sources:
  - paper: doi:10.1088/0266-5611/23/3/007
    title: Michael Elad, Peyman Milanfar and Ron Rubinstein, Analysis versus synthesis in signal priors, Inverse Problems 23(3), 2007
    locator: pages 947 to 968 (the two MAP formulations, their equality for a square invertible operator and their difference for redundant ones)
  - paper: doi:10.1016/j.acha.2012.03.006
    title: Sangnam Nam, Mike E. Davies, Michael Elad and Remi Gribonval, The cosparse analysis model and algorithms, Applied and Computational Harmonic Analysis 34(1), 2013
    locator: pages 30 to 56 (cosparsity, the union of subspaces of the analysis model and its uniqueness and recovery results)
  - paper: doi:10.1016/j.acha.2010.10.002
    title: Emmanuel J. Candes, Yonina C. Eldar, Deanna Needell and Paige Randall, Compressed sensing with coherent and redundant dictionaries, Applied and Computational Harmonic Analysis 31(1), 2011
    locator: pages 59 to 73 (recovery guarantees for l1 analysis with a tight frame)
  - paper: doi:10.1017/S0962492918000016
    title: Martin Benning and Martin Burger, Modern regularization methods for inverse problems, Acta Numerica 27, 2018
    locator: pages 1 to 111 (sparsity regularizers in the variational framework)
---

Sparsity priors come in two forms. A **synthesis** model writes the image as $x = Dz$ with a dictionary $D \in \mathbb{R}^{n \times p}$ and asks that the coefficient vector $z$ be sparse; an **analysis** model applies an operator $\Omega \in \mathbb{R}^{p \times n}$ to the image and asks that $\Omega x$ have many zeros, a property called **cosparsity**. The two give the same variational problem when the operator is square and invertible, for example an orthonormal wavelet basis, and different problems for redundant frames (Elad, Milanfar and Rubinstein 2007). Total variation is the main analysis prior in imaging.

## In plain words

There are two ways to say that an image is simple. The first way says: the image is built from a few pieces taken from a fixed list of building blocks. To store it, keep the few pieces and their weights. The second way says: if you run a set of tests on the image, most tests give zero. A test can be "is this pixel equal to its neighbor", and a cartoon image passes most of these tests. When the list of blocks and the set of tests are the same size and match one to one, the two ways say the same thing. When there are more blocks or tests than pixels, they say different things and give different reconstructions.

## The idea

**The two variational problems.** For data $y = Ax + e$ and weight $\lambda > 0$:

$$\text{synthesis:}\quad \hat z \in \arg\min_{z \in \mathbb{R}^p} \tfrac12\|ADz - y\|^2 + \lambda\|z\|_1,\qquad \hat x_S = D\hat z,$$

$$\text{analysis:}\quad \hat x_A \in \arg\min_{x \in \mathbb{R}^n} \tfrac12\|Ax - y\|^2 + \lambda\|\Omega x\|_1.$$

Both are instances of [variational regularization](/variational-regularization/). The synthesis problem is a [lasso](/lasso-regression/) in $z$ and is solved by [iterative shrinkage](/iterative-shrinkage-thresholding/), as the proximal operator of $\|z\|_1$ is soft thresholding. The analysis problem has the operator inside the norm, so its proximal operator has no closed form in general; [split Bregman](/split-bregman-method/), [ADMM](/admm/) or the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) split $\Omega x$ off as a new variable.

**When they agree.** If $p = n$ and $\Omega = D^{-1}$, the change of variables $z = \Omega x$ maps one problem onto the other, so $\hat x_S = \hat x_A$. An orthonormal basis with $\Omega = D^\top$ is the common case. When $p > n$ the matrix $D$ has a null space, and many $z$ give the same $x$; the synthesis problem picks the sparsest coding of each candidate in its penalty, while the analysis problem charges every candidate by all its correlations $\Omega x$. For a redundant tight frame with $\Omega = D^\top$ the two problems are in general different, as the example below shows.

**The geometry of the models.** In synthesis, an image with $k$ active atoms lies in the span of those $k$ columns of $D$, so the model is a union of subspaces of dimension at most $k$. In analysis, an image with $\ell$ zeros in $\Omega x$ lies in the orthogonal complement of those $\ell$ rows, so the model is a union of subspaces of dimension at least $n - \ell$ (Nam et al. 2013). The number $\ell$ of zeros is the cosparsity. For a redundant $\Omega$ the analysis model needs many zeros to be small, and its subspaces are of a different kind from the synthesis subspaces: a high cosparsity counts the constraints that hold, not the atoms that are used.

**Total variation as analysis.** With $\Omega$ the matrix of forward differences, $\|\Omega x\|_1$ is the anisotropic total variation, and the zeros of $\Omega x$ are the places where neighboring pixels are equal. A piecewise constant image with short boundaries is highly cosparse. [Total generalized variation](/total-generalized-variation/) is an analysis prior with a second order operator on the pair $(x, w)$.

**Recovery guarantees.** For synthesis, the theory of [compressed sensing](/compressed-sensing/) and [basis pursuit](/basis-pursuit/) needs $AD$ to satisfy a restricted isometry or coherence condition, which fails for a coherent $D$. Candes, Eldar, Needell and Randall (2011) prove error bounds for $\ell_1$ analysis with a tight frame $D$ and $\Omega = D^*$ under a restricted isometry condition on $A$ adapted to $D$, with the error controlled by the tail of $D^*x$. This allows highly redundant and coherent frames.

## Examples

**Haar basis against differences.** For $n = 4$, the orthonormal [Haar](/haar-wavelet/) coefficients of the step $(0, 0, 3, 3)$ are $(3, -3, 0, 0)$: 2 nonzeros. The step $(0, 3, 3, 3)$, with the edge at a different place, has the coefficients $(4.5, -1.5, -2.1213, 0)$: 3 nonzeros. Its forward differences $(3, 0, 0)$ have one nonzero, as do those of the first step, $(0, 3, 0)$, so both have cosparsity 2 for $\Omega$ the difference matrix. The Haar synthesis model depends on the position of the edge relative to the dyadic grid; the difference analysis model does not.

**A tight frame in the plane.** Let $D \in \mathbb{R}^{2 \times 3}$ have the three columns $d_k = \sqrt{2/3}\,(\cos\theta_k, \sin\theta_k)$ with $\theta_k = \pi/2 + 2\pi k/3$:

$$D = \begin{pmatrix} 0 & -0.707107 & 0.707107 \\ 0.816497 & -0.408248 & -0.408248 \end{pmatrix},\qquad DD^\top = I.$$

This is a Parseval tight frame, and $d_0 + d_1 + d_2 = 0$. Take $A = I$, $\Omega = D^\top$ and $\lambda = 0.3$.

| data $y$ | synthesis $\hat x_S$ | analysis $\hat x_A$ |
|---|---|---|
| $(0, 1)$, along the atom $d_0$ | $(0,\ 1 - \sqrt{3/2}\,\lambda) = (0, 0.6326)$ | $(0,\ 1 - 2\sqrt{2/3}\,\lambda) = (0, 0.5101)$ |
| $(1, 0)$, between $d_1$ and $d_2$ | $(0.575736, 0)$ | $(0.575736, 0)$ |

For $y = (0, 1)$ the synthesis solution uses one atom, $\hat z = (0.77474, 0, 0)$, and shrinks along it. The analysis solution has $\Omega\hat x_A = (0.4165, -0.20825, -0.20825)$, with no zero entry. The gradient of $\|D^\top x\|_1$ there is $d_0 - d_1 - d_2 = 2d_0$, so the analysis solution is $y - 2\lambda d_0$. The synthesis solution is $y - \lambda d_0/\|d_0\|^2 = y - 1.5\lambda d_0$. The analysis prior pulls harder along $d_0$, and the two reconstructions differ. For $y = (1, 0)$ the analysis vector $\Omega x$ has a zero in its first entry and the two models give the same point.

**Image models.** Wavelet synthesis with an orthonormal basis and wavelet analysis are the same problem. With the undecimated (translation invariant) wavelet frame they differ, and compressed sensing MRI often uses the analysis form. In one dimension, total variation equals a synthesis model whose atoms are step functions, with the constant left free. In two dimensions the difference operator has about two rows per pixel, so this change of variables is not available.

## Where it is used

- **Synthesis**: [dictionary learning](/dictionary-learning/) and K-SVD, sparse coding of patches, [convolutional sparse coding](/convolutional-sparse-coding/), and greedy pursuit methods, which select atoms one by one.
- **Analysis**: total variation and TGV in denoising, deblurring and tomography; $\ell_1$ of a redundant wavelet or curvelet frame in compressed sensing MRI; learned analysis operators and filter based models in [learned regularizers](/bilevel-learning-of-regularizers/).
- **Choice between them**: synthesis is natural when the data are known to be a few atoms, such as spikes or a few frequencies. Analysis is natural when the prior is a set of constraints, such as flat regions or smooth edges, and when the operator is a redundant filter bank.

## References
