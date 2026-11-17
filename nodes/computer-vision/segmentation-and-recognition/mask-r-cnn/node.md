---
tag: 24WQPY
kind: algorithm
slug: mask-r-cnn
name: Mask R-CNN
aliases:
- Mask RCNN
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Faster R-CNN with RoIAlign and a third head that predicts a binary mask per class for each detection, for instance segmentation.
solves: [instance-segmentation]
model: real-ram
complexity:
  vars: {R: the number of boxes, C: the number of feature channels, P: the side of the RoIAlign output, s: the samples per bin side, A: the total area in pixels of the R boxes, W: the image width, H: the image height}
  time: {worst: O(R C P^2 s^2 + R W H), average: O(R C P^2 s^2 + A), best: O(R C P^2 s^2 + A)}
  space: {extra: O(R C P^2 + R W H)}
properties: {deterministic: true, learned: true, network_cost_excluded: true, quantization_free: true}
history:
  year: 2017
  people: [Kaiming He, Georgia Gkioxari, Piotr Dollar, Ross Girshick]
  note: He, Gkioxari, Dollar and Girshick of Facebook AI Research presented Mask R-CNN at ICCV 2017, where it received the Marr Prize.
prereqs: [faster-r-cnn, roi-pooling, bilinear-interpolation]
see_also: [instance-segmentation, panoptic-segmentation, feature-pyramid-network, box-non-maximum-suppression, intersection-over-union, detection-mean-average-precision, cross-entropy-loss, semantic-segmentation]
sources:
  - paper: doi:10.1109/ICCV.2017.322
    title: "Kaiming He, Georgia Gkioxari, Piotr Dollar and Ross Girshick, Mask R-CNN, IEEE International Conference on Computer Vision (ICCV), 2017 (arXiv 1703.06870)"
    locator: "Section 3 (the mask branch with K masks of m x m, the per-pixel sigmoid, the loss L = L_cls + L_box + L_mask on the k-th mask only, the paragraph RoIAlign with four sampled points per bin), Section 3.1 (training with positive RoIs at IoU 0.5 or more, inference on the top 100 boxes, resize to the box and threshold at 0.5), Section 4.2 and Table 2 (the ablations)"
  - url: https://detectron2.readthedocs.io/en/latest/modules/layers.html
    title: "Detectron2 documentation, detectron2.layers (ROIAlign with the options aligned and sampling_ratio, paste_masks_in_image)"
    locator: "ROIAlign (aligned=True shifts the box by -0.5 before sampling, sampling_ratio of 0 or less is adaptive) and paste_masks_in_image"
  - paper: arxiv:1506.01497
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN, towards real-time object detection with region proposal networks, NIPS 2015"
    locator: the region proposal network and the two-stage detector that Mask R-CNN extends
  - paper: arxiv:1612.03144
    title: "Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan and Serge Belongie, Feature pyramid networks for object detection, CVPR 2017"
    locator: the assignment of each RoI to a pyramid level by its size, used by the FPN backbone of Mask R-CNN
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin et al., Microsoft COCO, common objects in context, European Conference on Computer Vision (ECCV), 2014"
    locator: the instance segmentation task and its mask AP, the benchmark of the Mask R-CNN paper
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.4, Semantic segmentation (the part on instance segmentation)"
---

Mask R-CNN is a two-stage detector for [instance segmentation](/instance-segmentation/). It extends [Faster R-CNN](/faster-r-cnn/) with a third head: for each detected box, a small fully convolutional network predicts $K$ masks of $m \times m$ values, one for each class, and the mask of the predicted class is resized to the box and thresholded. The paper made two changes that are not learned. RoIAlign replaces [RoI pooling](/roi-pooling/): it reads the feature map at points with no rounding, by [bilinear interpolation](/bilinear-interpolation/), so the features stay aligned with the box. The mask loss is a per-pixel sigmoid cross-entropy on the mask of the true class only, so the classes do not compete for a pixel. This page covers RoIAlign, the pasting of the mask into the image and the mask loss, with proofs and code. The network, its training and its cost are outside the page, and the quality of its masks is a benchmark result, not a theorem.

## In plain words

First a detector finds boxes around objects and says what class each object is. For each box, the method reads the features under the box into a small grid of fixed size. It does not snap the box to the coarse grid of the features. It reads values at exact points between grid cells by mixing the four nearest cells. A small network then draws a mask, a square of numbers between 0 and 1 that says which parts of the box belong to the object. It draws one mask for each class and keeps the one for the class that the detector chose. The method stretches this square to the size of the box, puts it in the image, and marks the pixels where the value is at least one half.

