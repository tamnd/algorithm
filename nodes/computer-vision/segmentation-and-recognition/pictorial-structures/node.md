---
tag: ZNK7K3
kind: model
slug: pictorial-structures
name: Pictorial structures
aliases:
- Fischler-Elschlager model
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Model an object as parts joined by springs, and with a tree of springs find the best placement of all parts by dynamic programming over the tree."
history:
  year: 1973
  people: [Martin A. Fischler, Robert A. Elschlager, Pedro F. Felzenszwalb, Daniel P. Huttenlocher]
  note: "Fischler and Elschlager (1973) described objects as pieces held by springs and matched them with a procedure similar to dynamic programming. Felzenszwalb and Huttenlocher (2000, 2005) restricted the springs to a tree with quadratic costs and made matching linear in the number of locations."
prereqs: [tree-dynamic-programming, felzenszwalb-distance-transform]
see_also: [deformable-part-model, implicit-shape-model, distance-transform, object-recognition, minimum-spanning-tree, belief-propagation, template-matching, dalal-triggs-detector]
sources:
  - paper: doi:10.1109/T-C.1973.223602
    title: "Martin A. Fischler and Robert A. Elschlager, The representation and matching of pictorial structures, IEEE Transactions on Computers C-22(1), 1973, 67-92"
    locator: "The model of components held by springs, the cost of a match, and the matching procedure similar to dynamic programming (abstract and main text)"
  - paper: doi:10.1023/B:VISI.0000042934.15159.49
    title: "Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Pictorial structures for object recognition, International Journal of Computer Vision 61(1), 2005, 55-79"
    locator: "Eq. (1) (the energy), Eq. (2) (the deformation cost as a Mahalanobis distance), Section 2 (the statistical framework with a tree-structured prior), Section 3 (learning, with the tree as a minimum spanning tree), Section 4.1 (NP-hardness for general graphs, the recurrences of Eq. (11) and (12), generalized distance transforms), Section 4.2 (sampling)"
  - paper: doi:10.4086/toc.2012.v008a019
    title: "Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Distance transforms of sampled functions, Theory of Computing 8, 2012, 415-428"
    locator: "The lower envelope algorithm for the squared Euclidean distance transform of a sampled function in one dimension, and its separable use in two dimensions"
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 3 (a star-structured pictorial structure on HOG features), Eq. (8) (the distance transform in matching)"
---

A pictorial structure models an object as a set of parts, each with its own appearance, and a set of springs between pairs of parts that say where the parts usually sit relative to each other. A face is two eyes, a nose and a mouth on springs; a person is a head, a torso and limbs. Matching the model to an image means placing every part at once so that the parts fit the image well and the springs are not stretched much. Fischler and Elschlager (1973) introduced the model; Felzenszwalb and Huttenlocher (2005) showed that when the springs form a tree and their costs are quadratic, the best placement can be found exactly in time linear in the number of possible locations of a part.

## The machine

**Parts and locations.** A model has $n$ parts $v_1, \ldots, v_n$. A location $l_i$ of part $i$ is a point of a discrete set $\mathcal{L}$ of $h$ values: a position $(x, y)$, and in some models also a scale and an orientation. A configuration is $L = (l_1, \ldots, l_n)$.

**Appearance.** For each part, a match cost $m_i(l)$ says how badly the image fits part $i$ at location $l$; lower is better. In practice it comes from a filter, such as the correlation of a template with [HOG](/histogram-of-oriented-gradients/) features, or from a colour model of a limb.

**Springs.** A graph $G = (V, E)$ on the parts has a deformation cost $d_{ij}(l_i, l_j)$ for each edge. Felzenszwalb and Huttenlocher use a Mahalanobis distance $d_{ij}(l_i, l_j) = (T_{ij}(l_i) - T_{ji}(l_j))^\top M_{ij}^{-1} (T_{ij}(l_i) - T_{ji}(l_j))$ with a diagonal $M_{ij}$, where the maps $T_{ij}$ and $T_{ji}$ take each location to the place of the joint between the two parts. For positions only, with the child $j$ resting at an offset $u$ from its parent $i$, this is
$$d_{ij}(l_i, l_j) = w_x (x_j - x_i - u_x)^2 + w_y (y_j - y_i - u_y)^2.$$

**The energy.** The best configuration minimizes
$$E(L) = \sum_{i = 1}^{n} m_i(l_i) + \sum_{(v_i, v_j) \in E} d_{ij}(l_i, l_j).$$
In the statistical form of the model, $\exp(-m_i)$ is a likelihood for the image near each part and $\exp(-d_{ij})$ is a Markov random field prior on the configuration, so the minimum of $E$ is the maximum a posteriori configuration.

## What it counts

The cost of matching is the number of operations to find $\min_L E(L)$ and a configuration that attains it, as a function of $n$ and $h$, in the [real RAM](/real-ram/). For a tree, the minimum is computed by [tree dynamic programming](/tree-dynamic-programming/): each part sends to its parent a message $B_j(l_i)$, the best cost of its whole subtree for each location $l_i$ of the parent. Computing one message by trying every pair of locations costs $\Theta(h^2)$, so the direct method costs $\Theta(n h^2)$. With $h$ in the hundreds of thousands, for positions, scales and angles, this is too slow, and the quadratic form of $d_{ij}$ is what brings it down to $O(nh)$. The model also counts the cost of learning: estimating the $m_i$, the $d_{ij}$ and the tree from labelled examples.

## Relation to other models

