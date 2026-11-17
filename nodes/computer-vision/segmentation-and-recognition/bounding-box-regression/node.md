---
tag: TRRBN0
kind: technique
slug: bounding-box-regression
name: Bounding box regression
aliases:
- box regression
- box offset encoding
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Predict a box as offsets from a reference box: the center shift divided by the reference size, and the log of the width and height ratios."
prereqs: [intersection-over-union, axis-aligned-bounding-box, ridge-regression]
see_also: [anchor-boxes, anchor-assignment, r-cnn, fast-r-cnn, faster-r-cnn, single-shot-multibox-detector, huber-m-estimator, detr]
sources:
  - url: https://arxiv.org/abs/1311.2524
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, CVPR 2014, 580-587 (arXiv 1311.2524, version 5 with appendices)"
    locator: "Appendix C, Bounding-box regression (the targets t_x, t_y, t_w, t_h, ridge regression on pool5 features with lambda = 1000, training pairs with IoU above 0.6)"
  - paper: doi:10.1109/ICCV.2015.169
    title: "Ross Girshick, Fast R-CNN, ICCV 2015, 1440-1448"
    locator: "Section 2.3, Multi-task loss (Eq. 1 to 3: class-specific targets, the smooth L1 loss, lambda = 1, targets normalized to zero mean and unit variance)"
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1.2, Loss function (Eq. 2, the same encoding with anchors as the reference boxes)"
  - url: https://arxiv.org/abs/1902.09630
    title: "Hamid Rezatofighi, Nathan Tsoi, JunYoung Gwak, Amir Sadeghian, Ian Reid and Silvio Savarese, Generalized intersection over union: a metric and a loss for bounding box regression, CVPR 2019"
    locator: "Section 3 (the definition of GIoU and the loss 1 - GIoU)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Bounding box regression is the step of a detector that turns a rough box into a tight one. It does not predict the corners of a box directly. It predicts four offsets from a reference box, which is a proposal in [R-CNN](/r-cnn/) and [Fast R-CNN](/fast-r-cnn/) and an [anchor box](/anchor-boxes/) in [Faster R-CNN](/faster-r-cnn/) and the [single shot multibox detector](/single-shot-multibox-detector/): the shift of the center divided by the reference width or height, and the logarithm of the ratio of the sizes. A network or a linear model learns these offsets from features; the cost of that model is not part of this page. The encoding and its inverse are exact maps, and they do not change when the image is shifted or scaled, which is the reason for the form.

## In plain words

A detector first finds a box that is roughly in the right place. The box may be a little too far left, or too narrow. The regression step corrects it. It does not say "the right edge is at pixel 140". It says "move the box by a tenth of its own width to the right, and make it 20 percent wider". Because the correction is measured in units of the box itself, a small box and a large box with the same kind of error get the same numbers. A learned model can then use one rule for objects of every size and at every place in the image. To get the final box, the detector applies the correction to the rough box.

## When it applies

The technique needs a reference box $a$ for each prediction and a target box $g$ for training. A box is $(x_1, y_1, x_2, y_2)$ in continuous image coordinates with $x_1 < x_2$ and $y_1 < y_2$, with $x$ to the right and $y$ down. Its center form is $(x, y, w, h)$ with $w = x_2 - x_1$, $h = y_2 - y_1$, $x = x_1 + w/2$ and $y = y_1 + h/2$. Old PASCAL VOC code uses inclusive pixel boxes with $w = x_2 - x_1 + 1$; this page uses the continuous form unless it says otherwise.

The targets are

$$t_x = \frac{x - x_a}{w_a}, \qquad t_y = \frac{y - y_a}{h_a}, \qquad t_w = \log \frac{w}{w_a}, \qquad t_h = \log \frac{h}{h_a}.$$

The map from $g$ to $t$ is a bijection from the boxes with $w, h > 0$ onto $\mathbb{R}^4$. A model predicts $\hat t$ from the features of the reference box, and the decoded box is the inverse map applied to $\hat t$.

The technique applies when the reference box is already close to the object. R-CNN trains its regressor only on pairs with an [intersection over union](/intersection-over-union/) above 0.6, and the anchor rules of [anchor assignment](/anchor-assignment/) play the same role. For a reference box far from the object, the targets are large and the relation between features and targets is far from linear, so the prediction is poor. This is a design limit, not a theorem.

