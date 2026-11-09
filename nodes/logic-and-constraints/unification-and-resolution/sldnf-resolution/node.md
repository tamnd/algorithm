---
tag: N5VQ4A
kind: algorithm
slug: sldnf-resolution
name: SLDNF resolution
aliases:
- negation as failure resolution
- SLD resolution with negation as failure
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: SLD resolution for programs with negative literals. A ground literal not A succeeds when the tree for A fails finitely. It is sound for the Clark completion but not complete in general.
solves: [first-order-theorem-proving]
model: word-ram
properties: {deterministic: true}
history:
  year: 1978
  people: [Keith L. Clark]
  note: Clark defined the negation as failure rule and the completion of a program, and proved that the rule is sound for the completion. The name SLDNF and the full theory of its trees came later, in the work of Lloyd and others.
prereqs: [sld-resolution, horn-clause, logic-programming, most-general-unifier]
see_also: [answer-substitution, warren-abstract-machine, datalog, datalog-evaluation, chronological-backtracking, refutation]
sources:
  - paper: "Keith L. Clark, Negation as failure, in Hervé Gallaire and Jack Minker (eds.), Logic and Data Bases, Plenum Press, New York, 293 to 322 (1978)"
    locator: the completed database, the equality axioms, the negation as failure rule and the proof of its soundness
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: Chapter 3 (normal programs, the completion, SLDNF resolution, soundness in Section 15, completeness results in Section 16)
  - paper: "Krzysztof R. Apt, Howard A. Blair and Adrian Walker, Towards a theory of declarative knowledge, in Jack Minker (ed.), Foundations of Deductive Databases and Logic Programming, Morgan Kaufmann, 89 to 148 (1988)"
    locator: stratified programs, the standard (perfect) model and the proof that it is a model of the completion
  - paper: "Krzysztof R. Apt and Roland N. Bol, Logic programming and negation: a survey, Journal of Logic Programming 19/20, 9 to 71 (1994)"
    locator: the sections on SLDNF resolution, floundering and the completeness results for restricted classes of programs
---

SLDNF resolution extends [SLD resolution](/sld-resolution/) to *normal programs*, whose clause bodies and queries may contain negative literals $\mathit{not}\ A$. Positive literals are resolved as in SLD resolution. A negative literal is selected only when it is ground. Then a separate, *subsidiary* tree is built for the query $\leftarrow A$: if that tree is finite and has no success, $\mathit{not}\ A$ succeeds (negation as failure); if it has a success, $\mathit{not}\ A$ fails. Clark (1978) showed that this is sound for the *completion* of the program, in which each predicate is defined by an "if and only if". SLDNF resolution is not complete for the completion, and a goal can *flounder* when only non-ground negative literals are left. Prolog uses this rule with leftmost selection and depth-first search, and adds more incompleteness and some unsoundness of its own.

## In plain words

A program states what is true. It does not list what is false. Negation as failure fills the gap with a rule: if you try every way to prove something and all of them fail after finitely many steps, then take it as false. So "a bird flies if it is not a penguin" works: try to prove that Tweety is a penguin, see the try fail, and conclude that Tweety flies. The rule only works for questions without unknowns. "Is there an X that is not a penguin?" cannot be answered by trying to prove "X is a penguin", because that proof finds Sam and says nothing about the rest.

## The problem

The input is a normal program $P$, a finite set of clauses $H \leftarrow L_1, \ldots, L_m$ where each $L_i$ is an atom or $\mathit{not}\ A$, and a query $\leftarrow L_1, \ldots, L_k$. The *completion* $\mathrm{comp}(P)$ replaces the clauses for each predicate $p$ by the formula

$$\forall \bar x\ \Big( p(\bar x) \leftrightarrow \bigvee_{i} \exists \bar y_i\, (\bar x = \bar t_i \wedge \text{body}_i) \Big),$$

one disjunct for each clause $p(\bar t_i) \leftarrow \text{body}_i$, with $\mathit{not}$ read as $\neg$. A predicate with no clauses gets $\forall \bar x\, \neg p(\bar x)$. Clark's equality axioms are added: different function symbols give different terms, function symbols are injective, and no term equals a proper subterm of itself. The task is to compute answers $\sigma$ with $\mathrm{comp}(P) \models \forall (L_1 \wedge \cdots \wedge L_k)\sigma$, or to show $\mathrm{comp}(P) \models \neg \exists (L_1 \wedge \cdots \wedge L_k)$.

## The algorithm

