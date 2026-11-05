---
tag: TVZ64D
kind: algorithm
slug: lsh-forest
name: LSH forest
area: searching/similarity-search
level: research
summary: Stores LSH hash prefixes in prefix trees so the number of hash functions need not be fixed in advance.
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, K: the maximum label length, l: the number of trees, C: the number of candidates}
  time: {build: O(l n K (d + log n)), query: O(l K (d + K log n) + C d)}
  space: {index: Θ(l n K + l K d)}
properties: {deterministic: false, online: false}
history:
  year: 2005
  people: [Mayank Bawa, Tyson Condie, Prasanna Ganesan]
  note: Bawa, Condie and Ganesan proposed storing variable-length LSH labels in prefix trees and descending them synchronously at WWW 2005.
prereqs: [locality-sensitive-hashing, random-hyperplane-lsh, trie]
see_also: [locality-sensitive-hashing, random-hyperplane-lsh, multi-probe-lsh, lsh-amplification, bit-sampling-lsh, e2lsh, trie, approximate-nearest-neighbor]
sources:
  - paper: doi:10.1145/1060745.1060840
    title: Mayank Bawa, Tyson Condie and Prasanna Ganesan, LSH forest, self-tuning indexes for similarity search, Proceedings of the 14th International World Wide Web Conference (WWW 2005)
    locator: pages 651 to 660 (the prefix trees of variable-length labels, the synchronous descent of the l trees, the choice of the number of candidates, and the comparison with LSH tuned for one key length)
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th Annual ACM Symposium on Theory of Computing (STOC 2002)
    locator: pages 380 to 388 (the random hyperplane hash, whose collision probability is 1 − θ/π)
  - paper: "Alexandr Andoni, Ilya Razenshteyn and Negev Shekel Nosatzki, LSH forest, practical algorithms made theoretical, Proceedings of the 28th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2017)"
    locator: pages 67 to 78 (an analysis of variants of the LSH forest for the Hamming distance, with query exponents that match standard LSH)
---

An LSH forest is a [locality-sensitive hashing](/locality-sensitive-hashing/) index in which the key length is not fixed. Each of $l$ trees gives every point a long label of $K$ hash bits, here [random hyperplane](/random-hyperplane-lsh/) bits, and stores the labels in a [trie](/trie/), or equivalently in sorted order. A query computes its own labels and descends all trees together: it starts at the deepest level where some point shares the query's prefix in some tree, and moves up one level at a time until the points that share a prefix of the current length, in some tree, number at least a target $M$. Then it ranks these candidates by their true distance. So the effective key length adapts to each query and to the local density of the data, instead of being tuned once for a fixed radius as in standard LSH. Bawa, Condie and Ganesan proposed it in 2005. Its guarantees reduce to those of LSH with any key length that the descent reaches.

## In plain words

Standard LSH gives each point a short code made of a fixed number of random bits, and only points with exactly the query's code are checked. Too many bits, and near points are missed. Too few, and far points crowd in. The right number depends on how dense the data is around the query, which is different for every query.

An LSH forest gives each point a long code and keeps the codes sorted, so it can ask how many leading bits each point shares with the query. It starts with the points that share the most bits. If there are not enough of them, it accepts points that share one bit fewer, and so on, until it has enough candidates. Several independent codes, the trees, are searched together, so a near point missed by one tree is likely found by another.

## The problem

Given $n$ points in $\mathbb{R}^d$ and a query $q$, find points of small angle $\theta(p, q)$ to $q$: the angular [approximate nearest neighbor](/approximate-nearest-neighbor/) problem. The same index works for any LSH family with labels made of independent hash values, such as [bit sampling](/bit-sampling-lsh/) for the Hamming distance. The goal is an index whose key length need not be chosen in advance for one radius.

## The algorithm

For tree $i$, draw $K$ independent standard Gaussian vectors $r_{i,1}, \ldots, r_{i,K}$, and label a vector $v$ by $\lambda_i(v) = (b_{i,1}(v), \ldots, b_{i,K}(v))$ with $b_{i,j}(v) = 1$ if $r_{i,j} \cdot v \ge 0$ and 0 otherwise. Two points *share depth $x$ in tree $i$* if their labels agree on the first $x$ bits. Let

$$C_x = \{\, p \in P : p \text{ shares depth } x \text{ with } q \text{ in some tree} \,\}.$$

