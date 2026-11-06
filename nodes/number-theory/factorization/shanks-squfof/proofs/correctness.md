---
title: Correctness of Shanks' square forms factorization
proves: [correctness, termination]
status: full
---

Let $D = kN$, not a perfect square, so $\sqrt D$ is irrational, and let $a = \lfloor \sqrt D \rfloor$. For integers $P$ and $Q > 0$, the number $x = (P + \sqrt D)/Q$ has conjugate $\bar x = (P - \sqrt D)/Q$. Call $x$ *reduced* if $x > 1$ and $-1 < \bar x < 0$.

**Lemma 1 (the step).** Let $x = (P + \sqrt D)/Q$ be reduced with integers $P$, $Q > 0$ and $Q \mid D - P^2$, let $Q'$ be the integer with $QQ' = D - P^2$, and let $b = \lfloor (a + P)/Q \rfloor$, $P^+ = bQ - P$, $Q^+ = Q' + b(P - P^+)$. Then $b = \lfloor x \rfloor \ge 1$, $QQ^+ = D - (P^+)^2$, and $x^+ = (P^+ + \sqrt D)/Q^+$ is reduced, with $x^+ = 1/(x - b)$. Also $0 < P < \sqrt D$ and $0 < Q < 2\sqrt D$.

*Proof.* From $x > 1 > -\bar x$ we get $x + \bar x = 2P/Q > 0$, so $P > 0$; from $\bar x < 0$, $P < \sqrt D$. From $x > 1$, $Q < P + \sqrt D < 2\sqrt D$. Since $Q \ge 1$ is an integer and $\lfloor P + \sqrt D \rfloor = P + a$, we have $\lfloor x \rfloor = \lfloor (P + \sqrt D)/Q \rfloor = \lfloor (P + a)/Q \rfloor = b$ (the floor of $y/Q$ equals the floor of $\lfloor y \rfloor / Q$ for a positive integer $Q$). As $x > 1$, $b \ge 1$.

Next, $(P^+)^2 - P^2 = (P^+ - P)(P^+ + P) = (P^+ - P) bQ$, so $D - (P^+)^2 = QQ' - bQ(P^+ - P) = Q(Q' + b(P - P^+)) = QQ^+$.

Now $x - b = (P - bQ + \sqrt D)/Q = (\sqrt D - P^+)/Q$, and $0 < x - b < 1$ because $x$ is irrational. Since $D$ is not a square, $D - (P^+)^2 = QQ^+ \ne 0$, so $Q^+ \ne 0$, and $x^+ = 1/(x - b) = Q(\sqrt D + P^+)/(D - (P^+)^2) = (P^+ + \sqrt D)/Q^+$. From $0 < x - b < 1$, $x^+ > 1$. The conjugate map is a field automorphism of $\mathbb Q(\sqrt D)$ that fixes the integers, so $\bar x^+ = 1/(\bar x - b)$. Since $\bar x \in (-1, 0)$ and $b \ge 1$, $\bar x - b < -1$, so $\bar x^+ \in (-1, 0)$. Then $x^+ - \bar x^+ = 2\sqrt D / Q^+$ is positive, because $x^+ > 1 > 0 > \bar x^+$, so $Q^+ > 0$. Hence $x^+$ is reduced. $\square$

**Lemma 2 (the forward walk).** Line L2 sets $P = a$, $Q' = 1$, $Q = D - a^2$. Throughout lines L3 and L4, $Q > 0$, $Q \mid D - P^2$ with $QQ' = D - P^2$, and $(P + \sqrt D)/Q$ is reduced.

