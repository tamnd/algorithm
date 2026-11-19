---
tag: 92204H
kind: algorithm
slug: hard-debiasing
name: Hard debiasing of word embeddings
aliases:
- Bolukbasi debiasing
- neutralize and equalize
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Find a bias direction by PCA of differences such as he - she, remove it from neutral words, and equalize pairs of gendered words about it.
model: real-ram
complexity:
  vars: {s: the number of words in the defining sets, d: the dimension of the vectors, k: the dimension of the bias subspace, q: the number of power iteration steps, n: the number of words that are neutralized or equalized}
  time: {worst: "O(s d^2 + q k d^2 + n k d)"}
  space: {extra: "O(d^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 2016
  people: [Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama, Adam Kalai]
  note: Bolukbasi and colleagues found a gender direction in word2vec vectors from pairs such as she and he, and proposed to remove it from words that should be neutral and to center gendered pairs on it.
prereqs: [word-embedding, principal-component-analysis]
see_also: [word-embedding-association-test, word-analogy, power-iteration, singular-value-decomposition, gram-schmidt-process, k-means, skip-gram-model, glove]
sources:
  - paper: "Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama and Adam Kalai, Man is to computer programmer as woman is to homemaker? Debiasing word embeddings, Advances in Neural Information Processing Systems 29 (NIPS 2016), pages 4349 to 4357"
    title: Bolukbasi et al. 2016
    locator: the identification of the gender subspace from ten definitional pairs, the direct bias measure, and the hard debiasing algorithm with its neutralize and equalize steps
  - paper: doi:10.18653/v1/N19-1061
    title: Hila Gonen and Yoav Goldberg, Lipstick on a pig, debiasing methods cover up systematic gender biases in word embeddings but do not remove them, NAACL-HLT 2019, pages 609 to 614
    locator: the clustering, bias-by-neighbors, classification and WEAT experiments on the debiased embeddings
  - paper: "Tolga Bolukbasi, Kai-Wei Chang, James Zou, Venkatesh Saligrama and Adam Kalai, arXiv:1607.06520, 2016"
    title: the arXiv version of Bolukbasi et al.
    locator: the appendix with the full lists of definitional pairs and equality sets
---

Hard debiasing removes one kind of bias, such as gender, from a set of [word vectors](/word-embedding/) by geometry. It finds a bias subspace, usually one direction, from defining sets of words such as {she, he} and {woman, man}, as the top principal component of their differences. Then it removes the component in that subspace from words that should be neutral, such as "nurse" or "doctor" (neutralize), and it moves the words of each equality set, such as {grandmother, grandfather}, so that they differ only in that subspace and are equally far from every neutral word (equalize). The geometric effect is exact; whether bias is gone is a measurement, and Gonen and Goldberg 2019 measured that it stays largely recoverable.

## In plain words

In vectors trained on news text, "nurse" lies closer to "she" than to "he", and "engineer" the other way around. The method first finds the direction in which "she" and "he", "woman" and "man", "mother" and "father" differ. That direction stands for gender. For every word that should have no gender, it cuts away the part of the vector that points along that direction, so "nurse" now sits exactly between "she" and "he". For pairs that really are about gender, like "grandmother" and "grandfather", it keeps the gender part but makes the rest the same, so that a neutral word such as "babysitter" is equally close to both. The method fixes what one direction shows. Bias that hides in other directions stays.

## The problem

The input is a set of word vectors, the defining sets $D_1, \ldots, D_n$ (small sets of words whose difference is the bias, usually pairs), the dimension $k$ of the bias subspace, a list $N$ of neutral words, and the equality sets $E_1, \ldots, E_m$ (words that should differ only in the bias subspace). The output is a new set of vectors in which every neutral word has no component in the bias subspace, and every neutral word is equidistant from the words of each equality set.

With $\mu_i$ the mean of $D_i$, the within-set covariance is

$$C = \sum_{i=1}^{n} \sum_{w \in D_i} \frac{(w - \mu_i)(w - \mu_i)^T}{|D_i|},$$

and the bias subspace $B$ is spanned by its top $k$ eigenvectors, the first $k$ right singular vectors of the stacked centered vectors. For a pair $\{a, b\}$ the term is $\frac{1}{4}(a - b)(a - b)^T$, so with pairs and $k = 1$ the bias direction is the top principal component, without centering, of the pair differences such as $she - he$. The paper measures the direct bias of a list $N$ of neutral words along a direction $g$ as $\mathrm{DirectBias}_c = \frac{1}{|N|}\sum_{w \in N} |\cos(w, g)|^c$.

## The algorithm

```pseudo id=main
HARD-DEBIAS(W, D_1 .. D_n, N, E_1 .. E_m, k)
L1  w ← w / ‖w‖   for every word vector w
L2  μ_i ← the mean of the vectors of D_i
L3  C ← Σ_i Σ_{w ∈ D_i} (w - μ_i)(w - μ_i)^T / |D_i|
L4  B ← the top k eigenvectors of C            ▷ power iteration with deflation
L5  for each w in N do  w ← (w - w_B) / ‖w - w_B‖          ▷ neutralize
L6  for each equality set E do  μ ← the mean of E;  ν ← μ - μ_B
L7      for each w in E do  w ← ν + sqrt(1 - ‖ν‖²) (w_B - μ_B) / ‖w_B - μ_B‖   ▷ equalize
L8  return W, B
```

Here $v_B$ is the projection of $v$ on $B$: $v_B = \sum_r (v \cdot b_r)\, b_r$ for the orthonormal basis $b_1, \ldots, b_k$. Line L4 needs only the top eigenvectors of a symmetric $d \times d$ matrix, so [power iteration](/power-iteration/) is enough; a full [singular value decomposition](/singular-value-decomposition/) gives the same subspace. Line L5 gives each neutral word length 1 again, so cosine and dot product agree. In line L7 the part $\nu$ outside $B$ is the same for all words of the set, and the parts inside $B$ have the same length.

## Example

The vectors are written for this page, in three dimensions, with the bias along the first axis. The defining pairs are she $(0.6, 0.8, 0)$ with he $(-0.6, 0.8, 0)$, and woman $(0.8, 0, 0.6)$ with man $(-0.8, 0, 0.6)$. The differences are $(1.2, 0, 0)$ and $(1.6, 0, 0)$, so $C = \frac{1}{4}(1.44 + 2.56)\, e_1 e_1^T = e_1 e_1^T$, and $B$ is spanned by $g = (1, 0, 0)$, with eigenvalue 1.

| word | before | after |
| --- | --- | --- |
| nurse (neutral) | (0.28, 0.96, 0) | (0, 1, 0) |
| doctor (neutral) | (-0.36, 0.48, 0.8) | (0, 0.5145, 0.8575) |
| grandmother (equality set) | (0.48, 0.6, 0.64) | (0.5495, 0.62, 0.56) |
| grandfather (equality set) | (-0.6, 0.64, 0.48) | (-0.5495, 0.62, 0.56) |

For the equality set, $\mu = (-0.06, 0.62, 0.56)$ and $\nu = (0, 0.62, 0.56)$, with $\sqrt{1 - \|\nu\|^2} = \sqrt{0.302} = 0.5495$. Before debiasing, nurse has the cosine 0.7104 with grandmother and 0.4464 with grandfather. After, both cosines are $0.62 = \text{nurse} \cdot \nu$. The direct bias of {nurse, doctor} along $g$ with $c = 1$ falls from $(0.28 + 0.36)/2 = 0.32$ to 0.

## Correctness

The proof below shows the geometric guarantees, which are theorems. After line L5 each neutral word has length 1 and a zero projection on $B$, because $w - w_B$ is orthogonal to $B$. After line L7 each word of an equality set has length 1, all of them share the component $\nu$ outside $B$, and every vector orthogonal to $B$ has the same dot product $n \cdot \nu$ with all of them, so it is equally far from each. For a pair, the two components inside $B$ are opposite. The square root is real because $\|\nu\| \le \|\mu\| \le 1$ for a mean of unit vectors. Line L4 finds the subspace that captures the largest share of the within-set variance, by the same trace argument as [principal component analysis](/principal-component-analysis/).

These are statements about one subspace. That the method removes bias in a wider sense is not a theorem. Bolukbasi et al. measured that the direct bias falls and that crowd workers judge fewer of the generated analogies as stereotypes. Gonen and Goldberg 2019 measured the opposite side: on the debiased word2vec vectors, k-means with two clusters on the 500 most male-biased and the 500 most female-biased words (by their projection on the original gender direction) still matched the original gender label with 92.5% accuracy, against 99.9% before debiasing. The correlation between the original bias of a word and the share of male-biased words among its neighbors stayed at 0.686, against 0.741 before. The WEAT gender tests still gave p-values below 0.05.

## Complexity

The model is the [real-RAM](/real-ram/).

- **Covariance.** Line L3 adds $s$ outer products: $O(s d^2)$ time and $O(d^2)$ space.
- **Subspace.** Each power iteration step multiplies $C$ by a vector, $O(d^2)$, so $k$ vectors with $q$ steps each cost $O(q k d^2)$. A full eigendecomposition costs $O(d^3)$.
- **Neutralize and equalize.** Each projection costs $O(k d)$, so $n$ words cost $O(n k d)$. On $|V|$ words with $d = 300$, this pass is linear in the vocabulary.

## Properties

- **Linear and local.** Only the neutral words and the equality sets change. All other words keep their vectors.
- **Unit length.** Every changed vector has length 1, so the method assumes cosine similarity.
- **Depends on lists.** The defining sets, the neutral words and the equality sets are inputs. The paper takes the definitional pairs from a list of ten (she and he, her and his, woman and man, Mary and John, herself and himself, daughter and son, mother and father, gal and guy, girl and boy, female and male), and it finds the gender-specific words with a classifier trained on a seed list. Every word not judged gender-specific is treated as neutral.
- **Irreversible.** The component along $B$ of a neutral word is lost. A use that needs it, such as gender agreement, breaks for those words.

## Variants and improvements

- **Soft debiasing.** The same paper proposes a linear map that reduces the bias component of neutral words while keeping the inner products of the other words close to the originals, with a parameter that trades the two goals.
- **Several directions.** With $k > 1$, or with defining sets of more than two words, $B$ captures bias that one pair difference misses. The algorithm is the same.
- **Training-time methods.** GN-GloVe (Zhao et al. 2018) trains [GloVe](/glove/) vectors that keep gender in a few reserved coordinates. Gonen and Goldberg 2019 measured that it too leaves the bias recoverable.
- **Projection with a classifier.** Iterative nullspace projection (Ravfogel et al. 2020) trains a linear classifier for the protected attribute, projects on its null space, and repeats until no linear classifier works. It targets the bias that Gonen and Goldberg found.

## When to use it

Use hard debiasing when a downstream use depends mainly on the projection of words on a known direction, for example analogies of the form "man is to X as woman is to Y" (see [word analogy](/word-analogy/)), and when a measurement on that use shows that the projection matters. Do not use it as evidence that an embedding is fair. Measure bias after debiasing with several tests, such as the [WEAT](/word-embedding-association-test/), clustering and neighbor tests, and with tests on the downstream task.

## Pitfalls

- **Bias outside the subspace.** The neighbors of a neutral word stay mostly the same, and they still carry gender. Gonen and Goldberg 2019 recovered gender from the debiased vectors with clustering and with a classifier. Report these measurements next to the direct bias.
- **Uncentered and centered PCA.** For pairs, line L3 gives the uncentered principal component of the differences. Centering the differences before PCA gives a different direction, and for pairs that point the same way it can remove the signal itself.
- **A neutral word in an equality set.** Neutralize and equalize contradict each other for such a word. Keep the lists disjoint.
- **Missing normalization.** Line L1 makes every vector unit length. Without it the square root in line L7 can be imaginary and the equidistance fails.
- **Wrong word lists.** Treating a gender-specific word, such as "beard" or "pregnant", as neutral removes real meaning. The lists need care for each language and for each kind of bias.

## Implementations

The code takes the word vectors as given and implements the within-set covariance, the bias subspace by power iteration with deflation, neutralize, equalize and the direct bias.

## History

Bolukbasi, Chang, Zou, Saligrama and Kalai 2016 showed that word2vec vectors trained on Google News complete analogies such as "man is to computer programmer as woman is to homemaker", found a gender direction from definitional pairs, and proposed hard and soft debiasing. Their experiments used 300-dimensional vectors restricted by a filter on the vocabulary to 26,377 words. Caliskan, Bryson and Narayanan 2017 measured similar biases with the [WEAT](/word-embedding-association-test/). Gonen and Goldberg 2019 then measured that the debiased vectors still encode gender in the arrangement of the words, which moved later work toward methods that remove all linearly decodable information and toward bias tests on the downstream tasks.

## References
