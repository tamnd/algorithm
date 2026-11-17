---
tag: 3BRV2P
kind: data-structure
slug: vocabulary-tree
name: Vocabulary tree
aliases:
- hierarchical k-means vocabulary
- Nister-Stewenius tree
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "A tree from hierarchical k-means on descriptors that quantizes a feature in logarithmic time to one of millions of visual words."
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of training descriptors, k: the branch factor, L: the depth, D: the descriptor dimension, I: the number of k-means iterations, m: the number of descriptors of one image, P: the total length of the inverted files read by a query, S: the number of postings in all the inverted files}
  time: {build: O(n k L D I), quantize: O(k L D), insert: O(m k L D), query: O(m k L D + P)}
  space: {total: O(k^L D + S)}
properties: {deterministic: true, exact: false, static: true}
history:
  year: 2006
  people: [David Nister, Henrik Stewenius]
  note: "Nister and Stewenius (CVPR 2006) built the vocabulary by hierarchical k-means, quantized by greedy descent, and scored images with entropy weights on all nodes and the L1 distance, which made search in a million images fast."
prereqs: [k-means, bag-of-visual-words, inverted-index]
see_also: [image-retrieval, kd-tree, randomized-kd-forest, approximate-nearest-neighbor-search, tf-idf, vlad, visual-place-recognition, spatial-verification]
sources:
  - paper: doi:10.1109/CVPR.2006.264
    title: "David Nister and Henrik Stewenius, Scalable recognition with a vocabulary tree, CVPR 2006, volume 2, 2161-2168"
    locator: "The hierarchical k-means tree, the quantization by greedy descent, the weights ln(N/N_i), and the L1 scoring with inverted files"
  - paper: doi:10.5201/ipol.2018.199
    title: "Esteban Uriza, Francisco Gomez Fernandez and Martin Rais, Efficient large-scale image search with a vocabulary tree, Image Processing On Line 8, 2018, 71-98"
    locator: "A full description and open implementation of the method of Nister and Stewenius, with the scoring formula and experiments"
  - paper: doi:10.1109/CVPR.2007.383172
    title: "James Philbin, Ondrej Chum, Michael Isard, Josef Sivic and Andrew Zisserman, Object retrieval with large vocabularies and fast spatial matching, CVPR 2007"
    locator: "The comparison of approximate flat k-means with hierarchical k-means on the Oxford 5K data set"
  - paper: doi:10.1109/TRO.2012.2197158
    title: "Dorian Galvez-Lopez and Juan D. Tardos, Bags of binary words for fast place recognition in image sequences, IEEE Transactions on Robotics 28(5), 2012, 1188-1197"
    locator: "The vocabulary tree on binary descriptors with the Hamming distance, used for loop detection"
---

A vocabulary tree is a tree of cluster centers that turns a local descriptor into a visual word. It is built by hierarchical [k-means](/k-means/): k-means splits the training descriptors into $k$ groups, then each group is split again, down to depth $L$. The leaves are the visual words of a [bag of visual words](/bag-of-visual-words/), so there can be $k^L$ of them, for example $10^6$ with $k = 10$ and $L = 6$. To quantize a descriptor, start at the root and go to the child with the nearest center, $L$ times. This costs $k L$ distance computations instead of $k^L$. The price is that the leaf found is not always the nearest leaf center. The tree also carries the [inverted files](/inverted-index/) and the weights for image search.

## In plain words

Sorting a huge number of patch types one by one is slow. A vocabulary tree sorts them like a library. First it decides between ten broad groups, then between ten smaller groups inside the chosen one, and so on. After six such choices it has picked one type out of a million, but it has made only sixty comparisons.

Each type keeps a list of the pictures that contain it. To search, the tree sorts the patches of the new picture and reads the lists of the types it reaches. Pictures that share many rare types with the new picture get the best scores.

## The abstract type

The tree implements a [similarity index](/similarity-index/) for images, through two parts.

- **Quantizer.** A map from a descriptor $x \in \mathbb{R}^D$ to a leaf, and to the path of nodes from the root to that leaf.
- **Image index.** A set of database images, each given by its descriptors. The query takes the descriptors of an image and returns the database images ranked by a score.

The tree is built once from training descriptors and then stays fixed. Images can be added to the index at any time, but the weights depend on the number of images, so they are usually computed after the database is complete.

## Representation

