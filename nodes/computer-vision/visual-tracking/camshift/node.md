---
tag: WQRMAE
kind: algorithm
slug: camshift
name: CAMShift
aliases:
- continuously adaptive mean shift
area: computer-vision/visual-tracking
level: core
summary: Mean shift on a color probability image whose window size and orientation adapt from the moments of the distribution at each frame.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {W: image width, H: image height, m: the number of pixels in the window, k: the iteration limit per frame, B: the number of histogram bins}
  time: {worst: Θ(W H + k m), average: Θ(W H + k m), best: Θ(W H + m)}
  space: {extra: Θ(W H + B)}
properties: {deterministic: true, exact: false, local: true, iterative: true, online: true}
history:
  year: 1998
  people: [Gary R. Bradski]
  note: Bradski built CAMShift at Intel to track faces for a perceptual user interface, running mean shift on a hue probability image and setting the window from its moments.
prereqs: [mean-shift-tracking]
see_also: [mean-shift, mean-shift-segmentation, visual-object-tracking, correlation-filter-tracking, histogram-equalization, eigenvalue, background-subtraction, kalman-filter]
sources:
  - paper: "Gary R. Bradski, Computer vision face tracking for use in a perceptual user interface, Intel Technology Journal, 2nd quarter 1998"
    locator: the whole paper (the hue histogram as a lookup table, the back projection, the mean shift loop on the moments, the size rule s = 2 sqrt(M00/256), and the orientation, length and width from the second moments)
  - paper: doi:10.1109/TPAMI.2003.1195991
    title: Dorin Comaniciu, Visvanathan Ramesh and Peter Meer, Kernel-based object tracking, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(5), 2003, 564 to 577
    locator: the whole paper (the related tracker with kernel histograms and the Bhattacharyya coefficient)
  - paper: doi:10.1109/34.1000236
    title: Dorin Comaniciu and Peter Meer, Mean shift, a robust approach toward feature space analysis, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(5), 2002, 603 to 619
    locator: the whole paper (the mean shift procedure with a flat kernel and its shadow kernel)
---

CAMShift (continuously adaptive mean shift) tracks a colored target by running [mean shift](/mean-shift/) on a probability image. A histogram of the target colors becomes a lookup table, and every pixel of a new frame is replaced by the table value of its color, so bright pixels in the probability image are pixels that look like the target. The tracker moves a window to the centroid of the probability inside it until the window stops moving. Then it reads the size of the window for the next frame from the total probability inside it, and the orientation, length and width of the target from the second moments. Gary Bradski described it in 1998 for face tracking in a user interface. It is a simpler cousin of [mean shift tracking](/mean-shift-tracking/), with an adaptive window in place of a fixed one.

## In plain words

Suppose the target is a face, and faces have a skin color. We make a gray picture in which each pixel is bright if its color is a common skin color and dark if not. We put a box where the face was and move the box to the center of brightness inside it. We repeat until the box stays still. Then we count how much brightness is in the box. A large face gives a lot, so we make the box larger for the next picture, and a small face gives less, so we make it smaller. The way the brightness spreads inside the box also tells us whether the face is tilted, and by how much.

## The problem

The frames are [digital images](/digital-image/) indexed $I[v][u]$, with the center of pixel $(u, v)$ at the point $(u, v)$, $u$ to the right and $v$ down. Each pixel has a bin $b(x) \in \{1, \ldots, B\}$; Bradski uses the hue of a color pixel and ignores pixels with low saturation, where hue is not reliable. On this page the bin is a gray value divided into $B$ equal ranges. The target is given as a window in the first frame. The histogram $h_1, \ldots, h_B$ of that window, scaled so that the largest entry is 255, is the lookup table, and the probability image of a frame is $P(x) = h_{b(x)}$.

For a window $R$, the moments of $P$ are

$$
M_{ij} = \sum_{(u, v) \in R} u^i v^j P(u, v), \qquad x_c = \frac{M_{10}}{M_{00}}, \quad y_c = \frac{M_{01}}{M_{00}} .
$$

The task in each frame is to find a window centered on the centroid of the probability inside it, and to report its size and the orientation and spread of the mass. A window here is a center $(c_u, c_v)$ with half sizes $(a_u, a_v)$, that is the pixels with $|u - c_u| \le a_u$ and $|v - c_v| \le a_v$.

## The algorithm

