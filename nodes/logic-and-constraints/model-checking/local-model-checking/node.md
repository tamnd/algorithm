---
tag: SYAG8V
kind: algorithm
slug: local-model-checking
name: Local model checking
aliases:
- On-the-fly mu-calculus evaluation
- Liu-Smolka local algorithm
- top-down model checking
area: logic-and-constraints/model-checking
level: research
summary: Decide whether one given state satisfies a mu-calculus formula by searching a dependency graph built on demand from that state, so that the parts the answer does not need are never built.
solves: [mu-calculus-model-checking]
model: word-ram
complexity:
  vars: {n: the number of states plus transitions of the system, m: the size of the formula}
  time: {worst: O(n m)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, on_the_fly: true}
history:
  year: 1989
  people: [Colin Stirling, David Walker, Rance Cleaveland, Kim G. Larsen, Xinxin Liu, Scott A. Smolka]
  note: Stirling and Walker (1989) and Cleaveland (1990) gave tableau systems that check one state against a mu-calculus formula; Liu and Smolka (1998) gave the linear-time local fixed-point algorithm on dependency graphs.
prereqs: [modal-mu-calculus, fixed-point, knaster-tarski-theorem]
see_also: [mu-calculus-model-checking, ctl-model-checking, on-the-fly-model-checking, explicit-state-model-checking, emerson-lei-algorithm, parity-game, nested-depth-first-search, modal-mu-calculus]
sources:
  - paper: "Xinxin Liu and Scott A. Smolka, Simple linear-time algorithms for minimal fixed points, 25th International Colloquium on Automata, Languages and Programming (ICALP 1998), Lecture Notes in Computer Science 1443, Springer, 1998"
    locator: dependency graphs, the global and the local algorithm for their least solution, and the encoding of alternation-free mu-calculus model checking
  - paper: "Colin Stirling and David Walker, Local model checking in the modal mu-calculus, Theoretical Computer Science 89(1), 1991 (first version at TAPSOFT 1989)"
    locator: the tableau system for checking one state, with its soundness and completeness proof
  - paper: "Rance Cleaveland, Tableau-based model checking in the propositional mu-calculus, Acta Informatica 27(8), 1990"
    locator: a tableau method for the full mu-calculus with a simpler success condition
  - paper: "Henrik Reif Andersen, Model checking and Boolean graphs, Theoretical Computer Science 126(1), 1994"
    locator: the reduction of alternation-free model checking to Boolean equation systems and their local solution
  - book: isbn:9783319105741
    title: Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith and Roderick Bloem (eds.), Handbook of Model Checking, Springer, 2018
    locator: the chapter The mu-calculus and model checking, by Julian Bradfield and Igor Walukiewicz (local and global algorithms)
---

Local model checking decides whether *one* state $s_0$ of a system satisfies a [modal mu-calculus](/modal-mu-calculus/) formula $\varphi$, and it explores only the states and subformulas that this one answer depends on. The question "does $s_0$ satisfy $\varphi$" becomes the question "is the vertex $(s_0, \varphi)$ true in the least solution of a *dependency graph*", a graph whose vertices are pairs of a state and a subformula. The algorithm of Liu and Smolka (1998) solves this by a depth-first search that builds the graph on demand and stops as soon as the start vertex is known to be true, in time linear in the part it builds. The opposite, *global* style, used by [CTL model checking](/ctl-model-checking/) and the [Emerson-Lei algorithm](/emerson-lei-algorithm/), computes the set of all states that satisfy each subformula, from the inside out.

## In plain words

A global model checker answers a question about one state by first answering it for every state of the system. That is wasteful when the system is huge and the answer is near: to know that some path from here reaches a bad state, it is enough to find one such path.

Local model checking works from the question backwards. To know whether this state satisfies the formula, it asks what that depends on, such as "does some next state satisfy this part?", and asks those questions in turn, one at a time, depth first. Each answered question can settle the questions that were waiting for it. When the first question is settled, the work stops, and the rest of the system is never looked at. Questions that are still open when nothing is left to explore are answered "no".

## The problem

The input is a finite system $M = (S, R, L)$, with transitions $R \subseteq S \times S$ and a labelling $L$ of states by atomic propositions, a state $s_0 \in S$, and a closed formula $\varphi$ of the modal mu-calculus in positive normal form:

