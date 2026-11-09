---
tag: K3M7D5
kind: technique
slug: partial-order-reduction
name: Partial-order reduction
aliases:
- Ample sets
- Persistent sets
- Stubborn sets
- POR
area: logic-and-constraints/model-checking
level: advanced
summary: Explore only some of the enabled transitions in each state, chosen with static dependency information so that one order of independent steps stands for all; it keeps deadlocks and LTL without next.
prereqs: [explicit-state-model-checking, stuttering-equivalence, linear-temporal-logic, depth-first-search]
see_also: [dynamic-partial-order-reduction, sleep-sets, stateless-model-checking, state-explosion-problem, stuttering-equivalence, symmetry-reduction, explicit-state-model-checking, nested-depth-first-search]
sources:
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 10, Partial order reduction (independence and invisibility, the conditions C0 to C3, the DFS version of the cycle condition, and the proof that the reduced structure is stuttering equivalent to the full one)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 8, Partial order reduction (the linear-time ample set approach with the conditions A1 to A4, and its correctness for LTL without next)
  - paper: "Patrice Godefroid, Partial-Order Methods for the Verification of Concurrent Systems, Lecture Notes in Computer Science 1032, Springer, 1996"
    locator: persistent sets and sleep sets, and the preservation of deadlocks
  - paper: "Antti Valmari, Stubborn sets for reduced state space generation, Advances in Petri Nets 1990, Lecture Notes in Computer Science 483, Springer, 1991"
    locator: stubborn sets and the preservation of deadlocks
  - paper: "Doron Peled, Combining partial order reductions with on-the-fly model-checking, Computer Aided Verification (CAV 1994), Lecture Notes in Computer Science 818, Springer, 1994"
    locator: ample sets for LTL without next, and the cycle proviso on the search stack
  - paper: "Doron Peled and Thomas Wilke, Stutter-invariant temporal properties are expressible without the next-time operator, Information Processing Letters 63(5), 1997"
    locator: the converse result, which shows that LTL without next is exactly the stutter-invariant part of LTL
---

Partial-order reduction (POR) makes an [explicit-state](/explicit-state-model-checking/) search of a concurrent system smaller by exploring, in each state, only a subset of the enabled transitions, the *ample set*, instead of all of them. The idea is that independent transitions of different processes, such as two writes to different variables, give the same state in either order, so for most properties one order can stand for all. Four conditions on the ample sets, C0 to C3 in the book of Clarke, Grumberg and Peled, make the reduced state graph [stuttering equivalent](/stuttering-equivalence/) to the full one, so that it satisfies the same formulas of [LTL](/linear-temporal-logic/) without the next operator; C0 and C1 alone already keep every deadlock. The name comes from the view of an execution as a partial order of events, of which each interleaving is one linearization. This page is the *static* method, which computes ample sets from the program text before or during a stateful search; [dynamic partial-order reduction](/dynamic-partial-order-reduction/) finds the dependencies at run time in a stateless search, and [sleep sets](/sleep-sets/) prune transitions instead of states and combine with both.

## In plain words

When two processes do unrelated things, such as each writing its own variable, the order in which they do them does not matter. The end state is the same. But a model checker that tries all orders sees every mixed state on the way, and with many processes the number of mixed states explodes.

Partial-order reduction picks, in each state, one process whose next step cannot interfere with anything the others can still do, and it explores only that step. The other orders are skipped, because they reach the same states in the end and show nothing new to the property. Some care is needed: the chosen step must not change what the property looks at, and no step may be put off forever around a loop.

## When it applies

The system is a set of processes that run by interleaving, given as a state graph whose transitions are labelled with *actions* (transitions) $\alpha$. Each action is deterministic: if $\alpha$ is enabled in $s$, it leads to one state $\alpha(s)$. POR needs:

