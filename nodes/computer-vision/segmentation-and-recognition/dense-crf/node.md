---
tag: 9CMFRH
kind: algorithm
slug: dense-crf
name: Fully connected CRF inference
aliases:
- dense CRF
- Krahenbuhl-Koltun CRF
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Mean field inference in a CRF with Gaussian pairwise terms between all pixel pairs, made linear time by high-dimensional filtering of messages.
solves: [semantic-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, L: the number of labels, N: the number of mean field iterations}
  time: {worst: O(N L W H), average: O(N L W H), best: O(N L W H)}
  space: {extra: O(L W H)}
properties: {deterministic: true, iterative: true, approximate_inference: true, convergence_guaranteed: false}
history:
  year: 2011
  people: [Philipp Krähenbühl, Vladlen Koltun]
  note: Krähenbühl and Koltun made mean field in the fully connected CRF practical in 2011 with the permutohedral lattice of Adams, Baek and Davis (2010).
prereqs: [conditional-random-field, mean-field-approximation, gaussian-filter, bilateral-filter]
see_also: [semantic-segmentation, markov-random-field, potts-model, image-segmentation-graph-cuts, loopy-belief-propagation, mask-r-cnn]
sources:
  - paper: arxiv:1210.5644
    title: Philipp Krähenbühl and Vladlen Koltun, Efficient inference in fully connected CRFs with Gaussian edge potentials, NIPS 24, 109-117, 2011
    locator: "Section 2 (model, equations 1 to 3), Section 3 (mean field, equations 4 and 5, Algorithms 1 and 2), Section 4 (parameters)"
  - url: https://proceedings.mlr.press/v28/kraehenbuehl13.html
    title: Philipp Krähenbühl and Vladlen Koltun, Parameter learning and convergent inference for dense random fields, ICML 2013, PMLR 28(3), 513-521
    locator: "Section 3 (convergence conditions, Sections 3.1 and 3.2)"
  - paper: doi:10.1111/j.1467-8659.2009.01645.x
    title: Andrew Adams, Jongmin Baek and Abe Davis, Fast high-dimensional filtering using the permutohedral lattice, Computer Graphics Forum 29(2), 753-762, 2010
    locator: The permutohedral lattice (splat, blur and slice)
  - paper: doi:10.1561/2200000001
    title: Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008
    locator: Section 5, Mean field methods
---

A fully connected CRF (dense CRF) labels each pixel of an image, for example with an object class, using a [conditional random field](/conditional-random-field/) in which every pair of pixels has a pairwise term, not only neighbors. The pairwise term is a Potts penalty times a sum of Gaussian kernels in position and color, so similar pixels that are close prefer the same label. Exact inference is out of reach, so Krähenbühl and Koltun (2011) use the [mean field approximation](/mean-field-approximation/). This page is about that inference: the update, why it is correct, where it can fail, and how the messages, a sum over all pixel pairs, become a Gaussian filter. The general CRF and the general mean field method are on their own pages. In practice a dense CRF refines the per-pixel scores of a classifier, often a convolutional network; the network is outside this page.

## In plain words

A classifier looks at each pixel and gives a score for each label, for example "70 percent road, 30 percent car". These scores are noisy, and they often blur at object edges. A dense CRF lets pixels vote. Each pixel asks every other pixel what it believes, and gives more weight to pixels that are close and have a similar color. Then it updates its own belief with the votes and its own score. After a few rounds of this, a region with one color tends to agree on one label, and the label changes where the color changes.

Asking every other pixel is too slow when done one pair at a time. The trick is that the weighted vote is a blur of the belief images with a Gaussian that also looks at color. A fast filter computes such a blur for all pixels at once.

## The problem

