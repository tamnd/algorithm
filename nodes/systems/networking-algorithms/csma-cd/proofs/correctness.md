---
title: With frames of at least two end-to-end delays, CSMA/CD detects every collision
proves: [correctness]
status: full
---

**Model.** The bus is a line segment. Station $i$ sits at position $x_i$, measured in bit times of propagation, and the positions are distinct. A burst (a frame, a cut frame or a jam) that station $A$ sends during the time interval $[s_a, e_a)$ is present at position $y$ during $[s_a + |y - x_A|, \; e_a + |y - x_A|)$. Let $\tau = \max_{i,j} |x_i - x_j|$ be the end-to-end delay. A station *hears* a burst of another station when the burst is present at its own position. The protocol of the page gives two rules:

- (R1) *Carrier sense.* A station starts a frame at time $s$ only if no burst of another station is present at its position at time $s$.
- (R2) *Collision detection.* A station that hears another burst while it sends a frame stops the frame (line L6), so the frame is not reported as sent.

Two bursts *collide* if they come from different stations and are both present at some position $y$ at some time.

**Theorem.** If every frame lasts at least $2\tau$ bit times, then whenever a frame $a$ of station $A$ collides with a burst $b$ of station $B \ne A$, station $A$ hears $b$ before $a$ is complete. So no frame that collides is reported as sent.

*Proof.* Let $d = |x_A - x_B|$, with $0 < d \le \tau$. Let $L \ge 2\tau \ge 2d$ be the full length of frame $a$, so it would end at $s_a + L$. If $A$ stops $a$ earlier, it has heard some burst during $a$, and $a$ is not reported as sent; so we may assume that $A$ hears nothing before $s_a + L$ and derive a contradiction. Burst $b$ is present at $x_A$ during $[s_b + d, \; e_b + d)$.

First, a fact used twice. *If $s_b \ge e_a + d$, then $a$ and $b$ do not collide.* At any position $y$, $b$ arrives at $s_b + |y - x_B| \ge e_a + d + |y - x_B| \ge e_a + |y - x_A|$, by the triangle inequality $|y - x_A| \le d + |y - x_B|$. So $a$ has left $y$ before $b$ reaches it. By symmetry, if $s_a \ge e_b + d$ they do not collide either.

*Case 1: $s_b \ge s_a$.* By (R1), $b$ started at a time when $a$ was not present at $x_B$, that is, $s_b < s_a + d$ or $s_b \ge e_a + d$. The second option gives no collision by the fact, so $s_b < s_a + d$. Then $b$ reaches $x_A$ at time $s_b + d$, with

$$s_a \le s_b < s_b + d < s_a + 2d \le s_a + L.$$

So $b$ is present at $x_A$ from time $s_b + d$, a time at which $A$ is still sending $a$: $A$ hears $b$, against the assumption.

*Case 2: $s_b < s_a$.* By (R1), $a$ started at a time when $b$ was not present at $x_A$: $s_a < s_b + d$ or $s_a \ge e_b + d$. The second option gives no collision by the fact, so $s_a < s_b + d$. The burst $b$ is present at $x_A$ during $[s_b + d, e_b + d)$, which starts after $s_a$ and before $s_a + d \le s_a + L$. So $A$ hears $b$ during $a$, against the assumption.

In both cases $A$ hears $b$ while it sends $a$, and by (R2) the frame is stopped. $\square$

**Corollary.** Under the same condition, a frame that its sender completes (line L8) collides with no burst, so it is received intact at every position of the bus.

**The bound $2\tau$ is needed.** Take two stations $A$ and $B$ at distance $d = \tau$ and a frame length $L < 2d$. Let $A$ start a frame at time $0$, and let $B$ start a burst at a time $s_b$ with $\max(0, L - d) < s_b < d$. This interval is not empty because $L < 2d$. At time $s_b < d$ the frame of $A$ has not reached $B$, so (R1) lets $B$ start. The burst of $B$ reaches $A$ at $s_b + d > L$, after $A$ has finished, so $A$ hears nothing and reports the frame as sent. At position $x_B$, the frame of $A$ is present during $[d, d + L)$ and the burst of $B$ from $s_b < d$ until at least $s_b + 1$; for a burst of $B$ of length at least $d - s_b + 1$ they overlap, so a receiver at or near $B$ gets a garbled frame. The test of the implementation runs this case with $d = 300$, $L = 100$ and $s_b = 380 - 96$ relative to the start of $A$.

**Termination of one frame.** Each pass through lines L2 to L7 either completes the frame (line L8) or adds one to the attempt count. At 16 attempts line L9 drops the frame. So each frame leaves the station after at most 16 attempts, sent or dropped. Each wait of line L10 is finite, at most $1023 \cdot 512$ bit times. The probability that a frame is dropped depends on the load; with $k$ stations that keep colliding with each other the drop probability falls fast with the window size, and in the tests no frame is dropped. $\square$
