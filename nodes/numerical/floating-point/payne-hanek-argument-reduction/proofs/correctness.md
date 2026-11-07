---
title: Payne-Hanek reduction returns the exact quadrant and an accurate reduced argument
proves: [correctness]
status: full
---

**Setting.** $x$ is a finite binary64 number with $|x| > \mathrm{fl}(\pi/4)$. Write $|x| = M 2^{E}$ with $M$ an integer, $0 < M < 2^{53}$, and $E \ge -53$. Write $2/\pi = \sum_{i \ge 1} b_i 2^{-i}$ with $b_i \in \{0, 1\}$. The table holds $b_1, \ldots, b_N$ with $N \ge i_1$ for every exponent that occurs. $P \ge 55$ and $Q \ge 1$ are integers, and $C$ is an integer with $|C - 2^{Q}\pi/2| \le 1/2$. All of lines L2 to L8 except the last conversion in L8 are exact integer operations.

**Theorem.** Lines L1 to L10 return $k \in \{0, 1, 2, 3\}$ and floats $r_{hi}, r_{lo}$ such that, for some integer $j$,
$$
x = (4j + k)\frac{\pi}{2} + r, \qquad \left| r - \frac{F C}{2^{P+Q}}\,\sigma \right| \le 2^{53 - P}\frac{\pi}{2} + 2^{-Q-2},
$$
where $\sigma = \operatorname{sign}(x)$, $F$ is the value after line L7, and $r_{hi} = \mathrm{fl}(\sigma F C / 2^{P+Q})$, $r_{lo} = \mathrm{fl}(\sigma F C / 2^{P+Q} - r_{hi})$. Also $|F C / 2^{P+Q}| \le \pi/4 + 2^{-Q-2}$.

**Step 1 (the dropped head).** Let $H = \sum_{1 \le i < i_0} b_i M 2^{E - i}$. If $i_0 = 1$ the sum is empty. Otherwise $i_0 = E - 1$, and each term has $E - i \ge 2$, so it is an integer multiple of $M \cdot 4$. In both cases $H = 4h$ for an integer $h$.

**Step 2 (the window).** By the definition in L4, $W = \sum_{i_0 \le i \le i_1} b_i 2^{i_1 - i}$. So
$$
\sum_{i_0 \le i \le i_1} b_i M 2^{E - i} = M W 2^{E - i_1} = \frac{Z}{2^{P}},
$$
since $i_1 - E = P$. This is exact, because $Z = MW$ is an exact integer product.

**Step 3 (the dropped tail).** Let $T = \sum_{i > i_1} b_i M 2^{E - i}$. Then $0 \le T \le M 2^{E - i_1} \sum_{t \ge 1} 2^{-t} = M 2^{-P}$, and the inequality is strict because $2/\pi$ is irrational, so not all $b_i$ with $i > i_1$ are 1. With $M < 2^{53}$ this gives $0 \le T < 2^{53 - P}$.

**Step 4 (the quadrant).** Let $Z = 2^{P} I + F_0$ with $0 \le F_0 < 2^{P}$, so L6 sets $k_0 = I \bmod 4$ and $F = F_0$. Steps 1 to 3 give
$$
|x|\frac{2}{\pi} = 4h + I + \frac{F_0}{2^{P}} + T.
$$
If $F_0 < 2^{P-1}$, line L7 does nothing, and $|x| \cdot 2/\pi = 4j' + k + F/2^{P} + T$ with $k = k_0$ and $4j' = 4h + I - k_0$. If $F_0 \ge 2^{P-1}$, line L7 sets $k = (k_0 + 1) \bmod 4$ and $F = F_0 - 2^{P}$. The same identity holds with $I + F_0/2^P = (I + 1) + F/2^{P}$. In both cases $F/2^{P} \in [-1/2, 1/2)$, and $4j' + k$ is an integer congruent to $k$ modulo 4. Multiply by $\pi/2$:
$$
|x| = (4j' + k)\frac{\pi}{2} + \rho, \qquad \rho = \left(\frac{F}{2^{P}} + T\right)\frac{\pi}{2}.
$$
This holds for whichever $k$ is chosen. So $k$ is never wrong: it is the quadrant that belongs to the returned reduced value.

**Step 5 (the constant).** $\left|\frac{F C}{2^{P+Q}} - \frac{F}{2^{P}}\frac{\pi}{2}\right| = \frac{|F|}{2^{P}} \cdot \frac{|C - 2^{Q}\pi/2|}{2^{Q}} \le \frac12 \cdot \frac{1}{2^{Q+1}} = 2^{-Q-2}$. With Step 3, $\left|\rho - \frac{F C}{2^{P+Q}}\right| \le T\frac{\pi}{2} + 2^{-Q-2} < 2^{53-P}\frac{\pi}{2} + 2^{-Q-2}$. Since $|F|/2^{P} \le 1/2$, also $|FC/2^{P+Q}| \le \pi/4 + 2^{-Q-2}$.

**Step 6 (the sign).** If $x > 0$, take $j = j'$ and $r = \rho$. If $x < 0$, then $x = -|x| = (-4j' - k)\frac{\pi}{2} - \rho$. Write $-4j' - k = 4j + ((-k) \bmod 4)$ for an integer $j$. Line L9 returns $(-k) \bmod 4$ and negates the reduced value, so $r = -\rho$, and the bound of Step 5 holds with $\sigma = -1$. Negation is exact in floating point, so negating $r_{hi}$ and $r_{lo}$ equals rounding the negated value under round to nearest. This proves the theorem.

**Step 7 (the early exit).** If $|x| \le \mathrm{fl}(\pi/4)$, then $|x| < \pi/4$, and $(k, r) = (0, x)$ is exact with $j = 0$.

**Corollary (relative accuracy).** The following fact is cited, not proved here: every binary64 $x$ with $|x| > \pi/4$ satisfies $|r| > 2^{-62}$. Ng (1992) and Muller (2016, Chapter 11) obtained this by a continued-fraction search over all exponents. The smallest value, at $x = 6381956970095103 \cdot 2^{797}$, is about $2^{-60.9}$. With $P = Q = 245$, the bound of the theorem is below $2^{-190}$. Write $\tilde r = \sigma F C / 2^{P+Q}$. Then $|\tilde r - r| < 2^{-128}|r|$. The conversion in L8 gives $r_{hi} = \mathrm{fl}(\tilde r)$ and $r_{lo} = \mathrm{fl}(\tilde r - r_{hi})$, with no underflow because $|\tilde r| > 2^{-63}$. So $|r_{hi} + r_{lo} - \tilde r| \le u |\tilde r - r_{hi}| \le u^2 |\tilde r|$ with $u = 2^{-53}$, and $|r_{hi} + r_{lo} - r| \le (2^{-106} + 2^{-127})|r|$. $\blacksquare$
