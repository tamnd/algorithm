---
tag: XQN0ZX
kind: theorem
slug: supporting-hyperplane-theorem
name: Supporting hyperplane theorem
aliases:
- supporting hyperplane lemma
area: optimization/convex-optimization
level: core
summary: At each boundary point of a convex set there is a hyperplane through the point with the whole set on one side.
prereqs: [separating-hyperplane-theorem, convex-set]
see_also: [supporting-hyperplane, support-function, subgradient, epigraph, farkas-lemma, kkt-conditions, extreme-point]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.5.2 (supporting hyperplanes, the theorem and its partial converse) and Section 3.1.3 (first-order condition, the tangent plane supports the epigraph)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 11, Separation theorems (supporting hyperplanes at relative boundary points), and Section 23 (existence of subgradients)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter A, Convex sets (supporting hyperplanes and the normal cone), and Chapter D (subdifferentials of finite convex functions)
  - paper: "Hermann Minkowski, Theorie der konvexen Körper, insbesondere Begründung ihres Oberflächenbegriffs, in Gesammelte Abhandlungen, Band II, Teubner, Leipzig, 1911"
    locator: supporting planes of convex bodies
---

The supporting hyperplane theorem says that at each boundary point $x_0$ of a [convex set](/convex-set/) $C \subseteq \mathbb{R}^n$ there is a hyperplane through $x_0$ that has all of $C$ on one side. Such a hyperplane is a [supporting hyperplane](/supporting-hyperplane/). The theorem follows from the [separating hyperplane theorem](/separating-hyperplane-theorem/), and a partial converse characterizes closed convex sets with nonempty interior by it. Applied to the [epigraph](/epigraph/) of a convex function, it gives the existence of [subgradients](/subgradient/), which is the basis of nonsmooth convex optimization.

## Statement

The *boundary* of $C$ is $\operatorname{bd} C = \operatorname{cl} C \setminus \operatorname{int} C$. A hyperplane $\{x : a^T x = a^T x_0\}$ with $a \neq 0$ *supports* $C$ at $x_0$ if $a^T x \le a^T x_0$ for all $x \in C$.

**Theorem 1 (supporting hyperplane).** Let $C \subseteq \mathbb{R}^n$ be nonempty and convex, and let $x_0 \in \operatorname{bd} C$. Then there is $a \ne 0$ with

$$a^T x \le a^T x_0 \quad \text{for all } x \in C.$$

**Theorem 2 (partial converse).** Let $C \subseteq \mathbb{R}^n$ be closed with nonempty interior, and assume that $C$ has a supporting hyperplane at each point of $\operatorname{bd} C$. Then $C$ is convex, and it equals the intersection of the closed half-spaces $\{x : a^T x \le a^T x_0\}$ of its supporting hyperplanes.

### Examples