The procedure explores the SLDNF tree of a goal up to a depth bound $d$. It uses the *safe* leftmost computation rule: select the leftmost literal that is positive or ground. It returns the success leaves and a status: *finite* if the whole tree, with all its subsidiary trees, was explored; *cut* if the bound cut a branch; *flounder* if a goal had only non-ground negative literals.

```pseudo id=main
SLDNF-TREE(P, G, θ, d)          ▷ goal G under the substitution θ, depth bound d
L1  if G is empty then return ({θ}, finite)
L2  if d = 0 then return (∅, cut)
L3  L ← the leftmost literal of Gθ that is positive, or negative and ground
L4  if there is no such literal then return (∅, flounder)
L5  if L = not A then
L6      (S, s) ← SLDNF-TREE(P, ← A, ε, d − 1)                  ▷ the subsidiary tree
L7      if S ≠ ∅ then return (∅, finite)                         ▷ A succeeds, so not A fails
L8      if s ≠ finite then return (∅, s)                          ▷ no decision for not A
L9      return SLDNF-TREE(P, G without L, θ, d − 1)               ▷ A fails finitely, so not A succeeds
L10 S ← ∅, s ← finite
L11 for each clause of P, renamed apart, H ← B_1, …, B_m do
L12     if μ = MGU(L, H) exists then
L13         (S', s') ← SLDNF-TREE(P, G with L replaced by B_1, …, B_m, θμ, d − 1); add S' to S; s ← the worse of s and s'
L14 return (S, s)
```

The order of the statuses is finite, then cut, then flounder. A query $Q$ is run as SLDNF-TREE$(P, Q, \varepsilon, d)$. Each success leaf $\theta$, restricted to the variables of $Q$, is a computed answer. If the result is $(\emptyset, \text{finite})$, the SLDNF tree of $Q$ is *finitely failed*. Line L7 does not wait for the rest of the subsidiary tree: one success of $A$ is enough to make $\mathit{not}\ A$ fail.

## Example

Take the program

```text
bird(tweety).   bird(sam).   penguin(sam).
flies(X) ← bird(X), not penguin(X).
```

and the query $\leftarrow \mathit{flies}(X)$.

| goal | selected | action | result |
|---|---|---|---|
| $\mathit{flies}(X)$ | $\mathit{flies}(X)$ | the rule | $\mathit{bird}(X), \mathit{not}\ \mathit{penguin}(X)$ |
| $\mathit{bird}(X), \mathit{not}\ \mathit{penguin}(X)$ | $\mathit{bird}(X)$ | first fact, $X = \mathit{tweety}$ | $\mathit{not}\ \mathit{penguin}(\mathit{tweety})$ |
| $\mathit{not}\ \mathit{penguin}(\mathit{tweety})$ | the ground negative literal | subsidiary tree for $\mathit{penguin}(\mathit{tweety})$: no clause head unifies, so it fails finitely | empty: answer $X = \mathit{tweety}$ |
| $\mathit{bird}(X), \mathit{not}\ \mathit{penguin}(X)$ | $\mathit{bird}(X)$ | second fact, $X = \mathit{sam}$ | $\mathit{not}\ \mathit{penguin}(\mathit{sam})$ |
| $\mathit{not}\ \mathit{penguin}(\mathit{sam})$ | the ground negative literal | subsidiary tree for $\mathit{penguin}(\mathit{sam})$ succeeds | this branch fails |

The only answer is $X = \mathit{tweety}$, and the status is *finite*. If the body is written as $\mathit{not}\ \mathit{penguin}(X), \mathit{bird}(X)$, the safe rule still selects $\mathit{bird}(X)$ first, because $\mathit{not}\ \mathit{penguin}(X)$ is not ground. Prolog would select $\mathit{not}\ \mathit{penguin}(X)$, find that $\mathit{penguin}(X)$ succeeds with $X = \mathit{sam}$, and answer *no*, which is wrong.

## Correctness

The proofs are in the [correctness proof](proofs/correctness.md).

