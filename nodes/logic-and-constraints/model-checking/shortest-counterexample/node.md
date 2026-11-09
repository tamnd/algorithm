---
tag: FQ8TYR
kind: problem
slug: shortest-counterexample
name: Shortest counterexample
aliases:
- Minimal counterexample
area: logic-and-constraints/model-checking
level: advanced
summary: Find a violating execution of minimal length. Breadth-first search solves it for invariants and plain Büchi products; for generalized Büchi conditions it is NP-hard.
prereqs: [counterexample-generation, breadth-first-search, buchi-automaton]
see_also: [counterexample-generation, breadth-first-search, nested-depth-first-search, bounded-model-checking, hamiltonian-cycle-problem, shortest-path, automata-theoretic-approach, invariant-checking]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (counterexamples for invariants) and Chapter 4, Section 4.4 (lasso counterexamples from the product with a Büchi automaton)
  - paper: "Viktor Schuppan and Armin Biere, Shortest counterexamples for symbolic model checking of LTL with past, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2005), Lecture Notes in Computer Science 3440, Springer, 2005"
    locator: the difference between shortest lassos in the product and in the system, and a construction that gives shortest counterexamples for LTL with past
  - paper: "Armin Biere, Alessandro Cimatti, Edmund M. Clarke and Yunshan Zhu, Symbolic model checking without BDDs, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 1999), Lecture Notes in Computer Science 1579, Springer, 1999"
    locator: bounded model checking with increasing bounds, which finds counterexamples of minimal bound
---

A shortest counterexample is a violating execution of the system with the fewest steps. For an invariant it is a shortest path from an initial state to a bad state, found by [breadth-first search](/breadth-first-search/) in linear time. For an LTL property it is a shortest *lasso*, a stem followed by a cycle, in the product of the system with a [Büchi automaton](/buchi-automaton/), and it is found with a few breadth-first searches per accepting state. When the acceptance condition is generalized, so that the cycle must meet several sets, finding a shortest lasso is NP-hard, by a reduction from the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). The page on [counterexample generation](/counterexample-generation/) explains what counterexamples are and how tools produce some counterexample; this page is about making it as short as possible.

## In plain words

When a checker finds a bug, it shows a run of the system that leads to the bug. A run of ten steps is easy to read. A run of ten thousand steps is not. So it is worth finding the shortest run that shows the bug.

For a bug that is a bad state, this is the shortest route on a map: search outward from the start, one layer of steps at a time, and stop at the first bad state. For a bad endless behaviour, the run is a path to a loop that repeats forever, and the length counts both parts. That is also easy when the loop must pass one kind of marked place. It becomes very hard when the loop must pass several kinds of marked place, because then it looks like a round trip that must visit every city.

## Definition

Let $G = (V, E)$ be a finite directed graph with a set $I \subseteq V$ of initial vertices: the reachable state graph of a system, or its product with an automaton for the negated property. Lengths count edges, and $d(x, y)$ is the length of a shortest path from $x$ to $y$ ($\infty$ if there is none), with $d(I, y) = \min_{x \in I} d(x, y)$.

- **Invariant version.** Given $G$, $I$ and a set $B \subseteq V$ of bad vertices, find a path from $I$ to $B$ of minimal length.
- **Büchi version.** Given $G$, $I$ and a set $F \subseteq V$, find a *lasso* of minimal length: a path $u$ from $I$ to a vertex $q$ and a closed walk $v$ from $q$ to $q$ with at least one edge that passes through a vertex of $F$. Its length is $|u| + |v|$.
- **Generalized version.** As the Büchi version, with sets $F_1, \ldots, F_k$, and the closed walk must pass through a vertex of each $F_i$.

The decision versions ask whether a solution of length at most a given $K$ exists.

When $G$ is the product $M \otimes A_{\neg\varphi}$ of the [automata-theoretic approach](/automata-theoretic-approach/), each lasso of $G$ projects to a lasso of $M$ of the same length whose trace violates $\varphi$. The converse is not exact: a shortest lasso of $M$ that violates $\varphi$ can need a longer lasso in the product, because the automaton may need several rounds of the cycle of $M$ to come back to the same automaton state. So "shortest in the product" is shortest for the chosen automaton, not always for the system; Schuppan and Biere (2005) discuss this gap and how to close it.

