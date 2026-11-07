---
title: Kahan summation has error at most (2u + (n + 4)u^2) times the sum of absolute values
proves: [correctness]
status: full
---

**Setting.** Binary floating-point arithmetic with precision $p \ge 9$, subnormal numbers, round to nearest with any tie rule, and no overflow. The unit roundoff is $u = 2^{-p}$, so $u \le 2^{-9}$. Every addition and subtraction satisfies $\mathrm{fl}(a \pm b) = (a \pm b)(1 + \epsilon)$ with $|\epsilon| \le u$; if the result underflows, the operation is exact. For a float $x$, $e_x$ is its exponent ($2^{e_x} \le |x| < 2^{e_x + 1}$ for normal $x$, and $e_x = e_{\min}$ for subnormal $x$ and for $0$).

**The iteration.** Let $s_0 = c_0 = 0$ and, for $i = 1, \ldots, n$,

$$y_i = \mathrm{fl}(x_i - c_{i-1}),\quad t_i = \mathrm{fl}(s_{i-1} + y_i),\quad c_i = \mathrm{fl}(\mathrm{fl}(t_i - s_{i-1}) - y_i),\quad s_i = t_i.$$

The algorithm returns $\hat s = s_n$. Let $A = \sum_{i=1}^n |x_i|$ and $s = \sum_{i=1}^n x_i$.

**Hypothesis (H).** For every $i$, $s_{i-1} = 0$ or $e_{s_{i-1}} \ge e_{y_i}$.

**Theorem.** Under (H) and $nu \le 1/10$, $|\hat s - s| \le \bigl(2u + (n + 4)u^2\bigr) A$.

**Step 1 (the correction is exact).** Fix $i$. If $s_{i-1} = 0$, then $t_i = y_i$, $\mathrm{fl}(t_i - 0) = y_i$ and $c_i = 0 = t_i - (s_{i-1} + y_i)$. Otherwise $e_{s_{i-1}} \ge e_{y_i}$, and the theorem on [Fast2Sum](/fast-two-sum/) applied to $a = s_{i-1}$, $b = y_i$ says that $z = \mathrm{fl}(t_i - s_{i-1}) = t_i - s_{i-1}$ exactly and $\mathrm{fl}(y_i - z) = y_i - z$ exactly, with $|y_i - z| \le \tfrac12\mathrm{ulp}(t_i)$. Line L6 computes $\mathrm{fl}(z - y_i) = -\mathrm{fl}(y_i - z)$, because rounding to nearest is symmetric. So in both cases

$$c_i = t_i - (s_{i-1} + y_i) \quad\text{exactly}, \tag{1}$$

and $|c_i| \le \tfrac12\mathrm{ulp}(t_i)$. If $t_i$ is normal, $\tfrac12\mathrm{ulp}(t_i) \le u|t_i|$. If $t_i$ is subnormal or zero, the addition $s_{i-1} + y_i$ is exact, so $c_i = 0$. Hence

$$|c_i| \le u|s_i|. \tag{2}$$

**Step 2 (telescoping).** Write $y_i = (x_i - c_{i-1})(1 + \epsilon_i)$ with $|\epsilon_i| \le u$. By (1), $s_i - c_i = s_{i-1} + y_i = s_{i-1} - c_{i-1} + x_i + \epsilon_i(x_i - c_{i-1})$. Let $D_i = s_i - c_i - \sum_{j \le i} x_j$; then $D_0 = 0$ and $D_i = D_{i-1} + \epsilon_i(x_i - c_{i-1})$, so

$$\hat s - s = s_n - \sum_{j=1}^n x_j = c_n + \sum_{i=1}^n \epsilon_i (x_i - c_{i-1}). \tag{3}$$

**Step 3 (bounding the partial sums).** Let $S = \max_{1 \le i \le n} |s_i|$. The same identity at step $i$ gives $s_i = \sum_{j \le i} x_j + c_i + D_i$ with $|D_i| \le u\sum_{j \le i}|x_j| + u\sum_{j < i}|c_j|$. By (2), $|c_j| \le uS$, so

$$|s_i| \le A + uS + uA + (i - 1)u^2 S \le (1 + u)A + wS, \qquad w = u + (n - 1)u^2.$$

Taking the maximum over $i$, $S(1 - w) \le (1 + u)A$. Since $nu \le 1/10$, $w \le u(1 + nu) \le 1.1u < 1/2$, so $S \le (1 + u)A/(1 - w)$.

**Step 4 (the bound).** From (3) and (2), with $c_0 = 0$,

$$|\hat s - s| \le u|s_n| + uA + u\sum_{i=1}^{n-1}|c_i| \le uA + uS + (n - 1)u^2 S = uA + wS \le uA + \frac{(1 + u)w}{1 - w}A.$$

For $0 \le w \le 1/2$, $1/(1 - w) \le 1 + 2w$, so $(1 + u)w/(1 - w) \le w + uw + 2w^2 + 2uw^2$. Write $w = ua$ with $a = 1 + (n - 1)u \le 1.1$. Then $uw = u^2 a \le 1.1u^2$, $2w^2 = 2u^2a^2 \le 2.42u^2$ and $2uw^2 \le 2.42u^3 \le 0.01u^2$, using $u \le 2^{-9}$. So

$$\frac{(1 + u)w}{1 - w} \le u + (n - 1)u^2 + 3.53u^2 \le u + (n + 3)u^2,$$

and $|\hat s - s| \le (2u + (n + 3)u^2)A \le (2u + (n + 4)u^2)A$. $\square$

**Remarks.** The proof uses round to nearest twice: in the Fast2Sum theorem and in the symmetry $\mathrm{fl}(-v) = -\mathrm{fl}(v)$. Without (H), line L6 need not be exact: for $s_{i-1} = 2^{-60}$ and $y_i = 1$, $t_i = 1$, $\mathrm{fl}(t_i - s_{i-1}) = 1$ and $c_i = 0$, while the true error is $-2^{-60}$. The general bound $(2u + O(nu^2))A$ without (H) is proved by Knuth (TAOCP Volume 2, Section 4.2.2) and by Goldberg (Theorem 8), with a case analysis of the steps where the term is larger than the running sum.
