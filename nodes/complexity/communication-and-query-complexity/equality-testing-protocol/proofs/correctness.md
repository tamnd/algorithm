---
title: The equality testing protocol has one-sided error at most (n-1)/q and sends 2⌈log2 q⌉ + 1 bits
proves: [correctness]
status: full
---

Alice holds $x \in \{0,1\}^n$ and Bob holds $y \in \{0,1\}^n$. For a string $s$ we write $A_s(z) = s_1 + s_2 z + \cdots + s_n z^{n-1}$, a polynomial with integer coefficients. Line L1 fixes $q$, the least prime with $q \ge \max(2, n^2)$. We write $w = \lceil \log_2 q \rceil$, the number of bits that write each of $0, \ldots, q-1$ in binary. All arithmetic on values of $A_s$ is in the field $\mathbb{F}_q$ of integers modulo $q$.

**Lemma 1 (roots).** A polynomial $P \ne 0$ of degree at most $d$ over a field $\mathbb{F}$ has at most $d$ roots in $\mathbb{F}$.

*Proof.* By induction on $d$. A nonzero polynomial of degree $0$ is a nonzero constant and has no root. Let $d \ge 1$. If $P$ has no root, we are done. If $P(c) = 0$, divide $P$ by $z - c$: $P(z) = (z - c) Q(z) + P(c) = (z - c) Q(z)$, where $Q \ne 0$ has degree at most $d - 1$. A field has no zero divisors, so $P(t) = 0$ gives $t = c$ or $Q(t) = 0$. By induction $Q$ has at most $d - 1$ roots, so $P$ has at most $d$. $\square$

**Lemma 2 (decoding).** Bob reads the values $r$ and $a$ that Alice computed.

*Proof.* Both values are in $\{0, \ldots, q-1\}$, and $q - 1 < 2^w$, so each one has a binary form of exactly $w$ bits (line L4). Bob knows $n$, so he computes the same $q$ and $w$ at line L1. He splits the first $2w$ bits of the transcript into two halves and reads $r$ and $a$ back. $\square$

**Theorem.** For every pair $(x, y)$:

1. If $x = y$, both players output 1 with probability 1.
2. If $x \ne y$, both players output 1 with probability at most $(n-1)/q$, and output 0 otherwise. For $n \ge 2$ this is less than $1/n$.
3. Every transcript has exactly $2w + 1$ bits, and $w \le \lceil \log_2 (2n^2) \rceil$ for $n \ge 2$.
4. Both players know the output at the end.

*Proof.* By Lemma 2, Bob uses the same $r$ that Alice drew at line L2, and the same $a = A_x(r) \bmod q$ that she computed at line L3. At line L5 he computes $b = A_y(r) \bmod q$.

Part 1. If $x = y$, then $A_x$ and $A_y$ are the same polynomial, so $a = b$ for every $r$. Bob sends 1 at line L6, for every value of the random point.

Part 2. Let $x \ne y$ and let $D = A_x - A_y$. Its coefficient of $z^{i-1}$ is $x_i - y_i \in \{-1, 0, 1\}$. There is an index $i$ with $x_i \ne y_i$, and for it $x_i - y_i = \pm 1$. Since $q \ge 2$, $\pm 1 \not\equiv 0 \pmod q$, so $D$ is a nonzero polynomial over $\mathbb{F}_q$. Its degree is at most $n - 1$. By Lemma 1, $D$ has at most $n - 1$ roots in $\mathbb{F}_q$. Bob sends 1 exactly when $a = b$, that is, when $D(r) = 0$ in $\mathbb{F}_q$. The point $r$ is uniform over the $q$ elements of $\mathbb{F}_q$, so

$$\Pr[\text{output } 1] = \frac{|\{r \in \mathbb{F}_q : D(r) = 0\}|}{q} \le \frac{n-1}{q}.$$

When $D(r) \ne 0$, Bob sends 0, which is the correct answer. For $n \ge 2$, $q \ge n^2$ gives $(n-1)/q \le (n-1)/n^2 < 1/n$.

Part 3. Line L4 sends $2w$ bits and line L6 sends 1 bit, and no other line sends anything, so the length is $2w + 1$ on every input and for every $r$. For $n \ge 2$, Bertrand's postulate gives a prime $p$ with $n^2 < p < 2n^2$. The least prime $q \ge n^2$ is at most $p$, so $q - 1 < 2n^2$ and $w = \lceil \log_2 q \rceil \le \lceil \log_2 (2n^2) \rceil$.

Part 4. The last bit of the transcript is Bob's answer. Alice receives it, so at line L7 both players output the same bit. $\blacksquare$

**Corollary.** With $n \ge 2$, the protocol is a private-coin protocol for the equality problem with one-sided error less than $1/n \le 1/2$ and cost $2\lceil \log_2 q \rceil + 1 \le 4\log_2 n + 5$ bits. For $n \ge 2$ the error is at most $1/5$, below the usual threshold of $1/3$.

*Proof.* $\lceil \log_2(2n^2) \rceil \le 2\log_2 n + 2$, so $2w + 1 \le 4\log_2 n + 5$. The error bound $(n-1)/q$ is $1/5$ for $n = 2$, $q = 5$, and it is at most $(n-1)/n^2 \le 2/9$ for $n \ge 3$. $\blacksquare$
