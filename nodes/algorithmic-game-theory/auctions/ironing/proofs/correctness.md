---
title: Correctness of ironing by the concave hull
proves: [correctness]
status: full
---

Let the distribution have values $s_1 < \cdots < s_K$ with probabilities $f_1, \ldots, f_K > 0$. Write $q_k = \sum_{j \ge k} f_j$, so $q_1 = 1$, and put $q_{K+1} = 0$ and $s_{K+1} q_{K+1} = 0$. Line L1 builds the revenue curve: the points $P_0 = (0, 0)$ and $(q_k, s_k q_k)$ for $k = K, \ldots, 1$, in increasing order of $q$. The segment of value $s_k$ runs from $(q_{k+1}, s_{k+1} q_{k+1})$ to $(q_k, s_k q_k)$. It has length $f_k$ and slope $\varphi_k = (s_k q_k - s_{k+1} q_{k+1})/f_k$, the virtual value. Let $\bar R$ be the least concave function on $[0, 1]$ that lies on or above all the points, and let $\bar\varphi_k$ be its slope on the segment of $s_k$.

## Claim 1: line L2 returns the vertices of $\bar R$

The scan keeps a stack $h$ of point indices. Invariant: after point $k$ is processed, the stack holds the vertices of the upper hull of points $0, \ldots, k$, in order, with strictly decreasing slopes between consecutive entries. This holds after point 0. When point $k$ arrives, the loop removes the top entry $t$ while $t$ lies on or below the chord from the entry under it to point $k$. Such a $t$ cannot be a vertex of the hull of points $0, \ldots, k$, because it lies on or below a segment between two points of the set. When the loop stops, the last two entries and point $k$ make a strict right turn, so the slopes still decrease strictly. Entries below were vertices before and stay vertices, since the new point lies to their right and the slopes decrease. So the invariant holds. At the end, the stack holds the vertices of the upper hull of all the points, from $P_0$ to $(1, s_1)$, and the piecewise linear function through them is concave and lies on or above every point, so it is $\bar R$. Each point enters and leaves the stack at most once, so the scan takes $O(K)$ steps.

## Claim 2: lines L3 to L6 give the slopes of $\bar R$, and they are nondecreasing in the value

Between consecutive vertices $a$ and $b$, $\bar R$ is the chord, so every segment of the curve from point $a$ to point $b$ gets the slope $m$ of the chord (line L4). The slopes of the hull decrease strictly from one chord to the next as $q$ grows. Since $q_k$ decreases as $k$ grows, $\bar\varphi_1 \le \cdots \le \bar\varphi_K$. Line L6 reverses the list so that it is in increasing order of value.

If the chord from $a$ to $b$ spans one segment only ($b = a + 1$), then $\bar\varphi = \varphi$ there. Otherwise line L5 records the value indices of points $a + 1, \ldots, b$ as an ironed interval. Curve point $j$ belongs to value index $K - j$ in increasing order, which is the conversion used in line L5. Every value outside the recorded intervals has its own chord, so $\bar\varphi_k = \varphi_k$ there.

## Claim 3: the mean of $\varphi$ on an ironed interval is the ironed value

On an ironed interval with values $s_{\ell}, \ldots, s_h$, the curve and the hull meet at both ends, the vertices $a$ and $b$. So $\sum_{k = \ell}^{h} f_k \varphi_k$, the rise of the curve over the interval, equals $\sum_{k = \ell}^{h} f_k \bar\varphi_k = \bar\varphi_\ell \sum_{k = \ell}^{h} f_k$, the rise of the hull. Over all values, both sums telescope from $(0, 0)$ to $(1, s_1)$: $\sum_k f_k \varphi_k = \sum_k f_k \bar\varphi_k = s_1$, the lowest value.

## Claim 4: ironing never lowers the virtual surplus of a monotone allocation, and keeps it when the allocation is flat on ironed intervals

Let $0 \le x_1 \le \cdots \le x_K$ and put $x_0 = 0$. Write $G_k = \sum_{j \ge k} f_j \varphi_j = s_k q_k$ and $\bar G_k = \sum_{j \ge k} f_j \bar\varphi_j = \bar R(q_k)$, with $G_{K+1} = \bar G_{K+1} = 0$. Summation by parts gives

$$\sum_k f_k x_k (\bar\varphi_k - \varphi_k) = \sum_{k \ge 1} (x_k - x_{k-1}) (\bar G_k - G_k).$$

Each factor $x_k - x_{k-1}$ is nonnegative, and $\bar G_k - G_k \ge 0$ because the hull lies above the curve. So the sum is at least 0. The term $k = 1$ is 0, since $(1, s_1)$ is a vertex. For $k \ge 2$, $\bar G_k > G_k$ only if the point $(q_k, s_k q_k)$ lies strictly below the hull, and then it is an inner point of an ironed interval that contains both $s_{k-1}$ and $s_k$. If $x$ is constant on each ironed interval, then $x_k = x_{k-1}$ for every such $k$, and the sum is 0.

This is the step that lets [Myerson's optimal auction](/myerson-optimal-auction/) replace $\varphi$ by $\bar\varphi$: its allocation depends on the value only through $\bar\varphi$, so it is constant on ironed intervals, and its revenue is the expected ironed virtual surplus. For any other monotone allocation, the expected ironed virtual surplus is an upper bound on the revenue.
