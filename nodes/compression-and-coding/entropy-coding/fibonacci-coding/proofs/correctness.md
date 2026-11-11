---
title: The Fibonacci decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

The Fibonacci numbers are $F_1 = F_2 = 1$ and $F_i = F_{i-1} + F_{i-2}$, so $F_{i+1} = F_i + F_{i-1}$ and $F_{i-1} \ge 1$ for $i \ge 2$.

**Lemma 1 (the encoder).** For $x \ge 1$, FIB-ENCODE writes $d_2 d_3 \cdots d_k 1$ where $d_k = 1$, no two adjacent digits $d_i, d_{i+1}$ are both 1, and $\sum_{i=2}^{k} d_i F_i = x$.

*Proof.* Line L1 gives $F_k \le x < F_{k+1}$; such a $k \ge 2$ exists because $F_2 = 1 \le x$ and the $F_i$ grow without bound. Write $x_0$ for the input and $x$ for the running value. We show this invariant for the loop of lines L3 and L4:

> **(G)** Before index $i$ is tested, $x_0 = x + \sum_{j > i} d_j F_j$ and $0 \le x < F_{i+1}$.

Before $i = k$ no digit is set and $x = x_0 < F_{k+1}$. At index $i$: if $F_i \le x$, line L4 sets $d_i = 1$ and the new value is $x - F_i < F_{i+1} - F_i = F_{i-1} \le F_i$; otherwise $d_i = 0$ and $x < F_i$. In both cases the new value is less than $F_i$, which is the bound of (G) for index $i - 1$, and the sum identity still holds. After $i = 2$ the value is less than $F_2 = 1$, so it is 0, and $\sum_i d_i F_i = x_0$.

At $i = k$, $F_k \le x_0$, so $d_k = 1$. If $d_i = 1$ for some $i \ge 3$, the value after index $i$ is less than $F_{i-1}$, so the test at index $i - 1$ fails and $d_{i-1} = 0$. Line L5 writes the digits in the order $d_2, \ldots, d_k$ and then a 1. $\square$

So each codeword $c(x)$ has length $k \ge 2$, ends in $d_k 1 = 11$, and has no pair 11 at positions $(i, i+1)$ with $i + 1 \le k$, that is, no 11 that ends before its last bit.

**Lemma 2 (one codeword).** Let the reader $R$ stand at the start of $c(x)$, followed by any bits. Then FIB-DECODE$(R)$ returns $x$ and leaves $R$ just after the last bit of $c(x)$.

*Proof.* Line L6 sets prev = 0. In the loop, when the $t$-th bit of $c(x)$ is read, $i = t + 1$ and prev is the bit before it (0 for $t = 1$). For $t \le k - 1$, the bit read is $d_{t+1}$, and the pair (prev, $b$) is not 11, since the digits have no adjacent ones; so line L8 does not return, and line L9 adds $F_{t+1}$ exactly when $d_{t+1} = 1$. At $t = k$, the bit read is the final 1 and prev $= d_k = 1$, so line L8 returns. By then $x = \sum_{i=2}^{k} d_i F_i$, which is the input by Lemma 1, and the reader has read exactly $k$ bits. $\square$

**Lemma 3 (prefix-free).** If $x \ne y$, then $c(x)$ is not a prefix of $c(y)$.

*Proof.* The decoder's choices depend only on the bits read so far. If $c(x)$ were a prefix of $c(y)$, then on input $c(y)$ the decoder would stop after the bits of $c(x)$ and return $x$, by Lemma 2 applied to $c(x)$ followed by the rest of $c(y)$. By Lemma 2 applied to $c(y)$ it returns $y$ on the same run. So $x = y$, a contradiction. $\square$

**Theorem.** Let $s = c(x_1) \cdots c(x_n)$ be the output of FIB-ENCODE on $x_1, \ldots, x_n \ge 1$. A decoder that calls FIB-DECODE until the reader reaches the end of $s$ returns $x_1, \ldots, x_n$, and no other sequence of positive integers has the code $s$.

*Proof.* By induction with Lemma 2, call $i$ starts at the first bit of $c(x_i)$ and returns $x_i$, and after call $n$ the reader is at the end of $s$. If $y_1, \ldots, y_p$ also has the code $s$ and both lists are nonempty, then $c(x_1)$ and $c(y_1)$ are both prefixes of $s$, so one is a prefix of the other, and Lemma 3 gives $x_1 = y_1$. Remove this codeword and repeat; each codeword has at least two bits, so the process ends, with both lists empty at the same time. So $p = n$ and $y_i = x_i$. $\blacksquare$
