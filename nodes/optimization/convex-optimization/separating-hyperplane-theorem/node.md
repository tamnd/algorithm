---
tag: HB1J0D
kind: theorem
slug: separating-hyperplane-theorem
name: Separating hyperplane theorem
aliases:
- hyperplane separation theorem
- separation theorem
area: optimization/convex-optimization
level: core
summary: Two disjoint convex sets in R^n lie on opposite sides of some hyperplane. If one is closed and the other compact, the separation is strict.
prereqs: [convex-set]
see_also: [supporting-hyperplane-theorem, farkas-lemma, slater-condition, lagrangian-duality, separation-oracle, support-vector-machine, minimax-theorem, convex-feasibility-problem]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.5.1 (separating hyperplane theorem, with the proof for sets at positive distance) and Section 8.1 (projection on a set)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 6 (relative interiors and closures of convex sets) and Section 11, Separation theorems
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter A, Convex sets (projection onto closed convex sets, and separation theorems)
  - paper: "Hermann Minkowski, Theorie der konvexen Körper, insbesondere Begründung ihres Oberflächenbegriffs, in Gesammelte Abhandlungen, Band II, Teubner, Leipzig, 1911"
    locator: the support and separation properties of convex bodies
---

The separating hyperplane theorem says that two disjoint [convex sets](/convex-set/) in $\mathbb{R}^n$ lie on opposite sides of some hyperplane. If one of them is closed and the other is compact, the hyperplane can be chosen so that both sets stay at a positive distance from it. The theorem is the geometric root of duality in optimization: [Farkas' lemma](/farkas-lemma/), [LP duality](/lp-duality/), [Slater's condition](/slater-condition/) and the [supporting hyperplane theorem](/supporting-hyperplane-theorem/) are all proved from it. In algorithms it appears as the [separation oracle](/separation-oracle/) of the [ellipsoid method](/ellipsoid-method/) and as the margin of a [support vector machine](/support-vector-machine/).

## Statement

A *hyperplane* is $H = \{x \in \mathbb{R}^n : a^T x = b\}$ with $a \in \mathbb{R}^n \setminus \{0\}$ and $b \in \mathbb{R}$. It *separates* sets $C$ and $D$ if $a^T x \le b$ for all $x \in C$ and $a^T y \ge b$ for all $y \in D$. It separates them *strictly* if, in addition, there is $\delta > 0$ with $a^T x \le b - \delta$ on $C$ and $a^T y \ge b + \delta$ on $D$.

**Theorem 1 (separation).** Let $C, D \subseteq \mathbb{R}^n$ be nonempty, convex and disjoint. Then there are $a \ne 0$ and $b$ with

$$a^T x \le b \le a^T y \quad \text{for all } x \in C \text{ and } y \in D.$$

**Theorem 2 (strict separation).** Let $C, D \subseteq \mathbb{R}^n$ be nonempty, convex and disjoint, with $C$ closed and $D$ compact. Then there are $a \ne 0$ and $b$ with

$$\sup_{x \in C} a^T x < b < \inf_{y \in D} a^T y.$$

Moreover, $a$ can be taken as $\bar y - \bar x$ for a pair $\bar x \in C$, $\bar y \in D$ at minimum distance, and then the gap $\inf_D a^T y - \sup_C a^T x$ is at least $\lVert a \rVert^2$.

### An example

Let $C$ be the closed unit disk around $(0, 0)$ and $D$ the closed unit disk around $(3, 1)$. The centers are $\sqrt{10} \approx 3.162 > 2$ apart, so the disks are disjoint. The closest points lie on the line of the centers, so $a$ is a positive multiple of $(3, 1)$. Take $a = (3, 1)$ and $b = a^T (1.5, 0.5) = 5$, the value at the midpoint of the centers. Then $\max_{x \in C} a^T x = \lVert a \rVert = \sqrt{10} \approx 3.162$ and $\min_{y \in D} a^T y = a^T (3, 1) - \sqrt{10} \approx 6.838$. So $3.162 < 5 < 6.838$, and the hyperplane $3x_1 + x_2 = 5$ separates the disks strictly.

## In plain words

