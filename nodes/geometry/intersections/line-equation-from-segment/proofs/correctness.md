---
title: LINE-THROUGH returns the unique canonical equation of the line through p and q
proves: [correctness, termination]
status: full
---

**Notation.** $p \ne q$ are integer points. A triple $(A, B, C) \in \mathbb{Z}^3$ with $(A, B) \ne (0, 0)$ *describes* the line $\ell(A, B, C) = \{(x, y) \in \mathbb{R}^2 : A x + B y + C = 0\}$. It is *canonical* if $\gcd(|A|, |B|, |C|) = 1$ and $A > 0$, or $A = 0$ and $B > 0$.

**Lemma 1.** The triple after line L3 describes the line through $p$ and $q$, and $A x + B y + C = \operatorname{cross}(q - p, (x, y) - p)$.

*Proof.* Expand: $\operatorname{cross}(q - p, (x - p_x, y - p_y)) = (q_x - p_x)(y - p_y) - (q_y - p_y)(x - p_x) = (p_y - q_y) x + (q_x - p_x) y - (p_y - q_y) p_x - (q_x - p_x) p_y$, which is $A x + B y + C$ with the values of lines L2 and L3. This expression vanishes at $p$ and at $q$, since the cross product of a vector with itself or with $0$ is $0$. Since $p \ne q$, $(A, B) = (p_y - q_y, q_x - p_x) \ne (0, 0)$, so $\ell(A, B, C)$ is a line, and it contains $p$ and $q$. Two distinct points lie on exactly one line, so it is the line through $p$ and $q$. $\square$

**Lemma 2.** Two triples describe the same line if and only if they are proportional.

*Proof.* Proportional triples have the same zero set. Conversely, let $\ell(A, B, C) = \ell(A', B', C')$ and take two distinct points $r, s$ of this line. Both $(A, B)$ and $(A', B')$ are orthogonal to $s - r \ne 0$, so $(A', B') = \lambda (A, B)$ for some $\lambda \ne 0$. Then $C' = -(A' r_x + B' r_y) = \lambda C$. $\square$

**Lemma 3.** Each line has at most one canonical triple, and lines L4 and L5 turn any triple into a canonical triple of the same line.

*Proof.* Let $(A, B, C)$ and $(A', B', C')$ be canonical triples of one line. By Lemma 2, $(A', B', C') = \lambda (A, B, C)$ with $\lambda = u / v$ in lowest terms, $v > 0$. Then $v (A', B', C') = u (A, B, C)$, so $v$ divides $u A, u B, u C$ and hence divides $\gcd(A, B, C) = 1$, and likewise $u$ divides $\gcd(A', B', C') = 1$. So $\lambda = \pm 1$. If $\lambda = -1$, then either $A > 0$ and $A' = -A < 0$, or $A = A' = 0$ and $B' = -B < 0$, which breaks the sign rule for $(A', B', C')$. So $\lambda = 1$.

Line L4 divides by $g = \gcd(|A|, |B|, |C|) \ge 1$, which is not $0$ since $(A, B) \ne (0, 0)$; the quotients are integers with gcd $1$. Line L5 multiplies by $-1$ exactly when the sign rule fails, and after it the sign rule holds, because $(A, B) \ne (0, 0)$: either $A \ne 0$ and then $A > 0$ afterwards, or $A = 0$, $B \ne 0$ and then $B > 0$. Multiplying by $-1$ keeps the gcd. Both steps multiply by a nonzero factor, so by Lemma 2 the line does not change. $\square$

**Theorem.** For distinct integer points $p, q$, LINE-THROUGH terminates and returns the unique canonical triple of the line through $p$ and $q$. For $p = q$ it stops with an error at line L1.

*Proof.* Every line runs once, and Euclid's algorithm in line L4 terminates. By Lemma 1 the triple after line L3 describes the line through $p$ and $q$, and by Lemma 3 lines L4 and L5 make it the unique canonical triple of that line. $\blacksquare$
