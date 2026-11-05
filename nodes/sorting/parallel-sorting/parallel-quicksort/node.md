---
tag: X4M2NF
kind: algorithm
slug: parallel-quicksort
name: Parallel quicksort
aliases:
- multithreaded quicksort
- parallel partition sort
area: sorting/parallel-sorting
level: core
summary: Quicksort that partitions in parallel and sorts the two halves concurrently.
solves: [parallel-sorting-problem]
model: work-span-model
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n²), average: Θ(n log n), best: Θ(n)}
  space: {extra: Θ(n)}
  depth: {worst: Θ(n log n), average: O(log² n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: false, comparison: true, recursive: true}
prereqs: [randomized-quicksort, parallel-pack, all-prefix-sums, work-span-model, chernoff-bound]
see_also: [randomized-quicksort, three-way-quicksort, parallel-pack, sample-sort, parallel-merge-sort, hyperquicksort, las-vegas-algorithm, blelloch-scan]
sources:
  - paper: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the quicksort example in NESL, with expected work O(n log n) and expected depth O(log n) levels of recursion
  - book: isbn:9780262023139
    title: Guy E. Blelloch, Vector Models for Data-Parallel Computing, MIT Press, 1990
    locator: the scan primitives and the split and pack operations used for quicksort
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, the section on quicksort (parallel formulations for the PRAM, the hypercube and message passing)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4, Chernoff and Hoeffding bounds
---

Parallel quicksort is [randomized quicksort](/randomized-quicksort/) in which the partition step is parallel and the two parts are sorted at the same time. The partition compares every key with a random pivot at once and moves the keys into place with [parallel pack](/parallel-pack/), which uses [prefix sums](/all-prefix-sums/). In the [work-span model](/work-span-model/) the expected work is $\Theta(n \log n)$ and the span is $O(\log^2 n)$ with high probability. With a three-way partition into keys less than, equal to and greater than the pivot, the sort is also stable.

## In plain words

To sort a pile of cards, pick one card at random and call it the pivot. Every other card is compared with the pivot at the same time, by many helpers. The cards that are smaller go to a left pile, the equal ones to a middle pile and the larger ones to a right pile.

To put the cards in their piles without collisions, each helper must know where to put their card. A running count of the smaller cards gives each small card its slot in the left pile, and the same is done for the other two piles. Running counts can also be computed quickly by many helpers.

Then the left pile and the right pile are sorted at the same time, in the same way. A random pivot is seldom bad, so the piles soon become small.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys from a total order. The output is the same keys in non-decreasing order, with equal keys in input order. This is the [parallel sorting problem](/parallel-sorting-problem/) in the [work-span model](/work-span-model/), where the cost is the work $T_1$ and the span $T_\infty$.

## The algorithm

PACK keeps the items of an array whose flag is 1, in input order. It uses an exclusive [prefix sum](/all-prefix-sums/) of the flags to give each kept item its output index. `spawn` and `sync` are as in the [fork-join model](/fork-join-model/).

```pseudo id=main
PAR-QUICKSORT(A)                           ▷ return the keys of A, sorted
L1  n ← |A|
L2  if n ≤ 1 then return A
L3  x ← A[i] for an index i chosen uniformly at random
L4  parallel for i ← 0 to n − 1 do  lt[i] ← [A[i] < x];  eq[i] ← [A[i] = x];  gt[i] ← [A[i] > x]
L5  L ← PACK(A, lt);  E ← PACK(A, eq);  G ← PACK(A, gt)
L6  spawn L′ ← PAR-QUICKSORT(L)
L7  G′ ← PAR-QUICKSORT(G)
L8  sync
L9  return L′ ∥ E ∥ G′                       ▷ a parallel copy into one array

PACK(A, f)
L10 (s, total) ← exclusive prefix sums of f[0 .. n − 1]
L11 parallel for i ← 0 to n − 1 do if f[i] = 1 then B[s[i]] ← A[i]
L12 return B[0 .. total − 1]
```

## Example

Sort $A = [5, 2, 8, 2, 9, 1, 5, 3]$, and suppose the first pivot is $x = 5$. The flags for "less than 5" are $[0, 1, 0, 1, 0, 1, 0, 1]$, with exclusive prefix sums $[0, 0, 1, 1, 2, 2, 3, 3]$. So the keys $2, 2, 1, 3$ at indices $1, 3, 5, 7$ go to slots $0, 1, 2, 3$ of $L$.

| level | call | pivot | $L$ | $E$ | $G$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $[5, 2, 8, 2, 9, 1, 5, 3]$ | $5$ | $[2, 2, 1, 3]$ | $[5, 5]$ | $[8, 9]$ |
| 2 | $[2, 2, 1, 3]$ | $2$ | $[1]$ | $[2, 2]$ | $[3]$ |
| 2 | $[8, 9]$ | $9$ | $[8]$ | $[9]$ | $[\,]$ |

The two calls of level 2 run at the same time, and the calls on one key or none return at once. The result is $[1, 2, 2, 3, 5, 5, 8, 9]$. The two keys $2$ and the two keys $5$ keep their input order, because PACK keeps the order of the kept items.

## Correctness

Every key of $L$ is less than $x$, every key of $E$ is equal to $x$ and every key of $G$ is greater than $x$, and each key of the call goes to exactly one of the three. By induction on $n$, the recursive calls return $L$ and $G$ sorted and stable, so $L' \parallel E \parallel G'$ is sorted. Two equal keys lie in the same part, and PACK keeps their order, so the sort is stable. The full proof, with the bounds on the span and the work, is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are in the [work-span model](/work-span-model/). A call on $s$ keys does work $O(s)$ and has span $O(\log s)$ for lines L4, L5 and L9, because a prefix sum has work $O(s)$ and span $O(\log s)$, for example with the [Blelloch scan](/blelloch-scan/).

**Depth of the recursion.** Call a pivot good if both $L$ and $G$ have at most $3s/4$ keys. At least half of the possible pivots are good, whatever the keys. Follow one key down the recursion. After $k = \lceil \log_{4/3} n \rceil + 1$ good pivots on its path, the key is in a call with at most one key. By a [Chernoff bound](/chernoff-bound/), the chance that $8k$ levels have fewer than $k$ good pivots is at most $n^{-3.9}$, and a union bound over the $n$ keys shows that the recursion depth is at most $8k = O(\log n)$ with probability at least $1 - n^{-2.9}$.

**Span.** Each level of the recursion adds span $O(\log n)$, so the span is $O(\log^2 n)$ with probability at least $1 - n^{-2.9}$. In the worst case every pivot is the largest key, the depth is $n$, and the span is $\Theta(n \log n)$.

**Work.** The work of one level is $O(1)$ for each key that is still in a call of more than one key. A key needs at most $2k$ levels in expectation to see $k$ good pivots, so the expected work is $O(n \log n)$. The worst case is $\Theta(n^2)$, as for sequential quicksort. If all keys are equal, the first call puts them all in $E$, and the work is $\Theta(n)$.

**Time on $p$ processors.** By [Brent's theorem](/brent-theorem/), a greedy scheduler runs the sort in expected time $O(n \log n / p + \log^2 n)$, which is linear speedup for $p = O(n / \log n)$.

**Space.** The flags, the prefix sums and the three parts take $O(n)$ extra cells per level. Reusing two buffers of $n$ cells across levels gives $\Theta(n)$ extra space.

## Properties

- **Stable.** PACK keeps the input order of the kept items, and equal keys always go to the same part.
- **Las Vegas.** The output is always correct. Only the running time depends on the random choices, so it is a [Las Vegas algorithm](/las-vegas-algorithm/).
- **Not in place.** The packed parts go to new arrays. The in-place parallel partitions used in practice give up stability.
- **Comparison-based.** Keys are only compared.
- **Work-efficient in expectation.** The expected work matches the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/).

## Variants and improvements

- **Sequential partition.** If the partition is the sequential one and only the two recursive calls run in parallel, the span is $\Theta(n)$ in expectation, because the first partition alone takes $n$ steps. The parallelism is then only $O(\log n)$.
- **In-place block partition.** Practical parallel quicksorts partition in place: threads take blocks of keys from both ends, swap misplaced keys block by block, and clean up the few blocks left over. This saves memory but is not stable.
- **Many pivots.** Taking $p - 1$ pivots from a sample and splitting into $p$ parts in one pass gives [sample sort](/sample-sort/), which moves each key only a few times.
- **Hypercube version.** On a [hypercube](/hypercube-hamiltonian-cycle/) of processors, [hyperquicksort](/hyperquicksort/) splits the machine in half with each pivot.
- **Two-way split.** With two parts, $\le x$ and $> x$, many equal keys can make the depth large. The three-way split of lines L4 and L5 removes all copies of the pivot at once, as in [three-way quicksort](/three-way-quicksort/).

## When to use it

Use parallel quicksort on a shared-memory machine when the expected bounds are enough and the code should be short. In NESL style languages it is a few lines. When the worst case must be bounded, use [parallel merge sort](/parallel-merge-sort/). On many processors with keys spread over local memories, [sample sort](/sample-sort/) moves fewer keys.

## Pitfalls

- **A fixed pivot.** Taking the first key as pivot gives depth $n$ on sorted input, and span $\Theta(n \log n)$.
- **A serial partition.** A parallel recursion around a sequential partition has span $\Theta(n)$, so it scales to only a few processors.
- **Equal keys with a two-way split.** If all keys are equal and the split is into $\le x$ and $> x$, every call keeps all the keys, and the recursion does not end unless the pivot is removed.
- **Too fine a grain.** A spawn and a scan for a call of a few keys cost far more than sorting them sequentially. Switch to a sequential sort below a grain size.

## Implementations

## History

Quicksort is due to Hoare. Its data-parallel form, with the partition done by scans and packs, was popularised by Blelloch in his work on scan primitives and on the language NESL, where quicksort is one of the first examples. The parallel formulations for message-passing machines, including the hypercube version, are covered in the book of Grama, Gupta, Karypis and Kumar.

## References
