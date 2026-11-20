---
tag: PEF750
kind: algorithm
slug: truncated-channel-inversion
name: Truncated channel inversion
aliases:
- channel inversion power control
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Power policy for a fading channel: send nothing below a cutoff SNR, and above it send power inversely proportional to the channel, so the receiver sees a constant SNR and a fixed-rate code works."
model: real-ram
complexity:
  vars: {K: the number of channel states}
  time: {worst: O(K log K)}
  space: {extra: O(K)}
properties: {deterministic: true, optimal: false, fixed_rate: true, needs_csit: true}
history:
  year: 1997
  people: [Andrea J. Goldsmith, Pravin P. Varaiya]
  note: "Goldsmith and Varaiya compared the capacity of a fading channel with side information at both ends to the rates of channel inversion and of truncated channel inversion, which keep the received SNR constant."
prereqs: [rayleigh-fading-channel, water-filling-power-allocation]
see_also: [water-filling-power-allocation, adaptive-modulation, link-adaptation, outage-capacity, ergodic-capacity, outage-probability, near-far-problem, fractional-knapsack]
sources:
  - paper: doi:10.1109/18.641562
    title: "Andrea J. Goldsmith and Pravin P. Varaiya, Capacity of fading channels with channel side information, IEEE Transactions on Information Theory 43(6), 1997, pages 1986 to 1992"
    locator: "the capacity with side information at both ends (water-filling in time), compared with the rates of channel inversion and truncated channel inversion"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 4 (capacity of fading channels: channel inversion, zero-outage capacity, truncated channel inversion and outage capacity)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 5 (fading channels with full channel side information, channel inversion compared with water-filling over time)"
---

Truncated channel inversion is a power policy for a fading channel whose gain the transmitter knows. Let $\gamma$ be the SNR that the receiver would see at the average power $\bar P$. When $\gamma$ is below a cutoff $\gamma_0$, the transmitter sends nothing. Otherwise it sends the power $P(\gamma) = \bar P \sigma/\gamma$, the inverse of the channel, so the received SNR is the constant $\sigma$. The average power limit fixes $\sigma = 1/\mathbb{E}[1/\gamma;\, \gamma \ge \gamma_0]$, and a single code for the AWGN channel at SNR $\sigma$ then gives the rate $R(\gamma_0) = \Pr(\gamma \ge \gamma_0)\log_2(1 + \sigma)$. The cutoff is chosen to maximize this rate. Without truncation ($\gamma_0 = 0$), channel inversion has zero rate on Rayleigh fading, since $\mathbb{E}[1/\gamma]$ is infinite there. Goldsmith and Varaiya (1997) compared it with [water-filling](/water-filling-power-allocation/) over time, which is optimal: inversion is simple and keeps one fixed rate, and on Rayleigh fading it loses about a third to two thirds of a bit against water-filling between 10 and 20 dB.

## In plain words

A wireless channel gets stronger and weaker all the time. If the sender knows how strong it is, it can push more power when the channel is weak and less when it is strong. Then the receiver always gets the same signal level, and one simple fixed code works all the time.

The trouble is that a very weak channel needs a huge amount of power to fix. So the sender gives up when the channel is too weak and sends nothing then. The level at which it gives up is a trade-off: give up too often and little time is used, give up too rarely and power is wasted on bad moments.

## The problem

The SNR $\gamma > 0$ is random with a known distribution, and the transmitter knows its current value. A policy $P(\gamma) \ge 0$ must satisfy $\mathbb{E}[P(\gamma)] \le \bar P$. Truncated inversion uses the received SNR $\sigma$ in every state with $\gamma \ge \gamma_0$ and nothing else; given the cutoff, the largest such $\sigma$ is $1/S(\gamma_0)$ with $S(\gamma_0) = \mathbb{E}[\gamma^{-1} \mathbf{1}\{\gamma \ge \gamma_0\}]$. The task is to find $\gamma_0$ that maximizes $R(\gamma_0) = \Pr(\gamma \ge \gamma_0)\log_2(1 + 1/S(\gamma_0))$. For a distribution with $K$ states, such as a quantized channel or a measured sample, the best cutoff is one of the states.

## The algorithm

The states are $\gamma_k > 0$ with probabilities $\pi_k$ (equal values merged first).

