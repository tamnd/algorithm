---
title: Fast doubling returns the pair of Fibonacci numbers F(n) and F(n + 1)
proves: [correctness, termination]
status: full
---

Let $F_0 = 0$, $F_1 = 1$ and $F_m = F_{m-1} + F_{m-2}$ for $m \ge 2$. Extend the sequence one step back by $F_{-1} = 1$, so that $F_1 = F_0 + F_{-1}$ also holds. Let $Q = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$.

**Lemma 1 (matrix form).** For each $k \ge 0$, $Q^k = \begin{pmatrix} F_{k+1} & F_k \\ F_k & F_{k-1} \end{pmatrix}$.

*Proof.* By induction on $k$. For $k = 0$, $Q^0 = I = \begin{pmatrix} F_1 & F_0 \\ F_0 & F_{-1} \end{pmatrix}$. If the claim holds for $k$, then

$$Q^{k+1} = Q^k Q = \begin{pmatrix} F_{k+1} + F_k & F_{k+1} \\ F_k + F_{k-1} & F_k \end{pmatrix} = \begin{pmatrix} F_{k+2} & F_{k+1} \\ F_{k+1} & F_k \end{pmatrix}$$

by the recurrence, valid for the indices $k + 2 \ge 2$ and $k + 1 \ge 1$. $\square$

**Lemma 2 (doubling).** For each $k \ge 0$,

$$F_{2k} = F_k (2F_{k+1} - F_k), \qquad F_{2k+1} = F_k^2 + F_{k+1}^2 .$$

*Proof.* By Lemma 1, $Q^{2k} = (Q^k)^2$. The top right entry of $(Q^k)^2$ is $F_{k+1}F_k + F_k F_{k-1} = F_k (F_{k+1} + F_{k-1})$, and the top left entry is $F_{k+1}^2 + F_k^2$. The top right and top left entries of $Q^{2k}$ are $F_{2k}$ and $F_{2k+1}$. Finally $F_{k-1} = F_{k+1} - F_k$ by the recurrence (for $k = 0$ by the definition of $F_{-1}$), so $F_{k+1} + F_{k-1} = 2F_{k+1} - F_k$. $\square$

**Invariant.** Let $t_{L-1} t_{L-2} \cdots t_0$ be the binary digits of $n$ read by line L2, most significant first. After $j$ passes, let $k_j = \sum_{i=0}^{j-1} t_{L-1-i}\, 2^{j-1-i}$ be the number formed by the first $j$ digits, so $k_0 = 0$, $k_{j+1} = 2k_j + t_{L-1-j}$ and $k_L = n$. The invariant is

$$(a, b) = (F_{k_j}, F_{k_j + 1}) .$$

*Initialization.* Line L1 sets $(a, b) = (0, 1) = (F_0, F_1)$, and $k_0 = 0$.

*Maintenance.* Assume $(a, b) = (F_k, F_{k+1})$ with $k = k_j$, and let $t$ be the next digit. By Lemma 2, line L3 sets $c = F_k(2F_{k+1} - F_k) = F_{2k}$ and line L4 sets $d = F_k^2 + F_{k+1}^2 = F_{2k+1}$. If $t = 0$, then $k_{j+1} = 2k$, and line L5 sets $(a, b) = (F_{2k}, F_{2k+1})$. If $t = 1$, then $k_{j+1} = 2k + 1$, and line L6 sets $(a, b) = (F_{2k+1}, F_{2k} + F_{2k+1}) = (F_{2k+1}, F_{2k+2})$ by the recurrence. In both cases $(a, b) = (F_{k_{j+1}}, F_{k_{j+1}+1})$.

*Termination.* The loop runs once for each of the $L$ binary digits of $n$.

**Theorem.** FAST-DOUBLING$(n)$ returns $(F_n, F_{n+1})$ for each $n \ge 0$.

*Proof.* After the $L$ passes, the invariant gives $(a, b) = (F_{k_L}, F_{k_L + 1}) = (F_n, F_{n+1})$. For $n = 0$ the single digit 0 gives $c = 0$, $d = 1$ and $(a, b) = (0, 1)$. $\blacksquare$

**Modular version.** Lemma 2 is an identity of integers, so it also holds modulo $m$: if $a \equiv F_k$ and $b \equiv F_{k+1} \pmod m$, then $c \equiv F_{2k}$ and $d \equiv F_{2k+1} \pmod m$, because sums, differences and products respect congruences. Reducing $a$ and $b$ after each pass keeps the invariant modulo $m$, and the result is $F_n \bmod m$.
