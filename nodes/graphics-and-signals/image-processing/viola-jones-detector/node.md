---
tag: 3QXCD1
kind: algorithm
slug: viola-jones-detector
name: Viola-Jones object detector
aliases:
- Viola-Jones face detection
- Haar cascade
area: graphics-and-signals/image-processing
level: advanced
summary: Slide a window over all positions and scales and reject it early in a cascade of boosted stumps on Haar-like features, each computed from an integral image.
solves: [face-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, T: the number of weak classifiers in the cascade}
  time: {worst: O(W H T), best: O(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, heuristic: true, rotation_invariant: false, invariant_to_gain: true}
history:
  year: 2001
  people: [Paul Viola, Michael Jones]
  note: Viola and Jones presented the detector at CVPR 2001 and in a longer form in the International Journal of Computer Vision in 2004. The paper reports a detection rate close to the best methods of the time at about 15 times their speed.
prereqs: [haar-features, adaboost, integral-image]
see_also: [face-detection, decision-stump, boosting, sliding-window, disjoint-set, non-maximum-suppression, normalized-cross-correlation, haar-wavelet]
sources:
  - paper: doi:10.1023/B:VISI.0000013087.49260.fb
    title: Paul Viola and Michael J. Jones, Robust real-time face detection, International Journal of Computer Vision 57(2), 137-154, 2004
    locator: Section 2 and 2.1 (features and the integral image); Section 3, Table 1 and Section 3.1 (AdaBoost and the stump search); Section 4 and 4.1, Table 2 (the cascade and its training); Sections 5.2 to 5.6 (structure, speed, variance normalization, scanning, merging)
  - paper: doi:10.1109/CVPR.2001.990517
    title: Paul Viola and Michael Jones, Rapid object detection using a boosted cascade of simple features, IEEE Conference on Computer Vision and Pattern Recognition, vol. 1, I-511 to I-518, 2001
    locator: the whole paper (the first form of the method)
  - paper: doi:10.1109/ICIP.2002.1038171
    title: Rainer Lienhart and Jochen Maydt, An extended set of Haar-like features for rapid object detection, IEEE International Conference on Image Processing, 2002
    locator: the whole paper (rotated features and their integral image)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 6, Recognition, Section 6.3 Object detection (face detection)
---

The Viola-Jones detector finds objects of one class, most often upright frontal faces, in a gray image. It slides a square window over every position and over a range of scales and decides for each window whether it contains the object. The decision uses [Haar-like features](/haar-features/), differences of the pixel sums of two to four adjacent rectangles, which an [integral image](/integral-image/) gives in a constant number of reads at any scale. [AdaBoost](/adaboost/) picks a few features from more than 160,000 candidates and joins threshold tests on them, [decision stumps](/decision-stump/), into a weighted vote. The votes are put in a cascade of stages: a cheap first stage rejects most windows, and only the windows that pass every stage are reported. The cost is $O(WHT)$ in the worst case for a $W \times H$ image and a cascade with $T$ weak classifiers, but on real images most windows stop after a few features. Paul Viola and Michael Jones published it in 2001. It is a learned heuristic: its detection rate depends on the training data, and it gives no guarantee on any image.

## In plain words

You want to find faces in a photo. Look at the photo through a small square frame, at every place and in several frame sizes. For each view, ask simple questions such as "is the band of the eyes darker than the band of the cheeks below it?". Each question is answered by adding up pixels in a few boxes, which a prepared table makes very fast. A training step with many example faces and non-faces picks the most useful questions and how much each one counts. The questions are put in groups. The first group has only two questions and throws away about half of the views that are clearly not faces. Later groups ask more questions, but only about the few views that are left. A view that passes every group is reported as a face, and nearby reports are joined into one.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows, one channel of integers, for example 8-bit values in $0$ to $255$, used as they are stored with no gamma step. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. Windows lie fully inside the image, so no border rule is needed. The detector has a base window of $n \times n$ pixels, $24 \times 24$ in the paper, and a trained cascade. The output is a list of square boxes $(x_0, y_0, x_1, y_1)$ with the object inside.

A feature $f$ is a pattern of two, three or four equal cells of $w \times h$ pixels at a position in the window. Its value is the sum of the pixels in the cells with weight $+1$ minus the sum in the cells with weight $-1$ (see [Haar-like features](/haar-features/)). A weak classifier is a stump

$$h(x) = \begin{cases} 1 & \text{if } p\, f(x) < p\, \theta, \\ 0 & \text{otherwise,} \end{cases}$$

with a feature $f$, a polarity $p \in \{1, -1\}$ and a threshold $\theta$, as in Section 3 of the paper. A stage is a weighted vote $\sum_t \alpha_t h_t(x) \ge \Theta$ of a few stumps. A cascade is a list of stages, and a window is accepted exactly when every stage accepts it.

## The algorithm

```pseudo id=main
DETECT(I, cascade, n, Δ)                       ▷ I is W × H, base window n × n, step Δ
L1  S1 ← INTEGRAL-IMAGE(I);  S2 ← INTEGRAL-IMAGE(I²)
L2  for s ← 1, 1.25, 1.25², … while ⌊n s⌋ ≤ min(W, H) do
L3      scale every feature of the cascade by s;  stride ← max(1, ⌊s Δ + 1/2⌋)
L4      for each window (x, y) of size ⌊n s⌋ with x, y multiples of stride do
L5          σ ← the standard deviation of the window, from S1 and S2
L6          for each stage (h_1 … h_k, α_1 … α_k, Θ) of the cascade, in order do
L7              if Σ_t α_t h_t(window) < Θ then reject the window and go to the next one
L8          add the window to the detections
L9  join the detections whose boxes overlap, transitively; return the average box of each group

TRAIN-STAGE(P, N, f_max, d_min)                ▷ positives P, negatives N that reach this stage
L10 w_i ← 1/(2l) for each of the l positives and 1/(2m) for each of the m negatives
L11 for t ← 1, 2, … do
L12     w ← w / Σ w
L13     h_t ← the stump with the least weighted error ε_t over all features, thresholds and polarities
L14     β_t ← ε_t / (1 − ε_t);  α_t ← log(1/β_t);  w_i ← w_i β_t for each example that h_t classifies correctly
L15     Θ ← min(½ Σ α_t, the largest value that keeps a fraction d_min of P);  stop when at most f_max of N pass
L16 the negatives that pass the stage are the negatives of the next stage
```

Line L1 builds two integral images, of $I$ and of $I^2$. Each feature value is then a sum of six, eight or nine table entries with integer weights, at any position and scale. Lines L2 and L3 follow Section 5.5 of the paper: the detector is scaled, not the image, by factors of $1.25$, and the window moves by $[s\Delta]$ pixels, where $[\,]$ is rounding. The implementation scales the position and size of each cell with the floor and divides the value by the ratio of the cell areas, so that a scaled feature has the same range as at scale 1. Line L5 is Section 5.4: the variance of the window is $\frac{1}{a}\sum x^2 - \left(\frac{1}{a}\sum x\right)^2$ for a window of $a$ pixels, from the two tables. Every feature value is divided by $\sigma$, which has the same effect as dividing the pixels by $\sigma$. The implementation uses $\sigma = 1$ for a flat window.

Lines L6 and L7 are the cascade of Section 4. A stage computes only its own features, and a window that one stage rejects is never seen by the later stages. Line L9 is Section 5.6: two detections are in the same group if their boxes overlap, and the groups are the connected parts of this relation, which a [disjoint-set](/disjoint-set/) structure finds. The corners of the result are the averages of the corners in the group.

Lines L10 to L14 are AdaBoost as in Table 1 of the paper. The start weights give the positives and the negatives half of the total each. Line L13 finds the best stump for each feature by one sweep over the examples sorted by the feature value, as Section 3.1 describes: with $S^+$ and $S^-$ the weight of the positives and the negatives below the threshold and $T^+$, $T^-$ the totals, the error is $S^- + (T^+ - S^+)$ for $p = 1$ and $S^+ + (T^- - S^-)$ for $p = -1$. Line L14 makes the correctly classified examples lighter, so the next stump must do well on the others. If some stump has $\varepsilon = 0$, it separates the examples alone and the implementation uses it as the whole stage.

Lines L15 and L16 are the cascade training of Table 2. The vote threshold of AdaBoost is $\frac{1}{2}\sum \alpha_t$. Table 2 lowers it until the stage keeps the required detection rate, and it adds stumps until the false positive rate of the stage is low enough. The negatives for the next stage are the ones the cascade so far still accepts, so each stage learns the cases that are hard for the stages before it. The paper collects these from a large set of images without faces; the implementation keeps them from a fixed list.

## Example

**One stump search.** Take five examples of one feature with values $1, 2, 4, 3, 5$, where the first three are positives ($l = 3$) and the last two negatives ($m = 2$). Line L10 gives the weights $\frac16, \frac16, \frac16, \frac14, \frac14$.

| round | weights at line L12 | best stump | $\varepsilon_t$ | $\beta_t$ | $\alpha_t$ |
|---|---|---|---|---|---|
| 1 | $\frac16, \frac16, \frac16, \frac14, \frac14$ | $p = 1$, $\theta = 2.5$ | $\frac16$ | $\frac15$ | $\ln 5 \approx 1.609$ |
| 2 | $\frac1{10}, \frac1{10}, \frac12, \frac3{20}, \frac3{20}$ | $p = 1$, $\theta = 4.5$ | $\frac3{20}$ | $\frac3{17}$ | $\ln \frac{17}{3} \approx 1.735$ |
| 3 | $\frac1{17}, \frac1{17}, \frac5{17}, \frac12, \frac3{34}$ | $p = -1$, $\theta = 3.5$ | $\frac7{34}$ | $\frac7{27}$ | $\ln \frac{27}{7} \approx 1.350$ |

In round 1 the stump "value below $2.5$" misses only the positive with value $4$, so $\varepsilon_1 = \frac16$. Line L14 multiplies the four correct weights by $\frac15$, and line L12 of round 2 scales the sum back to 1. Now the missed example carries half of the weight, so round 2 picks a stump that gets it right. After round 3 the vote threshold is $\frac12(1.609 + 1.735 + 1.350) \approx 2.347$. The vote is $3.344$ for the values $1$ and $2$, $3.085$ for $4$, $1.735$ for $3$ and $1.350$ for $5$, so the three stumps together classify all five examples correctly, though no single stump does.

**The cost of a cascade.** Let a cascade have three stages with $2$, $5$ and $20$ features, and let $\frac12$ of the windows that reach stage 1 pass it, and $\frac15$ of those that reach stage 2 pass it. Every window computes the 2 features of stage 1, half of them the 5 of stage 2, and a tenth of them the 20 of stage 3. The mean number of features per window is $2 + 5 \cdot \frac12 + 20 \cdot \frac12 \cdot \frac15 = 6.5$, against $27$ for one stage with all the features. This is the formula $N = n_0 + \sum_i n_i \prod_{j < i} p_j$ of Section 4.1 of the paper.

**The number of windows.** For a $384 \times 288$ image and $n = 24$, lines L2 to L4 with $\Delta = 1$ visit 12 scales, which matches the 12 scales that Section 2.1 of the paper gives for this size, and $264{,}069$ windows with the rounding used here. With $\Delta = 1.5$ and a first scale of $1.25$ they visit 11 scales and $65{,}072$ windows.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that each feature value from the corner weights equals the rectangle sums of its definition, that line L5 gives the standard deviation of the window, and that the sweep of line L13 finds a stump of least weighted error over all thresholds and both polarities. It also shows two facts of AdaBoost that the tests check exactly with rational weights: the weights at line L12 sum to 1, and after the update of line L14 the stump just chosen has a weighted error of exactly $\frac12$, so the next round cannot choose it again with the same effect. For the cascade it shows that a window is reported exactly when every stage accepts it, that the stages after a rejection compute nothing, and that the mean cost is the formula of the example. The threshold of line L15 keeps at least the fraction $d_{\min}$ of the training positives. None of this says that the detector finds faces: that is an empirical property of the trained cascade.

## Complexity

- **Tables (L1).** $\Theta(WH)$ time and space.
- **Windows (L2 to L4).** At scale $s$ there are about $(W - ns)(H - ns)/\text{stride}^2$ windows. With $\Delta \ge 1$ the stride grows like $s$, so the number over all scales is a geometric sum and is $\Theta(WH)$ for $n$ much smaller than $W$ and $H$. With a stride of 1 at every scale it is $O(WH \log(\min(W, H)/n))$.
- **Per window (L5 to L8).** Line L5 costs $O(1)$. Each feature costs at most 9 table reads, so a window that reaches the end costs $\Theta(T)$, and a window rejected by the first stage costs $\Theta(n_1)$ for its $n_1$ features.
- **Merge (L9).** The implementation compares all pairs of the $D$ detections, $O(D^2)$, and the number of detections is small in practice. A sweep over sorted boxes makes it $O(D \log D + \text{overlaps})$.

The total is $O(WHT)$ in the worst case and $O(WH)$ in the best case, when the first stage rejects every window. The mean cost is $O(WH \cdot \bar N)$ with $\bar N$ the mean number of features per window, which depends on the images and the cascade. For the 38-stage cascade of the paper with 6060 features, Section 5.3 reports a mean of 8 features per window on the MIT+CMU test set. That number is an observation on that data, not a bound.

**Training.** Let $F$ be the number of features and $K$ the number of examples. Sorting every feature once costs $O(FK\log K)$, and each round of AdaBoost then costs $O(FK)$ for the sweeps. The paper uses $F \approx 160{,}000$, so training is the expensive part of the method. Section 5.2 reports that training the 38-stage cascade took on the order of weeks on one machine of that time.

## Properties

- **Gain.** Dividing by $\sigma$ makes every feature value invariant to a gain $cI$ with $c > 0$.
- **Offset.** A feature whose weights sum to zero does not change when a constant is added. The two- and four-rectangle features do. The three-rectangle feature of the paper, center minus two outer cells, does not, so its value after division by $\sigma$ still depends on the mean of the window.
- **Scale.** The window is scaled in steps of $1.25$, so an object between two steps is seen at the nearest one. The training data must have the object at a fixed size and position in the window for this to work.
- **Rotation.** The features are aligned with the axes. A frontal detector does not find faces turned more than a small angle in the image plane or turned to the side. Separate cascades are trained for each pose.
- **Early rejection.** The mean cost is much smaller than the worst case only because most windows are easy negatives. On an image where many windows look like the object, the cost goes up.
- **Detection and false positive rates multiply.** With stage rates $d_i$ and $f_i$, the cascade has $D = \prod d_i$ and $F = \prod f_i$. With 10 stages of $d_i = 0.99$ and $f_i = 0.3$ one gets $D \approx 0.90$ and $F \approx 6 \cdot 10^{-6}$; this is the example of Section 4 of the paper.

## Variants and improvements

- **More features.** Lienhart and Maydt (2002) add features turned by $45°$, with a rotated integral image, and center-surround features.
- **Other boosting.** Real AdaBoost and Gentle AdaBoost use real-valued weak classifiers instead of 0 or 1 outputs. Variants such as soft cascades and boosting chains reuse the score of earlier stages instead of starting each stage from zero.
- **Other features.** Local binary patterns and histograms of gradients take the place of Haar-like features in later cascades. The cascade and the integral image stay.
- **Better merging.** Requiring a minimum number of detections per group, or [non-maximum suppression](/non-maximum-suppression/) by score, removes isolated false positives. Section 5.7.1 of the paper runs three cascades and keeps only the detections that at least two of them agree on.
- **CNN detectors.** Detectors based on convolutional neural networks are more accurate on hard poses and lighting and have replaced the cascade in most new systems.

## When to use it

Use a Viola-Jones cascade for fast detection of a rigid object class with a stable appearance, such as frontal faces, on devices with little compute or memory, or as a first filter before a slower classifier. Pretrained cascades are available in common libraries, so no training is needed for faces. Do not use it for objects with large changes of pose, shape or viewpoint, or when the best accuracy matters more than speed. For the problem in general, see [face detection](/face-detection/).

## Pitfalls

- **Variance in floating point.** $\frac1a\sum x^2 - m^2$ in single precision can lose all digits or come out negative on a nearly flat window. Compute $a\sum x^2 - (\sum x)^2$ in integers, as the [integral image](/integral-image/) page explains. The paper prints the formula as $\sigma^2 = m^2 - \frac1N \sum x^2$; the terms are swapped, and the correct form is $\sigma^2 = \frac1N\sum x^2 - m^2$.
- **Flat windows.** $\sigma = 0$ divides by zero. Use a minimum $\sigma$, as the implementation does with $\sigma = 1$.
- **Scaling the features.** Rounding the cells of a scaled feature changes their areas, and the two halves of a feature can get different areas. Divide by the area of the scaled cells, or round so that the cells stay equal.
- **Training data.** The positives must be aligned in the same way, and the negatives for later stages must come from images that contain no object. Too few hard negatives give a cascade that accepts too much.
- **The feature count.** The paper gives about 160,000 features for a $24 \times 24$ window (2001: over 180,000). The exact number for the five shapes with equal cells, two horizontal and vertical, three horizontal and vertical, and four, is $162{,}336$; other counts come from other shape sets or rules.
- **Thresholds of the cascade.** The stage thresholds are tuned on the training data. A stage that rejects too many positives loses them for good, because no later stage can bring them back.

## Implementations

## History

Paul Viola and Michael Jones presented the detector at CVPR 2001 under the title "Rapid object detection using a boosted cascade of simple features", and the longer version "Robust real-time face detection" appeared in the International Journal of Computer Vision in 2004. Its three ideas were the integral image for fast rectangle features, AdaBoost as a way to select a few features from a very large set, and the cascade that spends time only on promising windows. They built on the Haar wavelet features of Papageorgiou, Oren and Poggio (1998) and on the boosting of Freund and Schapire. The paper reports detection on $384 \times 288$ images at 15 frames per second on a conventional desktop of the time. Lienhart and Maydt extended the features in 2002, and their implementation in the OpenCV library made the "Haar cascade" a standard tool for many years.

## References
