---
tag: A430AD
kind: algorithm
slug: simhash
name: SimHash
aliases:
- Charikar's simhash
area: searching/similarity-search
level: core
summary: Maps a weighted feature set to a bit fingerprint whose Hamming distance estimates angular similarity, used for near-duplicate detection.
model: word-ram
complexity:
  vars: {m: the number of distinct features, b: the number of fingerprint bits}
  time: {fingerprint: O(m b), compare: O(1)}
  space: {working: O(b), stored: O(b)}
properties: {deterministic: true, online: true}
history:
  year: 2002
  people: [Moses Charikar, Gurmeet Singh Manku, Arvind Jain, Anish Das Sarma]
  note: Charikar defined the sign-of-random-projection fingerprint in 2002; Manku, Jain and Das Sarma made the 64-bit weighted version the near-duplicate detector of a Web crawler in 2007.
prereqs: [random-hyperplane-lsh, cosine-similarity, hamming-distance]
see_also: [random-hyperplane-lsh, minhash, shingling, locality-sensitive-hashing, bit-sampling-lsh, hamming-distance, cosine-similarity]
sources:
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: pages 380 to 388 (Section 3, sketches from random hyperplanes, with collision probability 1 − θ/π for the angle θ between weight vectors)
  - paper: doi:10.1145/1242572.1242592
    title: Gurmeet Singh Manku, Arvind Jain and Anish Das Sarma, Detecting near-duplicates for web crawling, Proceedings of the 16th International World Wide Web Conference (WWW), 2007
    locator: pages 141 to 150 (Section 2, the weighted simhash of a document, and Section 3, the Hamming distance problem with permuted tables of 64-bit fingerprints and k = 3)
---

SimHash maps a document, given as a set of features with weights, to a fingerprint of $b$ bits, often 64. Every feature votes on every bit with its weight, in a direction set by a hash of the feature, and each bit of the fingerprint is the sign of the total vote. Two documents with similar weight vectors get fingerprints that differ in few bits. When the votes are independent standard Gaussians, each bit differs with probability exactly $\theta/\pi$, where $\theta$ is the angle between the two weight vectors, so the [Hamming distance](/hamming-distance/) of the fingerprints divided by $b$ estimates $\theta/\pi$. It is the [random hyperplane](/random-hyperplane-lsh/) family applied to sparse feature vectors, without storing the hyperplanes. Charikar defined it in 2002; Manku, Jain and Das Sarma used 64-bit SimHash fingerprints to detect near-duplicate pages in a Web crawl of billions of pages in 2007.

## In plain words

Break a document into features, such as its words or its [shingles](/shingling/), and give each feature a weight, such as how often it occurs. Keep a row of 64 counters, all zero. For each feature, compute a hash of 64 bits. Where a bit of the hash is 1, add the weight of the feature to that counter; where it is 0, subtract the weight. At the end, write 1 for every positive counter and 0 for the others. That is the fingerprint.

Two documents that share most of their heavy features push the counters the same way, so their fingerprints match in most places. Two unrelated documents push the counters at random, and about half of the places differ. To compare two documents, count the places where their fingerprints differ.

## The problem

A document is a finite set $F$ of features with positive weights $w(f)$; equivalently, a sparse vector $x \in \mathbb{R}^U$ over the universe $U$ of all features, with $x_f = w(f)$ for $f \in F$ and $0$ elsewhere. The similarity of two documents $x$ and $y$ is the angle $\theta(x, y) = \arccos\big(x \cdot y / (\lVert x \rVert\, \lVert y \rVert)\big)$, or its [cosine](/cosine-similarity/). The goal is a fingerprint of $b$ bits per document, computed from the document alone, such that the Hamming distance of two fingerprints estimates $\theta$, and such that near-duplicates, with a small angle, have fingerprints within a small Hamming distance.

## The algorithm

```pseudo id=main
SIMHASH(F, w, H, b)                        ▷ F features, w weights, H a hash from features to b bits
L1  V ← an array of b zeros
L2  for each feature f in F do
L3      s ← H(f)
L4      for i ← 1 to b do
L5          if s[i] = 1 then V[i] ← V[i] + w(f) else V[i] ← V[i] − w(f)
L6  for i ← 1 to b do fp[i] ← 1 if V[i] > 0, else 0
L7  return fp

DISTANCE(fp1, fp2)
L8  return the number of 1 bits of fp1 XOR fp2
```

