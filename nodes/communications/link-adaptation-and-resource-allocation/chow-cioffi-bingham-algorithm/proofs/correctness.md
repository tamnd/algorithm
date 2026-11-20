---
title: The Chow-Cioffi-Bingham loading meets the bit target and the energy budget with one common margin
proves: [correctness]
status: full
---

The algorithm is a heuristic, so its correctness is a statement about what its output satisfies, not about optimality. The input is $\mathrm{SNR}_i > 0$, the SNR of subcarrier $i$ at unit energy, for $i = 1, \ldots, N$; the gap $\Gamma \ge 1$; the target $B$ with $0 \le B \le N b_{\max}$ (or $B \ge 0$ without a cap); the energy budget $P > 0$; and $\mathrm{MaxCount} \ge 1$. Write $\hat b_i$ for the integer bits, and $\gamma$ for the margin as a linear factor ($\gamma_{\mathrm{dB}} = 10 \log_{10} \gamma$).

**Theorem.** If the first round loads at least one bit or $B = 0$, the algorithm stops, and its output satisfies

1. $\sum_i \hat b_i = B$ and $0 \le \hat b_i \le b_{\max}$;
2. $\sum_i e_i = P$ and $e_i \ge 0$;
3. every used subcarrier ($\hat b_i > 0$) gets $e_i\, \mathrm{SNR}_i = \gamma^*\, \Gamma\, (2^{\hat b_i} - 1)$ with the same $\gamma^* = P / \sum_j \Gamma (2^{\hat b_j} - 1)/\mathrm{SNR}_j$, and every unused subcarrier gets $e_i = 0$;
4. $\gamma^* \le P / E^*(B)$, where $E^*(B)$ is the least energy that carries $B$ bits at margin 1.

**Lemma 1 (the margin loop stops).** Lines L2 to L5 run at most $\mathrm{MaxCount}$ rounds.

*Proof.* Each round raises the counter by 1, and line L5 stops the loop when the counter reaches $\mathrm{MaxCount}$. (The implementation also stops when a later round loads no bit, because then the margin step of line L4 is not defined.) $\square$

**Lemma 2 (the fix-up stops at the target).** Line L6 runs exactly $|B_{\mathrm{total}} - B|$ steps, and each step is possible.

*Proof.* Each step changes $B_{\mathrm{total}}$ by one toward $B$ and stops when they are equal. When $B_{\mathrm{total}} > B \ge 0$, some $\hat b_i > 0$, so a bit can be removed. When $B_{\mathrm{total}} < B \le N b_{\max}$, some $\hat b_i < b_{\max}$, so a bit can be added. Removing a bit from $\hat b_i > 0$ keeps $\hat b_i \ge 0$, and adding one to $\hat b_i < b_{\max}$ keeps $\hat b_i \le b_{\max}$. The rounding at line L2 is clipped to $[0, b_{\max}]$ as well, since $b_i \ge 0$. $\square$

This proves property 1.

**Lemma 3 (the energies).** Let $n_i = \Gamma (2^{\hat b_i} - 1)/\mathrm{SNR}_i$, the energy that carries $\hat b_i$ bits at margin 1, and $S = \sum_i n_i$. If $B > 0$, then $S > 0$, and lines L7 and L8 give $e_i = n_i P / S$.

*Proof.* If $B > 0$, some $\hat b_i \ge 1$, so $n_i > 0$. Then $\sum_i e_i = (P/S) \sum_i n_i = P$, and $e_i \ge 0$. For a used subcarrier, $e_i\, \mathrm{SNR}_i / (\Gamma(2^{\hat b_i} - 1)) = e_i / n_i = P/S$, the same for every $i$. For an unused one, $n_i = 0$, so $e_i = 0$. $\square$

This proves properties 2 and 3 with $\gamma^* = P/S$. Under the gap model, the margin $\gamma^*$ on every used subcarrier means that each one reaches the target error rate with the same reserve, which is the aim of the last step of the algorithm. If $B = 0$, all bits are 0 and the energies are 0; the margin is unbounded.

**Property 4.** The loading $\hat b$ carries $B$ bits, so its energy at margin 1 is $S \ge E^*(B)$ by the definition of $E^*$. So $\gamma^* = P/S \le P/E^*(B)$, the margin of an optimal loading such as that of the [Levin-Campello algorithm](/levin-campello-algorithm/). Equality can fail: for $\mathrm{SNR} = (20, 9, 5, 1.5)$, $\Gamma = 1$, $B = 8$ and $P = 4$, the loop stops after three rounds at $(3, 2, 2, 1)$ with $S = 1.95$, while the optimum $(4, 2, 2, 0)$ has $E^*(8) = 101/60 \approx 1.6833$, so the algorithm loses $10 \log_{10}(1.95 \cdot 60/101) \approx 0.64$ dB of margin.

**Lemma 4 (the size of a margin step).** For $x > 0$, $m > 0$ and $t \ge 0$,

$$0 \le \log_2\!\left(1 + \frac{x}{m}\right) - \log_2\!\left(1 + \frac{x}{m\, 2^{t}}\right) \le t,$$

with strict inequality on the right when $t > 0$.

*Proof.* The difference is $\log_2 r$ with $r = \dfrac{(m + x)\, 2^{t}}{m\, 2^{t} + x}$. Since $2^t \ge 1$, the denominator satisfies $m + x \le m 2^t + x \le (m + x) 2^t$. The right inequality gives $r \ge 1$, so the difference is at least 0. The left inequality gives $r \le 2^t$, so the difference is at most $t$; when $t > 0$ and $m > 0$, the left inequality is strict, and so is the bound. $\square$

So when line L4 raises the margin by the factor $2^t$ with $t = (B_{\mathrm{total}} - B)/U > 0$, every real rate $b_i$ falls by at most $t$, and the rates of subcarriers with high SNR fall by almost exactly $t$, since the difference tends to $t$ as $x/m \to \infty$. If all $U$ used subcarriers had high SNR and the rounding did not change, the next total would be $B$; this is the reason for the step. Rounding and subcarriers near zero bits can make the loop overshoot or cycle, which is why it has the cap $\mathrm{MaxCount}$ and the fix-up of line L6. The same bound holds for a lower margin ($t < 0$) with the signs reversed.
