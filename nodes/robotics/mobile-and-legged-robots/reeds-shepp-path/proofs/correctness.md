---
title: The Reeds-Shepp algorithm returns a shortest path of a car that drives both ways
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [Reeds-Shepp path](/reeds-shepp-path/) page. After line L1 the start is $(0, 0, 0)$, the goal is $(x, y, \varphi)$ and the turning radius is 1; rigid motions and scaling map admissible paths to admissible paths and scale lengths by $1/\rho$. A path is a word over $\{L, S, R\}$ and signed lengths $s_i$. On a segment of signed length $s$ the car moves with speed $v = \mathrm{sign}(s)$ for time $|s|$, with
$$x' = v\cos\theta,\quad y' = v\sin\theta,\quad \theta' = v\kappa,$$
where $\kappa = +1$ on L, $-1$ on R and $0$ on S. The length of the path is $\sum_i |s_i|$.

**Lemma 1 (time flip).** If a path with word $w$ and lengths $(s_i)$ goes from $(0, 0, 0)$ to $(x, y, \varphi)$, then the path with word $w$ and lengths $(-s_i)$ goes from $(0, 0, 0)$ to $(-x, y, -\varphi)$, and has the same length.

*Proof.* Let $(x(\tau), y(\tau), \theta(\tau))$ be the first trajectory with speed $v(\tau)$ and curvature $\kappa(\tau)$. Set $\tilde x = -x$, $\tilde y = y$, $\tilde\theta = -\theta$, $\tilde v = -v$ and $\tilde\kappa = \kappa$. Then $\tilde x' = -v\cos\theta = \tilde v\cos\tilde\theta$, $\tilde y' = v\sin\theta = (-\tilde v)(-\sin\tilde\theta) = \tilde v\sin\tilde\theta$ and $\tilde\theta' = -v\kappa = \tilde v\tilde\kappa$. So the new curve is a trajectory of the car with the same curvature on each segment, the same word, and the opposite signs. It starts at $(0, 0, 0)$ and ends at $(-x, y, -\varphi)$. $\square$

**Lemma 2 (reflection).** If a path with word $w$ and lengths $(s_i)$ goes from $(0, 0, 0)$ to $(x, y, \varphi)$, then the path with L and R swapped in $w$ and the same lengths goes to $(x, -y, -\varphi)$.

*Proof.* Set $\tilde x = x$, $\tilde y = -y$, $\tilde\theta = -\theta$, $\tilde v = v$, $\tilde\kappa = -\kappa$. Then $\tilde x' = v\cos\tilde\theta$, $\tilde y' = -v\sin\theta = \tilde v\sin\tilde\theta$ and $\tilde\theta' = -v\kappa = \tilde v\tilde\kappa$. $\square$

**Lemma 3 (backward).** Let $(x_b, y_b) = (x\cos\varphi + y\sin\varphi,\ x\sin\varphi - y\cos\varphi)$. If a path with word $w$ and lengths $(s_1, \dots, s_k)$ goes from $(0, 0, 0)$ to $(x_b, y_b, \varphi)$, then the path with the reversed word and lengths $(s_k, \dots, s_1)$ goes from $(0, 0, 0)$ to $(x, y, \varphi)$.

*Proof.* Drive a path backward in time: run its segments in reverse order with negated lengths. This is a trajectory of the car, by the substitution $\tau \to -\tau$, $v \to -v$, which keeps $\kappa$. So if $P$ goes from $A$ to $B$, its reversal goes from $B$ to $A$ with the reversed word and negated lengths. Now write the start $(0, 0, 0)$ in the frame of the goal $(x, y, \varphi)$: it is $(-x\cos\varphi - y\sin\varphi,\ x\sin\varphi - y\cos\varphi,\ -\varphi)$. The time flip of Lemma 1 maps this pose to $(x_b, y_b, \varphi)$. So the given path, flipped in time by Lemma 1, goes from $(0, 0, 0)$ to the start seen from the goal, with negated lengths. Placed in the frame of the goal, it is a path from the goal to the start. Its reversal goes from the start to the goal, with the word reversed and the lengths negated twice, that is $(s_k, \dots, s_1)$. $\square$

