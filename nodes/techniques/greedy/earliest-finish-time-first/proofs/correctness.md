---
title: Earliest finish time first returns a maximum set of compatible activities
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a finite set $S$ of $n \ge 0$ activities, each with $s(a) < f(a)$ and the half-open interval $[s(a), f(a))$. Two distinct activities $a, b$ are compatible when $f(a) \le s(b)$ or $f(b) \le s(a)$. Line L1 gives the order $a_1, \ldots, a_n$ with $f(a_1) \le \cdots \le f(a_n)$; ties are in any order. Let $i_1, i_2, \ldots, i_k$ be the activities appended in line L6, in the order of appending.

**Claim.** The algorithm stops after $n$ iterations, and the returned list $A = (i_1, \ldots, i_k)$ is a set of pairwise compatible activities of the largest possible size.

**Termination.** The loop of line L4 runs for $i = 1, \ldots, n$, and each iteration does a bounded number of steps. So the algorithm stops.

**Step 1: the invariant.** Before the iteration for $i$, with $1 \le i \le n + 1$:

> **(I)** the activities in $A$ are pairwise compatible; they appear in $A$ in non-decreasing order of finish time; and $last = -\infty$ if $A$ is empty, else $last$ is the finish time of the last activity of $A$, which is the largest finish time in $A$.

*Initialization.* Before the first iteration, $A$ is empty and $last = -\infty$ by lines L2 and L3. All three parts hold.

*Maintenance.* Assume (I) before the iteration for $i \le n$. If the test of line L5 fails, nothing changes and (I) holds before the next iteration. If it passes, then $s(a_i) \ge last$. Each activity $b$ in $A$ has $f(b) \le last$ by (I), so $f(b) \le s(a_i)$, and $b$ is compatible with $a_i$. The activities of $A$ come from $a_1, \ldots, a_{i-1}$, so $a_i$ is not one of them and each has finish time at most $f(a_i)$. After lines L6 and L7, $A$ is pairwise compatible, it is in non-decreasing order of finish time, and $last = f(a_i)$ is the finish time of its last activity and its largest finish time.

*Termination of the loop.* After the iteration for $i = n$, (I) holds, so $A$ is a set of pairwise compatible activities.

**Step 2: what the scan sees between two choices.** Let $i_0$ be a dummy with $f(i_0) = -\infty$. For $1 \le r \le k$, while the loop processes the activities strictly after $i_{r-1}$ in the sorted order (from the start if $r = 1$) and strictly before $i_r$, the value of $last$ is $f(i_{r-1})$, and none of these activities passes line L5. After $i_k$, the value of $last$ is $f(i_k)$, and no later activity passes line L5. Both statements hold because $last$ changes only in line L7, which runs exactly when an activity is appended.

So: **(S)** if an activity $x$ comes after $i_{r-1}$ in the sorted order and $s(x) \ge f(i_{r-1})$, then $x = i_r$ or $x$ comes after $i_r$; and if $r - 1 = k$, no such $x$ exists.

**Step 3: the greedy stays ahead.** Let $B$ be any set of pairwise compatible activities, and list it as $j_1, \ldots, j_m$ in non-decreasing order of finish time. For distinct compatible $j_{r-1}, j_r$ with $f(j_{r-1}) \le f(j_r)$, the case $f(j_r) \le s(j_{r-1})$ would give $f(j_r) \le s(j_{r-1}) < f(j_{r-1})$, which is false; so $f(j_{r-1}) \le s(j_r)$.

*Lemma.* For each $r$ with $1 \le r \le \min(k, m)$, $f(i_r) \le f(j_r)$.

*Proof by induction on $r$.* Set $f(j_0) = -\infty$, so the hypothesis $f(i_{r-1}) \le f(j_{r-1})$ holds for $r = 1$. Take $r \ge 1$ and assume $f(i_{r-1}) \le f(j_{r-1})$. Then $s(j_r) \ge f(j_{r-1}) \ge f(i_{r-1})$ (for $r = 1$ this is $s(j_1) \ge -\infty$). Suppose, for a contradiction, that $f(j_r) < f(i_r)$. Then $j_r$ comes before $i_r$ in the sorted order, because the sort is by finish time and the inequality is strict. Also $f(j_r) > s(j_r) \ge f(i_{r-1})$, so $j_r$ comes after $i_{r-1}$ in the sorted order (for $r = 1$, after the start). So $j_r$ is processed strictly between $i_{r-1}$ and $i_r$, with $s(j_r) \ge f(i_{r-1})$. By (S), $j_r = i_r$ or $j_r$ comes after $i_r$, which contradicts that $j_r$ comes before $i_r$. So $f(i_r) \le f(j_r)$. $\square$

**Step 4: optimality.** Suppose $m > k$. Then $j_{k+1}$ exists. If $k = 0$, then $n \ge m \ge 1$, and $a_1$ passes line L5 because $last = -\infty$, so $k \ge 1$; this is a contradiction. So $k \ge 1$, and by the lemma $f(i_k) \le f(j_k) \le s(j_{k+1})$. Also $f(j_{k+1}) > s(j_{k+1}) \ge f(i_k)$, so $j_{k+1}$ comes after $i_k$ in the sorted order, and $s(j_{k+1}) \ge f(i_k)$. By (S) with $r - 1 = k$, no such activity exists. This is a contradiction. So $m \le k$ for every compatible set $B$.

By Step 1, $A$ is compatible, and by Step 4 no compatible set is larger. So $A$ is a maximum set of pairwise compatible activities. $\blacksquare$

**Cost.** Line L1 is one sort of $n$ keys. Each of the $n$ iterations of lines L4 to L7 does one comparison and $O(1)$ other work. So the time is the time of the sort plus $\Theta(n)$.
