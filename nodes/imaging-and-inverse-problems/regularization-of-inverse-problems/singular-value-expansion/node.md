---
tag: YJYKG7
kind: concept
slug: singular-value-expansion
name: Singular value expansion
aliases:
- singular system of a compact operator
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "A compact operator A has a singular system (sigma_k; v_k, u_k) with A v_k = sigma_k u_k, A* u_k = sigma_k v_k and sigma_k decreasing to 0, so A x = sum of sigma_k <v_k, x> u_k."
model: real-ram
prereqs: [forward-operator, singular-value-decomposition, spectral-theorem]
see_also: [picard-condition, pseudoinverse, degree-of-ill-posedness, spectral-filter-factors, truncated-svd, fredholm-integral-equation-first-kind, galerkin-method, principal-component-analysis]
sources:
  - paper: doi:10.1007/BF01449770
    title: Erhard Schmidt, Zur Theorie der linearen und nichtlinearen Integralgleichungen, Mathematische Annalen 63(4), 1907, 433 to 476
    locator: the expansion of an integral operator with a non-symmetric kernel in pairs of eigenfunctions, and the best approximation by finite sums
  - paper: doi:10.1137/1035134
    title: G. W. Stewart, On the early history of the singular value decomposition, SIAM Review 35(4), 1993, 551 to 566
    locator: the section on Schmidt (the extension to function spaces and the approximation theorem)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 2, Ill-Posed Linear Operator Equations (the singular system of a compact operator and the expansion of the generalized inverse)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 2 (the SVD and its generalizations, and the computation of the SVE by discretization)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 2, Meet the Fredholm Integral Equation of the First Kind (the SVE and its properties)
---

The singular value expansion (SVE) writes a compact operator $A: X \to Y$ between Hilbert spaces as $A x = \sum_k \sigma_k \langle v_k, x \rangle u_k$, with orthonormal systems $(v_k)$ in $X$ and $(u_k)$ in $Y$ and positive numbers $\sigma_k$ that decrease to zero. It is the [singular value decomposition](/singular-value-decomposition/) of a matrix carried over to operators, and it was found first, by Erhard Schmidt in 1907, for integral operators. For inverse problems it is the main tool of analysis: it shows which components of the unknown the [forward operator](/forward-operator/) damps and by how much, it gives the [Picard condition](/picard-condition/) for existence, and it is the base of every spectral regularization method. It is a theoretical device; in computation it is approximated by the SVD of a discretized operator.

## In plain words

Think of the forward operator as a machine with many channels. Each channel takes one special input pattern and turns it into one special output pattern, scaled by a number, the gain of the channel. The patterns of different channels do not mix. Any input is a sum of input patterns, so the machine just scales each part by its gain. For a smoothing machine the gains get smaller and smaller as the patterns wiggle faster, and they go to zero. To undo the machine you divide each output part by its gain. For the fast channels that means dividing by a tiny number, and any noise in those channels becomes huge. The list of gains tells you at a glance how hard the inverse problem is.

## The idea

**The statement.** Let $A: X \to Y$ be a compact linear operator between Hilbert spaces. Then there are numbers $\sigma_1 \ge \sigma_2 \ge \cdots > 0$, an orthonormal system $(v_k)$ in $X$ and an orthonormal system $(u_k)$ in $Y$ such that
$$A v_k = \sigma_k u_k, \qquad A^* u_k = \sigma_k v_k,$$
$$A x = \sum_k \sigma_k \langle v_k, x \rangle u_k, \qquad A^* y = \sum_k \sigma_k \langle u_k, y \rangle v_k.$$
The triple $(\sigma_k; v_k, u_k)$ is the **singular system** of $A$. The sums are finite if the range of $A$ has finite dimension. Otherwise the system is infinite and $\sigma_k \to 0$. The $v_k$ span the closure of $N(A)^\perp$ and the $u_k$ span the closure of $R(A)$. Each $\sigma_k$ is repeated as often as its multiplicity, which is finite.

**Where it comes from.** $A^* A$ is compact, self-adjoint and positive. The [spectral theorem](/spectral-theorem/) for such operators gives an orthonormal system of eigenvectors $v_k$ with eigenvalues $\lambda_k > 0$ that tend to zero, and $A^* A$ is zero on the rest. Put $\sigma_k = \sqrt{\lambda_k}$ and $u_k = A v_k/\sigma_k$. Then $\langle u_j, u_k \rangle = \langle v_j, A^* A v_k \rangle/(\sigma_j \sigma_k) = \sigma_k^2 \langle v_j, v_k \rangle/(\sigma_j \sigma_k)$, which is $1$ for $j = k$ and $0$ otherwise. And $A^* u_k = A^* A v_k/\sigma_k = \sigma_k v_k$.

**The generalized inverse.** For $y$ in the domain of the [pseudoinverse](/pseudoinverse/),
$$A^\dagger y = \sum_k \frac{\langle u_k, y \rangle}{\sigma_k}\, v_k.$$
The factor $1/\sigma_k$ grows without bound. This is the instability of the problem in one formula: a data error $e = \delta u_k$ of norm $\delta$ causes the solution error $(\delta/\sigma_k) v_k$. The series converges exactly when $\sum_k |\langle u_k, y \rangle|^2/\sigma_k^2 < \infty$, which is the [Picard condition](/picard-condition/).

