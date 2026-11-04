---
tag: 7817P3
kind: algorithm
slug: horowitz-sahni-algorithm
name: Horowitz-Sahni algorithm
aliases:
- Horowitz-Sahni subset sum
- Horowitz-Sahni meet-in-the-middle
area: techniques/meet-in-the-middle
level: core
summary: Solves subset sum in O(2^(n/2)) time by sorting the sums of each half and merging them.
solves: [subset-sum-problem]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(2^(n/2)), average: Θ(2^(n/2)), best: Θ(2^(n/2))}
  space: {extra: Θ(2^(n/2))}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1974
  people: [Ellis Horowitz, Sartaj Sahni]
  note: Horowitz and Sahni split the items into two halves and combined the sorted lists of half sums, for subset sum and for the 0/1 knapsack problem.
prereqs: [subset-sum-problem, merging-sorted-lists, two-pointer-pair-search]
see_also: [meet-in-the-middle-attack, schroeppel-shamir-algorithm, howgrave-graham-joux-algorithm, knapsack-problem, two-sum-sorted, power-set-enumeration, pseudo-polynomial-time, exact-exponential-algorithms]
sources:
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2) (1974), 277-292
    locator: the two-list method for subset sums and its extension to the 0/1 knapsack problem
  - paper: doi:10.1137/0210033
    title: Richard Schroeppel and Adi Shamir, A T = O(2^{n/2}), S = O(2^{n/4}) algorithm for certain NP-complete problems, SIAM Journal on Computing 10(3) (1981), 456-464
    locator: the discussion of the two-list algorithm with time and space O(2^{n/2}) that the paper improves
  - paper: doi:10.1007/978-3-642-13190-5_12
    title: Nick Howgrave-Graham and Antoine Joux, New generic algorithms for hard knapsacks, EUROCRYPT 2010, LNCS 6110, 235-256
    locator: the discussion of earlier generic algorithms for knapsacks
---

The Horowitz-Sahni algorithm solves the [subset sum problem](/subset-sum-problem/) on $n$ numbers in $\Theta(2^{n/2})$ time and space. It splits the numbers into two halves, lists the $2^{n/2}$ subset sums of each half in sorted order, and finds two sums, one from each list, that add up to the target, with a [two-pointer](/two-pointer-pair-search/) scan. Each sorted list is built by repeated [merging](/merging-sorted-lists/), so no sort is needed. It is the classic meet-in-the-middle algorithm, and the best known worst-case time bound for subset sum on general instances is still of this form.

## In plain words

You want some weights from a pile to add up to a target exactly. Trying every group of weights takes too long, because the number of groups doubles with each new weight.

Cut the pile in two. For each half, list the totals of all its groups, from the smallest to the largest. Each list is short, because a half has only half of the weights. Now a good group is a group of the first half plus a group of the second half whose totals add up to the target.

Put one finger at the start of the first list and one at the end of the second. If the two totals are too small, move the first finger forward. If they are too large, move the second finger back. If they are right, you are done. If a finger falls off its list, there is no answer.

## The problem

The input is a list of integers $a_1, \ldots, a_n$ and an integer target $t$. The output is a set $I \subseteq \{1, \ldots, n\}$ with $\sum_{i \in I} a_i = t$, or NONE if there is no such set. The empty set is a valid answer for $t = 0$. The numbers may be negative. This is the search form of [subset sum](/subset-sum-problem/).

## The algorithm

A list entry is a pair $(s, T)$ of a sum $s$ and the set $T$ of the indices that give it. The lists are sorted by $s$.

```pseudo id=main
HOROWITZ-SAHNI(a[1 .. n], t)
L1  h ← ⌊n / 2⌋
L2  A ← SORTED-SUMS(a, 1, h)                  ▷ the 2^h sums of the first half
L3  B ← SORTED-SUMS(a, h + 1, n)              ▷ the 2^(n−h) sums of the second half
L4  i ← 0, j ← |B| − 1
L5  while i < |A| and j ≥ 0 do
L6      s ← A[i].s + B[j].s
L7      if s = t then return A[i].T ∪ B[j].T
L8      else if s < t then i ← i + 1           ▷ A[i] is too small for each B[q] with q ≤ j
L9      else j ← j − 1                         ▷ B[j] is too large for each A[p] with p ≥ i
L10 return NONE

SORTED-SUMS(a, lo, hi)                         ▷ all subset sums of a[lo .. hi], sorted
L11 S ← [(0, ∅)]
L12 for k ← lo to hi do
L13     S′ ← [(s + a[k], T ∪ {k}) for each (s, T) in S, in order]    ▷ sorted, since S is
L14     S ← MERGE(S, S′)
L15 return S
```

