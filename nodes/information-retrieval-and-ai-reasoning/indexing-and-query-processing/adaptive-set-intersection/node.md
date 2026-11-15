---
tag: 340HGS
kind: algorithm
slug: adaptive-set-intersection
name: Demaine-Lopez-Ortiz-Munro adaptive intersection
aliases:
- adaptive set intersection
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: research
summary: Intersects k sorted sets by cycling through them with galloping search, in time bounded by the size of a proof of the result.
solves: [posting-list-intersection]
model: comparison-model
complexity:
  vars: {k: the number of lists, m: the length of the shorter of two lists, n: the length of the longer of two lists}
  time: {two_lists: O(m log(n/m + 1)), lower: Ω(m log(n/m + 1))}
  space: {extra: O(k)}
properties: {deterministic: true, comparison: true, recursive: false}
prereqs: [small-versus-small-intersection, exponential-search, merging-lower-bound, adversary-argument]
see_also: [posting-list-intersection, baeza-yates-intersection, merge-based-list-intersection, decision-tree-model, information-theoretic-bound, binomial-coefficient, leapfrog-triejoin, posting-list]
sources:
  - paper: "Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Adaptive set intersections, unions, and differences, SODA 2000"
    title: Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Adaptive set intersections, unions, and differences, Proceedings of the 11th ACM-SIAM Symposium on Discrete Algorithms (SODA 2000), 743-752
    locator: Section 3 (proofs of the result, and their gap cost), Section 5 (the intersection algorithm with an eliminator and galloping from both ends), Theorem 5.1 and Corollary 5.2 (O(kG) time and at most 8kG comparisons)
  - paper: "Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Experiments on adaptive set intersections for text retrieval systems, ALENEX 2001"
    title: Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Experiments on adaptive set intersections for text retrieval systems, Algorithm Engineering and Experimentation (ALENEX 2001), Lecture Notes in Computer Science 2153, Springer, 91-104
    locator: the experiments with the adaptive intersection algorithm for text retrieval
  - paper: "Jérémy Barbay and Claire Kenyon, Adaptive intersection and t-threshold problems, SODA 2002"
    title: Jérémy Barbay and Claire Kenyon, Adaptive intersection and t-threshold problems, Proceedings of the 13th ACM-SIAM Symposium on Discrete Algorithms (SODA 2002), 390-399; journal version in ACM Transactions on Algorithms 4(1), Article 4, 2008
    locator: the Sequential algorithm, which searches the eliminator in one set after another, and its analysis
  - paper: doi:10.1145/1498698.1564507
    title: Jérémy Barbay, Alejandro López-Ortiz, Tyler Lu and Alejandro Salinger, An experimental investigation of set intersection algorithms for text searching, ACM Journal of Experimental Algorithmics 14, Article 3.7, 2009
    locator: the description of Adaptive, Small Adaptive, Sequential, SvS and Baeza-Yates, and their comparison on web query logs
---

The adaptive intersection of Erik Demaine, Alejandro López-Ortiz and Ian Munro intersects $k$ sorted lists by keeping one candidate id, the *eliminator*, and searching for it in the lists in turn with galloping steps. A list that holds an id greater than the eliminator gives a new eliminator; when all lists hold it, it goes to the output. The cost depends on how the lists interleave, not only on their lengths: an input whose result has a short proof is fast. The paper of 2000 gallops in each set from both ends and proves at most $8kG$ comparisons, where $G$ is the gap cost of the shortest proof of the result. This page gives the simpler form that gallops forward only. For two lists of lengths $m \le n$, it makes at most $2m \log_2(1 + n/m) + 6m$ tests, which is at most 8 times the lower bound $\log_2 \binom{m+n}{m}$ of every algorithm in the [comparison model](/comparison-model/). The proof of that lower bound is on this page, and the [merge](/merge-based-list-intersection/), [small-versus-small](/small-versus-small-intersection/) and [Baeza-Yates](/baeza-yates-intersection/) pages use it.

## In plain words

Pick the first number of the shortest list as the candidate. Go to the next list and jump forward in it, by steps that double, until you pass the candidate. Then search back in the last jump to find the first number that is not smaller than the candidate.

If that number is the candidate, this list agrees, and you go on to the next list. If it is larger, it is the new candidate, and the other lists must check it again. When every list agrees, the candidate is in the answer, and the next number of the last list becomes the new candidate.

Each list keeps its own place and never moves back. When the lists have long runs with no common numbers, the doubling jumps cross a run at a cost that grows only with the number of digits of its length.

## The problem

The input is $k \ge 1$ lists of document ids, each strictly increasing. The output is the list of ids that are in all of them, in increasing order. It is the AND query of [posting list intersection](/posting-list-intersection/).

## The algorithm

