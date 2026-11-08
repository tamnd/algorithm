---
tag: B7ZX0E
kind: definition
slug: courant-friedrichs-lewy-condition
name: Courant-Friedrichs-Lewy condition
aliases:
- CFL condition
- Courant condition
area: numerical/differential-equations
level: core
summary: The numerical domain of dependence of an explicit scheme must contain the exact one. For 3-point schemes for u_t + a u_x = 0 this is |a| Δt/Δx <= 1. Necessary for convergence, not sufficient.
prereqs: [advection-equation]
see_also: [von-neumann-stability-analysis, lax-equivalence-theorem, upwind-scheme, lax-friedrichs-scheme, lax-wendroff-method, ftcs-method, wave-equation, absolute-stability]
sources:
  - paper: doi:10.1007/BF01448839
    title: R. Courant, K. Friedrichs and H. Lewy, Über die partiellen Differenzengleichungen der mathematischen Physik, Mathematische Annalen 100 (1928) 32-74
    locator: the part on the wave equation, where the convergence of difference schemes is shown to need the mesh ratio condition
  - paper: doi:10.1147/rd.112.0215
    title: R. Courant, K. Friedrichs and H. Lewy, On the partial difference equations of mathematical physics, IBM Journal of Research and Development 11 (1967) 215-234 (English translation of the 1928 paper)
    locator: the domain of dependence argument for hyperbolic equations
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (advection equations; the section on the CFL condition and the domain of dependence)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 4 (finite volume methods; the section on the CFL condition)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (hyperbolic equations, the Courant-Friedrichs-Lewy condition) and Chapter 2 (von Neumann analysis)
---

The Courant-Friedrichs-Lewy (CFL) condition says that an explicit finite difference scheme for a hyperbolic PDE can converge only if its numerical domain of dependence contains the domain of dependence of the PDE. For the [advection equation](/advection-equation/) $u_t + a u_x = 0$ and a scheme that uses the three neighbours $x_{j-1}, x_j, x_{j+1}$, it is the bound $|a|\,\Delta t/\Delta x \le 1$ on the Courant number. Courant, Friedrichs and Lewy found it in 1928. It is a necessary condition only: a scheme that satisfies it can still be unstable, and the full stability analysis is [von Neumann analysis](/von-neumann-stability-analysis/) or an energy estimate.

## Definition

**Notation.** The PDE is for $u(x, t)$, the mesh is $x_j = j\Delta x$, $t_n = n\Delta t$, and $U_j^n \approx u(x_j, t_n)$. For $u_t + a u_x = 0$ the **Courant number** is $\nu = a\Delta t/\Delta x$; for a system $u_t + Bu_x = 0$ with real eigenvalues $\lambda_p$ of $B$ it is $\max_p |\lambda_p|\Delta t/\Delta x$.

**Domains of dependence.** The exact solution of $u_t + au_x = 0$ is $u(x, t) = u_0(x - at)$, so $u(X, T)$ depends only on the initial data at the point $X - aT$. For a hyperbolic system, $u(X, T)$ depends on the data in the interval spanned by the points $X - \lambda_p T$. Consider an explicit one-level scheme
$$U_j^{n+1} = \sum_{k=-l}^{r} c_k\, U_{j+k}^n$$
with $l, r \ge 0$. By induction on $n$, $U_j^n$ depends only on $U^0_i$ for $j - ln \le i \le j + rn$. With $X = x_j$ and $T = t_n$ this is the **numerical domain of dependence** $[X - lT\Delta x/\Delta t,\; X + rT\Delta x/\Delta t]$.

**The CFL condition.** As $\Delta x, \Delta t \to 0$ with $\Delta t/\Delta x$ fixed, the numerical domain of dependence of each point $(X, T)$ contains its exact domain of dependence. For the scheme above and $u_t + au_x = 0$ this reads
$$-r \le \nu = \frac{a\Delta t}{\Delta x} \le l.$$

**Theorem (Courant, Friedrichs and Lewy, 1928).** If the CFL condition fails, the scheme does not converge for all smooth initial data.

*Proof.* Fix $\Delta t/\Delta x = \mu$ and suppose, say, $a\mu > l$ (the case $a\mu < -r$ is symmetric). Fix $T > 0$ and a point $X$ that is a grid point for a sequence of meshes. Then $X - aT < X - lT/\mu$, so the point $X - aT$ lies outside the interval $I = [X - lT/\mu, X + rT/\mu]$, which does not depend on the mesh. Choose a smooth bump $\phi$ with $\phi(X - aT) = 1$ and support disjoint from $I$. For the data $u_0$ and $u_0 + \phi$ the scheme computes the same $U^n_j$ at $(X, T)$ on every mesh of the sequence, because it uses only data in $I$. The exact values differ by $\phi(X - aT) = 1$. So the scheme cannot converge to the exact value at $(X, T)$ for both data. $\square$

