---
tag: TNJGM1
kind: algorithm
slug: single-shot-multibox-detector
name: Single shot multibox detector
aliases:
- SSD detector
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Predict class scores and offsets for default boxes on several feature maps of different resolutions in one pass, followed by non-maximum suppression.
solves: [object-detection]
model: real-ram
complexity:
  vars: {D: the number of default boxes, C: the number of object classes}
  time: {worst: "O(C D^2)"}
  space: {extra: "O(C D)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu, Alexander C. Berg]
  note: "Presented at ECCV 2016. It removed the proposal stage and the per-region resampling of two-stage detectors and reached the accuracy of Faster R-CNN on PASCAL VOC at real-time speed."
prereqs: [anchor-boxes, anchor-assignment, bounding-box-regression, box-non-maximum-suppression]
see_also: [faster-r-cnn, yolo-detector, feature-pyramid-network, focal-loss, detr, intersection-over-union, cross-entropy-loss, data-augmentation]
sources:
  - paper: doi:10.1007/978-3-319-46448-0_2
    title: "Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu and Alexander C. Berg, SSD: single shot multibox detector, ECCV 2016, LNCS 9905, 21-37"
    locator: "Section 2.1, Model (multi-scale feature maps, convolutional predictors, default boxes); Section 2.2, Training (matching strategy with jaccard overlap above 0.5 and the best box for each truth, training objective with alpha = 1, scales s_min = 0.2 and s_max = 0.9 with ratios 1, 2, 3, 1/2, 1/3 and an extra box of scale sqrt(s_k s_k+1), hard negative mining at 3:1, data augmentation); Section 3, Experimental results (8732 boxes for SSD300; inference with confidence 0.01, NMS at 0.45 per class and the top 200 detections; SSD300 74.3 mAP at 59 FPS and SSD512 76.9 mAP on VOC 2007 test)"
  - url: https://arxiv.org/abs/1512.02325
    title: "Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu and Alexander C. Berg, SSD: single shot multibox detector, arXiv 1512.02325"
    locator: "the extended version, with the same Sections 2 and 3"
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1.1, Anchors (the anchors on one feature map that SSD extends to several maps)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

The single shot multibox detector (SSD) finds objects with one pass of a convolutional network and no proposal stage. It attaches small convolutional predictors to several feature maps of falling resolution, for example 6 maps of $38 \times 38$ down to $1 \times 1$ cells for an input of $300 \times 300$. Each cell of each map has a fixed set of default boxes, which are [anchor boxes](/anchor-boxes/) of a few aspect ratios at a scale that grows from map to map. For every default box the network outputs $C + 1$ class scores, the background included, and four offsets in the encoding of [bounding box regression](/bounding-box-regression/). At test time the offsets are decoded, and [non-maximum suppression](/box-non-maximum-suppression/) is applied to each class. SSD300 has 8732 default boxes and reached 74.3 percent mAP on PASCAL VOC 2007 at 59 frames per second. That was as accurate as [Faster R-CNN](/faster-r-cnn/) with the same backbone and several times faster.

## In plain words

SSD covers the image with many fixed boxes of several sizes and shapes, at every cell of several grids, from fine to coarse. For each box the network says at once what is in it, background included, and how to move and stretch the box to fit the object. No second look at the image is needed. Small objects are found on the fine grids and large objects on the coarse grids. In training, each true object is given the boxes that overlap it well. All other boxes learn to say "background", but only the hardest of them are used, three for each object box, so that the many easy background boxes do not swamp the loss. At test time, near copies of each class are removed.

## The problem

The input is an image and a trained network that gives, for every default box $d$, a vector of $C + 1$ class scores and four offsets $\delta_d$. The output is a list of boxes with a class and a score, judged by [detection mean average precision](/detection-mean-average-precision/). This page gives the steps that are not learned: the default boxes, the decoding and the NMS at test time, and the matching, the hard negative mining and the loss in training. It proves facts about these steps. The network is outside the page.

## The algorithm

```pseudo id=main
SSD-DETECT(I, network, τ_conf = 0.01, τ = 0.45, K = 200)
L1  for every default box d: class scores z_d and offsets δ_d ← network(I)   ▷ outside
L2  D ← the default boxes of every cell of every feature map
L3  p_d ← SOFTMAX(z_d) for every d ∈ D
L4  b_d ← DECODE(d, δ_d) for every d ∈ D
L5  for each class c = 1, ..., C
L6      greedy NMS at IoU τ of the boxes b_d with p_{d,c} > τ_conf, by score p_{d,c}
L7  merge the boxes kept for all classes
L8  return the K boxes of highest score
```

**Default boxes.** With $m$ feature maps, map $k$ has the scale
$$s_k = s_{min} + \frac{s_{max} - s_{min}}{m - 1}(k - 1), \qquad s_{min} = 0.2,\ s_{max} = 0.9,$$
as a fraction of the image side. For an aspect ratio $a$ in $\{1, 2, 3, \tfrac12, \tfrac13\}$ the box has width $s_k\sqrt{a}$ and height $s_k/\sqrt{a}$. For ratio 1 there is one more box of scale $s'_k = \sqrt{s_k s_{k+1}}$. The boxes of a map with $f_k \times f_k$ cells are centered at $((j + 0.5)/f_k, (i + 0.5)/f_k)$. In SSD300, the maps of $38^2, 19^2, 10^2, 5^2, 3^2, 1^2$ cells have 4, 6, 6, 6, 4 and 4 boxes per cell, which gives $5776 + 2166 + 600 + 150 + 36 + 4 = 8732$ boxes. The paper sets the scale of the first map, conv4_3, to 0.1, and does not give $s_{m+1}$. The code takes 1 for $s_{m+1}$ by default.

**Matching.** Each ground truth box is first matched to the default box of best IoU. Then every other default box whose IoU with some truth is above 0.5 is matched to the truth of best IoU. Matched boxes are positives and the rest are negatives. The code does the first step as a greedy bipartite matching: it takes the pair of largest IoU among the unmatched boxes and truths, again and again. So two truths never share their step-1 box. The [anchor assignment](/anchor-assignment/) page compares this rule with others.

**Loss.** With $N$ positives,
$$L = \frac{1}{N}\bigl(L_{conf} + \alpha L_{loc}\bigr), \qquad \alpha = 1,$$
where $L_{conf}$ is the softmax [cross-entropy](/cross-entropy-loss/) of the positives for their class and of the chosen negatives for background, and $L_{loc}$ is the smooth L1 loss of the positives between the offsets and the encoded truth. $L = 0$ when $N = 0$.

**Hard negative mining.** The negatives are sorted by their background loss, and only the largest ones are kept, so that negatives and positives are at most 3:1.

## Example

Take boxes in pixel units, for easy numbers. The ground truth boxes are $G_1 = (0, 0, 10, 10)$ and $G_2 = (20, 0, 30, 10)$. The default boxes are $D_0 = (0, 0, 10, 10)$, $D_1 = (0, 0, 10, 8)$, $D_2 = (0, 0, 10, 4)$, $D_3 = (25, 0, 35, 10)$ and $D_4 = (40, 0, 50, 10)$.

1. The IoUs with $G_1$ are 1, 0.8, 0.4, 0, 0. With $G_2$, only $D_3$ overlaps, with IoU $50/150 = 1/3$.
2. Step 1 matches $D_0$ to $G_1$ (IoU 1), then $D_3$ to $G_2$ (IoU 1/3). $D_3$ is positive only through this step.
3. Step 2 matches $D_1$ to $G_1$ (0.8 is above 0.5). $D_2$ (0.4) and $D_4$ (0) are negatives.
4. So the labels are $G_1, G_1, -, G_2, -$, with $N = 3$, and up to 9 negatives are kept, here both.

For the mining alone: with 1 positive and 5 negatives of background loss 0.1, 2.0, 0.5, 1.2 and 0.05, the 3 kept negatives are those with loss 2.0, 1.2 and 0.5.

For the loss, take four default boxes of side 0.5 that tile the unit square, a truth equal to the top left one of class 1, and $\alpha = 1$. The class probabilities are $(1/4, 3/4)$ for the positive and $(1/2, 1/2)$, $(3/4, 1/4)$ and $(1/4, 3/4)$ for the three negatives, with background first. The positive has offsets $(0.5, 0, 0, 0)$ against a target of zero. Then $L_{conf}$ of the positive is $-\ln(3/4)$, and $L_{loc} = \operatorname{smooth}_{L_1}(0.5) = 0.125$. With a ratio of 1 the only kept negative is the one of loss $\ln 4$, and $L = \ln(16/3) + 0.125 \approx 1.799$. With the ratio of 3 all three negatives count, and $L$ grows by $\ln 2 + \ln(4/3)$.

## Correctness

The network has no correctness theorem; its accuracy is measured. [The proof page](proofs/correctness.md) shows these facts for the steps that are not learned:

1. **Default boxes.** Every box of map $k$ with ratio $a$ has area $s_k^2$ and width over height $a$, and the count is $\sum_k f_k^2 n_k$.
2. **Matching.** The boxes of step 1 are distinct. A truth gets no box only when every box that overlaps it went to another truth in step 1. Every box of IoU above 0.5 with some truth is positive, and every negative has IoU at most 0.5 with every truth.
3. **Hard negatives.** The kept negatives are the $\min(3N, n_-)$ negatives of largest background loss.
4. **Output.** At most $K$ detections, sorted by score, each above $\tau_{conf}$, with pairwise IoU at most $\tau$ inside each class.

## Complexity

The network is outside. With $D$ default boxes and $C$ classes, the softmax costs $O(DC)$ and the decoding $O(D)$. Greedy NMS of one class costs $O(D \log D)$ to sort and $O(D^2)$ to compare in the worst case, so the test-time steps cost $O(C D^2)$, and the final sort $O(CD \log(CD))$. Implementations keep only a few hundred boxes of each class before NMS, which caps the quadratic term. In training, the matching costs $O(DG)$ for the IoUs of $G$ truths. The greedy step 1 of the code costs $O(D G^2)$, and the mining costs $O(D \log D)$. The extra space is $O(CD)$ for the probabilities.

## Properties

- **One stage.** No proposals and no per-region pooling, so the cost does not grow with the number of objects, apart from NMS.
- **Several maps.** Each map handles a range of sizes. The fine maps come early in the network and have weak features, so small objects are the weak point.
- **Translation-equivariant on each map.** The same default boxes and predictors are used at every cell.
- **Deterministic at test time; not exact,** since it is a learned method.

## Variants and improvements

- **DSSD and FPN.** A top-down path gives the fine maps stronger features. The [feature pyramid network](/feature-pyramid-network/) is the most used form.
- **RetinaNet.** It replaces hard negative mining with the [focal loss](/focal-loss/), which weights all negatives by how hard they are.
- **SSD512.** A larger input and one more map give 76.9 percent mAP on VOC 2007 test.
- **Lighter backbones.** MobileNet with SSD heads is a common detector on phones.
- **Anchor-free one-stage detectors.** FCOS and CenterNet predict from points rather than default boxes. [DETR](/detr/) predicts a set and needs neither defaults nor NMS.

## When to use it

Use SSD when one fast pass matters more than the last points of accuracy, and the objects are not mostly tiny. For small objects use a detector with a feature pyramid. For crowded scenes where NMS removes true boxes, consider [soft-NMS](/soft-nms/) or a set-based detector.

## Pitfalls

- **Box encoding scale.** Many implementations divide the center offsets by 0.1 and the log sizes by 0.2. Train and test must use the same scale.
- **Boxes in image fractions.** The default boxes are relative to the image, so a non-square image has non-square boxes for ratio 1, unless the image is resized to a square as in the paper.
- **Data augmentation.** The paper reports that its sampling of random crops raised mAP by 8.8 points. Without it, SSD is much weaker on small and large objects.
- **The forced matches.** Step 1 can make a box of low IoU positive. Without step 1, small truths may have no positive at all.
- **NMS threshold per class.** NMS at 0.45 inside each class does not remove a box of a second class at the same place.
- **Negatives swamping the loss.** Without mining or a focal loss, the many easy background boxes dominate $L_{conf}$.

## Implementations

The network is outside this page. The Python code takes the class scores and offsets of every default box as inputs, and the tests build them by hand or with a fixed seed. The code implements the scales and the default boxes, the encoding with optional scales of the offsets, the two-step matching, hard negative mining, the loss, and the detection of lines L1 to L8. The tests check the 8732 boxes of SSD300 and the shapes of the boxes, the matching example above and a case where step 1 gives a second truth its own box, the matching rule on random boxes, the mining and loss examples, the round trip of encoding and decoding, the properties of the output on random scores, and a run that recovers a known box.

## History

MultiBox (Erhan, Szegedy, Toshev and Anguelov 2014) predicted class-agnostic boxes from priors with a network, and [Faster R-CNN](/faster-r-cnn/) (2015) put anchors on one feature map. [YOLO](/yolo-detector/) (2016) made detection one pass but predicted from a coarse grid with a few boxes per cell. Liu, Anguelov, Erhan, Szegedy, Reed, Fu and Berg put SSD on arXiv in December 2015 and presented it at ECCV 2016. They combined default boxes of several shapes on several feature maps with the matching of MultiBox and hard negative mining. SSD300 reached 74.3 percent mAP at 59 frames per second on VOC 2007 test, which made real-time detection at the accuracy of two-stage methods practical. Its multi-scale prediction led to the [feature pyramid network](/feature-pyramid-network/) and RetinaNet.

## References
