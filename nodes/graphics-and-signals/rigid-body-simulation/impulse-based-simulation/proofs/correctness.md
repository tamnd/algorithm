---
title: The 2D collision integration ends after at most three phases and obeys Poisson's hypothesis and Coulomb friction, and microcollisions do no work
proves: [correctness, termination]
status: full
---

The setting is the 2D version of the page. A contact between bodies $A$ and $B$ has the unit normal $n$ from $B$ to $A$ and the tangent $t$. The contact velocity is $u = (u_t, u_n)$, the velocity of the material point of $A$ at the contact minus that of $B$, in the frame $(t, n)$. An impulse $p = (p_t, p_n)$ in this frame acts on $A$, and $-p$ acts on $B$. Positions do not change during a collision.

**Lemma 1 (linear response).** There is a symmetric matrix $K$ with $u = u^- + K p$ for every impulse $p$ applied so far, and $K$ is positive definite if at least one body is not static. In particular $K_{tt} > 0$, $K_{nn} > 0$ and $S = K_{nn} - K_{tn}^2 / K_{tt} > 0$.

*Proof.* By the Newton-Euler equations integrated over an instant, an impulse $P$ at the arm $r$ changes $v$ by $m^{-1} P$ and $\omega$ by $I^{-1}(r \times P)$, so the point velocity changes by $m^{-1} P + I^{-1}(r \times P)\, (-r_y, r_x)$. Its component along a unit vector $e$ is $m^{-1}(P \cdot e) + I^{-1} (r \times P)(r \times e)$, which is linear in $P$. Summing over $A$ (impulse $P$) and $B$ (impulse $-P$) gives $K_{de} = \sum_X m_X^{-1} (d \cdot e) + I_X^{-1} (r_X \times d)(r_X \times e)$ for $d, e \in \{t, n\}$. For one body that is not static, this is $m^{-1}$ times the identity plus the positive semidefinite rank one matrix $I^{-1} c c^T$ with $c = (r \times t, r \times n)$, so it is positive definite. A sum with a positive semidefinite term stays positive definite. The diagonal entries and the Schur complement $S$ of a positive definite $2 \times 2$ matrix are positive. $\square$

In COLLIDE, the parameter is $p_n$, and in each phase $dp/dp_n = d = (d_t, 1)$ is constant. By Lemma 1, $u$ then changes at the constant rate $(\dot u_t, \dot u_n) = K d$, with $\dot u_t = K_{tt} d_t + K_{tn}$ and $\dot u_n = K_{tn} d_t + K_{nn}$. The three modes are: slide, with $d_t = -\mu\, \mathrm{sgn}(u_t)$ when $u_t \ne 0$; stick, with $d_t = -K_{tn}/K_{tt}$ when $u_t = 0$ and $|K_{tn}| \le \mu K_{tt}$; and slide again, with $d_t = -\mu\, \mathrm{sgn}(K_{tn})$ when $u_t = 0$ and $|K_{tn}| > \mu K_{tt}$.

**Lemma 2 (the normal velocity rises unless the slip is about to stop).** In the stick mode and in the slide again mode, $\dot u_n > 0$. In the slide mode, if $u_t \dot u_t \ge 0$ (the slip does not decrease), then $\dot u_n > 0$.

*Proof.* Stick: $\dot u_n = K_{nn} - K_{tn}^2 / K_{tt} = S > 0$. Slide again: $\dot u_n = K_{nn} - \mu |K_{tn}|$, and $\mu < |K_{tn}| / K_{tt}$ gives $\mu |K_{tn}| < K_{tn}^2 / K_{tt}$, so $\dot u_n > S > 0$. Slide with $s = \mathrm{sgn}(u_t)$: $u_t \dot u_t \ge 0$ means $s(K_{tn} - \mu s K_{tt}) \ge 0$, that is $s K_{tn} \ge \mu K_{tt}$. If $\mu = 0$, then $\dot u_n = K_{nn} > 0$. Otherwise $\mu s K_{tn} \le (s K_{tn})^2 / K_{tt} = K_{tn}^2 / K_{tt}$ by multiplying the inequality by $s K_{tn} / K_{tt} \ge \mu$, and $\dot u_n = K_{nn} - \mu s K_{tn} \ge S > 0$. $\square$

**Lemma 3 (the sequence of modes).** The event "u_t reaches 0" happens at most once. After it, the mode is stick for the rest of the collision, or slide again followed by slide with the same sign for the rest of the collision.

