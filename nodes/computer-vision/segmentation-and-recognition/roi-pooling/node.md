---
tag: BAJKQQ
kind: technique
slug: roi-pooling
name: RoI pooling
aliases:
- region of interest pooling
- RoIAlign
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Turn the feature cells under a box into a fixed grid by max pooling over rounded bins. RoIAlign, with bilinear samples and no rounding, is the different step of Mask R-CNN."
prereqs: [object-proposals, convolution]
see_also: [fast-r-cnn, faster-r-cnn, r-cnn, mask-r-cnn, bilinear-interpolation, feature-pyramid-network, backpropagation]
sources:
  - paper: doi:10.1109/ICCV.2015.169
    title: "Ross Girshick, Fast R-CNN, ICCV 2015, 1440-1448"
    locator: "Section 2.1, The RoI pooling layer (an H x W grid of sub-windows of about h/H x w/W, max pooling in each, H = W = 7 for VGG16), and Section 2.3, Back-propagation through RoI pooling layers (Eq. 4)"
  - url: https://github.com/rbgirshick/caffe-fast-rcnn/blob/fast-rcnn/src/caffe/layers/roi_pooling_layer.cpp
    title: "Ross Girshick, caffe-fast-rcnn, the RoI pooling layer of the reference Fast R-CNN code (MIT license)"
    locator: "Forward_cpu (round of the box times spatial_scale, inclusive size, floor and ceil bin limits, clipping, empty bins set to 0, argmax switches)"
  - paper: doi:10.1109/ICCV.2017.322
    title: "Kaiming He, Georgia Gkioxari, Piotr Dollar and Ross Girshick, Mask R-CNN, ICCV 2017"
    locator: "Section 3, paragraph RoIAlign (the misalignment from quantization, bilinear samples with no rounding)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

RoI pooling turns the part of a convolutional feature map under one box into a grid of fixed size, $H \times W$ cells per channel, so that the same fully connected layers can classify boxes of every size. [Fast R-CNN](/fast-r-cnn/) introduced it to share one pass of the network over the whole image among all the [object proposals](/object-proposals/), where [R-CNN](/r-cnn/) ran the network once per proposal. The layer rounds the box to feature cells, cuts it into $H \times W$ bins of nearly equal size, and takes the maximum of each bin. Its backward pass sends each output gradient to the one input cell that gave the maximum. The rounding makes the output a step function of the box position. RoIAlign, the replacement in [Mask R-CNN](/mask-r-cnn/), is a different operation: it samples the map by [bilinear interpolation](/bilinear-interpolation/) at points with no rounding.

## In plain words

A detector has computed a grid of features for the whole image, and it has a list of candidate boxes of all sizes. The classifier after it wants the same amount of input for every box. RoI pooling cuts the part of the feature grid under each box into, for example, 7 by 7 pieces. A big box gives big pieces, a small box gives small ones. From each piece it keeps only the largest value. So every box gives exactly 7 by 7 numbers per feature channel. The features are computed once for the image, and each box only reads its own part of them. The cost is that the box is first snapped to the coarse feature grid, so its position becomes a little inexact.

## When it applies

The technique needs a feature map $F$ with $C$ channels and $h_F \times w_F$ cells, computed from the image by layers whose stride is $1/s$ pixels per cell, so $s = 1/16$ for the last convolution of VGG16. A box is $(x_1, y_1, x_2, y_2)$ in image pixels. The output size $H \times W$ is fixed by the layers that follow.

It fits a two-stage detector, where a fixed set of boxes is given and each needs a fixed-size feature: Fast R-CNN with external proposals, and [Faster R-CNN](/faster-r-cnn/) with its own proposals. With a [feature pyramid network](/feature-pyramid-network/), each box is pooled from the level that fits its size. It fits less well when the exact position matters, for example for masks or for a high IoU threshold, since the rounding moves the box by up to half a cell.

## The template

```pseudo id=template
ROIPOOL(F, b, s, H, W)            ▷ feature map F (C x h_F x w_F), box b in pixels, scale s
L1  (c_1, r_1, c_2, r_2) ← round(s · b)        ▷ the box in cells, inclusive ends, halves away from 0
L2  h ← max(r_2 - r_1 + 1, 1),  w ← max(c_2 - c_1 + 1, 1)
L3  for each bin (p, q) with 0 ≤ p < H and 0 ≤ q < W
L4      rows ← [r_1 + ⌊p h / H⌋, r_1 + ⌈(p + 1) h / H⌉) clipped to [0, h_F]
L5      cols ← [c_1 + ⌊q w / W⌋, c_1 + ⌈(q + 1) w / W⌉) clipped to [0, w_F]
L6      for each channel c: Y[c][p][q] ← max of F[c] over rows x cols, S[c][p][q] ← its first argmax; 0 and none if the bin is empty
L7  return Y, S

BACKWARD(dY, S)                   ▷ dY: the gradient of the loss with respect to Y
L8  dF[c][S[c][p][q]] += dY[c][p][q] for every c, p, q with a nonempty bin; all other dF are 0
```

Lines L4 and L5 follow the reference Caffe layer, which uses floor at the start and ceil at the end of each bin. So the bins of one box cover all its cells, next bins share at most one row or column, and every bin of a box inside the map has at least one cell, also when the box has fewer cells than bins. The forward pass is a maximum, and the backward pass is its gradient wherever each bin has one largest value: a small change of a cell that is the maximum of $k$ bins changes the loss by the sum of those $k$ output gradients, and a change of any other cell does nothing. These facts are proved in [the proof page](proofs/correctness.md).

