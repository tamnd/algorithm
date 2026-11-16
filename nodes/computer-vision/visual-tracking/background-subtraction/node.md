---
tag: 5YTBNW
kind: problem
slug: background-subtraction
name: Background subtraction
aliases:
- foreground detection
- change detection in video
area: computer-vision/visual-tracking
level: core
summary: Mark the pixels of each video frame that differ from a model of the static background as moving foreground.
prereqs: [digital-image, pixel]
see_also: [stauffer-grimson-background-model, vibe-background-subtraction, median-filter, kernel-density-estimation, robust-pca, image-segmentation, optical-flow, tracking-by-detection]
sources:
  - paper: doi:10.1109/ICCV.1999.791228
    title: "Kentaro Toyama, John Krumm, Barry Brumitt and Brian Meyers, Wallflower: principles and practice of background maintenance, Proceedings of the IEEE International Conference on Computer Vision, 1999, 255-261"
    locator: "the whole paper (the canonical problems of background maintenance and the comparison of methods on them)"
  - paper: doi:10.1109/ICSMC.2004.1400815
    title: "Massimo Piccardi, Background subtraction techniques: a review, IEEE International Conference on Systems, Man and Cybernetics, 2004"
    locator: "the whole paper (running average, temporal median, mixture of Gaussians, kernel density and other models, with their speed and memory)"
  - paper: doi:10.1016/j.cosrev.2014.04.001
    title: "Thierry Bouwmans, Traditional and recent approaches in background modeling for foreground detection: an overview, Computer Science Review 11, 2014, 31-66"
    locator: "the whole paper (the steps of background subtraction and a classification of the models)"
  - paper: doi:10.1109/CVPR.1999.784637
    title: "Chris Stauffer and W. Eric L. Grimson, Adaptive background mixture models for real-time tracking, CVPR 1999, vol. 2, 246-252"
    locator: "the whole paper (the mixture of Gaussians per pixel)"
  - paper: doi:10.1109/TIP.2010.2101613
    title: "Olivier Barnich and Marc Van Droogenbroeck, ViBe: a universal background subtraction algorithm for video sequences, IEEE Transactions on Image Processing 20(6), 2011, 1709-1724"
    locator: "Section 3 (the sample based model and its random update)"
  - paper: doi:10.1109/34.598236
    title: "Christopher R. Wren, Ali Azarbayejani, Trevor Darrell and Alex P. Pentland, Pfinder: real-time tracking of the human body, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(7), 1997, 780-785"
    locator: "the whole paper (a single Gaussian per pixel for the scene)"
---

Background subtraction is the problem of finding, in each frame of a video from a fixed camera, the pixels that show something other than the usual scene. The method keeps a model of the background, compares each new frame with it, and marks the pixels that do not fit as foreground. The model must also follow slow changes of the scene, such as the light of the day, without taking in the moving objects. This page states the problem and compares the methods. The [Stauffer-Grimson model](/stauffer-grimson-background-model/) fits a mixture of Gaussians to the values of each pixel and updates it with a learning rate. [ViBe](/vibe-background-subtraction/) keeps a set of raw sample values per pixel and replaces them at random, with no density at all.

## In plain words

A camera that does not move sees almost the same picture again and again. If we know what the empty scene looks like, we can find people and cars by looking for the places where the new picture is different. The hard part is to know what the empty scene looks like when the light changes, leaves move in the wind, and people walk through the picture all the time. A good method learns the empty scene from the video itself and keeps learning, but does not learn the people as part of the scene.

## Definition

The input is a sequence of frames $I_1, I_2, \ldots$, each a map $I_t \colon \Omega \to V$ from a pixel grid $\Omega$ with $P$ pixels to values $V$, gray values or color vectors. The camera is fixed, so a pixel $x$ shows the same point of the scene in every frame. The output is a sequence of masks $F_t \colon \Omega \to \{0, 1\}$, with $F_t(x) = 1$ when $x$ is foreground in frame $t$.

Most methods have the same three parts:

- a background model $B_t(x)$ for each pixel, such as a value, a distribution, or a set of samples;
- a decision $F_t(x) = 1$ when $I_t(x)$ does not fit $B_{t-1}(x)$, for example when a distance is above a threshold $\tau$;
- an update $B_t = U(B_{t-1}, I_t, F_t)$, which often takes in only the pixels that were background, a *conservative* update.

What is foreground is defined by a ground truth mask that a person draws, usually the moving objects and not their shadows. A method is scored on labeled frames by [precision and recall](/precision-and-recall/) of the foreground pixels, or by their harmonic mean, the F-measure. The problem is online when $F_t$ may only use $I_1, \ldots, I_t$.

## Variants

