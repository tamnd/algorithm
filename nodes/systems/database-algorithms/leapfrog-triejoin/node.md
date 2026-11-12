---
tag: R8QS9W
kind: algorithm
slug: leapfrog-triejoin
name: Leapfrog triejoin
aliases:
- leapfrog join
- LFTJ
- leapfrog trie join
area: systems/database-algorithms
level: research
summary: "A worst-case optimal multiway join: bind one attribute at a time, and intersect sorted trie levels by seeks that jump each list to the largest current key."
solves: [multiway-join]
model: word-ram
complexity:
  vars: {n: the total number of input tuples, k: the number of attributes, r: the number of relations, a: the AGM bound of the instance}
  time: {worst: O(k n log n + k r a log n)}
  space: {extra: O(k n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [generic-join, binary-search, trie, sorted-array-intersection]
see_also: [agm-bound, multiway-join, exponential-search, sort-merge-join, yannakakis-algorithm, hypercube-shares-join, triangle-listing-by-degree, k-way-merge]
sources:
  - paper: doi:10.5441/002/icdt.2014.13
    title: Todd L. Veldhuizen, Leapfrog triejoin, a simple, worst-case optimal join algorithm, ICDT 2014, 96 to 106 (arXiv 1210.0481)
    locator: the leapfrog join, the trie iterator interface (open, up, next, seek, key, atEnd), and the proof of worst-case optimality
  - paper: doi:10.1145/2590989.2590991
    title: Hung Q. Ngo, Christopher Ré and Atri Rudra, Skew strikes back, new developments in the theory of join algorithms, SIGMOD Record 42(4), 5 to 16 (2013)
    locator: generic join, of which leapfrog triejoin is an instance
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Dániel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 1737 to 1767 (2013)
    locator: the output size bound
---

Leapfrog triejoin is the worst-case optimal join algorithm that Todd Veldhuizen described in 2014 from the LogicBlox database system. It stores each relation as a sorted [trie](/trie/), binds the attributes one at a time in a fixed order, and finds the values of the next attribute with a *leapfrog join*: the list with the smallest current key seeks to the largest current key, round after round, until all lists agree. It is an instance of [generic join](/generic-join/), and its running time is within a log factor of the [AGM bound](/agm-bound/).

## In plain words

Three people each have a sorted list of numbers, and you want the numbers that are on all three lists. Each person points at a number in the list. The person who points at the smallest number jumps forward to the first number that is at least the largest number that anyone points at. Then the next person does the same. When all three point at the same number, write it down, and move one person forward by one.

The jumps skip long runs of numbers that cannot match. A short list makes the others jump far, so the work depends on the shortest list. To join many tables, do this for the first column, then for the next column inside each match, and so on.

## The problem

The input is a full join query with hypergraph $H = (V, E)$, one relation $R_e$ per edge, and an attribute order $v_1, \ldots, v_k$. The output is the natural join, the [multiway join](/multiway-join/) of all relations. Each relation is given as an array of tuples, sorted lexicographically with its attributes in the global order. The cost model is the word RAM with comparisons; $n$ is the total input size, $r = |E|$, and $a = \min_x \prod_e |R_e|^{x_e}$ over the fractional edge covers $x$ is the AGM bound.

## The algorithm

A **trie iterator** views a sorted array as a trie. At each depth it has a range of rows that share the bound prefix; in this range the next column is sorted. It supports `key` (the current value), `next` (move to the next larger value), `seek(x)` (move to the first value at least $x$), `atEnd`, `open` (go one level down, into the rows with the current key) and `up` (go back). With binary search, `next`, `seek` and `open` cost $O(\log n)$.

The **leapfrog join** keeps its $m$ iterators in an array $J$ and an index $p$. Read cyclically from $p$, the keys are in increasing order, so $J_p$ has the smallest key and $J_{p-1}$ the largest.

```pseudo id=main
TRIEJOIN(i)                                     ▷ called as TRIEJOIN(1)
L1  ▷ bind v_i given the bound values of v_1 .. v_(i-1)
L2  if i > k then output the bound tuple; return
L3  J ← the iterators of the edges e ∋ v_i; OPEN each of them
L4  LEAPFROG-INIT(J)
L5  while not atEnd do
L6      bind v_i ← key; TRIEJOIN(i + 1)
L7      LEAPFROG-NEXT(J)
    UP each iterator in J

LEAPFROG-INIT(J)
L8  if some iterator is at its end then atEnd ← true; return
L9  sort J by key; p ← 0; LEAPFROG-SEARCH(J)

LEAPFROG-SEARCH(J)
L10 x' ← key of J[(p - 1) mod m]                ▷ the largest key
    loop
L11     x ← key of J[p]                          ▷ the smallest key
L12     if x = x' then key ← x; return           ▷ all keys agree
L13     SEEK(J[p], x'); if J[p] is at its end then atEnd ← true; return
L14     x' ← key of J[p]; p ← (p + 1) mod m

LEAPFROG-NEXT(J)
L15 NEXT(J[p]); if J[p] is at its end then atEnd ← true; return
L16 p ← (p + 1) mod m; LEAPFROG-SEARCH(J)
```

## Example

**One leapfrog join.** Intersect $A = \{0, 1, 3, 4, 5, 6, 7, 8, 9, 11\}$, $B = \{0, 2, 6, 7, 8, 9\}$ and $C = \{2, 4, 5, 8, 10\}$. After the sort the keys are 0, 0 and 2, so the largest key is 2.

| step | move | new key | largest key |
|---|---|---|---|
| 1 | $A$ seeks 2 | 3 | 3 |
| 2 | $B$ seeks 3 | 6 | 6 |
| 3 | $C$ seeks 6 | 8 | 8 |
| 4 | $A$ seeks 8 | 8 | 8 |
| 5 | $B$ seeks 8 | 8 | 8 |
| 6 | all keys are 8: report 8; $C$ moves next | 10 | 10 |
| 7 | $A$ seeks 10 | 11 | 11 |
| 8 | $B$ seeks 11 | end | stop |

The result is $\{8\}$ after 8 moves, within the bound $m(n_{\min} + 1) = 3 \cdot 6 = 18$, where $n_{\min} = 5$ is the size of the smallest list.

**A triangle query.** For $R(A, B) \bowtie S(B, C) \bowtie T(A, C)$ with $R = \{(1,1), (1,2), (2,1), (2,3)\}$, $S = \{(1,2), (2,3), (3,1), (1,3)\}$ and $T = \{(1,2), (1,3), (2,3), (2,1)\}$, the first leapfrog join intersects the $A$ values of $R$ and $T$ and gives 1 and 2. For $A = 1$, it intersects $R[1] = \{1, 2\}$ with the $B$ values $\{1, 2, 3\}$ of $S$, and so on. The output, in lexicographic order, is $(1,1,2), (1,1,3), (1,2,3), (2,1,3), (2,3,1)$.

## Correctness

Within one leapfrog join, two invariants hold at line L11: the keys read cyclically from $p$ are non-decreasing, and no iterator has moved past a value of the intersection that has not been reported. A seek skips only values below the largest key, which some other list has already passed, so they cannot be in the intersection. When the smallest and the largest key agree, all keys agree and the value is in each list. So the leapfrog join reports the intersection in increasing order. At depth $i$, the keys of the opened iterator of $R_e$ are the values of $v_i$ that agree with the bound prefix, so the triejoin binds $v_i$ to exactly the values that extend the prefix to a partial join. The full proof is in the proof file.

## Complexity

- **One leapfrog join.** The moves visit the iterators in cyclic order, and each move on the iterator with the fewest keys moves it to a larger key. So a leapfrog join of $m$ iterators makes at most $m(n_{\min} + 1)$ moves, where $n_{\min}$ is the smallest number of keys.
- **All levels.** At level $i$, the sum of $n_{\min}$ over all prefixes is the same quantity $W_i$ that bounds generic join, and $W_i \le a$ by the entropy argument of the AGM bound. With binary search, the total time is $O(k n \log n + k r a \log n)$, including the sort.
- **Veldhuizen's bound.** With seeks that gallop from the current position, a leapfrog join costs $O(n_{\min} \log(n_{\max} / n_{\min}))$, and the whole join costs $O(a \log n)$ for a fixed query.
- **Space.** The sorted arrays take $O(k n)$; each iterator keeps a stack of at most $k$ ranges.

## Properties

- **Output in order.** The output comes in lexicographic order of the attribute order, which helps when the result feeds a merge or a group-by.
- **No intermediate relations.** The state is one position per relation per level.
- **Plain data structures.** The input can be any sorted, indexed storage with seek: a B-tree, a sorted array or a sorted file. No hash table is built at query time.
- **Order dependent cost.** The bound holds for each attribute order, but the actual work on an instance can differ much between orders.

## Variants and improvements

- **[Generic join](/generic-join/).** The same attribute-at-a-time plan with hash tries and an intersection that loops over the smallest set.
- **Galloping seeks.** [Exponential search](/exponential-search/) from the current position makes many short seeks cheap and gives the amortized bound in Veldhuizen's paper.
- **Minesweeper and tetris joins.** Later work uses gap boxes to reach beyond worst-case optimality on some instances.
- **Hybrid plans.** Systems such as LogicBlox, EmptyHeaded and Umbra use leapfrog or generic join for the cyclic parts of a query and pairwise joins elsewhere.
- **Parallel.** Each worker of the [HyperCube (shares) join](/hypercube-shares-join/) can run leapfrog triejoin on its share.

## When to use it

Use leapfrog triejoin for cyclic queries on graph data (triangles, cliques, cycles) when the relations are already stored sorted, for example in B-trees with a suitable key order, and when ordered output is useful. If the data is not sorted in the attribute order, building hash tries for generic join can be cheaper than sorting. For acyclic queries with small outputs, the [Yannakakis algorithm](/yannakakis-algorithm/) is output sensitive and often faster.

## Pitfalls

- **Index order.** Each relation must be sorted with its attributes in the global order. A relation stored in another order needs a second index or a sort.
- **Seek from the current position.** A seek that searches the whole range every time still gives the right result, but the move bound needs the search to start at the current position, and the amortized bound needs galloping.
- **Sort the iterators at init.** The search assumes that the cyclic order of keys is increasing. Skipping the sort in LEAPFROG-INIT can report a value that is not in every list.
- **Restore state.** Each `open` needs a matching `up`, also when the leapfrog join stops early; otherwise the iterators of the outer level are in the wrong range.

## Implementations

## History

Veldhuizen designed leapfrog triejoin for the LogicBlox system, and published it in 2012 as a technical report (arXiv 1210.0481) and at ICDT 2014. The paper proved that the algorithm is worst-case optimal, matching the bound of Atserias, Grohe and Marx (2008) and the algorithm of Ngo, Porat, Ré and Rudra (2012). Ngo, Ré and Rudra (2013) then showed that both algorithms are instances of generic join.

## References
