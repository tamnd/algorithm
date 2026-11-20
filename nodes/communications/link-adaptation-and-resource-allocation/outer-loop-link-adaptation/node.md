---
tag: ZM1GV1
kind: algorithm
slug: outer-loop-link-adaptation
name: Outer loop link adaptation
aliases:
- OLLA
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Subtracts a backoff offset from the reported SINR before choosing the modulation and coding scheme; the offset grows on each NACK and shrinks on each ACK, so the BLER meets a target."
solves: [link-adaptation]
model: real-ram
complexity:
  vars: {n: the number of transmissions, J: the number of modulation and coding schemes}
  time: {worst: O(n log J)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, feedback_driven: true, needs_model: false}
history:
  year: 2007
  people: [Klaus I. Pedersen, Guillaume Monghal, Istvan Z. Kovacs, Troels E. Kolding, Akhilesh Pokhariyal, Frank Frederiksen, Preben Mogensen]
  note: "Pedersen and coauthors described an outer loop that offsets the reported SINR from HARQ acknowledgments, with the down step equal to the up step times BLER_T/(1 - BLER_T), in a study of OFDMA scheduling with noisy channel feedback."
prereqs: [link-adaptation, hybrid-arq]
see_also: [link-adaptation, effective-snr-mapping, adaptive-modulation, hybrid-arq, stochastic-approximation, foschini-miljanic-power-control, binary-search, chase-combining]
sources:
  - paper: doi:10.1109/VETECF.2007.378
    title: "Klaus I. Pedersen, Guillaume Monghal, Istvan Z. Kovacs, Troels E. Kolding, Akhilesh Pokhariyal, Frank Frederiksen and Preben Mogensen, Frequency domain scheduling for OFDMA with limited and noisy channel feedback, IEEE Vehicular Technology Conference (VTC 2007-Fall), pages 1792 to 1796"
    locator: "the outer loop link adaptation offset, updated from ACK and NACK feedback with the down step set by the BLER target"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 9 (adaptive modulation and coding, and the effect of channel estimation error and feedback delay)"
---

Outer loop link adaptation (OLLA) corrects the channel quality reports that [link adaptation](/link-adaptation/) relies on. The inner loop maps a reported SINR $\hat\gamma$ (in dB) to the fastest modulation and coding scheme whose threshold it meets. The reports are biased by estimation error, delay and model error, so the block error rate (BLER) misses its target $\beta_T$. OLLA keeps one number, a backoff offset $\Delta$ in dB, and uses $\hat\gamma - \Delta$ in the lookup. After each transmission it reads the HARQ feedback: a NACK raises $\Delta$ by $\Delta_{\mathrm{up}}$, which makes the next choices more cautious, and an ACK lowers it by $\Delta_{\mathrm{down}} = \Delta_{\mathrm{up}}\beta_T/(1 - \beta_T)$. With these steps, an exact identity ties the NACK fraction to the offset: if the offset stays bounded, the NACK fraction tends to $\beta_T$, whatever the channel does. It costs $O(1)$ work per acknowledgment.

## In plain words

The receiver tells the sender how good the channel is, and the sender picks a speed from a table. But the reports are often a little too hopeful or too gloomy, so too many or too few packets fail.

OLLA fixes this with one number, a safety margin. The sender takes the margin off each report before it looks at the table. Each time a packet fails, the margin goes up by a large step. Each time a packet gets through, it goes down by a small step. If the goal is that one packet in ten fails, the large step is nine times the small one. Then nine successes and one failure leave the margin where it was, and in the long run about one packet in ten fails.

## The problem

There are $J$ schemes with increasing thresholds $\theta_1 < \cdots < \theta_J$ (in dB), set so that scheme $j$ has the BLER $\beta_T$ at the SINR $\theta_j$ on a reference channel. Transmission $n$ comes with a report $\hat\gamma_n$. The transmitter picks a scheme, sends, and receives an ACK or a NACK. The reports have an unknown and possibly slowly changing error. The goal is a long-run fraction of NACKs equal to $\beta_T$, with the fastest schemes that allow it. The algorithm does not need to know the error model or the BLER curves.

