---
tag: HAPT2H
kind: theorem
slug: motzkin-straus-theorem
name: Motzkin-Straus theorem
area: graphs/coloring-and-cliques
level: research
summary: Relates the clique number to the maximum of a quadratic form over the standard simplex.
prereqs: [clique-number, adjacency-matrix, quadratic-programming]
see_also: [turan-theorem, maximum-clique, lovasz-theta-function, tomita-maximum-clique, kkt-conditions, independence-number]
sources:
  - paper: doi:10.4153/CJM-1965-053-6
    title: T. S. Motzkin and E. G. Straus, Maxima for graphs and a new proof of a theorem of Turán, Canadian Journal of Mathematics 17, 533 to 540 (1965)
    locator: the main theorem and the derivation of Turán's theorem
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: the chapter Turán's graph theorem (the proof by weights on the vertices)
  - paper: "I. M. Bomze, Evolution towards the maximum clique, Journal of Global Optimization 10(2), 143 to 164 (1997)"
    locator: the regularized form with A + I/2, whose local maximizers are exactly the characteristic vectors of maximal cliques
---

The Motzkin-Straus theorem turns the [clique number](/clique-number/) of a graph into the optimum of a continuous problem: for the [adjacency matrix](/adjacency-matrix/) $A$ of a graph $G$, the largest value of $x^{\mathsf T} A x$ over all nonnegative vectors $x$ with entries summing to 1 is $1 - 1/\omega(G)$. It gives a short proof of [Turán's theorem](/turan-theorem/). It also shows that maximizing a quadratic form over the simplex is NP-hard, since it would compute $\omega(G)$, and it is the starting point of continuous heuristics for [maximum clique](/maximum-clique/).

## Statement

Let $G$ be a simple graph with vertices $1, \ldots, n$, $n \ge 1$, and adjacency matrix $A$. Let

$$\Delta_n = \{\, x \in \mathbb{R}^n : x_i \ge 0, \ \textstyle\sum_i x_i = 1 \,\}$$

be the standard simplex, and $f(x) = x^{\mathsf T} A x = 2 \sum_{ij \in E} x_i x_j$.

**Theorem (Motzkin and Straus 1965).**

$$\max_{x \in \Delta_n} f(x) = 1 - \frac{1}{\omega(G)}.$$

The maximum is attained at the vector that is $1/\omega$ on the vertices of a maximum clique and 0 elsewhere.

## In plain words

Spread one unit of weight over the vertices of a graph. Each edge scores the product of the weights at its two ends. How should the weight be spread to make the total score as large as possible?

The answer is: put equal weight on the vertices of a largest group of mutually linked vertices and nothing elsewhere. Weight on two unlinked vertices is wasted, because moving it from one to the other never lowers the score. So a hard counting question about groups becomes a question about the best way to spread weight.

## Proof

**Lower bound.** Let $K$ be a clique of size $\omega = \omega(G)$ and $x_i = 1/\omega$ for $i \in K$, $x_i = 0$ otherwise. Every ordered pair of distinct vertices of $K$ is an edge, so $f(x) = \omega(\omega - 1)/\omega^2 = 1 - 1/\omega$.

**Upper bound.** $f$ is continuous and $\Delta_n$ is compact, so $f$ has a maximizer on $\Delta_n$. Among all maximizers, choose $x$ with the fewest nonzero entries, and let $S$ be its support.

*$S$ is a clique.* Suppose $i, j \in S$ are distinct and not adjacent. For real $t$, let $y(t) = x + t(e_i - e_j)$; it stays in $\Delta_n$ for $-x_i \le t \le x_j$. Then

$$f(y(t)) = f(x) + 2t\big((Ax)_i - (Ax)_j\big) + t^2 \big(A_{ii} + A_{jj} - 2A_{ij}\big),$$

and $A_{ii} = A_{jj} = A_{ij} = 0$, so $f(y(t))$ is linear in $t$. A linear function on an interval is maximized at an end, so $f(y(t)) \ge f(x)$ at $t = x_j$ or at $t = -x_i$. Both ends have one fewer nonzero entry than $x$, and the value is at least the maximum, so it equals it. This contradicts the choice of $x$.

*The value on a clique.* Let $s = |S| \le \omega$. Since $S$ is a clique, $f(x) = \sum_{i \ne j \in S} x_i x_j = \big(\sum_{i \in S} x_i\big)^2 - \sum_{i \in S} x_i^2 = 1 - \sum_{i \in S} x_i^2$. By the Cauchy-Schwarz inequality, $\sum_{i \in S} x_i^2 \ge 1/s$, so $f(x) \le 1 - 1/s \le 1 - 1/\omega$. $\blacksquare$

## Consequences

- **Turán's theorem.** Take $x$ uniform, $x_i = 1/n$. Then $f(x) = 2m/n^2 \le 1 - 1/\omega$, so a graph with no $K_{r+1}$ has $m \le (1 - \frac1r)\frac{n^2}{2}$ edges. This is the proof by weights in Aigner and Ziegler.
- **Hardness of quadratic programming.** Maximizing a quadratic form over the simplex, the *standard quadratic program*, computes $\omega(G)$, so it is NP-hard, and it inherits the inapproximability of maximum clique. So [quadratic programming](/quadratic-programming/) with an indefinite matrix is NP-hard even with the simplest constraints.
- **Continuous heuristics for cliques.** Local search on $f$, for example replicator dynamics $x_i \leftarrow x_i (Ax)_i / f(x)$, finds local maximizers whose supports are cliques after the step of the proof. Such heuristics find large cliques in practice but give no guarantee.
- **Independent sets.** Applied to the complement, $\min_{x \in \Delta_n} x^{\mathsf T}(I + A_G) x = 1/\alpha(G)$, which links the [independence number](/independence-number/) to a convex-looking but nonconvex program.
- **Weighted and hypergraph versions.** Similar statements hold for vertex weights and, with more care, for the Lagrangians of hypergraphs, which are a tool in hypergraph Turán problems.

## Tightness

The value $1 - 1/\omega$ is exact for every graph, by the lower bound. But a maximizer need not be the uniform vector on a clique. For the path $a - b - c$, $\omega = 2$, and every $x = (t, \frac12, \frac12 - t)$ with $0 \le t \le \frac12$ has $f(x) = 2 \cdot \frac12 (t + \frac12 - t) = \frac12$, the maximum, although for $0 < t < \frac12$ its support $\{a, b, c\}$ is not a clique. So the theorem recovers $\omega$ from the maximum value, but recovering a clique needs the support-reduction step of the proof.

Bomze (1997) removed these spurious solutions by maximizing $x^{\mathsf T}(A + \frac12 I)x$ instead: its maximum over the simplex is $1 - \frac{1}{2\omega}$, and its local maximizers are exactly the uniform vectors on maximal cliques, with global maximizers on maximum cliques.

For the 5-cycle, the maximum is $\frac12$ at the uniform vector on an edge, while the uniform vector on all 5 vertices gives only $\frac{10}{25} = \frac25$: spreading the weight more evenly is not better.

## History

Theodore Motzkin and Ernst Straus published the theorem in 1965 as "a new proof of a theorem of Turán". The continuous view of cliques was later used for heuristics based on evolutionary game dynamics, and Bomze's regularization in 1997 made the correspondence between local maximizers and maximal cliques exact.

## References
