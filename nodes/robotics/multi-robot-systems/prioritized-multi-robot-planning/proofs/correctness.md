---
title: Prioritized planning returns only conflict-free plans, each robot gets the earliest arrival that the robots before it allow, and the method is incomplete
proves: [correctness]
status: full
---

The workspace is a grid of $g$ free cells. Time is discrete. In each step a robot moves to one of the 4 neighbor cells or waits. A plan for robot $i$ is a path $\pi_i(0), \pi_i(1), \dots, \pi_i(T_i)$ with $\pi_i(0) = s_i$ and $\pi_i(T_i) = g_i$, and the robot stays at $g_i$ for all $t \ge T_i$. Write $\pi_i(t) = g_i$ for $t > T_i$. Two plans have a *vertex conflict* if $\pi_i(t) = \pi_k(t)$ for some $t$, and a *swap conflict* if $\pi_i(t) = \pi_k(t + 1)$ and $\pi_k(t) = \pi_i(t + 1) \ne \pi_i(t)$ for some $t$. A robot may move into a cell that another robot leaves in the same step. Lines L1 to L6 refer to the pseudocode on the [prioritized multi-robot planning](/prioritized-multi-robot-planning/) page.

The reservation table after robots $1, \dots, k$ (in priority order) holds the pairs $(\pi_i(t), t)$ for $t \le T_i$, the moves $(\pi_i(t), \pi_i(t+1), t)$, and for each goal $g_i$ the time $T_i$ from which it is held for ever. A space-time state $(c, t)$ is *blocked* if some earlier robot is at $c$ at time $t$, counting the parked robots. A move from $(c, t)$ to $(c', t + 1)$ is *forbidden* if $(c', t+1)$ is blocked or an earlier robot moves from $c'$ to $c$ at time $t$. A goal state $(g_k, t)$ is *final* if no earlier robot is at $g_k$ at any time $\ge t$.

**Lemma 1 (the search).** If there is a path in space-time from $(s_k, 0)$ to a final goal state that uses no blocked state and no forbidden move, and its arrival time is at most the horizon $H$, then the search of line L3 returns such a path with the smallest arrival time. Otherwise it returns nothing.

*Proof.* The search is [A*](/a-star-search/) on the graph of states $(c, t)$ with unit cost per step, so the cost of a state is its time $t$. The heuristic $h(c) = |c_r - g_r| + |c_c - g_c|$ changes by at most 1 per step, and a step costs 1, so it is consistent, and $h(g_k) = 0$. With a consistent heuristic, A* pops states in nondecreasing order of $f = t + h$, and each state is reached first by a shortest path. A goal state has $f = t$, so the first final goal state that is popped has the smallest time among all reachable final goal states. States are expanded only up to time $H$, so a path is found exactly when one with arrival time at most $H$ exists. The state graph is finite, $g (H + 1)$ states, so the search ends. $\square$

**Theorem 1 (soundness).** If line L6 returns plans, no two of them have a vertex conflict or a swap conflict.

*Proof.* Take robots $i$ before $k$ in the order. The plan of $k$ was found when the plan of $i$ was in the table. For $t \le T_k$, the state $(\pi_k(t), t)$ is not blocked, so $\pi_k(t) \ne \pi_i(t)$, both while $i$ moves and after $i$ parks. For $t > T_k$, robot $k$ is at $g_k$, and the goal state $(g_k, T_k)$ was final, so $\pi_i(t) \ne g_k$ for $t \ge T_k$. So there is no vertex conflict. A swap needs both robots to move in the same step. If $t < T_k$, the move of $k$ at time $t$ is not forbidden, so $i$ does not move the other way at time $t$. If $t \ge T_k$, robot $k$ does not move. So there is no swap conflict. $\square$

**Theorem 2 (what each robot gets).** Robot $k$ gets a plan with the earliest arrival time among all plans that avoid the plans of robots $1, \dots, k - 1$ and arrive by time $H$. The robots after $k$ have no effect on it.

*Proof.* This is Lemma 1 for robot $k$; the table holds only the plans of the robots before $k$. $\square$

So the method is greedy over robots. A robot with high priority takes its shortest path and ignores everyone after it, which can leave no room for them.

**Theorem 3 (incompleteness).** There is an instance with 2 robots that has a conflict-free plan, while prioritized planning returns nothing for both orders, for every horizon.

*Proof.* Take the grid of 2 rows and 4 columns with walls at $(1, 2)$ and $(1, 3)$:

```
row 0:  .  .  .  .
row 1:  .  .  #  #
```

Robot 0 starts at $(0, 2)$ with goal $(0, 1)$. Robot 1 starts at $(0, 0)$ with goal $(0, 3)$. The cell $(0, 1)$ is the only link between the part $\{(0, 0), (1, 0), (1, 1)\}$ and the dead end $\{(0, 2), (0, 3)\}$.

*Order 0 then 1.* Robot 0 moves to $(0, 1)$ at time 1 and parks there for ever. Robot 1 is at $(0, 0)$ at time 0, and it must pass $(0, 1)$ to reach $(0, 3)$. The state $((0,1), t)$ is blocked for every $t \ge 1$. So there is no plan for robot 1.

*Order 1 then 0.* The only shortest path of robot 1 is $(0, 0), (0, 1), (0, 2), (0, 3)$, so by Lemma 1 it takes it and parks at $(0, 3)$ from time 3. Robot 0 starts in the dead end. It cannot be at $(0, 1)$ at time 1, because robot 1 is there. It cannot move from $(0, 2)$ to $(0, 1)$ between times 1 and 2, because robot 1 moves from $(0, 1)$ to $(0, 2)$ then, which is a swap. From $(0, 3)$ it cannot reach $(0, 1)$ in one step. So robot 0 is in the dead end at time 2. Robot 1 is at $(0, 2)$ at time 2, so robot 0 is at $(0, 3)$. Between times 2 and 3 robot 1 moves into $(0, 3)$ and stays, so robot 0 must leave $(0, 3)$, and its only free neighbor is $(0, 2)$, which is a swap with robot 1. So there is no plan for robot 0.

*A plan exists.* At time 1 robot 0 moves to $(0, 1)$ and robot 1 waits. At time 2 robot 0 moves down to $(1, 1)$ and robot 1 follows into $(0, 1)$. At time 3 robot 1 moves to $(0, 2)$ and robot 0 moves back to $(0, 1)$. At time 4 robot 1 reaches $(0, 3)$. There is no vertex conflict and no swap, and the makespan is 4. $\square$

The test `test_every_order_has_no_plan_but_a_plan_exists` checks both orders and finds the makespan 4 with a breadth-first search over the joint states of both robots. The search over joint states is complete, which is the difference described on the [coupled and decoupled planning](/coupled-and-decoupled-planning/) page.

**Running time.** With $g$ free cells and horizon $H$, one search visits at most $g (H + 1)$ states with at most 5 moves each, so it costs $O(g H \log(g H))$ with a binary heap, and the whole method costs $O(r g H \log(g H))$ for $r$ robots. The reservation table holds one entry per step of every plan, $O(r H)$ entries. The default horizon in the code is $H = g (r + 1)$, which is a design choice and not a bound from the paper.
