---
tag: 4YN1M9
kind: algorithm
slug: r-cnn
name: R-CNN
aliases:
- regions with CNN features
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Detect objects by warping each selective search proposal to a fixed size, extracting CNN features, classifying them with SVMs and regressing the box.
solves: [object-detection]
model: real-ram
complexity:
  vars: {P: the number of proposals, C: the number of classes, d: the feature length, S: the side of the warped patch}
  time: {worst: "O(P S^2 + P C d + C P^2)"}
  space: {extra: "O(S^2 + P (d + C))"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Ross Girshick, Jeff Donahue, Trevor Darrell, Jitendra Malik]
  note: "Put on arXiv in November 2013 and presented at CVPR 2014. It showed that features of a CNN trained for image classification and fine-tuned for detection beat the hand-made features of the time by a wide margin."
prereqs: [selective-search, support-vector-machine, bounding-box-regression, box-non-maximum-suppression]
see_also: [fast-r-cnn, faster-r-cnn, object-proposals, deformable-part-model, dalal-triggs-detector, object-detection, intersection-over-union, bilinear-interpolation]
sources:
  - paper: doi:10.1109/CVPR.2014.81
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, CVPR 2014, 580-587"
    locator: "Section 2.1, Module design (about 2000 selective search proposals, warping to 227 x 227); Section 2.2, Test-time detection (SVM scores and greedy NMS for each class, 13 s per image on a GPU and 53 s on a CPU); Section 2.3, Training (IoU 0.5 for fine-tuning, 32 positive and 96 background windows per batch of 128, SVM negatives below IoU 0.3 chosen by a grid search, hard negative mining)"
  - url: https://arxiv.org/abs/1311.2524
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, arXiv 1311.2524, version 5 with appendices"
    locator: "Appendix A, Object proposal transformations (context padding p = 16, the image mean outside the image, 3 to 5 mAP points over the other choices); Appendix B, Positive vs. negative examples and softmax (54.2 to 50.9 mAP on VOC 2007); Appendix C, Bounding-box regression (lambda = 1000, pairs with IoU above 0.6); Table 1 (VOC 2010) and Table 2 (VOC 2007)"
  - paper: doi:10.1007/s11263-013-0620-5
    title: "Jasper R. R. Uijlings, Koen E. A. van de Sande, Theo Gevers and Arnold W. M. Smeulders, Selective search for object recognition, International Journal of Computer Vision 104(2), 2013, 154-171"
    locator: "Section 3, the fast mode that R-CNN uses for its proposals"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

R-CNN is the first detector that used the features of a deep convolutional network (CNN) for [object detection](/object-detection/) at the scale of PASCAL VOC. It works in three stages. [Selective search](/selective-search/) gives about 2000 class-agnostic [proposals](/object-proposals/) per image. Each proposal is grown by a margin of context, warped to a fixed $227 \times 227$ patch and passed through a CNN that was trained for image classification and then fine-tuned on the warped proposals. A linear [support vector machine](/support-vector-machine/) for each class scores the features, a class-specific [box regression](/bounding-box-regression/) corrects the box, and greedy [non-maximum suppression](/box-non-maximum-suppression/) for each class removes duplicates. The CNN runs once for each proposal, which made R-CNN slow: 13 seconds per image on a GPU. [Fast R-CNN](/fast-r-cnn/) removed that cost by running the network once for each image.

## In plain words

First ask a cheap method, selective search, for about 2000 boxes that could hold an object. Cut each box out of the photo with a small border, and stretch it to a square of fixed size, because the network only takes one input size. Run the network on each square to get a long list of numbers that describe it. For each kind of object, such as "cat" or "car", a simple linear rule turns those numbers into a score. A second small rule nudges the box so that it fits the object better. Many boxes land on the same cat, so keep the best one and drop the boxes that overlap it too much. The network is the slow part: it runs 2000 times for one photo.

## The problem

The input is an image, a set of $C$ object classes, and trained parts: a feature function $\phi$ that maps a $S \times S$ patch to a vector in $\mathbb{R}^d$ (the CNN, with $S = 227$ and $d = 4096$ in the paper), a linear classifier $(w_c, b_c)$ for each class, and a box regressor for each class. The output is a list of boxes, each with a class and a score. Boxes are $(x_1, y_1, x_2, y_2)$ in continuous pixel coordinates, where pixel $(u, v)$ covers $[u, u + 1) \times [v, v + 1)$. How good the output is depends on the trained parts and is measured by [detection mean average precision](/detection-mean-average-precision/); this page proves facts about the steps that are not learned.

## The algorithm

