---
tag: CCWPAB
kind: algorithm
slug: tracking-learning-detection
name: Tracking-learning-detection
aliases:
- TLD
- Predator tracker
area: computer-vision/visual-tracking
level: advanced
summary: Run a median flow tracker and a detector side by side, and let each correct the other through positive and negative expert constraints that train the detector online.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {N: the number of frames, W: the number of scanning windows, D: the number of pixel comparisons in all ferns, M: the number of patches in the object model, Q: the number of pixels in a normalized patch, G: the number of tracked points times the pixels in the window of each point, P: the number of pixels in a frame, C: the number of counters in the fern tables}
  time: {worst: Θ(N (P + W (D + M Q) + G)), average: Θ(N (P + W (D + M Q) + G)), best: Θ(N (P + W + G))}
  space: {extra: Θ(P + W + M Q + C)}
properties: {deterministic: false, exact: false, local: false, iterative: false, online: true}
history:
  year: 2012
  people: [Zdenek Kalal, Krystian Mikolajczyk, Jiri Matas]
  note: Kalal, Mikolajczyk and Matas split long-term tracking into a tracker, a detector and a learning step, and trained the detector online from structural constraints on the trajectory.
prereqs: [lucas-kanade-method, forward-backward-error, integral-image]
see_also: [visual-object-tracking, kanade-lucas-tomasi-tracker, random-forest, k-nearest-neighbors, normalized-cross-correlation, intersection-over-union, tracking-by-detection, kernelized-correlation-filter]
sources:
  - paper: doi:10.1109/TPAMI.2011.239
    title: Zdenek Kalal, Krystian Mikolajczyk and Jiri Matas, Tracking-learning-detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(7), 2012, 1409 to 1422
    locator: Section 4.2 (stability of P-N learning, page 1413), Section 4.3 (simulated experts), Sections 5.1 to 5.6 (object model, detector cascade, median flow with failure detection, integrator, P-expert and N-expert, pages 1415 to 1418)
  - paper: doi:10.1109/ICPR.2010.675
    title: Zdenek Kalal, Krystian Mikolajczyk and Jiri Matas, Forward-backward error, automatic detection of tracking failures, International Conference on Pattern Recognition (ICPR), 2010, 2756 to 2759
    locator: the whole paper (the forward-backward error and the median flow tracker)
---

Tracking-learning-detection (TLD) is a method for long-term tracking of one object that is given by a box in the first frame. It runs two components on every frame. A short-term tracker, median flow, moves the box from the previous frame by the median motion of reliable points. A detector scans the whole frame with a cascade of three classifiers and finds every place that looks like the object. An integrator picks one answer, and a learning step uses the answer to correct the detector: windows on a reliable trajectory become positive examples, and windows far from it become negative examples. The tracker can follow new appearances that the detector does not know yet, and the detector can find the object again after the tracker has lost it. Kalal, Mikolajczyk and Matas published the method in 2012.

## In plain words

One helper follows the object from frame to frame. It is accurate but forgets nothing and fixes nothing, so after the object is hidden it is lost for good. A second helper looks at every place in the picture and asks whether the object is there. It can find the object anywhere, but at the start it knows only one picture of it. So we let the two teach each other. While the follower is sure, the places it visits teach the searcher what the object looks like, and every other place in the picture teaches the searcher what the object is not. When the follower gives up, the searcher, which has learned a lot by then, tells the follower where to start again.

## The problem

The input is a video and a box $B_0 = (x_1, y_1, x_2, y_2)$ around the object in frame 0. In each later frame the output is a box, or the answer that the object is not visible. The object can change its appearance, leave the view, be hidden for many frames and come back at another place. Two boxes are compared by their overlap, the [intersection over union](/intersection-over-union/). Pixel $(u, v)$ has its center at the point $(u, v)$.

