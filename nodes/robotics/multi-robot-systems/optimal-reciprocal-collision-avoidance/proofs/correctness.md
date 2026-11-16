---
title: When every ORCA linear program is feasible, no two robots collide within the time horizon, and the incremental solver finds the closest permitted velocity
proves: [correctness]
status: full
---

There are $r$ robots in the plane. Robot $A$ is a disc with center $p_A$, radius $r_A$, current velocity $v_A$, preferred velocity $v^{pref}_A$ and largest speed $v^{max}_A$. Robots are holonomic: each one can take any velocity in the disc $D(0, v^{max}_A)$. Time is synchronous: in one step of length $\Delta t$ every robot computes a new velocity from the same snapshot of positions and velocities, then all robots move. $\tau > 0$ is the time horizon. Lines L1 to L12 refer to the pseudocode on the [ORCA](/optimal-reciprocal-collision-avoidance/) page. Every robot uses its current velocity as the optimization velocity $v^{opt}_A = v_A$, as in the code.

For a pair $A, B$ write $p = p_B - p_A$ and $R = r_A + r_B$, and assume $\lVert p \rVert > R$ (the discs do not overlap). The truncated velocity obstacle is

$$VO^\tau_{A|B} = \{ w : \exists t \in (0, \tau] \text{ with } \lVert t w - p \rVert < R \}.$$

If the relative velocity $v'_A - v'_B$ stays constant and is not in $VO^\tau_{A|B}$, the discs do not overlap at any time in $[0, \tau]$, because $t (v'_A - v'_B) - p$ is the vector between the centers at time $t$, up to sign. Note that $VO^\tau_{B|A} = -VO^\tau_{A|B}$.

**Lemma 1 (the obstacle is open and convex).** $VO^\tau_{A|B}$ is an open convex set that does not contain $0$.

*Proof.* Substitute $s = 1/t$. Then $w \in VO^\tau_{A|B}$ if and only if there is $s \ge 1/\tau$ with $\lVert w - s p \rVert < s R$. The set $K = \{ (w, s) : s \ge 1/\tau, \lVert w - s p \rVert < s R \}$ is convex, because $\lVert w - s p \rVert - s R$ is a convex function of $(w, s)$ and $s \ge 1/\tau$ is a half-space. $VO^\tau_{A|B}$ is the image of $K$ under the linear map $(w, s) \mapsto w$, so it is convex. It is a union of open discs $D(s p, s R)$, so it is open. $0$ is not in it, because $\lVert 0 - s p \rVert = s \lVert p \rVert > s R$. $\square$

Let $w_0 = v_A - v_B$, and let $w_0 + u$ be the point of the boundary of $VO^\tau_{A|B}$ that is nearest to $w_0$. Let $n$ be the outward unit normal of $VO^\tau_{A|B}$ at $w_0 + u$. Then $n = u / \lVert u \rVert$ if $w_0$ is inside the obstacle, and $n = -u / \lVert u \rVert$ if $w_0$ is outside. Line L4 computes $u$: the code tests whether the nearest boundary point is on the cut-off circle of center $p / \tau$ and radius $R / \tau$ or on one of the two legs of the cone, and projects $w_0$ onto that part. Line L5 forms

$$ORCA^\tau_{A|B} = \{ v : (v - (v_A + \tfrac12 u)) \cdot n \ge 0 \}.$$

**Lemma 2 (the two half-planes are mirror images).** $ORCA^\tau_{B|A} = \{ v : (v - (v_B - \tfrac12 u)) \cdot (-n) \ge 0 \}$, with the same $u$ and $n$ as for $A$.

*Proof.* For $B$ the roles swap: $p$ becomes $-p$, $w_0$ becomes $-w_0$, and the obstacle becomes $-VO^\tau_{A|B}$. Point reflection through $0$ maps the nearest boundary point $w_0 + u$ to $-w_0 - u$, so the vector for $B$ is $-u$, and the outward normal for $B$ is $-n$. Put these into the formula of line L5. $\square$

The code computes both half-planes from the same formulas with the roles swapped. The test `test_lines_are_mirror_images` checks Lemma 2 on random pairs.

**Theorem 1 (reciprocal collision avoidance for one pair).** If $v'_A \in ORCA^\tau_{A|B}$ and $v'_B \in ORCA^\tau_{B|A}$, then $v'_A - v'_B \notin VO^\tau_{A|B}$. So, with constant velocities, $A$ and $B$ do not overlap during $[0, \tau]$.

*Proof.* By Lemma 1 and the supporting hyperplane theorem for open convex sets, $VO^\tau_{A|B} \subseteq \{ w : (w - (w_0 + u)) \cdot n < 0 \}$, since $n$ is the outward normal at the boundary point $w_0 + u$. Now

$$v'_A - v'_B - (w_0 + u) = \big(v'_A - (v_A + \tfrac12 u)\big) - \big(v'_B - (v_B - \tfrac12 u)\big),$$

because $w_0 = v_A - v_B$. Take the dot product with $n$. The first term gives a value $\ge 0$ because $v'_A \in ORCA^\tau_{A|B}$. The second term gives $(v'_B - (v_B - \frac12 u)) \cdot (-n) \ge 0$ by Lemma 2, because $v'_B \in ORCA^\tau_{B|A}$. So $(v'_A - v'_B - (w_0 + u)) \cdot n \ge 0$, and $v'_A - v'_B$ is not in the open half-plane that contains the obstacle. $\square$

