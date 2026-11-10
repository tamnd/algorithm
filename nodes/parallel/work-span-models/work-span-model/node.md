---
tag: KF3VY8
kind: model
slug: work-span-model
name: Work-span model
aliases:
- work-depth model
- multithreaded model
area: parallel/work-span-models
level: core
summary: Cost model where a parallel computation is a DAG of unit-time strands, measured by its work W (the number of strands) and its span S (the number of strands on a longest path).
prereqs: [directed-acyclic-graph, asymptotic-notation]
see_also: [work-and-span, computation-dag, work-span-analysis, brent-theorem, greedy-scheduling, fork-join-model, pram-model, work-stealing]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1 (the dag model of multithreaded execution, the ideal parallel computer, work and span, and Figure 27.3 for the series and parallel composition rules)
  - paper: doi:10.1145/227234.227246
    title: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the work and depth cost model and its use in the NESL language
  - paper: doi:10.1145/321812.321815
    title: "Richard P. Brent, The parallel evaluation of general arithmetic expressions, Journal of the ACM 21(2), 1974"
    locator: Lemma 2, the step-counting lemma that becomes the scheduling bound
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (the basics of fork-join parallelism)
---

The work-span model is a cost model for parallel algorithms in which one run of a program is a [directed acyclic graph](/directed-acyclic-graph/) of unit-time steps, called strands, and the cost is two numbers. The work $W$ is the number of strands, and the span $S$ is the number of strands on a longest path. The model does not fix the number of processors, and a scheduling theorem turns the two numbers into a time bound: on $p$ processors a greedy scheduler takes time $T_p$ with $\max(W/p, S) \le T_p \le W/p + S$.

## The machine

The machine is the *ideal parallel computer* of CLRS (third edition, Section 27.1). It has a shared memory that is sequentially consistent, and it has identical processors. The cost of scheduling is zero: a strand that is ready can start on an idle processor at once. A program is written in the [fork-join](/fork-join-model/) style, with three control words.

- *spawn* starts a procedure call that may run in parallel with the code after it.
- *sync* waits until all procedures that the current procedure spawned have finished.
- *parallel for* runs the iterations of a loop in parallel. It is compiled to a divide-and-conquer tree of spawns (see [parallel for](/parallel-for/)).

One run of a program on one input gives a [computation DAG](/computation-dag/). Its vertices are strands and its edges are the order constraints between them. On this page each strand is one unit-time step. A run of $k$ serial steps is a chain of $k$ unit strands. The DAG can depend on the input, as in a quicksort whose pivots depend on the data. The DAG does not depend on the number of processors or on the schedule.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work: the number of strands, and the time on one processor |
| $S$, $D$, $T_\infty$ | the span (or depth): the number of strands on a longest path, and the time on unbounded processors |
| $T_p$ | the time on $p$ processors under a given scheduler |
| $W/S$ | the [parallelism](/parallelism/) |

The cost model on this page is the work-span model. All bounds are for unit-time strands.

## What it counts

The model counts two things for each computation DAG $G$: the work $W(G) = |V(G)|$ and the span $S(G)$, the number of vertices on a longest path of $G$. The page [work and span](/work-and-span/) treats the two measures in detail, and the page [work-span analysis](/work-span-analysis/) gives the method of computing them with recurrences.

A fork-join program builds its DAG from single strands by two operations. Let $A$ and $B$ be DAGs on disjoint vertex sets.

- The *series composition* $A ; B$ is the union of $A$ and $B$ with one more edge from each sink of $A$ to each source of $B$. It is the DAG of "run $A$, then run $B$".
- The *parallel composition* $A \parallel B$ is the union of $A$ and $B$ with no new edge. It is the DAG of "run $A$ and $B$ at the same time".

A spawn of $A$ followed by $B$ and a sync is $x ; (A \parallel B) ; y$, where $x$ is the strand that spawns and $y$ is the strand after the sync. In CLRS each procedure has one first and one last strand, so the series composition there is one edge, and it is the same thing.

**Composition rules.** For DAGs $A$ and $B$ on disjoint vertex sets:

$$W(A ; B) = W(A) + W(B), \qquad S(A ; B) = S(A) + S(B),$$

$$W(A \parallel B) = W(A) + W(B), \qquad S(A \parallel B) = \max(S(A), S(B)).$$

*Proof.* Both compositions have the vertex set $V(A) \cup V(B)$, and the two sets are disjoint, so the work adds in both cases.

For the parallel composition, no edge joins $A$ and $B$. So each path lies inside $A$ or inside $B$, and the longest path has $\max(S(A), S(B))$ strands.

For the series composition, each new edge goes from $A$ to $B$, and no edge goes from $B$ to $A$. So a path that enters $B$ stays in $B$. Each path is then a path in $A$ (maybe empty) followed by a path in $B$ (maybe empty), and it has at most $S(A) + S(B)$ strands. For the other direction, take a longest path $P_A$ of $A$. Its first vertex is a source of $A$, because otherwise a predecessor would make a longer path. In the same way its last vertex is a sink of $A$. Take a longest path $P_B$ of $B$, which goes from a source of $B$ to a sink of $B$. The new edge from the last vertex of $P_A$ to the first vertex of $P_B$ joins them into a path of $S(A) + S(B)$ strands. $\blacksquare$

