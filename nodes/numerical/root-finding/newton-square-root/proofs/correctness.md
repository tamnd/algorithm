---
title: Newton's square root iteration squares the quantity (x - r)/(x + r), converges from every positive start, and terminates in floating point
proves: [correctness, termination, global-convergence, order]
status: full
---

Let $a > 0$, $r = \sqrt a$, $x_0 > 0$ and $x_{k+1} = (x_k + a/x_k)/2$. Write $e_k = x_k - r$ and $t_k = (x_k - r)/(x_k + r)$. For NEWTON-SQRT, $a$ is replaced by $m$ and $x_0 = 1$, so the $x$ of line L3 is $x_1$ and pass $k$ computes $x_{k+1}$.

**Lemma (the exact error formula).** For every $x_k > 0$, $x_{k+1} > 0$ and
$$x_{k+1} \pm r = \frac{(x_k \pm r)^2}{2 x_k}, \qquad\text{so}\qquad e_{k+1} = \frac{e_k^2}{2 x_k}, \qquad t_{k+1} = t_k^2 .$$

*Proof.* $x_{k+1} \pm r = (x_k^2 + a \pm 2 r x_k)/(2 x_k) = (x_k \pm r)^2/(2x_k)$, using $a = r^2$. Positivity is clear. Divide the two forms; $x_{k+1} + r > 0$, so $t_{k+1}$ is defined. $\square$

**Claim 1 (global convergence).** For every $x_0 > 0$: $|t_0| < 1$, $t_k = t_0^{2^k}$, $x_k \ge r$ for $k \ge 1$, $x_{k+1} \le x_k$ for $k \ge 1$, $x_k \to r$, and if no $e_k$ is zero, $e_{k+1}/e_k^2 \to 1/(2r)$.

*Proof.* Since $x_0 > 0$ and $r > 0$, $|x_0 - r| < x_0 + r$, so $|t_0| < 1$; the lemma gives $t_k = t_0^{2^k} \to 0$. Solving $t = (x - r)/(x + r)$ for $x$ gives $x_k = r (1 + t_k)/(1 - t_k)$, so $x_k \to r$. For $k \ge 1$, $e_k = e_{k-1}^2/(2 x_{k-1}) \ge 0$. Then $x_{k+1} - x_k = (a - x_k^2)/(2 x_k) \le 0$. Finally $e_{k+1}/e_k^2 = 1/(2 x_k) \to 1/(2r)$. $\square$

**Claim 2 (the reduced start).** If $1/2 \le m < 2$ and $x_0 = 1$, then $|t_0| \le 3 - 2\sqrt 2 < 0.1716$, and for $k \ge 1$ the relative error satisfies
$$0 \le \frac{x_k - r}{r} = \frac{2 t_k}{1 - t_k} \le \frac{2 \cdot 0.1716^{2^k}}{1 - 0.1716^{2^k}} .$$
For $k = 5$ the bound is below $1.1 \cdot 10^{-24} < u = 2^{-53}$.

*Proof.* $|t_0| = |1 - \sqrt m|/(1 + \sqrt m)$. The function $s \mapsto |1 - s|/(1 + s)$ decreases on $(0, 1]$ and increases on $[1, \infty)$, so on $[\sqrt{1/2}, \sqrt 2]$ its maximum is at an end. Both ends give $(\sqrt 2 - 1)/(\sqrt 2 + 1) = (\sqrt 2 - 1)^2 = 3 - 2\sqrt 2 \approx 0.17157$. The formula for the relative error follows from $x_k = r(1 + t_k)/(1 - t_k)$, with $t_k = t_0^{2^k} \ge 0$ for $k \ge 1$. For $k = 5$, $0.1716^{32} < 5.5 \cdot 10^{-25}$. $\square$

**Claim 3 (termination and the range reduction).** In binary64, NEWTON-SQRT returns for every input after at most $k_{\max}$ passes, and the loop also ends when $k_{\max} = \infty$. Line L2 is exact, and $\sqrt a = \sqrt m \cdot 2^e$.

*Proof.* Line L2: write $a = f \cdot 2^E$ with $1/2 \le f < 1$; if $E$ is even take $m = f$, $e = E/2$, otherwise $m = 2f$, $e = (E - 1)/2$. Multiplying by $2$ is exact, $1/2 \le m < 2$ and $a = m \cdot 4^e$. In the loop, the computed $x$ and $m/x$ are positive (the quotient of two positive normal numbers in $[1/4, 4]$ does not underflow), so every $x$ is a positive floating-point number. Line L7 runs only after line L6 found $y < x$, so the values of $x$ in successive passes strictly decrease. There are finitely many floating-point numbers in $(0, 2]$, so line L6 must eventually return. The final multiplication by $2^e$ is exact because $\sqrt m\cdot 2^e$ lies in the normal range for every finite positive binary64 $a$. $\square$

**What is not proved here.** That the returned value is within one unit in the last place of $\sqrt a$ and that the loop uses at most 5 passes in binary64 are observed on random tests (see the main page), not proved. A proof needs a rounding analysis of the last two passes near $\sqrt m$. $\blacksquare$