- an **independence relation**: a symmetric, irreflexive relation $I$ on actions such that, for $(\alpha, \beta) \in I$ and each state $s$ where both are enabled, $\alpha$ does not disable $\beta$ (and the converse), and $\alpha(\beta(s)) = \beta(\alpha(s))$. Actions that are not independent are *dependent*. In practice, steps of different processes are independent when they touch different variables, or only read a common one;
- a notion of **visibility**: an action is *invisible* if it never changes the truth of the atomic propositions that occur in the property;
- a property that cannot tell apart two runs that differ only in the order of independent invisible steps: deadlock freedom, invariants, and LTL without next ($\mathsf{LTL}_{\setminus \mathsf{X}}$), which is exactly the stutter-invariant part of LTL by Peled and Wilke (1997).

It does not apply to properties with the next operator, or to formulas that count steps, and it gains nothing when all steps are dependent, for example when all processes write the same variable.

## The template

The *ample set* $\mathit{ample}(s)$ is a subset of the enabled set $\mathit{enabled}(s)$. The conditions, for every state $s$ of the reduced graph:

- **C0 (emptiness).** $\mathit{ample}(s) = \emptyset$ iff $\mathit{enabled}(s) = \emptyset$.
- **C1 (dependency).** Along every path of the *full* graph that starts in $s$, no action that is dependent with an action of $\mathit{ample}(s)$ can occur before some action of $\mathit{ample}(s)$ occurs.
- **C2 (invisibility).** If $\mathit{ample}(s) \neq \mathit{enabled}(s)$, then every action of $\mathit{ample}(s)$ is invisible.
- **C3 (cycle).** No cycle of the reduced graph contains a state in which an action $\alpha$ is enabled but $\alpha$ is in the ample set of no state of the cycle. In a depth-first search, this follows from the *stack proviso*: if $\mathit{ample}(s) \neq \mathit{enabled}(s)$, then no action of $\mathit{ample}(s)$ leads to a state on the search stack.

C1 says that the actions outside the ample set, and everything they can lead to, are independent of the ample set until an ample action runs; a set with this property is also called *persistent* (Godefroid) and is close to a *stubborn* set (Valmari). The template computes the ample sets during a depth-first search. The holes are in capitals.

```pseudo id=main
REDUCED-DFS(s₀)
L1  Visited ← {s₀};  OnStack ← {s₀}
L2  push (s₀, AMPLE(s₀))
L3  while the stack is not empty do
L4      (s, A) ← top;  if A has no unexplored action then pop, remove s from OnStack, and continue
L5      α ← the next unexplored action of A;  t ← α(s);  if t ∈ Visited then continue
L6      add t to Visited and to OnStack;  push (t, AMPLE(t))

AMPLE(s)
L7  for each process i with an enabled next action α in CANDIDATES(s) do
L8      if VISIBLE(α) then skip i                                  ▷ C2
L9      if α is DEPENDENT with an action that another process can still run (by FUTURE) then skip i   ▷ C1
L10     if PROVISO and α(s) ∈ OnStack then skip i                  ▷ C3
L11     return {α}
L12 return enabled(s)                                              ▷ the full set satisfies C0 to C3
```

The holes:

- **CANDIDATES.** Which subsets to try. This version tries the single next action of each process; richer versions try the set of all enabled actions of one process, or close a set under dependency (stubborn sets).
- **DEPENDENT and FUTURE.** A static over-approximation of dependency, and of the actions that each other process can still execute, for example all instructions reachable in its control-flow graph. A coarser approximation is safe but reduces less.
- **VISIBLE.** The actions that may change a proposition of the property. For deadlock detection, no action is visible.
- **PROVISO.** The stack proviso for C3, or another way to break cycles, such as fully expanding one state on every cycle.

### Example

**Independent counters.** Let $n$ processes each write their own variable $k - 1$ times, with values $1, \ldots, k - 1$. The full state graph is a grid with $k^n$ states: 16 for $n = 2, k = 4$, 27 for $n = 3, k = 3$, and 81 for $n = 4, k = 3$. Every action is independent of every action of the other processes, so with nothing visible AMPLE returns the next action of process 0 until it ends, then of process 1, and so on. The reduced graph is a single path with $n(k - 1) + 1$ states: 7, 7 and 9. The one deadlock, the final state, is kept.

