---
tag: NTZ7MS
kind: problem
slug: join-ordering
name: Join ordering problem
aliases:
- join order optimization
- join order selection
- join enumeration problem
area: systems/database-algorithms
level: core
summary: "Choose the order and the tree shape in which to join n relations so that the estimated cost is least. NP-hard in general; polynomial for tree queries with ASI costs."
prereqs: [query-plan, cost-model]
see_also: [selinger-join-enumeration, matrix-chain-multiplication, query-optimization, cardinality-estimation, multiway-join, generic-join, agm-bound, yannakakis-algorithm]
sources:
  - paper: doi:10.1145/1270.1498
    title: Toshihide Ibaraki and Tiko Kameda, On the optimal nesting order for computing N-relational joins, ACM Transactions on Database Systems 9(3) (1984), 482 to 502
    locator: the NP-completeness of the optimal nesting order for general query graphs, and the O(n^2 log n) algorithm for tree queries
  - paper: "Ravi Krishnamurthy, Haran Boral and Carlo Zaniolo, Optimization of nonrecursive queries, Proceedings of VLDB 1986, 128 to 137"
    title: Optimization of nonrecursive queries
    locator: the O(n^2) algorithm for tree queries with cost functions that have the adjacent sequence interchange (ASI) property
  - paper: "Sophie Cluet and Guido Moerkotte, On the complexity of generating optimal left-deep processing trees with cross products, Proceedings of ICDT 1995, LNCS 893, 54 to 67"
    title: On the complexity of generating optimal left-deep processing trees with cross products
    locator: the NP-hardness of the problem for left-deep trees with cross products under the cost function C_out
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 5, p. 28 (the n factorial join orders, the search over successively larger subsets, and the deferral of cross products)
  - paper: "Michael Steinbrunn, Guido Moerkotte and Alfons Kemper, Heuristic and randomized optimization for the join ordering problem, The VLDB Journal 6(3) (1997), 191 to 208"
    title: Heuristic and randomized optimization for the join ordering problem
    locator: the comparison of greedy heuristics, iterative improvement, simulated annealing and the KBZ algorithm on large join queries
  - paper: "Guido Moerkotte and Thomas Neumann, Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products, Proceedings of VLDB 2006, 930 to 941"
    title: Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products
    locator: DPsize, DPsub and DPccp, and the number of csg-cmp pairs for chain, star and clique queries
---

The join ordering problem asks for the cheapest way to compute the natural join of $n$ relations: which pairs to join first, and the shape of the join tree. All join trees give the same result, because join is commutative and associative, but the sizes of the intermediate results, and so the costs, can differ by orders of magnitude. The problem is the core of [query optimization](/query-optimization/). It is NP-hard in general, so optimizers use dynamic programming such as the [Selinger enumeration](/selinger-join-enumeration/) for up to about a dozen relations, and heuristics or randomized search above that. For acyclic (tree) query graphs and cost functions with the ASI property, the best left-deep tree without cross products can be found in polynomial time by the IKKBZ algorithm.

## In plain words

A query joins several tables. You can join them in any order and get the same answer. But the work is not the same. If you first join two tables that have few matching rows, the later steps work on a small table. If you first join two tables that have many matching rows, every later step is slow.

So the database must choose the order. There are very many orders: more than three million for 10 tables, and many more if the steps can form a tree. The database estimates the size of each partial result and picks the order with the least total cost. For many tables, finding the very best order is too hard, and the database uses a good guess.

## Definition

**Input.**

- Relations $R_1, \ldots, R_n$ with estimated cardinalities $|R_i|$.
- A *query graph* $G$ with one node per relation and an edge $\{i, j\}$ for each join predicate between $R_i$ and $R_j$, labeled with its [selectivity](/selectivity/) $f_{ij}$. For a pair with no edge, $f_{ij} = 1$.
- A cost function $C$ on join trees.

Under the independence assumption, the size of the join of a set $S$ of relations is

$$|S| = \prod_{i \in S} |R_i| \cdot \prod_{\{i, j\} \subseteq S} f_{ij}.$$

**Output.** A join tree $T$, a binary tree whose leaves are $R_1, \ldots, R_n$, each once, from a given class of trees, with the least $C(T)$.

A standard cost function is $C_{\text{out}}$, the sum of the sizes of the results of all join nodes:

