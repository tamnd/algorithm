---
title: The Newton reciprocal is exact after a bounded correction, and the quotient is off by at most one
proves: [correctness, termination]
status: full
---

For an integer $D \ge 1$ let $B = B(D)$ be its binary length, so $2^{B-1} \le D < 2^B$, and let $R^* = 4^B / D$, a real number. Then $2^B < R^* \le 2^{B+1}$.

**Theorem.** RECIPROCAL$(D)$ terminates and returns $\lfloor 4^B/D \rfloor$; the loop of line L7 runs at most 16 times in each call. For $0 \le U < D 2^B$ and $R = \lfloor 4^B/D \rfloor$, DIVIDE$(U, D, R)$ terminates and returns $(\lfloor U/D \rfloor, U \bmod D)$, and the loop of line L10 runs at most once.

**1. Termination of the recursion.** If $B > B_0 \ge 1$, then $h = \lceil B/2 \rceil$ satisfies $1 \le h < B$, and $D_h = \lfloor D / 2^{B-h} \rfloor$ has binary length exactly $h$, since $2^{B-1}/2^{B-h} = 2^{h-1}$ and $D / 2^{B-h} < 2^h$. So each call recurses once on a divisor of strictly smaller length, and the recursion ends at line L1 after at most $\lceil \log_2 B \rceil$ levels. Line L1 is correct by definition. We now prove a call at length $B > B_0$ correct, assuming that the recursive call returns $X_h = \lfloor 4^h / D_h \rfloor$ (induction on $B$).

**2. The start.** Let $X_0 = X_h 2^{B-h}$, the value of line L4, and $t = 2^{B-h}$. Then $-t < X_0 - R^* < 4t$.

*Proof.* Put $d' = D / t$, a real number with $D_h \le d' < D_h + 1$. Then $R^*/t = 4^B/(Dt) = 2^{B+h}/D = 4^h/d'$, since $d' = D/2^{B-h}$. Now $4^h/D_h - 1 < X_h \le 4^h / D_h$, and

$$0 \le \frac{4^h}{D_h} - \frac{4^h}{d'} = \frac{4^h (d' - D_h)}{D_h d'} < \frac{4^h}{D_h^2} \le \frac{4^h}{4^{h-1}} = 4,$$

using $D_h \ge 2^{h-1}$. Hence $-1 < X_h - 4^h/d' < 4$, and multiplying by $t$ gives the claim. $\square$

**3. The Newton step squares the residual.** For any real $X$, let $E = 4^B - DX$ and $X^* = X + XE/4^B$. Then

$$4^B - DX^* = 4^B - DX - \frac{DX \cdot E}{4^B} = E - \frac{(4^B - E)E}{4^B} = \frac{E^2}{4^B} \ge 0 ,$$

so $X^* \le R^*$ and $R^* - X^* = E^2/(4^B D)$. $\square$

**4. After line L6.** Let $X_1$ be the value after line L6. Then $R^* - 17 < X_1 \le \lfloor R^* \rfloor$.

*Proof.* With $X = X_0$, line L5 computes the integer $E = 4^B - D X_0 = D(R^* - X_0)$. If $E \ge 0$, line L6 sets $X_1 = X_0 + \lfloor X_0 E / 4^B \rfloor$; if $E < 0$, it sets $X_1 = X_0 - \lceil X_0 |E| / 4^B \rceil$. In both cases $X_1 = \lfloor X^* \rfloor$ where $X^* = X_0 + X_0 E/4^B$, because $X_0$ is an integer and $-\lceil y \rceil = \lfloor -y \rfloor$. By part 3, $X^* \le R^*$, so the integer $X_1 \le \lfloor R^* \rfloor$. By part 2, $|E| < 4 D t$, so by part 3

$$R^* - X^* = \frac{E^2}{4^B D} < \frac{16 D^2 t^2}{4^B D} = \frac{16 D \, 4^{B-h}}{4^B} = \frac{16 D}{4^h} < 16,$$

since $D < 2^B \le 2^{2h} = 4^h$. With $X_1 > X^* - 1$ this gives $X_1 > R^* - 17$. $\square$

**5. Line L7.** Line L7 sets $E = 4^B - D X_1 = D(R^* - X_1) \ge 0$ and keeps the invariant $E = 4^B - DX$ while it increments $X$ and subtracts $D$ from $E$. It stops when $0 \le E < D$, that is, when $X \le R^* < X + 1$, that is, when $X = \lfloor R^* \rfloor$. Starting from $X_1 \le \lfloor R^* \rfloor$, it reaches this value after $\lfloor R^* \rfloor - X_1$ steps, an integer with $\lfloor R^* \rfloor - X_1 \le R^* - X_1 < 17$. So it runs at most 16 times and line L8 returns $\lfloor 4^B/D \rfloor$. This completes the induction. $\square$

**6. The quotient.** Let $0 \le U < D 2^B$ and $R = \lfloor R^* \rfloor$, so $R^* - 1 < R \le R^*$. Line L9 sets $q = \lfloor UR / 4^B \rfloor$. From $R \le R^*$, $q \le UR^*/4^B = U/D$, so $q \le \lfloor U/D \rfloor$. From $R > R^* - 1$ and $U < D 2^B \le 4^B$ (as $D < 2^B$),

$$q > \frac{UR}{4^B} - 1 > \frac{U}{D} - \frac{U}{4^B} - 1 > \frac{U}{D} - 2 \ge \Big\lfloor \frac{U}{D} \Big\rfloor - 2 ,$$

so the integer $q \ge \lfloor U/D \rfloor - 1$. Then $r = U - qD$ satisfies $0 \le r < 2D$, and line L10 subtracts $D$ at most once, keeping $U = qD + r$, and stops with $0 \le r < D$. By the uniqueness of division with remainder, $q = \lfloor U/D \rfloor$ and $r = U \bmod D$. $\square$

**7. Long dividends.** DIVIDE on blocks keeps the invariant that, after the blocks above position $j$ are processed, $q$ and $r$ are the quotient and remainder of the number formed by those blocks; each block step has $U = r 2^B + \text{block} < D 2^B$ since $r < D$, so part 6 applies. This is the invariant of [long division](/long-division/) with digits of $B$ binary digits. $\blacksquare$
