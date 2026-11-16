---
title: The distance gradient law decreases the formation error, keeps the centroid, and converges exponentially near an infinitesimally rigid target
proves: [correctness]
status: full
---

There are $r$ robots in the plane with positions $p_i \in \mathbb{R}^2$ and the model $\dot p_i = u_i$. The graph $G = (V, E)$ is fixed, undirected and connected, with $m$ edges, and each edge $\{i, j\}$ has a target distance $d_{ij} > 0$. Write $z_{ij} = p_i - p_j$, $e_{ij} = \lVert z_{ij} \rVert^2 - d_{ij}^2$, and $e \in \mathbb{R}^m$ for the vector of the $e_{ij}$. The potential is $V(p) = \frac14 \sum_{\{i,j\} \in E} e_{ij}^2 = \frac14 \lVert e \rVert^2$. The [rigidity matrix](/rigidity-matrix/) $R(p)$ is the $m \times 2r$ matrix whose row for the edge $\{i, j\}$ holds $z_{ij}^T$ in the columns of robot $i$ and $-z_{ij}^T$ in the columns of robot $j$. The target set is $\mathcal{E} = \{p : e(p) = 0\}$. Line numbers refer to the pseudocode on the [distance-based formation control](/distance-based-formation-control/) page.

**Lemma 1 (the law is a gradient flow).** Lines L4 to L8 compute $u_i = -\sum_{j \in N_i} e_{ij} z_{ij}$, and $u = -\nabla V(p) = -R(p)^T e(p)$.

*Proof.* $\nabla_{p_i} e_{ij} = 2 z_{ij}$ and $\nabla_{p_j} e_{ij} = -2 z_{ij}$. So $\nabla_{p_i} \frac14 e_{ij}^2 = \frac12 e_{ij} \nabla_{p_i} e_{ij} = e_{ij} z_{ij}$, and summing over the edges at $i$ gives $\nabla_{p_i} V = \sum_{j \in N_i} e_{ij} z_{ij}$. The block of $R^T e$ for robot $i$ is $\sum_{j \in N_i} e_{ij} z_{ij}$ by the definition of $R$, with the sign of $z_{ij} = -z_{ji}$ taken care of by the order of the edge. $\square$

**Lemma 2 (invariants).** The centroid $\frac1r \sum_i p_i$ is constant. If $Q$ is a rotation and $b$ a vector, the law maps $Q p_i + b$ to $Q u_i$. If all robots start on one line, they stay on that line.

*Proof.* Each edge adds $-e_{ij} z_{ij}$ to $u_i$ and $-e_{ij} z_{ji} = e_{ij} z_{ij}$ to $u_j$, so $\sum_i u_i = 0$ and the centroid does not move. Under $p_i \mapsto Q p_i + b$, $z_{ij} \mapsto Q z_{ij}$ and $e_{ij}$ does not change, so $u_i \mapsto Q u_i$. If all $p_i$ lie on a line $\ell$ through the point $c$ with direction $v$, each $z_{ij}$ is parallel to $v$, so each $u_i$ is parallel to $v$. The vector field restricted to the configurations on $\ell$ is the field of the same law in one dimension, which has a solution on $\ell$. The field is polynomial, so solutions are unique, and the solution from a point of $\ell^r$ is that one, which stays on $\ell$. $\square$

**Lemma 3 (descent and boundedness).** Along every solution, $\dot V = -\lVert \nabla V \rVert^2 \le 0$. Every solution exists for all $t \ge 0$, stays bounded, and approaches the set of critical points of $V$.

*Proof.* $\dot V = \nabla V^T \dot p = -\lVert \nabla V \rVert^2$. So $V(p(t)) \le V(p(0)) = V_0$, and each edge has $\lVert z_{ij} \rVert^2 \le d_{ij}^2 + 2 \sqrt{V_0}$. The graph is connected, so every robot is within $r - 1$ edges of every other, and with the fixed centroid of Lemma 2 all positions stay in a bounded set. So the solution exists for all time. The function $V$ is a [Lyapunov function](/lyapunov-function/) on that compact set, and the [LaSalle invariance principle](/lasalle-invariance-principle/) gives convergence to the largest invariant set in $\{\nabla V = 0\}$, which is the set of equilibria. $\square$

Lemma 3 does not say that the limit is in $\mathcal{E}$. Lemma 2 gives a counterexample: with the triangle graph and a collinear start, the robots never leave the line, so they cannot reach a target triangle of positive area. The robots then stop at a collinear equilibrium with $V > 0$.

**Lemma 4 (a local gradient inequality).** Let $p^*$ be in $\mathcal{E}$, and let the framework $(G, p^*)$ be [infinitesimally rigid](/infinitesimal-rigidity/) in the plane, that is, $\operatorname{rank} R(p^*) = 2r - 3$, with $r \ge 2$. Then there are a neighborhood $U$ of $p^*$ and a constant $c > 0$ such that $\lVert \nabla V(p) \rVert^2 \ge c \, V(p)$ for all $p \in U$.

