---
title: Row by row Givens QR gives the least squares step of square root SAM, for every column order
proves: [correctness]
status: full
---

**Setting.** $A$ is a real $M \times n$ matrix with rank $n$, and $b \in \mathbb{R}^M$. The rows of $[A \mid b]$ are processed one at a time by lines L9 to L14. A stored row with the pivot $c$ has zeros in all columns before $c$. A Givens rotation of two rows $p$ and $a$ that both start at column $c$, with $h = \sqrt{p_c^2 + a_c^2}$, $\cos = p_c / h$ and $\sin = a_c / h$, replaces them by $\cos\, p + \sin\, a$ and $-\sin\, p + \cos\, a$. The column $b$ is rotated with the rest of the row.

**Assumptions.**

- (A1) Exact arithmetic. (The code drops entries below $10^{-14} h$ after a rotation, which is rounding noise.)
- (A2) $A$ has full column rank, which the prior on the first pose ensures in the tests.

**Claim 1.** When line L14 is reached, the stored rows form an upper triangular $n \times n$ matrix $R$ with a nonzero diagonal, a vector $d$, and a vector $e$ of the right sides of the rows that became zero, such that there is an orthogonal $Q$ with

$$Q^\top [A \mid b] = \begin{bmatrix} R & d \\ 0 & e \end{bmatrix}.$$

*Proof.* Keep the invariant: the stored rows, the zero rows found so far and the rows not yet processed together equal $Q_k^\top [A \mid b]$ for an orthogonal $Q_k$, up to the order of the rows. At the start $Q_0 = I$. Installing a row at line L12 does not change the set of rows. A Givens rotation acts on two rows with an orthogonal $2 \times 2$ matrix, so the invariant holds with $Q_{k+1}^\top = G Q_k^\top$. A rotation sets the entry of the new row at column $c$ to $-\sin p_c + \cos a_c = (-a_c p_c + p_c a_c)/h = 0$, and the rows have no entry before $c$, so the leading column of the new row moves strictly to the right. Hence each row is rotated at most $n$ times and is then installed or becomes zero, and the algorithm ends. Each stored row has its pivot $c$ as its first nonzero entry, and there is at most one stored row per pivot, so the stored rows sorted by pivot form an upper triangular matrix with nonzero diagonal entries. By (A2) the rank of $A$ is $n$, and orthogonal transforms keep the rank, so all $n$ pivots are present. $\square$

**Claim 2.** The solution $\delta$ of $R \delta = d$ by back substitution is the unique minimizer of $\|A\delta - b\|^2$.

*Proof.* Orthogonal matrices keep the norm, so by Claim 1,

$$\|A\delta - b\|^2 = \|Q^\top (A\delta - b)\|^2 = \|R\delta - d\|^2 + \|e\|^2.$$

The second term does not depend on $\delta$, and the first is zero exactly when $R\delta = d$. $R$ is triangular with a nonzero diagonal, so back substitution finds this unique $\delta$. $\square$

It also follows that $R^\top R = A^\top A$, so $R$ is the Cholesky factor of $A^\top A$ up to the signs of its rows. The test checks this against a separate [Cholesky decomposition](/cholesky-decomposition/).

**Claim 3 (the column order).** Let $P$ be a permutation matrix of the columns. The step computed with the columns in the order $P$ is $P$ applied to the step computed in the natural order.

*Proof.* With the permuted columns the matrix is $A P$. The minimizer of $\|A P \gamma - b\|^2$ is $\gamma = P^\top \delta$, because $\delta \mapsto P^\top \delta$ is a bijection and $\|A P (P^\top \delta) - b\| = \|A\delta - b\|$. By Claim 2 the code finds this unique minimizer, so the variables get the same values. $\square$

The column order therefore changes only the number of nonzero entries of $R$ and the number of rotations, never the result. The test runs three orders and gets the same solution within $10^{-8}$.

**Claim 4 (the Gauss-Newton loop).** If lines L2 to L7 reach a step $\delta = 0$, the gradient of the cost $\sum \|e_f / \sigma_f\|^2$ at the estimate is zero.

*Proof.* $A$ is the whitened Jacobian and $b$ is minus the whitened error, so the gradient of the cost is $-2 A^\top b$. By Claim 2, $\delta$ solves the normal equations $A^\top A \delta = A^\top b$. If $\delta = 0$, then $A^\top b = 0$. $\square$

**What this does not show.** The loop is Gauss-Newton. It converges only near a minimum, the cost is not convex, and the minimum it reaches can be local. The claims say nothing about how much fill-in an order causes; minimum degree is a heuristic.
