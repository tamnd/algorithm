---
tag: 5JS7A5
kind: algorithm
slug: maximum-likelihood-parameter-generation
name: Maximum likelihood parameter generation
aliases:
- MLPG
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: "Turn per-frame Gaussian means and variances of static and delta features into the smooth static trajectory of highest likelihood, by one banded linear solve in O(T) time."
solves: [least-squares-problem]
model: real-ram
complexity:
  vars: {T: the number of frames, D: the number of windows, b: "the half-bandwidth, twice the largest window offset"}
  time: {worst: "O(T D b^2)"}
  space: {extra: "Θ(T b)"}
properties: {deterministic: true, exact: true, online: false, in_place: false}
history:
  year: 2000
  people: [Keiichi Tokuda, Takayoshi Yoshimura, Takashi Masuko, Takao Kobayashi, Tadashi Kitamura]
  note: Tokuda and colleagues gave the closed form for a given state sequence and algorithms for hidden state and mixture sequences, as the generation step of HMM-based speech synthesis.
prereqs: [delta-features, weighted-least-squares, cholesky-decomposition]
see_also: [hmm-based-speech-synthesis, banded-matrix, generalized-least-squares, gaussian-elimination, smoothing-spline, rauch-tung-striebel-smoother, hidden-semi-markov-model, unit-selection-synthesis]
sources:
  - paper: doi:10.1109/ICASSP.2000.861820
    title: Keiichi Tokuda, Takayoshi Yoshimura, Takashi Masuko, Takao Kobayashi and Tadashi Kitamura, Speech parameter generation algorithms for HMM-based speech synthesis, ICASSP 2000, volume 3, pages 1315 to 1318
    locator: the solution for a given state sequence and the algorithms for a hidden state and mixture sequence
  - paper: doi:10.1016/j.specom.2009.04.004
    title: Heiga Zen, Keiichi Tokuda and Alan W. Black, Statistical parametric speech synthesis, Speech Communication 51(11), 2009, pages 1039 to 1064
    locator: the description of parameter generation with dynamic features and the discussion of over-smoothing
  - book: isbn:9780521899277
    title: Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009
    locator: the chapter Hidden Markov model synthesis
---

Maximum likelihood parameter generation (MLPG) is the step of [HMM-based speech synthesis](/hmm-based-speech-synthesis/) that turns a sequence of Gaussian distributions into a smooth trajectory of speech parameters. The model gives, for each frame, a mean and a variance for each static feature and for its [delta features](/delta-features/), the slope and the curvature over time. The most likely value of each frame alone would be the static mean, a step function that jumps at each state boundary. MLPG instead asks for the static trajectory whose static and delta values together have the highest likelihood. This is a [weighted least squares](/weighted-least-squares/) problem, and its normal equations have a banded matrix, so a banded [Cholesky](/cholesky-decomposition/) solve gives the exact answer in time linear in the number of frames. Tokuda and colleagues gave the method in 2000.

## In plain words

A statistical voice predicts each short frame of speech from the sound being spoken. For each frame it gives a best value and how sure it is. It also gives a best value for how fast the parameter should change at that frame, and how fast that change should change.

If you just take the best value of each frame, the result jumps at every sound boundary and sounds buzzy. MLPG looks at all the frames together. It finds the one smooth curve that best fits both the values and the predicted rates of change, with each target weighted by how sure the model is. Where the model is sure about the value, the curve stays close to it. Where it is sure that the value changes slowly, the curve smooths over the boundary. The best curve comes from one system of linear equations, solved quickly.

## The problem

Work with one feature dimension; with a diagonal covariance, the dimensions are solved one at a time. The unknown is the static trajectory $c = (c_0, \ldots, c_{T-1})$. A window $w^{(d)}$ is a map from offsets $\tau$ to coefficients, and the $d$-th feature at frame $t$ is

$$o_{t,d} = \sum_\tau w^{(d)}_\tau\, c_{t+\tau}.$$

The usual windows are static $\{0: 1\}$, delta $\{-1: -\tfrac12,\ 1: \tfrac12\}$ and delta-delta $\{-1: 1,\ 0: -2,\ 1: 1\}$. Stack the $o_{t,d}$ into $o = Wc$, where $W$ is a $DT \times T$ matrix. A frame $t + \tau$ outside $0 \ldots T-1$ must be given a rule. The code uses the nearest end frame by default (the trajectory is held constant beyond its ends) and offers the rule that drops the term (the trajectory is 0 beyond its ends).

The model gives a mean $\mu_{t,d}$ and a variance $\sigma^2_{t,d} > 0$ for each frame and window, usually by repeating the parameters of each HMM state for its duration. With $U = \mathrm{diag}(\sigma^2_{t,d})$, find

