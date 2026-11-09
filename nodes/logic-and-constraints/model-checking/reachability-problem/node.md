---
tag: EMYCKR
kind: problem
slug: reachability-problem
name: Reachability problem
aliases:
- State reachability
- State-space reachability
area: logic-and-constraints/model-checking
level: intro
summary: Decide whether some state of a target set can be reached from an initial state of a transition system. Linear time on an explicit graph, PSPACE-complete when the system is given succinctly.
prereqs: [kripke-structure, breadth-first-search, graph-reachability]
see_also: [invariant-checking, deadlock-freedom-checking, symbolic-reachability, explicit-state-model-checking, state-explosion-problem, pushdown-reachability, petri-net-reachability-decidability, savitch-theorem]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (invariants, and invariant checking by a depth-first search of the reachable states, with a counterexample) and Chapter 2, Section 2.3 (the state-space explosion problem)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Section 8.1 (Savitch's theorem, with the yieldability procedure) and Section 8.3 (the PSPACE-completeness of TQBF, with the encoding of configurations); Section 8.5 (PATH is NL-complete)
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 1970, pages 177 to 192
    locator: the main theorem (nondeterministic space s(n) is in deterministic space s(n)^2), proved by the recursive reachability test
  - paper: "Dexter Kozen, Lower bounds for natural proof systems, Proceedings of the 18th Annual Symposium on Foundations of Computer Science (FOCS), 1977, pages 254 to 266"
    locator: the PSPACE-completeness of the non-emptiness of the intersection of finite automata, which is reachability in a product of automata
---

The reachability problem asks whether a system can get from one of its initial states to a state in a given target set. On an explicit graph it is solved in linear time by [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/), and it is the core of model checking: [invariant checking](/invariant-checking/), [deadlock detection](/deadlock-freedom-checking/) and the CTL operator $\mathsf{EF}$ are all reachability questions. The difficulty is size. A system is usually given by a program or a circuit, not by its graph, and for such succinct inputs the problem is [PSPACE](/pspace/)-complete.

## In plain words

A system moves from state to state. Some states are bad, for example a state in which two processes write the same file. The question is: can the system ever get into a bad state, starting from where it starts?

If you have the full map of states and moves, this is a search in a graph. Start from the initial states, follow every move, and mark each state when you first see it. Stop when you find a bad state or when nothing new appears. The search looks at each state and each move once, and the path it followed is the proof that the bad state is reachable.

The catch is that the map is rarely given. A program with a few dozen variables has more states than any computer can list, so the hard part is to search a graph that is too big to write down.

## Definition

This page writes $M = (S, I, R)$ for a transition system: a finite set $S$ of states, a set $I \subseteq S$ of initial states and a transition relation $R \subseteq S \times S$. It is a [Kripke structure](/kripke-structure/) without the labels and without the totality condition. A path of length $k$ is a sequence $s_0 s_1 \ldots s_k$ with $(s_{i-1}, s_i) \in R$ for $1 \le i \le k$. The set of **reachable states** is

$$\mathit{Reach}(M) = \{ s \in S : \text{there is a path } s_0 \ldots s_k \text{ with } s_0 \in I \text{ and } s_k = s \}.$$

**Reachability (decision).** Input: $M$ and a target set $T \subseteq S$. Question: is $\mathit{Reach}(M) \cap T \ne \emptyset$?

**Reachability (search).** Output a path from $I$ to $T$ when one exists. In verification this path is the *counterexample* (or *witness*), and a short one is easier to read.

**How the input is given.** The answer depends on the input form, so the bounds below name it.

- *Explicit:* $S$, $I$, $R$ and $T$ are listed, with $R$ as [adjacency lists](/adjacency-list/). The input size is $|M| = |S| + |R|$.
- *Implicit:* a program or a next-state function generates the successors of a state on request. The algorithm pays for each successor that it generates.
- *Succinct (symbolic):* the states are the vectors $x \in \{0,1\}^n$, and $I(x)$, $R(x, x')$ and $T(x)$ are given as Boolean formulas or circuits of polynomial size. The graph has $2^n$ states, exponential in the input.

## Variants

- **Backward reachability.** Compute $\mathit{pre}^*(T)$, the states that can reach $T$, and test whether it meets $I$. It answers the same question, and it is the form of the CTL operator $\mathsf{EF}$ and of the [CTL labelling algorithm](/ctl-labelling-algorithm/).
- **Bounded reachability.** Is $T$ reachable in at most $k$ steps? For succinct systems this is the question of [bounded model checking](/bounded-model-checking/), which unrolls $R$ $k$ times into a SAT instance.
- **Repeated reachability.** Is there a path that visits $T$ infinitely often? In a finite graph, this holds if and only if a state of $T$ is reachable and lies on a cycle. It is the emptiness test of a [Büchi automaton](/buchi-automaton/), solved by [nested depth-first search](/nested-depth-first-search/) or by [strongly connected components](/strongly-connected-components/).
- **Reachability in infinite-state systems.** For [Petri nets](/petri-net/) the problem is decidable ([Petri net reachability](/petri-net-reachability-decidability/)) and Ackermann-complete; for [pushdown systems](/pushdown-system/) it is in polynomial time ([pushdown reachability](/pushdown-reachability/)); for [timed automata](/timed-automata/) it is PSPACE-complete by the [region graph](/region-graph/); for machines with two counters it is undecidable.

## Examples

**An explicit search.** In the two-process mutual exclusion structure of the [Kripke structure](/kripke-structure/) page, a breadth-first search from $(n, n, 1)$ finds the 8 reachable states in four layers:

| distance | states found |
|---|---|
| 0 | $(n,n,1)$ |
| 1 | $(w,n,1)$, $(n,w,1)$ |
| 2 | $(c,n,0)$, $(w,w,1)$, $(n,c,0)$ |
| 3 | $(c,w,0)$, $(w,c,0)$ |

For the target $T = \{s : \ell_1 = c \text{ and } \ell_2 = c\}$ the answer is no: none of the 8 states is in $T$. For the target $\{(w, c, 0)\}$ the answer is yes, and the parent links of the search give the shortest witness $(n,n,1) \to (n,w,1) \to (n,c,0) \to (w,c,0)$ of length 3.

**A succinct system with a long witness.** Let the states be $x \in \{0,1\}^n$, read as a binary number, with $I = \{0\}$, $T = \{2^n - 1\}$ and $R(x, x')$ true when $x' = x + 1 \bmod 2^n$. The formula for $R$ has size $O(n)$ (an incrementer), but the only path from $0$ to $2^n - 1$ has $2^n - 1$ steps: 7 steps for $n = 3$, and $1\,048\,575$ steps for $n = 20$. So a witness can be exponentially longer than the input. This is why the succinct problem is not obviously in NP.

## Known algorithms

- **Explicit graph search.** [Breadth-first search](/breadth-first-search/) runs in $O(|S| + |R|)$ time and $O(|S|)$ space, and finds a shortest witness. [Depth-first search](/depth-first-search/) has the same cost and keeps the current path on its stack. Both work on the implicit form: [explicit-state model checking](/explicit-state-model-checking/) and [on-the-fly model checking](/on-the-fly-model-checking/) generate successors on demand and store only the visited states, so the cost is linear in the reachable part.
- **Reductions of the state space.** [Partial-order reduction](/partial-order-reduction/) and [symmetry reduction](/symmetry-reduction/) explore a smaller graph with the same reachable targets. [Bitstate hashing](/bitstate-hashing/) stores visited states in a bit array and may miss states.
- **Symbolic search.** [Symbolic reachability](/symbolic-reachability/) computes $\mathit{Reach}$ as the least fixed point $\mu Z.\, I \cup \mathit{post}(Z)$ on [BDDs](/binary-decision-diagram/), one breadth-first layer per step; the [saturation algorithm](/saturation-algorithm/) changes the order of the steps.
- **SAT-based methods.** [Bounded model checking](/bounded-model-checking/) finds witnesses up to a length bound. [k-induction](/k-induction/), [interpolation-based model checking](/interpolation-based-model-checking/) and [IC3/PDR](/ic3-pdr/) also prove that $T$ is unreachable.

## Bounds

**Explicit input.** Breadth-first search gives $O(|S| + |R|)$ time, which is optimal up to a constant, because an algorithm that does not read an edge can miss the only path. In space, directed reachability (the problem PATH) is [NL](/nondeterministic-logspace/)-complete, and [Savitch's theorem](/savitch-theorem/) solves it in $O(\log^2 |S|)$ deterministic space.

**Succinct input: PSPACE-complete.** *Theorem.* Reachability for systems given by Boolean circuits $I(x)$, $R(x, x')$, $T(x)$ over $n$ state variables is PSPACE-complete.

*Proof.* *In PSPACE.* A nondeterministic machine keeps one current state $x$ ($n$ bits) and a step counter $c < 2^n$ ($n$ bits). It guesses $x$ with $I(x)$, and while $T(x)$ is false and $c < 2^n$ it guesses $x'$, checks $R(x, x')$ by evaluating the circuit, and sets $x \leftarrow x'$ and $c \leftarrow c + 1$. If $T$ is reachable, a shortest path visits each state at most once, so it has fewer than $2^n$ steps and some run accepts. The machine uses space polynomial in the input, so the problem is in NPSPACE, which equals PSPACE by Savitch's theorem.

*PSPACE-hard.* Let $L$ be decided by a deterministic Turing machine $D$ in space $p(m)$ on inputs of length $m$. Change $D$ so that its accepting state loops on itself. A configuration of $D$ on input $w$ is a row of $p(m)$ cells, where each cell holds a tape symbol, and the cell under the head holds the control state too, as in the proof of the Cook-Levin theorem. We encode it in $n = O(p(m))$ bits $x$. The circuit $I(x)$ tests that $x$ is the initial configuration on $w$. The circuit $R(x, x')$ tests, for each cell $j$, that cell $j$ of $x'$ follows from cells $j - 1$, $j$, $j + 1$ of $x$ by the transition function of $D$; each test is a circuit of constant size, so $R$ has size $O(p(m))$. The circuit $T(x)$ tests that the control state is accepting. Then $T$ is reachable if and only if $D$ accepts $w$. The circuits are built in polynomial time from $w$, so this is a polynomial-time reduction from $L$. $\blacksquare$

The same holds for systems given as a product of finite automata: the non-emptiness of the intersection of finite automata is PSPACE-complete (Kozen 1977), and it is reachability of a tuple of accepting states in the product. This is the formal side of the [state explosion problem](/state-explosion-problem/).

## Reductions

- **Invariant checking.** A state predicate $p$ holds in each reachable state if and only if the target $\neg p$ is not reachable. So [invariant checking](/invariant-checking/) and reachability reduce to each other in linear time, and a counterexample is a reachability witness.
- **Deadlock detection.** [Deadlock detection](/deadlock-freedom-checking/) is reachability of the states with no enabled transition.
- **Safety properties.** A regular [safety property](/safety-property/) is checked by reachability in the product of $M$ with a finite automaton for its bad prefixes.
- **CTL.** The CTL formula $\mathsf{EF}\,p$ holds in $s$ if and only if a $p$-state is reachable from $s$, and $\mathsf{AG}\,p$ is its dual. So [CTL model checking](/ctl-model-checking/) contains reachability.
- **Liveness to safety.** The [liveness-to-safety](/liveness-to-safety/) transformation turns repeated reachability into plain reachability in a system with a copy of the state.

## Applications

Reachability is the most common question in hardware and software verification: mutual exclusion, assertion failures, buffer overflows and protocol errors are all "a bad state is reachable". It is also the problem of [planning as model checking](/planning-as-model-checking/), where a plan is a path to a goal state, and of puzzle solving, where the state graph is implicit.

## References