$$C_{\text{out}}(R_i) = 0, \qquad C_{\text{out}}(T_1 \bowtie T_2) = |T_1 \bowtie T_2| + C_{\text{out}}(T_1) + C_{\text{out}}(T_2).$$

It ignores the join algorithms. A physical [cost model](/cost-model/) also chooses an algorithm per join, which makes the problem larger but does not change its structure.

## Variants

- **Tree shape.** *Left-deep* trees (the right input of each join is a base relation) suit pipelines and index nested loop joins. *Bushy* trees allow any shape. *Zigzag* trees allow a base relation on either side. See [query plan](/query-plan/) for the shapes.
- **Cross products.** A join of two sets that have no edge between them is a cross product. Most systems forbid cross products, which shrinks the search space, but sometimes a cross product of two small relations is the best first step.
- **Query graph shape.** *Chain*, *star*, *cycle*, *tree* (acyclic) and *clique* graphs have very different numbers of valid plans.
- **Cost function.** $C_{\text{out}}$, the cost of nested loop joins ($C_{\text{nl}}$), a physical cost model, or the response time for parallel plans.
- **Physical properties.** The order of a result can save a later sort (*interesting orders*), so the optimizer must sometimes keep more than one plan per subset.

## Examples

**A chain of four relations.** Let $|R_1| = 100$, $|R_2| = 1000$, $|R_3| = 100$, $|R_4| = 10$, with the edges $R_1 - R_2$ ($f = 1/100$), $R_2 - R_3$ ($f = 1/2$) and $R_3 - R_4$ ($f = 1/2$). Then $|R_1 \bowtie R_2| = 1000$, $|R_2 \bowtie R_3| = 50\,000$, $|R_3 \bowtie R_4| = 500$, and the full result has $250\,000$ tuples, which every plan pays once in $C_{\text{out}}$.

| plan | intermediate results | $C_{\text{out}}$ |
|---|---|---|
| greedy: smallest join first, then the smallest next result: $((R_3 \bowtie R_4) \bowtie R_2) \bowtie R_1$ | 500, 250 000 | 500 500 |
| best left-deep tree without cross products: $((R_1 \bowtie R_2) \bowtie R_3) \bowtie R_4$ | 1000, 50 000 | 301 000 |
| best left-deep tree with cross products: $((R_1 \bowtie R_2) \times R_4) \bowtie R_3$ | 1000, 10 000 | 261 000 |
| best bushy tree: $(R_1 \bowtie R_2) \bowtie (R_3 \bowtie R_4)$ | 1000, 500 | 251 500 |

The greedy choice of the smallest first join is a trap here: $R_3 \bowtie R_4$ is small, but every left-deep tree that starts with it must next join $R_2$, which gives 250 000 tuples. The bushy tree joins both small pairs and keeps every intermediate result small. A cross product with the 10 tuples of $R_4$ also beats every left-deep tree without cross products.

**A star query.** A fact table $F$ with $10^6$ tuples joins two filtered dimension tables $D_1$ (2 tuples) and $D_2$ (3 tuples), each with $f = 1/100$. Without cross products, the best plan is $(F \bowtie D_1) \bowtie D_2$ with $C_{\text{out}} = 20\,000 + 600$. With the cross product $D_1 \times D_2$ (6 tuples) first, $C_{\text{out}} = 6 + 600$. Star queries in data warehouses are the main case in which optimizers allow cross products.

## Known algorithms

