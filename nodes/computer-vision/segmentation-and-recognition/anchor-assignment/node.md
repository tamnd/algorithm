---
tag: RFHSZS
kind: technique
slug: anchor-assignment
name: IoU-based anchor assignment
aliases:
- anchor matching
- label assignment for detection
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Label each anchor positive when its IoU with some true box exceeds a high threshold or is the best for that box, negative below a low threshold, else ignored.
prereqs: [anchor-boxes, intersection-over-union]
see_also: [faster-r-cnn, single-shot-multibox-detector, fast-r-cnn, bounding-box-regression, focal-loss, detr, hungarian-algorithm, feature-pyramid-network]
sources:
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1.2, Loss function (positive at the highest IoU for a true box or above 0.7, negative below 0.3 for all true boxes, the rest left out), and Section 3.1.3 (256 sampled anchors, up to 1:1)"
  - paper: doi:10.1007/978-3-319-46448-0_2
    title: "Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu and Alexander C. Berg, SSD: single shot multibox detector, ECCV 2016"
    locator: "Section 2.2, Matching strategy (each true box to its best default box, then every default box above 0.5) and Hard negative mining (at most 3:1)"
  - url: https://arxiv.org/abs/1708.02002
    title: "Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He and Piotr Dollar, Focal loss for dense object detection, ICCV 2017 (arXiv 1708.02002)"
    locator: "Section 4, RetinaNet detector, paragraph Anchors (positive at IoU 0.5, background below 0.4, the rest ignored)"
  - url: https://arxiv.org/abs/1912.02424
    title: "Shifeng Zhang, Cheng Chi, Yongqiang Yao, Zhen Lei and Stan Z. Li, Bridging the gap between anchor-based and anchor-free detection via adaptive training sample selection, CVPR 2020 (arXiv 1912.02424)"
    locator: "Section 4.1, Algorithm 1 (k nearest anchors per level, threshold mean plus standard deviation of their IoUs, center inside the box)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Anchor assignment decides, for each [anchor box](/anchor-boxes/) in a training image, whether it must learn an object, learn background, or stay out of the loss. A positive anchor learns the class of its matched true box and the [box regression](/bounding-box-regression/) offsets to that box. A negative anchor learns the class "background". An ignored anchor adds nothing. The rule of [Faster R-CNN](/faster-r-cnn/) uses the [intersection over union](/intersection-over-union/) of the anchor with the true boxes: positive above a high threshold or when it is the best anchor for some true box, negative below a low threshold, and ignored between. With $n$ anchors and $m$ true boxes the rule takes $O(nm)$ time. It is a heuristic: the thresholds and the sampling come from experiments, not from a theorem.

## In plain words

During training a detector has thousands of anchors and a few true objects in each image. Before it can compute a loss, it must say what each anchor should have predicted. An anchor that covers an object well should say "this object, and move me this much". An anchor on empty ground should say "nothing here". An anchor that half covers an object is unclear, so the simplest choice is to leave it out. Also, every object must get at least one anchor, even a small object that no anchor covers well, or the detector never learns to find it. Most anchors are empty, so the detector also picks a balanced subset of them for each step.

## When it applies

The technique needs a fixed list of anchors $A_1, \dots, A_n$ and the true boxes $G_1, \dots, G_m$ of one training image. A box is $(x_1, y_1, x_2, y_2)$ in continuous coordinates. It applies to every detector that predicts at fixed reference boxes: the region proposal network of Faster R-CNN, the [single shot multibox detector](/single-shot-multibox-detector/), RetinaNet and the anchor heads of a [feature pyramid network](/feature-pyramid-network/). The same kind of rule labels the proposals of [Fast R-CNN](/fast-r-cnn/), with the proposals in the role of the anchors.

It does not apply to a set predictor such as [DETR](/detr/), which assigns its predictions to the true boxes by a one-to-one matching of minimum cost, computed with the [Hungarian algorithm](/hungarian-algorithm/) for each image.

## The template

