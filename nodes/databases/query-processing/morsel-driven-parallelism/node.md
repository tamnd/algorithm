---
tag: DJF10W
kind: technique
slug: morsel-driven-parallelism
name: Morsel-driven parallelism
aliases:
- morsel-wise scheduling
area: databases/query-processing
level: research
summary: Split the input of each pipeline into small morsels that worker threads take dynamically, which balances load on many cores.
prereqs: [pipelining-and-materialization, exchange-operator, greedy-scheduling]
see_also: [data-centric-query-compilation, vectorized-query-execution, work-stealing, list-scheduling, data-skew, parallel-hash-join, hash-aggregation, amdahls-law]
sources:
  - paper: doi:10.1145/2588555.2610507
    title: Viktor Leis, Peter Boncz, Alfons Kemper and Thomas Neumann, Morsel-driven parallelism, a NUMA-aware query evaluation framework for the many-core age, Proceedings of ACM SIGMOD 2014, 743 to 754
    locator: the dispatcher, the morsel size, NUMA-aware work stealing, and the evaluation on TPC-H and SSB
  - paper: doi:10.14778/2002938.2002940
    title: Thomas Neumann, Efficiently compiling efficient query plans for modern hardware, Proceedings of the VLDB Endowment 4(9), 539 to 550 (2011)
    locator: the pipelines and pipeline breakers that the morsel tasks follow
  - paper: doi:10.1145/93597.98720
    title: Goetz Graefe, Encapsulation of parallelism in the Volcano query processing system, Proceedings of ACM SIGMOD 1990, 102 to 111
    locator: the exchange operator, the plan-driven model that morsels replace
---

Morsel-driven parallelism runs each pipeline of a query plan on all cores by cutting its input into small pieces, called morsels, of about 100,000 tuples. A fixed pool of worker threads, one per hardware thread, takes morsels from a dispatcher at run time, and each worker runs the whole pipeline on its morsel, up to the next pipeline breaker. Because the work is handed out in small pieces while the query runs, fast and slow threads finish at about the same time, and the number of threads for a query can change between morsels. Leis, Boncz, Kemper and Neumann (2014) built it in the HyPer system, with morsels placed and taken by NUMA node so that most memory accesses stay local.

## In plain words

A team must peel a big heap of potatoes. With the old method, the boss splits the heap into one pile per worker before they start. If one worker is slow, or one pile is larger, everyone waits for the last pile. With morsels, the heap stays in one place, and each worker takes a small bowl at a time. When a worker is done with a bowl, she takes the next one. No one waits long at the end, because the last bowls are small. The workers also take bowls from the heap that is nearest to them, and walk to another heap only when their own is empty.

## When it applies

- The machine has many cores, often on several sockets with their own memory (NUMA), and the data is in memory.
- The plan can be cut into pipelines, as in [pipelining and materialization](/pipelining-and-materialization/), and the work of one pipeline can be split by its input: each morsel can be run on its own.
- The work per tuple varies, because of [skew](/data-skew/), cache effects or other queries on the same machine, so a split fixed in advance gives some threads more work than others.
- Several queries share the machine, and the system wants to give cores to a new or more urgent query without waiting for the running ones to end.

## The template

A pipeline job $p$ has a source (a table, or the stored result of a pipeline breaker) and the code of the pipeline. The dispatcher keeps one queue of morsels for each NUMA node, filled with the morsels whose data lies on that node.

```pseudo id=main
RUN-PIPELINE(p)                            ▷ called when all inputs of p are complete
L1  cut the source of p into morsels; put each one in the queue of the node that holds its data
L2  for each worker w, in parallel do
L3      loop
L4          m ← a morsel from the queue of the node of w, or else one stolen from another node, nearest first
L5          if there is no morsel then leave the loop
L6          RUN(p, m, local state of w)    ▷ hole: the pipeline code, such as a filter and a hash probe
L7  wait until every worker has left the loop        ▷ the pipeline breaker
L8  FINISH(p)                              ▷ hole: merge the local states of the workers
```

The workers never wait for each other inside a pipeline. Each one writes into its own local state, such as a part of a hash table build, and the pipeline breaker merges the parts once, at line L8. A worker that leaves the loop at line L5 can take morsels of another query, so the degree of parallelism of a query is not fixed in its plan.