- **With a training period.** The first frames show the empty scene. Without it, the method must learn the background while objects move (the bootstrap case).
- **Gray or color.** Color helps to find objects with the same brightness as the scene, and to find shadows, which change the brightness more than the color.
- **With shadow removal.** Shadows of the objects are background in most ground truth, but they differ from the model.
- **Dynamic background.** Water, leaves and screens change all the time. A model with one value per pixel fails there; a model with several modes, such as a mixture or a sample set, works better.
- **Moving camera.** The frames must first be aligned, for example with [optical flow](/optical-flow/) or a global motion model. The rest of this page assumes a fixed camera.
- **Offline.** With the whole video known, the background can be the low rank part of the matrix of all frames, as in [robust PCA](/robust-pca/).

## Examples

**One frame.** A row of 5 pixels has the background values $B = (50, 52, 51, 49, 50)$, and the new frame is $I = (51, 90, 95, 50, 20)$. With the threshold $\tau = 15$, the differences $|I - B| = (1, 38, 44, 1, 30)$ give the mask $(0, 1, 1, 0, 1)$. The last pixel is darker than the scene, and a shadow could give the same result, so a later step must decide whether it is an object.

**Mean and median.** One pixel shows $50, 51, 200, 49, 52$ in 5 frames; the value 200 is a car that passed. The mean is $80.4$, so a model built from the mean is far from the empty scene. The median is $51$, so a model built from the [median](/median-filter/) over time is not disturbed by one passing object. This is why the median is a common simple model.

**Running average.** The model $B_t = (1 - \alpha) B_{t-1} + \alpha I_t$ with $\alpha = 0.1$ starts at 50. A car parks on the pixel and shows 150 from then on. After $t$ frames with the car the model is $150 - 100 \cdot 0.9^t$: about 97 after 6 frames and about 102 after 7. With $\tau = 50$ and the decision against the model of the frame before, the car is foreground in its first 7 frames and background from frame 8 on, since $150 - 102 = 48 < 50$. A smaller $\alpha$ keeps it foreground longer.

**A stopped object.** A car drives in and stops, and a painting is hung on a wall. Both give the same sequence of pixel values: a change, and then a new constant value. The ground truth calls the car an object and the painting a new background. No method that sees only the pixel values can be right on both; see the bounds below.

## Known algorithms

| Method | Model per pixel | Update | Cost per frame |
|---|---|---|---|
| Frame differencing | the last frame | replace | $O(P)$ |
| Running average | one value | exponential average | $O(P)$ |
| Single Gaussian (Pfinder) | a mean and a variance | exponential average | $O(P)$ |
| Temporal median | the last $L$ values | window | $O(P L)$ |
| [Stauffer-Grimson](/stauffer-grimson-background-model/) | $K$ Gaussians with weights | online, by match | $O(P K \log K)$ |
| [Kernel density](/kernel-density-estimation/) | the last $N$ values | window | $O(P N)$ |
| [ViBe](/vibe-background-subtraction/) | $N$ samples | random, conservative, to neighbors | $O(P N)$ |
| [Robust PCA](/robust-pca/) | a low rank matrix of all frames | offline | iterative |

The first rows are simple and fast but fail on dynamic backgrounds. The mixture and the sample models handle several modes. Piccardi compares the speed and the memory of these models, and Bouwmans gives a survey with many later methods, among them learned ones. After any of them, [morphological opening](/morphological-opening/) and [connected component labeling](/connected-component-labeling/) clean the mask and cut it into objects.

## Bounds

- **Theorem: a lower bound per frame.** Any method that is right on all inputs must read every pixel of every frame, so it needs $\Omega(P)$ time per frame. Proof: if a method does not read pixel $x$ in frame $t$, its output $F_t(x)$ is the same for two inputs that differ only there, one with $I_t(x)$ equal to the empty scene and one with an object at $x$. The correct answers differ, so one output is wrong. The online methods of the table meet this bound when the model size per pixel is fixed.
- **Theorem: pixel values alone cannot separate a stopped object from a changed background.** The two cases of the example above give the same input and different ground truth, so any method that is a function of the input fails on one of them. In practice this is handled by a rule, such as the learning rate or the time until absorption, which is a choice and not a solution.
- **Heuristic: the speed against the stability.** A model that adapts fast follows the light but absorbs slow objects; one that adapts slowly keeps the objects but makes errors after a change of light. Toyama et al. list such cases as the canonical problems of background maintenance.

## Reductions

- **To pixel classification.** Each frame is a [segmentation](/image-segmentation/) into two classes, with the background model giving the class scores.
- **To low rank plus sparse.** Stack the frames as the columns of a matrix $M$. A static background makes a low rank matrix $L$, and small moving objects a sparse matrix $S$, with $M = L + S$; this is the problem of [robust PCA](/robust-pca/).
- **From object detection.** A detector of a known class finds objects also when they stand still or the camera moves; background subtraction finds objects of any class but only when they move. [Tracking by detection](/tracking-by-detection/) can use either.

## Applications

- Video surveillance with fixed cameras: the masks start the tracking of people and cars.
- Traffic counting and parking control.
- Motion capture and human computer interaction with a fixed camera, as in Pfinder.
- Smart video coding, where the moving parts get more bits.
- Saving computation: a detector runs only where something moves.

## References
