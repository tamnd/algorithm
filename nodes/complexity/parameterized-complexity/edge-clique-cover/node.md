---
tag: 312T34
kind: problem
slug: edge-clique-cover
name: Edge clique cover
aliases:
- ECC
area: complexity/parameterized-complexity
level: research
summary: "Cover every edge of a graph by at most k cliques. FPT in k by a kernel with 2^k vertices; no 2^(2^o(k)) n^O(1) algorithm under ETH and no polynomial kernel unless NP is a subset of coNP/poly."
prereqs: [kernel, fixed-parameter-tractable, maximal-clique]
see_also: [kernel, kernel-lower-bounds, clique-cover, maximal-clique, bron-kerbosch, cluster-editing, set-cover, w-hierarchy]
sources:
  - paper: doi:10.1145/1412228.1412236
    title: "Jens Gramm, Jiong Guo, Falk Hüffner and Rolf Niedermeier, Data reduction and exact algorithms for clique cover, ACM Journal of Experimental Algorithmics 13 (2008)"
    locator: the data reduction rules and the kernel with at most 2^k vertices
  - paper: doi:10.1137/130947076
    title: "Marek Cygan, Marcin Pilipczuk and Michal Pilipczuk, Known algorithms for edge clique cover are probably optimal, SIAM Journal on Computing 45(1), 67-83 (2016)"
    locator: abstract (reduction from 3-CNF-SAT with k = O(log n); no 2^(2^o(k)) n^O(1) algorithm unless ETH fails; no kernel of size 2^o(k) unless P = NP)
  - paper: doi:10.1145/2594439
    title: "Marek Cygan, Stefan Kratsch, Marcin Pilipczuk, Michal Pilipczuk and Magnus Wahlström, Clique cover and graph separation: new incompressibility results, ACM Transactions on Computation Theory 6(2), article 6 (2014)"
    locator: no polynomial kernel for edge clique cover unless NP is a subset of coNP/poly
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: problems GT17 (covering by cliques) and GT59 (intersection graph basis)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (edge clique cover); Chapter 14, Lower bounds based on the exponential time hypothesis
---

Edge clique cover asks whether the edges of a graph can be covered by at most $k$ cliques. The parameter is $k$. Gramm, Guo, Hüffner and Niedermeier gave simple reduction rules that leave at most $2^k$ vertices, so the problem is [fixed-parameter tractable](/fixed-parameter-tractable/), and brute force on this [kernel](/kernel/) gives time $2^{2^{O(k)}} + n^{O(1)}$. Cygan, Pilipczuk and Pilipczuk showed that this double exponential bound is optimal: there is no $2^{2^{o(k)}} n^{O(1)}$ algorithm unless the exponential time hypothesis (ETH) fails, and no kernel of size $2^{o(k)}$ unless P = NP. It is one of the first natural FPT problems known to need a double exponential dependence on the parameter.

## In plain words

Draw a network, and then draw a few circles around groups of points. In each circle every two points must be linked. Every link of the network must lie in some circle. Can you do this with $k$ circles?

Give each point the list of circles it lies in. If two points have the same list, they are linked to exactly the same points, so one of them can be removed without changing the answer. After removing such copies, each point has its own list, and there are only $2^k$ possible lists. So at most $2^k$ points remain, and an exhaustive search over them works. This search is slow, with time doubly exponential in $k$, but it is known that nothing much faster is possible.

## Definition

- Instance: an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: are there cliques $C_1, \ldots, C_k$ of $G$ such that each edge of $G$ has both ends in some $C_i$?

Each clique can be enlarged to a maximal clique, so it is enough to use [maximal cliques](/maximal-clique/). Edge clique cover is different from [clique cover](/clique-cover/), which partitions the vertices into cliques.

## Variants

- **Intersection number.** The least $k$ for which $G$ has an edge clique cover of size $k$ is the *intersection number* of $G$. It is also the least size of a set $U$ such that $G$ is the intersection graph of subsets of $U$: give each vertex the set of cliques that contain it. Garey and Johnson list the two forms as GT17 and GT59.
- **Edge clique partition.** Each edge must be in exactly one clique. The twin argument does not apply in the same way, so it is a different problem.
- **Assignment form.** Equivalently, give each vertex $v$ a subset $S(v) \subseteq \{1, \ldots, k\}$ such that $uv \in E$ exactly when $S(u) \cap S(v) \ne \emptyset$, for $u \ne v$. This form is the base of the lower bound proof.

