---
tag: 20SPE1
kind: technique
slug: forward-backward-error
name: Forward-backward error
aliases:
- forward-backward consistency check
area: computer-vision/visual-tracking
level: advanced
summary: Track a point forward through frames, track it back, and reject it when it does not return near its start, a check for tracking failure.
prereqs: [kanade-lucas-tomasi-tracker]
see_also: [tracking-learning-detection, left-right-consistency-check, optical-flow, lucas-kanade-method, median, feature-track, stereo-matching, visual-object-tracking]
sources:
  - paper: doi:10.1109/ICPR.2010.675
    title: Zdenek Kalal, Krystian Mikolajczyk and Jiri Matas, Forward-backward error, automatic detection of tracking failures, International Conference on Pattern Recognition (ICPR), 2010, 2756 to 2759
    locator: the whole paper (the definition of the error for a trajectory, its use to filter point tracks, and the median flow tracker)
  - paper: doi:10.1109/TPAMI.2011.239
    title: Zdenek Kalal, Krystian Mikolajczyk and Jiri Matas, Tracking-learning-detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(7), 2012, 1409 to 1422
    locator: the section on the short-term tracker (median flow with failure detection)
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the parts on cross-checking of the left and right disparity maps to find occlusions
---

The forward-backward error is a test that a point tracker applies to its own output. Track a point from frame $F_0$ to frame $F_k$, then track the end point back from $F_k$ to $F_0$ with the same tracker. If the tracker was right and the point stayed visible, the backward track returns to the start. The distance between the start and the return point is the forward-backward error, and a large value marks a probable failure. The test needs no ground truth and no model of the scene, and it works with any tracker that can run in both directions. Its cost is one more tracking run. Kalal, Mikolajczyk and Matas gave it this name in 2010 and used it in the median flow tracker of [tracking-learning-detection](/tracking-learning-detection/). The same idea appears as the [left-right consistency check](/left-right-consistency-check/) in stereo and as the forward-backward check of [optical flow](/optical-flow/). The test is a heuristic. A small error does not prove that a track is correct.

## In plain words

You follow a spot on a moving object for a few pictures and end somewhere. To check yourself, you start from where you ended and follow the spot back through the same pictures. If you come back to where you started, your first trip was probably fine. If you come back far from the start, something went wrong on the way, for example the spot was covered or you jumped to a similar spot. You keep the good tracks and drop the bad ones. The check can still be fooled, because a mistake that you make the same way in both directions brings you back home.

## When it applies

- A tracker $T$ maps a point in one frame to a point in another frame, and it can run with the frames in the reverse order. The [Lucas-Kanade method](/lucas-kanade-method/), the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/), dense optical flow, [stereo matching](/stereo-matching/) and template search all qualify.
- The motion of a visible point is invertible: the point that goes from $x$ in $F_0$ to $y$ in $F_k$ goes from $y$ back to $x$. Points that are hidden in one of the frames break this, which is what the test detects.
- The failures to detect are not symmetric in time. Occlusion, a jump to a similar structure and divergence of an iterative solver usually give a different answer in the backward run.
- One more tracking run per point is affordable. The cost of the test is the cost of the tracker again.

## The template

Notation: $T_{a \to b}(x)$ is the position in frame $F_b$ that the tracker gives for the point $x$ of frame $F_a$. A track over $k$ frames is chained from single steps, $y = T_{k-1 \to k}(\cdots T_{0 \to 1}(x))$. The threshold is $\varepsilon$ in pixels.

```pseudo id=main
FB-FILTER(F_0, ..., F_k, points x_1, ..., x_n, ε)
L1  for i ← 1 to n do
L2      y_i ← x_i;  for t ← 0 to k - 1 do y_i ← T_{t→t+1}(y_i)          ▷ forward track
L3      z_i ← y_i;  for t ← k down to 1 do z_i ← T_{t→t-1}(z_i)          ▷ backward track from the end
L4      e_i ← ‖z_i - x_i‖                                                ▷ forward-backward error
L5  if ε is not given then ε ← the median of e_1, ..., e_n               ▷ keep the better half
L6  return the pairs (x_i, y_i) with e_i ≤ ε
```

Line L4 is the definition of Kalal and colleagues: the Euclidean distance between the start of the forward trajectory and the end of the backward trajectory. Line L5 is the rule of median flow, which keeps the half of the points with the smallest error and needs no threshold. A fixed $\varepsilon$, such as half a pixel for a subpixel tracker, is the other common choice.

**What is true.** If the tracker returns the true motion and the point is visible in all frames, then $z_i = x_i$ and $e_i = 0$. This is a theorem, and it follows from the invertibility of the motion. The converse is false: $e_i = 0$ does not imply that $y_i$ is right (see the pitfalls). So a large error is evidence of failure, and a small error is weak evidence of success.

**Cost.** The test doubles the number of tracker calls, $2 n k$ in all, and the median on line L5 costs $O(n)$ with [selection](/median/). Memory is $O(n)$ for the errors.

## Classic examples

**Filtering KLT tracks under an occluder.** The [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/) page tracks seven points on a texture that moves by $(1, 0.5)$, while a $17 \times 17$ block is replaced by another texture. With $\varepsilon = 0.5$:

