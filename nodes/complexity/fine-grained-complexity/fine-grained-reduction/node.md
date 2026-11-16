---
tag: Q2QQEM
kind: technique
slug: fine-grained-reduction
name: Fine-grained reduction
aliases:
- fine-grained reduction
area: complexity/fine-grained-complexity
level: core
summary: "A reduction from A to B such that saving a power in the time for B saves a power in the time for A. It transfers exact exponents such as n^2 or 2^n, not only polynomial time."
prereqs: [polynomial-time-reduction, turing-reduction, conditional-lower-bound]
see_also: [reduction-lower-bound, fine-grained-equivalence-class, seth-implies-ov-lower-bound, apsp-negative-triangle-equivalence, 3sum-hardness, min-plus-matrix-multiplication, gadget-reduction, parameterized-reduction]
sources:
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the definition of an (a, b)-fine-grained reduction and the survey of reductions from SETH, 3SUM and APSP
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010)"
    locator: the definition of subcubic reductions and the equivalences between APSP, min-plus product and negative triangle
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the split-and-list reduction from CNF-SAT to orthogonal vectors
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma and subexponential reduction families (SERF reductions)
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995, 165-185"
    locator: the definition of 3SUM-hard problems and the reduction from 3SUM to three collinear points
  - paper: doi:10.1145/2488608.2488673
    title: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515-524"
    locator: the reduction from orthogonal vectors to telling diameter 2 from diameter 3 in sparse graphs
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 375-388"
    locator: the consequences of saving polylogarithmic factors for edit distance and LCS
  - paper: doi:10.1145/2840728.2840746
    title: "Marco L. Carmosino, Jiawei Gao, Russell Impagliazzo, Ivan Mihajlin, Ramamohan Paturi and Stefan Schneider, Nondeterministic extensions of the strong exponential time hypothesis and consequences for non-reducibility, ITCS 2016, 261-270"
    locator: NSETH and the limits of deterministic fine-grained reductions from SAT to 3SUM and APSP
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract (integer 3SUM in deterministic O(n^1.9992) time), Theorem 2 (APSP in deterministic O(n^2.9995) time) and the introduction (the list of affected hypotheses; SETH, OV and plain OMv are not affected); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract (a randomized O(n^1.965) integer 3SUM algorithm); not yet refereed
---

A fine-grained reduction from a problem $A$ to a problem $B$ solves $A$ with calls to an algorithm for $B$, so that any saving of a fixed power in the running time of $B$ gives a saving of a fixed power in the running time of $A$. Each reduction names two time bounds: $a(n)$, the conjectured time for $A$, and $b(n)$, the conjectured time for $B$. Reductions of this kind give every [conditional lower bound](/conditional-lower-bound/) of fine-grained complexity, such as the quadratic bounds for orthogonal vectors and edit distance under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/).

A [Karp reduction](/polynomial-time-reduction/) only needs polynomial time, and a [Cook reduction](/turing-reduction/) may make polynomially many calls. Both are too coarse here: a reduction that takes time $n^2$ says nothing about whether $B$ needs time $n^2$. A fine-grained reduction counts the exponents. The [lower bound by reduction](/reduction-lower-bound/) is the same idea for unconditional bounds in a restricted model.

## In plain words

You believe that one job, call it the old job, cannot be done much faster than a known time. You want to show the same for a new job. So you write a method for the old job that does a little work of its own and asks a fast helper for the new job some questions.

Two things must hold. The work of your own must be clearly smaller than the known time for the old job. And all the questions together must cost little, if the helper is a bit faster than expected. Then a helper that saves any fixed power of time would also save a fixed power of time on the old job, which you believe is impossible.

The counting must be exact. A method that spends as much time as the known bound proves nothing.

## When it applies

- You have a source problem $A$ with a hypothesis "no $O(a(n)^{1-\varepsilon})$ algorithm for any $\varepsilon > 0$", such as SETH with $a(N) = 2^N$, the [OV hypothesis](/orthogonal-vectors-hypothesis/) or the [3SUM conjecture](/3sum-conjecture/) with $a(n) = n^2$, or the [APSP conjecture](/apsp-conjecture/) with $a(n) = n^3$.
- The target problem $B$ has a simple algorithm with time $b(n)$, and you want to show that it cannot be improved by a fixed power.
- An instance of $A$ can be split into parts and each part encoded as an instance of $B$, with little growth in size and in time well below $a(n)$.
- The model is the [word RAM](/word-ram/) with words of $O(\log n)$ bits, unless the hypothesis names another model, such as the real RAM for real 3SUM.

## The template

