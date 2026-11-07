---
title: TwoSum returns the exact error of a rounded addition
proves: [correctness]
status: full
---

**Setting.** Binary floating-point arithmetic with precision $p \ge 3$, minimal exponent $e_{\min}$, subnormal numbers, and no overflow in any operation. Every operation is rounded to nearest, written $\mathrm{RN}$, with a tie rule that is symmetric ($\mathrm{RN}(-v) = -\mathrm{RN}(v)$; ties to even and ties away from zero both are). For a float $x \ne 0$ let $e_x$ be the integer with $2^{e_x} \le |x| < 2^{e_x + 1}$ if $x$ is normal and $e_x = e_{\min}$ if $x$ is subnormal; let $e_0 = e_{\min}$, and $U_x = 2^{e_x - p + 1}$. Every float $x$ is an integer multiple of $U_x$. If $e \ge e_{\min}$ and $U = 2^{e - p + 1}$, every number $kU$ with $k$ an integer and $|k| \le 2^p$ is a float.

We use three facts about $\mathrm{RN}$: it is monotone; $\mathrm{RN}(v) = v$ for a float $v$; and $|\mathrm{RN}(v) - v| \le |f - v|$ for every float $f$. We also use the theorem on [Fast2Sum](/fast-two-sum/): if $e_x \ge e_y$, then $\mathrm{RN}(x + y) - x$ is a float, and so is $(x + y) - \mathrm{RN}(x + y)$, with absolute value at most $\tfrac12 U_{\mathrm{RN}(x+y)}$. By ordering the operands, it follows that **the rounding error of a sum or difference of two floats is a float** (fact E).

