---
tag: FENCPV
kind: algorithm
slug: consensus-based-bundle-algorithm
name: Consensus-based bundle algorithm
aliases:
- CBBA
area: robotics/multi-robot-systems
level: research
summary: A decentralized auction in which each robot builds a bundle of tasks greedily and neighbors agree on the winners by message passing, giving a conflict-free assignment.
solves: [multi-robot-task-allocation]
model: real-ram
complexity:
  vars: {r: the number of robots, t: the number of tasks, L: the largest bundle, D: the diameter of the communication graph, m: the number of edges}
  time: {per_round: O(r L t + m (t + r)), rounds: "O(min(t, L r) D)"}
  messages: {per_round: O(m), size: O(t + r)}
  space: {extra: O(r (t + r))}
properties: {deterministic: true, randomized: false, online: false}
history:
  year: 2009
  people: [Han-Lim Choi, Luc Brunet, Jonathan P. How]
  note: Choi, Brunet and How joined a greedy bundle auction with a consensus rule on winning bids, and proved agreement and a 50 percent bound under diminishing marginal gain.
prereqs: [multi-robot-task-allocation, market-based-task-allocation, submodular-function]
see_also: [contract-net-protocol, auction-algorithm, laplacian-consensus-protocol, consensus-problem, greedy-algorithm, matroid, synchronous-model, flooding]
sources:
  - paper: doi:10.1109/TRO.2009.2022423
    title: Han-Lim Choi, Luc Brunet and Jonathan P. How, Consensus-based decentralized auctions for robust task allocation, IEEE Transactions on Robotics 25(4), 2009
    locator: pages 912 to 926 (CBAA and CBBA, the decision table of the consensus phase, diminishing marginal gain, convergence and the 50 percent bound)
  - paper: doi:10.2514/6.2008-6839
    title: Luc Brunet, Han-Lim Choi and Jonathan P. How, Consensus-based auction approaches for decentralized task assignment, AIAA Guidance, Navigation and Control Conference, 2008
    locator: the paper as a whole (the first version of the consensus-based auctions)
  - paper: doi:10.1177/0278364913496484
    title: G. Ayorkor Korsah, Anthony Stentz and M. Bernardine Dias, A comprehensive taxonomy for multi-robot task allocation, International Journal of Robotics Research 32(12), 2013
    locator: pages 1495 to 1512 (the classes of task allocation with dependent costs)
---

The consensus-based bundle algorithm (CBBA) assigns tasks to a robot team without a central auctioneer. Each robot greedily builds a *bundle* of tasks it bids on, then it exchanges its list of winning bids with its neighbors and drops the tasks it has lost, and the rounds repeat until all robots agree. Unlike the [contract net protocol](/contract-net-protocol/), where a manager collects bids for one task, every robot here acts as bidder and auctioneer at once, and robots may hold several tasks. Under diminishing marginal gain it reaches a conflict-free assignment in at most $\min(t, L r) D$ rounds, and the assignment is at least half of the optimum.

## In plain words

Each robot looks at the list of jobs and writes down the best ones it can still win, one after the other, until its list is full or no job is worth more to it than to the robot that holds it now. Then it tells its neighbors: "this is who I think wins each job, and for how much." When a robot hears that someone else bids more on a job in its list, it gives the job up, and it also gives up every job it added after that one, because those bids counted on the lost job.

The robots repeat this. The news of the best bids travels one neighbor per round, so after enough rounds every robot has the same table and no job has two owners. Nobody ever needs to see the whole team at once.

## The problem

**The model.** There are $r$ robots and $t$ tasks. Robot $i$ can hold at most $L$ tasks. A task $j$ added to a bundle that already holds $n$ tasks is worth $a_{ij} \gamma^n$ to robot $i$, with scores $a_{ij} > 0$ and a discount $0 < \gamma \le 1$. This score has *diminishing marginal gain* (DMG): a task is never worth more to a robot after the robot has added other tasks. Each task goes to at most one robot. The communication graph is fixed, undirected and connected, with $m$ edges and diameter $D$. Time is synchronous: in each round every robot runs its bundle phase, then sends one message to each neighbor, then runs the consensus phase on what it received.

**Input.** The scores $a_{ij}$, the discount $\gamma$, the bundle limit $L$, and the neighbor lists.

**Output.** For each robot its bundle; for each robot and task the winner it believes and the winning bid. At the end all robots hold the same winners.

