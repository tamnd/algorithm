---
tag: 1DDN0J
kind: technique
slug: sliding-window-detection
name: Sliding window detection
aliases:
- exhaustive window scanning
area: computer-vision/segmentation-and-recognition
level: intro
summary: "Run a classifier on windows at every position and scale of an image pyramid and keep the windows it scores high, followed by non-maximum suppression."
prereqs: [image-pyramid]
see_also: [object-detection, viola-jones-detector, dalal-triggs-detector, deformable-part-model, box-non-maximum-suppression, template-matching, integral-image, object-proposals]
sources:
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3 (object detection: face detection and pedestrian detection with scanning windows)"
  - paper: doi:10.1109/CVPR.2005.177
    title: "Navneet Dalal and Bill Triggs, Histograms of oriented gradients for human detection, CVPR 2005"
    locator: "The detection window of 64 by 128 pixels scanned over all positions and scales, and the linear SVM on its HOG descriptor"
  - paper: doi:10.1109/CVPR.2001.990517
    title: "Paul Viola and Michael Jones, Rapid object detection using a boosted cascade of simple features, CVPR 2001"
    locator: "The integral image, the boosted classifier on Haar-like features, the attentional cascade, and the scanning of the detector over locations and scales"
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 3 (filters scored at every position of a feature pyramid) and Section 4 (data mining of hard negative examples)"
---

Sliding window detection turns an image classifier into an [object detector](/object-detection/). It scores a window of fixed size at every position of an image, repeats this on each level of an [image pyramid](/image-pyramid/) so that objects of every size fit the window at some level, keeps the windows that score above a threshold, and removes duplicate hits with [non-maximum suppression](/box-non-maximum-suppression/). It was the standard design of detectors from the 1990s to about 2013, including the [Viola-Jones](/viola-jones-detector/) face detector, the [Dalal-Triggs](/dalal-triggs-detector/) pedestrian detector and the [deformable part model](/deformable-part-model/).

## In plain words

Cut a small paper frame the size of a typical face in your photo. Put it at the top left corner, look through it and ask "is this a face?" Move it a little to the right and ask again. Go across the whole row, then down a little, until you have looked at every place.

Faces near the camera are bigger than the frame. So you shrink the photo a little and do the whole scan again, and keep shrinking until the photo is smaller than the frame. Each time you say yes, mark the place. One face usually gets several marks close together, so at the end you keep only the best mark in each group. The method is simple and sure to look everywhere, but it asks the question very many times.

## When it applies

- The object class has a fairly stable shape and aspect ratio when seen from a typical viewpoint: frontal faces, upright pedestrians, side views of cars, road signs.
- There is a classifier for a fixed-size patch, or one can be trained from cropped positive examples and random negative windows.
- The classifier is cheap per window, or most of its work can be shared between overlapping windows, such as features computed once for the whole image or a cascade that rejects most windows early.
- The objects are not too deformed or occluded. Very flexible objects need parts, as in the deformable part model, and very many aspect ratios need several window shapes.

## The template

Let the window have size $w \times h$ pixels, the stride be $s$ pixels, and the scale step be $\rho > 1$.

1. **Build the pyramid.** For $k = 0, 1, \ldots$ while the image still holds a window, resize the image by $\rho^{-k}$ and compute its features (pixels, an [integral image](/integral-image/), or a grid of [HOG](/histogram-of-oriented-gradients/) cells).
2. **Scan each level.** For every position $(x, y)$ on a grid of step $s$, score the window $f(\text{window at } (x, y))$ with the classifier.
3. **Threshold.** Keep each window whose score is above a threshold $t$. Map it back to the original image: a window at $(x, y)$ on level $k$ is the box $\rho^k (x, y, x + w, y + h)$.
4. **Merge.** Apply non-maximum suppression, or a merge such as averaging overlapping boxes or [mean-shift](/mean-shift/) in position and scale, so that each object gives one detection.

**Cost.** Level $k$ has about $(W \rho^{-k} - w)(H \rho^{-k} - h) / s^2$ windows. Summed over the levels this is at most $\frac{WH}{s^2} \cdot \frac{1}{1 - \rho^{-2}}$, so the finest level dominates, and the total work is this number times the cost $c$ of one classifier call. For example, with the 64 by 128 window of Dalal and Triggs and a stride of 8 pixels (one HOG cell), a 320 by 240 image this gives $(320 - 64)/8 + 1 = 33$ by $(240 - 128)/8 + 1 = 15$, or 495 windows at the first level, each with a HOG vector of 3780 numbers.

