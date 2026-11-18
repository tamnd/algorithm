---
tag: BXD0MK
kind: theorem
slug: join-ordering-np-hardness
name: NP-hardness of join ordering
aliases:
- Ibaraki-Kameda theorem
area: databases/query-planning
level: advanced
summary: "Finding an optimal join order is NP-hard in general, while for tree queries under an ASI cost function it is polynomial."
prereqs: [np-complete, clique-problem, join-ordering]
see_also: [ikkbz-algorithm, left-deep-and-bushy-join-trees, dpccp, greedy-operator-ordering, selinger-join-enumeration, polynomial-time-reduction, cost-model, matrix-chain-multiplication]
sources:
  - paper: doi:10.1145/1270.1498
    title: "Toshihide Ibaraki and Tiko Kameda, On the optimal nesting order for computing N-relational joins, ACM Transactions on Database Systems 9(3), 482 to 502 (1984)"
    locator: "the NP-completeness of the optimal nesting order for general query graphs under the cost of nested loop joins, and the O(n^2 log n) algorithm for tree queries"
  - paper: "Ravi Krishnamurthy, Haran Boral and Carlo Zaniolo, Optimization of nonrecursive queries, Proceedings of VLDB 1986, 128 to 137"
    title: Optimization of nonrecursive queries
    locator: the O(n^2) algorithm for tree queries with cost functions that have the adjacent sequence interchange (ASI) property
  - paper: "Sophie Cluet and Guido Moerkotte, On the complexity of generating optimal left-deep processing trees with cross products, Proceedings of ICDT 1995, LNCS 893, 54 to 67"
    title: On the complexity of generating optimal left-deep processing trees with cross products
    locator: the complexity of optimal left-deep trees when cross products are allowed
---

The NP-hardness of join ordering says that no polynomial algorithm finds the cheapest order of the joins of a query in general, unless P = NP, while some special cases are easy. Ibaraki and Kameda proved in 1984 that the choice of the best left-deep order without cross products is NP-complete for general query graphs under the cost of nested loop joins. For tree query graphs and costs with the adjacent sequence interchange (ASI) property, the same problem is polynomial, by the [IKKBZ algorithm](/ikkbz-algorithm/). Cluet and Moerkotte (1995) studied the case in which cross products are allowed. This page states the three results together and proves the hardness of left-deep ordering with cross products under the cost $C_{out}$ in full, by a reduction from CLIQUE. The [join ordering](/join-ordering/) page defines the problem and surveys its algorithms; this page holds the theorem and the proof.

## Statement

**Instances.** An instance of join ordering has relations $R_1, \ldots, R_n$ with estimated cardinalities $|R_i| > 0$, and a *query graph* with an edge $\{i, j\}$ for each join predicate, labeled with a selectivity $0 < f_{ij} \le 1$. For a pair with no edge, $f_{ij} = 1$. All numbers are rationals written in binary, and the size of the instance is the number of bits. The database itself is not part of the input. Under the independence assumption, the join of a set $S$ of relations has the estimated size

$$|S| = \prod_{i \in S} |R_i| \prod_{\{i, j\} \subseteq S} f_{ij}.$$

A [left-deep tree](/left-deep-and-bushy-join-trees/) is an order $R_{v_1}, \ldots, R_{v_n}$. It has a *cross product* at step $j$ if $R_{v_j}$ has no edge to $R_{v_1}, \ldots, R_{v_{j-1}}$. Its cost $C_{out}$ is the sum of the sizes of the results of its joins:

$$C_{out}(v) = \sum_{j=2}^{n} |\{v_1, \ldots, v_j\}|.$$

The sizes are counts of tuples of bag joins, so the problem is the same under set and bag semantics. The complexity measure is time in the size of the instance.

**Theorem.**

1. **Hardness with cross products.** The following problem is NP-complete: given an instance and a rational $K$, is there a left-deep tree, cross products allowed, with $C_{out} \le K$? So finding a left-deep tree of least $C_{out}$ is NP-hard.
2. **Hardness without cross products (Ibaraki and Kameda 1984).** For left-deep trees without cross products and the cost of nested loop joins of their model, the decision problem is NP-complete for general query graphs.
3. **The polynomial case (Ibaraki and Kameda 1984; Krishnamurthy, Boral and Zaniolo 1986).** If the query graph is a tree and the cost has the ASI property, as $C_{out}$ and the nested loop cost have, then a left-deep tree without cross products of least cost can be found in polynomial time: $O(n^2 \log n)$ in the first paper and $O(n^2)$ in the second.

