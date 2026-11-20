---
tag: H2AQFV
kind: algorithm
slug: optimum-multiuser-detector
name: Optimum multiuser detector
aliases:
- Verdu detector
- jointly optimum multiuser detector
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: "The maximum likelihood detector of the bits of all CDMA users: a matched filter bank and a Viterbi search over 2^(K-1) states, exponential in the number of users K."
solves: [multiuser-detection]
model: real-ram
complexity:
  vars: {K: the number of users, M: the number of symbols per user, N: the number of chips per symbol}
  time: {worst: O(M K^2 (2^K + N))}
  space: {extra: O(2^K K M)}
properties: {deterministic: true, maximum_likelihood: true, exponential_in_users: true, needs_amplitudes: true, needs_noise_level: false, handles_asynchronous_users: true}
history:
  year: 1986
  people: [Sergio Verdú]
  note: "Verdú showed that the jointly optimum detector for asynchronous Gaussian CDMA is a bank of matched filters followed by a Viterbi algorithm with 2^(K-1) states, and computed its asymptotic efficiency."
prereqs: [multiuser-detection, viterbi-algorithm]
see_also: [multiuser-detection-np-hardness, decorrelating-detector, mmse-multiuser-detector, successive-interference-cancellation, near-far-problem, minimum-distance-detector, semidefinite-relaxation-detection, fincke-pohst-enumeration]
sources:
  - paper: doi:10.1109/TIT.1986.1057121
    title: "Sergio Verdú, Minimum probability of error for asynchronous Gaussian multiple-access channels, IEEE Transactions on Information Theory 32(1), 1986"
    locator: "pp. 85 to 96 (the matched filter bank, the Viterbi algorithm with 2^(K-1) states and complexity O(2^K) per bit, and the asymptotic efficiency of the optimum detector)"
  - paper: doi:10.1109/milcom.1983.4794684
    title: "Sergio Verdú, Minimum probability of error for asynchronous multiple access communication systems, IEEE Military Communications Conference (MILCOM), 1983"
    locator: "pp. 213 to 219 (the first presentation of the optimum detector)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 4, Optimum multiuser detection"
  - paper: doi:10.1007/BF01553893
    title: "Sergio Verdú, Computational complexity of optimum multiuser detection, Algorithmica 4, 1989"
    locator: "pp. 303 to 312 (the synchronous problem is NP-hard in the number of users)"
  - paper: doi:10.1109/18.705573
    title: "C. Sankaran and A. Ephremides, Solving a class of optimum multiuser detection problems with polynomial complexity, IEEE Transactions on Information Theory 44(5), 1998"
    locator: "pp. 1958 to 1961 (nonpositive crosscorrelations give a minimum cut problem)"
---

The optimum multiuser detector decides the bits of all users of a [CDMA](/code-division-multiple-access/) channel jointly, by maximum likelihood. It is the best possible answer to the [multiuser detection](/multiuser-detection/) problem: no other detector has a smaller probability of deciding a wrong frame, and it is fully resistant to the [near-far problem](/near-far-problem/). Verdú found its structure in 1983 to 1986. A bank of [matched filters](/matched-filter/), one per user, gives sufficient statistics, and a [Viterbi algorithm](/viterbi-algorithm/) with $2^{K-1}$ states searches the bit sequences of the $K$ users. The cost per bit is exponential in $K$. This is not a weakness of the method: the problem itself is [NP-hard](/multiuser-detection-np-hardness/) in $K$. The detector is the reference against which the cheaper detectors are measured: the [decorrelator](/decorrelating-detector/), the [MMSE detector](/mmse-multiuser-detector/), [successive](/successive-interference-cancellation/) and [parallel](/parallel-interference-cancellation/) interference cancellation.

## In plain words

Several users send at the same time on the same band, each with its own spreading code. Their signals add up at the receiver, with noise. The optimum detector asks: of all the bit patterns the users could have sent, which one makes a received signal closest to what arrived? Checking every pattern is far too slow for long frames, but each bit overlaps only a few bits of the other users. So the detector works through the bits in time order and keeps, for each pattern of the last few bits, only the best history that ends in it. This is the Viterbi algorithm. The number of patterns it keeps doubles with each extra user, so the method is practical only for a small number of users.

## The problem

User $k = 1, \ldots, K$ sends bits $b_k[0], \ldots, b_k[M-1] \in \{-1, +1\}$ with amplitude $A_k > 0$ and a signature $s_k$ of $N$ chips with $\|s_k\| = 1$. The user starts $\tau_k$ chips late, $0 \le \tau_k < N$. The receiver sees the chip samples

$$y[n] = \sum_{k} A_k \sum_{i} b_k[i]\, s_k[n - iN - \tau_k] + w[n],$$

