---
title: Neutralize removes the bias component and equalize makes every neutral word equidistant
proves: [correctness]
status: full
---

We use the pseudocode of the page. All vectors are in $\mathbb{R}^d$. After line L1 every word vector has length 1. The rows $b_1, \ldots, b_k$ of $B$ are orthonormal, and $v_B = \sum_r (v \cdot b_r) b_r$ is the orthogonal projection of $v$ on the span of $B$, which we also call $B$.

**Lemma 1 (projection).** For every $v$, $v - v_B$ is orthogonal to every $b_r$, and $\|v\|^2 = \|v_B\|^2 + \|v - v_B\|^2$.

*Proof.* $(v - v_B) \cdot b_s = v \cdot b_s - \sum_r (v \cdot b_r)(b_r \cdot b_s) = v \cdot b_s - v \cdot b_s = 0$, by orthonormality. Since $v_B$ is a combination of the $b_r$, it is orthogonal to $v - v_B$, and the Pythagorean theorem gives the second statement. $\square$

**Lemma 2 (the covariance of pairs).** For a defining set $\{a, b\}$ of two words, the contribution of line L3 is $\frac{1}{4}(a - b)(a - b)^T$. So with pairs only, $C$ is $\frac{1}{4}$ times the sum of the outer products of the differences, and its top eigenvector is the first principal component, without centering, of the differences $a - b$.

*Proof.* $\mu = (a + b)/2$, so $a - \mu = (a - b)/2$ and $b - \mu = -(a - b)/2$. Each gives the outer product $\frac{1}{4}(a - b)(a - b)^T$, and line L3 adds both and divides by $|D| = 2$. $\square$

**Lemma 3 (the subspace).** The span of the top $k$ eigenvectors of $C$ maximizes $\sum_D \sum_{w \in D} \|(w - \mu_D)_B\|^2 / |D| = \operatorname{tr}(P C)$ over the $k$-dimensional subspaces with orthogonal projection $P$. This is the theorem of Ky Fan on the trace of a symmetric matrix, the basis of [principal component analysis](/principal-component-analysis/). When the $k$-th and the $(k+1)$-th eigenvalues differ, power iteration with deflation from a start vector that is not orthogonal to the eigenvectors converges to this basis (see [power iteration](/power-iteration/)). The tests check $C u = \lambda u$ and that no random unit vector has a larger Rayleigh quotient than the first eigenvalue. $\square$

**Theorem 1 (neutralize).** If $w$ is not in $B$, line L5 returns a unit vector $w'$ with $w' \cdot b_r = 0$ for every $r$. So the direct bias $|\cos(w', g)|$ is 0 for every $g$ in $B$.

*Proof.* By Lemma 1, $w - w_B$ is orthogonal to $B$, and it is not 0 because $w$ is not in $B$. Dividing by its length keeps the orthogonality and gives length 1. $\square$

**Theorem 2 (equalize).** Let $E$ be a set of unit vectors with mean $\mu$, and let $\nu = \mu - \mu_B$. Suppose $w_B \ne \mu_B$ for every $w \in E$. Line L7 maps each $w \in E$ to

$$e_w = \nu + \sqrt{1 - \|\nu\|^2}\, u_w, \qquad u_w = \frac{w_B - \mu_B}{\|w_B - \mu_B\|}.$$

Then (a) the square root is real, (b) every $e_w$ has length 1, (c) every $e_w$ has the same component $\nu$ outside $B$, and (d) for every vector $n$ orthogonal to $B$, such as a neutralized word, $n \cdot e_w = n \cdot \nu$ and $\|n - e_w\|$ is the same for all $w \in E$. (e) For a pair $E = \{a, b\}$, $(e_a)_B = -(e_b)_B$.

*Proof.* (a) $\|\mu\| \le 1$, because $\mu$ is a mean of unit vectors and the norm is convex. By Lemma 1, $\|\nu\| \le \|\mu\| \le 1$. (b) $u_w$ lies in $B$ and $\nu$ is orthogonal to $B$ by Lemma 1, so $\|e_w\|^2 = \|\nu\|^2 + (1 - \|\nu\|^2)\|u_w\|^2 = 1$. (c) The part of $e_w$ outside $B$ is $\nu$, since $u_w$ is in $B$. (d) $n \cdot u_w = 0$, so $n \cdot e_w = n \cdot \nu$. Then $\|n - e_w\|^2 = \|n\|^2 - 2 n \cdot \nu + 1$, which does not depend on $w$. (e) $a_B - \mu_B = (a_B - b_B)/2 = -(b_B - \mu_B)$, so $u_a = -u_b$, and the $B$ components $\sqrt{1 - \|\nu\|^2}\, u_a$ and $\sqrt{1 - \|\nu\|^2}\, u_b$ are opposite. $\square$

**Corollary.** After lines L5 to L7, every neutral word is at the same distance from all the words of each equality set, and its projection on the bias subspace is 0. Line L7 runs after line L5, and it changes only the words of the equality sets, so the neutral words keep the property of Theorem 1. A word that is both neutral and in an equality set is not allowed, since the two steps would contradict each other. $\blacksquare$

The theorems are about the geometry that the method enforces. They say nothing about other directions that still separate the words; that the bias stays recoverable from them is a measurement (Gonen and Goldberg 2019), and the test of the code reproduces it on a toy example.