## The algorithm

```pseudo id=main
OLLA(θ[1..J], β_T, Δ_up, Δ_0, the reports γ̂_1, γ̂_2, ...)
L1  Δ_down ← Δ_up · β_T / (1 - β_T);  Δ ← Δ_0
L2  for n = 1, 2, ... do
L3      γ_adj ← γ̂_n - Δ                       ▷ back off the report
L4      j ← the largest j with θ_j ≤ γ_adj, or 1 if none   ▷ binary search
L5      send with scheme j and receive ACK or NACK
L6      if NACK then Δ ← Δ + Δ_up
L7      else Δ ← Δ - Δ_down
L8      clamp Δ to [Δ_min, Δ_max] if bounds are given
```

The offset is in dB and is subtracted, so a positive offset means the reports are believed to be too high. Some texts add an offset instead, with the opposite signs; the rule is the same.

## Example

Take $\beta_T = 0.1$ and $\Delta_{\mathrm{up}} = 0.5$ dB, so $\Delta_{\mathrm{down}} = 0.5 \cdot 0.1/0.9 = 0.0556$ dB. From $\Delta = 0$, nine ACKs bring the offset to $-0.5$ dB, and one NACK brings it back to 0. Ten transmissions with exactly one NACK, in any order, leave the offset unchanged; more NACKs push it up, fewer push it down.

A simulation shows the effect. The five schemes of the [link adaptation](/link-adaptation/) example have rates $(0.5, 1, 2, 3, 4.5)$ bits per symbol and the model BLER curves $1/(1 + e^{1.5(\gamma - t_j)})$ with $t = (-2, 1, 6, 10, 15)$ dB; the thresholds are the 10% points. The true SINR is uniform on $[0, 20]$ dB, and each report adds a fixed bias and Gaussian noise with a standard deviation of 1 dB. Over 20000 transmissions with a fixed seed (computed values):

| report bias | NACK rate, table alone | throughput, table alone | NACK rate, with OLLA | throughput, with OLLA | mean offset, second half |
|---|---|---|---|---|---|
| +3 dB (too hopeful) | 0.300 | 2.00 | 0.100 | 2.23 | 1.84 dB |
| 0 dB | 0.032 | 2.18 | 0.100 | 2.23 | -1.20 dB |
| -3 dB (too gloomy) | 0.002 | 1.67 | 0.100 | 2.23 | -4.19 dB |

With OLLA the NACK rate and the throughput do not depend on the bias, and the learned offsets differ by the 3 dB steps of the bias. Even with no bias the offset is not zero: the reports are noisy and the true SINR is spread over each scheme's range, so the table alone fails less often than 10%, and the loop moves to faster schemes.

## Correctness

**Claim.** Let $A_n$ be the number of NACKs among the first $n$ transmissions. Without the bounds of line L8, for every $n$ and every sequence of feedback,

$$\frac{A_n}{n} = \beta_T + \frac{(1 - \beta_T)(\Delta_n - \Delta_0)}{n\,\Delta_{\mathrm{up}}}.$$

So if the offset stays in an interval of length $W$, the NACK fraction is within $(1 - \beta_T)W/(n\Delta_{\mathrm{up}})$ of the target.

**Key steps.** After $n$ steps the offset is $\Delta_0 + A_n\Delta_{\mathrm{up}} - (n - A_n)\Delta_{\mathrm{down}}$, by induction. Solving for $A_n$ and using $\Delta_{\mathrm{down}}/(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}}) = \beta_T$, which is how line L1 chooses the down step, gives the identity. The identity uses no model of the channel. Whether the offset stays bounded does depend on the channel: if more backoff gives fewer NACKs, the expected step $(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})(p(\Delta) - \beta_T)$ points back to the balance point, a stochastic approximation argument. If even the slowest scheme fails more often than $\beta_T$, the offset grows without bound, and the identity explains why. The full proof is in the proofs folder.

