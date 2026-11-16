---
title: The boids step is equivariant under relabeling and rigid motions, alignment alone is a consensus step, and on a complete graph alignment with cohesion makes the flock contract to one moving point
proves: [correctness]
status: full
---

Boids are not an algorithm with a specification that can be proved; the three rules are heuristics, and a run can split, stall or collide. What can be proved are structural facts of the step and the behavior of the linear part of the rules in the simplest case. Line numbers refer to the pseudocode on the [boids](/boids/) page.

There are $r$ boids with positions $p_i$ and velocities $v_i$ in the plane, a neighbor radius $R$, a separation radius $R_s$, weights $w_s, w_a, w_c \ge 0$, a time step $h > 0$, an acceleration limit $A$ and speed limits $0 \le s_{\min} \le s_{\max}$. $N_i = \{ j \ne i : \lVert p_j - p_i \rVert \le R \}$. One step computes, for every $i$ from the same snapshot, the steering $u_i$ of lines L3 to L7 and then $v_i' = \operatorname{clamp}(v_i + h u_i)$ and $p_i' = p_i + h v_i'$ (lines L8 and L9), where the clamp scales a nonzero vector to a norm in $[s_{\min}, s_{\max}]$ and does not change its direction.

**Lemma 1 (relabeling).** If the boids are listed in another order, the step gives the same new states in that order.

*Proof.* Every quantity in lines L3 to L9 for boid $i$ is a function of $(p_i, v_i)$ and of the set $\{(p_j, v_j) : j \ne i\}$, through sums and means over $N_i$, which do not depend on the order. $\square$

