---
tag: 5RE08B
kind: problem
slug: maximal-independent-set-enumeration
name: Enumeration of maximal independent sets
aliases:
- maximal independent set listing
area: combinatorics/exhaustive-search
level: advanced
summary: List every maximal independent set of a graph.
prereqs: [maximal-independent-set, enumeration-problem, output-sensitive-enumeration]
see_also: [tsukiyama-algorithm, maximal-clique-enumeration, bron-kerbosch, maximal-independent-set, output-sensitive-enumeration, minimal-transversal-enumeration, lawler-chromatic-number, reverse-search]
sources:
  - paper: doi:10.1007/BF02760024
    title: John W. Moon and Leo Moser, On cliques in graphs, Israel Journal of Mathematics 3, 1965, 23 to 28
    locator: the largest number of maximal cliques of a graph with n vertices, 3^(n/3) for n divisible by 3, and the extremal graphs
  - paper: doi:10.1137/0206036
    title: Shuji Tsukiyama, Mikio Ide, Hiromu Ariyoshi and Isao Shirakawa, A new algorithm for generating all the maximal independent sets, SIAM Journal on Computing 6(3), 1977, 505 to 517
    locator: listing all maximal independent sets in O(nmμ) time and O(n + m) space
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 1988, 119 to 123
    locator: polynomial delay in lexicographic order, and no polynomial delay in reverse lexicographic order unless P = NP
  - paper: "Etsuji Tomita, Akira Tanaka and Haruhisa Takahashi, The worst-case time complexity for generating all maximal cliques and computational experiments, Theoretical Computer Science 363(1), 2006, 28 to 42"
    locator: a pivot rule for the Bron-Kerbosch method that lists all maximal cliques in O(3^(n/3)) time
  - paper: "Eugene L. Lawler, A note on the complexity of the chromatic number problem, Information Processing Letters 5(3), 1976, 66 to 67"
    locator: the chromatic number by dynamic programming over subsets that lists the maximal independent sets of each subgraph, with the Moon-Moser bound
---

The enumeration of maximal independent sets asks for a list of all [maximal independent sets](/maximal-independent-set/) of a graph: all sets of vertices with no edge inside that cannot be extended by another vertex. A graph with $n$ vertices can have as many as $3^{n/3}$ of them, by the theorem of Moon and Moser, so the problem is studied with [output-sensitive](/output-sensitive-enumeration/) measures. It is solvable with polynomial delay, by the [algorithm of Tsukiyama and others](/tsukiyama-algorithm/) from 1977, and it is the same problem as listing all [maximal cliques](/maximal-clique-enumeration/) of the complement graph.

## In plain words

Think of the vertices of a graph as people and the edges as pairs of people who do not get along. An independent set is a group in which everyone gets along. It is maximal when nobody else can join the group without a conflict.

The task is to write down every such group. The groups can overlap, and there can be a very large number of them. The best methods make sure that the time spent between two groups on the list stays small, so no time is lost on choices that give nothing new.

## Definition

**Instance.** A simple undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$.

**Solutions.** The sets $S \subseteq V$ that are

- *independent*: no edge has both ends in $S$, and
- *maximal*: every vertex $u \notin S$ has a neighbor in $S$.

The task is to output each solution exactly once. An independent set is maximal if and only if it is a *dominating set*, so the solutions are also the independent dominating sets of $G$. Every graph has at least one solution, which the greedy method finds in $O(n + m)$ time, so the problem is about the listing and not about existence.

## Variants

- **Maximal cliques.** List the maximal cliques of $G$. They are the maximal independent sets of the complement of $G$, so the two problems are the same, but for sparse $G$ the complement is dense, and algorithms are tuned for one form.
- **Ordered output.** List the solutions in lexicographic order, or in reverse lexicographic order. The order changes the complexity: see the bounds.
- **Counting.** Count the solutions instead of listing them.
- **Bounded size.** List only the solutions of size at least $k$, or find the largest one, which is the [maximum independent set](/maximum-independent-set/) problem and is NP-hard.
- **Hypergraphs.** In a hypergraph, a set is independent when it contains no edge. Its maximal independent sets are the complements of its [minimal transversals](/minimal-transversal-enumeration/), and no polynomial total time algorithm is known for them.
- **Special classes.** For chordal graphs, bipartite graphs, and graphs of bounded degree, the bounds on the number of solutions and the time per solution are smaller.

## Examples

