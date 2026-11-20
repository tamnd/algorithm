---
tag: 7KBZXG
kind: definition
slug: weak-solution-of-conservation-law
name: Weak solution of a conservation law
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: A function that satisfies the conservation law after multiplying by smooth test functions and integrating by parts, which allows shocks.
prereqs: [hyperbolic-conservation-law]
see_also: [rankine-hugoniot-conditions, lax-entropy-condition, lax-wendroff-theorem, weak-formulation, burgers-equation, riemann-problem, entropy-stable-scheme, finite-volume-method]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 11.11 (weak solutions), Section 11.12 (manipulating conservation laws), Section 11.13 (nonuniqueness, admissibility and entropy conditions), Section 11.14 (entropy functions)
  - paper: doi:10.1002/cpa.3160100406
    title: P. D. Lax, Hyperbolic systems of conservation laws II, Communications on Pure and Applied Mathematics 10 (1957) 537-566
    locator: weak solutions of systems, the solution of the Riemann problem, the entropy condition for shocks
  - paper: doi:10.1070/SM1970v010n02ABEH002156
    title: S. N. Kruzkov, First order quasilinear equations in several independent variables, Mathematics of the USSR-Sbornik 10(2) (1970) 217-243
    locator: the entropy inequalities with the entropies |u - k|, existence and uniqueness of the entropy solution for scalar laws
---

A weak solution of a conservation law $u_t + f(u)_x = 0$ is a bounded function, possibly discontinuous, that satisfies the law in integrated form against every smooth test function. The derivatives move from $u$ to the test function, so $u$ needs no derivatives at all. This is the solution concept in which shocks exist. It is the definition that the other pages of this group use. The [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) are what the definition says at a jump. The [Lax entropy condition](/lax-entropy-condition/) is an extra condition, because weak solutions are not unique. The [Lax-Wendroff theorem](/lax-wendroff-theorem/) says that convergent conservative schemes produce weak solutions. The [weak formulation](/weak-formulation/) of finite element methods uses the same idea of test functions for elliptic problems, but there the weak solution has one derivative in $L^2$, and it is unique.

## Definition

Let $f : \mathbb{R}^m \to \mathbb{R}^m$ be continuous and $u_0 \in L^\infty(\mathbb{R})^m$. A function $u \in L^\infty_{\text{loc}}(\mathbb{R} \times [0, \infty))^m$ is a **weak solution** of the initial value problem

$$u_t + f(u)_x = 0, \qquad u(x, 0) = u_0(x),$$

if for every test function $\varphi \in C^1_c(\mathbb{R} \times [0, \infty))$, that is $C^1$ with compact support, which may touch the line $t = 0$,

$$\int_0^\infty\!\!\int_{-\infty}^\infty\big(u\,\varphi_t + f(u)\,\varphi_x\big)\,dx\,dt + \int_{-\infty}^\infty u_0(x)\,\varphi(x, 0)\,dx = 0.$$

A classical $C^1$ solution is a weak solution: multiply the equation by $\varphi$ and integrate by parts. A weak solution that is $C^1$ in an open set satisfies the equation pointwise there, because $\varphi$ can be any function with support in that set. The definition is equivalent to the integral form $\frac{d}{dt}\int_a^bu\,dx = f(u(a, t)) - f(u(b, t))$ in the sense of distributions.

## Examples and non-examples

All examples use [Burgers' equation](/burgers-equation/) $u_t + (u^2/2)_x = 0$ and a function that jumps from $u_L$ to $u_R$ along the line $x = st$.

- **The jump condition.** Split the integral at $x = st$ and integrate by parts on each side, where $u$ is constant. The terms along the line remain, and the definition becomes
$$\int_0^\infty\Big(s(u_R - u_L) - \big(f(u_R) - f(u_L)\big)\Big)\varphi(st, t)\,dt = 0 \quad \text{for every } \varphi.$$
So the jump is a weak solution exactly when $s(u_R - u_L) = f(u_R) - f(u_L)$, the [Rankine-Hugoniot condition](/rankine-hugoniot-conditions/).
- **A shock.** $u_L = 1$, $u_R = 0$, $s = \frac12$. Check: $s(u_R - u_L) = -\frac12$ and $f(u_R) - f(u_L) = 0 - \frac12 = -\frac12$. It is a weak solution, and it is the physical one.
- **A jump at the wrong speed.** The same states with $s = 1$: $-1 \ne -\frac12$. It is not a weak solution.
- **An expansion shock.** $u_L = 0$, $u_R = 1$, $s = \frac12$. Check: $s(u_R - u_L) = \frac12 = f(1) - f(0)$. It is a weak solution, but it is not physical: the characteristics leave the shock.
- **The rarefaction for the same data.** $u = 0$ for $x \le 0$, $u = x/t$ for $0 \le x \le t$, $u = 1$ for $x \ge t$. It is continuous and satisfies the equation where it is smooth, so it is also a weak solution. With the expansion shock, this gives two weak solutions for the same data. In fact there are infinitely many: any jump from $0$ to a value $a \in (0, 1)$ at speed $a/2$, followed by a fan from $a$ to $1$, is one too.
- **A non-example from a different law.** For smooth solutions Burgers' equation is equivalent to $(u^2/2)_t + (u^3/3)_x = 0$. The shock of the second example is not a weak solution of the second law, because it needs $s = \frac{1/3}{1/2} = \frac23$. Weak solutions depend on which quantities are conserved, not only on the smooth equation (LeVeque 2002, Section 11.12).

## Related definitions

- **Entropy solution (scalar laws).** A weak solution such that, for every constant $k$ and every test function $\varphi \ge 0$,
$$\int_0^\infty\!\!\int\big(|u - k|\,\varphi_t + \operatorname{sign}(u - k)(f(u) - f(k))\,\varphi_x\big)\,dx\,dt + \int|u_0 - k|\,\varphi(x, 0)\,dx \ge 0.$$
For a $C^1$ flux and bounded data there is exactly one entropy solution (Kruzkov 1970). For a convex flux, a piecewise smooth weak solution is the entropy solution when every jump satisfies the [Lax entropy condition](/lax-entropy-condition/).
- **Entropy pair.** A convex $\eta(u)$ with a flux $\psi(u)$ such that $\psi' = \eta'f'$. Admissible weak solutions satisfy $\eta(u)_t + \psi(u)_x \le 0$ in the weak sense. The Kruzkov entropies are $\eta = |u - k|$.
- **Systems.** For strictly hyperbolic systems and data with small total variation, Glimm (1965) proved that weak solutions exist, and uniqueness of the admissible solution in that class is known (Bressan 2000). For large data, existence and uniqueness are open in general.
- **Classical solution.** A classical solution is $C^1$. It exists in general only up to the time when the characteristics first cross.

## References
