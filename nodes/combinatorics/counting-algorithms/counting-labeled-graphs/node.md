---
tag: 9XNY9K
kind: problem
slug: counting-labeled-graphs
name: Counting labeled graphs
aliases:
- number of labeled graphs
- labeled graph enumeration
area: combinatorics/counting-algorithms
level: core
summary: Count the simple graphs on the vertex set [n]. The answer is 2^(n choose 2), and with exactly m edges it is the binomial coefficient of n choose 2 over m.
prereqs: [labeled-graph, binomial-coefficient, rule-of-product]
see_also: [counting-connected-labeled-graphs, counting-labeled-graphs-with-k-components, counting-labeled-bipartite-graphs, cayley-formula, polya-enumeration-theorem, exponential-generating-functions, erdos-renyi-model, graph-generation]
sources:
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 1, Labeled enumeration (graphs, digraphs, connected graphs and the exponential generating function), and Chapter 4 (unlabeled graphs)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (labelled graphs and the set construction)
  - url: https://oeis.org/A006125
    title: OEIS A006125, a(n) = 2^(n*(n-1)/2)
    locator: the data, and the comments on the number of labeled graphs
---

Counting labeled graphs asks for the number of simple undirected graphs whose vertex set is $[n] = \{1, \ldots, n\}$. Each of the $\binom{n}{2}$ possible edges is present or absent on its own, so the answer is $2^{\binom{n}{2}}$, and with exactly $m$ edges it is $\binom{\binom{n}{2}}{m}$. The problem is easy, but it is the base of the harder counts of [connected](/counting-connected-labeled-graphs/), [$k$-component](/counting-labeled-graphs-with-k-components/) and [bipartite](/counting-labeled-bipartite-graphs/) labeled graphs, which all start from this number and its [exponential generating function](/exponential-generating-functions/).

## In plain words

Draw a fixed set of numbered points. Between each two points you may draw a line or not. A graph is one complete set of these choices. Two drawings are different graphs if some pair of points is joined in one and not in the other, even when the two pictures look alike after a renaming of the points.

Each pair of points is one yes or no choice, and the choices do not depend on each other. So the number of graphs is two multiplied by itself once for each pair of points. This grows very fast: ten points already give more than thirty trillion graphs.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $\binom{[n]}{2}$ is the set of 2-element subsets of $[n]$, and $C(n, k) = \binom{n}{k}$.

A *labeled graph* on $[n]$ is a pair $([n], E)$ with $E \subseteq \binom{[n]}{2}$. Two labeled graphs are equal when their edge sets are equal.

**Problem.** Input: an integer $n \ge 0$, and optionally an integer $m \ge 0$. Output: the number $g_n$ of labeled graphs on $[n]$, or the number $g_{n,m}$ of those with $|E| = m$.

**Answer.** For every $n \ge 0$ and $m \ge 0$,

$$g_n = 2^{\binom{n}{2}}, \qquad g_{n,m} = \binom{\binom{n}{2}}{m}, \qquad \sum_{m \ge 0} g_{n,m} = g_n.$$

*Proof.* The map $E \mapsto$ (the indicator vector of $E$) is a bijection from labeled graphs on $[n]$ to binary vectors indexed by the $\binom{n}{2}$ pairs, and there are $2^{\binom{n}{2}}$ such vectors by the [rule of product](/rule-of-product/). The graphs with $m$ edges are the $m$-element subsets of $\binom{[n]}{2}$, counted by the [binomial coefficient](/binomial-coefficient/). The last identity is the [binomial theorem](/binomial-theorem/) at $x = y = 1$. $\square$

## Variants

