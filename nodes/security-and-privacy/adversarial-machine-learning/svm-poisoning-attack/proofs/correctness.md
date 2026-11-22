---
title: The gradient of the validation hinge loss of a linear SVM in one training point, with the active sets held fixed
proves: [correctness]
status: full
---

**Setting.** Training points $x_1, \ldots, x_m$ with labels $y_i \in \{+1, -1\}$, of which the last, $c = m$, is the attack point. $Q_{ij} = y_i y_j \langle x_i, x_j \rangle$. The dual is $\min \tfrac{1}{2}\alpha^\top Q \alpha - \mathbf{1}^\top \alpha$ over $0 \le \alpha_i \le C$, $\sum_i y_i \alpha_i = 0$; it is a convex quadratic program, so the KKT conditions are necessary and sufficient. With $g_i = y_i(\langle w, x_i \rangle + b)$ and $w = \sum_i \alpha_i y_i x_i$ they read: $\sum_i y_i \alpha_i = 0$, and for each $i$, either $0 < \alpha_i < C$ and $g_i = 1$ (set $S$), or $\alpha_i = C$ and $g_i \le 1$ (set $E$), or $\alpha_i = 0$ and $g_i \ge 1$ (set $R$). The primal $w$ is unique, and $b$ is unique when $S \ne \emptyset$.

**Claim 1 (an affine solution on a region).** Fix a partition of the points into $S$, $E$, $R$ and $\{c\}$, with $S \neq \emptyset$, and fix $\alpha_c \in \{0, C\}$; so $c$ is an error vector or a rest point, but it is listed apart from $E$ and $R$. Let $K = \begin{pmatrix} Q_{SS} & y_S \\ y_S^\top & 0 \end{pmatrix}$ and assume $K$ is nonsingular. For $x_c \in \mathbb{R}^d$ define $(\alpha_S(x_c), b(x_c))$ as the solution of

$$K \begin{pmatrix} \alpha_S \\ b \end{pmatrix} = \begin{pmatrix} \mathbf{1} - Q_{SE}\, C\mathbf{1} - Q_{Sc}(x_c)\, \alpha_c \\ -\, y_E^\top C\mathbf{1} - y_c \alpha_c \end{pmatrix}, \tag{1}$$

with $\alpha_E = C$, $\alpha_R = 0$, and $w(x_c) = \sum_{i} \alpha_i y_i x_i$. Let $U$ be the set of $x_c$ where these values satisfy the KKT inequalities ($0 < \alpha_s < C$ on $S$, $g_i \le 1$ on $E$, $g_i \ge 1$ on $R$, including $i = c$). Then on $U$ the SVM solution is $(w(x_c), b(x_c))$, and $\alpha_S$, $b$ and $w$ are affine in $x_c$.

*Proof.* The rows of (1) for $s \in S$ say $\sum_j Q_{sj}\alpha_j + y_s b = 1$, which is $g_s = 1$; the last row is $\sum_i y_i \alpha_i = 0$. So on $U$ all KKT conditions hold, and by sufficiency the point is optimal; since $w$ is unique and $b$ is unique when $S \ne \emptyset$, it is the SVM solution. The matrix $K$ uses only $Q_{SS}$ and $y_S$, which do not involve $x_c$ because $c \notin S$. On the right side, only $Q_{Sc}(x_c)$ depends on $x_c$, and its entries $y_s y_c \langle x_s, x_c \rangle$ are linear in $x_c$. So $(\alpha_S, b) = K^{-1}(\text{right side})$ is affine in $x_c$. Finally $w = \sum_{s \in S} \alpha_s y_s x_s + C\sum_{e \in E} y_e x_e + \alpha_c y_c x_c$, a sum of affine functions. $\square$

**Claim 2 (the derivative).** On $U$, for each coordinate $j$,

$$\frac{\partial}{\partial x_{c,j}} \begin{pmatrix} \alpha_S \\ b \end{pmatrix} = -K^{-1}\begin{pmatrix} \big(\alpha_c y_c y_s x_{s,j}\big)_{s \in S} \\ 0 \end{pmatrix}, \qquad \frac{\partial w}{\partial x_c} = \sum_{s \in S} y_s x_s \Big(\frac{\partial \alpha_s}{\partial x_c}\Big)^{\!\top} + \alpha_c y_c I .$$

*Proof.* Differentiate (1) in $x_{c,j}$. $K$ is constant, and the derivative of the row $s$ of the right side is $-\alpha_c\, \partial Q_{sc}/\partial x_{c,j} = -\alpha_c y_s y_c x_{s,j}$; the last row is constant. Multiply by $K^{-1}$. For $w$, the terms of $E$ are constant, the term $\alpha_s y_s x_s$ has derivative $y_s x_s (\partial \alpha_s / \partial x_c)^\top$, and $\alpha_c y_c x_c$ has derivative $\alpha_c y_c I$ because $\alpha_c$ is constant. $\square$

**Claim 3 (the gradient of $L$).** Let $V^+ = \{k : y_k f(x_k) < 1\}$ and assume no validation point has $y_k f(x_k) = 1$. Then near such an $x_c$ in the interior of $U$, $L(x_c) = \sum_{k \in V^+} \big(1 - y_k(\langle w(x_c), x_k \rangle + b(x_c))\big)$ with $V^+$ fixed, and

$$\nabla L = -\sum_{k \in V^+} y_k \Big( \Big(\frac{\partial w}{\partial x_c}\Big)^{\!\top} x_k + \nabla b \Big),$$

which is what poison_gradient computes.

*Proof.* Each $y_k f(x_k)$ is a continuous (affine) function of $x_c$ by Claim 1, so a strict inequality $y_k f(x_k) \ne 1$ holds near $x_c$, and the set $V^+$ does not change there. On that neighborhood $L$ is a finite sum of affine functions, and the chain rule with Claim 2 gives the formula. Since $L$ is affine on the neighborhood, central finite differences inside it equal the gradient up to rounding, which the tests use. $\square$

**Claim 4 (flat regions).** If moreover $\lvert S \rvert = d + 1$ and the vectors $(x_s, 1) \in \mathbb{R}^{d+1}$, $s \in S$, are linearly independent, then $w$ and $b$ are constant on $U$, and $\nabla L = 0$.

*Proof.* On $U$, the $d + 1$ equations $y_s(\langle w, x_s \rangle + b) = 1$ for $s \in S$ hold, and they form a linear system in $(w, b) \in \mathbb{R}^{d+1}$ whose matrix has the rows $y_s (x_s, 1)$, which is nonsingular by the hypothesis. Its right side is $\mathbf{1}$, which does not depend on $x_c$, and no point of $S$ is the attack point, so the unique solution $(w, b)$ does not depend on $x_c$. Then $L$ is constant near $x_c$. $\square$

**The algorithm.** Line L5 moves $x_c$ along $\nabla L / \lVert \nabla L \rVert$, which is the direction of fastest increase of the affine function $L$ on the current region, and projects onto the box. Nothing more is claimed: when the step leaves the region the sets change, $L$ may fall, and line L6 stops; $L$ is not concave, so the result is not a global maximum. $\blacksquare$
