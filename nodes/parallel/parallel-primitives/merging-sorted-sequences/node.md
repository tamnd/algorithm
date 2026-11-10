---
tag: 9G5HDB
kind: problem
slug: merging-sorted-sequences
name: Merging sorted sequences
aliases:
- merge problem
area: parallel/parallel-primitives
level: intro
summary: Combine two sorted sequences into one sorted sequence. In parallel, each item finds its output place by ranking, or the output is cut into equal pieces by co-ranking.
prereqs: [merging-sorted-lists, binary-search, work-span-model]
see_also: [parallel-merge, parallel-merging-problem, merge-path, valiant-parallel-merge, shiloach-vishkin-merge, merging-lower-bound, parallel-merge-sort, k-way-merge]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.3, Multithreaded merge sort (the procedure P-MERGE with work Theta(n) and span Theta(log^2 n))
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Section 4.2 (merging by ranking, and the optimal merging algorithm)
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: pp. 348 to 355 (merging in O(log log n) rounds in the parallel comparison model)
  - paper: doi:10.1016/0196-6774(81)90010-9
    title: Yossi Shiloach and Uzi Vishkin, Finding the maximum, merging, and sorting in a parallel computation model, Journal of Algorithms 2(1), 1981
    locator: pp. 88 to 102 (merging with p processors in O(n/p + log n) time by cutting both sequences)
  - paper: doi:10.1109/IPDPSW.2012.202
    title: Saher Odeh, Oded Green, Zahi Mwassi, Oz Shmueli and Yitzhak Birk, Merge Path, parallel merging made simple, IEEE IPDPS Workshops, 2012
    locator: pp. 1611 to 1618 (the merge path and the binary search on its cross diagonals)
---

Merging asks to combine two sorted sequences into one sorted sequence. In sequence it is a simple loop with at most $m + n - 1$ comparisons, studied on the [merging sorted lists](/merging-sorted-lists/) page. This page is the parallel view. Two facts make merging easy to parallelize. First, each item can compute its own output position by *ranking*: its index in its own sequence plus the number of items of the other sequence that come before it. Second, for each output position $k$, a [binary search](/binary-search/) finds how many of the first $k$ outputs come from each input, which is *co-ranking*; with it, the output can be cut into equal pieces that independent workers merge in sequence. With these, merging has $O(m + n)$ work and $O(\log n)$ span. The [parallel merging problem](/parallel-merging-problem/) page has the full table of models and lower bounds.

Notation on this page: $A$ has $m$ items and $B$ has $n$ items, $N = m + n$, $p$ is the number of processors or pieces, $W$ is the work and $S$ the span in the [work-span model](/work-span-model/). $\lg$ is $\log_2$.

## In plain words

Two sorted piles of cards must become one sorted pile. One person can do it by always taking the smaller of the two top cards.

With many people, each card can find its own place. A card from the first pile looks at its place in its own pile, and counts the cards of the second pile that are smaller. The sum is its place in the final pile. A card can count fast, because the second pile is sorted and halving the search is enough.

Another way is to split the final pile into equal parts first. For each split point, a quick search tells how many cards of each pile fall before it. Then each person merges one part in the plain way.

## Definition

**Input.** Sequences $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of keys from a total order, each sorted in non-decreasing order.

**Output.** $C[0 \ldots N-1]$ with the items of $A$ and $B$ in non-decreasing order. The merge is *stable* when the items of each input keep their order and an item of $A$ comes before an equal item of $B$.

**Ranking.** Let $\operatorname{rank}_B(a)$ be the number of items of $B$ less than $a$, and $\operatorname{rank}_A(b)$ the number of items of $A$ at most $b$. The stable merge puts $A[i]$ at $C[i + \operatorname{rank}_B(A[i])]$ and $B[j]$ at $C[j + \operatorname{rank}_A(B[j])]$. The [parallel merging problem](/parallel-merging-problem/) page proves this.

**Co-ranking.** For $0 \le k \le N$, the *co-rank* of $k$ is the pair $(i, j)$ with $i + j = k$ such that the first $k$ items of the stable merge are exactly $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$. For $\max(0, k - n) \le t < \min(k, m)$, let

