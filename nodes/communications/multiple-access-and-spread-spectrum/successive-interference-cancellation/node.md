---
tag: TZZ989
kind: algorithm
slug: successive-interference-cancellation
name: Successive interference cancellation
aliases:
- SIC
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Decides the strongest user, subtracts its rebuilt signal, and repeats. With Gaussian codes and whole codewords decoded, the same idea reaches the corner points of the MAC capacity region."
solves: [multiuser-detection]
model: real-ram
complexity:
  vars: {K: the number of users, N: the number of chips per symbol}
  time: {worst: O(K^2 N)}
  space: {extra: O(K^2)}
properties: {deterministic: true, linear: false, needs_amplitudes: optional, needs_noise_level: false, error_propagation: true, order_dependent: true}
history:
  year: 1994
  people: [Pulin Patel, Jack M. Holtzman]
  note: "Patel and Holtzman analyzed successive interference cancellation for direct-sequence CDMA, with amplitudes estimated from the matched filter outputs."
prereqs: [multiuser-detection, matched-filter]
see_also: [parallel-interference-cancellation, mac-capacity-region, non-orthogonal-multiple-access, superposition-coding, v-blast, decision-feedback-equalizer, near-far-problem, mmse-multiuser-detector]
sources:
  - paper: doi:10.1109/49.298053
    title: "Pulin Patel and Jack M. Holtzman, Analysis of a simple successive interference cancellation scheme in a DS/CDMA system, IEEE Journal on Selected Areas in Communications 12(5), 1994"
    locator: "pp. 796 to 807 (the scheme, its amplitude estimates, and its error analysis)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 7, Decision-driven multiuser detectors"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 6.1.1, Capacity via successive interference cancellation, and Section 8.3.2, MMSE-SIC"
---

Successive interference cancellation, or SIC, solves the [multiuser detection](/multiuser-detection/) problem one user at a time. It decides the strongest user with its [matched filter](/matched-filter/), rebuilds that user's signal from the decision, subtracts it from the received signal, and repeats with the next strongest user on what is left. Each step faces fewer interferers than the one before, and the last user sees none. The cost is $K$ matched filters and $K$ subtractions, so SIC is much cheaper than the [optimum detector](/optimum-multiuser-detector/) and needs no matrix inverse. It works best when the users have very different powers, which is the case where the plain matched filter fails, the [near-far problem](/near-far-problem/). Its weakness is error propagation: a wrong decision doubles the interference it was meant to remove. In information theory the same idea, applied to whole codewords of Gaussian codes, reaches the corner points of the [MAC capacity region](/mac-capacity-region/), and it is the receiver of [NOMA](/non-orthogonal-multiple-access/) and of [V-BLAST](/v-blast/).

## In plain words

When many people talk at once, the loudest voice is the easiest to understand. SIC listens to the loudest user first and decides what it said. It then knows what that user's signal looked like, so it takes it out of the recording. Now the second loudest user is the loudest one left, and it is easier to hear without the first. The receiver goes on in this way until it has heard everyone. The quietest user comes last, when nobody else is left to drown it out. If the receiver gets an early user wrong, it takes out the wrong signal, and that mistake makes the later users harder to hear.

## The problem

User $k = 1, \ldots, K$ sends one bit $b_k \in \{-1, +1\}$ per symbol interval with amplitude $A_k > 0$ and a signature $s_k$ of $N$ chips with $\|s_k\| = 1$. The users are synchronous, so the received chips in one interval are $y = S A b + w$, with $S = [s_1, \ldots, s_K]$, $A = \mathrm{diag}(A_k)$ and $w \sim \mathcal{N}(0, \sigma^2 I)$. The receiver knows the signatures, and it may or may not know the amplitudes. The output is a decision $\hat b_k$ for each user. The matched filter outputs are $z = S^\top y = R A b + n$, with $R = S^\top S$ and $n \sim \mathcal{N}(0, \sigma^2 R)$.

