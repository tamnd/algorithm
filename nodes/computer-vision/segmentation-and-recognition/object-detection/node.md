---
tag: YKE1TW
kind: problem
slug: object-detection
name: Object detection
aliases:
- object localization and classification
area: computer-vision/segmentation-and-recognition
level: core
summary: "Find every object of the known classes in an image and return for each a class, a bounding box and a confidence score."
prereqs: [object-recognition, intersection-over-union]
see_also: [sliding-window-detection, box-non-maximum-suppression, detection-mean-average-precision, faster-r-cnn, yolo-detector, detr, deformable-part-model, instance-segmentation]
sources:
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 6, Recognition: Section 6.3 (object detection, with face detection, pedestrian detection and general object detection)"
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "The detection task: a bounding box with a confidence for each object, a match when the overlap of the boxes exceeds 50 percent, duplicates counted as false positives, and average precision"
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar and C. Lawrence Zitnick, Microsoft COCO: common objects in context, ECCV 2014"
    locator: "The data set of 80 object categories with instance annotations; the detection metric averaged over IoU thresholds is given on the evaluation page of the data set"
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 1 and Section 7 (detection as scoring windows of a feature pyramid, bounding-box prediction and non-maximum suppression)"
---

Object detection is the problem of finding every object of a fixed set of classes in an image and saying, for each one, its class, a [bounding box](/axis-aligned-bounding-box/) around it, and a confidence score. It adds *where* to the *what* of [object recognition](/object-recognition/), and the number of objects is not known in advance: an image can hold no object of interest or a hundred. A detection is correct when its box overlaps a true box of the same class by enough [intersection over union](/intersection-over-union/), and a detector is judged by [detection mean average precision](/detection-mean-average-precision/) over a test set.

## In plain words

You give the computer a street photo and a list of things to look for, such as people, cars and bicycles. It must draw a tight rectangle around each one it finds, write the name of the thing on the rectangle, and say how sure it is.

This is harder than saying "there is a car in this photo". The computer must also count the cars, find small ones far away, and separate two people who stand close together. It must not draw two rectangles on one car. A rectangle that is a little off is still accepted, but only when it covers most of the true object. Methods look at many candidate rectangles, give each a score for each kind of thing, and then remove the doubles.

## Definition

Fix a set of classes $C = \{1, \ldots, K\}$. The input is a [digital image](/digital-image/) $I$. The output is a finite set of detections
$$\{(c_i, b_i, s_i) : i = 1, \ldots, m\}, \qquad c_i \in C, \quad s_i \in \mathbb{R},$$
where $b_i = (x_1, y_1, x_2, y_2)$ is an axis-aligned box in image coordinates and $m$ is chosen by the method.

The ground truth is a set of annotated boxes $(c, g)$ for the same image, drawn by people. A detection $(c_i, b_i, s_i)$ is a *true positive* when it is matched to a ground-truth box $g$ of class $c_i$ with $\mathrm{IoU}(b_i, g)$ above a threshold $\tau$, and each ground-truth box can be matched by at most one detection: the detections are matched in order of decreasing score, so a second detection of the same object is a *false positive*. PASCAL VOC uses $\tau = 0.5$; COCO averages over $\tau \in \{0.5, 0.55, \ldots, 0.95\}$. From the matches, the precision and recall at each score cut give the average precision of each class, and their mean over the classes is the score of the detector. There is no exact correct output, only a better or worse one under this metric.

## Variants

- **Single-class detection.** One class, such as faces or pedestrians. [Face detection](/face-detection/) with the [Viola-Jones detector](/viola-jones-detector/) and pedestrian detection with the [Dalal-Triggs detector](/dalal-triggs-detector/) are the classic cases.
- **Multi-class detection.** Many classes at once, as in PASCAL VOC (20 classes) and COCO (80 classes).
- **Instance segmentation.** A mask in place of a box for each object; see [instance segmentation](/instance-segmentation/).
- **Oriented boxes.** Rotated rectangles, common for aerial images and text.
- **3D detection.** Boxes in 3D space from depth or lidar data.
- **Open-vocabulary detection.** Classes given at test time by words, not fixed at training time.
- **Video detection.** Detection in each frame, with the help of the frames around it.