Take two blobs of clay on a table. Each blob has no dents or holes, and they do not touch. Then you can slide a flat sheet of paper between them, so that one blob is on each side. If the blobs have dents, this can fail: a blob shaped like a ring can surround a small ball, and no flat sheet passes between them.

When the blobs do not even come close, the sheet can be placed with a gap on each side. When they come closer and closer without touching, far out at infinity, the sheet still fits but may touch one of them.

## Proof

We write $\lVert \cdot \rVert$ for the Euclidean norm, $\operatorname{cl}$ for closure and $\operatorname{int}$ for interior.

**Lemma 1 (projection).** Let $K \subseteq \mathbb{R}^n$ be nonempty, closed and convex, and let $z \in \mathbb{R}^n$. There is a unique point $p \in K$ nearest to $z$, and

$$(z - p)^T (x - p) \le 0 \quad \text{for all } x \in K.$$

*Proof.* Pick $x_0 \in K$. A nearest point, if it exists, lies in $K \cap \{x : \lVert x - z \rVert \le \lVert x_0 - z \rVert\}$, which is closed and bounded, hence compact, and nonempty. The continuous function $\lVert x - z \rVert$ has a minimum $p$ on it, and $p$ is nearest to $z$ in all of $K$. For $x \in K$ and $t \in (0, 1]$, the point $p + t(x - p)$ is in $K$, so

$$\lVert z - p - t(x - p) \rVert^2 - \lVert z - p \rVert^2 = -2t (z - p)^T (x - p) + t^2 \lVert x - p \rVert^2 \ge 0.$$

Divide by $t$ and let $t \to 0^+$: $(z - p)^T (x - p) \le 0$. If $p$ and $q$ are both nearest, the inequality for $p$ with $x = q$ and for $q$ with $x = p$ add up to $\lVert q - p \rVert^2 \le 0$, so $q = p$. $\square$

**Lemma 2 (a point and a closed convex set).** Let $K$ be nonempty, closed and convex, and let $z \notin K$. Let $p$ be the nearest point of $K$ to $z$ and $a = z - p$. Then $a \ne 0$ and

$$a^T x \le a^T z - \lVert a \rVert^2 \quad \text{for all } x \in K.$$

*Proof.* $a \ne 0$ because $p \in K$ and $z \notin K$. Lemma 1 gives $a^T x \le a^T p = a^T z - a^T (z - p) = a^T z - \lVert a \rVert^2$. $\square$

**Lemma 3 (the interior of the closure).** Let $S \subseteq \mathbb{R}^n$ be convex. Then $\operatorname{int}(\operatorname{cl} S) \subseteq S$.

*Proof.* The closure of a convex set is convex, because a limit of convex combinations of points of $S$ is a convex combination of the limits. We prove the lemma in four steps.

