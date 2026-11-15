---
title: The fast solve of implicit ALS equals the full weighted ridge solve, each half step minimizes its block, and the objective does not increase
proves: [correctness]
status: full
---

The notation is that of the page. There are $m$ users and $n$ items. For each pair, $r_{ui} \ge 0$ is the count, $p_{ui} = 1$ if $r_{ui} > 0$ and $p_{ui} = 0$ otherwise, and $c_{ui} = 1 + \alpha r_{ui}$ with $\alpha \ge 0$, so $c_{ui} \ge 1$ for every pair. $I_u$ is the set of items with $r_{ui} > 0$. The objective is

$$J(X, Y) = \sum_{u=1}^{m} \sum_{i=1}^{n} c_{ui} (p_{ui} - x_u^\top y_i)^2 + \lambda \Bigl( \sum_u \lVert x_u \rVert^2 + \sum_i \lVert y_i \rVert^2 \Bigr), \qquad \lambda > 0.$$

$Y$ is the $n \times r$ matrix with rows $y_i^\top$, and $C^u$ is the $n \times n$ diagonal matrix with entries $c_{ui}$. All statements are about exact arithmetic.

**Lemma 1 (separation).** For fixed $Y$, $J(X, Y) = \sum_u g_u(x_u) + \lambda \sum_i \lVert y_i \rVert^2$ with

$$g_u(x) = \sum_{i=1}^{n} c_{ui} (p_{ui} - x^\top y_i)^2 + \lambda \lVert x \rVert^2.$$

*Proof.* Group the terms of the double sum by user. The term of $(u, i)$ depends on $X$ only through $x_u$, and so does $\lambda \lVert x_u \rVert^2$. $\square$

**Lemma 2 (one weighted ridge regression).** Let $A_u = Y^\top C^u Y + \lambda I$ and $b_u = Y^\top C^u p(u)$, where $p(u)$ is the vector of the $p_{ui}$. Then $A_u$ is symmetric positive definite and $g_u$ has the unique minimizer $x_u^* = A_u^{-1} b_u$.

*Proof.* Expanding, $g_u(x) = x^\top A_u x - 2 b_u^\top x + \sum_i c_{ui} p_{ui}^2$, since $\sum_i c_{ui} y_i y_i^\top = Y^\top C^u Y$ and $\sum_i c_{ui} p_{ui} y_i = Y^\top C^u p(u)$. For $z \ne 0$, $z^\top A_u z = \sum_i c_{ui} (y_i^\top z)^2 + \lambda \lVert z \rVert^2 \ge \lambda \lVert z \rVert^2 > 0$, because every $c_{ui} \ge 0$. So $A_u$ is positive definite, $g_u$ is strictly convex, and its gradient $2 A_u x - 2 b_u$ vanishes exactly at $A_u^{-1} b_u$, which is therefore the unique minimizer. $\square$

**Lemma 3 (the fast system is the same system).** Let $G = Y^\top Y$. The matrix and the vector built in lines L7, L9 and L10,

$$\hat A_u = G + \lambda I + \sum_{i \in I_u} (c_{ui} - 1) y_i y_i^\top, \qquad \hat b_u = \sum_{i \in I_u} c_{ui} y_i,$$

satisfy $\hat A_u = A_u$ and $\hat b_u = b_u$.

*Proof.* $Y^\top C^u Y = \sum_{i=1}^{n} c_{ui} y_i y_i^\top = \sum_{i=1}^{n} y_i y_i^\top + \sum_{i=1}^{n} (c_{ui} - 1) y_i y_i^\top$. The first sum is $G$. For $i \notin I_u$, $r_{ui} = 0$, so $c_{ui} = 1$ and the term of $i$ in the second sum is zero; only $i \in I_u$ remain. For the vector, $p_{ui} = 0$ for $i \notin I_u$ and $p_{ui} = 1$ for $i \in I_u$, so $\sum_i c_{ui} p_{ui} y_i = \sum_{i \in I_u} c_{ui} y_i$. $\square$

