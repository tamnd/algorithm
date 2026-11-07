---
title: The ripple-carry adder computes the exact sum
proves: [correctness, termination]
status: full
---

Let $n \ge 0$, let $a_0, \ldots, a_{n-1}$ and $b_0, \ldots, b_{n-1}$ be bits, and let $c_0$ be a bit. Write $A = \sum_{j<n} a_j 2^j$ and $B = \sum_{j<n} b_j 2^j$.

**Theorem.** RIPPLE-ADD$(a, b, c_0)$ terminates and returns bits $s_0, \ldots, s_n$ with $\sum_{j=0}^{n} s_j 2^j = A + B + c_0$.

*Proof.* The loop of line L2 has $n$ rounds, so the procedure terminates; as a circuit, it is a finite acyclic network of $5n$ gates, since each carry $c_{i+1}$ depends only on inputs and on $c_i$.

*Lemma (full adder).* For bits $x, y, z$, let $p = x \oplus y$, $g = x \wedge y$, $s = p \oplus z$ and $c' = g \vee (p \wedge z)$. Then $x + y + z = s + 2c'$, and $s, c'$ are bits.

*Proof of the lemma.* There are eight cases; group them by $k = x + y$. If $k = 0$, then $p = g = 0$, $s = z$ and $c' = 0$, and $x + y + z = z = s$. If $k = 1$, then $p = 1$, $g = 0$, $s = 1 - z$ and $c' = z$, and $s + 2c' = 1 - z + 2z = 1 + z$. If $k = 2$, then $p = 0$, $g = 1$, $s = z$ and $c' = 1$, and $s + 2c' = z + 2$. In each case $s + 2c' = k + z$. $\square$

*Invariant.* Let $c_i$ be the value of $c$ before round $i$, so $c_0$ is set by line L1. We show by induction on $i$, for $0 \le i \le n$, that $c_i$ is a bit and

$$\sum_{j=0}^{i-1} s_j 2^j + c_i 2^i = \sum_{j=0}^{i-1} (a_j + b_j) 2^j + c_0 .$$

For $i = 0$ both sides are $c_0$. Assume it for $i < n$. Round $i$ computes, by lines L3 to L6, $s_i$ and $c_{i+1}$ as in the lemma with $x = a_i$, $y = b_i$, $z = c_i$, so $a_i + b_i + c_i = s_i + 2c_{i+1}$, and $c_{i+1}$ is a bit. Adding $(a_i + b_i) 2^i$ to both sides of the invariant for $i$ gives

$$\sum_{j=0}^{i-1} s_j 2^j + (a_i + b_i + c_i) 2^i = \sum_{j=0}^{i-1} s_j 2^j + s_i 2^i + c_{i+1} 2^{i+1} = \sum_{j=0}^{i} (a_j + b_j) 2^j + c_0 ,$$

which is the invariant for $i + 1$.

*Result.* For $i = n$ the invariant reads $\sum_{j<n} s_j 2^j + c_n 2^n = A + B + c_0$. Line L7 sets $s_n = c_n$, so $\sum_{j=0}^{n} s_j 2^j = A + B + c_0$. Since $A + B + c_0 \le 2(2^n - 1) + 1 < 2^{n+1}$, the $n + 1$ bits hold the sum, and each $s_j$ is a bit by the lemma.

*Radix $2^w$.* The same argument works for limbs in $[0, 2^w - 1]$ with $t = a_i + b_i + c_i \le 2^{w+1} - 1$, $s_i = t \bmod 2^w$ and $c_{i+1} = \lfloor t / 2^w \rfloor \in \{0, 1\}$, by division with remainder: $t = s_i + 2^w c_{i+1}$, and the invariant holds with $2^j$ replaced by $2^{wj}$.

*Two's complement overflow.* Let $n \ge 1$ and let $A'$, $B'$ be the signed values, so $A' = A - a_{n-1}2^n$ and likewise for $B'$. The exact signed sum (with $c_0 = 0$) is $A' + B' = \sum_{j<n-1} s_j 2^j + c_{n-1}2^{n-1} + (a_{n-1} + b_{n-1})2^{n-1} - (a_{n-1} + b_{n-1})2^n$, by the invariant for $i = n - 1$. With $a_{n-1} + b_{n-1} + c_{n-1} = s_{n-1} + 2c_n$ this equals $S' + (c_{n-1} - c_n) 2^n$, where $S' = \sum_{j<n-1} s_j 2^j - s_{n-1} 2^{n-1}$ is the signed value of the $n$-bit result, in $[-2^{n-1}, 2^{n-1} - 1]$. So the exact sum equals the stored result, and is in range, if and only if $c_{n-1} = c_n$: when $c_{n-1} \ne c_n$ the two differ by $\pm 2^n$, and the exact sum lies outside the range. $\blacksquare$