Each node $i$ has a center $c_i \in \mathbb{R}^D$ and at most $k$ children. Leaves are at depth at most $L$. A database image $d$ with $m_i$ descriptors whose path passes through node $i$ has the entry $d_i = m_i w_i$, where
$$w_i = \ln \frac{N}{N_i},$$
$N$ is the number of database images and $N_i$ is the number of images with at least one descriptor through node $i$. This is the [tf-idf](/tf-idf/) weight on every node, not only on the leaves. The vector $d$ is divided by its L1 norm. Each node keeps an inverted file: the list of the images $d$ with $d_i > 0$ and their values $d_i$. Nister and Stewenius store the files at the leaves only; the file of an inner node is the union of the files of its leaves.

## Operations

```pseudo id=main
BUILD(X, k, L, depth)                ▷ X: training descriptors, depth 0 at the root
L1  c ← the mean of X
L2  if depth = L or X has fewer than k distinct points then return a leaf with center c
L3  split X into groups X_1, ..., X_k by k-means with k centers
L4  children ← BUILD(X_j, k, L, depth + 1) for each nonempty X_j
L5  return a node with center c and these children
QUANTIZE(x)
L6  node ← the root
L7  while node has children do
L8      node ← the child whose center is nearest to x, ties to the smaller index
L9  return the path of nodes from the root to node
```

**Insert an image.** Quantize each of its $m$ descriptors and count, for each node $i$, the number $m_i$ of paths through it.

**Query.** Compute the vector $q$ of the query image the same way, with the database weights, and normalize it. For a database image $d$, the score is the L1 distance, and for nonnegative vectors of L1 norm 1,
$$\lVert q - d \rVert_1 = 2 + \sum_{i:\ q_i > 0,\ d_i > 0} \big( |q_i - d_i| - q_i - d_i \big) = 2 - 2 \sum_i \min(q_i, d_i).$$
So only the nodes that both images use change the score, and the inverted files of the nodes of the query give all of them. Smaller is better.

## Example

Take $D = 1$, $k = 2$, $L = 2$, with the inner nodes $A$ (center $-1$, leaves $-6$ and $4$) and $B$ (center $10$, leaves $8$ and $12$). These are the k-means centers of the training points $\{-6, 4\}$ and $\{8, 12\}$.

**Greedy descent.** The descriptor $4.6$ is at distance $5.6$ from $A$ and $5.4$ from $B$, so it goes to $B$, then to the leaf $8$, at distance $3.4$. The nearest leaf is $4$, at distance $0.6$. The tree does not give the nearest word.

**Scoring.** The database has three images: $a = \{-6, 4\}$, $b = \{8, 12, 12\}$ and $c = \{4, 9\}$. The root is in all three images, so its weight is $\ln 1 = 0$. The nodes $A$, $B$, $4$ and $8$ are each in two images and get $\ln 1.5 = 0.4055$. The leaves $-6$ and $12$ are each in one image and get $\ln 3 = 1.0986$. Image $a$ has $(A, -6, 4) = (2 \cdot 0.4055, 1.0986, 0.4055)$, which is $(0.3503, 0.4746, 0.1751)$ after L1 normalization. The query $\{3, 5\}$ goes to $A, 4$ and to $B, 8$, so $q = (0.25, 0.25, 0.25, 0.25)$ on $(A, 4, B, 8)$. Image $c$ has the same paths, so its score is 0. For $a$, the shared nodes are $A$ and $4$, and the score is $2 - 2(0.25 + 0.1751) = 1.1497$. For $b$, it is $2 - 2(0.25 + 0.1062) = 1.2877$. The ranking is $c$, $a$, $b$. The tests check these numbers.

## Correctness

The proof in the correctness file shows four facts.

1. **Shape.** BUILD stops, every leaf has depth at most $L$, every node has at most $k$ children, so there are at most $k^L$ leaves. QUANTIZE ends at a leaf after at most $L$ steps.
2. **Nested cells.** Each descriptor reaches exactly one leaf, so the leaves split $\mathbb{R}^D$ into cells. The cell of a leaf is the set of points that pass the nearest-child test at each node of its path. It is not the Voronoi cell of the leaf center among all the leaves, as the example shows. So the tree is an approximate quantizer: a heuristic for nearest center search, with no bound on the error.
3. **Counts nest.** For an inner node, $m_i$ is the sum of $m_j$ over its children, since each path through $i$ continues to exactly one child. A node used by every image has weight 0.
4. **The scoring formula.** The identity above holds for all nonnegative vectors of L1 norm 1, and the query loop that adds $|q_i - d_i| - q_i - d_i$ over the inverted files of the query nodes computes it exactly.

