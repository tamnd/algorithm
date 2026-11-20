---
tag: 8TQVP4
kind: algorithm
slug: viterbi-equalizer
name: Viterbi equalizer
aliases:
- MLSE equalizer
area: communications/channel-estimation-and-equalization
level: core
summary: Finds the maximum likelihood symbol sequence over an ISI channel by the Viterbi algorithm on a trellis of channel states.
solves: [maximum-likelihood-sequence-estimation, channel-equalization]
model: word-ram
complexity:
  vars: {N: the number of symbols, M: the alphabet size, L: the number of channel taps}
  time: {worst: O(N M^L)}
  space: {extra: O(N M^(L-1))}
properties: {deterministic: true, exact_ml: true, needs_channel: true, states: "M^(L-1)"}
history:
  year: 1972
  people: [G. David Forney Jr.]
  note: "Forney applied the Viterbi algorithm to the discrete-time ISI channel after a whitened matched filter and showed that it is the maximum likelihood sequence estimator."
prereqs: [viterbi-algorithm, intersymbol-interference, whitened-matched-filter]
see_also: [maximum-likelihood-sequence-estimation, ungerboeck-mlse-receiver, reduced-state-sequence-estimation, per-survivor-processing, decision-feedback-equalizer, bcjr-algorithm, turbo-equalization, partial-response-signaling]
sources:
  - paper: "G. David Forney, Jr., Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972, pages 363 to 378"
    locator: "the discrete-time white-noise model, the ISI trellis with M^(L-1) states and the error event analysis"
  - paper: "Andrew J. Viterbi, Error bounds for convolutional codes and an asymptotically optimum decoding algorithm, IEEE Transactions on Information Theory 13(2), 1967, pages 260 to 269"
    locator: "the decoding algorithm"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.3 (maximum likelihood sequence estimation for the discrete-time white noise model, and its performance)"
---

The Viterbi equalizer finds the most likely transmitted sequence on a channel with [intersymbol interference](/intersymbol-interference/). The channel output at time $k$ depends on the current symbol and on the last $L-1$ symbols, so these $L-1$ symbols are a state. A sequence of symbols is a path through a trellis with $M^{L-1}$ states per time step, and the squared distance between the received samples and the noiseless output is a sum of branch metrics along the path. The [Viterbi algorithm](/viterbi-algorithm/) finds the path with the smallest sum. With white Gaussian noise this path is the [maximum likelihood sequence](/maximum-likelihood-sequence-estimation/). The input is usually the output of a [whitened matched filter](/whitened-matched-filter/), which gives a causal channel with white noise. This page gives the ISI trellis and its metric; the search itself is the one on the Viterbi algorithm page.

## In plain words

Each received sample is a mix of the current symbol and a few earlier ones. A detector that looks at one sample at a time treats the earlier symbols as noise. The Viterbi equalizer does not. It keeps, for every possible group of recent symbols, the best guess of the whole past that ends in that group. When a new sample arrives, it extends each guess by each possible new symbol, scores how well the result explains the sample, and keeps only the best extension into each group. At the end it reads back the best guess. The number of groups grows quickly with the length of the channel, which limits the method to short channels and small alphabets.

## The problem

The input is a known channel $f = (f_0, \ldots, f_{L-1})$, an alphabet $\mathcal{A}$ of $M$ points, the $L-1$ known symbols before the block, and the samples $y_k = \sum_{l=0}^{L-1} f_l x_{k-l} + n_k$ for $k = 0, \ldots, N-1$, with $n_k$ white $\mathcal{CN}(0, N_0)$. The output is the sequence $\hat x \in \mathcal{A}^N$ that minimizes
$$J(x) = \sum_{k=0}^{N-1} \Big| y_k - \sum_{l=0}^{L-1} f_l x_{k-l} \Big|^2 ,$$
which is the maximum likelihood sequence. If the transmitter ends the block with $L-1$ known tail symbols, the receiver adds their $L-1$ samples to $y$ and forces the tail in the trellis.

## The algorithm

The state at time $k$ is $s_k = (x_{k-1}, \ldots, x_{k-L+1})$. A symbol $a$ moves $s_k$ to $s_{k+1} = (a, x_{k-1}, \ldots, x_{k-L+2})$, and the branch metric is $\lambda_k(s, a) = |y_k - f_0 a - \sum_{l \ge 1} f_l s_l|^2$.

