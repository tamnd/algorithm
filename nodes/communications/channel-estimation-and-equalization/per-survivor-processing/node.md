---
tag: 24BB6C
kind: technique
slug: per-survivor-processing
name: Per-survivor processing
aliases:
- per-survivor estimation
area: communications/channel-estimation-and-equalization
level: advanced
summary: Runs a separate channel or phase estimator along each survivor path of the Viterbi algorithm, using its own tentative decisions.
prereqs: [viterbi-algorithm, maximum-likelihood-sequence-estimation, viterbi-equalizer, lms-algorithm]
see_also: [reduced-state-sequence-estimation, kalman-channel-tracking, rls-algorithm, decision-directed-carrier-recovery, adaptive-equalization, blind-equalization, channel-estimation, turbo-equalization]
sources:
  - paper: "Riccardo Raheli, Andreas Polydoros and Ching-Kae Tzou, Per-survivor processing: a general approach to MLSE in uncertain environments, IEEE Transactions on Communications 43(2/3/4), 1995, pages 354 to 364"
    locator: "the principle of per-survivor processing, with channel identification, phase tracking and reduced-state examples"
---

Per-survivor processing (PSP) is a way to run the [Viterbi algorithm](/viterbi-algorithm/) when some parameter of the channel is unknown or drifts: the taps of the channel, the carrier phase or the symbol timing. A conventional receiver has one estimator, driven by the tentative decisions of the detector. Those decisions are reliable only after a delay, when the survivors have merged, so the estimator works with old data. PSP gives each survivor its own estimator and drives it with the symbols of that survivor, at once. The branch metrics of a survivor use its own estimate. The best path then comes with the estimate that fits it best. Raheli, Polydoros and Tzou gave the general principle in 1995.

## In plain words

The Viterbi algorithm keeps one best path into each state. Each of these paths is a hypothesis about the symbols sent so far. If the path is right, the symbols on it are known, and the channel can be estimated as if from a training sequence. So every path gets its own estimator, trained on its own symbols. Wrong paths get poor estimates and soon fall behind. The right path gets a good estimate with no delay. The cost is one estimator per state instead of one in total.

## When it applies

- The detector is a search over a trellis or a tree: a [Viterbi equalizer](/viterbi-equalizer/), a [maximum likelihood sequence estimator](/maximum-likelihood-sequence-estimation/), a trellis decoder or [reduced-state sequence estimation](/reduced-state-sequence-estimation/).
- The branch metrics depend on a parameter that is unknown or changes with time, and a data-aided estimator for that parameter exists: [LMS](/lms-algorithm/), [RLS](/rls-algorithm/), a [Kalman filter](/kalman-channel-tracking/) or a phase-locked loop.
- The parameter changes too fast for an estimator that waits for the decision delay of the detector, or no training sequence is available.

## The template

1. **Attach an estimate to each state.** Next to the metric and the back pointer, each state holds the parameter estimate of its survivor.
2. **Score branches with the estimate of their start state.** A branch from the state $s$ with the new symbol $a$ gets the metric $\lvert y_n - \hat f(s)^{\top} \mathbf{x} \rvert^2$, where $\mathbf{x} = (a, s)$ holds the symbols of that branch.
3. **Add, compare and select as usual.** Each next state keeps its best incoming branch.
4. **Update along the winner.** The estimate of the next state is the estimate of the winning start state, updated by one step of the estimator with the error and the symbols of the winning branch.

For a channel with $L$ taps and LMS with the step size $\beta$, the receiver is:

```pseudo id=main
PSP-VITERBI(y, f0, β, pre)
L1  Γ(start) ← 0, f̂(start) ← f0                      ▷ start = the known symbols pre
L2  for n ← 0 to N - 1
L3      for each reached state s and each symbol a
L4          e ← y[n] - f̂(s)ᵀ (a, s)                    ▷ the prediction error with the estimate of s
L5          keep for t = first L-1 entries of (a, s) the branch with the smallest Γ(s) + e²
L6      for each next state t: f̂(t) ← f̂(s) + β e (a, s)  ▷ s, a, e of the winning branch
L7  trace back from the state with the smallest Γ
```

**Correctness.** By induction on $n$, the estimate of each state is the LMS estimate run on the symbols of its own survivor, so it never uses a decision from another path, and it uses the newest symbol without a delay. With $\beta = 0$, every estimate stays $f_0$, and the receiver is exactly the Viterbi equalizer for $f_0$, which returns the maximum likelihood sequence. With $\beta > 0$ it is not the maximum likelihood detector for an unknown channel, but a search in which every path is scored by the prediction errors of its own adaptive estimate. The proofs folder has the details.

