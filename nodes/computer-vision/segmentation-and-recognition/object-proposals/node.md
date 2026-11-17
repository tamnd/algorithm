---
tag: 4TJF3F
kind: problem
slug: object-proposals
name: Object proposal generation
aliases:
- region proposals
- objectness
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Produce a few hundred or thousand boxes or regions likely to contain some object, so that a detector need only classify those.
prereqs: [object-detection, intersection-over-union]
see_also: [selective-search, faster-r-cnn, r-cnn, fast-r-cnn, sliding-window-detection, felzenszwalb-segmentation, roi-pooling, box-non-maximum-suppression]
sources:
  - paper: doi:10.1007/s11263-013-0620-5
    title: "Jasper R. R. Uijlings, Koen E. A. van de Sande, Theo Gevers and Arnold W. M. Smeulders, Selective search for object recognition, International Journal of Computer Vision 104(2), 2013, 154-171"
    locator: "Section 4, Evaluation (recall at IoU 0.5, the average best overlap of Eq. 7 and its mean over classes, MABO), and Table 5 (selective search and objectness on PASCAL VOC 2007 test)"
  - paper: doi:10.1109/TPAMI.2015.2465908
    title: "Jan Hosang, Rodrigo Benenson, Piotr Dollar and Bernt Schiele, What makes for effective detection proposals?, IEEE Transactions on Pattern Analysis and Machine Intelligence 38(4), 2016, 814-830"
    locator: "The average recall measure, recall averaged over IoU thresholds from 0.5 to 1, and its relation to the average precision of detectors"
  - paper: doi:10.1109/TPAMI.2012.28
    title: "Bogdan Alexe, Thomas Deselaers and Vittorio Ferrari, Measuring the objectness of image windows, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(11), 2012, 2189-2202"
    locator: "The objectness measure: a score for any window that it contains an object of any class, from several image cues"
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1, Region proposal networks (proposals from anchors scored by the network, non-maximum suppression at IoU 0.7)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Object proposal generation is the problem of finding, in one image, a short list of boxes or regions that together cover most of the objects in it, of any class. The list does not say what the objects are. It cuts the search space of [object detection](/object-detection/) from all boxes of the image to a few hundred or a few thousand, so that a costly classifier only needs to look at those. A proposal method is judged by recall: the share of the true objects for which some proposal has an [intersection over union](/intersection-over-union/) of at least a threshold, for a given number of proposals. [Selective search](/selective-search/) and the region proposal network of [Faster R-CNN](/faster-r-cnn/) are the best known methods. The alias "objectness" is the name of one score of this kind, the measure of Alexe, Deselaers and Ferrari, and not of the whole problem.

## In plain words

A detector that checks every possible rectangle in a photo would check billions of them. Most are empty sky, half a car or a car with a lot of road. A proposal method makes a short list of rectangles that look like they hold one whole thing, whatever that thing is: a car, a cup, a dog. It does not name them. It only promises that almost every real object in the photo has a rectangle on the list that fits it well. Then the detector looks only at the list. A good method keeps the list short and still misses few objects, because an object that is not on the list cannot be found by the detector later.

## Definition

The input is a [digital image](/digital-image/) $I$ of $W \times H$ pixels and a budget $N$. The output is a ranked list $P = (p_1, \ldots, p_N)$ of boxes $p_k = (x_1, y_1, x_2, y_2)$ in image coordinates, with no class. Some methods return regions (sets of pixels) and use their bounding boxes. The order matters: the first $n$ entries are the answer for every smaller budget $n \le N$.

The quality is measured against a set $\mathcal G$ of true object boxes, from a data set whose objects of all annotated classes count. For a true box $g$ let $o_n(g) = \max_{k \le n} \operatorname{IoU}(g, p_k)$ be its best overlap with the first $n$ proposals. The standard measures are:

