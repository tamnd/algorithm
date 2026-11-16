---
title: Every sweep of the elastic band keeps a valid band valid, so the path through the bubble centers stays free of collision
proves: [correctness]
status: full
---

We use the notation of the page and of the code. The obstacles are closed discs $D_j$ with centers $o_j$ and radii $r_j$, and

$$\rho(p) = \min_j \bigl(\|p - o_j\| - r_j\bigr).$$

A band is a list of points $b_0, \dots, b_m$. It is *valid* if $\rho(b_i) > 0$ for every $i$ and every two neighbors overlap, $\|b_{i+1} - b_i\| < \rho(b_i) + \rho(b_{i+1})$. The bubble of $b$ is the open disc $B(b)$ with center $b$ and radius $\rho(b)$. The method gives no convergence guarantee, and this proof does not claim one. It proves that the band stays safe in a fixed scene.

## Lemma 1: a bubble contains no obstacle point

**Claim.** If $\rho(b) > 0$ and $\|q - b\| < \rho(b)$, then $q$ lies outside every disc $D_j$.

*Proof.* For every $j$, $\|q - o_j\| \ge \|b - o_j\| - \|q - b\| > \|b - o_j\| - \rho(b) \ge r_j$, because $\rho(b) \le \|b - o_j\| - r_j$. $\square$

## Lemma 2: a valid band gives a free path

**Claim.** If $a$ and $b$ overlap, the segment from $a$ to $b$ lies in $B(a) \cup B(b)$. So the polyline through the points of a valid band is free of collision.

*Proof.* Let $d = \|b - a\| < \rho(a) + \rho(b)$ and $p = a + s(b - a)$ with $0 \le s \le 1$. Then $\|p - a\| = sd$ and $\|p - b\| = (1 - s)d$. If $sd < \rho(a)$, then $p \in B(a)$. Otherwise $sd \ge \rho(a)$ and $(1 - s)d = d - sd < \rho(a) + \rho(b) - \rho(a) = \rho(b)$, so $p \in B(b)$. With Lemma 1, no point of the polyline is in an obstacle. $\square$

## Lemma 3: the distance function is 1-Lipschitz

**Claim.** $|\rho(p) - \rho(q)| \le \|p - q\|$ for all $p, q$.

*Proof.* Each function $p \mapsto \|p - o_j\| - r_j$ is 1-Lipschitz by the triangle inequality, and the minimum of 1-Lipschitz functions is 1-Lipschitz: if the minimum at $q$ is attained by $j$, then $\rho(p) \le \|p - o_j\| - r_j \le \|q - o_j\| - r_j + \|p - q\| = \rho(q) + \|p - q\|$, and the same holds with $p$ and $q$ exchanged. $\square$

## Lemma 4: a move keeps the band valid

**Claim.** If the band is valid before line L5 handles point $i$, it is valid afterwards.

*Proof.* Line L6 accepts a candidate $c$ only if $\rho(c) \ge \rho_{\min} > 0$ and $c$ overlaps the current points $i - 1$ and $i + 1$; the test uses the current band, so a neighbor that moved earlier in the same sweep is tested at its new place. Only the two pairs that contain point $i$ change, and both are tested. If no candidate is accepted after the given number of halvings, point $i$ does not move. $\square$

## Lemma 5: a midpoint insertion keeps the band valid

**Claim.** If $a$ and $b$ overlap and $m = (a + b)/2$, then $\rho(m) > 0$, $a$ overlaps $m$, and $m$ overlaps $b$.

*Proof.* Let $d = \|b - a\| < \rho(a) + \rho(b)$; then $\|m - a\| = \|m - b\| = d/2$. By Lemma 3, $\rho(m) \ge \rho(a) - d/2$ and $\rho(m) \ge \rho(b) - d/2$, so

$$\rho(m) \ge \frac{\rho(a) + \rho(b)}{2} - \frac d2 > 0.$$

Also $\rho(a) + \rho(m) \ge \rho(a) + \rho(b) - d/2 > d - d/2 = d/2 = \|m - a\|$, so $a$ and $m$ overlap; the same argument with $a$ and $b$ exchanged shows that $m$ and $b$ overlap. $\square$

Line L7 inserts at most one midpoint into each pair of neighbors, and each such pair overlaps after the moves (Lemma 4). So no test is needed for the insertion; the condition of line L7 only decides whether a new bubble is useful.

## Lemma 6: a deletion keeps the band valid

**Claim.** If the band is valid and line L8 deletes point $i$, the band is valid afterwards.

*Proof.* Line L8 deletes point $i$ only if $\|b_{i+1} - b_{i-1}\| < \beta(\rho(b_{i-1}) + \rho(b_{i+1}))$ with $\beta = 0.5$ in the code. The radii are positive and $\beta < 1$, so $b_{i-1}$ and $b_{i+1}$ overlap. The deletion removes the two pairs that contain point $i$ and adds this one; the other pairs do not change. The loop then tests the new neighbors of the next point, so each deletion is tested on the current band. $\square$

## Theorem

**Claim.** If the input band is valid for $\rho$, then every call of `update` with the same $\rho$ returns a valid band with the same first and last point, and its polyline is free of collision. So `elastic_band` returns a valid band after any number of sweeps in a fixed scene.

*Proof.* Lines L2 to L6 move only the interior points, one at a time, and keep the band valid by Lemma 4. Line L7 keeps the first point and every old point and adds midpoints of overlapping pairs, so the band stays valid by Lemma 5. Line L8 deletes only interior points and keeps the band valid by Lemma 6. So the ends never change, and the result is valid. Lemma 2 gives a free polyline. Induction over the sweeps of line L1 gives the second sentence. Each sweep ends: the move loop runs at most `tries` tests per point, line L7 at most doubles the number of points, and every step of line L8 either deletes a point or advances $i$. $\blacksquare$

## Moving obstacles

The theorem needs a band that is valid for the scene used in the update. When the obstacles move between two updates, the old band may already cut a bubble of the new scene, and nothing in the update repairs that, because the tests of lines L6 and L8 assume overlap before the change. In practice the band stays valid when the obstacles move slowly compared with the radii of the bubbles: if every obstacle moves by at most $\delta$, then $\rho$ drops by at most $\delta$ at every point, and the band stays valid as long as every pair of neighbors has an overlap margin $\rho(b_i) + \rho(b_{i+1}) - \|b_{i+1} - b_i\|$ larger than $2\delta$ and every radius is larger than $\delta$.

## What is not proved

Nothing here says that the band converges, that its length goes down at every sweep, or that it reaches the shortest path of its homotopy class. The forces are rules of thumb: the contraction and the repulsion balance at a point that depends on the gains and on $\rho_0$, and a different choice gives a different band. The moves are small compared with the bubbles, so in practice the band stays on the same side of each obstacle, and a band that goes around the wrong side stays there; this is a local method, and the proof above does not need or show more.
