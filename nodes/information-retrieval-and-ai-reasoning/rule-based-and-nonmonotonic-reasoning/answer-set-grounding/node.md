---
tag: JQHNQC
kind: algorithm
slug: answer-set-grounding
name: Answer set grounding
aliases:
- ASP grounder
- intelligent grounding
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Replaces variables of a safe ASP program by constants, producing only ground rules whose bodies can be true, by semi-naive evaluation.
model: word-ram
complexity:
  vars: {r: the number of rules, m: the largest number of positive body atoms in a rule, c: the number of constants, k: the largest number of variables in a rule, d: the number of atoms in the domain}
  time: {worst: "O(r · m^2 · c^k · d^2)"}
  space: {extra: "O(m · r · c^k + d)"}
properties: {deterministic: true}
history:
  year: 2007
  people: [Martin Gebser, Torsten Schaub, Sven Thiele]
  note: Gebser, Schaub and Thiele presented the gringo grounder in 2007. Earlier grounders came with the smodels and DLV systems.
prereqs: [answer-set-programming, semi-naive-evaluation, herbrand-universe]
see_also: [grounding, datalog-evaluation, stable-model-semantics, smodels-algorithm, conflict-driven-answer-set-solving, magic-sets, gelfond-lifschitz-reduct]
sources:
  - paper: doi:10.1007/978-3-540-72200-7_24
    title: "Martin Gebser, Torsten Schaub and Sven Thiele, GrinGo: a new grounder for answer set programming, in Logic Programming and Nonmonotonic Reasoning (LPNMR 2007), Lecture Notes in Computer Science, Springer, 266 to 271 (2007)"
    locator: the gringo grounder and the class of programs it accepts
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: Chapter 4, Grounding (safety, the instantiation of rules and the simplification of the ground program)
  - paper: doi:10.1145/1149114.1149117
    title: Nicola Leone, Gerald Pfeifer, Wolfgang Faber, Thomas Eiter, Georg Gottlob, Simona Perri and Francesco Scarcello, The DLV system for knowledge representation and reasoning, ACM Transactions on Computational Logic 7(3) (2006)
    locator: the intelligent grounding module of DLV
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: stable models of a program with variables defined through its ground instances
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: the data complexity and program complexity of normal programs under the stable model semantics
---

An answer set solver works on ground programs, but answer set programs are written with variables. A *grounder* replaces the variables by constants. The full instantiation, which tries every constant for every variable, is correct but much too large, so real grounders produce only the rule instances whose positive body can be true. They find these instances by [semi-naive evaluation](/semi-naive-evaluation/), as in [Datalog](/datalog/), and then simplify the result with the atoms that are certainly true or certainly false. The output has the same [stable models](/stable-model-semantics/) as the full instantiation, but it can still be exponential in the size of a rule.

## In plain words

A rule with variables is a pattern for many rules, one for each way of filling in the variables with names from the program. Writing out every one of them is wasteful: most would talk about things that can never be true. The grounder works forward instead. It starts from the plain facts and asks which filled-in rules could fire, ignoring the "not" conditions for now. Each rule that could fire adds its conclusion to a growing list of possible facts. Then it repeats with the new facts only, so no filled-in rule is produced twice. When nothing new appears, it cleans up: conditions that are surely true are dropped, and rules that are surely blocked are deleted. The solver gets the small program that is left.

## The problem

The input is a finite normal program $P$ with variables and constants but no function symbols. Its rules have the form $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$, where the head and the body literals are atoms such as $\mathit{edge}(X, Y)$. The [Herbrand universe](/herbrand-universe/) is the set $C$ of constants of $P$. A rule is *safe* if each variable in it occurs in some positive body atom $b_i$. The *full instantiation* $G$ is the set of all ground instances of the rules over $C$, and the stable models of $P$ are by definition those of $G$ (Gelfond and Lifschitz 1988). The output is a ground program with the same stable models as $G$. Grounding is the first step before any propositional solver, such as the [smodels search](/smodels-algorithm/) or [conflict-driven solving](/conflict-driven-answer-set-solving/).

## The algorithm

