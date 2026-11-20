---
title: LINCS solves the linearised constraint equations by a convergent series, and its corrected fixed point is the SHAKE solution
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. There are $N$ atoms with inverse masses $w_i > 0$ and $C$ constraints $c = (i, j, d_c)$. From the old positions, $n_c$ is the unit vector of $x^{\text{old}}_i - x^{\text{old}}_j$. $B$ is the $C \times 3N$ matrix whose row $c$ has $n_c$ at atom $i$, $-n_c$ at atom $j$ and 0 elsewhere, $W$ is the diagonal matrix of inverse masses, and $S = \operatorname{diag}(1/\sqrt{w_i + w_j})$. For a position vector $x$, $(Bx)_c = n_c \cdot (x_i - x_j)$ is the length of bond $c$ along its old direction.

**Claim 1 (the matrix).** $B W B^{\mathsf T} = S^{-1} (I - A) S^{-1}$, where $A$ is symmetric with zero diagonal, and for $c \ne d$
$$A_{cd} = -\epsilon_c \epsilon_d \, w_a \, (n_c \cdot n_d) \, S_c S_d$$
if $c$ and $d$ share the atom $a$, with $\epsilon_c = +1$ if $a$ is the first atom of $c$ and $-1$ if it is the second, and $A_{cd} = 0$ if they share no atom. Lines L1 and L2 build these numbers.

*Proof.* $(B W B^{\mathsf T})_{cd} = \sum_a w_a B_{c,a} \cdot B_{d,a}$, a sum over atoms of the blocks of rows $c$ and $d$. For $c = d$ the two atoms give $w_i + w_j = S_c^{-2}$, since $|n_c| = 1$. For $c \ne d$ only a shared atom contributes, with $\epsilon_c \epsilon_d w_a n_c \cdot n_d$. Two constraints on the same pair of atoms would share two atoms; the code does not support that, and it is not a meaningful input. Then $S (B W B^{\mathsf T}) S = I - A$ with $A$ as stated, which is symmetric because the formula is. $\square$

**Claim 2 (one projection).** Line L5 maps $x$ to $x' = x - W B^{\mathsf T} \Lambda$ with $\Lambda = S \, \mathrm{sol}$, where $\mathrm{sol}$ is the output of line L4 for the right side of line L3. If line L4 returned $(I - A)^{-1}$ times its input exactly, then $B x' = p$, the target lengths.

*Proof.* Line L5 subtracts $w_i \Lambda_c n_c$ from $x_i$ and adds $w_j \Lambda_c n_c$ to $x_j$, which is $x - W B^{\mathsf T} \Lambda$. With an exact solve, $\Lambda = S (I - A)^{-1} S (Bx - p) = (B W B^{\mathsf T})^{-1} (Bx - p)$ by Claim 1, so $B x' = Bx - (Bx - p) = p$. $\square$

**Claim 3 (the series).** Let $\rho$ be the spectral radius of $A$. If $\rho < 1$, the output of line L4 with order $k$ differs from $(I - A)^{-1}$ times its input $y$ by at most $\frac{\rho^{k+1}}{1 - \rho} \|y\|_2$ in the 2-norm. If $\rho \ge 1$, the series does not converge for some inputs.

*Proof.* Line L4 returns $\sum_{t=0}^{k} A^t y$, and $(I - A)^{-1} - \sum_{t=0}^{k} A^t = A^{k+1} (I - A)^{-1}$ when $\rho < 1$. $A$ is symmetric, so $\|A\|_2 = \rho$ and $\|(I - A)^{-1}\|_2 \le 1/(1 - \rho)$. If $\rho \ge 1$, take $y$ an eigenvector for an eigenvalue $\pm\rho$: the terms $A^t y$ do not go to 0. $\square$

$I - A$ is positive definite, since it is $S B W B^{\mathsf T} S$ and $B$ has independent rows for the inputs we consider, so all eigenvalues of $A$ are below 1. So $\rho$ is close to 1 only if an eigenvalue is close to 1, which happens when the rows of $B$ are close to dependent, as in a ring, or if an eigenvalue is close to or below $-1$. For three equal masses in a triangle of three constraints, the test measures $\rho = 0.5$ for an equilateral triangle, $0.75$ at an angle of $120°$, $0.933$ at $150°$ and $0.992$ at $170°$. When the triangle becomes flat, the rows of $B$ become dependent, $B W B^{\mathsf T}$ becomes singular, and $\rho \to 1$.

**Claim 4 (the rotation correction).** Suppose that after a projection $B x = p$, and let $q_c$ be the part of the bond $x_i - x_j$ normal to $n_c$. Then $|x_i - x_j|^2 = p_c^2 + q_c^2$. Line L6 sets the new target $p_c = \sqrt{d_c^2 - q_c^2}$, so if the next projection does not change $q_c$, the bond has length exactly $d_c$ after it. If the corrections of line L6 converge to a point $x^\star$ with exact solves, then every bond of $x^\star$ has length $d_c$, and $x^\star = x^{\text{unc}} - W B^{\mathsf T} \Lambda^\star$ for some $\Lambda^\star$.

*Proof.* The first part is Pythagoras. At a fixed point the projection does not move $x^\star$, so by Claim 2 $(B x^\star)_c = p_c$, that is, the part of the bond along $n_c$ has length $\sqrt{d_c^2 - q_c^2}$, and its total length is $d_c$. Every projection adds a vector of the form $W B^{\mathsf T} \Lambda$, and a sum of such vectors has the same form. $\square$

The constraint forces of SHAKE also act along the old bond directions, so the SHAKE solution has the same form, and where the solution of that form is locally unique, the fixed point of LINCS is the SHAKE solution. The test checks this to $10^{-11}$ with order 16 and 4 corrections. With the usual settings, order 4 and one correction, the bonds hold to about $10^{-5}$ relative error for the chain of the test, a heuristic accuracy that depends on the step size.

**Claim 5 (centre of mass).** Each projection keeps $\sum_i m_i x_i$.

*Proof.* Line L5 changes it by $-m_i w_i \Lambda_c n_c + m_j w_j \Lambda_c n_c = 0$ for each constraint. $\square$

**Cost.** Lines L1 and L2 cost $\Theta(C + \sum_a \deg(a)^2)$, where $\deg(a)$ is the number of constraints on atom $a$, which is at most 4 in a molecule. Each projection costs $\Theta((k + 1) \cdot \mathrm{nnz}(A))$ for order $k$, with no loop that runs until convergence, so the cost of a step is known in advance and each constraint can be handled by a separate thread.
