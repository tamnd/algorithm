---
tag: CYP3RG
kind: problem
slug: temporal-planning
name: Temporal planning
aliases:
- planning with durations
area: games-and-search/planning
level: advanced
summary: Planning with durative actions, concurrency and explicit time constraints.
prereqs: [classical-planning, pddl, simple-temporal-problem]
see_also: [graphplan, satplan, partial-order-plan, forward-state-space-search, bellman-ford, job-shop-scheduling, makespan, international-planning-competition]
sources:
  - paper: doi:10.1613/jair.1129
    title: "Maria Fox and Derek Long, PDDL2.1: an extension to PDDL for expressing temporal planning domains, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 61 to 124 (durative actions with conditions at start, over all and at end; plans, happenings and the separation of interfering happenings; general locator)
  - paper: "William Cushing, Subbarao Kambhampati, Mausam and Daniel S. Weld, When is temporal planning really temporal?, Proceedings of IJCAI 2007"
    locator: pp. 1852 to 1859 (required concurrency, and the incompleteness of decision epoch planners; general locator)
  - paper: "Jussi Rintanen, Complexity of concurrent temporal planning, Proceedings of ICAPS 2007, AAAI Press"
    locator: pp. 280 to 287 (plan existence is EXPSPACE-complete, and PSPACE-complete for a fragment that reduces to classical planning; general locator)
  - paper: doi:10.1016/0004-3702(91)90006-6
    title: "Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3) (1991)"
    locator: pp. 61 to 95 (simple temporal problems solved by shortest paths in the distance graph; general locator)
  - paper: "David E. Smith and Daniel S. Weld, Temporal planning with mutual exclusion reasoning, Proceedings of IJCAI 1999"
    locator: from p. 326 (TGP, a planning graph for actions with durations; the sources differ on the last page)
  - paper: doi:10.1613/jair.1156
    title: "Minh B. Do and Subbarao Kambhampati, SAPA: a multi-objective metric temporal planner, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 155 to 194 (forward search over time stamped states with decision epochs; general locator)
  - paper: doi:10.1609/icaps.v20i1.13403
    title: "Amanda Coles, Andrew Coles, Maria Fox and Derek Long, Forward-chaining partial-order planning, Proceedings of ICAPS 2010"
    locator: pp. 42 to 49 (POPF, forward search over start and end snap actions with a temporal constraint network per state; general locator)
---

Temporal planning is the problem of finding a plan whose actions take time. Each action has a duration, conditions that must hold when it starts, while it runs and when it ends, and effects at its start and at its end. Actions may run at the same time, and some tasks can only be solved when they do. A plan gives each action a start time, and the usual measure of quality is the makespan, the time at which the last action ends. The standard language is the durative action level of [PDDL](/pddl/) 2.1 (Fox and Long 2003). Temporal planning contains [classical planning](/classical-planning/) as the case of unit durations with no overlap, so it is at least PSPACE-hard. In general, plan existence is EXPSPACE-complete (Rintanen 2007).

## In plain words

In ordinary planning each action is a single jump from one state to the next. Here each action lasts a while. Some things must be true when it starts, some must stay true the whole time, and some must be true when it ends. It can change the world when it starts and again when it ends.

A plan is a timetable: what starts when. Actions that do not get in each other's way can run side by side, so a good plan finishes early. Some jobs even need two actions at once: you can only fix a fuse in the dark while a match is still burning. The planner must choose the actions, their order and their times all together.

## Definition

### Durative actions

A task has facts $F$, an initial state $I \subseteq F$, a goal $G \subseteq F$ and durative actions. A durative action $a$ has a duration $d(a) > 0$ and five sets of facts:

- the start condition $\mathrm{pre}_\vdash(a)$, which must hold when $a$ starts;
- the invariant $\mathrm{pre}_\leftrightarrow(a)$, which must hold while $a$ runs;
- the end condition $\mathrm{pre}_\dashv(a)$, which must hold when $a$ ends;
- the start effects, an add list and a delete list applied at the start;
- the end effects, an add list and a delete list applied at the end.

This is the durative action of PDDL 2.1 with a fixed duration (Fox and Long 2003). Each durative action splits into two *snap actions*: $a_\vdash$ at its start and $a_\dashv$ at its end. The snap actions are instantaneous STRIPS actions, and the end snap action needs the invariant and the end condition.

### Plans and validity

A plan is a finite set of pairs $(t, a)$: the action $a$ starts at time $t \ge 0$ and ends at $t + d(a)$. A *happening* is a time at which some snap action of the plan occurs. The plan is valid when the following holds as the happenings are processed in order of time, from the state $I$:

