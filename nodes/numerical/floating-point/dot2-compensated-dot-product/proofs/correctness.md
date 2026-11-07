---
title: The error bound of Dot2
proves: [correctness]
status: full
---

**Setting.** A binary floating-point system with precision $p$, unit roundoff $u = 2^{-p}$, round to nearest (any tie rule), and the standard model $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$. We assume that no overflow occurs, that no product $x_i y_i$ underflows in the sense that TwoProduct is exact (for TwoProduct with an FMA it suffices that $e_{x_i} + e_{y_i} \ge e_{\min} + p - 1$), and that $nu < 1$. Write $\gamma_k = ku/(1 - ku)$, $P = \sum_{i} |x_i y_i|$ and $x^{T}y = \sum_i x_i y_i$. Two facts are used.

- (EFT) TwoSum returns $(s, q)$ with $a + b = s + q$ exactly and $|q| \le u|s|$; TwoProduct returns $(h, r)$ with $ab = h + r$ exactly and $|r| \le u|h|$. The exactness is proved in the encyclopedia pages on TwoSum and TwoProduct; the bounds hold because the error of a rounding to nearest is at most half an ulp of the result, which is at most $u$ times its magnitude (Muller et al., Section 2.3.2, ulp as defined there), and because a sum whose result is subnormal is exact.
- (Gamma) $(1 + u)(1 + \gamma_k) \le 1 + \gamma_{k+1}$, and if $|\delta_j| \le u$ for $j \le k$ then $\prod_j (1 + \delta_j) = 1 + \theta_k$ with $|\theta_k| \le \gamma_k$, for $ku < 1$ (Higham, Lemma 3.1 and Lemma 3.3).

**Notation for the run.** Let $(p_1, s_1) = (h_1, r_1)$ be the output of L1, and for $i \ge 2$ let $(h_i, r_i)$, $(p_i, q_i)$ and $s_i$ be the values computed in L3, L4 and L5 at step $i$. Put $q_1 = 0$ and $e_i = q_i + r_i$ (exact, a real number), and let $t_i = \mathrm{fl}(q_i + r_i)$ be its computed value for $i \ge 2$, with $t_1 = r_1 = e_1$.

**Lemma 1 (an exact identity).** $x^{T}y = p_n + \sum_{i = 1}^{n} e_i$.

*Proof.* By (EFT), $x_1 y_1 = p_1 + r_1$ and, for $i \ge 2$, $x_i y_i = h_i + r_i$ and $p_{i - 1} + h_i = p_i + q_i$. Adding, $\sum_{i \le k} x_i y_i = p_k + \sum_{i \le k}(q_i + r_i)$ by induction on $k$. $\square$

**Lemma 2 (the small parts are small).** $\sum_{i = 1}^{n} |e_i| \le \gamma_n P$.

*Proof.* Let $S_k = \sum_{i \le k} |h_i|$. We show by induction that $|p_k| \le (1 + \gamma_{k-1}) S_k$ and $\sum_{i = 2}^{k} |q_i| \le \gamma_{k - 1} S_k$. For $k = 1$, $p_1 = h_1$ and the sum is empty. For $k \ge 2$, $p_k = \mathrm{fl}(p_{k-1} + h_k)$, so $|p_k| \le (1 + u)(|p_{k-1}| + |h_k|) \le (1 + u)(1 + \gamma_{k - 2}) S_k \le (1 + \gamma_{k - 1}) S_k$ by (Gamma). Then $|q_k| \le u|p_k| \le u(1 + \gamma_{k-1}) S_k = \frac{u}{1 - (k-1)u} S_k$, and
$$\sum_{i=2}^{k} |q_i| \le \gamma_{k-2} S_{k-1} + \frac{u}{1 - (k-1)u} S_k \le \Big(\gamma_{k-2} + \frac{u}{1 - (k-1)u}\Big) S_k \le \gamma_{k - 1} S_k,$$
since $\gamma_{k-1} - \gamma_{k-2} = \frac{u}{(1 - (k-1)u)(1 - (k-2)u)} \ge \frac{u}{1 - (k-1)u}$. Next, $|r_i| \le u|h_i|$ gives $\sum_i |r_i| \le u S_n$, and $|h_i| \le (1 + u)|x_i y_i|$ gives $S_n \le (1 + u) P$. So $\sum_i |e_i| \le (\gamma_{n-1} + u)(1 + u) P$. Finally $(\gamma_{n-1} + u)(1 + u) \le \gamma_n$: the left side is $\gamma_{n-1} + u\big(\tfrac{1}{1 - (n-1)u} + u\big)$, while $\gamma_n - \gamma_{n-1} = \tfrac{u}{1 - (n-1)u}\cdot\tfrac{1}{1 - nu} = \tfrac{u}{1 - (n-1)u}\big(1 + \tfrac{nu}{1 - nu}\big) \ge \tfrac{u}{1 - (n-1)u} + u \cdot nu \ge \tfrac{u}{1-(n-1)u} + u^2$. $\square$