## The template

```pseudo id=template
ENCODE(a, g)                        ▷ reference box a, target box g
L1  (x_a, y_a, w_a, h_a) ← the center form of a
L2  (x, y, w, h) ← the center form of g
L3  return ((x - x_a) / w_a, (y - y_a) / h_a, log(w / w_a), log(h / h_a))

DECODE(a, t)
L4  (x_a, y_a, w_a, h_a) ← the center form of a
L5  x ← x_a + t_x w_a,  y ← y_a + t_y h_a
L6  w ← w_a exp(t_w),   h ← h_a exp(t_h)
L7  return (x - w/2, y - h/2, x + w/2, y + h/2)

FIT(Φ, T, λ)                        ▷ R-CNN: one ridge regressor per coordinate
L8  W ← (Φ^T Φ + λ I)^-1 Φ^T T
```

DECODE inverts ENCODE, and ENCODE inverts DECODE. Both maps do not change when the same map $p \mapsto (s_x p_x + b_x, s_y p_y + b_y)$ with $s_x, s_y > 0$ is applied to $a$ and $g$. A center error of $e$ widths, with the rest exact, gives an IoU of $(1 - |e|)/(1 + |e|)$ with the target for $|e| \le 1$, and a log width error of $e$ gives an IoU of $e^{-|e|}$. So an error of $+e$ and an error of $-e$ cost the same IoU, which a plain ratio $w/w_a$ does not give. The proofs are in [the proof page](proofs/correctness.md).

**Loss.** R-CNN fits each coordinate by [ridge regression](/ridge-regression/) on fixed features, with $\lambda = 1000$ chosen on a validation set (line L8). Fast R-CNN trains the network with the smooth L1 loss

$$\operatorname{smooth}_{L_1}(z) = \begin{cases} 0.5 z^2 & |z| < 1, \\ |z| - 0.5 & \text{otherwise}, \end{cases}$$

summed over the four coordinates of $\hat t - t$. This is the [Huber function](/huber-m-estimator/) with threshold 1. It is quadratic near zero and grows linearly for large errors, so a few bad targets have a bounded gradient. Its derivative is $z$ inside $[-1, 1]$ and $\operatorname{sign}(z)$ outside, which is continuous.

**Cost.** ENCODE and DECODE take $O(1)$ time each, so $O(n)$ for $n$ boxes in the [real RAM](/real-ram/) model. FIT with $m$ training pairs and $d$ features costs $O(m d^2)$ for the normal equations and $O(d^3)$ to solve them, for each of the four coordinates.

**Example.** Take the anchor $a = (0, 0, 10, 10)$ and the true box $g = (2, 1, 14, 9)$. Then $(x_a, y_a, w_a, h_a) = (5, 5, 10, 10)$ and $(x, y, w, h) = (8, 5, 12, 8)$. The targets are $t = (0.3, 0, \log 1.2, \log 0.8) = (0.3, 0, 0.18232, -0.22314)$. Suppose a model predicts $\hat t = (0.25, 0.1, 0.2, -0.1)$. The differences are $(-0.05, 0.1, 0.01768, 0.12314)$, all inside $[-1, 1]$, so the smooth L1 loss is $0.5$ times the sum of their squares, $0.013988$. DECODE gives the center $(7.5, 6)$, the width $10 e^{0.2} = 12.214$ and the height $10 e^{-0.1} = 9.048$, so the box is $(1.393, 1.476, 13.607, 10.524)$, with IoU $0.7328$ with $g$.

**Implementation.** The Python code has ENCODE and DECODE with optional target weights, the inclusive pixel rule and a cap on $t_w$ and $t_h$, the smooth L1 loss and its derivative, IoU and generalized IoU, and the ridge fit. The tests check the example above with exact fractions for $t_x$ and $t_y$, the two inverse properties on random boxes, the invariance under scaling and shifting, the two IoU formulas, the derivative of the loss against finite differences, and the ridge fit on targets that are linear in the features.

## Classic examples

