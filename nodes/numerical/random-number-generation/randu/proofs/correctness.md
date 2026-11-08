---
title: The plane identity and the period of RANDU
proves: [correctness]
status: full
---

Let $m = 2^{31}$, $a = 65539 = 2^{16} + 3$, and let $x_0$ be odd with $0 < x_0 < m$. Let $x_{i+1} = a x_i \bmod m$ and $u_i = x_i / m$.

**Lemma 1 (line L1).** $(2^{16} x + 2 x + x) \bmod m = a x \bmod m$ for every integer $x$.

*Proof.* $2^{16} x + 2x + x = (2^{16} + 3) x = a x$. $\square$

**Lemma 2 (the plane identity).** $a^2 \equiv 6 a - 9 \pmod m$, and $x_{i+2} \equiv 6 x_{i+1} - 9 x_i \pmod m$ for all $i \ge 0$.

*Proof.* $a^2 = 2^{32} + 6 \cdot 2^{16} + 9$ and $6 a - 9 = 6 \cdot 2^{16} + 9$. Their difference is $2^{32}$, a multiple of $2^{31}$. Then $x_{i+2} \equiv a^2 x_i \equiv (6a - 9) x_i = 6 (a x_i) - 9 x_i \equiv 6 x_{i+1} - 9 x_i$. $\square$

**Theorem 1 (fifteen planes).** For each $i \ge 0$, the number $j_i = 9 u_i - 6 u_{i+1} + u_{i+2}$ is an integer with $-5 \le j_i \le 9$. So each point $(u_i, u_{i+1}, u_{i+2})$ lies on one of the 15 planes $9x - 6y + z = j$, $j \in \{-5, \ldots, 9\}$.

*Proof.* By Lemma 2, $9 x_i - 6 x_{i+1} + x_{i+2}$ is a multiple of $m$, so $j_i = (9 x_i - 6 x_{i+1} + x_{i+2}) / m$ is an integer. Each state is odd (Lemma 3 below), so $0 < u_k < 1$ for each $k$. Then $j_i < 9 \cdot 1 - 0 + 1 = 10$ and $j_i > 0 - 6 + 0 = -6$. The integers in the open interval $(-6, 10)$ are $-5, \ldots, 9$, which are 15 values. $\square$

**Lemma 3.** If $a \equiv 3 \pmod 8$ or $a \equiv 5 \pmod 8$, then for each $k \ge 1$ there is an odd integer $t_k$ with $a^{2^k} = 1 + 2^{k+2} t_k$.

*Proof.* By induction on $k$. For $k = 1$, write $a = 8 j + s$ with $s \in \{3, 5\}$. Then $a^2 = 64 j^2 + 16 j s + s^2$, and $s^2 \in \{9, 25\}$, so $a^2 = 1 + 8 (8 j^2 + 2 j s + (s^2 - 1)/8)$. Here $(s^2 - 1)/8 \in \{1, 3\}$ is odd and $8j^2 + 2js$ is even, so $t_1$ is odd. For the step, assume $a^{2^k} = 1 + 2^{k+2} t_k$ with $t_k$ odd. Then $a^{2^{k+1}} = 1 + 2^{k+3} t_k + 2^{2k+4} t_k^2 = 1 + 2^{k+3} (t_k + 2^{k+1} t_k^2)$, and $t_{k+1} = t_k + 2^{k+1} t_k^2$ is odd because $k + 1 \ge 1$. $\square$

**Theorem 2 (period).** Each state $x_i$ is odd, and the period of $(x_i)$ is exactly $2^{29}$.

*Proof.* The product of odd numbers is odd, and reduction modulo the even number $m$ keeps the parity, so every $x_i$ is odd by induction. Odd numbers are invertible modulo $m$. As in any multiplicative generator, $x_i = a^i x_0 \bmod m$, and $x_{i+k} = x_i$ holds if and only if $a^k \equiv 1 \pmod m$. So the period is the order $d$ of $a$ modulo $m$.

The odd residues modulo $2^{31}$ form a group of order $2^{30}$, so $d$ divides $2^{30}$ and is a power of 2. Since $a = 65539 \equiv 3 \pmod 8$, Lemma 3 with $k = 29$ gives $a^{2^{29}} = 1 + 2^{31} t_{29} \equiv 1 \pmod{2^{31}}$, and with $k = 28$ gives $a^{2^{28}} = 1 + 2^{30} t_{28}$ with $t_{28}$ odd, which is not $\equiv 1 \pmod{2^{31}}$. So $d$ divides $2^{29}$ but not $2^{28}$, and $d = 2^{29}$. $\blacksquare$

**Remark.** The same argument shows that every multiplicative generator modulo $2^e$, $e \ge 3$, with $a \equiv 3$ or $5 \pmod 8$ and an odd seed, has period $2^{e-2}$, and that no multiplier gives more: for every odd $a$, $a^2 \equiv 1 \pmod 8$, and the induction step of Lemma 3, without the oddness of $t_k$, gives $a^{2^k} \equiv 1 \pmod{2^{k+2}}$, so the order of $a$ divides $2^{e-2}$.
