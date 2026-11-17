---
tag: 5X16YR
kind: model
slug: deformable-part-model
name: Deformable part model
aliases:
- DPM
- Felzenszwalb deformable parts
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Score an object as a root HOG filter plus part filters at displaced positions minus a quadratic deformation cost, maximized fast with generalized distance transforms."
history:
  year: 2008
  people: [Pedro F. Felzenszwalb, David McAllester, Deva Ramanan, Ross B. Girshick]
  note: "Felzenszwalb, McAllester and Ramanan (CVPR 2008) put a star-shaped pictorial structure on HOG features and trained it as a latent SVM. The journal version with Girshick (2010) added mixtures of components, bounding-box prediction and context rescoring."
prereqs: [pictorial-structures, dalal-triggs-detector]
see_also: [felzenszwalb-distance-transform, histogram-of-oriented-gradients, support-vector-machine, sliding-window-detection, object-detection, implicit-shape-model, box-non-maximum-suppression, r-cnn]
sources:
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 3 (Eq. (2) to (4) the score and deformation features, Eq. (8) and (9) matching with distance transforms, Section 3.3 mixtures), Section 4 (latent SVM, semi-convexity, coordinate descent, stochastic gradient descent, data mining with Theorems 1 and 2), Section 5 (training), Section 6 (features), Section 7 (bounding-box prediction, non-maximum suppression, context), Section 8 (results)"
  - paper: doi:10.1109/CVPR.2008.4587597
    title: "Pedro F. Felzenszwalb, David McAllester and Deva Ramanan, A discriminatively trained, multiscale, deformable part model, CVPR 2008"
    locator: "The first version: a root filter, part filters at twice its resolution, and latent SVM training"
  - paper: doi:10.1023/B:VISI.0000042934.15159.49
    title: "Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Pictorial structures for object recognition, International Journal of Computer Vision 61(1), 2005, 55-79"
    locator: "Section 4.1 (matching a tree model with generalized distance transforms)"
  - paper: doi:10.1109/CVPR.2005.177
    title: "Navneet Dalal and Bill Triggs, Histograms of oriented gradients for human detection, CVPR 2005"
    locator: "The HOG features and the rigid linear template that the root filter extends"
---

The deformable part model (DPM) is an object model for [sliding-window detection](/sliding-window-detection/). It scores a window as a coarse *root filter* that covers the whole object, plus several *part filters* at twice the resolution, each allowed to move away from its rest position at a quadratic cost. It is a star-shaped [pictorial structure](/pictorial-structures/) on [HOG](/histogram-of-oriented-gradients/) features, so the best placement of the parts at every root position is found with [generalized distance transforms](/felzenszwalb-distance-transform/) in time linear in the number of positions. Felzenszwalb, Girshick, McAllester and Ramanan trained it discriminatively as a *latent SVM*, in which the part positions are hidden variables, and it was among the best detectors on PASCAL VOC from 2008 until convolutional networks such as [R-CNN](/r-cnn/) replaced it in 2014.

## The machine

**The feature pyramid.** A HOG feature map with cells of 8 by 8 pixels is computed at each level of an [image pyramid](/image-pyramid/). Each cell has a 31-dimensional vector: 18 contrast-sensitive orientation bins, 9 contrast-insensitive orientation bins and 4 gradient energy terms. The last 13 numbers are an analytic projection of the 36 numbers that the four block normalizations of [Dalal and Triggs](/dalal-triggs-detector/) give for one cell. The pyramid has $\lambda$ levels per octave, and a part filter is placed $\lambda$ levels below its root, where the cells are half as big, so the parts see twice the detail.

**The model.** A model with $n$ parts is $(F_0, P_1, \ldots, P_n, b)$. $F_0$ is the root filter, a $w_0 \times h_0$ array of 31-vectors. Each part is $P_i = (F_i, v_i, d_i)$: a filter $F_i$, an anchor position $v_i$ relative to the root, and four deformation coefficients $d_i$. The bias $b$ makes the scores of different models comparable.

**The score.** A placement is $z = (p_0, \ldots, p_n)$, with $p_i = (x_i, y_i, l_i)$ a cell and a level, and $l_i = l_0 - \lambda$ for the parts. Its score is (Eq. (2) of the paper)
$$\mathrm{score}(p_0, \ldots, p_n) = \sum_{i=0}^{n} F_i \cdot \phi(H, p_i) - \sum_{i=1}^{n} d_i \cdot \phi_d(dx_i, dy_i) + b,$$
where $\phi(H, p)$ is the subwindow of features at $p$ the size of the filter, $(dx_i, dy_i) = (x_i, y_i) - (2(x_0, y_0) + v_i)$ is the displacement of part $i$ from its anchor (Eq. (3)), and $\phi_d(dx, dy) = (dx, dy, dx^2, dy^2)$ (Eq. (4)). With $d_i$ having positive quadratic terms, the deformation cost is a separable quadratic spring.

**Detection.** The score of a root placement is the best score over the part placements:
$$\mathrm{score}(x_0, y_0, l_0) = R_{0, l_0}(x_0, y_0) + \sum_{i=1}^{n} D_{i, l_0 - \lambda}\big(2(x_0, y_0) + v_i\big) + b,$$
where $R_{i, l}$ is the response of filter $F_i$ on level $l$ (a correlation) and
$$D_{i, l}(x, y) = \max_{dx, dy} \big( R_{i, l}(x + dx, y + dy) - d_i \cdot \phi_d(dx, dy) \big)$$
is a generalized distance transform of that response (Eq. (8) and (9)). The root placements with a score above a threshold are detections; the argmax of each $D_i$ gives the part positions. Then:

