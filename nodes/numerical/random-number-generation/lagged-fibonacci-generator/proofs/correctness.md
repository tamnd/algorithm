---
title: The circular buffer computes the lagged Fibonacci recurrence, and the low bit is an LFSR sequence
proves: [correctness]
status: full
---

We use the pseudocode of the page, with lags $0 < j < k$, word size $w \ge 1$, an operation $\star \in \{+, -, \times, \oplus\}$ on $\{0, \ldots, 2^w - 1\}$ taken modulo $2^w$, and the sequence $x_n = (x_{n-k} \star x_{n-j}) \bmod 2^w$ for $n \ge k$ from initial values $x_0, \ldots, x_{k-1}$.

**Lemma 1 (buffer invariant).** Before the call of LFG-NEXT that produces $x_n$ ($n \ge k$), $B[(p + i) \bmod k] = x_{n-k+i}$ for every $0 \le i < k$, and $0 \le p < k$.

*Proof.* By induction on $n$. For $n = k$, line L6 sets $B[i] = x_i$ and $p = 0$. Assume the invariant before the call for $x_n$. Line L1 sets $q = (p + k - j) \bmod k$, which is position $i = k - j$, so $B[q] = x_{n-j}$; and $B[p]$ is position $i = 0$, so $B[p] = x_{n-k}$. Line L2 computes $x = (x_{n-k} \star x_{n-j}) \bmod 2^w = x_n$. Line L3 writes $x_n$ at position $p$. Line L4 sets $p' = (p + 1) \bmod k$. For $0 \le i < k - 1$, $B[(p' + i) \bmod k] = B[(p + i + 1) \bmod k]$ was not written, so it is $x_{n-k+i+1} = x_{(n+1)-k+i}$. For $i = k - 1$, $(p' + k - 1) \bmod k = p$, and $B[p] = x_n = x_{(n+1) - k + (k-1)}$. This is the invariant for $n + 1$. $\square$

**Theorem 1.** The $t$-th call of LFG-NEXT after LFG-SEED returns $x_{k+t-1}$.

*Proof.* Line L5 returns the value $x$ computed in line L2, which is $x_n$ by Lemma 1, and the calls produce $n = k, k+1, \ldots$ in order. $\square$

**Lemma 2 (reduction modulo 2).** For $\star \in \{+, -, \oplus\}$, the low bits $b_n = x_n \bmod 2$ satisfy $b_n = b_{n-k} \oplus b_{n-j}$.

*Proof.* Reduction modulo 2 is a ring homomorphism from $\mathbb{Z}/2^w\mathbb{Z}$ to $\mathbb{F}_2$, and $+$ and $-$ both become $\oplus$ in $\mathbb{F}_2$; for $\oplus$ the low bit of $a \oplus b$ is the $\oplus$ of the low bits. $\square$

**Theorem 2 (low bit and a lower bound on the period).** Let $\star \in \{+, -\}$, let $x^k + x^j + 1$ be primitive over $\mathbb{F}_2$, and let some $x_i$ with $i < k$ be odd. Then $(b_n)$ is purely periodic with period $2^k - 1$, the sequence $(x_n)$ is purely periodic, and its period is a multiple of $2^k - 1$.

*Proof.* By Lemma 2, $(b_n)$ satisfies the linear recurrence $b_n = b_{n-j} + b_{n-k}$ over $\mathbb{F}_2$, whose characteristic polynomial $x^k + x^{k-j} + 1$ is the reciprocal of $x^k + x^j + 1$ and therefore also primitive. The initial window $(b_0, \ldots, b_{k-1})$ is nonzero, so by the period theorem for LFSRs with primitive characteristic polynomial (see the [linear feedback shift register](/linear-feedback-shift-register/) page), $(b_n)$ is purely periodic with period $2^k - 1$.

The transition on windows is a bijection: from $(x_{n-k+1}, \ldots, x_n)$ one recovers $x_{n-k} = x_n - x_{n-j}$ for $\star = +$ and $x_{n-k} = x_n + x_{n-j}$ for $\star = -$ (modulo $2^w$). A bijection of a finite set has only pure cycles, so $(x_n)$ is purely periodic with some period $\rho$. Reducing modulo 2, $\rho$ is a period of $(b_n)$, so the least period $2^k - 1$ of $(b_n)$ divides $\rho$. $\square$

The exact value $\rho = (2^k - 1)\, 2^{w-1}$ is Brent's theorem (1994), cited on the page; the tests check it by exhaustive search for all primitive trinomials of degree at most 5, word sizes $w \le 3$ and every seed with an odd value.
