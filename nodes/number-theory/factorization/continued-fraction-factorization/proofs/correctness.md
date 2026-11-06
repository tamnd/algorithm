---
title: Correctness of continued fraction factorization
proves: [correctness, termination]
status: full
---

Let $D = kN$, not a perfect square, so $\sqrt D$ is irrational, and let $a = \lfloor \sqrt D \rfloor$. For integers $P$ and $Q \ne 0$, the number $x = (P + \sqrt D)/Q$ has conjugate $\bar x = (P - \sqrt D)/Q$. Call $x$ *reduced* if $x > 1$ and $-1 < \bar x < 0$. Since $1$ and $\sqrt D$ are linearly independent over $\mathbb Q$, the map $u + v\sqrt D \mapsto u - v\sqrt D$ for rational $u, v$ is a field automorphism of $\mathbb Q(\sqrt D)$; it fixes the rationals.

**Lemma 1 (the step).** Let $x = (P + \sqrt D)/Q$ be reduced, with integers $P$, $Q > 0$ and an integer $Q'$ such that $QQ' = D - P^2$. Let $b = \lfloor (a + P)/Q \rfloor$, $P^+ = bQ - P$ and $Q^+ = Q' + b(P - P^+)$. Then $0 < P < \sqrt D$, $0 < Q < 2\sqrt D$, $b = \lfloor x \rfloor \ge 1$, $QQ^+ = D - (P^+)^2$, and $x^+ = (P^+ + \sqrt D)/Q^+$ is reduced with $x^+ = 1/(x - b)$.

*Proof.* From $x > 1 > -\bar x$ we get $x + \bar x = 2P/Q > 0$, so $P > 0$; from $\bar x < 0$, $P < \sqrt D$. From $x > 1$, $Q < P + \sqrt D < 2\sqrt D$. For a real $y$ and a positive integer $Q$, $\lfloor y/Q \rfloor = \lfloor \lfloor y \rfloor / Q \rfloor$, and $\lfloor P + \sqrt D \rfloor = P + a$, so $\lfloor x \rfloor = \lfloor (P + a)/Q \rfloor = b$. As $x > 1$, $b \ge 1$.

Next, $(P^+)^2 - P^2 = (P^+ - P)(P^+ + P) = (P^+ - P) bQ$, so $D - (P^+)^2 = QQ' - bQ(P^+ - P) = Q(Q' + b(P - P^+)) = QQ^+$.

Now $x - b = (\sqrt D - P^+)/Q$, and $0 < x - b < 1$ since $x$ is irrational. As $D$ is not a square, $QQ^+ = D - (P^+)^2 \ne 0$, so $Q^+ \ne 0$ and $x^+ = 1/(x - b) = Q(\sqrt D + P^+)/(D - (P^+)^2) = (P^+ + \sqrt D)/Q^+$. From $0 < x - b < 1$, $x^+ > 1$. The conjugate gives $\bar x^+ = 1/(\bar x - b)$, and $\bar x - b < -1$ because $\bar x < 0$ and $b \ge 1$, so $-1 < \bar x^+ < 0$. Then $x^+ - \bar x^+ = 2\sqrt D/Q^+ > 0$, so $Q^+ > 0$. Hence $x^+$ is reduced. $\square$

**Lemma 2 (the expansion).** Let $P_1 = a$, $Q_0 = 1$, $Q_1 = D - a^2$, and define $b_i$, $P_{i+1}$, $Q_{i+1}$ by the recurrence of line L5. Let $x_i = (P_i + \sqrt D)/Q_i$. Then for every $i \ge 1$, $x_i$ is reduced, $Q_{i-1}Q_i = D - P_i^2$, $0 < Q_i < 2\sqrt D$, $b_i = \lfloor x_i \rfloor$ and $x_{i+1} = 1/(x_i - b_i)$. Also $\sqrt D = a + 1/x_1$.

