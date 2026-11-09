---
tag: T7BDP6
kind: theorem
slug: fenchel-duality
name: Fenchel duality
aliases:
- Fenchel-Rockafellar duality
- Fenchel's duality theorem
area: optimization/convex-optimization
level: advanced
summary: "inf f(x) + g(Ax) equals sup -f*(A^T y) - g*(-y), with the dual attained, when f and g are convex and some x in dom f has Ax in the interior of dom g."
prereqs: [convex-conjugate, supporting-hyperplane-theorem, subgradient]
see_also: [lagrangian-duality, lp-duality, strong-duality, weak-duality, slater-condition, minimax-theorem, lasso-regression, convex-envelope]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 31, Fenchel's duality theorem (the general form with a linear map, relative interior and polyhedral conditions)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter E, Conjugacy in convex analysis (conjugate of a sum and of a composition with a linear map)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 4, Conjugate functions (Fenchel's duality theorem and examples)
  - paper: "Werner Fenchel, On conjugate convex functions, Canadian Journal of Mathematics 1, 1949, 73-77"
    locator: the duality theorem for the difference of a convex and a concave function
  - paper: "R. Tyrrell Rockafellar, Extension of Fenchel's duality theorem for convex functions, Duke Mathematical Journal 33, 1966, 81-89"
    locator: the form with a linear map between the two functions
---

Fenchel duality pairs the problem of minimizing $f(x) + g(Ax)$, with $f$ and $g$ convex and $A$ a matrix, with a problem in the [convex conjugates](/convex-conjugate/) $f^*$ and $g^*$. The dual value is never above the primal value, and the two are equal, with a dual solution, when some point of the domain of $f$ maps into the interior of the domain of $g$. The theorem contains [LP duality](/lp-duality/) and the conjugate form of [Lagrangian duality](/lagrangian-duality/) as special cases, and its optimality conditions give closed forms for many proximal and shrinkage steps.

## Statement

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ and $g : \mathbb{R}^m \to \mathbb{R} \cup \{+\infty\}$ be proper [convex functions](/convex-function/), and let $A$ be an $m \times n$ matrix. Define

$$p^* = \inf_{x \in \mathbb{R}^n} \big( f(x) + g(Ax) \big), \qquad d^* = \sup_{y \in \mathbb{R}^m} \big( -f^*(A^T y) - g^*(-y) \big).$$

**Theorem 1 (weak duality).** $d^* \le p^*$.

**Theorem 2 (strong duality).** Suppose there is $x_0 \in \operatorname{dom} f$ with $A x_0 \in \operatorname{int} \operatorname{dom} g$, and $p^*$ is finite. Then $d^* = p^*$, and the supremum in $d^*$ is attained.

**Theorem 3 (optimality conditions).** Let $x^* \in \operatorname{dom} f$ with $A x^* \in \operatorname{dom} g$, and let $y^* \in \mathbb{R}^m$. Then $x^*$ attains $p^*$, $y^*$ attains $d^*$ and $p^* = d^*$, if and only if

$$A^T y^* \in \partial f(x^*) \quad \text{and} \quad -y^* \in \partial g(A x^*).$$

With $A = I$ and $g = -h$ for a concave $h$, Theorems 1 and 2 give Fenchel's original form: $\inf (f - h) = \max (h_* - f^*)$, where $h_*(y) = \inf_x (y^T x - h(x))$ is the concave conjugate.

## In plain words

Some problems ask for the lowest point of a sum of two bowl-shaped costs. Each cost can be described by the straight lines that stay below it, and the slopes of these lines give a second problem. In the second problem we choose one slope, and each cost gives the best lower line with that slope.

Any choice of slope gives a lower bound on the first problem. The theorem says that the best lower bound is exact, and that a best slope exists, when the two costs overlap in a sufficiently large region. At an optimal pair, the chosen slope touches both costs at the solution, so a solution of either problem tells us the solution of the other one.

## Proof

### Theorem 1

Let $x \in \operatorname{dom} f$ with $Ax \in \operatorname{dom} g$, and let $y \in \mathbb{R}^m$. The conjugates of proper functions never take the value $-\infty$. By the Fenchel-Young inequality (Theorem 2 on the [convex conjugate](/convex-conjugate/) page),