**Definition (Vassilevska Williams).** Let $a$ and $b$ be non-decreasing functions. $A$ is $(a, b)$-reducible to $B$ if for every $\varepsilon > 0$ there is a $\delta > 0$ and an algorithm $R$ for $A$ with an oracle for $B$ such that, on inputs of size $n$, $R$ runs in time $O(a(n)^{1-\delta})$ outside the oracle, and its calls have sizes $n_1, \ldots, n_q$ with

$$\sum_{i=1}^{q} b(n_i)^{1-\varepsilon} \ \le\ a(n)^{1-\delta}.$$

The reduction is **deterministic** if $R$ is, and **randomized** if $R$ uses random bits and errs with probability at most $1/3$. The order of the quantifiers matters: $\delta$ may depend on $\varepsilon$, and $R$ may depend on $\varepsilon$.

```pseudo id=template
SOLVE-A(x)                         ▷ x an instance of A of size n
L1  (x_1, ..., x_q) ← SPLIT(x)       ▷ time a(n)^(1-δ); q may be 1
L2  for i ← 1 to q do
L3      y_i ← ENCODE(x_i, z_1, ..., z_(i-1))   ▷ an instance of B of size n_i
L4      z_i ← SOLVE-B(y_i)           ▷ the oracle; time b(n_i)^(1-ε)
L5  return COMBINE(x, z_1, ..., z_q) ▷ time a(n)^(1-δ)
```

The holes are SPLIT, ENCODE and COMBINE, and the sizes $n_i$. ENCODE may use the earlier answers, so the calls may be adaptive. The budget on line L4 is the sum in the definition.

**Lemma (transfer).** If $A$ is $(a, b)$-reducible to $B$ and $B$ has an algorithm with time $O(b(n)^{1-\varepsilon})$ for some $\varepsilon > 0$, then $A$ has an algorithm with time $O(a(n)^{1-\delta})$ for some $\delta > 0$.

*Proof.* Take the $\delta$ and the algorithm $R$ that the definition gives for this $\varepsilon$. Replace each oracle call by the algorithm for $B$. Lines L1, L3 and L5 take $O(a(n)^{1-\delta})$ time, and line L4 takes $O\bigl(\sum_i b(n_i)^{1-\varepsilon}\bigr) = O(a(n)^{1-\delta})$ time over all calls. If $R$ is randomized, the result is a randomized algorithm with the same error. $\square$

So, conditional on the hypothesis for $A$, $B$ has no $O(b(n)^{1-\varepsilon})$ algorithm for any $\varepsilon > 0$. If the reduction is randomized, this rules out deterministic algorithms for $B$ only if the hypothesis for $A$ rules out randomized algorithms.

## Classic examples

Each example fills the holes and gives $a$, $b$, the sizes and whether it is randomized.

### CNF-SAT to orthogonal vectors

Williams (2005). $a(N) = 2^N$ for CNF-SAT with $N$ variables, and $b(n) = n^2$ for OV with $n$ vectors. Deterministic.

- **SPLIT:** apply the sparsification lemma of Impagliazzo, Paturi and Zane, which writes a $k$-CNF formula as the disjunction of $2^{\varepsilon' N}$ formulas with $O(N)$ clauses each, in time $2^{\varepsilon' N} \mathrm{poly}(N)$. Then split the variables of each formula into two halves.
- **ENCODE:** one vector for each assignment to each half, one coordinate for each clause; the coordinate is 1 when the half assignment makes no literal of the clause true. Two vectors are orthogonal if and only if the two half assignments together satisfy every clause. This gives $n = 2^{N/2}$ vectors of dimension $O(N) = O(\log n)$.
- **COMBINE:** the formula is satisfiable if and only if some call finds an orthogonal pair.

The calls cost $2^{\varepsilon' N} (2^{N/2})^{2(1-\varepsilon)} = 2^{(1 - \varepsilon + \varepsilon') N}$, times factors polynomial in $N$, so $\varepsilon' = \varepsilon/2$ makes any $\delta < \varepsilon/2$ work. The dimension depends on $\varepsilon'$, which is why the [OV hypothesis](/orthogonal-vectors-hypothesis/) says "for every $\varepsilon$ there is a $c$". The full proof is on [SETH implies the OV lower bound](/seth-implies-ov-lower-bound/).

### Orthogonal vectors to the diameter of a sparse graph

Roditty and Vassilevska Williams (2013). $a(n) = n^2$ for OV with $d = c \log n$, and $b(m) = m^2$ for the diameter of a graph with $m$ edges, where the simple algorithm runs breadth-first search from every vertex. Deterministic, one call.

