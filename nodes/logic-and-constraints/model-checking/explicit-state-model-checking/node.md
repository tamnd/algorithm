---
tag: WEREAY
kind: technique
slug: explicit-state-model-checking
name: Explicit-state model checking
aliases:
- Enumerative model checking
- explicit model checking
- state enumeration
area: logic-and-constraints/model-checking
level: core
summary: Verify a finite-state system by generating its reachable states one at a time from a successor function, storing each visited state in a hash table, and checking the property during the search.
prereqs: [kripke-structure, depth-first-search, breadth-first-search, hash-table]
see_also: [on-the-fly-model-checking, local-model-checking, symbolic-model-checking, nested-depth-first-search, state-explosion-problem, partial-order-reduction, bitstate-hashing, invariant-checking]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (invariant checking by depth-first search with a counterexample from the stack) and Chapter 4, Section 4.4 (nested depth-first search)
  - book: isbn:9780321228628
    title: Gerard J. Holzmann, The SPIN Model Checker, Primer and Reference Manual, Addison-Wesley, 2003
    locator: Chapter 8, Search algorithms, and Chapter 9, Search optimization (state compression, bitstate hashing, partial-order reduction)
  - book: isbn:9783319105741
    title: Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith and Roderick Bloem (eds.), Handbook of Model Checking, Springer, 2018
    locator: the chapter Explicit-State Model Checking by Gerard J. Holzmann
  - paper: "David L. Dill, Andreas J. Drexler, Alan J. Hu and C. Han Yang, Protocol verification as a hardware design aid, IEEE International Conference on Computer Design (ICCD 1992)"
    locator: the Murphi verifier (breadth-first enumeration of the reachable states)
  - paper: "Yuan Yu, Panagiotis Manolios and Leslie Lamport, Model checking TLA+ specifications, Correct Hardware Design and Verification Methods (CHARME 1999), Lecture Notes in Computer Science 1703, Springer, 1999"
    locator: the TLC model checker (breadth-first search with the state set on disk)
---

Explicit-state model checking verifies a finite-state system by listing its reachable states one at a time. A successor function produces the next states of a state, a [hash table](/hash-table/) records which states were already seen, and a search ([depth-first](/depth-first-search/) or [breadth-first](/breadth-first-search/)) visits each reachable state once while it checks the property. It is the method of SPIN, Murφ, TLC and Java PathFinder. The other main family is [symbolic model checking](/symbolic-model-checking/), which handles sets of states at once as BDDs or formulas.

This page is the general method. [On-the-fly model checking](/on-the-fly-model-checking/) is the mode of running it in which the state space is built during the check and the search stops at the first error; most explicit-state checkers work this way. [Local model checking](/local-model-checking/) is the same idea for branching-time and mu-calculus formulas: it explores only the pairs of states and subformulas that the answer for one state needs.

## In plain words

A program with a few variables and a few threads has a fixed set of possible situations, which we call states. The checker starts from the first state and asks: what can happen next? Each answer is a new state. It writes down each state it has seen in a big table, so that it never looks at the same state twice. It keeps going until no new state appears.

At each state it checks the rule it was given, for example "two threads are never in the critical section at the same time". If a state breaks the rule, the checker prints the steps that led there. That list of steps is a real run of the program that shows the bug. The method is simple and exact. Its limit is memory: the number of states grows very fast with the size of the program.

## When it applies

- The system has finitely many reachable states, or the part that is explored is finite: protocols, concurrent algorithms, controllers, models of hardware, and programs with bounded data.
- A *successor function* is available: from the full value of all variables (the *state vector*), the tool can compute each next state. The model is given in a language such as Promela, Murφ or TLA+, or is the program itself, as in Java PathFinder.
- The property is a state invariant, a deadlock check, an LTL formula (through a [Büchi automaton](/buchi-automaton/)), or a formula of [CTL](/computation-tree-logic/) evaluated over the stored graph.
- The number of reachable states fits in memory after the reductions, roughly up to $10^8$ to $10^9$ states on one machine with exact storage, and more with [bitstate hashing](/bitstate-hashing/). For large data domains with regular structure, symbolic methods often do better; for programs with complex data and pointers, explicit states are easier to represent.

## The template

The template checks a state property $P$ (an invariant). The holes are named in capitals.

