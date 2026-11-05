---
tag: QRMS1F
kind: algorithm
slug: odd-even-transposition-sort
name: Odd-even transposition sort
aliases:
- brick sort
- odd-even sort
area: sorting/parallel-sorting
level: intro
summary: Alternately compare-exchange disjoint odd and even neighbour pairs; sorts n keys in n parallel rounds on a linear array.
solves: [parallel-sorting-problem]
model: sorting-network
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n²)}
  space: {extra: Θ(1)}
  depth: {worst: n}
properties: {stable: true, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [comparator, zero-one-principle, bubble-sort]
see_also: [bubble-sort, cocktail-shaker-sort, sorting-network, network-depth, shearsort, mesh-sorting-problem, bitonic-sort]
sources:
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Chapter 1, Arrays and trees (odd-even transposition sort on a linear array, and its proof with the 0-1 principle)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, Section 9.3 (bubble sort and its variants, odd-even transposition, and the version with n/p keys per processor)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the zero-one principle and comparator networks)
  - paper: "A. N. Habermann, Parallel neighbor-sort (or the glory of the induction principle), Technical report, Carnegie Mellon University, 1972"
    locator: the proof that n rounds suffice
  - paper: "Gerard Baudet and David Stevenson, Optimal sorting algorithms for parallel computers, IEEE Transactions on Computers C-27(1), 1978"
    locator: the block version with a merge-split in place of each comparator
---

Odd-even transposition sort sorts $n$ keys on a linear array of $n$ processors in $n$ rounds. In odd rounds it compares and exchanges the neighbour pairs $(0, 1), (2, 3), \ldots$, and in even rounds the pairs $(1, 2), (3, 4), \ldots$. The pairs of one round are disjoint, so all their [comparators](/comparator/) work at the same time. It is a [sorting network](/sorting-network/) of [depth](/network-depth/) $n$ and size $n(n-1)/2$, the parallel form of [bubble sort](/bubble-sort/), and the standard way to sort the rows and columns of a mesh.

## In plain words

People stand in a line, each with a number card. In the first round, the first and second person compare cards, and so do the third and fourth, and so on. If the left card is larger, they swap. In the next round the pairs shift by one: the second and third compare, the fourth and fifth, and so on. The rounds alternate like the rows of bricks in a wall.

Each person only ever talks to a neighbour, and nobody waits for anybody else in a round. After as many rounds as there are people, the cards are in order. The method is slow in total work, because many comparisons repeat, but it needs no memory, no addresses and no long wires.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys from a total order, with $A[i]$ on processor $i$ of a linear array. Processor $i$ is linked only to processors $i - 1$ and $i + 1$. The output is the same keys in non-decreasing order, with the $i$-th smallest on processor $i$. This is the [parallel sorting problem](/parallel-sorting-problem/) on a linear array.

## The algorithm

```pseudo id=main
ODD-EVEN-TRANSPOSITION-SORT(A[0 .. n − 1])
L1  for t ← 1 to n do
L2      s ← (t − 1) mod 2                  ▷ round 1 starts at pair (0, 1)
L3      for each i ∈ {s, s + 2, s + 4, …} with i + 1 < n do in parallel
L4          COMPARE(A, i, i + 1)

COMPARE(A, i, j)                           ▷ a comparator [i:j], with i < j
L5  if A[i] > A[j] then exchange A[i] and A[j]
```

Line L3 runs the comparators of one round in parallel. They have disjoint wires, so the result does not depend on their order. Round $t$ uses the pairs $(i, i+1)$ with $i \equiv t - 1 \pmod 2$. The comparators do not depend on the keys, so the algorithm is an oblivious comparator network with $n$ layers.

## Example

Sort $A = [6, 3, 8, 1, 7, 2, 5, 4]$, so $n = 8$.

| round | pairs | array after the round |
| --- | --- | --- |
| 0 | | 6 3 8 1 7 2 5 4 |
| 1 | (0,1) (2,3) (4,5) (6,7) | 3 6 1 8 2 7 4 5 |
| 2 | (1,2) (3,4) (5,6) | 3 1 6 2 8 4 7 5 |
| 3 | (0,1) (2,3) (4,5) (6,7) | 1 3 2 6 4 8 5 7 |
| 4 | (1,2) (3,4) (5,6) | 1 2 3 4 6 5 8 7 |
| 5 | (0,1) (2,3) (4,5) (6,7) | 1 2 3 4 5 6 7 8 |
| 6 to 8 | | 1 2 3 4 5 6 7 8 |

This input is sorted after 5 rounds, but the algorithm runs all 8, because it does not test whether the array is sorted. The input $[2, 3, 4, 5, 6, 7, 0, 1]$ is still unsorted after 7 rounds and sorted after round 8.

