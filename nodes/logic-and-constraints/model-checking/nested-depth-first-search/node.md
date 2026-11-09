---
tag: CRQF4Q
kind: algorithm
slug: nested-depth-first-search
name: Nested depth-first search
aliases:
- NDFS
- Double DFS
- CVWY algorithm
area: logic-and-constraints/model-checking
level: core
summary: Find a reachable cycle through an accepting state of a Büchi automaton, or of the product of a system with one, with two interleaved depth-first searches in linear time and two extra bits per state.
solves: [ltl-model-checking]
model: word-ram
complexity:
  vars: {n: the number of states of the graph, m: the number of transitions of the graph}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, on_the_fly: true}
history:
  year: 1990
  people: [Costas Courcoubetis, Moshe Y. Vardi, Pierre Wolper, Mihalis Yannakakis]
  note: Presented at CAV 1990 and published in Formal Methods in System Design in 1992, as a memory-efficient emptiness check for on-the-fly verification.
prereqs: [depth-first-search, buchi-automaton, white-path-theorem]
see_also: [ltl-model-checking, tarjan-scc, automata-theoretic-approach, on-the-fly-model-checking, explicit-state-model-checking, bitstate-hashing, counterexample-generation, shortest-counterexample]
sources:
  - paper: doi:10.1007/BF00121128
    title: Costas Courcoubetis, Moshe Y. Vardi, Pierre Wolper and Mihalis Yannakakis, Memory-efficient algorithms for the verification of temporal properties, Formal Methods in System Design 1(2/3), 1992, pages 275 to 288
    locator: the nested search algorithm and its correctness proof
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 4, Section 4.4 (checking persistence with nested depth-first search, and the correctness lemma for the post-order of the inner searches)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 9 (checking emptiness of Büchi automata with a double depth-first search)
  - paper: "Gerard J. Holzmann, Doron Peled and Mihalis Yannakakis, On nested depth first search, The Spin Verification System (2nd SPIN Workshop, 1996), DIMACS Series in Discrete Mathematics and Theoretical Computer Science 32, AMS"
    locator: the early stop when the inner search reaches the outer stack, and the use with partial-order reduction
  - paper: doi:10.1007/978-3-540-31980-1_12
    title: Stefan Schwoon and Javier Esparza, A note on on-the-fly verification algorithms, TACAS 2005, Lecture Notes in Computer Science 3440, Springer, 2005
    locator: the colour-based nested search that reports a cycle as soon as the outer search closes one through an accepting state
  - book: isbn:9780321228628
    title: Gerard J. Holzmann, The SPIN Model Checker, Primer and Reference Manual, Addison-Wesley, 2003
    locator: Chapter 8, Search algorithms (the nested search used by SPIN for liveness)
---

Nested depth-first search decides whether a [Büchi automaton](/buchi-automaton/) accepts some word, that is, whether some accepting state lies on a cycle that is reachable from an initial state. An outer [depth-first search](/depth-first-search/) visits the graph, and when it finishes an accepting state, an inner search looks for a path back to that state. The inner searches share one set of marked states, so the whole run takes $O(n + m)$ time on a graph with $n$ states and $m$ transitions, and needs only two bits per state beyond the stacks. It is the emptiness check of the [automata-theoretic approach](/automata-theoretic-approach/) to [LTL model checking](/ltl-model-checking/) in SPIN, because it works on the fly and fits well with [bitstate hashing](/bitstate-hashing/).

## In plain words

You walk through a maze of rooms with a piece of chalk. Some rooms are special. You want to know if you can reach a special room and then walk in a circle back to it.

The first walk is an ordinary search that marks each room it enters. Each time it is done with a special room (it has seen everything you can reach from there), it starts a second walk from that room. The second walk uses a different colour of chalk and tries to get back to the special room. If it does, you have found the circle.

The trick is that the second colour is never erased. A later second walk skips rooms that an earlier second walk already marked. This seems wrong, but the order in which special rooms are finished makes it safe, and each room gets each colour at most once.

## The problem

The input is a finite directed graph $G = (V, E)$ with a set $I \subseteq V$ of initial states and a set $A \subseteq V$ of accepting states, usually the product $M \otimes A_{\neg\varphi}$ of a Kripke structure with a Büchi automaton. An *accepting lasso* is a path $s_0 \ldots s_k$ with $s_0 \in I$ and $s_k \in A$, together with a cycle $s_k\, t_1 \ldots t_\ell\, s_k$ with $\ell \ge 0$ (a self-loop has $\ell = 0$). The question is whether an accepting lasso exists. It exists iff the Büchi automaton accepts some word. The output is "empty" or one accepting lasso.