## The problem

The input of the non-learned steps is:

- a feature map $F$ with $C$ channels, each a grid of $W_F \times H_F$ cells, from a backbone network with stride $S$ pixels per cell;
- for each of $R$ boxes, a box $b = (x_1, y_1, x_2, y_2)$ in image coordinates, a class $k$ and $K$ mask logit grids of $m \times m$, from the heads of the network;
- the image size $W \times H$, the output size $P$ of RoIAlign, the number $s$ of samples per bin side and the threshold $\theta$.

The center of pixel $(u, v)$ is the point $(u, v)$, and values are read as $F[v][u]$. A box in image coordinates goes to feature coordinates by $x \mapsto (x + \tfrac12)/S - \tfrac12$, which keeps the cell centers aligned (Lemma 2 of the proof).

The output is, for each box, a $P \times P$ feature grid per channel for the heads, and a binary mask of $W \times H$ pixels. In training there is also the mask loss of each positive box.

## The algorithm

```pseudo id=main
ROI-ALIGN(F, b, P, s)                      ▷ b = (x1, y1, x2, y2) in feature coordinates
L1  bw ← (x2 - x1) / P ; bh ← (y2 - y1) / P
L2  for each bin (r, c) with 0 ≤ r, c < P do
L3      acc ← 0
L4      for each sample (a, d) with 0 ≤ a, d < s do
L5          y ← y1 + (r + (a + 1/2)/s) bh ; x ← x1 + (c + (d + 1/2)/s) bw
L6          acc ← acc + BILINEAR(F, x, y)     ▷ 0 if the point is more than 1 cell outside
L7      out[r][c] ← acc / s^2

PASTE-MASK(M, b, W, H, θ)                  ▷ M is m × m, b in image coordinates
L8  for each pixel (u, v) with x1 ≤ u < x2, y1 ≤ v < y2, 0 ≤ u < W, 0 ≤ v < H do
L9      mx ← (u - x1) m / (x2 - x1) - 1/2 ; my ← (v - y1) m / (y2 - y1) - 1/2
L10     out[v][u] ← 1 if BILINEAR(M, mx, my) ≥ θ, else 0    ▷ clamp to the mask, no zero rule
L11 return out
```

Lines L1 to L7 cut the box into $P \times P$ equal bins and average $s \times s$ bilinear samples at the centers of equal sub-rectangles of each bin. Nothing is rounded. The paper uses four samples per bin, $s = 2$, and allows the maximum or the average; the Detectron code and this page use the average. BILINEAR mixes the four nearest cells, clamps points that are less than one cell outside the map, and gives 0 for points further out, as the Detectron code does.

Lines L8 to L11 run at inference. Each pixel center in the box goes to mask coordinates so that the center of each of the $m \times m$ cells of the box lands on the matching mask value. The mask is that of the predicted class $k$, after the sigmoid, so $M = \sigma(\text{logits}[k])$. The paper thresholds at $\theta = 0.5$.

The mask loss for a positive box of true class $k$ with target $t$ ($m \times m$ values in $\{0, 1\}$) is the mean over the $m^2$ cells of $\log(1 + e^z) - t z$, where $z$ is the logit of mask $k$. The total loss is $L = L_{\mathrm{cls}} + L_{\mathrm{box}} + L_{\mathrm{mask}}$. The target is the ground-truth mask of the object matched to the box, cut to the box and resampled to $m \times m$. A box is positive if its [IoU](/intersection-over-union/) with a ground-truth box is at least 0.5.

The network around these steps, from Section 3 of the paper: a backbone (ResNet with a C4 head, or ResNet with a [feature pyramid network](/feature-pyramid-network/)) gives the feature map, a region proposal network gives the boxes, and the box head classifies and refines them. The mask head is a small stack of convolutions and a deconvolution on the RoIAlign output, and its masks are $28 \times 28$ in the FPN design of Table 2e. At inference the box head runs first, then [non-maximum suppression](/box-non-maximum-suppression/), and the mask head runs only on the top 100 boxes.

## Example

