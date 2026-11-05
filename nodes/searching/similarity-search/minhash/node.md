---
tag: 4BV5E4
kind: algorithm
slug: minhash
name: MinHash
aliases:
- min-wise hashing
area: searching/similarity-search
level: core
summary: Estimates Jaccard similarity by comparing the minimum hash values of sets under random permutations.
model: word-ram
complexity:
  vars: {n: the number of elements of the set, k: the number of hash functions}
  time: {worst: Θ(k n)}
  space: {extra: Θ(k)}
properties: {deterministic: false, online: true}
history:
  year: 1997
  people: [Andrei Broder]
  note: Broder estimated the resemblance of documents by the minimum of a random permutation of their shingle sets, for the AltaVista search engine, in 1997.
prereqs: [jaccard-similarity, shingling, hoeffding-inequality]
see_also: [jaccard-similarity, shingling, locality-sensitive-hashing, min-wise-independent-hashing, simhash, set-similarity-join, lsh-amplification, hyperloglog]
sources:
  - paper: doi:10.1109/SEQUEN.1997.666900
    title: Andrei Z. Broder, On the resemblance and containment of documents, Compression and Complexity of Sequences (SEQUENCES 1997)
    locator: pages 21 to 29 (the probability that the minima of a random permutation agree equals the resemblance, and the estimate from several permutations)
  - paper: doi:10.1006/jcss.1999.1690
    title: Andrei Z. Broder, Moses Charikar, Alan M. Frieze and Michael Mitzenmacher, Min-wise independent permutations, Journal of Computer and System Sciences 60(3), 2000
    locator: pages 630 to 659 (the definition of min-wise independent families, their size, and approximately min-wise families)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.3, Similarity-Preserving Summaries of Sets (minhashing, the signature matrix, computing signatures with hash functions) and Section 3.4, Locality-Sensitive Hashing for Documents (the banding technique)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4, Chernoff and Hoeffding Bounds (the Hoeffding bound for sums of independent bounded variables)
---

MinHash estimates the [Jaccard similarity](/jaccard-similarity/) $J(A, B) = |A \cap B| / |A \cup B|$ of two sets from short *signatures*: for each of $k$ random hash functions, a set keeps only the least hash value of its elements, and the fraction of the $k$ positions where two signatures agree is the estimate. Under truly random permutations the estimate is unbiased, and it is within $\varepsilon$ of $J$ with probability at least $1 - 2e^{-2k\varepsilon^2}$. Building a signature takes $\Theta(kn)$ time for a set of $n$ elements, and comparing two signatures takes $\Theta(k)$, independent of the set sizes. With [shingling](/shingling/) and the banding form of [locality-sensitive hashing](/locality-sensitive-hashing/), it finds near-duplicate documents among billions.

## In plain words

Put all possible elements in a random order, the same order for everyone. For a set, write down which of its elements comes first in that order. Do this for two sets. The element that comes first among all elements of both sets together is equally likely to be any of them. The two sets write down the same element exactly when that first element is in both sets. So the chance that they agree is the number of shared elements divided by the number of elements in either set, which is the Jaccard similarity.

One random order gives only a yes or no. Repeat with a hundred different random orders and count how often the two sets agree. The fraction is close to the true similarity. Each set is now a list of a hundred numbers, however large the set was, and two lists are quick to compare.

## The problem

The input is a finite set $A$ of elements of a universe $U$, and for comparison a second set $B$ with its own signature. The output is a signature $\mathrm{sig}(A) \in (\mathbb{Z} \cup \{\infty\})^k$, and for two signatures an estimate $\hat J$ of $J(A, B)$. The random choices are $k$ hash functions $h_1, \ldots, h_k : U \to \mathbb{Z}$, chosen once and shared by all sets. The analysis assumes that each $h_i$ is injective on $A \cup B$ and that its order on $A \cup B$ is a uniformly random order, independent for different $i$; a random permutation of $U$, or a [min-wise independent](/min-wise-independent-hashing/) family, gives this.

## The algorithm

