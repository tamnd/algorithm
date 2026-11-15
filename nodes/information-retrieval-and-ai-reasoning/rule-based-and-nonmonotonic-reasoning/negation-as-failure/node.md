---
tag: ZRPTR9
kind: concept
slug: negation-as-failure
name: Negation as failure
aliases:
- default negation
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: The negation not p in a rule body holds when p cannot be derived. Each semantics of logic programs reads "cannot be derived" in its own way, and all of them are nonmonotonic.
prereqs: [logic-programming, closed-world-assumption, sld-resolution]
see_also: [sldnf-resolution, clark-completion, stable-model-semantics, well-founded-semantics, stratified-logic-program, datalog, nonmonotonic-reasoning, default-logic]
sources:
  - paper: doi:10.1007/978-1-4684-3384-5_11
    title: Keith L. Clark, Negation as failure, in Hervé Gallaire and Jack Minker (eds.), Logic and Data Bases, Plenum Press, New York, 293 to 322 (1978)
    locator: the negation as failure rule and the completed database
  - paper: "Krzysztof R. Apt, Howard A. Blair and Adrian Walker, Towards a theory of declarative knowledge, in Jack Minker (ed.), Foundations of Deductive Databases and Logic Programming, Morgan Kaufmann, 89 to 148 (1988)"
    locator: stratified programs and their standard model
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the reading of not as failure to derive relative to a guessed set of beliefs
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: the three-valued reading of negation through unfounded sets
  - paper: "Krzysztof R. Apt and Roland N. Bol, Logic programming and negation: a survey, Journal of Logic Programming 19/20, 9 to 71 (1994)"
    locator: the comparison of the semantics of negation in logic programs
---

Negation as failure is the reading of $\mathit{not}\ p$ in a rule body as "$p$ cannot be derived", not as "$p$ is false" in classical logic. Clark (1978) introduced it as a proof rule: $\mathit{not}\ p$ succeeds when every attempt to prove $p$ fails finitely. That procedure, with its soundness proof and its limits, is the subject of [SLDNF resolution](/sldnf-resolution/), and the restricted form used in databases, where negation applies only to relations that are already computed, is covered with [Datalog](/datalog/). This page is about the idea itself and the main ways to give it a meaning: the [completion](/clark-completion/), the perfect model of [stratified programs](/stratified-logic-program/), [stable models](/stable-model-semantics/) and the [well-founded model](/well-founded-semantics/). On some programs these readings agree, and on others they differ.

## In plain words

A timetable lists the trains that run. If a train is not in the list, you conclude that it does not run, although the list never says so. Negation as failure is this habit, written into rules: "a train is cancelled if it is not listed as running". The conclusion can change. If a new train is added to the list, an old conclusion about it goes away. Classical logic never loses a conclusion when facts are added, so this is a different kind of negation. The hard cases are rules that depend on their own negation, such as "p holds if p does not hold". Different theories give such rules different meanings, and the choice of theory is the choice of what "cannot be derived" means.

## The idea

A normal rule has the form $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$. In a [closed world](/closed-world-assumption/), a definite program (with $k = 0$ in every rule) means its least model: what is derived is true, and the rest is false. Negation as failure lets rules refer to that "rest". The trouble is that a rule body can depend on what is not derived, while what is derived depends on the rule bodies. The semantics differ in how they break this circle.

- **Finite failure and the completion.** Clark read the rules for each atom as an "if and only if" definition, the [completion](/clark-completion/), and proved that finite failure of $p$ is sound for $\neg p$ in it.
- **Stratification.** If no atom depends on its own negation through a cycle, the program is evaluated in layers, and each negation refers to a layer that is already complete (Apt, Blair and Walker 1988).
- **Stable models.** Guess a set $M$ of true atoms, read $\mathit{not}\ c$ as true exactly when $c \notin M$, and keep $M$ if the rules then derive exactly $M$ (Gelfond and Lifschitz 1988). A program can have no, one or many stable models.
- **The well-founded model.** Derive only what is forced, and make an atom false when it can only be derived through itself. The result is one three-valued model, with some atoms undefined (Van Gelder, Ross and Schlipf 1991).

The negation is *nonmonotonic*: with $p \leftarrow \mathit{not}\ q$, the program derives $p$, but after adding the fact $q$ it does not. It is also not classical: as a formula, $p \leftarrow \mathit{not}\ q$ would be $q \vee p$, which has the two minimal models $\{p\}$ and $\{q\}$, while every semantics above gives $\{p\}$ only. Answer set programming adds a second, *strong* negation for atoms that are explicitly false, next to $\mathit{not}$.

## Examples

The table gives the meaning of four small ground programs. For the completion and the stable models it lists all models; for the well-founded semantics, the true and false atoms. SLDNF resolution is run on the query $p$.

| program | completion | stable models | well-founded model | SLDNF on $p$ |
|---|---|---|---|---|
| $p \leftarrow \mathit{not}\ q$ | $\{p\}$ | $\{p\}$ | $p$ true, $q$ false | succeeds |
| $p \leftarrow \mathit{not}\ p$ | no model | none | $p$ undefined | does not terminate |
| $p \leftarrow \mathit{not}\ q$, $q \leftarrow \mathit{not}\ p$ | $\{p\}$, $\{q\}$ | $\{p\}$, $\{q\}$ | $p$, $q$ undefined | does not terminate |
| $p \leftarrow p$ | $\emptyset$, $\{p\}$ | $\emptyset$ | $p$ false | does not terminate |

The first program is stratified, and all readings agree. The second has no stable model: the guess $\{p\}$ blocks the only rule for $p$, and the guess $\emptyset$ derives $p$. The third has two stable models, while the well-founded semantics, which must give one answer, leaves both atoms undefined. The fourth shows the difference between the completion and the other readings: $p \leftrightarrow p$ allows $p$ to be true, but nothing derives it.

A classic use is a default with an exception:

```text
flies(X) ← bird(X), not abnormal(X).
abnormal(X) ← penguin(X).
bird(tweety).   bird(sam).   penguin(sam).
```

Every reading gives $\mathit{flies}(\mathit{tweety})$ and not $\mathit{flies}(\mathit{sam})$. Adding $\mathit{penguin}(\mathit{tweety})$ removes the first conclusion.

## Where it is used

- **Prolog.** The operator `\+` implements negation as finite failure, with the restrictions and the unsoundness for non-ground calls that the [SLDNF](/sldnf-resolution/) page describes.
- **Deductive databases and SQL.** Stratified negation in [Datalog](/datalog/) corresponds to `NOT EXISTS` and `EXCEPT` on relations that are computed first.
- **Answer set programming.** [Answer set programming](/answer-set-programming/) uses the stable model reading to state search problems: rules such as $p \leftarrow \mathit{not}\ q$ and $q \leftarrow \mathit{not}\ p$ make a choice.
- **Tabled Prolog systems.** [SLG resolution](/slg-resolution/) computes the well-founded model goal by goal, and terminates where SLDNF resolution loops.
- **Knowledge representation.** Defaults with exceptions, the frame problem in reasoning about actions, and the [closed-world assumption](/closed-world-assumption/) are all written with negation as failure. It is one form of [nonmonotonic reasoning](/nonmonotonic-reasoning/), and stable models correspond to the extensions of a [default theory](/default-logic/).

## References