**Theorem 4 (the half steps are exact).** Line L4 returns the unique minimizer of $J(\cdot, Y)$ over $X$, and line L5 returns the unique minimizer of $J(X, \cdot)$ over $Y$.

*Proof.* By Lemma 1, minimizing $J(\cdot, Y)$ is the same as minimizing each $g_u$ alone, since the last term does not depend on $X$. By Lemma 3, line L11 solves $A_u x = b_u$, and the Cholesky decomposition exists because $A_u$ is positive definite by Lemma 2. So each $x_u$ is the unique minimizer of $g_u$. For the item step, $J$ is symmetric in the roles of users and items: exchange $u$ and $i$, and $X$ and $Y$, in Lemmas 1 to 3. $\square$

**Corollary 5 (the objective does not increase).** Let $Y_0$ be the start of line L2, $X_0 = 0$, and let $X_{k+1}$ and $Y_{k+1}$ be the results of lines L4 and L5 in sweep $k + 1$. Then

$$J(X_{k+1}, Y_{k+1}) \le J(X_{k+1}, Y_k) \le J(X_k, Y_k),$$

and the values $J_k = J(X_k, Y_k)$ converge to a limit $J^* \ge 0$.

*Proof.* $X_{k+1}$ minimizes $J(\cdot, Y_k)$, so its value is at most that of $X_k$. $Y_{k+1}$ minimizes $J(X_{k+1}, \cdot)$, so its value is at most that of $Y_k$. The sequence $J_k$ does not increase and is bounded below by 0, so it converges. $\square$

**Proposition 6 (limit points are stationary).** The iterates satisfy $\lVert X_k \rVert^2 + \lVert Y_k \rVert^2 \le J_0 / \lambda$ in the Frobenius norm, and every limit point $(X^*, Y^*)$ of the sequence $(X_k, Y_k)$ has $\nabla_X J = 0$ and $\nabla_Y J = 0$.

*Proof.* $J \ge \lambda (\lVert X \rVert^2 + \lVert Y \rVert^2)$ and $J_k \le J_0$ by Corollary 5, which gives the bound, so limit points exist. Let $(X_{k_j}, Y_{k_j}) \to (X^*, Y^*)$ with $k_j \ge 1$. Since $Y_k$ minimizes $J(X_k, \cdot)$, $\nabla_Y J(X_k, Y_k) = 0$, and by continuity $\nabla_Y J(X^*, Y^*) = 0$. For $X$, pass to a further subsequence with $X_{k_j + 1} \to X'$. For every $X$, $J(X_{k_j + 1}, Y_{k_j}) \le J(X, Y_{k_j})$, and in the limit $X'$ minimizes $J(\cdot, Y^*)$. By Corollary 5, $J(X_{k_j + 1}, Y_{k_j})$ lies between $J_{k_j + 1}$ and $J_{k_j}$, so $J(X', Y^*) = J^* = J(X^*, Y^*)$. Then $X^*$ also attains the minimum of $J(\cdot, Y^*)$, and by the uniqueness of Lemma 2, $X^* = X'$, so $\nabla_X J(X^*, Y^*) = 0$. $\square$

**Cost of a sweep.** Line L7 costs $O(n r^2)$ once per user half step. For user $u$, lines L9 and L10 add $|I_u|$ outer products, in $O(|I_u| r^2)$ time, and line L11 costs $O(r^3)$. Since $\sum_u |I_u| = s$, the user half step costs $O(n r^2 + s r^2 + m r^3)$, and the item half step costs $O(m r^2 + s r^2 + n r^3)$. One sweep costs $O(s r^2 + (m + n) r^3)$, because $(m + n) r^2 \le (m + n) r^3$. The direct system of Lemma 2 would cost $O(n r^2)$ for each user, so $O(m n r^2)$ per half step.

**What is not claimed.** Proposition 6 does not say that the factors converge, and a stationary point need not be a global minimum: $Y_0 = 0$ gives $b_u = 0$, so $X_1 = 0$, then $Y_1 = 0$, and the run stays at $(0, 0)$. Whether the ranking that the factors produce is good is a question of measurement on data, not of this proof. $\blacksquare$
