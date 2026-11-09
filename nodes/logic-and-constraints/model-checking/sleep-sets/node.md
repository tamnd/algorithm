---
tag: DD26ZR
kind: technique
slug: sleep-sets
name: Sleep sets
aliases:
- Sleep set reduction
- Godefroid sleep sets
area: logic-and-constraints/model-checking
level: advanced
summary: In a search of interleavings, carry along the transitions that an earlier branch already explored and that nothing since has disturbed, and skip them, so that equivalent orders are not explored twice.
prereqs: [partial-order-reduction, depth-first-search]
see_also: [partial-order-reduction, dynamic-partial-order-reduction, stateless-model-checking, state-explosion-problem, explicit-state-model-checking, race-condition]
sources:
  - paper: "Patrice Godefroid, Partial-Order Methods for the Verification of Concurrent Systems, Lecture Notes in Computer Science 1032, Springer, 1996"
    locator: the chapter on sleep sets (the sleep set algorithm, the result that sleep sets alone reduce transitions but not states, and the combination with persistent sets)
  - paper: "Patrice Godefroid and Pierre Wolper, Using partial orders for the efficient verification of deadlock freedom and safety properties, Computer Aided Verification (CAV 1991), Lecture Notes in Computer Science 575, Springer, 1992"
    locator: the first presentation of sleep sets together with persistent sets
  - paper: "Cormac Flanagan and Patrice Godefroid, Dynamic partial-order reduction for model checking software, 32nd ACM Symposium on Principles of Programming Languages (POPL 2005), ACM, 2005"
    locator: the combination of sleep sets with dynamic partial-order reduction in a stateless search
  - paper: "Parosh Aziz Abdulla, Stavros Aronis, Bengt Jonsson and Konstantinos Sagonas, Optimal dynamic partial order reduction, 41st ACM Symposium on Principles of Programming Languages (POPL 2014), ACM, 2014"
    locator: sleep-set blocked executions, and wakeup trees that avoid them
---

Sleep sets are a reduction for searches over the interleavings of a concurrent system, proposed by Godefroid (with Wolper, 1991). Each node of the search carries a *sleep set*: the transitions that were already explored from an ancestor or an earlier sibling, and that have stayed independent of everything executed since. A transition in the sleep set is not taken, because any execution that starts with it here is equivalent to one already explored. A transition leaves the sleep set as soon as a dependent transition is executed. Unlike [partial-order reduction](/partial-order-reduction/) with ample or persistent sets, which cuts states, sleep sets cut *transitions*: alone, in a stateful search, they still visit every reachable state. In a stateless search they explore at most one execution per Mazurkiewicz trace, which is why every [stateless model checker](/stateless-model-checking/) and [dynamic partial-order reduction](/dynamic-partial-order-reduction/) uses them.

## In plain words

Say a search has tried "thread A writes $x$" first, and now tries "thread B writes $y$" instead. A and B touch different data, so in this second branch, doing A next would only give an order already seen: B then A ends where A then B ended. So A is put to sleep in the B branch. It stays asleep while the steps taken do not touch what A touches. If some step does, for example a read of $x$, A wakes up, because now the order really matters.

The search never takes a sleeping step. This removes repeated work without any analysis of the program text. It only needs to know, for two steps, whether they can interfere.

## When it applies

The setting is that of [partial-order reduction](/partial-order-reduction/): processes or threads that interleave, deterministic transitions, and an independence relation such that two independent transitions enabled in a state do not disable each other and commute. Sleep sets are correct for properties of final states and deadlocks, for assertions that depend only on the trace of an execution, and, with care, for safety properties of states. They are most useful:

- in a **stateless** search, where no table catches repeated states, and every redundant execution costs a full run of the program;
- **together with persistent sets**, static or dynamic, which choose which transitions to explore, while sleep sets remove redundant orders among them.

## The template

The search is a depth-first search. In the stateful version a table $\mathit{asleep}[s]$ records the transitions that were asleep at every visit of $s$ so far, and were therefore never taken from $s$. The holes are in capitals.