- **Bounding-box prediction.** A linear function of the root and part positions, fit by least squares, predicts a better box (Section 7.1).
- **Non-maximum suppression.** Detections are sorted by score, and a detection is dropped when more than 50 percent of its box is covered by a box already kept (Section 7.2). This is the coverage test, not the [intersection over union](/intersection-over-union/) of later [box non-maximum suppression](/box-non-maximum-suppression/).
- **Context.** A second classifier rescores each detection with the best scores of all the class models in the image (Section 7.3).

**Mixtures.** A mixture model has $m$ components, each a full star model, for example for the front and the side view of a car. The score of a root placement is the best over the components (Section 3.3).

## What it counts

The model counts the work of scoring a whole feature pyramid. Let $k$ be the number of cells of the pyramid and $n$ the number of parts. The filter responses are correlations; each distance transform is $O(k)$ by the lower envelope method, so matching all parts at all root placements costs $O(nk)$ beyond the correlations. Compared with a single rigid filter of the same size, the parts add a small constant factor to the cost.

For training, it counts the solution of the latent SVM problem. With a vector $\beta$ of all filter weights, deformation coefficients and the bias, and a feature vector $\Phi(x, z)$ for an example $x$ and a latent value $z$ (the component and the part placements),
$$f_\beta(x) = \max_{z \in Z(x)} \beta \cdot \Phi(x, z),$$
and the training objective over labelled examples $(x_i, y_i)$, $y_i \in \{-1, 1\}$, is (Eq. (14))
$$L_D(\beta) = \frac{1}{2} \|\beta\|^2 + C \sum_{i} \max\big(0, 1 - y_i f_\beta(x_i)\big).$$

## Relation to other models

- **Pictorial structures.** The DPM is a [pictorial structure](/pictorial-structures/) with a star graph, the root as the centre, and quadratic springs; the dynamic program of that model becomes one distance transform per part.
- **The Dalal-Triggs detector.** With no parts, the model is a single HOG filter scored by a linear SVM, which is the [Dalal-Triggs detector](/dalal-triggs-detector/) with a different feature map. The paper reports that the root filter alone gives an average precision of 0.24 on the person class of PASCAL VOC 2006, and the full model 0.39 (Section 8).
- **Support vector machines.** With a single latent value for each example, $f_\beta$ is linear, and the objective is that of a linear [support vector machine](/support-vector-machine/). Multiple-instance SVMs are another special case, where the latent value picks one instance from a bag.
- **The implicit shape model.** The [implicit shape model](/implicit-shape-model/) is also a star of local appearance around a centre, but it is generative, uses many small codebook patches instead of a few learned part filters, and finds objects by voting instead of by scanning.
- **Convolutional networks.** Girshick and others later showed that the DPM can be written as a convolutional network with distance transform pooling. Region-based detectors such as R-CNN replaced it from 2014.

## Known results in the model

**Semi-convexity (Section 4.1).** $f_\beta$ is a maximum of linear functions of $\beta$, so it is convex. The hinge loss $\max(0, 1 - y f_\beta(x))$ is then convex for a negative example ($y = -1$), but not for a positive one. If the latent value of each positive example is fixed to one $z$, the objective becomes convex. This gives a coordinate descent (Section 4.2): fix the best latent value of each positive under the current $\beta$, then solve the convex problem in $\beta$, which is a standard SVM over the fixed positives and all latent values of the negatives; repeat. Neither step increases $L_D$, so the objective goes down monotonically, but only to a local optimum, and the method needs a good start.

**Data mining of hard negatives (Section 4.4).** A negative image gives a very large number of windows. Let $\beta^*(C)$ be the minimizer of the objective on a cache $C$ of examples, and $H(\beta, D)$ the hard examples of $D$ under $\beta$: those with $y_i f_\beta(x_i) < 1$. Theorem 1 states that if $H(\beta^*(C), D) \subseteq C$, then $\beta^*(C) = \beta^*(D)$, so the cache can be grown with hard examples and shrunk of easy ones while the solution on the cache stays correct for all of $D$. Theorem 2 gives conditions under which this loop terminates.

**Training procedure (Section 5).** Train the root filters of the components first, with the data split by the aspect ratio of the boxes; combine them into a mixture; then place 6 parts per component greedily on high-energy regions of the root filter at twice the resolution, and train the whole model with the coordinate descent and data mining above. The quadratic deformation coefficients are kept at least 0.01, so every spring stays a proper quadratic cost.

**Matching cost.** The cost $O(nk)$ for $n$ parts and $k$ positions follows from the linear-time [Felzenszwalb distance transform](/felzenszwalb-distance-transform/): without it, the best part placement for every root position by brute force would cost $O(nk \cdot r)$ for a search region of $r$ cells per part.

**Results (Section 8).** On PASCAL VOC 2008 the system had the best average precision of the entries in 9 of the 20 classes and the second best in 8, and on the INRIA person data it reached an average precision of 0.869.

## References