## Complexity

Each transmission takes one subtraction, one binary search over the $J$ thresholds and one update, so $n$ transmissions take $O(n \log J)$ time. The state is one number, so the extra space is $O(1)$ beyond the threshold table. With a uniform grid of thresholds, the lookup is $O(1)$ by division.

## Properties

- **Model free.** The update uses only ACKs and NACKs. It does not need the error model of the reports or the BLER curves.
- **Exact balance.** The step ratio $\Delta_{\mathrm{up}}/\Delta_{\mathrm{down}} = (1 - \beta_T)/\beta_T$ is the only choice for which the expected step is zero exactly when the NACK probability is $\beta_T$.
- **Sawtooth.** The offset never settles; it moves in a sawtooth around the balance point, with a spread that grows with $\Delta_{\mathrm{up}}$.
- **Speed against noise.** A large step tracks a changing bias quickly but adds noise to the choice of scheme; a small step is smooth but slow. After a jump of $D$ dB in the bias, the offset needs about $D/\Delta_{\mathrm{down}}$ transmissions to follow it downwards, and about $D/\Delta_{\mathrm{up}}$ NACKs to follow it upwards.
- **Target, not optimum.** OLLA meets a BLER target. It does not search for the throughput-best BLER, which can differ from the target.

## Variants and improvements

- **One offset per user, or per user and layer.** In cellular systems each link has its own loop; with several layers each layer can have one.
- **Bounded offset.** Line L8 keeps the offset in a window, so a long run of errors from an outage does not make the loop too cautious for a long time afterwards.
- **Variable steps.** A large step at the start of a connection and a smaller one later gives a fast start and a smooth steady state.
- **Feedback from the first transmission only.** With [hybrid ARQ](/hybrid-arq/), the loop usually counts the ACK or NACK of the first transmission of each block, because the target is a first-transmission BLER.
- **Throughput-seeking loops.** Some designs move the target itself, for example by comparing the throughput at two targets, to find the best BLER for the channel.
- **The same rule elsewhere.** The outer loop of power control in CDMA sets the SIR target with the same up and down steps, using frame errors instead of HARQ feedback.

## When to use it

Use it whenever a link chooses its scheme from quality reports and gets ACK or NACK feedback: the cost is a few operations per packet, and it removes biases that are hard to model, such as receiver differences between devices, report delay and a mapping like [EESM](/effective-snr-mapping/) with a slightly wrong parameter. Use a small step when the bias changes slowly and the traffic is steady; use a larger one, or bounds, when traffic comes in bursts.

## Pitfalls

- **Sparse traffic.** The loop learns one step per packet. With little traffic, the offset stays at its start value or follows an old bias.
- **Counting retransmissions.** If the loop counts the feedback of retransmissions, which succeed more often, it aims at a different BLER than intended.
- **Unbounded growth.** In an outage, every packet fails, and without a bound the offset grows for as long as the outage lasts. When the channel recovers, the loop is far too cautious.
- **Wrong sign.** The offset is subtracted from the report. Adding it, with the same step signs, makes the loop unstable: each NACK makes the next choice more aggressive.
- **A fixed step ratio with a changed target.** If the BLER target changes, $\Delta_{\mathrm{down}}$ must change with it; otherwise the loop converges to the old target.

## Implementations

## History

Pedersen, Monghal, Kovács, Kolding, Pokhariyal, Frederiksen and Mogensen, in "Frequency domain scheduling for OFDMA with limited and noisy channel feedback" at VTC 2007-Fall, studied OFDMA scheduling when the channel quality reports are coarse and noisy. Their link adaptation corrects the reports with an offset learned from HARQ acknowledgments, with the down step set by the BLER target as above. The step rule is the same as that of the outer loop of power control in CDMA systems, which sets an SIR target from frame errors.

## References
