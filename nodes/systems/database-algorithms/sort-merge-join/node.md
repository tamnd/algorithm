---
tag: CHDTJ2
kind: algorithm
slug: sort-merge-join
name: Sort-merge join
aliases:
- merge join
- sort-merge-join
- merge-scan join
area: systems/database-algorithms
level: intro
summary: "Sort both relations on the join attribute with external merge sort, then scan them in step and pair the groups of equal keys. About 3(M + N) page I/Os with enough memory."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of R, N: the number of pages of S, B: the number of buffer pages, p: the number of tuples per page of R, q: the number of tuples per page of S, T: the number of output tuples}
  time: {worst: Θ(p q M N), average: O((p M + q N) log (p M + q N) + T), best: O((p M + q N) log (p M + q N))}
  space: {extra: Θ(M + N)}
  io:
    worst: "O((M + N) log_B (M + N) + M N)"
    average: "3(M + N)"
    best: "3(M + N)"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: false}
history:
  year: 1977
  people: [Mike W. Blasgen, Kapali P. Eswaran]
  note: "Blasgen and Eswaran compared join methods for System R and found sorting both relations and merging them to be a good general method. System R used it as the merging scans join."
prereqs: [relational-join, external-merge-sort]
see_also: [hash-join, grace-hash-join, block-nested-loop-join, k-way-merge, replacement-selection, reduce-side-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.2, Sort-Merge Join (the algorithm, its cost, the refinement that combines the merge phases of the sorts with the join, and the examples with Reserves and Sailors), and Chapter 13, External Sorting
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the sections on sorting and on merge-join algorithms, and the comparison of sort-based and hash-based query processing
  - paper: doi:10.1147/sj.164.0363
    title: Mike W. Blasgen and Kapali P. Eswaran, Storage and access in relational data bases, IBM Systems Journal 16(4), 1977, pages 363 to 377
    locator: the comparison of join methods, including sorting both relations and merging
---

Sort-merge join computes the equi-join of two relations by sorting both on the join attribute and then scanning the two sorted files in step, as in the merge step of [merge sort](/merge-sort/). When the keys at the two cursors are equal, it pairs the whole group of tuples with that key in $R$ with the whole group in $S$. The sorts use [external merge sort](/external-merge-sort/), and when memory is large enough, the last merge of each sort is combined with the join, so the total cost is $3(M + N)$ page I/Os. The output comes out sorted on the key, which a later operator can use.

## In plain words

You have a stack of order slips and a stack of customer cards. First you sort both stacks by customer number. Then you put both stacks in front of you and look at the top of each. If the slip has the smaller number, that order has no customer, so you put the slip away. If the card has the smaller number, you put the card away. If the numbers are equal, you take all slips and all cards with that number and write one line for each slip and card pair.

Each stack is gone through only once after the sort. The sort is most of the work, and with enough desk space both stacks can be sorted in one sweep each, with the matching done during the last merge.

## The problem

The input is two relations $R$ and $S$ on disk and the condition $r.a = s.b$, where the keys have a total order. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/).

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ has $M$ pages with $p_R$ tuples per page, $S$ has $N$ pages with $p_S$ tuples per page, and memory holds $B \ge 3$ pages. The cost is the number of page reads and writes, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$. The [external memory model](/external-memory-model/) and the page [external merge sort](/external-merge-sort/) count the same transfers but use $N$ for the items, $M$ for the memory and $B$ for the block size.

## The algorithm

```pseudo id=main
SORT-MERGE-JOIN(R, S, a, b, B)              ▷ the join r.a = s.b, B ≥ 3
L1  form sorted runs of R on a and of S on b, from B pages at a time      ▷ pass 0
L2  while the runs of R and S together are more than B − 2 and one of them has two or more runs do
L3      do one merge pass, B − 1 runs at a time, on the input with more runs
L4  r ← the first tuple of the merge of the runs of R, s ← the first tuple of the merge of the runs of S
L5  while neither input is used up do
L6      if r.a < s.b then r ← the next tuple of R
L7      else if r.a > s.b then s ← the next tuple of S
L8      else                                   ▷ r.a = s.b = v
L9          G_R ← r and the next tuples of R with key v, G_S ← s and the next tuples of S with key v
L10         append r′ · s′ to out for each r′ in G_R and each s′ in G_S
L11 return out
```

