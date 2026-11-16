---
tag: BQXMXZ
kind: algorithm
slug: lo-ransac
name: LO-RANSAC
aliases:
- locally optimized RANSAC
area: computer-vision/multiple-view-geometry
level: advanced
summary: "RANSAC that, each time a sample gives a new best model, refines it by least squares fits on its inliers, so the number of samples comes close to the count the formula predicts."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap"}
  time: {worst: Θ(k n), average: Θ(k n), best: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Ondrej Chum, Jiri Matas, Josef Kittler]
  note: "Chum, Matas and Kittler introduced LO-RANSAC at DAGM 2003; Lebeda, Matas and Chum revised the local step in 2012 (LO+)."
prereqs: [ransac, ordinary-least-squares]
see_also: [ransac-iteration-bound, msac, magsac, prosac, iteratively-reweighted-least-squares, robust-model-fitting]
sources:
  - paper: doi:10.1007/978-3-540-45243-0_31
    title: "Ondrej Chum, Jiri Matas and Josef Kittler, Locally optimized RANSAC, Pattern Recognition, DAGM 2003, Lecture Notes in Computer Science 2781, 236-243"
    locator: "The observation that the number of samples is higher than predicted, and the local optimization step applied to each new best model"
  - paper: doi:10.5244/C.26.95
    title: "Karel Lebeda, Jiri Matas and Ondrej Chum, Fixing the locally optimized RANSAC, British Machine Vision Conference 2012"
    locator: "Algorithm 1 (when the local optimization runs), Algorithm 2 (the inner RANSAC on non-minimal samples), Algorithm 3 (iterated least squares with a shrinking threshold), Table 1 (parameter values) and the bound on the running time"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "Local optimization as one stage of the framework"
---

LO-RANSAC (locally optimized RANSAC) is a variant of [RANSAC](/ransac/) that adds a refinement step inside the loop. Each time a model from a minimal sample has more inliers than any earlier one, LO-RANSAC fits new models to the inliers of that model by least squares and keeps the best of them. The reason is noise: a model from a minimal sample of inliers is often tilted by the noise of its few items, so it misses many inliers and RANSAC must keep sampling until a lucky sample gives a better one. A least squares fit to many inliers averages the noise away. The step runs rarely, about $\ln k$ times in $k$ samples, so it adds little to the total time, and the number of samples comes close to the count of the [iteration bound](/ransac-iteration-bound/). Chum, Matas and Kittler introduced it in 2003, and Lebeda, Matas and Chum gave the current form of the step in 2012.

## In plain words

RANSAC guesses a line from two dots and counts the dots close to it. Even if both dots are good, they have small errors, and the line through them can tilt. A tilted line passes far from the good dots at the ends, so the count is too low. RANSAC then needs many more guesses before two dots happen to give a straight enough line.

LO-RANSAC fixes this. When a guess beats all earlier guesses, it does not stop there. It takes the dots that agree with the guess and fits a line through all of them at once, which averages out the small errors. It does this a few times, with a slightly wider band of agreement at first and a narrower one later. The improved line usually agrees with more dots, so the search can stop earlier.

## The problem

The input is as for [RANSAC](/ransac/): data $D = \{x_1, \ldots, x_n\}$, a minimal solver for samples of $s$ items, a residual $r(\theta, x)$, a threshold $\varepsilon$, a confidence $p$ and a cap $k_{\max}$. LO-RANSAC also needs a least squares solver that fits a model to any number of items, and four parameters of the local step: a factor $m_\theta > 1$ for a wider threshold, a number of repetitions, a number of inner iterations and a size $s_{\text{is}}$ of the non-minimal samples. The goal is a model with a large consensus set $I(\theta) = \{x : r(\theta, x) \le \varepsilon\}$.

## The algorithm

