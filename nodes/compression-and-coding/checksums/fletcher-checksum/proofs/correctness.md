---
title: The deferred Fletcher loop computes the two sums of the definition, and the exact rules for the errors it misses
proves: [correctness]
status: full
---

Let the words be $d_1, \ldots, d_m$, each in $[0, M]$, where $M = 2^b - 1$ is 255 or 65535. Write $A_i = (d_1 + \cdots + d_i) \bmod M$ and $B_i = (A_1 + \cdots + A_i) \bmod M$. The definition of the checksum is the pair $(A_m, B_m)$.

**Lemma 1 (closed form).** $A_m \equiv \sum_{i=1}^{m} d_i$ and $B_m \equiv \sum_{i=1}^{m} (m - i + 1)\, d_i \pmod M$.

*Proof.* The first claim is the definition. For the second, $B_m \equiv \sum_{t=1}^{m} \sum_{i=1}^{t} d_i = \sum_{i=1}^{m} d_i \cdot |\{t : i \le t \le m\}| = \sum_{i=1}^{m} (m - i + 1) d_i$. $\square$

**Lemma 2 (no overflow).** At the start of a block, let $0 \le A, B \le M - 1$. After $k$ runs of lines L5 and L6 inside the block, $A \le (M - 1) + kM$ and $B \le (M - 1) + k(M - 1) + M k(k + 1)/2$. For $M = 255$ and $k \le 5802$, and for $M = 65535$ and $k \le 360$, this bound is at most $2^{32} - 1$.

*Proof.* Each word is at most $M$, so after $t$ words $A \le (M - 1) + tM$. Line L6 adds this value of $A$ for $t = 1, \ldots, k$, so $B \le (M - 1) + \sum_{t=1}^{k} ((M - 1) + tM)$, which is the bound. Direct evaluation gives $4{,}294{,}272{,}227$ for $M = 255, k = 5802$ and $4{,}282{,}122{,}074$ for $M = 65535, k = 360$, both at most $2^{32} - 1 = 4{,}294{,}967{,}295$, while $k = 5803$ and $k = 361$ exceed $2^{32} - 1$. Since $A \le B$ after the first word, $A$ fits too. $\square$

**Theorem 1 (correctness).** FLETCHER returns $(A_m, B_m)$.

*Proof.* Let $p$ be the number of words read so far. We show the invariant: after each run of lines L5 and L6, the integer values satisfy $A \equiv \sum_{i \le p} d_i$ and $B \equiv \sum_{t \le p} \sum_{i \le t} d_i \pmod M$. At line L1 both are 0 with $p = 0$. Line L5 adds $d_{p+1}$ to $A$, and line L6 then adds the new $A$, which is congruent to the new prefix sum, to $B$. Lines L7 and L8 replace each value by its residue, which keeps the invariant and restores $A, B \le M - 1$ for Lemma 2. By Lemma 2 no step overflows, so the integer arithmetic is exact. When the outer loop of line L2 ends, $p = m$, and after line L8 both values are in $[0, M - 1]$. So $A = A_m$ and, by Lemma 1, $B = B_m$. $\square$

Below, the receiver compares the pair of the received words with the pair of the sent words. An error changes $d_i$ into $d_i + \delta_i$, with $|\delta_i| \le M$, and does not change $m$. By Lemma 1, the error is missed if and only if

$$\sum_i \delta_i \equiv 0 \quad\text{and}\quad \sum_i (m - i + 1) \delta_i \equiv 0 \pmod M. \qquad (\ast)$$

**Corollary 1 (single words).** A change of one word from $x$ to $y \ne x$ is missed if and only if $\{x, y\} = \{0, M\}$.

*Proof.* Condition $(\ast)$ reduces to $y - x \equiv 0 \pmod M$. Since $0 < |y - x| \le M$, this holds only for $|y - x| = M$, that is, $\{x, y\} = \{0, M\}$. Then both sums of $(\ast)$ are multiples of $M$. $\square$

**Corollary 2 (swaps).** Swapping $x$ at position $i$ with $y$ at position $j > i$ is missed if and only if $(j - i)(x - y) \equiv 0 \pmod M$. In particular an adjacent swap is missed only if $\{x, y\} = \{0, M\}$ or $x = y$.

*Proof.* Here $\delta_i = y - x$ and $\delta_j = x - y$. The first sum of $(\ast)$ is 0. The second is $(m - i + 1)(y - x) + (m - j + 1)(x - y) = (j - i)(y - x)$. For $j = i + 1$ it is $y - x$, and Corollary 1 applies. $\square$

**Corollary 3 (two adjacent words).** If only the words at positions $i$ and $i + 1$ change, the error is missed if and only if both $\delta_i$ and $\delta_{i+1}$ are in $\{0, M, -M\}$.

*Proof.* Condition $(\ast)$ reads $\delta_i + \delta_{i+1} \equiv 0$ and $(m - i + 1)\delta_i + (m - i)\delta_{i+1} \equiv 0$. Subtracting $(m - i)$ times the first from the second gives $\delta_i \equiv 0$, and then $\delta_{i+1} \equiv 0$. Conversely both conditions then hold. A value with $|\delta| \le M$ is a multiple of $M$ only if it is $0$ or $\pm M$. $\square$

**Corollary 4 (short bursts, Fletcher-16).** Every burst of at most 7 bits is detected. A burst of 8 bits is missed only if it is one whole aligned byte that goes from 0x00 to 0xFF or back.

*Proof.* A burst of at most 8 bits lies in at most two adjacent bytes. By Corollary 3, it is missed only if every byte it touches changes by $0$ or $\pm 255$. The first and the last bits of a burst are flipped, so each byte it touches has a nonzero change, which must then be $\pm 255$: all 8 bits of that byte flip in one direction. That needs 8 bits of the burst inside one byte, so the burst is exactly one aligned byte, going from 0x00 to 0xFF or back. A burst of at most 7 bits cannot do this. $\square$

**Corollary 5 (check bytes).** For $c_0 = 255 - ((A_m + B_m) \bmod 255)$ and $c_1 = 255 - ((A_m + c_0) \bmod 255)$, both sums of $d_1, \ldots, d_m, c_0, c_1$ are 0 mod 255.

*Proof.* Appending $c_0$ then $c_1$ gives the sums $A' = A_m + c_0 + c_1$ and $B' = B_m + (A_m + c_0) + (A_m + c_0 + c_1)$. The choice of $c_1$ gives $A' \equiv 0$. Then $B' \equiv B_m + A_m + c_0 \equiv 0$ by the choice of $c_0$. $\square$

**Cost.** Lines L5 and L6 run once per word, and lines L7 and L8 once per block of $K$ words. So the time is $\Theta(m) = \Theta(n)$, with two registers of extra space. $\blacksquare$
