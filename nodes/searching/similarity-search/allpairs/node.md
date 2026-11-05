---
tag: 0NZTCD
kind: algorithm
slug: allpairs
name: AllPairs
aliases:
- All-Pairs algorithm
- Bayardo et al. all-pairs
area: searching/similarity-search
level: advanced
summary: Finds all similar pairs by indexing prefix tokens in an inverted index and verifying candidates.
solves: [all-pairs-similarity-search]
model: real-ram
complexity:
  vars: {n: the number of vectors, N: the total number of nonzero entries, C: the number of index entries scanned, Z: the number of candidate pairs verified, ℓ: the largest number of nonzero entries in a vector}
  time: {worst: O(N log N + C + Z ℓ), best: O(N log N)}
  space: {total: O(N)}
properties: {stable: false, in_place: false, adaptive: true, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2007
  people: [Roberto J. Bayardo, Yiming Ma, Ramakrishnan Srikant]
  note: Bayardo, Ma and Srikant gave All-Pairs at WWW 2007, which indexes only the part of each vector that can still reach the threshold, and showed large speedups over inverted-index joins and LSH on web-scale data.
prereqs: [all-pairs-similarity-search, inverted-index, prefix-filtering]
see_also: [ppjoin, set-similarity-join, cosine-similarity, jaccard-similarity, minhash, top-k-selection]
sources:
  - paper: doi:10.1145/1242572.1242591
    title: Roberto J. Bayardo, Yiming Ma and Ramakrishnan Srikant, Scaling up all pairs similarity search, Proceedings of the 16th International World Wide Web Conference (WWW), 2007
    locator: pages 131 to 140 (the All-Pairs algorithms, with the max-weight bound, the vector and dimension orders, and the size filter)
  - paper: doi:10.1109/ICDE.2006.9
    title: Surajit Chaudhuri, Venkatesh Ganti and Raghav Kaushik, A primitive operator for similarity joins in data cleaning, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006
    locator: the prefix filter for set-similarity joins, which All-Pairs extends to weighted vectors
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6 and Chapter 7 (cosine scoring with an inverted index and term-at-a-time accumulators)
---

All-Pairs is an exact algorithm for [all-pairs similarity search](/all-pairs-similarity-search/) with a dot-product threshold $t$ on sparse vectors with nonnegative weights, such as unit-length TF-IDF vectors under [cosine similarity](/cosine-similarity/). It processes the vectors one at a time; each new vector first finds its matches among the earlier ones through an [inverted index](/inverted-index/), and then adds to the index only the part of itself beyond the point where the remaining weights could reach $t$ against any vector. This extends [prefix filtering](/prefix-filtering/) from sets to weighted vectors. The output is exact: every pair with dot product at least $t$ is reported once. Bayardo, Ma and Srikant gave it in 2007.

## In plain words

Think of each item as a list of words with weights. A pair of items scores high only if they share words with large weights.

Look at the items one at a time. For a new item, first find the earlier items it shares an indexed word with, and compute their exact scores. Then add the new item to the index, but not all of its words. The first words of the item, taken in a fixed order, cannot reach the limit on their own, even against the heaviest possible partner. So any good match must also share one of the later words, and only the later words go into the index. This keeps the lists short.

## The problem

The input is a list $V = (x_1, \dots, x_n)$ of sparse vectors in $\mathbb{R}_{\ge 0}^d$ and a threshold $t > 0$. The output is the set of pairs $(j, i)$ with $j < i$ and $x_j \cdot x_i \ge t$, each with its dot product. For unit vectors this is the cosine similarity join of Bayardo, Ma and Srikant. Sets fit as 0/1 vectors scaled to unit length.

## The algorithm

Fix an order of the dimensions, with the most frequent dimensions first, and let $m[i] = \max_{y \in V} y[i]$. For a vector $y$, the *unindexed part* $y'$ holds the entries of $y$ that are not put into the index.

```pseudo id=main
ALL-PAIRS(V, t)
L1  order the dimensions by decreasing frequency; m[i] ← max over y ∈ V of y[i]
L2  O ← ∅; I_i ← an empty list for each dimension i
L3  for each x ∈ V in input order do
L4      O ← O ∪ FIND-MATCHES(x, I, t)
L5      b ← 0
L6      for each i with x[i] > 0, in the dimension order, do
L7          b ← b + m[i] · x[i]
L8          if b ≥ t then append (x, x[i]) to I_i else put x[i] into x'
L9  return O

FIND-MATCHES(x, I, t)
L10 A ← an empty map from vectors to scores
L11 for each i with x[i] > 0 and each (y, y[i]) ∈ I_i do A[y] ← A[y] + x[i] · y[i]
L12 for each y with A[y] > 0: s ← A[y] + x · y'; if s ≥ t then report (y, x, s)
L13 return the reported pairs
```

Line L4 runs before line L8 adds $x$ to the index, so $x$ is matched only against earlier vectors. Line L11 computes, for each earlier $y$, the dot product of $x$ with the indexed part of $y$; this is term-at-a-time scoring with accumulators. Line L12 adds the dot product with the unindexed part $y'$, which is stored with $y$, and so gets the exact score.

The bound $b$ in line L7 is the largest dot product the entries seen so far could have with any vector of $V$, since every vector $z$ has $z[i] \le m[i]$. The first entries, while $b < t$, cannot reach $t$ alone. Since $b$ only grows, $x'$ is a prefix of $x$ in the dimension order, and the indexed part is the suffix. With the most frequent dimensions first, the indexed suffixes fall in rare dimensions, and the lists $I_i$ stay short.

## Example

Take four unit vectors over the dimensions 0 to 3, with $t = 0.55$:

| vector | dim 0 | dim 1 | dim 2 | dim 3 |
|---|---|---|---|---|
| $x_0$ | 0.6 | 0.8 | | |
| $x_1$ | 0.8 | | 0.6 | |
| $x_2$ | 0.36 | 0.48 | | 0.8 |
| $x_3$ | | | 0.6 | 0.8 |
| $m$ | 0.8 | 0.8 | 0.6 | 0.8 |

Dimension 0 has 3 entries and the others 2, so the order is 0, 1, 2, 3.

- $x_0$: no matches. In dimension 0, $b = 0.8 \cdot 0.6 = 0.48 < 0.55$, so $0.6$ goes into $x_0'$. In dimension 1, $b = 1.12$, so $(x_0, 0.8)$ goes into $I_1$.
- $x_1$: its lists $I_0$ and $I_2$ are empty, so no matches. In dimension 0, $b = 0.64 \ge 0.55$, so both entries are indexed: $I_0 = [(x_1, 0.8)]$ and $I_2 = [(x_1, 0.6)]$.
- $x_2$: $A[x_1] = 0.36 \cdot 0.8 = 0.288$ from $I_0$ and $A[x_0] = 0.48 \cdot 0.8 = 0.384$ from $I_1$. Verify: $x_1' = \emptyset$, so $s = 0.288 < 0.55$; and $s = 0.384 + 0.36 \cdot 0.6 = 0.6 \ge 0.55$, so $(x_0, x_2, 0.6)$ is reported. Then $0.36$ goes into $x_2'$, and dimensions 1 and 3 are indexed.
- $x_3$: $A[x_1] = 0.36$ from $I_2$ and $A[x_2] = 0.64$ from $I_3$. The scores are $0.36$ and $0.64$, so $(x_2, x_3, 0.64)$ is reported.

The output is $\{(x_0, x_2), (x_2, x_3)\}$. The pairs $(x_0, x_1)$ at $0.48$ and $(x_0, x_3)$ at $0$ were never formed: $x_0$ is indexed only in dimension 1, which neither $x_1$ nor $x_3$ has. A full inverted-index join would also have scored $(x_0, x_1)$ through dimension 0.

## Correctness

Each reported pair has the exact dot product $s$ and passed $s \ge t$. The other direction rests on one bound.

**Lemma.** For each vector $y$ and each $z \in V$, $z \cdot y' < t$.

*Proof.* The entries of $y'$ are those processed while $b < t$, and $b$ at the last of them is $\sum_{i \in y'} m[i] \, y[i]$. Since all weights are nonnegative and $z[i] \le m[i]$, $z \cdot y' \le \sum_{i \in y'} m[i] \, y[i] < t$.