```pseudo id=main
LO-RANSAC(D, s, ε, p, k_max)                 ▷ n = |D|
L1  θ* ← none, I* ← ∅, n_s ← 0, k ← k_max, t ← 0
L2  while t < k do
L3      t ← t + 1
L4      S ← s distinct items of D, drawn uniformly at random
L5      θ ← FIT-MINIMAL(S)                    ▷ none for a degenerate sample
L6      if θ is none then continue
L7      I ← I(θ)
L8      if |I| > n_s then                     ▷ best minimal-sample model so far
L9          n_s ← |I|
L10         (θ_L, I_L) ← LOCAL-OPT(θ, I)
L11         if |I_L| > |I*| then
L12             θ* ← θ_L, I* ← I_L
L13             k ← min(k_max, ⌈log(1 − p) / log(1 − (|I*|/n)^s)⌉)
L14 if θ* is none then return failure
L15 return θ*, I*

LOCAL-OPT(θ, I)                              ▷ keeps the model with most inliers at ε
L16 best ← (θ, I)
L17 try FIT-LSQ({x : r(θ, x) ≤ m_θ ε})
L18 repeat reps times
L19     S ← min(s_is, ⌊|I|/2⌋) items of I, drawn at random (at least s)
L20     θ' ← FIT-LSQ(S)
L21     θ' ← FIT-LSQ(I(θ')), ε' ← m_θ ε
L22     repeat iters times
L23         try θ'
L24         θ' ← FIT-LSQ({x : r(θ', x) ≤ ε'})
L25         ε' ← ε' − (m_θ ε − ε)/(iters − 1)
L26 return best, after a last try of θ'
```