$H$ is the set of lists that are known to hold the eliminator $e$, and $\ell$ is the list of the last search. Each list $s$ has an index $pos(s)$, below which all of its ids are already dealt with, and a step $jump(s)$.

```pseudo id=main
ADAPTIVE(L_0, ..., L_{k-1})              ▷ each list strictly increasing
L1  sort the lists by length, shortest first; if a list is empty then return ()
L2  e ← L_0[0], pos(0) ← 1, H ← {0}, ℓ ← 0; pos(s) ← 0, jump(s) ← 1 for each other s
L3  loop
L4      if |H| = k then                   ▷ all lists hold e
L5          append e to R
L6          if pos(ℓ) = |L_ℓ| then return R
L7          e ← L_ℓ[pos(ℓ)], pos(ℓ) ← pos(ℓ) + 1, H ← {ℓ}, and go to L4
L8      s ← the next list after s, in round robin, that is not in H
L9      if pos(s) = |L_s| then return R
L10     p ← min(pos(s) + jump(s) - 1, |L_s| - 1)
L11     if L_s[p] < e then                ▷ one doubling step
L12         if p = |L_s| - 1 then return R
L13         pos(s) ← p + 1, jump(s) ← 2 jump(s)
        else                              ▷ e lies in L_s[pos(s)..p]
L14         a ← pos(s), c ← p
L15         while a < c: q ← ⌊(a + c)/2⌋; if L_s[q] < e then a ← q + 1 else c ← q
L16         pos(s) ← a + 1, jump(s) ← 1, ℓ ← s
L17         if L_s[a] = e then H ← H ∪ {s}
L18         else e ← L_s[a], H ← {s}
```

Each pass of lines L8 to L18 makes one doubling step in one list, so with $k \ge 3$ the lists that are not in $H$ take turns, one step each. A *run* of a list is its sequence of steps from $jump = 1$ to the next search. The stops at lines L9 and L12 mean that one list has no id at least $e$, so no more ids can be common.

## Example

Intersect $A = (7, 20, 40)$ with $B = (2, 4, 6, \ldots, 40)$, the 20 even numbers from 2 to 40, with $B[i] = 2i + 2$. $A$ is shorter, so it is $L_0$, and the first eliminator is 7.

| run | eliminator | probes of line L11 | search of line L15 | line L17 | tests | result |
|---|---|---|---|---|---|---|
| $B$, 1 | 7 | $B[0] = 2$, $B[2] = 6$, $B[6] = 14$ | $B[4] = 10$, $B[3] = 8$ | $8 \ne 7$ | 6 | $e = 8$ |
| $A$, 1 | 8 | $A[1] = 20$ | none | $20 \ne 8$ | 2 | $e = 20$ |
| $B$, 2 | 20 | $B[4] = 10$, $B[6] = 14$, $B[10] = 22$ | $B[8] = 18$, $B[9] = 20$ | $20 = 20$ | 6 | output 20, $e = B[10] = 22$ |
| $A$, 2 | 22 | $A[2] = 40$ | none | $40 \ne 22$ | 2 | $e = 40$ |
| $B$, 3 | 40 | $B[11] = 24$, $B[13] = 28$, $B[17] = 36$, $B[19] = 40$ | $B[18] = 38$ | $40 = 40$ | 6 | output 40, then stop at line L6 |

The result is $(20, 40)$ after 22 tests. The bound of Theorem 2 below is $2 \cdot 3 \log_2(1 + 20/3) + 18 \approx 35.6$. On this input, [Baeza-Yates](/baeza-yates-intersection/) makes 13 tests and small-versus-small makes 19, because each new eliminator from $A$ starts a new run in $B$ with a step of 1.

On the toy collection, sorted AND array AND search sorts the lists to search $(1, 7)$, array $(1, 2, 8)$ and sorted $(1, 2, 4, 8)$, and returns document 1 after 12 tests. Posting AND list returns $(3, 4)$ after 4 tests. For 10 random ids and 10000 random ids below $10^6$, it made 211 tests, against the bound of about 259.3 and the lower bound of about 111.1.

## Correctness

The proof keeps four facts before each check of line L4. The output is strictly increasing and holds only common ids, all less than $e$. Every common id not yet in the output is at least $e$. In a list not in $H$, every id below $pos(s)$ is less than $e$. In a list in $H$, the id just below $pos(s)$ is $e$, and the ones before it are less. A doubling step keeps these facts because the list is sorted. A search finds the first id at least $e$, so either the list joins $H$ or its id becomes a larger eliminator, and no common id lies between the old and the new eliminator. The sum of the indices grows at each pass, so the loop stops, and each stop happens only when no common id at least $e$ is left. The full proof is in the proof file below.

## Complexity