The graph may be given implicitly, by the initial states and a successor function, so that states are created only when the search reaches them.

## The algorithm

Two sets record the state of the search: *visited* for the outer search and *flagged* for the inner searches. The variable *seed* holds the accepting state that the current inner search tries to reach again.

```pseudo id=main
NESTED-DFS(G, I, A)
L1  visited ← ∅, flagged ← ∅
L2  for each s₀ ∈ I do
L3      if s₀ ∉ visited then DFS1(s₀)          ▷ a report in DFS2 stops the whole run
L4  return "no accepting cycle"

DFS1(s)                                      ▷ the outer search
L5  visited ← visited ∪ {s}, push s on the outer stack
L6  for each t with (s, t) ∈ E do
L7      if t ∉ visited then DFS1(t)
L8  if s ∈ A then                            ▷ in post-order: all successors are finished
L9      seed ← s
L10     DFS2(s)
L11 pop s from the outer stack

DFS2(x)                                      ▷ the inner search
L12 for each t with (x, t) ∈ E do
L13     if t = seed then report the lasso: the outer stack, then the inner stack, then seed; stop
L14     if t ∉ flagged then
L15         flagged ← flagged ∪ {t}
L16         DFS2(t)
L17 return
```

When line L13 fires, the outer stack is a path from an initial state to *seed*, and the inner stack is a path from *seed* to a predecessor of *seed*. Together they form the stem and the cycle of the lasso. The implementation uses explicit stacks instead of recursion, so it handles graphs whose depth is larger than the recursion limit.

## Example

Take the graph with states 0 to 5, initial state 0, and transitions $0 \to 1$, $0 \to 3$, $1 \to 2$, $2 \to 2$, $3 \to 4$, $4 \to 5$ and $5 \to 3$. Let $A = \{1, 4\}$. State 1 is accepting, but it is not on a cycle; state 4 is on the cycle $3\,4\,5$.

| Step | Event | Outer stack | flagged after the step |
|---|---|---|---|
| 1 | DFS1 enters 0, 1, 2 | 0 1 2 | ∅ |
| 2 | 2 finishes (its self-loop goes to a visited state); 2 is not accepting | 0 1 | ∅ |
| 3 | 1 finishes; 1 is accepting, so DFS2 starts with seed 1 | 0 1 | ∅ |
| 4 | DFS2 goes $1 \to 2$, flags 2; $2 \to 2$ is flagged; no way back to 1 | 0 1 | {2} |
| 5 | 1 is popped; DFS1 enters 3, 4, 5; $5 \to 3$ is visited | 0 3 4 5 | {2} |
| 6 | 5 finishes, not accepting; 4 finishes, accepting: DFS2 with seed 4 | 0 3 4 | {2} |
| 7 | DFS2 goes $4 \to 5$, flags 5, then $5 \to 3$, flags 3 | 0 3 4 | {2, 5, 3} |
| 8 | $3 \to 4$ reaches the seed: report | 0 3 4 | {2, 5, 3} |

The result is the stem $0\,3$ and the cycle $4\,5\,3$, so the lasso is $0\,3\,(4\,5\,3)^\omega$. With $A = \{1\}$ the search ends at line L4 with "no accepting cycle". With $A = \{2\}$ it reports the stem $0\,1$ and the cycle $2$ (the self-loop).

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Soundness is direct: a report at line L13 joins two real paths. Completeness rests on one lemma. Suppose that an accepting state lies on a cycle, and let $s$ be the first such state that the outer search finishes. When DFS2 starts from $s$, no state of a cycle through $s$ is flagged yet. If a state $t$ of the cycle were flagged by an earlier inner search from an accepting $s'$, then $s'$ reaches $t$ and so reaches $s$. Since $s'$ finished before $s$, the properties of depth-first search (the [white-path theorem](/white-path-theorem/)) give a path from $s$ back to $s'$ in both possible cases, so $s'$ is an accepting state on a cycle that finished earlier. This contradicts the choice of $s$. So the inner search from $s$ finds its way back to $s$, unless the run already stopped with an earlier report.

The lemma needs the post-order of line L8. If the inner search starts when an accepting state is first entered, the shared flags can hide a cycle: on the graph $0 \to 1$, $1 \to 2$, $2 \to 1$ with $A = \{0, 1\}$, the inner search from 0 flags 1 and 2, and the later inner search from 1 is blocked at once, so the cycle $1\,2\,1$ is missed.