$$\varphi ::= \mathsf{true} \mid \mathsf{false} \mid p \mid \neg p \mid \varphi \wedge \varphi \mid \varphi \vee \varphi \mid \Diamond \varphi \mid \Box \varphi \mid \mu X.\, \varphi \mid \nu X.\, \varphi \mid X.$$

Here $\Diamond\varphi$ holds if some successor satisfies $\varphi$ and $\Box\varphi$ holds if every successor does. The output is whether $s_0 \models \varphi$. The system is given implicitly, by a successor function, and should be explored as little as possible. The method on this page is for formulas whose fixed points are all least ($\mu$); a greatest fixed point is handled through its negation, which is a least one, as described below.

**Dependency graphs.** A dependency graph has vertices $V$ and *hyperedges* $(v, T)$ with a source $v \in V$ and a finite set of targets $T \subseteq V$. A set $A \subseteq V$ is *closed* if for each hyperedge $(v, T)$ with $T \subseteq A$, also $v \in A$. The *least solution* is the smallest closed set; by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) it is the least fixed point of $F(A) = \{v : \text{some hyperedge } (v, T) \text{ has } T \subseteq A\}$. A hyperedge with $T = \emptyset$ makes its source true at once, and a vertex with no hyperedge is false.

For model checking, the vertices are the pairs $(s, \psi)$ of a state and a subformula of $\varphi$, and the hyperedges express the one-step meaning of each operator:

| Vertex | Hyperedges |
|---|---|
| $(s, \mathsf{true})$ | one, with no targets |
| $(s, \mathsf{false})$ | none |
| $(s, p)$, $(s, \neg p)$ | one with no targets if the literal holds in $s$, else none |
| $(s, \psi_1 \wedge \psi_2)$ | one, with targets $\{(s, \psi_1), (s, \psi_2)\}$ |
| $(s, \psi_1 \vee \psi_2)$ | two, with targets $\{(s, \psi_1)\}$ and $\{(s, \psi_2)\}$ |
| $(s, \Diamond\psi)$ | one for each successor $t$, with targets $\{(t, \psi)\}$ |
| $(s, \Box\psi)$ | one, with targets $\{(t, \psi) : (s, t) \in R\}$ |
| $(s, \mu X.\, \psi)$ | one, with targets $\{(s, \psi)\}$ |
| $(s, X)$ | one, with targets $\{(s, \mu X.\, \psi)\}$, the binder of $X$ |

When all fixed points of $\varphi$ are least, $s \models \psi$ iff $(s, \psi)$ is in the least solution.

## The algorithm

The algorithm keeps a value $0$ or $1$ for each vertex built so far ($1$ means "known true"), a list $D[u]$ of the hyperedges that wait for the vertex $u$, and a work stack $W$ of hyperedges to examine.

```pseudo id=main
LOCAL-LFP(v₀)                    ▷ is v₀ in the least solution?
L1  value[v₀] ← 0;  D[v₀] ← empty
L2  W ← the hyperedges of v₀
L3  while W is not empty do
L4      (v, T) ← pop(W)
L5      if value[v] = 1 then continue
L6      skip, in T, the targets with value 1     ▷ a pointer per hyperedge
L7      if every target in T has value 1 then
L8          value[v] ← 1;  if v = v₀ then return true
L9          push all hyperedges of D[v] onto W
L10     else u ← the first target in T whose value is not 1
L11         if u has not been built then
L12             value[u] ← 0;  D[u] ← [(v, T)]
L13             push the hyperedges of u onto W
L14         else append (v, T) to D[u]
L15 return false
```

A hyperedge waits for one target at a time, the first that is not yet true. When that target becomes true at line L8, line L9 puts the hyperedge back on the stack, and line L6 moves its pointer past the true targets. A vertex becomes true as soon as one of its hyperedges has only true targets. When the stack is empty, every vertex that is still $0$ is false.

