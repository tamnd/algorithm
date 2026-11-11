---
title: The affine cipher is a bijection exactly for units a, and two pairs fix the key unless the letters differ by 0 or 13
proves: [correctness]
status: full
---

We work in $\mathbb{Z}_{26}$ and write $E_{a,b}(x) = (ax + b) \bmod 26$. A *unit* is an $a$ with $\gcd(a, 26) = 1$; the units are the odd numbers of $\{1, \ldots, 25\}$ other than $13$.

**Claim 1.** $E_{a,b}$ is a bijection of $\mathbb{Z}_{26}$ if and only if $a$ is a unit. Then $D_{a,b}(y) = a^{-1}(y - b) \bmod 26$ satisfies $D_{a,b}(E_{a,b}(x)) = x$ for each $x$.

*Proof.* Let $g = \gcd(a, 26)$. If $g > 1$, then $x = 26/g$ is in $\{1, \ldots, 25\}$ and $a x = (a/g) \cdot 26 \equiv 0$, so $E_{a,b}(26/g) = b = E_{a,b}(0)$, and $E_{a,b}$ is not injective. If $g = 1$, the extended Euclidean algorithm gives integers $s, t$ with $sa + 26t = 1$, so $a^{-1} = s \bmod 26$ exists. Then $a^{-1}((ax + b) - b) \equiv a^{-1} a x \equiv x$, and since $x \in \{0, \ldots, 25\}$ the reduction gives exactly $x$. So $D_{a,b}$ is a left inverse of $E_{a,b}$ on the finite set $\mathbb{Z}_{26}$, and $E_{a,b}$ is a bijection. Lines L1 to L4 compute exactly these maps letter by letter. $\square$

**Claim 2 (the number of keys).** There are exactly $312$ keys, and different keys give different maps.

*Proof.* There are 12 units and 26 values of $b$, so $12 \cdot 26 = 312$ pairs. If $E_{a,b} = E_{a',b'}$, then the value at $0$ gives $b = b'$ and the value at $1$ gives $a + b = a' + b'$, so $a = a'$. $\square$

**Claim 3 (two known pairs).** Let $(a, b)$ be a key, let $x_1, x_2 \in \mathbb{Z}_{26}$, and let $y_j = E_{a,b}(x_j)$. Let $\Delta x = (x_1 - x_2) \bmod 26$. The set $K$ of keys $(a', b')$ with $E_{a',b'}(x_1) = y_1$ and $E_{a',b'}(x_2) = y_2$ is $\{(a, b)\}$ if $\Delta x \notin \{0, 13\}$, and has exactly 12 keys if $\Delta x \in \{0, 13\}$. AFFINE-RECOVER returns $K$.

*Proof.*

1. A key $(a', b')$ is in $K$ if and only if $a' x_1 + b' \equiv y_1$ and $a' \Delta x \equiv y_1 - y_2$. The first equation fixes $b' = (y_1 - a' x_1) \bmod 26$, and the second one is the difference of the two equations. So $K$ is in bijection with the set $U$ of units $a'$ with $a' \Delta x \equiv y_1 - y_2 = a \Delta x$.
2. The condition $a' \Delta x \equiv a \Delta x \pmod{26}$ is $(a' - a)\Delta x \equiv 0 \pmod{26}$. Since $26 = 2 \cdot 13$ with $\gcd(2, 13) = 1$, by the Chinese remainder theorem it holds if and only if $(a' - a)\Delta x \equiv 0 \pmod 2$ and $(a' - a)\Delta x \equiv 0 \pmod{13}$.
3. The condition modulo 2 always holds: both $a$ and $a'$ are units, so both are odd, and $a' - a$ is even.
4. If $13 \nmid \Delta x$, then $\Delta x$ is invertible modulo the prime 13, so the condition modulo 13 gives $a' \equiv a \pmod{13}$. Also $a' \equiv a \equiv 1 \pmod 2$. By the Chinese remainder theorem, $a' \equiv a \pmod{26}$, so $U = \{a\}$ and $K = \{(a, b)\}$.
5. If $13 \mid \Delta x$, which for $\Delta x \in \{0, \ldots, 25\}$ means $\Delta x \in \{0, 13\}$, then $(a' - a)\Delta x$ is a multiple of $2 \cdot 13$ for each unit $a'$, so $U$ holds all 12 units and $|K| = 12$.
6. Lines L7 and L8 test each unit $a'$ against the condition of step 1 and append $(a', (y_1 - a' x_1) \bmod 26)$ exactly when it holds. So the list of line L9 is $K$, in increasing order of $a'$. $\square$

The three claims prove that decryption inverts encryption, that the key space has 312 keys, and that the key recovery of the page is correct and returns a single key in all cases except $\Delta x \in \{0, 13\}$. $\blacksquare$
