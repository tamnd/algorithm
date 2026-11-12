---
tag: FM9AE7
kind: problem
slug: maximum-likelihood-sequence-estimation
name: Maximum-likelihood sequence estimation
aliases:
- MLSE
area: compression-and-coding/error-correcting-codes
level: core
summary: Given the channel output, find the code sequence (a trellis path) with the largest likelihood. The Viterbi algorithm solves it exactly in time linear in the length.
history:
  year: 1967
  people: [Andrew J. Viterbi, G. David Forney Jr.]
  note: Viterbi gave the algorithm in 1967 to bound the error rate of convolutional codes. Forney showed in 1972 and 1973 that it gives the maximum likelihood sequence, for codes and for channels with intersymbol interference.
prereqs: [trellis, maximum-likelihood-decoding, convolutional-code]
see_also: [viterbi-algorithm, symbol-by-symbol-map-decoding, bcjr-algorithm, union-bound, dag-shortest-paths, principle-of-optimality, additive-white-gaussian-noise-channel, hidden-markov-model]
sources:
  - paper: doi:10.1109/TIT.1967.1054010
    title: A. J. Viterbi, Error bounds for convolutional codes and an asymptotically optimum decoding algorithm, IEEE Transactions on Information Theory 13(2), 1967, pages 260 to 269
    locator: The decoding algorithm that keeps one survivor per state, and its error bounds
  - paper: doi:10.1109/PROC.1973.9030
    title: G. D. Forney, Jr., The Viterbi algorithm, Proceedings of the IEEE 61(3), 1973, pages 268 to 278
    locator: The algorithm as the shortest path through a trellis, its proof of optimality, the survivor memory and truncation, and the applications to codes and to intersymbol interference
  - paper: "G. D. Forney, Jr., Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972, pages 363 to 378"
    title: Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference
    locator: The whitened matched filter receiver and the Viterbi algorithm over the states of the channel memory
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 12 (the Viterbi algorithm, its hard and soft decision metrics, the union bound on the bit error probability with the weight enumerator, and the decision depth)
  - paper: "E. R. Berlekamp, R. J. McEliece and H. C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978, pages 384 to 386"
    title: On the inherent intractability of certain coding problems
    locator: The NP-completeness of maximum likelihood decoding of linear codes
---

Maximum-likelihood sequence estimation (MLSE) is the problem of finding, from the output of a noisy channel, the input sequence that makes this output most likely, when the input is constrained to the paths of a [trellis](/trellis/). For a [convolutional code](/convolutional-code/) the paths are the code sequences. For a channel with intersymbol interference the trellis states are the last symbols that the channel remembers. The Viterbi algorithm solves it exactly, with work linear in the length and exponential only in the memory. It is the sequence form of [maximum-likelihood decoding](/maximum-likelihood-decoding/), and it minimizes the probability that the whole sequence is wrong, not the error rate of each bit.

## In plain words

A sender transmits a long stream of bits through a noisy line. The bits are not free: a code or the line itself links each bit to the few bits before it. The receiver wants the one stream that best explains what it heard.

There are far too many streams to try one by one. But the links are short, so the receiver only needs to remember the last few bits of each candidate. It walks along the received signal. At each step, for each possible memory content, it keeps only the best candidate that ends there and drops the others, because a loser can never become the winner later. At the end it reads the best candidate back.

## Definition

The model is a memoryless channel with transition density $P(y \mid x)$, fed by a sequence that a finite state machine produces. A trellis of depth $T$ has states $\sigma_t$ at times $0, \ldots, T$, a known start state $\sigma_0$, and each edge $\sigma_t \to \sigma_{t+1}$ carries a channel input $x_t$ (one or more symbols). A path determines the sequence $x = (x_0, \ldots, x_{T-1})$.

**Input.** The trellis and the channel output $y = (y_0, \ldots, y_{T-1})$.

**Output.** A path whose sequence maximizes

$$P(y \mid x) = \prod_{t=0}^{T-1} P(y_t \mid x_t), \quad\text{that is, minimizes}\quad \sum_{t=0}^{T-1} \lambda_t(x_t), \qquad \lambda_t(x_t) = -\ln P(y_t \mid x_t).$$

The term $\lambda_t$ is the *branch metric*. Any metric of the form $a \lambda_t + b_t$ with $a > 0$ gives the same answer.

