---
title: Gosper's hack returns the next larger word with the same number of ones
proves: [correctness]
status: full
---

All arithmetic is on unsigned $w$-bit words, modulo $2^w$. For an integer $v \ge 0$ we write $\operatorname{pop}(v)$ for the number of ones in its binary form.

**Setup.** Let $0 < x < 2^w$. Let $t$ be the number of trailing zeros of $x$, and let $m \ge 1$ be the length of the block of ones that starts at bit $t$, so that bits $t, \ldots, t + m - 1$ of $x$ are ones and bit $t + m$ is a zero or lies outside the word. Then there is a unique integer $a \ge 0$ with
$$ x = a \cdot 2^{t+m+1} + (2^m - 1) \cdot 2^t . $$
We assume $t + m < w$, that is, the block does not end at the top bit of the word.

**Claim.** Under this assumption, GOSPER-NEXT$(x)$ returns $z = a \cdot 2^{t+m+1} + 2^{t+m} + 2^{m-1} - 1$, and $z$ is the least integer $y > x$ with $\operatorname{pop}(y) = \operatorname{pop}(x)$. Also $z < 2^w$.

*Step 1: the value of each line.*

- Line L1. In two's complement, $-x = 2^w - x$. The low $t$ bits of $x$ are 0 and bit $t$ is 1, so the low $t$ bits of $2^w - x$ are 0, bit $t$ is 1, and each bit above $t$ is the complement of the bit of $x$. The AND keeps only bit $t$. So $smallest = 2^t$.
- Line L2. $x + 2^t = a \cdot 2^{t+m+1} + (2^m - 1) \cdot 2^t + 2^t = a \cdot 2^{t+m+1} + 2^{t+m}$. Since $t + m < w$ and $x < 2^w$, bit $t + m$ of $x$ is a zero inside the word, so $a \cdot 2^{t+m+1} + 2^{t+m} < 2^w$ and no wrap-around happens. So $ripple = a \cdot 2^{t+m+1} + 2^{t+m}$.
- Line L3. $x$ and $ripple$ agree on the bits $t + m + 1$ and above (both hold $a$) and on the bits below $t$ (both 0). On bits $t$ to $t + m - 1$, $x$ has ones and $ripple$ zeros; on bit $t + m$, $x$ has a zero and $ripple$ a one. So $ones = (2^{m+1} - 1) \cdot 2^t$.
- Line L4. A logical shift right by 2 is $\lfloor \cdot / 4 \rfloor$, and unsigned division by $2^t$ is $\lfloor \cdot / 2^t \rfloor$. For integers $N \ge 0$ and $b, c \ge 1$, $\lfloor \lfloor N / b \rfloor / c \rfloor = \lfloor N / (bc) \rfloor$. So the new value is $\lfloor (2^{m+1} - 1) \cdot 2^t / 2^{t+2} \rfloor = \lfloor (2^{m+1} - 1)/4 \rfloor$. Since $(2^{m+1} - 1)/4 = 2^{m-1} - 1/4$ and $2^{m-1} - 1$ is an integer when $m \ge 1$, this is $2^{m-1} - 1$.
- Line L5. $2^{m-1} - 1 < 2^{m-1} \le 2^{t+m}$, so the ones of $2^{m-1} - 1$ lie below the lowest one of $ripple$, and the OR is a sum: the result is $z = a \cdot 2^{t+m+1} + 2^{t+m} + 2^{m-1} - 1$, and $z < 2^{t+m+1}(a + 1) \le 2^w$.

*Step 2: $z$ has the right count and is larger.* The three parts of $z$ use disjoint bits, so $\operatorname{pop}(z) = \operatorname{pop}(a) + 1 + (m - 1) = \operatorname{pop}(a) + m = \operatorname{pop}(x)$. The integers $z$ and $x$ agree on the bits above $t + m$, and at bit $t + m$ the integer $z$ has a 1 and $x$ a 0. So $z > x$.

*Step 3: $z$ is the least.* Let $y > x$ with $\operatorname{pop}(y) = \operatorname{pop}(x)$. Let $p$ be the highest bit where $y$ and $x$ differ. Since $y > x$, bit $p$ of $y$ is 1 and bit $p$ of $x$ is 0.

- Case $p < t$. Then all ones of $x$ lie above $p$ (the lowest one is at $t$), and $y$ has the same bits as $x$ above $p$ and one more 1 at bit $p$. So $\operatorname{pop}(y) \ge \operatorname{pop}(x) + 1$, a contradiction.
- Case $t \le p \le t + m - 1$. Bit $p$ of $x$ is 1, a contradiction.
- Case $p > t + m$. Then $z$ and $y$ agree with $x$ above $p$, bit $p$ of $z$ is bit $p$ of $x$, which is 0, and bit $p$ of $y$ is 1. So $z < y$.
- Case $p = t + m$. Then $y$ and $z$ agree on all bits from $t + m$ up. Let $\ell = y \bmod 2^{t+m}$. The ones of $y$ at bit $t + m$ and above number $\operatorname{pop}(a) + 1$, so $\operatorname{pop}(\ell) = \operatorname{pop}(x) - \operatorname{pop}(a) - 1 = m - 1$. An integer with $m - 1$ ones is at least $2^{m-1} - 1$, the integer whose ones are the $m - 1$ lowest bits. So $\ell \ge 2^{m-1} - 1 = z \bmod 2^{t+m}$, and $y \ge z$.

In each possible case $y \ge z$. With Step 2, $z$ is the least integer above $x$ with $\operatorname{pop}(x)$ ones. $\blacksquare$

**The case $t + m = w$.** Then $x = (2^m - 1) \cdot 2^{w-m}$ is the largest $w$-bit word with $m$ ones, so no answer exists inside the word. Line L2 wraps to $ripple = 0$, line L3 gives $ones = x$, and line L4 gives $\lfloor (2^m - 1) \cdot 2^{w-m} / 2^{w-m+2} \rfloor = \lfloor (2^m - 1)/4 \rfloor$, which is $2^{m-2} - 1$ for $m \ge 2$ and 0 for $m = 1$. The result is smaller than $x$ and has $\max(m - 2, 0)$ ones, so a caller must stop before this call.

**Enumeration.** Let $0 < k \le n < w$, start with $x_0 = 2^k - 1$, and set $x_{i+1} = $ GOSPER-NEXT$(x_i)$ while $x_i < 2^n$. Each $x_i < 2^n$ has its top bit at most $n - 1 < w - 1$, so the assumption $t + m < w$ holds and the claim applies. By the claim, the sequence is strictly increasing and contains every integer in $[x_0, 2^n)$ with $k$ ones. The least integer with $k$ ones is $2^k - 1 = x_0$. So the values below $2^n$ are exactly the $\binom{n}{k}$ masks of the $k$-subsets of $\{0, \ldots, n - 1\}$, in increasing order, and the loop stops after $\binom{n}{k}$ values, because the strictly increasing sequence of integers with $k$ ones has only $\binom{n}{k}$ terms below $2^n$. $\blacksquare$
