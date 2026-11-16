---
title: The Laplacian consensus protocol converges to the average on a connected undirected graph, and to a weighted average on a strongly connected directed graph
proves: [correctness]
status: full
---

There are $r$ agents with states $x_i \in \mathbb{R}$. The weights $a_{ij} \ge 0$ form the matrix $A$, with $a_{ii} = 0$, and $a_{ij} > 0$ exactly when agent $i$ reads the state of agent $j$. The Laplacian is $L = D - A$, where $D$ is the diagonal matrix of the weighted in-degrees $d_i = \sum_j a_{ij}$, and $\Delta = \max_i d_i$. The graph is fixed. The continuous protocol is $\dot x = -L x$. The sampled protocol of lines L1 to L7 on the [Laplacian consensus protocol](/laplacian-consensus-protocol/) page is $x(k+1) = P x(k)$ with $P = I - \varepsilon L$. $\mathbf 1$ is the all ones vector and $\bar x = \frac1r \mathbf 1^T x(0)$.

**Lemma 1 (agreement is an equilibrium).** $L \mathbf 1 = 0$, so every vector $c \mathbf 1$ is an equilibrium of both protocols.

*Proof.* Row $i$ of $L \mathbf 1$ is $d_i - \sum_j a_{ij} = 0$. $\square$

**Lemma 2 (the sum is invariant on an undirected graph).** If $A$ is symmetric, then $\mathbf 1^T L = 0$, so $\mathbf 1^T x$ is constant along both protocols, and the average stays $\bar x$.

*Proof.* $\mathbf 1^T L = (L^T \mathbf 1)^T = (L \mathbf 1)^T = 0$ by Lemma 1. Then $\frac{d}{dt} \mathbf 1^T x = -\mathbf 1^T L x = 0$, and $\mathbf 1^T x(k+1) = \mathbf 1^T x(k) - \varepsilon \mathbf 1^T L x(k) = \mathbf 1^T x(k)$. $\square$

**Lemma 3 (the quadratic form).** If $A$ is symmetric, then $x^T L x = \sum_{\{i,j\}} a_{ij} (x_i - x_j)^2$, where the sum is over unordered pairs. So $L$ is symmetric positive semidefinite, and $L x = 0$ if and only if $x$ is constant on each connected component of the graph.

*Proof.* $x^T L x = \sum_i d_i x_i^2 - \sum_{i,j} a_{ij} x_i x_j = \frac12 \sum_{i,j} a_{ij} (x_i^2 + x_j^2 - 2 x_i x_j)$, using $a_{ij} = a_{ji}$, and this is the sum over unordered pairs of $a_{ij} (x_i - x_j)^2 \ge 0$. For a symmetric positive semidefinite $L$, $L x = 0$ if and only if $x^T L x = 0$, that is, $x_i = x_j$ on every edge, that is, $x$ is constant along every path. $\square$

So on a connected undirected graph the eigenvalues of $L$ are $0 = \lambda_1 < \lambda_2 \le \dots \le \lambda_r$, and the kernel is spanned by $\mathbf 1$. The number $\lambda_2$ is the algebraic connectivity.

**Lemma 4 (a bound on the largest eigenvalue).** $\lambda_r \le 2 \Delta$.

*Proof.* By the [Gershgorin circle theorem](/gershgorin-circle-theorem/), every eigenvalue lies in a disk with center $d_i$ and radius $\sum_{j \ne i} |{-a_{ij}}| = d_i$, so it is at most $2 d_i \le 2 \Delta$. $\square$

**Theorem 1 (continuous time, undirected).** On a connected undirected graph, the error $e(t) = x(t) - \bar x \mathbf 1$ of $\dot x = -L x$ satisfies $\lVert e(t) \rVert_2 \le e^{-\lambda_2 t} \lVert e(0) \rVert_2$. So every $x_i(t)$ converges to $\bar x$ exponentially.

*Proof.* By Lemma 2, $\mathbf 1^T e(t) = 0$ for all $t$, and by Lemma 1, $\dot e = \dot x = -L x = -L e$. For a symmetric $L$ and $e \perp \mathbf 1$, the [Rayleigh quotient](/rayleigh-quotient/) gives $e^T L e \ge \lambda_2 \lVert e \rVert^2$, since $\mathbf 1$ spans the eigenspace of $\lambda_1 = 0$. So $\frac{d}{dt} \lVert e \rVert^2 = -2 e^T L e \le -2 \lambda_2 \lVert e \rVert^2$, and Gronwall's inequality gives $\lVert e(t) \rVert^2 \le e^{-2 \lambda_2 t} \lVert e(0) \rVert^2$. $\square$