SORTED-SUMS keeps the sums of the items seen so far in a sorted list $S$. A new item $a_k$ doubles the subsets: each old subset, with or without $k$. Adding $a_k$ to each sum of a sorted list keeps it sorted, so line L13 gives a second sorted list $S'$, and line L14 merges the two in time linear in their length. The main procedure is a [two-sum scan on sorted lists](/two-sum-sorted/): $A$ is read upward and $B$ downward.

## Example

Take $a = (7, 11, 2, 9, 5, 14)$ and $t = 27$, so $h = 3$. The first half is $(7, 11, 2)$ and the second half is $(9, 5, 14)$. The sums after each step of line L14 are:

| step | the list $A$ (items 1 to 3) | the list $B$ (items 4 to 6) |
|---|---|---|
| start | [0] | [0] |
| item 1 or 4 | [0, 7] | [0, 9] |
| item 2 or 5 | [0, 7, 11, 18] | [0, 5, 9, 14] |
| item 3 or 6 | [0, 2, 7, 9, 11, 13, 18, 20] | [0, 5, 9, 14, 14, 19, 23, 28] |

For example, the last step of $A$ merges $[0, 7, 11, 18]$ with $[2, 9, 13, 20]$. In $B$, the sum 14 comes twice: from $\{4, 5\}$ (9 + 5) and from $\{6\}$.

The scan of lines L5 to L9, with 0-based positions:

| step | $i$ | $j$ | $A[i].s$ | $B[j].s$ | $s$ | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 7 | 0 | 28 | 28 | $s > t$: $j \leftarrow 6$ |
| 2 | 0 | 6 | 0 | 23 | 23 | $s < t$: $i \leftarrow 1$ |
| 3 | 1 | 6 | 2 | 23 | 25 | $s < t$: $i \leftarrow 2$ |
| 4 | 2 | 6 | 7 | 23 | 30 | $s > t$: $j \leftarrow 5$ |
| 5 | 2 | 5 | 7 | 19 | 26 | $s < t$: $i \leftarrow 3$ |
| 6 | 3 | 5 | 9 | 19 | 28 | $s > t$: $j \leftarrow 4$ |
| 7 | 3 | 4 | 9 | 14 | 23 | $s < t$: $i \leftarrow 4$ |
| 8 | 4 | 4 | 11 | 14 | 25 | $s < t$: $i \leftarrow 5$ |
| 9 | 5 | 4 | 13 | 14 | 27 | $s = t$: return |

The sum 13 is $\{2, 3\}$ and $B[4]$ is the sum 14 of $\{6\}$, so the answer is $\{2, 3, 6\}$: $11 + 2 + 14 = 27$. For the target 24, which no subset reaches, the scan takes 15 steps, the largest possible number $|A| + |B| - 1$, and ends with $i = 8$.

## Correctness

SORTED-SUMS is correct by induction on the loop of line L12: after the item $k$, $S$ holds each subset of $\{lo, \ldots, k\}$ once, with its sum, sorted by sum. The scan keeps this invariant at line L5:

> no pair of positions $(p, q)$ with $p < i$ or $q > j$ has $A[p].s + B[q].s = t$.

Each subset of $\{1, \ldots, n\}$ splits in exactly one way into a part in the first half and a part in the second half. So a solution exists if and only if some pair $(p, q)$ has $A[p].s + B[q].s = t$. When the loop stops with $i = |A|$ or $j < 0$, the invariant covers every pair, so NONE is right. The [full proof](proofs/correctness/) gives all steps.

## Complexity

The model is the [word RAM](/word-ram/): a sum and a set of at most $\lceil n/2 \rceil$ indices, stored as a bit mask, each fit in one word, and an addition, a comparison or an OR of two words takes unit time.

- **SORTED-SUMS on $m$ items.** Before the item number $k$ of the half, $|S| = 2^{k-1}$. Line L13 builds $2^{k-1}$ entries, and line L14 writes $2^k$ entries with at most $2^k - 1$ comparisons. Over the $m$ items, the merges write $\sum_{k=1}^{m} 2^k = 2^{m+1} - 2$ entries. So SORTED-SUMS takes $\Theta(2^m)$ time.
- **Both halves.** With $m = \lfloor n/2 \rfloor$ and $m = \lceil n/2 \rceil$, lines L2 and L3 take $\Theta(2^{\lceil n/2 \rceil})$ time, which is $\Theta(2^{n/2})$ up to a factor of at most $\sqrt 2$.
- **The scan.** Each step of lines L5 to L9 increases $i$ or decreases $j$, or returns. So there are at most $|A| + |B| - 1 = 2^{\lfloor n/2 \rfloor} + 2^{\lceil n/2 \rceil} - 1$ steps.

