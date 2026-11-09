---
title: The focus pointer generator visits the reflected Gray code in order
proves: [correctness]
status: full
---

We write $g(k) = k \oplus \lfloor k/2 \rfloor$ and, for $k \ge 1$, $\rho(k)$ for the exponent of the largest power of 2 that divides $k$. The page of the [binary reflected Gray code](/binary-reflected-gray-code/) proves that $g(0), g(1), \ldots, g(2^n - 1)$ is the list $\Gamma_n$, that $g$ is one-to-one on $[0, 2^n)$, and that $g(k) \oplus g(k-1) = 2^{\rho(k)}$ for $k \ge 1$. We use these facts.

Fix $n \ge 0$. For $0 \le k < 2^n$ and $0 \le j \le n$, let $k_j$ be bit $j$ of $k$, with $k_j = 0$ for $j \ge n$, and let

$$t_j(k) = \max\{\, t \ge 0 : k_j = k_{j+1} = \cdots = k_{j+t-1} = 1 \,\},$$

the length of the run of ones of $k$ that starts at bit $j$. Since $k < 2^n$, $t_j(k) \le n - j$, and $t_n(k) = 0$. The number of trailing ones of $k$ is $t_0(k)$, and $t_0(k) = \rho(k + 1)$, because $k + 1$ has exactly $t_0(k)$ trailing zeros.

**Invariant $I(k)$.** At the $k$-th arrival at line L4, counting from $k = 0$:

1. $a = g(k)$, where $a$ is read as $\sum_j a_j 2^j$;
2. for each $0 \le j \le n$, $f_j = j + t_j(k)$ if $j = 0$ or $k_{j-1} = 0$, and $f_j = j$ if $j \ge 1$ and $k_{j-1} = 1$.

We call the first case of item 2 the *head* case: no 1 of $k$ sits just below bit $j$, so a run of ones that starts at bit $j$, if any, is a whole run.

**Lemma 1 (base).** $I(0)$ holds.

*Proof.* Lines L1 and L2 set $a = 0 = g(0)$ and $f_j = j$ for $0 \le j \le n$. All bits of $0$ are 0, so every $j$ is in the head case with $t_j(0) = 0$, and the rule asks for $f_j = j$. $\square$

**Lemma 2 (step).** Let $0 \le k < 2^n - 1$ and assume $I(k)$. Then the pass through lines L5 to L8 does not return, and the next arrival at line L4 satisfies $I(k+1)$.

*Proof.* Let $t = t_0(k)$. By item 2 in the head case $j = 0$, line L5 reads $j = f_0 = t$. Since $k < 2^n - 1$, not all of bits $0, \ldots, n-1$ of $k$ are 1, so $t < n$ and line L6 does not return. The binary forms of $k$ and $k + 1$ agree in bits $t + 1$ and higher. Bits $0$ to $t - 1$ are 1 in $k$ and 0 in $k + 1$. Bit $t$ is 0 in $k$ and 1 in $k + 1$.

*Item 1.* Line L8 flips bit $t$ of $a$, so the new $a$ is $g(k) \oplus 2^t = g(k) \oplus 2^{\rho(k+1)} = g(k+1)$.

*Item 2.* Lines L5 and L7 write $f_0 \leftarrow 0$, then $f_t \leftarrow f_{t+1}$ and $f_{t+1} \leftarrow t + 1$, in this order, and no other pointer changes. When $t = 0$, the write $f_t \leftarrow f_{t+1}$ replaces the 0 that line L5 put in $f_0$. Here $f_{t+1}$ on the right side is its old value. We check each $j$ against the rule for $k + 1$.

- *$j = t$.* This is the head case for $k + 1$: either $t = 0$, or $t \ge 1$ and bit $t - 1$ of $k + 1$ is 0. Bit $t$ of $k + 1$ is 1 and the bits above agree with $k$, so $t_t(k+1) = 1 + t_{t+1}(k)$. The new $f_t$ is the old $f_{t+1}$. In $k$ bit $t$ is 0, so $j = t + 1$ was in the head case for $k$, and the old $f_{t+1}$ is $t + 1 + t_{t+1}(k)$. So the new $f_t = t + t_t(k+1)$, as required.
- *$1 \le j \le t - 1$, when $t \ge 2$.* Bit $j - 1$ of $k$ is 1, so the old $f_j = j$, and it does not change. In $k + 1$, bit $j - 1$ is 0, so $j$ is in the head case, and bit $j$ is 0, so $t_j(k+1) = 0$. The rule asks for $f_j = j$.
- *$j = 0$, when $t \ge 1$.* The new $f_0 = 0$ from line L5. Bit 0 of $k + 1$ is 0, so $t_0(k+1) = 0$, and the rule asks for $f_0 = 0$.
- *$j = t + 1$.* Line L7 sets $f_{t+1} = t + 1$. Bit $t$ of $k + 1$ is 1, so this is not the head case, and the rule asks for $f_{t+1} = t + 1$. This also covers $t + 1 = n$, where the rule gives $f_n = n$ in both cases.
- *$t + 2 \le j \le n$.* $f_j$ does not change. Bit $j - 1 \ge t + 1$ is the same in $k$ and $k + 1$, so $j$ is in the same case for both, and $t_j$ depends only on bits $j$ and higher, which also agree. So the rule gives the same value for $k + 1$ as for $k$.

So $I(k+1)$ holds. $\square$

**Lemma 3 (stop).** If $I(2^n - 1)$ holds, then the pass returns at line L6.

*Proof.* All bits $0$ to $n - 1$ of $2^n - 1$ are 1, so $t_0(2^n - 1) = n$ and line L5 reads $j = f_0 = n$. $\square$

**Theorem.** LOOPLESS-GRAY$(n)$ visits exactly $2^n$ strings, and the $k$-th visit, counting from 0, shows $g(k)$. So it visits $\Gamma_n$ in order, each string of $\{0,1\}^n$ once, and each pass after line L2 runs a bounded number of operations.

*Proof.* By Lemma 1 and induction with Lemma 2, $I(k)$ holds at the $k$-th arrival at line L4 for each $0 \le k \le 2^n - 1$, and no pass returns before the arrival with $k = 2^n - 1$. By Lemma 3 that pass returns. So there are exactly $2^n$ visits, and by item 1 of the invariant the $k$-th shows $g(k)$. Since $g$ is one-to-one on $[0, 2^n)$, each string appears once, and $g(0), \ldots, g(2^n - 1)$ is $\Gamma_n$. Lines L4 to L8 contain no loop, so each pass does a bounded number of steps. For $n = 0$, Lemma 3 applies at $k = 0$: the single empty string is visited once. $\blacksquare$