**How it differs from close pages.** [Multi-robot task allocation](/multi-robot-task-allocation/) is the problem, and [market-based task allocation](/market-based-task-allocation/) is the family of auction methods; CBBA is the member that needs no auctioneer and no complete graph. The [contract net protocol](/contract-net-protocol/) gives one task per robot through managers that hear every bid. The [auction algorithm](/auction-algorithm/) of Bertsekas raises prices until an optimal assignment within $\varepsilon$ is reached, but it assumes one task per robot and a shared price list. CBBA trades optimality for local messages and gets a 50 percent bound instead. The consensus phase is a max-consensus on the bids, close to [flooding](/flooding/), and not the averaging of the [Laplacian consensus protocol](/laplacian-consensus-protocol/).

## The algorithm

Each robot $i$ keeps its bundle $b_i$, a winning bid $y_{ij}$ and a winner $z_{ij}$ for each task, and a timestamp $s_{ik}$ for each robot $k$: the last round in which it had news from $k$. A bid $(y, z)$ *beats* $(y', z')$ when $y > y'$, or $y = y'$ and $z$ has the smaller index.

```pseudo id=main
CBBA(a, gamma, L, neighbors)
L1  b_i ← empty;  y_ij ← 0;  z_ij ← none;  s_ik ← 0  for all i, j, k
L2  for round = 1, 2, ... do
L3      for each robot i do                                   ▷ bundle phase
L4          while |b_i| < L do
L5              c_ij ← a_ij · gamma^|b_i|  for each task j not in b_i
L6              J ← the tasks j where (c_ij, i) beats (y_ij, z_ij)
L7              if J is empty then break
L8              j ← the task in J with the largest c_ij;  append j to b_i;  y_ij ← c_ij;  z_ij ← i
L9      each robot i sends (y_i, z_i, s_i) to every neighbor
L10     for each robot i and each neighbor k do              ▷ consensus phase
L11         for each task j: update, reset or leave (y_ij, z_ij) by the decision table, using y_kj, z_kj and the timestamps
L12     each robot i sets s_ik ← round for its neighbors and takes the newer timestamps of the others
L13     each robot i finds the first task in b_i it no longer wins, removes it and every later task, and withdraws its own bids on the later tasks
L14     stop when nothing has changed for r rounds
L15 return b, y, z
```

Lines L4 to L8 are the greedy bundle phase: the robot adds the task with the best marginal score as long as that score beats the winner it knows. Line L11 is the decision table of Choi, Brunet and How (2009). It has one row for each case of "who the sender thinks wins" and "who the receiver thinks wins": the robot itself, the other robot, a third robot, or none. A receiver takes the sender's bid when the sender wins with a better bid, and it takes the sender's view of a third robot when the sender's timestamp for that robot is newer. Line L13 is the release rule: bids added after a lost task were computed with the lost task in the bundle, so they are no longer true.

The code changes one detail of line L13. The paper resets every later task of the bundle. The code removes these tasks from the bundle, but it keeps a record that another robot wins one of them, and it resets only the entries where the robot itself was the winner. With the paper's rule the code fell into a cycle on about one random instance in three thousand (measurement), because the reset erased the news about the true winner of a later task in every round.

## Example

Three robots on the path $0 - 1 - 2$, two tasks, $L = 1$ and $\gamma = 1$. The scores, in any unit of value, are:

| | task 0 | task 1 |
|---|---|---|
| robot 0 | 10 | 9 |
| robot 1 | 4 | 6 |
| robot 2 | 8 | 1 |

**Round 1.** In the bundle phase robot 0 claims task 0 with 10, robot 1 claims task 1 with 6, and robot 2 claims task 0 with 8. Robot 1 hears robots 0 and 2 and learns that robot 0 wins task 0 with 10. Robot 0 hears robot 1 and learns that robot 1 wins task 1 with 6. Robot 2 hears only robot 1, which did not know about task 0 at the end of the last round, so robot 2 keeps its claim.

**Round 2.** Robot 2 hears from robot 1 that robot 0 wins task 0 with 10, and it releases task 0. Robot 2 then bids 1 on task 1, which does not beat 6.

The result after 2 rounds is task 0 to robot 0 and task 1 to robot 1, with value $10 + 6 = 16$. This is also the sequential greedy assignment (SGA): take the largest score, 10, then the largest among the rest, 6. The optimum, found by brute force, gives task 1 to robot 0 and task 0 to robot 2, value $9 + 8 = 17$. So $16 \ge 17 / 2$ as Theorem 1 of the proof says, and the gap is real. The bound of Theorem 2 is $\min(t, L r) D = 2 \cdot 2 = 4$ rounds, and 2 were used.