**Why the load is balanced.** Within one pipeline, the morsels are independent tasks, and the dispatcher gives a morsel to any worker that asks. This is a greedy list schedule. If the morsels need total time $W$ on $P$ workers, and the largest morsel needs time $t_{\max}$, let the last morsel to finish start at time $s$. Until $s$ every worker is busy, since an idle worker would have taken that morsel, so $s \le W/P$, and the pipeline ends by time $W/P + t_{\max}$. This is the bound of [list scheduling](/list-scheduling/) and of [greedy scheduling](/greedy-scheduling/) (a theorem, for independent tasks and no cost to take a task). Small morsels make $t_{\max}$ small. Large morsels make the cost of taking a morsel small. Leis et al. found about 100,000 tuples to be a good size on their machines (a measurement).

**Two holes in detail.**

- **Hash join build.** In the build pipeline, each worker writes the tuples of its morsels into a storage area on its own NUMA node. At the pipeline breaker, the total number of tuples is known, so a hash table of the right size is made. A second parallel pass inserts pointers to the stored tuples into the table, with atomic compare-and-swap in place of locks. The probe pipeline then reads the table without any locks.
- **Hash aggregation.** Each worker aggregates its morsels into a small local hash table and moves full entries into partitions by a hash of the group key. After the breaker, each partition is aggregated by one worker, so no two workers update the same group. This is the two-phase [hash aggregation](/hash-aggregation/) with one partition per task.

## Classic examples

- **TPC-H on 32 cores.** On a 4-socket Nehalem EX machine (Xeon X7560 at 2.3 GHz) with 32 cores and 64 hardware threads, HyPer ran TPC-H at scale factor 100 with a geometric mean of 0.45 s per query and a total of 15.3 s, and scaled by a factor of 28.1 from one to 32 cores. Vectorwise on the same machine had a geometric mean of 2.84 s, a total of 93.4 s and a scaling of 9.3 (a measurement). Over TPC-H and SSB the paper reports an average speed-up of over 30 with 32 cores.
- **NUMA placement.** Placing the data and the morsels by NUMA node, against the default memory placement of the operating system, gave a geometric mean speed-up of 1.57 on the Nehalem EX machine and 2.40 on a 4-socket Sandy Bridge EP machine (a measurement).
- **A compiled pipeline per morsel.** In HyPer, RUN at line L6 is the loop of [data-centric query compilation](/data-centric-query-compilation/), restricted to the tuples of one morsel. A [vectorized](/vectorized-query-execution/) engine can use the same scheme and run its vectors over each morsel.

## Variations

- **Against the exchange operator.** In the [exchange operator](/exchange-operator/) model, the optimizer fixes the number of threads of each part of the plan, and the data is split in advance. Morsels move this choice to run time, and no exchange operators appear in the plan. The price is that the operators must be written for parallel use, with shared hash tables and local states, and are no longer serial code.
- **Work stealing.** A worker with no local morsel takes one from another NUMA node. This differs from [work stealing](/work-stealing/) on a deque of tasks made by recursion, since all morsels of a pipeline exist when it starts, but it serves the same goal.
- **Priorities and elasticity.** Since a worker asks for work after each morsel, the dispatcher can give the next morsel to a short or urgent query, and a long query loses cores for a while without being stopped.
- **Morsel size.** The size can be fixed or changed during the run, for example smaller at the end of a pipeline, so that the last morsels do not leave cores idle.

## Pitfalls

- **Morsels that are too large or too small.** Large morsels leave cores idle at the end of a pipeline, as in the $t_{\max}$ term above. Very small morsels make the cost of taking a morsel large compared with the work in it.
- **Shared state.** A global counter or a shared hash table that all workers update for each tuple becomes the bottleneck. Keep the state local to a worker and merge it once at the breaker.
- **Skew inside a partition.** After a partitioning step, one partition with a large group is still one task. The balance by morsels does not help when one task is much larger than $W/P$.
- **Serial parts.** The merge at line L8 and the start of each pipeline are serial or partly serial. [Amdahl's law](/amdahls-law/) limits the speed-up when these parts are large, for example for small queries.
- **Measurements are not bounds.** The speed-ups above depend on the hardware, the data placement and the benchmark. Measure them again on a new machine.

## Exercises

1. A pipeline has 1000 morsels of 1 ms each and one morsel of 50 ms, on 32 workers. Give the bound $W/P + t_{\max}$, and the best possible finish time.
2. Explain why the number of tuples in a build input is known only at the pipeline breaker, and why a hash table of the right size is then cheaper to build than one that grows.
3. Write FINISH for a parallel COUNT(\*) with a local counter per worker, and compare it with a shared counter updated by atomic increments.
4. Two queries share 32 workers, one long and one short. Describe how the dispatcher can make the short query finish first without stopping the long one.

## References