```pseudo id=main
EXPLICIT-SEARCH(INIT, NEXT, P)
L1  Visited ← STORE.empty();  W ← ORDER.empty()          ▷ a stack for DFS, a queue for BFS
L2  for each s ∈ INIT do
L3      STORE.insert(Visited, s);  parent[s] ← none;  W.add(s)
L4  while W is not empty do
L5      s ← W.take()
L6      if not P(s) then return the path parent*(s), reversed      ▷ a counterexample
L7      for each t ∈ REDUCE(s, NEXT(s)) do
L8          if not STORE.contains(Visited, t) then
L9              STORE.insert(Visited, t);  parent[t] ← s;  W.add(t)
L10 return "P holds in every reachable state"
```

The holes:

- **INIT and NEXT.** The initial states and the successor function. NEXT interleaves the enabled steps of the processes; each step is one atomic action of one process.
- **ORDER.** A stack gives depth-first search, which uses little memory beyond the table and gives the counterexample directly as the stack. A queue gives breadth-first search, which finds a shortest counterexample for an invariant, at the cost of storing a parent per state.
- **STORE.** An exact hash table of state vectors, a compressed table (collapse compression or minimised automata in SPIN), hash compaction (a short signature per state), or a bit array ([bitstate hashing](/bitstate-hashing/)). The last two can miss states.
- **REDUCE.** All of NEXT, or a subset that is enough for the property: [partial-order reduction](/partial-order-reduction/) keeps one order of independent steps, and [symmetry reduction](/symmetry-reduction/) replaces each state by a canonical representative of its orbit.
- **P.** A state predicate. For an LTL property, the search runs on the product with a Büchi automaton for $\neg\varphi$, and the check of line L6 is replaced by [nested depth-first search](/nested-depth-first-search/) or an SCC search for an accepting cycle.

### Example

Peterson's mutual exclusion algorithm for two processes. Process $i$ has five control locations: idle (0), then $\mathit{flag}_i \gets 1$ (1), then $\mathit{turn} \gets 1 - i$ (2), then wait until $\mathit{flag}_{1-i} = 0$ or $\mathit{turn} = i$ (3), then the critical section (4), then $\mathit{flag}_i \gets 0$ and back to 0. A state is the vector $(pc_0, pc_1, \mathit{flag}_0, \mathit{flag}_1, \mathit{turn})$, so there are $5 \cdot 5 \cdot 2 \cdot 2 \cdot 2 = 200$ vectors, and a breadth-first search reaches 34 of them through 62 transitions. No reachable state has $pc_0 = pc_1 = 4$, so mutual exclusion holds.

Swap the two assignments of each process, so that each one writes $\mathit{turn}$ before its flag. The search now reaches 50 states through 96 transitions, and finds a state with both processes critical. The breadth-first parent pointers give a shortest counterexample of 8 steps:

| Step | Move | $(pc_0, pc_1)$ | $(\mathit{flag}_0, \mathit{flag}_1)$ | turn |
|---|---|---|---|---|
| 0 | start | (0, 0) | (0, 0) | 0 |
| 1 | P0 leaves idle | (1, 0) | (0, 0) | 0 |
| 2 | P0 writes turn ← 1 | (2, 0) | (0, 0) | 1 |
| 3 | P1 leaves idle | (2, 1) | (0, 0) | 1 |
| 4 | P1 writes turn ← 0 | (2, 2) | (0, 0) | 0 |
| 5 | P1 writes flag₁ ← 1 | (2, 3) | (0, 1) | 0 |
| 6 | P1 sees flag₀ = 0 and enters | (2, 4) | (0, 1) | 0 |
| 7 | P0 writes flag₀ ← 1 | (3, 4) | (1, 1) | 0 |
| 8 | P0 sees turn = 0 and enters | (4, 4) | (1, 1) | 0 |

### Why it is correct

With an exact STORE and REDUCE equal to NEXT, the loop is graph search. Each state that enters $W$ is reachable, because its parent chain leads back to an initial state through transitions; so a returned path is a real run that ends in a state that violates $P$. Each reachable state enters $W$: if $s_0 s_1 \ldots s_k$ is a path from an initial state, then by induction on $i$ each $s_i$ is inserted, since $s_{i-1}$ is taken from $W$ at some point and line L7 looks at all its successors. So if no reachable state violates $P$, the search ends at line L10. With a reduced REDUCE, correctness is the theorem of the reduction (for example the conditions C0 to C3 of partial-order reduction). With a lossy STORE, an error report is still a real run, but "holds" is only probable.

