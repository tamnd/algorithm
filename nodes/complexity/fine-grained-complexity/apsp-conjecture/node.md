---
tag: NDJDBF
kind: concept
slug: apsp-conjecture
name: All-Pairs Shortest Paths conjecture
aliases:
- APSP hypothesis
- APSP conjecture
area: complexity/fine-grained-complexity
level: advanced
summary: "The hypothesis that APSP on n-vertex graphs with integer weights in a polynomial range has no O(n^(3-e)) algorithm. A preprint from October 2026 refutes it with an O(n^2.9995) algorithm."
prereqs: [all-pairs-shortest-paths, word-ram, conditional-lower-bound]
see_also: [apsp-negative-triangle-equivalence, negative-triangle, min-plus-matrix-multiplication, 3sum-conjecture, zero-k-clique-hypothesis, fine-grained-equivalence-class, floyd-warshall, omv-conjecture]
sources:
  - paper: doi:10.1109/FOCS.2014.53
    title: "Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014), 434-443"
    locator: Conjecture 2 (the APSP conjecture, weights in {1, ..., n^c}, n^(3-o(1)) expected time on the word RAM)
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the introduction (the problems that are subcubic equivalent to APSP)
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on the APSP hypothesis and the APSP class
  - paper: doi:10.1137/0205006
    title: "Michael L. Fredman, New bounds on the complexity of the shortest path problem, SIAM Journal on Computing 5(1), 1976, 83-89"
    locator: the decision trees of depth O(n^2.5) for the min-plus product and the first algorithm with a log-factor saving
  - paper: doi:10.1137/15M1024524
    title: "R. Ryan Williams, Faster all-pairs shortest paths via circuit complexity, SIAM Journal on Computing 47(5), 2018, 1965-1985 (conference version in STOC 2014)"
    locator: the main theorem (APSP in n^3 / 2^(Omega(sqrt(log n))) time, randomized); this page relies on the journal version
  - paper: doi:10.1145/3402926
    title: "Timothy M. Chan and R. Ryan Williams, Deterministic APSP, orthogonal vectors, and more: quickly derandomizing Razborov-Smolensky, ACM Transactions on Algorithms 17(1), 2021 (conference version in SODA 2016, 1246-1255)"
    locator: the deterministic form of the n^3 / 2^(Omega(sqrt(log n))) algorithm
  - paper: doi:10.1137/0222071
    title: "David R. Karger, Daphne Koller and Steven J. Phillips, Finding the hidden path: time bounds for all-pairs shortest paths, SIAM Journal on Computing 22(6), 1993, 1199-1217"
    locator: the Omega(n^3) lower bound for path-comparison algorithms
  - paper: doi:10.1006/jcss.1995.1078
    title: "Raimund Seidel, On the all-pairs-shortest-path problem in unweighted undirected graphs, Journal of Computer and System Sciences 51(3), 1995, 400-403"
    locator: the O(n^omega log n) algorithm for unweighted undirected graphs
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract, the introduction (the restricted lower bounds of Kerr and of Karger, Koller and Phillips), Theorem 2 and Theorem 22 (APSP in deterministic time O(n^2.9995)), Section 1.2 (the APSP class) and Figure 1 (the hypotheses that are refuted and those that are not); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract and Theorem 4.8 and Corollary 4.9 (deterministic real APSP in O(n^2.9997)); not yet refereed
---

The APSP conjecture, also called the APSP hypothesis, said that [all-pairs shortest paths](/all-pairs-shortest-paths/) has no algorithm that is faster than cubic by a polynomial factor: for every $\varepsilon > 0$, no algorithm computes the distances between all pairs of vertices of an $n$-vertex graph with integer weights in a polynomial range in time $O(n^{3-\varepsilon})$. [Floyd-Warshall](/floyd-warshall/) and many other simple methods take time $n^3$, and fifty years of work saved only factors smaller than any power of $n$. With [SETH](/strong-exponential-time-hypothesis/) and the [3SUM conjecture](/3sum-conjecture/), it was one of the three main hypotheses of fine-grained complexity. Vassilevska Williams and Williams showed in 2010 that it is the same as a conjecture about one [negative triangle](/negative-triangle/), and a long list of graph and matrix problems is equivalent to it.

In October 2026, Alman and Vassilevska Williams posted a preprint with a deterministic $O(n^{2.9995})$ algorithm for APSP with integer weights bounded by a polynomial in $n$. If the preprint is correct, the conjecture is false. This page states the conjecture as it was used, the evidence for it, and what the refutation changes.

## In plain words

You have a map of towns and one-way roads. Each road has a cost, which may be negative, but no round trip has a negative total. You want the cheapest cost from every town to every other town.