```pseudo id=main
CAMSHIFT(F₀, ..., F_N, window, k_max, ε)
L1   h ← histogram of the window in F₀, scaled so that max h = 255
L2   for t ← 1 to N do P(x) ← h_{b(x)} for every pixel x of F_t
L3       repeat up to k_max times
L4           compute M₀₀, M₁₀, M₀₁ of P in the window
L5           if M₀₀ = 0 then report LOST and keep the window
L6           move the window center to (M₁₀/M₀₀, M₀₁/M₀₀)
L7           if the center moved less than ε then leave the loop
L8       s ← 2 √(M₀₀ / 256), rounded up to an odd integer, at least 3
L9       (θ, l, w) ← the axis angle and the two spreads from M₂₀, M₁₁, M₀₂   ▷ formulas below
L10      the window for frame t + 1 has the new center and side s;  report (x_c, y_c, θ, l, w)
L11  return the reports
```

Lines L3 to L7 are mean shift with a flat kernel on the probability image: the step is the centroid of $P$ in the window. Line L8 is Bradski's size rule; the number 256 is the largest value of $P$ plus one, so for a solid target of probability near 255, $M_{00} / 256$ is close to its area in pixels. Bradski makes the next window $s$ wide and $1.2 s$ long for faces, which are longer than they are wide; the code has a factor for that, set to 1 by default. Line L9 uses

$$
a = \frac{M_{20}}{M_{00}} - x_c^2, \quad b = 2 \Big( \frac{M_{11}}{M_{00}} - x_c y_c \Big), \quad c = \frac{M_{02}}{M_{00}} - y_c^2, \quad \theta = \tfrac12 \operatorname{atan2}(b, a - c),
$$

$$
l = \sqrt{\frac{a + c + \sqrt{b^2 + (a - c)^2}}{2}}, \qquad w = \sqrt{\frac{a + c - \sqrt{b^2 + (a - c)^2}}{2}} .
$$

Here $\theta$ is the orientation of the major axis, measured from the $u$ axis toward the $v$ axis (clockwise on the screen, since $v$ points down), and $l$ and $w$ are the standard deviations of the mass along the two axes. Bradski writes the angle with the arctangent of $b / (a - c)$; atan2 picks the right quadrant. Bradski also computes the probability image only in a region a little larger than the window, not the whole frame.

## Example

**The size rule.** A $10 \times 10$ square of probability 255 inside the window gives $M_{00} = 25500$ and $s = 2\sqrt{25500 / 256} = 19.96$, which rounds up to 20 and then to the odd 21. So the next window is about twice the side of the target. The centroid is the center of the square, and $a = c = 99/12$ (the variance of 10 consecutive integers) and $b = 0$, so $l = w = 2.872$.

**A tilted ellipse.** A solid ellipse with semi-axes 12 and 5, tilted 30 degrees, covers 193 pixels of probability 255, so $M_{00} = 49215$ and $s = 29$. Line L9 gives $\theta = 30.98$ degrees, $l = 6.029$ and $w = 2.546$. For the continuous ellipse the exact values are 30 degrees, $12/2 = 6$ and $5/2 = 2.5$ (the proof shows why the lengths are half the semi-axes); the difference comes from the pixel grid. Started at $(36, 43)$ with half size 15, the loop moves the window to the center $(40, 40)$.

**A target that moves and grows.** The frames are $80 \times 80$ with gray noise from 0 to 119 (seed 7) and a square target with values from 180 to 239, which moves by $(3, 2)$ per frame while its half side grows from 4 to 8.5 over 10 frames. The first window is the target itself, so the lookup table is 0 for all background bins. In frame 1 the window has half size 4 and the target, now a little larger, has moved 3 pixels: the loop stops at $(21.98, 26.60)$, 1.09 pixels short of the true center, because a window no larger than the target sees only part of it and the centroid of the part is a fixed point. The size rule then sets the half size to 6.5. From frame 2 on, the window is larger than the target, the error stays between 0.08 and 0.33 pixel, and the half size grows with the target: 6.5, 9.5, 9.5, 11.5, 11.5, 12.5, 12.5, 14.5, 14.5.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). These are theorems about the formulas.