- **A disk.** For the closed unit disk and $x_0 = (0.6, 0.8)$, the only supporting hyperplane is $0.6 x_1 + 0.8 x_2 = 1$, with $a = x_0$. By the Cauchy-Schwarz inequality, $x_0^T x \le \lVert x \rVert \le 1 = x_0^T x_0$ for each $x$ in the disk.
- **A corner of a square.** For $C = [0, 1]^2$ and $x_0 = (1, 1)$, each $a = (\alpha, \beta)$ with $\alpha, \beta \ge 0$ and $a \ne 0$ gives a supporting hyperplane, since $\alpha x_1 + \beta x_2 \le \alpha + \beta$ on the square. For $a = (1, 2)$, the maximum of $x_1 + 2 x_2$ on the square is $3$, at $(1, 1)$. At the edge point $(1, 0.5)$, only the multiples of $a = (1, 0)$ work: a component $\beta \ne 0$ would make $\alpha x_1 + \beta x_2$ larger at $(1, 0.5 + 0.5\,\mathrm{sign}(\beta))$ than at $(1, 0.5)$.
- **A polyhedron.** For $P = \{x : Ax \le b\}$ and $x_0 \in P$, the supporting normals at $x_0$ are the nonzero vectors $a = \sum_{i \in I} y_i a_i$ with $y_i \ge 0$, where $I$ is the set of rows with $a_i^T x_0 = b_i$. This cone is the normal cone of $P$ at $x_0$, and it is what the [KKT conditions](/kkt-conditions/) ask the negative gradient to lie in. That every supporting normal has this form is [Farkas' lemma](/farkas-lemma/).

## In plain words

Push a flat board against a solid ball, a cube or any other solid with no dents. Wherever the board touches the solid, the whole solid stays on one side of the board. On a smooth part, like a point of a ball, the board can only lie flat in one way. At a corner of a cube, it can tilt in many ways and still touch only at the corner.

For a solid with a dent, this fails at a point inside the dent: any board through that point cuts into the solid. The converse also holds: a closed solid where a board fits at every point of the surface has no dents.

## Proof

We use the [separating hyperplane theorem](/separating-hyperplane-theorem/) (Theorem 1 there): two nonempty disjoint convex sets $C', D'$ have $a \ne 0$ and $b$ with $a^T x \le b \le a^T y$ for $x \in C'$, $y \in D'$.

**Proof of Theorem 1.**

*Case 1: $\operatorname{int} C \ne \emptyset$.*

1. *$\operatorname{int} C$ is convex.* If $B(y_1, r) \subseteq C$ and $B(y_2, r) \subseteq C$, then for $\theta \in [0, 1]$ each point $\theta y_1 + (1 - \theta) y_2 + v$ with $\lVert v \rVert < r$ equals $\theta (y_1 + v) + (1 - \theta)(y_2 + v)$, a convex combination of points of $C$. So $B(\theta y_1 + (1-\theta) y_2, r) \subseteq C$.
2. *Separate.* The sets $\operatorname{int} C$ and $\{x_0\}$ are nonempty and convex, and they are disjoint because $x_0 \notin \operatorname{int} C$. The separating hyperplane theorem gives $a \ne 0$ with $a^T y \le a^T x_0$ for all $y \in \operatorname{int} C$.
3. *Extend to all of $C$.* Fix $y \in \operatorname{int} C$ with $B(y, r) \subseteq C$, and let $x \in C$. For $t \in (0, 1]$, the point $x_t = (1 - t) x + t y$ has $B(x_t, t r) = (1 - t)x + t B(y, r) \subseteq C$ by convexity, so $x_t \in \operatorname{int} C$. By step 2, $a^T x_t \le a^T x_0$. Let $t \to 0$: $a^T x \le a^T x_0$.

*Case 2: $\operatorname{int} C = \emptyset$.* Then the affine hull of $C$ is not all of $\mathbb{R}^n$: otherwise $C$ contains $n + 1$ affinely independent points, and their simplex, which lies in $C$, has an interior point. So the affine hull is $x_0 + V$ for a linear subspace $V \ne \mathbb{R}^n$. Here $x_0 \in \operatorname{cl} C$ lies in the affine hull, because an affine subspace is closed. Pick $a \ne 0$ orthogonal to $V$. Then $a^T x = a^T x_0$ for all $x \in C$, so the inequality holds with equality. $\blacksquare$

The hyperplane of Case 2 contains all of $C$. It is a valid but weak support. Rockafellar's version with relative interiors gives, when $x_0$ is on the relative boundary, a hyperplane that does not contain all of $C$.

**Proof of Theorem 2.** Let $Q$ be the intersection of the half-spaces of all supporting hyperplanes of $C$. Each contains $C$, so $C \subseteq Q$. $Q$ is an intersection of convex sets, so it is convex. We show $Q \subseteq C$.

1. *A boundary point between an inner point and an outside point.* Let $z \notin C$ and pick $y \in \operatorname{int} C$. Let $t^* = \sup\{t \in [0, 1] : y + t (z - y) \in C\}$ and $w = y + t^*(z - y)$. Since $C$ is closed, $w \in C$, so $t^* < 1$. Since $y$ is interior, $t^* > 0$. The points $y + t(z - y)$ with $t \in (t^*, 1]$ are not in $C$ and tend to $w$, so $w \notin \operatorname{int} C$, and $w \in \operatorname{bd} C$.
2. *The supporting half-space at $w$ cuts off $z$.* By hypothesis there is $a \ne 0$ with $a^T x \le a^T w$ for all $x \in C$. Since $y + \varepsilon a \in C$ for small $\varepsilon > 0$, we get $a^T y + \varepsilon \lVert a \rVert^2 \le a^T w$, so $a^T y < a^T w$. Now $z = w + s(w - y)$ with $s = \frac{1}{t^*} - 1 > 0$, so $a^T z = a^T w + s (a^T w - a^T y) > a^T w$. So $z \notin Q$.

Hence $Q = C$, and $C$ is convex. $\blacksquare$

## Consequences

**Subgradients exist at interior points.** Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ be convex and let $x_0 \in \operatorname{int} \operatorname{dom} f$. Then there is $g$ with $f(x) \ge f(x_0) + g^T (x - x_0)$ for all $x$.

*Proof.* The [epigraph](/epigraph/) $E = \operatorname{epi} f$ is convex. The point $(x_0, f(x_0))$ is in $E$, and $(x_0, f(x_0) - \varepsilon) \notin E$ for each $\varepsilon > 0$, so it is a boundary point. Theorem 1 gives $(a, \beta) \ne (0, 0)$ with $a^T x + \beta t \le a^T x_0 + \beta f(x_0)$ for all $(x, t) \in E$. Since $t$ can be any number at least $f(x)$, $\beta \le 0$. If $\beta = 0$, then $a \ne 0$ and $a^T (x - x_0) \le 0$ for all $x \in \operatorname{dom} f$; but $x = x_0 + \varepsilon a$ is in $\operatorname{dom} f$ for small $\varepsilon > 0$ and gives $\varepsilon \lVert a \rVert^2 \le 0$, a contradiction. So $\beta < 0$. Put $t = f(x)$ and divide by $-\beta$: $f(x) \ge f(x_0) + g^T (x - x_0)$ with $g = a / (-\beta)$. $\square$

At a boundary point of the domain a subgradient can fail to exist: $f(x) = -\sqrt{x}$ on $[0, \infty)$ has no subgradient at 0, because the supporting hyperplane of its epigraph there is vertical.

**Further consequences.**

- **The [support function](/support-function/).** For a compact convex $C$ and a direction $a$, the maximum of $a^T x$ over $C$ is reached at a point where $\{a^T x = \max\}$ supports $C$. A linear program attains its optimum on a supporting face of the feasible polyhedron, and when the polyhedron has a vertex, at an [extreme point](/extreme-point/).
- **First-order optimality.** For a convex problem with a differentiable objective, $x^*$ is optimal if and only if $-\nabla f_0(x^*)$ is a supporting normal of the feasible set at $x^*$, or is 0. See the [convex optimization problem](/convex-optimization-problem/).
- **Outer descriptions.** Theorem 2 and its proof show that a closed convex set with nonempty interior is the intersection of its supporting half-spaces. Cutting-plane methods build such an intersection one supporting half-space at a time.
- **Extreme points.** A supporting hyperplane cuts a compact convex set in a face. Induction on the dimension of the face gives the Krein-Milman property in $\mathbb{R}^n$: a compact convex set is the convex hull of its [extreme points](/extreme-point/).

## Tightness

- **Convexity is needed in Theorem 1.** Let $C = \{x \in \mathbb{R}^2 : x_1 \le 0 \text{ or } x_2 \le 0\}$, the plane without the open positive quadrant. The origin is a boundary point. A supporting normal $a$ would satisfy $a^T x \le 0$ on the half-plane $x_1 \le 0$, which forces $a = (\alpha, 0)$ with $\alpha \ge 0$, and on the half-plane $x_2 \le 0$, which forces $a = (0, \beta)$ with $\beta \ge 0$. Together $a = 0$.
- **A nonempty interior is needed in Theorem 2.** Let $C = ([0, 1] \cup [2, 3]) \times \{0\}$ in $\mathbb{R}^2$. It is closed, each of its points is a boundary point, and the line $x_2 = 0$ supports $C$ at each of them. But $C$ is not convex.
- **The supporting hyperplane need not be unique.** At the corner of the square above, every $a \ge 0$ with $a \ne 0$ works. The hyperplane is unique at $x_0$ exactly when the normal cone at $x_0$ is a single ray, for example at a point where the boundary is smooth.
- **Strictness fails.** A supporting hyperplane can touch $C$ in more than one point, as the line $x_1 = 1$ does along an edge of the square.

## History

Supporting planes of convex bodies appear in Hermann Minkowski's work on convex bodies, published in his collected papers in 1911. The modern statements, with relative interiors and for convex functions through epigraphs, are in Rockafellar's Convex Analysis, Section 11 and Section 23.

## References