Write $\sigma_i(f) = +1$ when bit $i$ of $H(f)$ is 1, and $-1$ otherwise. After line L5, $V[i] = \sum_{f \in F} w(f)\, \sigma_i(f) = x \cdot \sigma_i$, the dot product of the weight vector with the vector $\sigma_i$ of signs. So bit $i$ of the fingerprint is the side of the hyperplane orthogonal to $\sigma_i$ on which $x$ lies: SimHash is random hyperplane LSH with one hyperplane per bit, and the hash $H$ produces the coordinates of the $b$ hyperplanes on demand, so a universe of millions of features needs no stored matrix.

The **Gaussian variant** replaces $\sigma_i(f)$ by a value $g_i(f)$ derived from a hash of $(f, i)$ and distributed as $N(0, 1)$, and line L5 by $V[i] \leftarrow V[i] + w(f)\, g_i(f)$.

## Example

Take fingerprints of $b = 4$ bits and three documents with word weights: $A = \{$the: 1, cat: 3, sat: 1$\}$, $B = \{$the: 1, cat: 3, mat: 1$\}$ and $C = \{$dog: 2, ran: 1$\}$. Suppose the hash is

| feature | the | cat | sat | mat | dog | ran |
|---|---|---|---|---|---|---|
| $H(f)$ | 1010 | 0110 | 1100 | 0011 | 1001 | 0101 |

For $A$, bit 1 gets $+1$ from "the", $-3$ from "cat" and $+1$ from "sat", so $V[1] = -1$. In the same way $V = (-1, 3, 3, -5)$ for $A$, $V = (-3, 1, 5, -3)$ for $B$, and $V = (1, -1, -3, 3)$ for $C$. The fingerprints are $A = 0110$, $B = 0110$ and $C = 1001$.

| pair | cosine | angle in degrees | $1 - \theta/\pi$ | bits that agree |
|---|---|---|---|---|
| $A, B$ | $10/11 \approx 0.9091$ | 24.62 | 0.8632 | 4 of 4 |
| $A, C$ | 0 | 90 | 0.5 | 0 of 4 |

$A$ and $B$ differ in one light word, and their fingerprints are equal. $A$ and $C$ share no word; the expected agreement is half the bits, and here no bit agrees, a large deviation that four bits allow. With $b = 64$ the estimate is much tighter, as the bound below shows.

## Correctness

**Theorem.** Model the hash as random: for the Gaussian variant, the values $g_i(f)$, for all features $f$ and bits $i$, are independent $N(0, 1)$. Let $x$ and $y$ be nonzero weight vectors at angle $\theta$, and $D$ the Hamming distance of their fingerprints. Then each bit differs with probability exactly $\theta/\pi$, the bits are independent, $\mathbb{E}[D] = b\,\theta/\pi$, and for every $\varepsilon > 0$, $\Pr\big[\,|D/b - \theta/\pi| \ge \varepsilon\,\big] \le 2 e^{-2 b \varepsilon^2}$.

The first claim is the collision lemma of [random hyperplane LSH](/random-hyperplane-lsh/), applied to the vectors $x$ and $y$ restricted to the finite set of features of the two documents, with the hyperplane $(g_i(f))_f$; ties $V[i] = 0$ have probability 0. Different bits use disjoint sets of independent values, so they are independent, and the bound is the [Hoeffding inequality](/hoeffding-inequality/) for $b$ independent indicators. For $b = 64$ and $\varepsilon = 0.1$ the bound is $2e^{-1.28} \approx 0.556$; for $\varepsilon = 0.2$ it is $2e^{-5.12} \approx 0.0119$.

**The $\pm 1$ version.** With signs from the bits of $H$, modeled as independent fair coins, the bits of the fingerprint are still independent and each differs with the same probability $\delta(x, y)$, so $D/b$ still concentrates around $\delta$ by the same Hoeffding bound. But $\delta$ is in general not $\theta/\pi$. For $x = (1, 0, 0)$ and $y = (1, 1, 1)$, the angle is $\arccos(1/\sqrt{3}) \approx 54.74^\circ$, so $1 - \theta/\pi \approx 0.6959$; a bit agrees when $\sigma_1$ has the sign of the majority of $\sigma_1, \sigma_2, \sigma_3$, which has probability $3/4$. For documents with many features of comparable weight, the sum $x \cdot \sigma_i$ is close to Gaussian and $\delta$ is close to $\theta/\pi$; this is the version Manku, Jain and Das Sarma used. The full proof of both statements is below.