```pseudo id=main
R-CNN-DETECT(I, proposals, φ, {(w_c, b_c)}, {reg_c}, τ)
L1  for each proposal p of the about 2000 from selective search
L2      warp the context box of p, filled with the image mean outside I, to an S × S patch
L3      f_p ← φ(patch)                          ▷ the CNN, outside this page
L4  for each class c
L5      s_{p,c} ← w_c · f_p + b_c for every p
L6      B_{p,c} ← DECODE(p, reg_c(f_p)) for every p
L7      keep_c ← greedy NMS of the boxes B_{p,c} with scores s_{p,c} at IoU threshold τ
L8  return the detections (c, s_{p,c}, B_{p,c}) for p in keep_c, for every c
```

**The context box (line L2).** Appendix A of the paper grows the box about its center so that, after the warp to $S \times S$, there are exactly $p = 16$ pixels of context around the original box. So each side grows by the factor $S / (S - 2p) = 227/195$. The warp scales the two axes on their own, so the aspect ratio of the object changes. Where the grown box goes past the image border, the missing pixels take the mean of the image, which the network input later subtracts.

**Scores and boxes (lines L5 and L6).** The SVM score is a dot product with the 4096 features of the second fully connected layer. The regressor is a ridge regression on the features of the last pooling layer that predicts the offsets $d = (d_x, d_y, d_w, d_h)$ of [bounding box regression](/bounding-box-regression/): with $p$ in center form $(p_x, p_y, p_w, p_h)$, the box is $(p_x + p_w d_x, p_y + p_h d_y, p_w e^{d_w}, p_h e^{d_h})$. The NMS threshold $\tau$ of line L7 is, in the words of the paper, a learned threshold, set on held-out data.

**Training labels.** Training has three steps, and each uses its own labels. They are a frequent source of confusion.

1. *Fine-tuning* of the CNN as an $(N + 1)$-way classifier: a proposal takes the class of the ground truth box it overlaps most if that IoU is at least 0.5, and is background otherwise. Each batch of 128 windows holds 32 positive and 96 background windows.
2. *The SVM of class $c$*: the positives are the ground truth boxes of class $c$ only, the negatives are the proposals with IoU below 0.3 with every box of class $c$, and the proposals in between are left out. Hard negative mining picks the negatives, since they do not fit in memory.
3. *The box regressor*: the pairs are a proposal and the ground truth box it overlaps most, if that IoU is above 0.6, with a ridge penalty of $\lambda = 1000$.

## Example

One ground truth box of class 1, $g = (0, 0, 10, 10)$, and five proposals:

| proposal | box | IoU with $g$ | fine-tuning | SVM | regression |
|---|---|---|---|---|---|
| $p_1$ | (0, 0, 10, 8) | 4/5 | class 1 | left out | pair |
| $p_2$ | (0, 0, 10, 5) | 1/2 | class 1 | left out | no |
| $p_3$ | (5, 0, 15, 10) | 1/3 | background | left out | no |
| $p_4$ | (6, 0, 16, 10) | 1/4 | background | negative | no |
| $p_5$ | (20, 20, 30, 30) | 0 | background | negative | no |

The SVM gets one positive, $g$ itself, and two negatives. Now let the scores of class 1 be 0.9, 0.6, 0.4, 0.3 and 0.2, with no box offsets, and $\tau = 0.3$. NMS keeps $p_1$. It drops $p_2$, since $\text{IoU}(p_1, p_2) = 50/80 = 0.625$. It keeps $p_3$, since $\text{IoU}(p_1, p_3) = 40/140 \approx 0.286$. It drops $p_4$, since $\text{IoU}(p_3, p_4) = 90/110 \approx 0.82$, and it keeps $p_5$. The output is $p_1, p_3, p_5$ with their scores; a threshold of 0.7 keeps $p_2$ as well. The context box of a $195 \times 195$ proposal at the origin is $(-16, -16, 211, 211)$, a square of side 227.

## Correctness

The trained parts have no correctness theorem; their quality is measured. For the steps of lines L2 and L5 to L7 and the labels, [the proof page](proofs/correctness.md) shows:

1. **Context.** In the warped patch the edges of the original proposal land exactly at $p$ and $S - p$, for any box.
2. **Warp.** The bilinear warp, inside the image, reproduces an image that is an affine function of the pixel position exactly, so the patch is the original image under the affine map from the box to the square.
3. **Decoding.** Decoding with the offsets of the encoding of $g$ relative to $p$ gives $g$ back, and zero offsets give $p$.
4. **Labels.** Every regression pair is also a fine-tuning positive of the class of its box, and every SVM negative of class $c$ has a fine-tuning label other than $c$.
5. **NMS.** The kept boxes of a class overlap each other by at most $\tau$, and every dropped box overlaps a kept box with a score at least as high by more than $\tau$.

## Complexity

