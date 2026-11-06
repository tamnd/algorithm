---
title: Binary GCD returns gcd(a, b) after at most 1 + lg(ab) passes and O(n^2) bit operations
proves: [correctness, termination, time.worst, bit_operations.worst]
status: full
---

We use the pseudocode BINARY-GCD of the page. The inputs $a_0, b_0$ are any integers, and $g = \gcd(a_0, b_0)$, with $\gcd(x, 0) = |x|$ and $\gcd(0, 0) = 0$. For $x > 0$, $\operatorname{tz}(x)$ is the exponent of $2$ in $x$, so $x = 2^{\operatorname{tz}(x)} u$ with $u$ odd.

**Lemma 1 (three gcd rules).** Let $u, v \ge 1$ be integers.

1. If $u$ is odd, then $\gcd(u, 2^s v) = \gcd(u, v)$ for each $s \ge 0$.
2. $\gcd(u, v) = \gcd(u, v - u)$.
3. If $k = \min(\operatorname{tz}(u), \operatorname{tz}(v))$, then $\gcd(u, v) = 2^k \gcd(u / 2^{\operatorname{tz}(u)}, v / 2^{\operatorname{tz}(v)})$.

*Proof.* (1) A common divisor of $u$ and $v$ divides $2^s v$. Conversely, let $d$ divide $u$ and $2^s v$. Since $u$ is odd, $d$ is odd, so $\gcd(d, 2^s) = 1$, and $d \mid 2^s v$ gives $d \mid v$ by Gauss's lemma. So the two pairs have the same common divisors. (2) $d$ divides $u$ and $v$ if and only if it divides $u$ and $v - u$. (3) Write $u = 2^{s} u'$ and $v = 2^{t} v'$ with $u', v'$ odd, $s \le t$ say, so $k = s$. Then $\gcd(u, v) = 2^s \gcd(u', 2^{t-s} v')$, because $\gcd(cx, cy) = c \gcd(x, y)$ for $c \ge 1$, and $\gcd(u', 2^{t-s} v') = \gcd(u', v')$ by rule 1. $\square$

**Theorem 1 (correctness).** BINARY-GCD$(a_0, b_0)$ stops and returns $g$.

*Proof.* After line L1, $a = |a_0|$, $b = |b_0|$, and $\gcd(a, b) = g$. If $a = 0$, line L2 returns $b = g$; if $b = 0$, line L3 returns $a = g$. Otherwise $a, b \ge 1$. Line L4 sets $k = \operatorname{tz}(a \mathbin{\mathrm{or}} b)$, which is $\min(\operatorname{tz}(a), \operatorname{tz}(b))$, since the lowest $1$ digit of $a \mathbin{\mathrm{or}} b$ is the lower of the lowest $1$ digits of $a$ and $b$. Let $a_1 = a / 2^{\operatorname{tz}(a)}$ and $b_1 = b / 2^{\operatorname{tz}(b)}$. By Lemma 1 (3), $g = 2^k \gcd(a_1, b_1) = 2^k \gcd(a_1, b)$, the last step by rule 1. Line L5 sets $a = a_1$. We use this invariant at the start of each pass of the loop L6 to L10:

> **(I)** $a$ is odd, $b \ge 1$, and $2^k \gcd(a, b) = g$.

*Initialization.* Shown above.

*Maintenance.* Line L7 makes $b$ odd; by rule 1, $\gcd(a, b)$ does not change. Line L8 swaps if needed, so now $a \le b$ and both are odd. Line L9 sets $b \leftarrow b - a \ge 0$, and rule 2 keeps the gcd. If $b \ge 1$ after line L9, the loop goes on and (I) holds: $a$ is odd and $b \ge 1$.

*Exit.* The loop exits at line L10 when $b - a = 0$, so $a = b$ and $\gcd(a, b) = a$. Then $g = 2^k a$, which line L11 returns. Termination follows from Theorem 2. $\blacksquare$

**Theorem 2 (number of passes).** If $a_0 b_0 \ne 0$, the loop runs at most $1 + \lg(|a_0| \cdot |b_0|)$ times. If the inputs have at most $n$ binary digits, this is at most $2n + 1$.

*Proof.* For pass $i$, let $P_i = a \cdot b$ right after line L8 of that pass. At that moment $a \le b$, both odd. If the pass does not exit, line L9 makes $b - a$, which is even and at least $2$, and line L7 of the next pass divides it by at least $2$. So the next pass starts its line L8 with the pair $a$ and $(b - a)/2^{s}$, $s \ge 1$, in some order, and

$$P_{i+1} \le a \cdot \frac{b - a}{2} < \frac{a b}{2} = \frac{P_i}{2}.$$

Let the loop run $t$ passes. Then $1 \le P_t < P_1 / 2^{t-1}$ when $t \ge 2$, so $2^{t-1} < P_1$. Lines L5 and L7 only divide, so $P_1 \le |a_0| \cdot |b_0|$. This gives $t < 1 + \lg(|a_0| |b_0|)$ for $t \ge 2$, and the bound holds for $t = 1$ too. Since $|a_0|, |b_0| < 2^n$, $t \le 2n + 1$. $\blacksquare$

**Tightness.** On $(2^n - 1, 1)$ the loop runs exactly $n$ times: the pair is $(1, 2^j - 1)$, line L9 gives $2^j - 2$, and line L7 gives $2^{j-1} - 1$. So the number of passes is $\Theta(n)$ in the worst case.

**Theorem 3 (time and bit operations).** On the word RAM with a constant-time count of trailing zeros, BINARY-GCD uses $O(n)$ word operations. On inputs of at most $n$ binary digits, it uses $O(n^2)$ bit operations.

*Proof.* Each pass does a constant number of shifts, comparisons, subtractions and trailing zero counts, so the word bound follows from Theorem 2. In the bit model, each of these operations on numbers of at most $n$ digits costs $O(n)$ bit operations: a shift by $s$ places costs $O(n)$, and $\operatorname{tz}$ by a scan from the low end costs $O(1 + \operatorname{tz}(x))$. Lines L1 to L5 and L11 cost $O(n)$, and there are $O(n)$ passes of $O(n)$ each, so the total is $O(n^2)$. If $\operatorname{tz}$ is computed by testing one digit at a time, the total count of digits shifted out over the whole run is at most $\lg |a_0| + \lg |b_0| \le 2n$, since each shift by one place halves a value that stays at least $1$; this does not change the bounds. $\blacksquare$
