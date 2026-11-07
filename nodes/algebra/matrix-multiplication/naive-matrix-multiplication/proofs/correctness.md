---
title: The triple loop computes the matrix product
proves: [correctness, termination]
status: full
---

Let $R$ be a ring, or more generally a semiring: a set with an associative addition that has a neutral element $0$, and a multiplication. Commutativity of the multiplication is not used. Let $A$ be an $n \times m$ matrix and $B$ an $m \times p$ matrix over $R$, with $n, m, p \ge 0$.

**Claim.** MATRIX-MULTIPLY$(A, B)$ stops, and it returns the $n \times p$ matrix $C$ with $C[i][j] = \sum_{k=0}^{m-1} A[i][k] B[k][j]$ for all $0 \le i < n$ and $0 \le j < p$. The sum is taken in the order $k = 0, 1, \ldots, m-1$, and it is $0$ when $m = 0$.

**Termination.** Each of the three loops of lines L2, L3 and L5 runs over a fixed finite range, and the body changes none of the loop variables. So line L6 runs exactly $nmp$ times and the procedure stops.

**Step 1 (the inner loop).** Fix $i$ and $j$. We show that each time the test of line L5 runs with the value $k$, this invariant holds:

> **(S)** $s = \sum_{t=0}^{k-1} A[i][t] \, B[t][j]$.

*Initialization.* Line L4 sets $s = 0$ and the first test has $k = 0$. The sum over the empty range is $0$, so (S) holds.

*Maintenance.* Assume (S) holds for $k < m$. Line L6 sets $s$ to $\sum_{t=0}^{k-1} A[i][t] B[t][j] + A[i][k] B[k][j] = \sum_{t=0}^{k} A[i][t] B[t][j]$, by associativity of addition. The next test has the value $k + 1$, so (S) holds again.

*Termination.* The loop exits at the test with $k = m$. By (S), $s = \sum_{t=0}^{m-1} A[i][t] B[t][j]$, which is the claimed value of $C[i][j]$.

**Step 2 (the outer loops).** Line L7 then writes this value into $C[i][j]$. Lines L2 and L3 run the body once for each pair $(i, j)$ with $0 \le i < n$ and $0 \le j < p$, and line L7 for the pair $(i, j)$ is the only write to $C[i][j]$. The computation of the pair $(i, j)$ reads only $A$ and $B$, which the procedure never writes, and $C$ is a new matrix that shares no memory with them. So no later step changes $C[i][j]$, and after the loops each entry has its claimed value. Line L8 returns $C$. $\blacksquare$

**Remark (loop orders).** In any of the six orders of the three loops, with $C$ set to $0$ at the start and the update $C[i][j] \leftarrow C[i][j] + A[i][k] B[k][j]$ as the body, the triples $(i, j, k)$ with fixed $(i, j)$ are visited in increasing order of $k$ in the orders $ijk$, $jik$, $ikj$, $jki$, $kij$ and $kji$, since $k$ is either the inner loop or an outer loop. So the same argument, applied to each fixed $(i, j)$, shows that all six orders return the same matrix, even when addition is not commutative.
