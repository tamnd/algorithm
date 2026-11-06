---
title: Correctness of the elliptic curve method
proves: [correctness, termination]
status: full
---

Throughout, $N > 1$ with $\gcd(N, 6) = 1$, and a curve $y^2 = x^3 + ax + b$ with $\gcd(4a^3 + 27b^2, N) = 1$ is fixed, as after line L3. For a prime $p \mid N$, $p \ge 5$ and $4a^3 + 27b^2 \not\equiv 0 \pmod p$, so the curve modulo $p$ is an elliptic curve and its points form the group $E(\mathbb{F}_p)$ under the chord and tangent rules, with zero $O_p$. For a point $P = (x, y)$ modulo $N$ write $P_p = (x \bmod p, y \bmod p)$, and $O$ reduces to $O_p$.

The addition $P_1 + P_2$ of the algorithm is: $O + P_2 = P_2$ and $P_1 + O = P_1$; otherwise (case 1) if $x_1 \not\equiv x_2 \pmod N$, the slope $\lambda = (y_2 - y_1) d^{-1}$ with $d = x_2 - x_1$; (case 2) if $x_1 \equiv x_2$ and $y_1 + y_2 \equiv 0 \pmod N$, the sum $O$; (case 3) otherwise the slope $\lambda = (3x_1^2 + a) d^{-1}$ with $d = y_1 + y_2$. In cases 1 and 3 the addition fails if $\gcd(d, N) > 1$, and otherwise returns $(\lambda^2 - x_1 - x_2, \lambda(x_1 - x_3) - y_1)$ modulo $N$.

**Lemma 1 (reduction).** Let $p$ be a prime factor of $N$, and let $P_1, P_2$ be $O$ or pairs modulo $N$ such that $(P_1)_p$ and $(P_2)_p$ are in $E(\mathbb{F}_p)$. If the addition $P_1 + P_2$ does not fail, then $(P_1 + P_2)_p = (P_1)_p + (P_2)_p$ in $E(\mathbb{F}_p)$.

*Proof.* If $P_1$ or $P_2$ is $O$ this is the rule for the zero. Case 1: $d$ is invertible modulo $N$, hence modulo $p$, so $x_1 \not\equiv x_2 \pmod p$, and the group law in $E(\mathbb{F}_p)$ uses the chord slope $(y_2 - y_1)(x_2 - x_1)^{-1}$, which is $\lambda \bmod p$; the formulas for $x_3$ and $y_3$ reduce to those of the group law. Case 2: $x_1 \equiv x_2$ and $y_1 \equiv -y_2 \pmod p$, so $(P_1)_p = -(P_2)_p$ and the sum is $O_p$. Case 3: $d = y_1 + y_2$ is invertible modulo $N$, hence $y_1 + y_2 \not\equiv 0 \pmod p$. Both reduced points lie on the curve modulo $p$ and $x_1 \equiv x_2$, so $y_1^2 \equiv x_1^3 + ax_1 + b \equiv y_2^2$, and $(y_1 - y_2)(y_1 + y_2) \equiv 0 \pmod p$ gives $y_1 \equiv y_2 \pmod p$. So $(P_1)_p = (P_2)_p$ with $2y_1 \equiv y_1 + y_2 \not\equiv 0$, and the group law uses the tangent slope $(3x_1^2 + a)(2y_1)^{-1} \equiv \lambda \pmod p$. The formulas for $x_3, y_3$ again reduce to those of the group law. $\square$

**Lemma 2 (multiples).** Let $P$ be a point modulo $N$ with $P_p \in E(\mathbb{F}_p)$ for every prime $p \mid N$. If the computation of $[m]P$ by double and add (or of $[m]P$ as a chain of additions of earlier computed multiples, as in stage two) does not fail, then its result $R$ satisfies $R_p = [m]P_p$ in $E(\mathbb{F}_p)$ for every prime $p \mid N$.

*Proof.* By induction over the additions of the chain. Every intermediate point is a sum of two earlier points of the chain, each of which reduces modulo $p$ to the corresponding multiple of $P_p$, which is in $E(\mathbb{F}_p)$. Lemma 1 then shows that the sum reduces to the sum of the multiples. Double and add computes $[2j]$ from $[j]$ and $[j + 1]$ from $[j]$ and $[1]$, so the final point reduces to $[m]P_p$. $\square$

The point $P = (x, y)$ of line L2 satisfies the curve equation modulo $N$ by the choice of $b$, so modulo each $p$ as well, and Lemma 2 applies to it and to all its computed multiples.

**Lemma 3 (detection).** Let $p$ be a prime factor of $N$ and let $m$ be a multiplier that the algorithm computes, $[m]P$ in stage one or $[m]P$ with $m = k q_i$ in stage two. If the order of $P_p$ in $E(\mathbb{F}_p)$ divides $m$, then the computation of $[m]P$ fails, or it gives the point $O$ modulo $N$, or an earlier step does one of these.

*Proof.* Suppose no step fails and the result $R$ is a pair $(x, y)$. By Lemma 2, $R_p = [m]P_p = O_p$, as the order divides $m$. But the reduction of a pair is a pair, not $O_p$. This contradiction shows that a step fails or $R = O$. $\square$

**Lemma 4 (a failure gives a proper factor).** If an addition fails, then $1 < \gcd(d, N) < N$.

*Proof.* A failure means $\gcd(d, N) > 1$. In case 1, $d = x_2 - x_1 \not\equiv 0 \pmod N$ by the case condition, so $N \nmid d$ and $\gcd(d, N) < N$. In case 3, $d = y_1 + y_2 \not\equiv 0 \pmod N$, since $d \equiv 0$ would be case 2, so again $\gcd(d, N) < N$. The test $g < N$ of line L6 is therefore a safeguard that never rejects. $\square$

**Theorem.** ECM stops, and it returns $1$ or a proper factor $g$ of $N$. If for some curve and some prime $p \mid N$ the order of $P_p$ divides $k$, or divides $kq$ for a prime $q \in (B_1, B_2]$, then that curve ends in a failure that returns a proper factor, or with a point $O$ modulo $N$.

*Proof.* *Termination.* There are $C$ curves. For each, line L4 does $\sum_q e_q$ multiplications with $O(\log q)$ additions each, and line L5 builds a table of at most $G/2$ points and does one addition per prime in $(B_1, B_2]$, so each curve does finitely many additions, each of finitely many operations modulo $N$.

*Correctness.* Line L3 returns $g = \gcd(4a^3 + 27b^2, N)$ only if $1 < g < N$. Line L6 returns $g = \gcd(d, N)$ only if $1 < g < N$, and a gcd with $N$ divides $N$. So any value returned other than $1$ is a proper factor. A prime $N$ has none, so then the output is $1$.

*Detection.* Stage one computes $[q]$ of the current point for each prime power step, so its last point is $[k]P$; stage two computes $[q_i]([k]P) = [kq_i]P$ by the chain $[k q_1]P$, $[k q_1]P + [k(q_2 - q_1)]P$, and so on, where each table entry $[2j]([k]P)$ is a chain of additions of $[2]([k]P)$. By Lemma 3, if the order of $P_p$ divides $k$ or $kq_i$, a failure or the point $O$ happens no later than that multiple. By Lemma 4, a failure returns a proper factor. $\blacksquare$
