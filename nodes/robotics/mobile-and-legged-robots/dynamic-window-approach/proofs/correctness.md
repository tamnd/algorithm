---
title: The dynamic window approach never collides and always has an admissible command
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [dynamic window approach](/dynamic-window-approach/) page. The claim is about safety only; reaching the goal is not guaranteed. The assumptions are: the obstacles are static discs that are known exactly; the robot is a disc of radius $R$ whose motion follows the [unicycle model](/unicycle-model/) exactly, with each command held for one cycle $\Delta t$; and the robot starts at rest in a free pose. The robot overlaps an obstacle of radius $r$ when the distance between the centers is less than $r + R$; touching is not overlap.

**Notation.** For a pair $(v, \omega)$ with $v > 0$, let $m(v, \omega) = \max(v/(a_v\Delta t), |\omega|/(a_\omega\Delta t))$ and $n(v, \omega) = \max(1, \lceil m(v, \omega)\rceil)$. The braking sequence of $(v, \omega)$ is $(v, \omega)\,(n - j)/n$ for $j = 0, 1, \dots, n$. Each pair is held for one cycle. Let $\operatorname{stop}(v, \omega) = \Delta t \sum_{j=0}^{n-1} v(n - j)/n = \Delta t\,v(n + 1)/2$, and $\operatorname{stop}(0, \omega) = 0$. The braking pair $b(v, \omega)$ is the pair with $j = 1$, that is $(v, \omega)(n - 1)/n$; for $v = 0$ it is $(0, \omega')$ where $\omega'$ moves $\omega$ toward 0 by at most $a_\omega\Delta t$. For a pose $p$, $\operatorname{dist}(p, v, \omega)$ is the arc length along the path of $(v, \omega)$ from $p$ to the first point where the robot touches an obstacle, or $\infty$; for $v = 0$ it is $\infty$. A pair is admissible at $p$ when $\operatorname{stop}(v, \omega) \le \operatorname{dist}(p, v, \omega)$, which is the test of line L4.

**Lemma 1 (the braking sequence is feasible and stays on the arc).** Consecutive pairs of the braking sequence differ by $v/n \le a_v\Delta t$ and $|\omega|/n \le a_\omega\Delta t$, and every pair of the sequence with a nonzero speed has the same ratio $\omega/v$. The robot covers exactly $\operatorname{stop}(v, \omega)$ along the path of $(v, \omega)$ and then stands still.

*Proof.* Since $n \ge m(v, \omega)$, we have $v/n \le a_v\Delta t$ and $|\omega|/n \le a_\omega\Delta t$. Every pair is a positive multiple of $(v, \omega)$ until the last one, so the ratio, and with it the radius $v/|\omega|$ and the direction of the turn, do not change. A unicycle that holds a pair with this ratio moves along the same circle (or the same line for $\omega = 0$), and the arc length of one cycle is the speed times $\Delta t$. Adding the arc lengths gives $\operatorname{stop}(v, \omega)$. $\square$

**Lemma 2 (the braking pair is admissible after one cycle).** Let $(v, \omega)$ with $v > 0$ be admissible at $p$, and let $p'$ be the pose after the robot holds $(v, \omega)$ for $\Delta t$. Then $b = b(v, \omega)$ is in the dynamic window of $(v, \omega)$, and $b$ is admissible at $p'$.

*Proof.* By Lemma 1, $b$ differs from $(v, \omega)$ by at most $a_v\Delta t$ and $a_\omega\Delta t$, and its components are no larger in absolute value, so it is inside the speed limits and the window of line L1.

First the stopping distance. If $n = 1$, then $b = (0, 0)$ and $\operatorname{stop}(b) = 0 = \operatorname{stop}(v, \omega) - v\Delta t$. If $n \ge 2$, then $m = m(v, \omega)$ satisfies $n - 1 < m \le n$, and $m(b) = m(n - 1)/n$. So $m(b) \le n - 1$, and $m(b) > (n - 1)^2/n \ge n - 2$, because $(n - 1)^2 = n(n - 2) + 1$. Hence $n(b) = n - 1$ and
$$\operatorname{stop}(b) = \Delta t\,\frac{v(n - 1)}{n}\cdot\frac{n}{2} = \Delta t\,v\,\frac{n - 1}{2} = \operatorname{stop}(v, \omega) - v\Delta t.$$

Now the free distance. The path of $b$ from $p'$ is the continuation of the path of $(v, \omega)$ from $p$, since the circle and the direction are the same and $p'$ lies on it at arc length $v\Delta t$ from $p$. Let $d = \operatorname{dist}(p, v, \omega)$. Admissibility gives $d \ge \operatorname{stop}(v, \omega) \ge v\Delta t$. Suppose the robot touched an obstacle at arc length $u < d - v\Delta t$ from $p'$. That point lies at arc length $u + v\Delta t < d$ from $p$ along the same path (if the path is a circle and $u + v\Delta t$ exceeds its length, the same point also lies at a smaller arc length). This contradicts the choice of $d$ as the first contact. So $\operatorname{dist}(p', b) \ge d - v\Delta t$. Together,
$$\operatorname{stop}(b) = \operatorname{stop}(v, \omega) - v\Delta t \le d - v\Delta t \le \operatorname{dist}(p', b). \qquad\square$$

**Lemma 3 (one admissible cycle is safe).** If $(v, \omega)$ is admissible at a free pose $p$, then the robot does not overlap an obstacle while it holds $(v, \omega)$ for $\Delta t$.

*Proof.* If $v = 0$, the round robot turns in place and its center does not move. Otherwise it covers the arc length $v\Delta t \le \Delta t\,v(n + 1)/2 = \operatorname{stop}(v, \omega) \le \operatorname{dist}(p, v, \omega)$, because $n \ge 1$. Before the arc length $\operatorname{dist}(p, v, \omega)$, the center stays out of every inflated disc, since $p$ is free and the first entry into a disc happens at a point of its boundary. $\square$

**Theorem (safety).** Under the assumptions above, at every cycle line L4 keeps at least one pair, and the robot never overlaps an obstacle.

*Proof.* We show by induction on the cycle $t$ that the pose $p_t$ is free and the current velocity $(v_t, \omega_t)$ is admissible at $p_{t-1}$, where for $t = 0$ the velocity is $(0, 0)$, which is admissible everywhere.

At cycle $t$, line L2 includes the braking pair $b(v_t, \omega_t)$. If $v_t > 0$, Lemma 2 applied to the admissible command $(v_t, \omega_t)$ at $p_{t-1}$ shows that $b$ is admissible at $p_t$. If $v_t = 0$, then $b$ has speed 0 and $\operatorname{dist} = \infty$, so it is admissible. Hence line L4 keeps $b$, and line L7 returns some admissible pair $(v_{t+1}, \omega_{t+1})$ in the window. By Lemma 3, the robot moves from $p_t$ to $p_{t+1}$ without overlap, so $p_{t+1}$ is free. This completes the induction. $\square$

**Remarks.** The theorem does not depend on the weights, on the grid of line L2, or on the cap $D$ of the clearance, which enters only the score. It needs the braking pair in the candidate set: a grid alone may contain no admissible pair after a coarse sampling. It fails when an obstacle appears inside the stopping distance, when obstacles move, or when the real robot does not follow the commanded arc; then a margin on the robot radius and a brake reflex are needed. The tests check the parts on random data: `test_arc_distance_matches_dense_sampling` compares the exact arc distance with a walk in steps of 2 mm, `test_stopping_distance_and_braking_stay_on_the_arc` checks Lemma 1 and the equation $\operatorname{stop}(b) = \operatorname{stop}(v, \omega) - v\Delta t$, and the run tests check Lemma 3 and the acceleration limits at every cycle.
