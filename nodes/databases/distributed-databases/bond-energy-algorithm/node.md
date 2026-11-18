---
tag: J9KWFD
kind: algorithm
slug: bond-energy-algorithm
name: Bond energy algorithm
aliases:
- BEA
- McCormick bond energy clustering
area: databases/distributed-databases
level: advanced
summary: "A greedy heuristic that permutes the rows and columns of a matrix so that large values sit next to each other. On an attribute affinity matrix it groups attributes that queries use together."
model: word-ram
complexity:
  vars: {a: the number of attributes (columns of the matrix), q: the number of queries in the workload}
  time: {worst: "O(a^3)"}
  space: {extra: "O(a^2)"}
properties: {deterministic: true, exact: false, online: false, in_place: false, recursive: false}
history:
  year: 1972
  people: [William T. McCormick, Paul J. Schweitzer, Thomas W. White]
  note: "McCormick, Schweitzer and White (1972) gave the bond energy algorithm as a general method to cluster the rows and columns of a data matrix. Navathe, Ceri, Wiederhold and Dou (1984) used it on an attribute affinity matrix to find vertical fragments."
prereqs: [vertical-fragmentation]
see_also: [horizontal-fragmentation, data-allocation-problem, schism-partitioning, traveling-salesman-problem, greedy-algorithm, decomposition-storage-model, k-means, local-search]
sources:
  - paper: doi:10.1287/opre.20.5.993
    title: William T. McCormick, Paul J. Schweitzer and Thomas W. White, Problem decomposition and data reorganization by a clustering technique, Operations Research 20(5), 1972, pages 993 to 1009
    locator: the measure of effectiveness of a permuted matrix and the bond energy algorithm, which places one column at a time at its best position
  - paper: doi:10.1145/1994.2209
    title: Shamkant Navathe, Stefano Ceri, Gio Wiederhold and Jinglie Dou, Vertical partitioning algorithms for database design, ACM Transactions on Database Systems 9(4), 1984, pages 680 to 710
    locator: the attribute affinity matrix, its clustering by the bond energy algorithm, and the split of the clustered attributes into fragments
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 2, Distributed and Parallel Database Design, the section on vertical fragmentation
---

The bond energy algorithm (BEA) reorders the rows and the columns of a matrix so that large values come together in blocks. McCormick, Schweitzer and White gave it in 1972 as a general method to cluster any data matrix. In database design, its input is the attribute affinity matrix of a workload, and the blocks of the result are groups of attributes that the queries use together, which are good candidates for a [vertical fragmentation](/vertical-fragmentation/). BEA is a [greedy](/greedy-algorithm/) heuristic: each step is the best possible insertion, but the final order is not always the best order.

## In plain words

A table has many columns, and the queries of a workload read only some of them. Two columns are close when many queries read both. BEA puts the columns in a row, one at a time. Each new column goes into the place where it sits next to the columns that it is closest to. At the end, close columns stand side by side, and the row of columns falls into a few groups. A second step cuts the row at the point that best separates the queries, and each part becomes a fragment of the table. Each part also keeps the key, so the table can be put back together.

## The problem

The input is a symmetric $a \times a$ matrix $AA$ with non-negative entries. For a workload of $q$ queries, where query $k$ uses the set of attributes $U_k$ and runs $f_k$ times in total over all sites, the attribute affinity matrix is $AA(i, j) = \sum f_k$ over the queries $k$ that use both $A_i$ and $A_j$. The bond of two columns is $\mathrm{bond}(x, y) = \sum_z AA(z, x) \, AA(z, y)$, the inner product of the two columns, and the bond with an empty place outside the order is 0. For an order $c_1, \dots, c_a$ of the columns, with the rows in the same order, the global affinity measure is

$$AM = \sum_{j=1}^{a} \big(\mathrm{bond}(c_j, c_{j-1}) + \mathrm{bond}(c_j, c_{j+1})\big) = 2 \sum_{j=1}^{a-1} \mathrm{bond}(c_j, c_{j+1}).$$

The goal is an order with a large $AM$. For a symmetric matrix whose rows and columns move together, $AM$ is the measure of effectiveness of McCormick et al. Finding the order of largest $AM$ is a maximum weight Hamiltonian path problem on the columns, a form of the [traveling salesman problem](/traveling-salesman-problem/), and BEA does not solve it exactly.