| graph | number of maximal independent sets |
|---|---|
| $n$ vertices and no edge | 1, the whole vertex set |
| complete graph $K_n$ | $n$, the single vertices |
| star with $n - 1$ leaves | 2, the center and the set of leaves |
| path $v_1 v_2 v_3 v_4$ | 3: $\{v_1, v_3\}$, $\{v_1, v_4\}$, $\{v_2, v_4\}$ |
| cycle $C_5$ | 5: each vertex with one of the two vertices at distance 2 |
| $k$ disjoint triangles, $n = 3k$ | $3^k = 3^{n/3}$: one vertex from each triangle |

**A non-example.** In the path $v_1 v_2 v_3 v_4$, the set $\{v_1\}$ is independent but not maximal, because $v_3$ can be added. The set $\{v_1, v_2\}$ is not independent.

The trace of the Tsukiyama algorithm on $C_5$ is on [its page](/tsukiyama-algorithm/).

## Known algorithms

| algorithm | time | space | notes |
|---|---|---|---|
| brute force over all $2^n$ subsets | $O(2^n (n + m))$ | $O(n)$ | test each subset |
| [Tsukiyama, Ide, Ariyoshi, Shirakawa](/tsukiyama-algorithm/) (1977) | $O(nm)$ per output | $O(n + m)$ | polynomial delay |
| Johnson, Yannakakis, Papadimitriou (1988) | polynomial delay | exponential | lexicographic order |
| [Bron-Kerbosch](/bron-kerbosch/) with Tomita's pivot (2006) | $O(3^{n/3})$ total | polynomial | on the complement; optimal in the worst case |
| Makino and Uno (2004) | matrix multiplication time per output | polynomial | dense graphs; also a bound in the maximum degree |

The algorithm of Tsukiyama and others adds the vertices one by one and keeps a single parent for each set. The pivoting Bron-Kerbosch search does not have polynomial delay, but its total time matches the largest possible output and it is the fastest in many practical cases.

## Bounds

**Number of solutions (Moon and Moser, 1965).** The largest number of maximal independent sets of a graph with $n \ge 2$ vertices is

$$
g(n) = \begin{cases} 3^{n/3} & n \equiv 0 \pmod 3, \\ 4 \cdot 3^{(n-4)/3} & n \equiv 1 \pmod 3, \\ 2 \cdot 3^{(n-2)/3} & n \equiv 2 \pmod 3. \end{cases}
$$

For $n = 2, \ldots, 6$ this gives $2, 3, 4, 6, 9$, which a search over all graphs with at most 6 vertices confirms. The extremal graphs for $n \equiv 0 \pmod 3$ are the disjoint unions of triangles. So any algorithm that lists all solutions needs $\Omega(3^{n/3})$ time in the worst case, and the pivoting Bron-Kerbosch method is worst-case optimal in this sense.

**Time per solution.** Polynomial delay is possible: $O(n(n + m))$ per solution for the simple form of the Tsukiyama algorithm, and less with the later methods.

**Order matters.** Johnson, Yannakakis and Papadimitriou show that the solutions can be listed in lexicographic order with polynomial delay, but that no algorithm lists them in reverse lexicographic order with polynomial delay unless $\mathrm{P} = \mathrm{NP}$.

## Reductions

- **Maximal cliques.** $S$ is a maximal independent set of $G$ if and only if it is a maximal clique of the complement $\overline{G}$. Building $\overline{G}$ takes $O(n^2)$ time.
- **Minimal vertex covers.** $S$ is a maximal independent set if and only if $V \setminus S$ is a minimal [vertex cover](/vertex-cover/). So the two lists have the same size and the same complexity.
- **Minimal transversals of a graph.** The minimal vertex covers of $G$ are the minimal transversals of the [hypergraph](/hypergraph/) whose edges are the edges of $G$. So the problem is the special case of [minimal transversal enumeration](/minimal-transversal-enumeration/) for hypergraphs with edges of size 2, which is why it is easier than the general case.

## Applications

- **Graph coloring.** Each color class of an optimal coloring can be extended to a maximal independent set. [Lawler's algorithm](/lawler-chromatic-number/) for the chromatic number lists the maximal independent sets of each induced subgraph, and the Moon-Moser bound gives its running time $O^*(2.4423^n)$.
- **Clique analysis.** Listing maximal cliques finds dense groups in social networks, in protein interaction networks and in the comparison of molecular structures.
- **Scheduling and compatibility.** When an edge marks two tasks that cannot run together, a maximal independent set is a largest-possible group of tasks that can run together.
- **Exact algorithms.** Lists of maximal independent sets of small subgraphs are subroutines of exact algorithms for coloring and related problems.

## References
