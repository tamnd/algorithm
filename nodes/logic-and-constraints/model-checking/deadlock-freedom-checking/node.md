---
tag: X57NPP
kind: problem
slug: deadlock-freedom-checking
name: Deadlock detection
aliases:
- Deadlock checking
- Deadlock-freedom checking
area: logic-and-constraints/model-checking
level: core
summary: Decide whether a concurrent system can reach a state with no enabled transition. It is reachability of the dead states, linear on an explicit graph and PSPACE-complete for programs and 1-safe nets.
prereqs: [reachability-problem, labelled-transition-system]
see_also: [reachability-problem, invariant-checking, dining-philosophers-problem, deadlock, deadlock-detection, petri-net, partial-order-reduction, explicit-state-model-checking]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.1 (deadlock as a terminal state that is not meant to terminate, with the dining philosophers) and Section 3.3 (invariant checking, of which deadlock checking is a case)
  - paper: "Allan Cheng, Javier Esparza and Jens Palsberg, Complexity results for 1-safe nets, Theoretical Computer Science 147, 1995, pages 117 to 136"
    locator: the PSPACE-completeness of deadlock and reachability for 1-safe Petri nets
  - book: "Gerard J. Holzmann, The SPIN Model Checker: Primer and Reference Manual, Addison-Wesley, 2003"
    locator: the checks for invalid end states (deadlocks) during the depth-first search of the state space
  - paper: "Patrice Godefroid, Partial-Order Methods for the Verification of Concurrent Systems, Lecture Notes in Computer Science 1032, Springer, 1996"
    locator: the stubborn and persistent set reductions, which keep every reachable deadlock
---

Deadlock detection asks whether a concurrent system can reach a state in which nothing can move: every process waits for something that will never happen. In the state graph this is a state with no outgoing transition, so the question is a case of the [reachability problem](/reachability-problem/), and a "yes" answer comes with a path that leads into the deadlock. The problem is linear in the size of an explicit state graph, but the graph is exponential in the number of processes, and for programs and [Petri nets](/petri-net/) given succinctly the problem is PSPACE-complete.

## In plain words

Several processes share locks, channels or forks. A deadlock is a moment where each one is waiting for another and none can go on. The classic case is a table of philosophers who each hold their left fork and wait for their right one.

A model checker finds deadlocks by trying every possible order of steps. It starts from the initial state, follows each step that any process can take, and looks for a state where no process can take a step. If it finds one, it prints the sequence of steps that leads there. If the search ends without one, the system is free of deadlock.

The search is simple. The difficulty is that the number of states grows very fast with the number of processes.

## Definition

Let $T = (S, \mathit{Act}, \to, I)$ be a [labelled transition system](/labelled-transition-system/) with a set $I$ of initial states. A state $s$ is **terminal** if it has no outgoing transition. Some terminal states are intended, for example "all processes have finished"; let $E \subseteq S$ be the set of these *valid end states*. A **deadlock** is a terminal state outside $E$.

**Deadlock detection.** Input: $T$ and $E$. Question: is some deadlock reachable from $I$? Output on "yes": a path $s_0 \xrightarrow{a_1} s_1 \cdots \xrightarrow{a_k} s_k$ with $s_0 \in I$ and $s_k$ a deadlock.

The system is **deadlock-free** when the answer is no. Equivalently, the predicate "some transition is enabled, or the state is in $E$" is an [invariant](/invariant-checking/). On a [Kripke structure](/kripke-structure/), where the transition relation must be total, the usual encoding adds a self-loop and a new proposition $\mathit{dead}$ to each terminal state; deadlock freedom is then $\mathsf{AG}\,\neg\mathit{dead}$, or $\mathsf{AG}\,\mathsf{EX}\,\mathit{true}$ before the self-loops are added.

## Variants

- **Explicit, implicit or succinct input.** As for reachability, the system is a listed graph, a program that generates successors, or a parallel composition of processes, a Petri net, or Boolean formulas. A state is terminal when no process and no synchronization has its guard true, which is a local test once the state is known.
- **Partial deadlock.** A subset of the processes is blocked forever while the others keep running. The global state graph has no terminal state, so this is not reachability: it is the liveness property "each process that waits is eventually enabled", checked with [LTL model checking](/ltl-model-checking/) or [fairness](/fairness/).
- **Livelock.** The system runs forever without progress. It is a reachable cycle of non-progress states, so it is a repeated reachability question, not a deadlock question. See [livelock](/livelock/).
- **Runtime detection.** An operating system can detect a deadlock that has already happened, by finding a cycle in the [wait-for graph](/wait-for-graph/) of the current state. That is [deadlock detection](/deadlock-detection/) in the concurrency sense. This page is about the static question: can the system ever get there?

