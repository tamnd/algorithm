---
title: The sliding window returns the leftmost shortest window that contains the pattern
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with $m \ge 1$. For a substring $w$ and a character $c$, write $\mathrm{cnt}_w(c)$ for the number of copies of $c$ in $w$. A window $s[i \ldots j]$ with $i \le j$ is *valid* if $\mathrm{cnt}_{s[i \ldots j]}(c) \ge \mathrm{cnt}_t(c)$ for every $c$. For a start $i$, let $e(i)$ be the smallest $j \ge i$ with $s[i \ldots j]$ valid, or $\infty$. Write $s[i \ldots j]$ with $j < i$ for the empty window, which is not valid because $m \ge 1$.

**Lemma 1 (closed under super-windows).** If $s[i \ldots j]$ is valid, $i' \le i$ and $j' \ge j$, then $s[i' \ldots j']$ is valid. Equivalently, every part of a window that is not valid is not valid.

*Proof.* Each count in $s[i' \ldots j']$ is at least the same count in $s[i \ldots j]$. $\blacksquare$

**Lemma 2 (the counter).** Let $need[c] = \mathrm{cnt}_t(c) - \mathrm{cnt}_w(c)$ for a window $w$, and $missing = \sum_c \max(need[c], 0)$. Then $w$ is valid if and only if $missing = 0$. Adding one copy of $c$ to $w$ decreases $need[c]$ by 1 and decreases $missing$ by 1 if and only if $need[c] > 0$ before the change. Removing one copy of $c$ increases $need[c]$ by 1 and increases $missing$ by 1 if and only if $need[c] > 0$ after the change.

*Proof.* $missing = 0$ if and only if every $need[c] \le 0$, which is validity. The term $\max(need[c], 0)$ changes by 1 exactly when $need[c]$ moves between 1 and 0, in either direction, and does not change otherwise. $\blacksquare$

**Claim.** At the start of each step $r$ of the loop of line L2, and after the loop with $r = n$:

> **(W)** $0 \le l \le r$; $need$ and $missing$ are the values of Lemma 2 for the window $s[l \ldots r-1]$; this window is not valid; for each start $i < l$, $e(i) \le r - 1$, and the window $s[i \ldots e(i)]$ was examined at line L6; and $(bestlen, beststart)$ is the length and start of the shortest examined window, with the smallest start among the shortest, or $(\infty, 0)$ if none was examined.

On return, the output is the leftmost shortest valid window, or the empty string if no window is valid.

*Proof.* *Initialization.* Line L1 sets the values of Lemma 2 for the empty window $s[0 \ldots -1]$, which is not valid, and $l = 0$, so there is no start $i < l$.

*Maintenance.* Assume (W) at the start of step $r$. Lines L3 and L4 add $s_r$ to the window, and by Lemma 2 they keep $need$ and $missing$ correct for $s[l \ldots r]$. The loop of line L5 runs while $s[l \ldots r]$ is valid, by Lemma 2. Let $l_0$ be the value of $l$ before the loop. In each run with left end $l \ge l_0$, the window $s[l \ldots r-1]$ is a part of $s[l_0 \ldots r-1]$, which is not valid by (W), so $s[l \ldots r-1]$ is not valid by Lemma 1, while $s[l \ldots r]$ is valid. So $e(l) = r$, and line L6 examines the window $s[l \ldots e(l)]$. Lines L7 to L9 remove $s_l$ and keep $need$ and $missing$ correct for $s[l+1 \ldots r]$ by Lemma 2. So after each run, every start $i$ below the new $l$ has $e(i) \le r$ and its window was examined. The loop ends when $s[l \ldots r]$ is not valid; it ends because $s[r+1 \ldots r]$ is empty and not valid, so $l \le r + 1$. Line L6 keeps the shortest examined window, and replaces it only by a strictly shorter one; since the windows are examined in increasing order of start, the kept one has the smallest start among the shortest. So (W) holds at the start of step $r + 1$.

*Result.* After the last step, (W) holds with $r = n$. Every start $i < l$ has had its window $s[i \ldots e(i)]$ examined. For every start $i \ge l$, the window $s[i \ldots n-1]$ is a part of $s[l \ldots n-1]$, which is not valid, so $e(i) = \infty$. Every valid window $s[i \ldots j]$ has $j \ge e(i)$, so it is at least as long as $s[i \ldots e(i)]$, which was examined. So the shortest examined window is a shortest valid window, and its start is the smallest among them: if two valid windows have the minimum length $L$ and starts $i < i'$, both are of the form $s[i \ldots e(i)]$, and the one with start $i$ was examined first. If no window is valid, nothing was examined, $bestlen = \infty$, and line L10 returns the empty string. $\blacksquare$

**No skipped answer.** The left end passes a start $i$ only after line L6 has examined $s[i \ldots e(i)]$, the shortest valid window with start $i$. The right end passes an end $r$ only when $s[l \ldots r]$ is not valid, and by Lemma 1 no valid window $s[i \ldots r]$ with $i \ge l$ exists; the windows $s[i \ldots r]$ with $i < l$ are longer than $s[i \ldots e(i)]$ or equal to it, and that window was examined. So no candidate for the minimum is lost.

**Termination and cost.** Each run of the loop of line L5 increases $l$ by 1, and $l \le n$ always, so the loop of line L5 runs at most $n$ times in total. The loop of line L2 runs $n$ times. Each run costs $O(1)$. Line L1 costs $\Theta(m + \sigma)$. The total is $\Theta(n + m + \sigma)$. $\blacksquare$
