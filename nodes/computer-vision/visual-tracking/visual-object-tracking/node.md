---
tag: 19P0YM
kind: problem
slug: visual-object-tracking
name: Visual object tracking
aliases:
- single object tracking
- model-free tracking
area: computer-vision/visual-tracking
level: core
summary: Given the box of a target in the first frame of a video, find its box in every later frame.
model: real-ram
complexity:
  vars: {N: the number of frames, P: the number of pixels of one frame}
  time: {worst: Θ(N P)}
prereqs: [optical-flow, digital-image, intersection-over-union]
see_also: [multi-object-tracking, tracking-by-detection, object-detection, kalman-filter, particle-filter, template-matching, background-subtraction, clear-mot-metrics]
sources:
  - paper: doi:10.1145/1177352.1177355
    title: Alper Yilmaz, Omar Javed and Mubarak Shah, Object tracking, a survey, ACM Computing Surveys 38(4), article 13, 2006
    locator: the whole paper (the representations of objects, point, kernel and silhouette tracking)
  - paper: doi:10.1109/TPAMI.2013.230
    title: Arnold W. M. Smeulders, Dung M. Chu, Rita Cucchiara, Simone Calderara, Afshin Dehghan and Mubarak Shah, Visual tracking, an experimental survey, IEEE Transactions on Pattern Analysis and Machine Intelligence 36(7), 2014, 1442 to 1468
    locator: the whole paper (nineteen trackers compared on 315 video fragments, survival curves)
  - paper: doi:10.1109/TPAMI.2014.2388226
    title: Yi Wu, Jongwoo Lim and Ming-Hsuan Yang, Object tracking benchmark, IEEE Transactions on Pattern Analysis and Machine Intelligence 37(9), 2015, 1834 to 1848
    locator: the whole paper (the annotated sequences, the success plot from the overlap and the precision plot from the center error)
  - paper: doi:10.1109/TPAMI.2016.2516982
    title: Matej Kristan, Jiri Matas, Aleš Leonardis, Tomáš Vojíř, Roman Pflugfelder, Gustavo Fernández, Georg Nebehay, Fatih Porikli and Luka Čehovin, A novel performance evaluation methodology for single-target trackers, IEEE Transactions on Pattern Analysis and Machine Intelligence 38(11), 2016, 2137 to 2155
    locator: the whole paper (accuracy and robustness, restarts after a failure)
---

Visual object tracking is the problem of following one target through a video when the only information about the target is a box around it in the first frame. The tracker must output a box in each later frame, using the frames up to that one, and some versions also ask it to say when the target is not visible. Nothing is known in advance about the class of the target, so the tracker must build a model of its appearance from that one box and keep the model useful while the target turns, deforms, changes its light or is hidden. The problem is the basis of video surveillance, camera control, robots that follow people and many measurements in science. Because two parts of a scene can look the same, no method is correct on every video. Trackers are compared on benchmarks of annotated videos by the overlap between their boxes and the true boxes.

## In plain words

Someone draws a rectangle around a thing in the first picture of a video and says: follow this. In each next picture you must draw the rectangle where the thing is now. You do not know what the thing is, only what it looked like in that first rectangle. It can move, turn, get bigger or smaller, go into shadow or go behind something else. You may only look at the pictures up to the present one, as a live camera would. A good tracker stays on the thing, does not jump to something that looks similar, and admits when the thing has gone.

## Definition

The input is a sequence of frames $F_0, F_1, \ldots, F_N$, each a [digital image](/digital-image/) of $P$ pixels, and a box $b_0 = (x_1, y_1, x_2, y_2)$ around the target in $F_0$. Pixel $(u, v)$ has its center at the point $(u, v)$. The output is a box $b_t$ for each $t = 1, \ldots, N$. In the long-term version $b_t$ may also be "absent". A tracker is *causal* if $b_t$ depends only on $F_0, \ldots, F_t$ and $b_0$.

**Quality.** Let $g_t$ be the true box. The overlap of two boxes is the [intersection over union](/intersection-over-union/)

$$
\mathrm{IoU}(b, g) = \frac{|b \cap g|}{|b \cup g|},
$$

and the center error is the distance between the centers of $b_t$ and $g_t$. Common scores built on them are these.

- **Success rate.** The fraction of frames with $\mathrm{IoU}(b_t, g_t) > \theta$. The success plot shows it for $\theta$ from 0 to 1, and the area under the plot summarizes it.
- **Precision.** The fraction of frames with a center error below a threshold in pixels.
- **Accuracy and robustness.** In the evaluation of the VOT challenges, the tracker is restarted after each failure. Accuracy is the mean overlap on the tracked frames, and robustness counts the failures.

A tracker is judged on many videos, because one video can favor any method.

## Variants

- **Short-term tracking.** The target is visible in almost every frame, and the tracker always outputs a box.
- **Long-term tracking.** The target can leave the view or be hidden for a long time. The tracker must report absence and find the target again, as [tracking-learning-detection](/tracking-learning-detection/) does.
- **Point tracking.** The target is a point, or a set of points, and the output is its position, as in the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/).
- **Contour and mask tracking.** The output is an outline or a mask instead of a box, as in the [CONDENSATION algorithm](/condensation-algorithm/) or with [active contours](/active-contours/).
- **Rotated boxes and scale.** Some benchmarks use rotated boxes, and some trackers keep a fixed size.
- **Many targets.** Following all objects of known classes, with identities, is [multi-object tracking](/multi-object-tracking/), a different problem with its own [metrics](/clear-mot-metrics/).
- **Other sensors.** Depth images, thermal images or event cameras add or replace the color frames.