## Variants

- **Weighted.** Steps have costs, for example durations, and the goal is a cheapest counterexample. Replace breadth-first search by [Dijkstra's algorithm](/dijkstra/).
- **Fewest preemptions or context switches.** In concurrent programs, a counterexample with few thread switches is easier to understand; stateless checkers such as CHESS search in order of the number of preemptions.
- **Fewest relevant variables.** Instead of a short trace, find a trace with few variables that matter, by removing assignments that are not needed for the violation. This is a minimization of the explanation, not of the length.
- **Shortest witness.** The same problem for a path that shows that an existential property holds, such as $\mathsf{EF}\, p$ or a fair path for $\mathsf{EG}\, p$.
- **Shortest in the system for an LTL formula.** Minimize over lassos of $M$ rather than of a fixed product; see Definition.

## Examples

**An invariant.** In Peterson's algorithm with the two assignments of each process swapped (see [explicit-state model checking](/explicit-state-model-checking/)), breadth-first search finds a shortest path of 8 steps to a state with both processes critical. A depth-first search can return a much longer path.

**A long and a short cycle.** Let $I = \{a\}$, with edges $a \to f$, $f \to b_1 \to b_2 \to \cdots \to b_{10} \to f$, and $f \to c \to f$, and $F = \{f\}$. A nested depth-first search that tries $b_1$ before $c$ closes the cycle through the $b_i$ and reports a lasso of length $1 + 11 = 12$. The shortest lasso has length $1 + 2 = 3$: the stem $a \to f$ and the cycle $f \to c \to f$.

**The loop need not start at the accepting vertex.** Let $I = \{a\}$, with edges $a \to q$, $q \to f$, $f \to q$, and $F = \{f\}$. Starting the loop at $f$ gives the stem $a \to q \to f$ and the cycle $f \to q \to f$, length $2 + 2 = 4$. Starting it at $q$ gives the stem $a \to q$ and the cycle $q \to f \to q$, length $1 + 2 = 3$, which is the minimum.

## Known algorithms

- **Invariants: breadth-first search.** Search from $I$ and stop at the first vertex of $B$; follow parent pointers back. Time $O(|V| + |E|)$. Symbolically, compute the layers of reachable states (the *onion rings*) and walk back through them with pre-images; this also gives a shortest path.
- **Büchi lassos: one search per accepting vertex.** For $q \ne f$ let $c(q, f) = d(q, f) + d(f, q)$, and let $c(f, f)$ be the length of a shortest cycle through $f$, which is $1 + \min_{(f, w) \in E} d(w, f)$. By the lemma below, the minimum is
  $$\min_{f \in F}\ \min_{q \in V}\ \bigl(d(I, q) + c(q, f)\bigr).$$
  Compute $d(I, \cdot)$ by one breadth-first search from $I$. For each $f \in F$, compute $d(f, \cdot)$ by a breadth-first search from $f$, and $d(\cdot, f)$ by a breadth-first search from $f$ along reversed edges. Then take the minimum over $q$. Time $O(|F| \cdot (|V| + |E|))$, which is $O(|V| \cdot (|V| + |E|))$ in the worst case.
- **Heuristic short lassos.** Run nested depth-first search, then shorten the result: replace the stem by a shortest path to the cycle, and the cycle by a shortest cycle through the same accepting vertex. This is linear but not always optimal.
- **Bounded model checking.** Encode lassos of length $k$ with SAT and try $k = 0, 1, 2, \ldots$; the first satisfiable bound gives a counterexample of minimal bound in the encoding used ([bounded model checking](/bounded-model-checking/)).
- **Generalized lassos.** Search for the shortest closed walk through all sets with dynamic programming over subsets of $\{1, \ldots, k\}$, in time exponential in $k$ only, or with a SAT or ILP encoding.

**Lemma.** In the Büchi version, the minimum length of a lasso equals $\min_{f \in F} \min_{q \in V} (d(I, q) + c(q, f))$.

*Proof.* Take any lasso with stem $u$ from $I$ to $q$ and a closed walk $v$ from $q$ through some $f \in F$ back to $q$. Then $|u| \ge d(I, q)$. If $q \ne f$, then $v$ splits at $f$ into a walk from $q$ to $f$ and one from $f$ to $q$, of lengths at least $d(q, f)$ and $d(f, q)$. If $q = f$, then $v$ is a closed walk through $f$ with at least one edge, of length at least $c(f, f)$. So every lasso is at least as long as the minimum. Conversely, for the $q$ and $f$ that attain the minimum, a shortest path from $I$ to $q$ followed by shortest paths from $q$ to $f$ and from $f$ back to $q$ (or a shortest cycle through $f$ when $q = f$) is a lasso of exactly that length. $\square$

## Bounds

| Problem | Complexity | Method |
|---|---|---|
| invariant, explicit graph | $O(\lvert V\rvert + \lvert E\rvert)$ | breadth-first search |
| Büchi lasso, explicit graph | $O(\lvert F\rvert \cdot (\lvert V\rvert + \lvert E\rvert))$ | the lemma |
| generalized Büchi lasso, decision version | NP-complete | the reduction below |
| generalized, $k$ sets | $O(2^k \cdot \lvert V\rvert \cdot (\lvert V\rvert + \lvert E\rvert))$ | dynamic programming over subsets |
| system given by a program or a formula | at least as hard as model checking | PSPACE-hard for LTL |

**Theorem.** The generalized version is NP-complete in its decision form.

*Proof.* *In NP.* If any lasso exists, one exists with a stem of fewer than $|V|$ edges and a cycle of at most $(k + 1)|V|$ edges, made of shortest paths from $q$ to a vertex of $F_1$, then to a vertex of $F_2$, and so on, and back to $q$. So if $K$ exceeds $(k + 2)|V|$, the question is whether any lasso exists, which is polynomial (a nontrivial strongly connected component that meets every $F_i$). Otherwise a lasso of length at most $K$ is a certificate of polynomial size, checked in polynomial time.

*NP-hard.* Let $H$ be a directed graph with vertices $v_1, \ldots, v_n$, $n \ge 2$. Take $G = H$, $I = \{v_1\}$, $F_i = \{v_i\}$ for each $i$, and $K = n$. A lasso has a cycle that visits all $n$ vertices, so its length is at least $n$, and it equals $n$ only if the stem is empty and the cycle is a closed walk of $n$ edges through all $n$ vertices, which is a Hamiltonian cycle. Conversely, a Hamiltonian cycle, started at $v_1$, is a lasso of length $n$. So $H$ has a Hamiltonian cycle iff $G$ has a lasso of length at most $n$, and the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) is [NP-complete](/np-complete/). $\square$

