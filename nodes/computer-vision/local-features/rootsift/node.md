---
tag: 5CC4QY
kind: technique
slug: rootsift
name: RootSIFT
aliases:
- Hellinger kernel SIFT
area: computer-vision/local-features
level: advanced
summary: L1-normalize a SIFT vector and take the square root of each entry, so that the dot product of two results equals the Hellinger kernel of the originals.
prereqs: [sift, feature-descriptor]
see_also: [lowe-ratio-test, feature-matching, bag-of-visual-words, image-retrieval, vlad, vocabulary-tree, principal-component-analysis, histogram-of-oriented-gradients]
sources:
  - paper: doi:10.1109/CVPR.2012.6248018
    title: "Relja Arandjelovic and Andrew Zisserman, Three things everyone should know to improve object retrieval, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2012"
    locator: "Section 3, RootSIFT: the Hellinger kernel, the identity between the Euclidean distance of the square-rooted vectors and the kernel, and the retrieval results on Oxford 5k and Oxford 105k"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004"
    locator: the SIFT descriptor, a histogram of gradient orientations with non-negative entries
---

RootSIFT is a change of the descriptor, not of the matcher. Divide a SIFT vector by the sum of its entries (L1 normalization) and take the square root of each entry. For two vectors mapped this way, the dot product is the Hellinger kernel $H(x, y) = \sum_i \sqrt{\bar x_i \bar y_i}$ of the original histograms, and the squared Euclidean distance is $2 - 2H$. So every tool that uses Euclidean distance, such as a [kd-forest](/randomized-kd-forest/), the [ratio test](/lowe-ratio-test/) or k-means for a visual vocabulary, compares the descriptors with the Hellinger kernel and needs no change. The map costs $O(D)$ per descriptor of length $D$ and is done once, before storage. Arandjelovic and Zisserman (2012) proposed it and measured better retrieval with it.

## In plain words

A SIFT descriptor is a histogram: it counts how much gradient points in each direction in each part of a patch. Plain Euclidean distance compares two histograms bin by bin, and a few large bins decide most of the result, so a small change in one strong edge can hide agreement in many weaker bins. Taking the square root makes large values smaller and small values larger, so all the bins count more evenly. Dividing by the sum first makes the result independent of the overall contrast. After this change you use the new vectors exactly as before, and the usual distance now measures how much two histograms overlap.

## When it applies

- The descriptors are histograms or other vectors with non-negative entries, such as [SIFT](/sift/), [SURF](/surf/) or [HOG](/histogram-of-oriented-gradients/). A descriptor with negative entries, such as one from a neural network, has no square root map of this kind.
- The rest of the system uses Euclidean distance or dot products, and you want a histogram distance without changing that code.
- You can store the mapped vectors, or map each descriptor when you read it. The map keeps the length $D$.

## The template

```pseudo id=main
ROOTSIFT-THEN(X, STEP)
L1  for each descriptor x in X: s ← Σ_i x_i
L2      if s = 0 then y ← x
L3      else y ← (sqrt(x_1 / s), …, sqrt(x_D / s))
L4  run STEP on the y vectors   ▷ hole: matching, k-means, vocabulary tree
```

Lines L1 to L3 map one descriptor. Line L2 keeps the zero vector, which has no direction. The hole is line L4: any method that uses Euclidean distance or dot products, for example exact nearest neighbor matching with the ratio test, a [vocabulary tree](/vocabulary-tree/) or a [bag of visual words](/bag-of-visual-words/). The code in `impl/python/rootsift.py` maps a descriptor and finds a nearest neighbor with the mapped vectors. The proof in `proofs/correctness.md` shows that a mapped vector has unit length, that the dot product of two mapped vectors is the Hellinger kernel, that the squared distance is $2 - 2H$, so the Euclidean nearest neighbor is the descriptor of largest Hellinger kernel, and that the result does not change when a descriptor is multiplied by a positive number.

Example. Take two-bin histograms $q = (9, 16)$, $p_1 = (0, 25)$ and $p_2 = (16, 9)$. Which one is nearer to $q$?

| | after L2 normalization | SIFT distance to $q$ | after RootSIFT | Hellinger kernel $H$ | RootSIFT distance $\sqrt{2 - 2H}$ |
|---|---|---|---|---|---|
| $q$ | $(0.4903, 0.8716)$ | | $(0.6, 0.8)$ | | |
| $p_1$ | $(0, 1)$ | 0.5068 | $(0, 1)$ | $0.8$ | 0.6325 |
| $p_2$ | $(0.8716, 0.4903)$ | 0.5393 | $(0.8, 0.6)$ | $0.6 \cdot 0.8 + 0.8 \cdot 0.6 = 0.96$ | 0.2828 |

Plain SIFT with L2 normalization picks $p_1$, because the large second bin of $q$ is close to that of $p_1$. RootSIFT picks $p_2$, whose histogram overlaps more with $q$ in both bins. You can check every value by hand.

## Classic examples

- **Object retrieval.** Arandjelovic and Zisserman (2012) used RootSIFT in a [bag of visual words](/bag-of-visual-words/) system for [image retrieval](/image-retrieval/). On Oxford 105k, they report that the mean average precision goes from 0.515 to 0.581 with tf-idf ranking and from 0.581 to 0.642 with spatial reranking. These are measurements on that dataset in 2012, not guarantees.
- **Descriptor matching.** Many structure from motion and image stitching systems apply RootSIFT before [feature matching](/feature-matching/) with the [ratio test](/lowe-ratio-test/), because it changes only one line of code.
- **Aggregated descriptors.** Encodings such as [VLAD](/vlad/) and Fisher vectors often take RootSIFT as input, and they apply the same signed square root idea to the final vector.

## Variations

- **Square root of a different histogram.** The same map applies to any histogram descriptor, such as [HOG](/histogram-of-oriented-gradients/) or color histograms.
- **Power normalization.** Use $x_i^{\alpha}$ with $0 < \alpha < 1$ in place of the square root, then normalize. The value $\alpha = 1/2$ gives the Hellinger kernel; other values are tuned and have no such identity.
- **Signed square root.** For vectors with negative entries, use $\operatorname{sign}(x_i) \sqrt{\lvert x_i \rvert}$. This is a heuristic and does not give the Hellinger kernel.
- **With PCA.** Apply [principal component analysis](/principal-component-analysis/) after RootSIFT to make the vectors shorter. The PCA step is learned on a sample and changes the distances.

## Pitfalls

- **L1, not L2, before the root.** SIFT descriptors are usually stored after L2 normalization. RootSIFT needs L1 normalization before the root; with L2 normalization the mapped vectors do not have unit length and the identity with the Hellinger kernel fails.
- **Clipping and quantization.** SIFT clips large entries and often stores bytes. The map still works, but it uses the clipped histogram, and if you store the mapped vectors as bytes you need a new scale.
- **Thresholds change.** Distances of mapped vectors are in $[0, \sqrt{2}]$ and have a different distribution. A distance threshold or a ratio test threshold tuned for plain SIFT must be tuned again.
- **Mixed databases.** All descriptors in a database and all queries must use the same map. Comparing a RootSIFT vector with a plain SIFT vector gives no useful distance.
- **Not a better detector.** RootSIFT changes only the descriptor distance. It does not add keypoints or fix wrong scales and orientations.

## References
