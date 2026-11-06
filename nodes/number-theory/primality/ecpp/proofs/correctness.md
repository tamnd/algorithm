---
title: ECPP is always right and always stops
proves: [correctness, termination]
status: full
---

We use the pseudocode ECPP$(N)$ of the page. For $n$ coprime to 6, a curve modulo $n$ is $E: y^2 = x^3 + ax + b$ with $\gcd(4a^3 + 27b^2, n) = 1$, and the points are computed with the addition rule of the code: for $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$,

- if $x_1 \not\equiv x_2$, then $\lambda = (y_2 - y_1)(x_2 - x_1)^{-1}$;
- if $x_1 \equiv x_2$ and $y_1 + y_2 \equiv 0$, the sum is $O$;
- if $x_1 \equiv x_2$ and $y_1 \equiv y_2$, then $\lambda = (3x_1^2 + a)(2y_1)^{-1}$;
- if $x_1 \equiv x_2$ and $y_1 \not\equiv \pm y_2$, the computation stops;

and then $x_3 = \lambda^2 - x_1 - x_2$, $y_3 = \lambda(x_1 - x_3) - y_1$. An inverse of a number not coprime to $n$ also stops the computation. A computation that does not stop is *carried out*. All congruences are modulo $n$ unless stated.

**Lemma 1 (reduction).** Let $p$ be a prime factor of $n$, with $\gcd(n, 6) = 1$, and let $\bar E$ be $E$ modulo $p$. If a sequence of additions starting from points of $E$ is carried out, then reducing each computed point modulo $p$ (with $O \mapsto O$) gives the same result as doing the additions in the group $\bar E(\mathbb{F}_p)$. In particular, a computed $[k]P$ reduces to $[k]\bar P$.

*Proof.* As $p \ge 5$ and $p \nmid 4a^3 + 27b^2$, $\bar E$ is an elliptic curve over $\mathbb{F}_p$, and the chord and tangent rule is its group law. We show for one addition that if the inputs reduce to $\bar P_1, \bar P_2 \in \bar E(\mathbb{F}_p)$, the output reduces to $\bar P_1 + \bar P_2$; induction over the sequence then gives the lemma. If an input is $O$, the output is the other input, which is right. In the first case $x_2 - x_1$ is invertible modulo $n$, so it is not $0$ modulo $p$, and $\bar x_1 \ne \bar x_2$; the group law uses the same chord formula, so the reduced output is $\bar P_1 + \bar P_2$. In the second case $\bar x_1 = \bar x_2$ and $\bar y_1 = -\bar y_2$, so $\bar P_2 = -\bar P_1$ and the sum is $O$. In the third case $\bar P_1 = \bar P_2$ and $2 y_1$ is invertible modulo $n$, so $\bar y_1 \ne 0$; the group law uses the tangent formula, which is the one computed. The fourth case does not occur, as the computation is carried out. $\square$

**Lemma 2 (Goldwasser and Kilian).** Let $n > 1$ with $\gcd(n, 6) = 1$, $E$ a curve modulo $n$, $P$ a point of $E$, $k \ge 1$, and $q$ a prime with $q > (n^{1/4} + 1)^2$. If $U = [k]P$ is carried out with $U \ne O$, and $[q]U$ is carried out with $[q]U = O$, then $n$ is prime.

*Proof.* Let $p$ be a prime factor of $n$. By Lemma 1, $[k]\bar P = \bar U$ and $[q]\bar U = O$ in $\bar E(\mathbb{F}_p)$. As $U$ is a pair $(x, y)$ modulo $n$, $\bar U$ is the pair $(\bar x, \bar y)$, not $O$. So $\bar U$ has order exactly $q$, since $q$ is prime, and by Lagrange's theorem $q$ divides $\#\bar E(\mathbb{F}_p)$. Hasse's theorem gives $\#\bar E(\mathbb{F}_p) \le p + 1 + 2\sqrt p = (\sqrt p + 1)^2$. So $(\sqrt p + 1)^2 \ge q > (n^{1/4} + 1)^2$, hence $\sqrt p > n^{1/4}$ and $p > \sqrt n$. If $n$ were composite, it would have a prime factor $p \le \sqrt n$. So $n$ is prime. $\square$