Take a $4 \times 4$ feature map with one channel, $F[v][u] = u + 4v$, and the box $(0.5, 0.5, 2.5, 2.5)$ with $P = 2$ and $s = 2$. Then $b_w = b_h = 1$. Bin $(0, 0)$ has samples at $x, y \in \{0.75, 1.25\}$. Their values are $0.75 + 3$, $1.25 + 3$, $0.75 + 5$ and $1.25 + 5$, and the mean is 5, the value at the bin center $(1, 1)$. The full output is

$$\begin{pmatrix} 5 & 6 \\ 9 & 10 \end{pmatrix}.$$

Move the box by 0.1 to the right, to $(0.6, 0.5, 2.6, 2.5)$: the output becomes $5.1, 6.1, 9.1, 10.1$. Move it by 0.01 to the left, to $(0.49, 0.5, 2.49, 2.5)$: the output becomes $4.99, 5.99, 8.99, 9.99$. Each output follows the box.

Quantized RoI max pooling, which rounds the box to whole cells (half up) and takes the maximum of each bin, gives $\begin{pmatrix} 10 & 11 \\ 14 & 15 \end{pmatrix}$ for the first box and $\begin{pmatrix} 9 & 10 \\ 13 & 14 \end{pmatrix}$ for the box moved by 0.01. A move of 0.01 cell changes every output by 1.

For the paste, take the $2 \times 2$ mask $\begin{pmatrix} 0.9 & 0.2 \\ 0.8 & 0.1 \end{pmatrix}$ and the box $(-0.5, -0.5, 3.5, 3.5)$, which covers the pixels 0 to 3 in both directions, in a $4 \times 4$ image. Pixel $u = 1$ goes to $m_x = 1.5 \cdot 2/4 - 0.5 = 0.25$, and pixel $u = 2$ to $m_x = 0.75$. In row $v = 0$, $m_y = -0.25$ is clamped to 0, so pixel $(1, 0)$ reads $0.75 \cdot 0.9 + 0.25 \cdot 0.2 = 0.725 \ge 0.5$ and pixel $(2, 0)$ reads $0.25 \cdot 0.9 + 0.75 \cdot 0.2 = 0.375 < 0.5$. In row $v = 3$, pixel $(1, 3)$ reads $0.75 \cdot 0.8 + 0.25 \cdot 0.1 = 0.625$ and pixel $(2, 3)$ reads $0.275$. The pasted mask is 1 in columns 0 and 1 and 0 in columns 2 and 3, in all four rows.

## Correctness

The non-learned steps have proofs, in `proofs/correctness.md`. These are theorems:

- **Bilinear sampling.** Each sample is a convex combination of at most four map values, it is exact for a map that is affine in the cell index, and it is Lipschitz in the sample point with the largest difference of neighboring cells as the constant.
- **RoIAlign.** The samples are the midpoint rule for the mean of the interpolated map over each bin. On an affine map each output is the value at the bin center. Each output is a Lipschitz function of the box, while samples stay inside the map, and a shift of map and box by whole cells does not change it. RoI pooling has none of these, because of the rounding.
- **Coordinates.** The map $x \mapsto (x + \tfrac12)/S - \tfrac12$ sends the pixels of a feature cell onto that cell, with centers on centers.
- **Pasting.** Exactly the pixels whose centers are in the half-open box are visited. The centers of the $m \times m$ cells of the box read the matching mask values. For a mask that is 1 on the left half and 0 on the right, the pasted edge is at the middle of the box, with no shift of half a mask cell.
- **Mask loss.** The per-pixel term is the binary cross-entropy of the sigmoid, convex in the logit with gradient $\sigma(z) - t$, and it does not depend on the masks of the other classes.

The quality of the masks is a benchmark result. The paper reports mask AP on COCO, with ablations in Table 2 that compare RoIAlign with RoI pooling and independent sigmoid masks with a per-pixel softmax over the classes. In both cases the variant of this page gave higher AP in the setting of the paper.

## Complexity

The model is the real RAM. The cost of the backbone, the region proposals and the heads is outside the page. Let $R$ be the number of boxes, $C$ the number of channels and $A$ the total area of the boxes in pixels.

- RoIAlign, lines L1 to L7, makes $P^2 s^2$ samples per box, each of cost $O(1)$ per channel: $O(R C P^2 s^2)$ in total.
- Pasting, lines L8 to L11, costs $O(1)$ per pixel in the box, so $O(A)$ in total, and $A \le R W H$.
- The mask loss costs $O(m^2)$ per positive box. Only the mask of the true class is read.

