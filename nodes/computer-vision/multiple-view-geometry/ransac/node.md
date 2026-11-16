---
tag: 648BZZ
kind: algorithm
slug: ransac
name: RANSAC
aliases:
- random sample consensus
area: computer-vision/multiple-view-geometry
level: intro
summary: "Fit a model to many random minimal samples of the data, count the data within a threshold of each model, and keep the model with the largest consensus set."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap", s: the size of a minimal sample}
  time: {worst: Θ(k n), average: Θ(k n), best: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1981
  people: [Martin A. Fischler, Robert C. Bolles]
  note: "Fischler and Bolles of SRI International published RANSAC in Communications of the ACM in June 1981, with the location determination problem (the pose of a camera from known landmarks) as the main application."
prereqs: [robust-model-fitting, least-squares-problem]
see_also: [ransac-iteration-bound, msac, lo-ransac, prosac, least-median-of-squares, hough-transform, homography-estimation, efficient-ransac-shape-detection]
sources:
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "The section on the RANSAC paradigm (the threshold, the number of trials with its mean and standard deviation, and the size of an acceptable consensus set)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.7, Robust estimation (RANSAC, the distance threshold, the number of samples and the adaptive rule), and Section 4.8, Automatic computation of a homography"
  - paper: doi:10.1007/978-3-540-45243-0_31
    title: "Ondrej Chum, Jiri Matas and Josef Kittler, Locally optimized RANSAC, Pattern Recognition, DAGM 2003, Lecture Notes in Computer Science 2781, 236-243"
    locator: "Section 1 (why the number of samples in practice is higher than the formula predicts: an all-inlier sample does not always give a model with all inliers)"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "Section 2 (the standard RANSAC loop, its stopping rule and its assumptions) and the survey of the variants in Sections 3 and 4"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 8, Image alignment and stitching (robust least squares and RANSAC for feature-based alignment)"
---

RANSAC (random sample consensus) is a randomized method to fit a model to data in which a large part of the items are wrong. It draws a random *minimal sample*, the smallest set of items that fixes the model (2 points for a line, 4 point matches for a [homography](/homography/)), fits the model to the sample, and counts the items whose error is at most a threshold $\varepsilon$. These items form the *consensus set* of the model. After many samples, RANSAC keeps the model with the largest consensus set and usually refits it to that set by least squares. Unlike [ordinary least squares](/ordinary-least-squares/), whose answer one bad item can move arbitrarily far, RANSAC can tolerate more than half of the data being outliers, because a model is judged only by the items that agree with it. It is the standard tool of [robust model fitting](/robust-model-fitting/) in computer vision.

## In plain words

You have a cloud of dots. Most of them lie close to one straight line, but many are scattered at random. You want the line. A line fit to all dots is pulled away by the scattered ones.

So you guess. Pick two dots at random and draw the line through them. Count how many dots lie close to that line. If both picked dots were on the true line, the count is large. If one of them was a stray dot, the count is usually small. Repeat many times and keep the line with the largest count.

How many times is enough? If half the dots are good, two random dots are both good about one time in four. Seventeen tries then find a good pair with a chance of 99 in 100. At the end, refit the line to all the dots that agreed with the best guess.

## The problem

The input is a set $D = \{x_1, \ldots, x_n\}$ of data items, a model class with a solver that fits a model $\theta$ to a minimal sample of $s$ items, a residual $r(\theta, x) \ge 0$, an inlier threshold $\varepsilon > 0$, a confidence $p \in (0, 1)$ and a cap $k_{\max}$ on the number of samples. The consensus set of a model is $I(\theta) = \{x \in D : r(\theta, x) \le \varepsilon\}$. The output is a model with a large consensus set, and that set. The exact goal, a model with the largest consensus set, is maximum consensus; it is NP-hard in general (see [robust model fitting](/robust-model-fitting/)), and RANSAC is a randomized heuristic for it with a probabilistic guarantee under stated assumptions.

## The algorithm

```pseudo id=main
RANSAC(D, s, ε, p, k_max)                    ▷ n = |D|
L1  θ* ← none, I* ← ∅, k ← k_max, t ← 0
L2  while t < k do
L3      t ← t + 1
L4      S ← s distinct items of D, drawn uniformly at random
L5      θ ← FIT-MINIMAL(S)                    ▷ none for a degenerate sample
L6      if θ is none then continue
L7      I ← {x ∈ D : r(θ, x) ≤ ε}
L8      if |I| > |I*| then
L9          θ* ← θ, I* ← I
L10         w ← |I*| / n
L11         k ← min(k_max, ⌈log(1 − p) / log(1 − w^s)⌉)
L12 if θ* is none then return failure
L13 θ ← FIT-LEAST-SQUARES(I*)
L14 return θ, I*
```

Lines L4 to L7 are one *hypothesize and verify* round: a model from a sample, then its consensus set over all the data. Lines L10 and L11 are the adaptive stopping rule of Hartley and Zisserman (Section 4.7). The inlier ratio $w$ is not known in advance, so the rule uses the ratio of the best consensus set found so far. This estimate only grows, so $k$ only shrinks. The count in line L11 is the [RANSAC iteration bound](/ransac-iteration-bound/). When $w^s = 1$, all items agree with the model, and the code stops at once. Line L13 is the final step of Fischler and Bolles: a least squares fit to the whole consensus set, which averages the noise of all inliers instead of the noise of $s$ items.

The threshold $\varepsilon$ is a design choice. For a residual of one dimension with Gaussian noise of standard deviation $\sigma$, a common choice is $\varepsilon^2 = 3.84\,\sigma^2$, the 95 percent point of a chi-square variable with one degree of freedom (Hartley and Zisserman, Section 4.7); it is tuned in practice.

## Example

Take the 8 points $(0,0), (1,1), (2,2), (3,3), (4,4), (0,4), (1,3), (4,0)$, a line model with $s = 2$, the point-to-line distance as the residual, $\varepsilon = 0.1$ and $p = 0.99$. Five points lie on $y = x$. Four points, $(0,4), (1,3), (2,2), (4,0)$, lie on $x + y = 4$; the point $(2,2)$ is on both lines.

| $t$ | sample | line | consensus set | $\lvert I^*\rvert$ | $w$ | $k$ |
|---|---|---|---|---|---|---|
| 0 | | | | 0 | | $k_{\max}$ |
| 1 | $(0,4), (4,0)$ | $x + y = 4$ | $(0,4), (1,3), (2,2), (4,0)$ | 4 | $1/2$ | 17 |
| 2 | $(1,1), (1,3)$ | $x = 1$ | $(1,1), (1,3)$ | 4 | | 17 |
| 3 | $(0,0), (3,3)$ | $y = x$ | the five points on $y = x$ | 5 | $5/8$ | 10 |

After row 1, $\lceil \log 0.01 / \log(1 - 0.25) \rceil = \lceil 16.01 \rceil = 17$. After row 3, $w^2 = 0.390625$ and $\lceil \log 0.01 / \log 0.609375 \rceil = \lceil 9.30 \rceil = 10$. The samples of rounds 4 to 10 can only tie or lose, so the loop stops at $t = 10$ and line L13 refits $y = x$ to its five points. The second structure, $x + y = 4$, is a strong competitor: if the threshold were larger or the data noisier, the two counts could swap. Fitting several lines at once is the task of [J-linkage](/j-linkage/).

## Correctness

RANSAC keeps an invariant at line L2: $I^*$ is the largest consensus set among the models of the samples drawn so far, and $\theta^*$ is its model. The loop ends, because $t$ grows by 1 in each round and $k \le k_{\max}$. The guarantee is probabilistic. Let $I$ be a largest consensus set, let $q$ be the probability that a random sample lies inside $I$, and assume that each sample inside $I$ gives a model whose consensus set has size $|I|$. If $q \ge (|I|/n)^s$ and $k_{\max} \ge \lceil \log(1 - p) / \log(1 - q) \rceil$, the run returns a consensus set of the largest size with probability at least $p$. The proof shows that the adaptive rule never stops before this count, because the estimate $w$ never exceeds $|I|/n$. For samples drawn with replacement, $q = (|I|/n)^s$ exactly. For distinct items, $q = \binom{|I|}{s} / \binom{n}{s}$, which is a little smaller, so the rule of line L11 is slightly optimistic for small $n$. The full proof is below.

## Complexity

The cost is given per round and for the number of rounds separately, as for any randomized sampler. One round costs the minimal solver, $O(1)$ for a fixed model type such as a line, a [homography](/homography/) or a [fundamental matrix](/fundamental-matrix/), plus $n$ residuals in line L7, so $\Theta(n)$ in the [real RAM](/real-ram/). With $k$ rounds the time is $\Theta(k n)$, and the final refit adds $O(n)$ for a fixed model type. The extra space is $\Theta(n)$ for the two consensus sets.

The number of rounds $k$ is random. It is at most $k_{\max}$. Under the assumptions of the [iteration bound](/ransac-iteration-bound/), with a known inlier ratio $w$, it is about $\log(1 - p) / \log(1 - w^s)$, which grows like $w^{-s} \ln \frac{1}{1 - p}$ for small $w^s$. This is exponential in $s$: with $w = 0.5$ and $p = 0.99$, the count is 17 for $s = 2$, 72 for $s = 4$, 588 for $s = 7$ and 1177 for $s = 8$. So a solver with a smaller minimal sample, such as the [five-point algorithm](/five-point-algorithm/) for the essential matrix instead of the [eight-point algorithm](/eight-point-algorithm/), cuts the number of rounds sharply. This count is not a worst case; it is a bound under assumptions that noise breaks (see Pitfalls).

## Properties

- **Randomized.** Two runs with different seeds can return different answers. The guarantee holds with probability $p$, not always.
- **Tolerates many outliers.** RANSAC does not average over all items, so its answer does not depend on how far the outliers are. It can recover a model supported by fewer than half of the items, as long as no false model gets a larger consensus set.
- **Needs a threshold.** The answer depends on $\varepsilon$, which must match the noise level. [MSAC](/msac/), [MLESAC](/mlesac/) and [MAGSAC](/magsac/) change how the threshold enters the score.
- **Ties.** The test in line L8 is strict, so among equal consensus sets the first one found wins.

## Variants and improvements

- **Better scores.** [MSAC](/msac/) scores a model by a truncated quadratic cost and [MLESAC](/mlesac/) by a likelihood, both from Torr and Zisserman (2000). [MAGSAC](/magsac/) removes the fixed threshold by marginalizing over the noise scale.
- **Local optimization.** [LO-RANSAC](/lo-ransac/) refits each new best model on its inliers inside the loop, which brings the count of rounds close to the formula.
- **Better sampling.** [PROSAC](/prosac/) draws first from the matches of best quality. Guided sampling by Tordoff and Murray (2002) uses match scores as prior probabilities.
- **Faster verification.** [Preemptive RANSAC](/preemptive-ransac/) scores a fixed set of models on blocks of data under a time budget. Chum and Matas (2008) apply the [sequential probability ratio test](/sequential-probability-ratio-test/) to stop the verification of a bad model early.
- **Several models.** Sequential RANSAC removes the inliers of each found model and runs again. [J-linkage](/j-linkage/) clusters the data by the models they agree with. [Efficient RANSAC](/efficient-ransac-shape-detection/) finds planes, spheres and cylinders in point clouds.
- **A framework.** USAC (Raguram et al., 2013) combines these parts into one pipeline.

## When to use it

Use RANSAC when a model has a fast minimal solver, the residual of one item is cheap, and the outlier ratio is moderate, for example the [homography](/homography-estimation/), the [fundamental matrix](/fundamental-matrix/), the [essential matrix](/essential-matrix/) and the [camera pose](/perspective-n-point/) from feature matches. Use it before a refinement that assumes inliers only, such as [Levenberg-Marquardt](/levenberg-marquardt/) on the [reprojection error](/reprojection-error/). If outliers are below about half of the data and the model is linear, [least median of squares](/least-median-of-squares/) or an [M-estimator](/m-estimator/) is an option without a threshold. If the minimal sample is large and $w$ is small, the count $w^{-s}$ explodes; then use a smaller solver, a better ordering of the data ([PROSAC](/prosac/)) or a [Hough transform](/hough-transform/) for low-dimensional models.

## Pitfalls

- **Trusting the count.** The formula assumes that every all-inlier sample gives the correct model. With noise, an all-inlier sample of close points can give a poor model, so the real number of rounds is larger (Chum, Matas and Kittler, 2003). [LO-RANSAC](/lo-ransac/) fixes much of this.
- **A wrong threshold.** If $\varepsilon$ is too small, true inliers fall out and the refit is noisy. If it is too large, outliers join, and a false model can win. Express $\varepsilon$ in the units of the residual, for example pixels for the [Sampson distance](/sampson-distance/).
- **Degenerate samples.** Two equal points give no line; three collinear points of four give no homography. The solver must detect these and return none, as in line L6. Some data are degenerate as a whole: a plane scene makes the fundamental matrix ill-defined, and RANSAC then returns a model with a large but wrong consensus set (Chum, Werner and Matas address this with DEGENSAC).
- **No final refit.** The model of line L5 comes from $s$ noisy items only. Refit it on the consensus set, then recompute the consensus set if needed.
- **Unnormalized data.** For homographies and fundamental matrices, fit with [Hartley normalization](/hartley-normalization/), both in the minimal solver and in the refit.
- **A fixed seed in production.** A fixed seed makes tests repeatable but can hide a rare failure. Test with several seeds.

## Implementations

The Python code fits a line in the plane with $s = 2$. The loop takes the minimal solver, the residual and the refit as arguments, so the same function fits other models. The refit is the total least squares line of the consensus set.

## History

Fischler and Bolles of SRI International published RANSAC in Communications of the ACM in 1981. They used it for the location determination problem, the pose of a camera from image points of known landmarks, and they gave the expected number of trials $w^{-s}$ and its standard deviation. Robust regression in statistics had other answers at the same time: Rousseeuw proposed [least median of squares](/least-median-of-squares/) in 1984, which also tries many random minimal fits but keeps the one of smallest median residual. In computer vision RANSAC became the default with the automatic estimation of two-view geometry in the 1990s, and the variants of the 2000s, from MLESAC to USAC, changed the score, the sampling and the verification step while keeping the loop.

## References
