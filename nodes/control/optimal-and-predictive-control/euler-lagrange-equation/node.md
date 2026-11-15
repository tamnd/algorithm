---
tag: ES9AKE
kind: theorem
slug: euler-lagrange-equation
name: Euler-Lagrange equation
aliases:
- Euler-Lagrange equation of the calculus of variations
area: control/optimal-and-predictive-control
level: core
summary: A necessary condition for a curve to extremize an integral of a Lagrangian, the root of the calculus of variations.
prereqs: [optimal-control-problem]
see_also: [pontryagin-maximum-principle, control-hamiltonian, hamiltonian-systems, lagrange-multiplier, transversality-conditions, hamilton-jacobi-bellman-equation, singular-arc]
sources:
  - book: isbn:9780486414485
    title: I. M. Gelfand and S. V. Fomin, Calculus of Variations, Prentice-Hall, 1963 (Dover reprint, 2000)
    locator: Chapter 1 (the simplest variational problem and Euler's equation)
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 2.3.1 (the Euler-Lagrange equation), Section 2.3.2 (historical remarks), Section 2.6.1 (the Legendre condition) and Section 3.1.1 (the Weierstrass-Erdmann corner conditions)
  - paper: "Leonhard Euler, Methodus inveniendi lineas curvas maximi minimive proprietate gaudentes, Bousquet, Lausanne and Geneva, 1744"
---

The Euler-Lagrange equation is the first-order necessary condition of the calculus of variations. If a curve $y(x)$ with fixed end points minimizes or maximizes the integral $\int_a^b L(x, y, y')\, dx$, then $\frac{d}{dx} L_{y'} = L_y$ along the curve. It plays the role that $\nabla F = 0$ plays for a function of finitely many variables. In optimal control it is the special case $\dot x = u$ with no constraint on $u$ of the [Pontryagin maximum principle](/pontryagin-maximum-principle/).

## Statement

Let $L : [a, b] \times \mathbb{R}^n \times \mathbb{R}^n \to \mathbb{R}$, $(x, y, z) \mapsto L(x, y, z)$, be $C^1$. Write $L_y$ and $L_{y'}$ for the gradients of $L$ in its second and third arguments. For $y \in C^1([a, b]; \mathbb{R}^n)$ let

$$J(y) = \int_a^b L(x, y(x), y'(x))\, dx.$$

Fix $A, B \in \mathbb{R}^n$. Suppose $y$ is $C^1$, $y(a) = A$, $y(b) = B$, and $y$ is a weak local minimizer: there is $\varepsilon > 0$ such that $J(y) \le J(\hat y)$ for every $C^1$ curve $\hat y$ with the same end points and $\max_x |\hat y(x) - y(x)| + \max_x |\hat y'(x) - y'(x)| < \varepsilon$.

Then the function $x \mapsto L_{y'}(x, y(x), y'(x))$ is $C^1$ on $[a, b]$, and

$$\frac{d}{dx} L_{y'}(x, y(x), y'(x)) = L_y(x, y(x), y'(x)) \quad \text{for all } x \in [a, b].$$

The same holds for a weak local maximizer. A curve that satisfies the equation is an **extremal**.

## In plain words

Take a curve between two fixed points, and a rule that gives each curve a number, such as the time a bead needs to slide along it. Bend the curve a little, keeping the ends in place. If the curve is the best one, no small bend can make the number smaller, so the first-order change of the number must be zero for every bend. Writing this out gives one differential equation that the best curve must satisfy. It is a necessary condition only: a curve can satisfy it and still not be the best, and in some problems no best curve exists.

## Proof

**Step 1: the first variation is zero.** Let $\eta \in C^1([a, b]; \mathbb{R}^n)$ with $\eta(a) = \eta(b) = 0$. For small $|s|$, the curve $y + s\eta$ has the same end points and lies in the $\varepsilon$ neighborhood, so $g(s) = J(y + s\eta)$ has a local minimum at $s = 0$. Because $L$ is $C^1$ and the integrand is continuous on a compact set, we may differentiate under the integral sign:

$$0 = g'(0) = \int_a^b \left( L_y^T \eta + L_{y'}^T \eta' \right) dx,$$

where $L_y$ and $L_{y'}$ are evaluated along $(x, y(x), y'(x))$, so they are continuous functions of $x$.

**Step 2: remove $\eta$.** Let $G(x) = \int_a^x L_y\, d\xi$. Then $G$ is $C^1$ with $G' = L_y$. Integration by parts, with $\eta(a) = \eta(b) = 0$, gives $\int_a^b L_y^T \eta\, dx = -\int_a^b G^T \eta'\, dx$. So with $h = L_{y'} - G$, a continuous function,

$$\int_a^b h(x)^T \eta'(x)\, dx = 0 \quad \text{for every admissible } \eta.$$

**Step 3: the lemma of du Bois-Reymond.** A continuous $h$ with this property is constant. Proof: let $c = \frac{1}{b - a} \int_a^b h\, dx$ and $\eta(x) = \int_a^x (h - c)\, d\xi$. Then $\eta$ is $C^1$, $\eta(a) = 0$, and $\eta(b) = \int_a^b h\, dx - (b - a) c = 0$, so $\eta$ is admissible. Then

$$\int_a^b |h - c|^2 dx = \int_a^b (h - c)^T \eta'\, dx = \int_a^b h^T \eta'\, dx - c^T (\eta(b) - \eta(a)) = 0.$$

Since $h - c$ is continuous, $h = c$ everywhere.

**Step 4: conclusion.** So $L_{y'} = G + c$. The right side is $C^1$, hence so is the left side, and differentiating gives $\frac{d}{dx} L_{y'} = G' = L_y$. For a maximizer, apply the result to $-L$. $\blacksquare$

The proof does not assume that $y$ has a second derivative. The integrated form $L_{y'} = \int_a^x L_y\, d\xi + c$ of Step 4 is the du Bois-Reymond form of the equation.

## Consequences

**Second-order form.** If $L$ is $C^2$ and $y$ is $C^2$, the chain rule gives

$$L_{y'x} + L_{y'y}\, y' + L_{y'y'}\, y'' = L_y,$$

a second-order differential equation. Where the matrix $L_{y'y'}$ is invertible it can be solved for $y''$, and the two end conditions $y(a) = A$, $y(b) = B$ make it a two-point boundary value problem.

**A hand example.** Minimize $J(y) = \int_0^1 (y'^2 + y^2)\, dx$ with $y(0) = 0$, $y(1) = 1$. The equation is $2 y'' = 2 y$, and the extremal with these end values is $y = \sinh x / \sinh 1$. Integration by parts gives $\int_0^1 y'^2 dx = y(1) y'(1) - \int_0^1 y y''\, dx$, and $y'' = y$, so $J(y) = y(1) y'(1) = \coth 1 \approx 1.31304$. The straight line $y = x$ gives $J = 1 + 1/3 = 4/3 \approx 1.33333$, which is larger. Here $L$ is convex in $(y, y')$, so the extremal is the global minimizer.

**Beltrami identity.** If $L$ does not depend on $x$ and $y$ is $C^2$, then

$$\frac{d}{dx}\left( L - y'^T L_{y'} \right) = y'^T \left( L_y - \frac{d}{dx} L_{y'} \right) = 0,$$

so $L - y'^T L_{y'}$ is constant along every extremal. This is a first integral, and it reduces the order of the equation by one.

**The brachistochrone.** A bead slides without friction from the origin to a lower point under gravity $g$. Measure $y$ downward. The speed at depth $y$ is $\sqrt{2 g y}$, so the travel time is

$$T(y) = \int_0^{x_1} \sqrt{\frac{1 + y'^2}{2 g y}}\, dx.$$

The Lagrangian does not depend on $x$, and the Beltrami identity gives $1/\sqrt{2 g y (1 + y'^2)} = \text{const}$, that is, $y (1 + y'^2) = 2 a$ for a constant $a > 0$. The cycloid $x = a(\theta - \sin\theta)$, $y = a(1 - \cos\theta)$ solves it: $y' = \sin\theta / (1 - \cos\theta)$, so $1 + y'^2 = 2/(1 - \cos\theta)$ and $y(1 + y'^2) = 2a$. Along the cycloid $ds = a\sqrt{2(1 - \cos\theta)}\, d\theta$ and the speed is $\sqrt{2 g a (1 - \cos\theta)}$, so $dt = \sqrt{a/g}\, d\theta$. To reach $(\pi, 2)$ metres, take $a = 1$ and $\theta$ from 0 to $\pi$. The time is $\pi / \sqrt{g} \approx 1.0030$ s for $g = 9.81$ m/s². On the straight line the acceleration along the line is constant, and the time is $\sqrt{\pi^2 + 4} / \sqrt{g} \approx 1.1890$ s.

**Free end point.** If $y(b)$ is free, the same proof with $\eta(b)$ arbitrary gives the natural boundary condition $L_{y'}(b, y(b), y'(b)) = 0$, a first example of the [transversality conditions](/transversality-conditions/).

**Hamiltonian form.** With $p = L_{y'}$ and, where $y'$ can be written as a function of $p$, $H(x, y, p) = p^T y' - L$, the equation becomes the pair $y' = H_p$, $p' = -H_y$ of a [Hamiltonian system](/hamiltonian-systems/).

**Link to optimal control.** Take $\dot x = u$, $u \in \mathbb{R}^n$, and the running cost $L(t, x, u)$. The [control Hamiltonian](/control-hamiltonian/) is $H = L + \lambda^T u$. The minimum condition gives $H_u = L_u + \lambda = 0$, so $\lambda = -L_{\dot x}$, and the costate equation $\dot\lambda = -H_x = -L_x$ is the Euler-Lagrange equation. The [maximum principle](/pontryagin-maximum-principle/) also gives the Weierstrass condition and works for a constrained $u$, where the Euler-Lagrange equation does not apply.

**Constraints.** An integral constraint $\int_a^b M(x, y, y')\, dx = c$ (an isoperimetric problem) gives the Euler-Lagrange equation of $L + \mu M$ for a constant [Lagrange multiplier](/lagrange-multiplier/) $\mu$, if $y$ is not an extremal of the constraint itself.

## Tightness

**Necessary, not sufficient.** Take $J(y) = \int_0^T (y'^2 - y^2)\, dx$ with $y(0) = y(T) = 0$. The curve $y = 0$ satisfies the equation $y'' + y = 0$ for every $T$. For $T > \pi$, the curve $\eta = \sin(\pi x / T)$ gives $J(\eta) = \frac{T}{2}(\pi^2 / T^2 - 1) < 0 = J(0)$, so $y = 0$ is not a minimizer. For $T < \pi$ it is one. The second-order tests, the Legendre condition $L_{y'y'} \ge 0$ along a minimizer and the Jacobi condition on conjugate points, separate the two cases.

**A minimizer need not exist.** Weierstrass's example: $J(y) = \int_{-1}^{1} x^2 y'^2\, dx$ with $y(-1) = -1$, $y(1) = 1$. The curves $y_\varepsilon = \arctan(x/\varepsilon) / \arctan(1/\varepsilon)$ give $J(y_\varepsilon) \to 0$ as $\varepsilon \to 0$. But $J(y) = 0$ forces $y' = 0$ away from $x = 0$, which is not possible with these end values. The equation gives $x^2 y' = c$, so $y = -c/x + d$, and no such curve is $C^1$ on $[-1, 1]$ and meets both end conditions. The theorem says nothing here, because it starts from a minimizer.

**The $C^1$ hypothesis.** Minimize $\int_{-1}^{1} y^2 (1 - y')^2\, dx$ with $y(-1) = 0$, $y(1) = 1$. The curve that is $0$ for $x \le 0$ and $x$ for $x \ge 0$ gives $J = 0$, the smallest possible value, but it has a corner at $x = 0$. No $C^1$ curve gives $J = 0$, so the minimum over $C^1$ curves is not attained. For piecewise $C^1$ curves, the equation holds between corners, and the du Bois-Reymond form shows that $L_{y'}$ is continuous across a corner (the first Weierstrass-Erdmann condition).

## History

Johann Bernoulli posed the brachistochrone problem in 1696, and several solutions, all giving the cycloid, appeared in 1697. Euler derived the general equation in his book *Methodus inveniendi* of 1744, by replacing the curve with a polygon and letting the number of sides grow. In a letter to Euler of 12 August 1755, the young Lagrange gave a direct method: vary the whole curve by $\delta y$ and integrate by parts. Euler adopted it and named the subject the calculus of variations. Legendre, Jacobi and Weierstrass later added the second-order conditions and the rigorous theory. Gelfand and Fomin (1963) and Liberzon (2012, Chapter 2) give modern treatments.

## References