1. At each happening, the conditions of every snap action that occurs there hold in the state before it. Then all deletes are applied, and then all adds.
2. Two snap actions at the same happening do not interfere: neither deletes a condition or an add effect of the other.
3. For each pair $(t, a)$, the invariant of $a$ holds in the state after each happening at a time in $[t, t + d(a))$.
4. The goal holds in the state after the last happening.

PDDL 2.1 also asks that interfering happenings be at least a small constant $\epsilon > 0$ apart, so that no plan depends on the exact order of events at one instant. With integer times, $\epsilon = 1$ works. The *makespan* of a plan is $\max_{(t, a)} (t + d(a))$.

### The problem

- Plan existence: is there a valid plan?
- Plan generation: give a valid plan, or report that none exists.
- Optimal planning: give a valid plan with the least makespan, or the least value of a given cost that mixes makespan and action costs.

A task is *temporally simple* if every solvable instance has a valid plan with no two actions that overlap in time. Otherwise it has *required concurrency* (Cushing, Kambhampati, Mausam and Weld 2007).

## Variants

- **Conservative actions.** All conditions hold over the whole action, and all effects happen at the end. TGP (Smith and Weld 1999) uses this model. Actions that interfere may not overlap, so overlapping actions cannot interact, and every solvable task has a plan without overlap.
- **Duration constraints.** The duration is a variable with bounds, or depends on numeric fluents, as in PDDL 2.1.
- **Timed initial literals.** Facts become true or false at fixed times, given in the task: time windows, such as the hours a shop is open.
- **Continuous change.** Numeric quantities change at a fixed rate while an action runs, as in the fuel level of a vehicle. PDDL+ adds processes and events that the planner does not control.
- **Scheduling.** If the actions are fixed and only the times must be found, the problem is scheduling, such as [job shop scheduling](/job-shop-scheduling/) with the [makespan](/makespan/) objective.
- **Temporal uncertainty.** Some durations are known only as intervals and are chosen by nature. The plan must then work for every outcome, which leads to temporal networks with uncertainty.

## Examples

### A match and a fuse

The action $\mathit{light}$ has duration 8. It needs $\mathit{match}$ at its start, deletes $\mathit{match}$ and adds $\mathit{lit}$ at its start, and deletes $\mathit{lit}$ at its end. The action $\mathit{mend}$ has duration 5. It needs $\mathit{lit}$ at its start and as an invariant, and it adds $\mathit{mended}$ at its end. The initial state is $\{\mathit{match}\}$ and the goal is $\{\mathit{mended}\}$.

The only light comes from the burning match, so $\mathit{mend}$ must run inside $\mathit{light}$. Its start must come at least $\epsilon$ after the start of $\mathit{light}$, which adds $\mathit{lit}$, and its end at least $\epsilon$ before the end of $\mathit{light}$, which deletes it. With $\epsilon = 1$ and integer times, the least makespan is 8, with $\mathit{light}$ at time 0 and $\mathit{mend}$ at time 1 or 2. No valid plan has the two actions without overlap. So the task has required concurrency, and a planner that only orders whole actions one after the other cannot solve it.

### A cycle that proves no plan

Keep the order of the four snap actions of the previous example: start of $\mathit{light}$, start of $\mathit{mend}$, end of $\mathit{mend}$, end of $\mathit{light}$. Their times $x_1, x_2, x_3, x_4$ must satisfy

$$x_4 - x_1 = 8, \qquad x_3 - x_2 = D, \qquad x_2 - x_1 \ge \epsilon, \qquad x_4 - x_3 \ge \epsilon,$$

where $D$ is the duration of $\mathit{mend}$. This is a [simple temporal problem](/simple-temporal-problem/). In its distance graph, the cycle $x_1 \to x_4 \to x_3 \to x_2 \to x_1$ has weight $8 - \epsilon - D - \epsilon$. The constraints are consistent exactly when no cycle is negative, so the fuse can be mended exactly when $D \le 8 - 2\epsilon$. With $\epsilon = 1$, [Bellman-Ford](/bellman-ford/) finds a negative cycle for $D = 7$ and $D = 8$ and none for $D \le 6$. Since this is the only order in which $\mathit{mend}$ can get its light, a fuse that takes 7 units cannot be mended at all.

### Fewer actions or a shorter makespan

From $\mathit{home}$, the action $\mathit{fly}$ of duration 10 reaches $\mathit{there}$. The action $\mathit{bus}$ of duration 3 reaches $\mathit{hub}$, and the action $\mathit{train}$ of duration 3 goes from $\mathit{hub}$ to $\mathit{there}$. The plan with fewest actions is $\mathit{fly}$, with makespan 10. The plan with least makespan is $\mathit{bus}$, then $\mathit{train}$ from time $3 + \epsilon$, with makespan $6 + \epsilon$. A classical planner that counts actions returns the first one.