### Size and time

The search takes $O(|S| + |R|)$ steps, where $|S|$ and $|R|$ count the reachable states and transitions, times the cost of one call of NEXT, one hash, and one comparison of state vectors. The memory is $|S|$ times the size of a stored state, plus the work list. For an invariant, BFS finds a shortest counterexample (in the number of transitions); DFS finds one quickly but it can be long. For LTL the time is $O(|M| \cdot 2^{O(|\varphi|)})$, as in [LTL model checking](/ltl-model-checking/). The number of reachable states is usually the limit: it grows exponentially with the number of processes and variables; see the [state explosion problem](/state-explosion-problem/).

## Classic examples

- **SPIN** (Holzmann). Promela models, depth-first search, LTL through Büchi automata and [nested depth-first search](/nested-depth-first-search/), [partial-order reduction](/partial-order-reduction/), collapse compression and [bitstate hashing](/bitstate-hashing/). Used for protocols and for flight software.
- **Murφ** (Dill and others, 1992). Breadth-first search for invariants and deadlocks, [symmetry reduction](/symmetry-reduction/) through scalarsets, and hash compaction. Used for cache coherence protocols.
- **TLC** (Yu, Manolios and Lamport, 1999). Breadth-first search over TLA+ specifications, with the state set on disk, so that the number of states is limited by disk space rather than memory.
- **Java PathFinder.** The states are states of a Java virtual machine, and NEXT runs the byte code of one thread up to the next scheduling point.
- **[Stateless model checking](/stateless-model-checking/).** The other extreme: the store is empty, and the search reruns the program for each schedule, as in VeriSoft and CHESS.

## Variations

- **Breadth-first versus depth-first.** BFS for shortest counterexamples to invariants, and for disk-based and parallel search, where layers can be processed in bulk. DFS for LTL, because the nested search needs depth-first post-order, and for small memory use beyond the store.
- **Disk-based and distributed search.** Partition the state space by a hash of the state across machines, or keep the visited set on disk and remove duplicates layer by layer.
- **Directed (heuristic) search.** Use A* or best-first search with a distance estimate to the error, to find short counterexamples quickly.
- **Lossy storage.** Hash compaction stores a $b$-bit signature of each state; bitstate hashing stores only $k$ bits in a shared array. Both give large coverage with little memory at the risk of missing states.
- **With reductions.** Partial-order reduction, symmetry reduction, and abstraction of data, each with its own correctness condition.

## Pitfalls

- **Hashing the state badly.** Two equal states must have equal vectors: padding bytes, pointers, and unused variables that still hold old values make equal states look different, so the search explodes.
- **Counting atomic steps too fine.** Each extra interleaving point multiplies the states. Group local computation into atomic steps where the semantics allows it, and do not split one statement into steps that no other process can observe.
- **Deadlock versus end state.** A state with no successor is a deadlock unless it is a valid end state. Mark the valid end states, or the check reports false deadlocks.
- **Trusting "no error" from a lossy run.** With bitstate hashing or a depth bound, a clean run proves nothing; report the coverage.
- **Long counterexamples.** A DFS trace can be thousands of steps long. Shorten it with a breadth-first search to the error state, or with an iterative search for shorter traces; see [shortest counterexample](/shortest-counterexample/).
- **Liveness without fairness.** Many liveness properties fail only because one process is never scheduled. State the fairness assumption, or most counterexamples are not interesting.

## Exercises

1. In the correct Peterson example, which of the $200$ state vectors are unreachable because of the order of the two writes? Give one unreachable vector with $pc_0 = pc_1 = 3$ and justify it.
2. Show that breadth-first EXPLICIT-SEARCH returns a counterexample with the least number of transitions among all paths to a state that violates $P$.
3. A model has $10^8$ reachable states of 120 bytes each. Estimate the memory of an exact hash table, and of a bitstate table with $k = 3$ hash functions and a probability of a missed state under $1\%$ by the bound on the [bitstate hashing](/bitstate-hashing/) page.

## References
