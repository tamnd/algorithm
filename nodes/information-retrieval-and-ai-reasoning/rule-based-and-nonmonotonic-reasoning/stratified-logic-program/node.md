---
tag: 95QH65
kind: definition
slug: stratified-logic-program
name: Stratified logic program
aliases:
- stratified negation
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: A logic program is stratified when no predicate depends on its own negation. Such a program has one standard model, computed layer by layer, and every major semantics agrees on it.
prereqs: [negation-as-failure, datalog, strongly-connected-components]
see_also: [datalog-evaluation, semi-naive-evaluation, stable-model-semantics, well-founded-semantics, splitting-set-theorem, tarjan-scc, topological-sort, clark-completion]
sources:
  - paper: "Krzysztof R. Apt, Howard A. Blair and Adrian Walker, Towards a theory of declarative knowledge, in Jack Minker (ed.), Foundations of Deductive Databases and Logic Programming, Morgan Kaufmann, 89 to 148 (1988)"
    locator: the definition of stratification and the standard model, and its independence of the stratification
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the result that a stratified program has exactly one stable model, its standard model
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: the result that the well-founded model of a stratified program is total and equals its standard model
  - paper: "Krzysztof R. Apt and Roland N. Bol, Logic programming and negation: a survey, Journal of Logic Programming 19/20, 9 to 71 (1994)"
    locator: the sections on stratified and locally stratified programs
---

A stratified logic program is a normal program whose predicates can be put in layers so that each predicate depends positively on predicates of its own or lower layers and negatively only on predicates of strictly lower layers. Apt, Blair and Walker (1988) showed that such a program has one natural model, the standard (or perfect) model, which does not depend on the choice of layers. The evaluation of stratified [Datalog](/datalog/) in databases, stratum by stratum with [semi-naive evaluation](/semi-naive-evaluation/), is on the Datalog pages. This page gives the definition for general logic programs and its place among the semantics of [negation as failure](/negation-as-failure/): it is the class on which they all agree.

## Definition

The *dependency graph* of a program $P$ has a vertex for each predicate and an edge from $p$ to $q$ for each rule with head predicate $p$ and $q$ in its body. The edge is *positive* if $q$ occurs in a positive literal and *negative* if it occurs under $\mathit{not}$; an edge can be both.

A *stratification* of $P$ is a map $\sigma$ from the predicates to the natural numbers such that, for each rule with head predicate $p$,

- $\sigma(q) \le \sigma(p)$ for each predicate $q$ in a positive body literal, and
- $\sigma(q) < \sigma(p)$ for each predicate $q$ in a negative body literal.

$P$ is *stratified* if it has a stratification. Equivalently, no cycle of the dependency graph contains a negative edge, which can be tested in [linear time](/linear-time/) by computing the [strongly connected components](/strongly-connected-components/) and checking that no negative edge joins two vertices of the same component.

Let $P_i$ be the rules whose head predicate has stratum $i$. The *standard model* is $M_0 = \emptyset$ and $M_{i+1}$ the least set that contains $M_i$ and is closed under the rules of $P_i$, with each $\mathit{not}\ q(\vec{t})$ read as $q(\vec{t}) \notin M_i$. This reading is fixed while $P_i$ is evaluated, because $q$ lies in a lower stratum. For a finite number of strata the last $M_i$ is the standard model.

A program is *locally stratified* (Przymusinski) if the same condition holds for its ground instance, with ground atoms in place of predicates and an ordinal-valued $\sigma$.

## Examples and non-examples

- **Stratified.** Reachability in a graph and its complement:

  ```text
  reach(X, Y) ← edge(X, Y).
  reach(X, Y) ← edge(X, Z), reach(Z, Y).
  unreach(X, Y) ← node(X), node(Y), not reach(X, Y).
  ```

  The strata are $\{\mathit{edge}, \mathit{node}\}$ at 0, $\mathit{reach}$ at 0 or 1, and $\mathit{unreach}$ above $\mathit{reach}$. The recursion through $\mathit{reach}$ is positive.
- **Stratified.** $\{p \leftarrow \mathit{not}\ q,\ r \leftarrow p,\ r \leftarrow r\}$ with $\sigma(q) = 0$ and $\sigma(p) = \sigma(r) = 1$. The standard model is $\{p, r\}$.
- **Not stratified.** $\{p \leftarrow \mathit{not}\ q,\ q \leftarrow \mathit{not}\ p\}$: the cycle $p \to q \to p$ has negative edges. It has two stable models.
- **Not stratified.** $\{p \leftarrow \mathit{not}\ p\}$: a negative self loop.
- **Locally stratified, not stratified.** $\mathit{even}(0)$, $\mathit{even}(s(X)) \leftarrow \mathit{not}\ \mathit{even}(X)$. The predicate $\mathit{even}$ depends negatively on itself, but each ground atom $\mathit{even}(s^{n+1}(0))$ depends only on $\mathit{even}(s^n(0))$.
- **Not locally stratified.** The game $\mathit{win}(X) \leftarrow \mathit{move}(X, Y), \mathit{not}\ \mathit{win}(Y)$ on a graph with a cycle: the ground atoms on the cycle depend negatively on each other. The [well-founded semantics](/well-founded-semantics/) leaves them undefined.

## Related definitions

- **Agreement of the semantics.** For a stratified program, the standard model is the unique [stable model](/stable-model-semantics/) (Gelfond and Lifschitz 1988) and the [well-founded model](/well-founded-semantics/), which is then total (Van Gelder, Ross and Schlipf 1991). It is also a model of the [completion](/clark-completion/), but the completion can have other models, as $\{p \leftarrow p\}$ shows.
- **Positive and definite programs.** A program without negation is stratified with one stratum, and its standard model is the least model.
- **Splitting.** The strata form a chain of splitting sets, so the [splitting set theorem](/splitting-set-theorem/) reduces the stable models of a stratified program to one least model per layer.
- **Stratified Datalog.** Restricted to function-free programs with a finite database, this is the stratified negation of [Datalog](/datalog/), evaluated in the order of a [topological sort](/topological-sort/) of the components.

## References
