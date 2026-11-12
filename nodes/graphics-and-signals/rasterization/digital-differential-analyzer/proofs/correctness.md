---
title: The DDA rounds the exact line, and its floating-point version does so off the ties under a size condition
proves: [correctness, termination]
status: full
---

Let $(x_0, y_0)$ and $(x_1, y_1)$ be integer points, and $n = \max(|x_1 - x_0|, |y_1 - y_0|)$. If $n = 0$, line L2 plots $(x_0, y_0)$ and stops. From now on $n \ge 1$. The loop of line L5 runs exactly $n + 1$ times, so the algorithm terminates. For one coordinate $c$ (either $x$ or $y$), write $c_0, c_1$ for its values at the endpoints,

$$\Delta = \frac{c_1 - c_0}{n}, \qquad c_i = c_0 + i \Delta \quad (i = 0, \ldots, n),$$

and $\rho(v) = \lfloor v + \tfrac12 \rfloor$ for rounding half up. The exact point of step $i$ is $(x_i, y_i)$, the point of the segment at the fraction $i/n$ of its length. The value $c_i$ is a *tie* when $c_i + \tfrac12$ is an integer.

## Part 1: exact arithmetic

**Claim 1.** With exact real arithmetic in lines L3 and L7, pass $i$ plots $(\rho(x_i), \rho(y_i))$. The first pixel is $(x_0, y_0)$, the last is $(x_1, y_1)$, and consecutive pixels differ by at most 1 in each coordinate.

*Proof.* By induction on $i$, the value of $c$ at line L6 of pass $i$ is $c_0 + i\Delta = c_i$: it is $c_0$ after line L4, and line L7 adds $\Delta$. So pass $i$ plots $(\rho(x_i), \rho(y_i))$. Since $c_0$ and $c_n = c_1$ are integers, $\rho(c_0) = c_0$ and $\rho(c_n) = c_1$. Since $|\Delta| \le 1$ and $\rho$ is non-decreasing with $\rho(v + 1) = \rho(v) + 1$, we get $|\rho(c_{i+1}) - \rho(c_i)| \le 1$. For the major axis, $|\Delta| = 1$, so $\rho(c_{i+1}) - \rho(c_i) = \pm 1$, and the line gets exactly one pixel for each value on the major axis. $\blacksquare$

## Part 2: floating-point arithmetic

We use the [standard model](/floating-point-model/) with round to nearest and unit roundoff $u$ ($u = 2^{-53}$ for binary64, $u = 2^{-24}$ for binary32): for representable $a, b$ the computed $a + b$ or $a / b$ is the exact result times $(1 + \delta)$ with $|\delta| \le u$, and each integer of absolute value at most $1/u$ is representable. Let $M = \max(|x_0|, |y_0|, |x_1|, |y_1|)$, and assume $M + 2 \le 1/u$. Write $\hat c_i$ for the computed value of $c$ at line L6 of pass $i$, and $E_i = \hat c_i - c_i$.

**Claim 2 (the major axis is exact).** On the major axis, $\Delta = \pm 1$ is computed exactly, and $\hat c_i = c_i$ for all $i$.

*Proof.* The quotient $\pm n / n = \pm 1$ is representable, so line L3 gives it exactly. Each $c_i$ is an integer with $|c_i| \le M$, so each sum of line L7 is a representable integer and has no rounding error. $\blacksquare$

**Claim 3 (drift bound).** Let $K = M + \tfrac52$. If $(n + 1) u K \le \tfrac12$, then $|E_i| \le i\,u K$ for each $i \le n$.

*Proof.* Line L3 gives $\hat\Delta = \Delta(1 + \delta)$ with $|\delta| \le u$. Since $|\Delta| \le 1$, $1$ is representable and rounding is monotone, $|\hat\Delta| \le 1$, and $|\hat\Delta - \Delta| \le u$. Line L7 gives $\hat c_{i+1} = (\hat c_i + \hat\Delta)(1 + \varepsilon_i)$ with $|\varepsilon_i| \le u$. So

$$E_{i+1} = \hat c_i + \hat\Delta + \varepsilon_i(\hat c_i + \hat\Delta) - c_i - \Delta = E_i + (\hat\Delta - \Delta) + \varepsilon_i(\hat c_i + \hat\Delta).$$

We show $|E_i| \le i u K$ by induction. For $i = 0$, line L4 stores the integer $c_0$ exactly, so $E_0 = 0$. Assume $|E_i| \le i u K$ for some $i < n$. Then $|E_i| \le \tfrac12$ by the hypothesis, so $|\hat c_i| \le |c_i| + \tfrac12 \le M + \tfrac12$ and $|\hat c_i + \hat\Delta| \le M + \tfrac32$. Hence

$$|E_{i+1}| \le |E_i| + u + u\left(M + \tfrac32\right) = |E_i| + uK \le (i + 1) u K. \qquad \blacksquare$$

**Claim 4 (same pixels off the ties).** Assume

$$2n(n + 1)\,u\,K < 1, \qquad K = M + \tfrac52 .$$

Then at each pass $i$ and for each coordinate $c$, if $c_i$ is not a tie, line L6 gives $\rho(c_i)$, the same pixel as exact arithmetic. If $c_i$ is a tie, line L6 gives $\rho(c_i)$ or $\rho(c_i) - 1$, so it is one of the two nearest integers. The last pixel is $(x_1, y_1)$.

*Proof.* The assumption implies $(n+1)uK < \tfrac{1}{2n} \le \tfrac12$, so Claim 3 applies. Line L6 computes $s = (\hat c_i + \tfrac12)(1 + \eta)$ with $|\eta| \le u$. Then

$$\left|s - \left(c_i + \tfrac12\right)\right| \le |E_i| + u\left|\hat c_i + \tfrac12\right| \le i u K + u(M + 1) \le (n + 1) u K < \frac{1}{2n}.$$

The exact value is

$$c_i + \frac12 = \frac{2 n c_0 + 2 i (c_1 - c_0) + n}{2n},$$

a fraction with denominator $2n$. If it is not an integer, its distance to each integer is at least $\tfrac{1}{2n}$. Then $s$ and $c_i + \tfrac12$ lie strictly between the same two consecutive integers, so $\lfloor s \rfloor = \lfloor c_i + \tfrac12 \rfloor = \rho(c_i)$. If it is an integer $t = \rho(c_i)$ (a tie), then $|s - t| < 1$, so $\lfloor s \rfloor \in \{t - 1, t\}$. For $i = n$, $c_n + \tfrac12 = c_1 + \tfrac12$ is not an integer, so the last pixel is $(\rho(x_1), \rho(y_1)) = (x_1, y_1)$. $\blacksquare$

**Consequences.** For binary64, the condition of Claim 4 holds when $n \le 2^{16}$ and $M \le 2^{16}$, because then $2n(n+1)K \le 2^{17}(2^{16} + 1)(2^{16} + 3) < 2^{50} < 2^{53}$. For binary32, $2^{24} = 16777216$, and the condition holds for $n \le 200$ and $M \le 200$, because $2 \cdot 200 \cdot 201 \cdot 202.5 = 16281000$. The condition is sufficient, not necessary. Without it, a pixel off a tie can change: in binary32 the segment from $(0, 0)$ to $(353, 337)$ reaches the computed height $326.5$ at step 342, where the exact height $337 \cdot 342 / 353 \approx 326.4986$ rounds to 326.
