---
tag: 5WFTBK
kind: algorithm
slug: faster-r-cnn
name: Faster R-CNN
aliases:
- region proposal network
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Fast R-CNN with a region proposal network that scores and refines anchors on the shared feature map, making detection one trainable network.
solves: [object-detection, object-proposals]
model: real-ram
complexity:
  vars: {A: the number of anchors, N: the number of boxes kept before NMS, P: the number of proposals, K: the number of object classes}
  time: {worst: "O(A log A + N P + K P^2)"}
  space: {extra: "O(A + P K)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun]
  note: "Presented at NIPS 2015 and extended in IEEE TPAMI in 2017. The region proposal network made proposals almost free and became the first stage of most two-stage detectors."
prereqs: [fast-r-cnn, anchor-boxes, anchor-assignment, bounding-box-regression]
see_also: [r-cnn, roi-pooling, feature-pyramid-network, mask-r-cnn, single-shot-multibox-detector, yolo-detector, box-non-maximum-suppression, object-proposals]
sources:
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1, Region proposal networks (3.1.1 Anchors: k = 9 from 3 scales and 3 aspect ratios; 3.1.2 Loss function: IoU above 0.7 or the best anchor for a box, below 0.3 negative, lambda = 10; 3.1.3 Training RPNs: 256 anchors per image, up to 1:1); Section 3.2, Sharing features (4-step alternating training); Section 3.3, Implementation details (cross-boundary anchors ignored in training, NMS at 0.7, about 2000 proposals); Section 4.1, Experiments on PASCAL VOC (Table 3: mAP 69.9 on VOC 2007 test trained on 07, 73.2 on 07+12; Table 5: 198 ms per image with VGG16, 10 ms for the proposals, 5 fps)"
  - url: https://arxiv.org/abs/1506.01497
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, NIPS 2015 (arXiv 1506.01497)"
    locator: "the conference version, with the same Section 3"
  - paper: doi:10.1109/ICCV.2015.169
    title: "Ross Girshick, Fast R-CNN, ICCV 2015, 1440-1448"
    locator: "Section 2, the detection network that Faster R-CNN keeps as its second stage"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Faster R-CNN is a two-stage detector in which the proposals come from the network itself. The first stage, the region proposal network (RPN), slides a small network over the convolutional feature map. At each position it looks at $k$ [anchor boxes](/anchor-boxes/) of fixed sizes and shapes, 9 in the paper, and for each anchor predicts an objectness score and four offsets in the encoding of [bounding box regression](/bounding-box-regression/). The decoded boxes are clipped to the image, ranked, and thinned by [non-maximum suppression](/box-non-maximum-suppression/) at IoU 0.7, and the best few hundred become the proposals. The second stage is [Fast R-CNN](/fast-r-cnn/) on the same feature map. Since both stages share the convolutional layers, a proposal costs almost nothing, and with VGG16 the whole detector runs at 5 frames per second on a GPU. "Region proposal network" is the name of the first stage only, not of the detector.

## In plain words

Fast R-CNN was quick, but it still needed a slow outside method to suggest where objects might be. Faster R-CNN lets the same network make those suggestions. It places a fixed set of boxes, the anchors, at every cell of the feature map: small, medium and large, and wide, square and tall. For each anchor a small layer answers two questions: is there an object here, and how should this box move and stretch to fit it? The best few hundred moved boxes, with near copies removed, go to the second stage. That stage pools the features under each box, names the object, and fixes the box once more. Both stages read one feature map, so the suggestions are almost free.

## The problem

The input is an image and a trained network: a backbone that gives a feature map of stride $\sigma$ pixels (16 for VGG16), an RPN head that gives, for each of the $k$ anchors at each cell, an objectness score and four offsets, and a Fast R-CNN head that gives class scores and offsets for each proposal. The output is a list of boxes with a class and a score. The quality depends on the training and is measured by [detection mean average precision](/detection-mean-average-precision/). This page gives the steps that are not learned and proves facts about them; the network is outside.

## The algorithm

```pseudo id=main
FASTER-R-CNN-DETECT(I, network, N_pre, N_post, τ_rpn, τ)
L1  F ← backbone(I); (o_a, δ_a) ← RPN head on F for every anchor a     ▷ network, outside
L2  A ← the k anchors at the center of every cell of F
L3  B_a ← CLIP(DECODE(a, δ_a)) to the image, for every a ∈ A
L4  drop every box with a side below the minimum size
L5  keep the N_pre boxes of highest o_a
L6  P ← greedy NMS at IoU τ_rpn = 0.7, keeping at most N_post boxes
L7  for each r ∈ P: RoI pooling on F, class scores p_r and offsets t_r   ▷ Fast R-CNN head
L8  return, for each class, NMS at τ of the boxes DECODE(r, t_r^k) with scores p_{r,k}
```

**Anchors.** The paper uses 3 sizes, areas $128^2$, $256^2$ and $512^2$ pixels, and 3 aspect ratios, 1:1, 1:2 and 2:1, so $k = 9$ anchors at each cell. For a feature map of $W \times H$ cells there are $WHk$ anchors, about 20000 for an image of about $1000 \times 600$ pixels. The anchors and the head are the same at every cell, so a shifted object gives a shifted proposal. The [anchor boxes](/anchor-boxes/) page treats the choice of sizes and shapes.

**Training the RPN.** An anchor is positive if its IoU with some ground truth box is above 0.7, or if it is the anchor of largest IoU for some ground truth box, so that every box has at least one positive. It is negative if its IoU is below 0.3 with every box, and ignored otherwise. Anchors that cross the image border are ignored in training, which leaves about 6000 of the 20000. Each image gives a mini-batch of 256 anchors with up to half positives, filled with negatives. The loss is

$$L = \frac{1}{N_{cls}} \sum_i L_{cls}(p_i, p_i^*) + \lambda \frac{1}{N_{reg}} \sum_i p_i^* L_{reg}(t_i, t_i^*),$$

with the log loss for $L_{cls}$, smooth L1 for $L_{reg}$, $p_i^* = 1$ for positives, $N_{cls} = 256$, $N_{reg}$ the number of anchor locations (about 2400) and $\lambda = 10$. The [anchor assignment](/anchor-assignment/) page compares this rule with those of SSD, RetinaNet and ATSS.

**Sharing the features.** The paper trains the two stages in four steps: train the RPN, train Fast R-CNN on its proposals, fix the shared layers and fine-tune the RPN layers, and then fine-tune the Fast R-CNN layers. The paper also describes an approximate joint training of both losses at once, which gives close results with 25 to 50 percent less training time and is in its released Python code.

**Proposals at test time.** The cross-border boxes are clipped, not dropped. NMS at 0.7 leaves about 2000 proposals per image; the detector is trained on 2000 and tested with the best 300.

## Example

Take an image of $64 \times 32$ pixels and four anchors of $32 \times 32$ in a row, centered at $x = 8, 24, 40, 56$: $(-8, 0, 24, 32)$, $(8, 0, 40, 32)$, $(24, 0, 56, 32)$ and $(40, 0, 72, 32)$. Let the RPN give the scores 0.9, 0.8, 0.3 and 0.6 and zero offsets.

1. Clipping makes the first box $(0, 0, 24, 32)$ and the last $(40, 0, 64, 32)$; the middle two are inside.
2. With a minimum size of 16 all four stay.
3. NMS at the paper's $\tau_{rpn} = 0.7$ keeps all four, since next boxes overlap by IoU $512/1280 = 0.4$ and the others less. The proposals are the four boxes in the order 0.9, 0.8, 0.6, 0.3.
4. With $\tau_{rpn} = 0.3$ instead, NMS keeps $(0, 0, 24, 32)$, drops $(8, 0, 40, 32)$ at IoU 0.4, keeps $(40, 0, 64, 32)$, and drops $(24, 0, 56, 32)$ at IoU 0.4 with it.

If the offsets of the third anchor are $(0.5, 0, \ln 2, 0)$, its center moves by half a width to $x = 56$ and its width doubles to 64, giving $(24, 0, 88, 32)$ before the clip and $(24, 0, 64, 32)$ after.

For training, take the image $40 \times 10$, anchors $(0, 0, 10, 10)$, $(5, 0, 15, 10)$, $(10, 0, 20, 10)$, $(20, 0, 30, 10)$ and $(35, 0, 45, 10)$, and ground truth boxes $(4, 0, 14, 10)$ and $(21, 0, 25, 4)$. The IoUs with their best box are 3/7, 9/11, 1/4, 4/25, and the last anchor crosses the border. The labels are: ignored, positive, negative, positive (it is the best anchor of the small box, though 4/25 is below 0.3), ignored.

## Correctness

The network has no correctness theorem; its accuracy is measured. [The proof page](proofs/correctness.md) shows for the steps that are not learned:

1. **Anchors.** The anchors at a cell have the stated areas and aspect ratios and are centered on the cell, so a shift of the image by a multiple of $\sigma$ shifts the anchor set onto itself.
2. **Proposals.** The output has at most $N_{post}$ boxes, sorted by score, inside the image, no smaller than the minimum, and with pairwise IoU at most $\tau_{rpn}$.
3. **Labels.** Every ground truth box with an inside anchor of positive IoU has at least one positive anchor, positives and negatives are disjoint, and anchors across the border are ignored.
4. **Sampling.** The batch has at most half positives and at most 256 anchors, and every sampled label agrees with the label rule.

## Complexity

The backbone and the heads are outside the page. Decoding and clipping cost $O(A)$ for $A$ anchors, the minimum-size filter $O(A)$, and the sort $O(A \log A)$ (a selection of the top $N$ would give $O(A)$). Greedy NMS that stops after $P$ kept boxes compares each of the $N$ candidates with at most $P$ kept boxes, $O(NP)$. The second stage costs the RoI pooling of [Fast R-CNN](/fast-r-cnn/) and $O(K P^2)$ for NMS of each class. With VGG16 the paper reports 198 ms per image for the whole system, 10 ms of it in the proposal layers, which is about 5 frames per second.

## Properties

- **Shared features.** The proposals and the detection read the same feature map, so proposals add little time.
- **Translation-equivariant anchors.** The same anchors and weights at every cell.
- **Learned proposals.** Unlike [selective search](/selective-search/), the proposals are trained for the classes of the data and improve with the backbone.
- **Two stages.** The second stage pools features again for each proposal, which costs more than a one-stage detector such as [SSD](/single-shot-multibox-detector/) or [YOLO](/yolo-detector/), but is usually more accurate on small objects.
- **Deterministic at test time; not exact,** since it is a learned method.

## Variants and improvements

- **Feature pyramid network.** [FPN](/feature-pyramid-network/) puts anchors of one size on each level of a feature pyramid and pools each RoI from the level that fits its size.
- **Mask R-CNN.** [Mask R-CNN](/mask-r-cnn/) adds a mask branch and replaces RoI pooling with RoIAlign.
- **R-FCN and Cascade R-CNN.** R-FCN moves most of the second stage before the pooling. Cascade R-CNN runs several second stages with rising IoU thresholds.
- **RPN alone.** The RPN is also a fast class-agnostic [proposal](/object-proposals/) method in its own right, and a one-class RPN is a simple detector.
- **Other assignment rules.** ATSS and other rules of the [anchor assignment](/anchor-assignment/) page replace the fixed 0.7 and 0.3.

## When to use it

Use Faster R-CNN, usually with an FPN, when accuracy matters more than speed, for small objects, and as a strong baseline that is well understood. Use a one-stage detector when the time budget is tight, and a set-based detector such as [DETR](/detr/) when NMS and anchors are to be avoided.

## Pitfalls

- **Anchor sizes that do not fit the data.** An object much smaller than the smallest anchor gets low IoU with every anchor and is learned only through the "best anchor" rule.
- **Border anchors.** The paper reports that with the anchors that cross the border in training, large error terms that are hard to correct appear and training does not converge. At test time the boxes are clipped instead.
- **Thresholds of two kinds.** The RPN uses NMS at 0.7 to keep many proposals, and the detector uses about 0.3 per class; swapping them loses recall or adds duplicates.
- **Proposals that differ between training and test.** The detector is trained on 2000 proposals and tested on 300 from the same RPN. In Table 2 of the paper, a detector trained on selective search proposals and tested on 300 RPN proposals reaches 56.8 percent mAP, against 59.9 percent when both stages use shared RPN proposals.
- **Ties in the "best anchor" rule.** Several anchors with the same largest IoU all become positive.
- **Clipping order.** Clip after decoding, then apply the minimum size; clipping first loses the regression of boxes that cross the border.

## Implementations

The network is outside this page: the Python code takes the RPN scores and offsets and the second-stage head as inputs, and the tests build them by hand or from the ground truth with a fixed seed. The code implements the anchors, the proposal step of lines L2 to L6, the second-stage decoding and NMS of each class, the anchor labels with the border rule, the sampling of 256 anchors, and the RPN loss. The tests check the anchor shapes and centers, the proposal example above with its variants, the label example, the label rule against its definition on random boxes, the RPN loss on hand values, the properties of the proposals on random outputs, and a run of the whole pipeline that recovers a known box.

## History

[R-CNN](/r-cnn/) (2014) and [Fast R-CNN](/fast-r-cnn/) (2015) depended on [selective search](/selective-search/), which took about 2 seconds per image on a CPU, more than the detector itself. MultiBox (Erhan et al. 2014) had learned proposals with a network, but not shared with the detector and without translation-invariant anchors. Ren, He, Girshick and Sun put Faster R-CNN on arXiv in June 2015 and presented it at NIPS 2015, with the extended version in IEEE TPAMI in 2017. It reached 73.2 percent mAP on VOC 2007 with VGG16 trained on VOC 2007 and 2012, at 5 frames per second, and its RPN and anchors became the base of the [feature pyramid network](/feature-pyramid-network/), [Mask R-CNN](/mask-r-cnn/) and most two-stage detectors, and through them of the one-stage [SSD](/single-shot-multibox-detector/) and RetinaNet as well.

## References