*Proof.* $Q_1 = D - a^2 \ge 1$ since $D$ is not a square, and $Q_0 Q_1 = D - P_1^2$. Since $0 < \sqrt D - a < 1$, $x_1 = (a + \sqrt D)/(D - a^2) = 1/(\sqrt D - a) > 1$, which also gives $\sqrt D = a + 1/x_1$. And $\bar x_1 = 1/(-\sqrt D - a)$ lies in $(-1, 0)$ because $\sqrt D + a > 1$. So $x_1$ is reduced. Lemma 1 with $(P, Q', Q) = (P_i, Q_{i-1}, Q_i)$ gives all the claims for $i$ and passes the hypotheses on to $i + 1$. Induction on $i$ completes the proof. $\square$

**Lemma 3 (convergents).** Let $A_{-1} = 1$, $A_0 = a$, $B_{-1} = 0$, $B_0 = 1$, and $A_i = b_i A_{i-1} + A_{i-2}$, $B_i = b_i B_{i-1} + B_{i-2}$ for $i \ge 1$. Then for every $i \ge 1$:

1. $\sqrt D = (A_{i-1} x_i + A_{i-2})/(B_{i-1} x_i + B_{i-2})$,
2. $A_{i-1} B_{i-2} - A_{i-2} B_{i-1} = (-1)^i$,
3. $A_{i-1}^2 - D B_{i-1}^2 = (-1)^i Q_i$.

*Proof.* (1) For $i = 1$ the right side is $(a x_1 + 1)/x_1 = a + 1/x_1 = \sqrt D$ by Lemma 2. If (1) holds for $i$, substitute $x_i = b_i + 1/x_{i+1}$ from Lemma 2. The numerator becomes $A_{i-1} b_i + A_{i-2} + A_{i-1}/x_{i+1} = (A_i x_{i+1} + A_{i-1})/x_{i+1}$, and in the same way the denominator becomes $(B_i x_{i+1} + B_{i-1})/x_{i+1}$; so (1) holds for $i + 1$. The denominators are positive, since all $B_j \ge 0$, $B_{i-1} \ge 1$ for $i \ge 1$, and $x_i > 0$.

(2) For $i = 1$: $A_0 B_{-1} - A_{-1} B_0 = 0 - 1 = -1$. And $A_i B_{i-1} - A_{i-1} B_i = (b_i A_{i-1} + A_{i-2}) B_{i-1} - A_{i-1}(b_i B_{i-1} + B_{i-2}) = -(A_{i-1} B_{i-2} - A_{i-2} B_{i-1})$, so the sign alternates.

(3) Multiply (1) out: $x_i(\sqrt D B_{i-1} - A_{i-1}) = A_{i-2} - \sqrt D B_{i-2}$. Let $M = A_{i-1}^2 - D B_{i-1}^2$, a nonzero integer since $\sqrt D$ is irrational. Multiplying both sides by $\sqrt D B_{i-1} + A_{i-1}$ gives $-M x_i = (A_{i-2} - \sqrt D B_{i-2})(\sqrt D B_{i-1} + A_{i-1}) = U + \sqrt D (A_{i-2} B_{i-1} - A_{i-1} B_{i-2})$ with the integer $U = A_{i-1} A_{i-2} - D B_{i-1} B_{i-2}$. By (2) this is $U - (-1)^i \sqrt D$. So $x_i = ((-1)^i \sqrt D - U)/M$. We also have $x_i = P_i/Q_i + \sqrt D/Q_i$. Since $1$ and $\sqrt D$ are linearly independent over $\mathbb Q$, the coefficients of $\sqrt D$ agree: $1/Q_i = (-1)^i/M$, so $M = (-1)^i Q_i$. $\square$

**Lemma 4 (the loop of lines L3 to L5).** At each test of line L4, with step counter $i$, the variables hold $P = P_i$, $Q = Q_i$, $Q' = Q_{i-1}$ and $A = A_{i-1} \bmod N$, $A' = A_{i-2} \bmod N$. Every relation $(A, v)$ in $R$ satisfies $A^2 \equiv \prod_{p \in F} p^{v_p} \pmod N$, where $v$ is the exponent vector and $p = -1$ is included.

*Proof.* Line L2 sets $P = a = P_1$, $Q' = 1 = Q_0$, $Q = Q_1$, $A' = 1 = A_{-1}$, $A = A_0 \bmod N$ and $i = 1$. Line L5 is the recurrence of Lemma 2 for $P$ and $Q$, and it replaces $(A', A)$ by $(A, (bA + A') \bmod N)$ with $b = b_i$, which is $(A_{i-1}, A_i)$ modulo $N$ because reduction modulo $N$ commutes with sums and products. Then $i$ grows by one, so the invariant holds at the next test. Line L4 appends $(A, v)$ only if $(-1)^i Q_i = \prod_{p \in F} p^{v_p}$. By Lemma 3, $A_{i-1}^2 = D B_{i-1}^2 + (-1)^i Q_i$, and $N \mid D$, so $A^2 \equiv A_{i-1}^2 \equiv (-1)^i Q_i \pmod N$. $\square$

