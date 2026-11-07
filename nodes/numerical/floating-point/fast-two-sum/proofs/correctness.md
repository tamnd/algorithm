---
title: Fast2Sum returns the exact error of a rounded addition
proves: [correctness]
status: full
---

**Setting.** Binary floating-point arithmetic with precision $p \ge 2$, minimal exponent $e_{\min}$, subnormal numbers, and an unbounded maximal exponent (that is, no overflow occurs). Every operation is rounded to nearest, with any rule for breaking ties. For a float $x \ne 0$ let $e_x$ be the integer with $2^{e_x} \le |x| < 2^{e_x + 1}$ if $x$ is normal, and $e_x = e_{\min}$ if $x$ is subnormal; let $e_0 = e_{\min}$. Write $U_x = 2^{e_x - p + 1}$. Every float $x$ is an integer multiple of $U_x$, and every integer multiple $kU$ of $U = 2^{e - p + 1}$ with $e \ge e_{\min}$ and $|k| \le 2^{p}$ is a float (if $|k| < 2^{p}$ it has at most $p$ significant bits, and if $|k| = 2^{p}$ it is a power of two).

**Theorem.** Let $a$ and $b$ be floats with $e_a \ge e_b$, and let $s = \mathrm{fl}(a + b)$, $z = \mathrm{fl}(s - a)$, $t = \mathrm{fl}(b - z)$. Then $z = s - a$ and $t = b - z$ exactly, so

$$s + t = a + b, \qquad |t| \le \tfrac12\mathrm{ulp}(s).$$

**Proof.** Let $U = U_b = 2^{e_b - p + 1}$. Since $e_a \ge e_b$, $U_a$ is a multiple of $U$, so $a$, $b$ and $a + b$ are integer multiples of $U$.

*Step 1 (the nearest float is closer than $a$).* The float $a$ is a candidate for the rounding of $a + b$, so $|s - (a + b)| \le |a - (a + b)| = |b|$. Hence

$$|s - a| \le |s - (a + b)| + |b| \le 2|b|. \tag{1}$$

*Step 2 (a small sum is exact).* If $|a + b| \le 2^{e_b + 1}$, then $a + b = kU$ with $|k| \le 2^{p}$, which is a float, so $s = a + b$. Then $s - a = b$ is a float and $z = b$; then $b - z = 0$ and $t = 0$. The claims hold. From now on assume $|a + b| > 2^{e_b + 1}$. Since $2^{e_b + 1}$ is a float and rounding is monotone, $|s| \ge 2^{e_b + 1}$, so $e_s \ge e_b + 1$ and $s$ is a multiple of $2U$.

*Step 3 ($s - a$ is a float).* Two cases.

- If $e_a \ge e_b + 1$, then $a$ is also a multiple of $2U$, so $s - a = k \cdot 2U$ for an integer $k$, and by (1), $|s - a| \le 2|b| < 2^{e_b + 2} = 2^{p} \cdot 2U$. So $|k| < 2^{p}$ and $s - a$ is a float.
- If $e_a = e_b$, then $a$ and $b$ have the same sign: otherwise $|a + b| < \max(|a|, |b|) < 2^{e_b + 1}$, which Step 2 excluded. Let $\delta = s - (a + b)$. It is a multiple of $U$ (both $s$ and $a + b$ are) and $|\delta| \le \tfrac12 \mathrm{ulp}(a + b)$. As $|a + b| < 2^{e_b + 2}$, $\mathrm{ulp}(a + b) \le 2U$, so $\delta \in \{-U, 0, U\}$. Then $s - a = b + \delta$ is a multiple of $U$ with $|b + \delta| \le |b| + U \le (2^{e_b + 1} - U) + U = 2^{e_b + 1} = 2^{p} U$, because $|b| \le 2^{e_b + 1} - U$ is the largest multiple of $U$ below $2^{e_b + 1}$. So $s - a$ is a float.

In both cases the exact difference $s - a$ is a float, so its correct rounding is itself: $z = s - a$.

*Step 4 ($b - z$ is a float).* Now $b - z = (a + b) - s = -\delta$. It is a multiple of $U$, and by Step 1, $|\delta| \le |b| < 2^{e_b + 1} = 2^{p} U$. So it is a float and $t = b - z = (a + b) - s$. Then $s + t = a + b$.

*Step 5 (the size of $t$).* $|t| = |s - (a + b)| \le \tfrac12\mathrm{ulp}(a + b)$ for rounding to nearest, with the ulp of Muller et al., Section 2.3.2. If $|s| \ge |a + b|$, then $\mathrm{ulp}(a + b) \le \mathrm{ulp}(s)$ because the ulp is nondecreasing in the magnitude. If $|s| < |a + b|$, then $s$ lies in the same binade as $a + b$, since the power of two at the bottom of that binade is a float between them, so the two ulps are equal. In both cases $|t| \le \tfrac12\mathrm{ulp}(s)$. $\blacksquare$

**Remarks.** The hypothesis $e_a \ge e_b$ holds in particular when $|a| \ge |b|$. Underflow does not break the theorem: the proof uses only the spacing of floats, which is uniform in the subnormal range. Overflow does: if $a + b$ overflows, $s = \pm\infty$ and $z$ and $t$ are infinite or NaN. Without the hypothesis the theorem fails; for $a = 2^{-60}$ and $b = 1$, the algorithm returns $s = 1$ and $t = 0$.