**Lemma 3 (the sum of the small parts).** $|s_n - \sum_{i} e_i| \le \gamma_n \sum_i |e_i|$.

*Proof.* $s_1 = e_1$, and for $i \ge 2$, $t_i = e_i(1 + \delta_i)$ and $s_i = (s_{i-1} + t_i)(1 + \varepsilon_i)$ with $|\delta_i|, |\varepsilon_i| \le u$. Unrolling, $s_n = e_1 \prod_{j=2}^{n}(1 + \varepsilon_j) + \sum_{i=2}^{n} e_i (1 + \delta_i) \prod_{j = i}^{n} (1 + \varepsilon_j)$. Each $e_i$ is multiplied by at most $n$ factors $(1 + \delta)$ ($n - 1$ for $i = 1$, $n - i + 2 \le n$ for $i \ge 2$), so by (Gamma) $s_n = \sum_i e_i (1 + \theta^{(i)})$ with $|\theta^{(i)}| \le \gamma_n$. $\square$

**Theorem.** Under the assumptions of the setting, the result $\mathrm{res}$ of Dot2 satisfies
$$|\mathrm{res} - x^{T}y| \le u\,|x^{T}y| + (1 + u)\,\gamma_n^{2}\, P .$$
If $x^{T}y \ne 0$ and $\mathrm{cond} = 2P/|x^{T}y|$ is the condition number of the dot product, the relative error is at most $u + \tfrac12(1 + u)\gamma_n^{2}\,\mathrm{cond}$.

*Proof.* Let $E = \sum_i e_i$, so $x^{T}y = p_n + E$ by Lemma 1, and $|s_n - E| \le \gamma_n^{2} P$ by Lemmas 2 and 3. L6 computes $\mathrm{res} = (p_n + s_n)(1 + \delta)$ with $|\delta| \le u$. Then
$$\mathrm{res} - x^{T}y = \delta\,(p_n + s_n) + (s_n - E) = \delta\, x^{T}y + (1 + \delta)(s_n - E),$$
so $|\mathrm{res} - x^{T}y| \le u|x^{T}y| + (1 + u)\gamma_n^{2} P$. Dividing by $|x^{T}y| = 2P/\mathrm{cond}$ gives the relative form. $\blacksquare$

**Remarks.** Ogita, Rump and Oishi state the bound with $\gamma_n^{2}$ in place of $(1 + u)\gamma_n^{2}$; the extra factor here, which changes the bound by a relative $2^{-53}$, comes from the cruder treatment of the last addition. The bound says that Dot2 behaves like a dot product computed with unit roundoff about $u^{2}$ and then rounded to working precision: the first term is the final rounding, and the second is negligible unless $\mathrm{cond} \gtrsim 1/(nu)^2$, roughly $u^{-2}/n^2$. With underflow, TwoProduct can lose the error term, and an additive term proportional to $n$ times the underflow unit must be added (Ogita, Rump and Oishi treat this case); the tests show a case where the bound above fails without it.
