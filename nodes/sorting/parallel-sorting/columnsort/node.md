---
tag: HTGXH0
kind: algorithm
slug: columnsort
name: Columnsort
aliases:
- Leighton's columnsort
area: sorting/parallel-sorting
level: advanced
summary: Sorts an r by s matrix with a fixed sequence of column sorts and fixed permutations, when r is large relative to s.
solves: [parallel-sorting-problem]
model: bsp-model
complexity:
  vars: {n: the number of keys, r: the number of rows, s: the number of columns}
  time: {worst: Θ(n log r)}
  space: {extra: Θ(n)}
  depth: {worst: O(r log r)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [zero-one-principle, sorting-network, parallel-sorting-problem]
see_also: [shearsort, mesh-sorting-problem, zero-one-principle, aks-sorting-network, sample-sort, external-merge-sort, sorting-network, distributed-sorting]
sources:
  - paper: "F. Thomson Leighton, Tight bounds on the complexity of parallel sorting, IEEE Transactions on Computers C-34(4), 1985"
    locator: columnsort, its eight steps and the condition r >= 2(s-1)^2 with s dividing r
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Chapter 1, Arrays and trees (columnsort and its proof by the 0-1 principle)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Problem 8-7, The 0-1 sorting lemma and columnsort
---

Columnsort sorts the $n = rs$ keys of a matrix with $r$ rows and $s$ columns using only four rounds of column sorts and four fixed moves of the keys between rounds. It works whenever $s$ divides $r$ and $r \ge 2(s-1)^2$. Leighton published it in 1985. Each column sort can be done by any sort on one processor, so columnsort turns a sort for $r$ keys into a sort for $rs$ keys on $s$ processors with a fixed communication pattern. The proof uses the [zero-one principle](/zero-one-principle/), which holds because every step either sorts columns or moves keys in a fixed way.

## In plain words

Lay the cards out in a few long columns. Sort each column. Then pick the cards up column by column and lay them down row by row, which spreads each column across all the columns. Sort the columns again, and undo the spreading move. Sort the columns a third time.

Now the cards are almost in order, read column by column. Only a short stretch near the border of two columns can still be wrong. Shift every column down by half its length, so that each border falls in the middle of a column, sort the columns once more, and shift back.

The method needs long, thin columns, so that the short stretch fits in half a column.

## The problem

The input is an $r \times s$ matrix of keys from a total order, column $k$ on processor $k$, with $s \mid r$ and $r \ge 2(s-1)^2$. The output is the same keys in *column-major* order: the keys of ranks $kr$ to $kr + r - 1$ are in column $k$, sorted from top to bottom. This is the [parallel sorting problem](/parallel-sorting-problem/) on $s$ processors, for example in the [BSP model](/bsp-model/), or as a [sorting network](/sorting-network/) built from smaller sorters.

## The algorithm

```pseudo id=main
COLUMNSORT(M[0 .. r − 1][0 .. s − 1])
L1  sort each column
L2  read M in column-major order and write the keys back in row-major order      ▷ "transpose"
L3  sort each column
L4  read M in row-major order and write the keys back in column-major order      ▷ the inverse of L2
L5  sort each column
L6  shift each column down by ⌊r/2⌋ into a matrix of s + 1 columns, with −∞ above and +∞ below
L7  sort each column
L8  shift back by ⌊r/2⌋ and drop the −∞ and +∞ keys
```

On line L6, the shifted matrix in column-major order is $\lfloor r/2 \rfloor$ copies of $-\infty$, then the keys of $M$ in column-major order, then $\lceil r/2 \rceil$ copies of $+\infty$. Its first column holds the top $\lceil r/2 \rceil$ keys of column $0$, and each later column holds the bottom $\lfloor r/2 \rfloor$ keys of one column of $M$ and the top $\lceil r/2 \rceil$ keys of the next. The $\pm\infty$ keys never move on line L7.

## Example

Sort a $9 \times 3$ matrix, which meets $3 \mid 9$ and $9 \ge 2 \cdot 2^2 = 8$. Each cell shows one row, with the three columns from left to right.

| row | input | L1 | L2 | L3 | L4 | L5 | L6 to L8 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 26 15 | 3 2 1 | 3 5 10 | 1 4 6 | 1 7 18 | 1 7 18 | 1 10 19 |
| 1 | 11 7 1 | 5 4 9 | 11 13 14 | 2 5 10 | 4 9 22 | 2 9 19 | 2 11 20 |
| 2 | 5 4 17 | 10 6 12 | 19 25 27 | 3 8 12 | 6 14 24 | 3 11 21 | 3 12 21 |
| 3 | 13 18 21 | 11 7 15 | 2 4 6 | 7 9 14 | 2 11 19 | 4 13 22 | 4 13 22 |
| 4 | 10 16 23 | 13 8 17 | 7 8 16 | 11 13 16 | 5 13 23 | 5 14 23 | 5 14 23 |
| 5 | 14 22 12 | 14 16 20 | 18 22 26 | 15 17 20 | 10 16 26 | 6 15 24 | 6 15 24 |
| 6 | 27 6 24 | 19 18 21 | 1 9 12 | 18 22 24 | 3 15 21 | 8 16 25 | 7 16 25 |
| 7 | 25 2 9 | 25 22 23 | 15 17 20 | 19 23 26 | 8 17 25 | 10 17 26 | 8 17 26 |
| 8 | 19 8 20 | 27 26 24 | 21 23 24 | 21 25 27 | 12 20 27 | 12 20 27 | 9 18 27 |

After line L5, the column-major order is $1, 2, 3, 4, 5, 6, 8, 10, 12, 7, 9, 11, \ldots$: the keys $8, 10, 12$ at the bottom of column $0$ are larger than the keys $7, 9, 11$ at the top of column $1$. The shifted column on line L6 that holds the bottom $4$ keys of column $0$ and the top $5$ keys of column $1$ contains this whole stretch, and sorting it on line L7 fixes it. The result is sorted in column-major order.

## Correctness

Every step either sorts columns or moves keys by a fixed permutation, and both commute with non-decreasing maps on keys, so the [zero-one principle](/zero-one-principle/) applies. For a matrix of zeros and ones:

1. After line L1, column $j$ has some number $z_j$ of zeros at the top.
2. Line L2 deals each column out over all $s$ columns in turn. So each new column gets either $\lfloor z_j / s \rfloor$ or $\lceil z_j / s \rceil$ zeros from old column $j$, and the zero counts of any two new columns differ by at most $s$.
3. After line L3, at most $s$ rows are mixed. Read in row-major order, the matrix is zeros, a mixed stretch of at most $s^2$ keys, and ones.
4. Line L4 turns this row-major order into column-major order, and line L5 sorts the columns. The mixed stretch is now a run of ones at the bottom of one column and a run of zeros at the top of the next, each of at most $s^2$ keys.
5. If $s^2 \le \lfloor r/2 \rfloor$, both runs lie inside one shifted column on line L6, so line L7 sorts them.

This proves the weaker condition $r \ge 2s^2$. Leighton's finer count of the mixed stretch gives the condition $r \ge 2(s-1)^2$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

**On $s$ processors.** Let column $k$ live on processor $k$. Each of the four column sorts is a local sort of $r$ keys, in time $O(r \log r)$ with a comparison sort. Lines L2 and L4 are total exchanges in which each processor sends $r/s$ keys to every other processor, so each is an [h-relation](/h-relation/) with $h < r$. Lines L6 and L8 send $\lfloor r/2 \rfloor$ keys to one neighbour. In the [BSP model](/bsp-model/), columnsort takes a constant number of [supersteps](/superstep/), local work $O(r \log r)$ per processor and communication $O(r)$ per processor.

**Work.** The four column sorts compare $O(s \cdot r \log r) = O(n \log r)$ times in total. For $r \ge 2(s-1)^2$, $\log r = \Theta(\log n)$, so this is $O(n \log n)$.

**As a network.** If each column is sorted by a sorting network of depth $d(r)$, columnsort is a sorting network for $n$ keys of depth $4 d(r)$, since lines L2, L4, L6 and L8 are fixed wirings. Leighton used this to derive sorting networks and fast parallel sorts from sorters for fewer keys.

**Size limit.** The condition $r \ge 2(s-1)^2$ means $s = O(n^{1/3})$. To use more processors, sort the columns themselves by columnsort, recursively.

## Properties

- **Oblivious.** The moves on lines L2, L4, L6 and L8 do not depend on the keys, and column sorts can be any sort. With column sorts done by networks, the whole algorithm is a sorting network.
- **Deterministic.** There is no sampling and no randomness.
- **Constant number of rounds.** Four rounds of local sorting and four fixed exchanges, whatever the input.
- **Not stable.** The column sorts and the transposes mix equal keys from different columns.

## Variants and improvements

- **Weaker size condition.** Later variants relax the condition on $r$ with extra steps, for example a step that sorts small subblocks of the matrix.
- **Out-of-core columnsort.** When the data is on disk, a column fits in memory, and the four rounds of columnsort become four passes over the file. This is used in out-of-core sorting on clusters, next to [external merge sort](/external-merge-sort/).
- **Recursive columnsort.** Sorting each column by columnsort again lifts the limit $s = O(n^{1/3})$, with a constant factor more rounds per level.
- **On a mesh.** With rows and columns of the matrix laid out on a mesh, columnsort sorts a mesh with a constant number of column sorts and fixed routings. See the [mesh sorting problem](/mesh-sorting-problem/).

## When to use it

Use columnsort when the data is split over $s$ processors or disks, each can sort its own share, and a fixed, simple communication pattern matters more than the fewest moves. It needs about $n^{1/3}$ processors or fewer. With more processors, or when keys should move only once, [sample sort](/sample-sort/) is usually faster. On a square mesh, [shearsort](/shearsort/) is simpler but slower.

## Pitfalls

- **Matrix too wide.** If $r < 2(s-1)^2$, the mixed stretch after line L5 can be longer than half a column, and the output can be unsorted. For example, with $r = 16$ and $s = 4$, the 0-1 input with $1, 1, 1, 5$ zeros in its columns is not sorted by columnsort.
- **$s$ does not divide $r$.** The transposes on lines L2 and L4 then do not give each column exactly $r/s$ keys from each old column, and the counting argument fails. Pad the input to a valid size.
- **Wrong direction of the transpose.** Line L4 must be the inverse of line L2. Doing the same move twice does not give the needed order.
- **Losing the $\pm\infty$ keys.** In an implementation that really builds the shifted matrix, the padding must sort to the ends of their columns. With keys that can equal the padding value, the unshift on line L8 removes the wrong keys.

## Implementations

## History

Leighton introduced columnsort in 1985, in a paper on tight bounds for parallel sorting, where it serves to build fast sorts from sorters for fewer keys. It later became a textbook exercise for the 0-1 principle. Chaudhry and Cormen and others later used it for out-of-core sorting on clusters.

## References