```pseudo id=main
GROUND(P)
L1  if some rule of P is not safe then fail
L2  O ← ∅; Δ ← the heads of the rules with no positive body atom; emit these rules
L3  while Δ ≠ ∅ do
L4      N ← ∅
L5      for each rule r = h ← b1, …, bm, not c1, …, not cn with m ≥ 1, and each j = 1, …, m do
L6          for each substitution θ with biθ ∈ O for i < j, bjθ ∈ Δ, and biθ ∈ O ∪ Δ for i > j do
L7              emit rθ; N ← N ∪ {hθ}
L8      O ← O ∪ Δ; Δ ← N ∖ O
L9  D ← O; F ← the least model of the emitted rules that have no negative literal
L10 for each emitted rule h ← pos, not neg do
L11     if neg contains an atom of F then delete the rule        ▷ it is blocked in every stable model
L12     else replace it by h ← (pos ∖ F), not (neg ∩ D)         ▷ an atom outside D is never true
L13 return the remaining rules, without duplicates
```

Lines L2 to L8 evaluate the positive part $G^+$ of the program, with the negative literals ignored. The final $O$ is the *domain* $D$, the least model of $G^+$, which contains every atom of every stable model. At line L6, $j$ is the first position of an atom that is new in the last round: the earlier positions take only older atoms. So each pair of a rule and a substitution is found in exactly one round and at one position. Real grounders compute the join at line L6 with indexes on the bound arguments, as in a [hash join](/hash-join/); the Python code scans the atoms of each predicate.

## Example

The program describes reachability from a start node, and a guess of a colour for each reached node:

```text
edge(a, b).   edge(b, c).   start(a).
reach(X) ← start(X).
reach(Y) ← reach(X), edge(X, Y).
red(X)   ← reach(X), not green(X).
green(X) ← reach(X), not red(X).
```

The constants are $a$, $b$ and $c$, so the full instantiation has $3 + 3 + 9 + 3 + 3 = 21$ rules.

| round | emitted instances | new atoms $\Delta$ |
|---|---|---|
| 0 | the three facts | $\mathit{edge}(a, b)$, $\mathit{edge}(b, c)$, $\mathit{start}(a)$ |
| 1 | $\mathit{reach}(a) \leftarrow \mathit{start}(a)$ | $\mathit{reach}(a)$ |
| 2 | $\mathit{reach}(b) \leftarrow \mathit{reach}(a), \mathit{edge}(a, b)$, and the two colour rules for $a$ | $\mathit{reach}(b)$, $\mathit{red}(a)$, $\mathit{green}(a)$ |
| 3 | $\mathit{reach}(c) \leftarrow \mathit{reach}(b), \mathit{edge}(b, c)$, and the two colour rules for $b$ | $\mathit{reach}(c)$, $\mathit{red}(b)$, $\mathit{green}(b)$ |
| 4 | the two colour rules for $c$ | $\mathit{red}(c)$, $\mathit{green}(c)$ |
| 5 | none | none: stop |

The run emits 12 instances in 5 rounds. The definite rules give $F = \{\mathit{edge}(a, b), \mathit{edge}(b, c), \mathit{start}(a), \mathit{reach}(a), \mathit{reach}(b), \mathit{reach}(c)\}$. Line L12 removes the $\mathit{reach}$ atoms from the bodies, so the output is the six facts of $F$ and six rules such as $\mathit{red}(c) \leftarrow \mathit{not}\ \mathit{green}(c)$. It has $2^3 = 8$ stable models, one for each colouring of the three nodes, the same as the 21 rules of the full instantiation.

The output can be exponential in the size of the input. The rule $p(X_1, \ldots, X_k) \leftarrow d(X_1), \ldots, d(X_k)$ with the facts $d(a)$ and $d(b)$ has $2^k$ instances, and each of them derives a different atom, so none can be left out:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| ground rules | 4 | 6 | 10 | 18 | 34 | 66 | 130 | 258 |

## Correctness

The [correctness proof](proofs/correctness.md) has the details. First, semi-naive evaluation gives the domain $D$ and exactly the instances whose positive body lies in $D$, each once: each atom has one round in which it is new, and an instance is found in the round after the last of its body atoms became new, at the first position that holds such an atom. Second, the other instances do not matter. Every rule of a reduct $G^M$ is a rule of $G^+$, so the least model of $G^M$ lies in $D$, and a rule with a body atom outside $D$ never fires. Third, simplification keeps the stable models. Every stable model contains the least model $F$ of the definite instances and lies in $D$. For such a set $M$, a rule with $\mathit{not}\ c$, $c \in F$, is deleted by the reduct anyway, a literal $\mathit{not}\ c$ with $c \notin D$ is true, and a body atom in $F$ is true, so the reducts have the same least model.