The simple methods take a number of steps that grows like the cube of the number of towns. The conjecture was a bet that no method can beat the cube by a real margin. Small savings did not count: a method that divides the cube by a slowly growing amount was allowed. Only a method with a smaller power would break the bet.

Many researchers used the bet to show that other problems are hard. In 2026, a research team posted a paper that claims to beat the cube by a very small power.

## The idea

### Hypothesis (APSP)

For every $\varepsilon > 0$, no algorithm solves APSP on $n$-vertex directed graphs with integer edge weights in $\{-n^{c}, \ldots, n^{c}\}$ and no negative cycle in time $O(n^{3-\varepsilon})$.

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, so each weight and each sum of $n$ weights fits in $O(1)$ words.
- The numbers are integers with absolute value at most $n^{c}$ for a constant $c$. Abboud and Vassilevska Williams (FOCS 2014, Conjecture 2) use weights in $\{1, \ldots, n^{c}\}$. The two forms are equivalent: both are equivalent to the [min-plus product](/min-plus-matrix-multiplication/), and adding $M$ to every entry of a min-plus product with entries in $\{-M, \ldots, M\}$ makes the entries nonnegative and adds $2M$ to every entry of the result.
- Randomized algorithms are excluded too: Abboud and Vassilevska Williams state the bound for expected time.
- Directed and undirected graphs give equivalent forms (Vassilevska Williams and Williams 2010).

The weight range is part of the statement. For small weights, APSP is not cubic: Seidel (1995) solves unweighted undirected APSP in time $O(n^{\omega} \log n)$, where $\omega < 2.371552$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/), and the min-plus product with entries in $\{-M, \ldots, M\}$ takes time $\tilde{O}(M n^{\omega})$.

### Equivalent forms

By the [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/), the following statements are all equivalent to the conjecture, for weights in a polynomial range. Each equivalence is a pair of deterministic subcubic reductions, and is unconditional:

- The min-plus product of two $n \times n$ matrices has no $O(n^{3-\varepsilon})$ algorithm.
- [Negative triangle](/negative-triangle/) detection in an $n$-vertex graph has no $O(n^{3-\varepsilon})$ algorithm.
- The same holds for the verification of a min-plus product, metricity, replacement paths and the second shortest simple path (Vassilevska Williams and Williams), minimum weight cycle (Roditty and Vassilevska Williams 2011), and radius, median and betweenness centrality (Abboud, Grandoni and Vassilevska Williams 2015).

### Evidence before 2026

- **Log-factor savings only.** Fredman (1976) gave the first algorithm with time $o(n^3)$, with a saving of $(\log n / \log \log n)^{1/3}$. After many further log-factor savings, Williams (STOC 2014, SIAM J. Comput. 2018) gave a randomized algorithm in time $n^3 / 2^{\Omega(\sqrt{\log n})}$, with the polynomial method of circuit complexity. Chan and Williams (SODA 2016) made it deterministic. None of these is $O(n^{3-\varepsilon})$.
- **Restricted models.** Kerr (1970) showed that straight-line programs over min and plus need $n^3$ operations for the min-plus product. Karger, Koller and Phillips (1993) proved $\Omega(n^3)$ for path-comparison algorithms. These bounds are unconditional but hold only in their models.
- **Decision trees beat the cube.** Fredman (1976) also showed that the min-plus product has decision trees of depth $O(n^{2.5})$. So no cubic lower bound can be proved in the general decision tree model, and the conjecture was about uniform algorithms only.

### Status in 2026

Alman and Vassilevska Williams (arXiv:2610.06783, 5 October 2026) give these results; the paper is not yet refereed:

- APSP on directed graphs with integer weights of absolute value at most $n^{O(1)}$ and no negative cycle, and the min-plus product, on the word RAM in deterministic time $O(n^{2.9995})$ (Theorem 2; the exponent is $3 - 1/1944$ in Theorem 22). This is unconditional: it refutes the conjecture, even in its deterministic form.
- APSP with real weights in expected time $O(n^{2.998})$, Las Vegas, with only comparisons, additions and subtractions on the weights. Chan, Itakura, Ma and Yu (arXiv:2610.42012, 30 October 2026, not yet refereed) give a deterministic algorithm for real APSP in time $O(n^{2.9997})$.
- The core step is exact triangle in deterministic time $O(n^{2.9983})$. The reduction from the min-plus product to a triangle problem then gives the APSP bound, with the loss of a factor 3 in the saving.
- Every member of the APSP class above has a truly subcubic algorithm too. Directed unweighted APSP gets a polynomial speedup over Zwick's algorithm (their Theorem 34).

