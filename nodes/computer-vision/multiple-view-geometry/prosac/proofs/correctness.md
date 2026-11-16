---
title: PROSAC draws valid samples on the schedule of its growth function, keeps the largest consensus set and stops
proves: [correctness]
status: full
---

We use the notation of the page: $D = (u_1, \ldots, u_N)$ sorted by quality, $U_n = \{u_1, \ldots, u_n\}$, $m \le N$ the sample size, $T_n = T_N \binom{n}{m} / \binom{N}{m}$, $T'_m = 1$, $T'_{n+1} = T'_n + \lceil T_{n+1} - T_n \rceil$ and $g(t) = \min\{n : T'_n \ge t\}$. The minimal solver and the residual are correct subroutines, and the model of computation is the real RAM.

**Claim.** (a) $T_{n+1} = \frac{n+1}{n+1-m} T_n$, and $T_n$ is the expected number of samples in $U_n$ among $T_N$ independent uniform samples of $m$ distinct items of $D$. (b) In every round, the sample $S$ consists of $m$ distinct items of $U_n$ for the current $n$. In a round $t$ with $t \le T'_n$, the current $n$ equals $g(t)$, and $S$ is $u_{g(t)}$ together with $m - 1$ distinct items of $U_{g(t)-1}$. (c) At each test of line L2, $I^*$ is the largest consensus set among the sampled models. (d) The loop ends after at most $k_{\max}$ rounds. (e) For $n^* = N$ and $t > T'_N$, the samples are uniform among the $m$-subsets of $D$, as in RANSAC.

**Lemma 1.** Part (a) holds.

*Proof.* $\binom{n+1}{m} / \binom{n}{m} = \frac{n+1}{n+1-m}$, which gives the recurrence. A uniform sample of $m$ distinct items lies in $U_n$ with probability $\binom{n}{m} / \binom{N}{m}$, so by linearity of expectation $T_N$ samples contain $T_n$ such samples on average. $\square$

**Lemma 2.** Part (b) holds.

*Proof.* The sequence $T'_n$ does not decrease, since each step adds $\lceil T_{n+1} - T_n \rceil \ge 0$ (by Lemma 1, $T_{n+1} \ge T_n$). Lines L4 and L5 raise $n$ only when $t > T'_n$, and $n$ never decreases. We show that $T'_{n-1} < t$ at line L6 whenever $n > m$. If $n$ was raised to its current value in this round, the raise happened because $t > T'_{n-1}$. Otherwise it was raised in an earlier round $t_0$ with $T'_{n-1} < t_0 < t$. Now let $t \le T'_n$. Every $n'' < n$ has $T'_{n''} \le T'_{n-1} < t$, because $T'$ does not decrease, so $n$ is the least index with $T'_n \ge t$, that is, $n = g(t)$; for $n = m$ this holds because $m$ is the least index. Line L7 then takes $u_n$ and $m - 1$ distinct items of $U_{n-1}$ (the set has $n - 1 \ge m - 1$ items since $n \ge m$), so $S$ has $m$ distinct items of $U_n$. Otherwise $t > T'_n$ and line L8 draws $m$ distinct items of $U_n$, with $n \ge m$. $\square$

**Lemma 3.** Part (c) holds.

*Proof.* As for RANSAC: before the first round $I^* = \emptyset$; line L11 replaces $I^*$ exactly when the consensus set of the new model is larger, so $I^*$ stays the largest among the sampled models. $\square$

**Lemma 4.** Part (d) holds.

*Proof.* $k^*$ starts at $k_{\max}$, and line L13 sets it to $k_{n^*}$ only when $k_{n^*} < k_{\max}$, or back to $k_{\max}$ when no prefix passes the test. So $k^* \le k_{\max}$ at all times, and since $t$ grows by 1 per round, the test of line L2 fails after at most $k_{\max}$ rounds. $\square$

**Lemma 5.** Part (e) holds.

*Proof.* With $n^* = N$, lines L4 and L5 raise $n$ up to $N$, and after round $T'_N$ the test of line L6 fails, so line L8 draws $m$ distinct items of $U_N = D$ uniformly. $\square$

**Remark (the schedule).** By Lemma 2, the rounds $t$ with $g(t) = n$ are $T'_{n-1} < t \le T'_n$, so while the pool grows, exactly $T'_n - T'_{n-1} = \lceil T_n - T_{n-1} \rceil$ samples have $u_n$ as their worst item. By Lemma 1, $T_n - T_{n-1}$ is the expected number of samples with worst item $u_n$ among $T_N$ uniform samples. So PROSAC draws the samples of a RANSAC run of length $T_N$ in the order of their worst item, with each count rounded up. If $T_N = \binom{N}{m}$, then $T_n = \binom{n}{m}$ is an integer and $T'_n = \binom{n}{m}$.

**Remark (what is not proved).** The stopping rule controls two error probabilities, $\Psi$ for a model supported by chance and $\eta_0$ for a better model missed in $U_{n^*}$, under the binomial model of chance inliers. It is not a guarantee of the largest consensus set. Chum and Matas state that they could not prove that PROSAC is never slower than RANSAC; the equal behavior on random orderings is a benchmark result.
