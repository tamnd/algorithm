---
title: Chan's algorithm returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** For each finite nonempty list $P$ of points, CHAN-HULL returns the same list as ANDREW-HULL of [Andrew's monotone chain](/andrew-monotone-chain/) on $P$. So it returns the vertices of $\mathrm{conv}(P)$, each once, in counterclockwise order from the smallest point, and the two end points when $P$ lies on a line. Each call of CHAN-UPPER terminates.

**Notation.** As in the proof for Andrew's algorithm, $u \times w = u_x w_y - u_y w_x$, so $\mathrm{orient}(p, q, r)$ has the sign of $(q - p) \times (r - p)$, and $\mathrm{orient}$ is alternating: a swap of two arguments changes its sign. A nonzero vector $u$ is *forward* if $u_x > 0$, or $u_x = 0$ and $u_y > 0$, so $q - p$ is forward exactly when $p < q$. A forward $u$ has an angle $\theta(u) \in (-\pi/2, \pi/2]$.

**Lemma A (angles).** For forward $u, w$: $u \times w > 0 \iff \theta(w) > \theta(u)$, and $u \times w = 0 \iff \theta(w) = \theta(u)$. This is Lemma A of the proof for Andrew's algorithm.

**Chains.** For a finite set $G$ with distinct points $g_1 < \cdots < g_r$, let $\mathrm{UC}(G)$ be the reversed output of the upper scan of Andrew's algorithm (lines L9 to L12 of ANDREW-HULL) on these points. This is what line L8 computes for each group. By the paragraph on the upper scan in the proof for Andrew's algorithm, the upper scan outputs a decreasing chain from $g_r$ to $g_1$ with strict left turns and all of $G$ on or left of each edge. Reversing a chain reverses each edge, which exchanges left and right, and reverses each triple, which changes the sign of $\mathrm{orient}$. So $\mathrm{UC}(G) = u_0 < u_1 < \cdots < u_k$ satisfies:

- (C1) $u_0 = \min G$ and $u_k = \max G$;
- (C2) $\mathrm{orient}(u_{i-1}, u_i, u_{i+1}) < 0$ for $0 < i < k$;
- (C3) $\mathrm{orient}(u_i, u_{i+1}, s) \le 0$ for $0 \le i < k$ and each $s \in G$.

Write $d_i = u_{i+1} - u_i$, a forward vector. By (C2) and Lemma A, $\theta(d_0) > \theta(d_1) > \cdots > \theta(d_{k-1})$.

**Lemma 1 (the successor).** Let $\mathrm{UC}(P) = w_0, \ldots, w_K$ and $i < K$. Then $w_{i+1}$ is the unique point $q \in P$ with $q > w_i$ such that, for each $s \in P$ with $s > w_i$, either $\theta(s - w_i) < \theta(q - w_i)$, or $\theta(s - w_i) = \theta(q - w_i)$ and $|s - w_i| \le |q - w_i|$.

*Proof.* Write $p = w_i$ and $q = w_{i+1}$. Let $s \in P$ with $s > p$. By (C3), $(q - p) \times (s - p) \le 0$, so $\theta(s - p) \le \theta(q - p)$ by Lemma A. Suppose $\theta(s - p) = \theta(q - p)$ and $|s - p| > |q - p|$. Then $s - q$ is a positive multiple of $d_i$, so $s > q$, and $q \ne \max P$, so $i + 1 < K$. Now $d_{i+1} \times (s - q)$ has the sign of $d_{i+1} \times d_i$, which is positive because $\theta(d_i) > \theta(d_{i+1})$. So $s$ is strictly left of the edge $q \to w_{i+2}$, against (C3). So $q$ has the stated property. Two points with the property have the same angle from $p$ and the same distance from $p$, so they are equal. $\square$

**Lemma 2 (vertices lie above chords).** Let $p = w_i$ be a vertex of $\mathrm{UC}(P)$, and let $A, c \in P$ with $A \le p \le c$. Then $\mathrm{orient}(A, c, p) \ge 0$.

