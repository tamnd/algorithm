---
tag: J95TFF
kind: algorithm
slug: hyperquicksort
name: Hyperquicksort
aliases:
- hypercube quicksort
area: sorting/parallel-sorting
level: advanced
summary: Quicksort on a hypercube that splits the data along one dimension per round.
solves: [parallel-sorting-problem]
model: bsp-model
complexity:
  vars: {n: the number of keys, p: the number of processors, L: the largest number of keys on one processor during the run}
  time: {worst: O(n log n + p L log p)}
  space: {extra: Θ(L)}
  depth: {worst: O((n/p) log n + L log p + log² p)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [quicksort, parallel-quicksort, merging-sorted-lists, hypercube-hamiltonian-cycle]
see_also: [parallel-quicksort, sample-sort, parallel-sorting-by-regular-sampling, bitonic-sort, distributed-sorting, bsp-model, quicksort, hypercube-hamiltonian-cycle]
sources:
  - paper: "Bruce Wagar, Hyperquicksort: a fast sorting algorithm for hypercubes, in Hypercube Multiprocessors 1987, M. T. Heath (editor), SIAM, 1987"
    locator: the algorithm, with a local sort first and the median of one list as the pivot of each subcube
  - book: isbn:9780072822564
    title: Michael J. Quinn, Parallel Programming in C with MPI and OpenMP, McGraw-Hill, 2004
    locator: Chapter 14, Sorting (parallel quicksort on a hypercube, hyperquicksort, and its load imbalance)
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, the section on quicksort (the formulation for a hypercube)
---

Hyperquicksort sorts $n$ keys on a hypercube of $p = 2^d$ processors. Each processor first sorts its own keys. Then, for each dimension from the highest to the lowest, every subcube picks one pivot, and each pair of processors joined by an edge of that dimension swaps keys, so that the lower processor keeps the keys at most the pivot and the upper one keeps the rest. After $d$ rounds, the keys are sorted in processor order. Each round needs only a merge of two sorted lists, but the loads can become uneven, because each pivot is the median of the keys of a single processor.

## In plain words

Picture eight helpers, each with a pile of cards, wired as the corners of a cube. Every helper first sorts their own pile.

In the first round, one helper looks at the middle card of their pile and announces it to everybody. The cube splits into two halves, and each helper has a partner in the other half. Partners swap cards so that the helper in the lower half keeps all cards up to the announced value and the partner keeps the larger ones. Each half now holds only small or only large cards.

Then the same is done inside each half, with a new value, and then inside each quarter. After one round per direction of the cube, all cards are in order across the helpers.

## The problem

The input is $n$ keys from a total order, spread over the $p = 2^d$ processors of a [hypercube](/hypercube-hamiltonian-cycle/), $n/p$ keys each. Processors are numbered $0$ to $p - 1$, and two processors are linked when their numbers differ in exactly one bit. The output is the keys sorted in processor order: each processor holds a sorted list, and every key on processor $q$ is at most every key on processor $q + 1$. This is the [parallel sorting problem](/parallel-sorting-problem/) on a hypercube, with one-port message passing, in which each processor sends and receives over one link at a time. It can also be analysed in the [BSP model](/bsp-model/), with one superstep per round.

## The algorithm

A subcube of dimension $i + 1$ is a set of $2^{i+1}$ processors whose numbers agree on all bits above bit $i$. Its root is its lowest-numbered processor.

```pseudo id=main
HYPERQUICKSORT(processor q holds the list X[q], for q = 0, …, 2^d − 1)
L1  parallel for q: sort X[q]
L2  for i ← d − 1 downto 0 do
L3      in each subcube of dimension i + 1: the root takes the median of its list as the pivot x and broadcasts x in the subcube
L4      parallel for each q with bit i of q equal to 0, and its partner q′ = q + 2^i, with the pivot x of their subcube:
L5          split X[q] and X[q′] by binary search into the keys ≤ x and the keys > x
L6          q′ sends its keys ≤ x to q, which merges them with its own keys ≤ x into X[q]
L7          q sends its keys > x to q′, which merges them with its own keys > x into X[q′]
```

If the root has no keys, another processor of the subcube with keys provides the pivot. If no processor of the subcube has keys, the round does nothing there.

## Example

Sort 16 keys on $p = 4$ processors, a square, so $d = 2$. The pivot is the key at index $\lfloor (k-1)/2 \rfloor$ of a sorted list of $k$ keys.

| step | $X[0]$ | $X[1]$ | $X[2]$ | $X[3]$ |
| --- | --- | --- | --- | --- |
| input | $42, 7, 93, 25$ | $60, 12, 88, 3$ | $54, 31, 76, 19$ | $65, 8, 47, 99$ |
| L1, local sort | $7, 25, 42, 93$ | $3, 12, 60, 88$ | $19, 31, 54, 76$ | $8, 47, 65, 99$ |
| $i = 1$, pivot $25$ | $7, 19, 25$ | $3, 8, 12$ | $31, 42, 54, 76, 93$ | $47, 60, 65, 88, 99$ |
| $i = 0$, pivots $19$ and $54$ | $3, 7, 8, 12, 19$ | $25$ | $31, 42, 47, 54$ | $60, 65, 76, 88, 93, 99$ |

In round $i = 1$ the pairs are $(0, 2)$ and $(1, 3)$, and the pivot $25$ is the median of $X[0]$. In round $i = 0$ the pairs are $(0, 1)$ with pivot $19$ from $X[0]$, and $(2, 3)$ with pivot $54$ from $X[2]$. The result is sorted across the processors, but the loads are $5, 1, 4, 6$ instead of $4$ each.

## Correctness

Each list stays sorted, because lines L6 and L7 merge two sorted lists. Take two processors $q < q'$, and let $i$ be the highest bit in which they differ, so $q$ has bit $i$ equal to $0$ and $q'$ has it equal to $1$. In the round for dimension $i$, both are in the same subcube, so after lines L4 to L7, every key on the lower half of that subcube is at most its pivot $x$, and every key on the upper half is greater than $x$. Later rounds only move keys between processors that differ in lower bits, so they stay within each half. So at the end every key on $q$ is at most every key on $q'$. Each round only moves keys, so the output holds exactly the input keys. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for a hypercube of $p = 2^d$ processors with one-port message passing, and $L$ is the largest number of keys on one processor at any time.

**One round.** The broadcast on line L3 takes $O(i + 1) = O(d)$ steps along a spanning tree of the subcube. Line L5 takes time $O(\log L)$. Lines L6 and L7 send at most $L$ keys over one link and merge at most $L$ keys, in time $O(L)$.

**Whole sort.** Line L1 takes time $O((n/p) \log(n/p))$, and the $d = \lg p$ rounds take time $O(L \log p + \log^2 p)$. If the loads stay balanced, $L = O(n/p)$, and the time is $O((n/p) \log n + \log^2 p)$. The work is then $O(n \log n)$.

**Load imbalance.** Each pivot is the median of one processor's list, not of the whole subcube, so $L$ can be much larger than $n/p$. On $p = 2$ processors with keys $0, \ldots, 7$ on processor $0$ and $8, \ldots, 15$ on processor $1$, the pivot is $3$ and processor $1$ ends with $12$ of the $16$ keys. With more dimensions the imbalance of each round adds to that of earlier rounds. When the keys are in random order, each root's list is a random sample of its subcube's keys, the pivots are close to the medians of the subcubes, and $L$ stays close to $n/p$.

**Space.** Each processor needs room for its largest list, $\Theta(L)$.

## Properties

- **Deterministic.** The pivots are taken from fixed positions, so the run depends only on the input.
- **Neighbour communication only.** Every exchange is along one hypercube edge, and each processor talks to one partner per round.
- **Merges instead of partitions.** Because each list is sorted first, a round is a split by binary search and one merge, not a partition of unsorted keys.
- **Not stable.** Keys move between processors in a way that does not keep the order of equal keys.
- **Not balanced.** The final loads depend on the input, and the output is not split into equal parts.

## Variants and improvements

- **Parallel quicksort on a hypercube.** Without the first local sort, each round partitions unsorted lists around a random pivot. Hyperquicksort replaces this by a sort at the start and merges in each round, and takes better pivots from sorted lists.
- **Better pivots.** Taking the median of the medians of all processors in the subcube, or of a sample from each, makes the loads more even at the cost of one more gather per round.
- **Regular sampling.** [Parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/) chooses all $p - 1$ splitters at once from samples of all processors, which bounds the load by $2n/p$ for distinct keys and needs only one exchange.
- **Bitonic sort.** [Bitonic sort](/bitonic-sort/) also uses one dimension at a time on a hypercube. It is fully balanced but needs $\Theta(\log^2 p)$ rounds of exchanges.

## When to use it

Use hyperquicksort on machines with a hypercube or similar network when the keys are in random order and the load per processor need not be exactly $n/p$. For adversarial inputs or when the output must be balanced, use [parallel sorting by regular sampling](/parallel-sorting-by-regular-sampling/) or [sample sort](/sample-sort/). On modern clusters, whose networks are not hypercubes, sample sort is the usual choice.

## Pitfalls

- **Load imbalance.** A bad pivot in an early round makes some processors hold far more than $n/p$ keys, and the time of every later round grows with $L$.
- **Empty root list.** After a few rounds the root of a subcube can have no keys at all. The pivot must then come from another processor of the subcube.
- **Wrong partner.** The partner of $q$ across dimension $i$ is $q$ with bit $i$ flipped. Pairing by any other rule breaks the halving into subcubes, and the output is not sorted.
- **Many equal keys.** If many keys equal the pivot, they all go to the lower processor, which can then hold most of the keys of the subcube.

## Implementations

## History

Wagar presented hyperquicksort in 1987, at a conference on hypercube multiprocessors, as an improvement of the parallel quicksort for hypercubes. Quinn's textbooks present it with parallel sorting by regular sampling as the main message-passing sorts, and point out its load imbalance.

## References