```pseudo id=template
ASSIGN(A, G, τ_pos, τ_neg)                 ▷ anchors A_1..A_n, true boxes G_1..G_m
L1  M[i][j] ← IoU(A_i, G_j) for every anchor i and true box j
L2  for each anchor i: m_i ← max_j M[i][j], g_i ← the first j with M[i][j] = m_i
L3      label_i ← 0 if m_i < τ_neg, else -1 (ignore)
L4  for each true box j with b_j ← max_i M[i][j] > 0
L5      for each anchor i with M[i][j] = b_j: label_i ← 1
L6  for each anchor i with m_i ≥ τ_pos: label_i ← 1
L7  return the labels and the matched boxes g

SAMPLE(label, B, f)                        ▷ batch size B, positive share f
L8  keep at most ⌊fB⌋ random positives, fill up to B with random negatives, set the rest to -1
```

A positive anchor $i$ learns the class of $G_{g_i}$ and the offsets of $G_{g_i}$ from $A_i$. Faster R-CNN uses $\tau_{pos} = 0.7$, $\tau_{neg} = 0.3$, $B = 256$ and $f = 0.5$. The paper says "higher than 0.7"; the py-faster-rcnn code uses $\ge 0.7$, and so does this page. The code keeps $g_i$ as the argmax of the row even for an anchor made positive by line L5, as py-faster-rcnn, Detectron2 and torchvision do.

The rule has these properties, which follow line by line from the template and which the tests check on random boxes:

- An anchor is positive exactly when $m_i \ge \tau_{pos}$ or when it ties for the best IoU of some true box with a positive best IoU. Otherwise it is negative when $m_i < \tau_{neg}$ and ignored when $\tau_{neg} \le m_i < \tau_{pos}$.
- Every true box with a positive best IoU has at least one positive anchor at that best IoU (line L5). Line L6 cannot undo line L5, since it only sets labels to 1.
- A true box with IoU 0 with every anchor has no positive anchor. Line L4 skips it on purpose: without the test $b_j > 0$, every anchor with IoU 0 for that box would tie and become positive.

**Cost.** Line L1 takes $O(nm)$ time and space. Lines L2 to L6 read each entry of $M$ a constant number of times, so they take $O(nm)$ too, and SAMPLE takes $O(n)$. For $n = 20000$ anchors and $m = 10$ boxes that is $2 \cdot 10^5$ IoU computations per image, small next to the network.

**Example.** Four anchors lie in a row: $A_1 = (0, 0, 10, 10)$, $A_2 = (5, 0, 15, 10)$, $A_3 = (10, 0, 20, 10)$ and $A_4 = (20, 0, 30, 10)$. The true boxes are $G_1 = (4, 0, 14, 10)$ and a small $G_2 = (21, 0, 25, 4)$. The IoUs with $G_1$ are $60/140 = 3/7$, $90/110 = 9/11$, $40/160 = 1/4$ and $0$. The only anchor that meets $G_2$ is $A_4$, with IoU $16/100 = 0.16$. With the Faster R-CNN thresholds:

- $A_1$ has $m_1 = 0.429$, between 0.3 and 0.7, so it is ignored.
- $A_2$ has $m_2 = 0.818 \ge 0.7$, so it is positive and matched to $G_1$.
- $A_3$ has $m_3 = 0.25 < 0.3$, so it is negative.
- $A_4$ has $m_4 = 0.16 < 0.3$, so line L3 makes it negative, but it is the best anchor for $G_2$, so line L5 makes it positive and matched to $G_2$.

Without lines L4 and L5 the small box $G_2$ would have no positive anchor. With the RetinaNet thresholds 0.5 and 0.4 and no best-anchor rule, $A_1$ is still ignored, since $3/7 \ge 0.4$, and $A_4$ is negative.

**Implementation.** The Python code has the rule of lines L1 to L7 with the best-anchor rule as an option, the sampling of line L8, the SSD matching and ATSS. IoU is exact with fractions on integer boxes, so ties are exact. The tests check the example, all three properties above on random boxes against the definition, the sampling counts, that SSD gives each true box its best anchor, and an ATSS threshold computed by hand.