```pseudo id=main
TRUNCATED-INVERSION(γ[1..K], π[1..K])
L1  sort the states so that γ[1] > γ[2] > .. > γ[K]
L2  S ← 0, Q ← 0, best ← (0, none, none)
L3  for k = 1 to K do                         ▷ serve the k strongest states
L4      S ← S + π_k / γ_k, Q ← Q + π_k          ▷ S = E[1/γ; γ ≥ γ_k], Q = Pr(γ ≥ γ_k)
L5      R ← Q · log2(1 + 1/S)
L6      if R > best rate then best ← (R, γ_k, 1/S)
L7  (R, γ0, σ) ← best
L8  return γ0, σ, R, and P(γ)/P̄ = σ/γ for γ ≥ γ0, 0 otherwise
```

For Rayleigh fading with mean SNR $\bar\gamma$, the sums have the closed form $S(\gamma_0) = E_1(\gamma_0/\bar\gamma)/\bar\gamma$ and $\Pr(\gamma \ge \gamma_0) = e^{-\gamma_0/\bar\gamma}$, where $E_1$ is the exponential integral, and the best cutoff is found by a one-dimensional search.

## Example

**Four states.** Let $\gamma \in \{8, 4, 2, 0.5\}$, each with probability $1/4$.

| served states | $S$ | $\sigma = 1/S$ | $\Pr(\text{served})$ | rate $Q\log_2(1 + \sigma)$ |
|---|---|---|---|---|
| 8 | 0.03125 | 32.000 | 0.25 | 1.2611 |
| 8, 4 | 0.09375 | 10.667 | 0.50 | 1.7722 |
| 8, 4, 2 | 0.21875 | 4.571 | 0.75 | 1.8585 |
| 8, 4, 2, 0.5 | 0.71875 | 1.391 | 1.00 | 1.2578 |

The best cutoff is $\gamma_0 = 2$, with $\sigma = 32/7 \approx 4.571$ (6.60 dB) and the rate 1.8585 bits per channel use. The powers are $P/\bar P = (4/7, 8/7, 16/7, 0)$ for $\gamma = (8, 4, 2, 0.5)$, and their mean is 1. Full inversion, the last row, must spend most of its power on the state $\gamma = 0.5$ and gets only 1.2578.

**Rayleigh fading.** For Rayleigh fading with mean SNR $\bar\gamma$, compare the best truncated inversion with the ergodic capacity without transmitter knowledge, $\mathbb{E}\log_2(1 + \gamma)$, with water-filling over time, and with an AWGN channel at the same mean SNR (values computed by the test code):

| $\bar\gamma$ | best $\gamma_0$ | outage | $\sigma$ | truncated inversion | no CSIT | water-filling | AWGN |
|---|---|---|---|---|---|---|---|
| 0 dB | -1.21 dB | 0.531 | 4.74 dB | 0.934 | 0.860 | 1.029 | 1.000 |
| 5 dB | 1.82 dB | 0.382 | 7.34 dB | 1.658 | 1.716 | 1.845 | 2.057 |
| 10 dB | 4.80 dB | 0.261 | 10.45 dB | 2.660 | 2.907 | 2.979 | 3.459 |
| 20 dB | 11.18 dB | 0.123 | 18.01 dB | 5.267 | 5.884 | 5.896 | 6.658 |

At 10 dB the policy gives up in 26% of the time and loses 0.32 bits against water-filling. At low SNR it beats the rate without transmitter knowledge, because it moves power to the good states.

## Correctness

**Claim.** The policy returned uses the average power exactly $\bar P$, gives the received SNR $\sigma$ in every state it serves, and its cutoff maximizes $R(\gamma_0)$ over all $\gamma_0 > 0$.

**Key steps.** With $P(\gamma)/\bar P = \sigma/\gamma$ on the served states, the mean power is $\sigma S$, so $\sigma = 1/S$ uses the budget exactly, and no larger constant SNR fits. For a discrete distribution, every cutoff serves some set of the strongest states, and the rate depends only on that set, so the $K$ cutoffs at the states cover all cases. The loop keeps $S$ and $Q$ as running sums over the strongest $k$ states, so line L5 computes each candidate rate exactly once, and line L6 keeps the largest. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), line L1 sorts in $O(K \log K)$ time, and the loop does $O(1)$ work per state, so the time is $O(K \log K)$ and the extra space is $O(K)$. When the states arrive sorted, as in a table of quantized SNR levels, the time is $O(K)$. For a continuous distribution with a closed form such as Rayleigh, each evaluation of $R(\gamma_0)$ costs one evaluation of $E_1$, and a golden section search needs about $\log_{1.618}(1/\epsilon)$ evaluations. The policy is computed once per channel distribution; at run time it costs one division per channel state.