**Object model.** A patch is the content of a box resampled to a fixed size and normalized to zero mean and unit norm; the paper uses $15 \times 15$ pixels. The similarity of two patches is $S(a, b) = \frac12 (\mathrm{NCC}(a, b) + 1)$, where NCC is the [normalized cross-correlation](/normalized-cross-correlation/). The model is a list of positive patches, in the order they were added, and a list of negative patches. For a patch $p$, let $S^+$ and $S^-$ be its largest similarity to a positive and to a negative patch, and $S^+_{50\%}$ its largest similarity to the older half of the positives. The **relative similarity** is $S^r = S^+ / (S^+ + S^-)$ and the **conservative similarity** is $S^c = S^+_{50\%} / (S^+_{50\%} + S^-)$.

## The algorithm

```pseudo id=main
MEDIAN-FLOW(F_prev, F, B)
L1   place a grid of points in B
L2   track each point from F_prev to F with Lucas-Kanade, and back again
L3   e_i ← the forward-backward error of point i;  c_i ← the NCC of the windows around it
L4   keep the points with e_i ≤ median(e) and c_i ≥ median(c); fail if none or median(e) > e_max
L5   d ← the median displacement of the kept points
L6   fail if the median distance of all displacements from d is above 10 pixels
L7   s ← the median ratio of point distances after and before;  return B moved by d and scaled by s

DETECT(F)
L8   reject each scanning window whose gray value variance is below half that of B₀
L9   reject each remaining window whose mean fern posterior is not above 1/2
L10  return the remaining windows with S^r > θ_NN

TLD-FRAME(F_prev, F)
L11  T ← MEDIAN-FLOW(F_prev, F, B) if B exists
L12  group the windows of DETECT(F) into clusters of overlap above 1/2, one box per cluster
L13  B ← the candidate (T or a cluster box) with the largest S^c, or NONE if there is no candidate
L14  reliable ← (B = T and reliable) or S^c(B) > θ_core
L15  if reliable then LEARN(F, B)

LEARN(F, B)
L16  for the 10 windows closest to B: train the ferns on warped copies labeled positive
L17  add the patch of B to the positives if S^r - θ_NN < λ
L18  for each window with overlap below 0.2 that passes the variance test and the ferns: train the ferns on it labeled negative
L19      add its patch to the negatives if S^r > θ_NN - λ
```

If line L13 gives NONE, the object is reported as not visible and the trajectory is not reliable. The detector of lines L8 to L10 is a cascade: each stage is more expensive than the one before and sees only the windows the earlier stages let through. The scanning windows are all positions and scales of the first box; the paper uses scales in steps of 1.2, shifts of 10 percent of the width and of the height, and a smallest box of 20 pixels, which gives about 50,000 windows on a $320 \times 240$ image. Line L8 computes each variance in constant time from two [integral images](/integral-image/), one of the values and one of their squares.

**Ferns.** Each fern compares a fixed random set of $d$ pixel pairs inside the window, which gives a $d$-bit code. It stores, for each code, the number $p$ of positive and $n$ of negative training windows with that code, and its posterior is $p / (p + n)$. Line L9 averages the posteriors of all ferns. The paper blurs the image with a Gaussian of standard deviation 3 before the comparisons and uses 13 comparisons per fern. A fern is trained on an example only if the ensemble classifies it wrongly, except in the first frame.

**Learning.** The P-expert (positive) assumes that the object moves along a trajectory, so windows close to a reliable box are positive. The N-expert (negative) assumes that the object is at one place only, so windows far from it are negative. In the first frame the paper takes the 10 windows closest to $B_0$ and makes 20 warped copies of each (shift by up to 1 percent, scale by up to 1 percent, rotation by up to 10 degrees, Gaussian noise of standard deviation 5), 200 positives in all. In later frames it makes 10 copies of each, with rotation up to 5 degrees. The nearest neighbor model gets a new patch only if its label is wrong or its margin $S^r - \theta_{\text{NN}}$ is smaller than $\lambda = 0.1$, so the model stays small. The paper uses $\theta_{\text{NN}} = 0.6$ and reports similar results from 0.5 to 0.7.

**Integrator and reliability.** The integrator outputs the most confident candidate by $S^c$, or nothing if neither the tracker nor the detector gives a box. A trajectory becomes reliable when $S^c$ of the box is above a threshold, which the paper calls entering the core of the model, and stays reliable until the detector reinitializes it or the tracker fails. Only reliable boxes train the detector.

