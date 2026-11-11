---
title: The delta decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

We write $\gamma(m)$ for the gamma codeword of $m \ge 1$ and $\delta(x)$ for the delta codeword of $x \ge 1$. We use two facts about the gamma code, proved on the [Elias gamma coding](/elias-gamma-coding/) page: GAMMA-DECODE, started at the first bit of $\gamma(m)$, returns $m$ and stops after the last bit of $\gamma(m)$; and the set of gamma codewords is prefix-free.

Let $N = \lfloor \log_2 x \rfloor$, and let $1 b_{N-1} \cdots b_0$ be the binary digits of $x$. Lines L1 to L3 give

$$\delta(x) = \gamma(N + 1)\, b_{N-1} \cdots b_0, \qquad |\delta(x)| = |\gamma(N+1)| + N.$$

Line L2 is valid because $N + 1 \ge 1$.

**Lemma 1 (one codeword).** Let the bit reader $R$ stand at the start of $\delta(x)$, followed by any bits. Then DELTA-DECODE$(R)$ returns $x$ and leaves $R$ just after the last bit of $\delta(x)$.

*Proof.* By the gamma fact, line L4 reads exactly $\gamma(N+1)$ and sets $N$ to the right value. Lines L5 and L6 keep this invariant:

> **(D)** After $j$ rounds of line L6, with $0 \le j \le N$, the reader has read $\gamma(N+1)\, b_{N-1} \cdots b_{N-j}$, and $x$ is the value of the binary string $1 b_{N-1} \cdots b_{N-j}$.

For $j = 0$, line L5 sets $x = 1$. A round reads the next bit $b_{N-j-1}$ and sets $x \leftarrow 2x + b_{N-j-1}$, which appends that digit, so (D) holds for $j + 1$. After $N$ rounds, $x$ is the value of $1 b_{N-1} \cdots b_0$, the coded integer, and the reader has read all of $\delta(x)$. Line L7 returns $x$. $\square$

**Lemma 2 (prefix-free).** If $x \ne y$, then $\delta(x)$ is not a prefix of $\delta(y)$.

*Proof.* Suppose that $\delta(x)$ is a prefix of $\delta(y)$. Let $N_x$ and $N_y$ be the values of $N$ for $x$ and $y$. Then $\gamma(N_x + 1)$ and $\gamma(N_y + 1)$ are both prefixes of $\delta(y)$, so one is a prefix of the other. The gamma code is prefix-free, so $N_x = N_y$. Then $|\delta(x)| = |\delta(y)|$, so $\delta(x) = \delta(y)$, and by Lemma 1 the decoder returns $x$ and $y$ on the same input, so $x = y$. This is a contradiction. $\square$

**Theorem.** Let $s = \delta(x_1) \cdots \delta(x_n)$ be the output of DELTA-ENCODE on $x_1, \ldots, x_n \ge 1$. A decoder that calls DELTA-DECODE until the reader is at the end of $s$ returns $x_1, \ldots, x_n$, and no other sequence of positive integers has the code $s$.

*Proof.* Before call $i$, the reader stands at the start of $\delta(x_i)$: this holds for $i = 1$, and Lemma 1 carries it from $i$ to $i + 1$ and shows that call $i$ returns $x_i$. After call $n$ the reader is at the end of $s$, so the decoder stops.

If $y_1, \ldots, y_p$ also has the code $s$ and both lists are nonempty, then $\delta(x_1)$ and $\delta(y_1)$ are both prefixes of $s$, so one is a prefix of the other, and Lemma 2 gives $x_1 = y_1$. Remove this codeword from the front of $s$ and repeat. Each codeword has at least one bit, so the process ends, and both lists end together because the empty string is not a nonempty concatenation of codewords. So $p = n$ and $y_i = x_i$ for each $i$. $\blacksquare$