## Properties

- **Constant received SNR.** One fixed code and one fixed modulation work in every served state. This is its main practical advantage over water-filling, which needs a different rate in each state.
- **Zero rate without truncation on Rayleigh fading.** $\mathbb{E}[1/\gamma] = \infty$ for the exponential distribution, so full inversion has $\sigma = 0$. Diversity changes this: with $L \ge 2$ branches of maximal ratio combining, $\mathbb{E}[1/\gamma]$ is finite.
- **Not capacity-achieving.** It spends the most power where the channel is weakest, the reverse of water-filling. Its rate is at most the water-filling capacity, which is at most $\log_2(1 + \mathbb{E}[\gamma])$ by Jensen's inequality.
- **Outage.** The cutoff sets the outage probability $\Pr(\gamma < \gamma_0)$, which is 0.261 at the best cutoff for Rayleigh fading at 10 dB. A delay-sensitive service can fix the outage first and accept the rate it gets; this is the outage capacity.
- **Sensitive to estimation errors.** A deep fade that the transmitter misreads leads to large power errors near the cutoff.

## Variants and improvements

- **Full channel inversion.** $\gamma_0 = 0$, the zero-outage capacity $\log_2(1 + 1/\mathbb{E}[1/\gamma])$. It is useful only when $\mathbb{E}[1/\gamma]$ is small, for example with diversity.
- **Fixed outage.** Choose $\gamma_0$ so that $\Pr(\gamma < \gamma_0) = p_{\mathrm{out}}$ instead of maximizing the rate.
- **Discrete rates.** [Adaptive modulation](/adaptive-modulation/) changes the constellation with $\gamma$ instead of holding the SNR constant. Combined forms invert the channel inside each region of a constellation, so the received SNR is just at the threshold of the constellation in use.
- **Water-filling over time.** $P(\gamma)/\bar P = \max(0, 1/\gamma_0 - 1/\gamma)$ with a variable rate attains the capacity with side information at both ends; see [water-filling](/water-filling-power-allocation/).
- **Closed-loop power control.** Cellular uplinks, such as CDMA, use fast power control steps to keep the received SNR near a target. This is a form of channel inversion that also solves the [near-far problem](/near-far-problem/); an outer loop moves the target.

## When to use it

Use it when the transmitter knows the channel, the codec or the service wants a fixed rate, and a small outage is acceptable, as for voice. When the rate may vary, adaptive modulation or water-filling gives more. On channels with strong diversity, the loss from inversion is small, and full inversion without truncation may be enough.

## Pitfalls

- **Inverting without a cutoff on Rayleigh fading.** The required mean power is unbounded; a simulation with a finite sample hides this and shows a rate that falls as the sample grows.
- **Using the received SNR in place of the channel SNR.** $\gamma$ is the SNR at the average power, before the policy changes the power.
- **Peak power.** Near the cutoff the power is $\bar P \sigma/\gamma_0$, which can be several times the mean. A real amplifier limits this, and the analysis must include the limit.
- **dB values.** The sums use linear SNR values.
- **Cutoffs between states.** For a discrete distribution, a cutoff between two states is the same as the next state above it; searching a fine grid wastes time without changing the answer.

## Implementations

## History

Channel inversion is the idea behind the power control of cellular CDMA systems, which keep the received power of every user at the same level. Goldsmith and Varaiya, in their 1997 paper on the capacity of fading channels with side information, derived the capacity when both ends know the channel, which uses water-filling in time, and compared it with the rates of channel inversion and truncated inversion, which keep the received SNR constant. On Rayleigh fading, inversion without truncation gives zero rate. Goldsmith's textbook calls the rate of channel inversion the zero-outage capacity and the rate of truncated inversion the outage capacity, and Tse and Viswanath make the same comparison with water-filling.

## References
