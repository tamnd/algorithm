---
tag: 30CAP0
kind: technique
slug: on-the-fly-model-checking
name: On-the-fly model checking
aliases:
- On-the-fly verification
area: logic-and-constraints/model-checking
level: advanced
summary: Generate the product of the system and the property automaton only as the search needs it, and stop at the first violation, so that an error can be found before the state space is built.
prereqs: [explicit-state-model-checking, automata-theoretic-approach, depth-first-search]
see_also: [explicit-state-model-checking, local-model-checking, nested-depth-first-search, ltl-to-buchi-translation, partial-order-reduction, state-explosion-problem, shortest-counterexample, counterexample-generation]
sources:
  - paper: doi:10.1007/BF00121128
    title: Costas Courcoubetis, Moshe Y. Vardi, Pierre Wolper and Mihalis Yannakakis, Memory-efficient algorithms for the verification of temporal properties, Formal Methods in System Design 1(2/3), 1992
    locator: the nested depth-first search, which needs only the successors of visited states and so runs on the fly
  - paper: "Rob Gerth, Doron Peled, Moshe Y. Vardi and Pierre Wolper, Simple on-the-fly automatic verification of linear temporal logic, Protocol Specification, Testing and Verification XV (PSTV 1995), Chapman and Hall, 1995"
    locator: the translation of LTL into a Büchi automaton whose nodes are expanded on demand during the search
  - paper: "Doron Peled, Combining partial order reductions with on-the-fly model-checking, Computer Aided Verification (CAV 1994), Lecture Notes in Computer Science 818, Springer, 1994"
    locator: the conditions under which partial-order reduction and an on-the-fly LTL search can be combined
  - paper: "Jean-Michel Couvreur, On-the-fly verification of linear temporal logic, FM'99, Lecture Notes in Computer Science 1708, Springer, 1999"
    locator: an on-the-fly emptiness check for generalized Büchi automata based on strongly connected components
  - book: isbn:9780321228628
    title: Gerard J. Holzmann, The SPIN Model Checker, Primer and Reference Manual, Addison-Wesley, 2003
    locator: Chapter 8, Search algorithms (the depth-first search of the product with a never claim, built during the search)
---

On-the-fly model checking interleaves the construction of the state space with the check of the property. The search asks the model for the successors of a state only when it reaches that state, it forms the product with the property automaton in the same way, and it stops as soon as it finds a violation. A system with an error near its initial states is then refuted after a tiny part of its states has been built, while a correct system costs the same as a full search. The technique needs a search that uses only the successors of states it has already seen, such as [depth-first search](/depth-first-search/) for invariants and [nested depth-first search](/nested-depth-first-search/) for LTL.

## In plain words

A simple checker works in two stages. First it builds the full map of every state the system can reach. Then it looks for a bad path on the map. If the map is too large, the checker runs out of memory in the first stage and never gets to look.

An on-the-fly checker builds the map and looks at the same time. It takes one step, asks the system what can happen next, checks the new state at once, and goes on. As soon as it sees a bad path, it stops and reports it. Bugs are often a few steps from the start, so the checker can find them after building only a little of the map. If there is no bug, it must still build the whole map, as the simple checker does.

## When it applies

- The system is given by a *successor function*: a program, or a model in a language such as Promela, from which the next states of a state can be computed. There is no need to have the state graph in advance.
- The property is checked by a search that moves only forward, from a state to its successors: [reachability](/reachability-problem/) of a bad state, an [invariant](/invariant-checking/), a [deadlock](/deadlock-freedom-checking/), or an accepting cycle in the product with a [Büchi automaton](/buchi-automaton/) for an LTL formula.
- The goal is to find errors. The gain over a global method shows only when the property fails.

It does not apply to algorithms that need the predecessors of a state or the whole graph at once, such as the backward labelling of [CTL model checking](/ctl-model-checking/) or a backward fixed point in [symbolic model checking](/symbolic-model-checking/). For branching-time logics, the analogue is [local model checking](/local-model-checking/), which explores only the part of the graph that the formula needs at a given state.

## The template

The holes are in capitals.

```pseudo id=main
ON-THE-FLY(INIT_M, INIT_B, SEARCH)
L1  Visited ← STORE.empty()
L2  for each s ∈ INIT_M and each q ∈ INIT_B do
L3      r ← SEARCH((s, q), SUCC, Visited)        ▷ reads the graph only through SUCC
L4      if r ≠ none then return r                ▷ stop: the rest is never generated
L5  return "no violation"

SUCC((s, q))                                      ▷ successors in the product, computed on demand
L6  for each s′ ∈ NEXT_M(s) do
L7      for each q′ ∈ NEXT_B(q, L(s)) do yield (s′, q′)
```

The holes:

- **NEXT_M.** The successor function of the system: it runs one atomic step of one process from the state vector $s$. It can include a reduction, for example [partial-order reduction](/partial-order-reduction/), which returns a subset of the successors.
- **NEXT_B and INIT_B.** The automaton for the negated property. In the simplest form it is translated in full before the search; in the method of Gerth, Peled, Vardi and Wolper (1995) its nodes are also expanded only when the product reaches them, so that unused parts of a large automaton are never built.
- **SEARCH.** A forward search that stops at the first witness: depth-first or breadth-first search for a bad state; [nested depth-first search](/nested-depth-first-search/) or an on-the-fly SCC algorithm (Couvreur 1999) for an accepting cycle.
- **STORE.** The visited set, exact or lossy, as in [explicit-state model checking](/explicit-state-model-checking/).

