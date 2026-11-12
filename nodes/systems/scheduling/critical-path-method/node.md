---
tag: EQ6EWJ
kind: algorithm
slug: critical-path-method
name: Critical path method
aliases:
- critical path scheduling
- critical path analysis of a project network
area: systems/scheduling
level: intro
summary: "Two passes over a project network in topological order give each activity's earliest and latest start, its float, and the critical path that fixes the least project time."
solves: [longest-path-problem]
model: word-ram
complexity:
  vars: {n: the number of activities, m: the number of precedence arcs}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1959
  people: [James E. Kelley Jr., Morgan R. Walker, Donald G. Malcolm, John H. Roseboom, Charles E. Clark, Willard Fazar]
  note: Kelley and Walker presented CPM in 1959 from work at du Pont and Remington Rand; PERT, built for the Polaris program, appeared the same year.
prereqs: [dag-longest-path, topological-sort]
see_also: [pert-chart, critical-path-lower-bound, critical-path, resource-constrained-project-scheduling, kahns-algorithm, directed-acyclic-graph, heft, list-scheduling]
sources:
  - paper: doi:10.1145/1460299.1460318
    title: James E. Kelley Jr. and Morgan R. Walker, Critical-path planning and scheduling, Papers presented at the Eastern Joint IRE-AIEE-ACM Computer Conference, December 1959
    locator: pages 160 to 173 (the project network, earliest and latest times, float, and the critical path)
  - paper: doi:10.1287/opre.7.5.646
    title: D. G. Malcolm, J. H. Roseboom, C. E. Clark and W. Fazar, Application of a technique for research and development program evaluation, Operations Research 7(5), 1959
    locator: pages 646 to 669 (PERT, with three time estimates per activity)
  - paper: doi:10.1287/opre.9.3.296
    title: James E. Kelley Jr., Critical-path planning and scheduling, mathematical basis, Operations Research 9(3), 1961
    locator: pages 296 to 320 (the linear programming view and the time-cost trade-off)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition
    locator: Section 24.2, Single-source shortest paths in directed acyclic graphs (the PERT chart and critical paths)
---

The critical path method (CPM) computes, for a project made of activities with fixed durations and precedence constraints, the least time in which the whole project can be done, and for each activity the earliest and latest times at which it can start without making the project longer. It does this with two passes over the precedence graph in topological order: a forward pass for the earliest times and a backward pass for the latest times. The activities with no slack form the critical path, a [longest path](/dag-longest-path/) of the graph; any delay on it delays the whole project. This page is the scheduling algorithm with the floats a planner reads off, and the systems uses such as build graphs and pipelines; the graph-technique page [PERT chart](/pert-chart/) presents the same passes as a longest-path template, and the [critical path lower bound](/critical-path-lower-bound/) uses the result as a bound for schedules on a fixed number of machines.

## In plain words

A project has many tasks. Some tasks must wait for others to finish. Each task takes a known time, and there are enough people to do any number of tasks at once. Go through the tasks so that each task comes after all the tasks it waits for. For each task, the earliest it can start is when the last task it waits for is done. The project ends when the last task ends. Then go back from the end. For each task, the latest it may finish is just before the first task that waits for it must start. The difference between latest and earliest is the slack of the task. Tasks without slack form the critical path. Speed up the project only by speeding up those tasks.

## The problem

There are $n$ activities with durations $p_j \ge 0$, and $m$ arcs $(i, j)$ that mean "activity $j$ starts only after activity $i$ finishes" (activity on node). The precedence graph must be a [directed acyclic graph](/directed-acyclic-graph/). There is no limit on resources, so any number of activities may run at once. A schedule gives each activity a start time $S_j \ge 0$ with $S_j \ge S_i + p_i$ for each arc. The task is to find the least project duration $T = \min \max_j (S_j + p_j)$ and, for each activity, its earliest start $ES_j$, its latest start $LS_j$ in a schedule of duration $T$, its total float $LS_j - ES_j$ and its free float.

