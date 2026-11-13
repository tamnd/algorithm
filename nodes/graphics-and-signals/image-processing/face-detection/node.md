---
tag: 7ZYHGD
kind: problem
slug: face-detection
name: Face detection
area: graphics-and-signals/image-processing
level: advanced
summary: Find every human face in an image and return a box around each one, judged by how many true faces the boxes cover and how many boxes cover no face.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, m: smallest face size in pixels}
  time: {worst: Ω(W H / m^2)}
prereqs: [digital-image]
see_also: [viola-jones-detector, haar-features, template-matching, non-maximum-suppression, sliding-window, principal-component-analysis, support-vector-machine, color-spaces]
sources:
  - paper: doi:10.1109/34.982883
    title: Ming-Hsuan Yang, David J. Kriegman and Narendra Ahuja, Detecting faces in images, a survey, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(1), 34-58, 2002
    locator: the whole survey (knowledge-based, feature invariant, template matching and appearance-based methods, and the evaluation of detectors)
  - paper: doi:10.1023/B:VISI.0000013087.49260.fb
    title: Paul Viola and Michael J. Jones, Robust real-time face detection, International Journal of Computer Vision 57(2), 137-154, 2004
    locator: Section 5.7 (results on the MIT+CMU frontal test set of 130 images with 507 faces, and the comparison with earlier detectors)
  - paper: doi:10.1109/34.655647
    title: Henry A. Rowley, Shumeet Baluja and Takeo Kanade, Neural network-based face detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(1), 23-38, 1998
    locator: the whole paper (a neural network on small windows at all positions and scales, and the merging of overlapping detections)
  - paper: doi:10.1109/34.655648
    title: Kah-Kay Sung and Tomaso Poggio, Example-based learning for view-based human face detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(1), 39-51, 1998
    locator: the whole paper (a model of the face class from clusters of examples, and the collection of hard negative examples)
  - paper: doi:10.1109/CVPR.2000.855895
    title: Henry Schneiderman and Takeo Kanade, A statistical method for 3D object detection applied to faces and cars, IEEE Conference on Computer Vision and Pattern Recognition, vol. 1, 746-751, 2000
    locator: the whole paper (histograms of wavelet coefficients for frontal and profile faces)
  - paper: doi:10.1162/jocn.1991.3.1.71
    title: Matthew Turk and Alex Pentland, Eigenfaces for recognition, Journal of Cognitive Neuroscience 3(1), 71-86, 1991
    locator: the whole paper (the distance from face space as a test for a face)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 6, Recognition, Section 6.3 Object detection (face detection)
---

Face detection is the problem of finding all human faces in an image and returning a box around each one. It does not ask whose face it is; that is face recognition, which starts from the boxes. The problem is defined by examples, not by a formula: a face is what a labeled set of test images calls a face, usually with a stated range of poses and a smallest size. A detector is judged by two numbers, the fraction of the true faces that its boxes find and the number of boxes that find no face, and by how these trade against each other as a threshold changes. Most methods classify windows at every position and scale as face or not face and then merge the overlapping positive windows into one box per face. The [Viola-Jones detector](/viola-jones-detector/) made this fast enough for video in 2001. All methods are heuristic: none comes with a guarantee for an image outside its test data.

## In plain words

You want a camera to find the faces in a picture, so that it can focus on them, or so that a program can count the people. The program must draw a box around each face, big or small, and draw no box where there is no face. That is harder than it sounds. Faces differ in shape, skin tone, age and expression. They are lit from many sides, turned, partly covered by hair, hands or glasses, and may be tiny in a crowd. And most of a picture is not a face, so even a rare mistake per place adds up to many false boxes. Most methods look at every small square of the picture, at many sizes, and ask a trained test whether it holds a face. Boxes on the same face are then joined into one.

## Definition