1. *If $\operatorname{int}(\operatorname{cl} S) \ne \emptyset$, then $\operatorname{int} S \ne \emptyset$.* If the affine hull of $S$ were not all of $\mathbb{R}^n$, then $S$ would lie in a hyperplane $H$, which is closed, so $\operatorname{cl} S \subseteq H$ would have empty interior. So $S$ contains $n + 1$ affinely independent points $v_0, \ldots, v_n$, and their convex hull $\Delta$ is in $S$. Each $x \in \mathbb{R}^n$ has unique barycentric coordinates $\lambda(x)$ with $\sum_i \lambda_i v_i = x$ and $\sum_i \lambda_i = 1$, and $x \mapsto \lambda(x)$ is affine, hence continuous. At $c = \frac{1}{n+1} \sum_i v_i$ all coordinates equal $\frac{1}{n+1} > 0$, so they stay positive on a ball around $c$. That ball lies in $\Delta \subseteq S$.
2. *The segment principle.* Let $y \in \operatorname{int} S$ with $B(y, r) \subseteq S$, let $w \in \operatorname{cl} S$ and $t \in (0, 1]$. Then $q = (1 - t) w + t y \in \operatorname{int} S$. For $t = 1$ this is the hypothesis. For $t < 1$, choose $w' \in S$ with $\lVert w - w' \rVert \le \frac{t r}{2(1 - t)}$ and put $y' = y + \frac{1 - t}{t} (w - w')$. Then $\lVert y' - y \rVert \le \frac{r}{2}$, so $B(y', \frac{r}{2}) \subseteq S$, and $q = (1 - t) w' + t y'$. For each $q'$ with $\lVert q' - q \rVert < \frac{t r}{2}$, we have $q' = (1 - t) w' + t (y' + (q' - q)/t)$ with $y' + (q' - q)/t \in B(y', \frac r2) \subseteq S$. So $q' \in S$ by convexity, and $q \in \operatorname{int} S$.
3. *The conclusion.* Let $z \in \operatorname{int}(\operatorname{cl} S)$. By step 1 there is $y \in \operatorname{int} S$. If $z = y$ we are done. Otherwise choose $\varepsilon > 0$ so small that $w = z + \varepsilon (z - y) \in \operatorname{cl} S$, which is possible because $z$ is an interior point of $\operatorname{cl} S$. Then $z = \frac{1}{1 + \varepsilon} w + \frac{\varepsilon}{1 + \varepsilon} y$, and step 2 with $t = \frac{\varepsilon}{1 + \varepsilon} \in (0, 1)$ gives $z \in \operatorname{int} S \subseteq S$. $\square$

**Proof of Theorem 1.**

1. *Reduce to one set.* Let $S = C - D = \{x - y : x \in C, y \in D\}$. It is nonempty. It is convex: if $s_1 = x_1 - y_1$ and $s_2 = x_2 - y_2$, then $\theta s_1 + (1-\theta) s_2 = (\theta x_1 + (1-\theta) x_2) - (\theta y_1 + (1 - \theta) y_2)$, and the two brackets lie in $C$ and $D$. Since $C \cap D = \emptyset$, $0 \notin S$.
2. *Points near 0 outside the closure.* By Lemma 3, $0 \notin \operatorname{int}(\operatorname{cl} S)$. So for each $k \ge 1$ there is $z_k \notin \operatorname{cl} S$ with $\lVert z_k \rVert < 1/k$.
3. *Separate each of them.* Apply Lemma 2 to $K = \operatorname{cl} S$, which is nonempty, closed and convex, and to $z_k$. This gives $a_k \ne 0$ with $a_k^T s < a_k^T z_k$ for all $s \in \operatorname{cl} S$. Let $u_k = a_k / \lVert a_k \rVert$. Then $u_k^T s < u_k^T z_k \le \lVert z_k \rVert < 1/k$.
4. *Take a limit.* The unit sphere is compact, so a subsequence of $(u_k)$ converges to some $u$ with $\lVert u \rVert = 1$. For each fixed $s \in S$, passing to the limit in $u_k^T s < 1/k$ along the subsequence gives $u^T s \le 0$.
5. *Return to $C$ and $D$.* So $u^T x \le u^T y$ for all $x \in C$ and $y \in D$. Fix any $y_0 \in D$. Then $b = \sup_{x \in C} u^T x \le u^T y_0$ is finite, and $u^T x \le b \le u^T y$ for all $x \in C$ and $y \in D$. With $a = u$ this is the claim. $\blacksquare$

**Proof of Theorem 2.**

1. *$S = C - D$ is closed.* Let $x_k - y_k \to s$ with $x_k \in C$ and $y_k \in D$. Since $D$ is compact, a subsequence $y_{k_j}$ converges to some $\bar y \in D$. Then $x_{k_j} = (x_{k_j} - y_{k_j}) + y_{k_j} \to s + \bar y$, and $s + \bar y \in C$ because $C$ is closed. So $s = (s + \bar y) - \bar y \in S$.
2. *Separate 0 from $S$.* $S$ is nonempty, closed and convex, and $0 \notin S$. Let $p = \bar x - \bar y$ be its nearest point to 0, with $\bar x \in C$ and $\bar y \in D$. Lemma 2 with $z = 0$ and $a' = -p$ gives $a'^T s \le -\lVert a' \rVert^2$ for all $s \in S$. Put $a = a' = \bar y - \bar x \ne 0$.
3. *Conclude.* For all $x \in C$ and $y \in D$, $a^T (x - y) \le -\lVert a \rVert^2$, so $\sup_C a^T x \le \inf_D a^T y - \lVert a \rVert^2$. Both sides are finite. Any $b$ strictly between $\sup_C a^T x$ and $\inf_D a^T y$ works. $\blacksquare$

The nearest pair $(\bar x, \bar y)$ minimizes $\lVert x - y \rVert$ over $C \times D$, so $\lVert a \rVert$ is the distance between the sets.

## Consequences

- **Closed convex sets are intersections of half-spaces.** If $K$ is closed and convex and $z \notin K$, Lemma 2 gives a half-space that contains $K$ and not $z$. So $K$ equals the intersection of all closed half-spaces that contain it. This is the outer description used by [cutting-plane methods](/cutting-plane-method/) and by the [convex conjugate](/convex-conjugate/).
- **[Supporting hyperplane theorem](/supporting-hyperplane-theorem/).** Separate a boundary point from the interior of the set.
- **[Farkas' lemma](/farkas-lemma/).** If $b$ is not in the cone $\{Ax : x \ge 0\}$, which is closed and convex, Lemma 2 gives $y$ with $A^T y \ge 0$ and $b^T y < 0$. This leads to [strong duality](/strong-duality/) for linear programs.
- **[Slater's condition](/slater-condition/).** Theorem 1 applied to two convex sets in the space of constraint and objective values gives the dual multipliers, and so strong [Lagrangian duality](/lagrangian-duality/) for convex problems.
- **Subgradients exist.** Separating a point below the graph from the [epigraph](/epigraph/) gives the existence of [subgradients](/subgradient/) at interior points of the domain.
- **Separation oracles.** For a closed convex set given by convex inequalities $f_i(x) \le 0$, a violated constraint $f_i(z) > 0$ and a subgradient $g$ of $f_i$ at $z$ give the separating half-space $f_i(z) + g^T(x - z) \le 0$. The [ellipsoid method](/ellipsoid-method/) needs only this.
- **Machine learning.** A [support vector machine](/support-vector-machine/) computes the hyperplane of Theorem 2 between the convex hulls of two finite point sets, with the largest gap. The [perceptron](/perceptron/) finds a separating hyperplane when one with a positive margin exists.
- **Game theory.** The [minimax theorem](/minimax-theorem/) for finite zero-sum games follows from a separation argument.

## Tightness

- **Convexity is needed.** Let $C$ be the unit circle $\{x : \lVert x \rVert = 1\}$ in $\mathbb{R}^2$ and $D = \{0\}$. They are disjoint, but if $a^T x \le b$ on $C$ and $a^T 0 = 0 \ge b$, then $x = a / \lVert a \rVert \in C$ gives $\lVert a \rVert \le b \le 0$, which contradicts $a \ne 0$.
- **Closed sets need not be strictly separated.** Let $C = \{x : x_1 > 0, \ x_2 \ge 1/x_1\}$ and $D = \{x : x_2 \le 0\}$. Both are closed and convex, and they are disjoint. Strict separation with gap $\delta$ would force $\lVert a \rVert \cdot \operatorname{dist}(C, D) \ge \delta > 0$. But the points $(t, 1/t) \in C$ and $(t, 0) \in D$ are $1/t$ apart, so $\operatorname{dist}(C, D) = 0$. The only separating hyperplane is $x_2 = 0$, and $D$ touches it. Theorem 2 avoids this by asking that one set be compact.
- **The sets may touch the hyperplane.** $C = \{x : x_1 \le 0\}$ and $D = \{x : x_1 > 0\}$ are disjoint and convex, and the hyperplane $x_1 = 0$ meets $C$. No hyperplane keeps both at a positive distance.
- **Disjointness of interiors is the true condition.** The proof of Theorem 1 works when only $0 \notin \operatorname{int}(C - D)$ is known, because Lemma 3 shows that $\operatorname{int}(\operatorname{cl} S) = \operatorname{int} S$ for convex $S$. For example, two closed squares that share an edge are separated by the line of the edge, although they are not disjoint.

## History

Separation and support properties of convex bodies appear in Hermann Minkowski's work on convex bodies, published in his collected papers in 1911. The Hahn-Banach theorem of functional analysis extends separation to infinite-dimensional spaces. Rockafellar, in Section 11, states the finite-dimensional theorems with relative interiors in place of interiors, which also covers sets of lower dimension.

## References
