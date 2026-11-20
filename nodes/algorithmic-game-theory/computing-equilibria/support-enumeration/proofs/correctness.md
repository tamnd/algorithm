---
title: Support enumeration outputs only equilibria, and all of them in a nondegenerate game
proves: [correctness]
status: full
---

Let $(A, B)$ be an $m \times n$ bimatrix game. For a mixed strategy $y$ of the column player write $(Ay)_i$ for the payoff of row $i$, and for $x$ write $(x^{\mathsf T} B)_j$ for the payoff of column $j$. The game is nondegenerate if no mixed strategy with $k$ strategies in its support has more than $k$ pure best responses.

**Lemma 1 (best response fact).** $x$ is a best response to $y$ if and only if every $i$ with $x_i > 0$ satisfies $(Ay)_i = \max_r (Ay)_r$.

*Proof.* $x^{\mathsf T} A y = \sum_i x_i (Ay)_i$ is an average of the numbers $(Ay)_i$ with weights $x_i$. It equals the maximum $\max_r (Ay)_r$, which is the most any mixed strategy can earn, if and only if all weight is on rows that reach the maximum. $\square$

**Theorem 1 (soundness).** Every pair $(x, y)$ output at line L8 is a Nash equilibrium.

*Proof.* By line L3, $y_j > 0$ for $j \in J$ (line L5), $y_j = 0$ for $j \notin J$ (line L6), and $\sum_j y_j = 1$, so $y \in \Delta_n$; in the same way $x \in \Delta_m$ with support $I$. By line L3, $(Ay)_i = \sum_{j \in J} A_{ij} y_j = u$ for each $i \in I$, and by line L7, $(Ay)_r \le u$ for each row $r$. So $\max_r (Ay)_r = u$, and every row of the support of $x$ reaches it. By Lemma 1, $x$ is a best response to $y$. Lines L4 and L7 give the same for $y$ against $x$. $\square$

**Lemma 2 (equal supports).** In a nondegenerate game every Nash equilibrium $(x, y)$ has $|\operatorname{supp}(x)| = |\operatorname{supp}(y)|$.

*Proof.* By Lemma 1 every column of $\operatorname{supp}(y)$ is a pure best response to $x$, so $x$ has at least $|\operatorname{supp}(y)|$ pure best responses, and nondegeneracy gives $|\operatorname{supp}(y)| \le |\operatorname{supp}(x)|$. Swap the players for the other inequality. $\square$

**Lemma 3 (unique solution).** Let the game be nondegenerate, let $(x, y)$ be an equilibrium with supports $I$ and $J$, $|I| = |J| = k$, and let $u = \max_r (Ay)_r$. Then $(y_J, u)$ is the only solution of the system $S$ of line L3: $\sum_{j \in J} A_{ij} z_j = t$ for $i \in I$ and $\sum_{j \in J} z_j = 1$, in the unknowns $z \in \mathbb{R}^J$ and $t$.

*Proof.* $(y_J, u)$ solves $S$ by Lemma 1. Suppose that $S$ has a second solution. Then the solutions form an affine set of dimension at least 1, and it contains a line $(y_J, u) + \lambda (d, \delta)$ with $(d, \delta) \ne 0$. Here $\sum_j d_j = 0$, and $d \ne 0$, because $d = 0$ forces $\delta = 0$ by the equations. Extend $z$ by 0 outside $J$ and set $z(\lambda) = y + \lambda d$.

At $\lambda = 0$, the rows outside $I$ earn strictly less than $u$: otherwise $y$, with support size $k$, would have more than $k$ pure best responses. Also $y_j > 0$ for $j \in J$. Since $d$ has a negative entry, $z(\lambda)_j$ becomes 0 for some $j \in J$ at a finite $\lambda > 0$. Let $\lambda^* > 0$ be the first value at which a coordinate $z_j$ with $j \in J$ reaches 0 or a row $r \notin I$ reaches $(A z)_r = t$. For $0 \le \lambda \le \lambda^*$, $z(\lambda)$ is a distribution on $J$, the rows of $I$ all earn $t(\lambda) = u + \lambda \delta$, and the rows outside $I$ earn at most $t(\lambda)$, so all rows of $I$ are pure best responses to $z(\lambda)$.

At $\lambda^*$, in the first case the support of $z(\lambda^*)$ has at most $k - 1$ elements and $z(\lambda^*)$ has at least $k$ pure best responses (the rows of $I$). In the second case the support has at most $k$ elements and there are at least $k + 1$ pure best responses. Both contradict nondegeneracy. $\square$

**Theorem 2 (completeness).** In a nondegenerate game, every Nash equilibrium is output.

*Proof.* Let $(x, y)$ be an equilibrium with supports $I$ and $J$. By Lemma 2, $|I| = |J| = k$ with $1 \le k \le \min(m, n)$, so lines L1 and L2 reach the pair $(I, J)$. By Lemma 3 the square system of line L3 has a unique solution, so its matrix is nonsingular, and the solver returns $(y_J, u)$. The same lemma with the players swapped shows that line L4 returns $(x_I, v)$ with $v = \max_c (x^{\mathsf T} B)_c$. All these entries are positive, so line L5 does not skip the pair. Line L6 rebuilds $x$ and $y$, and line L7 holds because $u$ and $v$ are the maximal payoffs. So line L8 outputs $(x, y)$. $\square$

**Termination.** There are finitely many pairs $(I, J)$, and each step does a finite amount of work, so the method ends. Each equilibrium is output at most once, because the pair $(I, J)$ is its pair of supports.