## The algorithm

```pseudo id=main
SIC(z, R, A)                      ▷ A may be unknown
L1  π ← the users sorted by A_k, or by |z_k|, largest first
L2  for i ← 1 to K, with k = π_i
L3      x_k ← z_k - Σ_{l<i} R_{k π_l} â_{π_l} b̂_{π_l}   ▷ cancel the users decided so far
L4      b̂_k ← sgn(x_k)
L5      â_k ← A_k if known, else |x_k|
L6  return b̂
```

Line L1 fixes the order. With known amplitudes it sorts by $A_k$; without them it sorts by $|z_k|$, which is a rough measure of strength. Line L3 is the matched filter output of user $k$ after the rebuilt signals $\hat a_j \hat b_j s_j$ of the earlier users are subtracted from $y$: since $s_k^\top s_j = R_{kj}$, the subtraction can be done on $z$ with the crosscorrelations or directly on the $N$ chips of $y$. Line L4 decides the bit, with $+1$ for a zero output. Line L5 keeps the amplitude used to rebuild the signal. With $\hat a_k = |x_k|$, the rebuilt signal is $x_k s_k$, as in the scheme of Patel and Holtzman.

## Example

Three users with $N = 8$ chips use $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$, so $R_{12} = 0.5$, $R_{13} = 0.25$ and $R_{23} = -0.25$. The amplitudes are $A = (1, 4, 2)$, the bits are $b = (+1, -1, +1)$, and $\sigma = 0.5$. One noisy draw gave $z = (-0.47, -4.21, 2.18)$, and the matched filter decides user 1 wrong. With known amplitudes, line L1 gives the order 2, 3, 1:

| step | user | line L3 | $x_k$ | $\hat b_k$ |
|---|---|---|---|---|
| 1 | 2 | $-4.21$ | $-4.21$ | $-1$ |
| 2 | 3 | $2.18 - (-0.25)(4)(-1)$ | $1.18$ | $+1$ |
| 3 | 1 | $-0.47 - (0.5)(4)(-1) - (0.25)(2)(+1)$ | $1.03$ | $+1$ |

All three decisions are right. With estimated amplitudes, $x_3 = 2.18 - (-0.25)(-4.21) = 1.13$ and $x_1 = -0.47 - (0.5)(-4.21) - (0.25)(1.13) = 1.35$, also right here. In a simulation of 400,000 intervals with known amplitudes, user 1 erred at a rate of about 0.023, close to its single-user bound $Q(2) = 0.0228$, and user 3 at about $1.1 \times 10^{-4}$, better than the decorrelator ($2.7 \times 10^{-4}$) and the MMSE detector ($1.7 \times 10^{-4}$). With estimated amplitudes the rates were about 0.18 and $5.6 \times 10^{-4}$. The reason is that $x_2$ also holds $R_{21} A_1 b_1$, so subtracting $R_{12} x_2$ from user 1 also removes a quarter of user 1's own signal.

## Correctness

**Claim.** Without noise and with known amplitudes, SIC decides every bit right if, in the order $\pi$, each user is stronger than the interference of the users after it: $A_{\pi_i} > \sum_{l > i} A_{\pi_l} |R_{\pi_i \pi_l}|$ for every $i$. With noise, the first user has the matched filter error rate, and user $\pi_i$ errs with probability at most $q_1 + \cdots + q_i$, where $q_l$ is the matched filter error rate of user $\pi_l$ in the system of the users $\pi_l, \ldots, \pi_K$ alone.

**Key step.** If the first $i - 1$ decisions are right, line L3 removes their terms exactly, so $x_k = A_k b_k + \sum_{l > i} R_{k \pi_l} A_{\pi_l} b_{\pi_l} + n_k$, the matched filter output in a smaller system. Induction on $i$ gives both statements. The full proof is in the proofs folder.

