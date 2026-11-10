---
title: The three parallel matrix products compute C = AB with no determinacy race
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be $n \times n$ matrices over a ring (the tests use the integers), and let $C = AB$, so $c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$. For the two recursive products $n$ is a power of 2. We use the line numbers of the pseudocode on the page.

**Lemma 1 (block product).** Split $A$, $B$ and $C$ into four $n/2 \times n/2$ blocks, with $A_{ik}$ the block in block row $i$ and block column $k$. Then $C_{ij} = A_{i1} B_{1j} + A_{i2} B_{2j}$ for $i, j \in \{1, 2\}$.

*Proof.* Take an entry $c_{rs}$ in block $C_{ij}$. Its sum over $k = 1, \ldots, n$ splits into the terms with $k \le n/2$ and those with $k > n/2$. The first part runs over row $r$ of $A_{i1}$ and column $s$ of $B_{1j}$, so it is the entry of $A_{i1} B_{1j}$ at the same place, and the second part is the entry of $A_{i2} B_{2j}$. $\blacksquare$

**Theorem 2 (the parallel loops).** The loop product writes $c_{ij} = \sum_k a_{ik} b_{kj}$ for each $i$ and $j$, and its parallel iterations have no race.

*Proof.* The iteration $(i, j)$ reads row $i$ of $A$ and column $j$ of $B$, which no iteration writes, and it writes only $c_{ij}$, with its own sum in a local variable. Different iterations write different cells. So each iteration computes its sum as a sequential loop would, and the order of the iterations does not matter. $\blacksquare$

**Theorem 3 (with a temporary matrix).** P-MATRIX-MULTIPLY-RECURSIVE ends and sets $C$ to $AB$, and its parallel calls have no race.

*Proof.* By induction on $n$. For $n = 1$, line L2 sets $c_{11} = a_{11} b_{11}$. Let $n \ge 2$. The calls of lines L5 and L6 have size $n/2$, so they end, and by the induction hypothesis they set $C_{ij} = A_{i1} B_{1j}$ and $T_{ij} = A_{i2} B_{2j}$. The eight calls only read $A$ and $B$. Each writes its own block: four distinct blocks of $C$ and four distinct blocks of the new matrix $T$, which no other call can reach. So no two of them write the same cell, and none writes a cell that another reads. After the sync of line L7, lines L8 to L10 add $T$ into $C$ entry by entry, each iteration on its own cell, which gives $C_{ij} = A_{i1} B_{1j} + A_{i2} B_{2j}$. This is $(AB)_{ij}$ by Lemma 1. $\blacksquare$

**Theorem 4 (with no temporary matrix).** P-MATRIX-MULTIPLY-ADD ends and adds $AB$ to $C$, and its parallel calls have no race.

*Proof.* By induction on $n$; the case $n = 1$ is line 1. Let $n \ge 2$, and let $C^0$ be the value of $C$ at the start. The four calls of line 3 add $A_{i1} B_{1j}$ to $C_{ij}$, one call for each of the four blocks. They read $A$, $B$ and their own block of $C$, and write only their own block, so they have no race, and after the sync of line 4, $C_{ij} = C^0_{ij} + A_{i1} B_{1j}$. In the same way the calls of line 5 add $A_{i2} B_{2j}$, so after line 6, $C_{ij} = C^0_{ij} + A_{i1} B_{1j} + A_{i2} B_{2j}$, which is $C^0_{ij} + (AB)_{ij}$ by Lemma 1. The two phases are separated by a sync, so the two calls that write the same block $C_{ij}$ never run at the same time. Started with $C = 0$, the procedure sets $C$ to $AB$. $\blacksquare$
