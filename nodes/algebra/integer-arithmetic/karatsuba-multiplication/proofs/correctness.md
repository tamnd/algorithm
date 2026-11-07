---
title: Karatsuba multiplication computes the exact product
proves: [correctness, termination]
status: full
---

Let $\beta \ge 2$ and $T \ge 1$. For a limb array $x = [x_0, \ldots, x_{k-1}]$ with $0 \le x_i < \beta$ write $\langle x \rangle = \sum_i x_i\beta^i$, so $0 \le \langle x \rangle < \beta^k$. We assume that SCHOOLBOOK$(a, b)$ returns $2n$ limbs of value $\langle a \rangle\langle b \rangle$ for $n$-limb inputs (this is proved on the page of the [schoolbook method](/schoolbook-multiplication/)), and that the additions and subtractions of limb arrays used in lines L5 and L6 are exact whenever their results are nonnegative and fit in the arrays.

**Theorem.** For every $n \ge 1$ and $n$-limb arrays $a$ and $b$, KARATSUBA$(a, b)$ terminates and returns $2n$ limbs of value $\langle a \rangle \langle b \rangle$.

*Proof.* By strong induction on $n$.

*Base, $n \le T$.* Line L1 returns the schoolbook product, which is correct by assumption.

*Step, $n > T$, so $n \ge 2$.* Assume the theorem for all sizes less than $n$. Let $h = \lceil n/2 \rceil$. Since $n \ge 2$, $h \le (n + 1)/2 < n$. Line L2 sets $a_0 = [a_0, \ldots, a_{h-1}]$ and $a_1 = [a_h, \ldots, a_{n-1}, 0, \ldots, 0]$, padded to $h$ limbs, and likewise for $b$. Writing $A_0 = \langle a_0 \rangle$ and so on, we have $\langle a \rangle = A_1\beta^h + A_0$ and $\langle b \rangle = B_1\beta^h + B_0$ with $0 \le A_0, A_1, B_0, B_1 < \beta^h$.

*Lines L3 and L4.* The calls are on $h$-limb arrays, $h < n$, so by the induction hypothesis they terminate with $z_0 = A_0B_0$ and $z_2 = A_1B_1$.

*Line L5.* Let $S = A_0 + A_1$ and $U = B_0 + B_1$, both in $[0, 2\beta^h - 2]$. Write $S = s + c\beta^h$ and $U = t + d\beta^h$ with $0 \le s, t < \beta^h$ and $c, d \in \{0, 1\}$; the $h$-limb arrays of $s$ and $t$ are the low limbs of the sums. The call on $h < n$ limbs terminates with $st$ by the induction hypothesis. Then

$$SU = (s + c\beta^h)(t + d\beta^h) = st + (ct + ds)\beta^h + cd\beta^{2h},$$

which is how the implementation forms the product of the sums from $st$, so it computes $SU$ exactly, in $2h + 2$ limbs since $SU < 4\beta^{2h} \le \beta^{2h + 2}$. Expanding,

$$SU - A_0B_0 - A_1B_1 = (A_0 + A_1)(B_0 + B_1) - A_0B_0 - A_1B_1 = A_0B_1 + A_1B_0 \ge 0 .$$

So after the two subtractions, which never go below 0 because each intermediate value $SU - A_0B_0 = A_0B_1 + A_1B_0 + A_1B_1$ is nonnegative, $z_1 = A_0B_1 + A_1B_0$.

*Line L6.*

$$z_0 + z_1\beta^h + z_2\beta^{2h} = A_0B_0 + (A_0B_1 + A_1B_0)\beta^h + A_1B_1\beta^{2h} = (A_1\beta^h + A_0)(B_1\beta^h + B_0) = \langle a \rangle\langle b \rangle .$$

All three terms are nonnegative, so every partial sum is at most $\langle a \rangle\langle b \rangle < \beta^{2n}$, and the result fits in $2n$ limbs; the limbs above position $2n$ of the buffer are 0 and are cut off.

*Termination.* Each call with $n > T$ makes three calls on $h < n$ limbs and otherwise a finite number of operations, so by induction every call terminates. The depth of the recursion is at most the number of halvings $n \mapsto \lceil n/2 \rceil$ needed to reach $T$, which is $\lceil \log_2 (n/T) \rceil$ for $T \ge 1$, plus one. $\blacksquare$

**Corollary (cost).** Let $M(n)$ be the number of limb operations, with $M(n) \le cn^2$ for $n \le T$ and $M(n) \le 3M(\lceil n/2 \rceil) + c'n$ for $n > T$. For $n = 2^jT$ the recursion tree has $3^i$ nodes of size $n/2^i$ at level $i$, with cost $c'n(3/2)^i$, so

$$M(n) \le \sum_{i=0}^{j-1} c'n(3/2)^i + 3^j cT^2 \le 2c'n(3/2)^j + cT^2 3^j = O(3^j) = O\big((n/T)^{\log_2 3}\big),$$

using $(3/2)^j n = 3^j T$ and $3^j = (n/T)^{\log_2 3}$. Monotonicity extends this to all $n$, and the $3^j$ leaf products give the matching lower bound, so $M(n) = \Theta(n^{\log_2 3})$ for fixed $T$.
