---
tag: HPT34J
kind: algorithm
slug: valiant-parallel-merge
name: Valiant's parallel merge
aliases:
- Valiant's merge
area: sorting/parallel-sorting
level: research
summary: Merges two sorted lists in O(log log n) parallel rounds using comparisons.
solves: [parallel-merging-problem]
model: comparison-model
complexity:
  vars: {m: the length of the first input, n: the length of the second input, N: the larger of m and n}
  time: {worst: O((m + n) log log N)}
  space: {extra: O(m + n)}
  depth: {worst: O(log log N)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [parallel-merging-problem, merging-sorted-lists, comparison-model, parallel-sorting-depth-lower-bound]
see_also: [parallel-merging-problem, shiloach-vishkin-merge, merge-path, cole-merge-sort, merging-lower-bound, parallel-sorting-depth-lower-bound, parallel-merge-sort, crew-pram]
sources:
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: the parallel comparison model, and merging two sorted lists in O(log log n) rounds by sampling about the square root of each list
  - paper: "Allan Borodin and John E. Hopcroft, Routing, merging, and sorting on parallel models of computation, Journal of Computer and System Sciences 30(1), 1985"
    locator: the lower bound of Omega(log log n) rounds for merging two lists of n items with n processors in the parallel comparison model
  - paper: "Clyde P. Kruskal, Searching, merging, and sorting in parallel computation, IEEE Transactions on Computers C-32(10), 1983"
    locator: merging on the CREW PRAM in O(log log n) time with n / log log n processors, built on Valiant's method
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting (fast merging), and Chapter 10, Lower bounds
---

Valiant's merge merges two sorted lists $A$ and $B$ in $O(\log \log N)$ rounds with $m + n$ processors, where $N = \max(m, n)$, in the parallel comparison model. In that model each processor makes one comparison per round, and everything else is free. The method takes every $\lceil \sqrt{m} \rceil$-th item of $A$ and every $\lceil \sqrt{n} \rceil$-th item of $B$ as samples, places all samples exactly in two rounds, and then merges the pieces between the samples in parallel by the same method. Each piece has fewer than $\sqrt{N}$ items of each list, so the size drops from $N$ to $\sqrt{N}$ every two rounds. Borodin and Hopcroft proved that $\Omega(\log \log n)$ rounds are needed, so merging takes $\Theta(\log \log n)$ rounds in this model, while sorting takes $\Theta(\log n)$.

## In plain words

Two sorted rows of people must become one sorted row, and there is one judge per person. In one round, each judge compares two people once.

Pick a few people from each row as markers: one out of every hundred, if a row has ten thousand people. In the first round, judges compare every marker of one row with every marker of the other. Now each marker knows between which two markers of the other row it stands. In the second round, each marker is compared with the hundred or so people in that gap, so it knows its exact place.

The markers cut both rows into short stretches of at most a hundred people each. Each stretch is the same problem again, much smaller. Repeat: the next stretches have at most ten people, then three.

## The problem

The input is two sorted lists $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of keys from a total order. The output is their stable merge $C$, in which each item of $A$ comes before each equal item of $B$. This is the [parallel merging problem](/parallel-merging-problem/).

The model is the parallel comparison model of Valiant, the [comparison model](/comparison-model/) with $P$ processors: in each round, each processor compares one pair of items, and the pairs of a round may depend on all answers of earlier rounds. Moving data, computing ranks from answers and assigning processors are free. The cost is the number of rounds. Here $P = m + n$.

All comparisons ask "$b < a$?" for an item $a$ of $A$ and an item $b$ of $B$. The answer "no" means that $a$ comes before $b$ in $C$, so one comparison decides the order of $a$ and $b$, ties included.

## The algorithm

All calls on line L8 run at the same time, so the rounds of one level of the recursion are shared.

```pseudo id=main
VALIANT-MERGE(A[0 .. m − 1], B[0 .. n − 1])          ▷ writes into C, from position 0
L1  if m = 0 or n = 0 then copy the other list to C; return
L2  if m·n ≤ m + n then compare every pair in one round; write each item at its index plus its rank in the other list; return
L3  s ← ⌈√m⌉;  t ← ⌈√n⌉;  the A-samples are A[s − 1], A[2s − 1], …, the B-samples are B[t − 1], B[2t − 1], …
L4  round 1: compare every A-sample with every B-sample; each sample learns between which two samples of the other list it lies
L5  round 2: compare each sample with every item of the other list between those two samples; each A-sample learns the number of items of B less than it, and each B-sample the number of items of A at most it
L6  write each sample to C at its index plus its rank
L7  the samples with their ranks, with (0, 0) and (m, n), cut A and B into pieces; remove from each piece the sample at its start
L8  in parallel for each piece: VALIANT-MERGE its part of A and its part of B, into C after the start of the piece, with as many processors as it has items
```

An A-sample at index $i$ with rank $j$ gives the split $(i, j)$: the first $i + j$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$, and $A[i]$ is at position $i + j$. The same holds for B-samples. Between two splits next to each other lies one piece.

## Example

Merge $A = [1, 4, 6, 9]$ and $B = [2, 3, 7, 8, 10]$ with $9$ processors. Here $m n = 20 > 9$, so the call samples, with $s = \lceil \sqrt{4} \rceil = 2$ and $t = \lceil \sqrt{5} \rceil = 3$. The A-samples are $A[1] = 4$ and $A[3] = 9$, and the B-sample is $B[2] = 7$.

| round | comparisons | result |
| --- | --- | --- |
| 1 | $7 < 4$? no. $7 < 9$? yes. | $4$ is before $7$, $9$ is after $7$ |
| 2 | $4$ with $2, 3$; $9$ with $8, 10$; $7$ with $6$ | rank of $4$ in $B$ is 2, rank of $9$ in $B$ is 4, rank of $7$ in $A$ is 3 |

Round 1 uses 2 comparisons and round 2 uses 5, both at most 9. The samples go to $C[1 + 2] = C[3] = 4$, $C[3 + 4] = C[7] = 9$ and $C[2 + 3] = C[5] = 7$. The splits in order are $(0, 0), (1, 2), (3, 2), (3, 4), (4, 5)$, and the pieces, without their starting samples, are:

| piece | part of $A$ | part of $B$ | output positions | how |
| --- | --- | --- | --- | --- |
| 1 | $[1]$ | $[2, 3]$ | $0, 1, 2$ | line L2, 2 comparisons |
| 2 | $[6]$ | none | $4$ | line L1 |
| 3 | none | $[8]$ | $6$ | line L1 |
| 4 | none | $[10]$ | $8$ | line L1 |

The third round compares $1$ with $2$ and $3$, and the result is $C = [1, 2, 3, 4, 6, 7, 8, 9, 10]$ after 3 rounds.

For two lists of $65536$ random keys each, the method takes 9 rounds, which is $2 \lceil \lg \lg 65536 \rceil + 1 = 2 \cdot 4 + 1$.

## Correctness

Line L2 is correct because an item of $A$ at index $i$ with $r$ items of $B$ before it is at position $i + r$ of $C$, and likewise for $B$. On line L4, an A-sample $a$ learns how many B-samples are less than it, so its rank in $B$ is in a gap of fewer than $t$ items between two B-samples, and line L5 counts the items of the gap below $a$. So each sample gets its exact position. The positions of all samples are splits of $C$, they form a chain, and the items between two splits next to each other are the stable merge of a part of $A$ and a part of $B$. So line L8 fills each remaining position once and correctly, by induction on the size. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for the parallel comparison model with $m + n$ processors. Let $N = \max(m, n)$.

**Processors per round.** There are at most $\sqrt{m}$ A-samples and $\sqrt{n}$ B-samples. Round 1 makes at most $\sqrt{m n}$ comparisons. In round 2, each A-sample makes at most $t - 1 < \sqrt{n}$ comparisons and each B-sample at most $s - 1 < \sqrt{m}$, at most $2 \sqrt{m n}$ in all. Since $2 \sqrt{m n} \le m + n$, both rounds fit. Line L2 makes $m n \le m + n$ comparisons. The pieces on line L8 have disjoint items, so they share the $m + n$ processors without conflict.

**Rounds.** Each piece has at most $s - 1 = \lceil \sqrt{m} \rceil - 1 < \sqrt{m}$ items of $A$ and fewer than $\sqrt{n}$ items of $B$, so the size $N$ of a call drops to less than $\sqrt{N}$. After $r$ levels it is less than $N^{1/2^r}$, which is at most 2 for $r = \lceil \lg \lg N \rceil$. A call with $\max(m, n) \le 2$ satisfies $m n \le m + n$ and ends on line L1 or L2. So the number of rounds is at most $2 \lceil \lg \lg N \rceil + 1$ for $N \ge 2$.

**Comparisons.** Each level makes at most $2(m + n)$ comparisons, so the total is $O((m + n) \log \log N)$. This is more than the $m + n - 1$ comparisons of a sequential merge by a factor $\log \log N$, which is the price of so few rounds.

**Lower bound.** Borodin and Hopcroft proved that merging two lists of $n$ items with $n$ processors in this model takes $\Omega(\log \log n)$ rounds, so the method is optimal up to a constant factor. See also the [depth lower bound](/parallel-sorting-depth-lower-bound/) for sorting, which is $\Omega(\log n)$ in the same model.

## Properties

- **Stable.** Every comparison is "$b < a$?", and a "no" puts $a$ first, so on equal keys items of $A$ come first.
- **Recursive.** The calls of one level run together and share the rounds.
- **Adaptive in the pairs it compares.** The pairs of round 2 and of later levels depend on earlier answers, so it is not a [merging network](/merging-network/), which needs depth $\Omega(\log n)$.
- **Free bookkeeping.** The model does not charge for computing ranks, moving items or assigning processors. On a PRAM these steps cost time too.

## Variants and improvements

- **On the CREW PRAM.** Kruskal turned the method into a [CREW PRAM](/crew-pram/) algorithm with time $O(\log \log n)$ and $n / \log \log n$ processors, so its work is $O(n)$, by merging small blocks sequentially and doing the bookkeeping with the processors at hand.
- **Unequal lengths.** Valiant's paper also treats lists of different lengths and other numbers of processors, and finding the maximum in $O(\log \log n)$ rounds with $n$ processors by a similar square-root split.
- **Sorting.** A merge sort with this merge takes $O(\log n \log \log n)$ rounds with $n$ processors in the parallel comparison model. The best bound is $O(\log n)$, by the AKS network or [Cole's merge sort](/cole-merge-sort/).
- **Practical merges.** On real machines, [merge path](/merge-path/) and [Shiloach-Vishkin merging](/shiloach-vishkin-merge/) with $O(\log n)$ time and $O(n)$ work are simpler and faster.

## When to use it

Use it as the reference for how fast merging can be when only comparisons count, and as the base of fast PRAM merges such as Kruskal's. It also shows the gap between merging, with $\Theta(\log \log n)$ rounds, and sorting, with $\Theta(\log n)$. Do not use it as written on real hardware, where the bookkeeping that the model leaves out dominates.

## Pitfalls

- **Ties.** If A-samples count the items of $B$ that are at most them and B-samples the items of $A$ that are at most them, an A-sample and a B-sample with equal keys get the same position. Use "less than" for one list and "at most" for the other, as one comparison "$b < a$?" does.
- **Samples at the start of a piece.** A piece that starts at a split of a sample begins with that sample, which is already in place. Leaving it in makes a piece one item larger, and with $N = 2$ the size no longer drops.
- **Counting processors.** Comparing each sample pair once in round 1 and reading the result in both directions keeps round 1 at $\sqrt{m n}$ comparisons. Comparing each pair twice still fits in $m + n$, but only because $2 \sqrt{m n} \le m + n$.

## Implementations

## History

Valiant introduced the parallel comparison model in 1975 and gave merging in $O(\log \log n)$ rounds and finding the maximum in $O(\log \log n)$ rounds with $n$ processors. Borodin and Hopcroft proved the matching lower bound for merging in 1985. Kruskal in 1983 carried the merge over to the CREW PRAM with linear work, and Valiant's sampling idea is part of later fast PRAM merges and sorts.

## References
