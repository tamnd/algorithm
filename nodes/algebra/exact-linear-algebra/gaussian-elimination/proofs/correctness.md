---
title: Gaussian elimination returns an echelon form, the rank and the pivot columns
proves: [correctness, termination]
status: full
---

Let $A_0$ be the input, an $m \times n$ matrix over a field $K$, and let $A$ be the working matrix. Rows and columns are indexed from $0$, as in the pseudocode.

**Claim.** GAUSSIAN-ELIMINATION$(A_0)$ stops after $n$ iterations of line L2 and returns $(E, r, P)$ such that $E = U A_0$ for an invertible $m \times m$ matrix $U$, $E$ is in [echelon form](/echelon-form/) with exactly $r$ nonzero rows, and $P = (P_0, \dots, P_{r-1})$ lists the column of the leading entry of rows $0, \dots, r-1$ of $E$. Hence $r = \operatorname{rank} A_0$ and $P$ is the column rank profile of $A_0$.

**Termination.** Line L2 runs $j$ over the $n$ values $0, \dots, n-1$. Lines L3 and L6 to L8 are loops over at most $m$ and $n$ values. So the algorithm stops.

**Invariant.** At the start of the iteration of line L2 with column $j$ (and at the end, with $j = n$):

- **(G1)** $A = U A_0$ for some invertible matrix $U$.
- **(G2)** $P$ has $r$ entries, $P_0 < P_1 < \cdots < P_{r-1} < j$, and for each $k < r$, row $k$ of $A$ has $A[k, P_k] \ne 0$ and $A[k, t] = 0$ for all $t < P_k$.
- **(G3)** For each row $i \ge r$ and each column $t < j$, $A[i, t] = 0$.

*Initialization.* For $j = 0$, $r = 0$ and $P$ is empty. (G1) holds with $U = I$, and (G2) and (G3) hold because there is no row $k < 0$ and no column $t < 0$.

*Maintenance.* Assume (G1) to (G3) at the start of the iteration for column $j$.

Case 1: line L3 finds no row $p \ge r$ with $A[p, j] \ne 0$. Then column $j$ is zero in rows $r, \dots, m-1$. Together with (G3) for columns $t < j$, this gives (G3) for columns $t < j+1$. Nothing else changes, so (G1) and (G2) hold for $j + 1$.

Case 2: line L3 finds $p \ge r$ with $A[p, j] \ne 0$. Line L5 swaps rows $r$ and $p$. Both rows have index at least $r$, so (G2) is not affected, and by (G3) both rows are zero in columns $t < j$. Now $A[r, j] \ne 0$. For each $i > r$, lines L7 and L8 subtract $f = A[i, j]/A[r, j]$ times row $r$ from row $i$. A row swap and the addition of a multiple of one row to another are left multiplications by invertible elementary matrices, so (G1) still holds. Line L8 changes only columns $t \ge j$, which is enough, because row $r$ is zero in columns $t < j$. After the update, $A[i, j] = A[i, j] - (A[i, j]/A[r, j]) A[r, j] = 0$. Rows $0, \dots, r-1$ do not change. So after the loop of line L6:

- row $r$ is zero in columns $t < j$ and $A[r, j] \ne 0$, so its leading column is $j$, and $j > P_{r-1}$ by (G2);
- each row $i > r$ is zero in columns $t < j$ (it was before, and those columns did not change) and in column $j$.

Line L9 appends $j$ to $P$ and line L10 adds $1$ to $r$. With the new values, (G2) holds by the first point, and (G3) holds for columns $t < j + 1$ by the second point.

*End.* At the end, $j = n$. By (G3), each row $i \ge r$ is zero in all $n$ columns. By (G2), rows $0, \dots, r-1$ are nonzero and their leading columns $P_0 < \cdots < P_{r-1}$ increase. This is the definition of echelon form with $r$ nonzero rows, and by (G1) the result is an echelon form of $A_0$. The theorem on the [echelon form](/echelon-form/) page shows that the number of nonzero rows and the pivot columns of any echelon form of $A_0$ are the rank and the column rank profile of $A_0$. $\blacksquare$

**Lemma (SOLVE).** SOLVE$(A_0, b)$ returns a vector $x$ with $A_0 x = b$ when one exists, and reports that there is no solution otherwise.

*Proof.* Let $(E, r, P)$ be the result of the elimination of the augmented matrix $[A_0 \mid b]$, which has $n + 1$ columns. By (G1), $[E \mid c] = U [A_0 \mid b]$ with $U$ invertible, where $c$ is the last column of the result. So $A_0 x = b$ holds exactly when $E' x = c$ holds, where $E'$ is the first $n$ columns. This is because $U$ and $U^{-1}$ both map the residual $A_0 x - b$ to $E' x - c$ and back.

If the last pivot column is $n$, the column of $b$, then row $r - 1$ is zero in columns $0, \dots, n-1$ and has $c_{r-1} \ne 0$. Its equation reads $0 = c_{r-1}$, so there is no solution.

Otherwise all pivots lie in columns $0, \dots, n-1$. Rows $r, \dots, m-1$ are zero including column $n$, so their equations read $0 = 0$. Back substitution sets each free variable (a column not in $P$) to $0$ and visits the pivot rows $k = r-1, r-2, \dots, 0$. Row $k$ reads $\sum_{t \ge P_k} E[k, t] x_t = c_k$, because the entries left of $P_k$ are zero. When row $k$ is visited, each $x_t$ with $t > P_k$ already has its final value: a free variable is $0$, and a pivot variable $x_{P_{k'}}$ with $P_{k'} > P_k$ has $k' > k$, so it was set earlier. The algorithm sets $x_{P_k} = (c_k - \sum_{t > P_k} E[k, t] x_t)/E[k, P_k]$, which is defined since $E[k, P_k] \ne 0$ and makes equation $k$ true. Later steps change only $x_t$ with $t < P_k$, which do not occur in equation $k$. So at the end each equation of $E' x = c$ holds, and $A_0 x = b$. $\blacksquare$