with $w[n]$ independent $\mathcal{N}(0, \sigma^2)$. This is the in-phase part of the complex baseband model for coherent BPSK, with $\sigma^2 = N_0/2$, so $A_k^2 / \sigma^2 = 2 E_b / N_0$ for user $k$. The receiver knows the signatures, the delays and the amplitudes. The output is the frame $b$ that maximizes the likelihood, which is the frame that minimizes $\|y - \sum_k A_k \sum_i b_k[i]\, s_k[\cdot - iN - \tau_k]\|^2$. With all delays 0, one interval is the synchronous model $y = S A b + w$: the frame maximizes $2 b^\top A z - b^\top A R A b$, where $z = S^\top y$ and $R = S^\top S$.

## The algorithm

Sort the $KM$ bits by their first chip and call them $t = 0, 1, \ldots, KM - 1$. Write $a_t$ for the amplitude of bit $t$, $u_t$ for its shifted signature, $z_t = \langle u_t, y \rangle$ for its matched filter output, and $\rho_{t,v} = \langle u_t, u_v \rangle$. A bit overlaps only the $K - 1$ bits before it and the $K - 1$ bits after it, so the log-likelihood is a sum of terms that each depend on one bit and the $K - 1$ bits before it.

```pseudo id=main
OPTIMUM-MUD(y, s, τ, A, M)
L1  sort the K M bits by their first chip i N + τ_k
L2  for each bit t: z_t ← ⟨u_t, y⟩ and ρ_{t,t-d} ← ⟨u_t, u_{t-d}⟩ for 1 ≤ d ≤ min(t, K - 1)
L3  metric[empty state] ← 0
L4  for t ← 0 to K M - 1
L5      for each state σ = (b_{t-1}, .., b_{t-min(t,K-1)}) and each b_t ∈ {+1, -1}
L6          λ ← 2 a_t b_t (z_t - Σ_d a_{t-d} b_{t-d} ρ_{t,t-d})      ▷ the branch metric
L7          candidate for the state σ' = (b_t, .., b_{t-K+2}) is metric[σ] + λ
L8      metric[σ'] ← the best candidate of σ', and its survivor ← the survivor of that σ, then b_t
L9  return the survivor of the state with the largest metric
```

Line L1 puts the bits in time order; for synchronous users with $M = 1$ this is just the user order. Line L2 is the matched filter bank and the correlations of overlapping bits. Line L6 is the gain in likelihood from deciding $b_t$, given the bits that overlap it from the left. Lines L7 and L8 are the add-compare-select step of the Viterbi algorithm on a trellis whose state is the last $K - 1$ bits, so there are $2^{K-1}$ states after the first $K - 1$ bits. Line L9 picks the best final state and returns its history, which is put back as $b_k[i]$ by user and symbol.

## Example

Three synchronous users with $N = 8$ chips use the signatures $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$, so $R_{12} = 0.5$, $R_{13} = 0.25$ and $R_{23} = -0.25$. The amplitudes are $A = (1, 4, 2)$ and the bits sent are $b = (+1, -1, +1)$. Without noise the matched filters give $z = R A b = (-0.5, -4, 3.25)$; user 1 has the wrong sign, because user 2 is four times stronger. With noise of $\sigma = 0.5$, one draw gave $z = (-0.47, -4.21, 2.18)$. The table lists the metric $\Omega(b) = 2 b^\top A z - b^\top A R A b$ of every candidate.

| $b_1$ | $b_2$ | $b_3$ | $\Omega(b)$ |
|---|---|---|---|
| +1 | +1 | +1 | -47.90 |
| +1 | +1 | -1 | -71.34 |
| +1 | -1 | +1 | **19.46** |
| +1 | -1 | -1 | 12.02 |
| -1 | +1 | +1 | -36.02 |
| -1 | +1 | -1 | -63.46 |
| -1 | -1 | +1 | 15.34 |
| -1 | -1 | -1 | 3.90 |

The largest metric, 19.46, belongs to the sent bits $(+1, -1, +1)$. The signs of $z$ give $(-1, -1, +1)$, with the metric 15.34, so the conventional receiver gets user 1 wrong. The trellis of lines L4 to L8 has three steps here. After the last step it keeps 4 states, one for each value of $(b_2, b_3)$, and each holds the better of the two rows that differ only in $b_1$. The best of the four is the row in bold.

## Correctness

**Claim.** The detector returns a frame that maximizes the likelihood of $y$ over all $2^{KM}$ frames.

