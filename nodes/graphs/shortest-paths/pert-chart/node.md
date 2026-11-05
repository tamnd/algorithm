---
tag: RTD4XC
kind: technique
slug: pert-chart
name: PERT chart and critical path method
aliases:
- PERT chart
- critical path method
- CPM
area: graphs/shortest-paths
level: core
summary: Scheduling method that finds the longest path in a task dependency DAG to determine the minimum project duration and critical tasks.
prereqs: [dag-shortest-paths, topological-sort, longest-to-shortest-paths-reduction]
see_also: [critical-path, dag-longest-path, longest-to-shortest-paths-reduction, dag-shortest-paths, topological-sort, difference-constraints, directed-acyclic-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.2, Single-source shortest paths in directed acyclic graphs (the application to PERT charts, critical paths as longest paths, and the two ways to compute them)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 4, Shortest paths, label-setting algorithms (the section on acyclic networks and the project scheduling application)
  - paper: doi:10.1287/opre.7.5.646
    title: D. G. Malcolm, J. H. Roseboom, C. E. Clark and W. Fazar, Application of a technique for research and development program evaluation, Operations Research 7(5), 646 to 669 (1959)
    locator: the PERT network, the three time estimates and the critical path
  - paper: "James E. Kelley Jr. and Morgan R. Walker, Critical-path planning and scheduling, Proceedings of the Eastern Joint Computer Conference, 1959, 160 to 173"
    locator: the critical path method, earliest and latest times, and float
---

A PERT chart is a directed acyclic graph of the tasks of a project and the order in which they must be done. The critical path method computes, for each task, its earliest start time by a forward pass in [topological order](/topological-sort/), and its latest start time by a backward pass. The least time to finish the project is the weight of a longest path in the graph, and the tasks on such a path are the [critical path](/critical-path/): any delay of them delays the whole project. Both passes are [DAG shortest paths](/dag-shortest-paths/) with $\max$ in place of $\min$, or with negated weights, so the method takes $O(n + m)$ time for $n$ tasks and $m$ precedence constraints.

## In plain words

A project has tasks, each with a length of time, and some tasks can only start when others are finished. Tasks that do not wait for each other can run at the same time.

Go through the tasks so that each comes after the tasks it waits for. A task can start as soon as the last of those is finished. The finish of the last task is the shortest possible time for the whole project.

Then go backward from the end. Each task must start early enough that the tasks waiting for it can still start on time. The difference between the latest and the earliest start is the spare time of the task. Tasks with no spare time form the critical path: if one of them is late, the project is late.

## When it applies

- **Tasks with fixed durations and precedence constraints** "task $j$ starts after task $i$ ends", and an unlimited supply of workers or machines, so that tasks with no constraint between them can run in parallel.
- **The precedence graph is acyclic.** A cycle of constraints cannot be satisfied when its durations sum to more than 0, and a topological sort finds such a cycle.
- **Durations are nonnegative real numbers.** The algorithm itself works for any real durations, but a negative duration has no meaning in scheduling. Integer durations are not needed.
- **Minimum lags.** A constraint "start $j$ at least $\ell$ after $i$ starts" is an arc of weight $\ell$; the same passes apply as long as the graph is acyclic.

It does not apply when resources are limited, for example when two tasks need the same machine. That is resource-constrained project scheduling, which is NP-hard in general.

## The template

Tasks are $1, \ldots, n$ with durations $p(j) \ge 0$. $\mathrm{pred}(j)$ and $\mathrm{succ}(j)$ are the tasks that $j$ waits for and the tasks that wait for $j$. The holes are the durations and the precedence arcs.

```pseudo id=main
CPM(tasks, p, pred, succ)
L1  order the tasks topologically; if there is a cycle then return "infeasible"
L2  for each task j in topological order do
L3      ES(j) ← max over i in pred(j) of ES(i) + p(i)        ▷ 0 if pred(j) is empty
L4  T ← max over all j of ES(j) + p(j)                          ▷ least project time
L5  for each task j in reverse topological order do
L6      LS(j) ← (min over k in succ(j) of LS(k)) − p(j)        ▷ the min is T if succ(j) is empty
L7  for each task j do slack(j) ← LS(j) − ES(j)
L8  return T, ES, LS and the critical tasks {j : slack(j) = 0}
```

**Why it is correct.** Add a start vertex $\alpha$ with an arc of weight 0 to each task, and an end vertex $\omega$; give each arc $i \to j$, and each arc $j \to \omega$, the weight $p$ of its tail. A schedule is feasible exactly when $S(j) \ge S(i) + p(i)$ on every arc. By induction in topological order, $ES(j)$ is the weight of a longest path from $\alpha$ to $j$, which is a lower bound for every feasible $S(j)$ (sum the constraints along the path), and the schedule $S = ES$ is feasible. So $T$, the longest path from $\alpha$ to $\omega$, is the least project time. In the same way, by induction in reverse order, $T - LS(j)$ is the longest path from $j$ to $\omega$, so $LS(j)$ is the latest start of $j$ in any schedule that ends by $T$. A task has slack 0 exactly when the longest path through it has weight $T$, so the critical tasks are the tasks on longest paths from $\alpha$ to $\omega$.

**Cost.** The topological sort and each pass look at each task and each arc once: $O(n + m)$ time and $O(n)$ extra space.

## Classic examples

**A six-task project.** The tasks are A (3), B (2), C (4) after A, D (6) after B, E (2) after A, and F (1) after C and D.

| task | duration | ES | LS | slack |
|---|---|---|---|---|
| A | 3 | 0 | 1 | 1 |
| B | 2 | 0 | 0 | 0 |
| C | 4 | 3 | 4 | 1 |
| D | 6 | 2 | 2 | 0 |
| E | 2 | 3 | 7 | 4 |
| F | 1 | 8 | 8 | 0 |

The forward pass gives $ES(F) = \max(3 + 4, 2 + 6) = 8$, and $T = \max(8 + 1, 3 + 2) = 9$. The backward pass gives $LS(F) = 9 - 1 = 8$, $LS(E) = 9 - 2 = 7$, $LS(C) = 8 - 4 = 4$, $LS(D) = 8 - 6 = 2$, $LS(A) = \min(4, 7) - 3 = 1$ and $LS(B) = 2 - 2 = 0$. The critical path is $B \to D \to F$, with $2 + 6 + 1 = 9$. Task E can start as late as time 7 without delaying the project.

**Activity on arc.** CLRS draws each task as an arc and each vertex as an event: "all tasks into this vertex are done". Then the weights are on the arcs, and a critical path is a longest path from the first to the last event, computed by DAG shortest paths on negated weights. The two drawings give the same numbers; activity-on-node needs no dummy arcs.

**A cycle.** If A must also wait for F, the arcs $A \to C \to F \to A$ form a cycle of total duration $3 + 4 + 1 = 8 > 0$, and no schedule exists. Line L1 reports it.

## Variations

- **PERT with three estimates.** In the original PERT, each task has an optimistic time $a$, a most likely time $b$ and a pessimistic time $c$, with the mean $(a + 4b + c)/6$ and the variance $((c - a)/6)^2$ of a beta distribution. The method adds the means and the variances along the critical path and uses a normal approximation for the chance to finish by a date.
- **Free slack and total slack.** The slack of line L7 is the total slack. The free slack, $\min_{k \in \mathrm{succ}(j)} ES(k) - ES(j) - p(j)$, is the delay that does not change the earliest start of any other task.
- **Time-cost trade-off.** If each task can be shortened at a cost, the cheapest way to reach a project time is a linear program, the dual of a min-cost flow problem (Fulkerson 1961, Kelley 1961).
- **General lags.** Constraints of both kinds, "at least" and "at most", give a system of [difference constraints](/difference-constraints/), which may have cycles; the earliest times are then longest paths computed by Bellman-Ford, and a positive cycle means the system is infeasible.

## Pitfalls

- **Using Dijkstra.** The earliest times are longest paths. Dijkstra on negated weights is wrong, and a shortest path in the chart gives no useful number.
- **Taking the minimum in the forward pass.** A task waits for the last of its predecessors, so line L3 takes the maximum. The minimum gives start times that break the constraints.
- **Only one critical path.** Several paths can have weight $T$, and all their tasks have slack 0. Shortening one critical task does not shorten the project if another critical path avoids it.
- **The PERT probability.** The normal approximation on one critical path ignores the other paths of nearly the same length, so it is too optimistic: the real chance to finish on time is lower.
- **Limited resources.** The passes assume that any number of tasks can run at once. With shared machines or staff, the schedule $S = ES$ may not be possible.

## Exercises

1. Add a task G of duration 3 after E and before F in the six-task project, and compute the new ES, LS, slack and critical path.
2. Show that the slack of a task is 0 if and only if the task lies on a longest path from the start to the end.
3. Convert the six-task project to the activity-on-arc form, with one arc per task and dummy arcs where needed, and check that the longest path still has weight 9.
4. For tasks with three estimates $(1, 2, 3)$, $(2, 4, 12)$ and $(1, 1, 1)$ in a chain, compute the mean and the variance of the project time.
5. Show that the earliest start times are the least solution of the system $S(j) \ge S(i) + p(i)$ with $S \ge 0$, and that the latest start times are the greatest solution with $S(j) + p(j) \le T$.

## References
