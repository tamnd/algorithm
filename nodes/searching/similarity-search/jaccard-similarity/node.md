---
tag: NWG4A9
kind: definition
slug: jaccard-similarity
name: Jaccard similarity
aliases:
- Jaccard coefficient
- Jaccard index
area: searching/similarity-search
level: intro
summary: The size of the intersection of two sets divided by the size of their union.
prereqs: [metric-space]
see_also: [minhash, shingling, cosine-similarity, set-similarity-join, all-pairs-similarity-search, prefix-filtering, hamming-distance, locality-sensitive-hash-family]
sources:
  - paper: doi:10.1111/j.1469-8137.1912.tb05611.x
    title: Paul Jaccard, The distribution of the flora in the alpine zone, New Phytologist 11(2), 1912
    locator: pages 37 to 50 (the coefficient of community of two floras)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.1.1 Jaccard Similarity of Sets, Section 3.3.3 Minhashing and Jaccard Similarity, and Section 3.5.3 Jaccard Distance
  - paper: doi:10.1109/SEQUEN.1997.666900
    title: Andrei Z. Broder, On the resemblance and containment of documents, Compression and Complexity of Sequences (SEQUENCES 1997)
    locator: pages 21 to 29 (resemblance as the Jaccard coefficient of the shingle sets, and its estimate by the minimum of a random permutation)
---

The Jaccard similarity of two finite sets is the number of elements they share divided by the number of elements in their union. It is 1 for equal sets and 0 for disjoint sets, and one minus it is a [metric](/metric-space/). It is the standard similarity of sets of words, of [shingles](/shingling/) of documents and of items bought by users, and [MinHash](/minhash/) estimates it from short signatures.

## Definition

Let $A$ and $B$ be finite sets. The **Jaccard similarity** of $A$ and $B$ is

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|} \quad \text{if } A \cup B \ne \emptyset, \qquad J(\emptyset, \emptyset) = 1.$$

So $0 \le J(A, B) \le 1$. The value is $1$ if and only if $A = B$, and $0$ if and only if $A$ and $B$ are disjoint and not both empty. The **Jaccard distance** is $d_J(A, B) = 1 - J(A, B) = |A \mathbin{\triangle} B| / |A \cup B|$, where $\triangle$ is the symmetric difference.

**Sets as bit vectors.** Fix a universe $U = \{u_1, \ldots, u_d\}$ and write a set $A \subseteq U$ as the vector $a \in \{0, 1\}^d$ with $a_i = 1$ if and only if $u_i \in A$. Then $|A \cap B| = a \cdot b$ and $|A \cup B| = |a| + |b| - a \cdot b$, where $|a|$ is the number of ones. In chemistry this form is the **Tanimoto coefficient**.

**Weighted Jaccard.** For $x, y \in \mathbb{R}_{\ge 0}^d$, not both zero, $J_w(x, y) = \sum_i \min(x_i, y_i) / \sum_i \max(x_i, y_i)$. It equals $J$ on 0/1 vectors.

### The MinHash property

Let $\pi$ be a uniformly random ordering of a finite universe $U$, and for a nonempty $S \subseteq U$ let $m_\pi(S)$ be the element of $S$ that comes first in $\pi$.

**Lemma.** For nonempty $A, B \subseteq U$, $\Pr[m_\pi(A) = m_\pi(B)] = J(A, B)$.

*Proof.* Let $u = m_\pi(A \cup B)$. Each element of $A \cup B$ comes first among the elements of $A \cup B$ with the same probability, so $u$ is uniform on $A \cup B$. If $u \in A \cap B$, then $u$ comes first in $A$ and in $B$, so $m_\pi(A) = m_\pi(B) = u$. If $u \in A \setminus B$, then $m_\pi(A) = u$ and $m_\pi(B) \ne u$ because $u \notin B$; the case $u \in B \setminus A$ is the same. So the two minima are equal exactly when $u \in A \cap B$, which has probability $|A \cap B| / |A \cup B|$. $\square$

This lemma is the base of [MinHash](/minhash/), and it makes the family $\{m_\pi\}$ a [locality-sensitive hash family](/locality-sensitive-hash-family/) for $d_J$.

