---
tag: 2G8JBK
kind: definition
slug: random-field
name: Random field
aliases:
- stochastic field
area: scientific-computing/uncertainty-quantification
level: core
summary: A family of random variables indexed by points in space, given by a mean and a covariance function, used for uncertain material properties.
prereqs: [random-variable, covariance-matrix, positive-definite-matrix]
see_also: [karhunen-loeve-theorem, gaussian-process, kriging, stationary-process, cholesky-decomposition, mercer-theorem, stochastic-galerkin-method, multilevel-monte-carlo]
sources:
  - book: isbn:9780521728522
    title: Gabriel J. Lord, Catherine E. Powell and Tony Shardlow, An Introduction to Computational Stochastic PDEs, Cambridge University Press, 2014
    locator: the chapters on stochastic processes and random fields (second order fields, covariance functions, stationarity, the Matern family, sampling by Cholesky factors, circulant embedding and the Karhunen-Loeve expansion)
  - paper: doi:10.1007/978-1-4612-3094-6
    title: Roger G. Ghanem and Pol D. Spanos, Stochastic Finite Elements. A Spectral Approach, Springer, 1991
    locator: Chapter 2 (the representation of stochastic processes, the Karhunen-Loeve expansion of a random field and its use for uncertain material properties)
  - book: isbn:9780262182539
    title: Carl Edward Rasmussen and Christopher K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006
    locator: Chapter 4 (covariance functions, stationarity and isotropy, the Matern class and mean square differentiability)
---

A random field is a random function of position: at each point $x$ of a domain, its value $a(x)$ is a random variable, and the values at different points are dependent. It is the standard model for a property that is uncertain and changes in space, such as the permeability of rock, the stiffness of a material or the roughness of a surface. A second order random field has a mean function, the expected value at each point, and a covariance function, which says how strongly the values at two points move together. For a Gaussian field these two functions fix the whole law. A model with a random field as input, such as a partial differential equation with a random coefficient, turns into a problem of [forward uncertainty propagation](/forward-uncertainty-propagation/) with infinitely many random inputs.

## Definition

Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space and $D \subseteq \mathbb{R}^n$ a domain. A **random field** on $D$ is a family $\{a(x, \cdot) : x \in D\}$ of real [random variables](/random-variable/) on $\Omega$. For a fixed $\omega \in \Omega$, the function $x \mapsto a(x, \omega)$ is a **realization**, or sample path. For $n = 1$, with $D$ an interval of time, a random field is a stochastic process. The law of a random field is the family of its finite-dimensional distributions, the joint laws of $(a(x_1), \ldots, a(x_m))$ for all finite sets of points.

The field is **second order** if $\mathbb{E}[a(x)^2] < \infty$ for every $x$. It then has a **mean function** and a **covariance function**

$$\bar{a}(x) = \mathbb{E}[a(x)], \qquad C(x, y) = \mathrm{Cov}\big(a(x), a(y)\big).$$

The covariance function is symmetric and positive semidefinite: for all points $x_1, \ldots, x_m$ and reals $c_1, \ldots, c_m$, $\sum_{j,k} c_j c_k C(x_j, x_k) = \mathrm{Var}(\sum_j c_j a(x_j)) \ge 0$. So every matrix $[C(x_j, x_k)]$ is a [covariance matrix](/covariance-matrix/), and it is [positive definite](/positive-definite-matrix/) if no nonzero combination of the values is constant.

The field is **Gaussian** if every finite set of values is jointly normal. For every function $\bar{a}$ and every symmetric positive semidefinite function $C$, there is a Gaussian field with this mean and covariance, by the Kolmogorov extension theorem, and its law is unique. For a field that is not Gaussian, the mean and the covariance do not fix the law.

The field is **stationary** (homogeneous) if $\bar{a}$ is constant and $C(x, y)$ depends only on $x - y$, and **isotropic** if it depends only on the distance $|x - y|$. A common isotropic family is the Matérn covariance with variance $\sigma^2$, correlation length $\ell$ and smoothness $\nu > 0$; it is the exponential $\sigma^2 e^{-r/\ell}$ for $\nu = 1/2$ and $\sigma^2(1 + \sqrt{3}\, r/\ell)e^{-\sqrt{3}\, r/\ell}$ for $\nu = 3/2$, and the field is mean square differentiable $k$ times exactly when $\nu > k$.

If $D$ is compact and $C$ is continuous, the [Mercer theorem](/mercer-theorem/) gives the eigenpairs $(\lambda_k, \phi_k)$ of the covariance operator, and the [Karhunen-Loève theorem](/karhunen-loeve-theorem/) gives the expansion

$$a(x, \omega) = \bar{a}(x) + \sum_{k \ge 1} \sqrt{\lambda_k}\, \phi_k(x)\, \xi_k(\omega),$$

