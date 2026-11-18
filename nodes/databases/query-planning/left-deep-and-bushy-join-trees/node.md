---
tag: F52X6N
kind: concept
slug: left-deep-and-bushy-join-trees
name: Left-deep and bushy join trees
aliases:
- left-deep join tree
- bushy join tree
- zig-zag join tree
area: databases/query-planning
level: core
summary: "The shapes of join plans: a left-deep tree has a base relation as each inner input, a bushy tree may join two intermediate results."
prereqs: [relational-join, query-plan]
see_also: [join-ordering, selinger-join-enumeration, dpccp, ikkbz-algorithm, greedy-operator-ordering, catalan-numbers, pipelining-and-materialization, index-nested-loop-join]
sources:
  - paper: doi:10.1145/582095.582099
    title: "P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34"
    locator: "Section 5, Access path selection for joins (join orders in which each new relation is joined to the result of the relations before it)"
  - paper: "Guido Moerkotte and Thomas Neumann, Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products, Proceedings of VLDB 2006, 930 to 941"
    title: Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products
    locator: the search space of bushy trees without cross products and its size for chain, star and clique queries
---

A join tree is a binary tree whose leaves are the relations of a query and whose inner nodes are joins. Its shape decides which intermediate results exist and how they flow between the operators. In a *left-deep* tree the right input of every join is a base relation, so the tree is a sequence: join the first two relations, then join the result with the third, and so on. In a *bushy* tree both inputs of a join can be results of other joins. This page defines the shapes, counts them and says when each one is used. The [join ordering](/join-ordering/) problem is the choice of the cheapest tree in a given space of shapes, and the [System R join enumeration](/selinger-join-enumeration/) is the classic search of the left-deep space.

## In plain words

You must join four tables. One way is a line: join two tables, then join the result with a third table, then with the fourth. At every step one input is a stored table. That is a left-deep plan.

Another way is to work on two parts at the same time: join the first two tables, join the other two tables, and then join the two results. That is a bushy plan. Bushy plans can keep every partial result small, and the two parts can run in parallel. But there are many more of them, so the search for the best one takes longer. Left-deep plans are fewer, and each step can use an index on the stored table.

## The idea

**Inputs of a join.** This page calls the left input of a join its *outer* input and the right input its *inner* input. For a nested loop join the outer input is read once and the inner input once for each outer tuple, so a base relation with an index on the join column is a good inner input, as in the [index nested-loop join](/index-nested-loop-join/). For a hash join, systems and papers differ in which input they build the hash table on, so the words left-deep and right-deep can change places from one source to the next. Read each source with its own convention.

**Shapes.** For relations $R_1, \ldots, R_n$:

- A **left-deep** tree has the form $((\cdots(R_{i_1} \bowtie R_{i_2}) \bowtie R_{i_3}) \cdots) \bowtie R_{i_n}$. It is fixed by the order $i_1, \ldots, i_n$ of its leaves.
- A **right-deep** tree is the mirror image: the left input of every join is a base relation.
- A **bushy** tree is any binary tree with the $n$ relations as leaves, each leaf once.
- Between them is a third shape, in which every join has at least one base relation as an input, on either side. The [query plan](/query-plan/) page counts it too.

Every left-deep and every right-deep tree is bushy. All of them compute the same result, because the natural join is commutative and associative under both set and bag semantics; the [equivalence rules](/relational-algebra-equivalences/) prove this. Only the intermediate results, and so the costs, differ.

**Counts with cross products.** A left-deep tree is an order of the leaves, so there are $n!$ of them. A bushy tree is a binary tree shape with $n$ leaves and ordered children, labeled with the relations. There are $C_{n-1} = \binom{2n-2}{n-1}/n$ shapes, the [Catalan number](/catalan-numbers/), because a shape is a way to put brackets into a product of $n$ factors. Each shape has $n!$ different labelings, so there are

$$n! \cdot C_{n-1} = n! \cdot \frac{(2n-2)!}{(n-1)!\, n!} = \frac{(2n-2)!}{(n-1)!}$$

bushy trees. For $n = 10$ these are 3 628 800 left-deep trees and 17 643 225 600 bushy trees.

