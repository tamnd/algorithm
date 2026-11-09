---
title: BRGC builds the reflected Gray code, and the code is a Gray cycle
proves: [correctness]
status: full
---

We write $g(k) = k \oplus \lfloor k/2 \rfloor$ for an integer $k \ge 0$. For $k \ge 1$, $\rho(k)$ is the exponent of the largest power of 2 that divides $k$. A string $a_{m-1} \ldots a_0$ is the integer $\sum_j a_j 2^j$.

**Lemma 1 (linearity).** For all $x, y \ge 0$, $g(x \oplus y) = g(x) \oplus g(y)$.

*Proof.* A right shift acts on each bit position on its own, so $\lfloor (x \oplus y)/2 \rfloor = \lfloor x/2 \rfloor \oplus \lfloor y/2 \rfloor$. Then $g(x \oplus y) = x \oplus y \oplus \lfloor x/2 \rfloor \oplus \lfloor y/2 \rfloor = g(x) \oplus g(y)$, because $\oplus$ is associative and commutative. $\square$

**Lemma 2.** For $m \ge 1$, $g(2^m - 1) = 2^{m-1}$.

*Proof.* $2^m - 1$ has ones in bits $0$ to $m-1$ and $\lfloor (2^m - 1)/2 \rfloor = 2^{m-1} - 1$ has ones in bits $0$ to $m-2$. Their exclusive or has a single one, in bit $m-1$. $\square$

**Lemma 3 (the loop).** For each $i$ with $0 \le i \le n$, when the test of line L2 is made with this value of $i$ (or the loop ends, for $i = n$), the list $G$ has $2^i$ entries, $G = \Gamma_i$, and $G[k] = g(k)$ for $0 \le k < 2^i$.

*Proof.* By [induction](/induction/) on $i$. For $i = 0$, line L1 sets $G = [0]$. This is $\Gamma_0$, which holds the empty string, whose integer is 0, and $g(0) = 0$.

Assume the claim for $i < n$. Line L3 fixes the bound $|G| - 1 = 2^i - 1$ before the loop starts, so the loop runs for $j = 2^i - 1, 2^i - 2, \ldots, 0$, and it reads only the entries $G[0 \ldots 2^i - 1]$, which line L4 does not change. Line L4 appends $G[j] + 2^i$ in this order. So after the loop, $G$ has $2^{i+1}$ entries: $G[k]$ is unchanged for $k < 2^i$, and for $0 \le j < 2^i$ the entry at position $p = 2^i + (2^i - 1 - j) = 2^{i+1} - 1 - j$ is $G_{\text{old}}[j] + 2^i$.

*The list is $\Gamma_{i+1}$.* Each entry of $\Gamma_i$ is less than $2^i$, so adding 0 leaves an $(i+1)$-bit string whose first bit is 0, and adding $2^i$ sets the first bit to 1 and keeps the other $i$ bits. The first $2^i$ entries are therefore $0\Gamma_i$, and the next $2^i$ entries are $1$ followed by $G_{\text{old}}[2^i - 1], \ldots, G_{\text{old}}[0]$, that is $1\Gamma_i^R$. This is the definition of $\Gamma_{i+1}$.

*The formula.* For $k < 2^i$, $G[k] = g(k)$ by the hypothesis. For $p = 2^{i+1} - 1 - j$ with $0 \le j < 2^i$: since $j < 2^{i+1}$, subtracting $j$ from $2^{i+1} - 1$ clears exactly the one bits of $j$, so $p = j \oplus (2^{i+1} - 1)$. By Lemma 1 and Lemma 2, $g(p) = g(j) \oplus 2^i$. Since $g(j)$ and $j$ have the same highest one bit, $g(j) < 2^i$, so $g(j) \oplus 2^i = g(j) + 2^i = G_{\text{old}}[j] + 2^i = G[p]$. $\square$

**Theorem.** For each $n \ge 0$, BRGC$(n)$ returns $\Gamma_n$, and $\Gamma_n[k] = g(k)$ for $0 \le k < 2^n$. The list contains each $n$-bit string exactly once. For $1 \le k < 2^n$, $\Gamma_n[k]$ and $\Gamma_n[k-1]$ differ exactly in bit $\rho(k)$. For $n \ge 1$, $\Gamma_n[2^n - 1]$ and $\Gamma_n[0]$ differ exactly in bit $n - 1$.

*Proof.* The loop of line L2 runs for $i = 0, \ldots, n-1$, so Lemma 3 with $i = n$ gives the first two statements, and line L5 returns $G$.

*Each string once.* Each $g(k)$ with $k < 2^n$ is less than $2^n$, as in the proof of Lemma 3. Suppose $g(x) = g(y)$ with $x, y < 2^n$, and let $z = x \oplus y$. By Lemma 1, $g(z) = 0$, so $z = \lfloor z/2 \rfloor$. If $z \ge 1$ then $\lfloor z/2 \rfloor < z$, which is false, so $z = 0$ and $x = y$. Thus $g$ maps the $2^n$ values $0, \ldots, 2^n - 1$ one to one into a set of $2^n$ values, and each $n$-bit string appears exactly once.

*One bit per step.* Let $1 \le k < 2^n$ and $r = \rho(k)$. Then $k = q \cdot 2^{r+1} + 2^r$ for some $q \ge 0$, and $k - 1 = q \cdot 2^{r+1} + (2^r - 1)$. These two numbers agree above bit $r$ and differ in bits $0$ to $r$, so $k \oplus (k - 1) = 2^{r+1} - 1$. By Lemma 1 and Lemma 2, $g(k) \oplus g(k-1) = g(2^{r+1} - 1) = 2^r$.

*Cyclic.* For $n \ge 1$, Lemma 2 gives $g(2^n - 1) = 2^{n-1}$, and $g(0) = 0$. Their exclusive or is $2^{n-1}$. $\blacksquare$
