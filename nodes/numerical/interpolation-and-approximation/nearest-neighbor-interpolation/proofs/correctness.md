---
title: Nearest-neighbor interpolation returns the value of a nearest node, with the left node on a tie
proves: [correctness, termination, error]
status: full
---

**Claim.** Let $x_0 < \cdots < x_n$ and $x_0 \le t \le x_n$. NN-INTERPOLATE$(x, y, t)$ terminates and returns $y_k$ for an index $k$ with $|t - x_k| = \min_j |t - x_j|$; if two nodes are at the same smallest distance, $k$ is the smaller index.

*Proof.* If $n = 0$, line L1 returns $y_0$ and $x_0$ is the only node. Let $n \ge 1$.

*The search.* Lines L2 to L5 are the binary search of piecewise linear interpolation. Its invariant is $0 \le lo < hi \le n$ and $x_{lo} \le t \le x_{hi}$. It holds after line L2 by the precondition. A pass with $hi - lo > 1$ picks $lo < mid < hi$ and keeps $x_{lo} \le t \le x_{hi}$, since line L5 moves $lo$ to $mid$ only when $x_{mid} \le t$ and moves $hi$ to $mid$ only when $t < x_{mid}$. The gap $hi - lo$ drops from $g \ge 2$ to $\lfloor g/2 \rfloor$ or $\lceil g/2 \rceil$, both at most $g - 1$, so the loop stops, with $hi = lo + 1$. Write $j = lo$; then $x_j \le t \le x_{j+1}$.

*Only two candidates.* For $k < j$, $x_k < x_j \le t$, so $|t - x_k| = t - x_k > t - x_j = |t - x_j|$. For $k > j + 1$, $x_k > x_{j+1} \ge t$, so $|t - x_k| > |t - x_{j+1}|$. Hence every nearest node is $x_j$ or $x_{j+1}$, and every node other than these two is strictly farther than one of them, so it is never a tied nearest node.

*The choice.* Line L6 compares $|t - x_j| = t - x_j$ with $|t - x_{j+1}| = x_{j+1} - t$. If the first is smaller, $x_j$ is the unique nearest node; if the second is smaller, line L7 returns $y_{j+1}$ and $x_{j+1}$ is the unique nearest node; if they are equal, both are nearest and line L6 returns $y_j$, the smaller index. $\square$

**Error bound.** If $|f(u) - f(v)| \le L |u - v|$ on $[x_0, x_n]$ and $y_j = f(x_j)$, then $|f(t) - s(t)| \le L h/2$ with $h = \max_j (x_{j+1} - x_j)$.

*Proof.* With $j$ as above, the nearest node $x_k$ satisfies $|t - x_k| = \min(t - x_j, x_{j+1} - t) \le (x_{j+1} - x_j)/2 \le h/2$, because two nonnegative numbers with sum $x_{j+1} - x_j$ have a minimum of at most half of it. Then $|f(t) - s(t)| = |f(t) - f(x_k)| \le L |t - x_k| \le L h / 2$. $\blacksquare$
