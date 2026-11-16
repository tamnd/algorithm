---
tag: D1ZTNC
kind: theorem
slug: ransac-iteration-bound
name: RANSAC iteration bound
aliases:
- RANSAC stopping criterion
area: computer-vision/multiple-view-geometry
level: core
summary: "If a sample of s items is all inliers with probability w^s, independently, then ceil(log(1-p)/log(1-w^s)) samples give one with probability at least p. With noise the count is optimistic."
prereqs: [ransac, geometric-distribution]
see_also: [ransac, robust-model-fitting, lo-ransac, prosac, msac, minimal-solver, five-point-algorithm, randomized-algorithm]
sources:
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "The discussion of the RANSAC parameters: the expected number of trials w^(-n) and its standard deviation, and the number of trials for a given probability of success"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.7, Robust estimation (the number of samples N = log(1 - p)/log(1 - (1 - e)^s), its table for sample sizes and outlier proportions, and the adaptive algorithm that updates N)"
  - paper: doi:10.1007/978-3-540-45243-0_31
    title: "Ondrej Chum, Jiri Matas and Josef Kittler, Locally optimized RANSAC, Pattern Recognition, DAGM 2003, Lecture Notes in Computer Science 2781, 236-243"
    locator: "The observation that the number of samples in practice is larger than the count the formula predicts, because not every all-inlier sample gives a good model"
---

The RANSAC iteration bound gives the number of random samples that [RANSAC](/ransac/) must draw so that, with a chosen probability $p$, at least one sample contains only inliers. If a fraction $w$ of the data are inliers and a sample has $s$ items, a sample is all inliers with probability about $w^s$, and $k = \lceil \log(1 - p)/\log(1 - w^s) \rceil$ samples are enough. For $p = 0.99$, $w = 0.5$ and $s = 4$, this is 72 samples. The count grows like $w^{-s}$, so it grows exponentially in the size of the sample, which is why small [minimal solvers](/minimal-solver/) matter. The bound is the stopping rule of RANSAC and of most of its variants. It assumes that the samples are independent and that every all-inlier sample gives a good model. Noise makes the second assumption false, so in practice the count is optimistic.

## Statement

Let one random sample be "good" with probability $q \in (0, 1)$, and let the samples be independent.

**Theorem.** The probability that at least one of $k$ samples is good is $1 - (1 - q)^k$. For $0 < p < 1$, this is at least $p$ if and only if

$$k \ge \frac{\log(1 - p)}{\log(1 - q)},$$

so the least such integer is $k^*(p, q) = \lceil \log(1 - p)/\log(1 - q) \rceil$. The number $K$ of samples up to and including the first good one has the geometric distribution $\Pr[K = k] = (1 - q)^{k-1} q$, with mean $1/q$ and standard deviation $\sqrt{1 - q}/q$.

**Corollary (RANSAC).** Let $D$ have $n$ items, of which $|I| = w n$ are inliers, and let a good sample be a sample of $s$ items that are all inliers. If the $s$ items are drawn independently and uniformly with replacement, then $q = w^s$ and $k^* = \lceil \log(1 - p)/\log(1 - w^s) \rceil$. If the $s$ items of a sample are distinct, as in RANSAC, then $q = \binom{wn}{s} / \binom{n}{s} \le w^s$, and the count with $q = w^s$ is a lower bound on the count needed.

## In plain words

Each sample is like the throw of a loaded coin that shows "good" with a small chance. To be almost sure of at least one good throw, you need enough throws that the chance of all bad throws is small. The chance of all bad throws drops by the same factor at every throw, so the number of throws you need grows only with the logarithm of how sure you want to be. It grows much faster when a good throw is rare: halving the share of good data items multiplies the work by two for each item in a sample.

## Proof

The samples are independent, and each is bad with probability $1 - q$, so all $k$ samples are bad with probability $(1 - q)^k$. At least one is good with probability $1 - (1 - q)^k$. This is at least $p$ if and only if $(1 - q)^k \le 1 - p$. Both sides are positive, and $\log$ is increasing, so this holds if and only if $k \log(1 - q) \le \log(1 - p)$. Since $0 < q < 1$, $\log(1 - q) < 0$, and dividing by it reverses the inequality: $k \ge \log(1 - p)/\log(1 - q)$. The least integer $k$ with this property is the ceiling.

