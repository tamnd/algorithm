---
title: Prediction finds the first contact, and resolution is an elastic bounce
proves: [correctness]
status: full
---

We use the notation of the page. Disks $i$ and $j$ have positions $r_i, r_j$, velocities $v_i, v_j$, radii $s_i, s_j$ and masses $m_i, m_j > 0$. Let $\Delta r = r_j - r_i$, $\Delta v = v_j - v_i$, $\sigma = s_i + s_j$, and

$$a = \Delta v \cdot \Delta v, \qquad b = \Delta v \cdot \Delta r, \qquad c = \Delta r \cdot \Delta r - \sigma^2, \qquad d = b^2 - a c.$$

On straight paths, the centres at time $t$ differ by $\Delta r + t\, \Delta v$. The disks touch exactly when $|\Delta r + t\, \Delta v| = \sigma$, that is, when $f(t) = 0$ for

$$f(t) = |\Delta r + t\, \Delta v|^2 - \sigma^2 = a t^2 + 2 b t + c.$$

**Lemma 1 (pair prediction).** Assume $c > 0$ (the disks do not touch or overlap at time 0) and $i \ne j$. Then TIME-TO-HIT$(i, j)$ returns the smallest $t \ge 0$ with $f(t) = 0$, and it returns $\infty$ exactly when no such $t$ exists.

*Proof.* We follow lines L4 to L8.

*Case $b \ge 0$ (line L4 returns $\infty$).* For $t \ge 0$ we have $a t^2 \ge 0$ and $2 b t \ge 0$, so $f(t) \ge c > 0$. No contact exists, and $\infty$ is right. This case contains $a = 0$: then $\Delta v = 0$ and $b = 0$.

*Case $b < 0$.* Then $\Delta v \ne 0$, so $a > 0$, and line L8 does not divide by 0.

- *Subcase $d < 0$ (line L7 returns $\infty$).* The quadratic $a t^2 + 2 b t + c$ with $a > 0$ has the minimum value $c - b^2/a = -d/a > 0$. So $f(t) > 0$ for each real $t$, no contact exists, and $\infty$ is right.
- *Subcase $d \ge 0$.* The roots of $f$ are $t_{\pm} = (-b \pm \sqrt d)/a$, and both are real. Their product is $c/a > 0$ and their sum is $-2b/a > 0$. So both roots are positive. Line L8 returns $t_- = -(b + \sqrt d)/a$, the smaller root. Since $f(0) = c > 0$ and $f$ has no root in $[0, t_-)$, $f > 0$ on $[0, t_-)$ by continuity, and $f(t_-) = 0$. So $t_-$ is the first time of contact. When $d = 0$ the two roots are equal and the disks graze. $\square$

The second root $t_+$ is the time at which the disks would stop overlapping if they passed through each other. It has no physical meaning, because the bounce at $t_-$ changes the paths.

**Lemma 2 (wall prediction).** Assume $s_i \le r_x \le 1 - s_i$. Lines L9 to L11 return the smallest $t \ge 0$ at which $r_x + t v_x = 1 - s_i$ or $r_x + t v_x = s_i$, or $\infty$ if there is none.

*Proof.* If $v_x = 0$, then $r_x$ never changes. If $r_x$ is strictly between $s_i$ and $1 - s_i$, there is no contact; if it is equal to one of them, the disk slides along the wall, which the method treats as no event. If $v_x > 0$, then $r_x + t v_x$ increases; it reaches $1 - s_i$ at $t = (1 - s_i - r_x)/v_x \ge 0$, and it reaches $s_i$ only at $t \le 0$. If $v_x < 0$, the same argument with the roles swapped gives $t = (s_i - r_x)/v_x \ge 0$, since the numerator and the denominator are both at most 0. The horizontal walls are the same with $r_y$ and $v_y$. $\square$

**Lemma 3 (resolution).** Let the disks touch, so $|\Delta r| = \sigma$, and let $n = \Delta r/\sigma$, a unit vector. Let $v_i', v_j'$ be the velocities after lines L14 to L17, and $\Delta v' = v_j' - v_i'$. Then

1. $m_i v_i' + m_j v_j' = m_i v_i + m_j v_j$ (momentum);
2. $\Delta v' = \Delta v - 2 (\Delta v \cdot n)\, n$, so $\Delta v' \cdot n = -\Delta v \cdot n$, and $\Delta v' \cdot w = \Delta v \cdot w$ for each $w$ orthogonal to $n$;
3. $m_i |v_i'|^2 + m_j |v_j'|^2 = m_i |v_i|^2 + m_j |v_j|^2$ (kinetic energy);
4. among all updates of the form $v_i' = v_i + (\lambda/m_i)\, n$, $v_j' = v_j - (\lambda/m_j)\, n$ (equal and opposite impulses along the line of centres), the energy is kept only for $\lambda = 0$ and for $\lambda = J$.

*Proof.* Lines L14 and L15 give the impulse vector $(J_x, J_y) = J n$ with

$$J = \frac{2 m_i m_j (\Delta v \cdot \Delta r)}{\sigma (m_i + m_j)} = 2 \mu\, (\Delta v \cdot n), \qquad \mu = \frac{m_i m_j}{m_i + m_j},$$

using $\Delta v \cdot \Delta r = \sigma (\Delta v \cdot n)$. Lines L16 and L17 set $v_i' = v_i + (J/m_i) n$ and $v_j' = v_j - (J/m_j) n$.

