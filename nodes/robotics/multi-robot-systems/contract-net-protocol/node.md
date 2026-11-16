---
tag: JAEWRV
kind: algorithm
slug: contract-net-protocol
name: Contract net protocol
aliases:
- CNP
area: robotics/multi-robot-systems
level: core
summary: Smith's protocol in which a manager announces a task, contractors bid, and the manager awards the contract to the best bid.
solves: [multi-robot-task-allocation]
model: real-ram
complexity:
  vars: {r: the number of robots, t: the number of tasks}
  time: {per_round: O(r t), total: O(r t^2)}
  messages: {full_window: O(r t^2), one_task_window: O(r t)}
  space: {extra: O(r + t)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 1980
  people: [Reid G. Smith]
  note: Smith designed the contract net for distributed problem solving with announcements, bids and awards between managers and contractors; robot teams later used it as the basic single-item auction.
prereqs: [multi-robot-task-allocation, market-based-task-allocation]
see_also: [consensus-based-bundle-algorithm, auction-algorithm, hungarian-algorithm, assignment-problem, multi-robot-system, synchronous-model]
sources:
  - paper: doi:10.1109/TC.1980.1675516
    title: Reid G. Smith, The contract net protocol, high-level communication and control in a distributed problem solver, IEEE Transactions on Computers C-29(12), 1980
    locator: pages 1104 to 1113 (task announcement, bid, award and the message formats)
  - paper: doi:10.1177/0278364904045564
    title: Brian P. Gerkey and Maja J. Mataric, A formal analysis and taxonomy of task allocation in multi-robot systems, International Journal of Robotics Research 23(9), 2004
    locator: pages 939 to 954 (the single-task, single-robot, instantaneous class and the analysis of greedy auction methods)
  - paper: doi:10.1109/JPROC.2006.876939
    title: M. Bernardine Dias, Robert Zlot, Nidhi Kalra and Anthony Stentz, Market-based multirobot coordination, a survey and analysis, Proceedings of the IEEE 94(7), 2006
    locator: pages 1257 to 1270 (single-item auctions and the contract net in robot teams)
---

The contract net protocol assigns tasks to agents by announcement, bid and award. The agent that holds a task acts as its *manager*: it announces the task, the idle agents that can do it reply with a bid, and the manager gives the contract to the best bid. Reid Smith designed it in 1980 for distributed problem solving, and robot teams use it as the simplest market for [multi-robot task allocation](/multi-robot-task-allocation/). Unlike the [auction algorithm](/auction-algorithm/) it never revises an award, and unlike the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) it gives one task per robot through managers that hear all bids, so it is fast but greedy, and its total cost has no bound against the optimum.

## In plain words

A robot team has jobs to do. For each job, someone shouts "who can do this, and at what cost?" Every free robot that can do the job answers with its cost, but a robot answers only for the job it likes best, so it never promises two jobs at once. The one who shouted picks the cheapest answer and tells that robot "the job is yours". The winner is now busy. The others wait for the next call.

This is quick, because each robot only has to price a few jobs and send a few short notes. It is also short-sighted: the cheapest robot for the first job may be the only robot that could do a later job well, and the protocol never takes such a choice back.

## The problem

**The model.** There are $r$ robots and $t$ tasks. Robot $i$ has a cost $c_{ij}$ for task $j$, in any unit (seconds, meters or energy), or no cost if it cannot do the task. Each robot does at most one task, and each task needs one robot: this is the single-task robot, single-robot task, instantaneous class (ST-SR-IA) of Gerkey and Matarić (2004). Every task has a manager, which can be a robot or an operator console. The communication graph is complete: an announcement reaches every robot, and a bid or an award is one message to one agent. Time is synchronous, in rounds of announce, bid and award.

**Input.** The costs $c_{ij}$, the order in which the managers announce, and the window size: how many open tasks are announced in each round (all of them, or one at a time).

