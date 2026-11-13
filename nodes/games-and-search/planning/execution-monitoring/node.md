---
tag: SF0N1W
kind: concept
slug: execution-monitoring
name: Execution monitoring
aliases:
- plan monitoring
area: games-and-search/planning
level: advanced
summary: Checking, while a plan runs, whether the observed state still lets the rest of the plan reach the goal, and choosing to go on, skip, repeat a step or replan.
prereqs: [strips, goal-regression]
see_also: [replanning, sussman-anomaly, classical-planning, belief-space, contingent-planning, plan-recognition, particle-filter, linear-temporal-logic]
sources:
  - paper: doi:10.1016/0004-3702(72)90051-3
    title: Richard E. Fikes, Peter E. Hart and Nils J. Nilsson, Learning and executing generalized robot plans, Artificial Intelligence 3, 1972
    locator: pp. 251 to 288 (triangle tables, kernels, and the PLANEX execution monitor of the robot Shakey)
  - paper: doi:10.1016/j.robot.2005.09.004
    title: Ola Pettersson, Execution monitoring in robotics, a survey, Robotics and Autonomous Systems 53(2), 2005
    locator: pp. 73 to 88 (model-based and model-free monitoring, fault detection and recovery)
  - book: isbn:9781107037274
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning and Acting, Cambridge University Press, 2016
    locator: whole book (acting with deliberation, monitoring of plans and of actions, general locator)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (planning and acting in nondeterministic domains, execution monitoring and replanning)
---

Execution monitoring is the part of an agent that compares what happens with what the plan expects while the plan runs. A planner builds its plan from a model, and the real world does not always follow the model: an action fails, an object moves, or a lucky event does part of the work. The monitor observes the state after each step and decides whether the agent can go on, skip ahead, repeat a step, or must call the planner again, which is [replanning](/replanning/). The classic form, from the robot Shakey, keeps for each step of a [STRIPS](/strips/) plan the condition that the rest of the plan needs, the **kernel**. The kernels are the [regressions](/goal-regression/) of the goal through the suffixes of the plan, and they make it possible to check only what matters for the goal.

## In plain words

You follow a recipe. Before each step you look at the table. If a step went wrong, you do it again. If someone already did a step for you, you skip it. If something you need later is gone, you stop now, and do not wait until you reach the step that needs it.

A good monitor does not only check that the next step can start. It checks whether the rest of the plan can still work from what it sees. For each point in the plan, it keeps a short list of the facts that the remaining steps need. After each step it finds the latest point whose list is all true, and it goes on from there. If no list is true, it asks the planner for a new plan.

## The idea

Let the plan be $a_0, a_1, \ldots, a_{n-1}$ for a goal $G$, with STRIPS actions $a = (\mathrm{pre}, \mathrm{add}, \mathrm{del})$ and the next state $(s \setminus \mathrm{del}) \cup \mathrm{add}$. The **kernels** are

$$K_n = G, \qquad K_k = \mathrm{pre}(a_k) \cup \big(K_{k+1} \setminus \mathrm{add}(a_k)\big),$$

and $K_k$ is not satisfiable if $K_{k+1} \setminus \mathrm{add}(a_k)$ meets $\mathrm{del}(a_k)$. By induction on $n - k$, the kernel $K_k$ holds in a state $s$ if and only if the steps $a_k, \ldots, a_{n-1}$ can all run from $s$ and end in a state that satisfies $G$. So the kernel is the exact test for "the rest of the plan from step $k$ works".

**The monitor.** After each step, observe the state $s$ and find the largest $k$ with $K_k \subseteq s$.

- If $k = n$, the goal holds, and the agent stops.
- If $k$ is the next step, the run is on track.
- If $k$ is later than the next step, an outside event did part of the work, and the agent skips ahead.
- If $k$ is earlier, a step failed or was undone, and the agent repeats steps from $k$.
- If no kernel holds, no suffix of the plan works, and the agent must replan.

Taking the largest $k$ uses the shortest suffix that still works. This was the rule of PLANEX, the executor of Shakey (Fikes, Hart and Nilsson 1972).

