---
tag: YE460Y
kind: algorithm
slug: ppjoin
name: PPJoin
aliases:
- positional prefix join
area: searching/similarity-search
level: advanced
summary: Extends prefix filtering with positional filtering to prune candidate pairs in set similarity joins.
model: word-ram
complexity:
  vars: {n: the number of sets, N: the total size of the sets, m: the size of the largest set}
  time: {worst: O(N log N + n^2 m)}
  space: {extra: Θ(N + n)}
properties: {deterministic: true, online: false}
history:
  year: 2008
  people: [Chuan Xiao, Wei Wang, Xuemin Lin, Jeffrey Xu Yu]
  note: Xiao, Wang, Lin and Yu added the positional filter and the suffix filter to the prefix filtering join at WWW 2008.
prereqs: [prefix-filtering, jaccard-similarity]
see_also: [prefix-filtering, set-similarity-join, allpairs, jaccard-similarity, inverted-index, minhash, shingling, string-similarity-join]
sources:
  - paper: doi:10.1145/1367497.1367516
    title: Chuan Xiao, Wei Wang, Xuemin Lin and Jeffrey Xu Yu, Efficient similarity joins for near duplicate detection, Proceedings of the 17th International World Wide Web Conference (WWW 2008)
    locator: pages 131 to 140 (Section 3, the positional filter and the PPJoin algorithm; Section 4, the suffix filter and PPJoin+)
  - paper: doi:10.1145/2000824.2000825
    title: Chuan Xiao, Wei Wang, Xuemin Lin, Jeffrey Xu Yu and Guoren Wang, Efficient similarity joins for near-duplicate detection, ACM Transactions on Database Systems 36(3), 2011
    locator: article 15 (the journal version, with the overlap thresholds for Jaccard, cosine and overlap similarity and the experiments)
  - paper: doi:10.1145/1242572.1242591
    title: Roberto J. Bayardo, Yiming Ma and Ramakrishnan Srikant, Scaling up all pairs similarity search, Proceedings of the 16th International World Wide Web Conference (WWW 2007)
    locator: pages 131 to 140 (All-Pairs, the indexing of a shorter prefix and the processing of the sets in order of size, which PPJoin builds on)
---

PPJoin answers the [set similarity join](/set-similarity-join/): given $n$ sets and a threshold $t$, report every pair whose [Jaccard similarity](/jaccard-similarity/) is at least $t$. It is [prefix filtering](/prefix-filtering/) with one more test, the *positional filter*. When the prefixes of two sets share an element, its positions in the two sorted sets bound how many more elements the sets can share; if the bound is below the overlap that $J \ge t$ requires, the pair is dropped before verification. The output is exact. The worst case is still all $\binom{n}{2}$ pairs, but on text data the filter removes most of the candidates that prefix filtering leaves. Xiao, Wang, Lin and Yu published it in 2008, with a second filter on the suffixes, in PPJoin+.

## In plain words

Each set is written in a fixed order, rare items first. Prefix filtering says that two sets that are similar enough must share an item near the front of both lists. So you only compare sets that share such a front item.

PPJoin looks also at where the shared item sits. Say it is the second item of one list of ten and the eighth item of another list of ten. All other shared items come after it in both lists, and the second list has only two items left. So the two sets share at most one item before it, this one, and two after. If being similar needs six shared items, the pair is hopeless, and you drop it without comparing the two sets in full. Only pairs that pass this cheap test are checked item by item.

## The problem

Input: a collection $R$ of $n$ finite sets over a universe with a total order, and a threshold $0 < t \le 1$. Output: all pairs $\{x, y\}$ of sets of $R$ with $J(x, y) = |x \cap y| / |x \cup y| \ge t$. Empty sets are left out.

The condition is a condition on the overlap. Write $o = |x \cap y|$. Then $o / (|x| + |y| - o) \ge t$ if and only if $o(1 + t) \ge t(|x| + |y|)$, so

$$J(x, y) \ge t \iff |x \cap y| \ge \alpha(x, y) = \left\lceil \frac{t}{1 + t}\,(|x| + |y|) \right\rceil.$$

## The algorithm

Sort the elements of each set by a global order $\prec$, usually by increasing frequency in $R$, and process the sets in order of size. For a set $x$, the *probing prefix* is its first $|x| - \lceil t|x| \rceil + 1$ elements, as in [prefix filtering](/prefix-filtering/). The *indexing prefix* is shorter, its first $|x| - \lceil \frac{2t}{1+t} |x| \rceil + 1$ elements, since every later set is at least as large as $x$ (the idea of All-Pairs). The [inverted index](/inverted-index/) $I$ maps an element $w$ to the pairs $(y, j)$ such that $w$ is the $j$-th element of $y$ and lies in the indexing prefix of $y$.

