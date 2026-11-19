---
tag: FCGMHH
kind: algorithm
slug: pyin
name: "pYIN"
aliases:
- probabilistic YIN
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: YIN with a distribution over thresholds that gives many pitch candidates with probabilities, then Viterbi decoding of a pitch HMM.
solves: [pitch-detection]
model: real-ram
complexity:
  vars: {F: the number of frames, W: the frame length, T: the largest lag, N: the number of thresholds, M: the number of pitch bins, J: the largest pitch jump in bins}
  time: {worst: O(F (W T + N T + M J))}
  space: {extra: O(T + F M)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2014
  people: [Matthias Mauch, Simon Dixon]
  note: Mauch and Dixon replaced the single threshold of YIN by a prior over 100 thresholds, which gives several period candidates with probabilities per frame, and chose the track with a hidden Markov model of pitch and voicing. They evaluated it on synthesized singing.
prereqs: [yin-algorithm, hidden-markov-model, viterbi-algorithm]
see_also: [cepstral-pitch-detection, rapt-pitch-tracker, pitch-detection, autocorrelation, forward-backward-algorithm, log-sum-exp-trick, median-filter, voice-activity-detection]
sources:
  - paper: doi:10.1109/ICASSP.2014.6853678
    title: Matthias Mauch and Simon Dixon, PYIN, a fundamental frequency estimator using probabilistic threshold distributions, Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2014, 659 to 663
    locator: "Section 2.1 (equations 1 to 5, the threshold prior and the candidate probabilities), Section 2.2 (equations 6 to 8, the pitch and voicing HMM) and Section 3 (the evaluation on synthesized singing)"
  - paper: doi:10.1121/1.1458024
    title: Alain de Cheveigné and Hideki Kawahara, YIN, a fundamental frequency estimator for speech and music, Journal of the Acoustical Society of America 111(4), 2002, 1917 to 1930
    locator: Section II, steps 2 to 5 (the difference function, the cumulative mean normalization, the absolute threshold and the parabolic interpolation)
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, 257 to 286
    locator: Section III, the solution to problem 2 (the Viterbi algorithm)
---

pYIN, or probabilistic YIN, is a pitch tracker by Matthias Mauch and Simon Dixon (2014) that keeps several period candidates per frame and then chooses one track over all frames. Its first stage is the [YIN algorithm](/yin-algorithm/) run with 100 thresholds at once, weighted by a prior, so that each candidate period gets a probability and the mass left over means unvoiced. Its second stage is a [hidden Markov model](/hidden-markov-model/) with a voiced and an unvoiced state for each pitch bin, decoded by the [Viterbi algorithm](/viterbi-algorithm/). Plain YIN commits to one period per frame with one threshold; the [cepstral detector](/cepstral-pitch-detection/) decides each frame alone from the cepstrum; [RAPT](/rapt-pitch-tracker/) also keeps candidates and uses a dynamic program, but with the normalized cross-correlation and hand-set costs instead of probabilities.

## In plain words

YIN looks for the first shift at which a sound matches a copy of itself well enough, and "well enough" is a fixed limit. The right limit changes from sound to sound. pYIN tries a hundred limits at once. Each limit points to some shift, and more likely limits count more, so each frame gets a short list of possible pitches with weights. What is left of the weight says that the frame may be noise. Then pYIN looks at all frames together and picks the path through the lists that is most likely, where the pitch moves smoothly and the voice does not switch on and off at every frame.

## The problem

Given a signal at a sample rate $f_s$, cut into $F$ frames, and a pitch range $f_{\min}$ to $f_{\max}$ (55 to 880 Hz in the paper), return for each frame either a fundamental frequency in Hz or the label unvoiced. A frame of $W$ samples needs $W + T + 2$ samples of signal, where $T = \lceil f_s / f_{\min} \rceil$ is the largest lag. The problem and its error measures are on the [pitch detection](/pitch-detection/) page. Unlike YIN, pYIN works on the whole sequence of frames, so it is an offline method.

## The algorithm

Stage 1 works on one frame. With the YIN difference function $d(\tau)$ and its cumulative mean normalized form $d'(\tau)$, let $Y(s)$ be the YIN period for the threshold $s$: the bottom of the first dip of $d'$ below $s$, or, if no value is below $s$, the lag of the global minimum of $d'$. For $N = 100$ thresholds $s_i = i / 100$ with prior probabilities $P(s_i)$, the probability of a period $\tau$ is (equation 4 of the paper)

$$P(\tau) = \sum_{i=1}^{N} a(s_i, \tau)\, P(s_i)\, [Y(s_i) = \tau], \qquad a(s_i, \tau) = \begin{cases} 1 & d'(\tau) < s_i \\ p_a & \text{otherwise,} \end{cases}$$

with $p_a = 0.01$. The prior is a Beta distribution with mean 0.1, 0.15 or 0.2, discretized as $P(s_i) = I_{s_i}(\alpha, \beta) - I_{s_{i-1}}(\alpha, \beta)$ with the Beta distribution function $I$; for mean 0.1 this page uses $\alpha = 2$ and $\beta = 18$.

Stage 2 works on all frames. The pitch range is cut into $M$ bins of 10 cents ($M = 480$ from 55 Hz up to just under 880 Hz). Each bin $m$ has a voiced state $(m, 1)$ and an unvoiced state $(m, 0)$. If $p^*_m$ is the candidate mass of frame $t$ whose frequency is nearest to bin $m$, the observation weights are (equation 6)

$$b_t(m, 1) = 0.5\, p^*_m, \qquad b_t(m, 0) = 0.5 \Bigl(1 - \sum_k p^*_k\Bigr).$$

The transition from $(i, v)$ to $(j, v')$ is the product of a pitch move and a voicing move: the pitch move is a triangle, $(J + 1 - |j - i|) / (J + 1)^2$ for $|j - i| \le J$ with $J = 25$ bins, and the voicing stays with probability 0.99 and switches with probability 0.01 (equations 7 and 8).

```pseudo id=main
PYIN(frames x_1 .. x_F, fs, P(s_1 .. s_N), p_a, M, J)
L1  for each frame t: d <- the YIN difference function of x_t for 0 <= tau <= T
L2      d' <- the cumulative mean normalized difference of d; mass <- empty
L3      for i <- 1 to N do
L4          (tau, below) <- Y(s_i): the bottom of the first dip of d' under s_i, or the argmin of d' with below = false
L5          mass[tau] <- mass[tau] + (1 if below else p_a) * P(s_i)
L6      each tau with mass[tau] > 0 gives a candidate fs / tau', with tau' from a parabola through d' around tau
L7      p*_m <- the candidate mass nearest to bin m; b_t(m, 1) <- 0.5 p*_m; b_t(m, 0) <- 0.5 (1 - sum_k p*_k)
L8  delta_1(q) <- log pi(q) + log b_1(q) for every state q = (m, v)
L9  for t <- 2 to F do
L10     delta_t(q) <- max over q' of delta_{t-1}(q') + log A(q', q); psi_t(q) <- the argmax
L11     delta_t(q) <- delta_t(q) + log b_t(q)
L12 q_F <- the argmax of delta_F
L13 for t <- F down to 2 do q_{t-1} <- psi_t(q_t)
L14 return, for each frame t, the frequency of the bin of q_t if q_t is voiced, else unvoiced
```

Lines L1 to L7 are stage 1, once per frame, and lines L8 to L13 are the Viterbi algorithm in log space. The maximum in line L10 runs only over the $2(2J + 1)$ states that can reach $q$. The code returns the center frequency of the chosen bin; the paper's Vamp plugin can also report the candidate frequency nearest to it.

The paper prints the Beta parameters as "α = 1 and β = 18, 11 1/3, 8". With $\alpha = 1$ the means would be 0.053, 0.081 and 0.111, not the stated 0.1, 0.15 and 0.2, and the density would be largest at 0, not near 0.07 as in its Figure 2. The stated means need $\alpha = 2$, the value that later ports use, and this page uses it.

The paper starts the chain uniformly over the unvoiced states. If the first frame has candidate mass 1, then every unvoiced weight $b_1(m, 0)$ is 0, and every path has probability 0. The code therefore starts uniformly over all $2M$ states by default and keeps the paper's start as an option.

## Example

**Stage 1.** Take $f_s = 8000$ Hz and $x[n] = 0.6 \sin(2\pi \cdot 220 n / f_s) + 0.3 \sin(4\pi \cdot 220 n / f_s + 0.5)$ plus Gaussian noise with standard deviation 0.12 (seed 3), $W = 200$ and the range 55 to 880 Hz, so $9 \le \tau \le 146$. The period is $8000 / 220 = 36.36$ samples. The noise makes the three dips of $d'$ nearly equal:

| $\tau$ | 35 | 36 | 37 | 72 | 73 | 74 | 108 | 109 | 110 |
|---|---|---|---|---|---|---|---|---|---|
| $d'(\tau)$ | 0.1003 | 0.0610 | 0.0740 | 0.0782 | 0.0570 | 0.0862 | 0.0891 | 0.0548 | 0.0691 |

For $s \le 0.05$ no value is below $s$, so $Y(s) = 109$, the global minimum, with weight $p_a$. For $s = 0.06$ the first value below is $d'(73) = 0.057$, since $d'(36) = 0.061$ is not. For $s \ge 0.07$ the first dip is at 36. With the Beta(2, 18) prior, $P(s \le 0.05) = 0.2453$, $P(s = 0.06) = 0.0718$ and $P(s \ge 0.07) = 0.6829$, so the candidates are

| period | frequency | probability |
|---|---|---|
| 36, interpolated | 220.68 Hz | 0.6829 |
| 73, interpolated | 109.71 Hz | 0.0718 |
| 109, interpolated | 73.26 Hz | $0.01 \times 0.2453 = 0.0025$ |

The voiced mass is 0.7572, so the unvoiced weight is $0.5 \times 0.2428 = 0.1214$. Plain YIN with $s = 0.05$ would return 73.26 Hz here, and with $s = 0.1$ it would return 220.68 Hz; pYIN keeps both and lets the next frames decide.

**Stage 2.** A tiny chain with $M = 2$ bins, $J = 1$, a voicing stay probability of 0.9 and a uniform start of $1/4$ over the four states. The pitch move is $2/4 = 0.5$ to the same bin and $1/4 = 0.25$ to the other one. The weights $b_t$ of three frames are

| state | frame 1 | frame 2 | frame 3 |
|---|---|---|---|
| (0, voiced) | 0.45 | 0.20 | 0 |
| (1, voiced) | 0 | 0.15 | 0.40 |
| (0, unvoiced) and (1, unvoiced) | 0.05 | 0.15 | 0.10 |

The best path is (0, voiced), (0, voiced), (1, voiced), with probability $\tfrac14 \cdot 0.45 \cdot (0.5 \cdot 0.9) \cdot 0.20 \cdot (0.25 \cdot 0.9) \cdot 0.40 = 0.00091125$. The path (0, voiced), (1, voiced), (1, voiced) gives $\tfrac14 \cdot 0.45 \cdot 0.225 \cdot 0.15 \cdot 0.45 \cdot 0.40 = 0.00068344$, and every path that ends on (0, voiced) gives 0. A search over all $4^3 = 64$ paths gives the same best value.

**A track.** The same tone with noise 0.05, 1000 samples followed by 600 samples of silence, frames of $W = 200$ every 200 samples and $M = 250$ bins, gives 220.0 Hz (bin 240) for the four frames inside the tone and unvoiced for the last three.

## Correctness

pYIN is an estimator, so no theorem says that its track is the true pitch. Two things can be proved: stage 1 computes equation 4, and stage 2 returns a state sequence of largest weight under the model. The proofs are in proofs/correctness.md.

For stage 1, line L4 returns the smallest lag $\tau$ in the range with $d'(\tau) < s$ and either $\tau = T$ or $d'(\tau + 1) \ge d'(\tau)$, which is the YIN rule, or the global minimum when there is none. Line L5 adds $P(s_i)$ times $a(s_i, \tau)$ to exactly one lag for each $i$, so after the loop the mass of each lag is the sum in equation 4. The total mass is $\sum_i a_i P(s_i) \le \sum_i P(s_i) = 1$, with equality only when every threshold finds a dip. For every threshold $s_i$ on the grid, the YIN estimate $Y(s_i)$ is among the candidates, because it gets the positive mass $a_i P(s_i)$; this is property 3 of the paper.

For stage 2, the weight of a state sequence $q_1, \ldots, q_F$ is $\pi(q_1) b_1(q_1) \prod_{t \ge 2} A(q_{t-1}, q_t)\, b_t(q_t)$. By induction on $t$, $\delta_t(q)$ is the log of the largest weight of a sequence of length $t$ that ends in $q$: the best such sequence ends with a best sequence of length $t - 1$ that ends in some $q'$, because the weight factors over $t$. So $q_F$ ends a best sequence, and the back pointers rebuild one. This holds for any nonnegative weights, so it does not matter that $b_t$ is not a normalized distribution or that the rows of $A$ near the ends of the bin range sum to less than 1. Log space changes nothing, since the log is increasing, and it avoids underflow.

## Complexity

In the [real RAM](/real-ram/), line L1 costs $O(W T)$ per frame directly, or $O((W + T) \log(W + T))$ with the FFT as on the YIN page. Lines L3 to L5 cost $O(N T)$, since each threshold scans at most $T$ lags. Line L10 looks at $2(2J + 1)$ predecessors for each of the $2M$ states, so a frame costs $O(M J)$. The total time is $O(F (W T + N T + M J))$. The memory is $O(T)$ for one frame of stage 1, $O(M)$ for $\delta$, and $O(F M)$ for the back pointers, which dominate. With the paper's numbers, $M = 480$ and $J = 25$, the Viterbi step costs about 98000 additions per frame.

## Properties

- **More candidates than YIN.** For every threshold on the grid, the YIN estimate is a candidate, so pYIN covers at least the correct estimates of YIN with any of those thresholds.
- **A voicing probability.** The mass not given to any period, $1 - \sum_\tau P(\tau)$, is a probability of unvoiced; YIN has no such number.
- **Offline.** The Viterbi step needs all frames before it returns the first one. A version with a fixed delay can decode a sliding window, at the cost of exactness.
- **Quantized output.** The track moves in 10 cent steps. The candidate frequency itself has the precision of the parabolic interpolation.
- **Measured accuracy.** On more than 30 hours of synthesized singing made from the pitch tracks of the RWC music database, at 44.1 kHz with frames of 2048 samples and a hop of 256, the median recall was 0.977, 0.982 and 0.984 for the three priors, against medians below 0.951 for YIN with the three single thresholds. These are measurements on that data set.

## Variants and improvements

- **Other priors.** The paper tests Beta priors with means 0.1, 0.15 and 0.2, and a prior with a single threshold, which is YIN followed by HMM smoothing.
- **Note tracking.** Mauch and others built a note transcription method on top of the pYIN pitch track, in the Tony tool for melody annotation.
- **Posterior decoding.** The [forward-backward algorithm](/forward-backward-algorithm/) gives the probability of voicing in each frame, which some ports report next to the Viterbi track.
- **Faster stage 2.** The transition matrix is banded, so the maximum of line L10 can use a sliding window maximum; with the triangle weights a direct band sum is already $O(M J)$.
- **Other trackers.** The [RAPT](/rapt-pitch-tracker/) dynamic program uses costs set by hand instead of probabilities, and a [median filter](/median-filter/) on a YIN track is the cheapest smoothing.

## When to use it

Use pYIN for offline pitch tracks of a single voice or instrument, such as intonation studies, singing analysis and melody annotation, when octave jumps and voicing errors matter more than speed. It needs no training data. For real-time use with a small delay, use YIN with a short smoothing filter. For polyphonic music it is the wrong tool, because the HMM allows one pitch per frame.

## Pitfalls

- **The printed Beta parameters.** With $\alpha = 1$ the priors do not have the stated means. Use $\alpha = 2$ with $\beta = 18$, $11\tfrac13$ and 8.
- **Starting on unvoiced states.** As above, a first frame with voiced mass 1 makes every path impossible. Start on all states, or put a small floor under the unvoiced weight.
- **Normalizing each transition row.** If each row of the pitch move is scaled to sum to 1, the rows near the ends of the range get larger weights, and an unvoiced path can sit at the end bin and win. The paper normalizes the triangle once, so those rows sum to less than 1.
- **Short voiced segments.** A switch of voicing costs a factor of 0.01 each way. In the test of the code, four noisy frames with voiced weight about twice the unvoiced weight did not pay for the two switches, and the whole track came out unvoiced.
- **Products of probabilities.** A track of a few hundred frames multiplies hundreds of small weights, which underflows to 0 in double precision. Work with logs, as in lines L8 to L11.
- **A frame that is too short.** The frame must cover $W + T + 2$ samples, with $T = \lceil f_s / f_{\min} \rceil$; at 55 Hz and 44.1 kHz that is more than 800 samples of lag alone.

## Implementations

## History

Alain de Cheveigné and Hideki Kawahara published YIN in 2002. Matthias Mauch and Simon Dixon, at Queen Mary University of London, presented pYIN at ICASSP 2014, with a Vamp plugin implementation. The idea of the paper is that some threshold usually gives the right YIN estimate, but no single threshold is right for every frame, so a distribution over thresholds and a tracking HMM can recover the right one. Ports of pYIN later appeared in common audio libraries.

## References