Then $C_0 = P \supseteq C_1 \supseteq \cdots \supseteq C_K$. The query returns the $k$ best of $C_{x^*}$, where $x^*$ is the largest $x$ with $|C_x| \ge \min(M, n)$.

```pseudo id=main
BUILD(P, K, l)
L1  for i ← 1 to l do draw K Gaussian vectors r[i][1..K]
L2      for each p in P do compute the label λ_i(p) of K bits
L3      store the points of P in tree i, sorted by λ_i(p)          ▷ a trie, or a sorted array

QUERY(q, k, M)
L4  x ← the largest depth that q shares with some point in some tree
L5  repeat
L6      C ← the union over i of the points that share depth x with q in tree i
L7      if |C| ≥ min(M, n) or x = 0 then exit the loop
L8      x ← x − 1
L9  return the k points of C of smallest angle to q
```

In a sorted array, the points whose labels begin with a given prefix form a contiguous range, found by two [binary searches](/binary-search/); in a trie it is a subtree. Line L4 finds, in each tree, the longest common prefix of $\lambda_i(q)$ with the labels just before and after its position in sorted order, which are the labels sharing the most leading bits with it. Line L6 forms $C_x$; since $C_x$ grows as $x$ decreases, the loop stops at $x^*$. Bawa et al. take $M = c \cdot l$ for a small constant $c$, so that each tree contributes a few candidates.

## Example

In the plane, take $K = 3$, $l = 2$, and, to keep the arithmetic readable, the fixed directions $r_1 = ((1, 0), (0, 1), (1, 1))$ for tree 1 and $r_2 = ((1, -1), (0, 1), (-1, 2))$ for tree 2. The points are $a = (4, 1)$, $b = (3, 2)$, $c = (1, 3)$, $d = (-2, 3)$, $e = (-3, -1)$, $f = (1, -3)$, $g = (4, -1)$.

| point | angle to $q$ | label in tree 1 | label in tree 2 |
|---|---|---|---|
| a | 12.53° | 111 | 110 |
| b | 7.13° | 111 | 111 |
| c | 45° | 111 | 011 |
| d | 97.13° | 011 | 011 |
| e | 171.87° | 000 | 001 |
| f | 98.13° | 100 | 100 |
| g | 40.60° | 101 | 100 |

The query $q = (2, 1)$ has label 111 in both trees. Line L4 finds depth 3, shared with $a$, $b$, $c$ in tree 1 and $b$ in tree 2, so $C_3 = \{a, b, c\}$. With $M = 2$ the loop stops at once, and the answer for $k = 1$ is $b$, the true nearest. With $M = 4$, depth 2 gives the same three points (prefix 11 in tree 1, and $a$, $b$ in tree 2), so the descent goes on to depth 1, where $C_1 = \{a, b, c, f, g\}$. With $M = 6$ it ends at depth 0 with all seven points, an exact scan. Tree 1 alone puts $c$, at 45°, with the query at full depth while $g$, at 40.60°, differs at the second bit: single trees err, and the union over trees and the adaptive depth compensate.

## Correctness

The proof of the following is in [the correctness proof](proofs/correctness.md). Write $s(\theta) = 1 - \theta/\pi$ for the probability that one random hyperplane bit agrees on two vectors at angle $\theta$.

1. **The candidates.** QUERY computes $x^* = \max\{x : |C_x| \ge \min(M, n)\}$ and $C = C_{x^*}$, and returns the $\min(k, |C|)$ points of $C$ of smallest angle to $q$. If $M \ge n$, the answer is exact.
2. **Comparison with fixed-length LSH.** For every depth $k_0$ with $x^* \le k_0$, the candidates include those of a standard LSH index with $l$ tables and keys of length $k_0$, the first $k_0$ bits of each label.
3. **Success probability.** For a point $p$ at angle $\theta$ to $q$ and any depth $k_0 \le K$, over the random directions,
$$\Pr[p \notin C] \le (1 - s(\theta)^{k_0})^l + \Pr[x^* > k_0] \le (1 - s(\theta)^{k_0})^l + \frac{\mathbb{E}\,|C_{k_0 + 1}|}{\min(M, n)},$$
with $C_{K+1} = \emptyset$. So if, at the depth $k_0$ that standard LSH would use, few points share depth $k_0 + 1$ with $q$, the forest finds $p$ with the probability that LSH with key length $k_0$ guarantees, $1 - (1 - s(\theta)^{k_0})^l$, up to the second term, and without knowing $k_0$.

