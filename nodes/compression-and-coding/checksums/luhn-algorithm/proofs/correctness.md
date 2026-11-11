---
title: The Luhn check digit makes the total 0 mod 10, catches every single error, and misses only 09 and 90 among adjacent swaps
proves: [correctness]
status: full
---

Let $D(x) = 2x$ for $0 \le x \le 4$ and $D(x) = 2x - 9$ for $5 \le x \le 9$. For a digit string $y$ read from the right as $y_1, y_2, \ldots$ and a flag $f$, let $T(y, f) = \sum_i g_i(y_i)$, where $g_i = D$ for the doubled places and $g_i$ is the identity otherwise; with $f$ false the doubled places are the even ones, and with $f$ true the odd ones.

**Lemma 1 (the loop).** LUHN-SUM$(y, f)$ returns $T(y, f) \bmod 10$.

*Proof.* The loop of line L3 visits $y_1, y_2, \ldots$ in this order. Line L2 starts the flag $d$ at $f$, and line L5 flips it after each digit, so $d$ is $f$ at odd places and not $f$ at even places. So $d$ is true exactly at the doubled places, and line L4 adds $g_i(y_i)$. Line L6 reduces the total. $\square$

**Lemma 2 (D is a permutation).** $D$ maps $\{0, \ldots, 9\}$ onto itself, and $D(a) \not\equiv D(b) \pmod{10}$ for $a \ne b$.

*Proof.* $D$ maps $0, \ldots, 4$ to the even digits $0, 2, 4, 6, 8$ and $5, \ldots, 9$ to the odd digits $1, 3, 5, 7, 9$, each in increasing order. So it is a bijection, and since all values are in $[0, 9]$, distinct values are distinct mod 10. $\square$

**Theorem 1 (generation).** For every payload $p$, the code word $w = p\,c$ with $c$ from line L7 passes line L8.

*Proof.* In $w$, the check digit is $w_1$ and the payload digit $p_j$ (from the right) is $w_{j+1}$. So the even places of $w$ are the odd places of $p$, and $T(w, \text{false}) = c + T(p, \text{true})$. Let $t = T(p, \text{true}) \bmod 10$, which is what line L7 uses by Lemma 1. Then $c = (10 - t) \bmod 10$ and $c + T(p, \text{true}) \equiv 0 \pmod{10}$. By Lemma 1, line L8 returns true. $\square$

**Theorem 2 (single errors).** If one digit of a valid code word changes, the result is invalid.

*Proof.* Let place $i$ change from $a$ to $b \ne a$. The total changes by $g_i(b) - g_i(a)$. If $g_i$ is the identity, this is $b - a$, with $0 < |b - a| \le 9$. If $g_i = D$, it is $D(b) - D(a)$, which is nonzero mod 10 by Lemma 2. In both cases the new total is not $0 \bmod 10$. $\square$

**Theorem 3 (adjacent transpositions).** If two adjacent digits $a \ne b$ of a valid code word are swapped, the result is valid if and only if $\{a, b\} = \{0, 9\}$.

*Proof.* Of two adjacent places, exactly one is doubled. Say the doubled place holds $a$ before the swap and $b$ after it. The total changes from $D(a) + b$ to $a + D(b)$ in these two places, so by the change
$$(a + D(b)) - (D(a) + b) = (D(b) - b) - (D(a) - a).$$
Let $h(x) = D(x) - x$, which is $x$ for $x \le 4$ and $x - 9$ for $x \ge 5$. Modulo 10, $h$ takes the values $0, 1, 2, 3, 4, 6, 7, 8, 9, 0$ for $x = 0, \ldots, 9$. The swap is missed if and only if $h(a) \equiv h(b)$, and the list shows that this happens for $a \ne b$ only when $\{a, b\} = \{0, 9\}$. $\square$

**Theorem 4 (twin errors).** A change $aa \to bb$ of two adjacent equal digits, $a \ne b$, is missed if and only if $\{a, b\}$ is $\{2, 5\}$, $\{3, 6\}$ or $\{4, 7\}$.

*Proof.* Exactly one of the two places is doubled, so the total changes by $E(b) - E(a)$ with $E(x) = D(x) + x$. Modulo 10, $E$ takes the values $0, 3, 6, 9, 2, 6, 9, 2, 5, 8$ for $x = 0, \ldots, 9$. The equal values for different digits are 6 at 2 and 5, 9 at 3 and 6, and 2 at 4 and 7. $\square$

**Theorem 5 (jump transpositions).** Every change $acb \to bca$ is missed.

*Proof.* Places $i$ and $i + 2$ are both doubled or both not, so $g_i = g_{i+2}$, and swapping their digits does not change the total. $\square$

**Cost.** By Lemma 1, each of LUHN-SUM, CHECK-DIGIT and IS-VALID does one lookup and one addition per digit, so it takes $\Theta(n)$ time and $O(1)$ extra space. $\blacksquare$