## Examples

**Dining philosophers.** In the [dining philosophers problem](/dining-philosophers-problem/) with $n$ philosophers and $n$ forks, philosopher $i$ thinks, takes fork $i$, takes fork $i + 1 \bmod n$, eats, and puts both forks back. A breadth-first search of the interleaved state graph gives:

| $n$ | reachable states | transitions | deadlocks | shortest path to the deadlock |
|---|---|---|---|---|
| 2 | 6 | 8 | 1 | 2 |
| 3 | 14 | 27 | 1 | 3 |
| 4 | 34 | 88 | 1 | 4 |
| 5 | 82 | 265 | 1 | 5 |

The one deadlock is the state in which each philosopher holds the left fork, and the shortest path to it takes the left forks one at a time, $n$ steps. Now let the last philosopher take fork $0$ first (a global order on the forks). For $n = 2, 3, 4, 5$ the search finds $5, 12, 29, 70$ reachable states and no deadlock. This is the resource-ordering fix, and the search proves it for each fixed $n$.

**A valid end state.** A program in which each process runs to its end has a terminal state where all processes are at their last line. It is in $E$, so it is not a deadlock. SPIN asks the modeller to mark such lines with end labels, for this reason.

## Known algorithms

- **Explicit search.** Run [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/) from $I$, and report the first state that has no successor and is not in $E$. The cost is $O(|S| + |{\to}|)$ time and $O(|S|)$ space, and breadth-first search gives a shortest path to the deadlock. This is the default check of [explicit-state model checkers](/explicit-state-model-checking/) such as SPIN and TLC.
- **Partial-order reduction.** In a system of independent processes, many interleavings lead to the same state. [Partial-order reduction](/partial-order-reduction/) with stubborn or persistent sets explores one representative order and still visits every reachable deadlock (Godefroid 1996). For deadlocks the reduction is simpler than for general properties, because no condition on visible actions is needed.
- **Symbolic search.** [Symbolic reachability](/symbolic-reachability/) computes the reachable set on BDDs and intersects it with the dead states, which are given by the formula $\neg \bigvee_a \mathit{en}_a$.
- **Petri net methods.** For Petri nets, siphons and traps give a sufficient condition for deadlock freedom with linear programming, and unfoldings give a smaller representation of the reachable markings.

## Bounds

**Explicit input.** $\Theta(|S| + |{\to}|)$ time. The problem is NL-complete in space, like directed reachability.

**Succinct input.** For a system given by Boolean formulas, deadlock detection is PSPACE-complete. It is in PSPACE as a case of succinct [reachability](/reachability-problem/), with the dead states as targets. It is PSPACE-hard because reachability reduces to it: given $M$ and a target $T$, add a self-loop to each terminal state of $M$, and remove all outgoing transitions from the states of $T$. Then a deadlock is reachable if and only if $T$ is.

**1-safe Petri nets and parallel programs.** Deadlock detection is PSPACE-complete for 1-safe Petri nets (Cheng, Esparza and Palsberg 1995), and for parallel compositions of finite-state processes. For general Petri nets it is decidable, by a reduction to [Petri net reachability](/petri-net-reachability-decidability/), with a very high complexity.

## Reductions

- **To reachability and invariants.** Deadlock detection is reachability of the set of dead states, and deadlock freedom is the invariant "some transition is enabled or the state is a valid end state" ([invariant checking](/invariant-checking/)). So every algorithm for invariants applies, including [bounded model checking](/bounded-model-checking/) and [IC3/PDR](/ic3-pdr/).
- **From reachability.** The construction in the bounds above reduces reachability to deadlock detection, so the two problems have the same complexity for each form of input.
- **To CTL.** Deadlock freedom is the CTL formula $\mathsf{AG}\,\mathsf{EX}\,\mathit{true}$ on a structure with terminal states, and $\mathsf{AG}\,\neg\mathit{dead}$ on the totalized structure. [CTL model checking](/ctl-model-checking/) decides it in linear time.

## Applications

Deadlock checking is the first check that most model checkers run, because a deadlock is a common error in protocols, lock-based programs and hardware with handshakes, and because a deadlock often hides other errors: a model that stops early satisfies many safety properties trivially. It is also used on workflow nets and on models of distributed algorithms. The [Coffman conditions](/coffman-conditions/) and the [banker's algorithm](/banker-algorithm/) address the same failure at design time and at run time.

## References
