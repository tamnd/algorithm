---
title: Lehmer's algorithm returns gcd(u, v)
proves: [correctness]
status: full
---

The input is $u \ge v \ge 0$ (the implementation takes absolute values and swaps first), and $w \ge 2$. We write $\beta = 2^w$. One **Euclid step** maps a pair $(x, y)$ with $x \ge y > 0$ to $(y, x - qy)$ with $q = \lfloor x/y \rfloor$; by the GCD recursion theorem it keeps the gcd.

We prove that each iteration of the outer loop (lines L2 to L10) replaces $(u, v)$ by the result of one or more Euclid steps. Then the gcd is kept, the loop ends, and line L11 is Euclid's algorithm.

**Setup of one outer iteration.** At line L1, $v \ge \beta$, and $u \ge v$, so $u$ has at least $w + 1$ bits and $s = \operatorname{bitlength}(u) - w \ge 1$. Let $x = u / 2^s$ and $y = v / 2^s$ be real numbers. Line L2 sets $\hat u = \lfloor x \rfloor$ and $\hat v = \lfloor y \rfloor$, so $x = \hat u + \alpha$ and $y = \hat v + \beta'$ with $\alpha, \beta' \in [0, 1)$.

Write $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$ and let $(\hat u, \hat v)$ denote the current values of the variables. Let $(\hat u_0, \hat v_0)$ be the values set at line L2, and define the **virtual pair** $(u', v') = (A u + B v,\ C u + D v)$.

**Lemma 1 (inner invariant).** Before each test of line L4:

1. $(\hat u, \hat v) = (A \hat u_0 + B \hat v_0,\ C \hat u_0 + D \hat v_0)$.
2. $(u', v')$ is obtained from $(u, v)$ by $j$ Euclid steps, where $j$ is the number of completed inner iterations; in particular $u' > v' \ge 0$ if $j \ge 1$.
3. Either $A \ge 0$, $B \le 0$, $C \le 0$, $D \ge 0$, or $A \le 0$, $B \ge 0$, $C \ge 0$, $D \le 0$.

*Proof.* Before the first test, $M$ is the identity, $j = 0$, and all three hold (the first sign pattern). Assume they hold, the test of line L4 passes, and line L6 does not break, so $q \ge 1$ and
$$q = \left\lfloor \frac{\hat u + A}{\hat v + C} \right\rfloor = \left\lfloor \frac{\hat u + B}{\hat v + D} \right\rfloor, \qquad \hat v + C > 0, \quad \hat v + D > 0.$$

*Claim: $q = \lfloor u'/v' \rfloor$.* By statements 1 and 3 and $u' / 2^s = A x + B y$,
$$\frac{u'}{2^s} - \hat u = A \alpha + B \beta', \qquad \frac{v'}{2^s} - \hat v = C \alpha + D \beta'.$$
In the first sign pattern, $A\alpha \in [0, A]$ and $B\beta' \in [B, 0]$, so $u'/2^s \in [\hat u + B, \hat u + A]$, and in the same way $v'/2^s \in [\hat v + C, \hat v + D]$. Let $N_1 = \hat u + B$, $N_2 = \hat u + A$, $V_1 = \hat v + C$, $V_2 = \hat v + D$. We have $V_1 > 0$, and $q \ge 1$ gives $N_1 \ge q V_2 > 0$. For $N \in [N_1, N_2]$ and $V \in [V_1, V_2]$ with all four bounds positive,
$$\frac{N_1}{V_2} \le \frac{N}{V} \le \frac{N_2}{V_1}.$$
Both ends have floor $q$, so $q \le N/V < q + 1$. With $N = u'/2^s$ and $V = v'/2^s$ this gives $\lfloor u'/v' \rfloor = q$. In the second sign pattern the roles of $(A, C)$ and $(B, D)$ swap, and the same argument applies with $N_1 = \hat u + A$, $N_2 = \hat u + B$, $V_1 = \hat v + D$, $V_2 = \hat v + C$. Also $v' \ge 2^s V_1 > 0$, so the Euclid step on $(u', v')$ is defined.

*Maintenance.* Line L7 sets the new matrix to $\begin{pmatrix} 0 & 1 \\ 1 & -q \end{pmatrix} M$, and line L8 sets $(\hat u, \hat v) \leftarrow (\hat v, \hat u - q \hat v)$, the same linear map, so statement 1 stays true. The new virtual pair is $(v', u' - q v')$, which by the claim is one Euclid step from $(u', v')$; this gives statement 2, and $u' - qv' = u' \bmod v' < v'$. The new rows are $(C, D)$ and $(A - qC, B - qD)$. In the first pattern, $(C, D)$ has $C \le 0 \le D$ and $A - qC \ge 0 \ge B - qD$, which is the second pattern; the second pattern turns into the first in the same way. So statement 3 stays true. $\square$

**Lemma 2 (one outer iteration).** Lines L2 to L10 replace $(u, v)$ by a pair obtained from it by at least one Euclid step. The new pair satisfies $u \ge v \ge 0$ and has the same gcd.

*Proof.* The inner loop ends after finitely many iterations, because by Lemma 1 each one is a Euclid step on the positive integers $(u', v')$, and $v'$ strictly decreases. If it ended with $j = 0$ steps, $M$ is the identity and $B = 0$, and line L9 does one Euclid step on $(u, v)$, which is defined since $v \ge \beta > 0$. If $j \ge 1$, then $B \ne 0$: after a step, $B$ is the value of $D$ before that step, and $D$ is never 0, because it starts at 1 and each step replaces it by $B - qD$ with $|B - qD| = |B| + q|D| \ge |D|$, since $B$ and $D$ have opposite signs or are 0 by statement 3. Then line L10 sets $(u, v) = (u', v')$, which is $j$ Euclid steps from the old pair by Lemma 1. In both cases the gcd is kept by the GCD recursion theorem, and the new pair has $u \ge v \ge 0$. $\square$

**Theorem.** LEHMER-GCD$(u, v)$ returns $\gcd(u, v)$.

*Proof.* By Lemma 2, $\gcd(u, v)$ is an invariant of the outer loop, and each iteration does at least one Euclid step, so $v$ strictly decreases while it is positive. Hence the outer loop ends, with $v < \beta$. Line L11 is Euclid's algorithm on $(u, v)$, which ends with $v = 0$ and $u = \gcd$ of the pair at that point; this is the gcd of the input. If the input has $v = 0$, the outer loop does not run, line L11 does nothing, and $u = \gcd(u, 0)$; in particular the result for $(0, 0)$ is 0. $\blacksquare$

**The quotients are the true ones.** Lemma 1 shows more than correctness: the quotients that the inner loop finds are exactly the quotients of Euclid's algorithm on $(u, v)$, in the same order. So Lehmer's algorithm performs the same sequence of Euclid steps, only grouped, and the Bézout coefficients can be tracked by multiplying the matrices.