**Counts without cross products.** A join of two inputs that no join predicate connects is a *cross product*. Most optimizers skip trees with cross products, and then the count depends on the *query graph*, with one node for each relation and an edge for each join predicate. A left-deep tree has no cross product exactly when each relation after the first has an edge to an earlier one.

- **Chain** $R_1 - R_2 - \cdots - R_n$: each prefix of the order is an interval of the chain, and after the first relation each step extends the interval to the left or to the right, so there are $2^{n-1}$ left-deep trees. For bushy trees, every subtree covers an interval, and the root splits the interval in $n - 1$ places, with two orders of the inputs. With $T(1) = 1$ and $T(m) = 2 \sum_{a=1}^{m-1} T(a)\, T(m-a)$, the Catalan recurrence gives $T(n) = 2^{n-1} C_{n-1}$.
- **Star** with center $R_0$ and $n - 1$ other relations: the center must be first or second, which gives $(n-1)! + (n-1)(n-2)! = 2(n-1)!$ left-deep trees.
- **Clique**: every order is allowed, so all $n!$ left-deep trees and all bushy trees have no cross product.

## Examples

**Four relations.** For $A, B, C, D$, the tree $((A \bowtie B) \bowtie C) \bowtie D$ is left-deep, $A \bowtie (B \bowtie (C \bowtie D))$ is right-deep, and $(A \bowtie B) \bowtie (C \bowtie D)$ is bushy and neither of the two. With cross products there are $4! = 24$ left-deep trees and $6!/3! = 120$ bushy trees. For the chain $A - B - C - D$ without cross products there are $2^3 = 8$ left-deep trees and $2^3 \cdot C_3 = 8 \cdot 5 = 40$ bushy trees.

**A bushy tree that is cheaper.** Take the chain $A - B - C - D$ with $|A| = |D| = 100$, $|B| = |C| = 1000$, and selectivities $1/1000$ on the edges $A - B$ and $C - D$ and $1/100$ on $B - C$. Then $|A \bowtie B| = |C \bowtie D| = 100$, $|B \bowtie C| = 10\,000$, $|A \bowtie B \bowtie C| = |B \bowtie C \bowtie D| = 1000$, and the result has 100 tuples. Take as the cost the sum of the sizes of the results of all joins.

| tree | results of the joins | cost |
|---|---|---|
| $((A \bowtie B) \bowtie C) \bowtie D$ | 100, 1000, 100 | 1200 |
| $((B \bowtie C) \bowtie A) \bowtie D$ | 10 000, 1000, 100 | 11 100 |
| $((A \bowtie B) \times D) \bowtie C$ | 100, 10 000, 100 | 10 200 |
| $(A \bowtie B) \bowtie (C \bowtie D)$ | 100, 100, 100 | 300 |

Every left-deep tree must at some point hold three of the four relations, and every set of three costs at least 1000, or 10 000 with a cross product. The bushy tree joins the two small pairs first and never builds a set of three, so it costs a quarter of the best left-deep tree.

**A pipeline.** In the left-deep tree $((A \bowtie B) \bowtie C) \bowtie D$ with index nested loop joins, each tuple of $A$ goes through all three joins before the next tuple is read, and no intermediate result is stored. The inner inputs $B$, $C$ and $D$ are read through their indexes. System R searched only left-deep plans, and this is one of them.

## Where it is used

- **System R and its successors** search only left-deep trees, by dynamic programming over subsets of relations ([System R join enumeration](/selinger-join-enumeration/)). The space is smaller, and every inner input is a stored relation that can use an index.
- **Polynomial cases.** The [IKKBZ algorithm](/ikkbz-algorithm/) finds the best left-deep tree without cross products for a tree query graph and a cost with the ASI property.
- **Bushy search.** [DPccp](/dpccp/) and [DPhyp](/dphyp/) find the best bushy tree without cross products by dynamic programming over connected subgraphs. [Greedy operator ordering](/greedy-operator-ordering/) builds a bushy tree by joining the pair with the smallest result first. Rule-based optimizers such as [Cascades](/cascades-framework/) reach bushy trees by commutativity and associativity.
- **Execution.** A left-deep tree of nested loop joins runs as one [pipeline](/pipelining-and-materialization/). A tree of hash joins with the build inputs all on one side can build all hash tables first and then stream one input through all of them, which needs memory for all tables at the same time. Bushy trees allow two subtrees to run in parallel.

## References
