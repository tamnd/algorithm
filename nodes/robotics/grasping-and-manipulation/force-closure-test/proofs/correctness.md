---
title: The force-closure test decides whether the primitive wrenches positively span the wrench space
proves: [correctness]
status: full
---

We use the notation of the page. The primitive wrenches are $w_1, \ldots, w_N \in \mathbb{R}^d$, with $d = 3$ in the plane and $d = 6$ in space. They are the columns of the $d \times N$ matrix $F$. The set of wrenches that the contacts can apply is the cone $\operatorname{pos}(W) = \{F k : k \ge 0\}$, because each linearized friction cone is the set of nonnegative combinations of its edges, and the wrench map of one contact is linear. The linearized grasp is in force closure when $\operatorname{pos}(W) = \mathbb{R}^d$: each external wrench can be balanced by contact forces inside the linearized cones. We write $\mathbf{1}$ for the vector of $N$ ones, and $k > 0$ or $k \ge 1$ for an inequality in each component.

**Lemma 1 (algebraic form).** $\operatorname{pos}(W) = \mathbb{R}^d$ if and only if $\operatorname{rank} F = d$ and $F k = 0$ for some $k > 0$.

*Proof.* Assume $\operatorname{pos}(W) = \mathbb{R}^d$. Then $\operatorname{span}(W) \supseteq \operatorname{pos}(W) = \mathbb{R}^d$, so $\operatorname{rank} F = d$. The vector $-F\mathbf{1}$ is in $\operatorname{pos}(W)$, so $-F\mathbf{1} = F a$ for some $a \ge 0$. Then $k = \mathbf{1} + a$ has $k \ge \mathbf{1} > 0$ and $F k = 0$.

Conversely, assume $\operatorname{rank} F = d$ and $F k = 0$ with $k > 0$. Let $x \in \mathbb{R}^d$. Because the columns of $F$ span $\mathbb{R}^d$, there is a $z \in \mathbb{R}^N$ with $F z = x$, with entries of any sign. Let $t = \max(0, \max_i (-z_i / k_i))$. Then $z + t k \ge 0$, and $F(z + t k) = x + t \cdot 0 = x$. So $x \in \operatorname{pos}(W)$. $\square$

**Lemma 2 (scaling).** There is a $k > 0$ with $F k = 0$ if and only if there is a $y \ge 0$ with $F y = -F \mathbf{1}$.

*Proof.* If $F k = 0$ with $k > 0$, let $s = \min_i k_i > 0$. Then $k' = k / s$ has $k' \ge \mathbf{1}$ and $F k' = 0$, so $y = k' - \mathbf{1} \ge 0$ and $F y = -F\mathbf{1}$. Conversely, if $y \ge 0$ and $F y = -F\mathbf{1}$, then $k = \mathbf{1} + y \ge \mathbf{1} > 0$ and $F k = 0$. $\square$

**Lemma 3 (phase one).** PHASE-ONE$(A, b)$ stops. It returns a $y \ge 0$ with $A y = b$ if one exists, and NONE if none exists.

*Proof.* Line L10 multiplies some equations by $-1$. This does not change the set of solutions, and afterwards $b \ge 0$. Line L11 adds one artificial variable $a_i \ge 0$ to row $i$ and gives the auxiliary problem: minimize $\mathbf{1}^T a$ subject to $A y + a = b$, $y \ge 0$, $a \ge 0$. The point $y = 0$, $a = b$ is feasible, and it is the basic solution of the first basis (the artificial columns form an identity matrix). A point $y$ with $A y = b$ and $y \ge 0$ exists if and only if the optimal value of the auxiliary problem is $0$.

The loop of lines L12 to L17 is the simplex method on this problem. We use three standard facts about a simplex tableau. (a) A pivot is a sequence of row operations, so each tableau describes the same set of solutions as the system of line L11. (b) The ratio test of line L16 picks the row in which the entering variable first drives a basic variable to $0$, so the basic solution stays nonnegative. (c) For each feasible point $x$ (the vector of all $y$ and $a$ variables), the cost is $z_B + \sum_j r_j x_j$, where $z_B$ is the cost of the current basic solution and $r_j$ are the reduced costs of line L13. Fact (c) follows when one substitutes the tableau rows, which give each basic variable as a function of the nonbasic ones, into the cost; the reduced cost of a basic variable is $0$.

