---
tag: CRAW0D
kind: model
slug: fork-join-model
name: Fork-join model
aliases:
- spawn-and-sync model
- Cilk model
area: parallel/work-span-models
level: core
summary: A program model in which a procedure can spawn a child that runs in parallel with it and later sync to wait for its children. Each run is a series-parallel DAG with work W and span S.
prereqs: [work-span-model, computation-dag]
see_also: [work-and-span, fork-join-parallelism, parallel-for, work-stealing, blumofe-leiserson-bound, determinacy-race, parallel-fibonacci, pram-model]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Chapter 27, Section 27.1 (spawn, sync and parallel, the serialization, the computation dag with its continuation, spawn, call and return edges, work and span, and the composition rules), Section 27.2 (multithreaded matrix multiplication) and Section 27.3 (multithreaded merge sort)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 26, Section 26.1 (the basics of fork-join parallelism)
  - paper: "Robert D. Blumofe, Christopher F. Joerg, Bradley C. Kuszmaul, Charles E. Leiserson, Keith H. Randall and Yuli Zhou, Cilk: an efficient multithreaded runtime system, PPoPP 1995"
    locator: pp. 207-216, the Cilk language and its runtime with a provably good work-stealing scheduler
  - paper: doi:10.1145/277650.277725
    title: "Matteo Frigo, Charles E. Leiserson and Keith H. Randall, The implementation of the Cilk-5 multithreaded language, PLDI 1998"
    locator: the spawn and sync keywords of Cilk-5, the serial elision, and the work-first principle
  - paper: doi:10.1145/258492.258493
    title: "Mingdong Feng and Charles E. Leiserson, Efficient detection of determinacy races in Cilk programs, SPAA 1997"
    locator: Section 3 (series-parallel dags, and Theorem 3, which states that the control-flow dag of a Cilk program is series-parallel)
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: Section 2 (fully strict multithreaded computations) and Theorems 5 and 13 (the space and time bounds of randomized work stealing)
---

The fork-join model is a way to write parallel programs and to count their cost. A procedure can *spawn* a child procedure, which may run in parallel with the code that follows the spawn, and it can *sync* to wait until all the children it has spawned are done. The children can spawn in turn, so the parallelism is nested. Each run of a program is a series-parallel [computation DAG](/computation-dag/), and its cost is the work $W$ and the span $S$ of the [work-span model](/work-span-model/).

## The machine

The notation is that of the work-span model.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W = T_1$ | the work, and the time on one processor |
| $S = T_\infty$ | the span, and the time on an unbounded number of processors |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |

A program is an ordinary serial program with three more control words. CLRS (third edition, Section 27.1) writes them as **spawn**, **sync** and **parallel**. Cilk (Blumofe and others, 1995, and the Cilk-5 language of Frigo, Leiserson and Randall, 1998) writes them as `spawn` and `sync`.

- `spawn F(x)` calls $F$, but the caller does not wait for the call to return. The caller goes on with the next statement, the *continuation*, and the child and the continuation may run at the same time.
- `sync` waits until every child that the current procedure has spawned has returned. Each procedure ends with an implicit sync, so a procedure never returns before its children.
- `parallel for` runs the iterations of a loop in parallel. It is not a new primitive: it is compiled to a balanced tree of spawns that splits the range of the loop in half at each level (see [parallel for](/parallel-for/)).

The keywords give permission for parallel execution. They do not force it. If one deletes every spawn and sync, the result is the *serialization* (CLRS) or *serial elision* (Cilk-5) of the program, which is an ordinary serial program. A run of the parallel program on one processor, in the order of the serial elision, does the same steps as the serial elision.

Which procedures run where is decided by a scheduler, not by the program. The processors share one memory. The program does not name the processors, and it does not know how many there are. This is the main difference from the [PRAM](/pram-model/), where the program says what each processor does in each step.

**The DAG of a run.** One run of a program on one input is a [computation DAG](/computation-dag/). A *strand* is a maximal sequence of instructions with no spawn, sync or return; on this page each strand is cut into unit-time steps, which are the vertices. CLRS (Section 27.1) has four kinds of edges.