**Lemma 5 (the elimination).** Let $v_1, \dots, v_m$ be the exponent vectors mod 2, as bit masks. The elimination keeps for each pivot a pair $(u, h)$ with $u = \bigoplus_{j \in h} v_j$, where $\oplus$ is the sum mod 2. When row $j$ reduces to $0$, the subset $h$ it carries is nonempty and $\bigoplus_{l \in h} v_l = 0$. If $m > |F|$, at least $m - |F|$ subsets are found.

*Proof.* Row $j$ starts with $u = v_j$ and $h = \{j\}$. Each reduction adds a pivot pair $(u', h')$ to $(u, h)$ by $\oplus$ in both parts, which keeps $u = \bigoplus_{l \in h} v_l$. The pivots stored before row $j$ come from rows $l < j$, so their sets $h'$ do not contain $j$, and $j$ stays in $h$; thus $h \ne \emptyset$. A row either becomes a new pivot, with a leading bit that no other pivot has, or reduces to $u = 0$. Each reduction step clears the leading bit of $u$ and changes only lower bits, so the process ends. The pivots have distinct leading bits among the $|F|$ positions, so there are at most $|F|$ pivots, and at least $m - |F|$ rows reduce to $0$. $\square$

**Theorem.** CFRAC stops, and it returns either $1$ or a proper factor $g$ of $N$ with $1 < g < N$. Every subset $T$ tried at line L7 gives $X^2 \equiv Y^2 \pmod N$. When the loop ends with $|R| = |F| + E$, at least $E$ subsets are tried.

*Proof.* *Termination.* Each pass of the loop increases $i$, and the loop stops when $i \ge I$, so it makes fewer than $I$ passes. All divisions in line L5 are by $Q = Q_i > 0$ (Lemma 2). The smoothness test of line L4 divides a nonzero integer by primes and stops. Line L6 runs Lemma 5 on finitely many rows, and lines L7 and L8 run once per subset. So the algorithm stops.

*Congruence of squares.* Let $T$ be a subset with $\bigoplus_{j \in T} v_j = 0$, and let $e = \sum_{j \in T} v_j$ over the integers. Then every $e_p$ is even, including $e_{-1}$. By Lemma 4, $X^2 = \prod_{j \in T} A_j^2 \equiv \prod_{p \in F} p^{e_p} = (-1)^{e_{-1}} \prod_{p \ne -1} \big(p^{e_p/2}\big)^2 = Y^2 \pmod N$, since $(-1)^{e_{-1}} = 1$. The count of subsets follows from Lemma 5 with $m = |F| + E$.

*Correctness.* The only return other than line L9 is line L8, which returns $g = \gcd(X - Y, N)$ only if $1 < g < N$. A gcd with $N$ divides $N$, so $g$ is a proper factor. Otherwise line L9 returns $1$. $\blacksquare$