**Triangle tables.** Fikes, Hart and Nilsson stored the kernels in a **triangle table**. Row $i$ holds the needs of step $i$, and row $n$ holds the goal. Column $0$ holds the facts of the initial state, and column $j$ the facts that step $j - 1$ adds. The entry in row $i$ and column $j$ marks the facts that row $i$ needs, that column $j$ supplies, and that no step between them adds again. The kernel $K_k$ is the union of the entries in rows $k$ to $n$ and columns $0$ to $k$, the rectangle at the lower left of step $k$. For a plan that works from its initial state, this union is the regression $K_k$ above.

**What a monitor checks.** A monitor that checks only the precondition of the next step is cheaper, but it can run on for many steps after the goal has become impossible, and the extra steps can make the state worse. A monitor that checks the whole predicted state stops for every change, also for changes that do not matter. The kernel checks the facts that matter and no others. With $f$ facts in the largest kernel, one check costs $O(n f)$ set tests, or less with an index that records which kernels each fact belongs to.

**Beyond STRIPS.** With uncertain or partial observations, the monitor tracks a [belief](/belief-space/), a set or distribution of states, for example with a [particle filter](/particle-filter/), and tests whether the kernel holds in all of it or with high probability. With durations and resources, it also checks time bounds, such as the deadline of the next step. For conditions on the whole run, such as "never enter the red zone", the monitor checks a formula of [linear temporal logic](/linear-temporal-logic/) on the prefix that it has seen.

## Examples

**The Sussman anomaly.** Three blocks: C is on A, and A and B are on the table. The goal is A on B and B on C. The plan is unstack C A, putdown C, pickup B, stack B C, pickup A, stack A B, the [Sussman anomaly](/sussman-anomaly/) plan of six steps. Its kernel before step 4 (pickup A) is {B on C, B clear, A on the table, A clear, hand empty}, and before step 0 it is the whole initial state.

| What happens | Kernel monitor | Steps run |
|---|---|---|
| Nothing unexpected | runs the plan | 0, 1, 2, 3, 4, 5 |
| After step 0, someone takes C and puts it on the table | skips putdown C | 0, 2, 3, 4, 5 |
| Step 3 fails, and B falls on the table | repeats pickup B | 0, 1, 2, 3, 2, 3, 4, 5 |
| After step 1, someone puts C back on A | starts again from step 0 | 0, 1, 0, 1, 2, 3, 4, 5 |
| After step 0, block A is taken away | replans at once | 0 |

In the fourth row, a monitor that checks only the next precondition runs pickup B and stack B C, which bury A under two blocks, and fails at pickup A after four steps. In the last row it also runs four steps before it sees that A is missing. The implementation reproduces the table, and it checks on random STRIPS problems that a kernel holds exactly when the rest of the plan works, and that the triangle table gives the same kernels as regression.

**A delivery robot.** A robot plans to go through a door. The kernel of the step "go through" contains "door open". If a person closes the door while the robot is still in the hall, the monitor sees it before the robot reaches the door, and the robot replans or waits.

**A process plan.** A chemical plant follows a recipe. The monitor checks temperatures and levels against the conditions that the remaining steps need, and it calls a recovery plan when a value is outside its range.

## Where it is used

- Robot control, from Shakey's PLANEX to modern task executives that check the preconditions of each skill and the conditions that later skills need. Pettersson (2005) surveys monitoring in robotics.
- The online loop of [replanning](/replanning/): monitor, and replan only when no part of the plan still works.
- Plan repair, where the kernels show which part of the plan failed and which part can be kept.
- Mixed planning and acting systems such as SIPE, which keep the reasons for each step so that a failure can be traced to the steps that it affects.
- Systems that act under [contingent plans](/contingent-planning/), where the monitor picks the branch that matches the observation.
- The observer side of [plan recognition](/plan-recognition/), which compares the actions it sees with the plans it expects.
- Runtime verification of software, where a monitor checks a temporal property on the run so far.

## References