**The code on this page** follows these rules with smaller numbers for small test images: a $10 \times 10$ grid of points, 10 ferns of 10 comparisons on unblurred pixels, warps by shift, scale and noise only (no rotation), $\theta_{\text{NN}} = \theta_{\text{core}} = 0.55$, and an extra failure test of line L4, a median forward-backward error above 5 pixels. These values are this page's choices.

## Example

**Similarities by hand.** Let a patch have $S^+ = 0.9$, $S^- = 0.6$ and $S^+_{50\%} = 0.8$. Then $S^r = 0.9 / 1.5 = 0.6$ and $S^c = 0.8 / 1.4 \approx 0.571$. A patch identical to a positive has $S^+ = 1$, but if one negative has $S^- = 0.636$, its relative similarity is only $1 / 1.636 \approx 0.611$. In small images with few textures this happens, and it is why the code uses thresholds of 0.55.

**Median flow by hand.** Five kept points move by $(1, 0)$, $(1.1, 0)$, $(0.9, 0.1)$, $(1, -0.1)$ and $(8, 6)$; the last one is on an occluder. The medians of the coordinates are $1$ and $0$, so the box moves by $(1, 0)$ and the bad point has no effect. Its distance from the median motion is about 9.2 pixels, but the median of the five distances is 0.1, so line L6 does not report a failure.

**A full run.** The frames are $40 \times 40$. The background is smooth, with two textured distractors, a checkerboard and vertical stripes. The object is a $10 \times 10$ square of random gray values from $\{30, 90, 160, 230\}$, first at $(6, 4)$, moving by $(2, 1)$ per frame. There are 2,891 scanning windows at the three scales $1/1.2$, 1 and 1.2; 708 of them pass the variance test in frame 0 (the object variance is 5,252). The first learning step adds 200 warped positives to the ferns, trains them on 527 negative windows, and puts 35 negative patches into the model.

| frame | object at | output box | IoU with truth | $S^c$ | reliable |
| --- | --- | --- | --- | --- | --- |
| 1 | $(8, 5)$ | $(8.00, 5.00, 18.00, 15.00)$ | 0.999 | 0.618 | yes |
| 4 | $(14, 8)$ | $(14.01, 8.01, 23.99, 17.99)$ | 0.995 | 0.618 | yes |
| 5 | hidden | none | | | no |
| 6 | hidden | none | | | no |
| 7 | $(26, 22)$ | $(25.75, 21.75, 36.25, 32.25)$ | 0.907 | 0.617 | yes |
| 8 | $(25, 24)$ | $(24.75, 23.75, 35.25, 34.25)$ | 0.907 | 0.617 | yes |

In frames 5 and 6 a flat gray square covers the object. Median flow fails because the median forward-backward error is far above 5 pixels, and the detector finds no window, so the output is "not visible". In frame 7 the object is back at another place. The tracker has nothing to follow, but the detector returns 4 windows in one cluster, and their mean box starts the trajectory again. In frame 8 median flow continues from it.

## Correctness