## In plain words

An optimizer must choose the order in which a query joins its tables. Each order gives the same answer, but the sizes of the partial results differ, and so does the work. The theorem says that no fast method always finds the best order, unless many hard problems all have fast methods.

The proof turns a known hard puzzle into a join order question. The puzzle asks if a network has a group of a given size in which every member knows every other member. Each person becomes a table, and each pair who know each other becomes a join condition that makes the result much smaller. A cheap order must start with a group where everyone knows everyone. So a fast join planner would also solve the puzzle fast.

There is one easy case: when the joins form a tree, a known method finds the best order quickly.

## Proof

**Part 1, membership in NP.** A certificate is an order $v$. Each prefix size is a product of at most $n$ cardinalities and at most $n(n-1)/2$ selectivities, so it has a number of bits polynomial in the size of the instance, and the sum $C_{out}(v)$ and the comparison with $K$ take polynomial time.

**Part 1, hardness.** The reduction is from CLIQUE, which is NP-complete: given a graph $G = (V, E)$ with $n \ge 2$ vertices and an integer $k$ with $2 \le k \le n$, does $G$ have $k$ vertices that are pairwise adjacent? This reduction was written for this page; it is not taken from the paper of Cluet and Moerkotte. Write $c(j) = j(j-1)/2$ for the number of pairs among $j$ vertices.

*Construction.* For each vertex $v$ take a relation $R_v$ with $|R_v| = 2$. For each edge $\{u, v\}$ of $G$ put a join predicate with selectivity $f = 2^{-2n}$ between $R_u$ and $R_v$, and put no predicate between two vertices that are not adjacent. Let

$$g(j) = j - 2n\, c(j), \qquad K = \sum_{j=2}^{k} 2^{g(j)} + (n - k)\, 2^{\,n - 2n\, c(k)}.$$

All numbers are powers of 2 with exponents of absolute value $O(n^3)$, so the instance and $K$ have $O(n^4)$ bits and are built in polynomial time.

*Cost of an order.* For an order $v$ of the vertices, let $e_j$ be the number of edges of $G$ among $v_1, \ldots, v_j$. The prefix of length $j$ has the size $s_j = 2^j f^{e_j} = 2^{\,j - 2n e_j}$, and $C_{out}(v) = \sum_{j=2}^{n} s_j$. Since $e_j \le c(j)$, every $s_j \ge 2^{g(j)}$. The function $g$ decreases, because $g(j+1) - g(j) = 1 - 2nj < 0$.

*If $G$ has a clique $Q$ of $k$ vertices,* put the vertices of $Q$ first. For $j \le k$ the prefix is a clique, so $e_j = c(j)$ and $s_j = 2^{g(j)}$. For $j > k$ the prefix holds all the edges of $Q$, so $e_j \ge c(k)$, and with $j \le n$ this gives $s_j \le 2^{\,n - 2n\, c(k)}$. There are $n - k$ such terms, so $C_{out}(v) \le K$.

*If $G$ has no clique of $k$ vertices,* take any order $v$. Its first $k$ vertices are not a clique, so some $j \le k$ has $e_j < c(j)$. Let $j^*$ be the least such $j$. For $2 \le j < j^*$, $e_j = c(j)$ and $s_j = 2^{g(j)}$. At $j^*$, $e_{j^*} \le c(j^*) - 1$, so $s_{j^*} \ge 2^{\,g(j^*) + 2n}$. So

$$C_{out}(v) \ge \sum_{j=2}^{j^*-1} 2^{g(j)} + 2^{\,g(j^*) + 2n}.$$

The same first sum is part of $K$. The rest of $K$ is $\sum_{j=j^*}^{k} 2^{g(j)} + (n-k)\, 2^{\,n - 2n\, c(k)}$. Each term of the sum is at most $2^{g(j^*)}$, because $g$ decreases. And $n - 2n\, c(k) \le n - 2n\, c(j^*) \le n + g(j^*)$, so each of the other $n - k$ terms is at most $2^{\,g(j^*) + n}$. The rest of $K$ has $k - j^* + 1 + n - k \le n$ terms, so it is at most $n \cdot 2^{\,g(j^*) + n} < 2^{\,g(j^*) + 2n}$, because $n < 2^n$. So $K < C_{out}(v)$ for every order.

