---
title: Two robots that choose velocities outside their reciprocal velocity obstacles on the same side never collide, and a mirrored choice does not oscillate
proves: [correctness]
status: full
---

Two robots $A$ and $B$ are discs in the plane with centers $p_A, p_B$, radii $r_A, r_B$ and current velocities $v_A, v_B$. Write $p = p_B - p_A$ and $R = r_A + r_B$, and assume $\lVert p \rVert > R$, so the discs do not overlap. Lines L1 to L9 refer to the pseudocode on the [reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) page. The horizon is infinite, as in van den Berg, Lin and Manocha (2008): a collision at any future time counts.

**The cone.** Let $C = \{ w \ne 0 : \exists t > 0 \text{ with } \lVert t w - p \rVert < R \}$. If the relative velocity $v'_A - v'_B$ stays constant, the discs overlap at some time $t > 0$ if and only if $v'_A - v'_B \in C$, because $p_B + t v'_B - (p_A + t v'_A) = p - t (v'_A - v'_B)$. The velocity obstacle of $A$ for $B$ is $VO_{A|B}(v_B) = v_B + C$, and the reciprocal velocity obstacle is

$$RVO_{A|B}(v_A, v_B) = \{ v' : 2 v' - v_A \in VO_{A|B}(v_B) \} = \{ v' : 2 v' - v_A - v_B \in C \}.$$

Its apex is $\frac12 (v_A + v_B)$. By symmetry, $RVO_{B|A}(v_B, v_A) = \{ v' : 2 v' - v_A - v_B \in -C \}$.

**Lemma 1 (the time to collision).** Let $a = \lVert w \rVert^2$, $b = p \cdot w$, $c = \lVert p \rVert^2 - R^2 > 0$ and $\Delta = b^2 - a c$. Then $w \in C$ if and only if $a > 0$, $b > 0$ and $\Delta > 0$, and then the first time of contact is $t^* = (b - \sqrt{\Delta}) / a > 0$.

*Proof.* $\lVert t w - p \rVert^2 - R^2 = a t^2 - 2 b t + c$. For $a = 0$ this is $c > 0$ for all $t$. For $a > 0$ the quadratic is negative for some $t$ if and only if $\Delta > 0$, and then exactly on the open interval between its roots $(b \pm \sqrt\Delta) / a$. Their product is $c / a > 0$, so both roots have the sign of $b$, and the interval meets $t > 0$ if and only if $b > 0$. If $\Delta = 0$ the discs only touch, which is not an overlap. $\square$

The function `time_to_collision` computes $t^*$, and `in_rvo` tests $2 v' - v_A - v_B \in C$ with it. The test compares `in_rvo` with a second test of the cone, $p \cdot w > 0$ and $|w \times p| / \lVert w \rVert < R$, which says that the ray meets the disc in front of the apex.

**Lemma 2 (the cone is an open wedge).** Let $\alpha = \arcsin(R / \lVert p \rVert) < \pi / 2$, and let $\ell_L$ and $\ell_R$ be the unit vectors of $p$ turned by $+\alpha$ and by $-\alpha$ (the left and the right leg). Then $C$ is the set of $w \ne 0$ whose angle to $p$ is less than $\alpha$. Its complement is $H_L \cup H_R$, with the closed half-planes $H_L = \{ w : \ell_L \times w \ge 0 \}$ and $H_R = \{ w : \ell_R \times w \le 0 \}$. Here $u \times w = u_x w_y - u_y w_x$.

*Proof.* The ray $\{ t w : t > 0 \}$ meets the open disc $D(p, R)$ if and only if its distance to $p$ is less than $R$ and $p$ lies ahead, that is, if and only if the angle $\theta$ between $w$ and $p$ satisfies $\theta < \pi / 2$ and $\lVert p \rVert \sin \theta < R$, that is, $\theta < \alpha$. This open wedge is the intersection of the two open half-planes $\{ \ell_L \times w < 0 \}$ and $\{ \ell_R \times w > 0 \}$, because $\alpha < \pi / 2$, so its complement is the union of their complements $H_L$ and $H_R$. $\square$