**Cost.** For one box, lines L4 to L6 read each cell of a bin once per channel, so the forward pass takes $O(C (h + H)(w + W))$ time, since the bins cover the box with at most one shared row or column between neighbors. The backward pass takes $O(C H W)$ time. For $R$ boxes the forward pass is $O(C \sum_r (h_r + H)(w_r + W))$, and the network that makes $F$ runs once for the image, which is the saving over R-CNN. The network cost is outside this page.

**Example.** Take one channel with $6 \times 8$ cells and the value $(3r + 5c) \bmod 11$ at row $r$ and column $c$, the scale $s = 1/4$, the box $(5, 3, 26, 17)$ and a $2 \times 2$ output. Line L1 gives $(1.25, 0.75, 6.5, 4.25)$ rounded to $(1, 1, 7, 4)$, so the box covers rows 1 to 4 and columns 1 to 7, with $h = 4$ and $w = 7$. The row ranges are $[1, 3)$ and $[3, 5)$. The column ranges are $[1, 1 + \lceil 3.5 \rceil) = [1, 5)$ and $[1 + \lfloor 3.5 \rfloor, 8) = [4, 8)$, so column 4 is in both. The four maxima are 10 at $(2, 3)$, 9 at $(2, 5)$, 10 at $(4, 4)$ and 10 at $(4, 4)$ again. With all output gradients equal to 1, the backward pass gives 2 at $(4, 4)$, 1 at $(2, 3)$ and at $(2, 5)$, and 0 elsewhere. The box $(5, 2, 26, 16)$, one pixel higher, rounds to the same cells and gives the same output.

**Implementation.** The Python code has the forward pass with the rounding of the Caffe layer in exact integer form, the switches, the backward pass, and a helper for a list of boxes. It does not have RoIAlign. The tests check the example above, the C rounding of halves, the bin limits against floor and ceil on 300 random sizes, the outputs and switches against a brute force maximum, the backward pass against finite differences, the equality under a shift by whole cells, a one-pixel shift that the rounding hides, and empty and one-cell boxes.

## Classic examples

- **Fast R-CNN.** RoI pooling on the conv5 map of VGG16 with $H = W = 7$ and $s = 1/16$, for about 2000 selective search proposals per image. The paper reports a test time of about 0.3 seconds per image without the proposal step, against many seconds for R-CNN (benchmark results of the 2015 paper).
- **Faster R-CNN.** The same layer on the proposals of the region proposal network, so the two stages share one feature map.
- **SPP-net.** The forerunner of RoI pooling: a spatial pyramid of max pooling grids, for example $1 \times 1$, $2 \times 2$, $3 \times 3$ and $6 \times 6$, on the region of each window. RoI pooling is the case of one level, and Fast R-CNN made the layer trainable end to end.
- **Feature pyramid network.** Each box is pooled from the pyramid level $P_k$ with $k = \lfloor k_0 + \log_2(\sqrt{wh}/224) \rfloor$ and $k_0 = 4$, so a small box reads a fine map.

## Variations

- **RoIAlign.** Mask R-CNN keeps the box and the bin limits as real numbers, samples a few points in each bin by bilinear interpolation, and takes their average or maximum. The output is then a continuous function of the box, and the paper reports large gains in mask accuracy and gains in box accuracy (benchmark results).
- **Precise RoI pooling.** Integrates the bilinear interpolant over each bin, which makes the output differentiable in the box coordinates too.
- **Position-sensitive RoI pooling.** R-FCN pools bin $(p, q)$ from its own group of channels, so the per-box layers after the pooling are almost free.
- **Average pooling.** Takes the mean of each bin instead of the maximum; the backward pass then spreads the gradient evenly over the bin.
- **Crop and resize.** Some code crops the box from the map and resizes the crop to $H \times W$ with bilinear interpolation, which is close to RoIAlign with one sample per bin.

## Pitfalls

- **Misalignment.** Rounding the box to cells moves each side by up to half a cell, 8 pixels at $s = 1/16$, and the floor and ceil of the bins add up to one more cell. For a small box this is a large part of its size. It is the problem that RoIAlign solves.
- **Inclusive ends.** The Caffe layer counts $c_2 - c_1 + 1$ cells. Code that uses $c_2 - c_1$ pools a box one cell smaller, and trained weights do not carry over.
- **Rounding rules.** C `round` sends halves away from zero, Python `round` sends them to the even integer, and floor and ceil computed in floating point can differ from the exact values at whole numbers. Each changes some boxes by a cell.
- **Empty bins.** A box partly or fully outside the map has empty bins. The layer outputs 0 there and passes no gradient.
- **No gradient for the box.** The output is a step function of the box coordinates, so its derivative with respect to the box is 0 almost everywhere. Box quality can only be learned by the regression head, not through the pooling.
- **Ties.** With equal values in a bin, the switch is the first in row-major order, and the whole gradient goes to that one cell.

## Exercises

1. Show that for $h \ge 1$ the row ranges of line L4 (before the clipping) cover $[r_1, r_1 + h)$, that each is nonempty, and that their lengths sum to at most $h + H - 1$.
2. A box has $h = 5$ rows and the output has $H = 7$ rows. List the row ranges of the seven bins. Which rows appear in two bins?
3. Show that the backward pass of line L8 is the gradient of $\sum_{c, p, q} dY[c][p][q] \, Y[c][p][q]$ with respect to $F$ at any $F$ whose bins each have one largest value.
4. At $s = 1/16$, find two boxes whose sides differ by 15 pixels and that give the same output on every feature map.
5. Write RoIAlign with one sample at the center of each bin, and show that its output is a continuous function of the box coordinates.

## References