- **One run.** A run that moves the index of its list by $c$ makes at most $2 \log_2 c + 2$ tests: $t + 1$ doubling probes, at most $t$ tests of the binary search, and one equality test, with $c \ge 2^t$.
- **One list.** The runs of a list cover disjoint parts of it, so by Jensen's inequality a list of length $n_s$ with $r_s$ runs makes at most $2 r_s \log_2(1 + n_s / r_s) + 2 r_s$ tests. Two runs of a list start under two different eliminators, so $r_s \le E$, the number of values of $e$.
- **Two lists.** For $k = 2$ the runs alternate between the lists, so the longer list has at most $m$ runs and the shorter one at most $m - 1$. This gives at most $2m \log_2(1 + n/m) + 6m \le 8 \log_2 \binom{m+n}{m}$ tests.
- **Lower bound.** Every comparison algorithm needs $\lceil \log_2 \binom{m+n}{m} \rceil$ comparisons in the worst case, and $2n - 1$ when $m = n$. The proof: on an input with no common id, an algorithm must compare each two ids that are next to each other in the merged order and come from different lists; if it skips one pair, making the two ids equal does not change any outcome, but it changes the answer. So the outcomes at a leaf of the decision tree fix the interleaving of the two lists, and the $\binom{m+n}{m}$ interleavings need that many leaves.
- **The paper.** With galloping from both ends, Demaine, López-Ortiz and Munro prove $O(kG)$ time and at most $8kG$ comparisons (Theorem 5.1 and Corollary 5.2), where $G$ is the gap cost of the shortest proof of the result. This page does not prove that bound for the one-sided form.
- **Time and space.** The code finds the next list not in $H$ by a scan, which costs $O(k)$ per step; a circular list of the lists not in $H$ makes it $O(1)$. The extra space is $O(k)$ for the indices and steps.

## Properties

- **Adaptive.** The cost follows the structure of the input. Two lists that interleave in a few long blocks cost a few galloping runs, whatever their lengths.
- **Forward only.** Each index only grows, so the galloping step can be replaced by any forward seek to the first id at least $e$, such as one on a [posting list](/posting-list/) with [skip pointers](/skip-pointers/) or a block index. The bounds of this page are for galloping on arrays.
- **No list is special.** After the first eliminator, the order of the lists does not matter for correctness. The sort by length only gives the first eliminator from the shortest list.
- **Output in order.** The ids come out in increasing order, so the result can be piped into the next query step.

## Variants and improvements

- **Galloping from both ends.** The algorithm of the paper also searches each set from its far end, so that the cost of the largest gap in a set is not paid in full. This is the form that the $8kG$ bound is for.
- **Sequential.** Barbay and Kenyon search the eliminator in one list until it is found or passed, then go to the next list in a cycle, in place of one doubling step per list. For two lists, the form of this page also searches one list at a time.
- **Small Adaptive.** Barbay, López-Ortiz, Lu and Salinger study this variant next to [small-versus-small](/small-versus-small-intersection/) and the adaptive methods in their experiments on web queries.
- **Joins.** The leapfrog join in [leapfrog triejoin](/leapfrog-triejoin/) uses the same pattern for $k$ sorted iterators with a seek: the largest current key is the target, and the other iterators seek to it in turn.

## When to use it

Use it for AND queries of three or more terms, or when the lists may interleave in long blocks, for example when the documents of one topic have nearby ids. For two lists that differ a lot in length, [small-versus-small](/small-versus-small-intersection/) or [Baeza-Yates](/baeza-yates-intersection/) have the same bound with less bookkeeping. For two lists of about the same length that interleave finely, the [merge](/merge-based-list-intersection/) makes fewer tests.

## Pitfalls

- **Galloping from the start of the list.** Each run must start at $pos(s)$, not at index 0. A restart costs about $\log_2 n$ per search and loses the adaptive bound.
- **Not resetting the step.** Line L16 must set $jump(s) \leftarrow 1$. If the step keeps its large value, the next run starts with a long jump and a long binary search, even when the next id is close.
- **Output too early.** An id is common only when all $k$ lists hold it. Output at line L5 only when $H$ has all $k$ lists, and remove the other lists from $H$ at each new eliminator, at line L7 and line L18.
- **Repeated ids.** The proof needs each list to be strictly increasing. A list with a repeated id can make the equality test of line L17 see the same id twice.
- **One list.** With $k = 1$, $H$ is full at the start. Line L7 must go back to line L4, else the round robin of line L8 finds no list to step on.

## Implementations

## History

Demaine, López-Ortiz and Munro defined the proof of a result of a set operation and its gap cost, and gave the adaptive algorithms for intersection, union and difference at SODA in 2000. They reported experiments with the intersection algorithm for text retrieval at ALENEX in 2001. Barbay and Kenyon gave the Sequential algorithm and its analysis at SODA in 2002, with a journal version in 2008. Barbay, López-Ortiz, Lu and Salinger compared these algorithms with small-versus-small and Baeza-Yates on a log of web queries in 2009.

## References