```pseudo id=main
SLEEP-SET-SEARCH(s₀)
L1  ENTER(s₀, ∅)
    while the stack is not empty do
        (s, Z, todo) ← top;  if todo is empty then pop and continue
L6      t ← the next transition of todo, in ORDER, removed from todo
L7      s' ← t(s)
L8      Z' ← {u ∈ Z : u and t are INDEPENDENT in s}
L9      Z ← Z ∪ {t}                          ▷ later siblings will not take t first
L10     ENTER(s', Z')

ENTER(s, Z)
    if s is in STORE then
L2      todo ← asleep[s] ∖ Z                 ▷ transitions asleep before, awake now
L3      asleep[s] ← asleep[s] ∩ Z
    else
L4      todo ← SELECT(s) ∖ Z
L5      asleep[s] ← SELECT(s) ∩ Z;  add s to STORE
    push (s, Z, todo)
```

The holes:

- **SELECT.** The transitions to consider in a state: all enabled ones for sleep sets alone, or a persistent set for the combined method.
- **INDEPENDENT.** The independence relation, for example "different threads, and no common variable or lock written by one of them".
- **ORDER.** The order in which the transitions of a state are tried. It changes which execution of each trace is explored, not how many.
- **STORE.** A table of visited states, or nothing. In a stateless search, ENTER always takes the second branch and nothing is stored.

### Example

Thread 0 runs $x := 1;\ y := 1$ and thread 1 runs $z := 1;\ r := x$. The only dependent pair is $x := 1$ and $r := x$. The full state graph has 11 states, 13 transitions and 2 final states ($r = 1$ and $r = 0$), and there are $\binom{4}{2} = 6$ maximal executions in 2 traces.

The stateless search, which tries thread 0 first:

1. It runs $0\,0\,1\,1$, the first execution. Back at the state after $x := 1$, thread 0 ($y := 1$) is now asleep for the sibling branch that starts with $z := 1$.
2. In that branch, $y := 1$ stays asleep after $z := 1$ and after $r := x$, since both are independent of it. After $x := 1, z := 1, r := x$, the only enabled transition is asleep, so the branch is *blocked*: it would have produced $0\,1\,1\,0$, which is the same trace as $0\,0\,1\,1$.
3. Back at the initial state, thread 0 ($x := 1$) is asleep in the branch that starts with $z := 1$. So after $z := 1$ the search must take $r := x$, which reads $x = 0$ and wakes thread 0 up, since it is dependent. It runs $1\,1\,0\,0$, the second execution.

The search explores 2 executions, one per trace, and 1 blocked branch, instead of 6 executions. The stateful version visits all 11 states but takes 10 transitions instead of 13. By contrast, plain [dynamic partial-order reduction](/dynamic-partial-order-reduction/) without sleep sets explores 3 executions on this program, two of them in the same trace.

### Why it is correct

Two maximal executions are *equivalent*, the same Mazurkiewicz trace, if one can be obtained from the other by swapping adjacent independent transitions; equivalent executions end in the same state. We say that a maximal execution $w$ from $s$ *can start with* $u$ if $w$ is equivalent to an execution whose first transition is $u$. The proofs below are for the stateless search with SELECT equal to all enabled transitions, on an acyclic state space, so that all executions are finite.

**Every trace is explored.** Claim: if the search enters $s$ with sleep set $Z$, then for each maximal execution $w$ from $s$ that cannot start with any member of $Z$, the search explores from this node a maximal execution equivalent to $w$. By induction on the length of $w$. If $w$ is empty, $s$ is final and is recorded. Otherwise, the transitions that $w$ can start with are enabled in $s$ and not in $Z$, so they are in todo; let $p$ be the first of them in the order of the search. Then $w$ is equivalent to $p\, w'$. When $p$ is taken, the new sleep set is $Z' = \{u \in Z \cup E : u \text{ independent of } p\}$, where $E$ holds the siblings tried before $p$. If $w'$ could start with some $u \in Z'$, then, as $u$ is independent of $p$, $w$ could start with $u$ too; this is false for $u \in Z$ by the hypothesis, and false for $u \in E$ by the choice of $p$ as the first possible start. So the induction hypothesis applies to $w'$ from $p(s)$. At the root, $Z = \emptyset$, so every trace of maximal executions is explored.

