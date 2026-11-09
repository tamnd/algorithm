---
title: Benson's algorithm stops and returns the vertices of the upper image
proves: [correctness]
status: full
---

All objectives are minimized. The input is $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$ and $C \in \mathbb{R}^{p \times n}$, with $X = \{x : A x \geqq b\}$. We assume:

- (H1) $X$ is not empty;
- (H2) each objective $c_i^\top x$ is bounded below on $X$.

The upper image is $\mathcal{P} = C[X] + \mathbb{R}^p_+ = \{y : y \geqq C x \text{ for some } x \in X\}$. We write $e = (1, \ldots, 1) \in \mathbb{R}^p$. For $y, y' \in \mathbb{R}^p$, $y' \le y$ means $y'_i \le y_i$ for each $i$. The set $Y_N$ is the set of points $y \in C[X]$ such that no $y' \in C[X]$ has $y' \le y$ and $y' \ne y$. Let

$$\Delta = \{(u, v) \in \mathbb{R}^p \times \mathbb{R}^m : A^\top v = C^\top u,\ e^\top u = 1,\ u \geqq 0,\ v \geqq 0\}$$

be the feasible set of $\mathrm{D}_2(t)$. It does not depend on $t$. The linear programs are solved exactly, and line L6 returns an optimal basic solution, that is, a vertex of $\Delta$.

**Lemma 1 (the upper image).** $\mathcal{P}$ is a nonempty polyhedron, $\mathcal{P} + \mathbb{R}^p_+ = \mathcal{P}$, and its recession cone is $\mathbb{R}^p_+$.

*Proof.* $\mathcal{P}$ is the projection onto the $y$ coordinates of the polyhedron $\{(x, y) : A x \geqq b,\ C x \leqq y\}$, and the projection of a polyhedron is a polyhedron (Fourier and Motzkin elimination). It is not empty by (H1). If $y \geqq C x$ and $d \geqq 0$, then $y + d \geqq C x$, so $\mathcal{P} + \mathbb{R}^p_+ = \mathcal{P}$, and $\mathbb{R}^p_+$ is in the recession cone. Conversely, let $d$ be a recession direction and fix $y \in \mathcal{P}$. For each $\lambda > 0$ there is $x_\lambda \in X$ with $C x_\lambda \leqq y + \lambda d$. If $d_i < 0$ for some $i$, then $c_i^\top x_\lambda \le y_i + \lambda d_i \to -\infty$, which contradicts (H2). So $d \geqq 0$. $\square$

**Lemma 2 (the meaning of $\mathrm{D}_2$).** For every $t \in \mathbb{R}^p$, the program $\mathrm{D}_2(t)$ has an optimal solution, and its optimal value is

$$z^*(t) = \min\{z \in \mathbb{R} : t + z e \in \mathcal{P}\},$$

where the minimum exists. Moreover, $t \in \mathcal{P}$ if and only if $z^*(t) \le 0$.

*Proof.* Consider the linear program $\mathrm{P}_2(t)$: minimize $z$ over $(x, z)$ subject to $A x \geqq b$ and $C x - z e \leqq t$. A pair $(x, z)$ is feasible exactly when $x \in X$ and $C x \leqq t + z e$. So the set of feasible values of $z$ is $\{z : t + z e \in \mathcal{P}\}$. It is not empty: take any $x \in X$ and $z = \max_i (c_i^\top x - t_i)$. It is bounded below: let $y^I_i = \inf_{x \in X} c_i^\top x$, which is finite by (H2); then $t_i + z \ge c_i^\top x \ge y^I_i$, so $z \ge \max_i (y^I_i - t_i)$. A feasible linear program with a bounded objective has an optimal solution, so $z^*(t)$ is attained. Write the constraints as $A x \geqq b$ with multipliers $v \geqq 0$ and $-C x + z e \geqq -t$ with multipliers $u \geqq 0$. The variables $x$ and $z$ are free, so the dual constraints are equations: $A^\top v - C^\top u = 0$ for $x$, and $e^\top u = 1$ for $z$. The dual objective is $b^\top v - t^\top u$. This is $\mathrm{D}_2(t)$, and by the strong duality theorem of linear programming it has an optimal solution with the value $z^*(t)$.