So $G$ has a clique of $k$ vertices if and only if some left-deep tree has $C_{out} \le K$. With membership, this proves part 1.

*An example.* Take the path $a - b - c$ and $k = 3$, so $n = 3$, $|R_v| = 2$ and $f = 2^{-6}$. Then $K = 2^{-4} + 2^{-15} = 1/16 + 1/32768$. The order $a, b, c$ has $s_2 = 4 \cdot 2^{-6} = 1/16$ and $s_3 = 8 \cdot 2^{-12} = 1/512$, so its cost $1/16 + 1/512$ is more than $K$. An order that starts with $a, c$ has $s_2 = 4$, which is worse. With the edge $a - c$ added, the graph is a triangle, the order $a, b, c$ has $s_3 = 8 \cdot 2^{-18} = 1/32768$, and its cost is exactly $K$.

**Part 2.** This is the theorem of Ibaraki and Kameda; the proof, a reduction for their cost of nested loop joins on a general query graph, is in their paper and is not repeated here.

**Part 3.** Fix the first relation $r$. In a tree query, an order without cross products is an order in which each relation comes after its parent in the tree hung from $r$, so the problem becomes the ordering of jobs under a tree of precedence constraints. For an ASI cost the cost of an order is $C(s_1) + T(s_1)\, C(s_2)$ for consecutive parts $s_1$ and $s_2$, and exchanging two adjacent blocks $A$ and $B$ changes the cost by a positive factor times $\mathrm{rank}(A) - \mathrm{rank}(B)$, with $\mathrm{rank}(s) = (T(s) - 1)/C(s)$. So an optimal order puts blocks in order of increasing rank, and a child block with a smaller rank than its parent block is glued to the parent. This gives the optimal order for each $r$ in polynomial time, and trying all $n$ choices of $r$ gives the optimum. The [IKKBZ](/ikkbz-algorithm/) page gives the algorithm, an example and the full proof. $\square$

## Consequences

- **Exponential exact search.** Unless P = NP, an exact join enumerator needs more than polynomial time on some queries. The dynamic programs used in practice, such as the [System R enumeration](/selinger-join-enumeration/) for left-deep trees and [DPccp](/dpccp/) for bushy trees, are exponential in $n$, and systems switch to heuristics such as [greedy operator ordering](/greedy-operator-ordering/) above a limit on the number of relations.
- **The shape of the query graph matters.** Part 3 makes tree queries easy for left-deep trees without cross products, and parts 1 and 2 need general graphs. Chain queries are easier still: for bushy trees without cross products, an interval dynamic program like that of [matrix chain multiplication](/matrix-chain-multiplication/) runs in $O(n^3)$ time.
- **Cross products do not make the problem easier.** Allowing cross products makes the space larger and can make the best plan cheaper, as the star query example on the [join ordering](/join-ordering/) page shows, but by part 1 the problem stays NP-hard.
- **Hardness is about estimates.** The theorem is about the estimated sizes, not about a database. An exact algorithm for the estimates still depends on the [cost model](/cost-model/) and on the quality of the estimates.

## Tightness

- **Number sizes.** The reduction of part 1 uses selectivities of $2n$ bits and estimated sizes far below one tuple. It shows NP-hardness for numbers written in binary. It does not show that the problem stays hard when all numbers are small integers written in unary.
- **The conditions of part 3 are needed.** Without the tree condition, part 2 gives hardness for the nested loop cost. Without the ASI property, the rank argument fails, because the cost change of an exchange no longer has the sign of a rank difference.
- **Other tree shapes.** Parts 1 and 2 are about left-deep trees. This page makes no claim about bushy trees, which have their own hardness results in the literature.
- **Fixed $n$.** For a fixed number of relations, all $n!$ orders can be tried, so the hardness is a statement about the growth in $n$.

## History

Ibaraki and Kameda (1984) studied the nesting order of nested loop joins. They proved the NP-completeness for general query graphs and gave an $O(n^2 \log n)$ algorithm for tree queries, based on results on sequencing jobs with precedence constraints. Krishnamurthy, Boral and Zaniolo (1986) stated the algorithm for every cost with the ASI property and made it $O(n^2)$; the pair of results gives the name IKKBZ. Cluet and Moerkotte (1995) then studied left-deep trees with cross products, the space that System R searched when it allowed cross products.

## References
