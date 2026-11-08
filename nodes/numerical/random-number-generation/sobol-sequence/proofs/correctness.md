---
title: The Gray-code recurrence produces the Sobol points, each coordinate is stratified, and nets are characterized by ranks
proves: [correctness]
status: full
---

Fix the word size $w$ and a dimension $s$. For each coordinate $j$ the direction numbers are $V_j[k] = m_{j,k}\, 2^{w-k}$ for $k = 1, \ldots, w$. The Sobol point of index $i$, $0 \le i < 2^w$, in natural order is

$$X(i) = \bigl(X_1(i), \ldots, X_s(i)\bigr), \qquad X_j(i) = \bigoplus_{k \,:\, i_k = 1} V_j[k],$$

where $i = \sum_{k \ge 1} i_k 2^{k-1}$ is the binary expansion of $i$, and the point in $[0, 1)^s$ is $X(i) / 2^w$. Write $g(n) = n \oplus \lfloor n/2 \rfloor$ for the binary reflected Gray code and $c(n)$ for one plus the number of trailing 1 bits of $n$, the value computed in lines L2 and L3.

**Lemma 1 (Gray code).** (a) $g(n+1) = g(n) \oplus 2^{c(n) - 1}$. (b) $g$ is a bijection of $\{0, \ldots, 2^w - 1\}$, and for every $m \le w$ it maps each aligned block $\{b 2^m, \ldots, (b+1) 2^m - 1\}$ onto an aligned block.

*Proof.* (a) Let $c = c(n)$. The low $c$ bits of $n$ are $0 1 \cdots 1$ (with $c - 1$ ones), and adding 1 turns them into $1 0 \cdots 0$ without changing the higher bits, so $n \oplus (n + 1) = 2^c - 1$. Since $g$ is linear over $\mathrm{GF}(2)$ in the bits, $g(n) \oplus g(n+1) = (2^c - 1) \oplus \lfloor (2^c - 1)/2 \rfloor = (2^c - 1) \oplus (2^{c-1} - 1) = 2^{c-1}$. (b) $n$ is recovered from $g(n)$ from the top bit down, since bit $p$ of $n$ is bit $p$ of $g(n)$ XOR bit $p + 1$ of $n$; so $g$ is injective on a finite set, hence a bijection. Bit $p$ of $g(n)$ depends only on bits $p$ and $p + 1$ of $n$, so for $p \ge m$ it is constant on an aligned block of size $2^m$. Thus $g$ maps the block injectively into one aligned block of the same size, hence onto it. $\square$

**Theorem 1 (the recurrence).** If the state starts with $X = 0$ and $n = 0$, the $(n+1)$-th call of SOBOL-NEXT returns $X(g(n))$, for $0 \le n < 2^w$. In particular, the first $2^m$ calls return the first $2^m$ Sobol points $X(0), \ldots, X(2^m - 1)$ in some order, and so does every aligned block of $2^m$ calls.

*Proof.* The map $i \mapsto X(i)$ is linear over $\mathrm{GF}(2)$: $X(i \oplus i') = X(i) \oplus X(i')$, because each bit of $i \oplus i'$ is the XOR of the corresponding bits. We show by induction that before the $(n+1)$-th call the state holds $X = X(g(n))$ and the counter $n$. For $n = 0$, $X = 0 = X(g(0))$. Line L1 copies the state, so the call returns $X(g(n))$. Lines L2 and L3 compute $c = c(n)$, line L4 replaces $X$ by $X(g(n)) \oplus X(2^{c-1}) = X(g(n) \oplus 2^{c-1}) = X(g(n+1))$ by linearity and Lemma 1(a), since $X_j(2^{c-1}) = V_j[c]$, and line L5 increments $n$. (When $n = 2^w - 1$, $c = w + 1$ and there is no successor; the implementation skips line L4.) The statement about blocks follows from Lemma 1(b). $\square$

**Lemma 2 (direction numbers).** Suppose the initial values $m_{j,1}, \ldots, m_{j,e}$ of coordinate $j$, with $e$ the degree of its polynomial $x^e + a_1 x^{e-1} + \cdots + a_{e-1} x + 1$, are odd and satisfy $m_{j,k} < 2^k$. Then the values produced by the recurrence

$$m_{j,k} = 2 a_1 m_{j,k-1} \oplus 2^2 a_2 m_{j,k-2} \oplus \cdots \oplus 2^{e-1} a_{e-1} m_{j,k-e+1} \oplus 2^e m_{j,k-e} \oplus m_{j,k-e}$$

