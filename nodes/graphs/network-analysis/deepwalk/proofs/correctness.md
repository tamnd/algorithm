---
title: DeepWalk is stochastic gradient descent on the skip-gram loss of its walks
proves: [correctness, termination]
status: full
---

Let $G$ be a graph with $V = \{0, \ldots, n-1\}$, given by the out-lists $\mathrm{Adj}[v]$, and let $T$ be a binary tree whose leaves are the $n$ vertices and in which every inner node has two children, so $T$ has $n - 1$ inner nodes. For a vertex $u$, let $P(u) = ((i_1, s_1), \ldots, (i_L, s_L))$ be the inner nodes on the path from the root to the leaf of $u$, with $s_l = +1$ for a step to the left child and $s_l = -1$ for a step to the right child. For $x \in \mathbb{R}^d$ and vectors $\Psi_i$, write

$$\Pr(u \mid x) = \prod_{(i, s) \in P(u)} \sigma(s\, \Psi_i \cdot x), \qquad \ell_u(x, \Psi) = -\log \Pr(u \mid x) = -\sum_{(i, s) \in P(u)} \log \sigma(s\, \Psi_i \cdot x),$$

with $\sigma(z) = 1/(1 + e^{-z})$.

**Termination.** Line L2 runs $\gamma$ times and line L4 runs $n$ times per pass. A walk has at most $t$ vertices, so lines L6 and L7 run at most $t \cdot 2w$ times per walk, and each tree path has at most $n - 1$ nodes. Every loop is over a finite range, so the algorithm stops.

**Lemma 1 (walks).** Given its start $v$, the sequence $W$ of line L5 has the distribution of the simple random walk on $G$ from $v$, stopped after $t$ vertices or at the first vertex with no out-neighbour. In particular, consecutive vertices of $W$ are joined by an arc.

*Proof.* The walk starts at $v$. While it has fewer than $t$ vertices and its last vertex $x$ has an out-neighbour, it appends an element of $\mathrm{Adj}[x]$ drawn uniformly and independently of the past, which is the transition rule of the simple random walk; otherwise it stops. $\square$

**Lemma 2 (pairs).** For a walk $W$ of length $L$, lines L6 and L7 visit each ordered pair of positions $(j, k)$ with $1 \le j, k \le L$ and $0 < |k - j| \le w$ exactly once, and no other pair.

*Proof.* Line L6 takes each $j$ once. Line L7 takes each $k$ in the range $\max(1, j - w) \le k \le \min(L, j + w)$ once and skips $k = j$. These are exactly the $k$ with $1 \le k \le L$ and $0 < |k - j| \le w$. $\square$

**Lemma 3 (the model is a distribution).** For every $x$ and every $\Psi$, $\Pr(u \mid x) > 0$ for each $u$, and $\sum_{u \in V} \Pr(u \mid x) = 1$.

*Proof.* Each factor $\sigma(\cdot)$ is positive. For a node $a$ of $T$, let $\pi(a)$ be the product of $\sigma(s\, \Psi_i \cdot x)$ over the inner nodes $i$ strictly above $a$ on the path from the root, with the sign $s$ of the step taken at $i$, so $\pi(\mathrm{root}) = 1$ and $\pi(\text{leaf of } u) = \Pr(u \mid x)$. We show by induction on the height of $a$ that the sum of $\pi$ over the leaves below $a$ equals $\pi(a)$. For a leaf it is clear. For an inner node $a$ with children $b$ (left) and $c$ (right), $\pi(b) = \pi(a)\, \sigma(\Psi_a \cdot x)$ and $\pi(c) = \pi(a)\, \sigma(-\Psi_a \cdot x)$, so by induction the sum below $a$ is $\pi(a)(\sigma(z) + \sigma(-z))$ with $z = \Psi_a \cdot x$. Since $\sigma(z) + \sigma(-z) = \frac{1}{1 + e^{-z}} + \frac{e^{-z}}{e^{-z} + 1} = 1$, this is $\pi(a)$. At the root, the sum over all leaves is $1$. $\square$

**Lemma 4 (one update is one gradient step).** Fix a pair of line L7, with $x = \Phi_{W[j]}$, $u = W[k]$ and the current $\Psi$. After lines L8 and L9,

$$\Psi_i^{\text{new}} = \Psi_i - \alpha\, \frac{\partial \ell_u}{\partial \Psi_i}(x, \Psi) \text{ for each } (i, s) \in P(u), \qquad x^{\text{new}} = x - \alpha\, \frac{\partial \ell_u}{\partial x}(x, \Psi),$$

and no other vector changes.

*Proof.* Since $\sigma'(z) = \sigma(z)(1 - \sigma(z))$, $\frac{d}{dz}\bigl(-\log \sigma(z)\bigr) = -(1 - \sigma(z))$. The inner nodes on $P(u)$ are distinct, so each $\Psi_i$ with $(i, s) \in P(u)$ occurs in exactly one term of $\ell_u$, and by the chain rule

$$\frac{\partial \ell_u}{\partial \Psi_i} = -(1 - \sigma(s\, \Psi_i \cdot x))\, s\, x, \qquad \frac{\partial \ell_u}{\partial x} = -\sum_{(i, s) \in P(u)} (1 - \sigma(s\, \Psi_i \cdot x))\, s\, \Psi_i,$$

while $\ell_u$ does not depend on the other $\Psi_i$ or on the other rows of $\Phi$.

Line L9 handles the nodes of $P(u)$ in turn. When it reaches $(i, s)$, the vector $\Psi_i$ has not yet changed during this pair, because the nodes are distinct, and $x$ has not changed, because $x$ is written only after the loop; the vectors $\Psi_i$ belong to inner nodes and are separate from the rows of $\Phi$, so writing $\Psi_i$ does not touch $x$, even when $u = W[j]$. So $g = \alpha (1 - \sigma(s\, \Psi_i \cdot x))\, s$ is computed from the values before the pair, and $\Psi_i^{\text{new}} = \Psi_i + g\, x = \Psi_i - \alpha\, \partial \ell_u / \partial \Psi_i$. The accumulator receives $g\, \Psi_i$ with the old $\Psi_i$, read before the update. After the loop it holds $\sum_{(i,s)} \alpha (1 - \sigma(s\, \Psi_i \cdot x))\, s\, \Psi_i = -\alpha\, \partial \ell_u / \partial x$, and adding it to $x$ gives the claim. $\square$

**Theorem.** DEEPWALK stops and returns $\Phi$ after the following process: it draws $\gamma n$ random walks as in Lemma 1, $\gamma$ from each vertex, and for each walk, in the order of Lemma 2, it takes for each pair of positions $(j, k)$ one gradient step of size $\alpha$ on the loss $\ell_{W[k]}$ of the probability distribution of Lemma 3, at the current values of $\Phi_{W[j]}$ and $\Psi$.

*Proof.* Termination was shown above. Lines L2 to L4 start one walk at each vertex in each of the $\gamma$ passes. By Lemma 1 each walk is a stopped simple random walk, by Lemma 2 the inner loops visit exactly the pairs of positions at most $w$ apart, once each, by Lemma 3 the loss of each pair is the negative logarithm of a probability distribution on $V$, and by Lemma 4 each visit performs exactly one gradient step on that loss and changes nothing else. Line L10 returns $\Phi$. $\blacksquare$

So DeepWalk is stochastic gradient descent, with the samples generated online, on $\sum_{(v, u)} -\log \Pr(u \mid \Phi_v)$, the sum over all pairs of its walks. The loss is not convex in $(\Phi, \Psi)$, so the theorem says nothing about reaching a global minimum.