**Lemma 3 (the exact bound).** For integers $q > 1$ and $n \ge 1$, $q > (n^{1/4} + 1)^2$ holds if and only if $A > 0$ and $A^2 > 16 (q + 1)^2 q$, where $A = q^2 + 6q + 1 - n$. This is the test of line L8 and of the checker.

*Proof.* Both sides of $q > (n^{1/4}+1)^2$ are positive, so it is equivalent to $\sqrt q - 1 > n^{1/4}$, and as $\sqrt q - 1 > 0$, to $(\sqrt q - 1)^4 > n$. Expanding, $(\sqrt q - 1)^4 = q^2 + 6q + 1 - 4(q + 1)\sqrt q$, so the condition is $A > 4(q + 1)\sqrt q$. The right side is positive, so this holds if and only if $A > 0$ and $A^2 > 16(q+1)^2 q$. $\square$

**Lemma 4 (the leaf).** For $0 \le n < 2^{64}$, line L4 returns exactly when $n$ is prime.

*Proof.* The code first divides by the 12 primes $2, \ldots, 37$ and then runs the strong test to these bases. A prime passes the strong test to every base it does not divide. No composite below $2^{64}$ is a strong pseudoprime to all of the first 12 prime bases; this is a computed fact (Sorenson and Webster, Mathematics of Computation 86, 2017, with the earlier list of base 2 pseudoprimes below $2^{64}$ of Feitsma and Galway), which we quote. $\square$

**Lemma 5 (steps in the list).** At every time, each element $(n_i, a_i, b_i, P_i, k_i, q_i)$ of $C$, in order, satisfies the hypotheses of Lemma 2 except possibly that $q_i$ is prime; the first has $n_1 = N$, each $n_{i+1} = q_i$, and the current $n$ is $q$ of the last element, or $N$ if $C$ is empty.

*Proof.* Initially $C$ is empty and $n = N$. Line L12 appends a step only after line L6 has checked $\gcd(n, 6) = 1$ and $n \ge 2^{64} > 1$, the code has checked $\gcd(4a^3 + 27b^2, n) = 1$ (a gcd above 1 calls REJECT), the point $P$ was built with $y^2 \equiv x^3 + ax + b$, line L8 has checked $q > (n^{1/4} + 1)^2$ by Lemma 3, and $U = [k]P \ne O$ and $[q]U = O$ were carried out. Then $n$ becomes $q$, which keeps the invariant. Line L16 removes the last element and sets $n$ to its number, which is the $q$ of the element before it, or $N$; the invariant holds again. $\square$

**Theorem 1 (prime answers are right).** If ECPP$(N)$ returns prime with certificate $C$, then $N$ is prime.

*Proof.* The answer comes from line L4, so the current $n$ is prime by Lemma 4. By Lemma 5, $n = q_t$ for the last element of $C$. By Lemma 2, $n_t$ is prime, and $n_t = q_{t-1}$; going back, $n_{t-1}, \ldots, n_1 = N$ are prime. If $C$ is empty, $n = N$ and $N$ is prime directly. $\square$

The same argument shows that the checker verify_certificate of the code accepts only primes: it tests each hypothesis of Lemma 2 for each row, the links $n_{i+1} = q_i$, and the last number with Lemma 4.

**Lemma 6 (each REJECT is right).** Whenever REJECT$(n)$ is called, the current $n$ is composite.

*Proof.* We go through the calls.