are odd and satisfy $m_{j,k} < 2^k$ for all $k \le w$. The implementation's update $V[k] = V[k-e] \oplus (V[k-e] \gg e) \oplus \bigoplus_{i} a_i V[k-i]$ is this recurrence multiplied by $2^{w-k}$.

*Proof.* Every term except the last is a multiple of 2, so $m_{j,k}$ is odd if $m_{j,k-e}$ is. Each term $2^i m_{j,k-i}$ is below $2^i 2^{k-i} = 2^k$ by induction, and the XOR of numbers below $2^k$ is below $2^k$. For the implementation, $V[k-i] = m_{j,k-i} 2^{w-k} 2^{i}$, and $V[k-e] \gg e = m_{j,k-e} 2^{w-k}$ exactly, because $w - k \ge 0$. $\square$

**Corollary 1 (each coordinate is stratified).** Let $C_j$ be the $w \times w$ matrix over $\mathrm{GF}(2)$ whose entry $(r, k)$ is the $r$-th binary digit after the point of $V_j[k] / 2^w$. Then $C_j$ is upper triangular with ones on the diagonal, and in every aligned block of $2^m$ points, $m \le w$, coordinate $j$ takes exactly one value in each interval $[a 2^{-m}, (a+1) 2^{-m})$.

*Proof.* $V_j[k] / 2^w = m_{j,k} 2^{-k}$ with $m_{j,k}$ odd and below $2^k$: its digits after position $k$ are 0 and digit $k$ is 1. So $C_j(r, k) = 0$ for $r > k$ and $C_j(k, k) = 1$. For $i = b 2^m + \rho$ with $0 \le \rho < 2^m$, the top $m$ digits of $X_j(i)$ are $C_j^{(m)} \rho \oplus \kappa$, where $C_j^{(m)}$ is the top left $m \times m$ block of $C_j$, $\rho$ is read as a bit vector, and $\kappa$ depends only on $b$. The block $C_j^{(m)}$ is unit upper triangular, hence invertible, so $\rho \mapsto C_j^{(m)} \rho \oplus \kappa$ is a bijection of $\mathrm{GF}(2)^m$. By Theorem 1, the same holds for aligned blocks of the output order. $\square$

**Lemma 3 (net criterion).** Let $0 \le t \le m \le w$. An aligned block of $2^m$ Sobol points is a $(t, m, s)$-net in base 2, meaning that every box $\prod_j [a_j 2^{-d_j}, (a_j + 1) 2^{-d_j})$ with integers $d_j \ge 0$, $\sum_j d_j = m - t$, contains exactly $2^t$ of the points, if and only if for every such $(d_1, \ldots, d_s)$ the $m - t$ vectors formed by the first $d_j$ rows of each $C_j$, restricted to its first $m$ columns, are linearly independent over $\mathrm{GF}(2)$.

*Proof.* As in Corollary 1, write the indices of the block as $i = b 2^m + \rho$. The point $X(i)/2^w$ lies in the box exactly when, for each $j$ and each $r \le d_j$, digit $r$ of $X_j(i)$ equals digit $r$ of $a_j$ written with $d_j$ digits. Digit $r$ of $X_j(i)$ is $\sum_{k \le m} C_j(r, k) \rho_k \oplus (\text{a constant depending on } b)$. So the condition is a linear system $A \rho = \beta$ with $A$ the $(m - t) \times m$ matrix of the stated rows and $\beta$ determined by the box and $b$. If $A$ has rank $m - t$, the system has exactly $2^{m - (m - t)} = 2^t$ solutions for every $\beta$, so every box holds $2^t$ points. If the rank is smaller, the image of $A$ is a proper subspace; for a $\beta$ outside it, and the box that gives that $\beta$ (every $\beta$ arises from exactly one box, since $a_j$ ranges over all $d_j$-digit values), the box is empty, so the block is not a net. $\square$

The implementation's `t_value` applies Lemma 3 for $t = 0, 1, \ldots$ and returns the least $t$ that works, computing ranks exactly by Gaussian elimination over $\mathrm{GF}(2)$. Sobol's theorem, which we cite and do not prove here, states that when the polynomials are distinct primitive polynomials of degrees $e_1, \ldots, e_s$ (with $e = 1$ for the first coordinate), every aligned block is a $(t, m, s)$-net with $t = \sum_j (e_j - 1)$, for all $m \ge t$. The tests confirm this bound with Lemma 3 for $s \le 5$ and $m \le 10$, confirm by direct counting that blocks of 256 points are $(0, 8, 2)$-nets in the first two coordinates and $(1, 8, 3)$-nets in the first three, and check by exact polynomial arithmetic that all the polynomials used are primitive. $\blacksquare$
