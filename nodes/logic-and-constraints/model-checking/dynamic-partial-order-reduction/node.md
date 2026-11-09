---
tag: EKPZ7C
kind: algorithm
slug: dynamic-partial-order-reduction
name: Dynamic partial-order reduction
aliases:
- DPOR
- Flanagan-Godefroid algorithm
area: logic-and-constraints/model-checking
level: research
summary: Explore the interleavings of a concurrent program without storing states, and add a branch only where the current run shows two dependent steps of different threads that could run in the other order.
solves: [deadlock-freedom-checking, invariant-checking]
model: word-ram
complexity:
  vars: {d: the length of the longest execution, n: the number of threads, t: the number of maximal executions explored}
  time: {worst: O(t d^2 (d + n))}
  space: {extra: O(d^2 + n d)}
properties: {deterministic: true, recursive: true, stateless: true, on_the_fly: true}
history:
  year: 2005
  people: [Cormac Flanagan, Patrice Godefroid]
  note: Flanagan and Godefroid presented DPOR at POPL 2005, to replace the static dependency analysis of partial-order reduction in stateless search by races observed at run time.
prereqs: [partial-order-reduction, stateless-model-checking, depth-first-search]
see_also: [partial-order-reduction, sleep-sets, stateless-model-checking, state-explosion-problem, vector-clocks, race-condition, explicit-state-model-checking, deadlock-freedom-checking]
sources:
  - paper: "Cormac Flanagan and Patrice Godefroid, Dynamic partial-order reduction for model checking software, 32nd ACM Symposium on Principles of Programming Languages (POPL 2005), ACM, 2005"
    locator: the algorithm with backtrack sets and a happens-before relation computed with clock vectors, its correctness theorem for acyclic state spaces, and the combination with sleep sets
  - paper: "Patrice Godefroid, Partial-Order Methods for the Verification of Concurrent Systems, Lecture Notes in Computer Science 1032, Springer, 1996"
    locator: persistent sets, sleep sets, and the theorem that a selective search with persistent sets reaches every deadlock of an acyclic state space
  - paper: "Parosh Aziz Abdulla, Stavros Aronis, Bengt Jonsson and Konstantinos Sagonas, Optimal dynamic partial order reduction, 41st ACM Symposium on Principles of Programming Languages (POPL 2014), ACM, 2014"
    locator: source sets, wakeup trees, and the optimal algorithm that explores exactly one execution per Mazurkiewicz trace
  - paper: "Yu Yang, Xiaofang Chen, Ganesh Gopalakrishnan and Robert M. Kirby, Efficient stateful dynamic partial order reduction, SPIN 2008, Lecture Notes in Computer Science 5156, Springer, 2008"
    locator: the combination of DPOR with state storage
---

Dynamic partial-order reduction (DPOR) is an algorithm for [stateless model checking](/stateless-model-checking/) of concurrent programs: it explores the executions of the program one at a time by depth-first search, and it uses the steps it actually observes to decide where other interleavings must be tried. Two steps of different threads that touch the same variable or lock, at least one of them as a write, form a *race* if neither is forced to come first; when the current execution contains a race, DPOR adds a branch that runs the later thread earlier, and nowhere else. Flanagan and Godefroid (2005) proved that for programs whose executions are finite, this explores a persistent set in each visited state, so it finds every deadlock and every final state, and one execution of every [Mazurkiewicz trace](/partial-order-reduction/) of complete executions. The static version, [partial-order reduction](/partial-order-reduction/), has to guess the dependencies before the search, while DPOR sees them.

## In plain words

Two threads that never touch the same data can run in any order, and the result is the same. Trying every order of their steps is wasted work, and with many threads the number of orders is huge. The useful orders differ only where two threads touch the same thing.

DPOR runs the program once, in some order, and watches. When it sees two steps of different threads that touch the same variable, and nothing forced the first to come first, it notes: "next time, try the other thread at that earlier point". Then it backs up and tries the noted alternatives, and notes new ones as it goes. Independent threads produce no notes, so they cost one run instead of thousands. It keeps no table of visited states, only the current run.

## The problem

The input is a concurrent program: a fixed set of threads that run steps on shared variables and locks, with the restriction that every execution is finite (the state space is acyclic). In a state $s$, each thread $p$ has at most one *next step* $\mathit{next}(s, p)$, which may be enabled or blocked, for example by a lock that another thread holds. Two steps are *dependent* if they belong to the same thread, or if they access the same variable or lock and at least one of them writes it (a lock or unlock counts as a write of the lock). Steps that are not dependent are *independent*: in this model they commute and do not enable or disable each other.