The output takes $O(R C P^2)$ for the RoI features and $O(R W H)$ for full-size masks. Implementations often keep the $m \times m$ masks with their boxes and paste only when needed. The paper reports that the system runs at about 5 frames per second; that is a measurement on the GPU of 2017 and includes the network.

## Properties

- **No quantization.** RoIAlign never rounds a coordinate. Its output is a continuous function of the box, so small errors of the box give small changes of the features.
- **Masks per class.** The head predicts $K$ masks and the class head chooses one. The loss of a box touches only one of them.
- **Masks at fixed resolution.** The mask has $m \times m$ values whatever the box size, so large objects get coarse masks. The paste interpolates, but it cannot add detail.
- **Box-limited masks.** Pixels outside the box are always 0. An error of the box cuts the mask.
- **Overlap.** Masks of different instances can overlap. A panoptic output needs an extra rule to give each pixel to one segment.
- **Learned.** The masks depend on the training data and the weights. There is no guarantee for a given image.

## Variants and improvements

- **RoIAlign options.** Detectron2 has an option aligned that shifts the box by half a pixel before sampling, as on this page, and a sampling ratio that can adapt the number of samples to the box size. The first Detectron code did not shift.
- **Keypoints.** The paper also predicts human keypoints with the same structure: one $m \times m$ map per keypoint with a single hot pixel and a softmax over the pixels.
- **Panoptic FPN.** A semantic segmentation branch on the same FPN features adds stuff classes, which gives a [panoptic segmentation](/panoptic-segmentation/).
- **Better masks.** Later work rescores masks by their predicted IoU, refines the mask at the boundary, or cascades several box heads.
- **Single-stage and set-based methods.** Other instance segmentation methods predict masks without RoIs, for example from dense grids of mask coefficients. Set-based detectors in the style of [DETR](/detr/) predict a set of masks with a matching loss.

## When to use it

Use Mask R-CNN when you need one mask per object, of a known set of classes, and a GPU is available: counting cells or people, robot grasping, or the instance part of a panoptic system. It is a strong and well documented baseline, with public code and weights. If you need only class labels per pixel, use [semantic segmentation](/semantic-segmentation/). If you need fine boundaries on large objects, add a refinement step, because of the $m \times m$ masks. Without a GPU, or without training data, classical segmentation with [graph cuts](/image-segmentation-graph-cuts/) or [watershed](/watershed-segmentation/) on a given box may be enough.

## Pitfalls

- **The half-pixel offset.** Mapping a box with $x / S$ instead of $(x + \tfrac12)/S - \tfrac12$ shifts all features by up to half a cell. Use the same convention in training and at inference.
- **The paste offset.** Without the $-\tfrac12$ of line L9 the pasted mask moves by half a mask cell, which is several pixels for large boxes.
- **Pasting at the wrong size.** Paste the mask with the box of the final, refined detection, not the proposal that the mask head saw, as the paper does at inference.
- **Softmax across classes.** A softmax over the $K$ masks at each pixel makes the classes compete, which the paper reports as worse.
- **Samples outside the map.** Boxes that reach far outside the image get zeros for the far samples. This is a rule of the code, not of the paper, and implementations differ.
- **Overlapping masks.** Instance masks are not a partition. Before computing a panoptic score, resolve the overlaps, for example by detection score.

## Implementations

The network is outside this page. The Python code in `impl/python/mask_r_cnn.py` implements only the steps that are not learned: bilinear sampling with the Detectron border rule, RoIAlign, the map from image to feature coordinates, the paste of an $m \times m$ mask into the image, and the mask loss. The tests use feature maps and logits that they build by hand or with a fixed seed. They check the example above, the tent-function form of bilinear sampling, exact values on constant and affine maps, invariance to a shift by whole cells, the bounded change under a small move of the box against the jump of a quantized RoI pooling, the zero rule far outside the map, the pasted pixel set of full and half masks, and that the loss ignores the masks of the other classes.

## History

R-CNN (2014) classified warped crops of proposals, Fast R-CNN (2015) shared the network over the image with RoI pooling, and Faster R-CNN (2015) learned the proposals. Instance segmentation before 2017 often built masks from segment proposals and then classified them. He, Gkioxari, Dollar and Girshick (2017) added a mask head to Faster R-CNN in parallel with the box head and fixed the misalignment of RoI pooling with RoIAlign. The method won the Marr Prize at ICCV 2017. It became the standard baseline on COCO, and Detectron and Detectron2 made its code widely used.

## References
