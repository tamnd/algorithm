---
tag: JAHPX8
kind: theorem
slug: stone-weierstrass-theorem
name: Stone-Weierstrass theorem
aliases:
- Stone's generalization of the Weierstrass theorem
- Generalized Weierstrass approximation theorem
area: numerical/interpolation-and-approximation
level: advanced
summary: 'Generalisation: on a compact space, a subalgebra of continuous real functions that contains the constants and separates points is uniformly dense.'
prereqs: [weierstrass-approximation-theorem]
see_also: [approximation-theory, jackson-theorem, trigonometric-interpolation, multivariate-interpolation, tensor-product-interpolation, radial-basis-function-interpolation, bernstein-polynomials, kolmogorov-width]
sources:
  - paper: "Marshall H. Stone, Applications of the theory of Boolean rings to general topology, Transactions of the American Mathematical Society 41 (1937) 375-481"
    locator: the first form of the generalized approximation theorem
  - paper: "Marshall H. Stone, The generalized Weierstrass approximation theorem, Mathematics Magazine 21 (1948) 167-184 and 237-254"
    locator: the lattice proof via |f| and the real and complex versions
  - book: isbn:9780070542358
    title: Walter Rudin, Principles of Mathematical Analysis, third edition, McGraw-Hill, 1976
    locator: Theorems 7.26 (Weierstrass), 7.32 (Stone's generalization) and 7.33 (the complex case)
  - paper: "Karl Weierstrass, Über die analytische Darstellbarkeit sogenannter willkürlicher Functionen einer reellen Veränderlichen, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin (1885) 633-639 and 789-805"
    locator: the original theorem for polynomials on an interval and trigonometric polynomials
---

The Stone-Weierstrass theorem says when a family of continuous functions is rich enough to approximate every continuous function uniformly. The answer is algebraic: it is enough that the family is closed under sums, products and scalar multiples, contains the constants, and can tell any two points apart. It contains the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) as the special case of polynomials on an interval, and gives at once the density of trigonometric polynomials, of multivariate polynomials, and of sums of products of functions of separate variables.

## Statement

Notation on the interpolation pages: $K$ is a compact Hausdorff space (for example a closed bounded set in $\mathbb{R}^d$), $C(K)$ is the space of continuous real functions on $K$ with $\|f\|_\infty = \max_{K} |f|$. A set $\mathcal{A} \subseteq C(K)$ is a **subalgebra** if it is closed under addition, multiplication and multiplication by real scalars. It **separates points** if for all $x \ne y$ in $K$ there is $g \in \mathcal{A}$ with $g(x) \ne g(y)$.

**Theorem (Stone 1937, 1948).** Let $K$ be compact Hausdorff and let $\mathcal{A} \subseteq C(K)$ be a subalgebra that contains the constant functions and separates points. Then $\mathcal{A}$ is dense in $C(K)$: for every $f \in C(K)$ and $\varepsilon > 0$ there is $g \in \mathcal{A}$ with $\|f - g\|_\infty < \varepsilon$.

**Complex version.** For complex-valued $C(K, \mathbb{C})$ the same conclusion holds if in addition $\mathcal{A}$ is closed under complex conjugation.

**Locally compact version.** If $X$ is locally compact Hausdorff and $\mathcal{A} \subseteq C_0(X)$ (functions vanishing at infinity) is a subalgebra that separates points and vanishes at no point, then $\mathcal{A}$ is dense in $C_0(X)$.

## In plain words

Suppose you have a collection of building-block functions that you may add, multiply and scale as often as you like. If the collection includes the constant functions, and for any two different points some function in it takes different values there, then you can build an approximation to any continuous function, as accurate as you want, everywhere at once on a bounded closed region.

The theorem says only that good approximations exist. It says nothing about how many building blocks are needed for a given accuracy; that requires more detailed results that use smoothness.

## Proof

Let $\bar{\mathcal{A}}$ be the closure of $\mathcal{A}$ in the norm $\|\cdot\|_\infty$. It is again a subalgebra containing the constants (sums and products of uniform limits are uniform limits of sums and products, since all functions are bounded). We show $\bar{\mathcal{A}} = C(K)$.

