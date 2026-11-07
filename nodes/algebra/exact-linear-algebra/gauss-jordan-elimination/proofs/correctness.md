---
title: Gauss-Jordan elimination returns the reduced row echelon form
proves: [correctness, termination]
status: full
---

Let $A_0$ be the input, an $m \times n$ matrix over a field $K$, and let $A$ be the working matrix. Indices start at $0$, as in the pseudocode. For $0 \le j \le n$, write $A_{<j}$ for the submatrix of $A$ in all rows and columns $0, \dots, j-1$.

**Claim.** GAUSS-JORDAN$(A_0)$ stops and returns the reduced row echelon form $E$ of $A_0$, its rank $r$, and the list $P$ of its pivot columns.

**Termination.** Line L2 runs $j$ over $n$ values. In each iteration, line L3 looks at most $m$ entries, and the loops of lines L6, L7 and L9 have at most $m$ and $n$ steps. So the algorithm stops after $O(mn \min(m, n) + mn)$ steps.

**Invariant.** At the start of the iteration of line L2 with index $j$:

- (I1) $A = T A_0$ for an invertible $m \times m$ matrix $T$.
- (I2) $r = |P|$, the list $P$ is increasing, and its entries are less than $j$.
- (I3) $A_{<j}$ is in reduced row echelon form, its pivot columns are the entries of $P$, and the rows $r, \dots, m-1$ of $A_{<j}$ are zero.

*Initialization.* For $j = 0$, $T = I$, $r = 0$ and $P$ is empty. The matrix $A_{<0}$ has no columns, so (I3) holds.

*Maintenance.* Assume the invariant at the start of iteration $j$.

If line L3 finds no row $i \ge r$ with $A[i, j] \ne 0$, then line L4 skips to the next column. Column $j$ is zero in the rows $r, \dots, m-1$, so the rows $r, \dots, m-1$ of $A_{<j+1}$ are zero. The rows $0, \dots, r-1$ of $A_{<j}$ already have their leading entries in the columns of $P$, so column $j$ adds no new leading entry. Hence $A_{<j+1}$ is in reduced row echelon form with the same pivot columns, and (I1) to (I3) hold for $j + 1$.

Otherwise line L5 swaps rows $r$ and $p$, line L6 divides row $r$ by the nonzero $c = A[r, j]$, and lines L7 to L9 subtract $f = A[i, j]$ times row $r$ from every other row $i$. Each of these steps multiplies $A$ on the left by an invertible elementary matrix, so (I1) holds after the iteration. By (I3), row $r$ is zero in the columns $0, \dots, j-1$ before the iteration, because $r$ is one of the zero rows of $A_{<j}$, and row $p \ge r$ is zero there too. So the code changes nothing in the columns less than $j$ when it updates only the columns $t \ge j$: the skipped updates subtract a multiple of $0$. After the iteration:

- Column $j$ is the unit vector $e_r$. Row $r$ has $A[r, j] = c / c = 1$, and each row $i \ne r$ has $A[i, j] - f \cdot 1 = 0$.
- The columns of $P$ do not change, because row $r$ is zero in them. So they are still unit vectors $e_0, \dots, e_{r-1}$.
- Row $r$ is zero in the columns less than $j$ and has the entry $1$ in column $j$. Its leading entry is in column $j$, to the right of the leading entries of the rows $0, \dots, r-1$, which are in the columns of $P$, all less than $j$.
- The rows $r+1, \dots, m-1$ are zero in the columns $0, \dots, j-1$ and now in column $j$ too.

Line L10 appends $j$ to $P$ and increments $r$. So $A_{<j+1}$ is in reduced row echelon form with pivot columns $P$, its rows $r, \dots, m-1$ are zero, and (I2) and (I3) hold for $j + 1$.

*End.* The loop ends with $j = n$. By (I3), $A = A_{<n}$ is in reduced row echelon form, with pivot columns $P$ and exactly $r$ nonzero rows. By (I1), $A = T A_0$ with $T$ invertible, so $A$ and $A_0$ have the same row space: each row of $A$ is a combination of the rows of $A_0$, and each row of $A_0 = T^{-1} A$ is a combination of the rows of $A$. A matrix in reduced row echelon form is determined by its row space (the uniqueness theorem on the [echelon form](/echelon-form/) page), so $A$ is the reduced row echelon form of $A_0$. Its nonzero rows are linearly independent, so $r$ is the rank of $A_0$. Line L11 returns $A$, $r$ and $P$. $\blacksquare$

**The inverse.** Let $A_0$ be $n \times n$ and run the algorithm on $[A_0 \mid I]$. The algorithm handles the columns from left to right, and the decisions in the first $n$ columns depend only on those columns, so the pivots among $0, \dots, n-1$ are the pivots of $A_0$. If $A_0$ is invertible, its rank is $n$, so the pivots are exactly $0, \dots, n-1$. Then the result is $T [A_0 \mid I] = [T A_0 \mid T]$, and its left half is a reduced row echelon form with $n$ pivots in $n$ columns, which is $I$. So $T A_0 = I$ and the right half $T$ is $A_0^{-1}$. If $A_0$ is singular, its rank is less than $n$, so some column less than $n$ is not a pivot, and INVERSE returns NONE. $\blacksquare$

**The solution.** Run the algorithm on $[A_0 \mid b]$ and get $[E \mid c]$ with $E = T A_0$ and $c = T b$. The systems $A_0 x = b$ and $E x = c$ have the same solutions, since $T$ is invertible. If column $n$ is a pivot, then some row of $[E \mid c]$ is $(0, \dots, 0, 1)$, which is the equation $0 = 1$, so there is no solution. Otherwise, the rows $r, \dots, m-1$ are zero, and row $i < r$ is the equation $x_{P_i} + \sum_{t \notin P} E[i, t]\, x_t = c_i$. With the free variables $x_t = 0$ for $t \notin P$, this gives $x_{P_i} = c_i$, which is what SOLVE returns. $\blacksquare$
