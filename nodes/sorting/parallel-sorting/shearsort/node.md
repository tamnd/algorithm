---
tag: YNCX5H
kind: algorithm
slug: shearsort
name: Shearsort
area: sorting/parallel-sorting
level: advanced
summary: Mesh sort that alternates sorting rows in snake order and columns, in O(log n) phases.
solves: [mesh-sorting-problem]
model: sorting-network
complexity:
  vars: {n: the number of keys, r: the number of rows, c: the number of columns}
  time: {worst: Θ(n (r + c) log r)}
  space: {extra: Θ(1)}
  depth: {worst: ⌈lg r⌉ (r + c) + c}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [mesh-sorting-problem, odd-even-transposition-sort, zero-one-principle]
see_also: [mesh-sorting-problem, odd-even-transposition-sort, columnsort, zero-one-principle, sorting-network, network-depth, bitonic-sort]
sources:
  - paper: "Isaac D. Scherson, Sandeep Sen and Adi Shamir, Shear sort: a true two-dimensional sorting technique for VLSI networks, Proceedings of the International Conference on Parallel Processing (ICPP), 1986"
    locator: the algorithm and its bound of about sqrt n (lg n + 1) steps on a square mesh
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Chapter 1, Arrays and trees (shearsort on a two-dimensional array, with the proof by the 0-1 principle)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the zero-one principle)
---

Shearsort sorts the $n = rc$ keys of an $r \times c$ mesh into snake order. It repeats a phase of two steps $\lceil \lg r \rceil$ times: sort each row, even rows left to right and odd rows right to left, then sort each column top to bottom. A last row sort finishes the job. Each row and column sort is an [odd-even transposition sort](/odd-even-transposition-sort/) between neighbours, so on a square mesh the whole sort takes $\sqrt{n}(\lg n + 1)$ steps when $\sqrt{n}$ is a power of 2. The proof by the [zero-one principle](/zero-one-principle/) is short: each phase halves the number of rows that are not yet all zeros or all ones.

## In plain words

Cards lie in a grid. First sort every row, but in alternating directions: the first row from left to right, the second from right to left, and so on, like a snake. Then sort every column from top to bottom. Repeat these two steps a few times, and then sort the rows once more.

Why does this work? Think of each card as either small or large. Two rows sorted in opposite directions have their small cards at opposite ends. When the columns are sorted, one of the two rows becomes all small or the other becomes all large. So each round turns at least half of the mixed rows into clean rows. After a few rounds, at most one mixed row is left, and the last row sort fixes it.

## The problem

The input is an $r \times c$ matrix $M$ of keys from a total order, with $M[i][j]$ on processor $P(i, j)$ of a mesh. The output is the same keys in snake order: row $i$ holds the keys of ranks $ic$ to $ic + c - 1$, in increasing order from left to right when $i$ is even and from right to left when $i$ is odd. This is the [mesh sorting problem](/mesh-sorting-problem/). A step is one round of compare-exchanges between disjoint pairs of neighbours.

## The algorithm

```pseudo id=main
SHEARSORT(M[0 .. r − 1][0 .. c − 1])
L1  for phase ← 1 to ⌈lg r⌉ do
L2      parallel for i ← 0 to r − 1 do
L3          sort row i, increasing to the right if i is even, increasing to the left if i is odd
L4      parallel for j ← 0 to c − 1 do
L5          sort column j, increasing downward
L6  parallel for i ← 0 to r − 1 do sort row i as on line L3
```

Each sort on lines L3, L5 and L6 is an odd-even transposition sort, which takes $c$ steps for a row and $r$ steps for a column. All rows, or all columns, are sorted at the same time.

## Example

Sort a $4 \times 4$ mesh, so $\lceil \lg 4 \rceil = 2$ phases.

| after | row 0 | row 1 | row 2 | row 3 |
| --- | --- | --- | --- | --- |
| input | $13, 2, 7, 10$ | $5, 16, 1, 12$ | $9, 4, 15, 8$ | $3, 14, 6, 11$ |
| phase 1, rows | $2, 7, 10, 13$ | $16, 12, 5, 1$ | $4, 8, 9, 15$ | $14, 11, 6, 3$ |
| phase 1, columns | $2, 7, 5, 1$ | $4, 8, 6, 3$ | $14, 11, 9, 13$ | $16, 12, 10, 15$ |
| phase 2, rows | $1, 2, 5, 7$ | $8, 6, 4, 3$ | $9, 11, 13, 14$ | $16, 15, 12, 10$ |
| phase 2, columns | $1, 2, 4, 3$ | $8, 6, 5, 7$ | $9, 11, 12, 10$ | $16, 15, 13, 14$ |
| last rows | $1, 2, 3, 4$ | $8, 7, 6, 5$ | $9, 10, 11, 12$ | $16, 15, 14, 13$ |