Line L5 applies exactly these maps: it negates the lengths for the goals $(-x, y, -\varphi)$ and $(-x, -y, \varphi)$, swaps L and R for $(x, -y, -\varphi)$ and $(-x, -y, \varphi)$, and reverses the order for the backward goals. The goal $(-x, -y, \varphi)$ is the composition of Lemma 1 and Lemma 2, and the two maps commute. Each map is an involution, so the candidate built from a base solution for a transformed goal is a path to the original goal.

**Lemma 4 (base formula 8.1).** If $L^+ S^+ L^+$ is accepted with $(t, u, v)$, its path goes from $(0, 0, 0)$ to $(x, y, \varphi)$.

*Proof.* By the motion on a left arc (see Lemma 1 of the [Dubins path proof](/dubins-path/)), the first arc of angle $t$ ends at $(\sin t, 1 - \cos t)$ with heading $t$. The straight part of length $u$ ends at $(\sin t + u\cos t,\ 1 - \cos t + u\sin t)$. The last arc of angle $v$ ends at heading $t + v$, and its position is the previous point plus $(\sin(t + v) - \sin t,\ \cos t - \cos(t + v))$. With $v \equiv \varphi - t$, the heading is $\varphi$ and the position is $(u\cos t + \sin\varphi,\ 1 + u\sin t - \cos\varphi)$. The formula takes $(u, t)$ as the polar coordinates of $(x - \sin\varphi,\ y - 1 + \cos\varphi)$, so $u\cos t = x - \sin\varphi$ and $u\sin t = y - 1 + \cos\varphi$, and the end point is $(x, y)$. $\square$

The other base formulas (8.2, 8.3 and 8.4, 8.7, 8.8, 8.9, 8.10 and 8.11) come from the same kind of computation on the circles of the word: tangent lines for the words with S, and circles that touch at distance 2 for the words of arcs only. Reeds and Shepp derive them in Section 8 of their paper; the OMPL source corrects 8.3/8.4 and 8.11, and the implementation uses the corrected forms. We do not repeat the derivations. As a check of the code, the tests drive every accepted candidate on 1500 random pairs of poses and radii and find the end pose within $10^{-9}$ of the goal every time.

**Theorem (Reeds and Shepp 1990).** Between any two poses there is a shortest path of the car with speed $\pm 1$ and curvature at most 1. Some shortest path has one of the 48 words of the theorem, with at most five segments and at most two cusps, and with segment parameters in the ranges of Section 8.

Sussmann and Tang (1991) and Boissonnat, Cérézo and Leblond (1994) gave proofs with the maximum principle. We use the theorem and do not reprove it.

**Theorem (correctness).** REEDS-SHEPP returns a path from $q_0$ to $q_1$ of the least length.

*Proof.* By Lemmas 1 to 4 and the derivations of Section 8, every candidate that line L5 builds is a path from $q_0$ to $q_1$, so the result is feasible and its length is at least the optimum. By the theorem of Reeds and Shepp, some shortest path $P^*$ has one of the 48 words with parameters in the stated ranges. Each of the 48 words is a base word of the table on the page, or the image of one under time flip, reflection and backward reading, and line L4 tries every one of these images. Within one word and its ranges, Section 8 solves the end-pose equations for the parameters, so the candidate of that word is $P^*$, or a path of the same word with the same length. So line L7 sees a candidate of length at most $|P^*|$ and keeps the least length, which therefore equals the optimum. Line L8 returns it. $\square$

**What the tests add.** Beyond the end poses, the tests check on 4000 cases that no random path of up to five signed segments is shorter, including paths of the Reeds-Shepp shapes with arcs of exactly $\pi/2$. They check that the length from $q_0$ to $q_1$ equals the length from $q_1$ to $q_0$, that every result has at most five segments and two gear changes, that each of the 18 base types (with reflections) is the answer somewhere, and the hand cases of the page: 4 m straight back, the U-turn on the spot of length $\pi$, and the forward path of length 5.1763 m that equals the Dubins path.