- On the [BSC](/binary-symmetric-channel/) with crossover $p < 1/2$ and hard decisions, $\lambda_t$ is $\ln\frac{1-p}{p}$ times the Hamming distance between the received bits and the edge bits, plus a constant. So MLSE finds the path at the least Hamming distance.
- On the [AWGN channel](/additive-white-gaussian-noise-channel/) with BPSK, a code bit $c$ is sent as $x = 1 - 2c$ and $y = x + z$ with $z \sim N(0, \sigma^2)$. Then $\lambda_t$ is the squared Euclidean distance $\sum (y - x)^2$ divided by $2\sigma^2$, plus a constant. These are soft decisions. The page uses $E_s = 1$ per code bit and $E_b/N_0 = 1/(2 R \sigma^2)$ for a code of rate $R$.

When all input sequences are equally likely, MLSE is also the MAP sequence estimate $\arg\max_x P(x \mid y)$. It is not the decoder that minimizes the bit error rate: that is [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/).

## Variants

- **Hard or soft decisions.** A hard decision keeps only the sign of each sample. A soft decision also keeps its size, which tells how reliable the sample is, so soft MLSE has a lower error rate at the same $E_b/N_0$ for the same work.
- **Terminated, truncated and tail-biting trellises.** A terminated code ends in state 0, so the decoder takes the survivor of state 0 at the end. A tail-biting code has paths that start and end in the same unknown state.
- **Intersymbol interference (Forney 1972).** The channel is $y_t = \sum_{j=0}^{L-1} h_j x_{t-j} + z_t$ with Gaussian $z_t$. The state is the last $L - 1$ symbols, so there are $2^{L-1}$ states for binary symbols, and the branch metric is $(y_t - \sum_j h_j x_{t-j})^2$. This is MLSE equalization.
- **List and soft-output versions.** The list Viterbi algorithm returns the $L$ best paths. The soft-output Viterbi algorithm (SOVA) adds a reliability to each decided bit. The exact bit posteriors come from the [BCJR algorithm](/bcjr-algorithm/).
- **The hidden Markov model version.** The [Viterbi algorithm](/viterbi-algorithm/) of the machine learning area finds the most likely state path of a [hidden Markov model](/hidden-markov-model/) with given transition and emission probabilities. MLSE for a code is the case where the transitions are the fixed edges of the code trellis, the inputs are equally likely, and the emission is the channel.

## Examples

**Hard decisions on the (7, 5) code.** The input 1011 with two tail zeros is encoded as 11 10 00 01 01 11. The channel flips the third and the eighth bit, so the receiver gets $r = $ 11 00 00 00 01 11. The branch metric is the Hamming distance. The table gives the best path metric of each state after each step; states are written with the newest input bit on the left, and a dash marks a state that is not reachable.

| step | received | state 00 | state 01 | state 10 | state 11 |
|---|---|---|---|---|---|
| 1 | 11 | 2 | - | 0 | - |
| 2 | 00 | 2 | 1 | 4 | 1 |
| 3 | 00 | 2 | 2 | 1 | 2 |
| 4 | 00 | 2 | 2 | 2 | 2 |
| 5 (tail) | 01 | 3 | 2 | - | - |
| 6 (tail) | 11 | 2 | - | - | - |

The survivor of state 00 at the end has metric 2, the number of channel errors. Its traceback gives the states 00, 10, 01, 10, 11, 01, 00 and the input 1011, so both errors are corrected. The free distance of this code is 5, so every pattern of at most 2 errors in a terminated block is corrected.

**Soft decisions and the union bound.** With the same code on BPSK and AWGN at $E_b/N_0 = 3$ dB ($R = 1/2$, $\sigma^2 = 1/(2 \cdot 0.5 \cdot 10^{0.3}) \approx 0.501$), a simulation of 200 blocks of 100 bits with the seed 2024 in the test gives a bit error rate of 0.00565. The union bound below with the terms $d = 5$ to 12 gives 0.00682, and uncoded BPSK at the same $E_b/N_0$ has $Q(\sqrt{2 \cdot 10^{0.3}}) \approx 0.0229$. At 4 dB the bound is 0.00087, and a simulation gives 0.00075.

**A channel with memory.** For $h = (1, 0.5)$ the state is the previous symbol. With the preamble $x_{-1} = +1$, the noiseless outputs of the bits 0, 1, 1 are $1.5$, $-0.5$ and $-1.5$. The Viterbi algorithm over the 2 states finds the same sequence as a search over all $2^T$ sequences, at a cost of $4T$ branch metrics in place of $2^T T$.

## Known algorithms

**The Viterbi algorithm (Viterbi 1967, Forney 1973).** Let $M_t(\sigma)$ be the least metric of a path from $\sigma_0$ to state $\sigma$ at time $t$. Then $M_0(\sigma_0) = 0$, $M_0(\sigma) = \infty$ for $\sigma \ne \sigma_0$, and

