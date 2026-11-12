---
title: Prefix sums invert the differences, also modulo a power of two
proves: [correctness, termination]
status: full
---

We use the notation of the page. $X = X[0 \ldots n-1]$ is a sequence of integers, $D = \mathrm{DELTA\text{-}ENCODE}(X)$, and we write $X[-1] = 0$.

**Lemma 1 (the encoder).** $D[i] = X[i] - X[i-1]$ for $0 \le i < n$.

*Proof.* Invariant: at the start of the step of line L2 with index $i$, $prev = X[i-1]$. It holds for $i = 0$ by line L1, since $X[-1] = 0$. In the step, line L3 sets $D[i] = X[i] - prev = X[i] - X[i-1]$, and line L4 sets $prev = X[i]$, which is the invariant for $i + 1$. The loop has $n$ steps and ends. $\square$

**Theorem 1 (the decoder inverts the encoder).** $\mathrm{DELTA\text{-}DECODE}(D) = X$.

*Proof.* Invariant: at the start of the step with index $i$, $total = X[i-1]$. It holds for $i = 0$ by line D1. In the step, line D3 sets $total = X[i-1] + D[i] = X[i-1] + X[i] - X[i-1] = X[i]$ by Lemma 1, and line D4 writes it. The loop has $n$ steps and ends. $\blacksquare$

**Theorem 2 (the encoder inverts the decoder).** For each integer sequence $D$, $\mathrm{DELTA\text{-}ENCODE}(\mathrm{DELTA\text{-}DECODE}(D)) = D$. So the two maps are inverse bijections of $\mathbb{Z}^n$.

*Proof.* Let $X = \mathrm{DELTA\text{-}DECODE}(D)$, so $X[i] = D[0] + \cdots + D[i]$ and $X[-1] = 0$ is the empty sum. By Lemma 1 the encoder outputs $X[i] - X[i-1] = D[i]$. $\blacksquare$

**Theorem 3 (modular differences).** Let all values be in $\{0, \ldots, 2^b - 1\}$, and let both sides compute modulo $m = 2^b$: $D[i] = (X[i] - X[i-1]) \bmod m$ and $total = (total + D[i]) \bmod m$. Then the decoder still returns $X$.

*Proof.* The invariant becomes $total \equiv X[i-1] \pmod m$ with $0 \le total < m$. Line D3 gives $total \equiv X[i-1] + X[i] - X[i-1] = X[i] \pmod m$, and $0 \le X[i] < m$, so $total = X[i]$ exactly. $\blacksquare$

**Theorem 4 (order $k$).** Applying the encoder $k$ times and the decoder $k$ times gives back $X$; and if $X[i] = p(i)$ for a polynomial $p$ of degree at most $k - 1$, the encoder applied $k$ times gives $0$ at each index $i \ge k$.

*Proof.* The first claim follows from Theorem 1 by induction on $k$. For the second, for $i \ge 1$ one application turns $p(i)$ into $p(i) - p(i - 1)$, a polynomial in $i$ of degree one less (the leading terms cancel), and a polynomial of degree 0 becomes 0. After $j$ applications, the value at index $i$ is $\Delta^j p(i)$ whenever $i \ge j$, because the first $j$ indices are the only ones that use the start value $X[-1] = 0$ in some round. So for $i \ge k$ the value is $\Delta^k p(i) = 0$. $\blacksquare$