### Work in parallel

Two trucks deliver two parcels, each in 4 time units, with no shared resource. Run side by side, the deliveries give makespan 4. A plan with one action after the other has makespan 8. The task is temporally simple, but concurrency still halves the makespan.

## Known algorithms

- **Plan, then schedule.** Solve the task as a classical task with the durations ignored, then lift a partial order from the plan and give the actions the earliest times. This is fast, and complete only for temporally simple tasks.
- **Decision epochs.** SAPA (Do and Kambhampati 2003) searches forward over states with a clock and a queue of pending end effects. A step either starts an action now or moves the clock to the next pending end. Cushing et al. (2007) show that such planners can miss plans of tasks with required concurrency, when an action must start at a time that is not a pending end.
- **Snap actions and temporal networks.** CRIKEY and its successor POPF (Coles, Coles, Fox and Long 2010) search forward over the start and end snap actions, as in a [forward state-space search](/forward-state-space-search/). Each state keeps the order constraints and the durations of the snap actions so far as a [simple temporal problem](/simple-temporal-problem/). A state is kept only if its constraints are consistent, which [Bellman-Ford](/bellman-ford/) checks by the absence of a negative cycle. The times are fixed only at the end, so the plan stays partially ordered.
- **Temporal planning graphs.** TGP (Smith and Weld 1999) extends the planning graph of [GRAPHPLAN](/graphplan/) to actions of different durations, with mutexes between actions, facts and their times.
- **Local search.** LPG plans by local search over action graphs, with times attached to the actions.
- **SAT and SMT.** Encodings in the style of [SATPLAN](/satplan/) use a variable for each snap action at each step, and either a fixed grid of times or real-valued time variables handled by an SMT solver for difference constraints.
- **Partial-order planners with time.** [Partial-order plans](/partial-order-plan/) with temporal constraints between their steps, as in constraint-based planners that keep timelines for the parts of a system.

## Bounds

Classical planning is the special case of unit durations, conditions at the start and as an invariant, and effects at the end, so temporal planning is PSPACE-hard. Rintanen (2007) proved that plan existence with integer time is EXPSPACE-complete, and that it is PSPACE-complete for a large fragment of temporal PDDL, by a reduction of that fragment to classical planning. Cushing et al. (2007) describe the condition of the fragment as: no action may overlap a running instance of itself. When an action can overlap itself, the number of its running instances has no bound, and the state must record each of them with its time left.

For a fixed set of snap actions in a fixed order, the times form a simple temporal problem. Its consistency, and the least makespan, come from shortest paths in a graph with one node per snap action, so they take $O(v e)$ time by Bellman-Ford for $v$ snap actions and $e$ constraints (Dechter, Meiri and Pearl 1991). The hard part is the choice of the actions and the order.

## Reductions

- **From classical planning.** Give each action duration 1, its preconditions at its start and as its invariant, and its effects at its end. A classical plan run with one action after the other is a temporal plan. Conversely, list the actions of a temporal plan in the order of their ends: the invariant keeps each precondition true up to the end, so the list is a classical plan. This gives the PSPACE lower bound.
- **To classical planning.** For temporally simple tasks, a classical task with the durations removed finds the actions, and a schedule adds the times. Rintanen (2007) reduces a large fragment of temporal PDDL, with integer time, to classical planning.
- **To simple temporal problems.** Once the snap actions and their order are chosen, finding the times is a simple temporal problem, solved by [Bellman-Ford](/bellman-ford/) or [Floyd-Warshall](/floyd-warshall/).
- **To scheduling.** With the actions fixed and only resource conflicts left, the problem is a scheduling problem such as [job shop scheduling](/job-shop-scheduling/).

## Applications

- **Spacecraft.** The Remote Agent experiment on NASA's Deep Space 1 in 1999 ran a temporal planner and scheduler on board, and the daily activity plans of the Mars Exploration Rovers were built with the help of a constraint-based temporal planner.
- **Benchmarks.** PDDL 2.1 was written for the [planning competition](/international-planning-competition/) of 2002, and temporal tracks have been part of many competitions since then, with domains such as satellites, rovers and depots.
- **Logistics and manufacturing.** Vehicles, machines and crews work in parallel, and the makespan is the time to finish the whole job.
- **Robotics and multi-agent systems.** Several robots act at once, and actions such as holding a door open while another robot passes need required concurrency.

## References