$$Q(t) \iff A[t] \le B[k - t - 1].$$

**Lemma (co-rank by binary search).** $Q$ is true on a prefix of its range and false on the rest, and the co-rank of $k$ has $i$ = the smallest $t$ in the range with $Q(t)$ false, or $i = \min(k, m)$ if there is none. So $i$ is found with at most $\lceil \lg(\min(m, n) + 1) \rceil$ comparisons.

*Proof.* As $t$ grows, $A[t]$ does not decrease and $B[k - t - 1]$ does not increase, so once $Q$ is false it stays false. In the stable order an item $A[t]$ comes before $B[s]$ exactly when $A[t] \le B[s]$. Let $(i, j)$ be the co-rank. If $t < i$, then $A[t]$ is among the first $k$ outputs, and $B[k - t - 1]$ is not, because only $j = k - i < k - t$ items of $B$ are, and so $B[k-t-1]$ has index at least $j$. So $A[t]$ comes before $B[k - t - 1]$ and $Q(t)$ is true. If $t \ge i$ (and $t < \min(k, m)$), then $A[t]$ is not among the first $k$ outputs, and $B[k - t - 1]$ is, because $k - t - 1 < k - i = j$. So $B[k - t - 1]$ comes before $A[t]$, which means $A[t] > B[k - t - 1]$, and $Q(t)$ is false. The range has at most $\min(k, m) - \max(0, k - n) + 1 \le \min(m, n) + 1$ candidates for $i$, and a binary search over them needs that many comparisons in the logarithm. $\square$

The co-rank is the point where the merge path of [merge path](/merge-path/) crosses the diagonal $i + j = k$ of the merge grid.

## Variants

- **Stable or not.** Without stability, ties may go either way; the ranks must still use "less than" on one side and "at most" on the other, or two equal items get the same position.
- **Very unequal lengths.** When $m \ll n$, $m$ independent binary searches of the items of $A$ in $B$ cost $O(m \log n)$ work and $O(\log n)$ span, much less than $N$. The lower bound is $\lg \binom{N}{m} = \Theta(m \log(n/m))$ comparisons ([merging lower bound](/merging-lower-bound/)).
- **Many sequences.** A [k-way merge](/k-way-merge/) of $k$ sorted sequences, as in [sample sort](/sample-sort/). Co-ranking extends to $k$ sequences with a search over $k$ indices at once.
- **Linked lists.** If the inputs are linked lists, there is no random access, and binary search is not possible. Convert them to arrays first by [list ranking](/list-ranking/).
- **In place.** Merge inside one array without a second buffer; parallel in-place merges exist but are complex.

## Examples

Let $A = [1, 3, 5, 7, 9, 11]$ and $B = [2, 4, 4, 8, 10, 12, 14]$, so $N = 13$. The merged output is $[1, 2, 3, 4, 4, 5, 7, 8, 9, 10, 11, 12, 14]$.

**Co-rank of $k = 8$.** The range of $i$ is $[\max(0, 8 - 7), \min(8, 6)] = [1, 6]$.

| step | lo | hi | $t$ | $A[t]$ | $B[8 - t - 1]$ | $Q(t)$ | new range |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 6 | 3 | 7 | $B[4] = 10$ | true | $[4, 6]$ |
| 2 | 4 | 6 | 5 | 11 | $B[2] = 4$ | false | $[4, 5]$ |
| 3 | 4 | 5 | 4 | 9 | $B[3] = 8$ | false | $[4, 4]$ |

So $i = 4$ and $j = 4$: the first 8 outputs are $1, 3, 5, 7$ from $A$ and $2, 4, 4, 8$ from $B$.

**Three equal pieces.** With $p = 3$, the cut points are $k = \lfloor tN/3 \rfloor = 0, 4, 8, 13$, with co-ranks $(0, 0)$, $(2, 2)$, $(4, 4)$ and $(6, 7)$.

| piece | outputs | from $A$ | from $B$ | merged |
|---|---|---|---|---|
| 0 | $C[0 \ldots 3]$ | 1, 3 | 2, 4 | 1, 2, 3, 4 |
| 1 | $C[4 \ldots 7]$ | 5, 7 | 4, 8 | 4, 5, 7, 8 |
| 2 | $C[8 \ldots 12]$ | 9, 11 | 10, 12, 14 | 9, 10, 11, 12, 14 |

