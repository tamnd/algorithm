---
title: "The order 1 virtual element method is computable, consistent and stable, and it passes the patch test"
proves: [correctness]
status: partial
---

## Setting

Let $\Omega$ be a polygon and let the mesh $\mathcal T_h$ cover $\Omega$ by polygons $E$ that meet edge to edge. Each polygon $E$ has the vertices $v_1, \dots, v_m$ in counterclockwise order, with indices taken modulo $m$. The edge $e_i$ goes from $v_i$ to $v_{i+1}$, $|e_i|$ is its length and $n_i$ is its outward unit normal. Collinear vertices are allowed. The local space is

$$V_E = \{v \in H^1(E) : \Delta v = 0 \text{ in } E,\ v|_{\partial E} \text{ is continuous and linear on each edge}\},$$

$P_1$ is the set of linear polynomials, $h = h_E$ is the diameter of $E$, $(x_E, y_E)$ is the average of the vertices, and $m_1 = 1$, $m_2 = (x - x_E)/h$, $m_3 = (y - y_E)/h$. The matrices $D$, $B$, $G$, $P^*$, $P$ and $K_E$ are those of lines L2 to L5. The local form is

$$a^h_E(v, w) = \int_E \nabla \Pi^\nabla_E v \cdot \nabla \Pi^\nabla_E w\,dx + \tau \sum_{i=1}^m \big((I - \Pi^\nabla_E) v\big)(v_i)\,\big((I - \Pi^\nabla_E) w\big)(v_i),$$

and the global form is $a^h(v, w) = \sum_E a^h_E(v, w)$ on the space $V_h$ of functions on $\Omega$ whose restriction to each $E$ is in $V_E$.

## Lemma 1 (degrees of freedom)

The map from $v \in V_E$ to its vertex values $(v(v_1), \dots, v(v_m))$ is a bijection onto $\mathbb R^m$, and $P_1 \subset V_E$.

**Proof.** Given values $c_1, \dots, c_m$, there is exactly one continuous function $g$ on $\partial E$ that is linear on each edge and has $g(v_i) = c_i$. The Dirichlet problem $\Delta v = 0$ in $E$, $v = g$ on $\partial E$ has exactly one solution $v \in H^1(E)$, because $g$ is the trace of an $H^1$ function (it is Lipschitz on $\partial E$) and the Dirichlet form is coercive on $H^1_0(E)$. So each vector of values gives exactly one $v \in V_E$, and the values of $v$ give back $c$. A linear $p$ has $\Delta p = 0$ and is linear on each edge, so $p \in V_E$. $\square$

## Lemma 2 (the matrix B)

For $v \in V_E$ and $a = 2, 3$, $\int_E \nabla v \cdot \nabla m_a\,dx = \sum_{i=1}^m B_{ai}\,v(v_i)$.

**Proof.** $\nabla m_a$ is a constant vector and $\Delta m_a = 0$, so Green's formula gives

$$\int_E \nabla v \cdot \nabla m_a\,dx = \int_{\partial E} v\,\nabla m_a \cdot n\,ds = \sum_{i=1}^m (\nabla m_a \cdot n_i) \int_{e_i} v\,ds.$$

On $e_i$ the function $v$ is linear, so the trapezoid rule is exact: $\int_{e_i} v\,ds = \tfrac12 |e_i| (v(v_i) + v(v_{i+1}))$. Collect the terms of $v(v_i)$. It gets half of $e_{i-1}$ and half of $e_i$, so its coefficient is $\tfrac12 (|e_{i-1}| n_{i-1} + |e_i| n_i) \cdot \nabla m_a$, which is line L3. For a counterclockwise polygon and the edge from $p$ to $q$, $|e|\,n = (q_y - p_y,\ p_x - q_x)$. So $\tfrac12(|e_{i-1}| n_{i-1} + |e_i| n_i) = \tfrac12 (y_{i+1} - y_{i-1},\ x_{i-1} - x_{i+1})$, and with $\nabla m_2 = (1/h, 0)$ and $\nabla m_3 = (0, 1/h)$ this is the formula of the reference code. $\square$

## Lemma 3 (the projection)

$G = BD = \operatorname{diag}(1, |E|/h^2, |E|/h^2)$, so $G$ is nonsingular. For $v \in V_E$ with vertex values $\mathbf v$, the vector $P^* \mathbf v$ holds the coefficients of $\Pi^\nabla_E v$ in the basis $m_1, m_2, m_3$, and $P^* D = I$.

