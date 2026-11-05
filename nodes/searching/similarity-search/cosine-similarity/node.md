---
tag: 9PWYRN
kind: definition
slug: cosine-similarity
name: Cosine similarity
aliases:
- cosine measure
- angular similarity
area: searching/similarity-search
level: intro
summary: The cosine of the angle between two vectors, equal to their normalized inner product.
prereqs: [dot-product, euclidean-distance]
see_also: [jaccard-similarity, random-hyperplane-lsh, simhash, maximum-inner-product-search, all-pairs-similarity-search, k-nearest-neighbor-search, metric-space]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6, Section 6.3 The vector space model for scoring, Section 6.3.1 Dot products (cosine similarity of two document vectors, and length normalization)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.5.4 Cosine Distance (the angle as a distance measure and its triangle inequality) and Section 3.7.2 Random Hyperplanes and the Cosine Distance
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: Section 3 (the random hyperplane hash, with collision probability 1 − θ/π)
---

Cosine similarity measures how close two nonzero vectors are in direction: it is the [dot product](/dot-product/) of the two vectors divided by the product of their lengths, which is the cosine of the angle between them. It ignores the lengths of the vectors, so a long document and a short one about the same words are similar. It is the standard similarity of the vector space model of information retrieval, of text and image embeddings, and of [k-nearest neighbor search](/k-nearest-neighbor-search/) over such data.

## Definition

Let $x, y \in \mathbb{R}^d$ with $x \ne 0$ and $y \ne 0$, and let $\|x\| = \sqrt{x \cdot x}$ be the [Euclidean](/euclidean-distance/) length. The **cosine similarity** of $x$ and $y$ is

$$\cos(x, y) = \frac{x \cdot y}{\|x\|\,\|y\|} = \frac{\sum_{i=1}^{d} x_i y_i}{\sqrt{\sum_{i=1}^{d} x_i^2}\,\sqrt{\sum_{i=1}^{d} y_i^2}}.$$

It is not defined when $x = 0$ or $y = 0$.

**Range.** By the Cauchy-Schwarz inequality $|x \cdot y| \le \|x\|\,\|y\|$, so $-1 \le \cos(x, y) \le 1$. The value is $1$ if and only if $y = \lambda x$ for some $\lambda > 0$, and $-1$ if and only if $y = \lambda x$ for some $\lambda < 0$. If all coordinates of $x$ and $y$ are non-negative, as for counts of words, then $x \cdot y \ge 0$ and the range is $[0, 1]$.

**The angle.** The **angular distance** is $\theta(x, y) = \arccos \cos(x, y) \in [0, \pi]$. On the unit sphere it is the great-circle distance, and it is a [metric](/metric-space/): it satisfies the [triangle inequality](/triangle-inequality/).

**Relation to the Euclidean distance.** Let $\hat x = x / \|x\|$ and $\hat y = y / \|y\|$. Then

$$\|\hat x - \hat y\|^2 = \hat x \cdot \hat x - 2\, \hat x \cdot \hat y + \hat y \cdot \hat y = 2 - 2 \cos(x, y).$$

So on vectors scaled to length 1, the order by decreasing cosine similarity is the order by increasing Euclidean distance. A nearest neighbor index for the Euclidean distance answers cosine queries after this [normalization](/normalization/), and the [maximum inner product search](/maximum-inner-product-search/) on unit vectors is the same problem.

**Invariance.** For $\lambda, \mu > 0$, $\cos(\lambda x, \mu y) = \cos(x, y)$, because the factor $\lambda \mu$ cancels. Cosine similarity is not invariant under translation: in general $\cos(x + v, y + v) \ne \cos(x, y)$.

## Examples and non-examples

**Two documents.** Count four words in two documents: $x = (3, 0, 1, 2)$ and $y = (1, 1, 0, 2)$. Then $x \cdot y = 3 + 0 + 0 + 4 = 7$, $\|x\|^2 = 14$ and $\|y\|^2 = 6$, so

$$\cos(x, y) = \frac{7}{\sqrt{14}\,\sqrt{6}} = \frac{7}{\sqrt{84}} \approx 0.7638,$$

and the angle is about $40.20$ degrees. After normalization, $\|\hat x - \hat y\|^2 = 2 - 2 \cdot 0.7638 \approx 0.4725$.

**Scale.** The document $z = 2x = (6, 0, 2, 4)$ is $x$ written twice. It has $\cos(z, y) \approx 0.7638$, the same value as $x$. The dot product changes from 7 to 14, so a raw dot product prefers long documents and cosine similarity does not.

**Shift.** Add 10 to each count: $x + 10 = (13, 10, 11, 12)$ and $y + 10 = (11, 11, 10, 12)$. Their cosine similarity is about $0.9952$. A large common offset makes all vectors point in almost the same direction. The **Pearson correlation** of $x$ and $y$ is the cosine similarity of the centered vectors $x - \bar x \mathbf{1}$ and $y - \bar y \mathbf{1}$, and it is about $0.3162$ here. It is invariant under a shift.

**Non-example: one minus cosine is not a metric.** Many libraries call $1 - \cos(x, y)$ the cosine distance. It fails the triangle inequality. Take $x = (1, 0)$, $y = (1, 1)$ and $z = (0, 1)$. Then $1 - \cos(x, z) = 1$, but $(1 - \cos(x, y)) + (1 - \cos(y, z)) = 2 (1 - 1/\sqrt 2) \approx 0.5858 < 1$. So a [metric tree](/metric-space-indexing/) that prunes by the triangle inequality can lose answers if it uses $1 - \cos$. The angle $\theta$ and the distance $\|\hat x - \hat y\| = \sqrt{2 - 2\cos}$ are metrics and are safe.

**Non-example: the zero vector.** An empty document has the vector $0$, and $\cos(0, y)$ is $0/0$. Code must treat it apart, for example by giving it similarity 0 to each vector.

## Related definitions

- **[Dot product](/dot-product/)** $x \cdot y$: the unnormalized inner product. On unit vectors it equals the cosine similarity.
- **[Jaccard similarity](/jaccard-similarity/)** $|A \cap B| / |A \cup B|$: the similarity of sets. For 0/1 vectors $a, b$ of sets $A, B$, the cosine similarity is $|A \cap B| / \sqrt{|A|\,|B|}$, the Ochiai coefficient.
- **[Random hyperplane LSH](/random-hyperplane-lsh/)** and **[SimHash](/simhash/)**: a random $r$ with Gaussian coordinates gives the bit $\mathrm{sign}(r \cdot x)$, and two vectors get the same bit with probability $1 - \theta(x, y)/\pi$. This is the [locality-sensitive hash family](/locality-sensitive-hash-family/) for the angle.
- **[Maximum inner product search](/maximum-inner-product-search/)**: find the stored vector of the largest dot product with the query. It is the same as cosine search only when the stored vectors have equal lengths.
- **[All-pairs similarity search](/all-pairs-similarity-search/)**: find all pairs whose cosine similarity is at least a threshold.

## References