## Examples

**Overlap by hand.** For $b = (0, 0, 2, 2)$ and $g = (1, 1, 3, 3)$ the intersection is the unit square, so $\mathrm{IoU} = 1 / (4 + 4 - 1) = 1/7$. For $g = (1, 0, 3, 2)$ the intersection has area 2, so $\mathrm{IoU} = 2 / (4 + 4 - 2) = 1/3$. A box shifted by half its width has an overlap of only $1/3$, so the usual threshold $\theta = 0.5$ is strict.

**A success score.** A tracker on a video of 5 frames has overlaps $0.8, 0.7, 0.4, 0.0, 0.6$. At $\theta = 0.5$ the success rate is $3/5$. The success plot is the fraction of overlaps above each $\theta$. The area under it equals the mean overlap, $2.5 / 5 = 0.5$, because the area under the curve $\theta \mapsto \frac1N \#\{t : o_t > \theta\}$ is $\frac1N \sum_t o_t$.

**An ambiguous video.** Two identical balls roll toward each other, touch in frame 10 and move apart. The target is the left ball. The frames are the same whether the balls bounced back or passed each other, so the true box after frame 10 is on different balls in the two cases, and every tracker is wrong on one of them. Motion models help when the physics is known, but they cannot remove this kind of ambiguity.

## Known algorithms

| Algorithm | Model of the target | Cost per frame |
|---|---|---|
| [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/) | small windows around corners, translation | $\Theta(k m)$ per point |
| [Mean-shift tracking](/mean-shift-tracking/) and [CAMShift](/camshift/) | color histogram in a kernel | $\Theta(k A)$ for $k$ steps on $A$ pixels |
| [MOSSE filter](/mosse-filter/) and [kernelized correlation filter](/kernelized-correlation-filter/) | [correlation filter](/correlation-filter-tracking/) learned online | $\Theta(A \log A)$ |
| [Tracking-learning-detection](/tracking-learning-detection/) | flow tracker, detector and online learning | linear in the number of windows scanned |
| [Siamese tracking](/siamese-tracking/) | embedding learned offline, fixed exemplar | one network pass and one correlation |
| [CONDENSATION algorithm](/condensation-algorithm/) | contour with dynamics, sample set | $\Theta(N_s (\log N_s + M L))$ for $N_s$ samples |
| [Inverse compositional alignment](/inverse-compositional-alignment/) | template with a warp | $\Theta(n A)$ per iteration for $n$ warp parameters |

Here $A$ is the number of pixels of the target region, $m$ of a window and $k$ the number of iterations. [Tracking by detection](/tracking-by-detection/) runs a detector in each frame and links its outputs. A [Kalman filter](/kalman-filter/) or a [particle filter](/particle-filter/) can be put on top of any of these to smooth the boxes.

## Bounds

- **Reading the frames.** A tracker that must find the target anywhere in the frame, for example after the target was hidden, must read every pixel in the worst case: a pixel it does not read could hold the target. So $\Omega(P)$ time per frame and $\Theta(N P)$ in all is needed, and a detector that scans the frame in linear time meets it. Local trackers read only a window around the last position and are faster, but they lose a target that jumps out of the window.
- **No tracker is always right.** If two videos have the same frames but different true boxes, as in the ambiguous example, a tracker gives the same output on both and is wrong on at least one. So any guarantee needs assumptions on the scene, such as a unique appearance or a known motion.
- **Drift.** A tracker that updates its model from its own output can add a small error at each frame. With an error of $\varepsilon$ pixels per frame in a random direction, the position error after $N$ frames grows like $\varepsilon \sqrt N$, and with a constant bias like $\varepsilon N$. Methods that keep the first appearance, or check their output against it, limit this.

## Reductions

- **To template matching.** With a fixed appearance and translation only, tracking in one frame is [template matching](/template-matching/) in a search window, for example by [normalized cross-correlation](/normalized-cross-correlation/).
- **To image registration.** With a parametric warp of the target, it is [image registration](/image-registration/) of the target region, solved by the [Lucas-Kanade method](/lucas-kanade-method/) or [inverse compositional alignment](/inverse-compositional-alignment/).
- **To filtering.** With a motion model and a likelihood of the image given the state, it is a [Bayes filter](/bayes-filter/), solved by a Kalman filter in the linear Gaussian case and by a particle filter otherwise.
- **To detection.** With a detector for the class of the target, each frame becomes [object detection](/object-detection/), and tracking is the association of detections over time.
- **To optical flow.** Tracking a point is following the [optical flow](/optical-flow/) from frame to frame.

## Applications

- Surveillance and traffic cameras that follow people or vehicles.
- Pan-tilt cameras and drones that keep a subject in view.
- Tracking of a face or a hand for interfaces, and of tools in medical video.
- Measurement of the motion of cells, animals or particles in science.
- Annotation of video, where a person draws the first box and a tracker fills the rest.
- Visual servoing of robots and the following of a target by a vehicle.

## References
