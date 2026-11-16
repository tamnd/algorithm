---
tag: 86C9V2
kind: algorithm
slug: preemptive-ransac
name: Preemptive RANSAC
aliases:
- preemptive scoring RANSAC
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Generate a fixed set of hypotheses, score them on the data in random order, and keep only the better half after each block of data, so the time is fixed in advance."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {M: the number of hypotheses, B: the block size of the preemption function, N: the number of observations, c: the cost of one minimal solve in units of one scoring}
  time: {worst: O(M (c + 2B) + M log M + N), average: O(M (c + 2B) + M log M + N), best: O(M (c + 2B) + M log M + N)}
  space: {extra: Θ(M + N)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [David Nistér]
  note: "Nistér presented preemptive RANSAC at ICCV 2003 as the robust core of a system for live structure and motion estimation with a calibrated camera."
prereqs: [ransac]
see_also: [ransac-iteration-bound, msac, prosac, lo-ransac, five-point-algorithm, relative-pose-problem, robust-model-fitting]
sources:
  - paper: "David Nistér, Preemptive RANSAC for live structure and motion estimation, Proceedings of the Ninth IEEE International Conference on Computer Vision (ICCV 2003), 199-206"
    title: "David Nistér, Preemptive RANSAC for live structure and motion estimation, ICCV 2003"
    locator: "Algorithm 1 (preemptive scoring), the preemption function f(i) = floor(M 2^(-floor(i/B))), the time t(f) and Table 1 (M = 500, B = 100)"
  - paper: doi:10.1007/s00138-005-0006-y
    title: "David Nistér, Preemptive RANSAC for live structure and motion estimation, Machine Vision and Applications 16(5), 2005, 321-329"
    locator: "The journal version of the same method"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "The survey of methods that speed up the verification of hypotheses, including preemptive RANSAC"
---

Preemptive RANSAC is a variant of [RANSAC](/ransac/) for real-time systems, where the time per frame is fixed and an answer must come in time. RANSAC works depth-first: it scores each hypothesis on all the data before it draws the next, and the number of hypotheses depends on the data. Preemptive RANSAC works breadth-first. It first generates a fixed number $M$ of hypotheses from random minimal samples. Then it puts the observations in random order and scores all hypotheses on the first observations; after every block of $B$ observations it drops the worse half of the hypotheses by their accumulated score, until one is left. So the total work is known in advance, at most $M\tau + 2BM$ scorings, where $\tau$ is the cost of one hypothesis. Nistér introduced it in 2003 for the live estimation of camera motion with the [five-point algorithm](/five-point-algorithm/).

## In plain words

Imagine a contest with 500 runners and a fixed amount of time. You do not have time to let every runner run the full course. So you let all of them run a short stretch and send home the slower half. The others run another stretch, and again the slower half goes home. After a few rounds one runner is left.

Preemptive RANSAC does this with guesses. It makes all its guesses at the start. Then it checks all guesses against a few points of the data, in a random order, and throws away the worse half. The survivors are checked against a few more points, and so on. Good guesses get checked on many points; bad guesses are dropped after a few. The total work is the same every time, which is what a live video system needs.

## The problem

The input is a set of $N$ observations, a minimal solver, a score $\rho(o, h)$ of one observation $o$ for a hypothesis $h$ (here a cost, lower is better), the number of hypotheses $M$ and a preemption function $f(i)$, the number of hypotheses that remain to be scored on observation $i$. Nistér uses

$$f(i) = \big\lfloor M \, 2^{-\lfloor i/B \rfloor} \big\rfloor,$$

which halves the number of hypotheses after each block of $B$ observations. The goal is the hypothesis with the best total score, found within a time that does not depend on the data. Preemptive RANSAC is a heuristic for this goal: it can drop the best hypothesis early.

## The algorithm

The steps follow Algorithm 1 of Nistér (2003).

```pseudo id=main
PREEMPTIVE-RANSAC(D, M, B, ρ)                ▷ N = |D|
L1  o_1, …, o_N ← the observations in random order
L2  h_1, …, h_M ← the models of M random minimal samples
L3  L(h) ← ρ(o_1, h) for every h; H ← all M hypotheses; i ← 2
L4  loop
L5      if i > N or f(i) ≤ 1 then return the h ∈ H of least L(h)
L6      if f(i) < |H| then H ← the f(i) hypotheses of H of least L
L7      L(h) ← L(h) + ρ(o_i, h) for every h ∈ H
L8      i ← i + 1
```

Line L6 needs only a partial order: the $f(i)$ best hypotheses, in any order. A selection algorithm such as [quickselect](/quickselect/) does it in $O(|H|)$ time, as Nistér suggests; the code sorts, which costs $O(|H| \log |H|)$. The score is a design choice. The code uses the truncated quadratic $\rho(o, h) = \min(r(o, h)^2, T^2)$ of [MSAC](/msac/); any additive score with a ceiling works. Ties in line L6 are broken by the index of the hypothesis in the code.

## Example

Take the 8 points of the [RANSAC](/ransac/) example, $(0,0), (1,1), (2,2), (3,3), (4,4), (0,4), (1,3), (4,0)$, with $T = 0.1$. All hypotheses pass exactly through their inliers, so each observation costs 0 or $T^2 = 0.01$, and the accumulated cost is $0.01$ times the number of outliers seen. Use $M = 8$ hypotheses and $B = 2$, so $f(1), \ldots, f(6) = 8, 4, 4, 2, 2, 1$. The hypotheses are

| $h$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| line | $y = x$ | $x + y = 4$ | $x = 1$ | $y = 0$ | $y = 4$ | $y = 3$ | $y = 3x$ | $3x + y = 4$ |

With the seed 2, the order of the observations starts $(0,4), (3,3), (4,4), (1,1), (2,2)$. The table shows the number of outliers seen by each hypothesis still in play:

| $i$ | $o_i$ | $f(i)$ | hypotheses kept, with outliers seen |
|---|---|---|---|
| 1 | $(0,4)$ | 8 | $h_0{:}1$, $h_1{:}0$, $h_2{:}1$, $h_3{:}1$, $h_4{:}0$, $h_5{:}1$, $h_6{:}1$, $h_7{:}0$ |
| 2 | $(3,3)$ | 4 | $h_1{:}1$, $h_4{:}1$, $h_7{:}1$, $h_0{:}1$ |
| 3 | $(4,4)$ | 4 | $h_0{:}1$, $h_1{:}2$, $h_4{:}1$, $h_7{:}2$ |
| 4 | $(1,1)$ | 2 | $h_0{:}1$, $h_4{:}2$ |
| 5 | $(2,2)$ | 2 | $h_0{:}1$, $h_4{:}3$ |

At $i = 6$, $f(6) = 1$, and the run returns $h_0$, the line $y = x$, after $8 + 4 + 4 + 2 + 2 = 20$ scorings instead of the $64$ of full scoring. With the seed 3 the order starts $(0,0), (0,4), (4,0), (2,2), (1,1)$, three points of $x + y = 4$ come first, and the run returns $h_1$, although $h_0$ has the lower total cost over all 8 points ($0.03$ against $0.04$). Preemption trades this risk for a fixed time.

## Correctness

The algorithm keeps an invariant at line L5: for every $h \in H$, $L(h)$ is the sum of $\rho(o_j, h)$ over $j < i$, and $H$ holds the $f(i-1)$ hypotheses that were best at each cut. The returned hypothesis has the least accumulated score among the survivors. The loop ends after at most $N$ steps, because $i$ grows by 1 and line L5 stops at $i > N$. The number of scorings is exactly $M + \sum_{i=2}^{i_{\text{end}}} f(i)$, which does not depend on the data. If $f(i) = M$ for all $i \le N$, nothing is dropped and the result is the hypothesis of least total score, as in full scoring. With preemption, there is no guarantee that the best hypothesis survives; Nistér studies the chance of this under a simple inlier and outlier model. The proof is below.

## Complexity

The cost is fixed in advance, as the design intends. The generation of the hypotheses costs $M\tau$ in units of one scoring. The scoring costs $\sum_i f(i)$ scorings, and for $f(i) = \lfloor M 2^{-\lfloor i/B \rfloor} \rfloor$ this is at most $BM(1 + \frac12 + \frac14 + \cdots) \le 2BM$. So the time is at most $M(\tau + 2B)$ scorings, plus the selections of line L6, which cost $O(M)$ in total with a linear-time selection, since $|H|$ halves each time. For $M = 500$, $B = 100$ and $N = 500$, the scorings are $99 \cdot 500 + 100 \cdot 250 + 100 \cdot 125 + 100 \cdot 62 + 100 \cdot 31 + 15 = 96315$. The extra space is $\Theta(M + N)$ for the hypotheses, their scores and the order of the observations. The front matter counts the code, which sorts instead of selecting.

## Properties

- **Fixed time.** The number of hypotheses and scorings is set by $M$, $B$ and $N$, not by the data.
- **Breadth-first.** All hypotheses are scored on the same first observations, so their scores are comparable at each cut.
- **No adaptive stopping.** Unlike RANSAC, the number of hypotheses does not adapt to the inlier ratio. If $M$ is too small for the outlier ratio, no hypothesis is correct and preemption cannot help.
- **Random observation order.** The order of line L1 makes each block a random subset of the data, so the partial score is an unbiased estimate of the mean score per observation.

## Variants and improvements

- **Other preemption functions.** Any non-increasing $f$ works; Nistér discusses the trade-off between depth-first and breadth-first schemes and implements a hybrid.
- **Sequential tests.** The test of Chum and Matas (2008), based on the [sequential probability ratio test](/sequential-probability-ratio-test/), stops the scoring of each hypothesis as soon as it is likely bad, depth-first, with a guarantee on the error of this decision.
- **Better hypotheses.** [PROSAC](/prosac/) sampling can feed the hypothesis set, and [LO-RANSAC](/lo-ransac/) can polish the winner.
- **Scores.** The truncated quadratic of [MSAC](/msac/) or a likelihood as in [MLESAC](/mlesac/) both fit the additive scoring of line L7.

## When to use it

Use preemptive RANSAC in real-time systems with a hard time budget, such as visual odometry from video, where a fair answer in time is better than the best answer late. Use it when the outlier ratio is known to be moderate, so that a fixed $M$ is enough. For offline estimation, where time can vary, plain RANSAC with adaptive stopping and [LO-RANSAC](/lo-ransac/) are more reliable.

## Pitfalls

- **$M$ too small.** With inlier ratio $w$ and minimal sample size $s$, the probability that no hypothesis is all-inlier is $(1 - w^s)^M$. Choose $M$ by the [iteration bound](/ransac-iteration-bound/) for the worst outlier ratio expected.
- **$B$ too small.** With few observations per block, a good hypothesis can lose a cut by bad luck, as in the example with the seed 3.
- **Correlated observation order.** If the observations are not shuffled, a block can come from one image region and favor a wrong model. Line L1 is required.
- **Unbounded scores.** A score with no ceiling lets one gross outlier decide a cut. Use a bounded score.

## Implementations

The Python code fits a line in the plane. The function `preemptive_ransac` takes an optional list of hypotheses, so the tests can fix them, and returns the number of scorings, which the tests compare with the formula. `total_scorings` gives the count $M + \sum_{i \ge 2} f(i)$ without running the algorithm.

## History

Nistér presented preemptive RANSAC at ICCV 2003, with a journal version in Machine Vision and Applications in 2005. It was the robust core of a system that estimated the motion of a calibrated camera from video in real time, with the five-point solver for the essential matrix and three-point pose for later frames. Later work on fast verification, such as the sequential test of Chum and Matas (2008) and the USAC framework of 2013, chose depth-first verification with early rejection instead.

## References
