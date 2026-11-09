---
tag: HKVV09
kind: theorem
slug: smoothed-simplex-analysis
name: Smoothed analysis of the simplex method
aliases:
- Spielman-Teng smoothed analysis
- Spielman-Teng theorem
area: optimization/linear-programming
level: research
summary: With random perturbation of the input, the simplex method runs in polynomial expected time.
prereqs: [simplex-method, smoothed-analysis, polyhedron]
see_also: [smoothed-analysis, klee-minty-cube, hirsch-conjecture, simplex-method, dantzig-pivot-rule, steepest-edge-pivot-rule, ellipsoid-method, interior-point-method]
sources:
  - paper: doi:10.1145/990308.990310
    title: Daniel A. Spielman and Shang-Hua Teng, Smoothed analysis of algorithms, why the simplex algorithm usually takes polynomial time, Journal of the ACM 51(3), 2004
    locator: pages 385 to 463, the main theorem on the two-phase shadow-vertex method and the bound on the shadow size
  - paper: doi:10.1137/070683386
    title: Roman Vershynin, Beyond Hirsch conjecture, walks on random polytopes and smoothed complexity of the simplex method, SIAM Journal on Computing 39(2), 2009
    locator: pages 646 to 678, a shadow bound polylogarithmic in the number of constraints and a simpler phase one
  - paper: doi:10.1137/18M1197205
    title: Daniel Dadush and Sophie Huiberts, A friendly smoothed analysis of the simplex method, SIAM Journal on Computing 49(5), 2020
    locator: the shadow bound for Gaussian perturbations and its proof by perimeter and edge length
  - paper: doi:10.1145/3564246.3585124
    title: Sophie Huiberts, Yin Tat Lee and Xinzhi Zhang, Upper and lower bounds on the smoothed complexity of the simplex method, STOC 2023
    locator: pages 1904 to 1917, the bound with sigma to the power -3/2 and the first lower bound for the shadow-vertex rule
  - paper: doi:10.1007/bf01917108
    title: Karl Heinz Borgwardt, The average number of pivot steps required by the simplex-method is polynomial, Zeitschrift für Operations Research 26, 1982
    locator: pages 157 to 177, the average-case analysis of the shadow-vertex method
---

The smoothed analysis of the simplex method is the theorem of Spielman and Teng (2001, journal version 2004) that a version of the [simplex method](/simplex-method/) takes polynomial time in expectation on every linear program whose data are perturbed by a small random noise. It explains why the method is fast in practice although the [Klee-Minty cube](/klee-minty-cube/) and its variants make it exponential in the worst case: the bad programs are isolated, and a small random change of the data destroys them. The method in the theorem uses the *shadow-vertex* pivot rule, and the key fact is a bound on the number of vertices of a random two-dimensional projection of the feasible region. The theorem started the field of [smoothed analysis](/smoothed-analysis/).

## Statement

Consider the program maximize $c^\top x$ subject to $Ax \le b$, with $A \in \mathbb{R}^{n \times d}$, $b \in \mathbb{R}^n$ and $c \in \mathbb{R}^d \setminus \{0\}$. Fix any data $\bar A$, $\bar b$ in which every row $(\bar a_i, \bar b_i)$ has Euclidean norm at most $1$. Let
$$A = \bar A + G, \qquad b = \bar b + g,$$
where the entries of $G$ and $g$ are independent Gaussian variables with mean $0$ and standard deviation $\sigma$.

**Theorem (Spielman and Teng).** There is a two-phase simplex method with the shadow-vertex pivot rule whose expected number of pivots on the perturbed program, for every $\bar A$, $\bar b$, $c$, is bounded by a polynomial in $n$, $d$ and $1/\sigma$ (for $\sigma$ below a threshold that depends on $n$ and $d$).

The main step is a bound on the *shadow size*. For a fixed two-dimensional subspace $W$, let $S(A, b, W)$ be the number of vertices of the projection of $\{x : Ax \le b\}$ onto $W$. Then $\mathbb{E}[S]$ is bounded by a polynomial in $n$, $d$ and $1/\sigma$. Later work improved the bound on the shadow size:

| work | bound on the expected shadow size |
|---|---|
| Spielman and Teng (2004) | polynomial in $n$, $d$, $1/\sigma$ |
| Vershynin (2009) | polynomial in $d$ and $1/\sigma$, polylogarithmic in $n$ |
| Dadush and Huiberts (2020) | $O(\sigma^{-2} d^2 \sqrt{\log n})$ for small $\sigma$ |
| Huiberts, Lee and Zhang (2023) | $O(\sigma^{-3/2} d^{13/4} \log^{7/4} n)$ for small $\sigma$ |

## In plain words

The simplex method walks from corner to corner of a region with flat sides. For some carefully built regions, every known rule for choosing the next corner makes a walk of exponential length. Yet on real problems the walk is short.

Spielman and Teng explained this gap. They take any problem, even the worst one, and move all its numbers by a tiny random amount. They prove that the expected length of the walk on the moved problem is small: it grows only like a power of the size and of the inverse of the noise. So the bad problems are like a pencil balanced on its tip: a small push makes them easy. Real data always contain some noise from measurement and rounding, which is a reason why the method behaves well in practice.

## Proof

The full proof is long. This section proves the step that connects the pivot rule with the shadow and then gives the outline of the probabilistic part.