- A *continuation* edge goes from a strand to the next strand of the same procedure.
- A *spawn* edge goes from the strand that spawns to the first strand of the child.
- A *call* edge goes from the strand that calls to the first strand of the called procedure.
- A *return* edge goes from the last strand of a child to the strand after the next sync in its parent (for a spawn), or to the strand after the call (for a call).

The DAG depends on the program and the input, but not on the number of processors or on the schedule.

**Series-parallel structure.** Every DAG that a fork-join program makes is *series-parallel*: it has one source and one sink, and it is built from single strands by two operations. The series composition $G_1 ; G_2$ puts the sink of $G_1$ before the source of $G_2$. The parallel composition $G_1 \parallel G_2$ puts the two graphs side by side between a new source and a new sink. A spawn followed by the code up to the next sync is a parallel composition of the child and that code, and the rest of the procedure is a series composition. Feng and Leiserson (1997, Theorem 3) prove that the control-flow DAG of a Cilk program is series-parallel.

## What it counts

The cost of a run is two numbers.

- The **work** $W$ is the number of unit strands, that is, the time on one processor.
- The **span** $S$ is the number of unit strands on a longest path of the DAG, that is, the time on an unbounded number of processors (see [work and span](/work-and-span/) and [critical path](/critical-path/)).

Because the DAG is series-parallel, both numbers follow from two rules, with no need to build the DAG.

$$W(G_1 ; G_2) = W(G_1) + W(G_2), \qquad S(G_1 ; G_2) = S(G_1) + S(G_2),$$

$$W(G_1 \parallel G_2) = W(G_1) + W(G_2), \qquad S(G_1 \parallel G_2) = \max\big(S(G_1), S(G_2)\big).$$

Applied to a recursive program, the rules give recurrences for $W(n)$ and $S(n)$, as on [work-span analysis](/work-span-analysis/). A spawn and the sync after it cost $O(1)$ in this model; a real runtime system has a cost per spawn, and programs stop spawning below a cutoff size to amortize it.

**Example.** The program

```text
F():
    work for 2 steps
    spawn G()        G works for 5 steps
    work for 3 steps
    sync
    work for 1 step
```

has $W = 2 + 5 + 3 + 1 = 11$ and $S = 2 + \max(5, 3) + 1 = 8$. If one deletes the sync, the last step can run in parallel with $G$, and the span falls to $2 + \max(5, 3 + 1) = 7$. If one writes `call` in place of `spawn`, the span is $11$. The test file checks these three numbers and checks, on 400 random programs, that the two rules give the same $W$ and $S$ as the longest path in the DAG that the program builds.

**Example (P-FIB).** [Parallel Fibonacci](/parallel-fibonacci/) spawns $F(n - 1)$, calls $F(n - 2)$ and syncs. With one strand before the spawn and one after the sync, $W(n) = W(n - 1) + W(n - 2) + 2$ and $S(n) = S(n - 1) + 2$, so $W(n) = 3F_{n+1} - 2$ and $S(n) = 2n - 1$ for $n \ge 1$, where $F_k$ is the $k$-th Fibonacci number.

**Example (parallel for).** A parallel loop of $n$ iterations, with $b$ unit steps in each body and one unit step in each split of the range, has $W = nb + (n - 1)$ and $S = \lceil \lg n \rceil + b$. The loop adds a span of $\Theta(\lg n)$ to the span of one iteration.

