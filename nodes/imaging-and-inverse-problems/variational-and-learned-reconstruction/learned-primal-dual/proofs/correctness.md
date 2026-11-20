---
title: "With the Chambolle-Pock update maps, learned primal-dual is the Chambolle-Pock algorithm, and with the gradient maps it is Landweber iteration"
proves: [correctness]
status: full
---

**Setting.** $A \in \mathbb{R}^{m \times n}$ is linear, $y \in \mathbb{R}^m$ is the data, and the scheme of lines L1 to L5 runs $K$ steps. The primal state is $x = (x^{(1)}, \ldots, x^{(N_p)})$ with $x^{(j)} \in \mathbb{R}^n$, and the dual state is $h = (h^{(1)}, \ldots, h^{(N_d)})$ with $h^{(j)} \in \mathbb{R}^m$. Step $i$ is

$$h_i = \Gamma_i\big(h_{i-1}, A x^{(2)}_{i-1}, y\big),\qquad x_i = \Lambda_i\big(x_{i-1}, A^T h^{(1)}_i\big),$$

and the output is $x^{(1)}_K$. For $N_p = 1$ the operator is applied to $x^{(1)}$. Because $A$ is linear, the adjoint of its derivative at any point is $A^T$; this is the case in which Algorithm 3 of Adler and Oktem (2018) uses $A^T$.

Nothing is proved here about trained maps $\Gamma_i$ and $\Lambda_i$. The two statements below are about special choices of the maps. They show that the scheme contains two classical methods, and that the code is correct on these choices.

**Chambolle-Pock.** Let $F$ and $G$ be closed proper convex functions, with $F = F_y$ depending on the data, and fix $\tau, \sigma > 0$ and $\theta \in [0, 1]$. Chambolle-Pock for $\min_x F_y(Ax) + G(x)$, started at $x^0$, $\bar x^0 = x^0$ and $h^0$, is

$$h^{i} = \operatorname{prox}_{\sigma F_y^*}(h^{i-1} + \sigma A\bar x^{i-1}),\qquad x^{i} = \operatorname{prox}_{\tau G}(x^{i-1} - \tau A^Th^{i}),\qquad \bar x^{i} = x^{i} + \theta(x^{i} - x^{i-1}).$$

Take $N_p = 2$, $N_d = 1$ and, for every $i$,

$$\Gamma_i(h, z, y) = \operatorname{prox}_{\sigma F_y^*}(h + \sigma z),\qquad \Lambda_i\big((u, v), w\big) = \big(p,\ (1 + \theta)p - \theta u\big)\ \text{ with } p = \operatorname{prox}_{\tau G}(u - \tau w).$$

**Claim 1.** If the scheme starts at $x_0 = (x^0, x^0)$ and $h_0 = h^0$, then $x_i = (x^i, \bar x^i)$ and $h_i = h^i$ for every $i \ge 0$. In particular the output $x^{(1)}_K$ is the Chambolle-Pock iterate $x^K$.

*Proof.* By induction on $i$. For $i = 0$ the claim is the choice of the start, since $\bar x^0 = x^0$. Suppose it holds for $i - 1$. Line L3 computes $h_i = \Gamma_i(h^{i-1}, A\bar x^{i-1}, y) = \operatorname{prox}_{\sigma F_y^*}(h^{i-1} + \sigma A\bar x^{i-1}) = h^i$. Line L4 computes $p = \operatorname{prox}_{\tau G}(x^{i-1} - \tau A^Th^i) = x^i$, and the second component $(1 + \theta)x^i - \theta x^{i-1} = x^i + \theta(x^i - x^{i-1}) = \bar x^i$. So $x_i = (x^i, \bar x^i)$.

**Consequence.** With $\theta = 1$ and $\tau\sigma\|A\|^2 < 1$, if a saddle point exists, the Chambolle-Pock iterates converge to a saddle point and the averages have a primal-dual gap of $O(1/K)$ (Chambolle and Pock 2011, Theorem 1; see [Chambolle-Pock algorithm](/chambolle-pock-algorithm/)). By Claim 1, learned primal-dual with these maps inherits both results. The test `test_cp_maps_give_chambolle_pock_on_a_matrix` compares the code with a direct Chambolle-Pock loop and finds equal iterates to $10^{-12}$.

**Gradient descent.** Take $N_p = N_d = 1$, $\Gamma_i(h, z, y) = z - y$ and $\Lambda_i(x, w) = x - \omega w$ for a step $\omega > 0$.

**Claim 2.** The output after $K$ steps is the $K$-th iterate of Landweber iteration $x \leftarrow x - \omega A^T(Ax - y)$ from the same start.

*Proof.* Line L3 sets $h_i = Ax_{i-1} - y$, the residual, and line L4 sets $x_i = x_{i-1} - \omega A^T(Ax_{i-1} - y)$. This is one Landweber step, so induction on $i$ gives the claim. Landweber converges to the minimum norm least squares solution for $x_0 = 0$ and $0 < \omega < 2/\|A\|^2$ (see [Landweber iteration](/landweber-iteration/)). With $A = 1$, $y = 1$, $\omega = 0.01$ and $K = 100$ the output is $1 - 0.99^{100} = 0.63397$, the Landweber filter factor at $\omega\sigma^2 = 0.01$; the test checks this value.

**What this does not prove.** Adler and Oktem argue that, since the scheme contains these methods, a trained scheme with the same number of steps should do at least as well as they do. This is a heuristic. It needs the network class to contain or approximate the maps above, and it needs training to find the best maps, which a nonconvex training problem does not guarantee. Measured comparisons are reported on the page as measurements.