**What the condition says about specific schemes.**

- Upwind for $a > 0$, $U_j^{n+1} = U_j^n - \nu(U_j^n - U_{j-1}^n)$: $l = 1$, $r = 0$, so the condition is $0 \le \nu \le 1$. Here it is also sufficient: for $0 \le \nu \le 1$ the new value is a convex combination of old values, so $\max_j |U_j^n|$ never grows.
- Lax-Friedrichs and [Lax-Wendroff](/lax-wendroff-method/): $l = r = 1$, so $|\nu| \le 1$, which is also their von Neumann stability condition.
- Leapfrog for the [wave equation](/wave-equation/) $u_{tt} = c^2u_{xx}$: $c\Delta t/\Delta x \le 1$.
- An implicit scheme couples all grid points in each step, so its numerical domain of dependence is the whole line, and the condition holds for every $\Delta t$.
- In two dimensions with mesh widths $\Delta x$ and $\Delta y$, the dimension-by-dimension upwind scheme needs $|a|\Delta t/\Delta x + |b|\Delta t/\Delta y \le 1$.

## Examples and non-examples

**Upwind, inside and outside the condition.** Solve $u_t + u_x = 0$ on $[0, 1]$ with periodic boundary, $u_0(x) = \sin 2\pi x$ and $\Delta x = 0.01$, with the upwind scheme. The maximum error over the grid, in the max norm, is:

| $\nu$ | after 50 steps | after 100 steps | after 200 steps |
|---|---|---|---|
| 0.8 | 0.0157 | 0.0311 | 0.0612 |
| 1.0 | $7 \cdot 10^{-16}$ | $7 \cdot 10^{-16}$ | $2 \cdot 10^{-15}$ |
| 1.2 | 0.0240 | 0.0627 | $1.06 \cdot 10^{13}$ |

At $\nu = 1$ the scheme is $U_j^{n+1} = U_{j-1}^n$, which is exact. At $\nu = 1.2$ the smooth mode is still accurate for a while, but the amplification factor of the shortest mode is $|1 - 2\nu| = 1.4$, so rounding errors in that mode grow by $1.4$ per step and destroy the solution.

**Non-example: CFL holds, but the scheme is unstable.** Forward time, centered space (FTCS), $U_j^{n+1} = U_j^n - \tfrac{\nu}{2}(U_{j+1}^n - U_{j-1}^n)$, has $l = r = 1$ and so satisfies CFL for $|\nu| \le 1$. Its amplification factor is $g(\theta) = 1 - i\nu\sin\theta$ with $|g|^2 = 1 + \nu^2\sin^2\theta > 1$, so it is unstable for every $\nu \ne 0$. In the experiment above with $\nu = 0.5$ the error is $0.051$ after 100 steps and $10^{32}$ after 1000 steps.

**Non-example: downwind differencing.** For $a > 0$, $U_j^{n+1} = U_j^n - \nu(U_{j+1}^n - U_j^n)$ has $l = 0$, $r = 1$, and the condition $-1 \le \nu \le 0$ fails for every $\nu > 0$. It never converges, whatever $\Delta t$.

**The heat equation.** For $u_t = \kappa u_{xx}$ the exact domain of dependence is the whole line. An explicit scheme satisfies the CFL condition only in the limit $\Delta t/\Delta x \to 0$. The stability bound of FTCS for this equation, $\kappa\Delta t/\Delta x^2 \le 1/2$, is stronger and implies it.

## Related definitions

- **[Von Neumann stability analysis](/von-neumann-stability-analysis/).** A necessary and sufficient test, in the $\ell^2$ norm, for linear constant-coefficient schemes with periodic data. CFL is a quick necessary check.
- **[Lax equivalence theorem](/lax-equivalence-theorem/).** A consistent scheme for a well-posed linear problem converges if and only if it is stable. CFL is a necessary condition for that stability.
- **[Absolute stability](/absolute-stability/).** In the [method of lines](/method-of-lines/), the eigenvalues of the semi-discrete operator scale like $|a|/\Delta x$, and the time-stepping method needs $\Delta t$ times them inside its stability region. This gives a CFL-type bound $\Delta t \le C\Delta x/|a|$ with a constant $C$ that depends on the time integrator.
- **CFL number.** In practice the Courant number $\nu$ itself is often called the CFL number, and codes choose $\Delta t$ from a target value such as $\nu = 0.9$.

## References