**Time on $p$ processors.** The work and the span bound the time of every schedule from below: $T_p \ge W/p$ (the [work law](/work-law/)) and $T_p \ge S$ (the [span law](/span-law/)). A greedy scheduler, which never leaves a processor idle while a strand is ready, takes at most $W/p + S$ steps ([Brent's theorem](/brent-theorem/) and [greedy scheduling](/greedy-scheduling/)). The test file runs a greedy schedule on random program DAGs and checks $\max(\lceil W/p \rceil, S) \le T_p \le \lfloor W/p \rfloor + S$.

## Relation to other models

- **The work-span model.** The fork-join model is the programming side of the [work-span model](/work-span-model/). The work-span model accepts any DAG; the fork-join model makes only series-parallel DAGs, and gives the composition rules above.
- **Fork-join parallelism as a pattern.** [Fork-join parallelism](/fork-join-parallelism/) and [task parallelism](/task-parallelism/) describe the same pattern from the side of the programmer. This page is about the model and its cost.
- **Fully strict computations.** Blumofe and Leiserson (1999, Section 2) study multithreaded computations in which every join edge from a thread goes to its parent. They call these fully strict. A fork-join program gives a fully strict computation, so their work-stealing bounds hold for it.
- **The PRAM.** The [PRAM](/pram-model/) has $p$ processors that run in lock step, and the program says what each one does in each step. A fork-join program does not name processors. The work-time framework for the PRAM measures work and time in the same way, and the two bounds $W/p + S$ and Brent's principle for the PRAM are the same idea. The PRAM charges nothing for concurrent access to one cell in some of its variants; the fork-join model has no rule for it, and two logically parallel accesses to one location with at least one write are a [determinacy race](/determinacy-race/), a bug.
- **Futures and general DAGs.** Some computations have a DAG that is not series-parallel, such as a pipeline or the wavefront of a dynamic program on an $n \times n$ grid, whose DAG has span $2n - 1$. A fork-join program must add edges to make the DAG series-parallel, and this can make the span larger. The natural divide-and-conquer program for the grid does the top-left quadrant, then the top-right and bottom-left quadrants in parallel, then the bottom-right quadrant, so $S(n) = 3S(n/2) + O(1) = \Theta(n^{\lg 3})$. Futures and other dataflow models can express the grid DAG directly.
- **BSP and message passing.** In the [BSP model](/bsp-model/), the program is a sequence of supersteps with explicit communication, and the cost counts the communication. The fork-join model has no cost for communication; its schedulers keep communication low, as the bound on steals in [work stealing](/work-stealing/) shows.

## Known results in the model

- **Greedy scheduling.** Every greedy schedule on $p$ processors has $T_p \le W/p + S$ ([Brent's theorem](/brent-theorem/)), which is within a factor 2 of the best schedule, because the best schedule needs $\max(W/p, S)$.
- **Work stealing.** The randomized [work-stealing](/work-stealing/) scheduler of Blumofe and Leiserson runs a fully strict computation in expected time $T_1/P + O(T_\infty)$ and in space at most $S_1 P$, where $S_1$ is the space of the serial run ([Blumofe-Leiserson bound](/blumofe-leiserson-bound/); BL99, Theorems 13 and 5, with the exact form of the high-probability bound on that page). Cilk runs a fork-join program by work stealing.
- **The work-first principle.** Frigo, Leiserson and Randall (1998) built Cilk-5 on the work-first principle: put the overhead of scheduling on the critical path, not on the work, because the work term $T_1/P$ dominates when the parallelism is much larger than $P$ (see [parallel slackness](/parallel-slackness/)).
- **Algorithms.** CLRS, third edition, gives multithreaded matrix multiplication with $W = \Theta(n^3)$ and $S = \Theta(\lg^2 n)$ (Section 27.2), and merge sort with a parallel merge, with $W = \Theta(n \lg n)$ and $S = \Theta(\lg^3 n)$ (Section 27.3; see [parallel merge sort](/parallel-merge-sort/)). [Parallel prefix sums](/all-prefix-sums/) have $W = O(n)$ and $S = O(\lg n)$. [P-FIB](/parallel-fibonacci/) has $W = \Theta(\phi^n)$ and $S = \Theta(n)$.
- **Race detection.** A fork-join program with no [determinacy race](/determinacy-race/) gives the same result on every schedule as its serial elision. The SP-bags algorithm of Feng and Leiserson (1997) checks one run for determinacy races in time $O(T\,\alpha(v, v))$, where $T$ is the serial time and $v$ is the number of shared locations. It uses the series-parallel structure of the DAG.

## References