- **SPLIT:** none; $q = 1$.
- **ENCODE:** a vertex for each vector of $A$ and of $B$, a vertex for each coordinate, and two vertices $x$ and $y$. Join each vector to its coordinates with value 1, $x$ to all of $A$ and all coordinates, $y$ to all of $B$ and all coordinates, and $x$ to $y$. The graph has $2n + d + 2$ vertices and at most $2nd + 2n + 2d + 1$ edges.
- **COMBINE:** answer yes if the diameter is 3, no if it is 2.

A vector of $A$ and a vector of $B$ are at distance 3 if they are orthogonal and at distance 2 otherwise; every other pair is at distance at most 2. With $n = 3$ and $d = 5$, the example on the [orthogonal vectors](/orthogonal-vectors/) page gives a graph with 13 vertices and 34 edges (the bound is 47) and diameter 3. Since $m = O(n \log n)$, the call costs $m^{2(1-\varepsilon)} = n^{2 - 2\varepsilon + o(1)}$. As the gap is between 2 and 3, the same reduction shows that, conditional on SETH, no algorithm with time $O(m^{2-\varepsilon})$ approximates the diameter within a factor below $3/2$.

### 3SUM to three collinear points

Gajentaan and Overmars (1995). $a(n) = b(n) = n^2$. Deterministic, one call of size $n$.

- **ENCODE:** map each integer $s$ to the point $(s, s^3)$.
- **COMBINE:** return the answer as it is.

The slope between $(a, a^3)$ and $(b, b^3)$ is $a^2 + ab + b^2$, and for distinct $a, b, c$ the three points lie on a line if and only if $a + b + c = 0$. For $S = \{-7, -3, 2, 5, 9\}$, the only triple with sum 0 is $-7, 2, 5$, and the only collinear triple of points is $(-7, -343)$, $(2, 8)$, $(5, 125)$, where all three slopes are 39. A check of all triples of distinct integers in $[-12, 12]$ found no exception. For integers in a polynomial range, the coordinates have $O(\log n)$ bits, so the reduction runs on the word RAM. See [3SUM-hardness](/3sum-hardness/) and [collinear points](/collinear-points/).

### Min-plus product and all-pairs shortest paths

Vassilevska Williams and Williams. $a(n) = b(n) = n^3$, where $n$ is the number of rows or of vertices. Both directions are deterministic.

**Min-plus product to APSP**, one call. The min-plus product of $n \times n$ matrices $A$ and $B$ is $C[i][k] = \min_j (A[i][j] + B[j][k])$; see [min-plus matrix multiplication](/min-plus-matrix-multiplication/).

- **ENCODE:** a directed graph with three layers $I$, $J$ and $K$ of $n$ vertices each, an edge $i \to j$ of weight $A[i][j]$ and an edge $j \to k$ of weight $B[j][k]$. It has $3n$ vertices and $2n^2$ edges, and no cycle, so negative weights are allowed.
- **COMBINE:** $C[i][k]$ is the distance from $i$ to $k$.

For $n = 3$, a run with $A = [[0, -3, 1], [5, -5, -4], [8, 3, -4]]$ and $B = [[0, 4, -5], [9, 3, -2], [-5, -4, 1]]$ gives a graph with 9 vertices and 18 edges, and its distances from layer $I$ to layer $K$ are $C = [[-4, -3, -5], [-9, -8, -7], [-9, -8, -3]]$, the min-plus product.

**APSP to min-plus product**, by repeated squaring. Let $D$ be the weight matrix with zeros on the diagonal. The min-plus power $D^{\ell}$ gives the shortest paths with at most $\ell$ edges, so $\lceil \log_2(n-1) \rceil$ squarings give $D^{n-1}$, the distances. The calls cost $\lceil \log_2 n \rceil\, n^{3(1-\varepsilon)} \le n^{3 - 2\varepsilon}$ for large $n$, so $\delta = 2\varepsilon$ works. For $n = 1000$ this is 10 calls. A run on 150 random graphs with 2 to 13 vertices matched the Floyd-Warshall distances.

The two reductions together make APSP and min-plus product equivalent: one has a truly subcubic algorithm if and only if the other has. See [fine-grained equivalence class](/fine-grained-equivalence-class/) and [APSP and negative triangle](/apsp-negative-triangle-equivalence/).

## Variations

