---
tag: 3H9VBZ
kind: model
slug: gilbert-elliott-channel
name: Gilbert-Elliott channel
aliases:
- Gilbert-Elliott model
- two-state Markov channel
area: communications/fading-channels
level: core
summary: "A binary channel whose crossover probability is set by a hidden two-state Markov chain, good or bad, so errors come in bursts: the standard model of channels with memory."
prereqs: [markov-chain, stationary-distribution, binary-symmetric-channel]
see_also: [binary-symmetric-channel, hidden-markov-model, interleaving, forward-backward-algorithm, rayleigh-fading-channel, reed-solomon-code, expectation-maximization, channel-capacity]
sources:
  - paper: doi:10.1002/j.1538-7305.1960.tb03959.x
    title: E. N. Gilbert, Capacity of a burst-noise channel, Bell System Technical Journal 39(5), 1960
    locator: pp. 1253 to 1265 (the two-state model with no errors in the good state, and the capacity of the channel)
  - paper: doi:10.1002/j.1538-7305.1963.tb00955.x
    title: E. O. Elliott, Estimates of error rates for codes on burst-noise channels, Bell System Technical Journal 42(5), 1963
    locator: pp. 1977 to 1997 (errors in the good state as well, and the probability of error patterns in blocks of bits)
  - paper: doi:10.1109/18.45284
    title: M. Mushkin and I. Bar-David, Capacity and coding for the Gilbert-Elliott channels, IEEE Transactions on Information Theory 35(6), 1989
    locator: pp. 1277 to 1290 (the capacity of the channel and the effect of the memory on it)
  - paper: doi:10.1109/25.350282
    title: H. S. Wang and N. Moayeri, Finite-state Markov channel, a useful model for radio communication channels, IEEE Transactions on Vehicular Technology 44(1), 1995
    locator: pp. 163 to 171 (a Markov chain over ranges of the SNR of a Rayleigh fading channel)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.4 (finite-state Markov channels)
---

The Gilbert-Elliott channel is a binary channel with memory. A hidden [Markov chain](/markov-chain/) with two states, good and bad, moves at each bit, and in each state the channel is a [binary symmetric channel](/binary-symmetric-channel/) with its own crossover probability, small in the good state and large in the bad state. The chain stays in a state for many bits, so the errors come in bursts. Gilbert defined the model in 1960 with no errors in the good state, and Elliott added errors in the good state in 1963.

## The machine

The state $S_t \in \{G, B\}$ is a stationary Markov chain with

$$\Pr[S_{t+1} = B \mid S_t = G] = p, \qquad \Pr[S_{t+1} = G \mid S_t = B] = r, \qquad 0 < p, r < 1 .$$

The input is a bit $X_t$, and the output is $Y_t = X_t \oplus Z_t$, where the error bit $Z_t$ is 1 with probability $e_G$ in state $G$ and $e_B$ in state $B$. Given the states, the $Z_t$ are independent of each other and of the input. The usual case is $e_G \ll e_B$. Neither the transmitter nor the receiver sees $S_t$ unless the page says so.

**Notation.** Gilbert 1960 writes $P$ for the probability of the move from good to bad ($p$ here), $p$ for the move from bad to good ($r$ here) and $h$ for the probability of a correct bit in the bad state, so $e_B = 1 - h$ and $e_G = 0$. Elliott 1963 adds $k$, the probability of a correct bit in the good state, so $e_G = 1 - k$. Check the letters before using a formula from a paper.

**Derived quantities.**

- Stationary distribution: $\pi_B = \frac{p}{p + r}$ and $\pi_G = \frac{r}{p + r}$.
- Average error rate: $\varepsilon = \pi_G e_G + \pi_B e_B$.
- Sojourn times: the chain stays in $B$ for a geometric number of bits with mean $1/r$, and in $G$ for a mean of $1/p$ bits.
- Memory: the second eigenvalue of the transition matrix is $\lambda = 1 - p - r$, and the state forgets its past as $\lambda^k$.

## What it counts

The model predicts the statistics of error patterns: the probability of a given pattern in a block, the distribution of the number of errors per block, the lengths of bursts and gaps, and the capacity.