## Complexity

In the [real RAM](/real-ram/), with $n$ training descriptors, each level of BUILD runs k-means on groups whose sizes add up to at most $n$, so with $I$ Lloyd iterations the build costs $O(n k L D I)$. QUANTIZE compares $x$ with at most $k$ centers at each of at most $L$ levels, so it costs $O(k L D)$. A flat vocabulary of $k^L$ words would need $O(k^L D)$ per descriptor without an index. Inserting an image with $m$ descriptors costs $O(m k L D)$. A query costs $O(m k L D)$ for its own vector plus the total length $P$ of the inverted files it reads. The tree takes $O(k^L D)$ space for the centers, and the index takes one posting for each pair of an image and a node it uses.

For $k = 10$, $L = 6$ and SIFT with $D = 128$, the tree has a million leaves and quantizes with 60 distance computations.

## Variants

- **Scoring choices.** Nister and Stewenius compared the L1 and L2 norms and scoring with all nodes or with the leaves only. They report that the L1 norm and larger vocabularies gave better results on their data. That is a benchmark result, not a theorem.
- **Flat approximate k-means.** Philbin et al. (2007) assign descriptors to a flat vocabulary of a million centers with a [randomized k-d forest](/randomized-kd-forest/). On Oxford 5K, their 1M word flat vocabulary gave a mean average precision of 0.618 against 0.439 for the best hierarchical vocabulary. That is a benchmark result: the greedy descent loses matches at the upper levels.
- **Search with backtracking.** Visiting several children at each level, best first, reduces the error of the greedy descent, at a higher cost.
- **Binary descriptors.** DBoW2 (Galvez-Lopez and Tardos 2012) builds the tree on binary descriptors with the [Hamming distance](/hamming-distance/) and uses it for loop detection in SLAM.
- **Direct index.** DBoW2 also stores, for each image, its features grouped by a node at a chosen level, to restrict feature matching to the same node.

## When to use it

Use a vocabulary tree when the vocabulary must be very large and quantization must be fast, as in [image retrieval](/image-retrieval/) on millions of images or in [place recognition](/visual-place-recognition/) on a robot. The tree is easy to build and needs no other index. If the accuracy of the assignment matters more than the build time, a flat vocabulary with approximate search usually ranks better. If each image must be one dense vector, use [VLAD](/vlad/) or a Fisher vector instead.

## Pitfalls

- **Errors at the top.** A wrong choice at the first level cannot be corrected later. Two close descriptors near a boundary at the top can end in leaves that are far apart.
- **Unbalanced trees.** Dense regions of descriptor space get deep, small cells, and sparse regions get large ones. Leaves with very few training points are noisy words.
- **Weights from a small database.** The weights $\ln(N / N_i)$ change with $N$. Weights computed on a small database, or on images of another kind, give poor rankings on the real one.
- **Ties to the root.** The root, and any node that all images use, has weight 0. Images whose descriptors all lie in such nodes get the zero vector and cannot be ranked.
- **Using the score as a probability.** The L1 distance ranks images. It is not calibrated, and a fixed threshold on it does not work across queries. Use [spatial verification](/spatial-verification/) to decide matches.

## Implementations

The Python code builds the tree by hierarchical k-means with Lloyd iterations from random distinct points and a fixed seed, quantizes by greedy descent with the tie rule of this page, computes the weights, keeps the inverted files on all nodes, and scores queries with the formula above. The tests check the example of this page, the greedy descent counterexample, the shape bounds, the nearest-child rule on each step, a zero score for an image queried with its own descriptors, and the equality of the inverted file score with the brute-force L1 distance and with $2 - 2 \sum_i \min(q_i, d_i)$ on random data.

## History

Tree-structured codebooks were known earlier in vector quantization for signal coding. Nister and Stewenius (CVPR 2006) applied hierarchical k-means to local image descriptors, scored images with entropy weights on all the nodes, and showed search in a database of a million images. Philbin et al. (2007) showed that a flat vocabulary with approximate nearest neighbor assignment gives better rankings. Galvez-Lopez and Tardos (2012) adapted the tree to binary descriptors in DBoW2, which ORB-SLAM uses for place recognition and loop closure.

## References
