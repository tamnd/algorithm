---
title: Truncated channel inversion meets the power constraint, holds the received SNR constant, and the scan finds the best cutoff
proves: [correctness]
status: full
---

**Setting.** The channel SNR at the average power $\bar P$ is a random variable $\gamma > 0$. A power policy $P(\gamma) \ge 0$ must satisfy $\mathbb{E}[P(\gamma)] \le \bar P$, and in state $\gamma$ the received SNR is $\gamma P(\gamma)/\bar P$. For a cutoff $\gamma_0 > 0$, let

$$Q(\gamma_0) = \Pr(\gamma \ge \gamma_0), \qquad S(\gamma_0) = \mathbb{E}\!\left[\frac{1}{\gamma}\,;\, \gamma \ge \gamma_0\right] = \mathbb{E}\!\left[\frac{1}{\gamma}\,\mathbf{1}\{\gamma \ge \gamma_0\}\right].$$

Assume $Q(\gamma_0) > 0$, so that $0 < S(\gamma_0) \le Q(\gamma_0)/\gamma_0 < \infty$. Truncated channel inversion with cutoff $\gamma_0$ is the policy

$$\frac{P(\gamma)}{\bar P} = \begin{cases} \sigma(\gamma_0)/\gamma, & \gamma \ge \gamma_0, \\ 0, & \gamma < \gamma_0, \end{cases} \qquad \sigma(\gamma_0) = \frac{1}{S(\gamma_0)},$$

and its rate is $R(\gamma_0) = Q(\gamma_0) \log_2(1 + \sigma(\gamma_0))$ bits per channel use: a fixed code for the AWGN channel with SNR $\sigma$ is used whenever $\gamma \ge \gamma_0$.

**Lemma 1 (power and received SNR).** The policy uses the average power exactly $\bar P$, the received SNR is $\sigma(\gamma_0)$ in every state with $\gamma \ge \gamma_0$, and no policy that sends nothing below $\gamma_0$ and gives the same received SNR $\sigma'$ in every state with $\gamma \ge \gamma_0$ within the power $\bar P$ has $\sigma' > \sigma(\gamma_0)$.

*Proof.* $\mathbb{E}[P(\gamma)]/\bar P = \sigma\, \mathbb{E}[\gamma^{-1} \mathbf{1}\{\gamma \ge \gamma_0\}] = \sigma S = 1$. In a state with $\gamma \ge \gamma_0$, the received SNR is $\gamma \cdot \sigma/\gamma = \sigma$. A policy with received SNR $\sigma'$ on the same states must use $P(\gamma)/\bar P = \sigma'/\gamma$ there, so its average power is $\sigma' S \bar P$, and $\sigma' S \le 1$ gives $\sigma' \le \sigma$. $\square$

**Lemma 2 (finitely many candidates).** Let $\gamma$ take the distinct values $\gamma_{(1)} > \gamma_{(2)} > \cdots > \gamma_{(K)} > 0$ with probabilities $\pi_1, \ldots, \pi_K > 0$. For $k = 1, \ldots, K$ put $Q_k = \sum_{j \le k} \pi_j$ and $S_k = \sum_{j \le k} \pi_j/\gamma_{(j)}$, and $R_k = Q_k \log_2(1 + 1/S_k)$. Then $\{R(\gamma_0) : \gamma_0 > 0,\ Q(\gamma_0) > 0\} = \{R_1, \ldots, R_K\}$.

*Proof.* For $\gamma_0$ with $\gamma_{(k+1)} < \gamma_0 \le \gamma_{(k)}$ (with $\gamma_{(K+1)} = 0$), the event $\gamma \ge \gamma_0$ is the event that $\gamma$ is one of $\gamma_{(1)}, \ldots, \gamma_{(k)}$, so $Q(\gamma_0) = Q_k$ and $S(\gamma_0) = S_k$, and $R(\gamma_0) = R_k$. For $\gamma_0 > \gamma_{(1)}$, $Q(\gamma_0) = 0$. These intervals cover $(0, \infty)$, and the choice $\gamma_0 = \gamma_{(k)}$ gives $R_k$. $\square$

