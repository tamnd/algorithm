---
tag: JNRSBB
kind: technique
slug: anchor-boxes
name: Anchor boxes
aliases:
- default boxes
- prior boxes
area: computer-vision/segmentation-and-recognition
level: advanced
summary: A fixed set of reference boxes of several scales and aspect ratios at each feature map position, from which a detector predicts offsets and scores.
prereqs: [intersection-over-union, bounding-box-regression]
see_also: [anchor-assignment, faster-r-cnn, single-shot-multibox-detector, feature-pyramid-network, yolo-detector, sliding-window-detection, k-means, object-detection]
sources:
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1.1, Anchors (3 scales and 3 aspect ratios, k = 9 anchors at each position, translation invariance, multi-scale anchors as regression references)"
  - paper: doi:10.1007/978-3-319-46448-0_2
    title: "Wei Liu, Dragomir Anguelov, Dumitru Erhan, Christian Szegedy, Scott Reed, Cheng-Yang Fu and Alexander C. Berg, SSD: single shot multibox detector, ECCV 2016"
    locator: "Section 2.2, Choosing scales and aspect ratios for default boxes (the linear scale rule with s_min = 0.2 and s_max = 0.9, the ratios 1, 2, 3, 1/2, 1/3 and the extra box of scale sqrt(s_k s_k+1))"
  - paper: doi:10.1109/CVPR.2017.106
    title: "Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan and Serge Belongie, Feature pyramid networks for object detection, CVPR 2017"
    locator: "Section 4.1, Feature pyramid networks for RPN (one anchor size from 32 to 512 per pyramid level, 3 aspect ratios, 15 anchor shapes in all)"
  - url: https://arxiv.org/abs/1612.08242
    title: "Joseph Redmon and Ali Farhadi, YOLO9000: better, faster, stronger, CVPR 2017 (arXiv 1612.08242)"
    locator: "Section 2, paragraphs Convolutional with anchor boxes and Dimension clusters (k-means with the distance 1 - IOU, k = 5, Table 1)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Anchor boxes are a fixed set of reference boxes that a detector places at every position of a feature map, with a few sizes and aspect ratios at each position. The detector does not search for boxes. For each anchor it predicts a class score and the four offsets of [bounding box regression](/bounding-box-regression/) that move the anchor onto the object. So the anchors decide which boxes the detector can reach with small offsets, and [anchor assignment](/anchor-assignment/) decides which anchors learn which objects. [Faster R-CNN](/faster-r-cnn/) introduced them for its region proposal network, and the [single shot multibox detector](/single-shot-multibox-detector/) calls them default boxes. The anchor grid costs $O(W_f H_f k)$ time and space for a $W_f \times H_f$ map with $k$ shapes; the network that scores them is not part of this page.

## In plain words

A detector looks at a grid of positions over the image. At each position it has a small menu of boxes: a square, a tall box, a wide box, each in a small, a middle and a large size. These are the anchors. For each box on the menu the detector answers two questions: is there an object that fits this box, and how must the box move and stretch to fit it well? The anchors never move. Only the answers change from image to image. The menu is chosen so that every object in the image has some anchor close to it in place, size and shape. If an object has no close anchor, the detector has a hard time finding it. So the choice of sizes, shapes and grid spacing is a real design decision.

## When it applies

The technique needs a feature map of $W_f \times H_f$ positions, where position $(u, v)$ looks at an area of the image around the point $((u + o)s, (v + o)s)$. Here $s$ is the stride, the number of image pixels between two positions, and $o$ is an offset that each code base fixes: $o = 0.5$ in SSD and $o = 0$ in torchvision. A box is $(x_1, y_1, x_2, y_2)$ in continuous image coordinates.

An anchor shape is a size $\sigma$ and an aspect ratio $r = h / w$. The shape has $w = \sigma / \sqrt r$ and $h = \sigma \sqrt r$, so its area is $\sigma^2$ for every ratio. With a set $S$ of sizes and a set $R$ of ratios there are $k = |S| \cdot |R|$ shapes, and the map has $W_f H_f k$ anchors.

The technique fits a detector whose head is a convolution: the same small network runs at every position and outputs $k$ scores and $4k$ offsets there. Then the anchors at one position all use the same features, and the shapes let the outputs specialize by size and shape. It also fits a detector with several feature maps, one set of anchor sizes per map. It does not fit a detector that predicts a set of boxes with no reference, such as [DETR](/detr/), or a detector that predicts boxes from points with no prior shape.

