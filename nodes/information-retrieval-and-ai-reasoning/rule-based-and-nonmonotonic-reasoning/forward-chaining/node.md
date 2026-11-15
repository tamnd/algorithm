---
tag: R9P28Z
kind: algorithm
slug: forward-chaining
name: Forward chaining
aliases:
- data-driven inference
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: intro
summary: Start from the known facts, find each rule whose conditions all match facts, add its conclusion, and repeat until no rule adds a new fact or the goal appears.
solves: [datalog-evaluation]
model: word-ram
complexity:
  vars: {n: the number of facts in the least model, r: the number of rules, m: the largest number of conditions in a rule, a: the largest arity of a fact}
  time: {worst: O(r m a n^m)}
  space: {extra: O(a n)}
properties: {deterministic: true, monotone: true}
history:
  year: 1972
  people: [Allen Newell, Herbert A. Simon]
  note: Newell and Simon used production systems, sets of condition and action rules that fire forward from the data in working memory, as models of human problem solving. Forward chaining as bottom-up inference over definite clauses has no single inventor.
prereqs: [horn-clause, production-system]
see_also: [backward-chaining, horn-sat-forward-chaining, semi-naive-evaluation, datalog, rete-algorithm, treat-algorithm, conflict-resolution-strategy, sld-resolution]
sources:
  - book: isbn:9780136042594
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, third edition, Prentice Hall (2010)
    locator: Chapter 7 (forward chaining for propositional definite clauses) and Chapter 9 (forward chaining with variables)
  - book: isbn:9780134454030
    title: Allen Newell and Herbert A. Simon, Human Problem Solving, Prentice-Hall (1972)
    locator: the chapters on production systems
  - book: isbn:9780201106473
    title: Lee Brownston, Robert Farrell, Elaine Kant and Nancy Martin, Programming Expert Systems in OPS5, Addison-Wesley (1985)
    locator: the chapters on the recognize-act cycle and forward chaining in OPS5
  - paper: "William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)"
    locator: the linear-time forward algorithm for the propositional case
---

Forward chaining is the inference method of data-driven rule systems. It starts from the facts in a working memory, finds every rule whose conditions all match facts, adds the conclusion of each such rule as a new fact, and repeats until no rule gives a new fact or a goal fact appears. This page treats it in the setting of [production systems](/production-system/) and expert systems: rules with pattern variables, a working memory that grows, and the set of matching rule instances (the *conflict set*) that the system must find again after each change. The propositional case, with its linear-time counter algorithm, is on [Horn-SAT forward chaining](/horn-sat-forward-chaining/). The database view, with relations and rounds of joins, is on [semi-naive evaluation](/semi-naive-evaluation/). The goal-directed opposite is [backward chaining](/backward-chaining/).

## In plain words

You have a list of things you know and a list of rules of the form "if these things are true, then that thing is true too". Go through what you know. Each time a rule has all of its "if" parts in your list, write its "then" part at the end of the list, unless it is there already. Each new entry can make more rules apply, so you keep going until nothing new comes out. The list you end with holds everything that the rules let you conclude, and nothing more. If you only want to know one thing, you can stop as soon as it appears. The order in which you use the rules does not change the final list, as long as the rules only add things.

## The problem

A *fact* is a ground atom $p(c_1, \ldots, c_k)$. A *rule* is a definite clause $h \leftarrow b_1, \ldots, b_m$ whose atoms may contain variables. The rule is *safe* when each variable of $h$ occurs in some $b_j$. For a finite set $P$ of safe rules and a finite set $F$ of facts, the immediate consequence operator is

$$T(I) = F \cup \{ h\theta : (h \leftarrow b_1, \ldots, b_m) \in P,\ \theta \text{ ground},\ b_1\theta, \ldots, b_m\theta \in I \}.$$

$T$ is monotone, so it has a least fixed point $M = \bigcup_{k \ge 0} T^k(\emptyset)$, the *least model* of $P \cup F$. A ground atom $g$ follows from $P \cup F$ exactly when $g \in M$. This is the semantics of a [Datalog](/datalog/) program, and of a [Horn clause](/horn-clause/) set in the propositional case.