## Examples

A scratch script took the graph on $1, \ldots, 8$ with the 13 edges $12$, $13$, $14$, $23$, $24$, $34$, $45$, $46$, $56$, $67$, $48$, $58$, $68$.

- It has 3 maximal cliques, $\{1, 2, 3, 4\}$, $\{4, 5, 6, 8\}$ and $\{6, 7\}$, and all three are needed, so the least edge clique cover has size 3.
- The cliques that contain each vertex are: $1, 2, 3$ lie in clique 1 only; $4$ in cliques 1 and 2; $5$ and $8$ in clique 2 only; $6$ in cliques 2 and 3; $7$ in clique 3 only. The vertices $1, 2, 3$ are twins, and so are $5$ and $8$.
- The twin rule removed $2$, $3$ and $8$. The rest has 5 vertices and 5 edges, and the least cover still has size 3. The 5 remaining vertices have 5 different nonempty subsets of $\{1, 2, 3\}$, as the kernel argument says.

## Known algorithms

- **Kernel with $2^k$ vertices (Gramm, Guo, Hüffner and Niedermeier).** Three rules suffice for the bound. Remove isolated vertices. If an edge $uv$ is a whole component, remove it and decrease $k$ by 1. If $u$ and $v$ are adjacent and have the same closed neighborhood with at least 3 vertices, remove $v$; then $u$ keeps a neighbor, so a cover of $G - v$ has a clique that contains $u$, and it extends by putting $v$ into every clique that contains $u$. In a YES instance, give each vertex the set of cliques of a solution that contain it. Two vertices with the same nonempty set have the same closed neighborhood, so after the rules all sets are distinct and nonempty. So at most $2^k - 1$ vertices remain, or the answer is NO.
- **Brute force on the kernel.** Try every assignment of a subset of $\{1, \ldots, k\}$ to each of the at most $2^k$ vertices. There are at most $(2^k)^{2^k} = 2^{k 2^k}$ assignments, so the time is $2^{2^{O(k)}} + n^{O(1)}$.
- **Search with further rules.** Gramm et al. also gave a search tree with more reduction rules and tested it in experiments.

## Bounds

- **Classical complexity.** NP-complete under polynomial-time many-one reductions (Garey and Johnson, GT17).
- **Lower bound in time.** Cygan, Pilipczuk and Pilipczuk reduced 3-CNF-SAT with $n$ variables and $m$ clauses to an instance with $k = O(\log n)$ and $O(n + m)$ vertices. So a $2^{2^{o(k)}} n^{O(1)}$ algorithm would solve 3-SAT in $2^{o(n)}$ time, and there is none unless ETH fails.
- **Kernels.** No kernel of size $2^{o(k)}$ exists unless P = NP (Cygan, Pilipczuk and Pilipczuk). No polynomial kernel exists unless NP is a subset of coNP/poly (Cygan, Kratsch, Pilipczuk, Pilipczuk and Wahlström). So the $2^k$ kernel is close to optimal. See [kernel lower bounds](/kernel-lower-bounds/).

## Reductions

- **From 3-SAT, with logarithmic $k$.** The reduction of Cygan, Pilipczuk and Pilipczuk maps a 3-CNF formula with $n$ variables and $m$ clauses to an equivalent instance with $k = O(\log n)$ and $O(n + m)$ vertices, in polynomial time. Since $2^k$ is only polynomial in $n$, an algorithm in time $2^{2^{o(k)}} n^{O(1)}$ would decide 3-SAT in $2^{o(n)}$ time.
- **To set cover.** Fix the list of maximal cliques. Then the problem is [set cover](/set-cover/) with the edges as elements and the maximal cliques as sets. The number of maximal cliques can be exponential in $n$, so this is useful mainly for sparse graphs.

## Applications

Edge clique covers appear in the compact representation of graphs as intersection graphs, in the analysis of social and biological networks, where cliques are communities that may overlap, and in the encoding of compatibility relations by a few shared labels. The data reduction rules of Gramm et al. make exact solutions possible on many sparse inputs.

## References
