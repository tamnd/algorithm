---
tag: 9YRZTW
kind: problem
slug: counting-labeled-bipartite-graphs
name: Counting labeled bipartite graphs
aliases:
- number of labeled bipartite graphs
- labeled bipartite graph enumeration
- counting 2-colored labeled graphs
area: combinatorics/counting-algorithms
level: core
summary: Problem of counting labeled bipartite graphs on n vertices, using exponential generating functions or recurrences from colored graph counts.
prereqs: [bipartite-graph, counting-labeled-graphs, exponential-generating-functions, binomial-coefficient]
see_also: [counting-connected-labeled-graphs, counting-labeled-graphs-with-k-components, bipartite-odd-cycle-theorem, bipartite-testing, counting-graph-colorings, graph-coloring, power-series-inversion, erdos-renyi-model]
sources:
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 1, Labeled enumeration (bicolored graphs and labeled bipartite graphs)
  - book: isbn:9780521789875
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Section 5.1, The exponential formula
  - url: https://oeis.org/A047864
    title: OEIS A047864, Number of labeled bipartite graphs with n nodes
    locator: the data, and the formula as the square root of the exponential generating function of A047863
  - url: https://oeis.org/A001832
    title: OEIS A001832, Number of labeled connected bipartite graphs on n nodes
    locator: the data and the exponential generating function
---

Counting labeled bipartite graphs asks for the number $b_n$ of [bipartite graphs](/bipartite-graph/) on the vertex set $[n] = \{1, \ldots, n\}$. A bipartite graph can have many 2-colorings, so one cannot just choose a color class and the edges. The fix is to count the easier objects first: *2-colored graphs*, which are a graph together with one proper 2-coloring. There are $t_n = \sum_k \binom{n}{k} 2^{k(n-k)}$ of them. A connected bipartite graph has exactly 2 proper 2-colorings, so in the language of [exponential generating functions](/exponential-generating-functions/) the connected bipartite graphs have the series $\frac12 \log T(x)$, and all bipartite graphs have the series $\sqrt{T(x)}$.

## In plain words

You want to count drawings on numbered points where the points can be split into two teams so that each line joins two points from different teams. Counting these directly is hard, because one drawing can often be split into teams in many ways.

So first count something easier: a drawing together with a choice of teams. Choose the team of each point, then join any pairs from different teams. Now ask how many team choices each drawing has. A drawing in one piece has exactly two, because once you place one point, every other point is forced, and you can swap the two teams. A drawing in several pieces has two choices for each piece. With this fact, you can turn the easy count into the count of drawings in one piece, and then into the count of all the drawings you want.

## Definition

Notation: $[n] = \{1, \ldots, n\}$. A *proper 2-coloring* of a graph on $[n]$ is a map $\chi : [n] \to \{\text{red}, \text{blue}\}$ such that each edge has ends of different colors. A graph is *bipartite* if it has a proper 2-coloring. A *2-colored graph* is a pair $(H, \chi)$ of a graph $H$ on $[n]$ and a proper 2-coloring $\chi$ of $H$.

Let $t_n$ be the number of 2-colored graphs, $b_n$ the number of bipartite graphs, and $a_n$ the number of connected bipartite graphs on $[n]$, with $a_0 = 0$ and $b_0 = t_0 = 1$.

**Problem.** Input: $n \ge 1$ (and optionally a prime $p$). Output: $b_n$, and possibly $a_n$ (or their values modulo $p$).

**Lemma 1.** $t_n = \sum_{k=0}^{n} \binom{n}{k} 2^{k(n-k)}$.

*Proof.* Choose the set of red vertices, of size $k$, in $\binom{n}{k}$ ways. A graph is properly colored by this choice exactly when its edges are among the $k(n-k)$ red-blue pairs, and each subset of these pairs is allowed. $\square$

**Lemma 2.** A bipartite graph with $m$ connected components has exactly $2^m$ proper 2-colorings. So $t_n = \sum_H 2^{\mathrm{comp}(H)}$, over the bipartite graphs $H$ on $[n]$.