**Greatest fixed points.** For a formula $\nu X.\, \psi$, the algorithm uses $s \models \nu X.\, \psi$ iff $s \not\models \overline{\nu X.\, \psi}$, where the bar is the positive normal form of the negation, which turns $\nu$ into $\mu$, $\wedge$ into $\vee$ and $\Box$ into $\Diamond$. In an *alternation-free* formula, a $\nu$ subformula met during a search for a $\mu$ formula is closed, so it is decided by a separate call, cached per state, and enters the graph as a vertex with one empty hyperedge or none.

## Example

Let the system have states $0$ to $5$ with transitions $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 4$, $3 \to 5$, $4 \to 4$ and $5 \to 5$, where $p$ holds only in state 1 and $q$ only in state 5. The question is whether state 0 satisfies $\mathsf{EF}\, p = \mu X.\, (p \vee \Diamond X)$. Write $\psi = p \vee \Diamond X$. The search, with the hyperedges of a vertex tried in order:

| Step | Hyperedge popped | Action |
|---|---|---|
| 1 | $(0, \mu X.\psi) \to \{(0, \psi)\}$ | build $(0, \psi)$ |
| 2 | $(0, \psi) \to \{(0, p)\}$ | build $(0, p)$, which has no hyperedge ($p$ is false in 0) |
| 3 | $(0, \psi) \to \{(0, \Diamond X)\}$ | build $(0, \Diamond X)$, with hyperedges to $(1, X)$ and $(2, X)$ |
| 4 | $(0, \Diamond X) \to \{(1, X)\}$ | build $(1, X)$ |
| 5 | $(1, X) \to \{(1, \mu X.\psi)\}$ | build $(1, \mu X.\psi)$ |
| 6 | $(1, \mu X.\psi) \to \{(1, \psi)\}$ | build $(1, \psi)$ |
| 7 | $(1, \psi) \to \{(1, p)\}$ | build $(1, p)$, with one empty hyperedge |
| 8 | $(1, p) \to \emptyset$ | $(1, p)$ is true; wake $(1, \psi)$ |
| 9 to 13 | the waiting hyperedges | $(1, \psi)$, $(1, \mu X.\psi)$, $(1, X)$, $(0, \Diamond X)$, $(0, \psi)$ become true |
| 14 | $(0, \mu X.\psi) \to \{(0, \psi)\}$ | $(0, \mu X.\psi)$ is true: answer yes |

The search built 8 vertices. The full dependency graph has $6 \cdot 5 = 30$ vertices, and a global algorithm computes all of them. States 2 to 5 were never touched; if the chain below state 2 were a million states long, the local search would still build 8 vertices. In the same system, $\mathsf{AF}\, p$ is false in state 0, since the path $0\, 2\, 4\, 4 \ldots$ avoids $p$; $\mathsf{AG}\, \neg q$ is false in state 1 and true in state 2.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). A vertex gets the value $1$ only when one of its hyperedges has only targets with value $1$, so by induction on time every vertex with value $1$ is in the least solution. When the stack is empty, every built hyperedge of a vertex with value $0$ waits for a target that has value $0$, so the set $Z$ of vertices with value $0$ has no hyperedge leaving it with all targets outside $Z$; the complement of $Z$ is then closed, and the least solution, the smallest closed set, avoids $Z$. The encoding is correct because the true pairs $\{(s, \psi) : s \models \psi\}$ form a closed set (so the least solution is inside it), and conversely the least solution, restricted to each $\mu X.\, \psi$, is a pre-fixed point of the function whose least fixed point is $\mu X.\, \psi$.

## Complexity

Each built hyperedge is pushed once when its source is built and once each time the target it waits for becomes true, and its pointer only moves forward, so the work for a hyperedge with $k$ targets is $O(k + 1)$. The algorithm thus runs in time linear in the size of the part of the dependency graph that it builds. The full graph for $M$ and $\varphi$ has at most $|S| \cdot |\varphi|$ vertices, and the total size of its hyperedges is $O((|S| + |R|) \cdot |\varphi|)$, since a $\Diamond$ or $\Box$ vertex of a state $s$ has one target per successor of $s$. So the time and space are $O(n m)$ for a formula with only least fixed points, the same worst case as the best global algorithms, but often much less in practice.

With greatest fixed points in an alternation-free formula, the simple scheme above makes one separate search per state and $\nu$ subformula, which can cost a factor $|S|$ more. Liu and Smolka avoid this by solving the alternation-free blocks of the formula in order with one shared graph, which keeps the total linear.