The task is to compute $M$, or to decide whether $g \in M$ for a goal $g$. Each match of a rule against facts is an *instantiation* $(\rho, \theta)$; the set of instantiations whose head is new is the conflict set of the rule system.

## The algorithm

The working memory $W$ holds the facts found so far and the agenda $Q$ holds the facts that have not yet been used to match rules. Each new fact is used once: it is matched against each condition of each rule, and the other conditions are joined with the facts already in $W$.

```pseudo id=main
FORWARD-CHAIN(P, F, g)          ▷ rules P, facts F, goal g (or none)
L1  W ← ∅, Q ← an empty queue
L2  for each fact f of F, and each head f of a rule of P with an empty body do
L3      if f ∉ W then
L4          add f to W and to the end of Q; if f = g then return true
L5  while Q is not empty do
L6      f ← remove the first fact of Q
L7      for each rule h ← b_1, …, b_m of P and each i in 1 .. m do
L8          if b_i matches f with the binding β then
L9              for each extension θ of β that matches every b_j with j ≠ i to a fact of W do
L10                 if hθ ∉ W then
L11                     add hθ to W and to the end of Q; if hθ = g then return true
L12 return false
```

When the call returns false, $W$ is the least model. Line L9 is a join: it binds the variables of the other conditions one condition at a time, the way a [nested loop join](/nested-loop-join/) does. A rule system with conflict resolution collects the instantiations of lines L9 to L11 into a conflict set and fires them one at a time in the order that its [conflict resolution strategy](/conflict-resolution-strategy/) gives.

## Example

Take the rules

$$\begin{aligned} R_1 &: \mathit{ancestor}(x, y) \leftarrow \mathit{parent}(x, y) \\ R_2 &: \mathit{ancestor}(x, z) \leftarrow \mathit{parent}(x, y), \mathit{ancestor}(y, z) \end{aligned}$$

and the facts $\mathit{parent}(\mathit{ann}, \mathit{bob})$ and $\mathit{parent}(\mathit{bob}, \mathit{cat})$, with no goal.

| step | fact taken from $Q$ | matches | new facts |
|---|---|---|---|
| 1 | $\mathit{parent}(\mathit{ann}, \mathit{bob})$ | $R_1$; $R_2$ condition 1, but no $\mathit{ancestor}(\mathit{bob}, z)$ in $W$ yet | $\mathit{ancestor}(\mathit{ann}, \mathit{bob})$ |
| 2 | $\mathit{parent}(\mathit{bob}, \mathit{cat})$ | $R_1$; $R_2$ condition 1, but no $\mathit{ancestor}(\mathit{cat}, z)$ | $\mathit{ancestor}(\mathit{bob}, \mathit{cat})$ |
| 3 | $\mathit{ancestor}(\mathit{ann}, \mathit{bob})$ | $R_2$ condition 2 with $y = \mathit{ann}$, but no $\mathit{parent}(x, \mathit{ann})$ | none |
| 4 | $\mathit{ancestor}(\mathit{bob}, \mathit{cat})$ | $R_2$ condition 2 with $y = \mathit{bob}$, joined with $\mathit{parent}(\mathit{ann}, \mathit{bob})$ | $\mathit{ancestor}(\mathit{ann}, \mathit{cat})$ |
| 5 | $\mathit{ancestor}(\mathit{ann}, \mathit{cat})$ | $R_2$ condition 2 with $y = \mathit{ann}$, no partner | none |

The agenda is empty after step 5, and $W$ holds the two parent facts and three ancestor facts, which is the least model. With the goal $\mathit{ancestor}(\mathit{bob}, \mathit{cat})$ the run stops in step 2, after two rule firings.

## Correctness

The [correctness proof](proofs/correctness.md) shows three facts. Every fact in $W$ is in $M$ (soundness, by induction on the order of addition). Each fact enters the agenda at most once, so the run stops. When the agenda is empty, $W$ is closed under every ground rule instance: for an instance whose body facts are all in $W$, look at the body fact that left the agenda last; at that moment the other body facts were in $W$, so line L9 found the instance. A closed set that contains $F$ contains $M$, so $W = M$. The proof uses no property of the agenda order, so any order of the queue and of the rules gives the same $M$.

