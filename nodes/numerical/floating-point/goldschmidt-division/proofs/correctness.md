---
title: Goldschmidt division with a final exact correction returns the correctly rounded quotient
proves: [correctness]
status: full
---

**Setting.** The algorithm of the page, for positive normal binary64 numbers $a = A \cdot 2^{e_a}$ and $b = B \cdot 2^{e_b}$ with $A, B \in [1, 2)$ and a normal quotient (signs are handled separately and are exact). The iteration works with integers scaled by $2^{-W}$, $W = 64$; every product is truncated toward zero to $W$ fractional bits. Write $\mathrm{tr}(x)$ for this truncation, so $0 \le x - \mathrm{tr}(x) < 2^{-W}$ for $x \ge 0$. The seed $f_0$ is $1/c_i$ rounded to $10$ fractional bits, where $c_i = 1 + (i + \tfrac12)/2^{7}$ and $i = \lfloor (B - 1) 2^{7} \rfloor$. The number of iterations is $k \ge 3$. Let $Q = A/B \in (\tfrac12, 2)$ and let $v = 2^{-52}$ if $A \ge B$ and $v = 2^{-53}$ otherwise, so that $v$ is the spacing of binary64 numbers at $Q$.

**Theorem.** The returned value is $\mathrm{RN}(a/b)$, the binary64 number nearest to $a/b$.

**Lemma 1 (seed).** $|1 - Bf_0| < 2^{-7}$.

*Proof.* $|B - c_i| \le 2^{-8}$ and $c_i \ge 1$, so $|1 - B/c_i| \le 2^{-8}$. Rounding gives $|f_0 - 1/c_i| \le 2^{-11}$, so $|B f_0 - B/c_i| \le 2 \cdot 2^{-11}$. Hence $|1 - Bf_0| \le 2^{-8} + 2^{-10} < 2^{-7}$. $\blacksquare$

**Lemma 2 (convergence with truncation).** Let $d_j = 1 - \eta_j$ and $n_j = Q d_j + \tau_j$ after line L3 ($j = 0$) and after the $j$-th pass of lines L5 and L6. Then $|\eta_0| < 2^{-7} + 2^{-64}$, $0 \le \eta_{j+1} < \eta_j^2 + 2^{-W}$, and $|\tau_j| < (j + 1) \cdot 2^{1-W} (1 + 2^{-6})^{j}$.

*Proof.* Line L3 gives $d_0 = Bf_0 - \beta_0$ and $n_0 = Af_0 - \alpha_0$ with $0 \le \alpha_0, \beta_0 < 2^{-W}$, so $\eta_0 = (1 - Bf_0) + \beta_0$, which with Lemma 1 gives the first claim, and $\tau_0 = n_0 - Qd_0 = Q\beta_0 - \alpha_0$, so $|\tau_0| < 2 \cdot 2^{-W}$ as $Q < 2$.

Line L5 sets $f_j = 2 - d_j = 1 + \eta_j$ exactly. Line L6 gives $d_{j+1} = d_j f_j - \beta = (1 - \eta_j)(1 + \eta_j) - \beta = 1 - \eta_j^2 - \beta$, so $\eta_{j+1} = \eta_j^2 + \beta \in [0, \eta_j^2 + 2^{-W})$. It also gives $n_{j+1} = n_j f_j - \alpha = Q d_j f_j + \tau_j f_j - \alpha = Q(d_{j+1} + \beta) + \tau_j f_j - \alpha$, so $\tau_{j+1} = \tau_j f_j + Q\beta - \alpha$ and $|\tau_{j+1}| < |\tau_j|(1 + |\eta_j|) + 2^{1-W}$. Since $|\eta_j| < 2^{-6}$ for all $j$, induction gives the bound on $\tau_j$. $\blacksquare$

**Lemma 3 (accuracy after three iterations).** For $3 \le k \le 64$, $|n_k - Q| < 2^{-54}$.

*Proof.* From Lemma 2, $\eta_1 < (2^{-7} + 2^{-64})^2 + 2^{-64} < 2^{-13.9}$, $\eta_2 < 2^{-27.8} + 2^{-64} < 2^{-27.7}$ and $\eta_3 < 2^{-55.4} + 2^{-64} < 2^{-55.3}$; for $j \ge 3$, $\eta_{j+1} < \eta_j^2 + 2^{-64} < 2^{-55.3}$ as well. For $\tau$, Lemma 2 gives $|\tau_3| < 4 \cdot 2^{-63} (1 + 2^{-6})^{3} < 2^{-60.9}$, and for $j \ge 3$ the recurrence $|\tau_{j+1}| < |\tau_j|(1 + 2^{-55}) + 2^{-63}$ gives $|\tau_k| < 2^{-60.9}(1 + 2^{-49}) + 61 \cdot 2^{-63} < 2^{-56.9}$ for $k \le 64$. Then $|n_k - Q| \le Q\eta_k + |\tau_k| < 2 \cdot 2^{-55.3} + 2^{-56.9} < 0.82 \cdot 2^{-54} + 0.14 \cdot 2^{-54} < 2^{-54}$. $\blacksquare$

**Proof of the theorem.** Let $q^{*}$ be the integer nearest to $Q/v$. By the no-midpoint property of quotients (a binary quotient $A/B$ of $p$-bit significands is never the midpoint of two consecutive $p$-bit numbers, see [floating-point division](/floating-point-division/)), $Q/v$ is not a half-integer, so $q^{*}$ is unique and $|Q/v - q^{*}| < \tfrac12$.

Line L7 rounds $n_k/v$ to the nearest integer $q$, so $|q - n_k/v| \le \tfrac12$. By Lemma 3, $|n_k - Q|/v < 2^{-54}/2^{-53} = \tfrac12$. Hence $|q - Q/v| < 1$, and $q \in \{q^{*} - 1, q^{*}, q^{*} + 1\}$.

Line L8 tests $Q < (q - \tfrac12)v$, that is $2 M_a 2^{s} < (2q - 1) M_b$ with $A = M_a 2^{-52}$, $B = M_b 2^{-52}$ and $v = 2^{-s}$, exactly in integers. It holds if and only if $q > q^{*}$, that is $q = q^{*} + 1$, and then it decrements $q$ to $q^{*}$. Line L9 tests $Q > (q + \tfrac12)v$, which holds if and only if $q < q^{*}$, and increments $q$. After both lines $q = q^{*}$.

Finally $q^{*} v = \mathrm{RN}(Q)$: $Q \in [1, 2)$ with $v = 2^{-52}$ or $Q \in (\tfrac12, 1)$ with $v = 2^{-53}$, so the binary64 numbers near $Q$ are exactly the multiples of $v$ (and $q^{*} v$ may be the power of two at the top of the binade, which is also a binary64 number). Line L10 multiplies by $2^{e_a - e_b}$, which is exact when the result is normal, so it returns $\mathrm{RN}(Q) 2^{e_a - e_b} = \mathrm{RN}(a/b)$. Ties never occur, so the result is the same for ties-to-even and ties-away. $\blacksquare$

**Remarks.** The correctness of the result rests on lines L8 and L9 and on Lemma 3; the iteration itself needs no rounding analysis beyond Lemma 2. With $k = 2$ the bound of Lemma 3 is only about $2^{-26}$, the correction can be off by many units, and the tests confirm that the result is then often wrong. Hardware implementations replace the exact integer comparisons by the sign of a remainder $a - qb$ computed with a multiplier, which is the same test.