The rules give the cost of a spawn and sync directly: $W = W(A) + W(B) + 2$ and $S = \max(S(A), S(B)) + 2$. For example, take a recursive sum of $n$ numbers that spawns the two halves. Its costs satisfy $W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + 2$ and $S(n) = S(\lceil n/2 \rceil) + 2$, with $W(1) = S(1) = 1$. So $W(n) = 3n - 2$ and $S(n) = 2\lceil \lg n \rceil + 1$. Each of the $n$ leaves adds one strand, and each of the $n - 1$ inner calls adds two. Each level of the recursion adds two strands to the longest path.

Constant factors depend on how many strands a spawn and a sync take. CLRS uses three strands for each procedure that spawns, so its counts differ from the counts above by a constant factor. The asymptotic bounds do not change.

## Relation to other models

- **The RAM.** With unit strands, the work $W$ is the running time of the serial elision of the program (the program with spawn and sync removed) on a [random-access machine](/random-access-machine/). So $T_1 = W$.
- **The PRAM.** The [PRAM](/pram-model/) has a fixed number of processors that run in lock step, and its variants say what happens when two processors use one memory cell. The work-time framework for the PRAM (JáJá, Chapter 1) also counts work and time, and Brent's principle turns them into a time on $p$ processors. The work-span model leaves the processors out of the program and gives that job to the scheduler. It does not charge for memory conflicts. A [determinacy race](/determinacy-race/) is a correctness problem in this model, not a cost.
- **Circuits.** A [Boolean circuit](/boolean-circuit/) has a size and a depth, which are like the work and the span. A circuit is fixed for each input length, but a computation DAG can depend on the input values.
- **Memory hierarchy.** The model does not count cache misses. The [cache-oblivious model](/cache-oblivious-model/) and the [external memory model](/external-memory-model/) count them.
- **BSP.** The [BSP model](/bsp-model/) adds a cost for communication and for each barrier, which the work-span model does not have.
- **Scheduling.** A scheduler maps the DAG to processors. The model leaves the choice open. A [greedy scheduler](/greedy-scheduling/) and [work stealing](/work-stealing/) are the two standard choices.

## Known results in the model

The model has a small set of general theorems, and the pages below prove them.

| Result | Statement | Where proved |
|---|---|---|
| [Work law](/work-law/) | $T_p \ge W/p$ for each scheduler | proved on its page |
| [Span law](/span-law/) | $T_p \ge S$ for each scheduler | proved on its page |
| [Brent's theorem](/brent-theorem/) | some schedule has $T_p \le W/p + S$ | proved on its page |
| [Greedy scheduling](/greedy-scheduling/) | each greedy schedule has $T_p \le W/p + S$, so it is within a factor 2 of optimal | proved on its page |
| [Work stealing](/work-stealing/) | $\mathbb{E}[T_p] \le W/p + O(S)$ for randomized work stealing | cited from Blumofe and Leiserson 1999, see the [Blumofe-Leiserson bound](/blumofe-leiserson-bound/) |
| Optimal schedules | finding a shortest schedule of a DAG of unit strands on $p$ processors is NP-hard when $p$ is part of the input | cited from Ullman 1975, see [precedence-constrained scheduling](/precedence-constrained-scheduling/) |

The work and span of standard algorithms in the model are below. The rows marked CLRS are proved in CLRS, third edition, Chapter 27. The sum and Fibonacci rows follow from the composition rules on this page and on [work and span](/work-and-span/).

| Algorithm | Work $W$ | Span $S$ | Source |
|---|---|---|---|
| sum of $n$ numbers ([parallel reduce](/parallel-reduce/)) | $\Theta(n)$ | $\Theta(\log n)$ | this page |
| [parallel Fibonacci](/parallel-fibonacci/) | $\Theta(\phi^n)$ | $\Theta(n)$ | CLRS Section 27.1 |
| [Blelloch scan](/blelloch-scan/) | $\Theta(n)$ | $\Theta(\log n)$ | Blelloch 1990 |
| [Hillis-Steele scan](/hillis-steele-scan/) | $\Theta(n \log n)$ | $\Theta(\log n)$ | Hillis and Steele 1986 |
| [merge sort](/merge-sort/) with parallel calls and a serial merge | $\Theta(n \log n)$ | $\Theta(n)$ | CLRS Section 27.3 |
| [parallel merge sort](/parallel-merge-sort/) with a parallel merge | $\Theta(n \log n)$ | $\Theta(\log^3 n)$ | CLRS Section 27.3 |
| recursive [matrix multiplication](/parallel-matrix-multiplication/) | $\Theta(n^3)$ | $\Theta(\log^2 n)$ | CLRS Section 27.2 |

## References