Two executions are equivalent, the same *Mazurkiewicz trace*, if one can be turned into the other by swapping adjacent independent steps; equivalent executions end in the same state. The goal is to visit all final states, including deadlocks, and to check an assertion or a safety property in every reachable final state, while exploring as few executions as possible, ideally one per trace.

## The algorithm

The search keeps the current execution $E = e_1 e_2 \ldots e_k$, the state $\mathit{pre}(E, i)$ before each step $e_i$, and for each prefix two sets of threads: $\mathit{backtrack}$, the threads that must be tried there, and $\mathit{done}$, those tried. The *happens-before* relation $\to_E$ on the steps of $E$ is the transitive closure of "$e_i$ and $e_j$ are dependent and $i < j$". A step $e_i$ happens before thread $p$, written $i \to_E p$, if $e_i$ is a step of $p$ or $e_i \to_E e_j$ for some step $e_j$ of $p$.

```pseudo id=main
EXPLORE(E)                                        ▷ s = the last state of E
L1  for each thread p that has a next step n = next(s, p) do
L2      let i be the largest index such that e_i and n are dependent, e_i is not a step of p, and not i →_E p
L3      if such an i exists then E_i ← the threads enabled in pre(E, i)
L4          if p ∈ E_i then add p to backtrack(pre(E, i))
L5          else add all of E_i to backtrack(pre(E, i))
        if no thread is enabled in s then record s as a final state and return
L6  backtrack(s) ← {some thread enabled in s};  done(s) ← ∅
L7  while backtrack(s) ≠ done(s) do
L8      pick p ∈ backtrack(s) ∖ done(s) and add p to done(s)
L9      EXPLORE(E · next(s, p))
```

Line L2 finds the last *race* of the next step of $p$ with the current execution: an earlier step of another thread that conflicts with it and that the steps in between do not force to come first. To reverse it, $p$ must start running at the state before $e_i$ (line L4). If $p$ is not enabled there, the algorithm does not know which thread would let $p$ proceed, and it adds every enabled thread (line L5). The happens-before relation is usually computed with [vector clocks](/vector-clocks/), one per step and per thread.

## Example

Thread 0 runs $x := 1;\ y := 1$ and thread 1 runs $z := 1;\ r := x$. The only dependent pair of different threads is $x := 1$ and $r := x$, so there are 2 traces and 2 final states ($r = 1$ and $r = 0$), out of $\binom{4}{2} = 6$ executions. DPOR, which tries the smallest thread first:

| Run | Order of threads | Race seen by line L2 | Effect |
|---|---|---|---|
| 1 | 0 0 1 1 | $x := 1$ (step 1) and $r := x$ | thread 1 is enabled in the initial state: add 1 to its backtrack set |
| 2 | 1 0 0 1 | $x := 1$ (step 2) and $r := x$ | thread 1 is enabled after $z := 1$: add 1 to the backtrack set there |
| 3 | 1 1 0 0 | $r := x$ and $x := 1$ | thread 0 is already in done after $z := 1$ |

Runs 1 and 2 are the same trace: in both, $x := 1$ comes before $r := x$. The redundancy comes from line L4, which can only add *thread* 1 at the initial state, and its first step there is $z := 1$, not the read. Adding [sleep sets](/sleep-sets/) removes run 2: after run 1, thread 0 is asleep in the branch that starts with $z := 1$, since $x := 1$ was already explored and is independent of $z := 1$, so the search must run $r := x$ next.

With 4 threads that each write 2 private variables, all steps are independent, no race is ever seen, and DPOR explores 1 execution out of $8! / (2!)^4 = 2520$. With $n$ threads that each write the same variable once, every order is a different trace, and DPOR explores all $n!$ executions, which is necessary; there are $n$ final states.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md); part of it is a sketch of the argument of Flanagan and Godefroid. Every explored execution is a real execution of the program, so every reported final state and assertion failure is real. For completeness, the key fact is that when EXPLORE leaves a state $s$, the set $\mathit{done}(s)$ is a *persistent set* in $s$: no sequence of steps from $s$ that avoids the threads in $\mathit{done}(s)$ contains a step that is dependent with the next step of one of those threads. Flanagan and Godefroid prove this by taking a smallest counterexample and showing that the race of line L2 would have added the missing thread. A selective search with persistent sets in an acyclic state space meets every Mazurkiewicz trace of maximal executions, by moving the first step of a persistent thread to the front of any execution; this part is proved in full.

## Complexity

