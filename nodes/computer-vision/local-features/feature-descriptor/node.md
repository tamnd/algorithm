---
tag: XNBPSX
kind: concept
slug: feature-descriptor
name: Feature descriptor
aliases:
- local descriptor
- keypoint descriptor
area: computer-vision/local-features
level: intro
summary: A vector computed from the patch around a feature so that patches of the same scene point have close vectors and patches of different points have distant ones.
prereqs: [feature-detection, digital-image]
see_also: [sift, histogram-of-oriented-gradients, brief-descriptor, orb-features, surf, feature-matching, invariant-local-features, lowe-ratio-test]
sources:
  - paper: doi:10.1109/TPAMI.2005.188
    title: Krystian Mikolajczyk and Cordelia Schmid, A performance evaluation of local descriptors, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(10), 1615-1630, 2005
    locator: the whole paper (the descriptors compared, the recall and 1-precision criterion, the GLOH descriptor)
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 6 (the local image descriptor) and Section 7.1 (matching by the nearest neighbor and the distance ratio)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Section 7.1.2 (feature descriptors) and Section 7.1.3 (feature matching)
---

A feature descriptor is a vector computed from the image around a feature, such as a corner or a blob found by a [feature detector](/feature-detection/). The aim is that two views of the same scene point give close vectors, and that views of different points give distant vectors. Then [feature matching](/feature-matching/) reduces to a search for near vectors. A descriptor has three parts: a region of support with a position, a scale and often an orientation, a measurement in that region, and a distance. The measurement is often a set of histograms of gradients, as in [SIFT](/sift/) and [HOG](/histogram-of-oriented-gradients/), or a string of intensity comparisons, as in [BRIEF](/brief-descriptor/) and [ORB](/orb-features/).

## In plain words

A detector tells you where the interesting spots of an image are. A descriptor tells you what each spot looks like, as a list of numbers. If you photograph the same building twice, from a slightly different place and in different light, the corner of a window should get almost the same list of numbers in both photos. A corner of a different window should get a clearly different list. To find which spot in one photo is which spot in the other, you compare the lists and pair each spot with the one whose list is most alike. A good descriptor ignores what changes between photos, such as the brightness, the size and the turn of the spot, and keeps what makes the spot special.

## The idea

A descriptor is a function $D$ from an image and a feature frame to a vector space with a distance. The frame of a feature at the pixel $(u, v)$, with $u$ the column and $v$ the row, gives the position, a scale $s$ and an angle $\theta$. The descriptor reads the image only in a region around the position, in coordinates scaled by $s$ and turned by $\theta$. So a change of the image by a translation, a scale and a rotation that the detector follows changes the frame but not the pixels that the descriptor reads, up to resampling. This is the main way to get geometric invariance. The descriptor itself adds invariance to light, usually by normalization:

- Gradients do not change when a constant is added to the image.
- Dividing a vector by its norm removes a gain on the image.
- Comparisons between pixels do not change under any increasing change of the intensities of the pixels compared.

Three groups of descriptors are common.

- **Histograms of gradients.** The region is divided into cells, and each cell holds a histogram of gradient directions weighted by the gradient magnitude. SIFT has $4 \times 4$ cells with 8 directions, 128 values. [SURF](/surf/) sums Haar responses on $4 \times 4$ cells, 64 values. [HOG](/histogram-of-oriented-gradients/) describes whole windows for detection. [DAISY](/daisy-descriptor/) samples smoothed gradient maps on circles so that it can be computed at every pixel. The distance is Euclidean, or a distance between histograms.
- **Binary strings.** [BRIEF](/brief-descriptor/), [ORB](/orb-features/) and [BRISK](/brisk-features/) compare the intensities of fixed pairs of points and keep one bit per pair. The distance is the [Hamming distance](/hamming-distance/), which is fast to compute.
- **Histograms of local codes or of points.** [Local binary patterns](/local-binary-patterns/) count codes over a region and describe texture. The [shape context](/shape-context/) counts the points of a shape in log-polar bins around a point.

Learned descriptors, such as the one of [SuperPoint](/superpoint/), are computed by a network trained so that matching patches have close vectors.

The size of the region, the number of cells and bins and the normalization are design choices, made by experiments on data. They are not results of a theory. Two properties are always in tension. Invariance makes matching vectors close under the changes between views, and distinctiveness keeps the vectors of different points apart. A descriptor that ignores everything is invariant and useless.

## Examples

**Euclidean distance after normalization.** Take three raw 4-value descriptors $a = (3, 4, 0, 0)$, $b = (6, 9, 1, 0)$ and $c = (0, 4, 3, 0)$. Divide each by its Euclidean norm. Then $\hat a = (0.6, 0.8, 0, 0)$, $\hat b \approx (0.5523, 0.8285, 0.0921, 0)$ and $\hat c = (0, 0.8, 0.6, 0)$. The distances are $\lVert \hat a - \hat b \rVert \approx 0.1075$ and $\lVert \hat a - \hat c \rVert \approx 0.8485$. So $a$ matches $b$. The raw vector $b$ is close to $2a$, a copy of $a$ under a gain of 2 with a little noise, and the normalization removes the gain. The [Lowe ratio test](/lowe-ratio-test/) compares the nearest and the second nearest distance: $0.1075 / 0.8485 \approx 0.127$, far below the usual threshold of 0.8, so the match is kept.

**Hamming distance.** Two binary descriptors 10101110 and 10111110 differ in one bit, so their Hamming distance is 1. A descriptor and an unrelated string of 256 random bits differ in about 128 bits on average. On a computer, one exclusive or and one population count per 64-bit word give the distance.

**Invariance by the frame.** If an image is turned by 30 degrees about a keypoint and the detector reports an angle that is 30 degrees larger, a descriptor that samples in the turned frame reads the same scene points as before, up to interpolation. [BRIEF](/brief-descriptor/) has no frame angle, so its tests read different pixels after the turn, and its bits change.

## Where it is used

- **Matching between images**, for [image stitching](/image-stitching/), [structure from motion](/structure-from-motion-problem/), [visual odometry](/visual-odometry/) and [image registration](/image-registration/). See [feature matching](/feature-matching/).
- **Recognition and retrieval**, by quantizing descriptors into visual words in the [bag of visual words](/bag-of-visual-words/), [VLAD](/vlad/) and the [Fisher vector](/fisher-vector/), for [image retrieval](/image-retrieval/).
- **Detection**, where a dense descriptor such as HOG feeds a classifier, as in the [Dalal-Triggs detector](/dalal-triggs-detector/).
- **Texture and faces**, with LBP histograms.
- **Evaluation.** Mikolajczyk and Schmid compared descriptors on images with known homographies, using recall against 1 - precision as the criterion. Their results are benchmark results on their data of 2005.

## References
