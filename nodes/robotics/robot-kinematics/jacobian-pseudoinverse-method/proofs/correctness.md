---
title: PSEUDOINVERSE-IK takes least norm least squares steps and converges quadratically near a solution
proves: [correctness]
status: full
---

We use the notation of the page.
All vector norms are Euclidean, and the norm of a matrix is its largest singular value.
The proof is in exact arithmetic, in the real RAM.

The loop of the page has the form

$$q_{k+1} = q_k + J(q_k)^{+}\,G(q_k),$$

where $G : \mathbb{R}^n \to \mathbb{R}^m$ is the error and $J$ is the matching Jacobian.
For the position task, $G(q) = x_d - f(q)$ and $J = Df$, so $DG = -J$.
For the pose task, $G(q) = \log(T(q)^{-1}T_d)$ is the body twist error and $J = J_b$.
Line L4 returns as soon as $G$ is below the tolerance, and line L7 returns FAILURE after $k_{\max}$ iterations, so the loop always stops; the content of the proof is what one step does and when the iterates converge.

## The step

**Lemma 1 (Penrose).** For every $m \times n$ matrix $J$ and every $e \in \mathbb{R}^m$, the vector $\Delta = J^{+}e$ minimizes $|J\Delta - e|$, and among all minimizers it is the unique one of least norm.

*Proof.*
Let $J = U\Sigma V^{\mathsf T}$ be a singular value decomposition with the nonzero singular values $\sigma_1, \dots, \sigma_r$, and $J^{+} = V\Sigma^{+}U^{\mathsf T}$, where $\Sigma^{+}$ is the $n \times m$ matrix with the entries $1/\sigma_i$ for $i \le r$ and zeros elsewhere.
Put $y = V^{\mathsf T}\Delta$ and $c = U^{\mathsf T}e$.
Since $U$ and $V$ are orthogonal, $|J\Delta - e|^2 = |\Sigma y - c|^2 = \sum_{i \le r}(\sigma_i y_i - c_i)^2 + \sum_{i > r} c_i^2$ and $|\Delta| = |y|$.
The first sum is zero exactly when $y_i = c_i/\sigma_i$ for $i \le r$, and the second does not depend on $y$, so the minimizers are the $y$ with these $r$ entries and any other entries.
The one of least norm has $y_i = 0$ for $i > r$, that is $y = \Sigma^{+}c$, and $\Delta = V\Sigma^{+}U^{\mathsf T}e = J^{+}e$.
$\square$

**Corollary 2.** If $J$ has rank $m$, then $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$, $JJ^{+} = I$, and $J^{+}e$ is the least norm solution of $J\Delta = e$.
If $J$ has rank $n$, then $J^{+} = (J^{\mathsf T}J)^{-1}J^{\mathsf T}$ and $J^{+}J = I$.
In both cases $\|J^{+}\| = 1/\sigma_{\min}$, the inverse of the smallest singular value of $J$.

*Proof.*
With rank $m$, $r = m$ and $\Sigma^{+}$ is the transpose of $\Sigma$ with the entries inverted, so $JJ^{+} = U\Sigma\Sigma^{+}U^{\mathsf T} = I$, and the formulas follow by expanding $J^{\mathsf T}(JJ^{\mathsf T})^{-1} = V\Sigma^{\mathsf T}(\Sigma\Sigma^{\mathsf T})^{-1}U^{\mathsf T} = V\Sigma^{+}U^{\mathsf T}$.
The case of rank $n$ is the same with $J^{\mathsf T}J$.
The singular values of $J^{+}$ are the $1/\sigma_i$.
$\square$

For a square invertible $J$ the step is $J^{-1}G$, the Newton step for $G(q) = 0$.

## The error map of the pose task

**Lemma 3.** Let $S(q) = T(q)^{-1}T_d$, and suppose that on a set $\Omega$ the rotation angle of $S(q)$ stays below $\pi$, so that $G(q) = \log S(q)$ is a smooth function.
Then $DG(q) = -A(q)\,J_b(q)$, where $A(q) = \mathcal J_l(G(q))^{-1}$ and $\mathcal J_l$ is the left Jacobian of SE(3).
$A$ is smooth, $A = I$ where $G = 0$, and on a compact part of $\Omega$ there is a constant $L$ with $\|A(q) - I\| \le L|G(q)|$.

*Proof.*
By the definition of the body Jacobian, $T(q)^{-1}\,\partial T/\partial q_i = [J_{b,i}(q)]$, the matrix of column $i$ of $J_b$.
So $\partial S/\partial q_i = -T^{-1}(\partial T/\partial q_i)T^{-1}T_d = -[J_{b,i}]\,S$: a change of $q$ multiplies $S$ on the left by $\exp(-[J_b\,dq])$ to first order.
The derivative of $\log$ at $S = e^{[V]}$ in the direction of a left perturbation $e^{[\xi]}S$ is $\mathcal J_l(V)^{-1}\xi$; this is the definition of the left Jacobian, which is a smooth, invertible matrix function of $V$ for rotation angles below $2\pi$, with $\mathcal J_l(0) = I$.
With $\xi = -J_b\,dq$ this gives $DG = -\mathcal J_l(G)^{-1}J_b$.
The map $V \mapsto \mathcal J_l(V)^{-1}$ is smooth with the value $I$ at $V = 0$, so it is Lipschitz on a compact set, which gives $L$.
$\square$

For the position task, $A = I$ and $L = 0$.
So both tasks fit the same frame: $DG = -AJ$ with $\|A - I\| \le L|G|$.

## Full row rank

Make these assumptions on a closed ball $B = \{q : |q - q_0| \le R\}$.

