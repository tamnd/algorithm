---
tag: D6VPA6
kind: algorithm
slug: yolo-detector
name: YOLO
aliases:
- you only look once
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Detect objects in one pass by having each cell of a grid over the image predict box coordinates, objectness and class scores directly.
solves: [object-detection]
model: real-ram
complexity:
  vars: {S: the side of the grid in cells, B: the number of boxes per cell, C: the number of classes}
  time: {worst: "O(C S^4 B^2)"}
  space: {extra: "O(S^2 B C)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi]
  note: "Presented at CVPR 2016. It cast detection as one regression from the image to a grid of boxes and class probabilities, and ran at 45 frames per second; YOLO9000 (2017) added anchors found by k-means and a bounded offset rule."
prereqs: [object-detection, intersection-over-union, box-non-maximum-suppression]
see_also: [single-shot-multibox-detector, faster-r-cnn, anchor-boxes, k-means, feature-pyramid-network, detr, bounding-box-regression, focal-loss]
sources:
  - paper: doi:10.1109/CVPR.2016.91
    title: "Joseph Redmon, Santosh Divvala, Ross Girshick and Ali Farhadi, You only look once: unified, real-time object detection, CVPR 2016, 779-788"
    locator: "Section 2, Unified detection (S x S grid, B boxes with x, y, w, h and confidence, C class probabilities, class-specific confidence; S = 7, B = 2, C = 20, a 7 x 7 x 30 tensor); Section 2.2, Training (the loss with lambda_coord = 5, lambda_noobj = 0.5 and square roots of w and h; the responsible predictor has the highest current IOU); Section 2.3, Inference (98 boxes per image, NMS adds 2 to 3 percent mAP); Section 2.4, Limitations; Section 4, Experiments (Table 1: 63.4 mAP at 45 FPS, Fast YOLO 52.7 mAP at 155 FPS on VOC 2007)"
  - url: https://arxiv.org/abs/1612.08242
    title: "Joseph Redmon and Ali Farhadi, YOLO9000: better, faster, stronger, CVPR 2017 (arXiv 1612.08242)"
    locator: "Section 2, Better (convolutional with anchor boxes: recall from 81 to 88 percent; dimension clusters: k-means with d = 1 - IOU and k = 5; direct location prediction: b_x = sigma(t_x) + c_x, b_w = p_w e^t_w; a 13 x 13 map for a 416 input); Table 3 (YOLOv2 at 416: 76.8 mAP at 67 FPS on VOC 2007)"
  - url: https://arxiv.org/abs/1804.02767
    title: "Joseph Redmon and Ali Farhadi, YOLOv3: an incremental improvement, arXiv 1804.02767, 2018"
    locator: "Section 2, The deal (predictions at 3 scales, 9 clusters, independent logistic classifiers)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

YOLO, short for "you only look once", treats detection as one regression problem. The image is resized and passed once through a convolutional network. The network divides it into an $S \times S$ grid. Each cell predicts $B$ boxes and $C$ class probabilities. For each box, the cell gives a center offset inside the cell, a width and height relative to the image, and a confidence. The paper uses $S = 7$, $B = 2$ and $C = 20$ for PASCAL VOC, so the output is a $7 \times 7 \times 30$ tensor and an image gives 98 boxes. At test time the score of a box for a class is the class probability of its cell times the box confidence. Low scores are dropped, and [non-maximum suppression](/box-non-maximum-suppression/) is applied to each class. YOLO ran at 45 frames per second with 63.4 percent mAP on VOC 2007, and the smaller Fast YOLO ran at 155 frames per second. Later versions, starting with YOLO9000, predict offsets from [anchor boxes](/anchor-boxes/) whose shapes are found by [k-means](/k-means/).

## In plain words

YOLO lays a grid over the image. The cell that holds the center of an object is in charge of that object. Each cell guesses a few boxes, says how sure it is that each box holds an object, and says which class the object of the cell is. All of this comes out of one pass of the network, so it is fast. To get the final list, each box's sureness is multiplied by the class guess of its cell. Weak boxes are removed, and near copies of the same class are removed too. Because each cell names only one class and holds few boxes, YOLO version 1 misses groups of small objects, such as a flock of birds.

## The problem

The input is an image and a trained network that gives the $S \times S \times (5B + C)$ tensor. The output is a list of boxes with a class and a score, judged by [detection mean average precision](/detection-mean-average-precision/). This page gives the steps that are not learned: the decoding, the class-specific scores and the NMS at test time, and the training loss of version 1 with its rule for the predictor in charge. It also gives the anchor decoding and the shape clusters of version 2, and proves facts about these steps. The network is outside.

## The algorithm

```pseudo id=main
YOLO-DETECT(I, network, S, B, C, τ_score, τ)
L1  T ← network(I), a tensor of S × S × (5B + C)        ▷ outside
L2  for each cell (i, j) and box k: b ← ((j + x)/S · W, (i + y)/S · H, w · W, h · H) as center and size
L3      score_c(b) ← Pr(class c | cell) · confidence(b) for c = 1, ..., C
L4  for each class c
L5      candidates ← the boxes with score_c > τ_score
L6      greedy NMS at IoU τ of the candidates by score_c
L7      add the kept boxes, with class c, to the output
L8  return the output sorted by score
```

**Confidence.** In training, the confidence target of a box is $\Pr(\text{object}) \cdot \text{IoU}$ with the truth. So the score of line L3 is $\Pr(\text{class}_c \mid \text{object}) \cdot \Pr(\text{object}) \cdot \text{IoU}$. It holds both the class and how well the box fits.

**Loss.** The cell that holds the center of a truth box is responsible for it. Inside that cell, the one of the $B$ predictors whose box has the largest IoU with the truth is the responsible predictor. Let $\mathbb{1}^{obj}_{ij}$ mark the responsible predictor $j$ of cell $i$, let $\mathbb{1}^{noobj}_{ij}$ mark all the others, and let $\mathbb{1}^{obj}_i$ mark the cells with an object. Then the loss is
$$\begin{aligned} L = {} & \lambda_{coord} \sum_{i,j} \mathbb{1}^{obj}_{ij}\bigl[(x - \hat x)^2 + (y - \hat y)^2 + (\sqrt{w} - \sqrt{\hat w})^2 + (\sqrt{h} - \sqrt{\hat h})^2\bigr] \\ & + \sum_{i,j} \mathbb{1}^{obj}_{ij}(c - \hat c)^2 + \lambda_{noobj} \sum_{i,j} \mathbb{1}^{noobj}_{ij}\, c^2 + \sum_i \mathbb{1}^{obj}_i \sum_{k} (p_k - \hat p_k)^2, \end{aligned}$$
with $\lambda_{coord} = 5$ and $\lambda_{noobj} = 0.5$. The hatted values are the targets, $\hat c$ is the IoU of the predicted box with the truth, and $\hat p$ is the one-hot class. The square roots make an error of a few pixels cost more on a small box than on a large one. The class term counts once per cell, not once per box.

**Version 2 decoding.** YOLO9000 predicts $t_x, t_y, t_w, t_h, t_o$ for each of $k$ anchors at a cell with corner $(c_x, c_y)$ in grid units:
$$b_x = \sigma(t_x) + c_x, \quad b_y = \sigma(t_y) + c_y, \quad b_w = p_w e^{t_w}, \quad b_h = p_h e^{t_h}, \quad \Pr(\text{object}) \cdot \text{IoU} = \sigma(t_o).$$
The sigmoid keeps the center inside the cell, which made training more stable than the free offsets of [bounding box regression](/bounding-box-regression/). The prior shapes $(p_w, p_h)$ are $k = 5$ centers of k-means on the training boxes, with the distance $d = 1 - \text{IoU}$ between two shapes placed at the same center. With a Euclidean distance, large boxes would give larger errors than small ones.

## Example

Take $S = 2$, $B = 1$, $C = 2$, an image of $100 \times 100$ pixels, $\tau_{score} = 0.2$ and $\tau = 0.5$. The cells give $(x, y, w, h, \text{conf}, p_0, p_1)$:

| cell | output | box | scores |
|---|---|---|---|
| (0, 0) | 0.8, 0.8, 0.6, 0.6, 0.9, 0.8, 0.2 | (10, 10, 70, 70) | 0.72, 0.18 |
| (0, 1) | 0.3, 0.5, 0.4, 0.4, 0.6, 0.1, 0.9 | (45, 5, 85, 45) | 0.06, 0.54 |
| (1, 0) | 0.8, 0.0, 0.6, 0.6, 0.6, 0.6, 0.4 | (10, 20, 70, 80) | 0.36, 0.24 |
| (1, 1) | 0.5, 0.5, 0.2, 0.2, 0.1, 0.5, 0.5 | (70, 70, 90, 90) | 0.05, 0.05 |

For cell (1, 0), the center is $((0 + 0.8)/2 \cdot 100, (1 + 0)/2 \cdot 100) = (40, 50)$ and the size is 60, which gives the box $(10, 20, 70, 80)$.

1. Class 0 keeps the scores above 0.2: 0.72 and 0.36. Their boxes overlap with IoU $3000/4200 = 5/7 > 0.5$, so NMS removes the second one. The same object is seen from two cells.
2. Class 1 keeps 0.54 and 0.24. Their boxes have IoU $625/4575 \approx 0.14$, so both stay.
3. The output is $(0.72, 0)$, $(0.54, 1)$ and $(0.24, 1)$, with the boxes above. The last one is the object of class 0 again, now under class 1, since NMS for each class does not compare across classes.

For the loss, take $S = 1$, $B = 2$, $C = 2$, the truth $(20, 20, 80, 80)$ of class 1, and the outputs $(0.6, 0.5, 0.6, 0.6, 0.7)$ and $(0.5, 0.5, 0.2, 0.2, 0.4)$ with class probabilities $(0.3, 0.7)$. The boxes are $(30, 20, 90, 80)$ with IoU $5/7$ and $(40, 40, 60, 60)$ with IoU $1/9$, so the first predictor is responsible. Then $L = 5 \cdot 0.1^2 + (0.7 - 5/7)^2 + 0.5 \cdot 0.4^2 + 0.3^2 + 0.3^2 \approx 0.3102$.

## Correctness

The network has no correctness theorem; its accuracy is measured. [The proof page](proofs/correctness.md) shows these facts for the steps that are not learned:

1. **Decoding.** For $0 \le x, y \le 1$ the center of a box lies in its cell. The version 2 center always lies in its cell, for any $t$.
2. **Output.** It is sorted by score, every score is above $\tau_{score}$, and two boxes of one class have IoU at most $\tau$.
3. **Loss.** The loss is zero exactly when the responsible predictors give the targets, all other confidences are zero, and the class vectors of the object cells are one-hot on the truth. For a fixed error in $w$, the term falls as the box grows.
4. **Clusters.** When the clustering converges, each shape is given to a center of largest IoU, and each center is the mean of its shapes.

## Complexity

The network is outside. Decoding and scoring the $S^2 B$ boxes for $C$ classes costs $O(S^2 B C)$. Greedy NMS of one class costs $O((S^2 B)^2)$ in the worst case, so the test-time steps cost $O(C S^4 B^2)$. For $S = 7$ and $B = 2$ this is at most 98 boxes per class, so the cost after the network is small. The loss costs $O(S^2 (B + C) + G)$ for $G$ truths. One round of the shape clustering costs $O(nk)$ for $n$ shapes and $k$ centers.

## Properties

- **One pass and global context.** The network sees the whole image when it predicts each box. The paper reports fewer background false positives than Fast R-CNN, but more localization errors.
- **Spatial limits.** In version 1, one class per cell and $B$ boxes per cell limit how many nearby objects can be found. Two objects whose centers fall in one cell compete for it.
- **Coarse grid.** The $7 \times 7$ grid and the fully connected output make the boxes coarse. Version 2 moved to a fully convolutional $13 \times 13$ map with anchors.
- **Deterministic at test time; not exact,** since it is a learned method.

## Variants and improvements

- **YOLO9000 (YOLOv2).** Batch normalization, a classifier trained at higher resolution, anchors from dimension clusters, the sigmoid offsets above, and training at several input sizes. At input 416 it reached 76.8 percent mAP at 67 frames per second on VOC 2007. Anchors raised recall from 81 to 88 percent.
- **YOLOv3.** Predictions at 3 scales with 9 clusters, in the spirit of the [feature pyramid network](/feature-pyramid-network/), and a separate logistic classifier for each class.
- **Later versions.** Many later detectors carry the name, with other authors. They add stronger backbones, mosaic [data augmentation](/data-augmentation/), anchor-free heads and, in some, training without NMS.
- **Other one-stage detectors.** [SSD](/single-shot-multibox-detector/) predicts from default boxes on several maps. RetinaNet uses the [focal loss](/focal-loss/). [DETR](/detr/) predicts a set with no grid and no NMS.

## When to use it

Use a YOLO-style detector when speed is the first need, as in video or on small devices, and the objects are not mostly tiny and crowded. Version 1 is mainly of teaching value. For accuracy on small objects, use a detector with a feature pyramid.

## Pitfalls

- **Objects that share a cell.** Two centers in one cell give one object to that cell in version 1. Groups of small objects are the known weak point.
- **Wrong axes.** The tensor is indexed by row and column, but $x$ goes with the column. Swapping them moves every box.
- **Negative widths.** A raw output for $w$ can be negative, and its square root is undefined. Clamp it, or predict $\sqrt{w}$ directly.
- **NMS for each class only.** As in the example, the same object can come out under two classes.
- **Score threshold.** The paper does not fix the threshold for the class-specific scores. Too high loses recall, too low gives many false positives.
- **Euclidean k-means on shapes.** Plain k-means on $(w, h)$ favours large boxes. Use $1 - \text{IoU}$ as the distance.

## Implementations

The network is outside this page. The Python code takes the output tensor as input, and the tests build it by hand or with a fixed seed. The code implements the decoding and detection of lines L1 to L8, the version 1 loss with the responsible predictor, the version 2 decoding with anchors, and k-means on shapes with the distance $1 - \text{IoU}$. The tests check the example above, the properties of the output on random tensors, the loss example, a zero loss on perfect outputs, the larger weight of an error on a small box, the version 2 center that stays in its cell, and the clusters on three groups of shapes.

## History

Before YOLO, detectors applied a classifier many times: on [sliding windows](/sliding-window-detection/), as in the [deformable part model](/deformable-part-model/), or on [proposals](/object-proposals/), as in [R-CNN](/r-cnn/) and its successors. Redmon, Divvala, Girshick and Farhadi put YOLO on arXiv in June 2015 and presented it at CVPR 2016. It was the first detector to run in real time at a useful accuracy on PASCAL VOC, with one network from pixels to boxes. Redmon and Farhadi added anchors and other changes in YOLO9000 at CVPR 2017. YOLOv3 followed in 2018. The name was later taken up by a long line of detectors from other groups.

## References
