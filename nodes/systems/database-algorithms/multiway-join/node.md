---
tag: HXYPG7
kind: problem
slug: multiway-join
name: Multiway join problem
aliases:
- Multiway join
- multi-way join
- multi-relation natural join
area: systems/database-algorithms
level: advanced
summary: "Given three or more relations, compute their natural join. Plans of two-way joins can build intermediate results far larger than the output; multiway algorithms avoid this."
prereqs: [relational-join, hash-join]
see_also: [agm-bound, generic-join, yannakakis-algorithm, leapfrog-triejoin, hypercube-shares-join, join-ordering, hypergraph, triangle-listing-by-degree]
sources:
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Dániel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 2013
    locator: the bound on the output size by fractional edge covers, its tightness, and the gap between join-project plans and the bound
  - paper: doi:10.1145/3180143
    title: Hung Q. Ngo, Ely Porat, Christopher Ré and Atri Rudra, Worst-case optimal join algorithms, Journal of the ACM 65(3), 2018
    locator: the worst-case optimal join algorithm and the lower bound for plans of pairwise joins on the triangle query and its relatives
  - paper: doi:10.1145/2590989.2590991
    title: Hung Q. Ngo, Christopher Ré and Atri Rudra, Skew strikes back, new developments in the theory of join algorithms, SIGMOD Record 42(4), 2013
    locator: the triangle query example where every pairwise plan is slow, and the generic join algorithm
  - paper: doi:10.1145/1739041.1739056
    title: Foto N. Afrati and Jeffrey D. Ullman, Optimizing joins in a map-reduce environment, EDBT 2010
    locator: the one-round multiway join with shares of the attributes, and the comparison with cascades of two-way joins
---

The multiway join problem asks for the natural join $R_1 \bowtie R_2 \bowtie \cdots \bowtie R_n$ of three or more relations. The [relational join problem](/relational-join/) is the case of two relations. Every multiway join can be computed as a *binary plan*: a tree of two-way joins, each done by an algorithm such as the [hash join](/hash-join/). This page adds what changes with many relations. The order and shape of the binary joins matter, and on some queries every binary plan builds intermediate results far larger than both the input and the output. The triangle query is the standard case. A *multiway* algorithm that looks at all relations at once can avoid this: [generic join](/generic-join/) runs within the [AGM bound](/agm-bound/) on the output size, and the [Yannakakis algorithm](/yannakakis-algorithm/) runs in time linear in the input plus the output when the query is acyclic.

## In plain words

You have three lists: who follows whom, who likes which post, and who wrote which post. You want every person who follows the author of a post they liked. Each line of the answer must agree with all three lists at once.

The usual way is to join two lists, then join the result with the third. But the middle result can be huge. Many people follow many others, so "follows, then likes" can give millions of lines, even if the final answer has ten. A multiway method builds the answer one column at a time. It tries a person, then only the posts that both lists allow for that person, and so on. So it never writes the huge middle list.

## Definition

A *join query* is given by a [hypergraph](/hypergraph/) $H = (V, E)$: the vertices $V$ are the attributes, and each edge $e \in E$ is the attribute set of one relation $R_e$. A database $D$ gives a finite set of tuples $R_e$ over the attributes $e$ for each edge. The output is
$$Q(D) = \{\, t : t \text{ is a tuple over } V \text{ and } t[e] \in R_e \text{ for every } e \in E \,\},$$
where $t[e]$ is the restriction of $t$ to the attributes of $e$. This is the natural join of all the relations, also called a *full conjunctive query*. Write $n = \sum_e |R_e|$ for the input size, $N$ for the size of each relation when they are equal, and $T = |Q(D)|$ for the output size. The query is fixed, so its size counts as a constant in the bounds below, unless stated otherwise.

**Binary plans and multiway plans.** A *binary plan* is a rooted tree with the relations at the leaves, in which each inner node joins the results of its two children. The relation at an inner node is an *intermediate result*, and a binary plan takes at least time proportional to the sum of the sizes of its intermediate results. A *multiway plan* is any algorithm that is not restricted to this form. Atserias, Grohe and Marx also consider join-project plans, which may project away attributes between joins.

