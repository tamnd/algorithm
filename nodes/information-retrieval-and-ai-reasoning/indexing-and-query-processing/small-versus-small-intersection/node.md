---
tag: 39S9T4
kind: algorithm
slug: small-versus-small-intersection
name: Small-versus-small intersection
aliases:
- SvS intersection
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Intersects many lists by taking the two shortest first and searching each candidate of the short list in the next one by galloping.
solves: [posting-list-intersection]
model: comparison-model
complexity:
  vars: {m: the length of the shortest list, n: the length of the next list, k: the number of lists}
  time: {worst: O(m log(n/m + 1)), best: O(m)}
  space: {extra: O(m)}
properties: {deterministic: true, comparison: true, recursive: false}
prereqs: [posting-list-intersection, merge-based-list-intersection, exponential-search]
see_also: [posting-list, baeza-yates-intersection, adaptive-set-intersection, skip-pointers, sorted-array-intersection, merging-lower-bound, leapfrog-triejoin]
sources:
  - paper: doi:10.1145/1498698.1564507
    title: Jérémy Barbay, Alejandro López-Ortiz, Tyler Lu and Alejandro Salinger, An experimental investigation of set intersection algorithms for text searching, ACM Journal of Experimental Algorithmics 14, Article 3.7, 2009
    locator: the description of SvS (sort the sets by size, search each element of the smallest set in the others, with binary or galloping search from the last position), the Swapping SvS and Small Adaptive variants, and the experiments on web queries
  - paper: doi:10.1145/1877766.1877767
    title: J. Shane Culpepper and Alistair Moffat, Efficient set intersection for inverted indexing, ACM Transactions on Information Systems 29(1), Article 1, 2010
    locator: the shortest-first intersection of posting lists with search in the longer lists, on uncompressed and compressed lists
  - paper: doi:10.1145/237496.237497
    title: Alistair Moffat and Justin Zobel, Self-indexing inverted files for fast text retrieval, ACM Transactions on Information Systems 14(4), 349-379, 1996
    locator: the evaluation of conjunctive queries from the rarest term, with candidates checked in the longer lists through skips
---

Small-versus-small (SvS) is an algorithm for [posting list intersection](/posting-list-intersection/) that sorts the $k$ lists by length, takes the shortest list as the set of candidates, and checks each candidate in the next list with a galloping search that starts where the last search ended. The candidates that survive are checked in the next list, and so on. For two lists of lengths $m \le n$ it makes at most $2m \log_2(1 + n/m) + 3m$ two-way comparisons, which is within a factor of 5 of the lower bound $\log_2 \binom{m+n}{m}$ for every algorithm in the [comparison model](/comparison-model/). Barbay, López-Ortiz, Lu and Salinger describe it as a simple and widely used method, and use it as a baseline for the adaptive algorithms.

## In plain words

Suppose a query has three words, and the lists of their documents have 10, 5000 and 80000 entries. The answer can hold at most 10 documents, the ones of the shortest list. So take those 10 as candidates.

For each candidate, look for it in the next list. The candidates are sorted, so each search can start where the last one stopped. Each search jumps ahead by 1, then 2, then 4, then 8 places, until it passes the candidate, and then it narrows down with halving. A candidate that is not found is dropped. Then do the same with the next list, with only the candidates that are left.

The work grows with the number of candidates and only slowly with the length of the long list.

## The problem

The input is $k \ge 1$ lists $L_1, \ldots, L_k$ of document ids, each strictly increasing. The output is the list of the ids in all of them, in increasing order.

## The algorithm

GALLOP$(L, x, lo)$ returns the least index $p \ge lo$ with $L[p] \ge x$, or $|L|$ if there is none. It probes $lo, lo + 1, lo + 3, lo + 7, \ldots$ until it finds an id at least $x$, then does a binary search in the last gap. It is the operation NEXT-GEQ of the [posting list](/posting-list/) page, and a form of [exponential search](/exponential-search/).