**The ignoring problem.** Process 0 loops forever on a local jump that does not change the state, and process 1 writes $x := 1$ once. The property is "$x = 1$ is never reached", so $x$ is visible. The jump is invisible and independent of everything, so without C3 its singleton set is ample in the initial state, and its successor is the initial state itself. The reduced graph is one state with a self-loop, and the search reports that $x = 1$ is unreachable, which is false. With the stack proviso, the successor is on the stack, AMPLE returns the full set, and the write is explored.

**Visibility.** Two processes write $x := 1$ and $y := 1$, and the property is $\mathsf{G}\, \neg(x = 1 \wedge y = 0)$. The writes are independent, but without C2 the reduction could keep only the order "$y$ first", which never passes through the state $x = 1, y = 0$, and wrongly report that the property holds. C2 forbids a reduced ample set of visible actions, so both orders are kept.

### Why it is correct

**Deadlocks (C0 and C1).** Let $s$ be a state of the reduced graph and $w = \alpha_1 \ldots \alpha_m$ a path of the full graph from $s$ to a deadlock $d$; we show by induction on $m$ that $d$ is in the reduced graph. If $m = 0$ this is clear. Otherwise $\mathit{ample}(s) \neq \emptyset$ by C0. Some $\alpha_j$ is in $\mathit{ample}(s)$: if not, pick $\beta \in \mathit{ample}(s)$; by C1 every $\alpha_j$ is independent of $\beta$, so $\beta$ stays enabled along $w$ and is enabled in $d$, which is not a deadlock. Let $\alpha_j$ be the first ample action of $w$. By C1, $\alpha_1, \ldots, \alpha_{j-1}$ are independent of $\alpha_j$, so $\alpha_j$ is enabled in $s$ and in each state before it, and swapping it to the front, one neighbour at a time, gives a path $\alpha_j\, \alpha_1 \ldots \alpha_{j-1}\, \alpha_{j+1} \ldots \alpha_m$ from $s$ to the same $d$. Its first step leads to $\alpha_j(s)$, which is in the reduced graph, and the rest has length $m - 1$, so the induction applies. This argument does not need C2 or C3, and it holds even when the full graph has cycles.

**LTL without next (C0 to C3).** The theorem of Peled (1994), proved in Chapter 10 of Clarke, Grumberg and Peled and in Chapter 8 of Baier and Katoen: if the ample sets satisfy C0 to C3, every path of the full graph from the initial state is stuttering equivalent to a path of the reduced graph, and the converse is trivial since the reduced graph is a subgraph. As $\mathsf{LTL}_{\setminus \mathsf{X}}$ formulas cannot tell stuttering equivalent paths apart, the two graphs satisfy the same such formulas. The proof builds the reduced path step by step from a full path $\sigma$. In the current state $s$, if the next action of $\sigma$ is in $\mathit{ample}(s)$, keep it. If not, then either some ample action $\beta$ occurs later in $\sigma$, and by C1 it can be moved to the front, or none occurs, and by C1 every later action is independent of an ample action $\beta$, which can be inserted at the front. By C2, $\beta$ is invisible, so in both cases the new path has the same sequence of labels up to stuttering. C3 makes sure that an action of $\sigma$ is not pushed back forever: on a cycle of the reduced graph, every enabled action is ample somewhere on the cycle, so it is taken. The limit of these paths is a reduced path stuttering equivalent to $\sigma$.

### Size and time

The reduced graph is a subgraph of the full one, so it is never larger. The search costs time and space linear in the size of the reduced graph, plus the cost of AMPLE in each state. With the static check of line L9, AMPLE costs $O(p \cdot \ell)$ per candidate for $p$ processes with programs of length $\ell$, because FUTURE can be precomputed per program counter. The gain can be exponential: for $n$ independent processes with $k$ local states each, $k^n$ states become $n(k - 1) + 1$. It can also be zero: when every pair of actions of different processes is dependent, or every action is visible, AMPLE returns the full set everywhere. Tools do not search for a smallest ample set; they use cheap choices such as single processes or stubborn-set closures. POR does not change the worst case of the [state explosion problem](/state-explosion-problem/).