## The algorithm

```pseudo id=main
CPM(p[1 .. n], arcs)
L1  σ ← a topological order of the activities   ▷ Kahn's algorithm; fail on a cycle
L2  for each j in σ do ES[j] ← max over arcs (i, j) of ES[i] + p[i]   (0 if none)
L3  T ← max over j of ES[j] + p[j]
L4  for each i in σ reversed do LF[i] ← min over arcs (i, j) of LF[j] − p[j]   (T if none)
L5  for each j do TF[j] ← LF[j] − p[j] − ES[j]               ▷ total float
L6  for each j do FF[j] ← min over arcs (j, k) of ES[k] (T if none) − ES[j] − p[j]   ▷ free float
L7  start at an activity with TF = 0 and ES = 0, and follow arcs (j, k) with TF[k] = 0 and ES[k] = ES[j] + p[j]
L8  return T, ES, LF, TF, FF and the path of line L7
```

The latest start is $LS_j = LF_j - p_j$. Line L2 is the forward pass and line L4 the backward pass; each looks at every arc once. The total float of line L5 is the delay that activity $j$ can take without delaying the project, if the other activities may move. The free float of line L6 is the delay it can take without moving the earliest start of any other activity. Line L7 extracts one critical path; there may be several.

## Example

A release pipeline with eight activities. Times are in minutes.

| activity | name | $p_j$ | waits for |
|---|---|---|---|
| A | fetch sources | 2 | |
| B | build library | 4 | A |
| C | generate code | 3 | A |
| D | build service | 5 | B, C |
| E | build docs | 2 | C |
| F | integration tests | 6 | D |
| G | package docs | 1 | E |
| H | publish release | 3 | F, G |

The forward pass of line L2, in the topological order A, B, C, D, E, F, G, H, gives $ES_D = \max(2 + 4, 2 + 3) = 6$ and $ES_H = \max(11 + 6, 7 + 1) = 17$, so line L3 gives $T = 20$. The backward pass of line L4 from $LF_H = 20$ gives $LF_G = LF_F = 17$, $LF_E = 17 - 1 = 16$, and $LF_C = \min(LF_D - 5, LF_E - 2) = \min(6, 14) = 6$.

| activity | $ES$ | $EF$ | $LS$ | $LF$ | total float | free float |
|---|---|---|---|---|---|---|
| A | 0 | 2 | 0 | 2 | 0 | 0 |
| B | 2 | 6 | 2 | 6 | 0 | 0 |
| C | 2 | 5 | 3 | 6 | 1 | 0 |
| D | 6 | 11 | 6 | 11 | 0 | 0 |
| E | 5 | 7 | 14 | 16 | 9 | 0 |
| F | 11 | 17 | 11 | 17 | 0 | 0 |
| G | 7 | 8 | 16 | 17 | 9 | 9 |
| H | 17 | 20 | 17 | 20 | 0 | 0 |

The critical path is A, B, D, F, H, with $2 + 4 + 5 + 6 + 3 = 20$. Activity C has one minute of total float: it can end at $6$ instead of $5$, and D still starts at $6$. Activity E has $9$ minutes of total float but no free float: if E starts late, G must start late too, though the release does not move. Activity G has $9$ minutes of free float: it alone can slip $9$ minutes and nothing else moves. Making the docs faster does not help the release; making the tests faster does, until another path becomes critical.

## Correctness

By induction along the topological order, $ES_j$ is the length of the longest chain of activities that must finish before $j$ starts: the base case is an activity with no predecessor, and line L2 takes the maximum over the last activity of such a chain. Every schedule has $S_j \ge ES_j$, by the same induction on the constraints $S_j \ge S_i + p_i$, and the schedule $S_j = ES_j$ satisfies every constraint because line L2 takes a maximum. So $T$ of line L3 is the least project duration, and it equals the length of a longest path. In the same way, backward, $LF_i = T - t_i$ where $t_i$ is the longest chain that must run after $i$ finishes; every schedule of duration $T$ has $S_i + p_i \le LF_i$, and the schedule $S_j = LS_j$ is feasible. So $TF_j = T - (ES_j + p_j + t_j)$ is $T$ minus the longest path through $j$, which is zero exactly on the longest paths. The full proof is below.

