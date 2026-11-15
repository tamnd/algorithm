---
tag: 06R0D3
kind: algorithm
slug: merge-based-list-intersection
name: Merge-based list intersection
aliases:
- linear merge intersection
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Walks two sorted posting lists with one pointer each and advances the smaller, in time linear in the sum of the lengths.
solves: [posting-list-intersection]
model: comparison-model
complexity:
  vars: {m: the length of the shorter list, n: the length of the longer list, k: the number of lists}
  time: {worst: O(m + n), best: Θ(m)}
  space: {extra: O(1)}
properties: {deterministic: true, comparison: true, recursive: false}
prereqs: [posting-list-intersection, sorted-array-intersection, loop-invariant]
see_also: [posting-list, skip-pointers, small-versus-small-intersection, baeza-yates-intersection, adaptive-set-intersection, positional-intersection, merging-sorted-lists, merging-lower-bound]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1, Section 1.3 (the INTERSECT algorithm for two postings lists, its time linear in the total length, and the processing of terms in order of increasing document frequency)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.2 (minimum-comparison merging, and the optimality of the straight merge when the two lists have equal length)
  - paper: doi:10.1145/1877766.1877767
    title: J. Shane Culpepper and Alistair Moffat, Efficient set intersection for inverted indexing, ACM Transactions on Information Systems 29(1), Article 1, 2010
    locator: the intersection methods for uncompressed and compressed posting lists, from the plain merge to the search-based and hybrid methods
---

Merge-based list intersection finds the common document ids of two sorted [posting lists](/posting-list/) by walking both with one pointer each: if the two ids are equal it outputs the id and advances both, else it advances the pointer at the smaller id. It solves [posting list intersection](/posting-list-intersection/) with at most $m + n - 1$ comparisons for lists of lengths $m$ and $n$, and it reads each list only from left to right, so it works on compressed lists that can only be decoded in order. The same two-pointer scan on plain arrays is on the page [sorted array intersection](/sorted-array-intersection/), which treats general arrays with repeated values and the search-based variants; this page is about the index setting, where the ids are strictly increasing, the lists come from a [posting list](/posting-list/) store, and a query with $k$ terms needs an order in which to intersect the lists.

## In plain words

Put two sorted lists of document numbers side by side, with a finger on the first number of each. Look at the two numbers under your fingers. If they are equal, write the number down and move both fingers. If they are not, the smaller number cannot be in the other list any more, because the other list has only bigger numbers left. So move the finger that is on the smaller number. Stop when a finger falls off the end of its list.

For a query with many words, take the two shortest lists first. Their common part is short, and each next step works with that short list.

## The problem

The input is two lists $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of document ids, each strictly increasing. The output is the list of ids in both, in increasing order. For a query with $k \ge 1$ terms, the input is $k$ such lists, and the output is the ids in all of them.

## The algorithm

INTERSECT is the two-list merge. INTERSECT-ALL runs it on the lists of a query, shortest first.

```pseudo id=main
INTERSECT(A, B)                          ▷ A and B strictly increasing
L1  R ← empty list, i ← 0, j ← 0
L2  while i < |A| and j < |B| do
L3      if A[i] = B[j] then
L4          append A[i] to R, i ← i + 1, j ← j + 1
L5      else if A[i] < B[j] then i ← i + 1
L6      else j ← j + 1
L7  return R

INTERSECT-ALL(L_1, …, L_k)
L8  sort the lists so that |L_1| ≤ |L_2| ≤ … ≤ |L_k|
L9  R ← L_1
L10 for t ← 2 to k while R is not empty do
L11     R ← INTERSECT(R, L_t)
L12 return R
```

Lines L3 and L5 make one three-way comparison. The loop reads $A[i]$ and $B[j]$ only, and $i$ and $j$ only grow, so a cursor that decodes the next id of a compressed list is enough.

## Example

Intersect the lists of "sorted" and "array" from the toy collection: $A = (1, 2, 4, 8)$ and $B = (1, 2, 8)$.

| step | $i$ | $j$ | $A[i]$ | $B[j]$ | line | $R$ |
|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 1 | 1 | L4 | 1 |
| 2 | 1 | 1 | 2 | 2 | L4 | 1, 2 |
| 3 | 2 | 2 | 4 | 8 | L5 | 1, 2 |
| 4 | 3 | 2 | 8 | 8 | L4 | 1, 2, 8 |

After step 4, $i = 4 = |A|$ and the loop stops. The merge made 4 comparisons; the bound is $4 + 3 - 1 = 6$.

For the query sorted AND array AND search, line L8 orders the lists as search $(1, 7)$, array $(1, 2, 8)$, sorted $(1, 2, 4, 8)$. The first merge compares 1 with 1, 7 with 2 and 7 with 8, and gives $(1)$ after 3 comparisons. The second merge compares 1 with 1 and stops after 1 comparison. The answer is document 1, after 4 comparisons.

## Correctness

