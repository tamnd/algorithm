---
tag: 9AEYS5
kind: algorithm
slug: schroeppel-shamir-algorithm
name: Schroeppel-Shamir algorithm
aliases:
- Schroeppel-Shamir
- split-and-list subset sum
area: techniques/meet-in-the-middle
level: advanced
summary: Subset sum in O(2^(n/2)) time with only O(2^(n/4)) memory, using heaps to generate the sums in order.
solves: [subset-sum-problem]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: O(n 2^(n/2)), best: O(n 2^(n/4))}
  space: {extra: O(2^(n/4))}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1981
  people: [Richard Schroeppel, Adi Shamir]
  note: Published in the SIAM Journal on Computing in 1981, as an improvement in memory of the 1974 method of Horowitz and Sahni.
prereqs: [subset-sum-problem, horowitz-sahni-algorithm, heapsort, two-pointer-pair-search]
see_also: [meet-in-the-middle-attack, howgrave-graham-joux-algorithm, representation-technique, k-way-merge, knapsack-problem, wagners-algorithm]
sources:
  - paper: doi:10.1137/0210033
    title: "Richard Schroeppel and Adi Shamir, A T = O(2^{n/2}), S = O(2^{n/4}) algorithm for certain NP-complete problems, SIAM Journal on Computing 10(3) (1981), 456-464"
    locator: the four-list algorithm for the knapsack problem and its time and space bounds
  - paper: doi:10.1145/321812.321823
    title: "Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2) (1974), 277-292"
    locator: the two-list method that the four-list method refines
  - paper: doi:10.1007/978-3-642-13190-5_12
    title: "Nick Howgrave-Graham and Antoine Joux, New generic algorithms for hard knapsacks, EUROCRYPT 2010, LNCS 6110, 235-256"
    locator: the introduction, which restates the Schroeppel-Shamir bounds as time and memory up to polynomial factors
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Section 6.5 (priority queues with a binary heap, O(lg n) per operation)
---

The Schroeppel-Shamir algorithm solves the [subset sum problem](/subset-sum-problem/) on $n$ items in $O(n \cdot 2^{n/2})$ time, within a factor $O(n)$ of the [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/), but with only $O(2^{n/4})$ memory instead of $O(2^{n/2})$. It splits the items into four quarters, and it uses two heaps to produce the sums of the first half in increasing order and the sums of the second half in decreasing order, without storing them. A two-pointer walk over these two streams then finds a pair with the target sum. It was for about 30 years the best known generic method for hard knapsacks, until the [representation technique](/representation-technique/) of Howgrave-Graham and Joux.

## In plain words

You want some of a set of numbers to add up to a target. Cut the numbers into four groups. Each group is small, so you can list all the sums that it can make.

A sum of the first two groups is one sum from group one plus one sum from group two. You never write down all these pairs. Instead, a heap gives you the next smallest such pair whenever you ask. In the same way, a second heap gives you the pairs of groups three and four from the largest down.

Now walk as in the classic search for a pair with a given sum in two sorted lists. If the smallest left value plus the largest right value is too small, take the next left value. If it is too large, take the next right value. If it is equal, you are done.

## The problem

The input is a list of integers $a_0, \ldots, a_{n-1}$ and a target $t$. The output is a set $S \subseteq \{0, \ldots, n-1\}$ with $\sum_{i \in S} a_i = t$, or NONE if no such set exists. This is the search version of the [subset sum problem](/subset-sum-problem/), which is [NP-complete](/np-complete/) in its decision form. The items may be negative, and equal items are allowed.

**The starting point.** The [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/) splits the items into two halves, lists the $2^{n/2}$ subset sums of each half in sorted order, and finds a pair with sum $t$ by a two-pointer walk. Its time is $\Theta(2^{n/2})$ when the sorted lists are built by merging, but it stores both lists, so its memory is $\Theta(2^{n/2})$. Schroeppel and Shamir keep the walk and remove the lists.