The input is an image of $n = WH$ pixels, a label set of size $L$, and a unary energy $U_i(l)$ for each pixel $i$ and label $l$, usually $U_i(l) = -\log p_i(l)$ for the class probabilities $p_i$ of a classifier. Pixel $i$ has the position $p_i = (u_i, v_i)$ and the color $I_i$. The energy of a labeling $x$ is (Krähenbühl and Koltun 2011, equations 1 to 3)
$$E(x) = \sum_i U_i(x_i) + \sum_{i < j} \mu(x_i, x_j)\, k(i, j),$$
$$k(i, j) = w^{(1)} \exp\Bigl(-\frac{\lVert p_i - p_j \rVert^2}{2 \theta_\alpha^2} - \frac{\lVert I_i - I_j \rVert^2}{2 \theta_\beta^2}\Bigr) + w^{(2)} \exp\Bigl(-\frac{\lVert p_i - p_j \rVert^2}{2 \theta_\gamma^2}\Bigr),$$
with the Potts compatibility $\mu(l, l') = [l \ne l']$ and weights $w^{(1)}, w^{(2)} \ge 0$. The first kernel is the *appearance* kernel, the second the *smoothness* kernel. The model is $P(x) \propto e^{-E(x)}$, a [Markov random field](/markov-random-field/) on the complete graph, with the [Potts model](/potts-model/) as its pair term.

The output is a product distribution $Q(x) = \prod_i Q_i(x_i)$ that approximates $P$, and the labeling $x_i = \arg\max_l Q_i(l)$. Mean field picks $Q$ to make $\mathrm{KL}(Q \| P)$ small. Finding the exact minimum energy labeling is NP-hard for the multi-label Potts energy, and this method does not try.

## The algorithm

The algorithm is Algorithm 1 of Krähenbühl and Koltun (2011), written for the Potts model with the two kernels merged into $k(i, j)$.

```pseudo id=main
DENSE-CRF(U, k, N)            ▷ U_i(l): unary energies; k(i, j): kernel sum, i ≠ j
L1  for each pixel i and label l do Q_i(l) ← exp(-U_i(l)) / Σ_l' exp(-U_i(l'))
L2  repeat N times
L3      for each pixel i and label l do M_i(l) ← Σ_{j ≠ i} k(i, j) Q_j(l)      ▷ message passing
L4      for each pixel i and label l do B_i(l) ← Σ_l' M_i(l') - M_i(l)          ▷ Potts compatibility
L5      for each pixel i and label l do Q_i(l) ← exp(-U_i(l) - B_i(l))           ▷ local update
L6      for each pixel i do divide each Q_i(l) by Σ_l' Q_i(l')                    ▷ normalize
L7  return Q and the labels x_i = argmax_l Q_i(l)
```

Line L4 is the compatibility transform: for the Potts model, the penalty for label $l$ is the total message for all other labels. All pixels update at the same time, from the old $Q$.

**Messages as filtering.** Line L3 is a sum over all pairs, $O(n^2 L)$. For each label, $M_i(l)$ is the value at pixel $i$ of a Gaussian filter applied to the image $Q_\cdot(l)$, minus the value at $i$ itself (equation 5 of the paper). The smoothness kernel is a [Gaussian filter](/gaussian-filter/) in $(u, v)$. The appearance kernel is a Gaussian in the 5D space of position and color, the kernel of the [bilateral filter](/bilateral-filter/). Krähenbühl and Koltun compute both with the permutohedral lattice of Adams, Baek and Davis (2010), which splats the values onto a lattice, blurs on it, and slices back (Algorithm 2 of the paper). Its cost is linear in $n$, and it approximates the sum.

## Example

Take one row of 4 pixels with gray values $0, 0, 10, 10$ and two labels. A classifier gives the probabilities $0.2, 0.6, 0.7, 0.9$ for label 1, so $U_i = (-\log(1 - p_i), -\log p_i)$. Pixel 1 has the color of pixel 0 but leans to label 1. The parameters are $w^{(1)} = 2$, $\theta_\alpha = 2$, $\theta_\beta = 3$, $w^{(2)} = 0.5$, $\theta_\gamma = 1$. The kernel values from pixel 1 are
$$k(1, 0) = 2 e^{-1/8} + 0.5 e^{-1/2} \approx 2.0683, \quad k(1, 2) = 2 e^{-1/8 - 100/18} + 0.5 e^{-1/2} \approx 0.3101, \quad k(1, 3) \approx 0.0724.$$
The color difference of 10 almost removes the appearance term between pixels 1 and 2.