TLD as a whole is a heuristic: nothing proves that its box covers the object. The full proof of the parts that can be proved is in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: exact variance in constant time.** Four reads from each integral image give the sum and the sum of squares of any box.
- **Theorem: median flow.** It is exact for a translation, the scale estimate is exact for a similarity, and if more than half of the kept displacements lie in an interval, the median does too.
- **Theorem: similarity ranges.** $S$, $S^r$ and $S^c$ are in $[0, 1]$, $S^r$ grows with $S^+$ and falls with $S^-$, and $S^c \le S^r$.
- **Theorem: stability of P-N learning (under the paper's model).** With constant precision and recall of the two experts, the false positives and false negatives follow $x(k + 1) = M x(k)$, and they go to 0 if and only if both eigenvalues of $M$ are below 1 in absolute value. If all four qualities equal $1 - \varepsilon$, this holds exactly when $\varepsilon < 1/2$.
- **Heuristic.** The failure tests, the integrator, the reliability rule and all thresholds.

## Complexity

Building the two integral images costs $\Theta(P)$ per frame. The variance test costs $O(1)$ per window, so $\Theta(W)$ in all. A window that reaches the ferns costs $\Theta(D)$ for the comparisons, and a window that reaches the nearest neighbor stage costs $\Theta(M Q)$ for the similarities to all model patches. Median flow costs $\Theta(G)$ for the Lucas-Kanade steps (with a fixed number of iterations), plus the medians and the distance ratios of line L7 over all pairs of kept points; for $K$ points these cost $O(K^2)$, which is below $G$ when $K$ is at most the number of pixels in the window of a point, as for a $10 \times 10$ grid with $7 \times 7$ windows. Learning visits every window once more, at the same cost per window. So a frame costs $\Theta(P + W (D + M Q) + G)$ in the worst case and $\Theta(P + W + G)$ in the best case, when the variance test rejects every window. In practice the cascade leaves only tens of windows for the last stage, which is the reason for the cascade, but there is no bound on that. The space is $\Theta(P)$ for the integral images, $\Theta(W)$ for the window list, $\Theta(M Q)$ for the model patches, and $\Theta(C)$ for the fern tables, which hold two counters for each of the $2^d$ codes of each fern.

## Properties

- **Long-term.** It can find the object again after a full occlusion or after it left the view, which a pure tracker cannot.
- **Online and from one example.** It starts from one box and learns all the rest during the run.
- **Randomized.** The ferns and the warps are random; the code fixes the seed.
- **Fixed aspect ratio.** The box changes its scale but not its shape, and in-plane rotation is not modeled.
- **Model growth is bounded by the update rule.** Patches enter the model only when they are misclassified or near the decision boundary; the paper also forgets templates at random when there are too many.
- **Gray values only.** The detector and the tracker use gray values; there is no color.

## Variants and improvements

- **P-N learning alone.** The same experts can train any detector from a video; the paper analyzes this before it describes the tracker.
- **[Forward-backward error](/forward-backward-error/) and median flow** are used alone as a fast short-term tracker.
- **Other detectors.** Later long-term trackers replace the fern cascade with a correlation filter (for example a [kernelized correlation filter](/kernelized-correlation-filter/) as the tracker and a separate detector for recovery) or with a learned network such as [siamese tracking](/siamese-tracking/) with a global search.
- **Tracking by detection.** [Tracking by detection](/tracking-by-detection/) with a pretrained detector replaces the online learning for known object classes.

## When to use it

Use TLD when one object must be followed for a long time, can disappear and come back, and no detector for its class exists in advance. Its learned detector is what lets it recover. For short sequences without occlusion, a [kernelized correlation filter](/kernelized-correlation-filter/) or a [KLT tracker](/kanade-lucas-tomasi-tracker/) is simpler and faster. For object classes that a pretrained detector knows, [tracking by detection](/tracking-by-detection/) is usually more reliable.

## Pitfalls

- **Learning from an occluder.** The trajectory stays reliable until the tracker fails. If a partial occluder still gives a good median motion, the model learns the occluder for a few frames. A strong failure test, such as the median forward-backward error, reduces this.
- **Thresholds copied from the paper.** The relative similarity of an exact match is $1 / (1 + S^-)$, so its scale depends on how similar the negatives are. Calibrate $\theta_{\text{NN}}$ and the core threshold on your data, as the example shows.
- **Similar distractors.** The N-expert assumes one object. A second object of the same kind gives negatives that look like positives, and the detector can lose both.
- **Small objects.** With few pixels, the fern comparisons and the $15 \times 15$ patches carry little information, and the variance test can reject the object itself after a change of light.
- **Number of windows.** The scanning grid grows with the image size and the number of scales; on large frames the detector dominates the cost.

## Implementations

## History

Kalal, Matas and Mikolajczyk introduced P-N learning, the training of a detector from positive and negative structural constraints, at CVPR 2010, and the forward-backward error with the median flow tracker at ICPR 2010. The full system, with the detector cascade of variance filter, random ferns (in the style of Özuysal and colleagues) and nearest neighbor classifier, and the analysis of P-N learning as a linear dynamical system, appeared in IEEE TPAMI in 2012. Early demonstrations of the system used the name Predator, which is why the name is still used for it. Its split into tracking, learning and detection shaped later long-term trackers, which often keep the idea of a short-term tracker plus a re-detector.

## References