$$c^* = \arg\max_c \log \mathcal{N}(Wc;\ \mu,\ U) = \arg\min_c\ (Wc - \mu)^\top U^{-1} (Wc - \mu).$$

Setting the gradient to zero gives the normal equations

$$P c = r, \qquad P = W^\top U^{-1} W, \qquad r = W^\top U^{-1} \mu.$$

## The algorithm

Let $L$ be the largest $|\tau|$ of any window. Then $P$ is symmetric with half-bandwidth $b = 2L$: entry $(u, v)$ is 0 when $|u - v| > b$. MLPG builds $P$ and $r$ row by row of $W$ and solves with a banded $LDL^\top$ factorization, the form of Cholesky without square roots.

```pseudo id=main
MLPG(μ, σ², w^(0) .. w^(D-1))          ▷ μ and σ² are T × D, w^(0) is the static window
L1  P ← 0 (symmetric, half-bandwidth b = 2L); r ← 0
L2  for t ← 0 to T - 1 and d ← 0 to D - 1 do          ▷ row (t, d) of W
L3      for each entry (u, a) of row (t, d) do
L4          for each entry (v, a') of row (t, d) with v ≤ u do P[u][v] ← P[u][v] + a a' / σ²[t][d]
L5          r[u] ← r[u] + a μ[t][d] / σ²[t][d]
L6  for j ← 0 to T - 1 do                                ▷ banded LDL^T
L7      D[j] ← P[j][j] - Σ over k from max(0, j - b) to j - 1 of L[j][k]² D[k]; stop with an error if D[j] ≤ 0
L8      for i ← j + 1 to min(T - 1, j + b) do L[i][j] ← (P[i][j] - Σ over k from max(0, i - b) to j - 1 of L[i][k] L[j][k] D[k]) / D[j]
L9  solve L y = r by forward substitution inside the band
L10 z[t] ← y[t] / D[t] for each t
L11 solve L^T c = z by back substitution inside the band
L12 return c
```

Lines L1 to L5 never form $W$: each row of $W$ has at most $2L + 1$ entries, and line L4 adds their pairwise products to $P$. Lines L6 to L8 are the dense $LDL^\top$ formulas with every sum cut to the band. The factorization makes no fill outside the band, so the cut loses nothing. The method uses only addition, subtraction, multiplication and division, so the code runs on `Fraction` for exact checks and on `float` for speed.

## Example

Take two HMM states of 3 frames each, so $T = 6$, with static means 0 and 1, static variance 1, delta mean 0 and delta variance $1/4$ in both states, and the static and delta windows with the end frames held. So $\mu$ static is $(0, 0, 0, 1, 1, 1)$. Then $P$ and $r$ are

$$P = \begin{pmatrix} 3 & -1 & -1 & 0 & 0 & 0 \\ -1 & 3 & 0 & -1 & 0 & 0 \\ -1 & 0 & 3 & 0 & -1 & 0 \\ 0 & -1 & 0 & 3 & 0 & -1 \\ 0 & 0 & -1 & 0 & 3 & -1 \\ 0 & 0 & 0 & -1 & -1 & 3 \end{pmatrix}, \qquad r = (0, 0, 0, 1, 1, 1),$$

with half-bandwidth 2. The diagonal 3 is $1$ from the static row plus $2 \cdot (1/2)^2 / (1/4)$ from the two delta rows that touch the frame. The solution is

$$c^* = (0.2,\ 0.3,\ 0.3,\ 0.7,\ 0.7,\ 0.8),$$

with deltas $(0.05, 0.05, 0.2, 0.2, 0.05, 0.05)$. The trajectory rises across the boundary instead of jumping. The objective $-\tfrac12 (Wc - \mu)^\top U^{-1} (Wc - \mu)$ is $-0.4$ at $c^*$ and $-1$ at the step $c = (0, 0, 0, 1, 1, 1)$, whose deltas $0.5$ at frames 2 and 3 are far from their mean 0.

Adding the delta-delta window with mean 0 and variance $1/4$ gives $c^* = (0.2352, 0.2951, 0.4163, 0.5837, 0.7049, 0.7648)$, rounded to 4 places, a smoother S-shaped curve. The pairs of equal values in the first result come from the central delta window, which links frame $t$ only to frames $t \pm 1$ through a difference over two frames; see the pitfalls.

## Correctness

The proofs file shows four facts. With a static window, $x^\top P x \ge \sum_t x_t^2 / \sigma^2_{t,0} > 0$ for $x \ne 0$, so $P$ is positive definite. Writing $c = c^* + x$ gives $\ell(c) = \ell(c^*) - \tfrac12 x^\top P x$, so $c^* = P^{-1} r$ is the unique maximizer. Each row of $W$ touches columns within $L$ of its frame under both end rules, so $P$ has half-bandwidth $2L$. An induction over the columns shows that $L$ stays inside the same band, so the banded formulas equal the dense ones, and Sylvester's criterion gives positive pivots. The tests compare the result in `Fraction` with dense Gaussian elimination on $W^\top U^{-1} W$ for many random cases, and check that the gradient is exactly 0 and that random moves lower the objective.