$$M_{t+1}(\sigma') = \min_{(\sigma \to \sigma') \text{ at time } t} \big( M_t(\sigma) + \lambda_t(x_{\sigma \to \sigma'}) \big).$$

The algorithm stores, for each state and time, the edge that gave the minimum (the survivor), and at the end it traces the survivors back from the end state.

```pseudo id=main
VITERBI(trellis, y)                      ▷ convolutional code, 2^m states, start and end in state 0
L1  M[0] ← 0; M[s] ← ∞ for s ≠ 0
L2  for t ← 0 to T − 1 do
L3      for each state s with M[s] < ∞ and each edge s → s' with input u and output x do
L4          m ← M[s] + λ_t(x)
L5          if m < M'[s'] then
L6              M'[s'] ← m; back[t][s'] ← (s, u)
        M ← M'
L7  s ← 0                                ▷ the end state of a terminated code
L8  for t ← T − 1 down to 0 do (s, u_t) ← back[t][s]
    return u_0, ..., u_{T−m−1}
```

*Correctness.* The recursion is the [principle of optimality](/principle-of-optimality/) on a DAG. Take a least metric path $P$ to $\sigma'$ at time $t + 1$, and let its last edge be $\sigma \to \sigma'$. Its prefix is a path to $\sigma$ at time $t$. If another path to $\sigma$ had a smaller metric, then this path followed by the same edge would beat $P$, because the metric is a sum. So the prefix is optimal, and $M_{t+1}(\sigma')$ is the minimum over the incoming edges of $M_t(\sigma) + \lambda_t$. By induction on $t$, $M_T(\sigma_T)$ is the least metric of a full path, and the survivors trace a path that has it. This is the same argument as for [shortest paths in a DAG](/dag-shortest-paths/), with the trellis layers as the topological order.

*Cost.* A rate $1/n$ code with memory $m$ has $2^m$ states and $2^{m+1}$ edges per step, so the time is $\Theta(T\, 2^m n)$ for $T$ steps and the survivor memory is $\Theta(T\, 2^m)$. With a traceback depth $D$, the decoder decides bit $t$ at time $t + D$ from the best state, so the memory is $\Theta(D\, 2^m)$ and the delay is $D$. A depth of about 5 constraint lengths is the usual rule; it is a heuristic, not a guarantee. In the test, a depth of 15 for the (7, 5) code ($K = 3$) gives the same decisions as the full traceback on all 40 blocks.

**Other algorithms.** Sequential decoding (the Fano and stack algorithms) explores only promising paths. Its expected work does not grow with $2^m$ below the cutoff rate, but it is not exact MLSE. Reduced-state and M-algorithm decoders keep only some states and are also approximate.

## Bounds

**The union bound for soft decisions.** For a linear code on BPSK and AWGN with soft MLSE, an error event of output weight $d$ beats the correct path with probability $Q(\sqrt{2 d R E_b/N_0})$. A union over the error events (see [union bound](/union-bound/)) gives the bit error rate bound

$$P_b \le \sum_{d \ge d_{\text{free}}} B_d\, Q\big(\sqrt{2 d R E_b / N_0}\big),$$

where $B_d$ is the total input weight of the paths of output weight $d$ that leave and rejoin state 0 (Lin and Costello, Chapter 12). For the (7, 5) code, $B_d = (d - 4)\, 2^{d - 5}$. The bound is tight at high $E_b/N_0$ and loose at low $E_b/N_0$, where it can exceed 1. With hard decisions on BSC($p$), the pairwise term is the probability that at least half of $d$ positions are in error.

**Complexity.** For a fixed trellis, the Viterbi algorithm is linear in $T$. The difficulty is in the number of states: maximum likelihood decoding of a general linear block code is NP-hard (Berlekamp, McEliece and van Tilborg 1978, see [maximum-likelihood decoding](/maximum-likelihood-decoding/)), and the minimal trellis of a good long block code has an exponential number of states.

## Reductions

- MLSE on a trellis is a shortest path in a [DAG](/dag-shortest-paths/) with the edge weights $\lambda_t$, which may be negative after a shift, because the DAG has no cycles.
- With a uniform prior on the inputs, MLSE is the MAP estimate of the whole sequence. With a non-uniform prior, add $-\ln P(u_t)$ to the branch metric.
- MLSE of a block code is the same problem on its syndrome [trellis](/trellis/), where it is maximum likelihood block decoding.

## Applications

- Decoding of the constraint length 7 convolutional code of CCSDS 131.0-B and IEEE 802.11, with soft decisions.
- Equalization of channels with intersymbol interference, such as GSM receivers and magnetic recording read channels (partial response maximum likelihood).
- Decoding of trellis coded modulation.
- Speech recognition and other [hidden Markov model](/hidden-markov-model/) tasks use the same recursion with model probabilities.

## References
