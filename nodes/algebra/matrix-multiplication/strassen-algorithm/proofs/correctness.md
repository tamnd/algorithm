---
title: Strassen's seven products give the matrix product
proves: [correctness, termination]
status: full
---

Let $R$ be a ring (an additive abelian group with an associative multiplication that distributes over addition). Commutativity of the multiplication is not used. For matrices over $R$ of matching shapes, the matrix ring laws hold: $X(Y + Z) = XY + XZ$, $(X + Y)Z = XZ + YZ$, $X(-Y) = -(XY) = (-X)Y$, and block multiplication: if $A$ and $B$ are split into $2 \times 2$ blocks with matching inner splits, then $(AB)_{rs} = A_{r1} B_{1s} + A_{r2} B_{2s}$.

**Lemma (the four identities).** For any blocks of matching shapes, with $M_1, \ldots, M_7$ defined as in lines L4 to L10 but with exact products,

$$\begin{aligned} M_1 + M_4 - M_5 + M_7 &= A_{11} B_{11} + A_{12} B_{21}, &\quad M_3 + M_5 &= A_{11} B_{12} + A_{12} B_{22}, \\ M_2 + M_4 &= A_{21} B_{11} + A_{22} B_{21}, &\quad M_1 - M_2 + M_3 + M_6 &= A_{21} B_{12} + A_{22} B_{22}. \end{aligned}$$

*Proof.* Expand each product by distributivity, with the $A$ factor kept on the left:

- $M_1 = A_{11}B_{11} + A_{11}B_{22} + A_{22}B_{11} + A_{22}B_{22}$
- $M_2 = A_{21}B_{11} + A_{22}B_{11}$
- $M_3 = A_{11}B_{12} - A_{11}B_{22}$
- $M_4 = A_{22}B_{21} - A_{22}B_{11}$
- $M_5 = A_{11}B_{22} + A_{12}B_{22}$
- $M_6 = A_{21}B_{11} + A_{21}B_{12} - A_{11}B_{11} - A_{11}B_{12}$
- $M_7 = A_{12}B_{21} + A_{12}B_{22} - A_{22}B_{21} - A_{22}B_{22}$

*First identity.* In $M_1 + M_4 - M_5 + M_7$, the term $A_{11}B_{22}$ appears in $M_1$ and in $-M_5$ and cancels. $A_{22}B_{11}$ appears in $M_1$ and with a minus sign in $M_4$. $A_{22}B_{22}$ appears in $M_1$ and with a minus sign in $M_7$. $A_{22}B_{21}$ appears in $M_4$ and with a minus sign in $M_7$. $A_{12}B_{22}$ appears in $-M_5$ with a minus sign and in $M_7$ with a plus sign. What is left is $A_{11}B_{11} + A_{12}B_{21}$.

*Second identity.* $M_3 + M_5 = A_{11}B_{12} - A_{11}B_{22} + A_{11}B_{22} + A_{12}B_{22} = A_{11}B_{12} + A_{12}B_{22}$.

*Third identity.* $M_2 + M_4 = A_{21}B_{11} + A_{22}B_{11} + A_{22}B_{21} - A_{22}B_{11} = A_{21}B_{11} + A_{22}B_{21}$.

*Fourth identity.* In $M_1 - M_2 + M_3 + M_6$: $A_{11}B_{11}$ cancels between $M_1$ and $M_6$; $A_{11}B_{22}$ cancels between $M_1$ and $M_3$; $A_{22}B_{11}$ cancels between $M_1$ and $-M_2$; $A_{21}B_{11}$ cancels between $-M_2$ and $M_6$; $A_{11}B_{12}$ cancels between $M_3$ and $M_6$. What is left is $A_{22}B_{22} + A_{21}B_{12}$. Addition is commutative, so this is the claimed right side. $\square$

**Lemma (padding).** Let $A'$ be $A$ with zero rows added at the bottom and zero columns added at the right, and $B'$ be $B$ with zero rows added at the bottom (as many as the zero columns of $A'$) and zero columns at the right. Then the top left $n \times p$ block of $A'B'$ is $AB$.

*Proof.* For $i < n$ and $j < p$, $(A'B')[i][j] = \sum_{k < m} A[i][k]B[k][j] + \sum_{k \ge m} A'[i][k] B'[k][j]$, and each term of the second sum has $A'[i][k] = 0$. $\square$

**Theorem.** For every $n_0 \ge 1$ and all $A \in R^{n \times m}$, $B \in R^{m \times p}$, STRASSEN$(A, B)$ stops and returns $AB$.

*Proof.* Let $\mu = \max(n, m, p)$. We use strong induction on $\mu$, and inside one value of $\mu$, we first treat the calls of line L3 (all sides even) and then the calls of line L2.

*Line L1.* If $\min(n, m, p) \le n_0$, the result is the classical product, which is correct by the [triple loop proof](/naive-matrix-multiplication/). This covers every $\mu \le n_0$ and every input with a side $0$.

*All sides even, $\min(n, m, p) > n_0 \ge 1$.* Then all sides are at least 2. Line L3 splits each side $d$ into two halves of length $d/2 < d$. Each of the seven calls of lines L4 to L10 has the shape $(n/2) \times (m/2)$ times $(m/2) \times (p/2)$, with $\max < \mu$, so by the hypothesis it returns the exact product of its two operands. By the first lemma, lines L11 to L14 compute the four blocks $(AB)_{rs}$, and by block multiplication the matrix of line L15 is $AB$.

*Some side odd, $\min(n, m, p) > n_0$.* Line L2 pads each odd side by one, so the padded sides are even and at most $\mu + 1$. The call on the padded matrices passes line L1 (its sides are at least the old ones) and goes to line L3 with all sides even. Its seven calls have sides at most $\lceil \mu / 2 \rceil$, which is less than $\mu$ since $\mu \ge 2$, so by the hypothesis and the case above, the padded call returns $A'B'$. By the padding lemma, removing the padding gives $AB$.

*Termination.* Each call either returns at line L1, or calls itself on sides at most $\lceil \mu/2 \rceil < \mu$ after at most one padding step. So $\mu$ drops along each path of the recursion, and the depth is $O(\log \mu)$. $\blacksquare$
