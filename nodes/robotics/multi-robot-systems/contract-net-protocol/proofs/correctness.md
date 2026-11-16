---
title: The contract net protocol for single-task robots gives a valid assignment in at most t rounds that is maximal, so it awards at least half as many tasks as possible, but its cost can be arbitrarily far from the optimum
proves: [correctness]
status: full
---

There are $r$ robots and $t$ tasks. $c_{ij}$ is the bid of robot $i$ for task $j$; it is a number, or it is missing when robot $i$ cannot do task $j$. Robot $i$ is *eligible* for task $j$ when $c_{ij}$ is not missing. Each robot does at most one task. Time is synchronous and runs in rounds. Lines L1 to L8 refer to the pseudocode on the [contract net protocol](/contract-net-protocol/) page. In a round, the managers announce a window $W$ of open tasks (all open tasks, or the first $k$ of them), each idle robot sends one bid for its cheapest eligible task in $W$ (ties to the smaller task index), and each manager that got bids awards its task to the lowest bid (ties to the smaller robot index). If no robot bids at all, the tasks of $W$ are closed without an award.

**Invariant.** At the start of each round: (a) the awards made so far form a partial assignment, that is, no task has two robots and no robot has two tasks; (b) a robot is idle exactly when it has no task; (c) every task that was closed without an award has no eligible idle robot.

**Lemma 1.** The invariant holds at the start of every round.

*Proof.* At the start, no task is awarded, all robots are idle and no task is closed, so (a) to (c) hold. Suppose they hold at the start of a round. Each idle robot sends at most one bid, so in line L7 each robot can win at most one task in this round, and it wins only if it was idle, so by (b) it had no task before. Each task gets at most one award, and an awarded task leaves the open list, so it is never awarded again. The winner leaves the idle set. So (a) and (b) hold after the round. For (c): tasks are closed in line L5 only when no idle robot sent a bid. An idle robot sends a bid whenever it is eligible for some task in $W$, so no idle robot is eligible for any task of $W$. The idle set never grows, so this stays true in later rounds, also for the tasks closed earlier. $\square$

**Theorem 1 (termination).** The protocol stops after at most $t$ rounds.

*Proof.* In each round, either some robot bids, and then at least one task gets an award in line L7 and leaves the open list, or no robot bids, and then all tasks of the nonempty window leave the open list in line L5. So the open list loses at least one task per round, and it starts with $t$ tasks. $\square$

**Theorem 2 (maximality).** When the protocol stops, no idle robot is eligible for a task without an award.

*Proof.* At the end the open list is empty, so every task without an award was closed in line L5. Apply (c) of Lemma 1. $\square$

Consider the bipartite graph with an edge from robot $i$ to task $j$ when $i$ is eligible for $j$. By Lemma 1 the awards are a matching $M$ in this graph, and by Theorem 2 the matching is maximal: no edge has both ends free.

**Corollary 3 (half of the maximum number of tasks).** $|M| \ge \frac12 |M^*|$ for every matching $M^*$, in particular for a maximum one.

*Proof.* Every edge of $M^*$ has an end that $M$ covers, by maximality. Each edge of $M$ covers two ends, and two edges of $M^*$ never share an end. So $|M^*| \le 2 |M|$. $\square$

**Theorem 4 (the cheapest pair).** With the full window, the eligible pair $(i, j)$ with the smallest bid $c_{ij}$ (ties to the smaller task, then to the smaller robot) is awarded in the first round.

*Proof.* In round 1 all tasks are open and all robots are idle. Robot $i$'s cheapest task is $j$, so it bids on $j$. Every other bid on $j$ is at least $c_{ij}$, and a tie goes to the smaller robot index, which is $i$ by the choice of the pair. So the manager of $j$ awards it to $i$. $\square$

**Theorem 5 (no bound on the cost ratio).** For every $M > 2$ there is an instance with $r = t = 2$ on which the protocol, with the full window or with a window of one task, returns cost $1 + M$, while the minimum cost assignment of both tasks costs $4$.

*Proof.* Let $c_{00} = 1$, $c_{01} = 2$, $c_{10} = 2$, $c_{11} = M$. With the full window, in round 1 both robots find task 0 cheapest and bid on it, and robot 0 wins it with bid 1. In round 2 robot 1 bids $M$ on task 1 and wins it. The total is $1 + M$. With a window of one task the rounds are the same. The other assignment, robot 0 to task 1 and robot 1 to task 0, costs $2 + 2 = 4$. $\square$

So the protocol is a greedy heuristic for the cost. When the robots can do any task and $r \ge t$, every task gets an award by Theorem 2, but the total cost has no constant factor bound. The test `test_ratio_to_optimum_is_unbounded` checks the instance above, and `test_cost_at_least_optimum_and_all_tasks_awarded` compares the cost with a brute force minimum over all assignments.

**Messages.** An announcement of one task goes to all $r$ robots. In a round with window $W$ there are $r |W|$ announcement messages, at most $r$ bids and at most $\min(r, |W|)$ awards. With a window of one task, each round handles exactly one task, so there are exactly $t$ rounds, $r t$ announcements, at most $r t$ bids and at most $\min(r, t)$ awards. With the full window, the window shrinks by at least one task per round, so the announcements are at most $r (t + (t - 1) + \dots + 1) = r t (t + 1) / 2$, and the bids at most $r t$.

**Window of one task.** With a window of one task, round $k$ is a sealed-bid auction of the $k$-th task in the given order among the idle eligible robots, won by the lowest bid. So the protocol is the same as a sequence of single-item auctions, and the test `test_batch_one_equals_sequential_auctions` checks this.
