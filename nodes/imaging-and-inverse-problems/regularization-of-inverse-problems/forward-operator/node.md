---
tag: ED73MA
kind: definition
slug: forward-operator
name: Forward operator
aliases:
- forward model
- measurement operator
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: intro
summary: The known map A from the unknown x to the noise-free data in y = A x + e. In linear problems it is a bounded linear operator between Hilbert spaces, with an adjoint A*.
model: real-ram
prereqs: [inverse-problem]
see_also: [singular-value-expansion, pseudoinverse, point-spread-function, radon-transform, back-projection-operator, mri-signal-equation, adjoint-state-method, data-fidelity-term]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 2, Ill-Posed Linear Operator Equations (bounded linear operators between Hilbert spaces and their adjoints)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 3, Discretizations
  - book: isbn:9780387220734
    title: Jari Kaipio and Erkki Somersalo, Statistical and Computational Inverse Problems, Springer, 2005
    locator: Chapter 3, Statistical Inversion Theory (the observation model with its noise)
---

The forward operator of an [inverse problem](/inverse-problem/) is the known map $A$ that sends the unknown $x$ to the data that an ideal, noise-free instrument would record. The full forward model adds the noise: $y = A x + e$. In the linear theory of this sub-area $A: X \to Y$ is a bounded linear operator between Hilbert spaces, and its adjoint $A^*$ is as important as $A$ itself, because every least squares method applies both. The forward operator says nothing about how to invert it; the conditions for a stable inversion are on the page [well-posed problem](/well-posed-problem/), and the spectral description of $A$ is its [singular value expansion](/singular-value-expansion/).

## Definition

Let $X$ (the space of unknowns) and $Y$ (the space of data) be Hilbert spaces. A **forward operator** is a map $F: D(F) \subseteq X \to Y$ such that the data of the experiment are modeled as
$$y = F(x) + e,$$
with $e$ the noise. The problem is **linear** if $F = A$ is linear. In this sub-area a linear forward operator is also assumed **bounded**: there is a constant $C$ with $\|A x\| \le C \|x\|$ for all $x$, and the smallest such $C$ is the norm $\|A\|$. A bounded operator is continuous, which means that the forward problem is stable: a small change of $x$ gives a small change of the data.

The **adjoint** of a bounded $A$ is the unique bounded operator $A^*: Y \to X$ with
$$\langle A x, y \rangle_Y = \langle x, A^* y \rangle_X \quad \text{for all } x \in X,\ y \in Y.$$
Inner products are linear in the second argument, $\langle u, v \rangle = \sum_i \overline{u_i} v_i$ in $\mathbb{C}^n$. For a matrix, $A^* = A^H$, the conjugate transpose. The normal equation $A^* A x = A^* y$ characterizes the least squares solutions.

The aliases name the same object from two sides. "Measurement operator" stresses that $A$ models an instrument. "Forward model" is often used for the whole relation $y = F(x) + e$, including the noise law; then $F$ alone is the forward operator.

**Discretization.** A computer works with an $m \times n$ matrix $A_n$ that approximates $A$: by quadrature on a grid, by projection onto a basis (Galerkin), or by sampling at the detector positions. The discrete operator should keep two properties of the continuous one: its adjoint should be the exact adjoint of the discrete scheme (not a separate discretization of $A^*$), and its singular values should approximate those of $A$.

## Examples and non-examples

**The integration operator.** $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$. Its adjoint is $(A^* y)(t) = \int_t^1 y(s)\,ds$, since both sides of the adjoint identity equal $\iint_{0 \le t \le s \le 1} x(t) y(s)\,dt\,ds$. For $x = y = 1$ both are $\int_0^1 s\,ds = \int_0^1 (1 - t)\,dt = \tfrac12$. Its norm is its largest singular value, $\|A\| = 2/\pi = 0.63662$. The rectangle rule with $h = 1/n$ gives the lower triangular matrix with $h$ on and below the diagonal; for $n = 24$ its largest singular value is $0.64999$.

**Convolution.** A blur with [point spread function](/point-spread-function/) $h$ is $(A x)(s) = \int h(s - t) x(t)\,dt$. Its adjoint is the correlation with $h$, which is the convolution with the flipped and conjugated kernel $\overline{h(-t)}$. With periodic boundary conditions the DFT diagonalizes both (see [convolution theorem](/convolution-theorem/)).

**The Radon transform.** In CT, $A$ maps an image to its line integrals, the [Radon transform](/radon-transform/). Its adjoint is the [back-projection operator](/back-projection-operator/), which smears each line integral back along its line.

**Subsampled Fourier sampling.** In MRI the forward operator is $A = P F S$: multiply by the coil sensitivity $S$, take the Fourier transform $F$, and keep the measured samples $P$ (see [MRI signal equation](/mri-signal-equation/)). Its adjoint is $S^* F^* P^T$, which fills the unmeasured samples with zeros.

**A nonlinear forward operator.** In [phase retrieval](/phase-retrieval/), $F(x) = |\mathcal{F} x|^2$ (the squared magnitude of the Fourier transform). It is a forward operator, but not a linear one. Methods linearize it, and the linear theory applies to the derivative $F'(x)$; the [adjoint-state method](/adjoint-state-method/) computes $F'(x)^*$ for forward operators given by a differential equation.

**Non-example: differentiation.** $D x = x'$ is not a bounded operator on $L^2(0,1)$: $x_k(t) = \sqrt2 \cos(k \pi t)$ has norm 1 and $\|D x_k\| = k\pi$. So it is not a forward operator in the sense above. It is the inverse of one, which is why numerical differentiation is ill posed.

**Non-example: an inexact adjoint.** In CT codes a ray-driven projector is often paired with a pixel-driven back-projector. The pair is not adjoint, and iterative methods that assume $\langle A x, y \rangle = \langle x, A^T y \rangle$ can then fail to converge. A cheap check is the adjoint test: for random $x$ and $y$,
$$\frac{|\langle A x, y \rangle - \langle x, A^* y \rangle|}{\|A x\|\,\|y\|}$$
should be at the level of rounding, about $10^{-15}$ in double precision.

## Related definitions

- [Inverse problem](/inverse-problem/): the task of finding $x$ from $y$; the forward operator is one of its inputs.
- [Singular value expansion](/singular-value-expansion/): for a compact $A$, the expansion $A x = \sum_k \sigma_k \langle v_k, x \rangle u_k$, which explains how $A$ damps each component.
- [Pseudoinverse](/pseudoinverse/): $A^\dagger$ maps $y$ to the minimum norm least squares solution. It is bounded exactly when the range of $A$ is closed.
- [Data fidelity term](/data-fidelity-term/): the misfit $\|A x - y\|^2$ or a negative log-likelihood, built from the forward model and its noise law.
- [Resolution matrix](/resolution-matrix/): the product $R_\alpha A$ of a reconstruction method and the forward operator.

## References
