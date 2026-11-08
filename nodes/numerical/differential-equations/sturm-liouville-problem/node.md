---
tag: 8EC3TP
kind: problem
slug: sturm-liouville-problem
name: Sturm-Liouville problem
aliases:
- Sturm-Liouville eigenvalue problem
- regular Sturm-Liouville problem
area: numerical/differential-equations
level: advanced
summary: "Find the eigenvalues λ and eigenfunctions y of -(p y')' + q y = λ w y with separated boundary conditions. The eigenvalues are real, simple and tend to infinity."
model: real-ram
prereqs: [bvp-boundary-value-problem, shooting-method, finite-differences, rayleigh-quotient]
see_also: [tridiagonal-eigenproblem, courant-fischer-theorem, rayleigh-ritz-method, finite-element-method, spectral-methods, wave-equation, heat-equation, legendre-polynomials]
sources:
  - book: "John D. Pryce, Numerical Solution of Sturm-Liouville Problems, Oxford University Press, 1993"
    locator: theory of the regular problem, Prüfer and scaled Prüfer methods, finite difference and finite element methods with asymptotic correction, coefficient approximation (Pruess) methods
  - book: isbn:9780821839058
    title: Anton Zettl, Sturm-Liouville Theory, American Mathematical Society, 2005
    locator: Chapter 4 (regular problems, existence and properties of eigenvalues), the oscillation theorems, the Prüfer transformation
  - book: "Earl A. Coddington and Norman Levinson, Theory of Ordinary Differential Equations, McGraw-Hill, 1955"
    locator: Chapters 7 and 8 (self-adjoint eigenvalue problems on a finite interval, oscillation and comparison theorems)
  - paper: "John W. Paine, Frank R. de Hoog and Robert S. Anderssen, On the correction of finite difference eigenvalue approximations for Sturm-Liouville problems, Computing 26 (1981) 123-139"
    locator: the O(n^4 h^2) error of difference eigenvalues and its asymptotic correction; doi:10.1007/BF02241779
  - paper: "Paul B. Bailey, W. Norrie Everitt and Anton Zettl, Algorithm 810, The SLEIGN2 Sturm-Liouville code, ACM Transactions on Mathematical Software 27 (2001) 143-192"
    locator: a Prüfer-based code for regular and singular problems; doi:10.1145/383738.383739
---

A Sturm-Liouville problem asks for the values $\lambda$ for which the boundary value problem