| Point | Forward error (pixels) | Forward-backward error | Decision |
|---|---|---|---|
| $(37, 27)$, under the occluder | 12.1 | 2.54 | dropped |
| $(22, 24)$, near the occluder | 18 | 18.5 | dropped |
| $(28, 23)$, at the edge of the occluder | 0.395 | 0.11 | kept |
| four points far from the occluder | below 0.02 | small | kept |

The first two failures are found. The third point is a miss: its error of 0.395 pixel is small enough to be harmless here, but the test passed it for the wrong reason, because the backward run was pulled in the same way as the forward run.

**Median flow.** Place a $10 \times 10$ grid of points in the box of the target, track them one frame forward with pyramidal Lucas-Kanade and back, and keep the half with the smallest forward-backward error. In the full TLD system the points are also ranked by the [normalized cross-correlation](/normalized-cross-correlation/) of their windows, and only the points in the better half of both rankings are kept. The box moves by the median of the remaining displacements, and its size changes by the median of the ratios of the pairwise distances. When the target is covered, most errors become large and the median error itself signals the failure. [Tracking-learning-detection](/tracking-learning-detection/) uses this as its short-term tracker.

**The left-right check in stereo.** Here the "tracker" is the disparity map, which takes a left pixel $u$ to the right pixel $u - d_L(u)$, and the backward map takes a right pixel $x$ to $x + d_R(x)$. A pixel passes when $|d_L(u) - d_R(u - d_L(u))| \le \tau$, which is the forward-backward error along the row. Take one row with a background of disparity 1 and a closer object of disparity 3 at the left pixels 4 and 5:

| Left pixel $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $d_L(u)$ | 1 | 1 | 1 | 1 | 3 | 3 | 1 | 1 |
| $u - d_L(u)$ | out | 0 | 1 | 2 | 1 | 2 | 5 | 6 |

In the right image the object covers the pixels 1 and 2, so $d_R = (1, 3, 3, 1, 1, 1, 1, 1)$. The left pixels 2 and 3 map to right pixels with $d_R = 3 \ne 1$ and fail. They are exactly the background points next to the object that the right camera cannot see. All other pixels inside the image pass. The [left-right consistency check](/left-right-consistency-check/) page treats this case in full.

**Occlusion in dense optical flow.** With the forward flow $w_f$ and the backward flow $w_b$, a pixel $x$ is consistent when $w_f(x) + w_b(x + w_f(x)) \approx 0$. Sundaram, Brox and Keutzer (2010) stop their dense point trajectories where this sum is large compared with the flow magnitudes, and many later flow methods use the same test to mark occluded pixels.

## Variations

- **One step or many.** The check can run over one frame pair or over the whole trajectory of $k$ frames. A long trajectory finds slow drift that one step misses, but one failure in the middle makes the whole trajectory fail.
- **Fixed threshold or rank.** A fixed $\varepsilon$ in pixels gives an absolute meaning. The median rule of line L5 adapts to the image and always keeps half of the points, which is useful when the points only vote, as in median flow.
- **Combined with appearance.** The error does not see the content of the window. Adding the [normalized cross-correlation](/normalized-cross-correlation/) or the residual of the window catches tracks that are consistent but have moved to other content.
- **Relative threshold.** For flow, the test $|w_f + w_b|^2 \le \alpha (|w_f|^2 + |w_b|^2) + \beta$ allows a larger error for a larger motion.
- **As a training signal.** Methods that learn optical flow or features without labels add the forward-backward error as a loss, and leave out the pixels that it marks as occluded.

## Pitfalls

- **A consistent error passes.** A tracker that always returns its input has $e_i = 0$ for every point, and its forward error is the full motion. A bias that acts the same way in both directions, such as the pull of an occluder on a window that it partly covers, can also give a small error, as for the point $(28, 23)$ above.
- **The aperture problem.** On a straight edge only the motion across the edge is measurable. A tracker that moves the point across the edge only returns along the same line, so its error is near 0 while the error along the edge can be large. Use the test only on corners, or together with the smaller eigenvalue of the gradient matrix.
- **Different start points.** The backward run of an iterative tracker starts at the end point $y_i$, and its result depends on its start. A test that reruns the solver from a different start measures the solver as well as the track.
- **Image borders.** A point that leaves the frame cannot return, and some trackers clamp it to the border. Treat points that reach the border as failed instead of computing an error.
- **Double cost.** The test doubles the tracker time. For dense flow it means a second full flow field, which can be the largest cost of the system.
- **Threshold in pixels.** A fixed threshold means different things at different image resolutions and pyramid levels. Scale it with the image or use a rank rule.

## Exercises

1. Prove that if $T$ returns the true positions and the point is visible in $F_0, \ldots, F_k$, then $e_i = 0$. Which property of the motion does the proof use?
2. A tracker returns its input point in every frame. A texture moves by $(2, 1)$ per frame for 3 frames. Give the forward error and the forward-backward error of every point, and explain why the test does not find this failure.
3. In the stereo example, add a third surface of disparity 2 at the left pixels 6 and 7. Compute $d_R$ and find the pixels that fail the check.
4. A point lies on a horizontal edge, and the edge moves by $(3, 1)$. The tracker measures only the vertical motion. Compute its forward error and its forward-backward error.
5. Show that the median of $n$ displacements, taken in each coordinate, equals the true motion when more than half of the points are tracked exactly, whatever the other displacements are. Why does median flow still filter the points before it takes the median?

## References
