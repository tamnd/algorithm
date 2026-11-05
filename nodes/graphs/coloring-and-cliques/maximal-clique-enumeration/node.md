---
tag: VQSEX3
kind: problem
slug: maximal-clique-enumeration
name: Maximal clique enumeration
aliases:
- listing maximal cliques
area: graphs/coloring-and-cliques
level: core
summary: List all maximal cliques of a graph; output-sensitive algorithms exist.
prereqs: [maximal-clique, clique]
see_also: [bron-kerbosch, maximal-independent-set-enumeration, maximum-clique, degeneracy-ordering, clique-percolation-method, lawler-chromatic-number, chordal-graph]
sources:
  - paper: doi:10.1007/BF02760024
    title: J. W. Moon and L. Moser, On cliques in graphs, Israel Journal of Mathematics 3(1), 23 to 28 (1965)
    locator: the theorem on the largest number of maximal cliques
  - paper: doi:10.1145/362342.362367
    title: Coen Bron and Joep Kerbosch, Algorithm 457, Finding all cliques of an undirected graph, Communications of the ACM 16(9), 575 to 577 (1973)
    locator: the whole paper
  - paper: doi:10.1016/j.tcs.2006.06.015
    title: Etsuji Tomita, Akira Tanaka and Haruhisa Takahashi, The worst-case time complexity for generating all maximal cliques and computational experiments, Theoretical Computer Science 363(1), 28 to 42 (2006)
    locator: the main theorem (O(3^(n/3)) time with the pivot rule)
  - paper: doi:10.1137/0206036
    title: Shuji Tsukiyama, Mikio Ide, Hiromu Ariyoshi and Isao Shirakawa, A new algorithm for generating all the maximal independent sets, SIAM Journal on Computing 6(3), 505 to 517 (1977)
    locator: the whole paper (O(nm) time for each maximal independent set, with polynomial space)
  - paper: doi:10.1007/978-3-540-27810-8_23
    title: Kazuhisa Makino and Takeaki Uno, New algorithms for enumerating all maximal cliques, Algorithm Theory, SWAT 2004, Lecture Notes in Computer Science 3111, 260 to 272 (2004)
    locator: the whole paper (delay by matrix multiplication, and a bound by the maximum degree for sparse graphs)
  - paper: doi:10.1007/978-3-642-17517-6_36
    title: David Eppstein, Maarten Löffler and Darren Strash, Listing all maximal cliques in sparse graphs in near-optimal time, ISAAC 2010, Lecture Notes in Computer Science 6506, 403 to 414 (2010)
    locator: the main theorem (O(d n 3^(d/3)) time for degeneracy d)
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 119 to 123 (1988)
    locator: the whole paper (polynomial delay, also in lexicographic order)
---

Maximal clique enumeration asks for the list of all [maximal cliques](/maximal-clique/) of a graph, each exactly once. A graph with $n$ vertices can have $3^{n/3}$ maximal cliques, so no algorithm runs in polynomial time in $n$ alone; the [Bron-Kerbosch algorithm](/bron-kerbosch/) with pivoting reaches this bound, $O(3^{n/3})$, in the worst case. The other measure is the cost per clique: there are algorithms with polynomial delay between two outputs, and algorithms whose time is near-optimal for sparse graphs in terms of the [degeneracy](/degeneracy/). The problem is the same as listing the maximal [independent sets](/independent-set/) of the [complement graph](/complement-graph/).

## In plain words

A maximal clique is a group of vertices that are all linked to each other, and no other vertex can join the group. The task is to write down every such group, with no group written twice.

The difficulty is that there can be very many of them. A graph made of many small groups of three, with every link between different groups, has a huge number of maximal cliques. So we judge a method by two numbers: the worst total time for any graph of a given size, and the time it spends for each clique that it outputs.

## Definition

**Input.** A finite simple undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$.

**Output.** The family

$$\mathcal{M}(G) = \{\, C \subseteq V : C \text{ is a clique of } G \text{ and } C \cup \{v\} \text{ is not a clique for any } v \in V \setminus C \,\},$$

listed so that each member appears exactly once. Write $\mu = |\mathcal{M}(G)|$.

Ways to measure an enumeration algorithm:

- **Total time** as a function of $n$ (worst case over all graphs with $n$ vertices).
- **Output-sensitive time**: total time $O(f(n, m) \cdot \mu)$ or $O(f(n, m) \cdot (\mu + 1))$.
- **Delay**: the largest time between two consecutive outputs, and before the first and after the last. Polynomial delay implies output-polynomial total time.

## Variants

- **Maximal independent sets.** $\mathcal{M}(\overline{G})$ is the family of maximal independent sets of $G$; see [maximal independent set enumeration](/maximal-independent-set-enumeration/). Each algorithm for one solves the other, after building the complement in $O(n^2)$ time.
- **Counting.** Computing $\mu$ alone, without the list, is #P-complete.
- **Ordered output.** Output the cliques in lexicographic order. Johnson, Yannakakis and Papadimitriou do this with polynomial delay, using a priority queue that can grow to exponential size.
- **Restricted output.** List only the maximal cliques with at least $k$ vertices, or only those through a given vertex.