**Acyclic and cyclic queries.** A query is *acyclic* (alpha-acyclic) if its hypergraph has a join tree: a tree on the relations in which the relations that hold an attribute form a connected subtree. The path $R(A, B) \bowtie S(B, C) \bowtie T(C, D)$ is acyclic. The triangle $R(A, B) \bowtie S(B, C) \bowtie T(C, A)$ is cyclic. See [acyclic join evaluation](/acyclic-join-evaluation/).

## Variants

- **Full or with projection.** Here all attributes are output. With a projection the query is a general conjunctive query, and with no output attributes it is a Boolean query, which asks only whether $Q(D)$ is empty.
- **Acyclic queries.** The [Yannakakis algorithm](/yannakakis-algorithm/) first removes every dangling tuple with [semijoins](/semijoin/) along the join tree and then joins along the tree.
- **Cyclic queries.** The worst-case optimal algorithms [generic join](/generic-join/) and [leapfrog triejoin](/leapfrog-triejoin/) bind one attribute at a time.
- **One round on a cluster.** In the MapReduce setting, the [hypercube or Shares join](/hypercube-shares-join/) of Afrati and Ullman sends each tuple to a set of reducers in a grid, so that every output tuple meets at one reducer, in one round. The aliases "conjunctive query evaluation in MapReduce" and "multi-relation join in one round" refer to this setting.
- **Choosing a binary plan.** When the algorithm is a binary plan, the problem of picking the best tree is [join ordering](/join-ordering/), solved in systems by dynamic programming as in [Selinger join enumeration](/selinger-join-enumeration/).
- **Graph patterns.** With one edge relation used several times, the query lists the copies of a small pattern in a graph, such as triangles or cliques.

## Examples

**The triangle query and the intermediate blowup.** Let $Q_\triangle = R(A, B) \bowtie S(B, C) \bowtie T(C, A)$. Take $R = S = T = \{(0, i) \mid 1 \le i \le m\} \cup \{(i, 0) \mid 1 \le i \le m\}$, the edges of a star with center 0 in both directions. Each relation has $N = 2m$ tuples.

- **The output.** A triangle $(a, b, c)$ needs $(a, b)$, $(b, c)$ and $(c, a)$ all to be edges. Every edge touches 0, so two of $a, b, c$ would be 0, and $(0, 0)$ is not an edge. So $Q_\triangle$ is empty.
- **A binary plan.** Join $R$ and $S$ on $B$ first. A tuple $(i, 0)$ of $R$ meets all $m$ tuples $(0, j)$ of $S$, which gives $m^2$ tuples, and a tuple $(0, i)$ meets $(i, 0)$, which gives $m$ more. So $|R \bowtie S| = m^2 + m$. The relations are equal and the query is symmetric, so $S \bowtie T$ and $T \bowtie R$ have the same size. Every binary plan must start with one of these three joins.

| $m$ | tuples per relation | first intermediate result | output | $N^{3/2}$ |
|---|---|---|---|---|
| 10 | 20 | 110 | 0 | 89 |
| 100 | 200 | 10,100 | 0 | 2,828 |
| 1000 | 2000 | 1,001,000 | 0 | 89,443 |

A script computed the intermediate sizes and checked that there is no triangle. For $m = 1000$, the inputs have 6000 tuples in total, the output is empty, and every binary plan builds a million tuples, about $N^2/4$. The [AGM bound](/agm-bound/) for the triangle is $N^{3/2}$, about 89,000 here, and generic join does at most that much work, up to factors that depend only on the query.

**The bound is reached.** Take $R = S = T = \{0, \dots, k - 1\}^2$, so $N = k^2$. Every triple is a triangle, so $|Q_\triangle| = k^3 = N^{3/2}$. For $k = 30$, $N = 900$ and the output has 27,000 tuples. So no algorithm can beat $N^{3/2}$ in the worst case, and the gap between binary plans and multiway plans on the triangle is a factor of about $N^{1/2}$.

**An acyclic query.** Let $R(A, B) = \{(1, 1), (2, 2), (3, 3)\}$, $S(B, C) = \{(1, 5), (2, 6), (4, 7)\}$ and $T(C, D) = \{(5, 8), (7, 9)\}$. The plan $(R \bowtie S) \bowtie T$ builds 2 intermediate tuples for 1 output tuple, $(1, 1, 5, 8)$. After the semijoin passes of the Yannakakis algorithm, worked out on the page [semijoin](/semijoin/), each relation holds one tuple, and no intermediate result of a plan along the join tree is larger than the output.

## Known algorithms