## Properties

- **On the fly.** It needs only an initial state and a successor function; states are generated when a vertex asks for them.
- **Early termination.** It stops as soon as the start vertex is true. A "no" answer for a least fixed point needs the whole reachable part of the graph, as for reachability.
- **Answers for many vertices.** At the end, every vertex with value $1$ is true; the false vertices are known false only when the search did not stop early.
- **Depth first.** The order of the stack makes it a depth-first search, so a "yes" answer for $\mathsf{EF}\, p$ comes with a path, read from the waiting hyperedges.
- **Restricted logic.** The linear-time bound holds for alternation-free formulas, which include CTL. Formulas with alternation need more, as for [parity games](/parity-game/).

## Variants and improvements

- **Tableau methods.** Stirling and Walker (1989) and Cleaveland (1990) build a proof tree for $s_0 \vdash \varphi$, unfolding fixed points and stopping at repeated sequents, with success conditions that tell least and greatest fixed points apart. They handle the full mu-calculus, but the tree can be large.
- **Boolean equation systems.** Andersen (1994) and later Mateescu, in the CADP toolset, write the problem as a system of Boolean equations in blocks of one fixed-point kind, and solve each block locally. This is the same idea as dependency graphs.
- **Global algorithm on the same graph.** Liu and Smolka also give a global version that computes the whole least solution in linear time, the analogue of [Emerson-Lei](/emerson-lei-algorithm/) for this setting.
- **Alternation.** Liu, Ramakrishnan and Smolka (1998) extended the local algorithm to formulas with alternating fixed points, at a higher cost. The general problem is equivalent to solving a [parity game](/parity-game/), and local game solving explores the game from one position.
- **Linear-time properties.** For LTL, the local and on-the-fly approach is the product of the system with a Büchi automaton explored by [nested depth-first search](/nested-depth-first-search/); see [on-the-fly model checking](/on-the-fly-model-checking/).
- **Parameterized and weighted dependency graphs.** Later work uses the same search for timed, weighted and probabilistic logics, with values other than 0 and 1.

## When to use it

Use local model checking when the question is about one state, usually the initial state, of a system that is given implicitly and is too large to build in full, and the answer is likely to be found in a small part of it: error detection, where a bug may be found near the start, and properties such as $\mathsf{EF}$ and $\mathsf{AG}$ on large state spaces. It is the method of explicit-state tools for branching-time logics, as [explicit-state model checking](/explicit-state-model-checking/) describes. Use a global algorithm, or [symbolic model checking](/symbolic-model-checking/), when the answer is needed for all states, when the property holds (so that the whole reachable graph is built anyway), or when the transition relation is easier to handle as a BDD than state by state.

## Pitfalls

- **Answering "no" too early.** A vertex with value $0$ is false only when the stack is empty. In the middle of the search it may still become true.
- **Least and greatest fixed points.** The least solution gives the meaning of $\mu$. Using it for $\nu X.\, \Box X$ would make false every state that has an infinite path, while the formula is true everywhere. Greatest fixed points need the dual call or a greatest-solution version of the algorithm.
- **Alternation.** For a $\nu$ subformula with a free variable bound by an outer $\mu$, the separate call is not well defined; the formula is not alternation-free, and this algorithm does not apply.
- **Deadlock states.** $\Box\psi$ is true in a state with no successor, and $\Diamond\psi$ is false; the hyperedge table gives this automatically ($\Box$ has one hyperedge with no targets). Many CTL tools instead assume a total transition relation, and the results then differ.
- **Repeated work.** Without a cache keyed by (state, subformula), separate calls for the same $\nu$ subformula from many states repeat their searches.

## Implementations

## History

Local model checking began with tableau methods. Larsen (1988) and Stirling and Walker (1989) gave proof systems that check one state of a finite system against a mu-calculus formula, and Cleaveland (1990) simplified the success conditions for the full logic. Andersen (1994) and Vergauwen and Lewi gave linear-time local algorithms for the alternation-free fragment through Boolean graphs. Liu and Smolka (1998) presented dependency graphs and the simple local algorithm on this page, with a matching global one. The approach is used in explicit-state tools for process algebras and in recent work on timed and weighted logics.

## References