Here "try $\theta'$" means: compute $I(\theta')$ and replace best if it has more inliers. Lines L8 and L9 follow Algorithm 1 of Lebeda, Matas and Chum: the local step runs when a minimal-sample model beats every earlier minimal-sample model, not every model found by the local step. Lines L18 to L25 follow their Algorithms 2 and 3: an inner RANSAC on non-minimal samples drawn from the inliers, each followed by iterated least squares while the threshold shrinks from $m_\theta \varepsilon$ to $\varepsilon$. Their Table 1 gives $m_\theta = \sqrt 2$, 10 repetitions, 4 iterations and $s_{\text{is}} = 12$ for homographies and 14 for epipolar geometry; the code uses the same values except $s_{\text{is}} = 8$ for a line. Their Algorithm 3 also weights the items; the code uses unit weights.

## Example

Take 14 points: the 10 inliers $(x, y_x)$ for $x = 0, 1, \ldots, 9$ with $y = 0.05, -0.05, 0.04, -0.03, 0, 0.05, -0.05, 0.02, -0.04, 0.03$, which lie near $y = 0$, and the 4 outliers $(2,3), (5,-2), (7,4), (8,-3)$. Use $\varepsilon = 0.08$, $p = 0.99$ and $m_\theta = \sqrt 2$, so the wide threshold is about 0.113.

The sample $(3, -0.03), (4, 0)$ gives the line $y = 0.03x - 0.12$, which tilts across the band. Its inliers at $\varepsilon$ are the 5 points with $x = 1, 3, 4, 5, 7$, so plain RANSAC would set $k = \lceil \log 0.01 / \log(1 - (5/14)^2) \rceil = 34$.

LO-RANSAC runs the local step. Line L17 takes the 7 points within 0.113 of the line, $x = 1, \ldots, 7$, and fits them by least squares. The new line is about $y = 0.0039x - 0.019$, and all 10 inliers are within 0.08 of it. The best model now has 10 inliers, and line L13 sets $k = \lceil \log 0.01 / \log(1 - (10/14)^2) \rceil = 7$.

Plain RANSAC would need a sample whose line has all 10 inliers. Only 4 of the 91 pairs of points give such a line, the pairs $x = \{4, 7\}, \{4, 8\}, \{4, 9\}, \{7, 9\}$, so its count of samples stays high much longer. With the seed 1, the code stops after 7 samples with all 10 inliers and 2 runs of the local step.

## Correctness

The loop of LO-RANSAC keeps an invariant at line L2: $I^*$ has the most inliers among all models evaluated so far, both the models of the samples and the models of the local steps, and $n_s$ is the largest consensus size of a minimal-sample model so far. The local step returns a model with at least as many inliers as its input, because it starts from the input and replaces it only by a model with more inliers; so $|I^*| \ge n_s$. The loop ends after at most $k_{\max}$ rounds, since $k \le k_{\max}$ and $t$ grows by 1. The guarantee of RANSAC carries over: the local step only increases $|I^*|$, so any sample that would make RANSAC succeed also makes LO-RANSAC succeed, and the stopping rule still uses the inlier ratio of a model that was evaluated. That the local step brings the number of samples close to the formula is a benchmark result of Chum, Matas and Kittler, not a theorem. The proof is below.

## Complexity

One round of the loop costs $\Theta(n)$ in the [real RAM](/real-ram/), as in RANSAC. One local step costs a fixed number of least squares fits and inlier counts, about $\text{reps} \cdot (\text{iters} + 2)$ of them, so $\Theta(n)$ for fixed parameters and a model type of fixed size. The local step runs once per strict record of the minimal-sample consensus sizes. If the sizes in $k$ rounds were independent with a continuous distribution, the expected number of records would be the harmonic number $H_k \approx \ln k$; with integer sizes, which can tie, the number of strict records is at most that in expectation. Lebeda, Matas and Chum write the total time as $C_R k + C_{LO} \lceil \log k \rceil$, with $C_R$ the cost of a round and $C_{LO}$ the cost of a local step. So the total time is $\Theta(k n)$, and the local steps add about $\ln k$ times a constant factor of $n$. Because $|I^*|$ is larger, $k$ is smaller than for RANSAC on noisy data.

For large inlier sets, the least squares fits of the local step can dominate. Lebeda, Matas and Chum limit the number of inliers used in these fits to 7 times the minimal sample size, drawn at random.

## Properties

- **Never worse than RANSAC on the same samples.** For the same sequence of minimal samples, $|I^*|$ of LO-RANSAC is at least that of RANSAC at every round, so its $k$ is no larger and it stops no later (a theorem; see the proof).
- **Few local steps.** About $\ln k$ in $k$ rounds under the assumption above.
- **Better final model.** The returned model is already a least squares fit, not a minimal-sample model, so no separate final refit is needed.
- **Model-independent.** The step needs only a least squares solver for the model, which most minimal problems have, for example the [eight-point algorithm](/eight-point-algorithm/) or the DLT for a [homography](/dlt-homography/).

## Variants and improvements

- **LO+.** Lebeda, Matas and Chum (2012) score the models of the local step with the truncated quadratic cost of [MSAC](/msac/).
- **Graph-cut RANSAC** (Barath and Matas, 2018) replaces the local step by an energy minimization that also uses the spatial coherence of the inliers.
- **[MAGSAC++](/magsac/)** uses an [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) step with weights marginalized over the noise scale, a local optimization without a fixed threshold.
- **USAC** (Raguram et al., 2013) includes local optimization as one stage, together with [PROSAC](/prosac/) sampling and early rejection of bad models.

## When to use it

Use LO-RANSAC whenever the inliers are noisy and a least squares solver exists. The gain is largest for models with a larger minimal sample, such as the fundamental matrix from 7 or 8 matches, where a minimal sample of noisy inliers often gives a poor model. For exact data, as in the tests of this page with no noise, the local step changes nothing, and plain RANSAC is enough.

## Pitfalls

- **A local step that fits outliers.** The wider threshold $m_\theta \varepsilon$ can include outliers near the model. The shrinking threshold of lines L22 to L25 removes them again; do not fit only at the wide threshold.
- **Degenerate inlier sets.** If all inliers are on a degenerate configuration, for example all matches on one plane for a fundamental matrix, the local step makes the wrong model more convincing. Check degeneracy before the local step.
- **Cost on large inlier sets.** Limit the number of items in each least squares fit, as Lebeda, Matas and Chum do.

## Implementations

The Python code fits a line in the plane with $s = 2$. The function `local_opt` is the local step and can be tested alone. `lo_ransac` returns the number of local steps that ran, so the tests can check that it stays at most the number of rounds.

## History

Chum, Matas and Kittler presented LO-RANSAC at the DAGM symposium in 2003. They observed that the number of samples RANSAC needs in practice is higher than the formula predicts, because a minimal sample of inliers does not always give a model with all inliers, and that a local optimization of each new best model closes the gap. Lebeda, Matas and Chum revisited the method in 2012 under the title "Fixing the locally optimized RANSAC". They gave the inner RANSAC with iterated least squares, the limit on the number of inliers in each fit and the truncated quadratic cost. Local optimization became a standard stage of USAC (2013) and of later methods such as Graph-cut RANSAC and [MAGSAC++](/magsac/).

## References
