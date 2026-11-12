---
title: The Chow-Liu tree has the largest likelihood among all tree-shaped Bayesian networks
proves: [correctness]
status: full
---

We use the pseudocode of the page. The data are $s$ samples $x^{(1)}, \dots, x^{(s)}$ of $n$ discrete variables $X_1, \dots, X_n$. Write $\hat P$ for the empirical distribution, $\hat H(X_v)$ and $\hat H(X_v \mid X_u)$ for its entropy and conditional entropy, and $\hat I(X_u; X_v) = \hat H(X_v) - \hat H(X_v \mid X_u)$ for its mutual information. All logarithms are natural.

**Claim.** Among all Bayesian networks whose DAG is a directed tree (one root, every other node with exactly one parent) and all choices of their tables, the output of the algorithm has the largest likelihood of the data.

*Step 1: the best tables for a fixed tree.* Fix a directed tree with parent function $\mathrm{pa}$. The log-likelihood is

$$\ell(\theta) = \sum_{t=1}^{s} \sum_{v} \log \theta_v\big(x^{(t)}_v \mid x^{(t)}_{\mathrm{pa}(v)}\big) = \sum_v \sum_{b} \sum_{a} N_v(a, b) \log \theta_v(a \mid b),$$

where $N_v(a, b)$ is the number of samples with $x_v = a$ and $x_{\mathrm{pa}(v)} = b$. The terms for different $v$ and $b$ use separate parameters, so each can be maximized alone. For fixed $v$ and $b$ with $N_v(b) = \sum_a N_v(a, b) > 0$, Gibbs' inequality says that $\sum_a N_v(a, b) \log \theta(a)$ over probability vectors $\theta$ is largest at $\theta(a) = N_v(a, b) / N_v(b)$. These are the empirical conditionals that line L10 sets. (Values $b$ that never occur do not affect the likelihood.) The root is the case with no parent.

*Step 2: the likelihood of a tree.* Put the best tables into $\ell$ and divide by $s$:

$$\frac{1}{s} \ell^*(\mathrm{pa}) = \sum_v \sum_{a, b} \hat P(a, b) \log \hat P(a \mid b) = -\sum_v \hat H(X_v \mid X_{\mathrm{pa}(v)}) = \sum_{v \ne r} \hat I(X_v; X_{\mathrm{pa}(v)}) - \sum_v \hat H(X_v),$$

where $r$ is the root, for which $\hat H(X_r \mid \cdot) = \hat H(X_r)$. The last sum does not depend on the tree. The first sum is the total weight of the undirected edges $\{v, \mathrm{pa}(v)\}$ under the weights $w(u, v) = \hat I(X_u; X_v)$, and mutual information is symmetric. So the best likelihood of a directed tree depends only on its undirected skeleton $T$, and

$$\ell^*(T) = s \sum_{uv \in T} w(u, v) - s \sum_v \hat H(X_v).$$

Every spanning tree $T$ of the complete graph on the $n$ variables is the skeleton of a directed tree (orient its edges away from any root), and every directed tree has a spanning tree as its skeleton. So a directed tree of largest likelihood is any orientation of a maximum weight spanning tree.

*Step 3: lines L3 to L7 find a maximum weight spanning tree.* These lines are Kruskal's algorithm with the edges in decreasing order of weight. The usual cut argument proves it: suppose the edges chosen so far lie in some maximum weight spanning tree $T^*$, and the algorithm adds $e = uv$. Let $C$ be the component of $u$ in the forest just before $e$ is added; it does not contain $v$. If $e \notin T^*$, the path in $T^*$ from $u$ to $v$ leaves $C$ through some edge $f$. The edge $f$ joins two components of the current forest. Components only grow, so if the algorithm had looked at $f$ earlier, its ends were in different components then too, and $f$ would have been chosen and would lie inside one component. So the algorithm has not yet looked at $f$, and $w(f) \le w(e)$ by the order. Then $T^* - f + e$ is a spanning tree with weight at least $w(T^*)$, so it is also a maximum weight spanning tree, and it contains all chosen edges and $e$. By induction the final forest, which has $n - 1$ edges because the complete graph is connected, is a maximum weight spanning tree. See [Kruskal's algorithm](/kruskal/).

*Step 4: lines L8 to L11.* Line L8 orients the tree away from the root by a graph search, which gives a directed tree with the same skeleton. Lines L9 and L10 set the tables of Step 1. By Steps 2 and 3 the result has the largest likelihood. $\blacksquare$

**Remarks.**

- The root does not matter: every orientation of the same skeleton has the same likelihood, by Step 2.
- Weights are never negative, since $\hat I \ge 0$. So a spanning tree is always at least as good as a forest, and the algorithm never needs to stop early. With a penalty per edge, as in BIC, edges with small weight can have negative penalized weight, and the best structure is a forest.
- Ties in the weights give several optimal trees with the same likelihood; the algorithm returns one of them.
- The same argument with the true distribution $P$ in place of $\hat P$ gives the original statement of Chow and Liu (1968): the tree distribution that minimizes the Kullback-Leibler divergence $D(P \,\|\, P_T)$ is built on a maximum weight spanning tree under the true mutual informations.
