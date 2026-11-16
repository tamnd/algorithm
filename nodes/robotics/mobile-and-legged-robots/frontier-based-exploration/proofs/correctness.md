---
title: Frontier exploration stops and maps every reachable free cell
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [frontier-based exploration](/frontier-based-exploration/) page. The world is a finite grid of $c$ cells, each free or occupied. Two cells are neighbors when they share a side. The robot's map gives each cell one of the states unknown, free and occupied.

**Assumptions.** (A1) The sensor is correct: it marks a cell free only if it is free, and occupied only if it is occupied, and it never changes a known cell. (A2) The sensor range is $r \ge 1$, so sensing at a cell reveals each of its neighbors: the neighbor is the first cell of the digital line toward the middle of one side of the square of radius $r$. (A3) The start cell is free, and min_size = 1, so line L3 keeps every frontier cell.

Let $R$ be the set of free cells that can be reached from the start by moves between free neighbors.

**Lemma 1 (the map stays correct and the robot stays safe).** At every moment, every cell marked free is free, every cell marked occupied is occupied, and the robot stands on a cell marked free.

*Proof.* Line L1 marks the start free, which is correct by (A3), and every other change of the map comes from the sensor, which is correct by (A1). The robot moves only along a path found by line L4, whose cells are marked free. $\square$

**Lemma 2 (each plan removes an unknown cell).** Let $u_k$ be the number of unknown cells when line L4 runs for the $k$-th time. If plan $k$ finds a path, then $u_{k+1} < u_k$.

*Proof.* After sensing at the robot's cell, all its neighbors are known by (A2). So the robot's cell is never a frontier cell when line L4 runs, and the path $P$ has at least two cells. Its last cell $t$ was a frontier cell when the plan was made, so $t$ had an unknown neighbor $v$. Line L7 senses at $t$, which reveals $v$ by (A2). Known cells never become unknown, so $u_{k+1} \le u_k - 1$. $\square$

**Theorem.** The method stops after at most $c$ plans, and when it stops, every cell of $R$ is marked free.

*Proof.* The number of unknown cells is between 0 and $c$, and by Lemma 2 it drops with every plan that finds a path. So after at most $c$ such plans, line L5 returns.

Suppose that when it returns, some cell of $R$ is not marked free. By Lemma 1, a cell of $R$ is never marked occupied, so that cell is unknown. Take a path $s = q_0, q_1, \dots, q_m$ of free neighbors from the start $s$ to that cell, and let $q_j$ be the first unknown cell on it; $j \ge 1$, since the start is marked free. The cells $q_0, \dots, q_{j-1}$ are known, and they are free, so by Lemma 1 they are marked free. Then $q_{j-1}$ is a frontier cell: it is marked free and has the unknown neighbor $q_j$. The robot stands on some cell marked free; to show that line L4 reaches $q_{j-1}$, it is enough that the robot's cell and $s$ are joined through cells marked free. Every path the robot took ran through cells marked free, and cells marked free stay marked free, so the robot's whole trail from $s$ is still a chain of cells marked free. Followed by $q_0, \dots, q_{j-1}$, it joins the robot to $q_{j-1}$ through cells marked free. So the breadth-first search of line L4 finds a path to a frontier cell, and line L5 does not return. This contradiction proves the claim. $\square$

**Remarks.** Only (A3) uses min_size = 1. With a larger minimum, Lemma 2 still holds, so the method still stops after at most $c$ plans, but a small frontier region can be dropped, and the second claim fails; the test `test_a_large_minimum_size_stops_at_once` shows the extreme case. With a noisy sensor, (A1) fails, and a cell of $R$ marked occupied by mistake can hide part of the world. The number of plans can be close to $c$: with $r = 1$ in a corridor of $L$ cells, the robot plans $L - 2$ times, which `test_corridor_by_hand` checks for $L = 10$. The test `test_explores_every_reachable_cell` checks Lemma 1 and the theorem on 25 random worlds.