## The algorithm

```pseudo id=main
BEA(AA)    ▷ AA is a symmetric a × a matrix; the result is an order of the columns and the clustered matrix
L1  order ← (A_1, A_2)
L2  for k = 3, ..., a do
L3      for each place loc = 0, ..., k - 1 in order do    ▷ between the neighbors A_i and A_j, or at an end
L4          value(loc) ← cont(A_i, A_k, A_j) = 2 bond(A_i, A_k) + 2 bond(A_k, A_j) - 2 bond(A_i, A_j)
L5      insert A_k into order at the leftmost place of largest value
L6  CA ← AA with its rows and columns both in the order of order
L7  return order, CA
```

Line L4 is the change of $AM$ caused by the insertion: the pair $A_i, A_j$ stops being neighbors, and the pairs $A_i, A_k$ and $A_k, A_j$ become neighbors. At an end of the order, the missing neighbor is an empty place and its bonds are 0. Line L6 orders the rows the same way as the columns, which keeps the matrix symmetric.

**The split step.** For vertical fragmentation, a second step cuts the clustered order into a top part $TA$ and a bottom part $BA$. For each split point, $CTQ$ is the total frequency of the queries that use only attributes of $TA$, $CBQ$ the same for $BA$, and $COQ$ the total frequency of the queries that use both parts. The step picks the split point with the largest $z = CTQ \cdot CBQ - COQ^2$ and adds the primary key to both fragments, so that a join on the key gives back the table. This rule is from Navathe et al. (1984). It is a rule of thumb, not the optimum of a cost model.

## Example

A relation has the attributes $A_1$ to $A_4$ and a key. The workload has four queries: $\{A_1, A_3\}$ runs 45 times, $\{A_2, A_3\}$ 5 times, $\{A_2, A_4\}$ 75 times and $\{A_3, A_4\}$ 3 times. The affinity matrix is

| | $A_1$ | $A_2$ | $A_3$ | $A_4$ |
|---|---|---|---|---|
| $A_1$ | 45 | 0 | 45 | 0 |
| $A_2$ | 0 | 80 | 5 | 75 |
| $A_3$ | 45 | 5 | 53 | 3 |
| $A_4$ | 0 | 75 | 3 | 78 |

The bonds that the run needs are $\mathrm{bond}(A_1, A_2) = 225$, $\mathrm{bond}(A_1, A_3) = 4410$, $\mathrm{bond}(A_1, A_4) = 135$, $\mathrm{bond}(A_2, A_3) = 890$, $\mathrm{bond}(A_2, A_4) = 11865$ and $\mathrm{bond}(A_3, A_4) = 768$.

- Line L1 gives the order $A_1 A_2$.
- For $A_3$, the three places give $\mathrm{cont} = 8820$ (before $A_1$), $10150$ (between $A_1$ and $A_2$) and $1780$ (after $A_2$). The order becomes $A_1 A_3 A_2$.
- For $A_4$, the four places give $270$, $-7014$, $23486$ and $23730$. The largest is at the end, and the order becomes $A_1 A_3 A_2 A_4$.

The order has $AM = 2(4410 + 890 + 11865) = 34330$. A search over all 24 orders shows that no order is better here; the starting order $A_1 A_2 A_3 A_4$ has $AM = 3766$. The clustered matrix has two blocks, $\{A_1, A_3\}$ and $\{A_2, A_4\}$, with small entries outside them.

The split step tries three points. After $A_1$: $CTQ = 0$, $CBQ = 83$, $COQ = 45$, $z = -2025$. After $A_3$: $CTQ = 45$, $CBQ = 75$, $COQ = 8$, $z = 3311$. After $A_2$: $CTQ = 50$, $CBQ = 0$, $COQ = 78$, $z = -6084$. The best point is after $A_3$, so the fragments are $(\text{key}, A_1, A_3)$ and $(\text{key}, A_2, A_4)$. Only the 8 runs of the two queries that read $A_3$ together with $A_2$ or $A_4$ need both fragments.

## Correctness

