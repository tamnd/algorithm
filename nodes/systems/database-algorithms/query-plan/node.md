---
tag: MHRFHJ
kind: concept
slug: query-plan
name: Query plan
aliases:
- execution plan
- query execution plan
- query evaluation plan
- physical query plan
area: systems/database-algorithms
level: intro
summary: "A tree of operators that computes a query. A logical plan uses algebra operators; a physical plan names the algorithm and access path for each one."
prereqs: [relational-algebra]
see_also: [query-optimization, iterator-model, cost-model, join-ordering, selinger-join-enumeration, predicate-pushdown, relational-join, matrix-chain-multiplication]
sources:
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Chapter 16, The Query Compiler (logical query plans, physical plans, join trees, left-deep join trees)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 12 (overview of query evaluation and query plans) and Chapter 15 (a typical relational query optimizer, left-deep plans)
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2) (1993)
    locator: Section 1 (query plans as trees of operators) and the sections on the shapes of join trees for parallel execution
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: Section 5, Access path selection for joins (an n-way join as a sequence of 2-way joins, n factorial join orders), p. 28
---

A query plan is a tree of operators that computes the answer to a query. The leaves read stored relations, each inner node takes the outputs of its children as input, and the root produces the answer. A *logical plan* is a tree of [relational algebra](/relational-algebra/) operators; a *physical plan* also says which algorithm runs each operator, for example a [hash join](/hash-join/) or an index scan. The [query optimizer](/query-optimization/) chooses the plan and the [executor](/iterator-model/) runs it.

## In plain words

A query says what answer you want, not how to get it. A plan is the "how". Think of a recipe drawn as a tree. At the bottom, you take the ingredients: you read the tables from disk. Each step above takes one or two results from below and makes a new one: it keeps only some rows, it drops some columns, or it matches the rows of two tables. The top step gives the answer.

One query has many plans that give the same answer. They can join the tables in a different order, filter rows earlier or later, or use a different method for each step. Their costs can differ by many orders of magnitude. So the database builds many candidate plans, estimates the cost of each one, and runs the cheapest.

## The idea

### Logical and physical plans

A **logical plan** is an expression of the relational algebra, drawn as a tree. Its leaves are relation names. Its inner nodes are selection $\sigma$, projection $\pi$, join $\bowtie$, grouping with aggregation $\gamma$, union and difference. Two logical plans are *equivalent* when they give the same result on every database. The algebraic laws (commutativity and associativity of $\bowtie$, the pushing of $\sigma$ through $\bowtie$, and others) turn one logical plan into another equivalent one.

A **physical plan** replaces each logical operator by an algorithm that computes it, and each leaf by an *access path*:

| logical operator | physical choices |
|---|---|
| leaf $R$ | full table scan, index scan, index-only scan |
| $\sigma_p$ | a filter on the input, or an index lookup that applies $p$ |
| $R \bowtie S$ | [nested-loop join](/nested-loop-join/), [block nested-loop join](/block-nested-loop-join/), [index nested-loop join](/index-nested-loop-join/), [sort-merge join](/sort-merge-join/), [hash join](/hash-join/) |
| $\gamma$ | [hash aggregation](/hash-aggregation/), sort-based aggregation |
| (none) | *enforcers*: sort, to give an order that a later operator or ORDER BY needs |

Each physical operator also has *physical properties* of its output, such as a sort order. A sort-merge join produces its output in the order of the join key, and this order can make a later merge join or ORDER BY free. System R called such an order an *interesting order* (see [System R join enumeration](/selinger-join-enumeration/)).

### Edges: pipelined or materialized

An edge of the plan carries tuples from a child to its parent. On a *pipelined* edge, the parent consumes each tuple as soon as the child produces it, and no intermediate result is stored. A *blocking* operator, such as a sort or the build phase of a hash join, must read all of its input before it gives its first output tuple, so the edge into it is in effect materialized. The [iterator model](/iterator-model/) gives one standard way to run a plan with pipelining.

### Shapes of join trees

Let a query join $n$ relations $R_1, \ldots, R_n$. A *join tree* is a binary tree whose $n$ leaves are the relations, each used once, and whose $n - 1$ inner nodes are joins. We write each join as (left input, right input), with the left input as the outer input; the two inputs play different roles in most join algorithms, so $(A \bowtie B)$ and $(B \bowtie A)$ count as two trees.

- **Left-deep**: the right input of each join is a leaf. The tree is a sequence $((R_{i_1} \bowtie R_{i_2}) \bowtie R_{i_3}) \cdots \bowtie R_{i_n}$.
- **Right-deep**: the left input of each join is a leaf.
- **Zigzag**: each join has at least one leaf as input.
- **Bushy**: any join tree. Both inputs of a join can be the results of joins, as in $(A \bowtie B) \bowtie (C \bowtie D)$.

**Counts.** For $n \ge 1$ relations:

$$\#\text{left-deep} = n!, \qquad \#\text{bushy} = n! \cdot C_{n-1} = \frac{(2(n-1))!}{(n-1)!}, \qquad \#\text{zigzag} = n! \cdot 2^{n-2} \ (n \ge 2),$$

where $C_m = \binom{2m}{m}/(m+1)$ is the $m$-th Catalan number.

