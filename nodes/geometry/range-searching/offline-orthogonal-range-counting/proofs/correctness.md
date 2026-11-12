---
title: The sweep with a Fenwick tree counts the points of every box in O((n + q) log(n + q)) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $P$ is a multiset of $n$ points, $Y = (Y_1 < \dots < Y_m)$ its distinct $y$-values, and the rank of a point is the index $r$ with $Y_r = p_y$. For a nonempty box $Q_i = [x_1, x_2] \times [y_1, y_2]$, $r_1 = |\{r : Y_r < y_1\}|$ and $r_2 = |\{r : Y_r \le y_2\}|$. The Fenwick tree $F$ supports ADD$(r, 1)$ and $\mathrm{PREFIX}(r)$, the sum of the counts at positions $1, \dots, r$.

**Claim.** OFFLINE-RANGE-COUNT returns $ans_i = |P \cap Q_i|$ for every $i$, in $O((n + q) \log (n + q))$ time and $O(n + q)$ space.

**Step 1 (what the tree holds).** Write $c_r$ for the count at position $r$. By induction over the events, after the POINT events of a set $S$ of points have been processed, $c_r$ is the number of points of $S$ with rank $r$, since each POINT event adds $1$ at its rank and nothing else changes the counts.

**Step 2 (reading a band of $y$).** For any set $S$ as in Step 1, $\mathrm{PREFIX}(r_2) - \mathrm{PREFIX}(r_1) = \sum_{r_1 < r \le r_2} c_r$, and $r_1 < r \le r_2$ holds exactly when $y_1 \le Y_r \le y_2$, because $Y$ is sorted. So the value read at line L6 is $|\{p \in S : y_1 \le p_y \le y_2\}|$.

**Step 3 (which points are in the tree).** Events are processed in the order of line L3. When the OPEN event of $Q_i$ at $x_1$ is processed, the POINT events processed before it are exactly those with $p_x < x_1$: points with smaller $x$ come earlier, and points with $p_x = x_1$ come later because OPEN precedes POINT at equal $x$. When the CLOSE event at $x_2$ is processed, the points processed are exactly those with $p_x \le x_2$, because POINT precedes CLOSE at equal $x$.

**Step 4 (the answer).** Let $B = \{p \in P : y_1 \le p_y \le y_2\}$. By Steps 2 and 3, $ans_i = |\{p \in B : p_x \le x_2\}| - |\{p \in B : p_x < x_1\}|$. Since $x_1 \le x_2$ for a nonempty box, the second set is contained in the first, and the difference is $|\{p \in B : x_1 \le p_x \le x_2\}| = |P \cap Q_i|$. Empty boxes get no events and keep $ans_i = 0 = |P \cap Q_i|$. Repeated points are separate POINT events and are counted with multiplicity.

**Step 5 (time and space).** There are $n + 2q$ events. Building $Y$ takes $O(n \log n)$, the $2q$ binary searches $O(q \log n)$, the sort $O((n + q) \log (n + q))$, and the sweep makes $n$ ADD and $4q$ PREFIX calls, each $O(\log m)$ by the Fenwick tree bound. The total is $O((n + q) \log (n + q))$. The events, $Y$, the tree and the answers take $O(n + q)$ space. The loop runs once per event, so the algorithm terminates. $\blacksquare$
