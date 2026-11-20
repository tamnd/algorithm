---
tag: 90RJYN
kind: definition
slug: sobolev-space
name: Sobolev space
aliases:
- H1 space
area: scientific-computing/finite-element-practice
level: core
summary: The space H^k of functions whose weak derivatives up to order k are square integrable, where weak formulations and error bounds are posed.
prereqs: [weak-formulation]
see_also: [lax-milgram-theorem, cea-lemma, bramble-hilbert-lemma, lagrange-finite-element, finite-element-method, boundary-conditions, poisson-equation]
sources:
  - book: isbn:9780120441433
    title: Robert A. Adams and John J. F. Fournier, Sobolev Spaces, second edition, Academic Press, 2003
    locator: Chapter 3 (the spaces W^{m,p}) and Chapter 4 (the Sobolev imbedding theorem)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, Graduate Studies in Mathematics 19, American Mathematical Society, 2010
    locator: Chapter 5 (weak derivatives, traces, Sobolev inequalities and the Poincaré inequality)
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 1 (weak derivatives, Sobolev norms, Sobolev's inequality, trace theorems) and Chapter 5 (coercivity of variational problems)
---

A Sobolev space $H^k(\Omega)$ is the space of functions on a domain $\Omega$ whose weak derivatives up to order $k$ are all square integrable. It is a Hilbert space, so the [Lax-Milgram theorem](/lax-milgram-theorem/) applies to [weak formulations](/weak-formulation/) posed in it, and its norms and seminorms are the units in which finite element errors are measured. Three facts carry most of the analysis: the trace theorem gives boundary values a meaning, the Poincaré and Friedrichs inequalities give coercivity, and the embedding theorems say when a Sobolev function is continuous.

## Definition

**Weak derivative.** Let $\Omega \subset \mathbb{R}^d$ be open and let $\alpha = (\alpha_1, \ldots, \alpha_d)$ be a multi-index with $|\alpha| = \alpha_1 + \cdots + \alpha_d$. A locally integrable function $g$ is the weak derivative $D^\alpha u$ of a locally integrable $u$ if

$$\int_\Omega u\, D^\alpha\varphi \, dx = (-1)^{|\alpha|} \int_\Omega g\, \varphi \, dx \quad \text{for all } \varphi \in C_c^\infty(\Omega).$$

This is integration by parts with the boundary terms removed by the test function $\varphi$. A weak derivative is unique up to a set of measure zero, and it equals the classical derivative when that exists and is continuous.

**The spaces.** For an integer $k \ge 0$,

$$H^k(\Omega) = \{u \in L^2(\Omega) : D^\alpha u \in L^2(\Omega) \text{ for all } |\alpha| \le k\},$$

with the inner product $(u, v)_k = \sum_{|\alpha| \le k} \int_\Omega D^\alpha u\, D^\alpha v \, dx$, the norm $\|u\|_k = (u, u)_k^{1/2}$ and the seminorm $|u|_k = \bigl(\sum_{|\alpha| = k} \|D^\alpha u\|_0^2\bigr)^{1/2}$. Here $\|\cdot\|_0$ is the $L^2(\Omega)$ norm, and $H^0 = L^2$. With this inner product $H^k(\Omega)$ is complete, so it is a Hilbert space. The space $H^1_0(\Omega)$ is the closure of $C_c^\infty(\Omega)$ in the $\|\cdot\|_1$ norm. The general spaces $W^{k,p}(\Omega)$ use $L^p$ in place of $L^2$, and $H^k = W^{k,2}$.

**Trace theorem.** Let $\Omega$ be bounded with a Lipschitz boundary. There is one bounded linear map $\gamma : H^1(\Omega) \to L^2(\partial\Omega)$ with $\gamma u = u|_{\partial\Omega}$ for every $u \in H^1(\Omega) \cap C(\overline\Omega)$, and

$$\|\gamma u\|_{L^2(\partial\Omega)} \le C \|u\|_1 .$$

So "$u = g$ on $\Gamma_D$" means $\gamma u = g$ almost everywhere on $\Gamma_D$, and $H^1_0(\Omega)$ is the set of $u \in H^1(\Omega)$ with $\gamma u = 0$. The range of $\gamma$ is the smaller space $H^{1/2}(\partial\Omega)$.

**Poincaré and Friedrichs inequalities.** Let $\Omega$ be bounded, connected and Lipschitz, and let $\Gamma_D \subset \partial\Omega$ have positive measure. There are constants with

$$\|v\|_0 \le C_P |v|_1 \ \text{ if } \gamma v = 0 \text{ on } \Gamma_D, \qquad \|v - \bar v\|_0 \le C |v|_1 \ \text{ for all } v \in H^1(\Omega),$$

where $\bar v$ is the mean of $v$ over $\Omega$. Books do not agree on which of the two is named after Poincaré and which after Friedrichs. With either one, $|v|_1$ is a norm equivalent to $\|v\|_1$ on the space in question, and the Dirichlet form $\int \kappa \nabla u\cdot\nabla v$ is coercive there.

**Embedding.** If $\Omega$ is Lipschitz and $k > d/2$, every $u \in H^k(\Omega)$ has a continuous representative and $\max |u| \le C\|u\|_k$. In one dimension this holds for $H^1$, because $|v(x) - v(y)| = |\int_y^x v'| \le |x - y|^{1/2} |v|_1$ by the Cauchy-Schwarz inequality. In two and three dimensions it needs $H^2$. Point values are therefore bounded functionals on $H^1$ only in one dimension, which is why the nodal interpolant $I_h u$ needs $u \in H^2$ in 2D and 3D.

## Examples and non-examples

**The absolute value.** On $(-1, 1)$ the function $u = |x|$ has the weak derivative $\operatorname{sign}(x)$: for every test function, $\int_{-1}^1 |x|\varphi'\,dx = -\int_{-1}^0 x\varphi' + \int_0^1 x\varphi' = \int_{-1}^0 \varphi - \int_0^1 \varphi$ after integration by parts. So $u \in H^1(-1,1)$. It is not in $H^2$, because the derivative of $\operatorname{sign}(x)$ would have to be $2\delta_0$, and that is not a function.

**Non-example: a step.** The Heaviside step $H$ on $(-1,1)$ is not in $H^1$. A weak derivative $g$ would need $\int_{-1}^1 g\varphi = -\int_0^1 \varphi' = \varphi(0)$ for every test function, and no locally integrable $g$ does that. This is why $H^1$-conforming finite element functions must be continuous across element faces: a piecewise polynomial is in $H^1$ if and only if it has no jumps.

**An unbounded function in two dimensions.** On the unit disk let $u(x) = \log\log(2/|x|)$. It is finite on the boundary circle and tends to $+\infty$ at the origin, so it has no continuous representative. With $r = |x|$ and $L = \log(2/r)$ we get $|\nabla u| = 1/(rL)$, and the substitution $t = \log(2/r)$ gives

$$|u|_1^2 = 2\pi \int_0^1 \frac{dr}{r\,\log^2(2/r)} = 2\pi\int_{\log 2}^\infty \frac{dt}{t^2} = \frac{2\pi}{\log 2} \approx 9.065 .$$

Also $u \in L^2$, because $\log\log$ grows more slowly than any power. So $u \in H^1$ of the disk, and $H^1$ in 2D contains unbounded functions.

**Powers of the radius.** On the unit disk, $r^\beta \in H^1$ exactly when $\beta > 0$, because $|\nabla r^\beta|^2 = \beta^2 r^{2\beta - 2}$ and $\int_0^1 r^{2\beta - 1}\,dr$ is finite only for $\beta > 0$. The solution of the Laplace equation near the reentrant corner of an L-shaped domain behaves like $r^{2/3}\sin(2\theta/3)$. It is in $H^1$ but not in $H^2$, since its second derivatives behave like $r^{-4/3}$. This loss of regularity lowers the convergence rate of finite elements on uniform meshes.

**A Poincaré constant you can check.** On $(0, 1)$ with $v(0) = v(1) = 0$ the best constant is $C_P = 1/\pi$, and $v = \sin(\pi x)$ attains it: $\|v\|_0^2 = \tfrac12$ and $|v|_1^2 = \pi^2/2$. For $v = x(1-x)$ we get $\|v\|_0^2 = \tfrac1{30}$ and $|v|_1^2 = \int_0^1 (1-2x)^2\,dx = \tfrac13$, so $\|v\|_0^2/|v|_1^2 = \tfrac1{10}$, just below $1/\pi^2 \approx 0.1013$.

**Non-example: Friedrichs without a boundary condition.** On $H^1(0,1)$ itself the inequality $\|v\|_0 \le C|v|_1$ fails for $v = 1$. The constant functions are exactly what the mean-value form of the inequality removes.

## Related definitions

- **Dual space $H^{-1}(\Omega)$.** The bounded linear functionals on $H^1_0(\Omega)$. The right side $l$ of a second-order [weak formulation](/weak-formulation/) must lie in it. A point load does in 1D and does not in 2D.
- **Fractional spaces $H^s$.** Defined for real $s$ by interpolation or by the Fourier transform. The trace space $H^{1/2}(\partial\Omega)$ and the corner regularity $H^{1+s}$ with $s < 2/3$ are examples.
- **$H(\mathrm{div})$ and $H(\mathrm{curl})$.** Square integrable vector fields with square integrable divergence or curl. They are the spaces of the [Raviart-Thomas](/raviart-thomas-element/) and [Nédélec](/nedelec-element/) elements.
- **Broken Sobolev spaces.** Functions in $H^k$ on each element with no condition across faces. They are the setting of the [discontinuous Galerkin method](/discontinuous-galerkin-method/).
- **Interpolation estimates.** The [Bramble-Hilbert lemma](/bramble-hilbert-lemma/) bounds $|u - I_h u|_m$ by $h^{k+1-m}|u|_{k+1}$, which turns the abstract [Céa lemma](/cea-lemma/) into rates.

## References
