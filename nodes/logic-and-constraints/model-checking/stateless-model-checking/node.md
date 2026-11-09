---
tag: CVKCC4
kind: technique
slug: stateless-model-checking
name: Stateless model checking
aliases:
- VeriSoft-style exploration
area: logic-and-constraints/model-checking
level: research
summary: Check a concurrent program by running it again and again under a controlled scheduler, one interleaving per run, without storing any program state; reductions cut the number of runs.
prereqs: [explicit-state-model-checking, depth-first-search, race-condition]
see_also: [dynamic-partial-order-reduction, sleep-sets, partial-order-reduction, explicit-state-model-checking, on-the-fly-model-checking, state-explosion-problem, race-condition, deadlock-freedom-checking]
sources:
  - paper: "Patrice Godefroid, Model checking for programming languages using VeriSoft, 24th ACM Symposium on Principles of Programming Languages (POPL 1997), ACM, 1997"
    locator: the systematic exploration of the state space of concurrent C programs by re-execution, without storing states, with persistent and sleep sets
  - paper: "Patrice Godefroid, Partial-Order Methods for the Verification of Concurrent Systems, Lecture Notes in Computer Science 1032, Springer, 1996"
    locator: the state-less search with persistent and sleep sets, and the result that it finds every deadlock of an acyclic state space
  - paper: "Cormac Flanagan and Patrice Godefroid, Dynamic partial-order reduction for model checking software, 32nd ACM Symposium on Principles of Programming Languages (POPL 2005), ACM, 2005"
    locator: dynamic partial-order reduction for stateless search
  - paper: "Madanlal Musuvathi and Shaz Qadeer, Iterative context bounding for systematic testing of multithreaded programs, ACM Conference on Programming Language Design and Implementation (PLDI 2007), ACM, 2007"
    locator: preemption bounding in the CHESS tool, and the number of executions with at most c preemptions
  - paper: "Parosh Aziz Abdulla, Stavros Aronis, Bengt Jonsson and Konstantinos Sagonas, Optimal dynamic partial order reduction, 41st ACM Symposium on Principles of Programming Languages (POPL 2014), ACM, 2014"
    locator: the optimal stateless search that explores exactly one execution per Mazurkiewicz trace
---

Stateless model checking explores the behaviours of a concurrent program by running the program itself many times, each time under a different schedule chosen by a controlled scheduler, and checking each run for errors. It stores no program states: the only memory is the current schedule and, at each scheduling point on it, the choices still to try. To return to an earlier point, it re-executes the program from the start along the stored prefix. This makes it applicable to real programs, whose states are too large or too opaque to store, at the price of exploring the same state again on every run that reaches it. Godefroid introduced the approach in the VeriSoft tool (1997), and [dynamic partial-order reduction](/dynamic-partial-order-reduction/) and [sleep sets](/sleep-sets/) are the main ways to cut the number of runs.

## In plain words

A program with several threads can behave differently each time it runs, because the threads take turns in a different order. A bug may show up in only one order out of millions. Ordinary testing runs the program a few times and hopes to hit that order.

A stateless model checker takes control of the turns. It runs the program once with one order, then goes back and tries a different choice at the last point where a choice was possible, then the one before, and so on, until every order has been tried. It does not save copies of the program's memory. To go back, it simply starts the program again and replays the same choices up to that point. Clever rules skip orders that cannot give a new result, which cuts the number of runs a great deal.

## When it applies

- The program is concurrent: threads or processes that share memory or exchange messages, with all the nondeterminism coming from the scheduler, or from inputs that the checker also controls.
- The program can be re-executed deterministically: the same schedule and the same inputs always give the same run. Clocks, random numbers and external input must be fixed or controlled.
- Every run is finite, as in a test harness that runs a few operations and stops, or the runs are cut at a depth bound. On a program with cycles in its state space, a stateless search without a bound may not terminate.
- The properties are checked on single runs: assertions, crashes, data races, deadlocks, and final-state checks. Liveness properties, which need cycles, are not covered by the basic method.

For finite models in a modelling language, where states are small and cycles are common, stateful [explicit-state model checking](/explicit-state-model-checking/) is usually better.

## The template

A schedule $\sigma$ is the sequence of threads chosen so far. The holes are in capitals.

```pseudo id=main
STATELESS-SEARCH(P)
L1  EXPLORE(P, [ ])
L2  return "no error found within the bound"

EXPLORE(P, σ)
L3  s ← REPLAY(P, σ)                                ▷ run P from its start along σ; nothing is stored
L4  if CHECK(s) fails then report σ and stop        ▷ σ reproduces the error
L5  if no thread is enabled in s or BOUND(σ) then return
L6  for each thread p in SCHEDULE(s, σ) do
L7      EXPLORE(P, σ · p)
```

The holes:

- **REPLAY.** Re-execute the program from its initial state, giving control at each scheduling point to the thread named by $\sigma$. Implementations keep the current run going and re-execute only when they backtrack, so each run costs one execution of the program.
- **CHECK.** Assertions, crashes, deadlock (no thread enabled but some not finished), data races, or a check of the final state.
- **SCHEDULE.** The threads to try from the current point. All enabled threads gives the full search over interleavings. A persistent set from a static analysis gives VeriSoft's reduction; [dynamic partial-order reduction](/dynamic-partial-order-reduction/) computes the needed choices from the races seen on the current run; [sleep sets](/sleep-sets/) remove the choices that only reorder independent steps already explored.
- **BOUND.** None, a depth bound, or a bound on the number of preemptions as in CHESS (Musuvathi and Qadeer 2007).

