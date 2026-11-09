---
title: Guided local search keeps the best local minimum, and penalties push it out of every fixed point
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The set of solutions $S$ is finite, $g : S \to \mathbb{R}$ is the objective to minimize, each solution $x$ has a finite set $F(x)$ of features, each feature $e$ has a cost $c_e \ge 0$ and a penalty $p_e \ge 0$, and $\lambda = a \, g(x_1) / |F(x_1)|$ is fixed after line L2, where $x_1$ is the first local minimum. The augmented objective is $h(y) = g(y) + \lambda \sum_{e \in F(y)} p_e$. LOCAL-SEARCH is a descent, such as best-improvement [hill climbing](/hill-climbing/), that on input $(x, h)$ returns a local minimum of $h$ in a neighborhood $N$. Write $x_k$ for the solution after iteration $k$.

**Lemma 1 (termination).** Each call of LOCAL-SEARCH stops, so the algorithm stops after $K + 1$ calls.

*Proof.* During one call the penalties do not change, so $h$ is a fixed function. Each move of the descent strictly lowers $h$, so no solution repeats within the call, and $S$ is finite. Line L3 makes exactly $K$ passes. $\square$

**Lemma 2 (penalties).** In each iteration, line L5 adds exactly 1 to $p_e$ for each feature $e \in F(x_{k-1})$ of maximum utility $u_e = c_e / (1 + p_e)$, and changes no other penalty. So every penalty is non-decreasing over the run, and the total penalty grows by at least 1 per iteration if $F(x_{k-1})$ is not empty.

*Proof.* Lines L4 and L5 are the only lines that change $p$, and they do exactly this. A nonempty finite set of utilities has a maximum, attained by at least one feature. $\square$

**Lemma 3 (the best solution).** After iteration $k$, $b$ is one of $x_1, \ldots, x_k$ and $g(b) = \min_{j \le k} g(x_j)$. Each $x_k$ is a local minimum of the augmented objective in force during iteration $k$.

*Proof.* Line L1 sets $b = x_1$, and line L7 replaces $b$ by $x_k$ exactly when $g(x_k) < g(b)$. The second claim is the property of LOCAL-SEARCH. $\square$

**Theorem 1 (no fixed point).** Suppose $\lambda > 0$, and suppose a solution $x$ has $c_e > 0$ for every $e \in F(x)$ and has a neighbor $y \in N(x)$ with $F(x) \not\subseteq F(y)$. Then GLS cannot stay at $x$ for ever: there is no $k_0$ with $x_k = x$ for all $k \ge k_0$.

*Proof.* Suppose $x_k = x$ for all $k \ge k_0$. Then from iteration $k_0 + 1$ on, line L5 penalizes only features of $x$.

First, every feature of $x$ is penalized infinitely often. If not, some $e \in F(x)$ is penalized for the last time at some iteration, and from then on its utility is a constant $u = c_e / (1 + p_e) > 0$. Each later iteration penalizes a feature $f \in F(x)$ whose utility is at least $u$, which needs $c_f / (1 + p_f) \ge u$, that is, $p_f \le c_f / u - 1$. Each penalty can take only finitely many values below this bound, and $F(x)$ is finite, so only finitely many later iterations are possible. This contradicts the fact that the run goes on with no end at $x$. So $p_e \to \infty$ for every $e \in F(x)$.

Now take the neighbor $y$ with some $e^* \in F(x) \setminus F(y)$. The penalties of the features in $F(y) \setminus F(x)$ do not change after iteration $k_0$, since only features of $x$ are penalized. So
$$h(y) - h(x) = g(y) - g(x) + \lambda \Big( \sum_{e \in F(y) \setminus F(x)} p_e - \sum_{e \in F(x) \setminus F(y)} p_e \Big),$$
and the last sum contains $p_{e^*} \to \infty$ while the first sum stays bounded. So $h(y) < h(x)$ after enough iterations, and $x$ is then not a local minimum of $h$. By Lemma 3, $x_k$ is a local minimum of $h$, so $x_k \ne x$ for this $k$. This is a contradiction. $\square$

**Theorem 2 (correctness).** The algorithm stops after $K + 1$ runs of the local search and returns $b$ with $g(b)$ the least value of $g$ among $x_1, \ldots, x_K$. The penalties never decrease.

*Proof.* This follows from Lemmas 1, 2 and 3. $\blacksquare$

**What is not claimed.** Theorem 1 says that the penalties move the search out of any one solution, not that the search reaches a global minimum or that it does not cycle among several solutions. The result $b$ is a local minimum of the augmented objective in force when it was found, which need not be a local minimum of $g$. GLS has no general optimality guarantee.
