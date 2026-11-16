---
title: After each iSAM update, R is the triangular factor of the whitened system of all factors, and delta is its least squares solution
proves: [correctness]
status: full
---

**Setting.** The variables have a column order. At the linearization point $\theta$, each factor gives whitened rows $[a \mid \beta]$, where $a$ is a row of the Jacobian divided by the standard deviation and $\beta = -e / \sigma$. Stack the rows of all factors so far into $[A \mid b]$. The solver keeps a map from a pivot column $c$ to a row $R_c$ with the right side $d_c$. Let $R$ be the matrix with the rows $R_c$ in the order of $c$, and $d$ the vector of the $d_c$.

The invariant is:

- (I1) every row $R_c$ is zero in the columns before $c$, and $(R_c)_c \neq 0$;
- (I2) $R^\top R = A^\top A$ and $R^\top d = A^\top b$.

**Assumptions.**

- (A1) Exact arithmetic. The code drops entries below $10^{-14}$ times the pivot, which is a rounding of zero.
- (A2) After each update, every column has a pivot row. If not, the code raises an error, because $A$ then has a column that no measurement constrains in the current order and $A^\top A$ is singular.

**Lemma 1 (one row).** Let (I1) hold, and let $S = R^\top R$, $s = R^\top d$ before ROTATE-IN of the row $[a \mid \beta]$. After it, (I1) holds, and $R^\top R = S + a^\top a$ and $R^\top d = s + a^\top \beta$.

*Proof.* Consider the augmented rows $[R_c \mid d_c]$ and $[a \mid \beta]$. The sum of the outer products $\sum_c [R_c \mid d_c]^\top [R_c \mid d_c] + [a \mid \beta]^\top [a \mid \beta]$ has $S + a^\top a$ in the top left block and $s + a^\top \beta$ in the top right block. Line L7 replaces the two rows $u = [R_c \mid d_c]$ and $w = [a \mid \beta]$ by $G (u, w)$ with $G = \begin{bmatrix} \cos\phi & \sin\phi \\ -\sin\phi & \cos\phi \end{bmatrix}$, and $G^\top G = I$, so $u^\top u + w^\top w$ does not change. With $\cos\phi = (R_c)_c / h$, $\sin\phi = a_c / h$ and $h = \sqrt{(R_c)_c^2 + a_c^2}$, the new $(R_c)_c$ is $h \neq 0$ and the new $a_c$ is $0$. Both rows were zero before column $c$ (the row $a$ because $c$ is its leading column, line L5), so they stay zero there, and the leading column of $a$ moves strictly to the right. So the loop of line L4 ends. It ends in one of two ways. At line L6, $a$ becomes the row of a column $c$ with no pivot; its leading column is $c$ and $a_c \neq 0$, so (I1) holds, and the sum of outer products now counts $a$ in $R$. Or $a$ has no nonzero entry left except $\beta$; then $[0 \mid \beta]^\top [0 \mid \beta]$ is zero outside the bottom right corner, so dropping the row does not change the two blocks. In both cases, the top left and top right blocks of the sum over the rows of $R$ are $S + a^\top a$ and $s + a^\top \beta$. $\square$

**Claim 1 (the incremental step keeps the invariant).** If (I1) and (I2) hold before an update without a batch step, they hold after it for the system with the new factors.

*Proof.* Line L1 appends the columns of the new variables at the end of the order. The old rows of $A$ and of $R$ are zero in the new columns, because no old factor involves a new variable, so (I1) and (I2) still hold for the extended matrices. The old variables keep their linearization point, and the new variables are linearized at their initial values, so the rows of the new factors at line L2 are exactly the new rows of $A$ and $b$. By Lemma 1, applied once per new row at line L3, $R^\top R = A^\top A + \sum a^\top a$ and $R^\top d = A^\top b + \sum a^\top \beta$, which are the blocks of the new system. $\square$

**Claim 2 (the batch step keeps the invariant).** After lines L9 and L10, (I1) and (I2) hold for the system of all factors at the new linearization point and in the new order.

*Proof.* Line L9 sets $\theta$ to the current estimate and fixes the new order. Line L10 starts with an empty $R$, for which (I1) and (I2) hold for an empty system, and rotates in every row of every factor at the new $\theta$ in the new order. By Lemma 1 and induction over the rows, the invariant holds for all of them. $\square$

**Claim 3 (the solution).** After line L11, $\delta$ is the unique minimizer of $\|A\delta - b\|^2$, the Gauss-Newton step from $\theta$ for all factors.

*Proof.* By (A2) and (I1), $R$ is square and upper triangular with nonzero diagonal entries, so it is invertible and line L11 finds the unique $\delta$ with $R\delta = d$. Then $A^\top A \delta = R^\top R \delta = R^\top d = A^\top b$ by (I2). These are the normal equations, and $A^\top A = R^\top R$ is positive definite, so $\delta$ is the unique minimizer. $\square$

**Corollary.** With the batch period $k = 1$, each update is one Gauss-Newton step on all factors, from the current estimate. Without batch steps, the estimate $\theta + \delta$ is the minimizer of the linear system at the first linearization point of each variable. The tests check (I1) and (I2) and the normal equations against dense products, with and without batch steps.

**What this does not show.** Between batch steps, iSAM does not relinearize, so the estimate is a Gauss-Newton step from a point that can be old. It is not a stationary point of the nonlinear cost in general. The number of Givens rotations and the fill-in of $R$ depend on the column order; nothing here bounds them. Appending new variables at the end of an order that was chosen earlier can make $R$ dense, which the periodic reordering is there to undo.