```pseudo id=main
PPJOIN(R, t)
L1  sort the elements of each set by ≺, and the sets by size
L2  I ← an empty inverted index
L3  for each set x of R in order of size do
L4      A ← an empty map from sets to counts
L5      for i ← 1 to |x| − ⌈t|x|⌉ + 1 do                  ▷ probing prefix of x
L6          w ← x[i]
L7          for each (y, j) in I[w] with |y| ≥ t|x| and y not pruned do     ▷ size filter
L8              α ← ⌈t (|x| + |y|) / (1 + t)⌉
L9              if A[y] + 1 + min(|x| − i, |y| − j) ≥ α then A[y] ← A[y] + 1     ▷ positional filter
L10             else mark y as pruned for x
L11         if i ≤ |x| − ⌈2t|x| / (1 + t)⌉ + 1 then append (x, i) to I[w]
L12     for each y with A[y] > 0 and y not pruned do
L13         if |x ∩ y| ≥ ⌈t (|x| + |y|) / (1 + t)⌉ then output (x, y)    ▷ verification
```

Line L7 reads the list of $w$ and applies the size filter $|y| \ge t|x|$: since $|y| \le |x|$, $J(x, y) \le |y| / |x|$. Line L9 is the positional filter. $A[y]$ counts the common elements found so far, all of which come before $w$ in both sets. The element $w$ is one more. Every common element after $w$ is among the last $|x| - i$ elements of $x$ and among the last $|y| - j$ elements of $y$. If even this optimistic count is below $\alpha$, the pair cannot reach the threshold, and line L10 removes $y$ for the rest of the probe of $x$. Line L11 indexes $x$ only in its indexing prefix. Line L13 verifies the survivors by a merge of the two sorted sets.

## Example

Take the six sets and the threshold $t = 0.6$ of the [prefix filtering](/prefix-filtering/) example, with the same order $H \prec F \prec G \prec A \prec B \prec E \prec C \prec D$. Then $t/(1+t) = 0.375$ and $2t/(1+t) = 0.75$. A set of size 3, 5 or 6 has a probing prefix of 2, 3 or 3 elements and an indexing prefix of 1, 2 or 2 elements.

| set | sorted | probe | index | positional tests (element, $y$, $i$, $j$, bound, $\alpha$) | verified |
|---|---|---|---|---|---|
| $r_4$ | H G A | H G | H | none | none |
| $r_1$ | A B E C D | A B E | A B | none | none |
| $r_2$ | F A B C D | F A B | F A | A, $r_1$, 2, 1, 4, 4 pass; B, $r_1$, 3, 2, 4, 4 pass | $r_1$: 0.6667, output |
| $r_5$ | H F E C D | H F E | H F | H, $r_4$, 1, 1, 3, 3 pass; F, $r_2$, 2, 1, 4, 4 pass | $r_4$: 0.1429; $r_2$: 0.4286 |
| $r_3$ | F G B E C D | F G B | F G | F, $r_2$, 1, 1, 5, 5 pass; F, $r_5$, 1, 2, 4, 5 pruned; B, $r_1$, 3, 2, 4, 5 pruned | $r_2$: 0.5714 |
| $r_6$ | G A B E C D | G A B | G A | G, $r_3$, 1, 2, 5, 5 pass; A, $r_1$, 2, 1, 5, 5 pass; A, $r_2$, 2, 2, 4, 5 pruned; B, $r_1$, 3, 2, 5, 5 pass | $r_3$: 0.7143, output; $r_1$: 0.8333, output |

The output is $(r_1, r_2)$, $(r_1, r_6)$ and $(r_3, r_6)$, the same as with prefix filtering, after 6 verifications instead of 10; the positional filter pruned 3 pairs. For instance, when $r_3$ = F G B E C D meets $r_5$ = H F E C D at F, the element F is first in $r_3$ and second in $r_5$, so the overlap is at most $0 + 1 + \min(5, 3) = 4$, below $\alpha = \lceil 0.375 \cdot 11 \rceil = 5$. Indeed $|r_3 \cap r_5| = 4$. The shorter indexing prefix also helps: $r_1$ is not indexed under E, so $r_5$ does not meet $r_1$ at all.

## Correctness

**Theorem.** PPJOIN outputs exactly the pairs of nonempty sets of $R$ with $J(x, y) \ge t$, each once.

*Proof sketch.* Line L13 outputs a pair only if $|x \cap y| \ge \alpha(x, y)$, which is equivalent to $J(x, y) \ge t$, so every output is correct. Each pair is examined only when its later set is probed, so it is output at most once. Now let $J(x, y) \ge t$ with $y$ before $x$ in the order of size. Let $u$ be the least common element under $\prec$, at position $i$ of $x$ and $j$ of $y$. Since $|x \cap y| \ge \alpha$ and the $\alpha$ common elements come at or after $u$ in both sets, $i \le |x| - \alpha + 1$ and $j \le |y| - \alpha + 1$. A computation shows that these lie in the probing prefix of $x$ and the indexing prefix of $y$, so line L7 finds $(y, j)$ under $u$, and the size filter passes. The positional bound of line L9 is never below the true overlap, since $A[y]$ is the number of common elements before the current one, so $y$ is never pruned, and line L13 verifies it. The full proof, with the computation of the two prefixes, is in [the correctness proof](proofs/correctness.md). $\square$