## Complexity

The outer search enters each state at most once, because of *visited*, and scans each edge once. Each inner search enters only states that are not flagged and flags them, so all inner searches together enter each state at most once and scan each edge at most once. The total time is $\Theta(n + m)$ in the worst case, with $n$ and $m$ the numbers of reachable states and transitions, and the run can stop early when it finds a lasso. The memory is the hash table of states with two bits each (visited and flagged), plus the two stacks, which hold at most $n$ states each. On an implicit graph, the successor function is called at most twice per state.

## Properties

- **On the fly.** The graph is built as the outer search runs, and a lasso can be found before the whole graph is built.
- **Order sensitive.** The correctness depends on the post-order start of the inner searches and on the shared flags. Changing either breaks it (see Pitfalls).
- **Small memory per state.** Two bits per state. This makes it the right partner for [bitstate hashing](/bitstate-hashing/), where a state is stored as a few bits, and for hash compaction.
- **One lasso, not the shortest.** The reported lasso is not minimal; see [shortest counterexample](/shortest-counterexample/).
- **Büchi acceptance only.** A generalized Büchi automaton with $k$ acceptance sets must be degeneralized first, which multiplies the states by $k$.
- **Hard to parallelize.** Like depth-first search, it depends on a sequential post-order.

## Variants and improvements

- **Early stop at the outer stack** (Holzmann, Peled and Yannakakis 1996). Each state on the outer stack can reach the current seed, through the outer stack itself. So the inner search can stop as soon as it reaches any state on the outer stack, not only the seed, and close the cycle with the part of the outer stack from that state to the seed. The implementation has this as an option. The paper also shows how to combine the nested search with [partial-order reduction](/partial-order-reduction/).
- **Colour-based nested search** (Schwoon and Esparza 2005). States are white, cyan (on the outer stack), blue (finished by the outer search) or red (flagged). The outer search reports a cycle at once when it meets a cyan state and the current state or the cyan state is accepting, and red states are skipped by the outer search too. This finds many lassos before any inner search starts.
- **SCC-based checks.** An accepting cycle exists iff some reachable non-trivial [strongly connected component](/strongly-connected-components/) contains an accepting state. [Tarjan's algorithm](/tarjan-scc/) and its on-the-fly versions (Couvreur 1999, Geldenhuys and Valmari 2005) find it in one pass, find lassos sooner, and handle generalized Büchi conditions directly, at the cost of more memory per state.
- **Multi-core versions** that run several nested searches with shared colours have been studied since about 2011, with correctness arguments that are much more involved.

## When to use it

Use it for on-the-fly emptiness of a Büchi automaton when memory per state is the limit, in particular with bitstate hashing or hash compaction, as in SPIN. Prefer an SCC-based check when the automaton is a generalized Büchi automaton with several acceptance sets, when you want all accepting components, or when the full graph fits in memory and time to the first counterexample matters. For [reachability](/reachability-problem/) of a bad state (a safety property), a single search is enough and no nested search is needed.

## Pitfalls

- **Starting the inner search in pre-order.** As in the example above, the shared flags then hide cycles. The inner search must start after all successors of the seed are finished.
- **Clearing the flags between inner searches.** This keeps the result correct but makes the time quadratic: each inner search can scan the whole graph.
- **Flagging the seed too early.** If the code flags the seed before the inner search starts and then tests "is $t$ flagged" before "is $t$ the seed", it never sees the seed again. Test for the seed first, as line L13 does.
- **Reporting the wrong lasso.** The stem is the outer stack without the seed, and the cycle is the inner stack. With the early stop, the cycle also takes the part of the outer stack after the state that was reached; forgetting it gives a path that is not a cycle.
- **Recursion depth.** State spaces have paths with millions of states. Recursive code overflows; use explicit stacks.
- **Generalized acceptance.** Running the search with "accepting = in some $F_i$" is wrong for a generalized Büchi automaton; it checks a weaker condition.

## Implementations

## History

Courcoubetis, Vardi, Wolper and Yannakakis presented the algorithm at CAV 1990 and published it in Formal Methods in System Design in 1992, to replace the SCC computation of earlier emptiness checks by a search that needs only a few bits per state and works with the hashing methods of Holzmann. It became the liveness search of SPIN. Holzmann, Peled and Yannakakis (1996) added the early stop and made it work with partial-order reduction. Schwoon and Esparza (2005) compared the nested and SCC-based algorithms and gave the colour-based version that is now standard.

## References