$$-(p(x)y')' + q(x)y = \lambda w(x)y, \quad a < x < b, \qquad \alpha_1 y(a) + \alpha_2 p(a)y'(a) = 0, \quad \beta_1 y(b) + \beta_2 p(b)y'(b) = 0$$

has a nonzero solution $y$, and for those solutions. It is the eigenvalue problem of a self-adjoint second-order differential operator. Separation of variables in the [heat](/heat-equation/), [wave](/wave-equation/) and Laplace equations leads to it, and the eigenfunctions are the natural bases for these problems: sines and cosines, Bessel functions, [Legendre polynomials](/legendre-polynomials/) and Hermite functions are all Sturm-Liouville eigenfunctions. Numerically, one either discretizes the operator into a matrix eigenproblem, or shoots on $\lambda$ with an ODE solver and uses the oscillation theory to find the $n$-th eigenvalue directly.

## In plain words

A guitar string fixed at both ends can only vibrate at certain pitches. Each pitch has its own shape: the lowest is a single arch, the next has one still point in the middle, the next has two, and so on. A Sturm-Liouville problem is the general form of this question for a string whose thickness and tension vary along its length.

The theory guarantees that the allowed pitches form an increasing list with no repeats, that the shape for the n-th pitch crosses zero exactly n - 1 times inside, and that the shapes can be combined to build any reasonable function. Computers find the pitches either by turning the string into a chain of beads and solving a matrix problem, or by trying a pitch, following the shape from one end, and counting how often it crosses zero.

## Definition

**The regular problem.** On a finite interval $[a, b]$, $p$, $p'$, $q$ and $w$ are real and continuous, $p > 0$ and $w > 0$ on $[a, b]$, and $(\alpha_1, \alpha_2) \ne (0, 0)$, $(\beta_1, \beta_2) \ne (0, 0)$ are real. A number $\lambda$ is an eigenvalue if the problem has a solution $y \not\equiv 0$, an eigenfunction.

**Theorem (proved in the cited books).** For a regular problem:

1. The eigenvalues are real and form an infinite sequence $\lambda_0 < \lambda_1 < \lambda_2 < \cdots \to \infty$. Each is simple: its eigenfunctions are multiples of one function $y_n$.
2. Eigenfunctions for different eigenvalues are orthogonal in the weighted inner product $\langle u, v\rangle_w = \int_a^b u v w\,dx$, and $\{y_n\}$ is a complete orthogonal system in $L^2_w(a, b)$.
3. **Oscillation (Sturm).** $y_n$ has exactly $n$ zeros in $(a, b)$.
4. **Variational characterization.** With the Rayleigh quotient $R[y] = \big(\int_a^b (p y'^2 + q y^2)\,dx + \text{boundary terms}\big)/\int_a^b w y^2\,dx$, $\lambda_0 = \min R$ and $\lambda_n$ is the min-max over $(n + 1)$-dimensional subspaces ([Courant-Fischer](/courant-fischer-theorem/)).
5. **Asymptotics (Liouville).** $\lambda_n = \big(n\pi/\int_a^b\sqrt{w/p}\,dx\big)^2 + O(1)$ for Dirichlet conditions; $\lambda_n$ grows like $n^2$.

**Prüfer variables.** Write $y = \rho\sin\theta$, $py' = \rho\cos\theta$. Then $\theta$ solves the first-order equation $\theta' = \cos^2\theta/p + (\lambda w - q)\sin^2\theta$, independent of $\rho$. With $\theta(a) = \alpha \in [0, \pi)$ fixed by the left condition, $\theta(b; \lambda)$ is continuous and strictly increasing in $\lambda$, and $\lambda_n$ is the unique solution of $\theta(b; \lambda) = \beta + n\pi$, where $\beta \in (0, \pi]$ comes from the right condition. This gives both the existence and the oscillation statements, and a robust algorithm.

**The computational task.** Given $p$, $q$, $w$, the boundary data and indices $n$, compute $\lambda_n$ (and $y_n$) to a stated accuracy. Errors are absolute or relative errors in $\lambda_n$.

## Variants

- **Periodic conditions** $y(a) = y(b)$, $p(a)y'(a) = p(b)y'(b)$: eigenvalues may be double (for example $\cos nx$ and $\sin nx$).
- **Singular problems.** An infinite interval or a coefficient that vanishes or blows up at an end, such as the Legendre equation on $[-1, 1]$ or the Schrödinger equation $-y'' + V(x)y = \lambda y$ on $\mathbb{R}$. Endpoints are classified as limit point or limit circle (Weyl); there may be continuous spectrum.
- **Eigenparameter in the boundary conditions**, indefinite weight $w$, and higher-order (fourth-order beam) problems.
- **Inverse Sturm-Liouville problems**: recover $q$ from the eigenvalues (Gelfand-Levitan).

## Examples

**The vibrating string.** $-y'' = \lambda y$, $y(0) = y(\pi) = 0$: $\lambda_n = (n + 1)^2$ with $y_n = \sin((n + 1)x)$, which has $n$ interior zeros.

**Robin condition.** $-y'' = \lambda y$ on $[0, 1]$, $y(0) = 0$, $y'(1) + y(1) = 0$. Then $y = \sin(\sqrt\lambda x)$ and the eigenvalues solve $\tan\sqrt\lambda = -\sqrt\lambda$. Prüfer shooting with $\theta(0) = 0$ and target $\theta(1) = \frac{3\pi}{4} + n\pi$ (because $\tan\theta = -1$ at the right end), bisection on $\lambda$ and RK4 with 2000 steps, gives $\lambda_0 = 4.115858$, $\lambda_1 = 24.13934$, $\lambda_2 = 63.6591$, with $\sqrt{\lambda_0} = 2.028758$ (observed; the residuals $\tan\sqrt\lambda + \sqrt\lambda$ are below $10^{-6}$).

**Quantum harmonic oscillator.** $-y'' + x^2y = \lambda y$ on $\mathbb{R}$ (singular, limit point at both ends) has $\lambda_n = 2n + 1$ with Hermite functions. Truncating to $[-L, L]$ with Dirichlet conditions and shooting as above gives $\lambda_0, \dots, \lambda_3 = 1.0000010$, $3.0000292$, $5.0004024$, $7.0033831$ for $L = 4$ and errors below $2 \times 10^{-9}$ for $L = 6$ (observed). The truncation error grows with $n$, because higher eigenfunctions reach farther out.

**Finite differences lose the high eigenvalues.** For $-y'' = \lambda y$ on $[0, \pi]$ with Dirichlet conditions, the three-point scheme on $N$ intervals ($h = \pi/N$) gives the tridiagonal matrix eigenvalues $\frac{4}{h^2}\sin^2\frac{kh}{2}$, $k = 1, \dots, N - 1$, against $k^2$. The errors are:

| $N$ | $k = 1$ | $k = 5$ | $k = 10$ |
|---|---|---|---|
| 20 | 2.05e-3 | 1.26 | 18.9 |
| 40 | 5.14e-4 | 0.320 | 5.04 |
| 80 | 1.29e-4 | 0.0802 | 1.28 |

The error is about $k^4h^2/12$: second order in $h$ but growing like $k^4$, so a mesh gives only its lowest eigenvalues accurately.

## Known algorithms

- **Matrix methods.** [Finite differences](/finite-differences/) give a symmetric tridiagonal (generalized) eigenproblem, solved by the [tridiagonal eigenvalue algorithms](/tridiagonal-eigenproblem/); [finite elements](/finite-element-method/) give a generalized problem $Kc = \lambda Mc$ whose eigenvalues are upper bounds by the [Rayleigh-Ritz](/rayleigh-ritz-method/) principle. Errors grow like $k^4h^2$ (for linear elements and the three-point scheme); the Paine-de Hoog-Anderssen correction removes the leading error of the difference eigenvalues for $q$ smooth.
- **Shooting with Prüfer variables.** Integrate the angle equation for a trial $\lambda$ and compare $\theta(b)$ with $\beta + n\pi$; bisection or a secant method then converges to $\lambda_n$ for any given $n$ (codes SLEIGN and SLEIGN2). Scaled Prüfer variables keep the angle equation nonstiff for large $\lambda$.
- **Coefficient approximation (Pruess) methods.** Replace $p$, $q$, $w$ by piecewise constants and solve each piece exactly with trigonometric or hyperbolic functions; the error is uniform in $n$ (code SLEDGE).
- **Constant perturbation and Magnus methods** (codes MATSLISE): high order, with errors that decrease as $\lambda$ grows.
- **[Spectral methods](/spectral-methods/)**: Chebyshev collocation gives geometric convergence for analytic coefficients, again for the low part of the spectrum.

## Bounds

- **Sturm comparison.** If $q_1 \le q_2$ (or $p_1 \le p_2$) then the $n$-th eigenvalues satisfy $\lambda_n^{(1)} \le \lambda_n^{(2)}$; this follows from the min-max characterization and gives rigorous brackets from simpler problems.
- **Discretization limits.** A matrix of order $N$ has only $N$ eigenvalues, and the three-point eigenvalues are bounded by $4/h^2$ (for $p = w = 1$), so $\lambda_k$ for $k$ near $N$ is never approximated; only $k \ll N^{2/3}$ is accurate to $O(1)$ without correction ($k^4h^2 \lesssim 1$).
- **Conforming finite elements** give $\lambda_k^h \ge \lambda_k$ for every $k$ (min-max), so they are upper bounds.
- **Cost.** A tridiagonal eigenvalue by bisection with Sturm sequences costs $O(N)$ per evaluation, $O(N\log(1/\varepsilon))$ per eigenvalue; Prüfer shooting costs one ODE integration per bisection step.

## Reductions

- **From PDEs by separation of variables.** $u_t = (pu_x)_x - qu$ with $u = e^{-\lambda t}y(x)$, or the wave equation with $u = \cos(\sqrt\lambda t)y(x)$, reduces to the Sturm-Liouville problem; the solution is the eigenfunction expansion of the data.
- **To a matrix eigenproblem.** Discretization gives a symmetric tridiagonal $A$ (with $W$ diagonal), and $W^{-1/2}AW^{-1/2}$ is symmetric.
- **To a two-point boundary value problem.** Add the equation $\lambda' = 0$ and a normalization $\int wy^2 = 1$ (as $z' = wy^2$, $z(a) = 0$, $z(b) = 1$), then use any BVP solver, such as the [shooting method](/shooting-method/).
- **Liouville transformation.** The change of variables $t = \int_a^x\sqrt{w/p}$, $y = (pw)^{-1/4}v$ gives $-v'' + Q(t)v = \lambda v$, which explains the asymptotics and underlies the asymptotic corrections.

## Applications

- **Vibrations and acoustics.** Natural frequencies of strings, rods and columns with variable properties.
- **Quantum mechanics.** Bound states of the one-dimensional Schrödinger equation and radial equations of central potentials.
- **Heat conduction and diffusion** in layered or variable media, by eigenfunction expansion.
- **Special functions and orthogonal polynomials**, defined as eigenfunctions of singular problems.
- **Waveguides, ocean acoustics and seismology** (normal mode computations).

## References