If $t \in \mathcal{P}$, then $z = 0$ is feasible, so $z^*(t) \le 0$. If $z^*(t) \le 0$, then $t + z^*(t) e \in \mathcal{P}$ and $t = (t + z^*(t) e) + (-z^*(t)) e \in \mathcal{P}$ by Lemma 1. $\square$

**Lemma 3 (every point of $\Delta$ gives a valid inequality).** If $(u, v) \in \Delta$, then $u^\top y \ge b^\top v$ for every $y \in \mathcal{P}$.

*Proof.* Let $y \geqq C x$ with $x \in X$. Since $u \geqq 0$, $u^\top y \ge u^\top C x$. By $C^\top u = A^\top v$, $u^\top C x = v^\top A x$. Since $v \geqq 0$ and $A x \geqq b$, $v^\top A x \ge v^\top b$. $\square$

**Lemma 4 (the cut separates and supports).** Let $(u, v)$ be optimal for $\mathrm{D}_2(t)$ with the value $z > 0$. Then $u^\top t < b^\top v$, and the hyperplane $\{y : u^\top y = b^\top v\}$ meets $\mathcal{P}$ at the point $t + z e$.

*Proof.* The value is $z = b^\top v - t^\top u$, so $u^\top t = b^\top v - z < b^\top v$. By Lemma 2, $t + z e \in \mathcal{P}$, and $u^\top (t + z e) = u^\top t + z\, e^\top u = (b^\top v - z) + z = b^\top v$. $\square$

So the inequality $u^\top y \ge b^\top v$ holds on $\mathcal{P}$ by Lemma 3, is tight at a point of $\mathcal{P}$, and is violated by $t$. It is a supporting half-space of $\mathcal{P}$ that cuts $t$ off.

**Lemma 5 (the invariant).** At the start of each execution of line L4, $\mathcal{T}$ is a polyhedron with $\mathcal{P} \subseteq \mathcal{T}$, its recession cone is $\mathbb{R}^p_+$, and $\mathcal{T} = \operatorname{conv}(V) + \mathbb{R}^p_+$, where $V$ is its finite, nonempty set of vertices.

*Proof.* $\mathcal{T}$ is the set of solutions of a finite list of inequalities $h^\top y \ge \beta$. The first $p$ inequalities are $y_i \ge y^I_i$, where $y^I_i$ is the minimum of $c_i^\top x$ over $X$, computed in line L1; it exists by (H1) and (H2). Each holds on $\mathcal{P}$, since $y \geqq C x$ gives $y_i \ge c_i^\top x \ge y^I_i$. Each later inequality comes from a point of $\Delta$ and holds on $\mathcal{P}$ by Lemma 3. So $\mathcal{P} \subseteq \mathcal{T}$, and $\mathcal{T}$ is not empty.

The recession cone of $\mathcal{T}$ is $\{d : h^\top d \ge 0 \text{ for each inequality}\}$. Every $h$ is a unit vector or a vector $u \geqq 0$, so $\mathbb{R}^p_+$ is in the cone. The unit vectors force $d \geqq 0$, so the cone is exactly $\mathbb{R}^p_+$. It contains no line, so $\mathcal{T}$ is a pointed polyhedron. By the resolution theorem for pointed polyhedra (Minkowski and Weyl), $\mathcal{T}$ has finitely many vertices, at least one, and $\mathcal{T} = \operatorname{conv}(V) + \mathbb{R}^p_+$. $\square$

**Lemma 6 (no cut is added twice).** Two cuts added in line L7 come from different vertices of $\Delta$.

*Proof.* Suppose the vertex $(u, v)$ of $\Delta$ gives a cut in some round. From then on, $u^\top y \ge b^\top v$ is one of the inequalities of $\mathcal{T}$, so every later vertex $t'$ of $\mathcal{T}$ has $u^\top t' \ge b^\top v$. If $(u, v)$ were again the optimal solution for $t'$ with a value $z' > 0$, Lemma 4 would give $u^\top t' < b^\top v$. This is a contradiction. $\square$

