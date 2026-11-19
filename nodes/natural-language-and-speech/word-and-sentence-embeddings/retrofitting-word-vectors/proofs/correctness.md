---
title: Retrofitting converges to the unique fixed point of its update, and with symmetric weights that point minimizes the objective
proves: [correctness, termination]
status: full
---

The loop of lines L2 to L4 runs exactly $T$ sweeps, so it terminates. We prove that the sweeps converge, as $T$ grows, to one fixed point, with a geometric rate, whatever the order of the words; that words without neighbours never change; and that with symmetric weights the fixed point is the unique minimizer of the objective $\Psi$.

**Setup.** Let $U$ be the set of words with at least one neighbour in the vocabulary (the words line L3 visits), with $N(i) \subseteq V \setminus \{i\}$ the neighbours of $i$. Words in $V \setminus U$ are never written, so they keep $\vec q_j = \hat{\vec q}_j$ at all times. The update of line L4 acts on each coordinate of the vectors separately and in the same way, so it is enough to prove the claims for one coordinate; write $x_i$ for that coordinate of $\vec q_i$ and $\hat x_i$ for that of $\hat{\vec q}_i$. For $i \in U$ let $s_i = \sum_{j \in N(i)} \beta_{ij} > 0$ and $c_{ij} = \beta_{ij}/(\alpha_i + s_i) \ge 0$. Line L4 is

$$x_i \leftarrow \sum_{j \in N(i)} c_{ij} x_j + \frac{\alpha_i}{\alpha_i + s_i} \hat x_i, \qquad \sum_{j \in N(i)} c_{ij} = \frac{s_i}{\alpha_i + s_i} =: \rho_i < 1,$$

since $\alpha_i > 0$. Let $\rho = \max_{i \in U} \rho_i < 1$. With $\alpha_i = 1$ and $\beta_{ij} = 1/|N(i)|$, $s_i = 1$ and $\rho = 1/2$.

## Step 1. There is exactly one fixed point.

A fixed point is a vector $x^*$ on $U$ with $x^*_i = \sum_j c_{ij} x^*_j + \frac{\alpha_i}{\alpha_i + s_i}\hat x_i$ for all $i \in U$, where $x^*_j = \hat x_j$ for $j \notin U$. Multiplying by $\alpha_i + s_i$, this is the linear system $A x^* = b$ with $A_{ii} = \alpha_i + s_i$, $A_{ij} = -\beta_{ij}$ for $j \in N(i) \cap U$, $A_{ij} = 0$ otherwise, and $b_i = \alpha_i \hat x_i + \sum_{j \in N(i) \setminus U} \beta_{ij} \hat x_j$. In row $i$, $\sum_{j \ne i} |A_{ij}| \le s_i < \alpha_i + s_i = A_{ii}$, so $A$ is strictly diagonally dominant by rows. Such a matrix is nonsingular: if $A y = 0$ with $y \ne 0$, pick $i$ with $|y_i| = \|y\|_\infty > 0$; then $A_{ii}|y_i| = |\sum_{j \ne i} A_{ij} y_j| \le \sum_{j \ne i}|A_{ij}|\,|y_i| < A_{ii}|y_i|$, a contradiction. So the system has exactly one solution $x^*$. $\square$

## Step 2. A Jacobi sweep shrinks the error by the factor $\rho$.

Let $e = x - x^*$ on $U$, and $e_j = 0$ for $j \notin U$ (those words are fixed at $\hat x_j = x^*_j$). A Jacobi sweep computes every new $x_i$ from the old vector. Subtracting the fixed point equation from the update gives $e'_i = \sum_{j \in N(i)} c_{ij} e_j$, so

$$|e'_i| \le \sum_{j} c_{ij} |e_j| \le \rho_i \|e\|_\infty \le \rho \|e\|_\infty.$$

Hence $\|e'\|_\infty \le \rho \|e\|_\infty$. $\square$