**Proof.** Column $a$ of $D$ holds the vertex values of $m_a$. Row 1 of $B$ is the vertex average, so $(BD)_{1a}$ is the vertex average of $m_a$. This is $1$ for $a = 1$ and $0$ for $a = 2, 3$, because $(x_E, y_E)$ is the vertex average. For $a = 2, 3$, Lemma 2 applied to $m_b \in V_E$ gives $(BD)_{ab} = \int_E \nabla m_b \cdot \nabla m_a\,dx$. This is $0$ for $b = 1$, $|E|/h^2$ for $b = a$ and $0$ for $b \ne a$, $b \ge 2$, because $\nabla m_2 \cdot \nabla m_3 = 0$. So $G$ is diagonal with positive entries when $|E| > 0$, which holds for a counterclockwise polygon.

Write $\Pi^\nabla_E v = \sum_b c_b m_b$. The two conditions that define $\Pi^\nabla_E$, tested with $p = m_2, m_3$ and with the vertex average, are the three equations $\sum_b (BD)_{ab} c_b = (B \mathbf v)_a$: for $a = 2, 3$ the left side is $\int_E \nabla \Pi^\nabla_E v \cdot \nabla m_a$ and the right side is $\int_E \nabla v \cdot \nabla m_a$ by Lemma 2, and for $a = 1$ both sides are vertex averages. A general linear $p$ is a combination of $m_1, m_2, m_3$, and $\nabla m_1 = 0$, so these equations are all the conditions. Hence $G c = B \mathbf v$ and $c = G^{-1} B \mathbf v = P^* \mathbf v$. Finally $P^* D = G^{-1} B D = G^{-1} G = I$. $\square$

So $P = D P^*$ maps the vertex values of $v$ to the vertex values of $\Pi^\nabla_E v$, and $P$ is a projection: $P^2 = D P^* D P^* = D P^* = P$.

## Lemma 4 (consistency)

For every $v \in V_E$ and every $p \in P_1$, $a^h_E(v, p) = \int_E \nabla v \cdot \nabla p\,dx$. In matrix form, $\mathbf v^\top K_E\, \mathbf p = \int_E \nabla v \cdot \nabla p\,dx$ where $\mathbf p = D c$ holds the vertex values of $p$.

**Proof.** $\Pi^\nabla_E p = p$, because $p$ satisfies both defining conditions. So $(I - \Pi^\nabla_E) p = 0$, and the stabilization term vanishes. In matrix form, $(I - P)\mathbf p = (I - D P^*) D c = D c - D c = 0$. The consistency part is $\int_E \nabla \Pi^\nabla_E v \cdot \nabla p\,dx$. By the definition of $\Pi^\nabla_E$ with the test polynomial $p$, $\int_E \nabla \Pi^\nabla_E v \cdot \nabla p = \int_E \nabla v \cdot \nabla p$. In matrix form, $\tilde G$ is $G$ with the first row set to zero, and since $\nabla m_1 = 0$ its entries are $\tilde G_{ab} = \int_E \nabla m_a \cdot \nabla m_b$ for all $a, b$. So $(P^* \mathbf v)^\top \tilde G (P^* \mathbf p) = \int_E \nabla \Pi^\nabla_E v \cdot \nabla \Pi^\nabla_E p$, which is the consistency part. $\square$

## Lemma 5 (stability of the local matrix)

$K_E$ is symmetric and positive semidefinite. For $\tau > 0$, $\mathbf v^\top K_E \mathbf v = 0$ only if $\mathbf v$ is a constant vector.

**Proof.** Both parts of $K_E$ have the form $M^\top S M$ with $S$ symmetric positive semidefinite ($\tilde G$ restricted to rows and columns 2 and 3 is $\operatorname{diag}(|E|/h^2, |E|/h^2)$, and its first row and column are zero), so $K_E$ is symmetric positive semidefinite. Suppose $\mathbf v^\top K_E \mathbf v = 0$. Both terms are nonnegative, so both vanish. The stabilization term is $\tau |(I - P)\mathbf v|^2$, so $\mathbf v = P \mathbf v = D P^* \mathbf v$, and $\mathbf v$ holds the vertex values of the linear polynomial $q = \Pi^\nabla_E v$. The consistency term is $\int_E |\nabla q|^2 = 0$, so $q$ is constant, and $\mathbf v$ is a constant vector. Constants do give zero, because their projection is the same constant. $\square$