1. **Soundness for the completion (Clark 1978).** If $\sigma$ is a computed answer for $Q$, then $\mathrm{comp}(P) \models \forall Q\sigma$. If $Q$ has a finitely failed SLDNF tree, then $\mathrm{comp}(P) \models \neg \exists Q$. The proof is an induction on the nesting of subsidiary trees and on the depth of the tree. The "if" half of the completion justifies the success steps, as in SLD resolution, and the "only if" half with the equality axioms justifies the failures.
2. **Not complete.** For the program `p ← q.`, `p ← not q.`, `q ← q.`, the completion contains $p \leftrightarrow q \vee \neg q$, so $\mathrm{comp}(P) \models p$. But the tree for $\leftarrow q$ is infinite, so $\mathit{not}\ q$ never succeeds or fails, and both branches of $\leftarrow p$ fail to finish. No SLDNF refutation of $\leftarrow p$ exists.
3. **Floundering.** For `p(X) ← not q(X).` and `q(a).`, the query $\leftarrow p(X)$ reaches the goal $\mathit{not}\ q(X)$ and flounders. The completion implies $p(b)$, so the query has a correct answer that SLDNF cannot compute. The ground query $\leftarrow p(b)$ succeeds.
4. **Stratified programs.** If no predicate depends negatively on itself through a cycle, the program is *stratified*, and its *perfect model* (Apt, Blair and Walker 1988) is a model of $\mathrm{comp}(P)$. So by part 1, every computed answer is true in the perfect model, and every finitely failed query is false in it. The tests check exactly this on random stratified programs whose trees are finite.

Completeness does hold for restricted classes, such as allowed hierarchical programs, and for wider classes under extra conditions. Lloyd (Section 16) and Apt and Bol give the exact statements.

## Complexity

The cost of each step is that of SLD resolution: one unification and one renaming. The tree has no size bound in general, and a negative literal can need a whole subsidiary tree, which must be explored to the end to show finite failure. Whether a query has an SLDNF refutation is undecidable, as it already is for definite programs. For Datalog programs that are stratified, bottom-up evaluation of the perfect model stratum by stratum takes polynomial time for a fixed program, and it is the usual method in deductive databases.

## Properties

- **Sound for the completion.** Answers are true and failures are false in every model of $\mathrm{comp}(P)$, if $\mathrm{comp}(P)$ is consistent.
- **Incomplete.** The rule cannot reason by cases, and it gives no answer when a subsidiary tree is infinite.
- **Needs a safe rule.** Selecting a non-ground negative literal is unsound, so the rule must wait, and it may flounder.
- **Non-monotonic.** Adding a fact can turn a success into a failure: with the fact `penguin(tweety)`, the answer $X = \mathit{tweety}$ disappears.

## Variants and improvements

- **Prolog's negation.** Prolog's `\+` selects the leftmost literal even when it is not ground, and searches depth first. This is unsound for non-ground calls and incomplete because of infinite branches.
- **Constructive negation.** Chan (1988) and later work compute answers for non-ground negative literals as inequality constraints, which avoids floundering.
- **Well-founded and stable semantics.** SLG resolution with tabling computes the well-founded semantics, which gives every program a three-valued meaning. Answer set programming uses stable models and is a different, bottom-up method.
- **Allowed programs.** If every variable of a clause occurs in a positive body literal, and the same holds for the query, the safe leftmost rule never flounders.

## When to use it

Use SLDNF resolution to run logic programs top-down with negation, when each negative call is ground at the time it is selected and the subsidiary trees are finite. Datalog-style programs with stratified negation satisfy this when their recursion terminates, and many Prolog programs are written this way. For recursive programs over finite data, or when negation is not stratified, use a tabled system or bottom-up evaluation instead.

## Pitfalls

- **Unsafe negation in Prolog.** With `p(X) :- \+ q(X).` and `q(a).`, the Prolog query `?- p(X).` answers *no*, but $p(b)$ follows from the completion. Put negative literals after the literals that bind their variables.
- **Depth-first search loses answers.** For `p :- p.` and `p.`, Prolog loops on `?- p.` although the second clause is a refutation of length 1. The same happens inside a subsidiary tree, where an infinite branch blocks the decision for $\mathit{not}\ A$.
- **Reasoning by cases.** In the incompleteness example above, $p$ holds whether $q$ is true or false, but SLDNF must decide $q$ first.
- **Inconsistent completion.** For `p ← not p.`, the completion contains $p \leftrightarrow \neg p$ and has no model. Soundness then says nothing, and the SLDNF tree for $\leftarrow p$ is infinite.

## Implementations

## History

Clark (1978) introduced negation as failure, the completed database and the equality axioms, and proved soundness. Shepherdson, Lloyd and others studied completeness in the 1980s; Lloyd's book (1984 and 1987) made SLDNF resolution the standard name. Apt, Blair and Walker (1988), Van Gelder (1988) and Przymusinski (1988) introduced stratified programs and the perfect model. Kunen (1987) gave a three-valued reading of the completion. Apt and Bol (1994) surveyed the field.

## References