$$f(x) + f^*(A^T y) \ge (A^T y)^T x = y^T A x, \qquad g(Ax) + g^*(-y) \ge -y^T A x.$$

Add the two inequalities: $f(x) + g(Ax) \ge -f^*(A^T y) - g^*(-y)$. Take the infimum over $x$ and the supremum over $y$. If no $x$ is feasible, $p^* = +\infty$ and there is nothing to prove. $\square$

### Theorem 2

Define the *value function*

$$v(u) = \inf_{x} \big( f(x) + g(Ax + u) \big), \qquad u \in \mathbb{R}^m,$$

so that $v(0) = p^*$. The proof shows that $v$ has a subgradient at 0, and that minus this subgradient solves the dual.

*Step 1: $v$ is convex.* Let $\theta \in [0, 1]$, let $\alpha_1 > v(u_1)$ and $\alpha_2 > v(u_2)$. Pick $x_i$ with $f(x_i) + g(A x_i + u_i) < \alpha_i$. Put $x = \theta x_1 + (1 - \theta) x_2$ and $u = \theta u_1 + (1 - \theta) u_2$. Then $Ax + u = \theta (A x_1 + u_1) + (1 - \theta)(A x_2 + u_2)$, and convexity of $f$ and $g$ gives

$$v(u) \le f(x) + g(Ax + u) < \theta \alpha_1 + (1 - \theta) \alpha_2. \tag{1}$$

This is the convexity of the epigraph of $v$, and it also holds when a value of $v$ is $-\infty$.

*Step 2: $v$ is bounded above near 0.* Since $A x_0 \in \operatorname{int} \operatorname{dom} g$, there is $\delta > 0$ such that the $2m$ points $A x_0 \pm \delta e_i$ are in $\operatorname{dom} g$. Let $M$ be the largest value of $g$ at these points. Then $g(A x_0) \le M$, since $A x_0$ is the midpoint of $A x_0 \pm \delta e_1$. If $\lVert u \rVert_1 \le \delta$, then

$$A x_0 + u = \sum_{i=1}^m \frac{\lvert u_i \rvert}{\delta} \big( A x_0 + \operatorname{sign}(u_i)\, \delta e_i \big) + \Big( 1 - \frac{\lVert u \rVert_1}{\delta} \Big) A x_0$$

