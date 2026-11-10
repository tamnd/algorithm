---
title: P-STRASSEN returns AB, and its parallel steps have no determinacy race
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be $n \times n$ matrices over a ring, which need not be commutative, with $n$ a power of 2. We use the lines of P-STRASSEN and the table of the sums $S_1, \ldots, S_{10}$ and the products $P_1, \ldots, P_7$ on the page. The blocks $A_{ik}$ and $B_{kj}$ are the four $n/2 \times n/2$ quarters, and by the block product rule $(AB)_{ij} = A_{i1} B_{1j} + A_{i2} B_{2j}$.

**Lemma 1 (Strassen's identities).** With the sums and products of the table,

$$P_5 + P_4 - P_2 + P_6 = A_{11}B_{11} + A_{12}B_{21}, \qquad P_1 + P_2 = A_{11}B_{12} + A_{12}B_{22},$$
$$P_3 + P_4 = A_{21}B_{11} + A_{22}B_{21}, \qquad P_5 + P_1 - P_3 - P_7 = A_{21}B_{12} + A_{22}B_{22}.$$

*Proof.* Expand each product by the distributive laws, and keep the factor from $A$ on the left in each term, so that commutativity is not used:

- $P_1 = A_{11}B_{12} - A_{11}B_{22}$, $P_2 = A_{11}B_{22} + A_{12}B_{22}$, $P_3 = A_{21}B_{11} + A_{22}B_{11}$, $P_4 = A_{22}B_{21} - A_{22}B_{11}$;
- $P_5 = A_{11}B_{11} + A_{11}B_{22} + A_{22}B_{11} + A_{22}B_{22}$;
- $P_6 = A_{12}B_{21} + A_{12}B_{22} - A_{22}B_{21} - A_{22}B_{22}$;
- $P_7 = A_{11}B_{11} + A_{11}B_{12} - A_{21}B_{11} - A_{21}B_{12}$.

In $P_5 + P_4 - P_2 + P_6$ the terms $A_{11}B_{22}$, $A_{22}B_{11}$, $A_{22}B_{22}$, $A_{22}B_{21}$ and $A_{12}B_{22}$ cancel in pairs, and $A_{11}B_{11} + A_{12}B_{21}$ is left. $P_1 + P_2$ and $P_3 + P_4$ each lose one pair. In $P_5 + P_1 - P_3 - P_7$ the terms $A_{11}B_{11}$, $A_{11}B_{22}$, $A_{22}B_{11}$, $A_{11}B_{12}$ and $A_{21}B_{11}$ cancel in pairs, and $A_{22}B_{22} + A_{21}B_{12}$ is left. $\blacksquare$

**Lemma 2 (no races).** The ten sums of line L4, the seven calls of line L5, and the four block sums of line L7 can each run in parallel with no [determinacy race](/determinacy-race/).

*Proof.* Each sum of line L4 reads two blocks of $A$ or of $B$ and writes its own new matrix $S_t$. Each call of line L5 reads two of the inputs and the sums, which no task of line L5 writes, and writes its own new matrix $P_t$ and the matrices it allocates. Each block sum of line L7 reads some of the $P_t$ and writes its own block of $C$. In each of the three steps, no cell is written by one task and read or written by another. The sync after each step makes the next step read only finished values. $\blacksquare$

**Theorem 3.** P-STRASSEN ends and returns $AB$.

*Proof.* By induction on $n$. For $n = 1$, line L2 returns $(a_{11} b_{11})$. For $n \ge 2$ the seven calls of line L5 have size $n/2$, so they end and return the seven products by the induction hypothesis. By Lemma 1, line L7 sets each block $C_{ij}$ to $A_{i1}B_{1j} + A_{i2}B_{2j} = (AB)_{ij}$, and by Lemma 2 the parallel run gives the same values as a run in sequence. $\blacksquare$