**Theorem (termination).** Under (H1) and (H2), the algorithm stops after at most $|\operatorname{vert} \Delta|$ cuts.

*Proof.* Each round of the loop L3 either adds a cut in line L7 or returns in line L8. Each round is finite, since $V$ is finite by Lemma 5 and each linear program in line L6 has an optimal basic solution by Lemma 2. Each cut comes from a vertex of $\Delta$. The set $\Delta$ is a polyhedron that contains no line, because $u \geqq 0$ and $v \geqq 0$, so it has finitely many vertices. By Lemma 6 the cuts come from distinct vertices. So the number of rounds is at most $|\operatorname{vert} \Delta| + 1$. $\blacksquare$

**Theorem (correctness).** When the algorithm returns in line L8, $\mathcal{T} = \mathcal{P}$. So the returned inequalities describe $\mathcal{P}$, and the returned set $V$ is the set of vertices of $\mathcal{P}$.

*Proof.* The algorithm returns only when every $t \in V$ has $z^*(t) \le 0$. By Lemma 2, $V \subseteq \mathcal{P}$. The set $\mathcal{P}$ is convex and $\mathcal{P} + \mathbb{R}^p_+ = \mathcal{P}$ by Lemma 1, so $\operatorname{conv}(V) + \mathbb{R}^p_+ \subseteq \mathcal{P}$. By Lemma 5 the left side is $\mathcal{T}$, and $\mathcal{P} \subseteq \mathcal{T}$. So $\mathcal{T} = \mathcal{P}$, and the vertices of $\mathcal{T}$ are the vertices of $\mathcal{P}$. $\blacksquare$

It remains to link the output to the nondominated set.

**Lemma 7 (vertices are nondominated images).** Every vertex $y$ of $\mathcal{P}$ is in $Y_N$.

*Proof.* Since $y \in \mathcal{P}$, $y = C x + d$ with $x \in X$ and $d \geqq 0$. If $d \ne 0$, then $y - d = C x \in \mathcal{P}$ and $y + d \in \mathcal{P}$ by Lemma 1, and $y$ is the midpoint of these two different points of $\mathcal{P}$. A vertex is not such a midpoint, so $d = 0$ and $y = C x \in C[X]$. Suppose some $y' \in C[X]$ has $y' \le y$ and $y' \ne y$. Put $d' = y - y' \ne 0$, with $d' \geqq 0$. Then $y - d' = y' \in \mathcal{P}$ and $y + d' \in \mathcal{P}$, and again $y$ is their midpoint, which is impossible. So $y \in Y_N$. $\square$

**Lemma 8 (the nondominated points of $\mathcal{P}$).** A point $y$ is in $Y_N$ if and only if $y \in \mathcal{P}$ and no $y' \in \mathcal{P}$ has $y' \le y$ and $y' \ne y$.

*Proof.* Let $y \in Y_N$. Then $y \in C[X] \subseteq \mathcal{P}$. If $y' \in \mathcal{P}$ had $y' \le y$ and $y' \ne y$, take $x' \in X$ with $C x' \leqq y'$. Then $C x' \le y$ and $C x' \ne y$, since some coordinate of $y'$ is less than the same coordinate of $y$. This contradicts $y \in Y_N$. Conversely, let $y$ be a nondominated point of $\mathcal{P}$, and write $y = C x + d$ with $d \geqq 0$. The point $C x$ is in $\mathcal{P}$ and $C x \le y$, so $C x = y$, and $y \in C[X]$. No point of $C[X] \subseteq \mathcal{P}$ dominates $y$, so $y \in Y_N$. $\square$

By the correctness theorem and Lemmas 7 and 8, the algorithm returns the extreme points of the front, and the returned inequalities describe a polyhedron whose nondominated points are exactly $Y_N$. $\blacksquare$