For the distribution of $K$: $K = k$ exactly when the first $k - 1$ samples are bad and sample $k$ is good, which has probability $(1 - q)^{k-1} q$. This is the [geometric distribution](/geometric-distribution/) with success probability $q$, with mean $\sum_{k \ge 1} k (1 - q)^{k-1} q = 1/q$ and variance $(1 - q)/q^2$.

For the corollary, with replacement each of the $s$ draws is an inlier with probability $w$, independently, so $q = w^s$. Without replacement, a uniform $s$-subset of $D$ lies inside $I$ with probability $\binom{wn}{s}/\binom{n}{s} = \prod_{j=0}^{s-1} \frac{wn - j}{n - j}$. Each factor is at most $w$, because $wn - j \le w(n - j)$ is the same as $j \ge wj$, which holds for $w \le 1$. So $q \le w^s$. Since $k^*(p, q)$ does not increase as $q$ grows, the count with $q = w^s$ is at most the count for the true $q$. $\square$

## Consequences

The table gives $k^*$ for $p = 0.99$ and $w = 0.5$:

| sample size $s$ | 2 | 3 | 4 | 5 | 7 | 8 |
|---|---|---|---|---|---|---|
| $k^*$ | 17 | 35 | 72 | 146 | 588 | 1177 |

With $w = 0.8$ and $s = 4$, $k^* = 9$. With $p = 0.95$, $w = 0.5$ and $s = 2$, $k^* = 11$.

- **Small samples.** For $w = 0.5$, the [five-point algorithm](/five-point-algorithm/) for the essential matrix needs 146 samples, but the [eight-point algorithm](/eight-point-algorithm/) needs 1177. This is the main reason to use minimal solvers inside RANSAC.
- **Logarithm in the confidence.** For small $q$, $\log(1 - q) \approx -q$, so $k^* \approx \ln\big(1/(1 - p)\big)/q$. Going from $p = 0.99$ to $p = 0.9999$ only doubles the count.
- **Adaptive stopping.** The true $w$ is not known. RANSAC uses the inlier ratio of the best model so far. If that model's inliers are true inliers, this ratio is at most $w$, and the count it gives is at least $k^*$, so the rule stops late, not early.
- **Spread.** For $w = 0.5$ and $s = 4$, the mean number of samples to the first good one is $16$ and the standard deviation is $\sqrt{15/16} \cdot 16 \approx 15.5$. The standard deviation is close to the mean, so a run can take several times the mean. This is why the stopping rule uses a confidence $p$ and not the mean.
- **Without replacement.** For small $n$ the bound with $w^s$ is optimistic. With $n = 20$, $|I| = 10$ and $s = 4$, the true probability is $q = 210/4845 \approx 0.0433$, not $0.0625$, and $k^* = 104$, not 72. With 72 samples the probability of success is about $0.959$, not $0.99$.

## Tightness

The bound on $k$ is exact for its model: $1 - (1 - q)^k$ is the probability of success, not a lower bound, so no smaller $k$ gives probability $p$. For example, with $q = 0.25$ ($w = 0.5$ and $s = 2$), 16 samples succeed with probability $0.98998$, just below $0.99$, and 17 samples succeed with probability $0.99248$.

In practice the guarantee is weaker than the theorem, for three reasons.

- **Noise.** The theorem assumes that every all-inlier sample gives a model that finds the inliers. With noisy inliers, a minimal sample of nearby points can give a poor model that misses many inliers. Chum, Matas and Kittler (2003) observed that RANSAC therefore runs longer than the formula predicts, and they proposed [LO-RANSAC](/lo-ransac/) to close the gap.
- **Degenerate samples.** Some all-inlier samples, such as collinear points for a homography, give no model or a wrong one.
- **Dependence.** The samples of RANSAC are independent, but guided samplers such as [PROSAC](/prosac/) draw from a changing set, and the theorem does not apply to them as stated.

## History

Fischler and Bolles introduced RANSAC in 1981 in Communications of the ACM. They analyzed the number of trials needed to find a sample of inliers, gave its mean $w^{-s}$ and its standard deviation $\sqrt{1 - w^s}/w^s$, and the number of trials for a given probability of success. Hartley and Zisserman (2004) gave the formula with a table and the adaptive algorithm that updates the count from the best model so far, which is the form that most implementations use. Chum, Matas and Kittler (2003) showed that the count is optimistic with noise and used it as a target for [LO-RANSAC](/lo-ransac/). Later work, such as [PROSAC](/prosac/) and the USAC framework, kept the same kind of stopping rule with other sampling schemes.

## References