## The template

```pseudo id=template
ANCHORS(W_f, H_f, s, S, R, o)          ▷ map size, stride, sizes, ratios, offset
L1  B ← empty list of shapes
L2  for each σ in S, for each r in R: append (σ / √r, σ √r) to B
L3  A ← empty list of boxes
L4  for v ← 0 to H_f - 1, for u ← 0 to W_f - 1
L5      (c_x, c_y) ← ((u + o) s, (v + o) s)
L6      for each (w, h) in B: append (c_x - w/2, c_y - h/2, c_x + w/2, c_y + h/2) to A
L7  return A
```

Anchor $j$ of position $(u, v)$ is the box with center $((u + o)s, (v + o)s)$ and the shape $B_j$. The output order is fixed, position by position and shape by shape, so the detector output with index $(v, u, j)$ belongs to that anchor. Lines L1 and L2 depend only on $S$ and $R$, so code computes them once. Lines L4 to L6 take $O(W_f H_f k)$ time in the [real RAM](/real-ram/) model, and the list uses $O(W_f H_f k)$ space.

**How close is the nearest anchor?** A design question is the [intersection over union](/intersection-over-union/) between an object box and its best anchor. Four facts give the answer for simple cases, with proofs in [the proof page](proofs/correctness.md).

1. Two boxes with the same center and ratio and sizes $\sigma_1 \le \sigma_2$ have IoU $(\sigma_1 / \sigma_2)^2$. So sizes spaced by a factor 2, as in Faster R-CNN, give every centered square between two sizes a best IoU of at least $1/2$, with $1/2$ at the size $\sigma \sqrt 2$.
2. Two boxes with the same center and area whose ratios differ by a factor $q \ge 1$ have IoU $1/(2\sqrt q - 1)$. For $q = 2$ this is $0.547$, and for $q = 4$, the factor between the ratios $1/2$ and $2$, it is $1/3$.
3. A square of side $\sigma$ whose center is $d_x$ and $d_y$ away from the center of a square anchor of the same side has IoU $p/(2\sigma^2 - p)$ with $p = (\sigma - d_x)(\sigma - d_y)$. On a grid of stride $s$ the nearest center is at most $s/2$ away in each axis, and the worst case is $d_x = d_y = s/2$.
4. For $\sigma = 32$ the worst case of fact 3 gives $576/1472 = 0.391$ at stride 16 and $900/1148 = 0.784$ at stride 4. So a small object on a coarse grid can have no anchor above 0.7, which is the reason why the matching rules have a "best anchor for each object" clause and why [feature pyramids](/feature-pyramid-network/) put small anchors on fine maps.

**Example.** The Faster R-CNN code places 9 anchors per position on a map of stride 16. With the legacy rule of that code (inclusive pixel boxes, base box $(0, 0, 15, 15)$, widths rounded), the 9 anchors of position $(0, 0)$ are $(-84, -40, 99, 55)$, $(-176, -88, 191, 103)$ and $(-360, -184, 375, 199)$ for ratio $1/2$; $(-56, -56, 71, 71)$, $(-120, -120, 135, 135)$ and $(-248, -248, 263, 263)$ for ratio $1$; and $(-36, -80, 51, 95)$, $(-80, -168, 95, 183)$ and $(-168, -344, 183, 359)$ for ratio $2$. The wide ones are $184 \times 96$, $368 \times 192$ and $736 \times 384$, so the rounding makes their areas a little larger than $128^2$, $256^2$ and $512^2$. A $60 \times 40$ map, from an image of about $1000 \times 600$, has $60 \cdot 40 \cdot 9 = 21600$ anchors.

**Implementation.** The Python code has the generator of lines L1 to L7, the legacy generator of the Faster R-CNN code, IoU with exact fractions on integer boxes, the best IoU over a list of anchors by brute force, and the k-means of YOLOv2 on box sizes with the distance $1 - \operatorname{IoU}$. The tests check the count, the area and the ratio of every shape, the centers for both offsets, the nine legacy boxes above, the four facts with exact values, that k-means finds three planted size clusters, and that more clusters give a higher mean best IoU.

## Classic examples