**Output.** An assignment of tasks to robots, the total cost, the number of rounds, and the messages sent.

**How it differs from close pages.** [Multi-robot task allocation](/multi-robot-task-allocation/) is the problem, and [market-based task allocation](/market-based-task-allocation/) is the general method of auctions; the contract net is the oldest concrete protocol of that method, with one item per auction and no re-trading. The [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) has no managers: each robot claims a bundle of tasks and the team agrees by message passing between neighbors, with a 50 percent bound under diminishing marginal gain. The [auction algorithm](/auction-algorithm/) of Bertsekas raises prices over many rounds and reaches an optimal assignment within $\varepsilon$, which the contract net does not. The [Hungarian algorithm](/hungarian-algorithm/) solves the same assignment exactly, but centrally.

## The algorithm

```pseudo id=main
CONTRACT-NET(c, order, k)
L1  open ← the tasks in announcement order;  idle ← all robots
L2  while open ≠ ∅ do
L3      W ← the first k tasks of open (or all of open);  each manager of a task in W announces it to every robot
L4      each idle robot i sends one bid (c_ij, i) for its cheapest eligible task j in W
L5      if no robot sent a bid then  remove W from open;  continue
L6      for each task j in W that received bids do
L7          award j to the bid with the smallest (c_ij, i);  remove j from open and the winner from idle
L8  return the awards
```

Line L3 is the *task announcement*. Line L4 is the *bid*: a robot bids only once per round, on the task it likes best, so it can never win two tasks in one round, which is what keeps robots single-task. Ties go to the smaller task index. Line L7 is the *award*, with ties to the smaller robot index. Robots that lost stay idle and bid again in the next round. Line L5 closes the window only when nobody bid at all: then no idle robot can do any task of the window, and since robots never become idle again, nobody ever will.

With $k = 1$ each round is one sealed-bid auction of one task, so the protocol is a sequence of single-item auctions in the announcement order. With the full window all managers announce at once and the robots choose between the offers.

## Example

Three robots and two tasks, with costs in seconds:

| | task 0 | task 1 |
|---|---|---|
| robot 0 | 1 | 2 |
| robot 1 | 10 | 3 |
| robot 2 | 1.5 | 2.5 |

**Full window.** Round 1: both tasks are announced to 3 robots, 6 messages. Robot 0 bids 1 on task 0, robot 1 bids 3 on task 1, and robot 2 bids 1.5 on task 0. Task 0 goes to robot 0 and task 1 to robot 1. The total cost is $1 + 3 = 4$ s after 1 round, with 6 announcements, 3 bids and 2 awards.

**One task per round.** Round 1 announces task 0: the bids are 1, 10 and 1.5, and robot 0 wins. Round 2 announces task 1 to the idle robots 1 and 2: the bids are 3 and 2.5, and robot 2 wins. The total cost is $1 + 2.5 = 3.5$ s after 2 rounds, with 6 announcements, 5 bids and 2 awards.

The minimum cost assignment, found by brute force over all assignments, costs 3.5 s. In this case the slower protocol is better, because robot 2 was free when task 1 came up and robot 1 was not forced on it.

**No bound on the cost.** With two robots, two tasks and costs $c_{00} = 1$, $c_{01} = 2$, $c_{10} = 2$, $c_{11} = M$, both robots bid on task 0 in round 1 and robot 0 wins, so robot 1 must take task 1. The protocol pays $1 + M$, but the other assignment pays $2 + 2 = 4$. For $M = 100$ the ratio is $101 / 4 = 25.25$, and it grows with $M$.

## Correctness

The [proof](proofs/correctness/) shows four facts, all theorems for the synchronous model above. The awards are always a valid assignment: no robot has two tasks and no task has two robots. The protocol stops within $t$ rounds, because each round removes at least one task from the open list. At the end no idle robot can do a task without an award, so the assignment is a maximal matching in the graph of eligible pairs, and it covers at least half as many tasks as a maximum matching. With the full window, the cheapest eligible pair is always awarded in round 1. The cost of the assignment has no constant factor bound, by the example above.