**Step 1: $\bar{\mathcal{A}}$ is closed under $|\cdot|$.** Let $f \in \bar{\mathcal{A}}$ and $M = \|f\|_\infty$. By the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) there are polynomials $P_k$ with $\max_{|t| \le M} \big| |t| - P_k(t) \big| < 1/k$. Then $P_k \circ f \in \bar{\mathcal{A}}$ because $\bar{\mathcal{A}}$ is an algebra with constants, and $\| |f| - P_k \circ f \|_\infty < 1/k$. Since $\bar{\mathcal{A}}$ is closed, $|f| \in \bar{\mathcal{A}}$.

**Step 2: $\bar{\mathcal{A}}$ is a lattice.** For $f, g \in \bar{\mathcal{A}}$, $\max(f, g) = \tfrac12 (f + g + |f - g|)$ and $\min(f, g) = \tfrac12 (f + g - |f - g|)$ are in $\bar{\mathcal{A}}$ by Step 1; by induction so are maxima and minima of finitely many functions.

**Step 3: two-point interpolation.** Let $x \ne y$ in $K$ and $a, b \in \mathbb{R}$. Choose $g \in \mathcal{A}$ with $g(x) \ne g(y)$ and put
$$h = a + (b - a)\, \frac{g - g(x)}{g(y) - g(x)}.$$
Then $h \in \mathcal{A}$ (constants and scalar multiples are allowed), $h(x) = a$ and $h(y) = b$. For $x = y$ the constant $a$ works.

**Step 4: approximation from above at one point.** Fix $f \in C(K)$, $\varepsilon > 0$ and $x \in K$. For each $y \in K$ choose $h_y \in \mathcal{A}$ with $h_y(x) = f(x)$ and $h_y(y) = f(y)$ (Step 3). The set $U_y = \{z : h_y(z) < f(z) + \varepsilon\}$ is open (both sides are continuous) and contains $y$. By compactness, $U_{y_1}, \ldots, U_{y_r}$ cover $K$. Let $g_x = \min(h_{y_1}, \ldots, h_{y_r}) \in \bar{\mathcal{A}}$ (Step 2). Then $g_x(z) < f(z) + \varepsilon$ for every $z \in K$, since $z$ lies in some $U_{y_i}$, and $g_x(x) = f(x)$.

**Step 5: approximation from both sides.** The set $V_x = \{z : g_x(z) > f(z) - \varepsilon\}$ is open and contains $x$. Cover $K$ by $V_{x_1}, \ldots, V_{x_s}$ and put $g = \max(g_{x_1}, \ldots, g_{x_s}) \in \bar{\mathcal{A}}$. Each $g_{x_j} < f + \varepsilon$ everywhere, so $g < f + \varepsilon$; each $z$ lies in some $V_{x_j}$, so $g(z) \ge g_{x_j}(z) > f(z) - \varepsilon$. Hence $\|f - g\|_\infty < \varepsilon$.

Since $\varepsilon$ was arbitrary and $\bar{\mathcal{A}}$ is closed, $f \in \bar{\mathcal{A}}$. Finally, every element of $\bar{\mathcal{A}}$ is within any $\varepsilon$ of an element of $\mathcal{A}$, so $\mathcal{A}$ is dense in $C(K)$. $\square$

**Complex version.** If $\mathcal{A}$ is closed under conjugation, then its real-valued members $\mathcal{A}_{\mathbb{R}}$ contain $\operatorname{Re} g = (g + \bar g)/2$ and $\operatorname{Im} g = (g - \bar g)/(2i)$ for every $g \in \mathcal{A}$. They form a real subalgebra with the constants that separates points (if $g(x) \ne g(y)$ then $\operatorname{Re} g$ or $\operatorname{Im} g$ differs), so it is dense in $C(K)$ by the real theorem; approximate $\operatorname{Re} f$ and $\operatorname{Im} f$ separately. $\square$

## Consequences

