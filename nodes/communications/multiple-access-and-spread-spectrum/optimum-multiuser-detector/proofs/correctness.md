---
title: The Viterbi search over 2^(K-1) states returns the bit sequences of maximum likelihood
proves: [correctness]
status: full
---

The receiver sees $y[n] = \sum_{t} a_t b_t\, u_t[n] + w[n]$, with $w[n]$ independent $\mathcal{N}(0, \sigma^2)$. Here $t = 0, \ldots, T - 1$ runs over the $T = KM$ bits in the order of line L1, $a_t > 0$ is the amplitude of the user of bit $t$, $b_t \in \{-1, +1\}$, and $u_t[n] = s_k[n - \mathrm{st}_t]$ is the signature of that user shifted to the start chip $\mathrm{st}_t = iN + \tau_k$ of the bit. Each signature has $\|s_k\| = 1$ and each delay satisfies $0 \le \tau_k < N$. Line L1 sorts the bits by start chip, so $\mathrm{st}_0 \le \mathrm{st}_1 \le \cdots \le \mathrm{st}_{T-1}$. Line L2 computes $z_t = \langle u_t, y \rangle$ and $\rho_{t,t-d} = \langle u_t, u_{t-d} \rangle$ for $1 \le d \le \min(t, K - 1)$.

**Lemma 1 (each bit overlaps at most $K - 1$ bits on each side).** If $v - t \ge K$, then $\mathrm{st}_v - \mathrm{st}_t \ge N$, and so $\langle u_t, u_v \rangle = 0$.

*Proof.* Suppose $\mathrm{st}_v - \mathrm{st}_t < N$. The $v - t + 1 \ge K + 1$ bits $t, t+1, \ldots, v$ all start in the half-open interval $[\mathrm{st}_t, \mathrm{st}_t + N)$. The start chips of one user are $\tau_k, \tau_k + N, \tau_k + 2N, \ldots$, so at most one of them lies in a half-open interval of length $N$. There are only $K$ users, so at most $K$ bits start in the interval, a contradiction. The support of $u_t$ is $[\mathrm{st}_t, \mathrm{st}_t + N)$, so two waveforms whose start chips differ by $N$ or more do not overlap. $\square$

**Lemma 2 (the log-likelihood is a sum of branch metrics).** Let $\Lambda(b) = -\|y - \sum_t a_t b_t u_t\|^2$. Then

$$\Lambda(b) = -\|y\|^2 - \sum_t a_t^2 + \sum_{t=0}^{T-1} \lambda_t, \qquad \lambda_t = 2 a_t b_t \Big( z_t - \sum_{d=1}^{\min(t, K-1)} a_{t-d}\, b_{t-d}\, \rho_{t,t-d} \Big). \tag{1}$$

*Proof.* Expand the square: $\|\sum_t a_t b_t u_t\|^2 = \sum_t a_t^2 b_t^2 \|u_t\|^2 + 2 \sum_{t > v} a_t a_v b_t b_v \langle u_t, u_v \rangle$. Here $b_t^2 = 1$ and $\|u_t\| = 1$, because the shift keeps all $N$ chips inside the frame. By Lemma 1 the cross terms vanish unless $t - v \le K - 1$, so we write $v = t - d$ with $1 \le d \le \min(t, K - 1)$. The linear term is $2 \sum_t a_t b_t \langle u_t, y \rangle = 2 \sum_t a_t b_t z_t$. Collecting the terms of each $t$ gives (1). $\square$

The first two terms of (1) do not depend on $b$. The noise is white and Gaussian, so the likelihood of $y$ given $b$ is proportional to $\exp(\Lambda(b) / (2\sigma^2))$. A sequence that maximizes $\sum_t \lambda_t$ therefore maximizes the likelihood. With independent, equally likely bits, it is also the sequence with the largest posterior probability, so it minimizes the probability that the decided frame differs from the sent frame. Line L6 computes $\lambda_t$ exactly as in (1).