The network, which runs $P$ times, costs far more than the rest and is not part of the page. With $P$ proposals, $C$ classes, features of length $d$ and patches of side $S$, the warps cost $O(P S^2)$, the scores $O(P C d)$ (one $P \times d$ by $d \times C$ matrix product), the decoding $O(PC)$ and NMS $O(C P^2)$ in the worst case. Extra space is $O(S^2)$ for one patch and $O(P(d + C))$ for the features and scores. The paper reports 13 seconds per image on a GPU and 53 seconds on a CPU, almost all of it in the network, and notes that the class-specific part is cheap: all scores of an image are one matrix product of $2000 \times 4096$ features by $4096 \times N$ weights, which for 100000 classes takes about 10 seconds on a multi-core CPU.

## Properties

- **Deterministic at test time.** Selective search, the warp, the scores and NMS have no random step.
- **Not exact.** It is a learned method for a problem with no exact output.
- **Separate stages.** The proposals, the CNN, the SVMs and the regressors are trained one after the other, not as one network.
- **No shared computation.** Overlapping proposals pass the same pixels through the network many times.
- **Recall bounded by the proposals.** An object with no proposal at IoU 0.5 or more is lost, and the regression can fix only small errors.

## Variants and improvements

- **Other proposals.** The pipeline does not depend on selective search; the paper chose it to compare with earlier detectors that used it. Any method for the [object proposal](/object-proposals/) problem can take its place.
- **Softmax instead of SVMs.** Appendix B uses the 21-way softmax of the fine-tuned network. On VOC 2007 mAP drops from 54.2 to 50.9 percent, which the authors explain by the positives of fine-tuning, which do not stress precise localization, and by the random negatives in place of hard negatives.
- **SPPnet.** He et al. (2014) ran the convolutional layers once for each image and pooled each proposal from the shared feature map with spatial pyramid pooling, which is much faster at test time.
- **Fast R-CNN.** Girshick (2015) pooled each proposal with [RoI pooling](/roi-pooling/) and trained classification and box regression together in one network.
- **Faster R-CNN.** Ren et al. (2015) made the proposals with a network that shares the features, the region proposal network of [Faster R-CNN](/faster-r-cnn/).

## When to use it

Today R-CNN is mainly of teaching and historical interest. Its parts are easy to see one at a time: proposals, a fixed-size warp, features, a linear classifier, box regression and NMS. Use it as a baseline when the classifier must be trained apart from the feature extractor, for example with a frozen feature model and few labels. For real detection use Fast R-CNN, Faster R-CNN or a one-stage detector such as the [single shot multibox detector](/single-shot-multibox-detector/).

## Pitfalls

- **Mixing the label rules.** The fine-tuning threshold of 0.5, the SVM negatives below 0.3 with only the ground truth as positives, and the regression pairs above 0.6 are three different rules. Using one rule for all changes the results.
- **No context padding.** In the pilot tests of Appendix A, warping with 16 pixels of context beat the other choices by 3 to 5 mAP points.
- **Forgetting the mean fill.** A context box that crosses the border needs a fill value; zero is a strong dark edge after mean subtraction.
- **Regression on the wrong box.** The offsets are relative to the proposal, not to the context box. Regress once: Appendix C found that scoring and regressing the new box again does not help.
- **NMS across classes.** NMS runs for each class on its own; a cat and a dog in the same place must both survive.
- **Speed.** Running the CNN 2000 times per image is the reason for the 13 seconds; caching the features to disk for SVM training also takes much space.

## Implementations

The CNN is outside this page: the Python code takes the feature function as an argument, and the tests pass a small hand-written function on the warped patch, as do the SVM weights and the box regressors. The code implements the context box, the bilinear warp with the image mean outside the image, the SVM scores, the class-specific decoding, greedy NMS for each class, and the three training label rules. The tests check the example above, the context box against the margin of $p$ pixels, the warp against an affine image, decoding against the encoding, a small end-to-end run on a synthetic image with a bright square, and the label rules and NMS on random boxes with a fixed seed.

## History

Before R-CNN, the best detectors on PASCAL VOC used hand-made features such as [HOG](/histogram-of-oriented-gradients/) in [deformable part models](/deformable-part-model/), and progress had slowed. Krizhevsky, Sutskever and Hinton showed in 2012 that a large CNN wins image classification. Girshick, Donahue, Darrell and Malik put the paper on arXiv in November 2013 and presented it at CVPR 2014. They took a CNN trained on ImageNet classification, fine-tuned it on warped proposals, and reached 53.7 percent mAP on VOC 2010 and 58.5 percent on VOC 2007 with box regression (54.2 percent without). The name stands for "regions with CNN features". SPPnet, [Fast R-CNN](/fast-r-cnn/) and [Faster R-CNN](/faster-r-cnn/) followed within two years, each removing a slow stage.

## References