The loop keeps this [invariant](/loop-invariant/): $R$ holds the common ids of the prefixes $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$, in order, and no id of a passed prefix is in the part of the other list that is not yet passed. When $A[i] < B[j]$, the id $A[i]$ cannot be in $B[j \ldots]$, since all those ids are at least $B[j]$, and it is not in $B[0 \ldots j-1]$ by the invariant. So line L5 can drop it. When the loop stops, one list is used up, and each of its ids that is in the other list is in $R$. For INTERSECT-ALL, after step $t$ the list $R$ is the intersection of the first $t$ lists, so an empty $R$ means an empty answer. The full proof is in the proof file below.

## Complexity

- **Comparisons, two lists.** Each step makes one comparison and increases $i + j$ by at least 1. A step runs only when $i \le m - 1$ and $j \le n - 1$, so there are at most $m + n - 1$ steps. The input $B = (1, 2, \ldots, n-1, n+m)$, $A = (n, \ldots, n+m-1)$ reaches this bound. With two-way tests in place of the three-way comparison, each step makes at most 2 tests.
- **Best case.** The loop needs at least $\min(m, n)$ steps, because each step advances each pointer by at most 1. This is reached, for example, when the shorter list is a prefix of the longer one.
- **Time and space.** $O(m + n)$ time and $O(1)$ extra space, besides the output, which has at most $\min(m, n)$ ids.
- **Many lists.** With $n_1 \le \cdots \le n_k$, INTERSECT-ALL makes at most $\sum_{t=2}^{k} (n_1 + n_t - 1)$ comparisons, since the list $R$ never has more than $n_1$ ids.
- **Optimality.** When $m = n$, the bound $2n - 1$ is optimal in the [comparison model](/comparison-model/): on the input $a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n$, each of the $2n - 1$ pairs of neighbours comes from different lists and must be compared directly, as shown in the proof file of [adaptive set intersection](/adaptive-set-intersection/). When $m$ is much smaller than $n$, the merge is far from the lower bound $\log_2 \binom{m+n}{m}$. For $m = 10$ random ids and $n = 10000$ random ids below $10^6$, the merge made 9956 comparisons, against a lower bound of about 111.

## Properties

- **One pass, in order.** Each list is read once, from left to right. This suits compressed lists and lists on disk.
- **Output in order.** The result is a sorted list of ids, so it can be the input of the next merge.
- **Not adaptive to length ratio.** The cost depends on how far the pointers move, which is up to $m + n$ even when one list is short.
- **Adaptive to the data in one way.** The loop stops as soon as one list ends. If all ids of $A$ are less than $B[0]$, it makes only $m$ comparisons.

## Variants and improvements

- **Skip pointers.** Store forward pointers in the long list, and follow one when its target is still at most the id in the other list. See [skip pointers](/skip-pointers/).
- **Galloping.** Replace the step of one position in line L5 or L6 by a doubling search for the first id at least the other id. With the search only in the longer list, this is [small-versus-small](/small-versus-small-intersection/); with the search in both, it is the method of Demaine, López-Ortiz and Munro, see [adaptive set intersection](/adaptive-set-intersection/).
- **Divide and conquer.** Search the median of the short list in the long list and recurse on both sides. See [Baeza-Yates intersection](/baeza-yates-intersection/).
- **k-way merge.** Merge all $k$ lists at once with a heap and output an id that appears $k$ times. This is the form that [document-at-a-time evaluation](/document-at-a-time-evaluation/) uses for ranked queries, but for AND it does more work than the shortest-first order.
- **Union and difference.** OR outputs each id that is in either list, with one copy of a common id; AND NOT outputs $A[i]$ in line L5 and drops it in line L4.
- **Positional merge.** In each common document, merge the position lists to test a phrase. See [positional intersection](/positional-intersection/).

## When to use it

Use the merge when the two lists have similar lengths, or when the lists are compressed with no way to jump. It is simple, it has no branches that depend on a search, and it reads memory in order. When one list is much shorter than the other, a search-based method such as small-versus-small makes far fewer comparisons.

## Pitfalls

- **Advancing the wrong pointer.** Line L5 must advance the pointer at the smaller id: "if $A[i] < B[j]$ then $i \leftarrow i + 1$". With "if $A[i] < B[j]$ then $j \leftarrow j + 1$", the pointer passes over ids of $B$ that may equal later ids of $A$. On $A = (3, 5)$ and $B = (4, 5)$, that version compares 3 with 4 and moves past 4, then compares 3 with 5 and moves past 5, and it returns an empty list although 5 is in both.
- **Or in place of and.** Line L2 must be "while $i < |A|$ and $j < |B|$". With "or", the loop reads past the end of the list that is used up.
- **The query order.** Line L8 must sort the lists by length. In the query order, posting AND list AND merge first gives $(3, 4)$ after 2 comparisons and then needs 3 more; shortest first, list AND merge is empty after 3 comparisons and the loop stops. On a real index, a common term first can make the first merge cost millions of steps.
- **Lists with repeated ids.** The proof needs strictly increasing lists. If a bad build puts the same id twice in each list, line L4 outputs it twice.

## Implementations

## History

The two-pointer merge of sorted lists is far older than search engines; Knuth gives the theory of merging with the fewest comparisons, including the result that the straight merge is optimal for two lists of equal length. Manning, Raghavan and Schuetze present the merge as the INTERSECT algorithm of their first chapter, with the rule to process the terms in order of increasing document frequency. Culpepper and Moffat compare it with search-based and hybrid methods on compressed and uncompressed lists.

## References