*Proof.* If $A = p$ or $c = p$, the value is 0. Otherwise $0 < i < K$, because $w_0 = \min P$ and $w_K = \max P$. Let $e = p - w_{i-1}$ and $f = w_{i+1} - p$, so $\theta(f) < \theta(e)$. The point $A$ is on or right of the edge $w_{i-1} \to p$, and $A - w_{i-1} = e - (p - A)$, so $e \times (e - (p - A)) = -e \times (p - A) \le 0$, and $\theta(p - A) \ge \theta(e)$ by Lemma A. The point $c$ is on or right of the edge $p \to w_{i+1}$: $f \times (c - p) \le 0$, so $\theta(c - p) \le \theta(f)$. So $\theta(c - p) < \theta(p - A)$ and $(p - A) \times (c - p) < 0$. Then $\mathrm{orient}(A, p, c)$ has the sign of $(p - A) \times (c - A) = (p - A) \times (c - p) < 0$, and $\mathrm{orient}(A, c, p) > 0$. $\square$

**Lemma 3 (monotone signs).** Let $\mathrm{UC}(G) = u_0, \ldots, u_k$, let $p$ be a point, and let $lo$ be the first index with $u_{lo} > p$. For $lo \le i < k$ let $\sigma_i = \mathrm{orient}(p, u_i, u_{i+1})$. If $\sigma_i < 0$ and $i + 1 < k$, then $\sigma_{i+1} < 0$.

*Proof.* Let $v = u_{i+1} - p$, forward because $u_{i+1} > u_{lo} > p$. Since $u_i - p = v - d_i$, the value $\sigma_i$ has the sign of $(v - d_i) \times d_i = v \times d_i$. So $v \times d_i < 0$, and by Lemma A, $\theta(d_i) < \theta(v)$. Then $\theta(d_{i+1}) < \theta(d_i) < \theta(v)$, so $v \times d_{i+1} < 0$, and $\sigma_{i+1}$ has the sign of $(u_{i+1} - p) \times (u_{i+2} - p) = v \times (v + d_{i+1}) = v \times d_{i+1} < 0$. $\square$

So on the indices $lo, \ldots, k - 1$ the predicate $\sigma_i < 0$ is false and then true. Lines T3 to T6 are a binary search for the first index $j^*$ in $[lo, k)$ where it is true, with the answer $k$ if there is none, and line T7 returns $c = u_{j^*}$. Lines T1 and T2 return none exactly when $\max G \le p$, by (C1).

**Lemma 4 (the tangent).** Let $p$ be a vertex of $\mathrm{UC}(P)$, let $G \subseteq P$ have a point larger than $p$, and let $c = \mathrm{TANGENT}(\mathrm{UC}(G), p)$. Then $c \in G$, $c > p$, and each $s \in G$ with $s > p$ and $s \ne c$ satisfies $\mathrm{orient}(p, c, s) \le 0$, with equality only when $s$ lies on the segment from $p$ to $c$.

*Proof.* $c = u_{j^*}$ with $j^* \ge lo$, so $c > p$. Let $v = c - p$, forward. Because $(c - p) \times (s - p) = v \times (s - c)$, we must show $v \times (s - c) \le 0$, with equality only for $s$ between $p$ and $c$. Take $s \in G$ with $s > p$ and $s \ne c$.

1. *Case $s > c$.* Then $c \ne \max G$, so $j^* < k$, and $\sigma_{j^*} < 0$. Let $B = u_{j^* + 1}$. As in the proof of Lemma 3, $\sigma_{j^*} < 0$ gives $v \times (B - c) < 0$, so $\theta(B - c) < \theta(v)$. By (C3), $(B - c) \times (s - c) \le 0$, so $\theta(s - c) \le \theta(B - c)$. So $\theta(s - c) < \theta(v)$ and $v \times (s - c) < 0$.

2. *Case $p < s < c$.* Let $w = c - s$, forward. Then $j^* > 0$, since $u_0 = \min G \le s < c$. Let $A = u_{j^* - 1}$ and $e = c - A$. By (C3) for the edge $A \to c$, $e \times (s - A) \le 0$. Since $s - A = e - w$, this gives $-e \times w \le 0$, so $\theta(w) \ge \theta(e)$. We now show $\theta(e) \ge \theta(v)$.
   - If $j^* > lo$, then $A > p$ and $\sigma_{j^* - 1} = \mathrm{orient}(p, A, c) \ge 0$, so $\mathrm{orient}(p, c, A) \le 0$: $v \times (A - c) = -v \times e \le 0$, and $\theta(e) \ge \theta(v)$.
   - If $j^* = lo$, then $A \le p < c$, and $A, c \in P$. By Lemma 2, $\mathrm{orient}(A, c, p) \ge 0$: $e \times (p - A) \ge 0$. Since $p - A = e - v$, this gives $-e \times v \ge 0$, so $\theta(v) \le \theta(e)$.

   So $\theta(w) \ge \theta(v)$, and $v \times w \ge 0$, so $v \times (s - c) = -v \times w \le 0$. If it is 0, then $s$, $p$ and $c$ are on one line and $p < s < c$, so $s$ is on the segment from $p$ to $c$. $\square$

