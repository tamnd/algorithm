---
tag: T081GV
kind: concept
slug: task-parallelism
name: Task parallelism
area: parallel/parallel-primitives
level: intro
summary: Run separate tasks, often of different kinds, at the same time, as far as their dependences allow. The program is a task graph or a set of futures, and a scheduler maps the tasks to processors.
prereqs: [computation-dag, work-span-model]
see_also: [data-parallelism, fork-join-parallelism, list-scheduling, greedy-scheduling, critical-path, work-stealing, graham-anomalies, topological-sort]
sources:
  - paper: doi:10.1137/0117039
    title: Ronald L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969
    locator: the list schedule of a task graph on m processors, its bound of 2 - 1/m times the optimum, and the anomalies
  - paper: doi:10.1145/4472.4478
    title: Robert H. Halstead Jr., Multilisp, a language for concurrent symbolic computation, ACM Transactions on Programming Languages and Systems 7(4), 1985
    locator: the future construct and its use for parallel evaluation
  - paper: doi:10.1145/344588.344618
    title: Yu-Kwong Kwok and Ishfaq Ahmad, Static scheduling algorithms for allocating directed task graphs to multiprocessors, ACM Computing Surveys 31(4), 1999
    locator: the task graph model, the NP-hardness of the general problem, and the survey of list scheduling heuristics
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 2 (task parallelism and data parallelism) and Chapter 8 (fork-join)
---

Task parallelism gets speed from doing separate tasks at the same time. A task is a piece of work, such as a function call, a file to compile or a request to serve, and different tasks may do quite different things. Some tasks need the results of others, so the program is a *task graph*: a [directed acyclic graph](/directed-acyclic-graph/) with an edge from each task to each task that must wait for it. A scheduler starts each task as soon as its inputs are ready and a processor is free. This is the other main style beside [data parallelism](/data-parallelism/), where one operation runs on many items at once. In task parallelism, the amount of parallelism comes from the shape of the task graph, not from the size of the data.

Notation on this page: $W$ is the work, the sum of the costs of all tasks, and $S$ is the span, the cost of the longest path in the task graph. $P$ is the number of processors, and $T_P$ is the time of a schedule on $P$ processors.

## In plain words

To cook a dinner, some jobs can happen at the same time. One cook boils the rice while another cuts the meat. But the meat must be cut before it is fried, and the sauce must be ready before the dish is served.

Write each job down with the jobs it must wait for. This list is the plan. The cooks then take any job whose earlier jobs are done.

The dinner can never be faster than the longest chain of jobs that must happen one after another. More cooks help only until that chain is the limit.

The order in which free cooks pick jobs also matters. A poor choice can make the dinner later, even with the same cooks.

## The idea

**The task graph.** Each task $v$ has a cost $t_v$, and an edge $u \to v$ means that $v$ starts only after $u$ ends. The work is $W = \sum_v t_v$, and the span $S$ is the largest sum of costs along a path, the [critical path](/critical-path/). The [work law](/work-law/) and the [span law](/span-law/) give $T_P \ge \max\{W/P, S\}$ for each schedule.

**Greedy schedules.** A *list schedule* keeps the tasks in a list of priorities and, whenever a processor is free, gives it the first ready task in the list ([list scheduling](/list-scheduling/)). Each such [greedy schedule](/greedy-scheduling/) has $T_P \le W/P + S$, which is less than twice the optimum, and Graham (1969) showed the sharper factor $2 - 1/P$. Finding an optimal schedule is NP-hard in general, so practical schedulers use heuristics, for example a priority by the longest path from a task to the end; Kwok and Ahmad (1999) survey them. A list schedule can also behave in strange ways: a faster task or one more processor can make it later ([Graham anomalies](/graham-anomalies/)).

**Ways to write the graph.**

- *Fork-join.* Tasks are spawned and joined in nested pairs, which gives a series-parallel graph ([fork-join parallelism](/fork-join-parallelism/)). Most divide and conquer code has this form.
- *Futures.* A `future` starts a computation and at once returns a handle. A task that reads the handle waits until the value is ready (Halstead 1985). Since a handle can be passed to any task, futures make graphs that are not series-parallel, such as pipelines.
- *Explicit dependences.* The program states for each task what it reads and writes, and the runtime builds the edges, as in a build file or OpenMP tasks with `depend` clauses.

**Task parallelism and data parallelism.**

| | task parallelism | data parallelism |
|---|---|---|
| unit of work | a task, which may differ from the others | one operation on one item |
| source of parallelism | independent branches of the task graph | the number of items |
| how it grows | with the width of the graph | with the size of the input |
| load balance | dynamic, since tasks have different costs | often static, since items cost the same |
| typical hardware | multicore CPUs and clusters | GPUs, vector units and SIMD |
| typical primitives | spawn, sync, futures, task queues | [parallel map](/parallel-map/), [parallel reduce](/parallel-reduce/), scans |

The two styles mix. A data parallel loop is often run as tasks, each task a chunk of the loop, and a task graph can have data parallel tasks inside it.

## Examples

**A small task graph.** Six tasks with the costs $A = 2$, $B = 3$, $C = 1$, $D = 4$, $E = 2$ and $F = 1$, and the edges $A \to B$, $A \to C$, $A \to D$, $B \to E$, $C \to E$, $D \to F$ and $E \to F$. The work is $W = 13$. The paths from $A$ to $F$ cost $8$ through $B$ and $E$, $7$ through $D$, and $6$ through $C$ and $E$, so $S = 8$, and the parallelism is $W/S \approx 1.6$. Two greedy schedules on $P = 2$ processors:

| list order | processor 1 | processor 2 | time |
|---|---|---|---|
| A, B, C, D, E, F | $A$ 0 to 2, $B$ 2 to 5, $E$ 5 to 7, $F$ 7 to 8 | $C$ 2 to 3, $D$ 3 to 7 | 8 |
| A, C, D, B, E, F | $A$ 0 to 2, $C$ 2 to 3, $B$ 3 to 6, $E$ 6 to 8, $F$ 8 to 9 | $D$ 2 to 6 | 9 |

The first schedule takes $8 = S$ and so is optimal. The second starts the short task $C$ before $B$, which is on the critical path, and loses one unit. Both are within the greedy bound $W/P + S = 14.5$.

**A build.** `make -j 8` reads the dependences between files from the makefile and compiles up to 8 files at a time. The final link waits for all object files, so it ends a long path in the graph.

**A pipeline with futures.** A program reads a file in blocks, compresses each block and writes it. With one future per block for the compression, the read of block $i + 1$, the compression of block $i$ and the write of block $i - 1$ run at the same time.

**A server.** Each request is a task. The tasks are independent, so the parallelism is the number of requests in flight, and a pool of threads serves them.

## Where it is used

- Fork-join runtimes: Cilk, Java `ForkJoinPool`, Intel TBB and rayon, which balance the load by [work stealing](/work-stealing/).
- Futures and promises: `std::async` and `std::future` in C++, `CompletableFuture` in Java, futures in Rust and in Python's `concurrent.futures`.
- Task graphs with dependences: OpenMP `task` with `depend`, the TBB flow graph, build tools such as make, and workflow engines for data jobs, which run the tasks in an order consistent with a [topological sort](/topological-sort/).
- Static scheduling of task graphs for embedded systems and clusters, where the costs are known in advance and a list scheduling heuristic plans the whole run.

## References