The theorem explains why degeneralization does not help: the degeneralized automaton has a polynomial-time shortest lasso, but its cycles must also bring the counter of the construction back to its starting value, so its shortest lasso can be longer than the shortest generalized one.

## Reductions

- **To shortest paths.** The invariant version is the single-source [shortest path](/shortest-path/) problem with unit weights; the Büchi version reduces to $2|F| + 1$ such problems by the lemma.
- **From Hamiltonian cycle.** As in the theorem, for the generalized version.
- **From model checking.** A system with a shortest counterexample of length at most $K$ has a counterexample, so deciding the existence of a short counterexample is at least as hard as the [model checking](/ltl-model-checking/) question when $K$ is large. For systems given as programs, the graph itself is exponential, and the costs above are in the size of the explored graph.

## Applications

- **Debugging.** Short counterexamples are easier to read. Tools such as SPIN offer a breadth-first mode or an iterative shortening of the depth bound, and symbolic and SAT-based tools report counterexamples of minimal length by construction.
- **Abstraction refinement.** In [CEGAR](/cegar/), a short abstract counterexample gives a small path formula to check against the concrete system and fewer predicates to add.
- **Test generation.** A shortest witness for a coverage goal is a short test case; model checkers are used to generate tests in this way.
- **Explaining failures.** A short counterexample is the input to methods that locate the cause of the failure by comparing the failing run with nearby passing runs.

## References