## Complexity

In the word-RAM model, with elements as words and an exact rational comparison for the thresholds:

- Sorting the elements and the sets takes $O(N \log N)$ time for $N = \sum_{x \in R} |x|$, after a count of the frequencies with a hash table in $O(N)$ expected time.
- The probe of a set reads the lists of its prefix elements; every entry read is one size test and at most one positional test, $O(1)$ each. A pair of sets meets at most once per element of the probing prefix of the later set, so this part costs $O(n^2 m)$ in the worst case, and $O(\sum_w |I[w]| \cdot c(w))$ in general, where $c(w)$ is the number of probing prefixes that contain $w$.
- Each verification costs $O(|x| + |y|) = O(m)$ by a merge, and there are at most $\binom{n}{2}$ of them.

So the worst case is $O(N \log N + n^2 m)$ time, met for example when all sets equal $\{1, \ldots, m\}$ and $t = 1$, where every pair is an answer and must be verified. The index holds at most $N$ entries and the map $A$ at most $n$, so the extra space is $\Theta(N + n)$. As with every exact join, the output itself can have $\Theta(n^2)$ pairs, and under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) no algorithm decides in time $O(n^{2 - \varepsilon})$ whether a join of sets of size $\omega(\log n)$ is empty; see the [set similarity join](/set-similarity-join/) page.

## Properties

- **Exact.** No randomness and no approximation: the output equals that of the quadratic scan for every input.
- **Offline.** The sets are processed in order of size, so all of them must be known in advance. Adding a set smaller than an indexed one breaks the indexing prefix argument.
- **Order of elements.** The result does not depend on $\prec$, but the cost does. Increasing frequency puts rare elements in the prefixes and keeps the lists short.

## Variants and improvements

- **PPJoin+ (suffix filter).** For a pair that passes the positional filter, take an element of the suffix of $x$, find it in the suffix of $y$ by binary search, and bound the [Hamming distance](/hamming-distance/) $|x \mathbin{\triangle} y|$ of the suffixes by the sizes of the parts left and right of it, recursively to a small depth. Since $J \ge t$ forces $|x \mathbin{\triangle} y| \le |x| + |y| - 2\alpha$, a larger lower bound drops the pair. Xiao et al. report that it pays off for large sets such as long documents.
- **Other similarities.** For the cosine $|x \cap y| / \sqrt{|x||y|}$ the overlap threshold is $\lceil t \sqrt{|x||y|} \rceil$ and the size filter is $|y| \ge t^2 |x|$; for the overlap similarity the threshold is the constant $t$. Only lines L5, L7, L8 and L11 change.
- **Verification from the prefix.** Real implementations do not merge the full sets in line L13; they start the merge after the last prefix positions and reuse the count $A[y]$, and they stop when the remaining elements cannot reach $\alpha$.
- **Later algorithms.** MPJoin bounds the prefix that still matters for each list entry and removes useless entries; AdaptJoin chooses the prefix length per set. In experimental comparisons none of them is best on every data set, and PPJoin remains a standard baseline.
- **Two collections.** For a join of $R$ against $S$, index one collection and probe with the other, with the size filter in both directions.

## When to use it

Use PPJoin to find all near-duplicate pairs among many sets, such as [shingle](/shingling/) sets of documents or token sets of records, when the answer must be exact and the threshold is high, say $t \ge 0.7$. For low thresholds the prefixes grow, almost every pair is a candidate, and [MinHash](/minhash/) with banding is the usual choice, at the cost of missing some pairs with a probability that the parameters fix.

## Pitfalls

- **Floating-point thresholds.** $\lceil 0.6 \cdot 5 \rceil$ computed in floating point can give 4 instead of 3, and a prefix one element too short loses answers. Compute $\lceil t|x| \rceil$ and $\alpha$ with rational arithmetic, or with a small tolerance toward the safe side.
- **Inconsistent order.** Every set must be sorted by the same order $\prec$, with ties broken the same way; otherwise the positions in line L9 mean nothing, and the lemma of prefix filtering fails.
- **Processing order.** The indexing prefix is safe only because each set is probed against sets that are not larger. Probing in another order with the short indexing prefix misses answers.
- **Pruned and then found again.** Once line L10 prunes $y$, a later element of $x$ may meet $y$ again with a bound that passes, because the bound uses the stale count. Keep $y$ pruned for the rest of the probe of $x$.
- **Duplicates in the input.** The method works on sets. A multiset must first be turned into a set, for example by numbering the copies of each element.

## Implementations

## History

Chaudhuri, Ganti and Kaushik introduced prefix filtering for similarity joins in 2006, and Bayardo, Ma and Srikant added the shorter indexing prefix and the order by size in All-Pairs at WWW 2007. Chuan Xiao, Wei Wang, Xuemin Lin and Jeffrey Xu Yu presented PPJoin and PPJoin+ at WWW 2008 for the detection of near-duplicate Web pages, and an extended version, with Guoren Wang, appeared in ACM Transactions on Database Systems in 2011.

## References