$H_L$ holds the relative velocities that pass $B$ on the left of $A$'s line of sight, and $H_R$ those that pass on the right.

**Theorem 1 (same side, no collision).** Let $w_A = 2 v'_A - v_A - v_B$ and $w_B = -(2 v'_B - v_A - v_B)$. So $v'_A \notin RVO_{A|B}$ if and only if $w_A \notin C$, and $v'_B \notin RVO_{B|A}$ if and only if $w_B \notin C$. If $w_A$ and $w_B$ both lie in $H_L$, or both lie in $H_R$, then $v'_A - v'_B \notin C$, so the robots never collide with these velocities.

*Proof.* $v'_A - v'_B = \frac12 (w_A + w_B)$. A closed half-plane through the origin is a convex cone, so it contains the average of two of its points. By Lemma 2 that half-plane is disjoint from $C$. $\square$

In words: if each robot takes a velocity outside its own reciprocal velocity obstacle, and both pass on the same side, each robot does half of the avoidance and the halves add up. The test `test_same_side_choices_never_collide` checks this on random pairs, and it also finds many pairs where each robot is outside its own obstacle but the two choose opposite sides and collide. So the same side condition is needed.

**Theorem 2 (a mirrored choice is stable).** Suppose the pair was on a collision course, $v_A - v_B \in C$, and the new velocities are mirrored: $v'_A + v'_B = v_A + v_B$. Then in the next step, with the new velocities as the current ones, (a) the old velocity $v_A$ is inside $RVO_{A|B}(v'_A, v'_B)$, and (b) the new velocity $v'_A$ is outside $RVO_{A|B}(v'_A, v'_B)$ whenever it was outside $RVO_{A|B}(v_A, v_B)$.

*Proof.* Write $\delta = v'_A - v_A = -(v'_B - v_B)$. (a) $2 v_A - v'_A - v'_B = 2 v_A - (v_A + v_B) = v_A - v_B \in C$. (b) $2 v'_A - v'_A - v'_B = v'_A - v'_B = v_A - v_B + 2 \delta$, and $2 v'_A - v_A - v_B = v_A - v_B + 2 \delta$ is the same vector. $\square$

So under a mirrored choice neither robot wants to go back to its old velocity, and the new velocity stays permitted. With the plain velocity obstacle, $v'_A \notin VO_{A|B}(v_B)$ means $v'_A - v_B \notin C$; when both robots dodge, each sees the other's dodge in the next step, the straight velocity becomes free again, both return to it, and the cycle repeats. This is the oscillation that the reciprocal obstacle removes. The test `test_plain_velocity_obstacles_oscillate` shows the cycle of period 2 for a head-on pair, and `test_head_on_pair_turns_to_the_same_side` shows the RVO pair turning once and staying on its side.

**Why the code makes mirrored choices in a mirrored scene.** Line L2 scores the preferred velocity, the zero velocity and a polar grid whose spokes are measured from the direction of the preferred velocity. If robot $B$ is the point reflection of robot $A$ through the midpoint, so $p$, $v_B$ and $v^{pref}_B$ are the negatives of the data of $A$, then $B$'s candidate list is the negated list of $A$ in the same order. Every quantity in lines L5 to L7 changes sign or stays the same under this reflection, and negation is exact in floating point, so the penalties are equal entry by entry and the first minimum has the same index. Then $v'_B = -v'_A$ and $v_B = -v_A$, which is the hypothesis of Theorem 2, and $w_A = 2 v'_A = w_B$, which is the hypothesis of Theorem 1.

**What the theorems do not give.** The selection rule of lines L2 to L8 is a heuristic. It may pick a velocity inside a reciprocal velocity obstacle when the penalty $\omega / t_c + \lVert v' - v^{pref} \rVert$ favors it, and with three or more robots nothing makes every pair pick the same side. So there is no collision guarantee for the full method. The tests measure that no discs overlap in a swap of 6 robots on a circle. The theorems also assume holonomic robots, synchronous steps, and exact velocities of the neighbors. [Optimal reciprocal collision avoidance](/optimal-reciprocal-collision-avoidance/) replaces the side choice by one half-plane per pair and gets a guarantee when its linear program is feasible.