- **Recall at a threshold** $\tau$: $R(n, \tau) = |\{g \in \mathcal G : o_n(g) \ge \tau\}| / |\mathcal G|$. The common choice is $\tau = 0.5$, the PASCAL VOC match rule.
- **Average best overlap**: $\operatorname{ABO}(n) = \frac{1}{|\mathcal G|} \sum_{g} o_n(g)$, computed per class. Its mean over the classes is MABO.
- **Average recall**: $\operatorname{AR}(n) = 2 \int_{0.5}^{1} R(n, \tau) \, d\tau$, the recall averaged over thresholds from 0.5 to 1. Hosang et al. found that AR follows the average precision of a detector that uses the proposals better than recall at 0.5 alone.

There is no exact correct output. A method is better than another at budget $n$ when it has a higher recall, ABO or AR there, and methods are compared by the curve over $n$. The running time counts too, since the proposals are only the first step of a detector.

## Variants

- **Box proposals.** The output is boxes only, as in the objectness measure, EdgeBoxes and the region proposal network.
- **Region proposals.** The output is segments, as in [selective search](/selective-search/), CPMC and MCG. The segments can feed a mask predictor, and their boxes feed a box detector.
- **Learned and fixed.** Classic methods use fixed grouping rules or a scoring rule trained once. A region proposal network is trained with the detector and shares its features.
- **Class-specific proposals.** A first stage that already scores some classes, as in cascades. This is closer to detection than to proposals.
- **Video and 3D.** Proposals for tubes over frames, or for 3D boxes from depth or lidar.

## Examples

- **A small computed case.** The true boxes are $g_1 = (0, 0, 10, 10)$ and $g_2 = (20, 0, 30, 10)$. The proposals in rank order are $p_1 = (0, 0, 10, 12)$, $p_2 = (22, 0, 30, 10)$ and $p_3 = (5, 0, 25, 10)$. Then $\operatorname{IoU}(g_1, p_1) = 100/120 = 0.833$, $\operatorname{IoU}(g_2, p_2) = 80/100 = 0.8$, and $p_3$ has IoU $50/250 = 0.2$ with each true box. So $R(1, 0.5) = 1/2$ and $R(2, 0.5) = 1$. With $n = 2$, $R(2, \tau)$ is 1 for $\tau \le 0.8$, $1/2$ for $0.8 < \tau \le 0.833$ and 0 above, so $\operatorname{AR}(2) = 2(0.3 + 0.5 \cdot 0.0333) = 0.633$. The ABO is $(0.833 + 0)/2 = 0.417$ for $n = 1$ and $(0.833 + 0.8)/2 = 0.817$ for $n = 2$; the third proposal does not change it.
- **Selective search on PASCAL VOC 2007 test.** The fast setting gives a recall of 0.980 at IoU 0.5 and a MABO of 0.804 with about 2134 boxes per image; the quality setting gives 0.991 and 0.879 with about 10097 boxes. In the same table the objectness measure gives 0.944 and 0.694 with 1853 boxes (benchmark results of the 2013 paper).
- **Region proposal network.** Faster R-CNN keeps the top 300 proposals per image at test time, after non-maximum suppression at IoU 0.7, and reports a higher detection accuracy than with 2000 selective search proposals on PASCAL VOC 2007 (a benchmark result).
- **A non-example.** A list of class-labelled boxes with scores is a detection output, not a proposal list. A list of all boxes of a sliding window at one size and stride is a valid but weak proposal list.

## Known algorithms

- **Exhaustive windows.** [Sliding-window detection](/sliding-window-detection/) at all positions and a few sizes is the baseline. It needs many windows for a high IoU, see the bounds below.
- **Window scoring.** The objectness measure of Alexe et al. scores windows by cues such as saliency, colour contrast, edge density and how much the window cuts through superpixels. EdgeBoxes scores windows by the number of edge contours that lie wholly inside the box. BING scores windows by a linear model on small binarized gradient maps. These methods sample many windows and keep the best after [non-maximum suppression](/box-non-maximum-suppression/).
- **Grouping.** [Selective search](/selective-search/) starts from the segments of [Felzenszwalb-Huttenlocher segmentation](/felzenszwalb-segmentation/) and merges the most similar neighbors over and over, in several colour spaces and with several similarity measures, keeping the box of every region it makes. CPMC and MCG solve many figure-ground cuts or group a hierarchy of contours, and rank the segments with a learned model.
- **Learned proposals.** The region proposal network of Faster R-CNN scores the [anchor boxes](/anchor-boxes/) of a convolutional feature map and regresses them, then keeps the best after non-maximum suppression. DeepMask and similar networks propose masks.