## Examples

| graph | $n$ | $\mu$ | the maximal cliques |
|---|---|---|---|
| $K_n$ | $n$ | 1 | $V$ |
| empty graph on $n \ge 1$ vertices | $n$ | $n$ | the single vertices |
| $C_n$, $n \ge 4$ | $n$ | $n$ | the edges |
| Petersen graph | 10 | 15 | the edges |
| edges $01, 02, 12, 13, 23, 34, 45$ | 6 | 4 | $\{0,1,2\}$, $\{1,2,3\}$, $\{3,4\}$, $\{4,5\}$ |
| $K_{3,3,3}$ | 9 | 27 | one vertex from each group |

The graph with no vertices has the single maximal clique $\emptyset$, so $\mu = 1$.

**Moon-Moser graphs.** The complete multipartite graph with $n/3$ groups of size 3 has $3^{n/3}$ maximal cliques. Moon and Moser proved that no graph with $n$ vertices has more, for $n$ divisible by 3, with matching bounds $4 \cdot 3^{(n-4)/3}$ and $2 \cdot 3^{(n-2)/3}$ for the other residues. For $n = 1$ to $6$ the largest values of $\mu$ are 1, 2, 3, 4, 6 and 9.

## Known algorithms

- **[Bron-Kerbosch](/bron-kerbosch/) (1973).** Recursive backtracking with three sets: the current clique $R$, the candidates $P$ that can extend it, and the excluded vertices $X$ that would make it non-maximal. It reports $R$ when $P$ and $X$ are both empty. Without a pivot it can spend exponential time between outputs.
- **Pivoting (Tomita, Tanaka and Takahashi 2006).** Choose a pivot $u \in P \cup X$ with the most neighbors in $P$, and branch only on $P \setminus N(u)$. The worst-case time is $O(3^{n/3})$, which matches the Moon-Moser bound, so it is optimal as a function of $n$.
- **Degeneracy order (Eppstein, Löffler and Strash 2010).** Run pivoted Bron-Kerbosch once for each vertex $v$, with $P$ the later neighbors and $X$ the earlier neighbors of $v$ in a [degeneracy ordering](/degeneracy-ordering/). The time is $O(d\, n\, 3^{d/3})$ for degeneracy $d$, and a graph with degeneracy $d$ can have $(n - d)\, 3^{d/3}$ maximal cliques, so this is near-optimal for sparse graphs.
- **Reverse search (Tsukiyama, Ide, Ariyoshi and Shirakawa 1977).** Polynomial delay $O(nm)$ for each clique and polynomial space, by moving from one maximal independent set to another along a tree of parent links.
- **Makino and Uno (2004).** Delay $O(M(n))$, the time to multiply two $n \times n$ matrices, for dense graphs, and $O(\Delta^4)$ per clique for graphs of maximum degree $\Delta$.
- **Chordal graphs.** At most $n$ maximal cliques; a [perfect elimination ordering](/perfect-elimination-ordering/) lists them all in $O(n + m)$ time.

## Bounds

- **Output size.** $\mu \le 3^{n/3}$ (Moon and Moser), so each algorithm needs $\Omega(3^{n/3})$ time on the Moon-Moser graphs just to write the output. The pivot version of Bron-Kerbosch matches this.
- **Sparse graphs.** For degeneracy $d$, $\mu \le (n - d)\, 3^{d/3}$, and the Eppstein-Löffler-Strash time is within a factor $O(d)$ of the output size in the worst case.
- **Per-clique cost.** Polynomial delay is possible (Tsukiyama et al. and later work), so the total time is at most a polynomial times $\mu + 1$.

## Reductions

- **To maximal independent sets.** $\mathcal{M}(G)$ equals the family of maximal independent sets of $\overline{G}$.
- **To maximum clique.** The largest member of $\mathcal{M}(G)$ is a [maximum clique](/maximum-clique/). A branch-and-bound method finds it much faster than listing all, but listing gives every maximum clique at once.
- **Exact coloring.** [Lawler's algorithm](/lawler-chromatic-number/) for the chromatic number lists the maximal independent sets of induced subgraphs, and its running time comes from the Moon-Moser bound.

## Applications

- **Network analysis.** The [clique percolation method](/clique-percolation-method/) builds overlapping communities from cliques, and cohesive groups in social networks are often maximal cliques.
- **Bioinformatics.** Protein complexes, gene co-expression modules and motif finding use the maximal cliques of interaction or similarity graphs.
- **Chemistry and vision.** Matching two structures reduces to cliques of an association graph; all maximal cliques give all maximal common substructures.
- **Exact algorithms.** Exponential-time coloring and other partition problems branch over maximal independent sets.

## References
