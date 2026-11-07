---
title: The blocked schedule computes AB and its I/O count
proves: [correctness, termination]
status: full
---

Let $R$ be a semiring: addition is associative and commutative with a zero, multiplication is associative and distributes over addition. Commutativity of the multiplication is not used, and no subtraction is used. $A$ is $n \times m$, $B$ is $m \times p$, and $b \ge 1$ is the tile side.

## Correctness

For $t \ge 0$ let $I_t = \{tb, \ldots, \min(tb + b, n) - 1\}$, and define $K_t$ for $m$ and $J_t$ for $p$ in the same way. The nonempty sets $I_t$ partition $\{0, \ldots, n-1\}$, and similarly for $K_t$ and $J_t$. Line L1 runs over the $I_t$, line L2 over the $J_t$ and line L4 over the $K_t$.

**Invariant of the loop at line L4.** Fix the tile $(I, J)$ chosen at lines L1 and L2. Before the iteration of line L4 for $K_s$, the tile in fast memory satisfies
$$T_C[i][j] = \sum_{t < s} \sum_{k \in K_t} a_{ik} b_{kj} \quad \text{for all } i \in I, j \in J.$$

*Initialization.* At line L3, $T_C$ is zero (the output starts as zero), which is the empty sum for $s = 0$.

*Maintenance.* Line L5 loads $T_A = (a_{ik})_{i \in I, k \in K_s}$ and $T_B = (b_{kj})_{k \in K_s, j \in J}$. Line L6 adds $\sum_{k \in K_s} a_{ik} b_{kj}$ to each entry $(i, j)$, by the correctness of the triple loop (each product keeps the $a$ factor on the left). So the invariant holds for $s + 1$.

*End.* After the last $K_s$, $T_C[i][j] = \sum_{k=0}^{m-1} a_{ik} b_{kj} = (AB)_{ij}$, because the $K_t$ partition $\{0, \ldots, m-1\}$. Line L7 writes this into $C$.

Every pair $(i, j)$ lies in exactly one tile $(I, J)$, and each tile is written only once, at line L7 of its own iteration. So at the end $C = AB$. $\square$

**Summation order.** In the proof of maintenance, line L6 runs the triple loop with $k$ increasing over $K_s$, and line L4 takes the $K_s$ in increasing order. So $c_{ij}$ receives the terms $a_{i0}b_{0j}, a_{i1}b_{1j}, \ldots, a_{i,m-1}b_{m-1,j}$ in this order, as in the plain loop. In floating point, each partial sum is rounded in the same order, so the two results agree bit for bit (when both use the same multiply and add instructions).

## Termination

Each of the loops at lines L1, L2 and L4 runs over a finite range with a positive step $b$, and line L6 runs a triple loop over finite ranges. So the method stops after $\lceil n/b \rceil \lceil p/b \rceil \lceil m/b \rceil$ iterations of line L5.

## The I/O count

Store each matrix in row-major order, starting at any word address. Blocks are the intervals $[\ell B, \ell B + B)$ of word addresses.

**Lemma 1.** A run of $w \ge 1$ consecutive words touches at most $\lceil w/B \rceil + 1$ blocks. If the run starts at a multiple of $B$ and $B$ divides $w$, it touches exactly $w/B$ blocks.

*Proof.* The run from address $x$ to $x + w - 1$ touches the blocks $\lfloor x/B \rfloor$ to $\lfloor (x + w - 1)/B \rfloor$, which is $\lfloor (x+w-1)/B \rfloor - \lfloor x/B \rfloor + 1 \le \lfloor (w-1)/B \rfloor + 2 \le \lceil w/B \rceil + 1$ blocks, since $\lfloor u + v \rfloor - \lfloor u \rfloor \le \lceil v \rceil$ for real $u$ and $v \ge 0$. The aligned case is direct. $\square$

**Lemma 2.** A tile with at most $b$ rows and at most $b$ columns touches at most $b(\lceil b/B \rceil + 1)$ blocks. If $b \ge B$ this is at most $3b^2/B$ blocks, that is $3b^2$ words.

*Proof.* Each row of the tile is a run of at most $b$ words in row-major storage, so Lemma 1 applies to each row. If $b \ge B$ then $\lceil b/B \rceil + 1 \le b/B + 2 \le 3b/B$. $\square$

**Theorem.** Let $n = m = p$, and let $T = \lceil n/b \rceil$.

1. *Aligned case.* If $b$ divides $n$, $B$ divides $b$, and the matrices start at multiples of $B$, the schedule makes exactly $2n^3/(bB) + 2n^2/B$ I/Os and needs $3b^2$ words of fast memory.
2. *General case.* If $B \le b \le n$, the schedule makes at most $2(T^3 + T^2) \cdot 3b^2/B \le 48 n^3/(bB) + 24 n^2/B$ I/Os and needs at most $9b^2$ words of fast memory. With $b = \lfloor \sqrt M / 3 \rfloor$ and $M \ge \max(9B^2, 36)$, this is $O(n^3/(B\sqrt M) + n^2/B)$.

*Proof.* There are $T^2$ tiles of $C$. Each is read once at line L3 and written once at line L7. For each of them, line L5 runs $T$ times and reads one tile of $A$ and one of $B$. So there are $2T^2$ tile transfers for $C$ and $2T^3$ for $A$ and $B$, $2(T^3 + T^2)$ in all. Fast memory holds three tiles at any time.

In the aligned case, every tile has $b$ rows of $b$ words, each row starts at a multiple of $B$, so by Lemma 1 a tile is $b \cdot b/B = b^2/B$ blocks, and $T = n/b$. The count is $2((n/b)^3 + (n/b)^2) \cdot b^2/B = 2n^3/(bB) + 2n^2/B$.

In the general case, Lemma 2 bounds each tile by $3b^2/B$ blocks and $3b^2$ words. Since $b \le n$, $T \le n/b + 1 \le 2n/b$, so $2(T^3 + T^2) \cdot 3b^2/B \le 6(8n^3/b^3 + 4n^2/b^2) b^2/B = 48n^3/(bB) + 24n^2/B$. Three tiles take at most $9b^2 \le M$ words when $b = \lfloor \sqrt M/3 \rfloor$. If $M \ge 36$, then $b \ge \sqrt M/3 - 1 \ge \sqrt M/6$, and if $M \ge 9B^2$, then $b \ge B$ (since $\sqrt M / 3 \ge B$ and $B$ is an integer). So the count is at most $288\, n^3/(B\sqrt M) + 24 n^2/B$. (If $b > n$, there is one tile of each matrix and the count is at most $4 \cdot 3n^2/B$.) $\square$

**Optimality.** Hong and Kung (1981) proved that every schedule of the conventional computation graph of the $n \times n$ product, with $S$ words of fast memory, moves $\Omega(n^3/\sqrt S)$ words; the [red-blue pebble game](/red-blue-pebble-game/) page proves $n^3/(4\sqrt{2S}) - S$ for the one-shot game. Take $S = M$. One I/O moves at most $B$ words, so every such schedule makes $\Omega(n^3/(B\sqrt M) - M/B)$ I/Os. It also reads the $2n^2$ input words, so it makes at least $2n^2/B$ I/Os. Together these give $\Omega(n^3/(B\sqrt M) + n^2/B)$ when $n^3 \ge c M^{3/2}$ for a suitable constant $c$, which is the case where the matrices do not fit in fast memory. So the theorem is optimal up to a constant factor.