- **Exhaustive dynamic programming.** The [Selinger enumeration](/selinger-join-enumeration/) of System R finds the best left-deep tree by DP over subsets, in $O(n\, 2^n)$ steps with cross products allowed. For bushy trees, DPsub tries all splits of all subsets, $O(3^n)$ pairs. DPccp (Moerkotte and Neumann 2006) enumerates only pairs of connected subgraphs with an edge between them, so its work equals the number of such *csg-cmp pairs*, the least that any DP of this kind must consider.
- **Interval DP for chains.** For a chain query without cross products, every connected set of relations is an interval $R_i, \ldots, R_j$. The DP over intervals has the same structure as [matrix chain multiplication](/matrix-chain-multiplication/) and runs in $O(n^3)$ time. The difference is the cost: the matrix chain cost of a split depends only on the three dimensions at its ends, while the join cost depends on the size of the whole interval's result.
- **IKKBZ.** For tree query graphs, left-deep trees without cross products, and a cost function with the *adjacent sequence interchange* (ASI) property, such as $C_{\text{out}}$ or the nested loop cost, the optimal order is found in polynomial time. Fix a root; the tree becomes a precedence order (a relation comes after its parent). Each relation gets a *rank* $(T - 1)/C$, where $T$ is its size factor ($|R_i| \cdot f$ to its parent) and $C$ its cost. A child with a smaller rank than its parent is merged into it, and the chains are merged by increasing rank. Trying every root gives the optimum. Ibaraki and Kameda (1984) gave $O(n^2 \log n)$ time; Krishnamurthy, Boral and Zaniolo (1986) improved it to $O(n^2)$. The method comes from job sequencing with tree precedence constraints.
- **Greedy heuristics.** Start with the pair with the smallest result (or the smallest relation) and repeatedly add the relation, or for bushy trees join the pair of subtrees, that gives the smallest next result (GOO, greedy operator ordering). These are fast, $O(n^3)$ or less, but they can be far from optimal, as the chain example shows.
- **Randomized and genetic search.** Iterative improvement and simulated annealing move through the space of join trees by local changes such as swaps and rotations; Steinbrunn, Moerkotte and Kemper (1997) compared them. PostgreSQL switches from DP to a genetic search (GEQO) at 12 relations by default (`geqo_threshold`).
- **Worst-case optimal joins.** For cyclic queries, any binary join tree can produce intermediate results larger than the final result. [Multiway joins](/multiway-join/) such as [generic join](/generic-join/) avoid binary trees and run within the [AGM bound](/agm-bound/); for acyclic queries the [Yannakakis algorithm](/yannakakis-algorithm/) bounds the intermediate results by the input plus the output. These avoid the ordering problem for binary joins but still choose an order of variables.

## Bounds

**Size of the search space.** With cross products, there are $n!$ left-deep trees and $(2(n-1))!/(n-1)!$ bushy trees over $n$ relations; for $n = 10$ that is 3 628 800 and 17 643 225 600. The number of left-deep trees without cross products depends on the query graph: $2^{n-1}$ for a chain, $2(n-1)!$ for a star, and $n!$ for a clique. The [query plan](/query-plan/) page derives these counts.

**Work of DPccp.** The number of csg-cmp pairs (unordered pairs of disjoint connected sets joined by an edge) is $(n^3 - n)/6$ for a chain, $(n-1)\, 2^{n-2}$ for a star and $(3^n - 2^{n+1} + 1)/2$ for a clique; these counts match an enumeration for $n \le 7$. So a chain of 20 relations needs 1330 pairs, while a clique of 20 needs about $1.7 \cdot 10^9$.

**Hardness.** Ibaraki and Kameda (1984) proved that finding the optimal nesting order (a left-deep tree, nested loop costs) is NP-complete for general query graphs. Cluet and Moerkotte (1995) proved that finding the optimal left-deep tree with cross products is NP-hard under $C_{\text{out}}$. So no polynomial algorithm is expected for the general problem, and the exponential DP is the exact method in practice.

**Polynomial cases.** For tree queries with ASI cost functions and left-deep trees without cross products, IKKBZ gives $O(n^2)$. For chain queries and bushy trees without cross products, the interval DP gives $O(n^3)$.

## Reductions

- **Matrix chain multiplication** has the same recursive structure as bushy join ordering for a chain query without cross products: both choose the last split of an interval and recurse. See [matrix chain multiplication](/matrix-chain-multiplication/).
- **Sequencing with precedence constraints.** Left-deep join ordering for a tree query with a fixed first relation is the problem of ordering jobs under a tree-shaped precedence order with an ASI cost; IKKBZ is based on the solution of that problem. The ordering of expensive selection predicates by rank, as in [predicate pushdown](/predicate-pushdown/), is the same rank rule without precedence.
- **Cardinality estimation is an input.** Every algorithm above is exact only for the estimated sizes; if the [cardinality estimates](/cardinality-estimation/) are wrong, the optimal plan for the estimates can be a poor plan for the data.

## Applications

Every relational database system with a cost-based optimizer solves this problem for each query with joins: System R and its successors with DP over subsets, PostgreSQL with DP and a genetic fallback, and data warehouse systems with special rules for star queries. The same problem appears for the joins in SPARQL queries over triple stores, where queries often have many self-joins, and for the order of operations in Datalog rule bodies.

## References