- **Star models.** A star is a tree with one root part and all other parts as its children. The [deformable part model](/deformable-part-model/) is a star pictorial structure on HOG features, with a root filter, part filters at twice the resolution, quadratic deformation costs, and discriminative training. The [implicit shape model](/implicit-shape-model/) is another star model, in which local features vote for the position of the object centre and parts are not explicit.
- **Constellation models.** Generative part models with a full joint Gaussian shape model, such as the constellation models of Perona and his students, give each pair of parts a dependency; matching them costs exponentially more in $n$. The tree drops most of these dependencies to get exact matching.
- **Templates.** A rigid [template match](/template-matching/) is a pictorial structure with one part, or with springs of infinite stiffness. The [Dalal-Triggs detector](/dalal-triggs-detector/) is such a rigid template on HOG features.
- **Graphical models.** The energy is a pairwise Markov random field on the parts. On a tree, the dynamic program is min-sum [belief propagation](/belief-propagation/). On a graph with cycles, loopy belief propagation and other approximate methods apply, but exactness is lost.

## Known results in the model

**General graphs are hard.** For an arbitrary graph $G$ and arbitrary costs, minimizing $E$ is NP-hard, as Felzenszwalb and Huttenlocher (2005) note in Section 4.1; with $n$ parts the brute-force search tries $h^n$ configurations.

**Trees in $O(nh^2)$.** For a tree, the recurrences of Felzenszwalb and Huttenlocher (Eq. (11) and (12)) compute the messages from the leaves to the root and the minimizing locations on the way back, in $O(n h^2)$ time for arbitrary pairwise costs.

**Trees with quadratic springs in $O(nh)$.** When $d_{ij}$ is a squared distance after the maps $T_{ij}$, each message is a generalized distance transform $D_f(x) = \min_y \big(\rho(x, y) + f(y)\big)$ of the function $f$ that the subtree sends up. The [Felzenszwalb distance transform](/felzenszwalb-distance-transform/) computes it for $\rho(x, y) = w (x - y)^2$ in linear time by building the lower envelope of the parabolas $w(x - q)^2 + f(q)$, one for each $q$, and the transform is separable over the coordinates. The whole match then costs $O(nh)$:

```pseudo id=main
DT1(f, w, u)                       ▷ D(p) = min over q of f(q) + w (q - p - u)^2
L1  k ← 0; v[0] ← 0; z[0] ← -∞; z[1] ← +∞
L2  for q ← 1 to N - 1 do
L3      s ← ((f(q) + w q^2) - (f(v[k]) + w v[k]^2)) / (2 w (q - v[k]))
L4      if s ≤ z[k] then k ← k - 1 and go back to L3
L5      k ← k + 1; v[k] ← q; z[k] ← s; z[k + 1] ← +∞
L6  k ← 0
L7  for p ← 0 to N - 1 do
L8      while z[k + 1] < p + u do k ← k + 1
L9      D(p) ← w (p + u - v[k])^2 + f(v[k]); A(p) ← v[k]

MATCH(tree, m, springs)
L10 for each part j in postorder (children before parents) do
L11     f_j ← m_j + the sum of B_c over the children c of j
L12     if j is not the root then (B_j, A_j) ← DT2 of f_j with the spring of j      ▷ DT1 on rows, then on columns
L13 l_root ← a location that minimizes f_root
L14 for each part j in preorder, below the root do l_j ← A_j(l_parent(j))
L15 return the configuration l and the energy f_root(l_root)
```

The correctness file proves that DT1 evaluates the lower envelope, that the two passes of DT2 give the two-dimensional transform, and that the messages give the minimum energy over each subtree, so the configuration is optimal.

**A small example.** Take the one-dimensional function $f = (3, 0, 5, 1, 4)$ on the positions $0, \ldots, 4$, with $w = 1$ and $u = 0$. The transform is $D = (1, 0, 1, 1, 2)$ with the minimizers $(1, 1, 1, 3, 3)$: for $p = 0$ the best is $q = 1$ with $0 + 1 = 1$, and for $p = 4$ it is $q = 3$ with $1 + 1 = 2$. For a three-part star on six positions in a row, with a torso as the root, the match costs torso $(2, 1, 3, 0, 2, 4)$, head $(1, 3, 0, 2, 4, 1)$ resting one position to the right of the torso, and leg $(3, 2, 2, 0, 1, 0)$ resting one position to the left, all with $w = 1$, the messages are $B_{\mathrm{head}} = (1, 0, 1, 2, 1, 2)$ and $B_{\mathrm{leg}} = (4, 3, 2, 1, 0, 1)$. The torso total is $(7, 4, 6, 3, 3, 7)$. The smallest value is 3, first reached at position 3; going back down, the head goes to position 5 (cost $1 + 1$) and the leg to position 3 (cost $0 + 1$). The energy is $0 + 2 + 1 = 3$, and a search over all $6^3$ configurations gives the same minimum.

**Learning.** Given labelled configurations, Felzenszwalb and Huttenlocher estimate the appearance models and the spring parameters of each pair by maximum likelihood, and choose the tree as a [minimum spanning tree](/minimum-spanning-tree/) of the pairwise costs, computed with Kruskal's algorithm.

**Sampling.** Instead of one best configuration, the same messages, with sums in place of minima, let one draw configurations from the posterior distribution (Section 4.2); the distance transform is replaced by a Gaussian convolution. Several samples give several hypotheses, which later steps can check.

**Uses.** With a tree of body parts (torso, head and limb segments) and locations with position, scale and angle, Felzenszwalb and Huttenlocher matched articulated people in images. The star-shaped special case, trained discriminatively, became the deformable part model, which had the best average precision on 9 of the 20 classes of PASCAL VOC 2008 in its authors' comparison, and tree models of body parts became a standard approach to human pose estimation before convolutional networks.

The Python code of this page implements DT1, the separable DT2 with offsets and weights, and MATCH for any tree. Its tests compare DT1 with a direct minimum over all $q$, DT2 with a quadratic search, and MATCH with a search over all configurations of up to four parts, and check the example above.

## References
