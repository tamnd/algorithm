---
title: The gamma decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

We write $\gamma(x)$ for the codeword that GAMMA-ENCODE writes for $x \ge 1$. Let $N = \lfloor \log_2 x \rfloor$, and let $b_N b_{N-1} \cdots b_0$ be the binary digits of $x$, with $b_N = 1$ and $x = \sum_{i=0}^{N} b_i 2^i$. Lines L2 and L3 give

$$\gamma(x) = 0^N \, b_N b_{N-1} \cdots b_0 = 0^N \, 1 \, b_{N-1} \cdots b_0.$$

**Lemma 1 (one codeword).** Let the bit reader $R$ stand at the start of $\gamma(x)$, followed by any bits. Then GAMMA-DECODE$(R)$ returns $x$ and leaves $R$ just after the last bit of $\gamma(x)$.

*Proof.* The first $N$ bits of $\gamma(x)$ are zeros and bit $N + 1$ is $b_N = 1$. So the loop of line L5 runs its body $N$ times, reads the $N + 1$ bits $0^N 1$, and stops with $N$ at the right value. Lines L6 and L7 use this invariant:

> **(D)** After $j$ rounds of line L7, with $0 \le j \le N$, the reader has read $0^N 1 b_{N-1} \cdots b_{N-j}$ and $x = \sum_{i=0}^{j} b_{N-i} 2^{j-i}$, the value of the top $j + 1$ digits.

For $j = 0$, line L6 sets $x = 1 = b_N$, and the reader stands after $0^N 1$. If (D) holds for $j < N$, the next round reads $b_{N-j-1}$ and sets $x \leftarrow 2x + b_{N-j-1} = \sum_{i=0}^{j+1} b_{N-i} 2^{j+1-i}$, so (D) holds for $j + 1$. After $N$ rounds, $x = \sum_{i=0}^{N} b_{N-i} 2^{N-i}$, the original value, and the reader has read exactly the $2N + 1$ bits of $\gamma(x)$. Line L8 returns $x$. $\square$

**Lemma 2 (prefix-free).** If $x \ne y$, then $\gamma(x)$ is not a prefix of $\gamma(y)$.

*Proof.* Suppose that $\gamma(x)$ is a prefix of $\gamma(y)$. Let $N_x = \lfloor \log_2 x \rfloor$ and $N_y = \lfloor \log_2 y \rfloor$. The first one bit of $\gamma(x)$ is at position $N_x + 1$, and the first one bit of $\gamma(y)$ is at position $N_y + 1$. Since $\gamma(x)$ is a prefix of $\gamma(y)$ and contains a one, the first one bits are at the same position, so $N_x = N_y$. Then both codewords have the length $2N_x + 1$, so the prefix is the whole word and $\gamma(x) = \gamma(y)$. By Lemma 1 the decoder returns $x$ on $\gamma(x)$ and $y$ on $\gamma(y)$, so $x = y$, which contradicts $x \ne y$. $\square$

**Theorem.** Let $x_1, \ldots, x_n \ge 1$ and let $s = \gamma(x_1)\gamma(x_2)\cdots\gamma(x_n)$ be the output of GAMMA-ENCODE called on each $x_i$ in turn. A decoder that calls GAMMA-DECODE until the reader is at the end of $s$ returns $x_1, \ldots, x_n$. No other sequence of positive integers has the code $s$.

*Proof.* By induction on $i$: before call $i$, the reader stands at the start of $\gamma(x_i)$. This is true for $i = 1$. If it is true for $i$, Lemma 1 shows that call $i$ returns $x_i$ and leaves the reader at the start of $\gamma(x_{i+1})$, or at the end of $s$ after call $n$. So the decoder returns exactly $x_1, \ldots, x_n$ and then stops.

For the uniqueness, let $y_1, \ldots, y_p$ also have the code $s$. If $p \ge 1$ and $n \ge 1$, both $\gamma(x_1)$ and $\gamma(y_1)$ are prefixes of $s$, so one of them is a prefix of the other. By Lemma 2, $x_1 = y_1$. Remove this codeword from the front of $s$ and repeat. Each codeword has at least one bit, so the process ends, and it ends with both lists empty at the same time, since an empty string cannot be a nonempty concatenation of codewords. So $p = n$ and $y_i = x_i$ for each $i$. $\blacksquare$