**Lemma 3 (the Viterbi invariant).** A state is a tuple of the last $\min(t, K - 1)$ bits, the most recent last. At the start of iteration $t$ of line L4, for every state $\sigma$ in `metric`, $\mathrm{metric}[\sigma] = \max \sum_{v < t} \lambda_v$ over all bit sequences $b_0, \ldots, b_{t-1}$ whose last bits are $\sigma$, and `survivor[σ]` is one such sequence that attains the maximum. Every possible tuple of length $\min(t, K-1)$ is a key of `metric`.

*Proof.* By induction on $t$. For $t = 0$, line L3 sets the empty state to 0, and the empty sum is 0. Assume the claim at the start of iteration $t$. By (1), $\lambda_t$ depends only on $b_t$ and on $b_{t-1}, \ldots, b_{t - \min(t, K-1)}$, which are exactly the bits in the state $\sigma$. So line L6 evaluates $\lambda_t(\sigma, b_t)$ correctly from $\sigma$ alone. A sequence $b_0, \ldots, b_t$ ends in the new state $\sigma'$, the last $\min(t + 1, K - 1)$ bits, if and only if it is a sequence $b_0, \ldots, b_{t-1}$ ending in some state $\sigma$ followed by a bit $b_t$, with $\sigma'$ the tail of $\sigma$ followed by $b_t$. Its value is $\sum_{v < t} \lambda_v + \lambda_t(\sigma, b_t)$. For a fixed $\sigma$ and $b_t$, the first sum is largest for the survivor of $\sigma$, by the induction hypothesis. Lines L5 to L7 try every pair $(\sigma, b_t)$ and keep, for each $\sigma'$, the largest value and the sequence that reaches it, so line L8 stores the maximum over all sequences that end in $\sigma'$. Every tuple $\sigma'$ is reached, because every $\sigma$ is present and both values of $b_t$ are tried. $\square$

**Theorem 1.** The output of the detector maximizes $\Lambda(b)$ over all $2^{KM}$ frames. It is a jointly maximum likelihood decision.

*Proof.* After the last iteration, Lemma 3 with $t = T$ says that each `metric[σ]` is the best total over the sequences ending in $\sigma$, and every sequence ends in some state. Line L9 takes the best state, so its survivor maximizes $\sum_t \lambda_t$ over all sequences, and by (1) it maximizes $\Lambda$. The final loop only moves each bit $t$ back to its user and symbol index. $\square$

**Corollary (the synchronous case).** With all delays 0 and $M = 1$, the bits are the $K$ users of one interval and every pair overlaps. The detector maximizes $2 b^\top A z - b^\top A R A b$, with $z = S^\top y$ and $R = S^\top S$, over $b \in \{-1, +1\}^K$. This is (1) with $T = K$ and all $\binom{K}{2}$ cross terms present.

**Remark (no noise).** If $w = 0$, the sent frame has $\Lambda = 0$, the largest possible value. Any other frame with $\Lambda = 0$ would give the same noiseless signal. If the shifted signatures $u_t$ are linearly independent, no such frame exists and the detector returns the sent frame. If they are dependent, two frames can give the same signal, and no detector can tell them apart.

**Remark (the cost).** Iteration $t$ visits $2^{\min(t, K-1)}$ states. For each it computes a sum of at most $K - 1$ terms and two branches, so the search costs $O(T K 2^{K}) = O(M K^2 2^K)$ operations. Line L2 costs $O(T K N)$. The interference sums of all $2^{K-1}$ states can instead be built one bit at a time: the sum over the last $j$ bits is the sum over the last $j - 1$ bits plus one term, so all of them cost $2 + 4 + \cdots + 2^{K-1} < 2^K$ additions. With this table the cost per bit is $O(2^K)$, the figure in Verdú's 1986 paper. The number of states, $2^{K-1}$, is the same in both forms.