```pseudo id=main
SVS(L_1, …, L_k)                         ▷ each list strictly increasing
L1  sort the lists so that |L_1| ≤ |L_2| ≤ … ≤ |L_k|
L2  C ← L_1                               ▷ the candidates
L3  for t ← 2 to k while C is not empty do
L4      R ← empty list, p ← 0
L5      for each x in C, in order do
L6          p ← GALLOP(L_t, x, p)
L7          if p = |L_t| then leave the loop of line L5
L8          if L_t[p] = x then append x to R, p ← p + 1
L9      C ← R
L10 return C
```

The search of line L6 starts at $p$, not at 0. All ids of $L_t$ before $p$ are smaller than the last candidate, so they are smaller than $x$ too.

## Example

Intersect $A = (7, 20, 40)$ with $B = (2, 4, 6, \ldots, 40)$, the 20 even numbers from 2 to 40. Indices of $B$ start at 0, so $B[i] = 2i + 2$.

| candidate | start $p$ | probes of the doubling | binary search | answer $p$ | $B[p]$ | tests | output |
|---|---|---|---|---|---|---|---|
| 7 | 0 | $B[0] = 2$, $B[1] = 4$, $B[3] = 8$ | $B[2] = 6$ | 3 | 8 | 4 + 1 | |
| 20 | 3 | $B[3] = 8$, $B[4] = 10$, $B[6] = 14$, $B[10] = 22$ | $B[8] = 18$, $B[9] = 20$ | 9 | 20 | 6 + 1 | 20 |
| 40 | 10 | $B[10] = 22$, $B[11] = 24$, $B[13] = 28$, $B[17] = 36$ | $B[19] = 40$, $B[18] = 38$ | 19 | 40 | 6 + 1 | 40 |

For the candidate 40, the next probe would be at index $10 + 15 = 25$, which is past the end, so the doubling stops without a test and the binary search runs on indices 18 and 19. The "+ 1" in each row is the equality test of line L8. The result is $(20, 40)$ after 19 tests. The bound is $2 \cdot 3 \log_2(1 + 20/3) + 9 \approx 26.6$. The merge of the same two lists takes 21 three-way steps, which is 40 two-way tests.

On the toy collection, the query sorted AND array AND search orders the lists as search $(1, 7)$, array $(1, 2, 8)$ and sorted $(1, 2, 4, 8)$. The candidates $(1, 7)$ go into the list of "array": 1 is found at index 0 after 2 tests, and the search for 7 stops at the id 8 after 3 tests. The one candidate left, 1, is found in the list of "sorted" after 2 tests. The answer is document 1, after 7 tests.

The gain is large when the lengths differ a lot. For 10 random ids and 10000 random ids below $10^6$, SvS made 210 tests, the bound of the next section is about 229.3, and the merge made 9956 three-way steps.

## Correctness

The candidate list after step $t$ is $L_1 \cap \cdots \cap L_t$. Inside one step, the loop keeps this invariant: each id of $L_t$ before index $p$ is less than the current candidate. So GALLOP from $p$ finds the first id of the whole list that is at least $x$, and $x$ is in $L_t$ exactly when that id equals $x$. If the search runs off the end, all ids of $L_t$ are less than $x$, so no later candidate can be in $L_t$, and line L7 may stop the step. The full proof, with the count of comparisons, is in the proof file below.

## Complexity

- **One search.** If GALLOP skips $g$ ids, it makes 1 test when $g = 0$ and at most $2 \lfloor \log_2 g \rfloor + 2$ tests when $g \ge 1$.
- **One step.** For $r$ candidates and a list of length $n$, the skips add up to at most $n$, and by the concavity of the logarithm the step makes at most $2r \log_2(1 + n/r) + 3r$ two-way tests.
- **All steps.** With $n_1 \le \cdots \le n_k$, the candidates never number more than $n_1$, so SVS makes at most $\sum_{t=2}^{k} \left(2 n_1 \log_2(1 + n_t/n_1) + 3 n_1\right)$ tests. For two lists this is $O(m \log(1 + n/m))$.
- **Against the lower bound.** For two lists, $\log_2 \binom{m+n}{m} \ge m \log_2(1 + n/m) \ge m$, so the bound $2m \log_2(1 + n/m) + 3m$ is at most 5 times the lower bound. When $m = n$, it is about $5n$ tests, worse than the $2n - 1$ steps of the [merge](/merge-based-list-intersection/), so the method is best for lists of different lengths.
- **Time and space.** The time is linear in the number of tests, plus the sort of $k$ lengths. The extra space is the list of candidates, at most $n_1$ ids.