The paper states that Claude, an AI model made by Anthropic, discovered the algorithm, and that Claude also verified the main results in the Lean 4 proof assistant with the Mathlib library.

What still stands:

- The bounds in restricted models: Kerr's bound for straight-line programs and the bound of Karger, Koller and Phillips for path-comparison algorithms. The new algorithm is algebraic, so it is outside these models.
- SETH, the [OV hypothesis](/orthogonal-vectors-hypothesis/) and the plain [OMv conjecture](/omv-conjecture/). Alman and Vassilevska Williams state that their algorithms do not affect them.
- The [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/). The new algorithms are algebraic, and the preprint states that no truly subcubic combinatorial algorithm for Boolean matrix multiplication is known.
- The true exponent of APSP. No lower bound of the form $n^{2+\delta}$ is known in any general model.
- Problems that were only APSP-hard, with a reduction from APSP to them but none back. A fast APSP algorithm does not make them fast; their exponent is now open.

### Relation to the other hypotheses

- **SETH.** The APSP conjecture was not known to follow from SETH. Carmosino et al. (ITCS 2016) showed that, under NSETH, there is no deterministic fine-grained reduction from SAT to APSP. Alman and Vassilevska Williams note that, now, a deterministic fine-grained reduction from CNF-SAT or OV to APSP would refute SETH.
- **3SUM.** No reduction was known between 3SUM and APSP in either direction. Both reduce to exact triangle, the case $k = 3$ of the [zero-k-clique hypothesis](/zero-k-clique-hypothesis/), so the hypothesis for exact triangle was weaker than both. The 2026 preprint refutes all three.
- **Min-weight k-clique.** The [min-weight k-clique hypothesis](/min-weight-k-clique-hypothesis/) for $k = 3$ is the min-weight triangle form, which is equivalent to APSP. The preprint refutes it for every $k \ge 3$.

### Pitfalls

- A conditional lower bound did not prove that a problem needs cubic time. It said only that a fast algorithm would refute the conjecture. The reductions still hold, but a fast algorithm for an APSP-hard problem would now give nothing new.
- The weight range matters. A bound for weights up to $n^{c}$ says nothing about unweighted graphs, where $O(n^{\omega} \log n)$ algorithms exist for undirected graphs.
- Dense against sparse. The conjecture is about $n$-vertex graphs with up to $n^2$ edges. For sparse graphs with $m$ edges, Dijkstra's algorithm from every vertex gives $\tilde{O}(mn)$ time with nonnegative weights, and the right hypotheses are different.
- The 2026 results are preprints. Until they are refereed, name the preprint when you say that the conjecture is refuted.

## Examples

**How small the gain is.** The exponent $2.9995$ beats 3 by $0.0005$. For $n = 10^6$ the factor $n^{0.0005}$ is about $1.0069$, and for $n = 10^9$ it is about $1.0104$. These are results about the exponent, not about practical speed.

**Why the Williams bound did not count.** Williams saves a factor $2^{\Omega(\sqrt{\log n})}$. With the constant 1 in the $\Omega$, at $n = 2^{64}$ this is $2^{8} = 256$, while $n^{0.0005} = 2^{0.032} \approx 1.022$. The two meet at $\log_2 n = 1/0.0005^2 = 4{,}000{,}000$, and only beyond that does the polynomial saving win. In the limit any polynomial factor wins, and that is what the conjecture was about.

**What a conditional bound now says.** Before 2026, the equivalence gave: negative triangle has no $O(n^{3-\varepsilon})$ algorithm, conditional on the APSP conjecture. If the preprint is correct, the reduction from negative triangle to the min-plus product gives a deterministic $O(n^{2.9995})$ algorithm for negative triangle instead. For a problem with a reduction from APSP only, the old bound simply goes away: it says that a fast algorithm for the problem gives a fast APSP algorithm, which is now known to exist.

## Where it is used

- **[The APSP class](/fine-grained-equivalence-class/).** Min-plus product, negative triangle, metricity, replacement paths, second shortest simple path, minimum weight cycle, radius, median and betweenness centrality are all equivalent to APSP. See [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/).
- **[Dynamic lower bounds](/dynamic-lower-bounds/).** Abboud and Vassilevska Williams (FOCS 2014) used the conjecture, together with 3SUM, triangle detection and SETH, for lower bounds on dynamic graph problems. Bounds that also follow from the OMv conjecture keep their base.
- **[Conditional lower bounds](/conditional-lower-bound/) for problems that are only APSP-hard.** These are the bounds that the 2026 preprint removes without replacing them.
- **[Min-plus convolution](/min-plus-convolution/) and knapsack.** The one-dimensional analog has its own hypothesis, which the same preprint refutes.

## References
