---
title: The linear program finds the largest independent contact regions for two fingers on two edges of a convex polygon
proves: [correctness]
status: full
---

We use the notation of the page. The polygon is convex and in counterclockwise order. Edge $e$ has the start point $A_e$, the direction $D_e$ and the inward normal $n_e$, which is $D_e$ turned by +90 degrees, so $\lvert n_e \rvert = \lvert D_e \rvert$. The point with parameter $t \in [0, 1]$ is $A_e + t D_e$. The friction coefficient is $\mu > 0$. The closed friction cone of edge $e$ is

$$C_e = \{\lambda_0 g_{e0} + \lambda_1 g_{e1} : \lambda_0, \lambda_1 \ge 0\}, \qquad \{g_{e0}, g_{e1}\} = \{n_e + \mu D_e,\ n_e - \mu D_e\},$$

with the two generators ordered so that $\operatorname{cross}(g_{e0}, g_{e1}) > 0$, where $\operatorname{cross}(a, b) = a_x b_y - a_y b_x$. Equivalently, $v \in C_e$ if and only if $\lvert v \cdot D_e \rvert \le \mu\, v \cdot n_e$. The cone is pointed: its half angle $\arctan \mu$ is less than 90 degrees. The fingers touch edge $i$ at $p_1(t_1) = A_i + t_1 D_i$ and edge $j \ne i$ at $p_2(t_2) = A_j + t_2 D_j$, and $d(t_1, t_2) = p_2 - p_1$. This map is affine in $(t_1, t_2)$.