## Complexity

A rule with $k$ variables over $c$ constants has $c^k$ instances, so a program with $r$ rules has at most $r \cdot c^k$ instances, and the example family shows that the output can need $2^k$ rules for a program of size $O(k)$. No grounder can avoid this, because the output itself is that large. For the Python code, each round, rule and position $j$ visits at most $m \cdot c^k$ partial substitutions, each visit scans at most $d$ atoms, and there are at most $d + 1$ rounds, which gives $O(r \cdot m^2 \cdot c^k \cdot d^2)$ time. The space is the stored instances plus the domain. For a fixed program, $k$ is a constant and grounding takes time polynomial in the number of facts. Deciding whether a normal program with variables has a stable model is NP-complete when the program is fixed and the facts are the input, and NEXPTIME-complete when the program is part of the input (Dantsin, Eiter, Gottlob and Voronkov 2001).

## Properties

- **Exact on the positive part.** The domain is the least model of the positive part of the program, so no atom of a stable model is missed.
- **Each instance once.** Semi-naive evaluation finds each pair of a rule and a substitution exactly once.
- **Stratified programs are solved.** For a program without negation, the output is the least model as a list of facts, so the solver has nothing left to do. Grounders that also evaluate stratified negation solve [stratified programs](/stratified-logic-program/) completely.
- **Safety is necessary.** An unsafe rule such as $p(X) \leftarrow \mathit{not}\ q(X)$ has an instance for each constant, and its meaning depends on which constants exist. Grounders reject it.

## Variants and improvements

- **Component order.** Real grounders split the program along the [strongly connected components](/strongly-connected-components/) of its predicate dependency graph and ground the components bottom-up. Atoms of finished lower components are then known exactly, so more literals can be decided.
- **Stratified negation.** If $c$ is in a lower component and is not derived, then $\mathit{not}\ c$ is true and can be dropped as soon as that component is done; if $c$ is a fact, the rule can be deleted.
- **Join order and indexes.** Choosing the order of the body atoms and indexing atoms by their bound arguments change the cost of line L6 a great deal, though not the output.
- **Function symbols and arithmetic.** With function symbols the Herbrand universe is infinite; grounders accept such programs only under conditions that make the domain finite, and they evaluate arithmetic during grounding.
- **Goal-directed grounding.** Methods in the spirit of [magic sets](/magic-sets/) ground only the part of the program that a query needs.

## When to use it

Every answer set system grounds first. Write the program so that the grounding is small: keep the number of variables per rule low, add domain predicates that restrict the variables, and avoid rules that join many large predicates. When the ground program is too large in practice, the problem usually lies in such a rule, not in the solver.

## Pitfalls

- **Grounding bottleneck.** The output grows as $c^k$. A rule with four variables over 1000 constants already has $10^{12}$ instances, which no system can write out.
- **Unsafe rules.** A variable that occurs only in the head, or only under $\mathit{not}$, has no positive atom to bind it. Add a domain predicate to the body.
- **The domain is an overestimate.** An atom in $D$ is not necessarily true in a stable model, because $D$ ignores the negative literals. Only atoms of $F$ are certain.
- **Simplification is semantic, not syntactic.** Dropping $\mathit{not}\ c$ is correct only for $c$ outside the domain. Dropping it because no rule for $c$ was emitted yet, in the middle of the evaluation, is wrong.
- **Duplicates.** Two rules of the program can have the same instance. This is harmless, but the counts of instances and of output rules then differ.

## Implementations

## History

Gelfond and Lifschitz (1988) defined stable models of programs with variables through the ground instances. The lparse grounder of the smodels system and the grounder of DLV (Leone et al. 2006) introduced domain restrictions and intelligent grounding, which produce only the relevant instances. Gebser, Schaub and Thiele (2007) presented the gringo grounder, which accepts a larger class of programs. Its later versions are part of the clingo system, and like the method on this page they evaluate the positive part of the program bottom-up, in the manner of Datalog engines.

## References