**No trace is explored twice.** Suppose the search explores two different equivalent maximal executions from the same node. Take the node where they part, with the branch of $u$ explored before the branch of $v$. Then $u$ is in the sleep set of the branch of $v$. As the two executions are equivalent, the execution in the $v$ branch can start with $u$, so every transition before the step of $u$ in it is independent of $u$. By line L8, $u$ stays in the sleep set along this execution until the moment it would be taken, and asleep transitions are never taken. This is a contradiction.

**States.** With the re-visit rule of lines L2 and L3, the stateful search with sleep sets alone visits every reachable state (Godefroid 1996): when a state is reached again with a smaller sleep set, the transitions that are now awake are taken. So sleep sets alone keep every state and every deadlock, and they save transitions. Combined with persistent sets, deadlocks are kept by the persistent-set argument on the [partial-order reduction](/partial-order-reduction/) page.

### Size and time

Sleep sets cost $O(n)$ space per node of the search for $n$ threads, and line L8 costs $O(n)$ independence tests per transition. In a stateless search the number of explored maximal executions equals the number of traces of maximal executions, which can be exponentially smaller than the number of executions: for $n$ threads with $k$ private steps each, $(nk)! / (k!)^n$ executions form one trace. But the search can also enter *sleep-set blocked* branches, which end in a state where every enabled transition is asleep; they produce no execution, and on some programs their number is exponential. In a stateful search the number of states is not reduced at all.

## Classic examples

- **VeriSoft** (Godefroid 1997) ran C programs under a controlled scheduler with persistent sets and sleep sets, without storing states.
- **DPOR with sleep sets** (Flanagan and Godefroid 2005), the standard form of [dynamic partial-order reduction](/dynamic-partial-order-reduction/); in benchmarks most of the redundancy of DPOR goes away.
- **Optimal DPOR** (Abdulla, Aronis, Jonsson and Sagonas 2014) keeps sleep sets and adds *wakeup trees*, which prescribe how to reverse each race and so avoid the blocked branches; it explores exactly one execution per trace and no blocked branch.
- **State-space caching.** Godefroid, Holzmann and Pirottin (1992) used sleep sets in a search that stores only part of the visited states; by removing most of the repeated visits, sleep sets made such caching practical.

## Variations

- **Sleep sets with persistent sets.** Take SELECT as a persistent set. The persistent set reduces the states, the sleep sets reduce the transitions between them; the combination keeps deadlocks.
- **Stateful sleep sets.** With a table of visited states, a state visited again with a sleep set that is not a superset of the stored one must be explored again for the newly awake transitions (lines L2 and L3); ignoring this loses states.
- **Sleep sets with state caching.** When only part of the states are stored, the stored sleep set gives the transitions that a revisit must still take.
- **Wakeup trees and source sets.** The optimal version of DPOR, where the sleep set is used together with a tree of sequences to run, so that no blocked branch is started.
- **Coarser equivalences.** For weak memory models and for reads-from equivalence, the role of the sleep set is taken by more general records of what has already been explored.

## Pitfalls

- **Expecting fewer states.** With a state table, sleep sets alone visit every reachable state; the saving is in transitions, and it shows as time, not memory.
- **Forgetting to wake.** Line L8 must remove every sleeping transition that is dependent with the transition taken. Keeping one that should wake loses traces.
- **Revisits in the stateful version.** Treating a revisited state as done, without lines L2 and L3, loses the transitions that were asleep at the first visit but are awake now, and with them states.
- **Thread versus step.** A sleeping entry stands for the next step of a thread. If the thread moves, its next step changes; this cannot happen while it sleeps, since a step of the same thread is dependent, but an implementation that names entries by thread must keep this in mind.
- **Blocked branches.** A sleep-set blocked branch is not an error and must not be reported as a deadlock: some transition is enabled, it is only asleep.

## Exercises

1. In the example, list the 6 maximal executions and group them into the 2 traces. Which one does the blocked branch correspond to?
2. Show that a sleep-set blocked branch cannot lead to a trace that the search would otherwise miss: every maximal execution that extends it is equivalent to one explored elsewhere.
3. Show that if line L8 is replaced by $Z' \leftarrow \emptyset$, the search explores every maximal execution, and if it is replaced by $Z' \leftarrow Z$, it can miss a trace.
4. For $n$ threads that each write their own variable once, how many maximal executions, traces, and blocked branches does the stateless search with sleep sets explore?

## References