### Example

Each of $n$ threads increments a shared counter $x$, initially $0$, in two steps: $r \gets x$, then $x \gets r + 1$. The assertion at the end is $x = n$. The table compares the number of runs of a full stateless search, the number of Mazurkiewicz traces (runs that differ in the order of two dependent steps), and the number of distinct states that a stateful search would store.

| $n$ | interleavings | traces | runs with $x = n$ | distinct states |
|---|---|---|---|---|
| 2 | 6 | 4 | 2 | 13 |
| 3 | 90 | 36 | 6 | 84 |
| 4 | 2520 | 576 | 24 | 755 |

The interleavings number $(2n)!/2^n$. Two loads of $x$ commute, so the four interleavings of $n = 2$ in which both threads load before either stores form two traces, and an optimal DPOR search explores 4 runs instead of 6. Here the number of traces is $(n!)^2$, which grows faster than the number of states: for $n = 4$, even an optimal stateless search makes 576 runs, while a stateful search stores only 755 states. The assertion fails on the first run that has two loads before a store, which a depth-first search with a fixed order of threads reaches on its second run.

### Why it is correct

With SCHEDULE returning all enabled threads and no bound, EXPLORE is a depth-first search of the tree of all schedules. REPLAY is correct because the program is deterministic given the schedule, so the state $s$ of line L3 is the state reached by $\sigma$, and every finite run of the program is the run of exactly one schedule. Every run is finite, so the tree is finite and the search ends, and it checks every reachable state on some run. With a reduced SCHEDULE, correctness is the theorem of the reduction: a search that explores a persistent set at each point reaches every deadlock and every final state, and with [sleep sets](/sleep-sets/) it still meets every trace; Godefroid (1996) proves this for acyclic state spaces, and the [DPOR page](/dynamic-partial-order-reduction/) gives the proof for its backtrack sets. With BOUND, the search is complete only for the runs within the bound.

### Size and time

The memory is $O(d \cdot t)$ for a depth $d$ and $t$ threads: the current schedule and the choices left at each point. The time is the number of runs times the cost of one run. Without reduction, $t$ threads with $k$ steps each have $(tk)!/(k!)^t$ interleavings. Since no state is stored, the same state is explored once for each run that reaches it, which can make a stateless search slower than a stateful one by a large factor, as in the example. With a preemption bound $c$, the number of runs grows only polynomially in the number of steps for fixed $c$ and $t$, which is why bounded searches scale to real programs.

## Classic examples

- **VeriSoft** (Godefroid 1997) explored concurrent C programs, with scheduling points at operations on communication objects, using persistent and sleep sets computed from static information.
- **CHESS** (Musuvathi and Qadeer) tests multithreaded Windows and .NET programs, with a scheduler that controls the threads through the synchronization library and a bound on preemptions that it raises step by step.
- **Nidhugg, Concuerror and later tools** apply DPOR and its optimal variant to C programs under weak memory models and to Erlang programs.
- **Java PathFinder** can be run as a stateful or a stateless checker of Java bytecode.

## Variations

- **Stateful hybrids.** Store some states, or hashes of them, to stop runs that reach a known state; Yang, Chen, Gopalakrishnan and Kirby (2008) combine this with DPOR, which needs care, because a state that is cut off may hide races.
- **State-space caching.** Keep a bounded cache of visited states, which Godefroid, Holzmann and Pirottin (1992) combined with sleep sets.
- **Preemption and delay bounding.** Explore only schedules with few preemptions or few deviations from a default scheduler. Many concurrency bugs need only a few preemptions.
- **Random and probabilistic scheduling.** Sample schedules at random, with a guaranteed probability of finding bugs of small depth, instead of exploring them all.
- **Weak memory models.** Explore the executions allowed by a memory model such as TSO or the C11 model, where a run is no longer a single interleaving of steps.

## Pitfalls

- **Nondeterminism outside the scheduler.** If the program reads the time, uses random numbers, or depends on input that is not replayed, REPLAY does not reach the same state, and the search is silently incomplete.
- **Non-terminating runs.** A spin loop that waits for another thread makes a run infinite under an unfair schedule. Bound the depth, or make the scheduler fair, and report the cut runs.
- **Coarse scheduling points.** If the scheduler can switch threads only at synchronization calls, races on plain variables are not explored. Either instrument every shared access, or first check that the program has no data races.
- **Counting runs as states.** A stateless search can explore the same state very many times. A large number of runs is not a sign of a large state space.
- **Bounded means incomplete.** A search with a depth or preemption bound that finds no error has not proved the program correct.

## Exercises

1. For $n = 2$ in the example, list the six interleavings, group them into the four traces, and say which give $x = 2$.
2. Show that $t$ threads with $k$ steps each have $(tk)!/(k!)^t$ interleavings, and evaluate it for $t = 3$, $k = 5$.
3. Explain why a stateless search does not terminate on a program in which one thread waits in a loop for a flag set by another, and propose a fix.
4. Why must a stateless search control every source of nondeterminism, while a stateful search only needs to enumerate them?

## References