**Key step.** If two bits are $K$ or more places apart in time order, they start at least $N$ chips apart, because each user has at most one bit starting in any window of $N$ chips. So their waveforms do not overlap, and $-\|y - \text{signal}\|^2$ is a constant plus $\sum_t \lambda_t$, where $\lambda_t$ depends only on $b_t$ and the $K - 1$ bits before it. The Viterbi invariant then holds: after step $t$, each state stores the best partial sum over all histories that end in it. The full proof is in the proofs folder.

## Complexity

Line L2 costs $O(K N)$ per bit, $O(M K^2 N)$ in all. The search visits at most $2^{K-1}$ states per bit with two branches each, and the interference sum of line L6 has at most $K - 1$ terms, so it costs $O(K 2^K)$ per bit and $O(M K^2 2^K)$ in all in the [real RAM](/real-ram/). Building the interference sums of all states one bit at a time removes the factor $K$ and gives the $O(2^K)$ per bit of Verdú's paper. The survivors need $O(2^K K M)$ space, or $O(2^K D)$ with a fixed decision depth $D$. For one synchronous interval the search is a brute force over $2^K$ vectors in disguise, and no polynomial algorithm is expected, because the problem is NP-hard.

## Properties

- **Optimal for the frame.** It minimizes the probability that the decided frame differs from the sent frame, for equally likely bits. The individually optimum detector, which minimizes the error probability of each bit, uses posterior probabilities instead of a maximum; at high SNR the two behave the same.
- **Near-far resistant.** Its asymptotic efficiency stays positive however strong the other users are, as long as the signatures are linearly independent. Lupas and Verdú showed that the decorrelator has the same near-far resistance.
- **Needs the amplitudes.** The branch metric uses $A_k$; the noise level $\sigma$ is not needed for the maximum likelihood frame.
- **Exponential in $K$, linear in $M$.** The trellis has $2^{K-1}$ states whatever the frame length.
- **Error rate.** At high SNR, each user's error rate is close to $Q(d_{\min,k} / (2 \sigma))$ up to a constant factor, where $d_{\min,k}$ is the smallest distance between two noiseless signals whose bits of user $k$ differ.

## Variants and improvements

- **Individually optimum detection.** Replace max by sum in the trellis (the BCJR algorithm) to get the posterior probability of each bit; this gives the minimum bit error rate and soft outputs for a decoder.
- **Sphere decoding.** For the synchronous case, write $\|y - S A b\|^2$ with a [Cholesky](/cholesky-decomposition/) factor of $R$ and search the binary vectors with [Fincke-Pohst](/fincke-pohst-enumeration/) or [Schnorr-Euchner](/schnorr-euchner-enumeration/) enumeration. The answer is still exact, and the average cost is much lower at high SNR.
- **Relaxations.** [Semidefinite relaxation](/semidefinite-relaxation-detection/) solves a convex problem and rounds; it is polynomial and often close to optimal.
- **Polynomial special cases.** When all crosscorrelations are nonpositive, the synchronous problem reduces to a minimum cut and is solvable in polynomial time (Sankaran and Ephremides 1998).
- **Reduced-state trellis.** Keep only the best few states per step, or cancel the far bits with decisions, as in reduced-state sequence estimation.

## When to use it

Use it when $K$ is small, about ten users or fewer, and the signatures and amplitudes are known: as a benchmark in simulations, in a receiver for a few strong users, or as the inner step of an iterative receiver for a small group. For large $K$ use the [MMSE detector](/mmse-multiuser-detector/), [interference cancellation](/successive-interference-cancellation/) or a sphere decoder.

## Pitfalls

- **Wrong amplitudes or delays.** The metric uses $A_k$, $\tau_k$ and the signatures. Errors in these parameters break the optimality, and the result can be worse than a linear detector.
- **Forgetting the edges of the frame.** In the asynchronous case the first and last bits overlap fewer bits. The trellis must start with an empty state and grow, as here, not with $2^{K-1}$ equal states.
- **Delays not in $0, \ldots, N-1$.** A delay of $N$ or more shifts the symbol index. Reduce delays modulo $N$ and renumber the symbols, or the overlap argument fails.
- **Expecting it to scale.** The cost doubles with each user. For $K = 30$ there are about $5 \times 10^8$ states per bit.

## Implementations

## History

Verdú presented the optimum detector for asynchronous Gaussian multiple access channels at MILCOM 1983 and published it in the IEEE Transactions on Information Theory in 1986. He showed that a bank of matched filters gives sufficient statistics and that a Viterbi algorithm with $2^{K-1}$ states finds the maximum likelihood bits, and he computed the asymptotic efficiency of the optimum detector, which showed that the conventional receiver loses much more than necessary in a near-far situation. In 1989 he proved that the synchronous problem is NP-hard in $K$, which explained why the search over states could not be avoided in general. These results started the work on suboptimal multiuser detectors with polynomial cost, collected in his 1998 book.

## References