## Properties

- **Shortest first.** The candidate list never grows, and the first list sets the cost of all later steps.
- **Each list in one direction.** In one step, $p$ only grows, so each list is read from left to right, with jumps.
- **Not adaptive between lists.** A candidate is searched in list $t$ only after it has passed all lists before $t$. A candidate that the last list would reject at once still costs a search in each list before it. The method of Demaine, López-Ortiz and Munro avoids this.

## Variants and improvements

- **Binary search from the last position.** The original SvS of the experimental literature uses binary search over the rest of the list, from $p$ to the end. Each search then costs about $\log_2(n - p)$ tests, so the total is $O(m \log n)$ instead of $O(m \log(1 + n/m))$.
- **Swapping SvS.** A variant that can swap the roles of the candidate list and the searched list, so that the search always runs from the list with fewer ids left. Barbay et al. credit it to Hwang and Lin.
- **Small Adaptive.** Search each candidate in all other lists before it moves to the next candidate, and keep the lists sorted by the number of ids that remain. Barbay et al. describe it as a mix of SvS and the adaptive method.
- **Skips on compressed lists.** On a compressed list, line L6 jumps with [skip pointers](/skip-pointers/) or with a table of the first id of each block, then decodes one block.
- **Divide and conquer.** [Baeza-Yates intersection](/baeza-yates-intersection/) has the same bound with a recursive split in place of the left-to-right scan.
- **Galloping in all lists.** The [adaptive set intersection](/adaptive-set-intersection/) of Demaine, López-Ortiz and Munro gallops in all lists in turn with one candidate at a time.

## When to use it

Use SvS for AND queries over posting lists of very different lengths, which is the common case for web queries with one rare and one common term. Use it when the lists support random access or have a block index. When all lists have about the same length, the [merge](/merge-based-list-intersection/) makes fewer comparisons and has simpler branches.

## Pitfalls

- **Searching from 0.** Line L6 must start at the last position: "$p \leftarrow$ GALLOP$(L_t, x, p)$". With "$p \leftarrow$ GALLOP$(L_t, x, 0)$", each search costs up to about $2 \log_2$ of the index of its answer, and the total can reach about $2m \log_2 n$ in place of $2m \log_2(1 + n/m) + 3m$. The result is still right.
- **Not advancing after a match.** Line L8 must set $p \leftarrow p + 1$ after a match. Without it, the result is still right, but the next search makes one extra test at the old position.
- **Missing the end test.** Line L7 must stop the step when GALLOP returns $|L_t|$. Without it, line L8 reads $L_t[|L_t|]$, past the end.
- **Wrong order of lists.** Line L1 must sort by length. If the longest list of $n$ ids is the candidate list, the first step makes a search for each of its ids until the short list runs out, which can be $n$ searches, so the cost is linear in $n$ again.

## Implementations

## History

Moffat and Zobel in 1996 evaluated conjunctive queries from the term with the shortest list and checked each candidate in the longer lists with the help of skips, which is the SvS plan on compressed lists. Demaine, López-Ortiz and Munro in 2000 used galloping for intersection in their adaptive analysis. Barbay, López-Ortiz, Lu and Salinger in 2009 described SvS with binary and galloping search and compared it with the adaptive algorithms on a log of web queries. Culpepper and Moffat in 2010 studied the method on compressed lists, with hybrid representations for long lists.

## References