- **Binary plans.** Any tree of two-way joins, each computed by a method of the [relational join problem](/relational-join/), in an order chosen by [join ordering](/join-ordering/). This is what most systems do. On the triangle it takes $\Theta(N^2)$ time in the worst case, as the example shows.
- **[Yannakakis algorithm](/yannakakis-algorithm/) (1981).** For acyclic queries, two passes of semijoins along the join tree and then the joins, in $O(n + T)$ time for a fixed query.
- **[Generic join](/generic-join/) and NPRR.** Ngo, Porat, Ré and Rudra (2012) gave the first algorithm that runs within the AGM bound on every query. Generic join is the simple form in "Skew strikes back" (2013): bind one attribute at a time and intersect the candidate values, looping over the smallest set.
- **[Leapfrog triejoin](/leapfrog-triejoin/).** Veldhuizen's algorithm for sorted tries does the same intersections with seeks, and is also worst-case optimal up to a log factor.
- **[Triangle listing by degree](/triangle-listing-by-degree/).** For the triangle query on one graph, orienting each edge toward the endpoint of higher degree lists all triangles in $O(m^{3/2})$ time for $m$ edges, which matches the AGM bound.
- **[Hypercube or Shares join](/hypercube-shares-join/).** One round on a cluster, with the share of each attribute chosen to minimize the data sent.

## Bounds

- **Output size.** By the [AGM bound](/agm-bound/), $|Q(D)| \le \prod_e |R_e|^{x_e}$ for every fractional edge cover $x$ of $H$, and the best cover gives a bound that some database reaches. For the triangle, $x = (\tfrac12, \tfrac12, \tfrac12)$ gives $\sqrt{|R| |S| |T|}$, which is $N^{3/2}$ for equal sizes.
- **Worst-case optimal time.** Generic join and leapfrog triejoin run in $O(n + \mathrm{AGM})$ time up to factors in the query size and a log factor, which no algorithm can beat on all databases with given relation sizes, because the output alone can be that large.
- **Binary plans are not optimal.** On the star instance of the example, every binary plan for the triangle builds $\Theta(N^2)$ tuples while the AGM bound is $N^{3/2}$. Atserias, Grohe and Marx compared join plans and join-project plans with the bound, and Ngo, Porat, Ré and Rudra gave families of queries for which every join-project plan is slower than the bound by a factor that grows polynomially with $N$.
- **Acyclic queries.** $O(n + T)$ by Yannakakis, which is optimal for a fixed query, because any algorithm must read the input and write the output.
- **The query as input.** If the query is part of the input, even deciding whether a conjunctive query has an answer is NP-complete, by a reduction from clique (Chandra and Merlin, 1977). The bounds above treat the query as fixed.

## Reductions

- **To binary joins.** A multiway join is a sequence of $n - 1$ two-way joins, so every algorithm of the [relational join problem](/relational-join/) gives one. The reduction is correct for any order but can be slow, as above.
- **From graph patterns.** Listing the triangles of a graph with edge set $E$ is the triangle query with $R = S = T = E$. Listing the $k$-cliques is the query with one relation $E(A_i, A_j)$ for each pair $i < j$.
- **To semijoins, for acyclic queries.** By the reducer identity of the [semijoin](/semijoin/), semijoins along a join tree remove all dangling tuples, and the remaining binary plan along the tree has intermediate results no larger than the output. For cyclic queries this fails: the semijoin page shows three relations that no semijoin reduces while their join is empty.
- **To one round of communication.** The hypercube join reduces the multiway join on $p$ machines to local joins of the tuples each machine receives.

## Applications

- **Graph queries.** Subgraph patterns, such as triangles, cliques and cycles, in graph databases and in network analysis. These are cyclic queries, where multiway algorithms help most.
- **Datalog and rule engines.** Systems that evaluate many rules with cyclic bodies, such as the LogicBlox engine, for which Veldhuizen designed leapfrog triejoin.
- **Data warehouses.** Star joins of a fact table with several dimension tables. These are acyclic, and systems use binary plans with filters, such as the bitmap filters of the [Bloom join](/bloom-join/).
- **Distributed joins.** Joins of several large tables on a cluster, where one round of the hypercube join can send less data than a cascade of [reduce-side joins](/reduce-side-join/).
- **Query optimizers.** The optimizer decides between binary plans in some order and, in newer systems, a multiway operator for the cyclic parts of a query.

## References