- **Different time classes.** $a$ and $b$ may differ. The reduction from CNF-SAT to OV goes from $2^N$ to $n^2$. Reductions from $k$-OV give bounds of the form $n^{k}$, as for the LCS of $k$ strings.
- **Equivalences.** Reductions in both directions with $a = b$ put two problems in one class. The APSP class has many members, among them negative triangle; the [3SUM-hard](/3sum-hardness/) problems are hard but are mostly not known to be equivalent to 3SUM.
- **Randomized reductions.** Many reductions use hashing or random sampling. They transfer bounds only for hypotheses that also rule out randomized algorithms.
- **Exponential time.** Impagliazzo, Paturi and Zane defined SERF reductions (subexponential reduction families) for ETH: for every $\varepsilon > 0$, the reduction runs in time $2^{\varepsilon n} \mathrm{poly}(n)$ and maps an instance with parameter $n$ to instances with parameter $O(n)$, where the constant may depend on $\varepsilon$. This preserves "no $2^{o(n)}$ algorithm" rather than an exact exponent.
- **Gap reductions.** If the instances of $B$ have a gap, as diameter 2 against 3, the reduction also gives a bound for approximation.
- **Limits.** Carmosino et al. (2016) showed that, under NSETH, a nondeterministic form of SETH, there is no deterministic fine-grained reduction from SAT to 3SUM or to APSP with the usual time bounds. So some hypotheses may not be comparable by this technique.

## Pitfalls

- **The wrong direction.** To show that $B$ is hard, reduce the hard problem $A$ to $B$. A reduction from $B$ to $A$ gives an algorithm for $B$, not a bound.
- **The budget.** The work outside the calls must be $O(a(n)^{1-\delta})$. A Karp reduction from OV that takes $\Theta(n^2)$ time is polynomial but proves nothing about quadratic time.
- **The size blow-up.** If an instance of size $n$ becomes an instance of size $N = n^{1+\gamma}$, the bound $n^2$ for $A$ gives only $N^{2/(1+\gamma)}$ for $B$. A reduction from OV to a graph with $n^2$ edges gives no useful bound in the number of edges.
- **The quantifiers.** The OV hypothesis allows the dimension $c \log n$ to depend on $\varepsilon$. A reduction that works only for $d = 2 \log n$ does not reduce from the hypothesis.
- **Log factors.** The definition ignores factors $n^{o(1)}$. A reduction with $N = n \log^2 n$ does not turn an $O(N^2 / \log N)$ algorithm for $B$ into an $O(n^2 / \log n)$ algorithm for $A$. Abboud, Hansen, Vassilevska Williams and Williams (2016) used reductions from branching programs, with smaller overhead, to show that some savings of polylogarithmic factors for edit distance and LCS would still have surprising consequences.
- **The model.** A reduction for real 3SUM uses the real RAM; a reduction on the word RAM must keep numbers of $O(\log n)$ bits.
- **"Truly subquadratic" is not $o(n^2)$.** The conclusion is "no $O(b(n)^{1-\varepsilon})$ for any $\varepsilon > 0$". Algorithms that save a factor $\log n$ are not excluded.
- **A refuted source.** A reduction transfers a bound only while the hypothesis for $A$ stands. In October 2026, Alman and Vassilevska Williams (arXiv:2610.06783) gave a deterministic $O(n^{1.9992})$ algorithm for integer 3SUM and a deterministic $O(n^{2.9995})$ algorithm for APSP, and Chan, Itakura, Ma and Yu (arXiv:2610.42012) gave a randomized $O(n^{1.965})$ algorithm for integer 3SUM. Both preprints are not yet refereed. If they are correct, the reductions from 3SUM and from APSP are still valid, but the bounds they gave no longer hold: a reduction from 3SUM to $B$ now says only that a fast algorithm for $B$ gives a fast algorithm for 3SUM. Reductions to APSP now carry the new algorithm to the reduced problems, such as [negative triangle](/negative-triangle/). Reductions from SETH, from OV and from the plain OMv conjecture are not affected.

## Exercises

1. One-list OV asks whether a set $S$ of $n$ vectors has two orthogonal members. Give fine-grained reductions in both directions between one-list OV and two-list OV with $a(n) = b(n) = n^2$. (Hint: append $10$ to the vectors of one list and $01$ to the other; treat the zero vector apart.)
2. Prove transitivity: if $A$ is $(a, b)$-reducible to $B$ and $B$ is $(b, c)$-reducible to $C$, then $A$ is $(a, c)$-reducible to $C$. Where do you need that $b$ is non-decreasing?
3. A reduction maps OV with $n$ vectors to one instance of $B$ of size $n^{1.5}$, and $B$ has a simple $O(N^2)$ algorithm. What bound for $B$ follows from OVH?
4. Explain why a reduction with polylogarithmic blow-up from OV to edit distance does not show that an $O(N^2 / \log^2 N)$ edit distance algorithm gives an $O(n^2 / \log^2 n)$ OV algorithm.
5. In the reduction from APSP to min-plus product, how many calls are needed for $n = 5$ and for $n = 13$? Check that every power of $D$ with at least $n - 1$ edges equals the distance matrix.
6. In the reduction from CNF-SAT to OV, what goes wrong if you skip the sparsification and a formula has $2^{N/4}$ clauses?

## References
