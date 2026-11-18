---
title: Footskate cleanup keeps every planted ankle on its target, changes the bones by at most the allowed factor, and leaves clean motion alone
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
The character is planar, with the hip (root) $h$, a thigh of length $l_1 > 0$ and a shin of length $l_2 > 0$ in each leg, and $\epsilon \ge 0$.
The direction $e(\varphi) = (\sin\varphi, -\cos\varphi)$ points down for $\varphi = 0$, and the ankle of a leg with thigh angle $\varphi$ and knee angle $\kappa$ is $h + l_1 e(\varphi) + l_2 e(\varphi + \kappa)$.
A plant of a leg is a run of frames; its target $c$ is the mean of the ankle positions of the input over the run (line L1).
On a frame with planted legs, $\rho = (1 + \epsilon)(l_1 + l_2)$ is the longest allowed leg.

We assume that on every planted frame:
- (A1) the disks of radius $\rho$ around the targets of the planted legs meet (else the code raises an error);
- (A2) the new hip is not too close to a target: $|\hat h - c| \ge s\,|l_1 - l_2|$ for the stretch factor $s$ of line L3.

## The root

**Lemma 1.** For one or two closed disks with a common point and a point $h$, line L2 returns the point $\hat h$ of the intersection $K$ nearest to $h$.

*Proof.*
$K$ is convex, closed and not empty, so it has a unique nearest point $\hat h$.
If $h \in K$, $\hat h = h$, and the code returns $h$.
Otherwise $\hat h$ is on the boundary of $K$.
If $\hat h$ is strictly inside one disk $D_2$, then near $\hat h$ the set $K$ equals the other disk $D_1$, so $\hat h$ is a local minimum of the distance to $h$ over $D_1$; a local minimum of a convex function on a convex set is global, so $\hat h$ is the projection of $h$ onto $D_1$.
If $\hat h$ is on both circles, it is one of the at most two intersection points of the circles.
The code lists the projections onto each disk and the intersection points of the circles, keeps those inside $K$, and returns the nearest to $h$; the list contains $\hat h$ and only points of $K$. $\square$

So the root moves as little as possible, and not at all when every planted target is already in reach of the longest allowed leg.

## The legs

**Lemma 2.** On a planted frame, for each planted leg with target $c$ and $d = |\hat h - c|$, the factor $s = \max(1, d/(l_1 + l_2))$ of line L3 satisfies $1 \le s \le 1 + \epsilon$ and $d \le s (l_1 + l_2)$.

*Proof.*
$d \le \rho$ by Lemma 1, so $d/(l_1 + l_2) \le 1 + \epsilon$.
If $d \le l_1 + l_2$, $s = 1$ and $d \le l_1 + l_2$; otherwise $s (l_1 + l_2) = d$. $\square$

**Lemma 3.** Let $a = s l_1$, $b' = s l_2$ and $|a - b'| \le d \le a + b'$ with $d > 0$.
Let $\psi$ be the angle with $e(\psi) = (c - \hat h)/d$, let $\alpha \in [0, \pi]$ and $\beta \in [0, \pi]$ be the angles of the triangle with sides $a$, $b'$, $d$ at the hip and at the knee (law of cosines), and let $\sigma = \pm 1$.
Then the leg with $\varphi = \psi - \sigma\alpha$ and $\kappa = \sigma(\pi - \beta)$ puts the ankle at $c$, and $\sigma\kappa \ge 0$.

*Proof.*
The knee is $k = \hat h + a\, e(\psi - \sigma\alpha)$, at the angle $\alpha$ from the line to the target, on the side that $\sigma$ selects.
In the triangle $\hat h, k, c$ the inner angle at $k$ is $\beta$, so the direction from $k$ to $c$ is the direction of the thigh turned by the outer angle $\pi - \beta$, toward the line $\hat h c$, which is the turn by $\sigma(\pi - \beta)$.
The side $|k - c|$ of this triangle is $b'$ by the law of cosines, so $k + b'\, e(\varphi + \kappa) = c$.
$\sigma\kappa = \pi - \beta \ge 0$. $\square$

**Theorem 1.** On every frame of every plant, the ankle of the planted leg after cleanup is exactly its target $c$.
So the planted foot does not move during the plant.

*Proof.*
By Lemma 2 and A2, $s|l_1 - l_2| \le d \le s(l_1 + l_2)$, so the target is reachable by a leg with the bones $s l_1$ and $s l_2$.
Line L4 computes the angles of Lemma 3, so the ankle is at $c$.
The frame keeps these angles and lengths, because the blend weight is 1 on planted frames. $\blacksquare$

**Theorem 2.** On every frame, each bone length is $(1 + w(s - 1))$ times its original length for some $w \in [0, 1]$ and some $s \in [1, 1 + \epsilon]$, so it changes by a factor in $[1, 1 + \epsilon]$, and the thigh and the shin of a leg change by the same factor.

*Proof.*
On planted frames $w = 1$ and $s$ is the factor of Lemma 2.
On other frames the code takes $s$ from the nearest planted frame and $w$ from the blend weight in $[0, 1]$. $\blacksquare$

## Clean motion and far frames

**Theorem 3.** Suppose that in the input every planted ankle is constant over its plant, is at most $l_1 + l_2$ from the hip, and its knee is not straight.
Then the output equals the input.

*Proof.*
Each target $c$ equals the constant ankle position, so every target is within $\rho$ of the hip, and Lemma 1 returns $\hat h = h$.
Then $d \le l_1 + l_2$ and $s = 1$.
For a reachable target with a bent knee there are exactly two planar solutions, one for each side of the knee, and line L4 takes the side of the input knee, so it returns the input angles.
All offsets and angle changes are zero, so every blended frame is also unchanged. $\blacksquare$

**Theorem 4.** A frame whose distance to every planted frame is more than $b$ is unchanged.

*Proof.*
Line L5 gives the weight $1 - u^2(3 - 2u)$ with $u = \delta/(b + 1)$ for a distance $\delta$, and 0 for $\delta \ge b + 1$.
A frame farther than $b$ from every planted frame has $\delta \ge b + 1$ for the nearest one, so its root offset and its leg changes are multiplied by 0 at lines L5 and L6. $\blacksquare$

The weight is 1 at $\delta = 0$, decreases, and has zero slope at both ends, so the change fades in and out without a jump of the root or the joint angles.

## In floating point

The straight leg is the hard case: at $d = l_1 + l_2$ the knee angle is an arc cosine near $-1$, where a rounding error of $u$ in the cosine gives an angle error near $\sqrt{2u}$.
The code returns the straight leg directly when $d \ge (l_1 + l_2)(1 - 10^{-12})$, so the test can check Theorem 1 within $10^{-9}$ on frames that need the full stretch.