**Theorem.** ALL-PAIRS reports each pair $(y, x)$ with $y$ before $x$ and $x \cdot y \ge t$ exactly once, with $s = x \cdot y$, and reports no other pair.

If $x \cdot y \ge t$, then the indexed part $y'' = y - y'$ has $x \cdot y'' = x \cdot y - x \cdot y' > 0$ by the lemma. So some dimension $i$ has $x[i] > 0$ and $(y, y[i]) \in I_i$ when $x$ is processed, and line L11 makes $A[y] = x \cdot y'' > 0$. Line L12 then computes $s = x \cdot y$ and reports the pair. The map $A$ has one entry per $y$, so the pair is reported once. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/) with hash maps of $O(1)$ expected time per operation. Let $N$ be the total number of nonzero entries, $C$ the number of index entries scanned at line L11 over the whole run, $Z$ the number of pairs verified at line L12, and $\ell$ the largest number of nonzero entries of a vector.

- **Order and weights.** Counting frequencies and $m$ takes $O(N)$; sorting the dimensions and the entries of each vector takes $O(N \log N)$.
- **Matching.** Line L11 costs $O(C)$ over the run, and line L12 costs $O(\ell)$ per verified pair for the sparse dot product with $y'$. With the bound $Z \le C$ this is $O(N \log N + C + Z\ell)$ expected time.
- **Worst case.** If one heavy dimension is in every vector, every vector is indexed there, $C = \Theta(n^2)$, and the time is quadratic, even with few output pairs. No exact method avoids this in general: the R-S join form is as hard as orthogonal vectors (see [all-pairs similarity search](/all-pairs-similarity-search/)).
- **Space.** The index and the unindexed parts hold each entry once: $O(N)$, plus $O(n)$ for the accumulator.