## Classic examples

- **SPIN.** The static POR of Holzmann and Peled (1994) uses ample sets made of the actions of one process, with a static check that they touch only local variables or exclusive channels, and a stack proviso. It is on by default for safety and for LTL without next.
- **Petri net tools.** Stubborn sets of Valmari reduce the reachability graph of a Petri net; they are computed by a closure over the conflict relation of transitions and preserve deadlocks and, with extra conditions, LTL without next.
- **Deadlock detection.** With nothing visible, only C0 and C1 are needed, and the reductions are largest.
- **Software model checkers.** Java PathFinder and similar tools combine a static or partly dynamic POR with state storage, treating accesses to thread-local objects as independent.

## Variations

- **Persistent sets and sleep sets** (Godefroid 1996). Persistent sets are the dependency condition C1 on its own; [sleep sets](/sleep-sets/) remember which transitions were already explored in a sibling branch and skip them, which removes redundant transitions but not states; the two together are the basis of [stateless model checking](/stateless-model-checking/).
- **Dynamic POR** (Flanagan and Godefroid 2005). Compute persistent sets during a stateless search from the races observed on the current execution; see [dynamic partial-order reduction](/dynamic-partial-order-reduction/).
- **Branching time.** For $\mathsf{CTL}^*$ without next, add the condition C4: every ample set is either a single action or the full enabled set. The reduced graph is then branching bisimilar (stuttering bisimilar) to the full one (Gerth, Kuiper, Peled and Penczek).
- **Other cycle conditions.** Instead of the stack proviso, expand fully one state on each cycle, found by a static analysis of the control flow, which also works with breadth-first search, or use conditions based on the visited set that are weaker and work in parallel searches.
- **Symbolic POR.** Alur, Brayton, Henzinger, Qadeer and Rajamani (1997) apply ample sets in BDD-based search; others restrict the transition relation in [bounded model checking](/bounded-model-checking/).
- **With nested depth-first search.** For LTL, the proviso must be checked with care in the inner search; Holzmann, Peled and Yannakakis (1996) showed that the stack proviso can make the inner and outer searches choose different ample sets, and that the inner search should reuse the choices of the outer one; see [nested depth-first search](/nested-depth-first-search/).

## Pitfalls

- **Forgetting C3.** Without a cycle condition, a search can ignore a process forever, as in the example, and report that an error state is unreachable when it is not. This *ignoring problem* is the classic bug of hand-made reductions.
- **Using the next operator.** POR is correct only up to stuttering. A formula with $\mathsf{X}$, such as "after $p$ comes $q$ at the next step", may change its value.
- **Unsound independence.** Two actions that touch the same variable through aliases, or a channel that another process can also read, must be dependent. An independence relation that is too fine makes the reduction miss states.
- **Visible propositions.** The set of visible actions depends on the property. A state predicate added to the property later, for example in a test, must be added to VISIBLE, or C2 is broken.
- **Expecting a reduction on shared-variable code.** When every step touches the same few shared variables, all actions are dependent, and the reduced graph is the full graph.

## Exercises

1. Two processes each run $a := a + 1$ on their own variable twice and then both run $s := s + 1$ on a shared variable $s$. Draw the full state graph, and the reduced graph that REDUCED-DFS builds with $s$ invisible. How many states does each have?
2. Show that in a depth-first search, the stack proviso implies C3: every cycle of the reduced graph contains a fully expanded state.
3. Give a system with two processes and an $\mathsf{LTL}_{\setminus \mathsf{X}}$ formula that the reduced graph satisfies and the full graph does not, when C2 is dropped but C0, C1 and C3 are kept.
4. Show that the sets that AMPLE returns satisfy C1, assuming that DEPENDENT and FUTURE over-approximate the true dependency relation and the true future actions of each process.

## References