## Complexity

- **Time.** Line L1 is [Kahn's algorithm](/kahns-algorithm/), $\Theta(n + m)$. Lines L2, L4 and L6 look at each arc once, and lines L3 and L5 at each activity once. Line L7 walks one path and scans the out-arcs of its activities. All together $\Theta(n + m)$.
- **Space.** $\Theta(n + m)$ for the adjacency lists and the arrays.

## Properties

- **Exact** for the project duration with unlimited resources.
- **The project duration is a longest path.** $T$ is the length of a heaviest chain of activities. Adding any arc or lengthening any activity can only keep $T$ or raise it.
- **Floats.** $0 \le FF_j \le TF_j$ for each activity. Activities on a critical path have $TF_j = 0$.
- **Several critical paths.** There may be more than one, and an activity with zero float need not lie on the path that line L7 returns.
- **Integer data.** If all $p_j$ are integers, so are all times.

## Variants and improvements

- **PERT.** Malcolm, Roseboom, Clark and Fazar 1959 gave each activity three estimates, optimistic $o$, most likely $m$ and pessimistic $q$, with mean $(o + 4m + q)/6$, and used the passes on the means. The [PERT chart page](/pert-chart/) covers the variance and the normal approximation. The method underestimates the expected project time, because the longest of several random paths is on average longer than the longest of their means.
- **Activity on arc.** Kelley and Walker drew activities as arcs between events. The two forms are equivalent; activity on arc may need dummy arcs of duration $0$ to express the precedences.
- **Time-cost trade-off.** If each activity can be shortened at a linear cost, the cheapest way to reach a target duration is a linear program (Kelley 1961).
- **Limited resources.** With a limit on how many activities can run at once, or on shared resources, the problem is the [resource-constrained project scheduling problem](/resource-constrained-project-scheduling/), which is strongly NP-hard. CPM then gives the lower bound $T$ and the latest finish times used as priorities.
- **Processors.** On $P$ identical machines, $T$ is the [critical path lower bound](/critical-path-lower-bound/) for [list scheduling](/list-scheduling/), and in a parallel program it is the span, see [critical path](/critical-path/).

## When to use it

Use CPM when a plan is a set of tasks with known durations and "after" constraints and the resources are not the bottleneck: project planning, the build graph of a large program when there are more cores than ready jobs, a CI pipeline, or the stages of a data workflow. The critical path tells you which tasks to speed up, and the floats tell you which tasks can wait. If resources are limited, CPM gives a lower bound and priorities, not a schedule.

## Pitfalls

- **A cycle.** A cycle of precedences has no schedule. Kahn's algorithm finds it; check for it before the passes.
- **Minimum in the forward pass.** An activity waits for the last of its predecessors, so line L2 takes the maximum.
- **Forgetting the activity's own time in the backward pass.** Line L4 subtracts $p_j$ of the successor, not of the activity itself.
- **Free float versus total float.** Using total float as if it were free float leads to delays that push other activities. In the example, E has $9$ minutes of total float, but any delay of E moves G.
- **Ignoring resources.** Two activities with float may still compete for one machine or one person. CPM assumes they never do.
- **Three-point means as certainties.** The PERT mean of the project time is biased low when several paths are near-critical.

## Implementations

## History

The method came from two projects that ran at about the same time in the late 1950s. Morgan R. Walker of du Pont and James E. Kelley Jr. of Remington Rand developed CPM for the planning of plant construction and maintenance, and presented it at the Eastern Joint Computer Conference in December 1959. PERT was developed for the US Navy's Polaris missile program, and Malcolm, Roseboom, Clark and Fazar published it in Operations Research in 1959. Kelley gave the mathematical basis, including the linear program for the time-cost trade-off, in 1961.

## References
