---
title: Casting out nines never rejects a correct result and misses exactly the errors that are multiples of 9
proves: [correctness]
status: full
---

Let $x = \sum_{i=0}^{k-1} d_i 10^i$ with decimal digits $d_i$. Write $t$ for the true result $a + b$ or $a b$, and $c$ for the claimed result.

**Lemma 1 (digit sum).** $x \equiv \sum_i d_i \pmod 9$.

*Proof.* $10 \equiv 1 \pmod 9$, so $10^i \equiv 1^i = 1$, and $d_i 10^i \equiv d_i$. Summing over $i$ gives the claim. $\square$

**Lemma 2 (the loop).** EXCESS9$(x)$ returns $x \bmod 9$.

*Proof.* Invariant: after the loop of line L2 has read some digits, $0 \le r \le 8$ and $r \equiv$ the sum of those digits $\pmod 9$. It holds after line L1 with no digits read. Line L3 adds a digit $d \le 9$, so $r \le 17$ and the congruence still holds. Line L4 subtracts 9 when $r \ge 9$, which keeps the congruence and brings $r$ into $0..8$. At the end, $r$ is the digit sum mod 9 and lies in $0..8$, so by Lemma 1 it equals $x \bmod 9$. $\square$

**Theorem 1 (the rule).** CHECK-ADDITION$(a, b, c)$ and CHECK-MULTIPLICATION$(a, b, c)$ return true if and only if $c \equiv t \pmod 9$.

*Proof.* By Lemma 2, line L6 compares $((a \bmod 9) + (b \bmod 9)) \bmod 9 = (a + b) \bmod 9$ with $c \bmod 9$, and line L7 compares $((a \bmod 9)(b \bmod 9)) \bmod 9 = a b \bmod 9$ with $c \bmod 9$. These are equal exactly when $c \equiv t \pmod 9$. $\square$

**Corollary 1 (no false alarm).** If $c = t$, the check returns true. So a false result proves $c \ne t$.

**Corollary 2 (the missed errors).** A wrong result $c \ne t$ passes if and only if $9 \mid c - t$. In particular these pass:

- any permutation of the digits of $t$, since by Lemma 1 it has the same digit sum;
- a digit 0 changed to 9 or back, a change of $\pm 9 \cdot 10^i$;
- $c = 10 t$, a change of $9t$;
- a partial product $p 10^i$ written one column too far left, a change of $9 p 10^i$.

A change of one digit by $k$ with $1 \le k \le 8$ changes $c$ by $\pm k 10^i$, which is not a multiple of 9 because $\gcd(10^i, 9) = 1$; so it is caught. $\square$

**Lemma 3 (elevens).** $x \equiv \sum_i (-1)^i d_i \pmod{11}$, and the elevens checks pass if and only if $c \equiv t \pmod{11}$.

*Proof.* $10 \equiv -1 \pmod{11}$, so $10^i \equiv (-1)^i$. The implementation adds the digits at even places from the right and subtracts the others, reducing mod 11 at each step, so it returns $x \bmod 11$; the rest is as in Theorem 1. $\square$

**Theorem 2 (adjacent swaps under elevens).** Swapping two different adjacent digits $a \ne b$ of $t$ is caught by casting out elevens, and swapping two different digits two places apart is not.

*Proof.* The adjacent swap changes the value by $\pm(10a + b - 10b - a)10^i = \pm 9(a - b)10^i$. Since 11 is prime and divides none of $9$, $a - b$ (as $0 < |a - b| \le 9$) and $10^i$, it does not divide the change. The swap two places apart changes the value by $\pm 99(a - b) 10^i$, a multiple of 11. $\square$

**Theorem 3 (both checks).** A result passes both checks if and only if $c \equiv t \pmod{99}$.

*Proof.* By Theorem 1 and Lemma 3, passing both means $9 \mid c - t$ and $11 \mid c - t$. Since $\gcd(9, 11) = 1$, this is the same as $99 \mid c - t$, by the Chinese remainder theorem. $\square$

**Cost.** By Lemma 2, EXCESS9 does one addition and at most one subtraction per digit, so a check on numbers with $n$ digits in total takes $\Theta(n)$ time and $O(1)$ extra space. $\blacksquare$