BEA is a heuristic, so "correct" here means two facts, both proved on [the proof page](proofs/correctness.md). First, $AM$ is the bond energy of McCormick et al.: for a symmetric matrix with its rows and columns in the same order, the measure of effectiveness $\tfrac{1}{2} \sum_{i,j} a_{ij} (a_{i,j-1} + a_{i,j+1} + a_{i-1,j} + a_{i+1,j})$ equals $2 \sum_j \mathrm{bond}(c_j, c_{j+1})$. Second, the value of line L4 is exactly the change of $AM$, so line L5 picks the best of the $k$ possible insertions of $A_k$ (a theorem about each step). There is no guarantee for the final order.

## Complexity

- **Time (theorem).** A table of all $a(a+1)/2$ bonds costs $O(a^3)$. Step $k$ looks at $k$ places with three lookups each, so all steps cost $O(a^2)$. The total is $O(a^3)$. Building the affinity matrix from the workload costs $O(q a^2)$ more.
- **Space.** $O(a^2)$ for the matrix and the table of bonds.
- **The split step.** A direct count over all split points and queries costs $O(a^2 q)$.

## Properties

- **Not optimal (theorem).** Take four attributes and the queries $\{A_1, A_2\}$ 4 times, $\{A_1, A_4\}$ 2 times and $\{A_1, A_3\}$ once. BEA gives $A_3 A_4 A_1 A_2$ with $AM = 128$, but $A_3 A_2 A_1 A_4$ has $AM = 132$. The tests check this case.
- **Depends on the input order.** The form on this page inserts the columns in their index order, so a different numbering of the attributes can give a different result.
- **Only pairs.** The affinity matrix records how often two attributes are used together, not which larger sets of attributes a query reads. Two workloads with the same pair counts give the same clusters.
- **Deterministic.** With the leftmost place on a tie, the result depends only on the matrix.
- **General.** Nothing in lines L1 to L7 is about databases. Any non-negative matrix can be clustered this way; the original paper used it on problem decomposition and other data.

## Variants and improvements

- **The original form.** McCormick et al. place one column first and then, at each step, try every column not yet placed at every place, and insert the best pair of column and place. This is the cheapest insertion heuristic for the path problem. It costs more, $O(a^3)$ contributions in total with a table of bonds, and it is also not optimal: the tests show a matrix of five columns where no start column reaches the best order.
- **Rectangular matrices.** For a data matrix that is not symmetric, the rows and the columns are ordered apart, each by its own bonds, and the measure of effectiveness is the sum of the two parts.
- **Better searches for the same objective.** Since the objective is a traveling salesman path, any exact solver or a [local search](/local-search/) such as 2-opt can improve the order. For a small number of attributes, a full search is cheap.
- **Many fragments.** The split step can be applied again to each part, or the cut can be done at several points at once. The textbook form of the split also shifts the order in a circle and tries the cuts again, so that a block in the middle of the order can be cut out.
- **Without the matrix order.** Later work groups attributes with other clustering methods or with a cost model of the queries; see [vertical fragmentation](/vertical-fragmentation/).

## When to use it

Use BEA to get a first proposal of vertical fragments from a workload, when the number of attributes is small to medium and the query frequencies are known. Check the proposal with a cost model, because neither the order nor the split rule is optimal. For row stores with many short queries, also compare with the [decomposition storage model](/decomposition-storage-model/), which puts each attribute in its own fragment.

## Pitfalls

- **Forgetting the key.** A vertical fragment without the key cannot be joined back. The split must add the primary key, or a tuple identifier, to each fragment.
- **Reading the order as optimal.** BEA gives a local choice at each step. A different first pair or a different numbering can give a better order.
- **Mixing frequencies and sites.** In a distributed workload the frequency of a query is the sum over all sites where it runs. Using the frequency at one site gives a matrix for that site only.
- **Splitting only at one point.** If the best block is in the middle of the order, a single cut cannot isolate it. Shift the order in a circle or use several cuts.
- **Ties.** The leftmost place on a tie is a choice. Other choices give other orders with the same steps.

## Implementations

## History

McCormick, Schweitzer and White published the bond energy algorithm in Operations Research in 1972. They wanted to find groups in data matrices, such as the parts of a problem that interact, and they measured a permuted matrix by the sum of the products of neighboring entries. Navathe, Ceri, Wiederhold and Dou (1984) built the attribute affinity matrix from a workload, clustered it with BEA, and split the result into vertical fragments. The textbook of Özsu and Valduriez presents this form, with the columns inserted in index order, as the standard method for vertical fragmentation.

## References