## Properties

- **Exact.** No similar pair is missed, unlike [MinHash](/minhash/) banding.
- **Deterministic and one-pass.** Each vector is read once, matched, and indexed; the only global data are the frequencies and $m$.
- **Needs nonnegative weights and $t > 0$.** The lemma uses $z[i] \le m[i]$ and $y[i] \ge 0$; with negative weights the unindexed part can contribute more than the bound.
- **Adaptive.** The work depends on the data: skewed dimension frequencies, typical of text, keep $C$ far below $n^2$.

## Variants and improvements

- **A tighter weight bound.** Process the vectors in decreasing order of their largest weight $\max_i x[i]$, and use $\min(m[i], \max_j x[j])$ in place of $m[i]$; every later vector then has entries at most that value, so fewer entries need indexing.
- **Size filtering and remaining-score bounds.** For unit vectors, $x \cdot y \le \max(x) \cdot \|y\|_1 \le \max(x) \cdot |y|$, where $|y|$ is the number of entries. With the vectors in decreasing order of their largest weight, a vector with $|y| < t/\max(x)$ can never match $x$ or any later vector, so it is dropped from the lists for good, and the scan of a list can stop once the accumulated bound shows that no new candidate can pass $t$.
- **Sets.** For binary vectors this is [prefix filtering](/prefix-filtering/); [PPJoin](/ppjoin/) adds a position filter on the prefix tokens.
- **Distributed.** The index is split by dimension across machines, and the accumulators are merged.

## When to use it

Use All-Pairs when you need every pair above a high threshold, say $t \ge 0.7$, on sparse vectors with skewed frequencies, such as text, queries or user-item data. High thresholds keep the indexed suffixes short. For low thresholds or dense vectors, the filters prune little; then [MinHash](/minhash/) banding or [random hyperplane](/random-hyperplane-lsh/) LSH give approximate answers faster, or a nearest-neighbor index such as [HNSW](/hnsw/) gives the top pairs per vector.

## Pitfalls

- **Forgetting the unindexed part.** Line L12 must add $x \cdot y'$. Without it, scores are too low and pairs are lost.
- **Bounding with the wrong maximum.** $m[i]$ must bound the weights of all vectors that will be matched against the index, not only the earlier ones. With All-Pairs-1, the vector order is what makes the smaller bound valid.
- **Unnormalized input.** For cosine similarity, normalize the vectors first; the algorithm thresholds the raw dot product.
- **Floating-point ties.** Pairs with similarity very close to $t$ can flip with the order of summation; compare with a small tolerance if the output must match another method exactly.

## Implementations

## History

Chaudhuri, Ganti and Kaushik in 2006 used prefix filters for set-similarity joins in databases. Bayardo, Ma and Srikant in 2007 extended the idea to real-valued weights and the cosine similarity, with the max-weight bound, the order of vectors and the size filter, and showed that the exact method could beat LSH on large web data sets.

## References
