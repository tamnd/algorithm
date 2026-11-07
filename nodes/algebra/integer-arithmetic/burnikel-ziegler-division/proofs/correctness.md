---
title: Burnikel-Ziegler division returns the quotient and the remainder
proves: [correctness, termination]
status: full
---

Let $\beta = 2^w$. A number $X$ of $k$ limbs is *normalized* if $\beta^k/2 \le X < \beta^k$.

**Termination.** DIV2N1N on $n$ limbs either stops at line L1 or calls DIV3N2N twice with $h = n/2$, and DIV3N2N calls DIV2N1N at most once with $h$ limbs. So the size halves every two levels and the recursion has depth at most $2 \log_2 n$. The loop of line L9 runs at most twice by Lemma 2. SCHOOLBOOK-DIVREM terminates (Knuth, Algorithm D).

**Lemma 1 (trial quotient).** Let $b = \beta^h$, $B = B_1 b + B_2$ with $0 \le B_2 < b$ and $b/2 \le B_1 < b$, and $A = A_1 b^2 + A_2 b + A_3$ with $0 \le A_2, A_3 < b$ and $A < bB$. Let $Q^* = \lfloor A/B \rfloor$ and $\hat Q = \min(\lfloor (A_1 b + A_2)/B_1 \rfloor, b - 1)$. Then $Q^* < b$ and $Q^* \le \hat Q \le Q^* + 2$.

*Proof.* $Q^* < b$ since $A < bB$. *$\hat Q \ge Q^*$:* if $\hat Q = b - 1$ this holds. Otherwise $\hat Q = \lfloor (A_1 b + A_2)/B_1 \rfloor$, so $A_1 b + A_2 - \hat Q B_1 \le B_1 - 1$, and then

$$A - \hat Q B \le A - \hat Q B_1 b = (A_1 b + A_2 - \hat Q B_1) b + A_3 \le (B_1 - 1)b + A_3 < B_1 b \le B,$$

so $A - (\hat Q + 1)B < 0$ and $Q^* \le \hat Q$. *$\hat Q \le Q^* + 2$:* if $B_2 = 0$, then $B = B_1 b$ and $\lfloor (A_1 b + A_2)/B_1 \rfloor = \lfloor (A - A_3)/B \rfloor \le Q^*$, so $\hat Q = Q^*$. Otherwise $B > B_1 b \ge b$, and $B_1 b > B - b > 0$ since $B < (B_1 + 1)b$. Suppose $\hat Q \ge Q^* + 3$. Since $\hat Q \le (A_1 b + A_2)/B_1 = (A - A_3)/(B_1 b) \le A/(B_1 b) < A/(B - b)$ and $Q^* > A/B - 1$,

$$3 \le \hat Q - Q^* < \frac{A}{B - b} - \frac{A}{B} + 1 = \frac{A}{B} \cdot \frac{b}{B - b} + 1 ,$$

so $A/B > 2(B - b)/b \ge 2(B_1 - 1)$, using $B \ge B_1 b$. As $2(B_1 - 1)$ is an integer, $Q^* = \lfloor A/B \rfloor \ge 2(B_1 - 1)$. With $\hat Q \le b - 1$ this gives $2(B_1 - 1) \le Q^* \le \hat Q - 3 \le b - 4$, that is $B_1 \le b/2 - 1$, which contradicts $B_1 \ge b/2$. $\square$

(This is Knuth's Theorems A and B of Section 4.3.1, with base $b = \beta^h$ and a divisor of two $b$-digits.)

**Lemma 2 (DIV3N2N).** Under the hypotheses of Lemma 1, and provided the call of line L6 returns the correct quotient and remainder, DIV3N2N returns $(Q^*, A - Q^* B)$, and line L9 runs at most twice.

*Proof.* Since $A < bB$, $A_1 \le B_1$: otherwise $A \ge (B_1 + 1) b^2 > bB$. If $A_1 < B_1$, then $A_1 b + A_2 < B_1 b$, which is the precondition of DIV2N1N with the normalized $h$-limb divisor $B_1$, and line L6 returns $Q = \lfloor (A_1 b + A_2)/B_1 \rfloor \le b - 1$ and $R_1 = A_1 b + A_2 - Q B_1$. If $A_1 = B_1$, then $\lfloor (A_1 b + A_2)/B_1 \rfloor \ge b$, and line L7 sets $Q = b - 1$ and $R_1$ the same way. In both cases $Q = \hat Q$, and line L8 gives

$$R = R_1 b + A_3 - \hat Q B_2 = (A_1 b + A_2 - \hat Q B_1)b + A_3 - \hat Q B_2 = A - \hat Q B .$$

By Lemma 1, $\hat Q - Q^* \in \{0, 1, 2\}$, so $R = (A - Q^* B) - (\hat Q - Q^*)B \ge -2B$, and $R < B$. Each pass of line L9 lowers $Q$ by 1 and raises $R$ by $B$, keeping $R = A - QB$, and it stops at the first $Q$ with $R \ge 0$, which is $Q^*$, after $\hat Q - Q^* \le 2$ passes. $\square$

**Theorem.** If $B$ is a normalized $n$-limb number and $0 \le A < \beta^n B$, DIV2N1N returns $(\lfloor A/B \rfloor, A \bmod B)$.

*Proof.* By strong induction on $n$. If line L1 applies, SCHOOLBOOK-DIVREM is correct (Knuth, Algorithm D, whose trial quotients are bounded by Lemma 1 with $h = 1$). Otherwise let $h = n/2$, $b = \beta^h$, and $A = A_1 b^3 + A_2 b^2 + A_3 b + A_4$. The top half $B_1 = \lfloor B/b \rfloor$ is a normalized $h$-limb number, so the calls of DIV2N1N inside DIV3N2N are correct by the induction hypothesis.

*First call (line L3).* $A' = \lfloor A/b \rfloor = A_1 b^2 + A_2 b + A_3$ satisfies $A' \le A/b < bB$. By Lemma 2 it returns $Q_1 = \lfloor A'/B \rfloor$ and $R = A' - Q_1 B \in [0, B)$.

*Second call (line L4).* $A'' = Rb + A_4 \le (B - 1)b + b - 1 < bB$, so Lemma 2 applies and returns $Q_2 = \lfloor A''/B \rfloor < b$ and $S = A'' - Q_2 B \in [0, B)$.

*Result.* $A = A' b + A_4 = (Q_1 B + R) b + A_4 = Q_1 b B + A'' = (Q_1 b + Q_2) B + S$ with $0 \le S < B$, so by the uniqueness of [division with remainder](/division-with-remainder/), $Q_1 b + Q_2 = \lfloor A/B \rfloor$ and $S = A \bmod B$; line L5 returns them. $\blacksquare$