- **Weierstrass's theorem.** Polynomials on $[a, b]$ form a subalgebra with constants, and $x$ separates points. (The proof above used Weierstrass's theorem only for $|t|$ on one interval, which also has a direct proof by the binomial series of $\sqrt{1 - s}$, so there is no circularity in deriving the general case.)
- **Multivariate polynomials** are dense in $C(K)$ for every compact $K \subset \mathbb{R}^d$: the coordinate functions separate points. This is the existence statement behind [multivariate interpolation](/multivariate-interpolation/) and approximation.
- **Trigonometric polynomials** $\sum_{|k| \le n} c_k e^{ik\theta}$ are dense in the continuous $2\pi$-periodic functions: on the circle $K = \{e^{i\theta}\}$ they form an algebra with constants, closed under conjugation, and $e^{i\theta}$ separates points. This is the uniform density behind [trigonometric interpolation](/trigonometric-interpolation/).
- **Sums of products.** Functions $\sum_{i} u_i(x) v_i(y)$ with $u_i \in C(X)$, $v_i \in C(Y)$ are dense in $C(X \times Y)$; this justifies [tensor-product](/tensor-product-interpolation/) and separated representations.
- **Exponential sums and Gaussians.** The span of $e^{a \cdot x}$, $a \in \mathbb{R}^d$, is an algebra ($e^{a \cdot x} e^{b \cdot x} = e^{(a+b) \cdot x}$) with constants that separates points, hence dense on compact sets; the same argument applies to many neural network and kernel families.
- **Separability.** If $K$ is a compact metric space, $C(K)$ is separable: polynomials with rational coefficients in countably many distance functions $d(\cdot, x_j)$ are dense.
- **Unique determination of measures.** Two finite Borel measures on compact $K$ that agree on a point-separating algebra with constants agree on $C(K)$, and so are equal (with the Riesz representation theorem).

## Tightness

Every hypothesis is needed.

- **Constants (or no common zero).** Polynomials on $[0, 1]$ with $p(0) = 0$ form a point-separating subalgebra without constants; their closure is $\{f : f(0) = 0\}$, so the constant 1 is at distance 1 from it.
- **Separation of points.** Even polynomials on $[-1, 1]$ form a subalgebra with constants but cannot separate $x$ from $-x$. For $f(x) = x$ and any even $g$, $\max(|1 - g(1)|, |-1 - g(1)|) \ge 1$, so $\|f - g\|_\infty \ge 1$: the closure is the even functions only.
- **Closure under products.** The linear span of $1$ and $x$ on $[0, 1]$ contains constants and separates points, but its closure is itself (it is finite dimensional), not $C[0, 1]$.
- **Compactness.** On $\mathbb{R}$, polynomials form a subalgebra with constants that separates points, but a uniform limit of polynomials on all of $\mathbb{R}$ is a polynomial (the differences of the approximants are bounded polynomials, hence eventually constant), so $\sin x$ cannot be approximated uniformly.
- **Conjugation in the complex case.** On the unit circle, polynomials in $z$ form a complex algebra with constants that separates points, but $\oint p(z)\, dz = 0$ for every polynomial while $\oint \bar z\, dz = 2\pi i$, so $\bar z$ is at uniform distance at least $1$ from all of them (since $|\oint (\bar z - p)\, dz| \le 2\pi \|\bar z - p\|_\infty$). Their closure is the disk algebra of functions analytic inside.
- **No rate.** The theorem gives no rate of approximation. For each sequence $\varepsilon_n \to 0$ there are continuous functions whose best polynomial errors $E_n(f)$ decrease more slowly than $\varepsilon_n$ (Bernstein's lethargy theorem); rates need smoothness, as in [Jackson's theorem](/jackson-theorem/).

## History

Weierstrass (1885) proved that continuous functions on an interval are uniform limits of polynomials, and that continuous periodic functions are limits of trigonometric polynomials. Marshall Stone generalized the result to compact spaces and algebras of functions in a long 1937 paper on Boolean rings and topology, and in 1948 published a short self-contained account with the lattice proof given here, which made the theorem a standard tool of analysis. The idea of reducing everything to approximating $|t|$ was Lebesgue's (1898), who used it in a proof of Weierstrass's theorem.

## References