**Training.** The classifier is trained on cropped and aligned positives, and on negatives cut from images with no object. Because the scan will see millions of background windows, a few rounds of *hard negative mining* help: scan the negative images with the current classifier, add the false positives to the training set, and train again.

## Classic examples

- **Neural network face detectors.** Rowley, Baluja and Kanade (1998) ran a neural network on 20 by 20 pixel windows over an image pyramid and merged overlapping detections.
- **The Viola-Jones detector.** The [Viola-Jones detector](/viola-jones-detector/) differs from a plain sliding window in where it saves work. It does not resize the image; it scales the Haar-like features themselves, which the integral image computes in constant time at any size. And it is a cascade: each window passes through a chain of boosted stages, and most background windows are rejected by the first few stages, so the average cost per window is a small number of features, not the thousands of the full detector.
- **The Dalal-Triggs detector.** The [Dalal-Triggs detector](/dalal-triggs-detector/) computes HOG cells once per pyramid level, then scores each 64 by 128 window with one linear [support vector machine](/support-vector-machine/). Because the score is linear, the scan is a correlation of the weight vector with the HOG map.
- **The deformable part model.** The [deformable part model](/deformable-part-model/) scans a root filter and several part filters over a HOG pyramid and uses distance transforms to let the parts move; the scan is still over every position and scale.
- **OverFeat.** Sermanet and others (2014) applied a convolutional network to the whole image at several scales, which computes the scores of all windows of one level at once and shares the convolutions between them.

## Variations

- **Cascades.** Order the tests from cheap to expensive and stop as soon as one rejects, as in Viola-Jones.
- **Feature pyramids instead of image pyramids.** Compute features at a few scales and approximate the rest, or scale the classifier instead of the image.
- **Several aspect ratios.** Use one model per aspect ratio or viewpoint, as the mixtures of the deformable part model do.
- **Branch and bound.** Lampert, Blaschko and Hofmann (2008) find the best-scoring box among all boxes without scoring each one, by bounding the score of sets of boxes.
- **Region proposals.** Score only a few thousand [object proposals](/object-proposals/) from [selective search](/selective-search/) or a learned proposal network. This replaces the exhaustive scan with a cheap first stage, and is the design of [R-CNN](/r-cnn/) and [Faster R-CNN](/faster-r-cnn/).
- **Dense one-stage networks.** [YOLO](/yolo-detector/) and the [single shot multibox detector](/single-shot-multibox-detector/) score [anchor boxes](/anchor-boxes/) at every cell of a feature map; this is a sliding window over the feature map, with [bounding-box regression](/bounding-box-regression/) to correct the coarse grid.

## Pitfalls

- **Stride and scale step too coarse.** With a stride of $s$ pixels, the best window can be off by up to $s/2$ pixels in each direction, and a scale step of $\rho$ can be off by a factor of $\sqrt{\rho}$. For a small object this lowers the IoU with the true box below the threshold.
- **Too many false positives.** A false positive rate of $10^{-4}$ per window still gives about one false alarm per image when an image has $10^4$ windows. Detectors are therefore measured by misses against false positives per window or per image, and trained with hard negatives.
- **Duplicate detections.** Without non-maximum suppression, one object gives many overlapping hits, each counted as a false positive by the [mean average precision](/detection-mean-average-precision/) metric.
- **Boundary effects.** Objects cut by the image border, or larger than the image at every level, are never seen as a whole window. Padding the image helps a little.
- **Fixed aspect ratio.** One window shape fits upright people well but not people sitting or lying, nor cars seen from the front and from the side.
- **Context.** A window sees only its own pixels plus a small margin. Dalal and Triggs found that a margin of about 16 pixels around the person helped; much more context needs a different design.

## Exercises

1. An image of $640 \times 480$ pixels is scanned with a $64 \times 128$ window, a stride of 8 pixels and a scale step of $\rho = 1.2$. Count the windows on the first level, and bound the total over all levels.
2. Show that if a cascade has $T$ stages, stage $t$ costs $c_t$, and a background window passes stage $t$ with probability $p_t$, then the expected cost on a background window is $c_1 + p_1 c_2 + p_1 p_2 c_3 + \cdots$. With $c_t = 10t$ and $p_t = 0.5$, compare this with the cost of the last stage alone.
3. For a linear classifier $f(x) = w^\top \phi(x) + b$ on a grid of feature cells, write the scores of all windows of one level as a correlation, and give its cost with and without the fast Fourier transform.
4. A window at $(x, y)$ on pyramid level $k$ is mapped to the box $\rho^k (x, y, x + w, y + h)$. Find the largest IoU that can be lost by the position grid alone, for a square window of side $w$ and stride $s$.

## References
