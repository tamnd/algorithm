---
title: Bottom-left fill puts each rectangle at its lexicographically least feasible position
proves: [correctness, termination]
status: full
---

**Setting.** The strip is $[0, W] \times [0, \infty)$. A placed rectangle is $Q = [x', x' + w'] \times [y', y' + h']$. A position $(x, y)$ of a new $w \times h$ rectangle, with $0 < w \le W$ and $h > 0$, is *feasible* when $0 \le x \le W - w$, $y \ge 0$, and the interior of $[x, x + w] \times [y, y + h]$ meets the interior of no placed rectangle. Two closed boxes have meeting interiors exactly when their open $x$-intervals meet and their open $y$-intervals meet, so $(x, y)$ is blocked by $Q$ if and only if
$$y' < y + h,\quad y' + h' > y,\quad x' < x + w,\quad x' + w' > x. \tag{1}$$

**Claim.** Let $P$ be a finite set of placed rectangles with pairwise disjoint interiors inside the strip. Lines L3 to L10 return the feasible position $(x^*, y^*)$ that is least in the order of $(y, x)$, that is, least $y$ first and least $x$ among those. Hence BLF places every rectangle, the placed rectangles stay pairwise disjoint in their interiors, and each one is at its bottom-left position with respect to the ones before it.

**Step 1 (a least position exists).** Let $F$ be the set of feasible positions. Condition (1) is a conjunction of strict inequalities, so the set of positions blocked by $Q$ is open, and $F$ is the closed set $[0, W - w] \times [0, \infty)$ minus a finite union of open sets. So $F$ is closed. It is not empty: with $T$ the largest top $y' + h'$ (or $0$ if $P$ is empty), the position $(0, T)$ fails $y' + h' > y$ for every $Q$. The set $F \cap \{y \le T\}$ is closed and bounded, so it has a point with least $y$, call it $y^*$. The section $\{x : (x, y^*) \in F\}$ is closed, bounded and not empty, so it has a least element $x^*$.

**Step 2 (the least height is a candidate).** Let $Y = \{0\} \cup \{y' + h' : Q \in P\}$. Suppose $y^* \notin Y$. Then $y^* > 0$. Take $\delta > 0$ smaller than $y^*$ and smaller than $y^* - t$ for every top $t \in Y$ with $t < y^*$. We claim $(x^*, y^* - \delta) \in F$, which contradicts the choice of $y^*$. Let $Q$ satisfy (1) at $(x^*, y^* - \delta)$. Its $x$ conditions do not depend on $y$, so they hold at $(x^*, y^*)$ too. Also $y' < y^* - \delta + h < y^* + h$. Since $(x^*, y^*)$ is feasible, (1) fails there, so $y' + h' \le y^*$. With $y' + h' > y^* - \delta$, the top $y' + h'$ lies in $(y^* - \delta, y^*]$. It is not $y^*$, because $y^* \notin Y$, so it lies in $(y^* - \delta, y^*)$, which the choice of $\delta$ excludes. So no $Q$ blocks $(x^*, y^* - \delta)$, and $y^* \in Y$.

**Step 3 (the row scan).** Fix $y \in Y$. Let $Q_1, \dots, Q_m$ be the rectangles with $y' < y + h$ and $y' + h' > y$, the band of line L6, sorted by $a_k = x'_k$, and let $b_k = x'_k + w'_k$. By (1), a position $(x, y)$ with $x \ge 0$ is blocked by $Q_k$ exactly when $x \in I_k = (a_k - w, b_k)$. Let $x_k$ be the value of $x$ after the loop has handled $Q_1, \dots, Q_k$ without a break, with $x_0 = 0$. We show by induction that

(a) $x_k \ge b_j$ for every $j \le k$, so $x_k$ is in none of $I_1, \dots, I_k$, because each of them is open at its right end $b_j$;

(b) every $t \in [0, x_k)$ lies in some $I_j$ with $j \le k$.

Both hold for $k = 0$. For the step, look at $Q_{k+1}$ at line L7. If $a_{k+1} \ge x_k + w$, the loop breaks. Otherwise $a_{k+1} - w < x_k$, and line L8 sets $x_{k+1} = \max(x_k, b_{k+1})$. Then (a) holds for $k + 1$ at once. For (b), take $t \in [0, x_{k+1})$. If $t < x_k$, use (b) for $k$. Otherwise $x_k \le t < b_{k+1}$, and with $a_{k+1} - w < x_k$ this gives $t \in I_{k+1}$.

Let the loop end with the value $\hat x$, after a break at $Q_{k+1}$ or after all $m$ rectangles. In the case of a break, $a_j \ge a_{k+1} \ge \hat x + w$ for all $j > k$, so $\hat x \notin I_j$ for $j > k$. With (a), $\hat x$ is in no $I_j$, and by (b) every smaller $t \ge 0$ is in some $I_j$. So $\hat x$ is the least $x \ge 0$ that no rectangle blocks at height $y$. Rectangles outside the band do not block at height $y$ by (1). Hence row $y$ has a feasible position if and only if $\hat x + w \le W$, which is the test of line L9, and then $\hat x$ is the least feasible $x$ in that row.

**Step 4 (the answer).** Line L4 tries the heights of $Y$ in increasing order and returns at the first one whose row has a feasible position, with the least $x$ in that row. By Step 2, $y^* \in Y$, and no $y < y^*$ has a feasible position, so the first such height is $y^*$, and the returned $x$ is $x^*$. The largest element $T$ of $Y$ has an empty band, so line L9 succeeds there with $\hat x = 0 \le W - w$, and the loop of line L4 always returns.

**Corollaries.** The returned position is feasible, so the interiors stay disjoint, and by induction on the input order this holds for the whole output. With integer sizes, every element of $Y$ and every value of $x$ in the scan is a sum of input numbers, so the bottom-left position is a pair of integers. That is why a brute force over all integer positions finds the same position. For Fraction input the same holds with all values in the additive group generated by the sizes.

**Termination.** Each loop runs over a finite list, and the outer loop of line L2 places one rectangle per pass. $\blacksquare$