**Theorem 2 (all robots).** Suppose every robot senses every robot that it could meet within $\tau$, and every robot's linear program on line L6 is feasible. Then no two robots overlap during the next $\tau$ time units if they keep their new velocities. In particular they do not overlap after the step of line L12 when $\Delta t \le \tau$.

*Proof.* Robot $A$'s new velocity lies in $ORCA^\tau_{A|B}$ for every sensed $B$, and $B$'s new velocity lies in $ORCA^\tau_{B|A}$. Apply Theorem 1 to each pair. A pair that does not sense each other cannot meet within $\tau$ by the assumption. $\square$

Each robot chooses its velocity alone, from the same snapshot, without messages. The guarantee only needs that both robots of a pair compute the two halves of the same $u$, which Lemma 2 gives.

**Lemma 3 (the incremental linear program).** Let $H_1, \dots, H_m$ be closed half-planes, let $C_0 = D(0, v^{max})$ and $C_i = C_{i-1} \cap H_i$. Let $f(v) = \lVert v - v^{pref} \rVert^2$. Suppose $C_{i-1}$ is not empty and $x$ is the unique minimizer of $f$ on $C_{i-1}$. If $x \notin H_i$ and $C_i$ is not empty, the minimizer $y$ of $f$ on $C_i$ lies on the boundary line $\ell_i$ of $H_i$.

*Proof.* $f$ is strictly convex and $C_i$ is compact and convex, so $y$ exists and is unique. Suppose $y \notin \ell_i$, so $y$ is in the open side of $H_i$. The segment from $x$ to $y$ lies in $C_{i-1}$ and crosses $\ell_i$ at a point $z \ne y$, since $x$ is outside $H_i$. Then $z \in C_i$, and by strict convexity $f(z) < \max(f(x), f(y)) = f(y)$, since $f(x) \le f(y)$. This contradicts the choice of $y$. $\square$

**Theorem 3 (lines L6 to L8 return the closest permitted velocity).** If the intersection of the ORCA half-planes and the speed disc is not empty, the solver of lines L6 to L8 returns the velocity in it that is closest to $v^{pref}$. If it is empty, the solver reports this.

*Proof.* Induction on $i$. Before the loop the result is the point of $C_0$ closest to $v^{pref}$, which is $v^{pref}$ itself or its scaling to length $v^{max}$. If the current result satisfies $H_i$, it is still optimal on the smaller set $C_i$. If not, by Lemma 3 the new optimum lies on $\ell_i$. On $\ell_i$, parametrized as $q + t d$ with a unit vector $d$, the set $C_i$ is an interval $[t_{left}, t_{right}]$: the disc gives the two roots of $\lVert q + t d \rVert = v^{max}$, and each earlier half-plane cuts one end, depending on the sign of the cross product of the two directions. A half-plane parallel to $\ell_i$ either holds on all of $\ell_i$ or on none of it. $f(q + t d)$ is a convex quadratic in $t$ with minimum at $t^* = d \cdot (v^{pref} - q)$, so the optimum is $t^*$ clamped to the interval. If the interval is empty, then $C_i$ is empty by the contrapositive of Lemma 3, and the solver stops and reports index $i$. $\square$

The same argument holds when the objective is linear, $\max\, v \cdot c$ for a direction $c$ (the flag `direction_opt` in the code). Then the optimum may not be unique, but some optimum lies on $\ell_i$, and on the interval it is the end point in the direction of $c$.

**Lemma 4 (the fallback program).** When the program of line L6 is infeasible, lines L9 and L10 return a velocity in the speed disc that minimizes the largest distance $\delta(v) = \max_j \operatorname{dist}(v, H_j)$ by which $v$ is outside a half-plane.

*Proof.* This is a linear program in the three variables $(v, \delta)$: minimize $\delta$ subject to $\operatorname{dist}(v, H_j) \le \delta$ for every $j$ and $\lVert v \rVert \le v^{max}$. The code solves it incrementally in the same way. When the current $v$ violates $H_i$ by more than the current $\delta$, the new optimum makes the violations of some constraint tie with that of $H_i$, by the argument of Lemma 3 one dimension higher. For each earlier $j$, the set of $v$ whose violation of $H_j$ is at most its violation of $H_i$ is a half-plane bounded by the bisector of $\ell_i$ and $\ell_j$. This bisector passes through $\ell_i \cap \ell_j$ with direction $d_j - d_i$, or is the middle line when $\ell_i$ and $\ell_j$ are parallel with opposite directions; when they are parallel with the same direction, the constraint is dominated and is skipped. Inside these half-planes and the disc, the violation of $H_i$ is the largest violation, and it decreases fastest in the direction of the inner normal of $H_i$. So the 2D program with the bisector half-planes and the linear objective in that direction, solved by Theorem 3, gives the optimum for constraints $1, \dots, i$. $\square$

The test `test_lp3_minimizes_the_largest_violation` compares the result with a grid search over the disc. When the fallback runs, Theorem 2 does not apply, and robots can overlap; this is a measurement in the tests, not a defect of the code.

**What the theorems do not give.** There is no liveness theorem. A fully symmetric scene, such as robots on a circle that all aim at the antipodal point, can reach an equilibrium in which every robot stops short of its goal. The tests add a small random change to each preferred velocity, as the RVO2 library does, to break such symmetry. Theorem 2 also needs exact arithmetic, the same snapshot for all robots, and holonomic robots that track the new velocity at once.