*Proof.* At the start, $Q = D - a^2 \ge 1$ because $D$ is not a square, and $Q \cdot 1 = D - a^2$. The number $x_1 = (a + \sqrt D)/(D - a^2) = 1/(\sqrt D - a)$ is greater than $1$ since $0 < \sqrt D - a < 1$, and $\bar x_1 = 1/(-\sqrt D - a)$ lies in $(-1, 0)$ since $\sqrt D + a > 1$. So $x_1$ is reduced. Each pass of line L3 is the step of Lemma 1, with $(Q', Q)$ replaced by $(Q, Q^+)$ and $QQ^+ = D - (P^+)^2$, so the invariant is kept. $\square$

**Lemma 3 (the start of the second walk).** Suppose line L5 runs with $Q = r^2$. Then $R$ and $S = (D - R^2)/r$ are integers, $S > 0$, $rS = D - R^2$, and $y = (R + \sqrt D)/S$ is reduced.

*Proof.* By Lemma 2, $D - P^2 = Q'Q = Q' r^2$. Since $R = br + P \equiv P \pmod r$, $D - R^2 \equiv D - P^2 \equiv 0 \pmod r$, so $S$ is an integer and $rS = D - R^2$.

Let $b = \lfloor (a - P)/r \rfloor$; since $0 < P \le a$ by Lemma 1, $b \ge 0$. Then $R = br + P$ is the largest integer $\le a$ congruent to $P$ modulo $r$, so $a - r < R \le a$, that is $a - r + 1 \le R \le a$. Hence $0 < R < \sqrt D$, and $D - R^2 > 0$, so $S > 0$.

Also $r^2 = Q < 2\sqrt D$ (Lemma 1), so $r < \sqrt{2\sqrt D} \le \sqrt D$ when $D \ge 4$; for $D < 4$, $D \in \{2, 3\}$ and $Q_i \in \{1, 2\}$, and $r = 1 < \sqrt D$ too. Now $y > 1$ means $S < R + \sqrt D$, that is $(\sqrt D - R)(\sqrt D + R)/r < R + \sqrt D$, that is $\sqrt D - R < r$, which holds since $R \ge a - r + 1 > \sqrt D - r$. And $\bar y = (R - \sqrt D)/S < 0$ since $R < \sqrt D$, while $\bar y > -1$ means $\sqrt D - R < S = (\sqrt D - R)(\sqrt D + R)/r$, that is $r < \sqrt D + R$, which holds since $r < \sqrt D$. So $y$ is reduced. $\square$

**Lemma 4 (the second walk).** Throughout lines L6 to L8, $S > 0$, $SS' = D - R^2$, and $(R + \sqrt D)/S$ is reduced. If the repeat ends at line L8 with $R^+ = R$, then $S \mid 2R$ and $S \mid D - R^2$, and for every odd prime $\ell$ and every $e \ge 1$, $\ell^e \mid S$ implies $\ell^e \mid D$.

*Proof.* The invariant holds at the start by Lemma 3 (with $S' = r$), and each pass of line L8 that does not leave the repeat is the step of Lemma 1, so it is kept. If $R^+ = R$, then $bS - R = R$, so $2R = bS$ and $S \mid 2R$; and $S \mid SS' = D - R^2$. Let $\ell$ be an odd prime with $\ell^e \mid S$. From $\ell^e \mid 2R$ and $\ell$ odd, $\ell^e \mid R$, so $\ell^{e} \mid R^2$; with $\ell^e \mid D - R^2$, we get $\ell^e \mid D$. $\square$

So the odd part of the final $S$ divides $kN$; when it is coprime to $k$ it divides $N$, and since it also divides $R$, it divides $\gcd(N, R)$. This explains why line L9 uses $\gcd(N, R)$; whether this gcd is proper is not decided by these lemmas.

**Theorem.** For every valid input, SQUFOF$(N, k, I)$ stops, and its result is either $1$ or an integer $g$ with $1 < g < N$ and $g \mid N$. For a prime $N$ the result is $1$.

*Proof.* *Termination.* Each pass of line L3 increases $i$, so line L3 runs at most $I$ times. Each run of lines L6 to L8 makes at most $I$ passes. All divisions are by positive integers ($Q > 0$, $r > 0$, $S > 0$ by Lemmas 2 to 4) and are exact where the algorithm needs an integer (Lemmas 1 and 3), so no step fails. Hence the algorithm stops after at most $I + I^2$ passes of the inner lines.

*Correctness.* The only return other than line L11 is line L10, which returns $g = \gcd(N, R)$ only if $1 < g < N$. A gcd with $N$ divides $N$. So the result is $1$ or a proper divisor of $N$. A prime $N$ has no proper divisor, so the test of line L10 always fails, and line L11 returns $1$. $\blacksquare$