**Theorem 2 (sampled protocol, undirected).** On a connected undirected graph with $0 < \varepsilon < 1/\Delta$, the error of the sampled protocol satisfies $\lVert e(k) \rVert_2 \le \rho^k \lVert e(0) \rVert_2$ with $\rho = \max(|1 - \varepsilon \lambda_2|, |1 - \varepsilon \lambda_r|) < 1$.

*Proof.* As in Theorem 1, $e(k+1) = (I - \varepsilon L) e(k)$ and $e(k) \perp \mathbf 1$. The symmetric matrix $I - \varepsilon L$ maps the subspace $\mathbf 1^\perp$ to itself, and on it its eigenvalues are $1 - \varepsilon \lambda_i$ for $i = 2, \dots, r$. Its norm there is the largest of their absolute values, which is $\rho$, since $1 - \varepsilon \lambda$ is monotone in $\lambda$. Now $\lambda_2 > 0$ gives $1 - \varepsilon \lambda_2 < 1$, and Lemma 4 gives $1 - \varepsilon \lambda_r \ge 1 - 2 \varepsilon \Delta > -1$. Both values lie in $(-1, 1)$, so $\rho < 1$. $\square$

**Corollary (disconnected graphs).** If the undirected graph has several connected components, the protocol runs on each component on its own, because $L$ is block diagonal after a renumbering of the agents. By Theorems 1 and 2, each component converges to the average of its own initial states.

**Theorem 3 (directed graph).** Let the directed graph be strongly connected, and let $0 < \varepsilon < 1/\Delta$. Then there is a unique vector $w$ with $w^T L = 0$, $\mathbf 1^T w = 1$, and all $w_i > 0$. The sampled protocol converges to $(w^T x(0)) \mathbf 1$. The limit is the plain average $\bar x \mathbf 1$ for every start if and only if the graph is balanced, that is, $\sum_j a_{ij} = \sum_j a_{ji}$ for every $i$.

*Proof.* The entries of $P = I - \varepsilon L$ are $p_{ii} = 1 - \varepsilon d_i > 0$ and $p_{ij} = \varepsilon a_{ij} \ge 0$ for $j \ne i$, and every row sums to 1 by Lemma 1. So $P$ is a row-stochastic matrix. It has the same off-diagonal pattern as $A$, so it is irreducible when the graph is strongly connected, and its positive diagonal makes it primitive: if there is a path of length $\ell$ from $i$ to $j$, then there is a walk of every length $m \ge \ell$, by waiting at a vertex, so all entries of $P^{m}$ are positive for $m \ge r - 1$. By the [Perron-Frobenius theorem](/perron-frobenius-theorem/) for primitive matrices, the eigenvalue 1 of $P$ is simple and every other eigenvalue has modulus less than 1. Its left eigenvector $w$ can be scaled to have positive entries and $\mathbf 1^T w = 1$, and $P^k \to \mathbf 1 w^T$. So $x(k) = P^k x(0) \to \mathbf 1 (w^T x(0))$. Since $w^T P = w^T$ if and only if $w^T L = 0$, $w$ is the left kernel vector of $L$.

If the graph is balanced, then column $j$ of $L$ sums to $d_j - \sum_i a_{ij} = 0$, so $\mathbf 1^T L = 0$, and $w = \mathbf 1 / r$ by uniqueness. Conversely, if $w^T x(0) = \bar x$ for every $x(0)$, then $w = \mathbf 1 / r$, so $\mathbf 1^T L = 0$, which is the balance condition. $\blacksquare$

**What is not proved here.** For the continuous protocol on a directed graph, the same limit $w^T x(0)$ holds under the same hypothesis, by the same Perron argument applied to $e^{-L t}$, which is a positive matrix for $t > 0$. Olfati-Saber and Murray (2004) give these results and the extension to switching balanced graphs with a common Lyapunov function. When the graph is directed and only has a rooted spanning tree, the protocol still reaches agreement, and the limit is a weighted average of the states of the root strongly connected component; Ren and Beard (2005) prove this and the switching case. For switching undirected graphs, agreement holds when the union of the graphs over bounded intervals is connected (Jadbabaie, Lin and Morse 2003). These results are cited on the page and not proved here.