*Proof.* In a connected bipartite graph, the color of one vertex fixes the color of every other vertex, since the colors alternate along each path. Both choices for the first vertex give a proper coloring, so there are exactly 2. The components are colored on their own, so the counts multiply. $\square$

**Theorem.** Let $T(x) = \sum_{n \ge 0} t_n x^n / n!$, $A(x) = \sum_{n \ge 1} a_n x^n / n!$ and $B(x) = \sum_{n \ge 0} b_n x^n / n!$, as formal power series. Then

$$T(x) = e^{2A(x)}, \qquad B(x) = e^{A(x)} = \sqrt{T(x)}.$$

*Proof.* A bipartite graph is a set of components, each a connected bipartite graph on its own label set, so $B = e^{A}$ by the exponential formula. A 2-colored graph is a set of components, each a connected bipartite graph with one of its 2 proper colorings (Lemma 2). So the connected 2-colored structures have the series $2A(x)$, and $T = e^{2A}$ by the exponential formula. Then $B^2 = e^{2A} = T$, and $B$ is the square root with constant term 1. $\square$

**Recurrences.** Comparing coefficients gives, for $n \ge 1$,

$$b_n = \frac12 \Big( t_n - \sum_{k=1}^{n-1} \binom{n}{k} b_k \, b_{n-k} \Big), \qquad a_n = \frac12 \Big( t_n - \sum_{k=1}^{n-1} \binom{n-1}{k-1} \, 2 a_k \, t_{n-k} \Big).$$

The first is the coefficient of $x^n / n!$ in $B^2 = T$. The second is the coefficient of $x^{n-1} / (n-1)!$ in $T' = 2A' \, T$, and it is also the split of a 2-colored graph by the component of vertex 1, as on [counting connected labeled graphs](/counting-connected-labeled-graphs/).

## Variants

- **A fixed bipartition.** If the two sides are given, with sizes $k$ and $n - k$, the count is $2^{k(n-k)}$. This is the count of bipartite graphs "with given sides", and it is not the same as $b_n$.
- **With $k$ components.** The connected counts $a_j$ in the recurrence of [counting labeled graphs with k components](/counting-labeled-graphs-with-k-components/) give the bipartite graphs with exactly $k$ components, with series $A(x)^k / k!$.
- **By the number of edges.** Replace $2^{k(n-k)}$ by $(1 + y)^{k(n-k)}$ in Lemma 1. The same square root, taken over polynomials in $y$, counts bipartite graphs by edges, which gives the probability that $G(n, p)$ is bipartite for any $p$.
- **Proper $q$-colorings.** For $q$ colors, the pairs of a graph on $[n]$ and a proper $q$-coloring number $\sum \binom{n}{n_1, \ldots, n_q} 2^{e(n_1, \ldots, n_q)}$, where $e$ is the number of pairs of vertices with different colors. This is the analog of $t_n$; see also [counting graph colorings](/counting-graph-colorings/). For $q \ge 3$ there is no analog of Lemma 2, because the number of proper colorings of a connected graph is not fixed, so the count of $q$-colorable graphs does not follow by a square root.

## Examples

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $t_n$ (A047863) | 1 | 2 | 6 | 26 | 162 | 1442 | 18306 | 330626 | 8488962 | 309465602 | 16011372546 |
| $b_n$ (A047864) | 1 | 1 | 2 | 7 | 41 | 376 | 5177 | 103237 | 2922446 | 116011231 | 6433447397 |
| $a_n$ (A001832) | | 1 | 1 | 3 | 19 | 195 | 3031 | 67263 | 2086099 | 89224635 | 5254054111 |