*Proof.* The stop event can only end a slide phase with $u_t \dot u_t < 0$. After it, $u_t = 0$. In the stick mode $\dot u_t = 0$, so $u_t$ stays $0$ and the mode stays stick. In the slide again mode with $s = \mathrm{sgn}(K_{tn})$, $\dot u_t = s(|K_{tn}| - \mu K_{tt})$ has the sign $s$, so $u_t$ takes the sign $s$ at once, the next mode is slide with $\mathrm{sgn}(u_t) = s$ and the same $d_t$, and $u_t \dot u_t > 0$, so no stop event follows. $\square$

**Theorem 1 (termination).** If $u_n^- < 0$ and $K$ is positive definite, COLLIDE returns after at most three phases.

*Proof.* Each phase ends at exactly one of the events stop, max (u_n reaches 0) and end (p_n reaches the target), whichever comes first. The step to each event is nonnegative: during compression $u_n < 0$, so $-u_n / \dot u_n > 0$ when $\dot u_n > 0$; a stop is listed only when $u_t \dot u_t < 0$; and the target $(1 + e) p_{mc}$ is at least the current $p_n$. During compression the list of candidate events is never empty: if the mode is slide with $u_t \dot u_t < 0$, the stop is a candidate; otherwise $\dot u_n > 0$ by Lemma 2, and max is a candidate. During restitution, end is always a candidate. Stop happens at most once (Lemma 3), max exactly once (after it, the target is set and max is no longer a candidate), and end ends the procedure. So there are at most three phases. $\square$

**Theorem 2 (the result obeys the model).** Let $p$ be the result and $p_{mc}$ the value of $p_n$ at the max event. Then:

