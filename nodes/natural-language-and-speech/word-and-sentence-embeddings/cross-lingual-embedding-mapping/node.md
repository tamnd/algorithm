---
tag: CP9A01
kind: algorithm
slug: cross-lingual-embedding-mapping
name: Cross-lingual embedding mapping
aliases:
- bilingual embedding mapping
- orthogonal Procrustes mapping
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Learn a linear, often orthogonal, map from the embedding space of one language to another from a seed dictionary, solved in closed form by SVD.
model: real-ram
complexity:
  vars: {n: "the number of word pairs in the seed dictionary", d: "the dimension of the vectors"}
  time: {worst: "O(n d^2 + d^3)"}
  space: {extra: "O(d^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2013
  people: [Tomas Mikolov, Quoc V. Le, Ilya Sutskever]
  note: "Mikolov, Le and Sutskever showed in 2013 that a linear map fitted on a few thousand translation pairs carries word vectors of one language to another. Xing, Wang, Liu and Lin added unit-length vectors and an orthogonal map in 2015, which turns the fit into the orthogonal Procrustes problem that Schönemann had solved in 1966."
prereqs: [word-embedding, singular-value-decomposition]
see_also: [cross-domain-similarity-local-scaling, kabsch-algorithm, optimal-superposition, ordinary-least-squares, cosine-similarity, hubness, k-nearest-neighbor-search, word-analogy]
sources:
  - paper: "Tomas Mikolov, Quoc V. Le and Ilya Sutskever, Exploiting similarities among languages for machine translation, arXiv:1309.4168, 2013 (preprint)"
    title: Mikolov, Le and Sutskever 2013
    locator: the linear map between the two vector spaces, fitted by least squares on a seed dictionary of frequent words, and translation by the nearest neighbour of the mapped vector
  - paper: "Chao Xing, Dong Wang, Chao Liu and Yiye Lin, Normalized word embedding and orthogonal transform for bilingual word translation, Proceedings of NAACL-HLT 2015, pages 1006 to 1011"
    title: Xing, Wang, Liu and Lin 2015
    locator: the unit-length normalization of the vectors and the orthogonal constraint on the map
  - paper: "Peter H. Schönemann, A generalized solution of the orthogonal Procrustes problem, Psychometrika 31(1), 1966, pages 1 to 10"
    title: Schönemann 1966
    locator: the solution of the orthogonal Procrustes problem from the singular value decomposition
  - paper: "Alexis Conneau, Guillaume Lample, Marc'Aurelio Ranzato, Ludovic Denoyer and Hervé Jégou, Word translation without parallel data, ICLR 2018, arXiv:1710.04087"
    title: Conneau, Lample, Ranzato, Denoyer and Jégou 2018
    locator: "Section 2 (equation 1, the linear map; equation 2, the Procrustes solution U V^T from the SVD of Y X^T; the refinement that alternates a new dictionary and Procrustes), Section 3.4 (the dictionary of mutual nearest neighbours under CSLS), Table 1 (the Procrustes baseline on 5,000 source words, with nearest neighbour and with CSLS retrieval)"
---

Cross-lingual embedding mapping learns a matrix $W$ that sends the word vectors of a source language into the vector space of a target language, so that the image of a word lies near the vector of its translation. It needs word vectors trained separately on text in each language and a seed dictionary of a few thousand translation pairs. Mikolov, Le and Sutskever (2013) fitted $W$ by least squares. Xing, Wang, Liu and Lin (2015) normalized the vectors to unit length and required $W$ to be orthogonal, so that the map keeps all distances and angles within the source space. The orthogonal fit is the orthogonal Procrustes problem, and its solution is $W = U V^\top$ from the [singular value decomposition](/singular-value-decomposition/) $U \Sigma V^\top$ of the $d \times d$ matrix $Y^\top X$ (Schönemann 1966). After the map, a source word is translated to the target word nearest to its image, often by [CSLS](/cross-domain-similarity-local-scaling/) rather than plain cosine.

## In plain words

Word vectors trained on English text and on Spanish text have a similar shape: "dog" is near "cat" in both, and "king" is to "queen" in both as "man" is to "woman". But the two spaces are not lined up, because each training run places its vectors in an arbitrary orientation.

Given a short list of known translations, find the turn (and possibly a mirror flip) of the English space that brings each listed English word as close as possible to its Spanish translation. A turn does not stretch anything, so the English space keeps its shape.

There is an exact recipe for the best turn, using a standard matrix factorization. After the turn, translate any English word by finding the Spanish word closest to where it lands.

## The problem

The input is a seed dictionary of $n$ pairs, given as two matrices $X, Y \in \mathbb{R}^{n \times d}$ whose row $i$ holds the source vector $\vec x_i$ and the target vector $\vec y_i$ of pair $i$. The orthogonal mapping problem is

$$\min_{W \in O(d)} \sum_{i=1}^{n} \|W \vec x_i - \vec y_i\|^2 = \min_{W \in O(d)} \|X W^\top - Y\|_F^2,$$

where $O(d)$ is the set of orthogonal $d \times d$ matrices ($W^\top W = I$). It allows rotations and reflections. The unconstrained version, over all $d \times d$ matrices, is the least squares map of Mikolov et al. With columns instead of rows, as in Conneau et al., the matrix $Y^\top X$ is written $Y X^\top$.

For an orthogonal $W$, $\|W \vec x_i - \vec y_i\|^2 = \|\vec x_i\|^2 + \|\vec y_i\|^2 - 2\,\vec y_i^\top W \vec x_i$, so the problem is the same as maximizing $\sum_i \vec y_i^\top W \vec x_i = \operatorname{tr}(W^\top M)$ with $M = Y^\top X$.

## The algorithm

```pseudo id=main
ORTHOGONAL-MAP(X, Y)
L1  scale every row of X and of Y to unit length (optionally center first)
L2  M ← Y^T X                                   ▷ d × d, a sum of n outer products
L3  U, Σ, V ← SVD(M)                            ▷ M = U Σ V^T
L4  W ← U V^T
L5  return W                                    ▷ translate x by the target nearest to W x
```

Line L1 makes the squared distance a function of the cosine, which is the measure used for retrieval. Line L2 is the only step that reads the dictionary: $M = \sum_i \vec y_i \vec x_i^\top$. Line L3 takes the SVD of this small matrix, and line L4 drops the singular values: $W$ is the orthogonal factor of the polar decomposition of $M$. The code computes the SVD by the one-sided Jacobi method and checks $W$ against the Newton iteration $W \leftarrow (W + W^{-\top})/2$ for the polar factor.

## Example

Take $d = 2$ and three pairs, without normalization: $X$ has the rows $(1, 0)$, $(0, 1)$, $(1, 1)$ and $Y$ the rows $(0.9, 0.5)$, $(-0.5, 0.9)$, $(0.4, 1.3)$.

| step | line | value |
|---|---|---|
| $M = Y^\top X$ | L2 | $\begin{pmatrix} 1.3 & -0.1 \\ 1.8 & 2.2 \end{pmatrix}$ |
| singular values | L3 | 2.9530, 1.0295 |
| $W = U V^\top$ | L4 | $\begin{pmatrix} 0.8789 & -0.4771 \\ 0.4771 & 0.8789 \end{pmatrix}$ |
| loss $\sum_i \|W \vec x_i - \vec y_i\|^2$ | | 0.0051 |

$W$ is the rotation by $28.50°$. In two dimensions the best rotation has the angle $\operatorname{atan2}(M_{21} - M_{12}, M_{11} + M_{22}) = \operatorname{atan2}(1.9, 3.5)$, which agrees. The identity map has the loss 0.97. The least squares map is $\begin{pmatrix} 0.9 & -0.5 \\ 0.4667 & 0.8667 \end{pmatrix}$ with a smaller loss, 0.0033, but it is not orthogonal: the entries of $W W^\top - I$ reach 0.06.

**The reflection case.** Take $X = I$ and $Y = \operatorname{diag}(1, -1)$ (the rows $(1, 0)$ and $(0, -1)$). Then $M = \operatorname{diag}(1, -1)$, and the algorithm returns $W = \operatorname{diag}(1, -1)$, a reflection with loss 0. Every rotation by an angle $\theta$ has the loss $(2 - 2\cos\theta) + (2 + 2\cos\theta) = 4$.

## Correctness

For orthogonal $W$, write $Z = V^\top W^\top U$, which is orthogonal. Then $\operatorname{tr}(W^\top M) = \operatorname{tr}(W^\top U \Sigma V^\top) = \operatorname{tr}(Z \Sigma) = \sum_k z_{kk} \sigma_k \le \sum_k \sigma_k$, because every entry of an orthogonal matrix is at most 1 in absolute value and $\sigma_k \ge 0$. The bound is reached at $Z = I$, that is $W = U V^\top$, which line L4 returns. When $M$ is nonsingular the maximizer is unique. The full proof, with the rank-deficient case, is in the proof file.

**Difference from Kabsch.** The [Kabsch algorithm](/kabsch-algorithm/) solves the same problem for molecules over the rotations only ($\det W = +1$), because no rigid motion turns a molecule into its mirror image. It replaces $U V^\top$ by $U \operatorname{diag}(1, \ldots, 1, s) V^\top$ with $s = \operatorname{sign}\det(U V^\top)$, and it centers both point sets to remove the translation. For word vectors a reflection is as good as a rotation: it keeps every dot product and every distance, so no sign fix is needed, and the minimum over $O(d)$ is never worse than the minimum over rotations. In the reflection example above, the Kabsch answer would be a rotation with loss 4 instead of the reflection with loss 0.

## Complexity

Line L1 costs $O(nd)$. Line L2 costs $O(nd^2)$. Lines L3 and L4 work on a $d \times d$ matrix and cost $O(d^3)$ for an SVD to fixed precision (the Jacobi method used here needs a few sweeps of $O(d^3)$ each in practice). The total is $O(nd^2 + d^3)$ time and $O(d^2)$ extra space beyond the input. Since $d$ is a few hundred and $n$ a few thousand, this is small next to the training of the vectors. Translating one word afterwards is a nearest neighbour search over the target vocabulary, $O(Vd)$ by brute force, or faster with an index ([k-nearest neighbor search](/k-nearest-neighbor-search/)).

## Properties

- **Isometry.** An orthogonal $W$ keeps the norms, the dot products and the distances of the source space, so monolingual similarity is unchanged.
- **Closed form.** No learning rate, no iterations over the data, and the answer is the global optimum.
- **Unique when $M$ is nonsingular.** With $n < d$ or a degenerate dictionary, $M$ is singular, and the optimum is not unique; any completion of $U$ and $V$ gives an optimal $W$.
- **Symmetric.** The map for the opposite direction is $W^\top$, since the problem with $X$ and $Y$ swapped has $M^\top = V \Sigma U^\top$ and the answer $V U^\top = W^\top$.
- **Linear.** The method assumes that the two spaces differ by a rotation or reflection; it cannot fix differences in shape between the spaces.

## Variants and improvements

- **Least squares.** Mikolov et al. fit an unconstrained $W$, the [ordinary least squares](/ordinary-least-squares/) solution $W = (Y^\top X)(X^\top X)^{-1}$ when $X$ has full column rank. It fits the seed pairs better but distorts the source space.
- **Refinement.** Conneau et al. alternate two steps: build a new dictionary from the mutual nearest neighbours of the mapped words, then refit $W$ by Procrustes. This can start from a very small dictionary, or from an unsupervised one found by adversarial training.
- **Retrieval.** Plain nearest neighbour retrieval suffers from [hubness](/hubness/): a few target words are nearest to many mapped words. [CSLS](/cross-domain-similarity-local-scaling/) corrects for it and gives a large gain in precision.
- **Preprocessing.** Unit length, then centering, then unit length again is a common normalization before line L2. Centering keeps the problem a pure rotation by removing the mean of each space, as Kabsch does with the translation.
- **Scaling.** Allowing $W = c\,Q$ with an orthogonal $Q$ and a scalar $c > 0$ adds one degree of freedom and gives the same $Q$.

## When to use it

Use the orthogonal map when the two monolingual spaces are trained in the same way and you have a seed dictionary of a few thousand pairs, or a way to build one. It is the standard supervised baseline for bilingual lexicon induction. Use least squares only when the spaces have clearly different shapes and the dictionary is large, since it overfits the seed pairs. For distant languages or very different corpora, the linear assumption is weaker, and methods that learn both spaces jointly may do better.

## Pitfalls

- **The order of the factors.** Line L2 must form $Y^\top X$ (target by source) for a map $\vec x \mapsto W\vec x$. With $X^\top Y$, the result is $W^\top$, the inverse map, which is not optimal in general.
- **Keeping the singular values.** Line L4 must drop $\Sigma$. $U \Sigma V^\top$ is $M$ itself, not an orthogonal matrix.
- **Adding the Kabsch sign fix.** Copying the determinant correction from molecular superposition into line L4 restricts the answer to rotations and can give a worse map. Embeddings have no handedness, so reflections are allowed.
- **Normalizing after the fit.** The normalization of line L1 must be applied before line L2 and also to every vector translated later. A map fitted on unit vectors and applied to raw vectors gives images of the wrong scale, which matters for distances though not for cosines.
- **Duplicate source words.** A dictionary with several translations of one word gives it several rows; this is allowed, but it weights that word more in $M$.

## Implementations

## History

Mikolov, Le and Sutskever (2013) observed that word vectors of different languages have similar geometric arrangements and fitted a linear map on a few thousand frequent words and their translations. Xing, Wang, Liu and Lin (2015) argued that the map should be orthogonal and the vectors normalized, so that training and retrieval use the same cosine measure. The orthogonal problem had been solved long before in psychometrics: Schönemann (1966) gave the SVD solution of the orthogonal Procrustes problem, and Kabsch (1976) gave the rotation-only version for crystallography. Conneau, Lample, Ranzato, Denoyer and Jégou (2018) combined Procrustes refinement with adversarial training and CSLS retrieval, and reached good precision without any parallel data.

## References