The input is a [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows. Most detectors use one gray channel with values 0 to 255, used as they are stored with no gamma step; some also use the color channels, for example to find skin. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. Windows that leave the image are not tested, so no border rule is needed. The output is a list of boxes $B_1, \ldots, B_k$, each an axis-aligned rectangle, often with a score. Some benchmarks use ellipses or a set of landmark points instead.

Detection is judged against a labeled list $G_1, \ldots, G_n$ of true face boxes. A common rule is the *overlap ratio*

$$\mathrm{IoU}(B, G) = \frac{|B \cap G|}{|B \cup G|},$$

where $|\cdot|$ is the area. A box $B_i$ is a *hit* for $G_j$ if $\mathrm{IoU}(B_i, G_j) \ge \frac{1}{2}$, and each true face can be matched by at most one box; this is a one-to-one matching between boxes and faces. The *detection rate* is the number of matched faces divided by $n$, and every unmatched box is a *false positive*. A detector with a score threshold $\tau$ gives one pair of these numbers for each $\tau$, and the curve of all pairs, a ROC curve or a precision-recall curve, describes the detector. The threshold $\frac{1}{2}$ and the matching rule are conventions of each benchmark, and results from different benchmarks cannot be compared directly.

## Variants

- **Frontal and upright faces.** The face looks at the camera and is turned by at most a small angle in the image plane. This is the case of the early benchmarks, such as the MIT+CMU frontal test set of 130 images with 507 faces.
- **Turns in the plane.** The face may be at any angle in the image. A detector either tests several angles or first estimates the angle of each window.
- **Several views.** Profile and half-profile faces are also wanted. Separate detectors are trained for each range of views, or one model covers them all.
- **Face localization.** The image is known to hold exactly one face, as in a photo for an identity card, and only its box is wanted.
- **Landmarks.** The output is also the position of the eyes, the nose and the mouth, which is the first step of face alignment.
- **Video.** Faces are detected in every frame, and the detections are linked over time, so that a detector can use the previous frame to search less.
- **Faces in the wild.** Images from the web with crowds, small faces, strong blur and heavy occlusion, as in the newer benchmarks.

## Examples

**Scoring three boxes.** Let one true face be $G = [10, 30) \times [10, 30)$, a square of area $400$, and let a detector return three boxes:

| Box | Intersection with $G$ | Union | IoU |
|---|---|---|---|
| $B_1 = [15, 35) \times [12, 32)$ | $15 \times 18 = 270$ | $530$ | $0.509$ |
| $B_2 = [20, 40) \times [20, 40)$ | $10 \times 10 = 100$ | $700$ | $0.143$ |
| $B_3 = [12, 28) \times [8, 28)$ | $16 \times 18 = 288$ | $400 + 320 - 288 = 432$ | $0.667$ |

The box $B_3$ has an area of $16 \times 20 = 320$ and lies inside $G$ except for its two top rows. Both $B_1$ and $B_3$ pass the rule, but only one box can match the face. The best one, $B_3$, matches, and $B_1$ and $B_2$ count as false positives. The detection rate is $1$ with $2$ false positives. Detectors remove such duplicates before scoring. If $B_3$ has the highest score, non-maximum suppression with an overlap limit of $0.3$ removes $B_1$, whose IoU with $B_3$ is $208/512 \approx 0.41$, and keeps $B_2$, whose IoU with $B_3$ is $64/656 \approx 0.10$. Then only $B_2$ is a false positive.

**Why false positives dominate.** A $100 \times 100$ image searched for faces of at least $20 \times 20$ pixels, with sizes $20, 25, 31, 39, 48, 61, 76, 95$ (a factor of about $1.25$) and a step of one pixel, has $(101 - s)^2$ windows at size $s$, which is $26{,}151$ windows in all. If the image holds two faces, almost all of these windows are not faces. A window classifier that wrongly accepts a non-face window with probability $10^{-4}$ still gives about $2.6$ false windows per image on average. So a face detector needs a false positive rate per window far below what is usual for other classification tasks, and most methods spend their effort on rejecting non-faces.

## Known algorithms

| Method | Idea | Notes |
|---|---|---|
| Rules and skin color | regions of skin color in a suitable [color space](/color-spaces/), then tests on shape and on dark regions for the eyes | fast; fails under colored light and on skin-colored background |
| [Template matching](/template-matching/) | correlation with a fixed or deformable face template | works only for one pose and size |
| Eigenfaces (Turk and Pentland, 1991) | the distance of a window from a low-dimensional face space found by [principal component analysis](/principal-component-analysis/) | an early appearance-based test |
| Sung and Poggio (1998) | distances to clusters of face and non-face examples, then a learned classifier | introduced the collection of hard negatives |
| Rowley, Baluja and Kanade (1998) | a neural network on $20 \times 20$ windows at all positions and scales | merging and arbitration of overlapping detections |
| Schneiderman and Kanade (2000) | products of histograms of wavelet coefficients | frontal and profile faces |
| [Viola-Jones detector](/viola-jones-detector/) (2001) | a cascade of boosted [Haar-like features](/haar-features/) on an integral image | reported at 15 frames per second on $384 \times 288$ images on a desktop computer of 2001 |
| Learned deep detectors | convolutional neural networks trained on large labeled sets | the usual choice in new systems |

All the window-based methods test $\Theta(WH)$ windows per scale with a step of one pixel, and their cost is that number times the mean cost of the classifier per window. For a cascade the mean cost depends on the images and is observed, not bounded.

## Bounds

- **Reading enough of the image.** Suppose that a face of size $m \times m$ can be put anywhere in the image without changing the rest. Then a correct detector must read at least one pixel of every one of the $\lfloor W/m \rfloor \lfloor H/m \rfloor$ disjoint $m \times m$ blocks, because an unread block could hold a face or not. So $\Omega(WH/m^2)$ time is needed in the worst case.
- **The number of windows.** With windows of sizes $s_k = s_0 c^k$ for a factor $c > 1$ and a step of one pixel, the number of windows is $\sum_k (W - s_k + 1)(H - s_k + 1)$, which is $O(WH \log_c(\min(W, H)/s_0))$. With a step that grows in proportion to $s_k$, it is $O(WH)$, as on the page of the [Viola-Jones detector](/viola-jones-detector/).
- **No exact answer.** The class of faces is given by examples, so no detector is correct on every image. The best possible error of any classifier on a distribution of windows is the Bayes error, and for small, blurred or turned faces it is not zero even for people.

## Reductions

- **To classification of windows.** Detection reduces to a binary classifier on windows of a fixed size, applied at every position and scale, as a [sliding window](/sliding-window/) over the image and over the scales. Any classifier can be used, such as [boosting](/boosting/), a [support vector machine](/support-vector-machine/) or [logistic regression](/logistic-regression/).
- **Merging to grouping.** The overlapping positive windows on one face are joined by [non-maximum suppression](/non-maximum-suppression/) or by grouping the connected parts of the overlap relation with a [disjoint-set](/disjoint-set/) structure.
- **Scoring to bipartite matching.** Matching boxes to true faces one to one is a [bipartite matching](/bipartite-matching/) problem. Benchmarks usually solve it greedily in the order of the scores.
- **One known face to template matching.** When one fixed face is sought, as when a face is tracked from frame to frame, the problem reduces to [template matching](/template-matching/).

## Applications

- Focus, exposure and framing in cameras and in video calls.
- The first step of face recognition, face alignment and the analysis of expressions.
- Counting and following people, for example in shops or in traffic.
- Blurring faces to protect privacy in street views and in published video.
- Organizing and searching photo collections by the people in them.

## References