- **Centroid.** Line L6 moves the window to the centroid of the probability inside it, and a window centered on its own centroid is a fixed point of the loop.
- **Orientation and lengths.** With $\Sigma = \begin{pmatrix} a & b/2 \\ b/2 & c \end{pmatrix}$ the covariance of the mass, $(\cos\theta, \sin\theta)$ is an [eigenvector](/eigenvalue/) for its larger eigenvalue, and $l$ and $w$ are the square roots of the two eigenvalues. For a uniform ellipse with semi-axes $A \ge B$ these are $A/2$ and $B/2$, and $\theta$ is the angle of its major axis.
- **Size.** For a uniform target of $n$ pixels at 255, $s = 2\sqrt{n}\sqrt{255/256}$, so for a square of side $\ell$ the window side is just under $2\ell$ before rounding.
- **Stopping.** The loop stops after at most $k_{\max}$ iterations.

Bradski's paper says that mean shift converges. For a disc window the flat-kernel step climbs a density estimate with the Epanechnikov kernel, as on the [mean shift tracking](/mean-shift-tracking/) page. The rectangular window used here is not covered by that argument, and on a pixel grid the loop can stop short, as in the example. So the page claims no convergence theorem; the cap is what ends the loop. Whether the window covers the true target depends on the colors, and the back projection is a heuristic.

## Complexity

The back projection reads every pixel once, $\Theta(W H)$ per frame, or $\Theta(m')$ for a calculation region of $m'$ pixels as in Bradski's version. Each loop iteration sums over the $m$ pixels of the window, so the loop costs $\Theta(k m)$ in the worst case and $\Theta(m)$ if it stops at once. Lines L8 to L10 cost $\Theta(m)$ for the second moments. Building the lookup table costs $\Theta(m + B)$ once. The extra space is $\Theta(W H)$ for the probability image and $\Theta(B)$ for the table.

## Properties

- **Adaptive size and orientation.** The window grows and shrinks with the target, and the tilt comes for free from the moments.
- **Cheap.** A few sums per frame over a small region, with no training beyond one histogram.
- **Color only.** Like [mean shift tracking](/mean-shift-tracking/), it ignores where colors are inside the window, so it cannot tell two objects of the same color apart.
- **Self-growing.** If the background has some target color near the target, the window grows to cover it, and the size rule feeds that growth back.
- **Local.** The target must overlap the window from the previous frame.

## Variants and improvements

- **Hue and saturation.** Use a 2D histogram of hue and saturation, or mask out pixels with low saturation or low brightness, which have unreliable hue.
- **Kernel histograms.** Weight pixels by their distance to the window center and compare histograms with the Bhattacharyya coefficient, which gives [mean shift tracking](/mean-shift-tracking/).
- **Background ratio.** Divide the target histogram by a background histogram, so that colors common in the scene get a low probability.
- **Prediction.** Start the search where a [Kalman filter](/kalman-filter/) predicts the target.
- **Other probability images.** Any image of per-pixel target probability works, for example the output of [background subtraction](/background-subtraction/) or of a skin color classifier.

## When to use it

Use CAMShift for a target with a distinctive color in a scene without many similar colors, when the size changes over time and you want a very cheap tracker, for example a hand or a face in front of a computer. It is a common first tracker in teaching because each step is a few sums. Do not use it for gray images, for targets whose colors are common in the background, or when two targets of the same color can meet.

## Pitfalls

- **A window as small as the target.** The loop stops at the centroid of the part of the target it can see, so a tight window lags behind a moving target, as in frame 1 of the example. The size rule makes the window larger than the target for this reason.
- **Low saturation.** Gray, white and black pixels have a random hue. Leave them out of the histogram and the back projection.
- **Runaway growth.** A target-colored background next to the target pulls the window, the window grows, and then it holds even more background. Limit the size or use a background ratio.
- **The angle when the mass is round.** When $b^2 + (a - c)^2$ is near 0, $\theta$ is noise. Report it only when $l$ is clearly larger than $w$.
- **Image axes.** With $v$ pointing down, a positive $\theta$ is a clockwise turn on the screen; mixing this with a $y$-up convention flips the sign of the angle.

## Implementations

## History

Gary Bradski described CAMShift in the Intel Technology Journal in 1998 as the face tracker of a perceptual user interface, in which the position and tilt of the head serve as input to the computer. The work used the mean shift procedure of Fukunaga and Hostetler and Cheng, and added the adaptive window and the moment-based orientation. The method became widely known through the OpenCV library, which Bradski led at Intel. Comaniciu, Ramesh and Meer (2000, 2003) developed the related [mean shift tracking](/mean-shift-tracking/) with kernel histograms and the Bhattacharyya coefficient.

## References