**The shadow-vertex rule.** Let $P = \{x : Ax \le b\}$, and let $v_0$ be a vertex of $P$ that maximizes some objective $u^\top x$. For $\lambda \in [0, 1]$ let $c_\lambda = (1 - \lambda) u + \lambda c$. The shadow-vertex method moves through the vertices of $P$ that maximize $c_\lambda^\top x$ as $\lambda$ grows from $0$ to $1$.

**Lemma.** Let $W = \operatorname{span}(u, c)$, let $\pi$ be the orthogonal projection onto $W$, and assume general position, so that every $c_\lambda$ has a unique optimal vertex except at finitely many $\lambda$. Then the shadow-vertex method makes at most $S(A, b, W)$ pivots.

*Proof.* Since $c_\lambda \in W$, $c_\lambda^\top x = c_\lambda^\top \pi(x)$ for every $x$. So a vertex $v$ of $P$ maximizes $c_\lambda^\top x$ over $P$ exactly when $\pi(v)$ maximizes $c_\lambda^\top y$ over the polygon $\pi(P)$. A unique maximizer of a linear function over a polygon is one of its vertices. So each vertex that the method visits projects to a vertex of $\pi(P)$, and different visited vertices project to different vertices, since each visited vertex is the unique maximizer for an open interval of $\lambda$ and the polygon has one maximizer for each such $\lambda$. At a value of $\lambda$ where the maximizer changes, the optimal face of $P$ for $c_\lambda$ is an edge (by general position) whose two ends are the old and the new vertex, so the step is one pivot along that edge. As $\lambda$ grows, the directions $c_\lambda$ turn monotonically within $W$, so the method passes the vertices of the polygon in order along one of its two chains and never visits a vertex of the polygon twice. So the number of pivots is less than the number of vertices of $\pi(P)$. $\square$

**Outline of the shadow bound.** With the lemma, it is enough to bound $\mathbb{E}[S]$ for a fixed plane $W$ (the plane depends on $c$ and on the start, and the phase-one construction makes the start independent enough of the noise). The proof of Dadush and Huiberts works with the polar view: the vertices of the shadow polygon correspond to the facets of a convex hull built from the rows of $(A, b)$ that meet the plane $W$, so it counts the edges of a random polygon in $W$. It shows two estimates:

1. The perimeter of this polygon is bounded, because the perturbed rows stay, with high probability, in a ball whose radius is close to $1$ for small $\sigma$.
2. Each edge of the polygon is, in expectation, not too short. This uses the Gaussian density: conditioned on the $d$ rows that form a facet, the facet can still move by an amount of order $\sigma$, so a very short edge is unlikely. The exact estimate is a lower bound polynomial in $\sigma$ and $1/d$.

The number of edges is about the perimeter divided by the typical edge length, and a careful version of this division gives the bound in the table. Spielman and Teng proved the first polynomial bound with a different, longer argument on the angles of the facets.

**Outline of the two phases.** The shadow-vertex method needs a start vertex and its objective $u$. Spielman and Teng solve an auxiliary program, built from the data, whose start vertex is known and whose optimal vertex gives a start for the original program; both phases are shadow-vertex runs on perturbed data. Vershynin gave a simpler phase one that adds $d$ random constraints, and the total expected number of pivots is a constant number of shadow sizes. The full arguments are in the papers listed in the references.

## Consequences

- **An explanation of practice.** The simplex method is exponential in the worst case but polynomial on every slightly noisy version of every program. Since real data come with noise, this is the first theorem that matches the experience of six decades of practice.
- **Short paths on perturbed polytopes.** The shadow path is a path in the graph of the polytope, so a perturbed polytope has, with high probability, a short path between the two vertices that the method connects. This is a random version of the [Hirsch question](/hirsch-conjecture/).
- **A new measure of complexity.** The same model was applied to many other algorithms, such as [the k-means method](/lloyds-algorithm/), local search and condition numbers, and Spielman and Teng received the Gödel Prize in 2008 for it.
- **Average-case results as special cases.** Borgwardt (1982) had shown that the shadow-vertex method is polynomial on average for programs whose rows are drawn from a rotation-symmetric distribution. Smoothed analysis is stronger, since it covers every center $\bar A$, not only the zero matrix.

## Tightness

- **The noise is needed.** At $\sigma = 0$ the theorem would say that the simplex method is polynomial in the worst case, which is false for all classical rules, and is false for the shadow-vertex rule too.
- **The dependence on $\sigma$.** Huiberts, Lee and Zhang (2023) proved the first lower bound for the shadow-vertex rule: there are programs on which it needs $\Omega(\min(\sigma^{-1/2} d^{-1/2} \log^{-1/4} d,\ 2^d))$ pivots with high probability. So a polynomial dependence on $1/\sigma$ cannot be removed, and for $\sigma$ near $0$ the count can be exponential in $d$.
- **Only some rules are covered.** The theorem is about the shadow-vertex rule. No smoothed polynomial bound is known for [Dantzig's rule](/dantzig-pivot-rule/), [steepest edge](/steepest-edge-pivot-rule/) or the other rules of production codes.

## History

Borgwardt (1977, published in 1982) and Smale (1983) gave the first average-case analyses of the simplex method, for special random models. Spielman and Teng presented smoothed analysis at STOC 2001 and published the full proof in the Journal of the ACM in 2004. Vershynin (2009) improved the dependence on $n$ to polylogarithmic, Dadush and Huiberts (STOC 2018, SIAM Journal on Computing 2020) gave a much shorter proof with a better bound, and Huiberts, Lee and Zhang (2023) improved the dependence on $\sigma$ and gave the first lower bound.

## References
