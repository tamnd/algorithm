---
tag: SRAJ81
kind: algorithm
slug: baeza-yates-intersection
name: Baeza-Yates intersection
aliases:
- double binary search intersection
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Searches the median of the shorter list in the longer one and recurses on both halves, adapting to the ratio of the list lengths.
solves: [posting-list-intersection]
model: comparison-model
complexity:
  vars: {m: the length of the shorter list, n: the length of the longer list}
  time: {worst: O(m log(n/m + 1))}
  space: {extra: O(log m)}
properties: {deterministic: true, comparison: true, recursive: true}
prereqs: [posting-list-intersection, binary-search, merge-based-list-intersection]
see_also: [small-versus-small-intersection, adaptive-set-intersection, sorted-array-intersection, merging-lower-bound, posting-list, exponential-search]
sources:
  - paper: doi:10.1007/978-3-540-27801-6_30
    title: Ricardo Baeza-Yates, A fast set intersection algorithm for sorted sequences, Combinatorial Pattern Matching (CPM 2004), Lecture Notes in Computer Science 3109, Springer, 400-408
    locator: the algorithm (binary search of the median of the smaller sequence in the larger one, then recursion on both sides) and its worst case analysis as a function of the two lengths
  - paper: doi:10.1007/11575832_2
    title: Ricardo Baeza-Yates and Alejandro Salinger, Experimental analysis of a fast intersection algorithm for sorted sequences, String Processing and Information Retrieval (SPIRE 2005), Lecture Notes in Computer Science, Springer, 13-24
    locator: the experiments that compare the algorithm with the merge and with the adaptive algorithms, and its use for more than two sequences
  - paper: doi:10.1145/1498698.1564507
    title: Jérémy Barbay, Alejandro López-Ortiz, Tyler Lu and Alejandro Salinger, An experimental investigation of set intersection algorithms for text searching, ACM Journal of Experimental Algorithmics 14, Article 3.7, 2009
    locator: the description of the Baeza-Yates algorithm for k sets, two at a time from the smallest, and its comparison with SvS and the adaptive algorithms on web queries
---

Baeza-Yates intersection computes the common ids of two sorted lists by divide and conquer: it takes the median of the shorter list, finds its place in the longer list by [binary search](/binary-search/), and recurses on the two left parts and on the two right parts. Ricardo Baeza-Yates published it in 2004 for [posting list intersection](/posting-list-intersection/). For lists of lengths $m \le n$ it makes at most $2m \log_2(2 + n/m) + 6m$ two-way comparisons, so it is within a constant factor of the lower bound $\log_2 \binom{m+n}{m}$ for every ratio of the lengths. When the lengths are equal it costs $O(n)$, like the [merge](/merge-based-list-intersection/), and when one list is very short it costs about a binary search for each of its ids.

## In plain words

Take the shorter list and pick the number in its middle. Look it up in the longer list with a halving search. This cuts the longer list in two at that place. Everything in the left half of the short list can only match something in the left part of the long list, and the same is true on the right. So the problem breaks into two smaller problems of the same kind, one on each side, plus a check of the middle number itself.

Solve each side the same way. At each new step, take the middle of whichever list is shorter now. A side with an empty list has no common numbers and needs no work.

## The problem

The input is two lists $A$ and $B$ of document ids, each strictly increasing. The output is the list of ids in both, in increasing order. For $k$ lists, the method runs on two lists at a time, from the shortest.

## The algorithm

The call BY$(A, 0, |A|, B, 0, |B|)$ appends $A \cap B$ to the output $R$. The ranges are half-open: $A[alo..ahi)$ holds $A[alo], \ldots, A[ahi - 1]$.

```pseudo id=main
BY(A, alo, ahi, B, blo, bhi)              ▷ appends A[alo..ahi) ∩ B[blo..bhi) to R
L1  if ahi - alo > bhi - blo then swap (A, alo, ahi) and (B, blo, bhi)
L2  if alo = ahi then return              ▷ the smaller range is empty
L3  mid ← alo + ⌊(ahi - alo) / 2⌋, x ← A[mid]
L4  p ← the least index in [blo, bhi] with p = bhi or B[p] ≥ x   ▷ binary search
L5  BY(A, alo, mid, B, blo, p)
L6  if p < bhi and B[p] = x then append x to R, p ← p + 1
L7  BY(A, mid + 1, ahi, B, p, bhi)
```

Line L1 keeps the median in the smaller range at each call, so the smaller range at least halves from a call to its children. Line L6 sits between the two calls, so the ids go to $R$ in increasing order.

## Example

Intersect $A = (7, 20, 40)$ with $B = (2, 4, 6, \ldots, 40)$, the 20 even numbers from 2 to 40, with indices from 0, so $B[i] = 2i + 2$.

| call | smaller range | larger range | $x$ | probes of line L4 | $p$ | line L6 | tests |
|---|---|---|---|---|---|---|---|
| root | $A[0..3)$ | $B[0..20)$ | 20 | $B[10] = 22$, $B[5] = 12$, $B[8] = 18$, $B[9] = 20$ | 9 | output 20 | 4 + 1 |
| left | $A[0..1)$ | $B[0..9)$ | 7 | $B[4] = 10$, $B[2] = 6$, $B[3] = 8$ | 3 | $8 \ne 7$ | 3 + 1 |
| right | $A[2..3)$ | $B[10..20)$ | 40 | $B[15] = 32$, $B[18] = 38$, $B[19] = 40$ | 19 | output 40 | 3 + 1 |