## The algorithm

Split the positions into four quarters $A, B, C, D$ of sizes $\lfloor n/4 \rfloor$ or $\lceil n/4 \rceil$. For a quarter $X$, let $L_X$ be the list of the $2^{|X|}$ pairs (subset sum, subset) of $X$. A subset $S$ of all positions is the same as four subsets, one of each quarter, and its sum is $u + v$, where $u$ is a sum of $L_A$ plus a sum of $L_B$, and $v$ is a sum of $L_C$ plus a sum of $L_D$.

```pseudo id=main
SCHROEPPEL-SHAMIR(a[0 .. n − 1], t)
L1  build L_A, L_B, L_C, L_D: the subset sums of the four quarters
L2  sort L_B and L_D by sum, increasing
L3  H1 ← min-heap of (L_A[i] + L_B[0], i, 0) for each i
L4  H2 ← max-heap of (L_C[k] + L_D[last], k, last) for each k
L5  while H1 and H2 are not empty do
L6      (s1, i, j) ← top of H1;  (s2, k, l) ← top of H2
L7      if s1 + s2 = t then return the union of the four subsets of i, j, k, l
L8      if s1 + s2 < t then pop H1; if j + 1 < |L_B| then push (L_A[i] + L_B[j + 1], i, j + 1) on H1
L9      else pop H2; if l > 0 then push (L_C[k] + L_D[l − 1], k, l − 1) on H2
L10 return NONE
```

Think of the sums $L_A[i] + L_B[j]$ as a table with one row for each $i$. Because $L_B$ is sorted, each row is increasing from left to right. The heap $H_1$ holds one cursor for each row: the leftmost entry of the row that has not been popped yet. The top of $H_1$ is then the smallest sum of the whole table that is still unused. When line L8 pops the cursor of row $i$, it pushes the next entry of the same row. This is the [k-way merge](/k-way-merge/) of the $2^{|A|}$ sorted rows, done lazily. The heap $H_2$ does the same for $L_C[k] + L_D[l]$, from right to left, so it produces the second-half sums in decreasing order.

Lines L5 to L9 are the [two-pointer pair search](/two-pointer-pair-search/) on the two streams. A left sum that is too small for the largest right sum that is still unused is too small for each unused right sum, so line L8 drops it. Line L9 is the mirror case.

## Example

Take $a = [31, 17, 45, 8, 26, 53, 12, 39]$ and $t = 110$. The quarters are $A = \{31, 17\}$, $B = \{45, 8\}$, $C = \{26, 53\}$, $D = \{12, 39\}$. After line L2:

| list | the sums |
|---|---|
| $L_A$ | 0, 31, 17, 48 |
| $L_B$ (sorted) | 0, 8, 45, 53 |
| $L_C$ | 0, 26, 53, 79 |
| $L_D$ (sorted) | 0, 12, 39, 51 |

At the start, $H_1$ holds the sums $L_A[i] + 0$, that is $\{0, 17, 31, 48\}$, and $H_2$ holds the sums $L_C[k] + 51$, that is $\{51, 77, 104, 130\}$. Each row of the table below is one pass of the loop of line L5. The heap columns show the sums in the heap before the step.