In the first iteration, with $Q_0 = (0.8, 0.2)$, $Q_2 = (0.3, 0.7)$ and $Q_3 = (0.1, 0.9)$:
- $M_1(0) = 2.0683 \cdot 0.8 + 0.3101 \cdot 0.3 + 0.0724 \cdot 0.1 \approx 1.7549$ and $M_1(1) \approx 0.6959$.
- The Potts penalties are $B_1(0) = M_1(1) \approx 0.6959$ and $B_1(1) = M_1(0) \approx 1.7549$.
- The new energies are $0.9163 + 0.6959 = 1.6122$ for label 0 and $0.5108 + 1.7549 = 2.2657$ for label 1, so $Q_1(1) = 1 / (1 + e^{0.6535}) \approx 0.3422$.

Pixel 1 now prefers label 0, like its neighbor with the same color.

| iteration | $Q_0(1)$ | $Q_1(1)$ | $Q_2(1)$ | $Q_3(1)$ | labels | $F(Q)$ |
|---|---|---|---|---|---|---|
| 0 | 0.2000 | 0.6000 | 0.7000 | 0.9000 | 0 1 1 1 | 2.0853 |
| 1 | 0.2815 | 0.3422 | 0.9256 | 0.9541 | 0 0 1 1 | 1.7535 |
| 2 | 0.1224 | 0.4579 | 0.9306 | 0.9808 | 0 0 1 1 | 1.6964 |
| 5 | 0.1324 | 0.2934 | 0.9369 | 0.9815 | 0 0 1 1 | 1.6484 |

$F(Q)$ is the mean field free energy of the correctness section. It stays above $-\log Z \approx 1.2960$, computed by brute force over the 16 labelings. The values of $Q_0(1)$ go up and down, a small sign of the parallel update. The test file checks these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The facts that are proved:
- Lines L3 to L6 compute the mean field equation (equation 4 of the paper) for the Potts model.
- For every product distribution $Q$, the free energy $F(Q) = \mathbb{E}_Q[E] - H(Q)$ equals $\mathrm{KL}(Q \| P) - \log Z$, so $F(Q) \ge -\log Z$.
- With all other pixels fixed, the update of one pixel is the unique minimizer of $F$ over that pixel. So *sequential* updates, one pixel at a time, never increase $F$, and the values of $F$ converge. This is the classical mean field result (Wainwright and Jordan 2008, Section 5). It gives a local result, not the global minimum.
- The *parallel* update of lines L3 to L6 has no such guarantee, as Krähenbühl and Koltun (2013) point out. A two-pixel example with a strong link and opposite unaries makes it swap the beliefs of the two pixels at every step (see the proof). The test file checks it.
- Krähenbühl and Koltun (2013, Section 3) give sufficient conditions under which a parallel scheme converges: positive definite kernels, which the Gaussian kernels are, and a negative semidefinite compatibility, which the Potts model is after a shift by a constant. Their variant of Section 3.2 adds the self term $k(i, i) Q_i(l)$ to each message, and then each parallel update is a step of the concave-convex procedure and does not increase an approximate objective. The proof file proves this.
- The separable blur of the smoothness kernel, minus the self term, gives the exact messages of line L3 for that kernel.

What is not proved: the error of the permutohedral lattice, which is an approximation, and the quality of the labels, which is measured on benchmarks.

## Complexity

The front matter gives the cost with a linear-time filter for the messages, as in the paper, for a fixed feature dimension. The filter is an approximation. With exact messages an iteration costs $O(n^2 L)$ time for line L3 and $O(nL)$ for lines L4 to L6, with $n = WH$. That is $O(N L W^2 H^2)$ for $N$ iterations, in the [real-RAM](/real-ram/) model. With a filter that is linear in $n$, an iteration costs $O(nL)$ times the cost per sample of the filter, so $O(N L W H)$ for fixed feature dimension. Adams, Baek and Davis state that their filter is linear in the input size and polynomial in the dimension of the feature space. Krähenbühl and Koltun also downsample the images before filtering, by a factor tied to the kernel width (Section 5 of their paper). A general compatibility matrix instead of Potts adds $O(n L^2)$ per iteration for line L4. The extra space is $O(nL)$ for $Q$ and the messages, plus the lattice. The number of iterations is a choice; it is not given by a bound.

## Properties