1. $m_i v_i' + m_j v_j' = m_i v_i + J n + m_j v_j - J n = m_i v_i + m_j v_j$.
2. $\Delta v' = \Delta v - J (1/m_i + 1/m_j)\, n = \Delta v - (J/\mu)\, n = \Delta v - 2 (\Delta v \cdot n)\, n$. Taking the dot product with $n$, and using $n \cdot n = 1$, gives $\Delta v' \cdot n = \Delta v \cdot n - 2 \Delta v \cdot n = -\Delta v \cdot n$. For $w \perp n$, $\Delta v' \cdot w = \Delta v \cdot w$.
3. Let $M = m_i + m_j$ and $V = (m_i v_i + m_j v_j)/M$, the velocity of the centre of mass. Then $v_i = V - (m_j/M) \Delta v$, since $V - (m_j/M)(v_j - v_i) = (m_i v_i + m_j v_j - m_j v_j + m_j v_i)/M = v_i$, and in the same way $v_j = V + (m_i/M) \Delta v$. Expanding,
$$m_i |v_i|^2 + m_j |v_j|^2 = M |V|^2 - 2\, V \cdot \Delta v \left( \frac{m_i m_j}{M} - \frac{m_j m_i}{M} \right) + \left( \frac{m_i m_j^2}{M^2} + \frac{m_j m_i^2}{M^2} \right) |\Delta v|^2 = M |V|^2 + \mu |\Delta v|^2.$$
The same identity holds after the bounce with $V'$ and $\Delta v'$. By part 1, $V' = V$. By part 2, $\Delta v'$ is the reflection of $\Delta v$ in the line orthogonal to $n$, so $|\Delta v'|^2 = |\Delta v|^2 - 4 (\Delta v \cdot n)^2 + 4 (\Delta v \cdot n)^2 |n|^2 = |\Delta v|^2$. So the energy is the same.
4. For a general $\lambda$, the momentum is kept as in part 1, so $V' = V$, and $\Delta v' = \Delta v - (\lambda/\mu) n$. By the identity of part 3, the energy is kept if and only if $|\Delta v - (\lambda/\mu) n|^2 = |\Delta v|^2$, that is, $-2 (\lambda/\mu)(\Delta v \cdot n) + \lambda^2/\mu^2 = 0$, that is, $\lambda = 0$ or $\lambda = 2 \mu (\Delta v \cdot n) = J$. $\square$

When the disks approach, $\Delta v \cdot n < 0$, so after the bounce $\Delta v' \cdot n > 0$ and they separate: a new call of TIME-TO-HIT on the pair has $b > 0$ and returns $\infty$. The root $\lambda = 0$ would let the disks pass through each other. A wall bounce (lines L19 and L20) reverses the component normal to the wall and keeps the other one, so it keeps $|v_i|$ and the kinetic energy.

**Theorem (the main loop).** Assume the start state is valid and that no two events have the same time. Then SIMULATE processes the collisions of the system in the order of time, each at its true time, with the right velocities after it.

*Proof.* Call an event in $Q$ *valid* when its stored counts equal the current counts of its disks. We prove by induction on the number of iterations that, at the start of each iteration with current time $t$:

> **(I)** The state at time $t$ is the true state of the system. For each disk $i$ and each disk $k$ (and each wall), if the true next contact of $i$ with $k$ on the current paths happens at a time $t' \le$ limit, then $Q$ holds a valid event $(t', i, k)$ or $(t', k, i)$. Each valid event in $Q$ is a true future contact on the current paths, at a time $\ge t$.

*Initialization.* At $t = 0$ the state is the input. Line L26 calls PREDICT for every disk, which by Lemmas 1 and 2 inserts each first contact on the current paths with the current counts.

*Maintenance.* Let $e$ be the event popped by line L28. If $e$ is stale, line L29 drops it, and (I) still holds, since a stale event is not counted by (I). Let $e$ be valid, at time $t_e$. Each valid event is a true future contact, so $t_e \ge t$. Assume that a true contact happens at a time $t'' < t_e$ between some disks $p$ and $q$ (or $p$ and a wall). The first such contact is the next contact of $p$ and $q$ on their current paths, so by (I) a valid event at $t''$ is in $Q$, and EXTRACT-MIN would return it before $e$. So no contact happens in $(t, t_e)$, all disks move on straight lines up to $t_e$, and line L30 gives the true state at $t_e$. Line L32 applies the true bounce, by Lemma 3 or the wall rule. Now only the paths of $e.a$ and $e.b$ change. Line L18 or lines L19 and L20 raise their counts, so every old event that involves them becomes stale. The events of other pairs keep their counts and remain true, since their paths did not change. Line L33 inserts the new next contacts of $e.a$ and $e.b$ with every other disk and with the walls, by Lemmas 1 and 2. So (I) holds at time $t_e$.

*Termination.* We assume, as the hard-disk model does, that only finitely many contacts happen up to the limit (no infinite chain of collisions in a finite time). Each valid event is a distinct contact, so there are finitely many of them. Each stale event was inserted by the start or by a valid event, and each call of PREDICT inserts at most $n + 2$ events. So the loop pops finitely many events and stops. When $Q$ is empty, no valid event at a time $\le$ limit remains, so by (I) no contact happens in $(t, \text{limit}]$, and line L34 moves every disk to its true position at the limit. $\blacksquare$

When several events have the same time, the order among them is the order of the queue. Then the result is one of the possible outcomes of the simultaneous contacts; a triple contact has no unique physical answer in the hard-disk model.
