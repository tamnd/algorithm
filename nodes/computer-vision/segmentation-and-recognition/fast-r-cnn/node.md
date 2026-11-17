---
tag: CTWF7A
kind: algorithm
slug: fast-r-cnn
name: Fast R-CNN
aliases:
- Fast RCNN
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Compute the CNN features of an image once, pool each proposal from them by RoI pooling, and classify and regress all proposals in one network.
solves: [object-detection]
model: real-ram
complexity:
  vars: {R: the number of RoIs, K: the number of object classes, c: the number of channels, m: the largest side of an RoI in feature cells, H: the number of bins per side}
  time: {worst: "O(R c (m + H)^2 + K R^2)"}
  space: {extra: "O(c H^2 + R K)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Ross Girshick]
  note: "Put on arXiv in April 2015 and presented at ICCV 2015. It trained one network for classification and box regression, end to end except for the proposals."
prereqs: [r-cnn, roi-pooling, bounding-box-regression, box-non-maximum-suppression]
see_also: [faster-r-cnn, selective-search, softmax-regression, cross-entropy-loss, huber-m-estimator, backpropagation, stochastic-gradient-descent, object-detection]
sources:
  - paper: doi:10.1109/ICCV.2015.169
    title: "Ross Girshick, Fast R-CNN, ICCV 2015, 1440-1448"
    locator: "Section 2.1, The RoI pooling layer (H = W = 7 for VGG16); Section 2.3, Fine-tuning for detection (multi-task loss with smooth L1 and lambda = 1, mini-batches of N = 2 images and R = 128 RoIs, 25 percent foreground at IoU 0.5 or more, background in [0.1, 0.5), back-propagation through RoI pooling); Section 2.4, Scale invariance (s = 600); Section 3, Fast R-CNN detection and Section 3.1, Truncated SVD; Section 4, Main results"
  - url: https://arxiv.org/abs/1504.08083
    title: "Ross Girshick, Fast R-CNN, arXiv 1504.08083"
    locator: "the same sections; the abstract gives 9 times faster training and 213 times faster testing than R-CNN with VGG16"
  - paper: doi:10.1109/CVPR.2014.81
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, CVPR 2014, 580-587"
    locator: "Section 2, the R-CNN pipeline that Fast R-CNN replaces"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Fast R-CNN is the detector that fixed the speed problem of [R-CNN](/r-cnn/). R-CNN ran a CNN on each of about 2000 warped proposals. Fast R-CNN runs the convolutional layers once on the whole image, and then cuts a fixed-size feature grid for each proposal out of the shared feature map with [RoI pooling](/roi-pooling/). Fully connected layers turn each grid into two outputs: a softmax over $K$ object classes and background, and four box offsets for each class, the encoding of [bounding box regression](/bounding-box-regression/). One multi-task loss, a log loss plus a smooth L1 box loss, trains the whole network at once, with gradients that flow back through RoI pooling. With VGG16 it trains 9 times faster than R-CNN and tests 213 times faster, at about 0.3 seconds per image, with a higher mAP. The proposals still come from outside, usually from [selective search](/selective-search/); [Faster R-CNN](/faster-r-cnn/) moved them into the network.

## In plain words

R-CNN looked at each candidate box of a photo on its own, so it read the same pixels again and again. Fast R-CNN reads the whole photo once and makes a map of features, a smaller grid where each cell describes a patch of the photo. For each candidate box it takes the part of the map under the box and squeezes it into a small grid of fixed size, say 7 by 7, by taking the largest value in each part. Then a small network looks at that grid and answers two questions at once: what is in the box, and how should the box move to fit the object. Both answers are learned together. Many boxes then land on the same object, so the best box is kept and the others are removed.

## The problem

The input is an image, a set of proposals (RoIs) in image pixels, and a trained network in two parts: the convolutional layers, which give a feature map with $c$ channels at a stride of $1/\text{scale}$ pixels (16 for VGG16), and a head that maps an $H \times W$ grid of pooled features to $K + 1$ class scores and $4K$ offsets. The output is a list of boxes with a class and a score. How good it is depends on the training and is measured by [detection mean average precision](/detection-mean-average-precision/). This page proves facts about the steps that are not learned, and leaves the network out.

## The algorithm

```pseudo id=main
FAST-R-CNN-DETECT(I, RoIs, conv, head, τ)
L1  F ← conv(I scaled so that its shorter side is s)      ▷ once per image, outside this page
L2  for each RoI r
L3      x_r ← ROI-POOL(F, r · scale) into H × W bins       ▷ max over each bin
L4      (z_r, t_r) ← head(x_r); p_r ← softmax(z_r)          ▷ K + 1 scores, 4K offsets
L5  for each class k = 1, ..., K
L6      B_{r,k} ← DECODE(r, t_r^k) for every r
L7      keep_k ← greedy NMS of the B_{r,k} with scores p_{r,k} at threshold τ
L8  return the detections (k, p_{r,k}, B_{r,k}) for r in keep_k, for every k
```

**RoI pooling (line L3).** The RoI is mapped to feature cells and split into $H \times W$ bins of about equal size, here $7 \times 7$, and each bin takes the maximum of its cells in each channel. The output size does not depend on the RoI size, so the fully connected layers of a classification network fit on top. The exact rounding and the backward pass are on the [RoI pooling](/roi-pooling/) page: the gradient of a bin goes to the cell that held its maximum, and a cell that is the maximum of several bins gets the sum.

**The multi-task loss.** For an RoI with true class $u$ (0 for background) and box target $v$, with $p$ the softmax and $t^u$ the offsets for class $u$,

$$L(p, u, t^u, v) = -\log p_u + \lambda [u \ge 1] \sum_{i \in \{x, y, w, h\}} \operatorname{smooth}_{L_1}(t^u_i - v_i), \qquad \operatorname{smooth}_{L_1}(x) = \begin{cases} 0.5 x^2 & |x| < 1 \\ |x| - 0.5 & \text{otherwise.} \end{cases}$$

The paper uses $\lambda = 1$ and normalizes the targets $v$ to zero mean and unit variance, so decoding first undoes that normalization. Background RoIs have no box loss. The smooth L1 term is the [Huber loss](/huber-m-estimator/) with threshold 1: its gradient has absolute value at most 1, so a far-off target cannot make the gradient explode, which the L2 loss of R-CNN could.

**Mini-batches.** SGD uses $N = 2$ images and $R = 128$ RoIs per batch, so 64 RoIs per image. Up to 25 percent are foreground, RoIs with IoU at least 0.5 with a ground truth box, which take that box's class. The rest are background, RoIs whose largest IoU is in $[0.1, 0.5)$. The lower limit 0.1 acts as a simple form of hard example mining. Since the RoIs of one image share their feature map, a batch of 128 RoIs from 2 images costs about as much as 2 images, not 128.

**Truncated SVD.** At test time the fully connected layers take a large part of the time, since they run once per RoI. Fast R-CNN replaces a layer $W$ with the two smaller layers of its rank-$t$ truncated singular value decomposition $U_t \Sigma_t V_t^T$, which cuts the cost from $uv$ to $t(u + v)$ for a $u \times v$ matrix.

## Example

One ground truth box $g = (0, 0, 10, 10)$ of class 1 and five RoIs:

| RoI | box | IoU with $g$ | role |
|---|---|---|---|
| $r_1$ | (0, 0, 10, 8) | 4/5 | foreground, class 1 |
| $r_2$ | (0, 0, 10, 6) | 3/5 | foreground, class 1 |
| $r_3$ | (6, 0, 16, 10) | 1/4 | background |
| $r_4$ | (9, 0, 19, 10) | 1/19 | not used, below 0.1 |
| $r_5$ | (30, 30, 40, 40) | 0 | not used |

A batch of 4 RoIs from this image takes one foreground RoI (25 percent of 4) at random and fills the rest with background; only $r_3$ qualifies, so the batch has 2 RoIs. Say the network gives $r_1$ the softmax $(0.2, 0.8)$ and the offsets $t^1 = (0.5, -2, 0, 0.1)$, and its target is $v = 0$. The loss is

$$-\log 0.8 + (0.125 + 1.5 + 0 + 0.005) \approx 0.223 + 1.630 = 1.853.$$

The second offset is in the linear part of smooth L1, so it adds $2 - 0.5 = 1.5$ and not $0.5 \cdot 4 = 2$. For a background RoI only $-\log p_0$ counts, whatever the offsets.

For RoI pooling, the check value of the [RoI pooling](/roi-pooling/) page applies: on the map $(3r + 5c) \bmod 11$ of $6 \times 8$ cells, the box $(5, 3, 26, 17)$ at scale $1/4$ pools to $[[10, 9], [10, 10]]$ on a $2 \times 2$ grid.

## Correctness

The network has no correctness theorem; its accuracy is measured. For the steps that are not learned, [the proof page](proofs/correctness.md) shows:

1. **RoI pooling and its gradient.** Each bin outputs the maximum of its cells, and where the maximum is unique the backward pass is the exact gradient of the pooled output with respect to the feature map.
2. **Loss.** Smooth L1 is continuous with a continuous derivative of absolute value at most 1, and the loss has no box term for background RoIs.
3. **Decoding.** Decoding with the normalization undone inverts the encoding.
4. **Sampling.** Every sampled foreground RoI has IoU at least 0.5 with the box whose class it takes, every background RoI has largest IoU in $[0.1, 0.5)$, and there are at most $\operatorname{round}(0.25 \cdot \text{batch})$ foreground RoIs.
5. **NMS.** The kept boxes of a class overlap by at most $\tau$, and each dropped box overlaps a kept box of at least the same score by more than $\tau$.

The tests check all five, the first by finite differences.

## Complexity

The convolutional layers run once per image and the head once per RoI; both are outside this page. RoI pooling of an RoI with at most $m$ cells per side into $H \times H$ bins reads at most $(m + H - 1)^2$ cells per channel, since next bins share at most one row or column, so it costs $O(c (m + H)^2)$. The softmax and the decoding cost $O(K)$ per RoI, and NMS costs $O(K R^2)$ in the worst case. In total, $O(R c (m + H)^2 + K R^2)$ time and $O(c H^2 + RK)$ extra space beyond the feature map. In the paper, with VGG16 and about 2000 proposals, detection takes about 0.3 seconds per image on a GPU, the proposals not included.

## Properties

- **Shared computation.** The cost of the convolutional layers does not grow with the number of proposals.
- **One-stage training.** Classification and box regression are learned together, and all layers can be fine-tuned, unlike in SPPnet, which could not update the layers below its pooling.
- **No disk cache.** R-CNN stored the features of every proposal for SVM training; Fast R-CNN trains from images.
- **Deterministic at test time** given the proposals; not exact, since it is a learned method.
- **Still two stages.** The proposals come from a separate method, and with selective search they take more time than the detector itself.

## Variants and improvements

- **Single scale or image pyramid.** The paper tests one scale, $s = 600$ for the shorter side, against a pyramid of five scales; the pyramid helps only a little and costs much more time, so one scale is the default.
- **Softmax or SVMs.** The paper compares the softmax of the network with SVMs trained as in R-CNN and finds that the softmax is slightly better, so the SVM stage is dropped.
- **Faster R-CNN.** A region proposal network on the same feature map replaces selective search; see [Faster R-CNN](/faster-r-cnn/).
- **RoIAlign.** [Mask R-CNN](/mask-r-cnn/) replaces the rounding of RoI pooling with [bilinear](/bilinear-interpolation/) samples, which matters for masks and small objects.
- **Feature pyramids.** With a [feature pyramid network](/feature-pyramid-network/), each RoI is pooled from the level that matches its size.

## When to use it

Use Fast R-CNN when good proposals are already at hand, for example from a different sensor, a tracker or a fixed set of regions, and a detector must classify and refine them. As a full detector it is replaced by Faster R-CNN, which needs no outside proposals. Its parts, RoI pooling and the multi-task loss, are still the head of most two-stage detectors.

## Pitfalls

- **Wrong scale.** RoIs are in image pixels of the scaled image; mapping them with the wrong scale, or forgetting the resize of line L1, puts every pooled grid in the wrong place.
- **Normalized targets.** If training normalizes the targets, test-time decoding must undo it with the same mean and deviation.
- **Background range.** RoIs with IoU below 0.1 are not used as background in the paper; using all of them gives many easy negatives.
- **Class-specific offsets.** The offsets of class $k$ are $t^k$; decoding all classes with the offsets of the best class is a different, weaker variant.
- **Ties in max pooling.** Equal values in a bin send the whole gradient to one cell; the choice must match between the forward and the backward pass.
- **Proposal time.** The 0.3 seconds do not include selective search, which takes seconds per image on a CPU.

## Implementations

The network is outside this page: the Python code takes the feature map and the head as inputs, and the tests build both by hand on tiny maps. The code implements RoI pooling with the rounding of the original Caffe layer and its backward pass, the softmax, the decoding with target normalization, NMS for each class, the sampling of a mini-batch of RoIs, and the multi-task loss with smooth L1. The tests check the example above, the RoI pooling check value, the backward pass against finite differences on random maps, decoding against the encoding, a small detection run, the sampling rules on random boxes, and the smooth L1 function and its gradient.

## History

R-CNN (2014) was accurate but slow, since it ran the network once per proposal. He, Zhang, Ren and Sun's SPPnet (2014) shared the convolutional layers and pooled each proposal with a spatial pyramid, but kept the multi-stage training of R-CNN and could not fine-tune the layers below the pooling. Girshick's Fast R-CNN, on arXiv in April 2015 and at ICCV 2015, used a single-level pyramid, the RoI pooling layer, trained everything in one network with a multi-task loss, and reached 66.9 percent mAP on VOC 2007. It was released with open Caffe code, and later in 2015 Ren, He, Girshick and Sun added the region proposal network to make [Faster R-CNN](/faster-r-cnn/).

## References