| step | $H_1$ | $H_2$ | $s_1$ | $s_2$ | $s_1 + s_2$ | action |
|---|---|---|---|---|---|---|
| 1 | 0 17 31 48 | 130 104 77 51 | 0 | 130 = 79 + 51 | 130 | too large, L9: push 79 + 39 = 118 |
| 2 | 0 17 31 48 | 118 104 77 51 | 0 | 118 = 79 + 39 | 118 | too large, L9: push 79 + 12 = 91 |
| 3 | 0 17 31 48 | 104 91 77 51 | 0 | 104 = 53 + 51 | 104 | too small, L8: push 0 + 8 = 8 |
| 4 | 8 17 31 48 | 104 91 77 51 | 8 | 104 | 112 | too large, L9: push 53 + 39 = 92 |
| 5 | 8 17 31 48 | 92 91 77 51 | 8 | 92 = 53 + 39 | 100 | too small, L8: push 0 + 45 = 45 |
| 6 | 17 31 45 48 | 92 91 77 51 | 17 = 17 + 0 | 92 | 109 | too small, L8: push 17 + 8 = 25 |
| 7 | 25 31 45 48 | 92 91 77 51 | 25 = 17 + 8 | 92 | 117 | too large, L9: push 53 + 12 = 65 |
| 8 | 25 31 45 48 | 91 77 65 51 | 25 | 91 = 79 + 12 | 116 | too large, L9: push 79 + 0 = 79 |
| 9 | 25 31 45 48 | 79 77 65 51 | 25 | 79 = 79 + 0 | 104 | too small, L8: push 17 + 45 = 62 |
| 10 | 31 45 48 62 | 79 77 65 51 | 31 = 31 + 0 | 79 = 79 + 0 | 110 | equal, L7 |

Step 10 returns $\{31\} \cup \emptyset \cup \{26, 53\} \cup \emptyset$, so $S = \{0, 4, 5\}$ and $31 + 26 + 53 = 110$. The heaps never held more than 4 entries, while the Horowitz-Sahni lists for this input have 16 entries each.

## Correctness

Call a sum of $L_A[i] + L_B[j]$ a *left entry* $(i, j)$ and a sum of $L_C[k] + L_D[l]$ a *right entry* $(k, l)$. An entry is *used* once it has been popped. The proof rests on two invariants of the loop of line L5.

- **(H)** The top of $H_1$ is a smallest unused left entry, and the top of $H_2$ is a largest unused right entry. A heap is empty only when all its entries are used.
- **(S)** If a left entry and a right entry have total $t$, then both are unused.

(H) holds because each row of the table is sorted and the heap holds the first unused entry of each row that still has one. (S) holds because line L8 pops a left entry $s_1$ only when $s_1$ plus the largest unused right entry is less than $t$, so $s_1$ has no partner among the unused right entries, and by (S) it has none among the used ones. Line L9 is symmetric. Each pass uses one entry, so the loop stops. If it stops at line L10, one side has no unused entry, and by (S) no subset has sum $t$. The full proof is in the proof file.

## Complexity

Let $h = \lceil n/4 \rceil$, so each quarter list has at most $2^h$ entries. The model is the [word RAM](/word-ram/), with each subset sum in $O(1)$ words.

- **Lines L1 and L2.** Building the four lists takes $O(2^h)$ additions. Sorting two of them takes $O(2^h \cdot h) = O(n \cdot 2^{n/4})$ time.
- **The heaps.** $H_1$ holds at most one entry for each row, so at most $|L_A| \le 2^h$ entries. Each push or pop costs $O(\log 2^h) = O(n)$ comparisons with a binary heap.
- **The walk.** Each pass of the loop pops one entry, and each entry is pushed at most once. There are $2^{|A| + |B|} = 2^{\lfloor n/2 \rfloor}$ left entries and $2^{\lceil n/2 \rceil}$ right entries, so the loop runs at most $2^{\lfloor n/2 \rfloor} + 2^{\lceil n/2 \rceil} = O(2^{n/2})$ times.
- **Total.** The worst-case time is $O(n \cdot 2^{n/2})$. The best case is a hit at the first pass, after $O(n \cdot 2^{n/4})$ time for lines L1 to L4.
- **Space.** Four lists and two heaps of at most $2^h$ entries each: $O(2^{n/4})$ words.

**The bound in the title.** The paper states $T = O(2^{n/2})$ and $S = O(2^{n/4})$. With a binary heap, the version above has the extra factor $n$ from the heap operations. Later papers, such as Howgrave-Graham and Joux (2010), restate the bounds as $\tilde{O}(2^{n/2})$ time and $\tilde{O}(2^{n/4})$ memory, where $\tilde{O}$ hides factors polynomial in $n$.