| objects on $[n]$ | count | reason |
|---|---|---|
| simple graphs | $2^{\binom{n}{2}}$ | each pair is an edge or not |
| simple graphs with $m$ edges | $\binom{\binom{n}{2}}{m}$ | choose the edge set |
| graphs with loops allowed | $2^{\binom{n+1}{2}}$ | $n$ more possible edges |
| directed graphs, no loops | $2^{n(n-1)}$ | each ordered pair is an arc or not |
| oriented graphs | $3^{\binom{n}{2}}$ | each pair: no arc, or one of two directions |
| tournaments | $2^{\binom{n}{2}}$ | each pair has exactly one of two directions |
| trees | $n^{n-2}$ for $n \ge 1$ | [Cayley's formula](/cayley-formula/) |
| connected graphs | a recurrence | [counting connected labeled graphs](/counting-connected-labeled-graphs/) |
| graphs with $k$ components | a recurrence | [counting labeled graphs with k components](/counting-labeled-graphs-with-k-components/) |
| bipartite graphs | a recurrence | [counting labeled bipartite graphs](/counting-labeled-bipartite-graphs/) |
| graphs up to isomorphism | the cycle index | [Pólya enumeration theorem](/polya-enumeration-theorem/) |

The labeled and the unlabeled counts differ. A graph on $[n]$ has $n! / |\mathrm{Aut}(G)|$ labeled copies, so the unlabeled count $u_n$ satisfies $g_n / n! \le u_n \le g_n$.

## Examples

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $g_n = 2^{\binom{n}{2}}$ (A006125) | 1 | 1 | 2 | 8 | 64 | 1024 | 32768 | 2097152 | 268435456 |
| unlabeled $u_n$ (A000088) | 1 | 1 | 2 | 4 | 11 | 34 | 156 | 1044 | 12346 |

For $n = 3$, the 8 graphs are the empty graph, 3 graphs with one edge, 3 paths with two edges and the triangle, so $g_{3,m} = 1, 3, 3, 1$. They form 4 classes up to isomorphism. For $n = 4$, $g_{4,m} = \binom{6}{m} = 1, 6, 15, 20, 15, 6, 1$ for $m = 0, \ldots, 6$, which sums to 64, and the 64 graphs form 11 classes. For $n = 10$, $g_{10} = 2^{45} = 35184372088832$.

**A non-example.** Multigraphs, with more than one edge between two vertices, are not counted by $2^{\binom{n}{2}}$; with no bound on the multiplicity there are infinitely many.

## Known algorithms

- **The closed form.** Compute $\binom{n}{2}$ and output $2^{\binom{n}{2}}$, a 1 followed by $\binom{n}{2}$ zeros in binary. This takes $O(n^2)$ bit operations, which is the length of the output, so it is optimal. In decimal the output has $\lfloor \binom{n}{2} \log_{10} 2 \rfloor + 1$ digits, and the conversion to decimal dominates the cost.
- **With $m$ edges.** Compute $\binom{N}{m}$ with $N = \binom{n}{2}$ by the methods of [binomial coefficient computation](/binomial-coefficient-computation/), for example the product $\prod_{i=1}^{m} (N - m + i)/i$ with exact division at each step, in $O(m)$ big-integer operations.
- **Modulo a prime $p$.** Use [modular exponentiation](/modular-exponentiation/) for $2^{\binom{n}{2}} \bmod p$, in $O(\log n)$ multiplications modulo $p$. Reduce the exponent modulo $p - 1$ by Fermat's little theorem when $p$ is odd.
- **Listing.** To list the graphs rather than count them, enumerate the binary vectors of length $\binom{n}{2}$, for example in [Gray code](/gray-code/) order, so that each next graph differs by one edge. To list them up to isomorphism, use the methods of [graph generation](/graph-generation/).

## Bounds

The output has exactly $\binom{n}{2} + 1$ binary digits, so every algorithm that writes $g_n$ in binary needs $\Omega(n^2)$ time, and the closed form meets this bound. For the unlabeled count, the bound $g_n / n! \le u_n$ above is tight up to a factor $1 + o(1)$: almost all labeled graphs have no symmetry other than the identity, so $u_n \sim 2^{\binom{n}{2}} / n!$ as $n \to \infty$. Harary and Palmer give the proof.

## Reductions

- **To connected graphs.** Let $G(x) = \sum_{n \ge 0} 2^{\binom{n}{2}} x^n / n!$, a formal power series. Every graph is a set of connected components, so the EGF of connected graphs is $C(x) = \log G(x)$. The coefficient recurrence is on [counting connected labeled graphs](/counting-connected-labeled-graphs/).
- **To random graphs.** The [Erdős-Rényi model](/erdos-renyi-model/) $G(n, 1/2)$ is the uniform distribution on the $2^{\binom{n}{2}}$ labeled graphs. So the probability that $G(n, 1/2)$ has a property is the number of labeled graphs with the property divided by $g_n$, and each count on this family of pages is also a probability.
- **To the matrix view.** Labeled graphs on $[n]$ are the symmetric 0-1 matrices of order $n$ with zero diagonal.

## Applications

- The base case of the recurrences for connected, $k$-component and bipartite labeled graphs.
- The probabilities of graph properties in $G(n, 1/2)$, for example the probability that a random graph is connected, $c_n / g_n$, which tends to 1.
- The count of the search space in brute-force graph algorithms and in tests that check a property on all graphs of a small order.

## References