```pseudo id=main
VITERBI-EQUALIZER(y, f, A, pre, tail)
L1  S ← the M^(L-1) states; before x[0] the past symbols come from pre
L2  metric[s] ← 0 for the start state, ∞ for the others
L3  for k ← 0 to K - 1
L4      for each state s with metric[s] < ∞ and each symbol a allowed at k    ▷ only the tail symbol after x[n-1]
L5          λ ← |y[k] - f[0] a - Σ_{l≥1} f[l] x[k-l](s)|²
L6          if metric[s] + λ < new[next(s, a)] then keep it and set ptr[k][next(s, a)] ← (s, a)
L7  s ← the state with the smallest metric
L8  follow ptr from s back to k = 0 and read the symbols
L9  return the first n symbols
```

Line L1 fixes the trellis. Line L2 starts from the known past. Lines L4 to L6 are the add-compare-select step: each state keeps the one path into it with the smallest metric, its survivor. Line L5 is the only part that depends on the channel. For $k \ge L-1$ the noiseless output depends only on $(s, a)$, so the implementation computes the $M^L$ values once. Lines L7 and L8 are the traceback. With a known tail, one state remains at the end and line L7 has no choice.

## Example

Take $f = (1, 0.5)$, BPSK with $\mathcal{A} = \{+1, -1\}$, and the known symbol $x_{-1} = +1$. The state is the last symbol, so there are 2 states. The transmitted block is $x = (+1, -1, -1, +1)$, the noiseless outputs are $(1.5, -0.5, -1.5, 0.5)$, and the noise gives $y = (1.4, 0.1, -1.2, 0.6)$. Each cell shows the survivor metric of the state and the state it came from:

| $k$ | $y_k$ | state $+1$ | state $-1$ |
|---|---|---|---|
| 0 | 1.4 | 0.01 from $+1$ | 3.61 from $+1$ |
| 1 | 0.1 | 1.97 from $+1$ | 0.37 from $+1$ |
| 2 | -1.2 | 3.26 from $-1$ | 0.46 from $-1$ |
| 3 | 0.6 | 0.47 from $-1$ | 4.47 from $+1$ |

At $k = 2$, the state $+1$ compares $1.97 + (-1.2 - 1.5)^2$ with $0.37 + (-1.2 - 1 + 0.5)^2$, that is 9.26 with 3.26, and keeps the path from $-1$. At the end, the state $+1$ has the smallest metric, 0.47. The traceback reads $+1, -1, -1, +1$ backward through the "from" column, so $\hat x = (+1, -1, -1, +1)$, which is correct. A slicer on $y$ decides $x_1 = +1$, because $y_1 = 0.1 > 0$. Both survivors at $k = 1$ come from the state $+1$ at $k = 0$, so the two paths merge there and $x_0 = +1$ is final after one step. In a stream, the receiver outputs a symbol when all survivors agree on it.

On $f = (1, 0.5)$ at $N_0 = 0.4$, a run of 60000 BPSK symbols with seed 7505 gave 572 errors, a rate of 0.00953. The [matched filter](/matched-filter/) bound $Q(\sqrt{2\|f\|^2/N_0})$ is 0.00621. For this channel, the minimum squared distance between two output sequences is $d_{\min}^2 = 5 = 4\|f\|^2$, the same as for a single isolated symbol, so the ISI costs nothing at high SNR. On the channel B of Proakis, $f = (0.407, 0.815, 0.407)$, a search over error events up to length 16 gives $d_{\min}^2 = 2.6569$ against $4\|f\|^2 = 3.9821$, a loss of 1.76 dB. On the channel C of Proakis, $f = (0.227, 0.460, 0.688, 0.460, 0.227)$, the same search gives $d_{\min}^2 = 1.2624$ against 3.9984, a loss of 5.01 dB. A linear equalizer loses much more on both channels, because their zeros are near the unit circle.

## Correctness

**Claim.** The returned sequence minimizes $J$ over $\mathcal{A}^N$ with the known pre and tail symbols, so it is a maximum likelihood sequence when the noise is white and Gaussian.

**Key step.** The noiseless output at time $k$ depends only on the state and the new symbol, so $J$ is a sum of branch metrics along a trellis path. Two paths that reach the same state at time $k$ have the same future branch metrics, so only the better one can be part of the best full path. By induction on $k$, each survivor is the best path into its state, and the best final survivor is the best path overall. The proofs folder has the details and the high-SNR bounds $Q(\sqrt{d_{\min}^2/(2N_0)})$ and $Q(\sqrt{2\|f\|^2/N_0})$.

## Complexity