## Classic examples

- **Faster R-CNN, region proposal network.** The template with 0.7 and 0.3 and the best-anchor rule, and 256 anchors per image with up to half positive. Anchors that cross the image border are ignored in training.
- **Fast R-CNN, second stage.** Proposals with IoU at least 0.5 with a true box are foreground, those with a maximum IoU in $[0.1, 0.5)$ are background, and 25 percent of the 64 regions sampled from each image are foreground. The lower bound 0.1 acts as a heuristic for hard negatives.
- **Single shot multibox detector.** Each true box first takes the default box with the best IoU, then every default box with IoU above 0.5 with some true box is positive. There is no ignore zone. The many negatives are cut by hard negative mining to at most 3 negatives per positive, taking the ones with the highest confidence loss.
- **RetinaNet.** Positive at IoU 0.5 or more, background below 0.4, ignored between, with no sampling: the [focal loss](/focal-loss/) down-weights the easy negatives instead.
- **ATSS.** For each true box, take the $k = 9$ anchors of each pyramid level whose centers are closest to the box center. Set the threshold to the mean plus the standard deviation of their IoUs, and keep those at or above it whose center lies inside the box. An anchor positive for several boxes takes the one with the highest IoU. The threshold adapts to each box, and $k$ is the only parameter. The paper reports a COCO AP of 38.0 at $k = 3$ and 39.3 at $k = 9$ (benchmark results).

## Variations

- **Thresholds.** Each detector tunes $\tau_{pos}$ and $\tau_{neg}$. Cascade R-CNN trains a chain of second-stage heads at IoU thresholds 0.5, 0.6 and 0.7.
- **Center rules.** Anchor-free detectors label a point positive when it lies in the box, or in a central part of it, and in the right pyramid level for the box size.
- **Set matching.** DETR and its followers use a one-to-one matching of predictions and true boxes by a cost that mixes class scores and box distances, so each true box has exactly one positive prediction.
- **Dynamic assignment.** OTA and SimOTA assign by a transport or a top-$k$ rule on a cost that includes the current predictions, so the labels change during training.

## Pitfalls

- **Strict and non-strict thresholds.** "Above 0.7" and "at least 0.7" differ for exact values, which occur with integer boxes and with anchors equal to a true box. State the choice.
- **The matched box of a forced anchor.** In the Faster R-CNN code an anchor made positive by line L5 for box $j$ still regresses to its own argmax $g_i$, which can be another box. When two boxes share their best anchor, one of them has no anchor that learns it. The SSD code instead gives the forced anchor to the box that forced it.
- **Boxes with no overlap.** A true box that lies between all anchors, or outside the area they cover, has no positive anchor. Check the training set for such boxes, or add anchors.
- **Crowd and difficult boxes.** COCO marks crowd regions, and PASCAL VOC marks difficult objects. Anchors that match them are usually ignored, not negative. Treating them as background teaches the detector to miss them.
- **Sampling with few positives.** If an image has 10 positive anchors, the batch of 256 gets 246 negatives, not 128. The share of positives then varies from image to image, which changes the effective loss weight.
- **The cost of the IoU matrix.** For $10^5$ anchors and 100 boxes the matrix has $10^7$ entries. Compute it in blocks or on the device that holds the anchors.

## Exercises

1. Show that after ASSIGN every true box $j$ with $\max_i M[i][j] > 0$ has a positive anchor $i$ with $M[i][j] = \max_i M[i][j]$.
2. Find a set of anchors and two true boxes for which the Faster R-CNN rule leaves one true box with no anchor whose matched box is that true box.
3. Show that without the test $b_j > 0$ on line L4, a true box that meets no anchor makes every anchor with IoU 0 for it positive. What would such an anchor learn?
4. An anchor of side 32 and a true box of side 32 have centers $d$ apart along one axis. For which $d$ is the anchor positive, ignored and negative under the thresholds 0.7 and 0.3?
5. In ATSS, find three IoU values for the candidates of a true box for which no candidate reaches the threshold mean plus sample standard deviation.

## References
