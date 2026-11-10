---
title: P-TRANSPOSE transposes the matrix in place, and its parallel calls touch disjoint cells
proves: [correctness, termination]
status: full
---

We use the lines of P-TRANSPOSE and P-SWAP-T on the page. For a block $X$ we write $X^{\mathsf T}$ for its transpose, and we split an $n \times n$ block with $n \ge 2$ into four blocks of size $n/2$, with $X_{ab}$ the block in block row $a$ and block column $b$. Then

$$(X^{\mathsf T})_{ab} = (X_{ba})^{\mathsf T}, \tag{1}$$

because the entry in row $r$ and column $s$ of $X^{\mathsf T}$ is the entry in row $s$ and column $r$ of $X$, and the swap of $r$ and $s$ also swaps the block row and the block column.

**Lemma 1 (P-SWAP-T).** Let $X$ and $Y$ be two $n \times n$ blocks of $A$ with no cell in common, with $n$ a power of 2. Then P-SWAP-T on $X$ and $Y$ ends, sets $X$ to $Y^{\mathsf T}$ and $Y$ to $X^{\mathsf T}$ (both with their old values), changes no other cell, and its parallel calls touch disjoint sets of cells.

*Proof.* By induction on $n$. For $n = 1$, line L7 swaps the two cells, and a $1 \times 1$ block is its own transpose. Let $n \ge 2$. The four calls of lines L9 and L10 work on the pairs $(X_{11}, Y_{11})$, $(X_{12}, Y_{21})$, $(X_{21}, Y_{12})$ and $(X_{22}, Y_{22})$. The four blocks of $X$ are disjoint, the four blocks of $Y$ are disjoint, and no block of $X$ meets a block of $Y$, so the calls touch disjoint cells, and each pair has no common cell. By the induction hypothesis, the call on $(X_{ab}, Y_{ba})$ ends and sets $X_{ab}$ to $(Y_{ba})^{\mathsf T}$, which is $(Y^{\mathsf T})_{ab}$ by (1), and sets $Y_{ba}$ to $(X_{ab})^{\mathsf T} = (X^{\mathsf T})_{ba}$. As $(a, b)$ runs over the four pairs, this covers all blocks of $X$ and of $Y$. $\blacksquare$

**Theorem 2 (P-TRANSPOSE).** For $n$ a power of 2, P-TRANSPOSE on an $n \times n$ block $D$ on the diagonal of $A$ ends, sets $D$ to $D^{\mathsf T}$, changes no other cell, and its parallel calls touch disjoint cells. Each off-diagonal pair of cells of $D$ is swapped exactly once, and no cell on the diagonal is touched.

*Proof.* By induction on $n$. For $n = 1$, line L1 returns, and a $1 \times 1$ block is its own transpose. Let $n \ge 2$. By (1), $D^{\mathsf T}$ has the blocks $(D_{11})^{\mathsf T}$, $(D_{22})^{\mathsf T}$ on the diagonal, $(D_{21})^{\mathsf T}$ at the top right and $(D_{12})^{\mathsf T}$ at the bottom left. The calls of lines L3 and L4 transpose $D_{11}$ and $D_{22}$ by the induction hypothesis, and the call of line L5 swaps $D_{12}$ with $(D_{21})^{\mathsf T}$ by Lemma 1, because $D_{12}$ lies above the diagonal and $D_{21}$ below it, so they share no cell. The three calls touch the disjoint cell sets $D_{11}$, $D_{22}$ and $D_{12} \cup D_{21}$, so they have no [determinacy race](/determinacy-race/), and after the sync of line L6, $D = D^{\mathsf T}$.

For the count, an off-diagonal pair $\{(r, s), (s, r)\}$ with $r \ne s$ either lies inside $D_{11}$ or $D_{22}$, and is swapped once by the induction hypothesis, or has one cell in $D_{12}$ and one in $D_{21}$, and is swapped once by line L7 in the call of line L5. The diagonal cells lie in $D_{11}$ or $D_{22}$, so by induction they are never touched. $\blacksquare$

**Theorem 3 (any n).** The variant for any $n$, which splits $n$ into $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$ and swaps the $\lfloor n/2 \rfloor \times \lceil n/2 \rceil$ block at the top right with the transpose of the block at the bottom left by halving the longer side of the two blocks, is correct for the same reasons.

*Proof.* Identity (1) holds for any split of the rows and columns at the same index, since the transpose maps the cell $(r, s)$ to $(s, r)$. A $p \times q$ block $X$ split into a top part of $\lfloor p/2 \rfloor$ rows and the rest matches a split of the $q \times p$ block $Y^{\mathsf T}$ at the same rows, which is a split of $Y$ at the same columns. So each step of the swap pairs a part of $X$ with the matching part of $Y$, the parts are disjoint, and the induction on $p + q$ is the same as in Lemma 1. The induction for the transpose is the same as in Theorem 2. $\blacksquare$