Line L1 is pass 0 of [external merge sort](/external-merge-sort/): it reads $B$ pages, sorts them in memory and writes a run. Lines L2 and L3 are merge passes with a [k-way merge](/k-way-merge/) of fan-in $B - 1$. They stop as soon as all runs of both inputs fit in $B - 2$ frames, one frame per run, with one frame left for the output and one for scratch. Line L4 then merges all runs of $R$ and all runs of $S$ at the same time as the join. This is the refinement of Ramakrishnan and Gehrke, Section 14.4.2: the last merge pass of each sort and the join are one pass.

Lines L5 to L10 are the merge phase. The cursors only move forward, except inside a group. Line L10 forms the product of the two groups with key $v$. If the group $G_S$ does not fit in the free frames, it must be read again for each further page of $G_R$. When it comes from a merge of runs, it is first written to a temporary file so that it can be read again.

## Example

Let $R$ have the keys $[7, 2, 9, 2, 4, 7, 1, 5]$ (tuples $r_0$ to $r_7$) and $S$ have the keys $[2, 7, 3, 7, 8, 2]$ ($s_0$ to $s_5$), two tuples per page, so $M = 4$ and $N = 3$. With $B = 4$, line L1 makes one run of each: $R$ sorted is $1, 2, 2, 4, 5, 7, 7, 9$ and $S$ sorted is $2, 2, 3, 7, 7, 8$. There are 2 runs and $B - 2 = 2$ frames, so line L2 does nothing.

| line | key of $r$ | key of $s$ | action | output so far |
|---|---|---|---|---|
| L6 | 1 | 2 | advance $r$ | 0 |
| L8 to L10 | 2 | 2 | $G_R = \{r_1, r_3\}$, $G_S = \{s_0, s_5\}$, 4 pairs | 4 |
| L7 | 4 | 3 | advance $s$ | 4 |
| L6 | 4 | 7 | advance $r$ | 4 |
| L6 | 5 | 7 | advance $r$ | 4 |
| L8 to L10 | 7 | 7 | $G_R = \{r_0, r_5\}$, $G_S = \{s_1, s_3\}$, 4 pairs | 8 |
| L7 | 9 | 8 | advance $s$, and $S$ is used up | 8 |

The output has 8 tuples. Pass 0 reads and writes 7 pages, and the merge phase reads 7 pages, so the cost is $3(M + N) = 21$.

**The textbook sizes.** For Reserves ($M = 1000$) and Sailors ($N = 500$), the simulator of the implementation gives these exact counts, with one tuple per page:

| $B$ | runs after pass 0 | plan | I/Os |
|---|---|---|---|
| 35 | 29 and 15 | sort each fully, then merge | $4 \cdot 1000 + 4 \cdot 500 + 1500 = 7500$ |
| 35 | 29 and 15 | one merge pass on $R$, then join with 1 + 15 runs | $2000 + 1000 + 2000 + 1500 = 6500$ |
| 300 | 4 and 2 | join directly from the 6 runs | $3 \cdot 1500 = 4500$ |

Ramakrishnan and Gehrke give 7500 for the plain plan and 4500 for the combined plan with $B = 300$.

## Correctness

The invariant of line L5 is: every pair of matching tuples with key less than $\min(r.a, s.b)$ has been output exactly once, and no pair with a key at least $\min(r.a, s.b)$ has been output. Line L6 skips an $r$ whose key is less than every key that remains in $S$, so $r$ has no match left. Line L7 is the same for $s$. Line L10 outputs all pairs with key $v$ at once and moves both cursors past $v$. When one input is used up, the remaining tuples of the other have no match. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Sorting.** With the plain plan, each input is sorted fully by [external merge sort](/external-merge-sort/). A sort of $M$ pages with $B$ buffers makes $\lceil M/B \rceil$ runs and does $1 + \lceil \log_{B-1} \lceil M/B \rceil \rceil$ passes, each of which reads and writes $M$ pages. The merge phase then reads $M + N$ pages. With two passes per input, the total is $4M + 4N + M + N = 5(M + N)$.
- **Combined plan.** If the runs of pass 0 already fit, that is $\lceil M/B \rceil + \lceil N/B \rceil \le B - 2$, the cost is $2M + 2N$ for pass 0 and $M + N$ for the join, or $3(M + N)$. Because $\lceil x \rceil < x + 1$, the condition holds when $B(B - 4) \ge M + N$, so roughly when $B > \sqrt{M + N} + 2$.
- **The textbook condition.** Ramakrishnan and Gehrke state $3(M + N)$ when $B > \sqrt{L}$, where $L$ is the size of the larger relation. They assume pass 0 uses [replacement selection](/replacement-selection/), which makes runs of about $2B$ pages on random input, so each relation has fewer than $\sqrt{L}/2$ runs. This implementation sorts $B$ pages at a time, which gives the slightly stronger condition above. Both are sufficient conditions, not exact ones.
- **Duplicate keys.** If a group of key $v$ spans $h$ pages of sorted $R$ and $g$ pages of sorted $S$, and $g$ is more than the free frames, the group of $S$ is read $h$ times instead of once. In the worst case all keys are equal, and the merge phase costs $M + MN$ in this model. Ramakrishnan and Gehrke state the worst case as $MN$. The sorts still cost the same.
- **Work in memory.** The sorts make $O(n \log n)$ comparisons with $n = p_R M + p_S N$ tuples, and the merge phase does $O(n + T)$ work. In the worst case, $T = p_R p_S M N$.