## Complexity

Lines L2 to L5 cost $O(T \sum_d s_d^2)$, where $s_d \le 2L + 1$ is the number of taps of window $d$. The factorization costs $O(T b^2)$ and the two solves cost $O(T b)$. The band of $P$ and $L$ takes $\Theta(T b)$ space. With the usual windows $L = 1$ and $b = 2$, so the whole computation is $\Theta(T)$, against $\Theta(T^3)$ for a dense solve. A sentence of a few hundred frames and a few dozen feature dimensions is a few hundred thousand operations.

## Properties

- **Exact.** It returns the true maximizer of the Gaussian likelihood for the given state sequence and durations, not an approximation.
- **Linear in the means.** $c^*$ is a fixed linear function $P^{-1} W^\top U^{-1}$ of $\mu$, so it is a smoother, close in spirit to a [smoothing spline](/smoothing-spline/), with the variances as local weights.
- **Variances matter.** Unlike the frame-wise maximum, which ignores the variances, MLPG trades the static and delta targets by their precisions. A small delta variance gives a flatter curve.
- **Not online.** The answer at a frame depends on all frames. The [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) solves the same kind of banded system in a forward and a backward pass. A system with low latency must solve over a sliding block of frames instead.
- **Over-smoothing.** The generated trajectories have less variance over time than natural speech, a measured effect that makes the voice sound muffled (Zen, Tokuda and Black 2009).

## Variants and improvements

- **Hidden state sequence.** Tokuda and colleagues also treat the case where the state and mixture sequence is not fixed, maximizing over it with an EM-type iteration. Most systems instead fix the states and durations from a duration model and use the closed form.
- **Global variance.** Toda and Tokuda (2007) add a term for the likelihood of the variance of the whole trajectory, which counters over-smoothing; the objective is no longer quadratic and is maximized iteratively.
- **Trajectory HMM.** Training with the same constraint $o = Wc$ gives the trajectory HMM of Zen, Tokuda and Kitamura (2007), so training and generation agree.
- **Neural acoustic models.** Deep network and recurrent acoustic models often predict static and delta means and variances and still run MLPG at the end, or predict a smooth trajectory directly.
- **Full covariance.** With a covariance between dimensions, the system couples all dimensions and the band holds blocks instead of numbers.

## When to use it

Use MLPG whenever a model gives per-frame Gaussians over static and dynamic features and a single smooth trajectory is needed: the spectral, F0 and aperiodicity streams of an HMM-based or DNN-based parametric synthesizer, voice conversion with Gaussian mixture models, and articulatory or motion synthesis. If the model already outputs a trajectory, as end-to-end neural synthesizers such as [Tacotron](/tacotron/) do, there is nothing for MLPG to do.

## Pitfalls

- **The edges.** The windows reach past the first and last frames. Holding the end frames and dropping the terms are different models; dropping them makes the delta-delta window pull the end frames toward 0. Use the same rule as the one used to compute the deltas in training.
- **Central delta and odd-even split.** With the delta window $\tfrac12 (c_{t+1} - c_{t-1})$ alone, $P$ links each frame only to frames two apart, except at the ends, so the even and odd frames are nearly separate problems and the curve can show pairs or a zigzag. Add the delta-delta window, which links neighbors.
- **No static window.** Without a static window, a constant shift does not change any delta, so $P$ is singular. The code stops with an error.
- **A dense solve.** Forming the dense $T \times T$ matrix and inverting it costs $\Theta(T^3)$ time and $\Theta(T^2)$ space; keep the band.
- **Unvoiced frames.** F0 is undefined in unvoiced regions. Generate F0 only over the voiced segments, which is what the multi-space distribution of HMM-based synthesis supports.

## Implementations

## History

Tokuda, Kobayashi and Imai described parameter generation from HMMs with dynamic features in 1995. The 2000 ICASSP paper by Tokuda, Yoshimura, Masuko, Kobayashi and Kitamura gave the algorithms in the form used afterwards: the closed form for a given state sequence and iterative algorithms for a hidden state and mixture sequence. With the HMM-based synthesizer of Yoshimura and colleagues (1999), it became the generation step of the HTS system and of most statistical parametric synthesizers of the 2000s. Toda and Tokuda added the global variance in 2007 to reduce over-smoothing, and neural acoustic models kept the step in the early 2010s before end-to-end models made it unneeded.

## References