## Correctness

The [proof](proofs/correctness/) has three parts. Theorem 1, a full proof: the score of each robot is monotone and submodular, the rule "one robot per task" is a partition matroid, and SGA is the greedy algorithm for this function, so by the argument of Fisher, Nemhauser and Wolsey (1978) its value is at least half of the optimum. Theorem 2 is the theorem of Choi, Brunet and How (2009): under DMG, on a fixed connected graph with synchronous rounds and the paper's decision table, all robots agree on a conflict-free assignment equal to SGA within $\min(t, L r) D$ rounds. It is stated with a proof sketch, and the changed release rule of the code is checked by measurement on 300 random instances. Theorem 3, a full proof: on a path with one task, $D$ rounds are needed.

## Complexity

- **Rounds (theorem).** At most $N_{min} D$ with $N_{min} = \min(t, L r)$, by Theorem 2, and at least $D$ in the worst case, by Theorem 3. On a path of $r$ robots with one task the tests measure exactly $r - 1 = D$ rounds.
- **Messages (theorem).** Every round sends one message along each edge in each direction, $2 m$ messages, each with $t$ bids, $t$ winners and $r$ timestamps.
- **Work per round.** The bundle phase of one robot scans $t$ tasks for each of at most $L$ additions, $O(L t)$, so $O(r L t)$ for the team. The consensus phase costs $O(t + r)$ per message, $O(m (t + r))$ in total, in the [real RAM](/real-ram/) model.
- **Memory.** Each robot stores $O(t + r)$ numbers, and the team $O(r (t + r))$.

## Properties

- **Conflict-free at convergence (theorem, under DMG).** No task has two winners.
- **Half of the optimum (theorem, under DMG).** The value is at least $1/2$ of the best assignment; the example shows $16$ against $17$.
- **Local messages.** Robots talk only to neighbors, and the graph need not be complete. A message has a fixed size.
- **Needs DMG.** The convergence theorem assumes it. If a task can be worth more after other tasks are added, for example because it lies on the way, a robot can outbid itself later and the robots may not agree (heuristic warning, no bound).
- **Deterministic** with the tie rule on robot indices.

## Variants and improvements

- **CBAA.** The consensus-based auction algorithm of the same paper is the case $L = 1$: one task per robot, and the same 50 percent bound.
- **Path scores.** In the paper the score of a task is its gain when it is inserted at the best place in the robot's path. Many path scores break DMG, and later work changed the score to restore it.
- **Asynchronous versions.** Later work from the same group replaced the synchronous rounds by message rules for asynchronous networks and changing graphs. The bound of Theorem 2 does not carry over directly.
- **Coupled constraints.** Extensions add time windows and tasks that need several robots.
- **Centralized greedy.** If one server can collect all scores, it can run SGA directly: at most $\min(t, L r)$ steps, each a scan of $r t$ pairs, so $O(\min(t, L r) \, r t)$ time, with the same assignment and no rounds.

## When to use it

Use CBBA when a team of a few to a few tens of robots must split many tasks, each robot may take several, the network is not complete, and no robot should be a single point of failure. It fits search, surveillance and delivery missions where a task is worth less as the robot gets busier. Do not use it when the scores have no diminishing gain, when an optimal assignment is needed, or when one reliable server can run an exact solver.

## Pitfalls

- **Scores without DMG.** Bundle scores that grow with the bundle make the consensus cycle. Check the score, or use a discount like $\gamma^n$.
- **Release rule details.** Resetting too much in line L13 can erase news about other winners and cause cycles; resetting too little leaves stale bids. Test the release rule on many random instances.
- **Stopping too early.** A round with no change does not mean the robots agree, because news may still be on its way. Wait at least $D$ quiet rounds; the code waits $r$.
- **Timestamps.** Without timestamps, old news about a third robot can overwrite new news, and the table cannot decide between them.
- **Changing graphs.** The bound of Theorem 2 assumes a fixed connected graph. If links drop, rounds can be lost and the bound no longer holds.

## Implementations

## History

Brunet, Choi and How presented consensus-based auctions at the AIAA Guidance, Navigation and Control Conference in 2008. Choi, Brunet and How published CBAA and CBBA in the IEEE Transactions on Robotics in 2009, with the decision table, the convergence theorem and the 50 percent bound under diminishing marginal gain. The bound comes from the classic result of Fisher, Nemhauser and Wolsey (1978) on greedy maximization of submodular functions over a matroid. Later work from the same group added asynchronous messages and coupled constraints.

## References