**The algorithm.** $s = \mathrm{RN}(a + b)$, $a' = \mathrm{RN}(s - b)$, $b' = \mathrm{RN}(s - a')$, $\delta_a = \mathrm{RN}(a - a')$, $\delta_b = \mathrm{RN}(b - b')$, $t = \mathrm{RN}(\delta_a + \delta_b)$.

**Theorem.** $s + t = a + b$.

**Reduction.** It suffices to show that

$$\text{(i) } a - a' \text{ is a float},\qquad \text{(ii) } s - a' \text{ is a float},\qquad \text{(iii) } b - (s - a') \text{ is a float}.$$

Indeed, (ii) gives $b' = s - a'$, then (i) and (iii) give $\delta_a = a - a'$ and $\delta_b = b - b'$, and $\delta_a + \delta_b = a + b - (a' + b') = a + b - s$, which is a float by fact E, so $t = a + b - s$.

Moreover (iii) follows from (ii): if $b' = s - a'$, then $b - b' = a' - (s - b) = \mathrm{RN}(s - b) - (s - b)$, which is minus the rounding error of the difference $s - b$ of two floats, a float by fact E. So only (i) and (ii) remain. Negating $a$ and $b$ negates every intermediate value (symmetry of $\mathrm{RN}$), so we may assume $a + b \ge 0$ when convenient; the arguments below do not depend on signs except where stated.

**Case 1: the sum is exact, $s = a + b$.** Then $s - b = a$, so $a' = a$ and $a - a' = 0$, and $s - a' = b$. Both are floats.

**Case 2: $e_b \ge e_a$.** By the Fast2Sum theorem for $(b, a)$, $s - b$ is a float, so $a' = s - b$, and $a - a' = a + b - s$ is a float. Also $s - a' = b$. So (i) and (ii) hold.

**Case 3: $e_a > e_b$ and $s \ne a + b$.** Then $a \ne 0$, $b \ne 0$, and $e_a > e_b \ge e_{\min}$, so $a$ is normal and $|b| < 2^{e_b + 1} \le 2^{e_a} \le |a|$. Let $r = (a + b) - s \ne 0$. By the Fast2Sum theorem for $(a, b)$, $z = s - a$ is a float, $r = b - z$ is a float, and $|r| \le \tfrac12 U_s$. Since $s$ is inexact, it is normal (sums in the subnormal range are exact).

*Bounds.* $|a + b| \le |a| + |b| < 2|a|$, and $2|a|$ is a float, so by monotonicity $|s| \le 2|a| < 2^{e_a + 2}$; hence $e_s \le e_a + 1$, $U_s \le 2U_a$ and $|r| \le U_a$.

We have $s - b = a - r$ and $a' = \mathrm{RN}(a - r)$. Since $a$ is a float, $|a' - (a - r)| \le |r|$, so $|a' - a| \le 2|r| \le 2U_a = 2^{e_a - p + 2} \le 2^{e_a - 1}$, using $p \ge 3$. Hence $|a'| \ge 2^{e_a - 1}$ and $a'$ has the sign of $a$; so $e_{a'} \ge e_a - 1$ and $a'$ is a multiple of $V = U_a/2 = 2^{(e_a - 1) - p + 1}$, as is $a$. Note $e_a - 1 \ge e_{\min}$.

*(i).* $a - a'$ is a multiple $kV$ of $V$ with $|kV| \le 2U_a = 4V$, so $|k| \le 4 \le 2^p$, and $a - a'$ is a float.

*(ii).* If $a' = a$, then $s - a' = z$, a float. Suppose $a' \ne a$.

*Case 3a: $e_b \le e_a - 2$.* Write $s - a' = b - \rho$ with $\rho = a' - (s - b)$, so $|\rho| \le |r| \le U_a$. Then $|s - a'| \le |b| + U_a < 2^{e_a - 1} + 2^{e_a - p + 1} \le 2^{e_a}$, since $p \ge 2$. Next, $a' \ne a$ means that $a - r$ is at least as close to a float other than $a$ as to $a$; the floats adjacent to $a$ are at distance at least $V$ from $a$, so $|r| \ge V/2$, and with $|r| \le \tfrac12 U_s$ this gives $U_s \ge V$. Thus $s$ and $a'$ are both multiples of $V$, and $s - a' = kV$ with $|kV| < 2^{e_a} = 2^p V$, so $|k| < 2^p$ and $s - a'$ is a float.

*Case 3b: $e_b = e_a - 1$.* Then $U_b = V$, and $a$, $b$, $a + b$ are multiples of $V$. Since $s \ne a + b$, $U_s > V$, so $U_s \in \{U_a, 2U_a\}$ and $s$ is a multiple of $U_a = 2V$. Hence $r = a + b - s$ is a nonzero multiple of $V$ with $|r| \le \tfrac12 U_s \le U_a = 2V$: $r = \pm V$ or $r = \pm 2V$.

- If $a - r$ is a float, then $a' = a - r$ and $s - a' = s - a + r = z + r = b$, a float.
- Otherwise $a - r$ lies strictly between two consecutive floats. If $|r| = 2V = U_a$, then $a - r = a \mp U_a$, which is a float: floats in the binade of $a$ are spaced $U_a$, the number $2^{e_a + 1}$ is a float, and below $2^{e_a}$ the floats are spaced $V$, so a step of $U_a$ from a float of magnitude at least $2^{e_a}$ lands on a float. So $|r| = V$, $a - r = a \mp V$ is the midpoint between $a$ and its neighbour $a \mp U_a$ in the binade, and $a' \ne a$ forces $a' = a - 2r$. Then $s - a' = z + 2r = b + r$. This is a multiple of $V$ with $|b + r| \le |b| + V < 2^{e_a} + V$; since $|b| < 2^{e_b + 1} = 2^{e_a}$ is a multiple of $V$, $|b| \le 2^{e_a} - V$, so $|b + r| \le 2^{e_a} = 2^p V$, and $b + r$ is a float.

In every case (i) and (ii) hold, which proves the theorem. $\square$

**The bound on $t$.** $t = a + b - s$ is the rounding error of $s$, so $|t| \le \tfrac12\mathrm{ulp}(s)$ by the Fast2Sum theorem, and $\tfrac12\mathrm{ulp}(s) \le u|s|$ for normal $s$ (if $s$ is subnormal, $t = 0$).

**Remarks.** The proof uses round to nearest in fact E and in $|a' - (a - r)| \le |r|$. With directed rounding the rounding error of an addition need not be a float, and the theorem fails. The hypothesis $p \ge 3$ is used only to keep $a'$ in the binade of $a$ or the one below; an exhaustive machine check of all pairs in a small format with $p = 2$ found no counterexample, but this is not a proof for $p = 2$.
