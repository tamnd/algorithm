---
title: The sweep for maximum overlap returns the depth
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is $n \ge 0$ intervals $I_j$ with end points $l_j, r_j$, all closed $[l_j, r_j]$ with $l_j \le r_j$, or all half-open $[l_j, r_j)$ with $l_j < r_j$, or all open $(l_j, r_j)$ with $l_j < r_j$. Let $c(x) = |\{j : x \in I_j\}|$ and $d = \max_x c(x)$, with $d = 0$ for $n = 0$.

**Claim.** SWEEP-MAX-OVERLAP returns $best = d$. For closed and half-open intervals, $c(at) = d$; for open intervals, $c(y) = d$ for all $y$ in an open gap $(at, at + \varepsilon)$ with $\varepsilon > 0$. For $n = 0$ it returns $(0, \mathrm{nil})$.

*Proof.* If $n = 0$ the loop does not run, and the result is $(0, \mathrm{nil})$. Let $n \ge 1$, and let $e_1, \ldots, e_{2n}$ be the events in the order of line L3. Call an interval *active after step $t$* if its start event is among $e_1, \ldots, e_t$ and its end event is not. Each interval has its start event before its end event in the order of line L3: if $l_j < r_j$ this follows from the coordinates, and if $l_j = r_j$ (closed only) the start comes first by the tie rule.

**Step 1 (the counter).** By induction on $t$, after line L6 of step $t$ the variable $count$ equals the number $A_t$ of intervals active after step $t$. Before the loop, $count = 0 = A_0$. A $+1$ event makes one more interval active, and a $-1$ event makes one active interval inactive (its start came earlier). So $count$ follows $A_t$.

**Step 2 (no overshoot).** Fix a step $t$ with event coordinate $x$. Every active interval has its start among $e_1, \ldots, e_t$, so $l_j \le x$, and its end not among them, so $r_j \ge x$.

- Closed: the active intervals all contain $x$, so $A_t \le c(x) \le d$.
- Half-open or open, $e_t$ a start event: all ends at $x$ come before all starts at $x$, so each end at $x$ is already processed, and an active interval has $r_j > x$. An active interval with $l_j = x$ started at this coordinate. Each active interval then contains every point of $(x, x + \varepsilon)$ with $\varepsilon = \min_j (r_j - x) > 0$ over the active ones, because $l_j \le x < y < r_j$. So $A_t \le d$.
- Half-open or open, $e_t$ an end event: no start at $x$ is processed yet, so each active interval has $l_j < x \le r_j$, and all contain the points of $(x - \varepsilon, x)$ for $\varepsilon = \min_j(x - l_j) > 0$. So $A_t \le d$.

Hence $best \le d$ at all times, since $best$ is a maximum of values $A_t$ or 0.

**Step 3 (the depth is reached).** Let $y$ be a point with $c(y) = d$, and let $J$ be the set of intervals that contain $y$; $|J| = d \ge 1$. Let $x = \max_{j \in J} l_j$, so $x \le y$, and let $e_t$ be the last start event with coordinate $x$.

- Closed: each $j \in J$ has $l_j \le x \le y \le r_j$. Its start has coordinate at most $x$, and it is processed by step $t$, since the starts at $x$ are processed by the last of them. Its end has coordinate $r_j \ge x$; if $r_j > x$ it comes later, and if $r_j = x$ it comes after all starts at $x$ by the tie rule. So all of $J$ is active after step $t$, and $A_t \ge d$.
- Half-open or open: each $j \in J$ has $l_j \le x$ and $r_j > y \ge x$ (for half-open, $y < r_j$; for open, $y < r_j$ too). Its start is processed by step $t$, and its end has a coordinate greater than $x$, so it is not processed. So $A_t \ge d$.

With Step 2, $A_t = d$. Line L7 then sets $best = d$ at step $t$ or has done so earlier, and it never sets $best$ above $d$.

**Step 4 (the witness).** Let $s$ be the step at which line L7 last changes $best$, to the value $d$. A change needs $count$ to grow, so $e_s$ is a start event; let $x$ be its coordinate. By Step 2 for a start event, the $d$ intervals active after step $s$ all contain $x$ in the closed case, and all contain $(x, x + \varepsilon)$ in the half-open and open cases. For half-open intervals, each active one has $l_j \le x < r_j$, so it contains $x$ too. So $c(at) = d$ for closed and half-open intervals, and $c = d$ on $(at, at + \varepsilon)$ for open intervals.

*Termination.* The loop processes each of the $2n$ events once. $\blacksquare$

**Cost.** Line L3 sorts $2n$ events; the loop does $2n$ steps of $O(1)$ work.
