---
tag: JZ943Y
kind: algorithm
slug: ctl-labelling-algorithm
name: CTL labelling algorithm
aliases:
- Clarke-Emerson-Sistla labelling algorithm
- CTL labeling algorithm
- Explicit-state CTL model checking
area: logic-and-constraints/model-checking
level: core
summary: Label each state with the CTL subformulas it satisfies, from the inside out. EU and AU are backward searches, and EG uses strongly connected components, so the time is linear.
solves: [ctl-model-checking]
model: word-ram
complexity:
  vars: {m: the number of states plus the number of transitions, f: the number of symbols of the formula, n: the number of states}
  time: {worst: O(m·f), best: O(m·f)}
  space: {extra: O(m + n·f)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1986
  people: [Edmund M. Clarke, E. Allen Emerson, A. Prasad Sistla]
  note: Clarke, Emerson and Sistla gave the labelling algorithm with the SCC treatment of EG and of fairness, in time linear in the structure and the formula.
prereqs: [computation-tree-logic, kripke-structure, breadth-first-search, tarjan-scc]
see_also: [ctl-model-checking, ctl-model-checking-linear-time, computation-tree-logic, fairness, emerson-lei-algorithm, symbolic-model-checking, strongly-connected-components, local-model-checking]
sources:
  - paper: doi:10.1145/5397.5399
    title: Edmund M. Clarke, E. Allen Emerson and A. Prasad Sistla, Automatic verification of finite-state concurrent systems using temporal logic specifications, ACM Transactions on Programming Languages and Systems 8(2), 1986, pages 244 to 263
    locator: the labelling algorithm for CTL with EX, EU and EG, the use of strongly connected components for EG, the linear bound, and the extension to fairness constraints
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press, 2004
    locator: Section 3.6.1 (the labelling algorithm, with the cases for EX, AF, EU and the SCC version of EG)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.4 (the bottom-up algorithm, the backward searches for EU and the SCC-based algorithm for EG, with the time complexity) and Section 6.5 (fair CTL)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 4, Section 4.1 (CTL model checking by labelling, with the SCC procedure for EG and its fair version)
---

The CTL labelling algorithm decides [CTL model checking](/ctl-model-checking/): it computes, for a [Kripke structure](/kripke-structure/) $M$ and a [CTL](/computation-tree-logic/) formula $\varphi$, the set of states that satisfy $\varphi$. It visits the subformulas of $\varphi$ from the smallest to the largest, and labels each state with the subformulas that hold there. The Boolean cases and $\mathsf{EX}$ are one pass over the states and edges, $\mathsf{EU}$ and $\mathsf{AU}$ are backward searches, and $\mathsf{EG}$ uses the [strongly connected components](/strongly-connected-components/) of a subgraph. Each step takes time $O(|S| + |R|)$, so the whole algorithm takes $O(|M|\,|\varphi|)$. This is the algorithm of Clarke, Emerson and Sistla (1986); the [linear-time theorem](/ctl-model-checking-linear-time/) states and proves its bound, and the [fairness](/fairness/) page gives its extension to fair paths.

## In plain words

A CTL formula is built from small pieces. The algorithm works out the small pieces first, for every state, and writes the answers on the states as labels. Then it uses those labels to work out the bigger pieces, until it reaches the whole formula.

Each kind of piece has its own short procedure. "Some next state has the label" looks at the neighbours. "There is a way to reach a state with the label, through states with another label" is a search backwards from the target states. "There is a way to stay forever in states with the label" looks for loops among those states, and then for every state that can walk into such a loop.

Each procedure looks at each state and each edge a fixed number of times. So the total work is the size of the graph times the number of pieces.

## The problem

Given a finite Kripke structure $M = (S, I, R, L)$ with a total transition relation and a CTL formula $\varphi$, compute $[\![\varphi]\!] = \{s \in S : s \models \varphi\}$. Then $M \models \varphi$ if and only if $I \subseteq [\![\varphi]\!]$. The input is given as [adjacency lists](/adjacency-list/), and $|M| = |S| + |R|$.

## The algorithm

The algorithm keeps a table $T$ that maps each processed subformula $\psi$ to the set $[\![\psi]\!]$. It uses the predecessor lists of $M$, built once in $O(|M|)$ time. The other operators reduce to the ones in the pseudocode: $\mathsf{EF}\,\alpha = \mathsf{E}[\mathit{true}\,\mathsf{U}\,\alpha]$, $\mathsf{AF}\,\alpha = \mathsf{A}[\mathit{true}\,\mathsf{U}\,\alpha]$ and $\mathsf{AG}\,\alpha = \neg\mathsf{EF}\,\neg\alpha$.

```pseudo id=main
SAT(M, φ)                                     ▷ M = (S, I, R, L) with R total
L1  for each subformula ψ of φ, each one after its parts do
L2      case ψ of
L3      p:          T[ψ] ← { s ∈ S : p ∈ L(s) }
L4      ¬α:         T[ψ] ← S ∖ T[α]
L5      α ∧ β:      T[ψ] ← T[α] ∩ T[β]
L6      α ∨ β:      T[ψ] ← T[α] ∪ T[β]
L7      EX α:       T[ψ] ← { s ∈ S : some t ∈ R(s) has t ∈ T[α] }
L8      AX α:       T[ψ] ← S ∖ { s ∈ S : some t ∈ R(s) has t ∉ T[α] }
L9      E[α U β]:   T[ψ] ← CHECK-EU(T[α], T[β])
L10     A[α U β]:   T[ψ] ← CHECK-AU(T[α], T[β])
L11     EG α:       T[ψ] ← CHECK-EG(T[α])
L12 return T[φ]

CHECK-EU(A, B)                                ▷ states with a path in A to B
L13 X ← B, and Q ← a queue that holds the states of B
L14 while Q is not empty do
L15     t ← DEQUEUE(Q)
L16     for each s with (s, t) ∈ R do
L17         if s ∈ A and s ∉ X then add s to X, ENQUEUE(Q, s)
L18 return X

CHECK-AU(A, B)                                ▷ states whose every path goes through A to B
L19 c[s] ← |R(s)| for each s ∈ S; X ← B; Q ← a queue that holds the states of B
L20 while Q is not empty do t ← DEQUEUE(Q)
L21     for each s with (s, t) ∈ R do c[s] ← c[s] − 1     ▷ c[s] successors of s are not in X
L22         if c[s] = 0 and s ∈ A and s ∉ X then add s to X, ENQUEUE(Q, s)
L23 return X

CHECK-EG(A)                                   ▷ states with an infinite path inside A
L24 X ← ∅
L25 for each SCC C of the subgraph of M on A do if C has an edge then X ← X ∪ C
L26 Q ← a queue that holds the states of X; while Q is not empty do t ← DEQUEUE(Q)
L27     for each s with (s, t) ∈ R do if s ∈ A and s ∉ X then add s to X, ENQUEUE(Q, s)
L28 return X
```

CHECK-EU is a backward [breadth-first search](/breadth-first-search/) from $B$ that only enters states of $A$. CHECK-AU is the same search, but a state of $A$ may join only when all its successors have joined; the counter $c[s]$ holds the number of successors of $s$ that have not joined yet. CHECK-EG finds the nontrivial components of the subgraph on $A$ with [Tarjan's algorithm](/tarjan-scc/): a component *has an edge* when it has two or more states or one state with a self-loop. Every state of such a component lies on a cycle inside $A$. Then a backward search inside $A$ adds each state that can reach one of these components.

## Example

Take the structure with states $0, \ldots, 5$ and edges $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 2$, $2 \to 4$, $3 \to 0$, $4 \to 5$, $5 \to 4$. Let $p$ hold in $0, 1, 2, 3, 5$ and $q$ hold in $3$.

**$\mathsf{EG}\,p$.** The subgraph on $T[p] = \{0, 1, 2, 3, 5\}$ has the edges $0 \to 1$, $0 \to 2$, $1 \to 3$, $3 \to 0$ and $2 \to 2$; the edge $5 \to 4$ leaves it. Its components are $\{0, 1, 3\}$, $\{2\}$ and $\{5\}$. The first has a cycle and the second a self-loop, so line L25 gives $X = \{0, 1, 2, 3\}$. State $5$ is a trivial component, and no state of $X$ is reachable from it inside $p$, so the backward search adds nothing. $[\![\mathsf{EG}\,p]\!] = \{0, 1, 2, 3\}$.

**$\mathsf{E}[p\,\mathsf{U}\,q]$.** CHECK-EU starts with $X = \{3\}$:

| dequeued | predecessors | added |
|---|---|---|
| 3 | 1 | 1 |
| 1 | 0 | 0 |
| 0 | 3 | none |

So $[\![\mathsf{E}[p\,\mathsf{U}\,q]]\!] = \{0, 1, 3\}$.

**$\mathsf{A}[p\,\mathsf{U}\,q]$.** The counters start as $c = (2, 1, 2, 1, 1, 1)$ for states $0$ to $5$, and $X = \{3\}$. Dequeuing $3$ lowers $c[1]$ to $0$, and $1 \in A$, so $1$ joins. Dequeuing $1$ lowers $c[0]$ to $1$, so $0$ does not join: its successor $2$ never joins, and indeed the path $0\,2\,2\,2 \ldots$ satisfies $p$ forever and never $q$. $[\![\mathsf{A}[p\,\mathsf{U}\,q]]\!] = \{1, 3\}$.

**$\mathsf{AG}\,\mathsf{EF}\,q$.** $\mathsf{EF}\,q = \mathsf{E}[\mathit{true}\,\mathsf{U}\,q] = \{0, 1, 3\}$, since $2$, $4$ and $5$ cannot reach $3$. Then $\mathsf{AG}\,\mathsf{EF}\,q = \neg\mathsf{EF}\,\neg\mathsf{EF}\,q$, and every state can reach $\{2, 4, 5\}$ (state $3$ through $0$), so the result is $\emptyset$.

## Correctness

The proof is by induction on the subformulas: line L1 visits each subformula after its parts, so when $\psi$ is processed, $T[\alpha] = [\![\alpha]\!]$ and $T[\beta] = [\![\beta]\!]$. Lines L3 to L8 are the definitions. For CHECK-EU, every state added at line L17 has a path through $A$ to $B$ (induction on the time it is added), and every state with such a path of length $j$ is added (induction on $j$); this is the least fixed point $\mu Z.\, B \cup (A \cap \mathsf{EX}\,Z)$ of [computation tree logic](/computation-tree-logic/). CHECK-AU computes $\mu Z.\, B \cup (A \cap \mathsf{AX}\,Z)$, because the counter reaches $0$ exactly when all successors are in $X$. For CHECK-EG, a path that stays in $A$ forever ends up inside one nontrivial component of the subgraph on $A$, and conversely each state that reaches such a component inside $A$ can then cycle in it forever. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The number of distinct subformulas is at most $|\varphi|$. For each of them, the work is $O(|S| + |R|)$:

- Lines L3 to L8 touch each state and each edge at most once (the sets are arrays of Booleans indexed by state, or hash sets).
- CHECK-EU and CHECK-AU enqueue each state at most once and scan each predecessor list once, so they look at each edge once.
- Tarjan's algorithm on the subgraph on $A$ is $O(|S| + |R|)$, and the backward search of lines L26 and L27 is too.

So the time is $O(|M|\,|\varphi|)$, which is optimal up to a constant factor, since an algorithm must read the structure and the formula. The space is $O(|M|)$ for the predecessor lists, the counters and the queues, plus $O(|S|\,|\varphi|)$ for the table $T$. Keeping only the sets that are still needed lowers the second term in practice. With $k$ justice sets, fair $\mathsf{EG}$ costs $O(|M| + k|S|)$, and the total becomes $O(|M|\,|\varphi|\,k)$ in the worst case; see [fairness](/fairness/).

## Properties

- **Global.** It computes $[\![\varphi]\!]$ for all states at once, not only for the initial states. This helps when the same structure is checked from many states, and wastes work when only one state matters.
- **Linear.** The time is linear in the structure and in the formula, the [linear-time theorem](/ctl-model-checking-linear-time/).
- **Deterministic and exact.** No randomness and no approximation.
- **Explicit.** The structure must be in memory as a graph. This is its limit: real systems have exponentially many states, the [state explosion problem](/state-explosion-problem/).
- **Witnesses.** The parent links of CHECK-EU give a witness path for $\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$, and the components of CHECK-EG give a lasso for $\mathsf{EG}\,\alpha$. Negated, they are counterexamples for $\mathsf{AG}$ and $\mathsf{AF}$.

## Variants and improvements

- **Fairness.** With justice sets $J_1, \ldots, J_k$, a component counts in line L25 only when it also meets each $J_i$; with compassion pairs, components are refined further. Then $\mathit{fair} = \mathsf{E}_f\mathsf{G}\,\mathit{true}$, and $\mathsf{EX}$ and $\mathsf{EU}$ use $T[\alpha] \cap \mathit{fair}$ and $T[\beta] \cap \mathit{fair}$ as targets. See [fairness](/fairness/).
- **Only $\mathsf{EX}$, $\mathsf{EU}$ and $\mathsf{EG}$.** The original paper has no CHECK-AU; it uses $\mathsf{A}[\alpha\,\mathsf{U}\,\beta] = \neg\mathsf{E}[\neg\beta\,\mathsf{U}\,(\neg\alpha \wedge \neg\beta)] \wedge \neg\mathsf{EG}\,\neg\beta$. The counter version is shorter and avoids the SCC pass, but it does not extend to fairness, where the implementation falls back to the identity.
- **Fixed-point iteration.** Compute $\mathsf{EG}\,\alpha$ as $\nu Z.\, \alpha \wedge \mathsf{EX}\,Z$ by repeated passes. Each pass costs $O(|M|)$ and up to $|S|$ passes may be needed, so this is $O(|S|\,|M|)$ per operator on explicit graphs, but it is the natural form for [symbolic model checking](/symbolic-model-checking/) with [BDDs](/binary-decision-diagram/).
- **Local and on-the-fly checking.** [Local model checking](/local-model-checking/) evaluates $s \models \varphi$ on demand, by a depth-first search over pairs (state, subformula), and can stop early.
- **Mu-calculus.** The same bottom-up scheme, with fixed points in place of the special cases, is [mu-calculus model checking](/mu-calculus-model-checking/); the [Emerson-Lei algorithm](/emerson-lei-algorithm/) is its version for nested fixed points.

## When to use it

Use it when the structure fits in memory as a graph: models of protocols with up to some hundred million states, state spaces generated by an explicit-state tool, or the reachable part of a small program. It is also the right choice when the answer for every state is needed, as in a counterexample explanation or a fixed-point computation inside another algorithm. For systems given by circuits or programs with many Boolean variables, use [symbolic model checking](/symbolic-model-checking/) or SAT-based methods; for LTL properties use [LTL model checking](/ltl-model-checking/).

## Pitfalls

- **States with no successor.** The semantics assumes a total relation. On a state with no successor, $\mathsf{AX}\,\mathit{false}$ would hold and $\mathsf{EG}\,\mathit{true}$ would not. Add a self-loop with a $\mathit{dead}$ label first, or reject such input; the implementation raises an error.
- **Trivial components.** A single state with no self-loop is a strongly connected component, but it has no cycle. Counting it in line L25 makes $\mathsf{EG}$ wrong.
- **$\mathsf{AF}$ from $\mathsf{EG}$ under fairness.** With fairness, $\mathsf{A}_f\mathsf{F}\,\alpha$ must be $\neg\mathsf{E}_f\mathsf{G}\,\neg\alpha$, not the counter version, because the counter version also follows unfair paths.
- **Shared subformulas.** Identify equal subformulas, by hashing or by a DAG, so that each is computed once. A recursion that recomputes them can take exponential time on formulas with shared parts.
- **Deep recursion.** Tarjan's algorithm and the subformula traversal should be iterative; a structure with a long path or a deeply nested formula overflows a recursive stack.

## Implementations

## History

Clarke and Emerson introduced CTL and model checking by fixed points in 1981, and Queille and Sifakis gave a fixed-point model checker for a similar logic in 1982. Clarke, Emerson and Sistla presented the labelling algorithm with the SCC treatment of $\mathsf{EG}$ at POPL in 1983, and published it with fairness in ACM TOPLAS in 1986. It was the core of the EMC model checker, and in 2007 Clarke, Emerson and Sifakis received the Turing Award for the invention of model checking.

## References