The time is $\Theta(2^{n/2})$ in each case, because lines L2 and L3 always build both full lists. The space is $\Theta(2^{n/2})$ for the lists. The output set takes $O(n)$ time to convert from a mask to a list of indices.

**With a sort.** If each half's sums are made in any order and then sorted by a comparison sort, the sort takes $\Theta(2^{n/2} \log 2^{n/2}) = \Theta(n \, 2^{n/2})$ comparisons in the worst case. The merge of line L14 removes this factor of $n$, because each list is built from two lists that are already sorted.

**Compared with exhaustive search.** [Brute-force search](/brute-force-search/) over all $2^n$ subsets takes $\Theta(2^n)$ time with a [Gray code](/gray-code/) order. The split takes the square root of this time and pays with $\Theta(2^{n/2})$ memory.

## Properties

- **Exact.** It answers each instance correctly. It is not a heuristic or an approximation.
- **Any integers.** The numbers and the target can be negative, and the numbers can be large. Only sums and comparisons are used. The cost does not depend on the size of the numbers in the word RAM.
- **Deterministic and not adaptive.** The time does not depend on the numbers. The lists cost $\Theta(2^{n/2})$ even when the answer is easy.
- **Memory bound.** For $n = 80$, each list has $2^{40}$ entries, about $1.1 \times 10^{12}$. The memory, not the time, sets the limit in practice.

## Variants and improvements

- **0/1 knapsack.** Horowitz and Sahni apply the same split to the [0/1 knapsack problem](/knapsack-problem/). Each half gives a list of (weight, profit) pairs. One way to combine them removes the dominated pairs, with more weight and not more profit, and then finds the best partner for each entry of the other list.
- **Less memory.** The [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/) splits into four quarters and makes the sums of each half in sorted order with priority queues. It keeps the time $O(2^{n/2})$ and needs only $O(2^{n/4})$ space.
- **Random dense instances.** The [Howgrave-Graham-Joux algorithm](/howgrave-graham-joux-algorithm/) uses the [representation technique](/representation-technique/) and runs in about $2^{0.337 n}$ time on random instances whose numbers have about $n$ bits. The bound is heuristic, and it does not hold for every instance.
- **Counting and all solutions.** To count the solutions or to list all of them, group equal sums in each list and scan the groups. The counting form is [counting subset sum](/counting-subset-sum/).
- **Hash instead of scan.** Put the sums of one half in a hash table and look up $t - s$ for each sum $s$ of the other half. This needs no sort at all, and takes $\Theta(2^{n/2})$ expected time.
- **Double encryption.** The [meet-in-the-middle attack](/meet-in-the-middle-attack/) on double encryption has the same structure: a list from each side, then a match in the middle.

## When to use it

Use it for subset sum and knapsack with up to about 40 to 60 items and large numbers, when the target or the numbers are too large for the [pseudo-polynomial](/pseudo-polynomial-time/) dynamic program in $O(nt)$ time. When the numbers are small, the dynamic program is faster. When memory is the limit, use Schroeppel-Shamir. For an approximate answer in polynomial time, use the [subset sum FPTAS](/subset-sum-fptas/).

## Pitfalls

- **A sort in place of the merge.** Building the sums in any order and calling a sort costs $\Theta(n \, 2^{n/2})$. Line L14 must merge the two sorted lists $S$ and $S'$.
- **Both pointers forward.** If $B$ is also scanned upward, the scan is wrong: after $s < t$ the right move can be in either list. Line L4 starts $j$ at the end of $B$, and line L9 moves it down.
- **Equal sums.** Do not remove the second entry with a sum already in the list, if you need all solutions or the subsets. For a yes or no answer, removing equal sums is safe and saves memory. In the example, the sum 14 has two subsets of the second half.
- **Losing the subset.** If the lists keep only the sums, line L7 can say yes but cannot give the subset. Keep the mask, or a pointer, with each sum.
- **Overflow.** A sum of $n/2$ numbers of $w$ bits needs about $w + \lg n$ bits. In a language with fixed-width integers, use a wider type for $s$ in line L6.

## Implementations

## History

Horowitz and Sahni published the method in 1974 in the Journal of the ACM, in a paper on computing partitions with applications to the knapsack problem. They gave the split into two halves for subset sums and its extension to the 0/1 knapsack problem. The split takes the time from about $2^n$, for a search over all subsets, to about $2^{n/2}$. Schroeppel and Shamir in 1981 kept the time and reduced the space to $O(2^{n/4})$.

## References
