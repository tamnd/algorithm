---
title: node2vec samples the second-order walk exactly and takes gradient steps on the skip-gram loss
proves: [correctness, termination]
status: full
---

We use the notation of the page. $G = (V, E)$ is an undirected graph with positive weights $w$, $N(v)$ is the set of neighbours of $v$, and $p, q > 0$. For an edge $\{t, v\}$ and $x \in N(v)$ let $\alpha(t, x) = 1/p$ if $x = t$, $1$ if $x \in N(t)$, and $1/q$ otherwise, and $\pi(t, v, x) = \alpha(t, x)\, w(v, x)$.

**Lemma 1 (the step distribution is defined).** For every edge $\{t, v\}$, the weights $\pi(t, v, x)$ for $x \in N(v)$ are positive and their sum $Z(t, v)$ is positive, so $P(x \mid t, v) = \pi(t, v, x) / Z(t, v)$ is a probability distribution on $N(v)$.

*Proof.* Each $\alpha(t, x)$ is one of $1/p$, $1$ and $1/q$, which are positive, and each $w(v, x) > 0$, so every $\pi(t, v, x) > 0$. Since $t \in N(v)$, the set $N(v)$ is not empty and $Z(t, v) \ge \pi(t, v, t) > 0$. $\square$

**Lemma 2 (exact sampling).** Let $x_1, \dots, x_j$ be the neighbours of $v$ with weights $\pi_1, \dots, \pi_j$ and $Z = \sum_i \pi_i$. Drawing $U$ uniform in $[0, 1)$ and returning the first $x_i$ with $U Z < \pi_1 + \dots + \pi_i$ returns $x_i$ with probability $\pi_i / Z$.

*Proof.* The event that $x_i$ is returned is $\pi_1 + \dots + \pi_{i-1} \le U Z < \pi_1 + \dots + \pi_i$, an interval of length $\pi_i / Z$ for $U$. These intervals partition $[0, 1)$. $\square$

**Lemma 3 (walks).** A walk produced by lines L5 to L7 from a vertex $u$ is a sequence of vertices in which consecutive vertices are adjacent. If $N(u) = \emptyset$ or $\ell = 1$ it is $[u]$; otherwise it has exactly $\ell$ vertices. Given its first $i \ge 2$ vertices ending in $t, v$, the next vertex is $x$ with probability $\pi(t, v, x) / Z(t, v)$, independently of the earlier vertices.

*Proof.* Line L5 appends a neighbour of $u$ when one exists and $\ell > 1$; by Lemma 2 with the weights $w(u, \cdot)$ it is chosen in proportion to the weight. If no vertex was appended, the walk has one vertex and the condition $1 < |walk|$ of line L6 fails, so the walk is $[u]$. Otherwise the last two vertices $t, v$ are adjacent, and by Lemma 1 and Lemma 2 line L7 appends a neighbour $x$ of $v$ with the stated probability, which depends only on $t$ and $v$. Then $v, x$ are adjacent, so the invariant "the last two vertices are adjacent" holds again, and each round adds one vertex, so the loop stops when the walk has $\ell$ vertices. $\square$

**Lemma 4 (reduction to the weighted walk).** If $p = q = 1$, then $P(x \mid t, v) = w(v, x) / \sum_{y \in N(v)} w(v, y)$, the first-order weighted random walk.

*Proof.* Every $\alpha(t, x)$ equals 1. $\square$

**Lemma 5 (the update is a gradient step).** For a pair $(u, c)$ with negative samples $x_1, \dots, x_s$, let $\lambda(z_u) = -\log \sigma(z_u \cdot y_c) - \sum_{i} \log \sigma(-z_u \cdot y_{x_i})$, with $\sigma(a) = 1/(1 + e^{-a})$. Then

$$\nabla_{z_u} \lambda = -(1 - \sigma(z_u \cdot y_c))\, y_c + \sum_i \sigma(z_u \cdot y_{x_i})\, y_{x_i},$$

and the analogous formulas hold for each context vector. The implementation adds $\eta (\ell_j - \sigma(z_u \cdot y_j))\, y_j$ to $z_u$ for each target $j$ with label $\ell_j = 1$ for $c$ and $0$ for the samples, which is $-\eta \nabla_{z_u} \lambda$.

*Proof.* $\frac{d}{da} \log \sigma(a) = 1 - \sigma(a)$ and $\frac{d}{da} \log \sigma(-a) = -\sigma(a)$; apply the chain rule with $a = z_u \cdot y_j$, whose gradient in $z_u$ is $y_j$. For the label 1 term, $-(1 - \sigma)\, y_c$; for a label 0 term, $\sigma\, y_{x_i}$. Negating and scaling by $\eta$ gives $\eta(1 - \sigma)\, y_c$ and $\eta(0 - \sigma)\, y_{x_i}$. $\square$

**Theorem.** NODE2VEC stops, and its walks are independent samples of the second-order walk of Grover and Leskovec, $r$ from every vertex, each with $\ell$ vertices (or one vertex from an isolated vertex). Its vectors are the result of stochastic gradient steps on the skip-gram loss with negative sampling over the pairs of these walks.

*Proof.* Lines L3 and L4 run $r n$ times, each walk has at most $\ell$ vertices by Lemma 3, and line L9 visits each of the at most $r n \ell$ positions of the walks, with at most $2k$ context vertices and $s$ samples each, a finite number of updates. So the algorithm stops. The walks have the stated distribution by Lemma 3 and use fresh random numbers, so they are independent given the graph. The learning phase consists of the updates of Lemma 5. $\blacksquare$