is a convex combination of points where $g \le M$, so $g(A x_0 + u) \le M$ by [Jensen's inequality](/jensens-inequality/). So $v(u) \le f(x_0) + M$ on the set $U = \{ u : \lVert u \rVert_1 \le \delta \}$, which contains a ball around 0.

*Step 3: $v$ is proper.* Suppose $v(u_1) = -\infty$ for some $u_1$. Choose $t > 0$ with $-t u_1 \in U$. Then $0 = \frac{t}{1+t} u_1 + \frac{1}{1+t} (-t u_1)$. In (1), take $\alpha_2 = f(x_0) + M + 1$ and let $\alpha_1 \to -\infty$. This gives $v(0) = -\infty$, which contradicts the finiteness of $p^*$. So $v$ takes values in $\mathbb{R} \cup \{+\infty\}$, it is finite on $U$, and $0 \in \operatorname{int} \operatorname{dom} v$.

*Step 4: a subgradient.* By Theorem 1 on the [subgradient](/subgradient/) page, which rests on the [supporting hyperplane theorem](/supporting-hyperplane-theorem/), there is $s \in \mathbb{R}^m$ with $v(u) \ge v(0) + s^T u$ for all $u$. Let $x \in \operatorname{dom} f$ and $z \in \operatorname{dom} g$, and put $u = z - Ax$. Then $f(x) + g(z) \ge v(z - Ax) \ge p^* + s^T z - s^T A x$, that is,

$$\big( f(x) + s^T A x \big) + \big( g(z) - s^T z \big) \ge p^*.$$

The two brackets depend on $x$ and on $z$ separately. Their infima are $-f^*(-A^T s)$ and $-g^*(s)$. Put $y = -s$:

$$-f^*(A^T y) - g^*(-y) \ge p^*.$$

So $d^* \ge p^*$, the point $y$ attains it, and Theorem 1 gives equality. $\square$

### Theorem 3

For $x$ and $y$ as in the statement, write the gap as two parts:

$$\big( f(x) + g(Ax) \big) - \big( -f^*(A^T y) - g^*(-y) \big) = \big[ f(x) + f^*(A^T y) - y^T A x \big] + \big[ g(Ax) + g^*(-y) + y^T A x \big].$$

By Fenchel-Young, each bracket is $\ge 0$, and it is 0 if and only if $A^T y \in \partial f(x)$, respectively $-y \in \partial g(Ax)$. If both conditions hold, the gap is 0, so the primal value at $x^*$ equals the dual value at $y^*$, and Theorem 1 shows that both are optimal and $p^* = d^*$. Conversely, if $x^*$ and $y^*$ are optimal and $p^* = d^*$, the gap is 0, so both brackets are 0. $\square$

## Consequences

### Example: soft thresholding

Let $f(x) = \frac{1}{2} \lVert x - a \rVert_2^2$, $g(x) = \lambda \lVert x \rVert_1$ with $\lambda > 0$, and $A = I$. This is the step of the [proximal operator](/proximal-operator/) of the $\ell_1$ norm, and the core of the [lasso](/lasso-regression/). The conjugates are

$$f^*(w) = \tfrac{1}{2} \lVert w \rVert_2^2 + a^T w, \qquad g^*(z) = \begin{cases} 0 & \lVert z \rVert_\infty \le \lambda, \\ +\infty & \text{otherwise.} \end{cases}$$

The dual is $\max_{\lVert y \rVert_\infty \le \lambda} \big( \frac{1}{2} \lVert a \rVert_2^2 - \frac{1}{2} \lVert y + a \rVert_2^2 \big)$, so $y^*$ is the projection of $-a$ onto the box, $y^*_i = \min(\max(-a_i, -\lambda), \lambda)$. The condition $y^* = \nabla f(x^*) = x^* - a$ of Theorem 3 gives $x^* = a + y^*$, which is the soft-threshold formula $x^*_i = \operatorname{sign}(a_i) \max(\lvert a_i \rvert - \lambda, 0)$. The domain of $g$ is all of $\mathbb{R}^n$, so Theorem 2 applies.

With $a = (3, -\frac{1}{2}, \frac{6}{5})$ and $\lambda = 1$:

| | coordinate 1 | coordinate 2 | coordinate 3 | value |
| --- | --- | --- | --- | --- |
| $y^*$ | $-1$ | $\frac{1}{2}$ | $-1$ | $d^* = \frac{5}{2} + \frac{1}{8} + \frac{7}{10} = \frac{133}{40}$ |
| $x^* = a + y^*$ | $2$ | $0$ | $\frac{1}{5}$ | $p^* = \frac{9}{8} + \frac{11}{5} = \frac{133}{40}$ |

So $p^* = d^* = 3.325$. The condition $-y^* = (1, -\frac{1}{2}, 1) \in \partial \lVert \cdot \rVert_1 (x^*)$ holds: the entries are the signs of the nonzero entries $2$ and $\frac{1}{5}$, and $-\frac{1}{2} \in [-1, 1]$ for the zero entry. A script checked both values in exact arithmetic, and a brute-force minimum and maximum over a grid of step $\frac{1}{20}$ in each coordinate gave the same number $\frac{133}{40}$.

### LP duality

Take $f(x) = c^T x$ for $x \ge 0$ and $+\infty$ otherwise, and $g(z) = 0$ for $z \ge b$ and $+\infty$ otherwise. Then $p^*$ is the linear program $\min \{ c^T x : Ax \ge b,\ x \ge 0 \}$. The conjugates are $f^*(w) = 0$ if $w \le c$ and $+\infty$ otherwise, and $g^*(z) = b^T z$ if $z \le 0$ and $+\infty$ otherwise. So

$$d^* = \max \{ b^T y : A^T y \le c,\ y \ge 0 \},$$

the [LP dual](/lp-duality/). Theorem 3 gives complementary slackness. Theorem 2 needs a point with $A x_0 > b$, but for polyhedral $f$ and $g$ the interior condition can be dropped (Rockafellar, Section 31), which recovers the LP strong duality theorem.

### Other consequences

- **Lagrangian duality.** With $g$ the indicator of a convex set $C$, the primal is $\min f(x)$ subject to $Ax \in C$, and $g^*$ is the support function of $C$. The dual is the [Lagrange dual](/lagrangian-duality/) written with conjugates, and the interior condition is a [Slater condition](/slater-condition/).
- **Conjugate of a sum.** Applying Theorem 2 to $f(x) - w^T x$ and $g$ with $A = I$ gives $(f + g)^*(w) = \min_y \big( f^*(w - y) + g^*(y) \big)$ when $\operatorname{dom} f \cap \operatorname{int} \operatorname{dom} g$ is nonempty. Without the condition the right side can be smaller.
- **A saddle point.** If $g$ is also closed, then $g(Ax) = \sup_y \big( -y^T A x - g^*(-y) \big)$, so $p^*$ is the inf-sup and $d^*$ the sup-inf of $L(x, y) = f(x) - y^T A x - g^*(-y)$. Strong duality is a [minimax theorem](/minimax-theorem/) for $L$, and $(x^*, y^*)$ is a saddle point. Primal-dual splitting methods iterate on this saddle-point form.

## Tightness

Each example below was checked with a short script.

- **The interior condition is needed for a zero gap.** Let $f(x) = -\sqrt{x_1 x_2}$ on $\mathbb{R}^2_+$ and $+\infty$ elsewhere, let $g$ be the indicator of the line $\{ x_1 = 0 \}$, and $A = I$. The feasible points have $x_1 = 0$, so $p^* = 0$. By the arithmetic-geometric mean inequality, $f^*(y)$ is 0 if $y_1 \le 0$, $y_2 \le 0$ and $y_1 y_2 \ge \frac{1}{4}$, and $+\infty$ otherwise. And $g^*(z)$ is 0 if $z_2 = 0$ and $+\infty$ otherwise. A finite dual value needs $y_2 = 0$ and $y_1 y_2 \ge \frac{1}{4}$ at the same time, which is impossible. So $d^* = -\infty < 0 = p^*$. Here $\operatorname{dom} g$ has no interior, and the interiors of the two domains do not meet.
- **The interior condition is needed for dual attainment.** Let $f(x) = -\sqrt{x}$ for $x \ge 0$ and $+\infty$ otherwise, $g$ the indicator of $\{0\}$, and $A = 1$. Then $p^* = f(0) = 0$. For $y < 0$, $f^*(y) = -\frac{1}{4y}$, and $f^*(y) = +\infty$ for $y \ge 0$. Also $g^* = 0$. So $d^* = \sup_{y < 0} \frac{1}{4y} = 0 = p^*$, but no $y$ attains it. The function $f$ has no subgradient at 0, which is where Step 4 fails.
- **Convexity is needed.** Weak duality holds for any $f$ and $g$, but the gap can be positive. Let $f(x) = \min((x - 1)^2, (x + 1)^2)$, $g$ the indicator of $\{0\}$, and $A = 1$. Then $p^* = f(0) = 1$, while $d^* = \sup_y (-f^*(y)) = f^{**}(0) = 0$, the value at 0 of the [convex envelope](/convex-envelope/) of $f$. The gap is exactly the nonconvexity of $f$ at the solution.
- **Finiteness of $p^*$.** If $p^* = -\infty$, weak duality forces $d^* = -\infty$, so there is no dual solution to attain.

## History

Werner Fenchel proved the theorem in 1949 for $A = I$ in the form $\inf (f - h) = \max (h_* - f^*)$, with $f$ convex and $h$ concave, in the same paper that introduced conjugate convex functions in several variables. He developed the theory further in his Princeton lecture notes of 1951. R. Tyrrell Rockafellar extended the theorem to the composition with a linear map in 1966, and his book of 1970 states it with relative interiors instead of interiors and with weaker conditions for polyhedral functions. For this reason the general form is often called Fenchel-Rockafellar duality. The same conjugate framework later gave the perturbation theory of duality, in which every dual problem comes from a value function such as $v$ in the proof above.

## References