*Proof.* An infinitesimally rigid framework is rigid (Asimow and Roth), so near $p^*$ the set $\mathcal{E}$ is the orbit of $p^*$ under the proper rigid motions of the plane. This orbit $\mathcal{O}$ is a smooth manifold of dimension 3 near $p^*$, because the points of $p^*$ are not all equal, and its tangent space at each of its points $q$ is the space of infinitesimal rigid motions, which is $\ker R(q)$ by infinitesimal rigidity. All points of $\mathcal{O}$ are congruent to $p^*$, so they have the same singular values of $R$; let $\sigma > 0$ be the smallest positive one.

For $p$ near $p^*$, let $q$ be a nearest point of $\mathcal{O}$ to $p$ and $\delta = p - q$. Then $\delta$ is normal to $\mathcal{O}$ at $q$, that is, $\delta \perp \ker R(q)$, so $\lVert R(q) \delta \rVert \ge \sigma \lVert \delta \rVert$ and $\lVert R(q)^T R(q) \delta \rVert \ge \sigma^2 \lVert \delta \rVert$. Since $e(q) = 0$ and $e_{ij}$ is quadratic in $p$, $e(p) = 2 R(q) \delta + s$, where $s_{ij} = \lVert \delta_i - \delta_j \rVert^2$, so $\lVert s \rVert \le C_1 \lVert \delta \rVert^2$. The matrix $R$ is linear in $p$, so $R(p) = R(q) + R(\delta)$ with $\lVert R(\delta) \rVert \le C_2 \lVert \delta \rVert$. Then

$$\nabla V(p) = R(p)^T e(p) = 2 R(q)^T R(q) \delta + R(q)^T s + R(\delta)^T e(p),$$

and the last two terms are at most $C_3 \lVert \delta \rVert^2$ in norm. So $\lVert \nabla V(p) \rVert \ge 2 \sigma^2 \lVert \delta \rVert - C_3 \lVert \delta \rVert^2 \ge \sigma^2 \lVert \delta \rVert$ when $\lVert \delta \rVert \le \sigma^2 / C_3$. Also $\lVert e(p) \rVert \le C_4 \lVert \delta \rVert$, so $V(p) \le \frac14 C_4^2 \lVert \delta \rVert^2$. Together, $\lVert \nabla V \rVert^2 \ge \sigma^4 \lVert \delta \rVert^2 \ge (4 \sigma^4 / C_4^2) V$. The constants are uniform on a small ball around $p^*$, because the nearest point $q$ is then close to $p^*$. $\square$

**Theorem (local exponential convergence).** Under the hypotheses of Lemma 4, there is a $\rho > 0$ such that every solution with $\lVert p(0) - p^* \rVert < \rho$ converges to a point $p_\infty \in \mathcal{E}$, and $V(p(t)) \le V(p(0)) e^{-c t}$. So every distance $\lVert p_i - p_j \rVert$ on an edge converges to $d_{ij}$ exponentially, and $p_\infty$ is congruent to $p^*$.

*Proof.* Choose a ball $B$ of radius $\beta$ around $p^*$ inside the set $U$ of Lemma 4. While $p(t)$ stays in $B$, $\dot V = -\lVert \nabla V \rVert^2 \le -c V$, so $V(t) \le V(0) e^{-c t}$. Also, where $V > 0$,

$$\frac{d}{dt} \sqrt{V} = \frac{\dot V}{2 \sqrt V} = -\frac{\lVert \nabla V \rVert^2}{2 \sqrt V} \le -\frac{\sqrt c}{2} \lVert \nabla V \rVert = -\frac{\sqrt c}{2} \lVert \dot p \rVert.$$

Integrating, the length of the path from time 0 to $t$ is at most $(2 / \sqrt c) \sqrt{V(p(0))}$. $V$ is continuous and $V(p^*) = 0$, so for $\rho$ small enough, $\rho + (2/\sqrt c) \sqrt{V(p(0))} < \beta$ whenever $\lVert p(0) - p^* \rVert < \rho$. Then the path never leaves $B$, the bound on $V$ holds for all $t$, and the path has finite length, so $p(t)$ converges to a point $p_\infty \in B$. By continuity, $V(p_\infty) = 0$, so $p_\infty \in \mathcal{E}$, and near $p^*$ the set $\mathcal{E}$ consists of the congruent copies of $p^*$. Each $e_{ij}(t)^2 \le 4 V(t)$, so each squared distance error decays at least like $e^{-c t / 2}$. $\blacksquare$

**What is not proved here.** The theorem is local: the size $\rho$ of the region depends on the target and is not computed. Krick, Broucke and Francis (2009) prove the same local stability with the center manifold theorem. A proof that almost every start converges to $\mathcal{E}$ is known only for special graphs, for example the triangle (Dörfler and Francis 2010), and the other equilibria, such as the collinear ones of Lemma 2, make a global result impossible. Convergence of every bounded solution to a single equilibrium, not only to the set of equilibria, follows from the Lojasiewicz inequality for the polynomial $V$; it is cited, not proved here.