The search keeps only the current execution, of length at most $d$, with a happens-before set or a vector clock per step, and the two sets per prefix: $O(d^2 + n d)$ space. Each explored step costs $O(d)$ per thread at line L2 and $O(d^2)$ to update the happens-before sets as written in the reference code; with vector clocks the per-step work is $O(n d)$. The number $t$ of explored maximal executions lies between the number of traces of maximal executions and the number of all maximal executions, so the total time is $O(t d^2 (d + n))$ in the simple version. On programs with little sharing $t$ is close to the number of traces, which can be exponentially smaller than the number of executions; in the worst case, when every pair of steps conflicts, the two are equal and no reduction is possible, in line with the [state explosion problem](/state-explosion-problem/).

## Properties

- **Stateless.** No set of visited states is kept, so memory stays small, and the program can be run for real, as in VeriSoft and later tools, instead of being modelled.
- **Sound and complete for final states** of acyclic programs: every deadlock and every final state, and every assertion that depends only on the trace, is reached.
- **Not optimal.** It can explore several executions of the same trace, as the example shows; sleep sets remove many of them, and Optimal DPOR removes all.
- **Precise dependencies.** It uses the addresses actually accessed, so two writes to $a[i]$ and $a[j]$ with $i \neq j$ are independent, which a static analysis may not know.
- **Needs termination.** On a program with an infinite execution the depth-first search does not end; tools bound the depth or the number of preemptions.

## Variants and improvements

- **DPOR with sleep sets.** Flanagan and Godefroid already combine the two; sleep sets block the threads whose step was explored in a sibling branch and has not been disturbed since, and they remove most redundant runs.
- **Optimal DPOR** (Abdulla, Aronis, Jonsson and Sagonas 2014). Backtrack sets are replaced by *source sets*, which are smaller than persistent sets, and *wakeup trees* record the exact sequence that reverses a race. It explores exactly one execution per Mazurkiewicz trace of maximal executions, and its source-set version without wakeup trees is already much closer to this than plain DPOR. It is implemented in Nidhugg and Concuerror.
- **Stateful DPOR** (Yang, Chen, Gopalakrishnan and Kirby 2008). Combine DPOR with a table of visited states, with extra care because a state reached earlier may have an incomplete backtrack set.
- **Weak memory and other equivalences.** Tools such as CDSChecker and GenMC adapt the idea to C11 and other weak memory models, and some algorithms use a coarser equivalence than Mazurkiewicz traces, such as reads-from equivalence, so that two executions where each read sees the same write count as one.
- **Bounded search.** Preemption bounding, the bound used by the CHESS tool, limits the number of times a thread is interrupted; Coons, Musuvathi and McKinley (2013) showed how to combine such a bound with DPOR without losing the executions inside the bound.

## When to use it

Use DPOR to test or verify a concurrent program with a small number of threads and terminating executions, where the state is too large or too hard to store: unit tests of concurrent data structures, Erlang or C programs, and models of distributed protocols with message passing. It needs a way to run the program under a controlled scheduler and to observe each access to shared data. For finite-state models with cycles, use stateful [partial-order reduction](/partial-order-reduction/) inside an [explicit-state model checker](/explicit-state-model-checking/) instead; for liveness properties neither plain DPOR nor stateless search is enough.

## Pitfalls

- **Missing dependencies.** Every shared access must be visible to the scheduler. A shared variable that the instrumentation misses makes two dependent steps look independent, and DPOR then misses executions without any warning.
- **Wrong happens-before.** The relation must be computed on the current execution only, and be recomputed when the search backs up; reusing clocks of an abandoned branch gives wrong races.
- **Lock steps.** A blocked lock is not enabled, so line L5 adds all enabled threads; treating it as line L4 loses the executions where the lock owner releases first.
- **Cycles and non-termination.** The guarantee is for acyclic state spaces. A spin loop that waits for another thread produces an infinite execution and an endless search.
- **Expecting one run per trace.** Plain DPOR may run the same trace more than once; counting runs is not counting traces.

## Implementations

## History

Godefroid's VeriSoft (1997) explored the executions of real C programs without storing states, using static [partial-order reduction](/partial-order-reduction/) with persistent and [sleep sets](/sleep-sets/). Static dependency information was too coarse for programs with pointers and arrays, which motivated Flanagan and Godefroid (2005) to compute the dependencies during the search. Since then DPOR has been the core of most stateless model checkers. Abdulla, Aronis, Jonsson and Sagonas (2014) made it optimal with source sets and wakeup trees, and later work adapted it to weak memory models, to message passing, and to coarser equivalences between executions.

## References