For example, if all points other than $p$ are at angle at least $\theta_2$ to $q$, then $\mathbb{E}|C_{k_0 + 1}| \le 1 + l(n - 1) s(\theta_2)^{k_0 + 1}$ by a union bound over trees, which is at most $1 + l$ for $k_0 = \lceil \log_{1/s(\theta_2)} n \rceil$, the key length of the [random hyperplane LSH](/random-hyperplane-lsh/) page. With $M = 4(l + 1)$ and $n \ge M$ the second term is then at most $1/4$.

## Complexity

In the real RAM, counting $O(d)$ for one inner product:

- **Build.** $lnK$ hash bits, $O(lnKd)$ time, and the sort of $n$ labels of $K$ bits per tree, $O(nK \log n)$ comparisons of bits each. Space $\Theta(lnK)$ bits for the labels, or a trie of $O(nK)$ nodes per tree, plus $\Theta(lKd)$ numbers for the directions.
- **Query.** $lK$ hash bits, $O(lKd)$. Line L4 costs $O(K \log n)$ per tree. Each round of lines L6 and L7 costs two binary searches per tree, $O(K \log n)$ each, and at most $K + 1$ rounds run, so $O(lK^2 \log n)$ in the worst case; a trie with sizes stored in its nodes lowers this to $O(lK)$ by walking up from the deepest node. Then $O(Cd)$ to rank the $C = |C_{x^*}|$ candidates.

So the worst case is $O(lK(d + K \log n) + Cd)$, with $C$ up to $n$; the candidate count $C$ is at least $\min(M, n)$ and, at the level just below $x^*$, fewer than $M$ points had been found, so $C$ is usually close to $M$ unless one level adds many points at once.

## Properties

- **Randomized.** The directions are random; given them, the query is deterministic.
- **Self-tuning.** The key length adapts to each query, and one index serves queries of different radii and regions of different density.
- **Monotone in $M$.** A larger $M$ gives a superset of candidates, never a worse answer, and $M \ge n$ gives the exact answer.
- **Dynamic.** Points can be inserted and deleted in the tries, unlike the fixed parameters of standard LSH, which must be retuned when $n$ changes.

## Variants and improvements

- **Tries with compressed paths.** Store each label only up to the first bit that distinguishes it from all other labels, as in a Patricia trie, so the space is $O(n)$ nodes per tree regardless of $K$.
- **Other families.** Use [bit sampling](/bit-sampling-lsh/) for the Hamming distance, or [p-stable](/e2lsh/) hash values compared one coordinate at a time for the Euclidean distance; any label made of independent hash values works.
- **Theory.** Andoni, Razenshteyn and Shekel Nosatzki analyze variants of the forest for the Hamming distance and show query exponents that match those of standard LSH.
- **[Multi-probe LSH](/multi-probe-lsh/).** Another way to reduce the number of tables, by probing nearby buckets of fixed-length keys instead of shortening the keys.

## When to use it

Use an LSH forest when queries differ widely in the distance of their nearest neighbors, when the data has regions of very different density, or when points are inserted over time and retuning a standard LSH index is impractical. For static data at large scale, graph indexes such as [HNSW](/hnsw/) usually give a higher recall for the same time.

## Pitfalls

- **Too small a $K$.** The adaptivity works only below depth $K$; if $K$ is less than the key length that LSH would need, the descent starts too shallow and returns many far points.
- **Too small a $M$.** A candidate count that is reached at a deep level by points of one tree alone, which share a long prefix by chance, can stop the descent before the near point appears in any tree. Take $M$ proportional to $l$.
- **One big level.** Moving up one level can double the candidates of a tree, so $|C|$ can far exceed $M$. Cap the candidates by taking the deeper ones first if time matters.
- **Degenerate directions.** Fixed or correlated directions, as in the example, break the independence that the bound assumes; draw them at random.
- **Zero vectors.** The angle to a zero vector is undefined; give it a fixed convention or drop it.

## Implementations

## History

Charikar defined the random hyperplane hash in 2002. Mayank Bawa, Tyson Condie and Prasanna Ganesan proposed the LSH forest at WWW 2005, to remove the tuning of the key length of LSH for data whose density varies, with an index that also supports insertions and deletions. Andoni, Razenshteyn and Shekel Nosatzki revisited it in 2017 and gave a theoretical analysis of variants.

## References