**Lemma 5 (one wrap step).** Suppose that before line L11, $H = w_0, \ldots, w_i$ with $i < K$, where $\mathrm{UC}(P) = w_0, \ldots, w_K$. Then lines L11 to L15 append $w_{i+1}$.

*Proof.* Let $p = w_i$ and $q = w_{i+1}$. For a group $G$ with $\max G \le p$, TANGENT returns none, and the group is skipped. For each other group, Lemma 4 gives a candidate $c_G \in P$ with $c_G > p$. Each candidate is larger than $p$, so by Lemma 1, $\theta(c_G - p) \le \theta(q - p)$, and on equality $|c_G - p| \le |q - p|$. Let $G^*$ be a group that contains $q$. By Lemma 4 applied to $s = q$, either $c_{G^*} = q$, or $\theta(q - p) < \theta(c_{G^*} - p)$, or $q$ is on the segment from $p$ to $c_{G^*}$ and $q \neq c_{G^*}$. The last two contradict Lemma 1. So $q$ is a candidate.

By Lemma A, the test of line L14 replaces $best$ by $c$ exactly when $(\theta(c - p), |c - p|)$ is lexicographically larger than $(\theta(best - p), |best - p|)$. So after the loop, $best$ is a candidate whose pair is maximum. The pair of $q$ is larger than the pair of every other candidate, by Lemma 1, so $best = q$. $\square$

**Lemma 6 (CHAN-UPPER).** If $a = \min P < b = \max P$, then CHAN-UPPER$(P, a, b)$ terminates and returns $\mathrm{UC}(P)$.

*Proof.* In each round, $H$ starts as $[w_0] = [a]$. By Lemma 5 and induction, after $r$ steps $H = w_0, \ldots, w_r$ as long as $r \le K$, and $w_r = b$ only for $r = K$. So the round returns $\mathrm{UC}(P)$ at step $K$ if $K \le m$, and ends without a return if $K > m$. Since $P$ has at least $K + 1$ distinct points, $K \le n - 1$. The value of $m$ grows with $t$ until it equals $n$, so some round has $m \ge K$. $\square$

**Proof of the claim.** Line L1 handles the empty input, and line L2 the input with one distinct point, which is also what ANDREW-HULL returns. Otherwise $a < b$. Let ANDREW-HULL on $P$ build the lower chain $\Lambda = v_1, \ldots, v_k$ (from $a$ to $b$) and the upper chain $\Upsilon = y_1, \ldots, y_r$ (from $b$ to $a$), and return $v_1, \ldots, v_{k-1}, y_1, \ldots, y_{r-1}$. For two distinct points, line L2 of ANDREW-HULL returns $a, b$, which is the same list, since then $\Lambda = a, b$ and $\Upsilon = b, a$.

- By Lemma 6, $U = \mathrm{UC}(P) = \mathrm{reverse}(\Upsilon)$, so $\mathrm{reverse}(U)$ without its last point is $y_1, \ldots, y_{r-1}$.
- The smallest point of $-P$ is $-b$ and the largest is $-a$, so by Lemma 6 the call in line L4 returns $\mathrm{UC}(-P)$. The upper scan of Andrew's algorithm on $-P$ reads the points of $-P$ in decreasing order, which are $-p[1], -p[2], \ldots, -p[n]$, and makes the same orientation tests as the lower scan on $P$, because $\mathrm{orient}(-x, -y, -z) = \mathrm{orient}(x, y, z)$. So it outputs $-v_1, \ldots, -v_k$, and $\mathrm{UC}(-P) = -v_k, \ldots, -v_1$. Line L4 reflects it back: $L = v_k, \ldots, v_1$, and $\mathrm{reverse}(L)$ without its last point is $v_1, \ldots, v_{k-1}$.

So line L5 returns the output of ANDREW-HULL, which is the hull in counterclockwise order by the correctness proof of Andrew's algorithm. Termination follows from Lemma 6. $\blacksquare$