Read in snake order, the result is $1, 2, \ldots, 16$. The step count is $2 \cdot (4 + 4) + 4 = 20 = \sqrt{16}(\lg 16 + 1)$.

## Correctness

Shearsort is a fixed network of compare-exchanges, some of which put the smaller key on the right, so by the [zero-one principle](/zero-one-principle/) it is enough to sort every matrix of zeros and ones. Call a row clean if it is all zeros or all ones, and dirty otherwise. Before each phase, the clean rows of zeros are at the top, the clean rows of ones are at the bottom, and the dirty rows are in between. A phase pairs the dirty rows two by two. Two neighbouring rows are sorted in opposite directions, so their zeros are at opposite ends, and comparing them column by column makes one of the two rows clean. Sorting the columns gives at least as many clean rows as this pairwise comparison does. So each phase turns $D$ dirty rows into at most $\lceil D/2 \rceil$, and after $\lceil \lg r \rceil$ phases at most one dirty row is left, between the zeros and the ones. The last row sort sorts it in its direction. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

**Steps.** Each phase takes $c$ steps for the rows and $r$ steps for the columns, so the step count is $\lceil \lg r \rceil (r + c) + c$. For a square mesh with $\sqrt{n} = 2^k$, this is $\tfrac{1}{2} \lg n \cdot 2\sqrt{n} + \sqrt{n} = \sqrt{n}(\lg n + 1)$. This is the [depth](/network-depth/) of shearsort as a network.

**Comparisons.** Each step makes at most $n/2$ compare-exchanges, so the total is $O(n \sqrt{n} \log n)$ on a square mesh. Work is not the main cost on a mesh, where all processors run in every step.

**Optimality.** The diameter bound of $2\sqrt{n} - 2$ steps, from the [mesh sorting problem](/mesh-sorting-problem/), shows that shearsort is a factor $\Theta(\log n)$ from optimal. Algorithms with $O(\sqrt{n})$ steps exist, but they are more complex.

**Space.** Each processor holds one key and $O(1)$ extra words.

## Properties

- **Oblivious.** The compare-exchange pattern does not depend on the keys, so shearsort is a [sorting network](/sorting-network/) with comparators between mesh neighbours only.
- **In place.** Each processor holds one key at all times.
- **Not stable.** Odd-even transposition is stable on one line, but rows sorted in opposite directions reverse the order of equal keys.
- **Only local links.** Every comparison is between neighbours, which suits a grid of processors on a chip.

## Variants and improvements

- **Shorter column phases.** After phase $k$, at most $\lceil r / 2^k \rceil$ rows are dirty, so later column sorts need only a few odd-even rounds instead of $r$. This cuts the step count by a constant factor without changing the $\Theta(\sqrt{n} \log n)$ order.
- **Blocks of keys.** With $k$ keys per processor, each compare-exchange becomes a merge-split of two sorted blocks, as in the block version of odd-even transposition sort.
- **Higher dimensions.** The same halving argument sorts a $d$-dimensional mesh by alternating sorts along the dimensions.
- **Faster mesh sorts.** The algorithm of Schnorr and Shamir takes $3\sqrt{n} + o(\sqrt{n})$ steps. It cuts the mesh into blocks of side about $n^{3/8}$ and sorts and mixes these blocks.
- **Columnsort.** [Columnsort](/columnsort/) uses a fixed number of column sorts and fixed permutations, and it is the standard way to sort a matrix with many more rows than columns.

## When to use it

Use shearsort on a mesh or grid of processors when the code must be short and easy to prove, and the $\log n$ factor is acceptable. It is also a good teaching example of the zero-one principle in two dimensions. For large meshes, the $O(\sqrt{n})$ algorithms are faster. On machines with a global network, [bitonic sort](/bitonic-sort/) or [sample sort](/sample-sort/) are better choices.

## Pitfalls

- **Same direction in all rows.** If all rows are sorted left to right, two dirty rows have their zeros at the same end, and the column sort need not clean either of them. The alternating directions are essential.
- **Too few phases.** With fewer than $\lceil \lg r \rceil$ phases, more than one dirty row can be left, and the last row sort does not finish the sort.
- **Row-major output.** Shearsort gives snake order. To get row-major order, reverse the odd rows at the end, which takes about $c$ more steps.
- **Rows and columns swapped.** The number of phases depends on the number of rows $r$, because the halving is of dirty rows. Sorting rows and columns in the other roles needs $\lceil \lg c \rceil$ phases instead.

## Implementations

## History

Shearsort was published by Scherson, Sen and Shamir in 1986. Leighton's book of 1992 gives the proof by the zero-one principle with clean and dirty rows, as on this page.

## References