Each step visits $M^{L-1}$ states with $M$ branches, so $N$ symbols cost $O(N M^L)$ time once the $M^L$ noiseless outputs are tabulated, in the [word RAM](/word-ram/) with the metrics as numbers of fixed precision. The pointers take $O(N M^{L-1})$ space. A stream receiver keeps only the last $D$ steps of pointers, with a decision delay $D$ of about 5 times the channel memory, and needs $O(D M^{L-1})$ space. The cost is exponential in the channel memory: 8-PSK on 5 taps needs $8^4 = 4096$ states, and 64-QAM on 3 taps needs 4096 states as well. A linear or decision feedback equalizer costs $O(N L)$.

## Properties

- **Exact.** It is the maximum likelihood sequence detector, so it minimizes the probability of a sequence error, not of a symbol error. The [BCJR algorithm](/bcjr-algorithm/) on the same trellis gives the symbol-wise MAP decisions and soft outputs.
- **Error events.** At high SNR, errors come in short events, and the rate is close to $c\,Q(\sqrt{d_{\min}^2/(2N_0)})$. The minimum distance $d_{\min}$ is at most the matched filter bound distance $2\|f\|$, and often equal to it.
- **No noise enhancement.** Unlike linear equalizers, it never inverts the channel, so spectral nulls do not amplify the noise. They only reduce $d_{\min}$.
- **Needs white noise.** The Euclidean metric is the log-likelihood only for white noise. With colored noise, whiten first, or use the [Ungerboeck metric](/ungerboeck-mlse-receiver/) on the matched filter output.
- **Needs the channel.** The receiver must know $f$. A wrong estimate gives a wrong metric for every branch. [Per-survivor processing](/per-survivor-processing/) tracks the channel inside the trellis.

## Variants and improvements

- **Ungerboeck receiver.** Works on the matched filter output with a modified branch metric, so it needs no whitening filter. See [Ungerboeck MLSE receiver](/ungerboeck-mlse-receiver/).
- **Reduced states.** [Reduced-state sequence estimation](/reduced-state-sequence-estimation/) keeps only a few recent symbols or only subsets of the alphabet in the state, and cancels the rest of the ISI with decisions from each survivor. DDFSE with a memory of $\mu < L-1$ symbols uses $M^\mu$ states instead of $M^{L-1}$.
- **Soft outputs.** The soft-output Viterbi algorithm and the [BCJR algorithm](/bcjr-algorithm/) give reliabilities for a decoder, which is the start of [turbo equalization](/turbo-equalization/).
- **Adaptive.** [Per-survivor processing](/per-survivor-processing/) updates a channel estimate or a phase estimate along each survivor.
- **Partial response.** On a channel designed to have a short known response, such as duobinary $f = (1, 1)$ in [partial-response signaling](/partial-response-signaling/), the trellis is small and fixed. Magnetic recording uses this.

## When to use it

Use it when the channel memory and the alphabet are small enough that $M^{L-1}$ states are affordable, the channel is known or well estimated, and the best detection matters: GSM receivers with binary symbols and a few taps, partial-response read channels, short optical and wireline links. For long channels or large constellations, use a [DFE](/decision-feedback-equalizer/), [RSSE](/reduced-state-sequence-estimation/), or a block transmission with [frequency-domain equalization](/frequency-domain-equalization/).

## Pitfalls

- **Colored noise.** Running the Euclidean metric on matched filter samples, or on samples with colored noise, is no longer maximum likelihood. Use the WMF output or the Ungerboeck metric.
- **Maximum-phase channels.** The full Viterbi equalizer does not care about the phase of the channel, but a short decision delay does: if the energy comes late, the survivors merge late. The WMF gives the minimum-phase channel.
- **The start state.** The trellis must start from the known past, or from all states with metric 0 if the past is unknown. Starting from a wrong known state adds errors at the start of each block.
- **Metric overflow.** Metrics grow without bound in a stream. Subtract the minimum metric at each step, or use modular arithmetic on fixed-point metrics.
- **States grow quickly.** $M^{L-1}$ looks small for BPSK, but 16-QAM on 4 taps already needs 4096 states.

## Implementations

## History

Viterbi published the algorithm in 1967 to decode convolutional codes. In 1972, Forney showed that the ISI channel is a finite-state machine like a convolutional encoder, that the whitened matched filter gives a discrete-time model with white noise, and that the Viterbi algorithm on this model is the maximum likelihood sequence estimator. He also gave the error event analysis with $d_{\min}$ and showed that for many channels the loss against the matched filter bound is small. In 1974, Ungerboeck gave the same detector on the matched filter output without the whitening filter. Later work reduced the number of states: reduced-state sequence estimation and DDFSE in the late 1980s, and per-survivor processing in the 1990s added channel tracking.

## References
