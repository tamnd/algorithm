---
tag: 7BC4KB
kind: algorithm
slug: dalal-triggs-detector
name: Dalal-Triggs pedestrian detector
aliases:
- HOG-SVM detector
area: computer-vision/segmentation-and-recognition
level: core
summary: "Detect people by a linear SVM on HOG descriptors of sliding windows over an image pyramid, with hard negative mining during training."
solves: [object-detection]
model: real-ram
complexity:
  vars: {m: the number of pixels of the input image, d: the length of the HOG vector of one window (3780 by default), k: the number of windows that score above the threshold}
  time: {worst: O(m d + k^2), average: O(m d + k^2), best: O(m d)}
  space: {extra: O(m + d)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2005
  people: [Navneet Dalal, Bill Triggs]
  note: "Dalal and Triggs presented histograms of oriented gradients with a linear SVM at CVPR 2005, together with the INRIA person data set. The detector became the standard baseline for pedestrian detection and the root filter of the deformable part model."
prereqs: [histogram-of-oriented-gradients, support-vector-machine, sliding-window-detection, box-non-maximum-suppression]
see_also: [viola-jones-detector, deformable-part-model, image-pyramid, object-detection, detection-mean-average-precision, r-cnn, mean-shift, sift]
sources:
  - paper: doi:10.1109/CVPR.2005.177
    title: "Navneet Dalal and Bill Triggs, Histograms of oriented gradients for human detection, CVPR 2005, vol. 1, 886-893"
    locator: "Figure 1 (the chain), Section 4 (the INRIA data set and hard examples), Section 6 (the study of each step: gradients, orientation bins, blocks, normalization, window size, SVM), Section 7 (summary of the default detector)"
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 4.4 (data mining of hard examples, Theorem 1 and Theorem 2), and the Dalal-Triggs detector as the root filter"
  - paper: doi:10.1007/BF00994018
    title: "Corinna Cortes and Vladimir Vapnik, Support-vector networks, Machine Learning 20(3), 1995, 273-297"
    locator: "The soft-margin support vector machine"
  - paper: doi:10.1145/1390156.1390208
    title: "Cho-Jui Hsieh, Kai-Wei Chang, Chih-Jen Lin, S. Sathiya Keerthi and S. Sundararajan, A dual coordinate descent method for large-scale linear SVM, ICML 2008"
    locator: "The dual coordinate descent method for the hinge-loss linear SVM, used by the code of this page"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3.2, Pedestrian detection"
---

The Dalal-Triggs detector finds people in an image by scoring every window of a fixed size, at every position and scale, with a linear [support vector machine](/support-vector-machine/) on a [histogram of oriented gradients](/histogram-of-oriented-gradients/) (HOG) of the window. Windows that score above a threshold are reported as boxes, and [non-maximum suppression](/box-non-maximum-suppression/) merges the boxes around each person. Dalal and Triggs (2005) studied each step of this chain on a new data set of people in varied poses and backgrounds, and the default settings they found became a standard for [sliding-window detection](/sliding-window-detection/) until convolutional networks replaced it.

## In plain words

A person in a photo has a typical outline: a round head, two shoulders, a vertical body and legs. The detector does not look at colours or exact brightness. It cuts the window into small squares and, for each square, counts in which directions the edges run. A person gives many vertical edges on both sides of the body and curved edges at the head and shoulders, in about the same squares every time.

These counts go into a simple scoring rule learned from thousands of pictures with and without people. The detector slides the window over the image, and over smaller copies of the image to find larger people, and reports the places where the score is high. Training adds a second pass: it looks for the background windows that the first rule wrongly scored high, adds them to the training set, and learns the rule again.

## The problem

The input is an image and a trained model: a window of $w \times h$ pixels (64 by 128 for people), the HOG parameters, a weight vector $w$ and a bias $b$. The output is a list of boxes with scores, one box for each person that the detector finds. Training takes a set of positive windows, each with one centred person, and a set of images with no people. This is an instance of [object detection](/object-detection/) for one class.

## The algorithm

```pseudo id=main
DETECT(I, w, b, τ)
L1  for each level of the image pyramid of I, with scale σ do
L2      compute the gradient of every pixel with the masks [-1, 0, 1] and its transpose
L3      vote each magnitude into 9 orientation bins over 0 to 180 degrees of its cells, bilinear in angle and position
L4      normalize every block of 2 × 2 cells with L2-Hys
L5      for each window position p on the cell grid do
L6          f ← w · φ(p) + b                      ▷ φ = the blocks of the window, in order
L7          if f > τ then add the box of p, scaled by σ, with the score f
L8  K ← GREEDY-NMS of the added boxes
L9  return K

TRAIN(P, N, r)                                  ▷ P: person windows, N: images without people
L10 X ← HOG of every window in P and of its mirror image, label +1
L11 add HOG of random windows of N, label -1
L12 (w, b) ← linear SVM on X
L13 repeat r times                              ▷ Dalal and Triggs use one round
L14     H ← every window of every level of N with w · φ + b > -1
L15     add H to X with label -1, (w, b) ← linear SVM on X
L16 return (w, b)
```

The default chain of the paper is as follows. Pixels are RGB with no gamma correction; for each pixel the gradient of the colour channel with the largest magnitude is used. Gradients use the centred masks $[-1, 0, 1]$ with no smoothing. The orientation is unsigned and goes into 9 bins over 0 to 180 degrees. Cells have $8 \times 8$ pixels and blocks have $2 \times 2$ cells, with a stride of 8 pixels, so each cell is in four blocks. Each block is weighted with a Gaussian window of $\sigma = 8$ pixels and normalized with L2-Hys: an L2 normalization $v / \sqrt{\|v\|^2 + \varepsilon^2}$, a clip of every entry at 0.2, and a second L2 normalization. The window has $64 \times 128$ pixels, and the classifier is a linear soft-margin SVM (SVMLight with $C = 0.01$).

Line L14 uses the margin $-1$: a background window is "hard" when the SVM does not push it past the margin. Dalal and Triggs search the negative images exhaustively for false positives and train once more on the enlarged set.

## Example

**The size of the vector.** A window of $64 \times 128$ pixels has $8 \times 16$ cells, so $7 \times 15 = 105$ blocks. Each block has $4 \times 9 = 36$ entries, and $\phi$ has $105 \cdot 36 = 3780$ entries. At scale 1, a $320 \times 240$ image has $(40 - 8 + 1) \times (30 - 16 + 1) = 33 \times 15 = 495$ window positions on the cell grid; the smaller levels of the pyramid add more.

**One vote.** A pixel at column 10 and row 5, with cells of 8 pixels and the gradient $(g_x, g_y) = (3, 4)$, has the magnitude 5 and the angle $53.13$ degrees. The bin centres are at $10, 30, 50, \ldots, 170$ degrees, so the angle is $3.13/20 = 0.1565$ of the way from the centre of bin 2 (50 degrees) to the centre of bin 3 (70 degrees). The pixel centre is at $(10.5, 5.5)$, and the cell centres are at $4, 12, 20, \ldots$ in each axis, so the pixel is $0.8125$ of the way from cell column 0 to cell column 1 and $0.1875$ of the way from cell row 0 to cell row 1. The pixel adds $5 \cdot 0.8125 \cdot 0.8125 = 3.3008$ to the cell in row 0 and column 1, split as $2.7842$ to bin 2 and $0.5166$ to bin 3, and smaller amounts to the three other cells. The eight weights sum to 1.

**One block.** If a block before normalization were $(3, 1, 0, \ldots, 0)$, L2 normalization gives $(0.949, 0.316, 0, \ldots)$, the clip gives $(0.2, 0.2, 0, \ldots)$, and the second normalization gives $(0.707, 0.707, 0, \ldots)$. The clip stops one strong edge from taking over the whole block.

## Correctness

A detector has no correctness theorem: its error rate is measured on a test set. The correctness file proves what the program computes. The vector has $(w_c - 1)(h_c - 1) \cdot 4B$ entries, 3780 for the default window. Each pixel inside the grid gives its full magnitude to the histograms, with the tent weights of trilinear interpolation. The HOG vector does not change when the image brightness is changed by $aI + k$ with $a > 0$, up to the effect of $\varepsilon$. The scan of lines L5 to L7 scores every window position of every level. For mining, the argument of Felzenszwalb et al. (2010) shows that when no negative outside the training cache violates the margin, the SVM on the cache is the SVM on all negatives, so repeated mining reaches the SVM of the whole negative set; one round, as in the paper, does not guarantee this.

## Complexity

For an image of $m$ pixels, lines L2 and L3 do a constant amount of work per pixel, $O(m)$, and line L4 is smaller. There are $O(m / c^2)$ window positions per level, and each dot product costs $O(d)$, so the scores cost $O(m d / c^2)$ in the [real RAM](/real-ram/), with $c^2 = 64$ for the default cells. A pyramid with scale step $s$ has at most $s^2/(s^2 - 1)$ times as many pixels as the image, a constant factor. Line L8 costs $O(k^2)$ in the worst case for $k$ boxes above the threshold. The dot products dominate: for each window the cost is the 3780 multiplications of the default vector. The vector of a window is never stored on its own; the block grid of each level takes $O(m)$ space. Dalal and Triggs report that their implementation needs less than a second for a $320 \times 240$ image with about 4000 windows (2005 hardware). Training costs one SVM solve on the initial set, a scan of all negative images, and a second solve.

## Properties

- **Deterministic.** The detector is a fixed function of the image and the model.
- **Linear in the features.** The score is a dot product, so the detector can be written as a filter: each block of $w$ is a template that is correlated with the block grid. The [deformable part model](/deformable-part-model/) uses this view.
- **Invariant to contrast** up to $\varepsilon$, by the block normalization.
- **Not invariant to rotation or aspect ratio.** The window is upright with a fixed shape. People who lie down, or who are partly hidden, score low.
- **Dense and overlapping.** Each cell is in four blocks with different normalizations, and the paper finds that this overlap improves the results.
- **Each step was chosen by experiment.** The paper reports the effect of each change on the miss rate at $10^{-4}$ false positives per window (FPPW), on the INRIA test set. These choices are benchmark results, not theorems.

## Variants and improvements

- **Mean-shift fusion.** Dalal's thesis (2006) fuses detections by finding modes in position and scale with [mean shift](/mean-shift/) instead of the greedy suppression of line L8.
- **Faster features.** Computing the cell grid once per level, as the code of this page does, and integral histograms make the scan much faster than computing each window alone.
- **Cascades.** A cascade of HOG classifiers on blocks of different sizes, in the style of the [Viola-Jones detector](/viola-jones-detector/), rejects most windows after a few blocks.
- **Parts.** The [deformable part model](/deformable-part-model/) of Felzenszwalb et al. adds parts at twice the resolution on springs, mixtures of models for different views, a latent SVM, and a 31-dimensional variant of HOG.
- **Learned features.** [R-CNN](/r-cnn/) and later detectors replace HOG and the linear SVM with convolutional features and a network head.

## When to use it

Use it for a rigid, mostly upright object class with a typical outline, such as pedestrians, and when a small, fast, explainable detector is enough, for example on hardware without a GPU or as a baseline. It needs only a few thousand labelled windows. For many classes, large changes of pose, or strong occlusion, use a part-based model or a convolutional detector.

## Pitfalls

- **Smoothing the image.** The paper finds that Gaussian smoothing before the gradient makes the results worse; the plain $[-1, 0, 1]$ mask is the best of the masks it tests.
- **Too few bins or signed orientation.** Fewer than about 9 bins loses shape information, and for people the sign of the gradient carries little information, because clothes and background can be lighter or darker.
- **Skipping hard negatives.** The paper reports a gain of 5 percent in miss rate at $10^{-4}$ FPPW from one round of retraining on hard examples. Without it, the classifier sees too few of the background patterns that look like people.
- **Window margin.** The positive windows keep a band of background around the person. The paper finds that a smaller margin makes the detector worse, because the outline of the body against the background is the signal.
- **Comparing curves.** DET curves per window and precision-recall curves per image measure different things; [detection mean average precision](/detection-mean-average-precision/) depends on NMS and on the matching rule, a per-window curve does not.
- **Scale range.** The smallest person that can be found is the window size; people smaller than 64 by 128 pixels need an upsampled level of the pyramid.

## Implementations

The Python code implements the chain on gray images: centred gradients with repeated borders, trilinear voting into 9 unsigned bins, $2 \times 2$-cell blocks with L2-Hys, a cell grid per pyramid level with bilinear downsampling, a linear SVM trained by dual coordinate descent with the bias as an extra feature, hard-negative mining, and greedy NMS. It leaves out the colour channel choice and the Gaussian block window. The tests check the 3780 entries of the default vector, the bins of ramps at 0, 45 and 90 degrees, the voting against a direct sum of tent functions, L2-Hys, the invariance to brightness and contrast, the duality gap of the SVM, the equality of mined training with training on all negatives, the shift of the score map by whole cells, and the detection of a synthetic object at two scales.

## History

Before 2005, detectors of people and faces used Haar wavelets, as in the work of Papageorgiou and Poggio and the [Viola-Jones detector](/viola-jones-detector/), or edge templates. Dalal and Triggs (2005) introduced dense histograms of oriented gradients, inspired by the orientation histograms of [SIFT](/sift/) and of earlier work on shape contexts, and showed on the new INRIA person data set that they reduce false positives by more than an order of magnitude compared with the Haar wavelet detector they tested. The INRIA set has 1239 positive training images, used with their mirror images as 2478 windows, and 12180 negative windows taken from 1218 images without people. Felzenszwalb, Girshick, McAllester and Ramanan (2010) state that the Dalal-Triggs detector won the 2006 PASCAL object detection challenge, and they built the deformable part model on it. HOG with a linear SVM remained a standard baseline until convolutional detectors such as R-CNN (2014) took over.

## References