- **Approximate inference.** Mean field gives a product distribution and a labeling, not the minimum energy labeling.
- **Parallel and simple.** Each step is a few filters and per-pixel arithmetic, which suits GPUs.
- **No convergence guarantee for the plain parallel update.** In practice a few iterations are run. That is a heuristic choice, not a result.
- **Edge-preserving.** The appearance kernel lets labels follow color edges, like a bilateral filter of the beliefs.
- **Differentiable.** Each step is smooth in $U$ and in the kernel weights. This is what lets later work train the CRF together with a network.

## Variants and improvements

- **Sequential or damped updates.** Updating a subset of pixels at a time, or mixing the new $Q$ with the old one, avoids oscillation. A sequential schedule has the guarantee of the correctness section, but it is slow with filtering, which works on all pixels at once.
- **Convergent parallel mean field** (Krähenbühl and Koltun 2013). A CCCP form (Section 3.1) and the cheaper concave approximation (Section 3.2) both converge under the conditions above. The same paper learns the kernel parameters by gradient descent through the inference.
- **General compatibilities.** A learned matrix $\mu(l, l')$ lets, for example, "person" and "bicycle" be next to each other at a lower cost than "person" and "sky".
- **CRF as a network layer.** Later work wrote the mean field iterations as layers of a recurrent network and trained them with a convolutional network end to end (CRF-as-RNN), and the DeepLab models used a dense CRF to sharpen network outputs. These are applications of the same update.
- **Other inference.** For a CRF with only neighbor terms, [graph cuts](/image-segmentation-graph-cuts/) find the exact minimum of a binary submodular energy, and alpha-expansion is within a factor 2 of the optimum for Potts. These methods do not scale to all pixel pairs.

## When to use it

Use a dense CRF to sharpen the output of a per-pixel classifier near object boundaries, when the image colors carry the boundary. It adds long-range consistency at a low cost. Do not use it when the classifier is already sharp at boundaries, as many recent networks are; the gain then is small or negative. Do not use it when you need the exact minimum energy labeling or a certificate, and do not use it when the colors of two classes are the same, because the appearance kernel then pulls their labels together.

## Pitfalls

- **Self term.** The message of line L3 excludes $j = i$. A filter that sums over all pixels includes it, with weight $k(i, i) = w^{(1)} + w^{(2)}$. Forgetting to subtract it gives the variant of the 2013 paper, which has different fixed points: in the two-pixel example of the proof, each pixel then keeps its own label.
- **Oscillation.** Strong kernel weights can make the parallel update oscillate. Watch the labels, or use damping.
- **Units of the kernels.** $\theta_\alpha$ and $\theta_\gamma$ are in pixels and $\theta_\beta$ in color units. A change of image size or color range changes the model unless the parameters change with it. Krähenbühl and Koltun report that $w^{(2)} = \theta_\gamma = 1$ worked well on their data; this is a tuned value, not a result.
- **Unary scale.** If $U$ comes from a network with overconfident probabilities, the pairwise terms have little effect. The balance between $U$ and $w^{(m)}$ needs tuning.
- **Free energy is not accuracy.** A lower $F$ means a better fit to the model, not more correct labels.
- **Filter error.** The permutohedral lattice and the downsampling are approximations. Results can differ between implementations, and the messages are not exactly symmetric.

## Implementations

The Python code in `impl/python/dense_crf.py` implements lines L1 to L7 with exact messages over all pixel pairs, for tiny images. It also has the separable Gaussian filter for the smoothness kernel, the sequential update, the variant with the self term, the free energy, and $\log Z$ by brute force. It does not implement the permutohedral lattice. The tests check that the marginals are distributions, that zero weights give the unary softmax, that the filter equals the exact sum, that sequential updates never raise $F$, that $F \ge -\log Z$, the oscillation example, the monotone objective of the variant, and a small denoising example.

## History

Earlier CRFs for segmentation used pairwise terms between neighbor pixels, or terms over regions, because inference over all pairs of pixels was too slow. Krähenbühl and Koltun (2011) noticed that the mean field messages with Gaussian kernels are a high-dimensional Gaussian filter, and used the permutohedral lattice of Adams, Baek and Davis (2010) to compute them in time linear in the number of pixels. They evaluated the method on the MSRC-21 and PASCAL VOC 2010 data sets. In 2013 they studied the convergence of the parallel update and learned the parameters. The method then became a common post-processing step for [semantic segmentation](/semantic-segmentation/) with networks.

## References