with uncorrelated $\xi_k$ of mean 0 and variance 1, independent standard normal for a Gaussian field, and convergence in mean square, uniform in $x$. Truncating after $K$ terms turns the field into a function of $K$ random variables $\xi_1, \ldots, \xi_K$, which is the form that sampling methods, [stochastic collocation](/stochastic-collocation-method/) and the [stochastic Galerkin method](/stochastic-galerkin-method/) use.

## Examples and non-examples

**Exponential covariance at three points.** Let $C(x, y) = e^{-|x - y|/\ell}$ with $\ell = 1/2$, at the points $0$, $1/2$ and $1$. With $\rho = e^{-1} \approx 0.3679$, the covariance matrix and its [Cholesky factor](/cholesky-decomposition/) are

$$\Sigma = \begin{pmatrix} 1 & \rho & \rho^2 \\ \rho & 1 & \rho \\ \rho^2 & \rho & 1 \end{pmatrix}, \qquad L = \begin{pmatrix} 1 & 0 & 0 \\ \rho & \sqrt{1 - \rho^2} & 0 \\ \rho^2 & \rho\sqrt{1 - \rho^2} & \sqrt{1 - \rho^2} \end{pmatrix},$$

and $a = L z$ with $z$ standard normal in $\mathbb{R}^3$ is a sample of the zero mean Gaussian field at the three points. The last row gives $a_3 = \rho\, a_2 + \sqrt{1 - \rho^2}\, z_3$, so the third value depends on the first only through the second: the exponential covariance in one dimension gives a Markov field, the Ornstein-Uhlenbeck process. On a grid of $m$ points, this sampling costs $O(m^3)$ for the factor; on a regular grid, circulant embedding with the [fast Fourier transform](/fast-fourier-transform/) is much cheaper for stationary fields.

**Brownian motion.** On $D = [0, 1]$, the covariance $C(s, t) = \min(s, t)$ is that of Brownian motion. Its eigenvalues are $\lambda_k = 1/((k - \frac{1}{2})^2\pi^2)$ with eigenfunctions $\sqrt{2}\sin((k - \frac{1}{2})\pi t)$. They add up to $\int_0^1 C(t, t)\, dt = 1/2$, the mean of the variance $t$ over the interval. The field is not stationary, because its variance grows with $t$.

**A lognormal coefficient.** In subsurface flow, the permeability is often modelled as $a(x) = e^{g(x)}$ with $g$ a Gaussian field with Matérn covariance. The field $a$ is positive at every point, as a permeability must be, and it is not Gaussian. A partial differential equation $-\nabla \cdot (a \nabla u) = f$ with this coefficient is a standard test problem for [multilevel Monte Carlo](/multilevel-monte-carlo/) and for stochastic [finite element methods](/finite-element-method/).

**Non-example: a box kernel.** The function $C(x, y) = 1$ if $|x - y| \le 1$ and $0$ otherwise is symmetric, but at the points $0$, $0.6$ and $1.2$ its matrix is $\begin{pmatrix} 1 & 1 & 0 \\ 1 & 1 & 1 \\ 0 & 1 & 1 \end{pmatrix}$, with determinant $-1$. A matrix with a negative determinant has a negative eigenvalue, so this $C$ is not positive semidefinite and is not the covariance of any random field.

**Non-example: white noise.** Gaussian white noise has the formal covariance $\delta(x - y)$, which is not a function. It is not a random field in the sense above, because it has no value at a point; it is a generalized random field, defined only through its integrals against test functions.

**Edge case: independent values.** The covariance $C(x, y) = 1$ for $x = y$ and $0$ otherwise is positive semidefinite, so it defines a Gaussian field with independent values at all points. It satisfies the definition, but $C$ is not continuous, the field is not continuous in mean square, and the Karhunen-Loève expansion does not apply. In geostatistics this is the nugget, added to a continuous covariance to model measurement noise.

## Related definitions

- **Gaussian process.** A [Gaussian process](/gaussian-process/) is a Gaussian random field. The term is more common in statistics and machine learning, where the index set is any input space and the field is a prior over functions in regression; random field is more common in physics and engineering, where the index set is physical space and the field is an uncertain input of a model.
- **Karhunen-Loève theorem.** The [Karhunen-Loève theorem](/karhunen-loeve-theorem/) is a statement about a second order field with continuous covariance on a compact domain: it gives its optimal expansion in the eigenfunctions of $C$. A random field is the object; the theorem gives one representation of it.
- **Stationary process.** A [stationary process](/stationary-process/) is a stationary random field on a one-dimensional index set.
- **Kriging.** [Kriging](/kriging/) predicts a random field at new points from observed values, by the conditional mean of a Gaussian field given the data.
- **Polynomial chaos.** A [polynomial chaos expansion](/polynomial-chaos-expansion/) writes a non-Gaussian field, such as a lognormal one, as a series of orthogonal polynomials in the Gaussian variables $\xi_k$ of its Karhunen-Loève expansion.

## References