```pseudo id=main
MINHASH-SIGNATURE(A, h1, ..., hk)          ▷ A is a finite set
L1  for i ← 1 to k do
L2      sig[i] ← ∞
L3      for each a in A do
L4          sig[i] ← min(sig[i], hi(a))
L5  return sig

ESTIMATE(sA, sB)                           ▷ two signatures of length k
L6  m ← 0
L7  for i ← 1 to k do
L8      if sA[i] = sB[i] then m ← m + 1
L9  return m / k
```

Lines L1 to L4 keep, for each hash function, the least value over the set. The order of the loops does not matter: one pass over the elements that updates all $k$ minima per element gives the same signature, and it is the form used on a stream. The empty set has the signature $(\infty, \ldots, \infty)$. Two empty sets then agree in all positions, which matches the convention $J(\emptyset, \emptyset) = 1$, and an empty and a nonempty set agree in none. ESTIMATE counts the agreeing positions.

## Example

Let $U = \{0, 1, \ldots, 6\}$, $A = \{0, 1, 2, 3\}$ and $B = \{2, 3, 4\}$, so $J(A, B) = 2/5 = 0.4$. Take $k = 6$ hash functions $h(x) = (ax + b) \bmod 7$; each is a permutation of $U$ because $a \ne 0$ and 7 is prime.

| $(a, b)$ | $h(0), \ldots, h(6)$ | $\min_A h$ | $\min_B h$ | agree |
|---|---|---|---|---|
| (1, 1) | 1 2 3 4 5 6 0 | 1 | 3 | no |
| (3, 1) | 1 4 0 3 6 2 5 | 0 | 0 | yes |
| (2, 5) | 5 0 2 4 6 1 3 | 0 | 2 | no |
| (5, 2) | 2 0 5 3 1 6 4 | 0 | 1 | no |
| (4, 3) | 3 0 4 1 5 2 6 | 0 | 1 | no |
| (6, 0) | 0 6 5 4 3 2 1 | 0 | 3 | no |

The signatures are $(1, 0, 0, 0, 0, 0)$ and $(3, 0, 2, 1, 1, 3)$, and the estimate is $1/6 \approx 0.1667$. Six functions are too few for a precise estimate: the standard deviation of $\hat J$ is $\sqrt{0.4 \times 0.6 / 6} = 0.2$. These linear functions are also far from random orders. Over all $7! = 5040$ permutations of $U$, exactly $2016$ give equal minima, and $2016 / 5040 = 0.4$.

With $k = 185$ truly random permutations, the bound below gives $|\hat J - J| < 0.1$ with probability at least $0.95$.

## Correctness

Let $u$ be the element of $A \cup B$ with the least value of $h_i$. By the assumption, $u$ is uniform on $A \cup B$. The minima of $A$ and $B$ agree exactly when $u \in A \cap B$: if $u$ is in both sets, it is the minimum of both; if it is in only one, that set has minimum $h_i(u)$ and the other set has a larger minimum, since $h_i$ is injective on $A \cup B$. So each position agrees with probability $J(A, B)$, the indicator variables $X_i$ of the positions are independent, and $\hat J = \frac1k \sum_i X_i$ has

$$\mathbb{E}[\hat J] = J(A, B), \qquad \operatorname{Var}[\hat J] = \frac{J(1 - J)}{k} \le \frac{1}{4k}, \qquad \Pr\big[|\hat J - J| \ge \varepsilon\big] \le 2 e^{-2k\varepsilon^2}$$

for each $\varepsilon > 0$, by the [Hoeffding inequality](/hoeffding-inequality/). So $k = \lceil \ln(2/\delta) / (2\varepsilon^2) \rceil$ functions give an additive error below $\varepsilon$ with failure probability at most $\delta$. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/), with a hash value in one word and $O(1)$ time per hash evaluation.

- **Signature.** Lines L1 to L4 evaluate each $h_i$ on each element: $kn$ evaluations and $kn$ comparisons, so $\Theta(kn)$ time in every case. The space is $\Theta(k)$ words besides the input, and the input can be a stream read once if the loops are swapped.
- **Estimate.** Lines L6 to L9 take $\Theta(k)$ time.
- **All pairs.** For $N$ sets, comparing all signatures takes $\Theta(N^2 k)$ time. Banding avoids most comparisons: split each signature into $b$ bands of $r$ rows, hash each band, and compare only sets that share a band bucket. Two sets of similarity $s$ become candidates with probability $1 - (1 - s^r)^b$. For $b = 20$ and $r = 5$ this is $0.0064$ at $s = 0.2$, $0.1860$ at $s = 0.4$, $0.8019$ at $s = 0.6$ and $0.9996$ at $s = 0.8$. The pages [locality-sensitive hashing](/locality-sensitive-hashing/) and [LSH amplification](/lsh-amplification/) derive this curve.