**Lemma 3 (the scan).** After the pass of lines L3 to L6 for the $k$-th state in sorted order, $S = S_k$, $Q = Q_k$, and the stored best rate is $\max_{j \le k} R_j$, stored with its cutoff $\gamma_{(j)}$ and $\sigma = 1/S_j$ for the first $j$ that attains it.

*Proof.* Line L1 merges equal values, adding their probabilities, and sorts the distinct values in decreasing order. Before the first pass, $S = Q = 0$ and the best rate is 0. Line L4 adds $\pi_k/\gamma_{(k)}$ and $\pi_k$, which gives $S_k$ and $Q_k$ from $S_{k-1}$ and $Q_{k-1}$. Line L5 computes $R_k$, and line L6 keeps it if it is larger than all earlier ones. Every $R_k > 0$, so the first pass always stores its state. $\square$

**Theorem.** For a discrete distribution, TRUNCATED-INVERSION returns a cutoff $\gamma_0$ that maximizes $R(\gamma_0)$ over all $\gamma_0 > 0$, the value $\sigma(\gamma_0)$, the rate $R(\gamma_0)$, and the power of each state, and this policy uses the average power $\bar P$ and gives the constant received SNR $\sigma(\gamma_0)$ in every state it serves.

*Proof.* By Lemma 3, after the last pass the stored rate is $\max_k R_k$, which by Lemma 2 is the largest rate over all cutoffs. Its cutoff is $\gamma_{(k)}$ and its $\sigma$ is $1/S_k = \sigma(\gamma_{(k)})$. Line L8 sets $P/\bar P = \sigma/\gamma$ for $\gamma \ge \gamma_0$ and 0 otherwise, which is the policy of Lemma 1. $\square$

**Remark (the Rayleigh closed form).** For Rayleigh fading, $\gamma$ has the density $e^{-\gamma/\bar\gamma}/\bar\gamma$, so with $t = \gamma/\bar\gamma$,

$$S(\gamma_0) = \int_{\gamma_0}^{\infty} \frac{e^{-\gamma/\bar\gamma}}{\bar\gamma\, \gamma}\, d\gamma = \frac{1}{\bar\gamma} \int_{\gamma_0/\bar\gamma}^{\infty} \frac{e^{-t}}{t}\, dt = \frac{E_1(\gamma_0/\bar\gamma)}{\bar\gamma},$$

and $Q(\gamma_0) = e^{-\gamma_0/\bar\gamma}$. So $\sigma = \bar\gamma/E_1(\gamma_0/\bar\gamma)$ and $R(\gamma_0) = e^{-\gamma_0/\bar\gamma}\log_2(1 + \bar\gamma/E_1(\gamma_0/\bar\gamma))$. As $\gamma_0 \to 0$, $E_1 \to \infty$ and $R \to 0$; this is why full inversion has zero rate on Rayleigh fading. As $\gamma_0 \to \infty$, $Q \to 0$ faster than $\log_2(1 + \sigma)$ grows, so $R \to 0$. The function is continuous, so a best cutoff exists, and the implementation finds it by a grid on a log scale followed by a golden section search.

**Remark (what the theorem does not say).** The theorem is about threshold policies, which is what truncated channel inversion means. Among all policies with a constant received SNR on the served states, serving part of a state at random can do better on a discrete distribution. For a fixed served probability $Q$, the cost $S$ is least when the served probability sits on the largest values of $\gamma$, as in the fractional knapsack problem, so the best such policy serves the top states and a fraction of one more. For a continuous distribution this fraction has no effect, and the threshold policy is the best of this class. Policies whose received SNR varies with $\gamma$ can do better still: water-filling over time attains the capacity with side information at both ends, and $R(\gamma_0)$ is at most that capacity.