## Bounds

**The size of the search space.** An image of $W \times H$ pixels has $\binom{W+1}{2}\binom{H+1}{2} = \Theta(W^2 H^2)$ boxes with integer corners: a box picks two of the $W + 1$ grid lines in $x$ and two of the $H + 1$ in $y$. For $500 \times 375$ that is $125250 \cdot 70500 \approx 8.8 \cdot 10^9$ boxes.

**Shift tolerance.** Two boxes of the same width $w$ and the same $y$ range whose $x$ ranges are $d \le w$ apart have IoU $(w - d)/(w + d)$, since the overlap is $(w - d)h$ and the union $(w + d)h$. So the IoU is at least $\tau$ exactly when $d \le w(1 - \tau)/(1 + \tau)$, which is $w/3$ for $\tau = 0.5$ and $w/19$ for $\tau = 0.9$. If both $x$ and $y$ are off, by $d_x$ and $d_y$ for a square of side $w$, the IoU is $q/(2w^2 - q)$ with $q = (w - d_x)(w - d_y)$.

**Windows for a guaranteed recall.** Take square windows of side $w$ on a grid with step $\delta$ and a true square of the same side. Its center is at most $\delta/2$ from a grid point in each axis, so the shift formula gives an IoU of at least $(w - \delta/2)^2 / (2w^2 - (w - \delta/2)^2)$. This is at least $0.5$ exactly when $(w - \delta/2)^2 \ge 2w^2/3$, that is, $\delta \le 2(1 - \sqrt{2/3}) w \approx 0.367 w$, so one size alone needs about $WH / (0.367 w)^2 \approx 7.4 \, WH / w^2$ windows, and a size mismatch or a shape mismatch needs more. For $\tau = 0.7$ the step falls to $2(1 - \sqrt{1.4/1.7}) w \approx 0.185 w$, about four times as many windows. This is why a fixed grid needs many boxes for a high recall at a high IoU, and why proposal methods adapt the boxes to the image.

**Recall limits the detector.** A detector that only scores the proposals, with no change of the boxes, cannot find an object that no proposal covers: a detection is a true positive at IoU $\tau$ only if its box, which is a proposal, has IoU at least $\tau$ with the object. So its recall at $\tau$ is at most $R(N, \tau)$. [Bounding box regression](/bounding-box-regression/) moves the boxes and can beat this limit, but only for proposals that are near the object already.

No worst-case lower bound on the quality is known in a useful form: the measures depend on the data set, and methods are compared by benchmark curves.

## Reductions

- **Detection to proposals and classification.** [R-CNN](/r-cnn/) and [Fast R-CNN](/fast-r-cnn/) reduce detection to object proposals plus a classifier on each proposal and [non-maximum suppression](/box-non-maximum-suppression/). [RoI pooling](/roi-pooling/) makes the classifier step cheap.
- **Proposals to segmentation.** Grouping methods reduce proposals to a hierarchy of [image segmentations](/image-segmentation/): every region of the hierarchy gives a proposal.
- **Proposals to binary detection.** A region proposal network is a detector with two classes, object and background, on anchors.

## Applications

The first stage of two-stage detectors such as R-CNN, Fast R-CNN and Faster R-CNN; weakly supervised detection, where a classifier picks among proposals; instance segmentation from region proposals; object discovery in unlabeled image sets; and visual search, where an index stores the features of proposals.

## References