**Cost.** With $M$ symbols and $M^{L-1}$ states, each step evaluates $M^L$ branches and updates $M^{L-1}$ estimates, each at $O(L)$. A block of $N$ samples costs $O(N L M^L)$ time in the [word RAM](/word-ram/) with unit-cost real arithmetic, the same order as the Viterbi equalizer, and $O(N M^{L-1})$ space for the back pointers. A conventional receiver has one estimator instead of $M^{L-1}$, which matters when the estimator is expensive, such as RLS with $O(L^2)$ per update.

## Classic examples

**A drifting channel.** BPSK on the channel with the taps $f_{n,k} = b_k + 0.4 \sin(2\pi n/500 + k)$, $b = (1, 0.5, 0.3)$, noise variance 0.05 and 3000 symbols (seed 8001). The tests count the errors:

| receiver | errors in 3000 | agreement with the known-channel Viterbi |
|---|---|---|
| Viterbi that knows $f_n$ at every time | 1 | |
| Viterbi with the fixed estimate $f_0$ | 297 | |
| PSP with LMS, $\beta = 0.05$ | 0 | 2999 of 3000 |

With $\beta = 0.01$ and $0.02$, PSP made 70 and 23 errors on the same data, because the estimates lag behind the drift.

**Learning the channel from a wrong start.** On the fixed channel $(1, 0.5, 0.3)$ with noise variance 0.05 and 1000 symbols (seed 8003), the Viterbi equalizer for the wrong channel $(1, 0, 0)$ makes 44 errors. PSP from the same wrong start with $\beta = 0.02$ makes no errors, and its final estimate of the best survivor is $(1.010, 0.533, 0.311)$.

**Carrier phase.** For a channel $y_n = e^{j\theta_n} (f^{\top} \mathbf{x}_n) + w_n$ with an unknown, slowly drifting phase, each survivor runs its own phase-locked loop, driven by the phase error between $y_n$ and the noiseless output of its branch. This is [decision-directed carrier recovery](/decision-directed-carrier-recovery/) with the decisions of each survivor, and it avoids the delay that a single loop driven by the detector output would have.

**Decision feedback in reduced-state detectors.** In [reduced-state sequence estimation](/reduced-state-sequence-estimation/) and delayed decision feedback sequence estimation, the trellis keeps only part of the channel memory, and each survivor cancels the rest with its own past symbols. This is per-survivor processing applied to the symbols that the state does not hold.

## Variations

- **The estimator.** LMS is the cheapest. RLS and the [Kalman filter](/kalman-channel-tracking/) track faster channels at $O(L^2)$ per survivor and step.
- **Fewer estimators.** Keep estimators only for the best few survivors, or share one estimator among the states that differ only in old symbols, to cut the cost.
- **Blind start.** With no training, PSP can start from a rough estimate and let the survivors learn the channel, as in the second example. The sign of the channel is ambiguous for BPSK, so a known start or differential coding is still needed.
- **Tree and list searches.** The same idea works in the M-algorithm and in other breadth-first searches, where each kept path carries its estimate.
- **Soft output.** In iterative receivers, the per-survivor estimates can feed soft-output detectors, as in [turbo equalization](/turbo-equalization/).

## Pitfalls

- **The step size.** Too small, and the estimates lag behind the drift (70 errors with $\beta = 0.01$ in the first example). Too large, and the noise in the estimates raises the error rate. Tune it to the drift rate and the SNR.
- **No ML guarantee with adaptation.** With $\beta > 0$, a wrong path can fit its own estimate well and win, in particular when the channel is badly known at the start. The detector is a good heuristic, not the ML detector for an unknown channel.
- **Phase and sign ambiguity.** A blind PSP receiver can converge to $-f$ with all symbols inverted, or to a rotated channel for QAM. Use a known preamble or differential coding.
- **Cost with many states.** With $M^{L-1}$ states, each with an RLS estimator, the cost grows fast. Combine PSP with a reduced-state trellis.
- **Ties in the metric.** When two branches into a state have equal metrics, the choice decides which estimate survives. Break ties in a fixed order so that the result is reproducible.

## Exercises

1. Show by induction that, after time $n$, the estimate of each state is the LMS estimate run on the symbols of its own survivor.
2. Show that with $\beta = 0$ the receiver gives the same decisions as the Viterbi equalizer for $f_0$.
3. For the channel with one tap $f = 1$, the step size 0.1 and $y = (0.9, -1.2, 0.1)$, compute the decisions and the final estimate by hand. (The answer is $(+1, -1, +1)$ and 0.9199.)
4. A conventional adaptive Viterbi equalizer updates one estimate with the decision made $D$ steps back. Explain why it must predict the channel $D$ steps ahead on a fast-fading channel, and why PSP does not.
5. Count the operations per symbol for PSP with RLS on a channel with $L$ taps and $M$ symbols, and compare them with a single RLS estimator.

## References