- (B1) $J(q)$ has rank $m$ and $\sigma_m(J(q)) \ge \sigma_0 > 0$ for $q \in B$.
- (B2) $|G(q + \delta) - G(q) - DG(q)\delta| \le \tfrac{H}{2}|\delta|^2$ whenever $q$ and $q + \delta$ are in $B$.
- (B3) $DG = -AJ$ on $B$ with $\|A(q) - I\| \le L|G(q)|$.

Let $C = L + H/(2\sigma_0^2)$ and $\theta = C|G(q_0)|$.

**Theorem 4.** If $\theta < 1$ and $R \ge |G(q_0)|/(\sigma_0(1 - \theta))$, then all iterates lie in $B$, $C|G(q_k)| \le \theta^{2^k}$, and $q_k$ converges to a point $q^* \in B$ with $G(q^*) = 0$.

*Proof.*
Write $G_k = G(q_k)$, $J_k = J(q_k)$ and $\delta_k = J_k^{+}G_k$.

*One step.* If $q_k$ and $q_{k+1}$ are in $B$, then by (B2), (B3) and $J_kJ_k^{+} = I$ (Corollary 2),

$$G_{k+1} = G_k - A(q_k)J_k\delta_k + r_k = (I - A(q_k))G_k + r_k, \qquad |r_k| \le \tfrac{H}{2}|\delta_k|^2.$$

With $|\delta_k| \le |G_k|/\sigma_0$ (Corollary 2 and (B1)), $|G_{k+1}| \le L|G_k|^2 + \tfrac{H}{2\sigma_0^2}|G_k|^2 = C|G_k|^2$.

*Induction.* We show by induction on $k$ that $q_0, \dots, q_k \in B$ and $C|G_j| \le \theta^{2^j}$ for $j \le k$.
For $k = 0$ this is the definition of $\theta$, and $q_0 \in B$.
Suppose it holds for $k$.
For $j \le k$, $|\delta_j| \le |G_j|/\sigma_0 \le \theta^{2^j - 1}|G_0|/\sigma_0$, because $C|G_j| \le \theta^{2^j}$ and $C|G_0| = \theta$ give $|G_j| \le \theta^{2^j - 1}|G_0|$ when $C > 0$; when $C = 0$, the one-step bound gives $G_j = 0$ for $j \ge 1$, and the same inequality holds with $\theta^0 = 1$.
Since $2^j - 1 \ge j$,

$$|q_{k+1} - q_0| \le \sum_{j=0}^{k}|\delta_j| \le \frac{|G_0|}{\sigma_0}\sum_{j \ge 0}\theta^j = \frac{|G_0|}{\sigma_0(1 - \theta)} \le R,$$

so $q_{k+1} \in B$.
Then the one-step bound applies, and $C|G_{k+1}| \le (C|G_k|)^2 \le \theta^{2^{k+1}}$.

*Limit.* The same sum shows that $\sum_j|\delta_j|$ converges, so $q_k$ is a Cauchy sequence with a limit $q^* \in B$, since $B$ is closed.
$G$ is continuous and $G(q_k) \to 0$, so $G(q^*) = 0$.
$\square$

So the error falls quadratically, $|G_{k+1}| \le C|G_k|^2$, and the total joint motion is at most $|G(q_0)|/(\sigma_0(1 - \theta))$.
The limit is a solution in $B$, but it need not be the solution nearest to $q_0$.

## Full column rank

**Theorem 5.** Suppose $G(q^*) = 0$, and on the closed ball $B^* = \{q : |q - q^*| \le R\}$: $J(q)$ has rank $n$ with $\sigma_n(J(q)) \ge \sigma_0 > 0$ and $\|J(q)\| \le \Gamma_J$; $\|DG(q)\| \le \Gamma$; (B2) holds; and (B3) holds.
Let $D = (L\Gamma\Gamma_J + H/2)/\sigma_0$.
If $q_0 \in B^*$ and $D|q_0 - q^*| < 1$, then $|q_{k+1} - q^*| \le D|q_k - q^*|^2$ for every $k$, and $q_k \to q^*$.

*Proof.*
Let $q = q_k \in B^*$ and $h = q^* - q$.
By (B2) on the segment from $q$ to $q^*$, $0 = G(q^*) = G(q) + DG(q)h + r$ with $|r| \le \tfrac{H}{2}|h|^2$, so $G(q) = A(q)J(q)h - r$.
By Corollary 2, $J^{+}J = I$, so

$$\delta = J^{+}G(q) = h + J^{+}(A(q) - I)J h - J^{+}r.$$

By the mean value inequality, $|G(q)| = |G(q) - G(q^*)| \le \Gamma|h|$, so $\|A(q) - I\| \le L\Gamma|h|$.
Hence $|q + \delta - q^*| = |\delta - h| \le \frac{1}{\sigma_0}\big(L\Gamma|h|\,\Gamma_J|h| + \tfrac{H}{2}|h|^2\big) = D|h|^2$.
If $D|h| < 1$, then $|q_{k+1} - q^*| \le D|h|^2 < |h| \le R$, so $q_{k+1} \in B^*$ and $D|q_{k+1} - q^*| < D|h| < 1$.
By induction the bound holds for every $k$, and $D|q_k - q^*| \le (D|q_0 - q^*|)^{2^k} \to 0$.
$\square$

For a square $J$ both theorems apply, and Theorem 5 is the classical local quadratic convergence of Newton's method.

## What the theorems do not give

Both results are local.
They need a start where the error is small compared with $\sigma_0^2/H$, and they say nothing about starts far from every solution, about targets out of reach, or about singular solutions where $\sigma_0 = 0$.
In those cases the iteration can move far, cycle, or approach a singular configuration where the steps blow up, and the loop of the page ends with FAILURE after $k_{\max}$ iterations.
