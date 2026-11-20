---
title: Successive cancellation decides every bit right without noise when each user dominates the users after it, and each stage sees a smaller system
proves: [correctness]
status: full
---

The model is $y = S A b + w$ for one symbol interval, with unit-norm signatures $s_k$, amplitudes $A_k > 0$, bits $b_k \in \{-1, +1\}$ and $w \sim \mathcal{N}(0, \sigma^2 I_N)$. Let $R = S^\top S$ and $z = S^\top y = R A b + n$, with $n \sim \mathcal{N}(0, \sigma^2 R)$. Line L1 fixes an order $\pi_1, \ldots, \pi_K$ of the users. In step $i$ of line L2, with $k = \pi_i$, line L3 computes

$$x_k = z_k - \sum_{l < i} R_{k \pi_l}\, \hat a_{\pi_l}\, \hat b_{\pi_l}, \tag{1}$$

line L4 sets $\hat b_k = \mathrm{sgn}(x_k)$, and line L5 sets $\hat a_k$ to the known $A_k$ or to the estimate $|x_k|$.

**Lemma 1 (cancelling on z is cancelling on y).** Let $y^{(i)} = y - \sum_{l < i} \hat a_{\pi_l} \hat b_{\pi_l} s_{\pi_l}$ be the received vector after the first $i - 1$ signals are rebuilt and subtracted. Then $x_{\pi_i} = s_{\pi_i}^\top y^{(i)}$.

*Proof.* $s_k^\top y^{(i)} = s_k^\top y - \sum_{l < i} \hat a_{\pi_l} \hat b_{\pi_l}\, s_k^\top s_{\pi_l}$, and $s_k^\top y = z_k$, $s_k^\top s_{\pi_l} = R_{k \pi_l}$. $\square$

**Lemma 2 (what step i sees).** With known amplitudes, if the first $i - 1$ decisions are right, then for $k = \pi_i$

$$x_k = A_k b_k + \sum_{l > i} R_{k \pi_l} A_{\pi_l} b_{\pi_l} + n_k. \tag{2}$$

*Proof.* By Lemma 1, $z_k = A_k b_k + \sum_{j \ne k} R_{kj} A_j b_j + n_k$. With $\hat a_{\pi_l} = A_{\pi_l}$ and $\hat b_{\pi_l} = b_{\pi_l}$ for $l < i$, (1) removes exactly the terms of the users decided before $k$. $\square$

So (2) is the matched filter output of user $k$ in a smaller system that holds only the users $\pi_i, \ldots, \pi_K$. The first user, $\pi_1$, is decided by its plain matched filter.

**Theorem 1 (no noise).** Let $w = 0$ and the amplitudes be known. If

$$A_{\pi_i} > \sum_{l > i} A_{\pi_l} |R_{\pi_i \pi_l}| \quad \text{for every } i = 1, \ldots, K, \tag{3}$$

then every decision is right.

*Proof.* By induction on $i$. Assume the first $i - 1$ decisions are right. By (2) with $n = 0$, $x_k = A_k b_k + e$ with $|e| \le \sum_{l > i} A_{\pi_l} |R_{k \pi_l}| < A_k$ by (3). So $x_k$ has the sign of $b_k$, and line L4 decides $b_k$. The case $i = 1$ needs no assumption on earlier steps. $\square$

Condition (3) is the reason line L1 orders the users by decreasing amplitude: the strongest user must beat the interference of all the others, but the last user faces no interference at all. Condition (3) holds for any correlations when the amplitudes grow fast enough, for example when $A_{\pi_i} > \sum_{l > i} A_{\pi_l}$. With equal amplitudes it can fail: three users with $R_{12} = R_{13} = 0.75$ and $b = (+1, -1, -1)$ give $z_1 = 1 - 0.75 - 0.75 = -0.5$, a wrong first decision without noise.

**Theorem 2 (with noise).** With known amplitudes, let $q_i$ be the error probability of the matched filter decision $\mathrm{sgn}(A_k b_k + \sum_{l > i} R_{k \pi_l} A_{\pi_l} b_{\pi_l} + n_k)$, $k = \pi_i$, in the smaller system of Lemma 2:

$$q_i = 2^{-(K - i)} \sum_{b_{\pi_{i+1}}, \ldots, b_{\pi_K}} Q\Big( \frac{A_k + \sum_{l > i} R_{k \pi_l} A_{\pi_l} b_{\pi_l}}{\sigma} \Big).$$

Then user $\pi_1$ has the error probability $q_1$ exactly, and user $\pi_i$ has an error probability of at most $q_1 + q_2 + \cdots + q_i$.

*Proof.* The decision on $\pi_1$ is $\mathrm{sgn}(z_{\pi_1})$, and $n_k \sim \mathcal{N}(0, \sigma^2)$ because $R_{kk} = 1$. Averaging $Q$ over the other bits, as in the proof for any matched filter, gives $q_1$. For $i > 1$, let $E_l$ be the event that the matched filter statistic of (2) for user $\pi_l$ has the wrong sign. If all of $E_1, \ldots, E_{i-1}$ fail, then by induction the first $i - 1$ decisions are right: on that event each $x_{\pi_l}$ equals the statistic of (2). Then $x_{\pi_i}$ also equals its statistic in (2), so user $\pi_i$ errs only if $E_i$ occurs. Hence the error event of user $\pi_i$ lies in $E_1 \cup \cdots \cup E_i$, and $P(E_l) = q_l$. $\square$

The bound shows the main weakness of the method: one wrong decision doubles the interference it was meant to remove, since $b - \hat b = 2b$, and the error propagates to every later user.

**Remark (estimated amplitudes).** With $\hat a_k = |x_k|$, the estimate of Patel and Holtzman, $\hat a_k \hat b_k = x_k$, so (1) subtracts $R_{jk} x_k$ from a later user $j$ instead of $R_{jk} A_k b_k$. When $\hat b_k$ is right, the difference is $R_{jk}$ times the interference and noise left in $x_k$. This is small when the correlations are small, but it is not zero, so the theorems above hold for this form only approximately.

**Remark (capacity, cited).** With Gaussian codebooks, decoding each user's whole codeword and cancelling the re-encoded codeword reaches the corner points of the capacity region of the Gaussian multiple access channel. That statement concerns codewords decoded with a vanishing error probability, not single bits decided by their sign; see Tse and Viswanath, Section 6.1.1.

**Remark (the cost).** Line L1 sorts in $O(K \log K)$, and step $i$ of line L3 costs $O(i)$, so the loop costs $O(K^2)$ after $z$ and $R$, which cost $O(K N)$ and $O(K^2 N)$. Done on $y$ as in Lemma 1, each step correlates and subtracts $N$ chips, and the whole detector costs $O(K N)$ without forming $R$.
