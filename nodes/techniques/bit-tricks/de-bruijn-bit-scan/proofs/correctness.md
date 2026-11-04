---
title: The de Bruijn bit scan returns the index of the lowest 1-bit
proves: [correctness]
status: full
---

Fix $n \ge 1$ and the word size $w = 2^n$. Words are integers in $[0, 2^w)$, bit $t$ of a word $a$ is $\lfloor a / 2^t \rfloor \bmod 2$, and $-a$ means $(2^w - a) \bmod 2^w$. For $x \ne 0$ let $\rho(x)$ be the least $t$ with bit $t$ of $x$ equal to 1.

**Lemma 1 (isolation).** For $0 < x < 2^w$ with $k = \rho(x)$, $x \wedge (-x) = 2^k$.

*Proof.* Write $x = h \cdot 2^{k+1} + 2^k$ with $0 \le h < 2^{w-k-1}$; this is possible because bits $0$ to $k-1$ of $x$ are 0 and bit $k$ is 1. Then $\overline{x} = (2^w - 1) - x$ has bits $0$ to $k - 1$ equal to 1, bit $k$ equal to 0, and bits above $k$ equal to the complements of those of $x$. Adding 1 to $\overline{x}$ turns its $k$ low 1-bits into 0-bits with a carry into bit $k$, which becomes 1, and the carry stops there. So $-x = \overline{x} + 1 \bmod 2^w$ has bits $0$ to $k - 1$ equal to 0, bit $k$ equal to 1, and each bit above $k$ the complement of the same bit of $x$. In $x \wedge (-x)$ the bits below $k$ are 0, bit $k$ is 1, and each bit above $k$ is $a \wedge \overline{a} = 0$. So $x \wedge (-x) = 2^k$. $\square$

**Windows.** For a word $D$ and $0 \le k < w$, let $\mathrm{win}_k(D) = ((2^k D) \bmod 2^w) \gg (w - n)$, an integer in $[0, 2^n)$. Write $d_0 d_1 \dots d_{w-1}$ for the bits of $D$ read from the top, so $d_j$ is bit $w - 1 - j$ of $D$. Extend the indices cyclically: $d_j = d_{j \bmod w}$.

**Lemma 2 (window).** For $0 \le k < w$, the $n$ bits of $\mathrm{win}_k(D)$, from the top, are $c_k, c_{k+1}, \dots, c_{k+n-1}$, where $c_j = d_j$ for $j < w$ and $c_j = 0$ for $j \ge w$.

*Proof.* Multiplying by $2^k$ moves bit $t$ of $D$ to bit $t + k$, and the reduction modulo $2^w$ deletes the bits that reach position $w$ or more; positions $0$ to $k - 1$ become 0. The shift by $w - n$ keeps positions $w - 1$ down to $w - n$ of the product, as the top $n$ bits of the result in the same order. Position $w - 1 - m$ of the product, for $0 \le m < n$, holds bit $w - 1 - m - k$ of $D$ if $w - 1 - m - k \ge 0$, which is $d_{k+m}$, and holds 0 otherwise, that is when $k + m \ge w$. So the bit at place $m$ from the top of $\mathrm{win}_k(D)$ is $c_{k+m}$. $\square$

**Lemma 3 (distinct windows).** Let the cyclic sequence $d_0 \dots d_{w-1}$ be a binary de Bruijn sequence of order $n$, that is, the $w$ cyclic windows $(d_k, d_{k+1}, \dots, d_{k+n-1})$ for $0 \le k < w$ are the $2^n$ binary words of length $n$, each once. Suppose also $d_0 = d_1 = \dots = d_{n-1} = 0$. Then $\mathrm{win}_0(D), \dots, \mathrm{win}_{w-1}(D)$ are pairwise distinct.

*Proof.* By Lemma 2, $\mathrm{win}_k(D)$ has bits $c_k, \dots, c_{k+n-1}$. For an index $j = k + m$ with $k < w$ and $m < n$, if $j < w$ then $c_j = d_j$, and if $j \ge w$ then $j - w < n$, so $d_j = d_{j - w} = 0 = c_j$ by the hypothesis on the top $n$ bits. Hence $c_j = d_j$ for every index used, and $\mathrm{win}_k(D)$ is the $k$-th cyclic window of the de Bruijn sequence. These $w$ windows are pairwise distinct by definition. $\square$

The hypothesis can always be met: a de Bruijn sequence contains the window $0^n$ once, and its rotation that starts there has $n$ leading zeros and is again a de Bruijn sequence.

**Table.** Under the condition of Lemma 3 the map $k \mapsto \mathrm{win}_k(D)$ is injective from $\{0, \dots, w - 1\}$ into $\{0, \dots, 2^n - 1\}$, a set with $2^n = w$ elements, so it is a bijection. The table filled by $T[\mathrm{win}_k(D)] \gets k$ for $k = 0, \dots, w - 1$ therefore writes each entry exactly once and satisfies $T[\mathrm{win}_k(D)] = k$ for every $k$.

**Theorem.** Let $D$ and $T$ be as above and $0 < x < 2^w$. Then DE-BRUIJN-SCAN$(x)$ returns $\rho(x)$.

*Proof.* Let $k = \rho(x)$. By Lemma 1, line L1 sets $b = 2^k$. Line L2 sets $p = (2^k D) \bmod 2^w$, and line L3 sets $i = p \gg (w - n) = \mathrm{win}_k(D)$. Line L4 returns $T[\mathrm{win}_k(D)] = k$ by the property of the table. $\square$

**Remark (zero).** For $x = 0$, $x \wedge (-x) = 0$, so $i = 0$ and the procedure returns $T[0] = T[\mathrm{win}_0(D)] = 0$, which is $\rho(1)$. The precondition $x \ne 0$ is needed.

**Termination.** The procedure has four lines and no loop, and the table is built by a loop of $w$ iterations, so both stop. $\blacksquare$