**Filters.** Every linear regularization method in this sub-area replaces $1/\sigma_k$ by a bounded function: $x_\alpha = \sum_k f_\alpha(\sigma_k)\, \frac{\langle u_k, y \rangle}{\sigma_k}\, v_k$. The [spectral filter factors](/spectral-filter-factors/) $f_\alpha$ define [truncated SVD](/truncated-svd/), Tikhonov regularization and Landweber iteration.

**Hilbert-Schmidt operators.** For an integral operator with kernel $K \in L^2$, $\sum_k \sigma_k^2 = \|K\|_{L^2}^2$. So the singular values are square summable, and since they decrease, $\sigma_k = o(k^{-1/2})$. The speed of the decay is the [degree of ill-posedness](/degree-of-ill-posedness/).

**The SVE and the SVD.** A matrix is a compact operator on finite-dimensional spaces, so the SVD $A = \sum_{i=1}^r \sigma_i u_i v_i^H$ is the special case. A discretization $A_n$ of $A$ has an SVD whose first singular values and vectors approximate those of the SVE. For a Galerkin discretization with orthonormal bases, $\sigma_k(A_n) \le \sigma_k(A)$, with convergence as the bases grow. This is how the SVE is computed in practice.

**Schmidt's approximation theorem.** The truncated sum $A_k = \sum_{i \le k} \sigma_i \langle v_i, \cdot \rangle u_i$ is the best approximation of $A$ by an operator of rank at most $k$ in the operator norm, with error $\sigma_{k+1}$. For matrices this is the Eckart-Young theorem, and it is the reason why truncation is the natural first regularization.

## Examples

**The integration operator.** $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$ has the singular system
$$\sigma_k = \frac{2}{(2k-1)\pi}, \qquad v_k(t) = \sqrt2 \cos\big((k - \tfrac12)\pi t\big), \qquad u_k(s) = \sqrt2 \sin\big((k - \tfrac12)\pi s\big).$$
Check with $w = (k - \tfrac12)\pi$: $\int_0^s \sqrt2 \cos(w t)\,dt = \sqrt2 \sin(w s)/w = \sigma_k u_k(s)$. The adjoint is $(A^* y)(t) = \int_t^1 y(s)\,ds$, and $\int_t^1 \sqrt2 \sin(w s)\,ds = \sqrt2 (\cos(w t) - \cos w)/w = \sigma_k v_k(t)$ because $\cos w = 0$. The first values are $0.63662$, $0.21221$, $0.12732$, $0.09095$ and $0.07074$.

The rectangle-rule matrix with $h = 1/n$ on and below the diagonal has the exact singular values $\sigma_k = 1/(2n \sin((2k-1)\pi/(4n+2)))$, which tend to $2/((2k-1)\pi)$ as $n \to \infty$. For $n = 24$:

| $k$ | matrix, $n = 24$ | operator |
|---|---|---|
| 1 | 0.64999 | 0.63662 |
| 2 | 0.21696 | 0.21221 |
| 3 | 0.13053 | 0.12732 |
| 4 | 0.09362 | 0.09095 |

The first values agree to about 2 percent. The last one, $\sigma_{24} = 0.02088$, is the matrix's version of the tail; the operator's values go on to zero.

**A symmetric kernel.** The kernel $K(s,t) = s(1-t)$ for $s \le t$ and $t(1-s)$ for $s > t$ on $(0,1)^2$ is the Green's function of $-x''$ with zero boundary values. It is self-adjoint with eigenfunctions $\sqrt2 \sin(k\pi t)$ and eigenvalues $1/(k\pi)^2$. For a positive self-adjoint operator the SVE is the eigenvalue expansion, with $u_k = v_k$.

**Periodic convolution.** On functions of period 1, convolution with $h$ maps $e^{2\pi i k t}$ to $\hat h_k e^{2\pi i k t}$. The singular values are the numbers $|\hat h_k|$ in decreasing order, $v_k$ is the Fourier mode, and $u_k$ is the same mode times the phase of $\hat h_k$.

**The backward heat equation.** The map from $u(\cdot, 0)$ to $u(\cdot, T)$ for $u_t = u_{xx}$ on $(0,1)$ with zero boundary values has $\sigma_k = \exp(-k^2 \pi^2 T)$ and $u_k = v_k = \sqrt2 \sin(k\pi x)$. With $T = 0.01$: $\sigma_1 = 0.906$, $\sigma_5 = 0.0848$, $\sigma_{10} = 5.17 \times 10^{-5}$.

## Where it is used

- To classify an inverse problem by the decay of $\sigma_k$ ([degree of ill-posedness](/degree-of-ill-posedness/)).
- To decide whether data are consistent ([Picard condition](/picard-condition/)), and in discrete form to read a Picard plot.
- To define and analyze spectral regularization: [truncated SVD](/truncated-svd/), Tikhonov, Landweber, and their [resolution matrices](/resolution-matrix/).
- To prove convergence rates under a [source condition](/source-condition/) $x^\dagger = (A^* A)^\nu w$, which in the singular system reads $\langle v_k, x^\dagger \rangle = \sigma_k^{2\nu} \langle v_k, w \rangle$.
- In statistics as the Karhunen-Loeve expansion of a random field, which is the SVE of its covariance operator, and in finite dimension as [principal component analysis](/principal-component-analysis/).

## References