The condition fails with equal powers. Three equal users with $R_{12} = R_{13} = 0.75$ and $b = (+1, -1, -1)$ give $z_1 = -0.5$, a wrong first decision without any noise.

## Complexity

With $z$ and $R$, which cost $O(K N)$ and $O(K^2 N)$, line L1 costs $O(K \log K)$ and step $i$ of line L3 costs $O(i)$, so the loop costs $O(K^2)$ in the [real RAM](/real-ram/). Done on the chips, each step correlates $N$ chips with $s_k$ and subtracts $N$ chips, so the whole detector costs $O(K N + K \log K)$ without forming $R$. The steps are sequential, so the delay grows with $K$.

## Properties

- **Ordered.** The result depends on the order. Deciding a weak user first fails, since it faces the full interference of the strong users.
- **Benefits from unequal powers.** The more the powers differ, the better the condition of the claim holds. Equal powers are the worst case.
- **Error propagation.** A wrong decision gives $b - \hat b = 2b$ in the residual, which doubles that user's interference on all later users.
- **No matrix inverse and no noise level.** It needs the signatures, and the amplitudes or their estimates.
- **The first user sees all the interference.** It is decided by its matched filter, so its error rate depends on the other users' powers and bits.
- **Capacity achieving at the codeword level.** With Gaussian codebooks, decoding whole codewords in order and subtracting them reaches the corner points of the capacity region of the Gaussian multiple access channel, and time sharing between orders gives the rest of the dominant face (Tse and Viswanath, Section 6.1.1). That result needs codes with a vanishing error probability, not single bits decided by their sign.

## Variants and improvements

- **MMSE-SIC.** Replace the matched filter in each step by an [MMSE filter](/mmse-multiuser-detector/) against the users not yet decided. With Gaussian codes this reaches the sum capacity, and it is the receiver of V-BLAST.
- **Decorrelating decision feedback.** Whiten with the Cholesky factor of $R$ and cancel in order; it is the multiuser form of the [decision feedback equalizer](/decision-feedback-equalizer/).
- **Soft cancellation.** Subtract $\hat a_k \tanh(\cdot)$ or a clipped value instead of a hard decision, which limits the damage of a wrong decision.
- **Power allocation for SIC.** Choose the powers so that each user's SINR, after the users before it are removed, meets a target; this is the design rule of power domain NOMA.
- **Parallel form.** Cancel all users at once in stages, which is [parallel interference cancellation](/parallel-interference-cancellation/).

## When to use it

Use SIC when the users have very different received powers, when the receiver must be cheap, or when the users send coded data that can be decoded and re-encoded before subtraction, as in NOMA and in uplink receivers. Do not use it when the powers are almost equal and the correlations are large; then a linear detector or parallel cancellation started from a linear detector is safer.

## Pitfalls

- **Wrong order.** Sorting by $|z_k|$ in a single interval is noisy. Average the strength over many intervals before ordering.
- **Amplitude estimates that hold the user's own signal.** $|x_k|$ also holds interference and noise, and subtracting $x_k s_k$ can remove part of a later user's own signal, as the example shows.
- **Error propagation.** One wrong early decision spoils the later users. Use soft decisions or decoded codewords when the error rate of the first users is not small.
- **Latency.** The $K$ steps run in sequence. For many users, group the users and cancel each group in parallel.
- **Reading the capacity result as a bit-level fact.** Corner-point optimality holds for whole Gaussian codewords, not for the uncoded sign decisions of this page.

## Implementations

## History

The idea of decoding one user, subtracting it, and decoding the next is old in information theory, where successive decoding is the standard proof that the corner points of the multiple access capacity region are achievable. For uncoded direct-sequence CDMA, Patel and Holtzman analyzed a simple scheme in 1994 that orders the users by their matched filter outputs and uses those outputs as amplitude estimates. Verdú's 1998 book treats SIC among the decision-driven detectors. In the 2010s, SIC became the receiver of power domain NOMA, where the transmitter assigns the powers to make the cancellation order work.

## References