**Example.** Take $p = 0.01$, $r = 0.1$, $e_G = 0.001$ and $e_B = 0.3$. Then $\pi_B = 0.0909$, the mean stays are 100 bits in $G$ and 10 bits in $B$, and $\varepsilon = 0.0282$. With $e_G = 0$ (Gilbert's case) $\varepsilon = 0.0273$. A [binary symmetric channel](/binary-symmetric-channel/) with the same $\varepsilon$ looks very different:

| | Gilbert-Elliott | BSC with the same $\varepsilon$ |
|---|---|---|
| $\Pr[\text{no error in 10 bits}]$ | 0.865 | 0.751 |
| $\Pr[\text{no error in 100 bits}]$ | 0.382 | 0.0573 |
| $\Pr[Z_{t+1} = 1 \mid Z_t = 1]$ | 0.262 | 0.0282 |

The errors cluster. Many blocks are clean, and the blocks with errors have many of them, which is bad for a short code with small correction power and good for retransmission of whole blocks.

**Block probabilities.** Let $\Pi$ be the transition matrix, $D_0 = \mathrm{diag}(1 - e_G, 1 - e_B)$ and $D_1 = \mathrm{diag}(e_G, e_B)$. A pattern $z_1, \ldots, z_n$ of error bits has the probability

$$\Pr[Z_1 = z_1, \ldots, Z_n = z_n] = \pi^T D_{z_1} \Pi D_{z_2} \Pi \cdots \Pi D_{z_n} \mathbf{1},$$

where $\pi = (\pi_G, \pi_B)^T$. This is the forward recursion of a [hidden Markov model](/hidden-markov-model/), and it costs $O(n)$ operations with a 2 by 2 matrix at each step. The table above uses it with all $z_i = 0$.

## Relation to other models

- **Binary symmetric channel.** If $e_G = e_B$, or if $p + r = 1$ so that $\lambda = 0$ and the states are independent, the channel is a BSC with crossover $\varepsilon$.
- **Gilbert channel.** The case $e_G = 0$. The case $e_G = 0$ and $e_B = 1/2$ makes every bit in the bad state useless.
- **Hidden Markov models.** The channel is an HMM whose hidden state is $S_t$ and whose output is $Z_t$. The [forward-backward algorithm](/forward-backward-algorithm/) estimates the states from a known error sequence, and [expectation maximization](/expectation-maximization/) (the Baum-Welch algorithm) fits $p$, $r$, $e_G$ and $e_B$ to a measured error trace.
- **Fading channels.** A [Rayleigh fading channel](/rayleigh-fading-channel/) that moves slowly has long good periods and short deep fades. Wang and Moayeri 1995 split the range of the SNR into intervals and make each one a state of a Markov chain, with transition rates from the [level crossing rate](/level-crossing-rate/); with two intervals this gives a Gilbert-Elliott channel. This is a fit; the true fading process is not a Markov chain of finite order.
- **Interleaving.** An [interleaver](/interleaving/) deeper than the bursts spreads the errors across codewords, and the code then sees a channel close to a BSC with crossover $\varepsilon$. Codes for bursts, such as [Reed-Solomon codes](/reed-solomon-code/) over bytes, use the bursts directly.
- **Packet loss.** The same two-state chain with "lost" and "received" outputs is a common model of bursty packet loss in networks.

## Known results in the model

1. **Stationary distribution.** The chain is irreducible and aperiodic for $0 < p, r < 1$. The balance equation $\pi_G p = \pi_B r$ with $\pi_G + \pi_B = 1$ gives $\pi_B = p/(p+r)$. See [stationary distribution](/stationary-distribution/).
2. **Correlation of the errors.** For a two-state chain, $\Pi^k = \mathbf{1}\pi^T + \lambda^k (I - \mathbf{1}\pi^T)$, which can be checked by induction. With $e = (e_G, e_B)^T$, for $k \ge 1$,
   $$\Pr[Z_t = 1, Z_{t+k} = 1] = \pi^T D_1 \Pi^k e = \varepsilon^2 + \lambda^k\, \pi_G \pi_B (e_B - e_G)^2 .$$
   So the excess correlation of the errors decays geometrically with ratio $\lambda$. In the example, $\lambda = 0.89$, and $\Pr[Z_{t+1} = 1 \mid Z_t = 1] = (\varepsilon^2 + 0.89 \cdot 0.0826 \cdot 0.299^2)/\varepsilon = 0.262$.
3. **Capacity (a theorem).** The channel adds the noise $Z$ to the input, and $Z$ is stationary and ergodic. For such a binary additive noise channel, the capacity is $C = 1 - \bar H(Z)$ bit per channel use, where $\bar H(Z) = \lim_n H(Z_1, \ldots, Z_n)/n$ is the entropy rate, reached with uniform independent inputs (Mushkin and Bar-David 1989). Two bounds follow. First, $H(Z_1, \ldots, Z_n) \le n\, h(\varepsilon)$, so $C \ge 1 - h(\varepsilon)$, the capacity after ideal interleaving. Second, $H(Z_1, \ldots, Z_n) \ge H(Z_1, \ldots, Z_n \mid S_1, \ldots, S_n) = n(\pi_G h(e_G) + \pi_B h(e_B))$, so $C \le \pi_G (1 - h(e_G)) + \pi_B (1 - h(e_B))$, the capacity with the state known at the receiver. Here $h$ is the binary entropy function. In the example the bounds are 0.815 and 0.910 bit. Interleaving throws away the memory, and the gap is what a decoder that tracks the state can gain.
4. **Burst and gap lengths.** In Gilbert's case with $e_B$ close to 1, bursts of errors follow the stays in $B$, with mean length $1/r$. In general an error burst is shorter than a stay in $B$, because the bad state also gives correct bits.

### Pitfalls

- **Average error rate is not enough.** Two channels with the same $\varepsilon$ can have very different block error rates (the table above). Report $p$, $r$, $e_G$ and $e_B$, or at least $\varepsilon$ and $\lambda$.
- **Letters across papers.** $p$, $P$, $r$, $h$ and $k$ mean different things in Gilbert, Elliott and later papers.
- **Start state.** A simulation that starts every run in $G$ is not stationary for the first $1/(p+r)$ bits or so. Draw the first state from $\pi$.
- **Hidden state.** Results with the state known at the receiver are upper bounds. A real decoder must estimate $S_t$ from the data.

## References