Line L16 always finds a row. If $r_q < 0$ and column $q$ has no positive entry, then $x_q$ can grow without limit while each basic variable stays nonnegative. By fact (c), the cost then goes to $-\infty$. But the cost $\mathbf{1}^T a$ is never negative, so this cannot happen.

The loop stops. Each pivot keeps the cost or lowers it. Bland's rule (line L15 for the entering index, and the ties of line L16 broken by the smallest basic index) never visits the same basis twice (Bland 1977). There are at most $\binom{N + d}{d}$ bases, so the loop makes finitely many pivots.

The loop exits at line L14 in one of two cases. If the cost of the basic solution is $0$, then every artificial variable is $0$, and the $y$ part satisfies $A y = b$, $y \ge 0$. If no reduced cost is negative, then by fact (c) each feasible point costs at least $z_B$, so $z_B$ is the optimal value. Line L18 then returns the $y$ part if $z_B = 0$, and NONE if $z_B > 0$. By the remark at the end of the first paragraph, both answers are correct. $\square$

**Theorem.** FORCE-CLOSURE returns CLOSED if and only if the linearized grasp is in force closure. When it returns CLOSED, the vector $k$ that it gives has $k \ge \mathbf{1}$ and $F k = 0$.

*Proof.* Lines L1 to L4 put into $W$ the wrench $(p_i \times f, f)$ of each edge $f$ of each linearized cone, so the columns of $F$ (line L5) are the primitive wrenches. If $\operatorname{rank} F < d$, the grasp is not in force closure by Lemma 1, and line L6 returns NOT CLOSED. Otherwise line L7 calls PHASE-ONE$(F, -F\mathbf{1})$. By Lemma 3 it returns a $y$ exactly when some $y \ge 0$ has $F y = -F\mathbf{1}$. By Lemma 2 this happens exactly when some $k > 0$ has $F k = 0$, and by Lemma 1 (with $\operatorname{rank} F = d$) exactly when the grasp is in force closure. Line L9 returns $k = \mathbf{1} + y$, and the proof of Lemma 2 shows that $k \ge \mathbf{1}$ and $F k = 0$. $\blacksquare$

**Corollary (convex hull form).** $\operatorname{pos}(W) = \mathbb{R}^d$ if and only if the origin is in the interior of the convex hull of $w_1, \ldots, w_N$.

*Proof.* If a ball $B(0, r)$ lies in $\operatorname{conv}(W)$, it lies in the cone $\operatorname{pos}(W)$. A cone that contains a ball about the origin is all of $\mathbb{R}^d$, because each $x \ne 0$ is a positive multiple of $r x / (2 \lVert x \rVert)$.

Conversely, let $\operatorname{pos}(W) = \mathbb{R}^d$. Lemma 1 gives $\operatorname{rank} F = d$ and $F k = 0$ with $k > 0$. Let $\lambda = k / (\mathbf{1}^T k)$. Then $\lambda > 0$, $\mathbf{1}^T \lambda = 1$ and $F \lambda = 0$. Let $F^+ = F^T (F F^T)^{-1}$, which exists because $F$ has rank $d$, and let $x \in \mathbb{R}^d$ with $\lVert x \rVert \le \rho$. Put $z = F^+ x$ and $\mu = \lambda + z - (\mathbf{1}^T z) \lambda$. Then $F \mu = 0 + x - 0 = x$ and $\mathbf{1}^T \mu = 1 + \mathbf{1}^T z - \mathbf{1}^T z = 1$. Each $\lvert z_i \rvert$ is at most $\lVert F^+ \rVert \rho$, so for $\rho$ small enough each $\mu_i > 0$. Then $x \in \operatorname{conv}(W)$, so the ball $B(0, \rho)$ lies in $\operatorname{conv}(W)$. $\square$

**What the test does not decide.** The theorem is about the linearized cones. Each edge that the code builds lies on the boundary of the true circular cone, so each pyramid lies inside its true cone. If the linearized grasp is in force closure, the true grasp is in force closure too, because its wrench cone is larger. The converse can be false in space: a grasp can be in force closure with the circular cones and not with the pyramids. In the plane a friction cone has exactly two edges, so the planar test is exact. With $\mu = 0$ each cone is the ray of the normal, and the test decides first-order form closure.

**Reference.** R. G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 103-107, 1977.
