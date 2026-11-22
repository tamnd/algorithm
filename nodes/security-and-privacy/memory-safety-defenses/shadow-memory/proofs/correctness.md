---
title: Shadow memory returns the last value set for each granule
proves: [correctness, invariant]
status: full
---

**Setting.** Let $k \ge 0$. The abstract state is a map $\sigma$ from granules to bytes, with $\sigma(g) = d$ for every $g$ at the start, where $d$ is the default. SET$(a, v)$ changes $\sigma$ to $\sigma[a \gg k \mapsto v]$. SETRANGE$(lo, hi, v)$, for multiples $lo \le hi$ of $2^k$, sets $\sigma(g) = v$ for every $g$ with $lo \le g \cdot 2^k < hi$. GET$(a)$ must return $\sigma(a \gg k)$. Application writes go to addresses in $[0, N)$ and do not change $\sigma$.

**Lemma 1 (direct map).** Let $\mathit{off} \ge N$. Before and after each operation, $M[g + \mathit{off}] = \sigma(g)$ for every granule $g < N / 2^k$.

*Proof.* By induction on the number of operations. At the start the constructor writes $d$ to every byte of $[\mathit{off}, \mathit{off} + N/2^k)$, so the claim holds. The map $g \mapsto g + \mathit{off}$ is one to one, and its image is disjoint from $[0, N)$ because $\mathit{off} \ge N$.

- SET$(a, v)$ writes $M[(a \gg k) + \mathit{off}]$ in lines L1 and L3. That is the stored byte of $g_0 = a \gg k$ and of no other granule, so after the write the claim holds for $g_0$ with value $v$ and is unchanged for every other $g$.
- SETRANGE runs SET in line L5 for $a = lo, lo + 2^k, \dots, hi - 2^k$, whose granules are exactly the $g$ with $lo \le g \cdot 2^k < hi$. Each step keeps the claim by the case above.
- GET writes nothing.
- An application write changes a byte in $[0, N)$, which is not a stored byte. $\square$

**Lemma 2 (two-level table).** Let $0 \le k \le c \le b$ and $s = 2^{c-k}$. Before and after each operation: (a) for every distinguished chunk $D_v$, every byte of $D_v$ is $v$; (b) for every granule $g < 2^{b-k}$, $P[g \gg (c-k)][g \bmod s] = \sigma(g)$; (c) no two entries of $P$ refer to the same private chunk.

*Proof.* By induction. At the start every entry refers to $D_d$, which holds only $d$, so (a), (b) and (c) hold. For an address $a$, lines L6 and L7 compute $i = a \gg c$ and $j = (a \bmod 2^c) \gg k$. With $g = a \gg k$ we have $i = g \gg (c-k)$ and $j = g \bmod s$, so $(i, j)$ is the position of $g$ in (b), and distinct granules have distinct positions.

- SET$(a, v)$. If $P[i]$ is distinguished and $P[i][j] = v$, nothing changes and $\sigma(g)$ was already $v$ by (b). If $P[i]$ is distinguished and $P[i][j] \ne v$, line L9 puts a new private copy in $P[i]$; the copy has the same bytes, so (b) still holds, no distinguished chunk changes, and the copy is referred to by $P[i]$ only, so (c) holds. Now $P[i]$ is private, and line L10 writes byte $j$ of it. By (c), this changes position $(i, j)$ and no position of another entry, so (b) holds with $\sigma(g) = v$ and is unchanged elsewhere. A distinguished chunk is never written, so (a) holds.
- SETRANGE$(lo, hi, v)$. Line L12 makes entry $i$ of each chunk inside the range refer to $D_v$. By (a), every position of entry $i$ then holds $v$, which is the new $\sigma$ on all granules of that chunk. The private chunk it referred to, if any, is no longer referred to, so (c) holds. Line L13 handles the other granules of the range by SET, which keeps (a), (b) and (c) by the case above. Every granule of the range is covered once, by line L12 or by line L13, and no granule outside it is touched.
- GET writes nothing. $\square$

**Theorem.** In both representations, GET$(a)$ returns $\sigma(a \gg k)$: the value of the last SET or SETRANGE that covered the granule of $a$, or the default $d$ if there was none.

*Proof.* In the direct map, line L2 returns $M[(a \gg k) + \mathit{off}]$, which is $\sigma(a \gg k)$ by Lemma 1. In the two-level table, GET returns $P[i][j]$, which is $\sigma(a \gg k)$ by Lemma 2(b) and the computation of $(i, j)$. By the definition of SET and SETRANGE on $\sigma$, that value is the one of the last operation that covered the granule, or $d$. $\blacksquare$

**Termination.** Every operation is a bounded number of steps, except SETRANGE, which runs once per granule or chunk of the finite range, and the copy in line L9, which copies $s$ bytes.