- Line L5: by Lemma 4, $n < 2^{64}$ is not prime.
- Line L6: here $n \ge 2^{64}$. A multiple of 2 or 3 above 3 is composite, a square above 1 is composite, and an odd prime passes the strong test to the base 2.
- A gcd of $n$ with some number that lies strictly between 1 and $n$, from an inverse or from a Jacobi symbol equal to 0, is a proper factor of $n$.
- A failed square root. For a prime $n$ and $(c/n) = 1$, $c$ is a quadratic residue, and the Tonelli-Shanks algorithm with a non-residue $z$ (found with $(z/n) = -1$) returns a root. So if $(c/n) = 1$ and the computed $y$ has $y^2 \not\equiv c$, $n$ is not prime. This covers the root of $D$ in line L7 and the points of line L11.
- The fourth case of the addition rule. If $n$ were prime, all points computed lie on the curve (Lemma 1 with $p = n$), and $x_1 = x_2$ gives $y_1^2 = y_2^2$, so $y_1 = \pm y_2$ in the field $\mathbb{F}_n$.
- A curve with $\gcd(4a^3 + 27b^2, n) = n$. For $D = -3$ and $D = -4$ the discriminant is $27 g^{2e}$ or $-4 g^{3e}$ times a unit, and $g$ is coprime to $n$. Otherwise $c = j (j - 1728)^{-1}$ with $j \not\equiv 0, 1728$, and $4(-3c)^3 + 27(2c)^2 = 108 c^2 (1 - c)$, with $c \not\equiv 0$ and $1 - c = -1728 (j - 1728)^{-1} \not\equiv 0$. So for a prime $n$ the discriminant is never $0$ modulo $n$.
- Line L13. Suppose $n$ is prime. Then $(D/n) = 1$, $4n = u^2 + |D| v^2$, $j$ is a root of $H_D$ modulo $n$ (the code checks $H_D(j) \equiv 0$), and $H_D$ is the Hilbert class polynomial (the code checks that the computed coefficients are within $10^{-10}$ of integers; we assume the rounding is right). By the theory of complex multiplication (Deuring; Atkin and Morain, Section 3; Crandall and Pomerance, Algorithm 7.5.9), the curve with $j$-invariant $j$ and its twists over $\mathbb{F}_n$ have as orders exactly the numbers of the list for $D$, and the twists of line L10 are one curve for each order: for $D \ne -3, -4$ the twist by a non-residue $g$, for $D = -4$ the four classes $g^e$ modulo fourth powers, and for $D = -3$ the six classes modulo sixth powers, as $g$ is neither a square nor a cube. So one twist has exactly $m$ points, and every point $P$ on it has $[m]P = O$ by Lagrange's theorem. On that twist, every $P$ has either $[k]P = O$, so another point is tried, or $[q]([k]P) = [m]P = O$, so line L12 succeeds. Hence not every twist can have a point with $[q]U \ne O$, and line L13 cannot call REJECT. $\square$

**Theorem 2 (composite answers are right).** If ECPP$(N)$ returns composite, $N$ is composite.

*Proof.* Composite is returned only at line L15, inside REJECT$(n)$ with $C$ empty. By Lemma 5, then $n = N$, and by Lemma 6, $n$ is composite. $\square$

**Theorem 3 (termination).** ECPP$(N)$ stops: it returns prime, returns composite, or stops at line L14 with no answer (only when $C$ is empty).

*Proof.* First, one pass from line L2 to the next "go to L2" takes a finite number of operations. The table of line L7 is finite, each $D$ has at most 6 orders, the loop of line L10 has at most 6 twists, and the code bounds the tries for a point and for a root. Each power, gcd, square root and Euclid chain is a loop that ends. So each pass ends with a return, a stop, or a jump to line L2 from line L12 or line L16 (line L14 with $C$ not empty also goes to line L16).

A jump from line L12 replaces $n$ by $q$ with $q < n$: as $m \le n + 1 + 2\sqrt n = (\sqrt n + 1)^2$ for every listed order and $k \ge 2$, $q \le (\sqrt n + 1)^2/2 < n$ for $n \ge 6$. A jump from line L16 adds the current $n$ to the set bad, and that $n$ is not in bad before: a number in bad is never chosen again at line L8, and $n$ was either $N$, which is not removed (line L15 returns instead), or a $q$ chosen at line L8 after it was last added. All numbers that enter bad are below $N$, so line L16 runs at most $N$ times. Between two runs of line L16, line L12 runs at most as many times as the list $C$ can grow, and each step lowers $n$, so at most $N$ times. So there are finitely many passes, and the method stops. In practice the list has $O(\log N)$ steps and line L16 almost never runs. $\square$

$\blacksquare$