## Complexity

The model is the [word RAM](/word-ram/) with a hash of $b$ bits computed in $O(1)$ time per word of output, and $b$ at most the word size $w$.

- **Fingerprint.** Lines L2 to L5 do $b$ additions per feature: $O(mb)$ time for $m$ distinct features, and $O(b)$ space for the counters. Lines L6 and L7 take $O(b)$.
- **Compare.** Line L8 is one XOR and one population count: $O(1)$ time when $b \le w$, and $O(b/w)$ in general.
- **Storage.** $b$ bits per document, 8 bytes for $b = 64$, against the full feature set for an exact cosine.

## Properties

- **Deterministic.** For a fixed hash $H$ the fingerprint is a function of the weighted feature set; equal documents always get equal fingerprints. The randomness is in the analysis, which models $H$ as random.
- **Order independent.** The sums of line L5 do not depend on the order of the features.
- **Scale invariant.** Multiplying all weights by $c > 0$ multiplies $V$ by $c$ and does not change the fingerprint.
- **Online.** A fingerprint is computed from one document, in one pass over its features, without reference to other documents.
- **Weights matter.** A heavy feature can decide many bits on its own; changing a light feature rarely changes any bit. This is the difference from [MinHash](/minhash/), which treats all elements of a set alike.

## Variants and improvements

- **Search by Hamming distance.** Manku, Jain and Das Sarma look for all stored fingerprints within Hamming distance $k = 3$ of a query. If two 64-bit fingerprints differ in at most $k$ bits and the bits are split into $k + 1$ blocks, at least one block is equal in both, by the pigeonhole principle. Storing copies of the fingerprint table, each sorted with a different block first, turns the search into exact lookups on the leading bits.
- **LSH tables.** Taking $k$ of the $b$ bits as a key, in $L$ tables, gives the [LSH](/locality-sensitive-hashing/) index of [random hyperplane LSH](/random-hyperplane-lsh/) or of [bit sampling](/bit-sampling-lsh/) on the fingerprints.
- **Weights.** Term frequency, term frequency times inverse document frequency, or learned weights. Rare and frequent features can be dropped before line L2.
- **Features.** Words, word [shingles](/shingling/), character $n$-grams, or tokens of source code; Manku, Jain and Das Sarma use the features of a Web page with weights after removing HTML.

## When to use it

Use SimHash for near-duplicate detection in large collections, where a few bytes per document must suffice and the documents are weighted feature vectors: Web pages, news, emails, source files. Use [MinHash](/minhash/) when the similarity of interest is the [Jaccard similarity](/jaccard-similarity/) of unweighted sets, or when containment matters. Use [random hyperplane LSH](/random-hyperplane-lsh/) directly for dense vectors such as embeddings, where the coordinates exist and no hash is needed to produce the hyperplanes.

## Pitfalls

- **The $\pm 1$ estimate is biased.** Converting the Hamming distance to an angle by $\theta \approx \pi D/b$ is exact only in expectation for the Gaussian variant. With $\pm 1$ signs and few features, the error can be large, as in the example with three features above.
- **A weak hash.** If the bits of $H(f)$ are correlated across positions, for example from a linear congruential generator, the bits of the fingerprint are correlated and the Hoeffding bound fails. Use a well mixed 64-bit hash.
- **Ties.** With integer weights, $V[i] = 0$ happens with positive probability in the $\pm 1$ version. The rule of line L6 sends ties to 0; it must be the same for all documents.
- **Unnormalized features.** Without removal of markup, dates and boilerplate, two copies of a page differ in heavy features, such as a long navigation menu, that dominate the vote.
- **Short documents.** With few features, a single changed feature can flip many bits, so the threshold on the Hamming distance must depend on the length.

## Implementations

## History

Charikar presented the sketch based on random hyperplanes at STOC 2002, as an example of similarity estimation from the rounding scheme of Goemans and Williamson, and proved that the probability of a collision is $1 - \theta/\pi$. The name SimHash and the weighted form with signs from a hash of each feature come from its use in practice; Manku, Jain and Das Sarma described it at WWW 2007, with 64-bit fingerprints of 8 billion Web pages and the permuted-table search for fingerprints within Hamming distance 3.

## References