Each piece is merged with the sequential merge, independently of the others. In piece 1, the 4 of $B$ comes before the 5 of $A$; the tie between the two items 4 of $B$ is kept in input order.

## Known algorithms

| method | model | work | span or time | page |
|---|---|---|---|---|
| sequential merge | RAM | $\Theta(N)$ | $\Theta(N)$ | [merging sorted lists](/merging-sorted-lists/) |
| rank each item by binary search | work-span, CREW PRAM | $\Theta(N \log N)$ | $\Theta(\log N)$ | [parallel merging problem](/parallel-merging-problem/) |
| P-MERGE: split at the median of the longer input, recurse | work-span | $\Theta(N)$ | $\Theta(\log^2 N)$ | [parallel merge](/parallel-merge/) |
| co-rank $p$ cut points, merge each piece in sequence | work-span, CREW PRAM | $O(N + p \log N)$ | $O(N/p + \log N)$ | [merge path](/merge-path/) |
| Shiloach and Vishkin 1981 | CREW PRAM | $O(N + p \log N)$ | $O(N/p + \log N)$ | [Shiloach-Vishkin merge](/shiloach-vishkin-merge/) |
| Valiant 1975 | parallel comparison model, $N$ processors | $O(N \log \log N)$ comparisons | $O(\log \log N)$ rounds | [Valiant's merge](/valiant-parallel-merge/) |
| odd-even or bitonic merging network | comparator network | $\Theta(N \log N)$ | depth $\lceil \lg N \rceil$ | [bitonic sort](/bitonic-sort/), [odd-even merge sort](/odd-even-merge-sort/) |

With $p = N / \lg N$, co-ranking gives $W = O(N)$ and $S = O(\log N)$, which is work-optimal. On the CREW PRAM the time can be lower: Kruskal (1983) merges in $O(\log \log N)$ time with $N / \log \log N$ processors. The two binary searches of a piece, at its start and at its end, read the same items as other pieces' searches, so these methods need concurrent reads; P-MERGE and the ranking method have the same need. Valiant's merge is faster in rounds, but its model counts only comparisons and lets all other work be free.

## Bounds

- **Work.** For $m = n$, each merge in the comparison model needs $2n - 1$ comparisons in the worst case, so $W = \Omega(N)$. For unequal lengths the bound is $\lg \binom{N}{m}$ ([merging lower bound](/merging-lower-bound/)).
- **Rounds.** In the parallel comparison model with $n$ processors, merging two lists of $n$ items needs $\Omega(\log \log n)$ rounds (Borodin and Hopcroft 1985), so Valiant's bound is tight there.
- **Span.** With binary forking, any value that depends on all $N$ inputs needs span $\Omega(\log N)$, so co-ranking with $p = N / \lg N$ is optimal in the work-span model.

## Reductions

- **Merging reduces to ranking.** The output position of each item is its own index plus its rank in the other sequence. So any method that computes all cross ranks merges with one more parallel step of $O(1)$ span and $O(N)$ work.
- **Sorting reduces to merging.** Merge sort sorts with $\lceil \lg N \rceil$ levels of merges. With P-MERGE this is [parallel merge sort](/parallel-merge-sort/) with span $\Theta(\log^3 N)$; with co-ranking at each level, span $O(\log^2 N)$.
- **Merging reduces to $p$ co-ranks and $p$ sequential merges.** This is the reduction that GPU and multicore libraries use, because each piece then runs the fast sequential loop on contiguous memory.

## Applications

- The merge step of [parallel merge sort](/parallel-merge-sort/) and of [Cole's merge sort](/cole-merge-sort/).
- The last phase of [sample sort](/sample-sort/) and of other multiway sorts, through a [k-way merge](/k-way-merge/).
- Union, intersection and difference of sorted sets, and merge joins in databases, which use the same co-rank cut to split the work.
- Merging on GPUs, where merge path or co-ranking gives each block an equal piece of the output.

## References
