---
tag: 2Y8G4M
kind: algorithm
slug: groebner-walk
name: Gröbner walk
aliases:
- Collart-Kalkbrener-Mall walk
- Gröbner walk conversion
area: algebra/computer-algebra
level: research
summary: Moves a Gröbner basis across the cones of weight vectors to change monomial order.
model: blum-shub-smale-machine
complexity:
  vars: {S: the number of cones of the Gröbner fan crossed by the path, C: the largest cost of one step, B: the size of the largest intermediate basis}
  time: {worst: O(S C), best: O(C)}
  space: {extra: O(B)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [reduced-groebner-basis, groebner-basis-conversion, buchberger-algorithm]
see_also: [fglm-algorithm, monomial-ordering, multivariate-division-algorithm, elimination-ideal, polynomial-system-solving, groebner-basis-computation, normal-form]
sources:
  - paper: doi:10.1006/jsco.1996.0145
    title: Stéphane Collart, Michael Kalkbrener and Daniel Mall, Converting bases with the Gröbner walk, Journal of Symbolic Computation 24(3-4), 465-469, 1997
    locator: the walk along a segment of weight vectors, the lifting of the basis of the initial ideal and the proof of correctness
  - book: isbn:9780387207063
    title: David A. Cox, John Little and Donal O'Shea, Using Algebraic Geometry, second edition, Springer, 2005
    locator: Chapter 8, Section 4 (the Gröbner fan of an ideal) and Section 5 (the Gröbner walk, with the algorithm in matrix-order form and a worked example)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Sections 2 and 7 (monomial orders and reduced Gröbner bases) and Chapter 10, Section 5 (the Gröbner walk)
  - paper: "Teo Mora and Lorenzo Robbiano, The Gröbner fan of an ideal, Journal of Symbolic Computation 6(2-3), 183-208, 1988"
    locator: the finiteness of the set of reduced Gröbner bases of an ideal and the fan of their cones
  - book: isbn:9780821804872
    title: Bernd Sturmfels, Gröbner Bases and Convex Polytopes, University Lecture Series 8, American Mathematical Society, 1996
    locator: Chapters 1 and 2 (initial ideals, weight vectors, the Gröbner fan and the state polytope)
  - paper: "Beatrice Amrhein, Oliver Gloor and Wolfgang Küchlin, On the walk, Theoretical Computer Science 187(1-2), 179-202, 1997"
    locator: the perturbed walk, which handles target weights on walls, and implementation experience
---

The Gröbner walk converts a Gröbner basis of an ideal for one monomial order into the Gröbner basis of the same ideal for another order, for ideals of any dimension. It uses the fact that an ideal has only finitely many reduced Gröbner bases, and that the weight vectors giving each one fill a convex cone; together these cones form the Gröbner fan. The walk follows a straight segment from a weight vector of the start order to one of the target order. Each time the segment crosses a wall between cones, the algorithm computes a Gröbner basis of a small ideal of initial forms and lifts it to a basis of the whole ideal for the next cone. Collart, Kalkbrener and Mall published it in 1997. It is the standard conversion for positive-dimensional ideals, where the [FGLM algorithm](/fglm-algorithm/) does not apply.

## In plain words

A Gröbner basis depends on a rule that ranks the terms of a polynomial. Some rules are cheap to compute with, others give more useful answers, and computing directly with a useful rule can be very slow.

The walk changes the rule gradually. It mixes the two rules with a slider, moving from the cheap one to the useful one. For most slider positions nothing changes. At a few positions two terms of some polynomial tie, and the basis must be updated. The update only looks at the tied terms, which is a much smaller problem, and then adds back the rest. After the last update the slider is at the useful rule and the basis is the one wanted.

## The problem

Let $K$ be a field (the implementation uses $K = \mathbb{Q}$) and $R = K[x_1, \ldots, x_n]$. A *weight vector* is $w \in \mathbb{Q}_{\ge 0}^n$; the weight of $x^\alpha$ is $w \cdot \alpha$. The *initial form* $\operatorname{in}_w(f)$ is the sum of the terms of $f$ of largest weight, and $\operatorname{in}_w(I)$ is the ideal spanned by the initial forms of the elements of $I$. Monomial orders are given as matrix orders: a matrix $M$ with rows $r_1, \ldots, r_k$ orders $x^\alpha > x^\beta$ when $(r_1 \cdot \alpha, \ldots, r_k \cdot \alpha)$ is lexicographically larger than $(r_1 \cdot \beta, \ldots, r_k \cdot \beta)$. With $x_1 > \cdots > x_n$, lex is the identity matrix, grlex has first row $(1, \ldots, 1)$ followed by the first $n - 1$ unit vectors, and grevlex has rows $(1, \ldots, 1), (1, \ldots, 1, 0), \ldots, (1, 0, \ldots, 0)$. For a matrix $M$ and a weight $w$, $(w; M)$ is the matrix with $w$ on top; when $w \ge 0$ it is a monomial order that refines $w$. $\operatorname{LT}$, $\operatorname{LM}$ and $\operatorname{LC}$ denote leading term, monomial and coefficient.

**Input:** matrix orders $M_s$ and $M_t$ whose first rows $\sigma$ and $\tau$ are nonnegative, and the reduced Gröbner basis $G_s$ of $I$ for $M_s$.
**Output:** the reduced Gröbner basis $G_t$ of $I$ for $M_t$.

Costs are counted in operations in $K$. The degree bound of the input is $d$ and the number of terms is $t$.

## The algorithm

```pseudo id=main
GROEBNER-WALK(G, M_s, M_t)
L1  w ← first row σ of M_s; τ ← first row of M_t; M_old ← M_s
L2  loop
L3      M_new ← (w; M_t)
L4      H ← the reduced Gröbner basis of ⟨in_w(g) : g ∈ G⟩ for M_new
L5      for each h ∈ H: divide h by the in_w(g) for M_old, h = Σ p_g in_w(g), and set h' ← Σ p_g g
L6      G ← the reduced Gröbner basis formed from the h' by interreduction for M_new
L7      if w = τ then return G
L8      u ← the least w·(α-β) / (w·(α-β) - τ·(α-β)) over g ∈ G with α = LM(g) for M_new and β in the support of g with τ·(α-β) < 0; u ← 1 if there is none
L9      w ← (1 - u) w + u τ; M_old ← M_new
```

The value $u$ at line L8 is the first point on the segment from $w$ to $\tau$ where some $g$ has a term $\beta$ whose weight catches up with that of its leading monomial $\alpha$: the next wall. The implementation keeps $w$ as a primitive integer vector, which changes nothing since a positive multiple of a weight gives the same initial forms. The basis of line L4 is computed with Buchberger's algorithm; the inputs are $w$-homogeneous and usually have only two or three terms each.

## Example

Let $I = \langle x^2 + y^2 - 4,\ xy - 1 \rangle \subseteq \mathbb{Q}[x, y]$, the circle and hyperbola of the [conversion](/groebner-basis-conversion/) page. Its reduced grevlex basis is $G = \{x^2 + y^2 - 4,\ xy - 1,\ y^3 + x - 4y\}$. Walk from grevlex, $\sigma = (1, 1)$, to lex, $\tau = (1, 0)$. The trace, from the implementation:

| step | $w$ | $\operatorname{in}_w(G)$ | $H$ | $G$ after the lift | next $u$ |
|---|---|---|---|---|---|
| 1 | $(1, 1)$ | $x^2 + y^2$, $xy$, $y^3$ | the same | unchanged | $2/3$, from $g = y^3 + x - 4y$ and $\beta = x$ |
| 2 | $(3, 1)$ | $x^2$, $xy$, $y^3 + x$ | $x + y^3$, $y^4$ | $x + y^3 - 4y$, $y^4 - 4y^2 + 1$ | none, so $u = 1$ |
| 3 | $(1, 0)$ | $x$, $y^4 - 4y^2 + 1$ | the same | unchanged | stop at line L7 |

At step 1, $\alpha - \beta = (-1, 3)$, so $w \cdot (\alpha - \beta) = 2$ and $\tau \cdot (\alpha - \beta) = -1$, giving $u = 2/(2+1) = 2/3$ and $w = \frac13 (1, 1) + \frac23 (1, 0) = (1, \frac13)$, scaled to $(3, 1)$. There $y^3$ and $x$ both have weight 3. At step 2 the lift of $y^4 = y \cdot (y^3 + x) - 1 \cdot xy$ is $y \cdot (y^3 + x - 4y) - (xy - 1) = y^4 - 4y^2 + 1$, and the lift of $x + y^3$ is $y^3 + x - 4y$ itself. The result is the lex basis $\{x + y^3 - 4y,\ y^4 - 4y^2 + 1\}$, which Buchberger's algorithm gives directly. On $x^5 - y$, $y^5 - x - 1$, whose lex basis has degree 25, the path is $(1,1) \to (5,1) \to (1,0)$.

## Correctness

The full proof is in the correctness file. The invariant at line L4 is that $G$ is the reduced Gröbner basis of $I$ for $M_{\text{old}}$ and that $\operatorname{LM}_{M_{\text{old}}}(g)$ appears in $\operatorname{in}_w(g)$ for every $g$. Then the initial forms are a Gröbner basis of $\operatorname{in}_w(I)$ for $M_{\text{old}}$, so the division at line L5 has remainder 0. Each lift $h'$ lies in $I$, and its leading monomial for $M_{\text{new}}$ is that of $h$, because the other terms of $h'$ have smaller weight. Since $\operatorname{LM}_{M_{\text{new}}}(I) = \operatorname{LM}_{M_{\text{new}}}(\operatorname{in}_w(I))$, the lifts form a Gröbner basis for $M_{\text{new}}$. The choice of $u$ at line L8 keeps the invariant for the next $w$. The walk stops because $u > 0$ at each step, and each step enters a new cone of the finite Gröbner fan (Mora and Robbiano 1988). At $w = \tau$ the order $(\tau; M_t)$ is $M_t$.

## Complexity

- **Number of steps.** One step per cone met by the segment from $\sigma$ to $\tau$, plus the last step. The Gröbner fan is finite, so the number is finite, proved; but it has no useful bound in terms of $n$, $d$ and $t$. In examples it is often small, observed: 3 on the example above, and at most 7 on the 540 random systems in two and three variables of the tests.
- **One step.** A Gröbner basis computation for $\operatorname{in}_w(I)$, a division and an interreduction. For a generic point of a wall, the initial forms have few terms, and the Gröbner basis computation is cheap, observed. At the end point $\tau = (1, 0, \ldots, 0)$ of lex, which lies on many walls, the initial forms can be large; this is the "last step" problem.
- **Worst case.** The output itself can have degree doubly exponential in $n$ (Mayr and Meyer 1982), so no conversion is better than doubly exponential in the worst case. The walk inherits that bound in each step.
- **Space.** The intermediate bases, which can be larger than both the start and the target basis.

## Properties

- **Any dimension.** Unlike FGLM, the walk does not need $R/I$ to be finite dimensional.
- **Deterministic.** The path and the walls are fixed by $\sigma$, $\tau$ and $I$.
- **Exact.** All arithmetic is in $K$; the weights are rational.
- **Local work.** Each step only needs the initial forms, which are usually binomials or trinomials at a generic wall point.

## Variants and improvements

- **The perturbed walk** (Amrhein, Gloor and Küchlin 1997). Replace the start and target weights by perturbations, small changes along the later rows of the matrices, so that the path avoids walls of lower dimension and the last step is cheap.
- **The fractal walk.** When an initial ideal is itself large, walk recursively inside it with perturbed orders.
- **Tropical walks.** Moving through the whole Gröbner fan, rather than along a segment, computes all initial ideals and is used to compute tropical varieties (Gfan, Jensen).
- **FGLM** for zero-dimensional ideals, with a proved $O(n D^3)$ bound; see [FGLM](/fglm-algorithm/).
- **Hilbert-driven Buchberger** (Traverso 1997) for homogeneous ideals, using the Hilbert series known from the start basis.

## When to use it

Use it to change order for a positive-dimensional ideal, for example to compute an [elimination ideal](/elimination-ideal/) or an implicit equation from a grevlex basis. For zero-dimensional ideals FGLM is usually better, since its cost is controlled by the number of solutions. When the start and target first rows coincide, as for grlex and grevlex, the walk degenerates to a single step that is a full Gröbner basis computation for the homogeneous parts; then convert by other means.

## Pitfalls

- **Negative weights.** The weights must be nonnegative and the matrix orders must have their weight as first row. A weight with a negative entry gives a matrix that is not a well-order.
- **The order used for division.** The division at line L5 must be with respect to the old order $M_{\text{old}}$, for which the initial forms are a Gröbner basis. Dividing for $M_{\text{new}}$ can leave a nonzero remainder.
- **The last step.** The lex target weight $(1, 0, \ldots, 0)$ lies on many walls, so the initial forms at the last step can be almost the whole basis. Use a perturbed target.
- **Exact walls.** The value $u$ must be computed exactly. With floating point weights, a wall can be missed and the invariant broken.
- **Intermediate swell.** Intermediate bases can have larger coefficients than both the start and the target.

## Implementations

## History

Mora and Robbiano (1988) showed that an ideal has finitely many reduced Gröbner bases and that they correspond to the cones of a fan, the Gröbner fan; Bayer and Morrison studied the corresponding state polytope at the same time. Collart, Kalkbrener and Mall turned this into the conversion algorithm in 1997. Amrhein, Gloor and Küchlin made it practical with the perturbed walk and the fractal walk, and the walk was implemented in Singular and Maple. The study of the Gröbner fan grew into the computation of tropical varieties.

## References