1. $p_n = (1 + e) p_{mc}$ (Poisson's hypothesis), and $u_n^+ \ge 0$, with $u_n^+ > 0$ when $e > 0$.
2. $|p_t| \le \mu p_n$, and more strongly, the impulse increment of every phase lies in the friction cone.
3. In every slide phase, the friction increment opposes the slip, which has a constant sign in the phase. In a stick phase, $u_t = 0$ throughout. The choice between stick and slide again at $u_t = 0$ is the only one that is consistent with the Coulomb law under the rule that friction keeps the contact stuck when it can (the assumption of Routh, used by Mirtich and Canny in Section 4.4).

*Proof.* (1) The target is set to $(1 + e) p_{mc}$ at the max event, and the procedure returns when $p_n$ reaches it. The phase in which max happens has $\dot u_n > 0$. Every later phase comes after a stop or is the same mode continued, so by Lemma 2 and Lemma 3 it also has $\dot u_n > 0$. Hence $u_n$ increases from $0$ during the whole restitution of length $e\, p_{mc}$, so $u_n^+ \ge 0$, and $u_n^+ > 0$ if $e > 0$ (note $p_{mc} > 0$ because $u_n^- < 0$).

(2) In every mode $|d_t| \le \mu$: for stick this is the test $|K_{tn}| \le \mu K_{tt}$. Integrating $dp_t = d_t\, dp_n$ over the phases gives $|p_t| \le \mu p_n$.

(3) A slide phase ends when $u_t$ reaches $0$, so $u_t$ has a constant sign in it, and $d_t = -\mu\, \mathrm{sgn}(u_t)$ is the Coulomb force direction of a sliding contact. At $u_t = 0$: if the contact stays stuck, $\dot u_t = 0$ forces $d_t = -K_{tn} / K_{tt}$, which is allowed exactly when $|K_{tn}| \le \mu K_{tt}$. Otherwise the contact must slide with some sign $s$ and $d_t = -\mu s$; then $\dot u_t = -\mu s K_{tt} + K_{tn}$ must have the sign $s$, which holds for $s = \mathrm{sgn}(K_{tn})$ and fails for $s = -\mathrm{sgn}(K_{tn})$, because then $\dot u_t = \mathrm{sgn}(K_{tn}) (\mu K_{tt} + |K_{tn}|)$ has the sign $-s$. $\square$

Within one phase, $u$ is an affine function of $p_n$ (Lemma 1 with constant $d$), so the event steps computed by one division are exact, and with exact rational input the procedure returns the exact solution of the piecewise linear model.

**Theorem 3 (microcollisions do no work).** If the impulse $q = K^{-1}(-2 u^-)$ is applied, then $u^+ = -u^-$, and the total kinetic energy of the two bodies does not change.

*Proof.* $u^+ = u^- + K q = -u^-$ by Lemma 1. For one body and an impulse $P$ at the arm $r$, $\tfrac12 m (|v^+|^2 - |v^-|^2) = \tfrac12 P \cdot (v^+ + v^-)$ and $\tfrac12 I ((\omega^+)^2 - (\omega^-)^2) = \tfrac12 (r \times P)(\omega^+ + \omega^-)$, whose sum is $\tfrac12 P \cdot (w^+ + w^-)$, where $w$ is the velocity of the material point at the contact. Summing over $A$ with $P$ and $B$ with $-P$ gives $\Delta T = \tfrac12 q \cdot (u^+ + u^-) = 0$. $\square$

**Theorem 4 (the simulation loop for discs).** Assume $g > 0$ or no ground, and that every contact handled by the loop has $K$ positive definite. Then:

1. The motion between events is exact, and each event time is the first time at which some pair has a gap of at most $\varepsilon_c$ and closes it.
2. For discs, $r_A$ and $r_B$ are parallel to $n$, so $K_{tn} = 0$, $\dot u_n = K_{nn} > 0$ in every mode, and $u_n$ is the rate of change of the gap.
3. After every resolved event, $u_n \ge 0$, so a pair that is inside the envelope is never closing after the loop has handled it at that time.

*Proof.* (1) Between events every body moves under gravity alone, $x(\tau) = x + v \tau + \tfrac12 g \tau^2$, which the loop applies in closed form. The gap to the ground is quadratic in $\tau$, and the root used is the later root of $h + v_y \tau - \tfrac12 g \tau^2 = 0$, the time at which the gap falls to $\varepsilon_c$. For two discs the gravity terms cancel, the relative position is linear in $\tau$, and the smaller root of $|d + w \tau|^2 = (R_A + R_B + \varepsilon_c)^2$ is the entry time, which exists only if $d \cdot w < 0$. The loop takes the minimum over all pairs, so no earlier event is skipped.

(2) The contact point is $x_A - R_A n$, so $r_A = -R_A n$ and $r_B = (|d| - R_A) n$. Then $r_X \times n = 0$ and $K_{tn} = \sum_X I_X^{-1} (r_X \times t)(r_X \times n) = 0$. The rotation term of the point velocity along $n$ is $\omega (r \times n) = 0$, so $u_n = n \cdot (v_A - v_B)$, the rate of change of the gap.

(3) A collision ends with $u_n^+ \ge 0$ by Theorem 2, and a microcollision with $u_n^+ = -u_n^- > 0$ by Theorem 3. $\square$

**Corollary (a single resting disc has a bounded event rate).** Take one disc on the ground, $g > 0$, $0 < e \le 1$, and let the first event have an approach speed of at least $v_e = \sqrt{2 g \varepsilon_c}$. After the first event with an approach speed below $v_e$, every event happens at the gap $\varepsilon_c$ with the same approach speed $u \in [e v_e, v_e)$, so the events are $2u/g \ge 2 e v_e / g$ apart, and the gap stays below $\varepsilon_c + u^2 / (2g) < 2 \varepsilon_c$.

*Proof.* By (2), $K_{tn} = 0$, so a collision under Poisson's hypothesis maps the approach speed $u$ to the separation speed $e u$, and the slow sliding rule of line L8 ($e = 1$) and a microcollision map it to $u$. A ballistic flight that starts and ends at the same gap returns with the speed it started with. So the approach speeds before the first slow event are $U_0, e U_0, e^2 U_0, \dots$, all at least $v_e$. The first slow event has the speed $e U_k$ with $U_k \ge v_e$, so its speed is at least $e v_e$, and from then on the speed does not change. The height formula is the apex of the ballistic flight. $\square$

**What is not proved.** The theorems are about the model: instantaneous collisions, Poisson's hypothesis, Coulomb friction with Routh's sticking rule, and the collision envelope. Nothing here says that the model matches real impacts. The rule that a slow, sliding contact uses $e = 1$ is a heuristic of this page. The event rate bound is only for a single disc; for stacks and for bodies other than discs, the number of collisions per unit time is not bounded by this argument and can grow without limit, which is the known weakness of the method for resting contact. In 3D the sliding direction turns during a collision, the integration is a numerical solve of a nonlinear differential equation, and Mirtich and Canny state the uniqueness of the outward sliding direction as a conjecture.