**Lemma 2 (rigid motions).** Let $g(x) = Qx + b$ with $Q$ a rotation or reflection matrix and $b$ a vector. If every $p_i$ is replaced by $g(p_i)$ and every $v_i$ by $Q v_i$, then the step gives $g(p_i')$ and $Q v_i'$.

*Proof.* Distances do not change, so $N_i$ and the test $\lVert p_i - p_j \rVert \le R_s$ do not change. Differences $p_i - p_j$ become $Q(p_i - p_j)$, and the separation term, which is $\sum (p_i - p_j) / \lVert p_i - p_j \rVert^2$, becomes $Q$ times itself. The alignment term is a difference of velocities and the cohesion term is a difference of positions, so both become $Q$ times themselves. So $u_i$ becomes $Q u_i$. The norm limits of lines L7 and L8 only scale vectors by factors that depend on norms, and $\lVert Q x \rVert = \lVert x \rVert$, so they commute with $Q$. The prioritized allocation also uses only the norms of the requests. Then $v_i' \mapsto Q v_i'$ and $p_i + h v_i' \mapsto Q p_i + b + h Q v_i' = g(p_i')$. $\square$

**Lemma 3 (the linear part on a complete graph).** Let $R$ be larger than the diameter of the flock at all times, so $N_i$ is all other boids, let $w_s = 0$, and let there be no limits. With $\kappa = r / (r - 1)$, $\bar p = \frac1r \sum_j p_j$ and $\bar v = \frac1r \sum_j v_j$, the step is

$$v_i' = v_i + h \kappa \left( w_a (\bar v - v_i) + w_c (\bar p - p_i) \right), \qquad p_i' = p_i + h v_i'.$$

*Proof.* The mean of the other velocities is $\frac{r \bar v - v_i}{r - 1}$, and minus $v_i$ this is $\frac{r}{r - 1} (\bar v - v_i)$. The same holds for positions. $\square$

**Lemma 4 (center of mass).** Under the assumptions of Lemma 3, $\bar v' = \bar v$ and $\bar p' = \bar p + h \bar v$. So the mean velocity never changes, and the center of mass moves on a straight line at constant speed.

*Proof.* Average the formulas of Lemma 3 over $i$: the averages of $\bar v - v_i$ and of $\bar p - p_i$ are zero. $\square$

**Theorem 1 (alignment alone is a consensus step).** Under the assumptions of Lemma 3 with $w_c = 0$, the velocity errors $e_i = v_i - \bar v$ satisfy $e_i' = (1 - h \kappa w_a) e_i$. So all velocities converge to $\bar v$ if and only if $0 < h \kappa w_a < 2$.

*Proof.* By Lemmas 3 and 4, $v_i' - \bar v' = v_i - \bar v - h \kappa w_a (v_i - \bar v)$. $\square$

This is the [Laplacian consensus protocol](/laplacian-consensus-protocol/) on the complete graph with the weights $w_a / (r - 1)$.

**Theorem 2 (cohesion alone does not settle).** Under the assumptions of Lemma 3 with $w_a = 0$ and $0 < h^2 \kappa w_c < 4$, let $x_i = p_i - \bar p$ and $y_i = v_i - \bar v$. Then $(x_i', y_i') = M (x_i, y_i)$ in each coordinate with

$$M = \begin{pmatrix} 1 - h^2 \kappa w_c & h \\ -h \kappa w_c & 1 \end{pmatrix}, \qquad \det M = 1.$$

So no nonzero deviation goes to zero: the boids oscillate about the center of mass.

*Proof.* By Lemma 3, $y_i' = y_i - h \kappa w_c x_i$ and $x_i' = x_i + h y_i'$, which gives $M$. Its determinant is $(1 - h^2 \kappa w_c) + h^2 \kappa w_c = 1$. Its trace $T = 2 - h^2 \kappa w_c$ lies in $(-2, 2)$, so the roots of $z^2 - T z + 1$ are two distinct complex conjugate numbers $z$ and $\bar z$ with $z \bar z = 1$, both of modulus one. Then $M$ is diagonalizable over the complex numbers, and $M^k = S \operatorname{diag}(z^k, \bar z^k) S^{-1}$ with $|z^k| = 1$. If $M^k w \to 0$ for a vector $w$, then $\operatorname{diag}(z^k, \bar z^k) S^{-1} w \to 0$, so $S^{-1} w = 0$ and $w = 0$. $\square$

**Theorem 3 (alignment and cohesion contract the flock).** Under the assumptions of Lemma 3 with $w_a, w_c > 0$, let $a = h \kappa w_a$ and $c = h^2 \kappa w_c$. If $a < 2$ and $c + 2a < 4$, then every $p_i - \bar p$ and every $v_i - \bar v$ goes to zero geometrically, so the flock contracts to one point that moves with the constant velocity $\bar v$.

*Proof.* As in Theorem 2, $y_i' = (1 - a) y_i - h \kappa w_c x_i$ and $x_i' = x_i + h y_i'$, so the deviation in each coordinate is multiplied by

$$M = \begin{pmatrix} 1 - c & h (1 - a) \\ -h \kappa w_c & 1 - a \end{pmatrix}, \qquad D = \det M = 1 - a, \qquad T = \operatorname{tr} M = 2 - c - a.$$

The eigenvalues are the roots of $z^2 - T z + D$. A real quadratic $z^2 - T z + D$ has both roots in the open unit disk if and only if $|D| < 1$ and $|T| < 1 + D$ (the Schur-Cohn or Jury test for degree two). Here $|D| < 1$ because $0 < a < 2$. Next $T < 1 + D$ is $2 - c - a < 2 - a$, which holds because $c > 0$. Last $-T < 1 + D$ is $c + a - 2 < 2 - a$, that is $c + 2a < 4$. So the spectral radius of $M$ is less than one, and $M^k \to 0$ geometrically. $\blacksquare$

**What is not proved here.** With separation, a neighbor radius smaller than the flock, or the limits on acceleration and speed, the step is nonlinear and its graph changes over time. The flock can then split into groups, as the example on the page shows, and nothing above says that the boids align, stay together or avoid collisions. Results of this kind need other rules and assumptions, such as the flocking algorithms with potential functions of Olfati-Saber (2006), or the connectivity conditions of Jadbabaie, Lin and Morse (2003) for the Vicsek model; they are not proved here.