## Properties

- **Sorted output.** The output is in key order, so a later join on the same key, an ORDER BY or a GROUP BY can use it with no new sort.
- **Inequality and band joins.** With a change to lines L6 to L10, it also computes $r.a < s.b$ or $|r.a - s.b| \le c$ joins, which hash joins cannot do.
- **No sensitivity to skew in the sort.** Unlike a hash partition, a sort never makes one run much larger than the others. Skew only hurts in line L10, when one key has many tuples on both sides.
- **Exact and deterministic.** The I/O count depends only on the sizes and on the duplicate groups.

## Variants and improvements

- **Inputs already sorted.** If $R$ or $S$ is already sorted on the key, for example by a [clustered index](/clustered-index/) or by an earlier operator, its sort is skipped. With both sorted, the cost is $M + N$.
- **Replacement selection.** Pass 0 with [replacement selection](/replacement-selection/) makes runs of about $2B$ pages, which halves the number of runs.
- **Block I/O.** Read and write runs in blocks of several pages to cut seeks. This lowers the fan-in of each merge.
- **Hash join.** The [Grace hash join](/grace-hash-join/) has the same $3(M + N)$ cost and needs only $B > \sqrt{f M}$, with $M$ the smaller relation, while sort-merge needs memory for the runs of both. Graefe's survey discusses the duality between sorting and hashing in detail.
- **On a cluster.** The [reduce-side join](/reduce-side-join/) of MapReduce shuffles tuples by key and sorts them at each reducer, then joins the groups of equal keys. It is a distributed form of the merge phase.

## When to use it

Use it when the output must be sorted on the key, when one or both inputs are already sorted, when the condition is an inequality or a band, or when the key distribution is so skewed that hash partitions would overflow. For two large unsorted inputs and an equality, a [hash join](/hash-join/) usually needs less memory for the same cost. If one input is small, a [block nested-loop join](/block-nested-loop-join/) or an in-memory hash join is cheaper.

## Pitfalls

- **Advancing both cursors on a match.** If line L10 pairs only $r$ with $s$ and then moves both cursors, every pair beyond the first in a group is lost. With keys $2, 2$ on both sides, the output would have 2 tuples instead of 4. Line L9 must collect the whole groups.
- **Advancing the wrong cursor.** Line L6 must move the cursor with the smaller key. Moving the other one skips tuples that can still match.
- **Not rereading a large group.** If the group $G_S$ of line L9 spans more pages than fit in memory, the merge must read it again for each page of $G_R$. An implementation that assumes groups fit in memory either fails or loses tuples on heavily duplicated keys.
- **Merging too many runs at once.** Line L2 must stop only when all runs of both inputs fit in $B - 2$ frames. With more runs than frames, line L4 cannot hold one page of each run.

## Implementations

## History

Blasgen and Eswaran (1977) compared join methods for System R and recommended sorting both relations and merging them as the general method. The System R optimizer of Selinger et al. (1979) costed this merging scans join. Sorting was the main method for joins and grouping until hash joins became common in the 1980s. Graefe's survey (1993) gives the sort-based algorithms and their duality with the hash-based ones. Ramakrishnan and Gehrke, Section 14.4.2, give the cost formulas and the refinement that combines the last merge passes with the join, used here.

## References
