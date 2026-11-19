---
title: The mel filter bank has the shape its definition asks for
proves: [correctness]
status: full
---

We work in the real RAM, so the arithmetic is exact. The inputs satisfy line L1: $M \ge 1$ and $0 \le f_{lo} < f_{hi} \le f_s / 2$. The function $\operatorname{mel}(f) = 2595 \log_{10}(1 + f / 700)$ is continuous and strictly increasing on $f \ge 0$, with the inverse $\operatorname{mel}^{-1}(m) = 700 (10^{m / 2595} - 1)$.

**Lemma 1 (the edges).** Line L3 gives $f_0 = f_{lo}$, $f_{M+1} = f_{hi}$, $f_0 < f_1 < \cdots < f_{M+1}$, and $\operatorname{mel}(f_{i+1}) - \operatorname{mel}(f_i) = \Delta$ for $0 \le i \le M$.

*Proof.* By line L3, $\operatorname{mel}(f_i) = m_{lo} + i \Delta$. For $i = 0$ this is $\operatorname{mel}(f_{lo})$, and for $i = M + 1$ it is $m_{lo} + (m_{hi} - m_{lo}) = \operatorname{mel}(f_{hi})$; since $\operatorname{mel}$ is one to one, $f_0 = f_{lo}$ and $f_{M+1} = f_{hi}$. Since $f_{lo} < f_{hi}$ and $\operatorname{mel}$ is strictly increasing, $\Delta > 0$, so the values $\operatorname{mel}(f_i)$ strictly increase with $i$, and so do the $f_i$, because $\operatorname{mel}^{-1}$ is strictly increasing too. The difference of consecutive mel values is $\Delta$ by the formula. $\square$

By Lemma 1 the denominators $f_m - f_{m-1}$ and $f_{m+1} - f_m$ of lines L6 and L7 are positive, so the weights are well defined. Write $T_m(f)$ for the value that lines L6 to L8 give at the frequency $f$, so that $W[m][k] = T_m(k f_s / N)$.

**Lemma 2 (the triangles).** For $1 \le m \le M$ and every $f \ge 0$: $0 \le T_m(f) \le 1$; $T_m(f) > 0$ exactly when $f_{m-1} < f < f_{m+1}$; and $T_m(f) = 1$ exactly when $f = f_m$.

*Proof.* The three cases of lines L6 to L8 cover every $f$ and do not overlap. If $f_{m-1} < f \le f_m$, then $0 < f - f_{m-1} \le f_m - f_{m-1}$, so $0 < T_m(f) \le 1$, with equality to 1 only for $f = f_m$. If $f_m < f < f_{m+1}$, then $0 < f_{m+1} - f < f_{m+1} - f_m$, so $0 < T_m(f) < 1$. Otherwise $T_m(f) = 0$. $\square$

**Lemma 3 (overlap by half).** For every $f$ with $f_1 \le f \le f_M$, $\sum_{m=1}^{M} T_m(f) = 1$, and at most two terms are positive. For $f \le f_0$ or $f \ge f_{M+1}$, every $T_m(f)$ is 0.

*Proof.* The last claim follows from Lemma 2, since the support of $T_m$ is inside $(f_{m-1}, f_{m+1}) \subseteq (f_0, f_{M+1})$. For the first claim, if $f = f_1$, then $T_1(f) = 1$ by Lemma 2, and every other $T_m(f)$ is 0 because $f_1 \le f_{m-1}$ for $m \ge 2$. Otherwise $f_1 < f \le f_M$, and there is exactly one $j$ with $1 \le j \le M - 1$ and $f_j < f \le f_{j+1}$, because the edges strictly increase. Then $T_j(f) = (f_{j+1} - f)/(f_{j+1} - f_j)$ by line L7, and $T_{j+1}(f) = (f - f_j)/(f_{j+1} - f_j)$ by line L6. Their sum is $(f_{j+1} - f_j)/(f_{j+1} - f_j) = 1$. Every other filter $m$ has $f \le f_{m-1}$ (if $m \ge j + 2$) or $f \ge f_{m+1}$ (if $m \le j - 1$), so its weight is 0. $\square$

Applied to the bin frequencies $f = k f_s / N$, Lemma 3 says that every bin between the first and the last center has a total weight of 1, which is what the column sums of the example show and what the tests check on a bank of 26 filters.

**Lemma 4 (the band energies and their logs).** Line L9 gives $E[m] = \sum_k T_m(k f_s / N) P[k] \ge 0$, and line L10 gives $\ln \max(E[m], 10^{-10})$. If every $P[k]$ is multiplied by $c > 0$, and both $E[m]$ and $c E[m]$ are at least $10^{-10}$, then the output for filter $m$ grows by exactly $\ln c$.

*Proof.* The first part restates the lines. The weights and the power values are nonnegative, so $E[m] \ge 0$. The sum is linear in $P$, so the new energy is $c E[m]$, and under the condition the output changes from $\ln E[m]$ to $\ln(c E[m]) = \ln c + \ln E[m]$. $\square$

**Theorem.** MEL-FILTER-BANK returns, for each $m$, the log, floored at $10^{-10}$, of the power spectrum weighted by a triangle whose feet and top are three consecutive edges equally spaced in mel; the triangles sum to 1 between the first and last centers, and a gain $c$ on the spectrum adds $\ln c$ to each output above the floor.

*Proof.* Lemmas 1 to 4. $\square$

The implementation computes the same quantities in floating point. The tests compare it with a direct DFT and with explicit triangles, check the column sums of Lemma 3 to $10^{-12}$, the peak of each triangle on a fine grid, and the shift by $\ln 4$ when the amplitude doubles.
