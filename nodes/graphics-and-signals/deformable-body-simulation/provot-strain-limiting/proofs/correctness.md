---
title: Each correction is a projection, and repeated sweeps converge when the limits can hold
proves: [correctness]
status: full
---

We use the notation of the page.
A spring $s = (a, b, L)$ has the limit $r_s = (1 + \tau)(1 - \sigma) L$, where $\sigma \ge 0$ is the slack ($\sigma = 0$ in Provot's rule).
The variables are the positions of the free particles; a fixed particle is a constant.
Write $y$ for the vector of all free positions, and give it the norm $\|y\|_c^2 = \sum_i c_i |y_i|^2$, with $c_i = 1$ for Provot's equal split and $c_i = m_i$ for the mass split.
For a spring with at least one free end let

$$C_s = \{\, y : |x_b(y) - x_a(y)| \le r_s \,\}.$$

The vector $x_b - x_a$ is an affine function of $y$, and a ball is convex, so $C_s$ is a closed convex set.

## One correction

**Lemma 1.** Let $d = x_b - x_a$ with $l = |d| > r_s$ and $e = (l - r_s) d / l$, as in line L5.
After lines L6 to L8 the spring has the length $r_s$ and the same direction.
In the equal split the midpoint of the two particles stays; in the mass split their centre of mass stays.

*Proof.*
Both ends free: the new separation is $d - (s_a + s_b) e = d - e$, because $s_a + s_b = 1$.
One end free: the new separation is $d - e$ as well.
Now $d - e = (1 - (l - r_s)/l) d = (r_s / l) d$, which has the length $r_s$ and the direction of $d$.
The change of $x_a + x_b$ is $(s_a - s_b) e$, which is zero for $s_a = s_b = \frac12$.
For the mass split, $m_a s_a = m_a w_a / (w_a + w_b) = 1 / (w_a + w_b) = m_b s_b$, so the change $m_a s_a e - m_b s_b e$ of $m_a x_a + m_b x_b$ is zero. $\square$

**Lemma 2.** Lines L3 to L8 map $y$ to the closest point of $C_s$ in the norm $\|\cdot\|_c$.

*Proof.*
If $l \le r_s$, then $y \in C_s$ and line L4 keeps it, which is the closest point.
Let $l > r_s$.
Only the free ends of $s$ appear in the constraint, so the closest point changes only those.

Both ends free.
Write $\Delta_a$ and $\Delta_b$ for the moves and $d' = d + \Delta_b - \Delta_a$ for the new separation.
For a fixed $d'$, minimize $c_a |\Delta_a|^2 + c_b |\Delta_b|^2$ subject to $\Delta_b - \Delta_a = d' - d$.
The minimum is at $\Delta_a = -\frac{c_b}{c_a + c_b}(d' - d)$ and $\Delta_b = \frac{c_a}{c_a + c_b}(d' - d)$, with the value $\frac{c_a c_b}{c_a + c_b} |d' - d|^2$.
So the best $d'$ is the point of the ball $|d'| \le r_s$ closest to $d$, which is $d' = (r_s / l) d = d - e$.
Then $\Delta_a = \frac{c_b}{c_a + c_b} e$ and $\Delta_b = -\frac{c_a}{c_a + c_b} e$.
For $c_a = c_b = 1$ the factors are $\frac12$, which is line L6 in the equal split.
For $c_i = m_i = 1 / w_i$, $\frac{c_b}{c_a + c_b} = \frac{w_a}{w_a + w_b} = s_a$, which is line L6 in the mass split.

One end free, say $a$.
The new separation is $d - \Delta_a$, and the closest point of the ball to $d$ is $d - e$, so $\Delta_a = e$, which is line L7.
Line L8 is the same with the roles exchanged. $\square$

A spring with two fixed ends has no variables; line L4 skips it.

## Repeated sweeps

Let $P_s$ be the map of Lemma 2.
One sweep (line L2) is the composition of the $P_s$ in the order of the list.
Let $y^0$ be the input and $y^k$ the state after $k$ sweeps.

**Lemma 3.** For a closed convex set $C$, its projection $P$ and any $z \in C$,
$\|P y - z\|_c^2 \le \|y - z\|_c^2 - \|y - P y\|_c^2$.

*Proof.*
The projection is characterized by $\langle y - P y, z - P y \rangle_c \le 0$ for all $z \in C$.
Expand $\|y - z\|_c^2 = \|y - P y\|_c^2 + \|P y - z\|_c^2 + 2 \langle y - P y, P y - z \rangle_c$, and the last term is at least zero. $\square$

**Theorem 4.** If the sets $C_s$ have a common point, the states $y^k$ converge to a common point of all $C_s$.

*Proof.*
Let $z$ be a common point.
By Lemma 3 each single correction does not increase the distance to $z$, and the sum of the squared lengths of all moves over all sweeps is at most $\|y^0 - z\|_c^2$.
So the states are bounded, and the total move $\delta_k$ in sweep $k$ tends to zero, since a sweep has a fixed number of moves.
Take a subsequence $y^{k_j} \to \bar y$.
Inside sweep $k_j$, the state right after the correction of spring $s$ lies in $C_s$ and is within $\delta_{k_j}$ of $y^{k_j}$.
As $j \to \infty$ these states tend to $\bar y$, and $C_s$ is closed, so $\bar y \in C_s$ for every $s$.
Now apply the first sentence with $z = \bar y$: the distance $\|y^k - \bar y\|_c$ never increases, and it tends to zero along the subsequence, so it tends to zero. $\square$

This answers the remark of Provot (1995, Section 6) that the repeated procedure seems to converge: it does, whenever the limits can hold at the same time.
The theorem says nothing about one sweep, and the limit may be reached only in the limit of infinitely many sweeps.

**Corollary 5.** Let $\sigma > 0$, and let the sets $C_s$ with the shortened limits $r_s = (1 + \tau)(1 - \sigma) L$ have a common point.
Then after a finite number of sweeps no spring is longer than $(1 + \tau) L$, and the loop of line L1 stops.

*Proof.*
By Theorem 4 the states converge to a point $\bar y$ where every spring has length at most $(1 + \tau)(1 - \sigma) L < (1 + \tau) L$.
The lengths are continuous in $y$, and there are finitely many springs, so there is a ball around $\bar y$ where every spring is shorter than $(1 + \tau) L$.
The states enter the ball after finitely many sweeps. $\square$

**A sufficient condition.** If every fixed particle is at its rest position and $(1 + \tau)(1 - \sigma) \ge 1$, the rest shape is a common point, because there every spring has the length $L$.
The test with pins at the rest positions uses this.

**When the limits cannot hold.** If the fixed particles force a stretch, no common point exists and the loop cannot stop.
For a chain of $n$ springs of rest length $L$ between two fixed particles at the distance $D$, the triangle inequality gives $\sum l_s \ge D$, so some spring has $l_s \ge D / n$.
For $D = 1.3\, n L$ some spring is at least 30% too long after any number of sweeps.
This is the case that Bridson, Fedkiw and Anderson (2002, Section 4) name.

**One sweep is not enough.** Take three free particles at $0$, $1.5$ and $3.5$ on a line, two springs of rest length 1 and $\tau = 0.1$.
The first correction moves the first two particles to $0.2$ and $1.3$.
The second spring then has the length $2.2$, and its correction moves the last two particles to $1.85$ and $2.95$.
Now the first spring has the length $1.65$, a strain of 65%.
A later correction can stretch a spring that an earlier one fixed, so a single sweep gives no bound on the strain.

## The step

Lines L9 to L11 call the explicit step, then the sweeps, then set $v = (x_{\text{new}} - x) / \Delta t$.
So the positions at the end of the step obey the statements above, and the velocity is the one of the straight move from the old to the new positions.
For a fixed particle, $x_{\text{new}} = x$ and the velocity is zero.