## Examples

- **Two pedestrians.** In a street photo, a detector returns (person, (40, 60, 90, 200), 0.97), (person, (120, 70, 165, 195), 0.91) and (person, (42, 58, 93, 205), 0.62). The third box covers the first person again; [non-maximum suppression](/box-non-maximum-suppression/) removes it, and if it stayed it would count as a false positive.
- **A missed small car.** A car of 15 by 10 pixels far down the road gives no detection; it lowers the recall.
- **A loose box.** A box that covers a whole dog but is twice its size has an IoU of about 0.5 with the true box; under VOC it may or may not count, and under COCO it fails at all thresholds above 0.5.
- **A non-example.** Saying only "this image contains a dog" is image classification, not detection; a box around the dog with no class is object proposal generation.

## Known algorithms

- **Sliding windows.** [Sliding-window detection](/sliding-window-detection/) scores a fixed-size window at every position and scale of an [image pyramid](/image-pyramid/), then applies non-maximum suppression. The [Viola-Jones detector](/viola-jones-detector/) (boosted Haar-like features on an [integral image](/integral-image/)), the [Dalal-Triggs detector](/dalal-triggs-detector/) ([HOG](/histogram-of-oriented-gradients/) and a linear [support vector machine](/support-vector-machine/)) and the [deformable part model](/deformable-part-model/) are of this kind.
- **Voting.** The [implicit shape model](/implicit-shape-model/) lets local features vote for object centres in a [generalized Hough](/generalized-hough-transform/) space.
- **Proposals and classification.** [Selective search](/selective-search/) and other [object proposal](/object-proposals/) methods give a few thousand candidate boxes; [R-CNN](/r-cnn/) classifies each with features of a convolutional network, [Fast R-CNN](/fast-r-cnn/) shares the network over the image with [RoI pooling](/roi-pooling/), and [Faster R-CNN](/faster-r-cnn/) learns the proposals too, from [anchor boxes](/anchor-boxes/).
- **One-stage detectors.** [YOLO](/yolo-detector/) and the [single shot multibox detector](/single-shot-multibox-detector/) predict classes and [box offsets](/bounding-box-regression/) directly on a dense grid; [focal loss](/focal-loss/) handles the many easy background positions. A [feature pyramid network](/feature-pyramid-network/) helps all of these with objects of different sizes.
- **Set prediction.** [DETR](/detr/) predicts a fixed-size set of boxes with a transformer and a one-to-one matching loss, and needs no non-maximum suppression.

## Bounds

There is no worst-case lower bound on the quality of a detector; methods are compared by average precision on a benchmark, and the numbers depend on the data set, the metric and the year. The search space has a simple size: an image of $W \times H$ pixels has $\Theta(W^2 H^2)$ axis-aligned boxes with integer corners, so no method scores them all. A sliding window with stride $s$ at aspect ratio fixed and scales spaced by a factor $\rho > 1$ visits about $\sum_k WH / (s^2 \rho^{2k}) = O(WH/s^2)$ windows, a geometric series dominated by the finest level; at each window the classifier costs the size of its feature vector. Greedy non-maximum suppression on $n$ boxes costs $O(n^2)$ IoU computations in the worst case.

## Reductions

- **To classification.** Each candidate box is classified as one of the $K$ classes or as background, so detection reduces to classification of windows or regions plus non-maximum suppression. This is the reduction of sliding-window and proposal-based detectors.
- **To keypoint or centre estimation.** Some detectors predict the centre of each object as a peak of a heat map, then its size; this reduces detection to finding the maxima of a map, as the implicit shape model does with votes.
- **From instance segmentation.** The bounding box of each mask of an instance segmentation is a detection, so a solution of that harder problem gives one of this problem.

## Applications

Pedestrian, car and traffic sign detection for driver assistance and autonomous driving; face detection in cameras and phones; counting people, animals or cells; video surveillance; robot grasping; retail shelf analysis; document layout analysis; and as the first step of tracking, pose estimation and face recognition.

## References