## Correctness

The algorithm is a comparator network, so by the [zero-one principle](/zero-one-principle/) it is enough to show that it sorts each input of zeros and ones. In a 0-1 input with $k$ ones, number the ones $1, \ldots, k$ from the right. Ones only move right and never pass each other. The main lemma is that from round $j$ on, one number $j$ is never blocked by one number $j - 1$, so from round $j + 1$ on it moves one step to the right in each round until it reaches its final position $n - j$. It has at most $n - j$ steps to go, so it is in place after round $j + (n - j) = n$. The full proof is below.

## Complexity

- **Depth.** $n$ rounds, so $n$ parallel steps on a linear array of $n$ processors, or with $\lfloor n/2 \rfloor$ comparators working at once.
- **Size.** Odd rounds have $\lfloor n/2 \rfloor$ comparators and even rounds have $\lfloor (n-1)/2 \rfloor$. There are $\lceil n/2 \rceil$ odd rounds and $\lfloor n/2 \rfloor$ even rounds, so the total is exactly $n(n-1)/2$ comparators for each $n \ge 1$. For $n = 8$ this is 28.
- **Sequential time.** $\Theta(n^2)$ in each case, since the network makes the same comparisons on each input.
- **Work.** $n$ processors for $n$ steps give work $\Theta(n^2)$, against $\Theta(n \log n)$ for the best sequential sort. So the algorithm is not [work-efficient](/work-efficiency/).
- **Lower bound on a linear array.** Any algorithm on a linear array of $n$ processors with one key per processor needs at least $n - 1$ steps, because the smallest key may start at processor $n - 1$ and must reach processor 0, one link per step. For odd $n \ge 3$, odd-even transposition sort needs all $n$ rounds on the input $[1, 2, \ldots, n-1, 0]$: position $n - 1$ is in no pair of round 1, so the key 0 does not move in round 1, and it then needs $n - 1$ more moves of one step each.

## Properties

- **Oblivious.** The comparators are fixed, so the same hardware sorts every input, and the running time does not depend on the data.
- **Local.** Each comparison is between neighbours. This is why it is the row and column sort of [shearsort](/shearsort/) and of other mesh sorts.
- **Stable.** Line L5 exchanges two neighbours only when the left key is strictly larger. Keys move only by exchanges of neighbours, so two equal keys never pass each other and keep their input order.
- **In place.** Each processor holds one key, and the sequential form needs $O(1)$ extra space.

## Variants and improvements

- **Blocks of keys.** With $p < n$ processors, each processor first sorts its $n/p$ keys. Each comparator is then replaced by a merge-split: the two processors merge their blocks, and the left one keeps the smaller half. After $p$ rounds the keys are sorted. The local sort takes $O((n/p)\log(n/p))$ time and the $p$ rounds take $O(n)$ time in total. Baudet and Stevenson gave this method.
- **Odd-even transposition on a ring or a mesh.** The same rounds sort each row of a mesh in the row length, which is the inner step of shearsort.
- **Early exit.** A sequential version can stop after a round with no exchange. This makes it adaptive, but it is then no longer a fixed network.
- **Faster networks.** [Bitonic sort](/bitonic-sort/) and [odd-even merge sort](/odd-even-merge-sort/) have depth $\Theta(\log^2 n)$, but they need long wires between distant positions.

## When to use it

Use it when only neighbour links exist: a linear array, a systolic array, the rows and columns of a mesh, or a small fixed sort in hardware. Use the block version with a few processors when the merge-split step is cheap. Do not use it for large $n$ on a shared-memory machine, where its $\Theta(n^2)$ work is far more than the $\Theta(n \log n)$ of [parallel merge sort](/parallel-merge-sort/) or [sample sort](/sample-sort/).

## Pitfalls

- **Too few rounds.** $n - 1$ rounds are not enough in general. For $n = 8$, the input $[2, 3, 4, 5, 6, 7, 0, 1]$ needs all 8.
- **The wrong start.** If the first round uses the pairs $(1, 2), (3, 4), \ldots$, the algorithm still sorts in $n$ rounds, but a trace or a test written for the other order gives different intermediate arrays.
- **Sequential pairs.** Running the pairs of one round from left to right in place is still correct, since they are disjoint. Running the pairs $(0,1), (1,2), (2,3), \ldots$ in one sweep is bubble sort, not this algorithm.

## Implementations

## History

Habermann proved in a technical report of 1972 that $n$ rounds are enough. The block version with merge-split steps is due to Baudet and Stevenson in 1978. Leighton's book gives a proof by the zero-one principle, as on this page.

## References
