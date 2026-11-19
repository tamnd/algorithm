---
title: The removed direction carries the most energy and the output is orthogonal to it
proves: [correctness]
status: full
---

We use the pseudocode of the page. The sentence vectors after line L2 are $v_1, \ldots, v_n \in \mathbb{R}^d$, and $X$ is the $n \times d$ matrix with these rows. The claim has three parts: the weights do what the page says, line L4 finds the direction that carries the most energy of the sentence vectors, and line L6 removes exactly that direction.

**Lemma 1 (the weights).** For $a > 0$, the weight $f(p) = a / (a + p)$ is in $(0, 1]$, equals 1 at $p = 0$ and $1/2$ at $p = a$, and strictly decreases in $p \ge 0$.

*Proof.* $f(0) = a/a = 1$ and $f(a) = a / 2a = 1/2$. For $p \ge 0$ the denominator $a + p$ is positive and strictly increases, so $f$ is positive and strictly decreases. $\square$

So a word with $p(w) \gg a$ gets about $a / p(w)$, and a word with $p(w) \ll a$ gets about 1.

**Lemma 2 (the top direction).** Let $G = X^T X$, a symmetric positive semidefinite $d \times d$ matrix. For a unit vector $r$, $\|X r\|^2 = \sum_i (v_i \cdot r)^2 = r^T G r$. This is largest when $r$ is an eigenvector of $G$ for its largest eigenvalue $\sigma_1^2$, which is the first right singular vector of $X$, and then $\|X r\| = \sigma_1$.

*Proof.* Write $G = \sum_j \lambda_j q_j q_j^T$ with orthonormal eigenvectors $q_j$ and $\lambda_1 \ge \lambda_2 \ge \cdots \ge 0$. For a unit $r$, $r^T G r = \sum_j \lambda_j (q_j \cdot r)^2 \le \lambda_1 \sum_j (q_j \cdot r)^2 = \lambda_1$, with equality at $r = q_1$. The singular value decomposition $X = U \Sigma Q^T$ gives $G = Q \Sigma^2 Q^T$, so $q_1$ is the first right singular vector and $\lambda_1 = \sigma_1^2$. $\square$

The matrix $G$ is not centered: $u$ is the direction with the largest mean squared projection of the sentence vectors, not the largest variance. When all sentence vectors share a large common part, as in the generative model of the paper, this direction points along that part.

**Lemma 3 (power iteration).** If $\lambda_1 > \lambda_2$ and the start vector $u_0$ has $q_1 \cdot u_0 \ne 0$, the iterates $u_{t+1} = G u_t / \|G u_t\|$ converge to $\pm q_1$, and the angle to $q_1$ shrinks by a factor of about $\lambda_2 / \lambda_1$ per step.

*Proof.* $G^t u_0 = \sum_j \lambda_j^t (q_j \cdot u_0) q_j$. Divide by $\lambda_1^t (q_1 \cdot u_0)$: the coefficient of $q_1$ is 1 and every other coefficient is at most $|q_j \cdot u_0| / |q_1 \cdot u_0| \cdot (\lambda_2/\lambda_1)^t$, which goes to 0. Normalizing gives the claim (see [power iteration](/power-iteration/)). A random Gaussian start has $q_1 \cdot u_0 \ne 0$ with probability 1. $\square$

The code fixes the sign so that the largest entry of $u$ is positive. The sign does not matter for line L6, since $u u^T = (-u)(-u)^T$.

**Theorem (removal).** For a unit vector $u$, line L6 returns $w_i = v_i - (u \cdot v_i) u$. Then (a) $w_i \cdot u = 0$, (b) $\|v_i\|^2 = (u \cdot v_i)^2 + \|w_i\|^2$, (c) removing again changes nothing, and (d) among all vectors of the form $v_i - c\, u$, the vector $w_i$ is the shortest.

*Proof.* (a) $w_i \cdot u = v_i \cdot u - (u \cdot v_i)(u \cdot u) = 0$. (b) $v_i = (u \cdot v_i) u + w_i$ with orthogonal terms, so the Pythagorean theorem applies. (c) By (a), $(u \cdot w_i) = 0$, so $w_i - 0 \cdot u = w_i$. (d) $\|v_i - c u\|^2 = \|w_i\|^2 + ((u \cdot v_i) - c)^2$ by (b) applied to $v_i - c u$, which is smallest at $c = u \cdot v_i$. $\square$

**Corollary.** After lines L1 to L7, every output vector is orthogonal to $u$, and $u$ is the direction in which the sentence vectors of line L2 have the largest sum of squared projections. If all sentence vectors of line L2 are equal, they all lie on $u$ and the output is the zero vector for every sentence. $\blacksquare$

The proof shows what the steps compute. That this improves the similarity of sentences is a measurement on benchmarks, not a theorem. The paper motivates the weights with a generative model and shows that, in that model, the maximum likelihood estimate of the discourse vector is close to the weighted average; that derivation uses approximations and is a heuristic argument.
