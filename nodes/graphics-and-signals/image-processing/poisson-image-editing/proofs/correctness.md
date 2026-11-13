---
title: The discrete Poisson system of seamless cloning is a positive definite least squares system, and Gauss-Seidel and SOR solve it
proves: [correctness]
status: full
---

Let $\Omega$ be a set of $m$ pixels, $N_p$ the 4-neighbors of $p$ inside the image, $n_p = |N_p|$, and $t$ the target. A guidance is a number $v_{pq}$ for each ordered pair of neighbors with $v_{qp} = -v_{pq}$. Source differences $v_{pq} = g_p - g_q$ have this property, and so do mixed gradients, because the test $|t_p - t_q| > |g_p - g_q|$ is the same for $(p, q)$ and $(q, p)$ and both candidate values change sign. Order the pixels of $\Omega$ and let $A$ be the $m \times m$ matrix with $A_{pp} = n_p$, $A_{pq} = -1$ for $q \in N_p \cap \Omega$, and 0 elsewhere; let $b_p = \sum_{q \in N_p} v_{pq} + \sum_{q \in N_p \setminus \Omega} t_q$, as at line L2. The system (7) is $Af = b$ for the values of $f$ on $\Omega$.

**Claim 1 (least squares).** Let $\mathcal{E}$ be the set of unordered neighbor pairs $\{p, q\}$ with at least one pixel in $\Omega$, and

$$J(f) = \sum_{\{p, q\} \in \mathcal{E}} (f_p - f_q - v_{pq})^2, \qquad f_q = t_q \text{ for } q \notin \Omega.$$

Then $\nabla J(f) = 2(Af - b)$, so the minimizers of $J$ are the solutions of $Af = b$.

*Proof.* Each term is well defined because $(f_q - f_p - v_{qp})^2 = (f_p - f_q - v_{pq})^2$. For $p \in \Omega$, the terms that contain $f_p$ are those of the pairs $\{p, q\}$ with $q \in N_p$, and writing each from the side of $p$,

$$\frac{\partial J}{\partial f_p} = 2 \sum_{q \in N_p} (f_p - f_q - v_{pq}) = 2\Big(n_p f_p - \sum_{q \in N_p \cap \Omega} f_q - \sum_{q \in N_p \setminus \Omega} t_q - \sum_{q \in N_p} v_{pq}\Big) = 2(Af - b)_p.$$

$J$ is a convex quadratic, so its minimizers are its stationary points. $\square$

**Claim 2 (positive definite).** $A$ is symmetric, and for every $x \in \mathbb{R}^m$,

$$x^\top A x = \sum_{\{p, q\} \subseteq \Omega \text{ neighbors}} (x_p - x_q)^2 + \sum_{p \in \Omega} |N_p \setminus \Omega|\, x_p^2.$$

So $A$ is positive definite if and only if every 4-connected part of $\Omega$ has a pixel with a neighbor outside $\Omega$.

*Proof.* Symmetry: $q \in N_p$ if and only if $p \in N_q$. Split $n_p = |N_p \cap \Omega| + |N_p \setminus \Omega|$. Then $x^\top A x = \sum_p n_p x_p^2 - \sum_{p} \sum_{q \in N_p \cap \Omega} x_p x_q$. Each unordered pair inside $\Omega$ appears twice in the double sum, and $\sum_{\text{pairs}} (x_p - x_q)^2 = \sum_p |N_p \cap \Omega|\, x_p^2 - \sum_p \sum_{q \in N_p \cap \Omega} x_p x_q$, which gives the formula. Both sums are nonnegative. If $x^\top A x = 0$, the first sum makes $x$ constant on each 4-connected part of $\Omega$, and the second sum makes it zero at each pixel with an outside neighbor, so $x = 0$ on every part that has such a pixel. If every part has one, $A$ is positive definite. If a part $C$ has none, the vector that is 1 on $C$ and 0 elsewhere gives $x^\top A x = 0$, so $A$ is singular. $\square$

So under the condition checked by the implementation, $J$ has exactly one minimizer, $f^\ast = A^{-1} b$, and that is the output that Gauss-Seidel approaches.

**Claim 3 (one relaxed step).** Let $\Phi(x) = \frac12 x^\top A x - b^\top x$ and $r = b - Ax$. Lines L6 to L8 at pixel $p$ replace $x_p$ by $x_p + \omega r_p / n_p$, and this changes $\Phi$ by

$$-\tfrac12\, \omega (2 - \omega)\, \frac{r_p^2}{n_p}.$$

*Proof.* $(Ax)_p = n_p x_p - \sum_{q \in N_p \cap \Omega} x_q$, so the value of line L6 is $(b_p + \sum_q x_q)/n_p = x_p + r_p / n_p$, and line L7 moves $x_p$ by $\alpha = \omega r_p / n_p$. For any $\alpha$, $\Phi(x + \alpha e_p) - \Phi(x) = -\alpha r_p + \frac12 \alpha^2 n_p$. Substituting gives $-\omega r_p^2/n_p + \frac12 \omega^2 r_p^2 / n_p$. $\square$

**Claim 4 (convergence).** If $A$ is positive definite and $0 < \omega < 2$, the iterates of the loop of line L3 converge to $f^\ast$ from any start.

*Proof.* By Claim 3 every step lowers $\Phi$ by $c\, n_p \alpha^2$ with $c = (2 - \omega)/(2\omega) > 0$, where $\alpha$ is the size of the step, because $r_p^2/n_p = n_p \alpha^2/\omega^2$. $\Phi$ is bounded below by $\Phi(f^\ast)$ since $A$ is positive definite. So the sum of $\alpha^2$ over all steps is finite, and the step sizes go to 0.

Let $x^k$ be the iterate at the end of sweep $k$. For a pixel $p$, the residual $r_p$ at the time of its update in sweep $k$ is $n_p \alpha / \omega$, and each later step in the same sweep changes one neighbor of $p$ and so changes $r_p$ by at most the size of that step. There are at most $m$ such steps per sweep. So $|r_p(x^k)|$ is bounded by a constant times the largest step size of sweep $k$, which goes to 0. Then $x^k - f^\ast = -A^{-1} r(x^k) \to 0$. $\square$

**Error bound for a stop rule.** For any $f$, $\lVert f - f^\ast \rVert_2 \le \lVert b - Af \rVert_2 / \mu$, where $\mu > 0$ is the least eigenvalue of $A$. The test of line L9 bounds the size of the last steps, which by the argument of Claim 4 bounds the residual up to a factor that depends on $\omega$ and $\Omega$; it does not bound the error by $\varepsilon$ itself, and $\mu$ is small for a large region ($\mu$ is of order $1/k^2$ for a square of side $k$).

**Invariance to an offset.** With source differences, if $g = t + c$ on $\Omega$ and its neighbors for a constant $c$, then $v_{pq} = t_p - t_q$ and $f = t$ satisfies every equation: $n_p t_p - \sum_{q \in N_p \cap \Omega} t_q = \sum_{q \in N_p \setminus \Omega} t_q + \sum_{q \in N_p}(t_p - t_q)$. By uniqueness (Claim 2) the output is $t$.

**Cost.** Line L2 and each sweep visit every pixel of $\Omega$ once and look at at most four neighbors, so they take $\Theta(m)$ time; the arrays $n$, $b$ and the neighbor lists take $\Theta(m)$ space.