## Properties

- **Exact and deterministic.** It returns a solution whenever one exists, and NONE only when none exists. There is no randomness and no heuristic assumption.
- **Not a comparison algorithm.** It adds the items. It compares only sums.
- **Search, not counting.** Line L7 stops at the first hit. The walk does not report all solutions, because equal sums may be skipped in groups.
- **Any integers.** Negative items and equal items need no special case: the proof uses only the order of the sums.

## Variants and improvements

- **Lists for all solutions.** To count or list all solutions, on a hit pop all left entries equal to $s_1$ and all right entries equal to $s_2$, and output each pair. The time then also grows with the number of solutions.
- **Modular four-list merge.** Fix a modulus $M$ near $2^{n/4}$. For each residue $r$, join $L_A$ with $L_B$ on the sums that are $r$ modulo $M$, and $L_C$ with $L_D$ on those that are $t - r$ modulo $M$, with hash tables, then match the two joins on the full sum. Each solution is found at the residue of its left part, so the method is exact. When the sums spread evenly over the residues, each join has about $2^{n/4}$ entries, and the total time over all $M$ residues is about $2^{n/2}$, with no heaps. This even spread is an assumption about the input, not a worst-case bound. The [Howgrave-Graham-Joux algorithm](/howgrave-graham-joux-algorithm/) builds its lists with this kind of modular join.
- **Other problems.** The title of the paper refers to a class of NP-complete problems. The proof on this page uses only that a solution splits into four independent parts and that its value is the sum of the values of the parts.
- **Faster heuristic algorithms.** For random instances of density near 1, the [representation technique](/representation-technique/) gives heuristic time below $2^{n/2}$; see [Howgrave-Graham-Joux](/howgrave-graham-joux-algorithm/).

## When to use it

Use Schroeppel-Shamir when an exact answer is needed for subset sum or the [knapsack problem](/knapsack-problem/) with large numbers, and the $2^{n/2}$ memory of Horowitz-Sahni does not fit. At $n = 64$, Horowitz-Sahni stores $2^{32}$ sums for each half, while Schroeppel-Shamir stores lists and heaps of $2^{16}$ entries. If the memory of Horowitz-Sahni fits, use Horowitz-Sahni: it is simpler, and it needs no heap. If the numbers are small, the [dynamic program](/knapsack-dynamic-programming/) in $O(n t)$ time is better. For random instances of density near 1 where a heuristic method is acceptable, the [Howgrave-Graham-Joux algorithm](/howgrave-graham-joux-algorithm/) is faster.

## Pitfalls

- **Sorting the wrong lists.** Line L2 must sort $L_B$ and $L_D$, the lists that the cursors step through. Sorting $L_A$ and $L_C$ instead makes the rows unsorted, and the heap no longer gives the sums in order.
- **The wrong direction for the right side.** Line L4 must start each cursor at the last (largest) entry of $L_D$, and line L9 must step to $l - 1$. Starting at $L_D[0]$ with a max-heap gives a stream that is not decreasing, and the walk then misses solutions.
- **Pushing too early.** Push the next entry of a row only when line L8 or L9 pops its cursor. Pushing a whole row at once restores the $2^{n/2}$ memory of Horowitz-Sahni.
- **Overflow.** The sums of 64-bit items can need more than 64 bits. Use a wider integer type or bound the items.
- **An odd split.** When $n$ is not a multiple of 4, the quarters differ in size by one. The bounds stay the same up to a constant factor; do not drop the extra items.

## Implementations

## History

Horowitz and Sahni published the two-list method for the knapsack problem in 1974. Schroeppel and Shamir published the four-list method with priority queues in the SIAM Journal on Computing in 1981, under the title "A $T = O(2^{n/2})$, $S = O(2^{n/4})$ algorithm for certain NP-complete problems".

## References