- **R-CNN.** One class-specific linear regressor per coordinate on the pool5 features of the proposal, trained by ridge regression on pairs with IoU above 0.6. On PASCAL VOC 2007 test it raised the mean average precision from 54.2 to 58.5 percent (a benchmark result of the 2014 paper).
- **Fast R-CNN.** The network outputs $4K$ offsets for $K$ classes, one set per class, and uses the set of the true class $u$ in the loss $L_{cls} + \lambda [u \ge 1] L_{loc}$ with $\lambda = 1$. The targets are normalized to zero mean and unit variance over the training set.
- **Faster R-CNN.** The region proposal stage uses the same encoding with an anchor as the reference box, and the second stage uses it again with the proposal as the reference.
- **Single shot multibox detector.** The same encoding with the default boxes, divided in common code by "variances" 0.1 for the center and 0.2 for the size, which is the weighting of the next section with weights 10 and 5.
- **YOLO.** The first YOLO does not use this encoding: it predicts the center as an offset inside a grid cell and the square roots of the width and height as fractions of the image. YOLOv2 returned to a reference box form, $w = p_w e^{t_w}$, with the center kept inside its cell by a sigmoid.

## Variations

- **Target weights.** Detectron and torchvision multiply the targets of the second stage by $(10, 10, 5, 5)$, which has the effect of the normalization of Fast R-CNN with fixed constants.
- **A cap on the size offsets.** Before the exponential, torchvision and Detectron2 cap $t_w$ and $t_h$ at $\log(1000/16) \approx 4.135$, so one bad prediction cannot make a huge box.
- **IoU losses.** Losses of the form $1 - \operatorname{IoU}$ or $1 - \operatorname{GIoU}$ act on the decoded box and not on $t$. Generalized IoU subtracts the share of the smallest enclosing box $C$ that the union does not cover, $\operatorname{GIoU} = \operatorname{IoU} - |C \setminus (A \cup B)| / |C|$, so it is still informative for boxes that do not overlap. [DETR](/detr/) uses it with an L1 loss on the normalized center and size.
- **Distances to the sides.** Anchor-free detectors predict the four distances from a point to the sides of the box, often in log form or divided by the stride.
- **Iterative refinement.** Apply the regressor again to its own output, or use a cascade of regressors trained at higher IoU each.

## Pitfalls

- **Inclusive and continuous widths.** The $+1$ of inclusive pixel boxes must be used in both ENCODE and DECODE, or in neither. Code that mixes the two rules shifts every box by one pixel, which matters for small objects.
- **Corner form and center form.** A target computed from corners with the center formulas, or the other way round, gives boxes that are wrong but look plausible. Convert once, at the boundary of the module.
- **The wrong reference box.** In Faster R-CNN the second stage encodes relative to the proposal, not to the anchor that made the proposal.
- **Unnormalized targets.** Without the weights or the normalization, the size terms and the center terms have different scales, and the loss weight $\lambda$ that works for one detector fails for another.
- **Overflow in the exponential.** An untrained network can output $t_w = 50$, and $e^{50}$ is a box larger than any image. Cap the offset, then clip the box to the image.
- **Regressing far boxes.** Training on reference boxes with a low IoU adds targets that the model cannot fit and makes the near ones worse.

## Exercises

1. Show that DECODE(a, ENCODE(a, g)) = g and ENCODE(a, DECODE(a, t)) = t for all boxes with positive sizes and all $t \in \mathbb{R}^4$.
2. Two boxes have the same height and $y$ range, the same width $w$, and centers $d$ apart with $d \le w$. Show that their IoU is $(w - d)/(w + d)$, and find the largest center error in widths that keeps an IoU of 0.5.
3. Show that if the target width is $w_a e^{e}$ and everything else is exact, the IoU is $e^{-|e|}$. What IoU does the ratio form $w/w_a - 1 = e$ give for $e = 0.5$ and $e = -0.5$?
4. Write the inclusive form of DECODE so that it inverts the inclusive ENCODE, and check it on the box $(0, 0, 9, 9)$ and the target $(2, 1, 13, 8)$.
5. Show that $\Phi^{\mathsf T}\Phi + \lambda I$ is positive definite for $\lambda > 0$, so line L8 has exactly one solution even when two features are equal.

## References