*Proof.* A left-deep tree is fixed by the order of its leaves from the bottom up, and each of the $n!$ orders gives a different tree. For bushy trees, the number of binary tree shapes with ordered children and $n$ leaves is $C_{n-1}$ (the shapes with $n$ leaves are in bijection with the ways to put parentheses in a product of $n$ factors). Each shape gets the $n$ distinct labels in $n!$ ways, and different labelings of one shape are different trees. So there are $n! \, C_{n-1} = n! \cdot \frac{(2n-2)!}{(n-1)! \, n!} = \frac{(2n-2)!}{(n-1)!}$ trees. A zigzag tree is a path of $n - 1$ joins. The bottom join has two leaves. Each of the other $n - 2$ joins has one leaf and one join as inputs, and the leaf can be on the left or on the right. That gives $2^{n-2}$ shapes, each labeled in $n!$ ways. $\square$

| $n$ | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|
| left-deep $n!$ | 2 | 6 | 24 | 120 | 720 | 40320 | 3628800 |
| zigzag $n! \, 2^{n-2}$ | 2 | 12 | 96 | 960 | 11520 | 2580480 | 928972800 |
| bushy $(2n-2)!/(n-1)!$ | 2 | 12 | 120 | 1680 | 30240 | 17297280 | 17643225600 |

These counts include trees with *cross products*: a join of two inputs that no join predicate connects. Optimizers often skip such trees. Then the count depends on the *query graph*, which has a node for each relation and an edge for each join predicate. For left-deep trees in which each prefix of the order is connected:

- a **chain** query $R_1 - R_2 - \cdots - R_n$ has $2^{n-1}$ such trees: the joined relations always form an interval, so if the first relation is $R_s$, the order is an interleaving of the $s - 1$ relations on its left (taken from right to left) with the $n - s$ relations on its right (taken from left to right); there are $\binom{n-1}{s-1}$ interleavings, and $\sum_{s=1}^{n} \binom{n-1}{s-1} = 2^{n-1}$;
- a **star** query with one center and $n - 1$ satellites has $2 \, (n-1)!$ such trees for $n \ge 2$: each satellite joins only the center, so the center is first or second. With the center first, the satellites follow in $(n-1)!$ orders; with a satellite first and the center second, there are $(n-1)$ choices for the first satellite and $(n-2)!$ orders for the rest;
- a **clique** query has all $n!$ orders.

For $n = 4$ these are 8, 12 and 24; for $n = 7$ they are 64, 1440 and 5040.

## Examples

**One query, two logical plans.** Take `Emp(eid, name, dno)` and `Dept(dno, city)` and the query "the names of the employees whose department is in Paris":

```text
SELECT E.name FROM Emp E, Dept D
WHERE E.dno = D.dno AND D.city = 'Paris'
```

The direct translation is $\pi_{name}(\sigma_{E.dno = D.dno \wedge city = \text{Paris}}(E \times D))$: a cross product, then a filter. The equivalent plan $\pi_{name}(E \bowtie_{dno} \sigma_{city = \text{Paris}}(D))$ filters $D$ first and replaces the product by a join. With $|E| = 10000$ and $|D| = 100$, the first plan builds $10^6$ pairs; the second builds none. The rewrite is [predicate pushdown](/predicate-pushdown/).

**A physical plan for the second logical plan.** Assume an index on `Emp.dno`. One physical plan is:

```text
Project [E.name]                          pipelined
  IndexNestedLoopJoin [D.dno = E.dno]     outer: D, inner: index on Emp.dno
    Filter [D.city = 'Paris']             pipelined
      TableScan Dept
    IndexLookup Emp.dno
```

Another is a hash join that builds a hash table on the filtered `Dept` rows and probes it with a scan of `Emp`. If 2 departments are in Paris, the first plan does 2 index lookups, and the second reads all of `Emp`. If 90 departments are in Paris, the hash join can win. The choice between them is the job of the [cost model](/cost-model/), and it depends on the estimate of the [selectivity](/selectivity/) of `city = 'Paris'`.

**Shapes for four relations.** For $A, B, C, D$: $((A \bowtie B) \bowtie C) \bowtie D$ is left-deep. $A \bowtie (B \bowtie (C \bowtie D))$ is right-deep. $(A \bowtie (B \bowtie C)) \bowtie D$ is zigzag but neither left-deep nor right-deep. $(A \bowtie B) \bowtie (C \bowtie D)$ is bushy and not zigzag. Of the 120 trees, 24 are left-deep, 24 are right-deep and 96 are zigzag.

**Non-example.** The SQL text is not a plan: it fixes no order and no algorithm. A list of the tables in the FROM clause is not a plan either, because many trees of joins match it.

## Where it is used

- [Query optimization](/query-optimization/) searches the space of plans. The counts above are the reason that exhaustive search over bushy trees fails beyond about a dozen relations, and the reason that System R kept only left-deep trees ([System R join enumeration](/selinger-join-enumeration/)). The [join ordering](/join-ordering/) problem is the choice of the tree of joins.
- The [cost model](/cost-model/) assigns a cost to each physical plan, bottom up, from the estimated sizes of the intermediate results ([cardinality estimation](/cardinality-estimation/)).
- The [iterator model](/iterator-model/) runs a physical plan: each node is an object with open, next and close.
- Left-deep trees suit pipelines of index nested-loop joins, because each inner input is a stored relation with an index. Right-deep trees of hash joins build every hash table first and then stream the probe input through all of them, which suits parallel systems with much memory. Bushy trees allow independent subtrees to run in parallel.
- The shape count has the same root as [matrix chain multiplication](/matrix-chain-multiplication/), which also counts parenthesizations by Catalan numbers. There the order of the factors is fixed; in a join tree the leaves can be in any order, which adds the factor $n!$.
- The [materialized view](/materialized-view/) pages treat a stored result of a subplan as a new leaf.

## References
