---
title: The block-swap rounds transpose the bit matrix
proves: [correctness]
status: full
---

Let $n = 2^q$ with $n \le w$, and let the words $A[0], \ldots, A[n-1]$ hold the matrix $M$, with $M[r][c]$ at bit $c$ of $A[r]$. For an index $0 \le r < n$ and $0 \le i < q$ write $r_i$ for bit $i$ of $r$. For a power of two $j = 2^i$ define the map $\sigma_j$ on pairs of indices by
$$ \sigma_j(r, c) = \begin{cases} (r, c) & \text{if } r_i = c_i, \\ (r \oplus j, \, c \oplus j) & \text{if } r_i \ne c_i . \end{cases} $$
So $\sigma_j$ exchanges bit $i$ of the row index with bit $i$ of the column index and keeps all other bits: if the two bits are equal there is nothing to exchange, and if they differ, flipping both exchanges them. Hence $\sigma_j$ is an involution, and the maps $\sigma_j$ for different $j$ act on different pairs of bits, so they commute.

**Lemma 1 (the mask).** At the start of the round with block side $j = 2^i$, the mask $m$ is $\sum_{0 \le c < n, \, c_i = 0} 2^c$.

*Proof.* At line L1, $j = n/2$ and $m = 2^{n/2} - 1$, the set of $c < n$ with bit $q - 1$ equal to 0. Suppose that $m$ is the set $C_{i+1}$ of $c < n$ with $c_{i+1} = 0$ in the round $j = 2^{i+1}$, so $m$ is the union of the intervals $[2a \cdot 2^{i+1}, (2a + 1) 2^{i+1})$ for $0 \le a < n / 2^{i+2}$. Line L7 sets $j = 2^i$ and $m \leftarrow m \oplus (m \ll 2^i)$. The shift moves each interval up by $2^i$, so $m \ll 2^i$ is the union of $[2a \cdot 2^{i+1} + 2^i, (2a + 1) 2^{i+1} + 2^i)$. The XOR of the two unions keeps, from each pair of intervals, the part covered by exactly one: $[2a \cdot 2^{i+1}, 2a \cdot 2^{i+1} + 2^i)$ and $[(2a + 1) 2^{i+1}, (2a + 1) 2^{i+1} + 2^i)$. These are exactly the $c < n$ with $c_i = 0$, since $(2a + 1) 2^{i+1} + 2^i \le n$. $\square$

**Lemma 2 (one round).** Let $N$ be the matrix before the round with block side $j = 2^i$, and $N'$ the matrix after it. Then $N'[\sigma_j(r, c)] = N[r][c]$ for all $(r, c)$.

*Proof.* The loop of line L3 visits each $k$ with $k_i = 0$ once, and the pairs $\{k, k + j\}$ for these $k$ partition the rows; row $k + j$ is row $k$ with bit $i$ set. Each iteration reads and writes only the rows $k$ and $k + j$, so the iterations do not interfere. Fix $k$. By Lemma 1, for a column $c$, bit $c$ of $t$ after line L4 is
$$ t_c = \begin{cases} N[k][c + j] \oplus N[k + j][c] & \text{if } c_i = 0, \\ 0 & \text{if } c_i = 1 , \end{cases} $$
since bit $c$ of $A[k] \gg j$ is bit $c + j$ of $A[k]$, which exists when $c_i = 0$ and $c < n$, because then $c + j < n$. Line L5 sets bit $c$ of row $k + j$ to $N[k + j][c] \oplus t_c$, which is $N[k][c + j]$ when $c_i = 0$ and $N[k + j][c]$ when $c_i = 1$. Line L6 XORs $t \ll j$ into row $k$, so bit $c$ of row $k$ becomes $N[k][c] \oplus t_{c - j}$ when $c_i = 1$, which is $N[k + j][c - j]$, and stays $N[k][c]$ when $c_i = 0$; the bits of $t \ll j$ at the columns with $c_i = 0$ are 0, because $t_{c - j} = 0$ or $c - j < 0$ there, and the bits of $t \ll j$ at $c \ge n$ are 0, because $t_{c-j} \ne 0$ needs $(c - j)_i = 0$ and so $c < n$.

So in rows $k$ and $k + j$ the entries with $r_i = c_i$ (row $k$ with $c_i = 0$, row $k + j$ with $c_i = 1$) keep their values, and the entries $(k, c)$ with $c_i = 1$ and $(k + j, c - j)$ swap values. Since $\sigma_j(k, c) = (k + j, c - j)$ for $c_i = 1$, this is the claim. $\square$

**Theorem.** After the loop, bit $r$ of $A[c]$ is $M[r][c]$ for all $0 \le r, c < n$.

*Proof.* The rounds run with $j = 2^{q-1}, \ldots, 2, 1$, each once, because line L7 halves $j$ and the loop stops when $j = 0$. By Lemma 2 the entry that starts at $(r, c)$ ends at $\sigma_1 \circ \sigma_2 \circ \cdots \circ \sigma_{2^{q-1}}(r, c)$. Each $\sigma_{2^i}$ exchanges bit $i$ of the row index with bit $i$ of the column index and changes no other bit, so the composition exchanges every bit of $r$ with the same bit of $c$, and the entry ends at $(c, r)$. So the final matrix $M'$ has $M'[c][r] = M[r][c]$, which is the statement. The same argument shows that the rounds may run in any order, since the maps $\sigma_j$ commute. $\square$

**The one-word version.** With $M[r][c]$ at bit $8r + c$ of one word, for $j \in \{1, 2, 4\}$, the entry $(r, c)$ with $r_i = 0$ and $c_i = 1$ is at position $p = 8r + c$, and $\sigma_j(r, c) = (r + j, c - j)$ is at $p + 7j$. The mask of the round with shift $7j$ has a one at exactly these positions $p$, and $t = (x \oplus (x \gg 7j)) \mathbin{\&} m$, $x \leftarrow x \oplus t \oplus (t \ll 7j)$ swaps the bits at $p$ and $p + 7j$ for each marked $p$ and changes no other bit, because the marked positions and the positions $7j$ above them are disjoint. So each round applies $\sigma_j$, and the three rounds give the transpose by the same argument. $\blacksquare$