- **Faster R-CNN.** Three areas $128^2$, $256^2$ and $512^2$ and three ratios $1{:}1$, $1{:}2$ and $2{:}1$, so $k = 9$, on the last map of stride 16. The paper calls the scheme translation invariant: if an object moves, the same anchor at the new position and the same weights predict it.
- **Single shot multibox detector.** Default boxes on six feature maps. Map $k$ of $m$ has the scale $s_k = s_{\min} + (s_{\max} - s_{\min})(k - 1)/(m - 1)$ of the image size, with $s_{\min} = 0.2$ and $s_{\max} = 0.9$, ratios $\{1, 2, 3, 1/2, 1/3\}$ and one extra square of scale $\sqrt{s_k s_{k+1}}$. SSD300 has 8732 default boxes in all.
- **Feature pyramid network.** One anchor size per level, $32^2$ to $512^2$ on the levels $P_2$ to $P_6$, with three ratios each, so 15 shapes in all and 3 per position. The size grows with the stride, which keeps fact 4 the same on every level.
- **RetinaNet.** Three sizes $2^0$, $2^{1/3}$ and $2^{2/3}$ times the base size of each pyramid level and three ratios, so 9 anchors per position, from $32$ to about $813$ pixels.
- **YOLOv2.** Five anchor shapes per cell of a $13 \times 13$ map, found by [k-means](/k-means/) on the sizes of the training boxes with the distance $1 - \operatorname{IoU}$ of two centered boxes. On VOC 2007 the 5 cluster shapes give an average IoU of 61.0 with the closest shape, against 60.9 for the 9 hand-picked shapes of Faster R-CNN, and 9 clusters give 67.2 (benchmark results of the 2017 paper).

## Variations

- **Data-driven shapes.** Choose the shapes by clustering the training boxes, as in YOLOv2, instead of by hand. With the distance $1 - \operatorname{IoU}$ the mean of a cluster is not the point that minimizes the sum of distances, so the k-means loop is a heuristic and the code stops after a fixed number of rounds.
- **Anchors per level.** With a pyramid, each level has its own sizes in proportion to its stride, as in FPN and RetinaNet.
- **Densities.** Some detectors put more anchors on small sizes, with centers at sub-stride offsets, to raise the IoU of fact 3 for small objects.
- **Learned anchors.** Guided anchoring and similar methods predict the anchor shape at each position from the features.
- **Anchor-free detectors.** FCOS and CenterNet use one point per position and predict distances to the sides or a size directly, which removes the anchor design but keeps the grid.

## Pitfalls

- **The offset $o$.** One code base centers anchors at $(u + 0.5)s$, another at $us$. Trained weights from one do not fit anchors from the other; the boxes are off by half a stride.
- **The ratio convention.** Some code takes $r = h/w$ and other code takes $w/h$. With the symmetric set $\{1/2, 1, 2\}$ the set of shapes is the same, but the order changes, and the order must match the order of the network outputs.
- **Inclusive pixels and rounding.** The legacy anchors above are not exactly the continuous ones. Use one rule from training to test.
- **Anchors outside the image.** Large anchors near the border extend past the image. Faster R-CNN ignores them in training and clips the proposals at test time. Using them without care adds targets that point outside the image.
- **Coverage gaps.** A size or a shape with no close anchor gives few positive anchors in training and a low recall at test time. Check the best IoU of the training boxes with the anchors before training.
- **Too many anchors.** Doubling the shapes doubles the head outputs and the number of easy negatives; the extra negatives need sampling or a loss such as [focal loss](/focal-loss/).

## Exercises

1. Show that the shape $(\sigma/\sqrt r, \sigma\sqrt r)$ has area $\sigma^2$ and ratio $h/w = r$, and count the anchors of SSD300 from the map sizes $38, 19, 10, 5, 3, 1$ with 4, 6, 6, 6, 4 and 4 boxes per position.
2. Show that two centered boxes of the same area whose ratios differ by a factor $q$ have IoU $1/(2\sqrt q - 1)$. Which $q$ gives an IoU of exactly $1/2$?
3. A square object of side 32 lies at the worst place on a grid of stride 16 with square anchors of side 32. Show that no anchor has an IoU above 0.4 with it. What is the largest stride for which some anchor of side 32 always has IoU at least 0.5?
4. Sizes $\sigma_1 < \sigma_2 < \dots$ are spaced by a factor $c > 1$. Find the smallest best IoU of a centered square with sizes between $\sigma_1$ and the largest size, as a function of $c$.
5. Run k-means with the distance $1 - \operatorname{IoU}$ on a small set of box sizes and find an input where the mean update makes the total distance larger.

## References