### The Jaccard distance is a metric

**Theorem.** $d_J$ is a metric on the finite subsets of a set.

*Proof.* The definition is symmetric in $A$ and $B$, and $d_J(A, B) = 0$ if and only if $J(A, B) = 1$, that is $A = B$. For the triangle inequality $d_J(A, C) \le d_J(A, B) + d_J(B, C)$, first let $A$, $B$ and $C$ be nonempty, and take $U = A \cup B \cup C$. By the lemma, $d_J(X, Y) = \Pr[m_\pi(X) \ne m_\pi(Y)]$ for each two of the three sets. If $m_\pi(A) \ne m_\pi(C)$, then $m_\pi(A) \ne m_\pi(B)$ or $m_\pi(B) \ne m_\pi(C)$. The [union bound](/union-bound/) gives the inequality. Distances that involve an empty set are 0 or 1. If $A$ and $C$ are both empty, $d_J(A, C) = 0$. If exactly one of them is empty, $d_J(A, C) = 1$, and $B$ differs in emptiness from $A$ or from $C$, so $d_J(A, B) = 1$ or $d_J(B, C) = 1$. If $A$ and $C$ are nonempty and $B$ is empty, the right side is $2 \ge d_J(A, C)$. $\blacksquare$

## Examples and non-examples

**Two small sets.** $A = \{a, b, c, d\}$ and $B = \{c, d, e\}$ have $A \cap B = \{c, d\}$ and $A \cup B = \{a, b, c, d, e\}$, so $J(A, B) = 2/5 = 0.4$ and $d_J(A, B) = 0.6$. Of the $5! = 120$ orderings of $\{a, b, c, d, e\}$, exactly 48 put $c$ or $d$ first, and $48/120 = 0.4$, as the lemma says.

**Shingles of two words.** The 2-shingles of "banana" are $\{an, ba, na\}$, and those of "bandana" are $\{an, ba, da, na, nd\}$. They share 3 shingles out of 5, so $J = 0.6$.

**Weighted.** For $x = (3, 0, 1, 2)$ and $y = (1, 1, 0, 2)$, $\sum \min = 3$ and $\sum \max = 7$, so $J_w(x, y) = 3/7 \approx 0.4286$.

**Non-example: the Dice coefficient.** $D(A, B) = 2|A \cap B| / (|A| + |B|) = 2J/(1 + J)$ gives the same order of pairs as $J$, so a threshold on one is a threshold on the other. But $1 - D$ is not a metric. With $X = \{1\}$, $Y = \{1, 2\}$ and $Z = \{2\}$, $1 - D(X, Z) = 1$, and $(1 - D(X, Y)) + (1 - D(Y, Z)) = 2/3$.

**Non-example: the overlap coefficient.** $|A \cap B| / \min(|A|, |B|)$ is $2/3$ for the sets $A$ and $B$ above. It is 1 whenever one set holds the other, so it measures containment, not similarity.

## Related definitions

- **[MinHash](/minhash/)**: $k$ independent minima give $k$ values whose rate of agreement estimates $J$ with standard error at most $1/(2\sqrt k)$.
- **[Shingling](/shingling/)**: turn a document into the set of its substrings of length $w$, then compare the sets by $J$.
- **[Cosine similarity](/cosine-similarity/)**: on 0/1 vectors it is $|A \cap B| / \sqrt{|A|\,|B|}$. It is at least $J(A, B)$, since $\sqrt{|A|\,|B|} \le (|A| + |B|)/2 \le \max(|A|, |B|) \le |A \cup B|$.
- **[Hamming distance](/hamming-distance/)**: on bit vectors it is $|A \mathbin{\triangle} B|$, the numerator of $d_J$, without the scaling by $|A \cup B|$.
- **[Set similarity join](/set-similarity-join/)** and **[all-pairs similarity search](/all-pairs-similarity-search/)**: find all pairs of sets with $J \ge t$. The [prefix filter](/prefix-filtering/) uses the fact that $J(A, B) \ge t$ implies $|A \cap B| \ge t\,|A \cup B| \ge t \max(|A|, |B|)$, so $|A \cap B| \ge \lceil t\,|A| \rceil$.

## References