**Lemma 1 (Nguyen's condition).** The contacts $p_1, p_2$ form a force-closure grasp if and only if $d \in \operatorname{int} C_i$ and $-d \in \operatorname{int} C_j$.

*Proof.* Let $W$ be the $3 \times 4$ matrix of the primitive wrenches $(\operatorname{cross}(p, g), g)$ of the four generators. By the characterization on the [force-closure test](/force-closure-test/) page, the grasp is in force closure if and only if $\operatorname{rank} W = 3$ and $W k = 0$ for some $k$ with all entries positive.

Assume $d \in \operatorname{int} C_i$ and $-d \in \operatorname{int} C_j$. Then $d = \lambda_0 g_{i0} + \lambda_1 g_{i1}$ and $-d = \nu_0 g_{j0} + \nu_1 g_{j1}$ with all four coefficients positive, because the interior of a two-generator cone is the set of strictly positive combinations. The forces $d$ at $p_1$ and $-d$ at $p_2$ have the sum 0 and the total moment $\operatorname{cross}(p_1, d) - \operatorname{cross}(p_2, d) = -\operatorname{cross}(d, d) = 0$, so $k = (\lambda_0, \lambda_1, \nu_0, \nu_1)$ is a positive null vector. For the rank, take moments about $p_1$; this multiplies $W$ by an invertible matrix. The two wrenches at $p_1$ become $(0, g_{i0})$ and $(0, g_{i1})$, which span all pure forces. The wrench of $g_{j0}$ at $p_2$ becomes $(\operatorname{cross}(d, g_{j0}), g_{j0})$. Here $\operatorname{cross}(d, g_{j0}) \ne 0$: if $g_{j0}$ were a positive multiple of $-d$, then $-d$ would be on the boundary of $C_j$, not in its interior, and if it were a positive multiple of $d$, then $C_j$ would contain both $d$ and $-d$, which a pointed cone does not. So the rank is 3.

Conversely, let the grasp be in force closure, with $W k = 0$ and $k > 0$. Let $f_1 = k_1 g_{i0} + k_2 g_{i1}$ and $f_2 = k_3 g_{j0} + k_4 g_{j1}$. These are in the interiors of $C_i$ and $C_j$, so they are not zero. The force rows give $f_1 + f_2 = 0$ and the moment row gives $\operatorname{cross}(p_1, f_1) + \operatorname{cross}(p_2, f_2) = -\operatorname{cross}(d, f_1) = 0$. If $d = 0$, all four wrenches have zero moment about $p_1$ and the rank is at most 2, which is false. So $d \ne 0$ and $f_1 = \lambda d$ for some $\lambda \ne 0$. The polygon is convex, so $p_2$ is in the closed inner half plane of edge $i$, and $d \cdot n_i \ge 0$. Every nonzero vector in $C_i$ has a positive normal part, so $f_1 \cdot n_i > 0$, and $\lambda < 0$ would give $d \cdot n_i < 0$. So $\lambda > 0$, $d = f_1 / \lambda \in \operatorname{int} C_i$ and $-d = f_2 / \lambda \in \operatorname{int} C_j$. $\square$

**Lemma 2 (the cone as two inequalities).** $v \in C_e$ if and only if $\operatorname{cross}(g_{e0}, v) \ge 0$ and $\operatorname{cross}(v, g_{e1}) \ge 0$.

*Proof.* The generators are a basis of the plane. Write $v = \lambda_0 g_{e0} + \lambda_1 g_{e1}$. Then $\operatorname{cross}(g_{e0}, v) = \lambda_1 \operatorname{cross}(g_{e0}, g_{e1})$ and $\operatorname{cross}(v, g_{e1}) = \lambda_0 \operatorname{cross}(g_{e0}, g_{e1})$, and $\operatorname{cross}(g_{e0}, g_{e1}) > 0$. $\square$

Lines L4 to L6 write, for each of the four corner pairs $(t_1, t_2) \in \{s_1, u_1\} \times \{s_2, u_2\}$, the inequalities of Lemma 2 for $d \in C_i$ and $-d \in C_j$. Each is affine in $(t_1, t_2)$, so it is a linear constraint on the variables $s_1, u_1, s_2, u_2$. Line L7 adds $0 \le s_e$, $u_e \le 1$ and $u_e - s_e \ge z$. Call a point of this program *feasible*.

**Lemma 3 (corners suffice).** $(s_1, u_1, s_2, u_2, z)$ with $z \ge 0$ is feasible if and only if $d(t_1, t_2) \in C_i \cap (-C_j)$ for every $(t_1, t_2)$ in the closed rectangle $R = [s_1, u_1] \times [s_2, u_2] \subseteq [0, 1]^2$, and $u_e - s_e \ge z$.

*Proof.* The rectangle is the convex hull of its four corners, and $d$ is affine, so $d(R)$ is the convex hull of the four corner images. The set $C_i \cap (-C_j)$ is convex. So it contains $d(R)$ if and only if it contains the corner images, which is what the constraints say by Lemma 2. $\square$

**Lemma 4 (the open rectangle is in the open cones).** Let $(s_1, u_1, s_2, u_2, z)$ be feasible with $z > 0$. Then every $(t_1, t_2)$ in the open rectangle $(s_1, u_1) \times (s_2, u_2)$ has $d \in \operatorname{int} C_i$ and $-d \in \operatorname{int} C_j$.

*Proof.* Let $v = d(t_1, t_2)$ and $P = d(R)$. Suppose $v \notin \operatorname{int} C_i$. By Lemma 3, $v \in C_i$, so $v$ is on the boundary of the convex cone $C_i$, and there is a linear function $\ell \ne 0$ with $\ell \ge 0$ on $C_i$ and $\ell(v) = 0$. Because $t_1$ can move a little both ways inside the rectangle, $v + \epsilon D_i$ and $v - \epsilon D_i$ are in $P \subseteq C_i$ for a small $\epsilon > 0$. So $\ell(v \pm \epsilon D_i) = \pm \epsilon\, \ell(D_i) \ge 0$, which forces $\ell(D_i) = 0$. Then $\ell(x) = \kappa\, x \cdot n_i$ for some $\kappa \ne 0$, and $\ell(n_i) = \kappa \lvert n_i \rvert^2 \ge 0$ because $n_i \in C_i$, so $\kappa > 0$. Now $\ell(v) = 0$ gives $v \cdot n_i = 0$, and $v \in C_i$ gives $\lvert v \cdot D_i \rvert \le \mu\, v \cdot n_i = 0$, so $v = 0$. Then $\epsilon D_i \in C_i$, which needs $\lvert \epsilon D_i \cdot D_i \rvert \le \mu\, \epsilon D_i \cdot n_i = 0$, a contradiction. The same argument with $-d$, the cone $C_j$ and the moves of $t_2$ gives $-v \in \operatorname{int} C_j$. $\square$

**Theorem.** Let $z^*$ be the optimum of the program of lines L1 to L8.

1. If $z^* > 0$, then the open intervals $(s_1, u_1)$ on edge $i$ and $(s_2, u_2)$ on edge $j$ returned by line L10 are independent contact regions: every choice of one contact in each gives force closure.
2. Every pair of intervals $I_1, I_2$ of parameters, open, closed or half open, that are independent contact regions has $\min(\lvert I_1 \rvert, \lvert I_2 \rvert) \le z^*$. So the returned regions maximize the smaller width.
3. If the program is infeasible or $z^* = 0$, then no pair of contacts on the two edges gives force closure, and line L9 correctly returns NONE.

*Proof.* Part 1 follows from Lemma 4 and Lemma 1.

Part 2. Let $I_1, I_2$ be independent regions with closures $[s_1, u_1]$ and $[s_2, u_2]$. By Lemma 1, every pair in $I_1 \times I_2$ has $d \in C_i \cap (-C_j)$. The set $C_i \cap (-C_j)$ is closed and $d$ is continuous, so every pair in the closed rectangle also satisfies it. By Lemma 3, the point $(s_1, u_1, s_2, u_2, \min(u_1 - s_1, u_2 - s_2))$ is feasible, so its last entry is at most $z^*$.

Part 3. Suppose some pair $(t_1, t_2)$ gives force closure. By Lemma 1, $d(t_1, t_2)$ is in the open set $\operatorname{int} C_i \cap (-\operatorname{int} C_j)$. By continuity there is $\epsilon > 0$ such that every pair in a square of side $\epsilon$ inside $[0, 1]^2$ with the corner $(t_1, t_2)$ also has this property; such a square exists even when $t_1$ or $t_2$ is 0 or 1. By Lemma 3, the square gives a feasible point with $z = \epsilon > 0$, so the program is feasible and $z^* > 0$. $\square$

**The solver.** The program is feasible or not, and it is bounded, because $0 \le s_e \le u_e \le 1$ and $z \le u_1 - s_1 \le 1$. The two-phase simplex method with Bland's smallest index rule cannot cycle (Bland 1977), so phase one stops with a zero cost exactly when the program is feasible, and phase two stops at an optimal basic solution. All arithmetic is in exact rationals, so the comparisons $z^* = 0$ and $z^* > 0$ in line L9 have no rounding error.