### Example

Take $n$ counters modulo $4$, all $0$ at the start; a step adds one to one counter. There are $4^n$ reachable states. The property says that counters $0$ and $1$ are never both $1$, as a mutual exclusion requirement between two of the components. A depth-first search that tries counter $0$ first follows the path

$$(0,0,\ldots) \to (1,0,\ldots) \to (2,0,\ldots) \to (3,0,\ldots) \to (3,1,\ldots) \to (0,1,\ldots) \to (1,1,\ldots)$$

and stops at the seventh state, whatever $n$ is. A breadth-first search stops at the first state of depth $2$ that violates the property. The number of states generated before the stop:

| $n$ | all states | global method | on-the-fly DFS | on-the-fly BFS |
|---|---|---|---|---|
| 3 | 64 | 64 | 7 | 13 |
| 4 | 256 | 256 | 7 | 19 |
| 5 | 1024 | 1024 | 7 | 26 |
| 6 | 4096 | 4096 | 7 | 34 |
| 7 | 16384 | 16384 | 7 | 43 |

The gain depends on the error. If the bad state is the one where all $n$ counters are $1$, the same depth-first search stores 28 of the 64 states for $n = 3$ and 6940 of the 16384 states for $n = 7$, and the path it reports has 27 and 6939 steps, since every stored state lies on it; a breadth-first search stores 27 and 3384 states and gives a shortest path of $n$ steps. If the property holds, every method stores all $4^n$ states.

### Why it is correct

A search that reads the graph only through SUCC behaves in the same way whether SUCC looks up a stored graph or computes the successors when asked: it receives the same answers in the same order. So the on-the-fly search makes the same moves as the same search run on the full product, up to the point where it stops, and its answer is correct whenever the search is correct on the full product. For the product itself, SUCC yields exactly the edges of the product of the [automata-theoretic approach](/automata-theoretic-approach/), so a reachable accepting cycle found by the search is a counterexample of the system, and no cycle means that the property holds. Stopping early is sound, because the search stops only when it holds a complete witness: a path to a bad state, or a stem and a cycle.

### Size and time

In the worst case, when the property holds, the search generates the whole reachable product, $O(|M| \cdot |B|)$ states and transitions, as a global method does. When the property fails, the cost is the number of states generated before the first witness, which can be as small as the length of the counterexample and does not depend on the size of the rest of the system. Memory is the visited set plus the search stack. The [state explosion problem](/state-explosion-problem/) is not solved, only postponed until the first error.

## Classic examples

- **SPIN.** The never claim for the negated property and the processes of the model run in lockstep, and the nested depth-first search builds the product as it goes. Most errors are found long before the search could finish.
- **Murphi and TLC.** The breadth-first search checks each invariant as soon as a new state is generated, and stops with a shortest counterexample.
- **Program model checkers.** Tools such as Java PathFinder execute the program itself as the successor function, so a full state graph never exists; [stateless model checking](/stateless-model-checking/) goes further and stores no states at all.
- **CADP.** The OPEN/CÆSAR interface gives an implicit successor function for labelled transition systems, on which on-the-fly checkers for the modal μ-calculus run.

## Variations

- **On-the-fly translation.** Gerth, Peled, Vardi and Wolper (1995) build the Büchi automaton from the formula by need, during the search, so that the formula's automaton is never built in full.
- **Generalized acceptance.** Couvreur (1999) checks emptiness of generalized Büchi automata on the fly by merging strongly connected components during a single depth-first search, without degeneralization.
- **With partial-order reduction.** Peled (1994) showed how to choose the reduced successor sets during an on-the-fly LTL search, with a proviso that prevents an action from being postponed forever around a cycle.
- **Breadth-first.** A breadth-first on-the-fly search finds a [shortest counterexample](/shortest-counterexample/) for an invariant, at the cost of storing the frontier.
- **Branching time.** [Local model checking](/local-model-checking/) evaluates a CTL or μ-calculus formula at one state by exploring only what the formula needs, which is the same idea with a goal set by the formula.

## Pitfalls

- **Expecting a gain when the property holds.** On-the-fly checking does not shrink the state space; a correct system is explored in full.
- **Backward algorithms.** An algorithm that needs predecessors, or a fixed point over all states, cannot run on the fly. Use a forward algorithm such as nested depth-first search.
- **Long counterexamples.** Depth-first search finds an error quickly, but the path can be very long, as in the second example above. Rerun with breadth-first search or a depth bound to get a short one; see [counterexample generation](/counterexample-generation/).
- **Reductions that look ahead.** A reduction that needs the full graph, such as the minimisation of the system by [bisimulation](/bisimulation/), cannot be done on the fly. Partial-order reduction can, with its cycle proviso.
- **The first error is not the only one.** Fixing the reported error and rerunning is the normal cycle; tools can also continue after an error to report more.

## Exercises

1. In the example, why does the depth-first search stop after 7 states for every $n$? Which successor order would make it stop later?
2. Give a family of systems in which on-the-fly breadth-first search generates all but a constant number of the reachable states before it finds an error at depth $1$.
3. Explain why the backward labelling algorithm for $\mathsf{EG}$ cannot run on the fly, and why nested depth-first search can.
4. A property automaton has $2^{20}$ states, but the product with the system reaches only 50 of them. Compare the cost of translating the formula in full with that of an on-the-fly translation.

## References