**The case $n = 3$.** Lemma 1 gives $t_3 = 1 + 3 \cdot 4 + 3 \cdot 4 + 1 = 26$. The bipartite graphs on $[3]$ are all graphs except the triangle: the empty graph, 3 graphs with one edge and 3 paths, so $b_3 = 7$. Lemma 2 checks the count: the empty graph has 3 components and 8 colorings, each one-edge graph has 2 components and 4 colorings, and each path is connected with 2 colorings, so $8 + 3 \cdot 4 + 3 \cdot 2 = 26$. The recurrence gives $b_3 = \frac12 (26 - 3 \cdot 1 \cdot 2 - 3 \cdot 2 \cdot 1) = 7$ and $a_3 = \frac12 (26 - (1 \cdot 2 \cdot 1 \cdot 6 + 2 \cdot 2 \cdot 1 \cdot 2)) = \frac12 (26 - 20) = 3$, the 3 paths.

**The case $n = 4$.** $t_4 = 1 + 32 + 96 + 32 + 1 = 162$, and $b_4 = 41$. On 4 vertices the only odd cycles are triangles, so the other $64 - 41 = 23$ graphs are the graphs that contain a triangle.

## Known algorithms

- **The recurrences.** Compute $t_0, \ldots, t_n$ by Lemma 1 in $O(n^2)$ operations, then $b_1, \ldots, b_n$ and $a_1, \ldots, a_n$ by the recurrences in $O(n^2)$ operations each. With exact integers the numbers have about $n^2/4$ binary digits, which multiplies the cost by the cost of one big-integer product. Modulo an odd prime, the division by 2 is a multiplication by the inverse of 2.
- **Power series.** Modulo a prime $p > n$ that supports [FFT multiplication](/convolution-via-fft/), compute $\sqrt{T}$ or $\frac12 \log T$ by Newton iteration with [power series inversion](/power-series-inversion/). This gives all values up to $n$ in $O(n \log n)$ operations modulo $p$.
- **Listing.** For small $n$, enumerate all $2^{\binom{n}{2}}$ graphs and test each for bipartiteness by [breadth-first 2-coloring](/bipartite-testing/). This is the brute-force check.

## Bounds

For $n \ge 1$,

$$\frac{t_n}{2^n} \le b_n \le \frac{t_n}{2}, \qquad 2^{\lfloor n^2/4 \rfloor} \le t_n \le 2^n \, 2^{\lfloor n^2/4 \rfloor}.$$

*Proof.* By Lemma 2 each bipartite graph has between $2$ and $2^n$ proper colorings, and $t_n$ is the total number of pairs. For the second pair of bounds, the term $k = \lfloor n/2 \rfloor$ in Lemma 1 is at least $2^{\lfloor n^2/4 \rfloor}$, and each of the terms is at most $\binom{n}{k} 2^{\lfloor n^2/4 \rfloor}$, because $k(n-k) \le \lfloor n^2/4 \rfloor$; the binomial coefficients sum to $2^n$. $\square$

So $\log_2 b_n = n^2/4 + O(n)$, while the number of all labeled graphs has $\log_2 g_n = n^2/2 - n/2$. A random labeled graph is bipartite with probability $2^{-n^2/4 + O(n)}$.

## Reductions

- **To 2-colored graphs.** $b_n$ and $a_n$ are determined by $t_0, \ldots, t_n$ through the square root and the logarithm, and $t_n$ has the closed sum of Lemma 1.
- **From connected bipartite graphs.** $b_n$ is the exponential transform of $a_1, \ldots, a_n$, the same transform that turns connected graphs into all graphs.
- **To probabilities.** The probability that the [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, 1/2)$ is bipartite is $b_n / 2^{\binom{n}{2}}$.

## Applications

- The probability that a small random graph is bipartite, or that it has no odd cycle, by the [odd cycle theorem](/bipartite-odd-cycle-theorem/).
- A standard example of the exponential formula where the connected objects have a fixed number of decorations, here two colorings.
- Tests for bipartiteness code: a correct test must accept exactly $b_n$ of the $2^{\binom{n}{2}}$ graphs on $[n]$.

## References