## Complexity

Each of the $n$ facts of $M$ leaves the agenda once. For each such fact, each of the $r$ rules and each of its at most $m$ conditions, the join at line L9 tries at most $n^{m-1}$ tuples of facts, and each match costs $O(a)$. The total time is $O(r\, m\, a\, n^m)$, and the space for $W$ and $Q$ is $O(a\, n)$.

For a fixed rule set, $n$ is at most the number of ground atoms over the $c$ constants of the input, which is polynomial in $c$. So the *data complexity*, with the rules fixed, is polynomial, and deciding $g \in M$ is P-complete. In *combined complexity*, with the rules part of the input, $n$ can be exponential in the size of the rules, and the problem is EXPTIME-complete; the [Datalog evaluation](/datalog-evaluation/) page gives the results. Even one rule application is hard in combined complexity: finding the matches of a single rule body is the conjunctive query problem, which is [NP-complete](/np-complete/). In the propositional case there are no variables, and the counter method of [Horn-SAT forward chaining](/horn-sat-forward-chaining/) runs in time linear in the size of the rules.

## Properties

- **Monotone.** Facts are only added. Each fact in $W$ stays true for the rest of the run.
- **Order independent.** For definite rules, the final $W$ does not depend on the order of the agenda or of the rules. This fails as soon as rules can delete facts, as in OPS5.
- **Complete for ground goals.** Every atom of the least model is found, so every ground atom that follows from the rules is derived.
- **Not goal directed.** Without a goal, the run computes every consequence, including the many that are not relevant to a question.

## Variants and improvements

- **Counter based propositional chaining.** Keep for each rule the number of body atoms not yet true, and fire the rule when the counter reaches zero. This is [Horn-SAT forward chaining](/horn-sat-forward-chaining/), linear in the input size.
- **Semi-naive evaluation.** Work in rounds and join only with at least one fact from the last round. This is the same idea as the agenda, in the language of relations; see [semi-naive evaluation](/semi-naive-evaluation/).
- **Incremental matching.** A production system keeps the conflict set between cycles and updates it after each change of the working memory. The [Rete algorithm](/rete-algorithm/) stores partial matches in a network; the [TREAT algorithm](/treat-algorithm/) stores only the matches of single conditions and recomputes the joins.
- **Goal-directed bottom-up evaluation.** The [magic sets](/magic-sets/) rewriting adds conditions so that forward chaining only derives facts relevant to a query.
- **Rules with actions.** In OPS5 and CLIPS a rule can also remove or modify facts. The run is then a sequence of recognize-act cycles, and the [conflict resolution strategy](/conflict-resolution-strategy/) decides the result.

## When to use it

Use forward chaining when new data arrives and the system must react to it, as in monitoring, configuration and business rule systems. It also fits when most consequences of the facts are needed anyway, or when there are many possible goals. Use [backward chaining](/backward-chaining/) when there is one question and most of the rules are irrelevant to it.

## Pitfalls

- **Unsafe rules.** A head variable that is not in the body gives infinitely many or non-ground conclusions. Reject such rules, as the implementation does.
- **Function symbols.** With terms such as $s(x)$ the least model can be infinite and the run does not stop. Forward chaining as given here is for function-free rules.
- **Duplicate work.** Without the agenda, a naive loop that rematches every rule against the whole memory after each new fact repeats the old matches again and again.
- **Join order.** The join at line L9 is cheap or expensive depending on the order of the conditions. A condition that binds no variable of the others makes a cross product.
- **Negation.** A rule with a negated condition cannot fire safely before all facts that the condition depends on are known. Use a [stratified](/stratified-logic-program/) order, or a semantics such as the [well-founded semantics](/well-founded-semantics/).

## Implementations

## History

Post (1943) defined [canonical systems](/post-canonical-system/), the first formal systems built from productions. Newell and Simon (1972) used production systems that fire forward from the data in working memory as models of human problem solving, and OPS5 (Forgy 1981) and its successors made forward chaining the standard control method of rule-based expert systems. In logic programming the same computation is bottom-up evaluation, the least fixed point construction of van Emden and Kowalski (1976). Dowling and Gallier (1984) gave the linear-time propositional algorithm.

## References