The number $k$ is set by the accuracy, not by $n$: an additive error $\varepsilon$ with confidence $1 - \delta$ needs $k = O(\varepsilon^{-2} \log(1/\delta))$, for example $k = 185$ for $\varepsilon = 0.1$ and $\delta = 0.05$, and $k = 738$ for $\varepsilon = 0.05$.

## Properties

- **Randomized.** The answer is an estimate; its error depends on $k$ and on the quality of the hash functions.
- **One pass.** Each element is read once, and the signature can be updated when an element is added. Removing an element is not supported, since the old minimum is lost.
- **Mergeable.** The signature of $A \cup B$ is the position-wise minimum of the two signatures.
- **Locality-sensitive.** One position of the signature is a hash function with $\Pr[h(A) = h(B)] = J(A, B)$, so it forms a [locality-sensitive hash family](/locality-sensitive-hash-family/) for the Jaccard distance.

## Variants and improvements

- **One permutation, bottom-$k$.** Use one hash function and keep the $k$ least values of the set. The estimate is the fraction of the $k$ least values of $A \cup B$ that lie in both sketches. It needs $n$ hash evaluations instead of $kn$.
- **One permutation hashing with bins.** Split the hash range into $k$ bins and keep the least value in each bin, with a rule to fill empty bins.
- **$b$-bit MinHash.** Store only the lowest $b$ bits of each minimum. Random agreements of the bits raise the agreement rate, and a corrected estimator removes this bias; many more positions then fit in the same memory.
- **Weighted MinHash.** For vectors with nonnegative weights, consistent weighted sampling makes the agreement probability equal to the weighted Jaccard similarity.
- **Min-wise independent families.** A family of permutations is min-wise independent when each element of each set is the minimum with equal probability. Broder, Charikar, Frieze and Mitzenmacher showed that exact families must be exponentially large, and studied approximate families that are small. See [min-wise independent hashing](/min-wise-independent-hashing/).

## When to use it

Use MinHash when the objects are sets, such as [shingle](/shingling/) sets of documents or sets of items per user, and the similarity is Jaccard. It turns sets of any size into fixed-size signatures, and with banding it finds similar pairs without comparing all of them. For cosine similarity of real vectors, use [SimHash](/simhash/) or [random hyperplane LSH](/random-hyperplane-lsh/). When an exact list of all pairs above a high threshold is needed, an exact [set similarity join](/set-similarity-join/) with [prefix filtering](/prefix-filtering/) can be faster and has no false negatives.

## Pitfalls

- **Weak hash functions.** The linear functions of the example have only $7 \times 6 = 42$ choices and are far from min-wise independent, and the estimate can be biased. Use a well-mixed 64-bit hash with an independent seed for each $i$ in line L4.
- **Collisions.** If $h_i$ maps two different elements of $A \cup B$ to the same value, two sets can agree without a shared minimum element. With $m = |A \cup B|$ and $b$-bit values, the chance is at most $\binom{m}{2} 2^{-b}$; use $b = 64$, or 32 only for small sets.
- **One function, many times.** Using the same $h$ in all $k$ positions gives $k$ copies of one indicator, and the error does not shrink. The $k$ functions must be independent.
- **Comparing sizes.** The estimate says nothing about the sizes of the sets; two sets of very different sizes can only have a small $J$. Containment needs the sizes as well: $|A \cap B| = J\,(|A| + |B|)/(1 + J)$.

## Implementations

## History

Andrei Broder introduced the estimate of resemblance by the minima of a random permutation in 1997, to find near-duplicate pages for the AltaVista search engine, and with Glassman, Manasse and Zweig applied it to cluster the Web in the same year. Broder, Charikar, Frieze and Mitzenmacher defined min-wise independent permutations and studied their size in a paper at STOC 1998, published in the Journal of Computer and System Sciences in 2000.

## References