## Theorem 1 (the global system)

Let the mesh be connected (every two polygons are joined by a chain of polygons that share edges) and let at least one vertex carry a boundary value. For $\tau > 0$ the global matrix restricted to the free vertices is symmetric positive definite. So line L7 has a unique solution, and conjugate gradients converge to it in exact arithmetic in at most as many steps as there are free vertices.

**Proof.** The global matrix $K = \sum_E A_E^\top K_E A_E$, where $A_E$ picks the vertex values of $E$ from the global vector, is symmetric positive semidefinite by Lemma 5. Let $\mathbf u$ be zero at the boundary vertices and $\mathbf u^\top K \mathbf u = 0$. Then every term $\mathbf u_E^\top K_E \mathbf u_E$ is zero, so $\mathbf u$ is constant on the vertices of each polygon, by Lemma 5. Two polygons that share an edge share its end vertices, so the constants agree, and by connectedness $\mathbf u$ is one constant everywhere. It is zero at a boundary vertex, so $\mathbf u = 0$. The restriction of $K$ to the free vertices is therefore positive definite. The statement about conjugate gradients is the standard finite termination property for symmetric positive definite systems. $\square$

## Theorem 2 (the patch test)

Let $f = 0$ and $g = p$ for a linear $p$. Then the vertex values of $p$ solve the global system of line L7, so the method returns $u_I = p(v_I)$ at every vertex and $\Pi^\nabla_E u_h = p$ on every polygon. This holds on every mesh that satisfies the assumptions of Theorem 1, for every $\tau > 0$, and convexity of the polygons is not used.

**Proof.** With $f = 0$ the load $F$ is zero. The free rows of $K\mathbf p = F$ say that $a^h(p, \varphi_I) = 0$ for every free vertex $I$, where $\varphi_I \in V_h$ has the value $1$ at vertex $I$ and $0$ at the others. Edge conformity means that two polygons that share an edge list the same vertices on it, so the traces of $\varphi_I$ from the two sides are the same piecewise linear function on the edge, and $\varphi_I$ is continuous across the edge. Hence $\varphi_I \in H^1(\Omega)$, and it vanishes on $\partial \Omega$ because $I$ is a free vertex. By Lemma 4 on each polygon,

$$a^h(p, \varphi_I) = \sum_E a^h_E(\varphi_I, p) = \sum_E \int_E \nabla \varphi_I \cdot \nabla p\,dx = \int_\Omega \nabla \varphi_I \cdot \nabla p\,dx = -\int_\Omega \varphi_I\, \Delta p\,dx = 0,$$

by integration by parts with $\varphi_I = 0$ on $\partial\Omega$ and $\Delta p = 0$. So $\mathbf p$ solves the free rows, and it has the right boundary values. By Theorem 1 the solution is unique, so the method returns $\mathbf p$. By Lemma 3 the projection of $p$ on each polygon is $p$. $\square$

On a triangle $P_1 = V_E$ by Lemma 1, since both have dimension 3. Then $P = I$, the stabilization vanishes for every $\tau$, and $K_E$ is the stiffness matrix of the linear Lagrange element. So on a triangle mesh the method is the linear finite element method.

## Theorem 3 (abstract error estimate)

Let $u \in H^1(\Omega)$ solve $-\Delta u = f$ with $u = g$ on $\partial\Omega$, and let $u_h \in V_h$ be the discrete solution, with $u_h = u_I$ at the boundary vertices for an interpolant $u_I \in V_h$ of $u$. Assume stability: there are constants $0 < \alpha \le \alpha^*$ such that for every polygon $E$ and every $v \in V_E$,

$$\alpha\, |v|_{1,E}^2 \le a^h_E(v, v) \le \alpha^* |v|_{1,E}^2.$$

