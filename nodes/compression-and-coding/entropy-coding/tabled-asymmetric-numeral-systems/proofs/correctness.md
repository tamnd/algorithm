---
title: The FSE spread fills each cell once, each encoding step is undone by one decoding step, and all steps together cost at most 1 bit more than the sum of lg((L + u)/(f + j))
proves: [correctness, termination, length]
status: full
---

Notation. $L = 2^R$ with $R \ge 4$. Each symbol $s$ that occurs has $f_s = \max(norm[s], 1)$ cells, and $\sum_s f_s = L$. A cell $u \in [0, L)$ stands for the encoder value $x = L + u \in [L, 2L)$. For a symbol $s$, its cells in increasing order are $u_0 < u_1 < \cdots < u_{f_s - 1}$ (the list $states[s]$ of line L11), and line L9 gives the cell $u_j$ the number $t = f_s + j$.

**Lemma 1 (the spread).** Lines L1 to L6 give every cell exactly one symbol, give the symbol $s$ exactly $f_s$ cells, and end with $pos = 0$.

*Proof.* Lines L1 and L2 fill the top cells, one per symbol with $norm[s] = -1$, from $L - 1$ down, and leave $high$ just below them. For $R \ge 4$, $(L \gg 1) + (L \gg 3)$ is even, so the step is odd and thus prime to $L$. So the positions $0, step, 2 \cdot step, \ldots$ taken mod $L$ visit all $L$ cells once in each cycle of $L$ moves. Line L6 skips the cells above $high$, so lines L4 to L6 place the symbols on the cells $0, \ldots, high$ in the order of this cycle, and each such cell is reached once. There are $high + 1 = \sum_{norm[s] > 0} norm[s]$ of these cells, so they are exactly filled. After the last placement, the next cell of the cycle that is not above $high$ is the start of the next cycle, cell 0. $\square$

**Lemma 2 (the next states of a symbol partition the table).** For each symbol $s$, every $x \in [L, 2L)$ has exactly one $k \ge 0$ with $f_s \le \lfloor x / 2^k \rfloor < 2 f_s$. With $t = \lfloor x/2^k \rfloor$ and $j = t - f_s$, the cell $u_j$ has $nb = k$ and $base + (x \bmod 2^k) = x - L$. So the ranges $[base, base + 2^{nb})$ of the cells of $s$ partition $[0, L)$.

*Proof.* The intervals $[f_s 2^k, 2 f_s 2^k)$ for $k = 0, 1, \ldots$ are disjoint and cover $[f_s, \infty)$, and $x \ge L \ge f_s$, so $k$ exists and is unique. Since $\lfloor \lg x \rfloor = R$, the number $t = \lfloor x / 2^k \rfloor$ has $\lfloor \lg t \rfloor = R - k$, so line L10 gives $nb = R - \lfloor \lg t \rfloor = k$ and $base = t 2^k - L$. Then $base + (x \bmod 2^k) = t 2^k + (x \bmod 2^k) - L = x - L$. Each $x$ gives one cell and one offset, and different $x$ give different pairs, so the ranges partition $[0, L)$. $\square$

**Theorem 1 (correctness).** For each message $d_0 \ldots d_{n-1}$ of symbols that occur, DECODE returns it and uses up the stream.

*Proof.* Let $c_i$ be the cell of the encoder after it handles $d_i$: $c_{n-1}$ is set at line L12, and for $i = n - 2, \ldots, 0$ lines L14 to L16 compute $c_i$ from $c_{i+1}$ and write $k_i$ bits. By line L11 the cell $c_i$ holds the symbol $d_i$. By Lemma 2, the decoder at cell $c_i$ reads $nb = k_i$ bits and computes $base + bits = c_{i+1}$, provided that the bits it reads are the bits that the encoder wrote at step $i$. The writer appends the bits of steps $n - 2, \ldots, 0$, then the $R$ bits of $c_0$, then the end mark. The reader finds the end mark and reads backward, each group of bits as the number that the writer wrote. So it reads $c_0$ first, then the bits of step 0, then of step 1, and so on: the groups in the reverse order of writing, which is the order in which the decoder needs them. By induction on $i$, the decoder is at cell $c_i$ when it outputs symbol $i$, so it outputs $d_i$. After symbol $n - 1$ it reads nothing more (line L21), and all groups have been read, so line L22 passes. $\square$

**Theorem 2 (length).** Let step $i$ code $d_i$ from the value $x_i = L + c_{i+1}$ into the cell $c_i = u_{j_i}$ of $d_i$, with $t_i = f_{d_i} + j_i$. Then
$$\sum_{i=0}^{n-2} k_i \le 1 + \sum_{i=0}^{n-2} \lg \frac{L + c_i}{t_i},$$
and the stream has $\sum_i k_i + R + 1$ bits before the padding to a byte.

*Proof.* By Lemma 2, $x_i \ge t_i 2^{k_i}$, so $k_i \le \lg(x_i / t_i) = \lg((L + c_i)/t_i) + \lg x_i - \lg(L + c_i)$. The value $x_i$ is $L + c_{i+1}$, so the last terms sum to $\lg(L + c_{n-1}) - \lg(L + c_0) < \lg(2L) - \lg L = 1$. $\square$

If the cells of $s$ were placed at $u_j = jL/f_s$ exactly, then $(L + u_j)/(f_s + j) = L / f_s$, and each step would cost at most the ideal $\lg(L/f_s)$. The spread places them only close to these points, and the difference is the loss of the tabled form.

**Termination.** The spread makes $O(L)$ moves, because each cell of the cycle is visited at most once. Building the tables takes $O(L + k)$ for $k$ symbols. Line L15 finds $k$ from the bit lengths of $x$ and $f_s$ with one correction, so each coding step and each decoding step takes a constant number of operations. $\blacksquare$