## Complexity

- **Rounds (theorem).** At most $t$; exactly $t$ with a window of one task.
- **Messages (theorem).** A round with window $W$ sends $r |W|$ announcements, at most $r$ bids and at most $\min(r, |W|)$ awards. With a window of one task the total is $r t$ announcements, at most $r t$ bids and at most $\min(r, t)$ awards. With the full window the announcements are at most $r t (t + 1) / 2$.
- **Work (theorem).** In a round each idle robot scans the window, $O(r |W|)$ operations in the [real RAM](/real-ram/) model, so $O(r t^2)$ in total with the full window and $O(r t)$ with one task per round.
- **Memory.** A robot keeps its own costs and its state; a manager keeps the bids of one round, at most $r$ numbers.

## Properties

- **Decentralized decisions.** Each manager decides only its own task, and each robot prices only its own work. No agent needs the whole cost matrix.
- **Greedy and final.** Awards are never taken back, so a bad early award stays. This is why the cost ratio is unbounded.
- **Maximal.** Every task that some idle robot could do gets an award (theorem).
- **Order dependent.** With one task per round, the result depends on the announcement order, as in the example.
- **Online.** A task that appears later is announced in a later round, and the protocol needs no change.
- **Deterministic** with the fixed tie rules above.

## Variants and improvements

- **Sequential single-item auctions.** The window of one task, used by many robot systems, for example MURDOCH of Gerkey and Matarić; see [market-based task allocation](/market-based-task-allocation/).
- **Re-auction and trading.** A robot may sell a task it holds when a cheaper robot appears; TraderBots and other market systems in the survey of Dias et al. (2006) do this, which removes some bad early awards (heuristic).
- **Bundles.** Robots bid on sets of tasks, as in the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) or in combinatorial auctions, when the cost of a task depends on the other tasks of the robot.
- **Optimal assignment.** When the costs are known and one robot or one server can collect them, the [Hungarian algorithm](/hungarian-algorithm/) gives the minimum cost in $O(n^3)$ time with $n = \max(r, t)$, and the [auction algorithm](/auction-algorithm/) reaches it within $\varepsilon$ by distributed bidding.
- **Lost messages and time-outs.** Smith's protocol has expiration times on announcements and bids, so a manager that hears nothing can announce again.

## When to use it

Use the contract net when tasks arrive over time, robots know their own costs best, and a quick valid assignment matters more than the optimal one. It suits teams with a reliable broadcast channel and a few tens of robots. Do not use it when the total cost must be near optimal, or when the value of a task depends on the other tasks of the robot; then use an optimal assignment or a bundle method.

## Pitfalls

- **Double awards.** If a robot may bid on several tasks in one round, two managers can award it at the same time. Bid on one task per round, as in line L4, or let robots refuse an award.
- **Closing tasks too early.** A task with no bid in one round may get a bid later from a robot that lost elsewhere. Close the window only when no robot bid on anything.
- **Expecting a cost bound.** Maximality bounds the number of tasks, not the cost (theorem); the ratio to the optimum can be arbitrarily large.
- **Order effects.** With one task per round, the order of announcements changes the result. Announce the most constrained tasks first if you know them (heuristic).
- **Stale costs.** A bid is a promise based on the robot's state at bid time. If the robot moves before the award, the cost is no longer true.

## Implementations

## History

Reid Smith proposed the contract net in his work on distributed problem solving, and published the protocol with its message formats in 1980. Randall Davis and Smith described it in 1983 as negotiation between managers and contractors. In robotics, auction protocols built on the contract net appeared around 2000, and Gerkey and Matarić (2004) analyzed them in their taxonomy of task allocation. Dias, Zlot, Kalra and Stentz (2006) surveyed the market-based methods that grew from it.

## References
