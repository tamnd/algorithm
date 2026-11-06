---
title: Correctness of Montgomery multiplication
proves: [correctness, termination]
status: full
---

Let $n \ge 1$ be odd, let $r$ be the number of binary digits of $n$, and let $R = 2^r$. Then $2^{r-1} \le n < 2^r$, so $R > n$, and $\gcd(n, R) = 1$ because $n$ is odd. So $R$ has an inverse $R^{-1}$ modulo $n$. (The same proof works for any $r$ with $2^r > n$.)

**Lemma 1 (setup, lines L2 to L6).** The loop of lines L4 and L5 terminates, and afterwards $nx \equiv 1 \pmod R$. Hence $n' = (-x) \bmod R$ satisfies $n n' \equiv -1 \pmod R$ and $0 \le n' < R$.

*Proof.* We show the invariant $nx \equiv 1 \pmod{2^j}$. At the start, $x = 1$, $j = 1$, and $n \cdot 1 \equiv 1 \pmod 2$ because $n$ is odd. Suppose $nx \equiv 1 \pmod{2^j}$ before a pass, and let $j' = \min(2j, r)$ and $x' = x(2 - nx) \bmod 2^{j'}$. Then

$$1 - n x(2 - nx) = 1 - 2nx + (nx)^2 = (1 - nx)^2,$$

and $2^j \mid 1 - nx$ gives $2^{2j} \mid (1 - nx)^2$, so $nx(2 - nx) \equiv 1 \pmod{2^{2j}}$ and hence modulo $2^{j'}$, since $j' \le 2j$. Reducing $x(2 - nx)$ modulo $2^{j'}$ does not change this congruence. So the invariant holds after the pass. Each pass strictly increases $j$, because $j < r$ and $j \ge 1$ give $\min(2j, r) > j$, and $j$ never exceeds $r$. So the loop stops, with $j = r$, and then $nx \equiv 1 \pmod{2^r}$. Line L6 gives $n n' \equiv -nx \equiv -1 \pmod R$. $\square$

Line L7 sets $R2 = R^2 \bmod n$ by ordinary division with remainder.

**Lemma 2 (REDC, lines L8 to L11).** For every integer $T$ with $0 \le T < nR$, REDC$(T)$ returns $t$ with $0 \le t < n$ and $t \equiv T R^{-1} \pmod n$.

*Proof.* Line L8 sets $m = ((T \bmod R) \cdot n') \bmod R$, so $0 \le m < R$ and $m \equiv T n' \pmod R$. Then

$$T + mn \equiv T + T n' n \equiv T + T \cdot (-1) = 0 \pmod R$$

by Lemma 1. So $R$ divides $T + mn$, and $t = (T + mn)/R$ in line L9 is an integer. The equation $tR = T + mn$ gives $tR \equiv T \pmod n$, and multiplying by $R^{-1}$ gives $t \equiv T R^{-1} \pmod n$.

Bounds: $T + mn \ge 0$, so $t \ge 0$. And $T < nR$ and $m \le R - 1$ give $T + mn < nR + (R - 1) n < 2nR$, so $t < 2n$. If $t \ge n$, line L10 replaces $t$ by $t - n$, which lies in $[0, n)$ and is congruent to $t$ modulo $n$. If $t < n$, it is already in $[0, n)$. In both cases the returned value is the unique residue in $[0, n)$ congruent to $TR^{-1}$, that is, $TR^{-1} \bmod n$. $\square$

**Theorem.** For $a, b \in \{0, \ldots, n - 1\}$, write $\tilde a = aR \bmod n$ for the Montgomery form. Then:

1. TO-MONT$(a) = \tilde a$;
2. FROM-MONT$(\tilde a) = a$;
3. MONT-MUL$(\tilde a, \tilde b) = \widetilde{ab \bmod n}$;
4. FROM-MONT$($MONT-MUL$($TO-MONT$(a)$, TO-MONT$(b))) = ab \bmod n$.

*Proof.* (1) The argument of REDC in line L13 is $T = a \cdot R2$ with $0 \le a < n$ and $0 \le R2 < n < R$, so $0 \le T < nR$. By Lemma 2 the result is $\equiv a R^2 R^{-1} = aR \pmod n$ and lies in $[0, n)$, so it equals $\tilde a$.

(2) In line L14, $T = \tilde a < n < nR$, so Lemma 2 gives $\tilde a R^{-1} \equiv aRR^{-1} = a$, and the result in $[0, n)$ is $a$.

(3) In line L12, $T = \tilde a \tilde b$ with $0 \le \tilde a, \tilde b < n$, so $0 \le T < n^2 < nR$. Lemma 2 gives $\tilde a \tilde b R^{-1} \equiv aR \cdot bR \cdot R^{-1} = abR \pmod n$, and the result in $[0, n)$ is $(ab \bmod n) R \bmod n$.

(4) follows from (1), (3) and (2), applied in this order to $ab \bmod n$. $\blacksquare$

**Termination.** The setup loop terminates by Lemma 1, and REDC, MONT-MUL, TO-MONT and FROM-MONT have no loops. So every call returns.

**Exponentiation.** By (3), every MONT-MUL in square-and-multiply maps forms to forms; so if the accumulator starts as the form of $1$ and the base as the form of $x$, then after processing the exponent $e$ the accumulator is the form of $x^e \bmod n$, and FROM-MONT returns $x^e \bmod n$ by (2).