Let $u_\pi$ be any function that is linear on each polygon (it need not be continuous), and write $|w|_{1,h}^2 = \sum_E |w|_{1,E}^2$ for such functions. Let $F_h$ be the discrete load, with $\|F - F_h\|_{V_h'} = \sup_{v \in V_h^0} |(f, v) - F_h(v)| / |v|_1$, where $V_h^0$ is the subspace of $V_h$ that vanishes on $\partial\Omega$. Then

$$|u - u_h|_1 \le C\,\big(|u - u_I|_1 + |u - u_\pi|_{1,h} + \|F - F_h\|_{V_h'}\big),$$

with $C$ depending only on $\alpha$ and $\alpha^*$.

**Proof.** Let $\delta = u_h - u_I \in V_h^0$. By the lower stability bound and the discrete equation $a^h(u_h, \delta) = F_h(\delta)$,

$$\alpha |\delta|_1^2 \le a^h(\delta, \delta) = F_h(\delta) - \sum_E a^h_E(u_I, \delta).$$

On each $E$, add and subtract $u_\pi|_E \in P_1$ and use Lemma 4 with the polynomial $u_\pi$:

$$a^h_E(u_I, \delta) = a^h_E(u_I - u_\pi, \delta) + \int_E \nabla u_\pi \cdot \nabla \delta = a^h_E(u_I - u_\pi, \delta) + \int_E \nabla (u_\pi - u) \cdot \nabla \delta + \int_E \nabla u \cdot \nabla \delta.$$

The sum over $E$ of the last terms is $\int_\Omega \nabla u \cdot \nabla \delta = (f, \delta)$, since $\delta \in H^1_0(\Omega)$ by edge conformity. So

$$\alpha |\delta|_1^2 = \big(F_h(\delta) - (f, \delta)\big) - \sum_E a^h_E(u_I - u_\pi, \delta) - \sum_E \int_E \nabla(u_\pi - u) \cdot \nabla \delta.$$

The local form is symmetric and positive semidefinite, so Cauchy-Schwarz and the upper bound give $|a^h_E(w, \delta)| \le \alpha^* |w|_{1,E} |\delta|_{1,E}$ for $w, \delta \in V_E$. The function $u_I - u_\pi$ is in $V_E$ on each $E$, since $P_1 \subset V_E$. Hence

$$\alpha |\delta|_1^2 \le \Big(\|F - F_h\|_{V_h'} + \alpha^* |u_I - u_\pi|_{1,h} + |u - u_\pi|_{1,h}\Big) |\delta|_1.$$

Divide by $|\delta|_1$ (the case $\delta = 0$ is trivial) and use $|u_I - u_\pi|_{1,h} \le |u_I - u|_1 + |u - u_\pi|_{1,h}$. This gives $|\delta|_1 \le \big(\|F - F_h\|_{V_h'} + \alpha^* |u - u_I|_1 + (1 + \alpha^*) |u - u_\pi|_{1,h}\big)/\alpha$. Then $|u - u_h|_1 \le |u - u_I|_1 + |\delta|_1$ gives the bound with the common constant $C = 1 + (1 + \alpha^*)/\alpha$. $\square$

## Remark 1 (what the reference code computes)

The code builds $K_E$ from lines L2 to L5 with exactly the matrices of Lemmas 2 and 3, and the load from $F_E[i] = \int_E f\, \Pi^\nabla_E \varphi_i$ with a quadrature rule. With $f = 0$ this load is zero, so Theorem 2 applies to the code up to rounding and the stopping test of conjugate gradients. The tests check the hand computed matrix of the unit square, the identity $P^* D = I$ on random polygons with 3 to 9 vertices, Lemma 4 as $\mathbf v^\top K_E \mathbf p = |E|\,\nabla \Pi^\nabla_E v \cdot \nabla p$, the symmetry of $K_E$ and the constants in its kernel, the reduction to the linear element on a triangle, and the patch test on a jittered mesh with hanging nodes for $\tau = 0.1$, $1$ and $10$.

## Remark 2 (rates, cited)

Theorem 3 reduces the convergence rate to three approximation results: an interpolation estimate in $V_h$, a polynomial approximation estimate on each polygon, and a bound for the load error. Under the mesh assumptions of the 2013 paper of Beirão da Veiga, Brezzi, Cangiani, Manzini, Marini and Russo (each $E$ star shaped with respect to a disc of radius at least $\rho h_E$, and each edge of length at least $\rho h_E$, for a fixed $\rho > 0$), these give $|u - u_h|_1 = O(h)$ for $u \in H^2(\Omega)$, and on convex $\Omega$ a duality argument gives $O(h^2)$ in $L^2$. The same assumptions give the stability bounds $\alpha$ and $\alpha^*$ for the dofi-dofi stabilization, with constants that depend on $\rho$ and $\tau$. This proof does not reproduce these estimates. They are taken from the 2013 paper and the 2023 survey in Acta Numerica, and the reference tests only observe them numerically. That is why the status of this proof is partial.