The four calls below these have an empty range of $A$ and return at line L2. The result is $(20, 40)$ after 13 tests. [Small-versus-small](/small-versus-small-intersection/) makes 19 tests on the same input and the merge makes 21 three-way steps. The bound of this page is $2 \cdot 3 \log_2(2 + 20/3) + 18 \approx 36.7$.

On the toy collection, sorted AND array is BY on $(1, 2, 8)$ and $(1, 2, 4, 8)$, with the result $(1, 2, 8)$, and the query sorted AND array AND search gives document 1.

For 10 random ids and 10000 random ids below $10^6$, the method made 125 tests. The bound is about 259.4, the lower bound is about 111.1, and the merge made 9956 steps.

## Correctness

Let $x = A[mid]$ and let $p$ be its place in the larger range. The ids of $A[alo..mid)$ are less than $x$ and the ids of $B[p..bhi)$ are at least $x$, so each common id less than $x$ is in the two left parts. In the same way, each common id greater than $x$ is in the two right parts, and $x$ itself is common exactly when $B[p] = x$. The two calls work on ranges with fewer ids in total, so by induction they output the common ids of their parts, in order. The full proof, with the count of comparisons, is in the proof file below.

## Complexity

- **Comparisons.** At most $2m \log_2(2 + n/m) + 6m \le 2m \log_2(1 + n/m) + 8m$ two-way tests for $m \ge 1$. The proof counts the recursion level by level: level $\ell$ has at most $2^\ell$ working calls, the ranges of one level do not overlap, and the depth is at most $\lfloor \log_2 m \rfloor$. Jensen's inequality bounds the cost of the binary searches of one level, and the sum over the levels is a geometric series.
- **Against the lower bound.** The bound is at most $10 \log_2 \binom{m+n}{m}$, so the method is optimal up to a constant factor. When $m = n$, it is about $2n \log_2 3 + 6n \approx 9.2n$ tests in the worst case, more than the $2n - 1$ steps of the merge; on random lists the count is far below this bound.
- **Empty sides.** A call whose range of $B$ is empty returns at once after the swap. If all ids of $A$ are less than $B[0]$, each left child gets an empty range of $B$, so only a chain of about $\log_2 m$ calls does work, at about $\log_2 n$ tests each.
- **Space.** The recursion depth is $O(\log m)$, because the smaller range halves at each level. The output has at most $m$ ids.
- **Time.** Linear in the number of tests, on the word RAM with random access to both lists.

## Properties

- **Adaptive to the ratio.** The same code costs $O(n)$ for equal lengths and $O(m \log n)$ for a very short list, with no parameter to tune.
- **Random access.** The binary search jumps to the middle of a range, so the lists must support access by index. On compressed lists this needs a block index or a code such as [Elias-Fano encoding](/elias-fano-encoding/).
- **Output in order.** With line L6 between the two calls, $R$ comes out sorted.
- **Recursive.** It suits a parallel run: the two calls of lines L5 and L7 work on disjoint ranges.

## Variants and improvements

- **More than two lists.** Intersect the two shortest lists, then the result with the next one, and so on. Barbay et al. describe the $k$-list form this way, with a sort of the result at the end, which is needed if the middle id is output before the left call.
- **Galloping in place of binary search.** Line L4 can gallop from one end of the range; this changes the constants only.
- **Stop when both sides are small.** When both ranges hold only a few ids, a [merge](/merge-based-list-intersection/) of the two ranges avoids the cost of more calls. This changes the constant factor, not the bound.
- **Hwang and Lin merging.** The merge of Hwang and Lin also uses binary search in blocks of the longer list, see [sorted array intersection](/sorted-array-intersection/).

## When to use it

Use it for two lists in memory with random access, when the ratio of their lengths is not known in advance: it adapts with no tuning. For many lists, or for lists that can only be read in order, [small-versus-small](/small-versus-small-intersection/) with a block index or the [adaptive algorithm](/adaptive-set-intersection/) of Demaine, López-Ortiz and Munro are the usual choices.

## Pitfalls

- **The median from the long list.** Line L1 must take the median from the smaller range. Without the swap, a call with $|A| = n$ and $|B| = m$ splits the long list and makes a binary search for each of up to $n$ ids, which is no better than the merge.
- **The whole list in the search.** Line L4 must search only $B[blo..bhi)$. A search over all of $B$ is still correct, but costs about $\log_2 n$ in each call, and the bound becomes $O(m \log n)$.
- **The order of output.** Line L6 must come after the call of line L5 and before the call of line L7. If line L6 comes first, the result is the right set but not in increasing order, and the next intersection step, which needs a sorted list, gives wrong results.
- **Skipping the matched id.** After a match, line L6 sets $p \leftarrow p + 1$. Without it, the right call still works, because all ids of $A[mid+1..ahi)$ are greater than $x$, but its range has one more id to search.

## Implementations

## History

Ricardo Baeza-Yates presented the algorithm at the CPM conference in 2004, with an analysis of its worst case as a function of the two lengths. Baeza-Yates and Salinger studied it in experiments in 2005. Barbay, López-Ortiz, Lu and Salinger compared it in 2009 with SvS and with the adaptive algorithms of Demaine, López-Ortiz and Munro and of Barbay and Kenyon on a log of web queries.

## References
