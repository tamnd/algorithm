---
title: The VByte decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

For $x \ge 0$ let $m = \max(1, \lceil (\lfloor \log x \rfloor + 1)/7 \rceil)$ for $x \ge 1$ and $m = 1$ for $x = 0$, and write $x$ in base 128 as

$$x = \sum_{i=0}^{m-1} g_i\, 128^{i}, \qquad 0 \le g_i < 128,$$

with $g_{m-1} \ne 0$ when $x \ge 1$. This form is unique.

**Lemma 1 (the encoder).** VBYTE-ENCODE$(x)$ appends the $m$ bytes $c(x) = b_0 b_1 \cdots b_{m-1}$ with $b_i = g_i + 128$ for $i < m - 1$ and $b_{m-1} = g_{m-1}$.

*Proof.* Let $x_i$ be the value of $x$ at the start of round $i$ of lines L1 to L5, so $x_0 = x$. Line L2 sets $b = x_i \bmod 128$ and $x_{i+1} = \lfloor x_i / 128 \rfloor$. By induction $x_i = \sum_{j \ge i} g_j 128^{j-i}$, so $x_i \bmod 128 = g_i$, and $x_{i+1} \ne 0$ exactly when some $g_j$ with $j > i$ is nonzero, that is when $i < m - 1$. So line L3 adds 128 exactly for $i < m - 1$, and line L5 ends the loop after round $m - 1$, when $x_m = 0$. For $x = 0$ the loop runs once and writes $b_0 = 0$. $\square$

**Lemma 2 (one codeword).** If the input of VBYTE-DECODE starts with $c(x)$, followed by any bytes, it returns $x$ and has read exactly the $m$ bytes of $c(x)$.

*Proof.* The loop of lines L7 to L10 keeps the invariant that after $i$ rounds, $s = 7i$ and $x = \sum_{j < i} g_j 128^j$. It holds for $i = 0$ by line L6. In round $i + 1$ the byte read is $b_i$, and $b_i \bmod 128 = g_i$, so line L9 adds $g_i 2^{7i} = g_i 128^i$ and adds 7 to $s$. For $i < m - 1$, $b_i \ge 128$ and the loop goes on; $b_{m-1} = g_{m-1} < 128$, so the loop stops after round $m$ with $x = \sum_{j < m} g_j 128^j$. $\square$

**Lemma 3 (prefix-free).** If $x \ne y$, then $c(x)$ is not a prefix of $c(y)$.

*Proof.* In $c(y)$, every byte before the last is at least 128. If $c(x)$ were a proper prefix of $c(y)$, the last byte of $c(x)$, which is below 128, would be a byte of $c(y)$ before its last, a contradiction. If $c(x) = c(y)$, then Lemma 2 gives $x = y$. $\square$

**Theorem.** Let $s = c(x_1) \cdots c(x_n)$. A decoder that calls VBYTE-DECODE until the input is used up returns $x_1, \ldots, x_n$, and no other sequence of integers has the code $s$.

*Proof.* By induction with Lemma 2, call $i$ starts at the first byte of $c(x_i)$ and returns $x_i$, and after call $n$ the input is used up. If another sequence $y_1, \ldots, y_p$ has the code $s$, the canonical encoder of Lemma 1 gives one of $c(x_1)$ and $c(y_1)$ as a prefix of the other, so $x_1 = y_1$ by Lemma 3. Remove this codeword and repeat; each codeword has at least one byte, so $p = n$ and $y_i = x_i$. $\blacksquare$