## Step 3. A Gauss-Seidel sweep, in any order, shrinks the error by at least the factor $\rho$.

A Gauss-Seidel sweep visits the words of $U$ in some order $i_1, i_2, \ldots$ and writes each new value at once. Let $E = \|e\|_\infty$ at the start of the sweep. We show by induction on $m$ that after the $m$-th update every entry of the error is at most $E$ in absolute value, and the entries already updated in this sweep are at most $\rho E$.

*Base.* Before the first update, all entries are at most $E$, and no entry is updated.

*Step.* Assume the hypothesis after $m - 1$ updates. The update of $i_m$ gives $e'_{i_m} = \sum_j c_{i_m j} e_j$ with the current errors, each at most $E$ in absolute value by the hypothesis, so $|e'_{i_m}| \le \rho_{i_m} E \le \rho E \le E$. The other entries do not change. So the hypothesis holds after $m$ updates.

At the end of the sweep every word of $U$ has been updated once, so $\|e'\|_\infty \le \rho E$. $\square$

## Step 4. Convergence.

By Steps 2 and 3, after $T$ sweeps of either kind, $\|x^{(T)} - x^*\|_\infty \le \rho^T \|\hat x - x^*\|_\infty$, since the start is $x^{(0)} = \hat x$ (line L1). As $\rho < 1$, the sweeps converge to $x^*$, whatever the order of the words, and the limit is the unique fixed point of Step 1. Applying this to every coordinate gives the claim for the vectors, in the max norm over all words and coordinates. Words in $V \setminus U$ keep their original vectors at every step, by the setup. $\square$

## Step 5. With symmetric weights the fixed point minimizes $\Psi$.

Assume now that the lexicon is symmetric ($j \in N(i)$ if and only if $i \in N(j)$), that $\beta_{ij} = \beta_{ji} = w_{ij} > 0$, and that each unordered edge is counted once:

$$\Psi(Q) = \sum_{i \in V} \alpha_i \|\vec q_i - \hat{\vec q}_i\|^2 + \sum_{\{i, j\}} w_{ij} \|\vec q_i - \vec q_j\|^2.$$

Every word with a neighbour is in $U$, and its neighbours are in $U$ too, so the words outside $U$ appear only in their own first term, which is minimized by $\vec q_j = \hat{\vec q}_j$. $\Psi$ is strictly convex, because the first sum is a strictly convex quadratic ($\alpha_i > 0$) and the second is convex. The partial gradient is

$$\frac{\partial \Psi}{\partial \vec q_i} = 2\alpha_i(\vec q_i - \hat{\vec q}_i) + 2\sum_{j \in N(i)} w_{ij}(\vec q_i - \vec q_j),$$

because the edge $\{i, j\}$ appears once and contains $\vec q_i$ once. Setting it to zero gives $(\alpha_i + s_i)\vec q_i = \sum_j w_{ij}\vec q_j + \alpha_i \hat{\vec q}_i$, which is exactly line L4. So line L4 sets $\vec q_i$ to the exact minimizer of $\Psi$ in $\vec q_i$ with the other vectors fixed, and the stationarity conditions of $\Psi$ are the fixed point equations of Step 1. A strictly convex function has exactly one stationary point, its global minimizer, so the fixed point $x^*$ is the unique minimizer of $\Psi$. In this case a Gauss-Seidel sweep is exact block coordinate descent, and $\Psi$ does not increase during the sweep. $\blacksquare$

**Remark.** If each unordered edge were counted twice in $\Psi$ (once as $(i, j)$ and once as $(j, i)$), the gradient would have the factor $4 w_{ij}$, and line L4 would no longer be the coordinate minimizer. With $\beta_{ij} = 1/|N(i)|$ and unequal degrees, $\beta_{ij} \ne \beta_{ji}$, and Step 5 does not apply: the iteration still converges by Step 4, to the solution of the system of Step 1.
