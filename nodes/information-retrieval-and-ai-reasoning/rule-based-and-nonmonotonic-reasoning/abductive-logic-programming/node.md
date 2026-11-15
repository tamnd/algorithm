---
tag: XQ9SQ0
kind: model
slug: abductive-logic-programming
name: Abductive logic programming
aliases:
- ALP
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Extends logic programs with abducible predicates and integrity constraints, so a query is answered by hypotheses that explain it.
prereqs: [abductive-reasoning, stable-model-semantics, negation-as-failure]
see_also: [answer-set-programming, choice-rule, consistency-based-diagnosis, sldnf-resolution, hitting-set, assumption-based-truth-maintenance, default-logic, stable-model-np-completeness]
sources:
  - paper: doi:10.1093/logcom/2.6.719
    title: Antonis C. Kakas, Robert A. Kowalski and Francesca Toni, Abductive logic programming, Journal of Logic and Computation 2(6), 719 to 770 (1992)
    locator: the definition of abductive frameworks with abducibles and integrity constraints, generalized stable models, and the survey of proof procedures
  - paper: doi:10.1016/s0743-1066(97)00026-5
    title: Tze Ho Fung and Robert Kowalski, The IFF proof procedure for abductive logic programming, Journal of Logic Programming 33(2), 151 to 165 (1997)
    locator: the IFF proof procedure and its soundness with respect to the completion
  - paper: doi:10.1016/s0743-1066(97)00074-5
    title: Marc Denecker and Danny De Schreye, SLDNFA, an abductive procedure for abductive logic programs, Journal of Logic Programming 34(2), 111 to 167 (1998)
    locator: the SLDNFA procedure for programs with abducible predicates
  - paper: "Thomas Eiter, Georg Gottlob and Nicola Leone, Abduction from logic programs, semantics and complexity, Theoretical Computer Science 189(1-2), 129 to 177 (1997)"
    locator: the complexity of abduction from logic programs under the stable and other semantics
  - paper: doi:10.1145/200836.200838
    title: Thomas Eiter and Georg Gottlob, The complexity of logic-based abduction, Journal of the ACM 42(1), 3 to 42 (1995)
    locator: the complexity of propositional abduction, including the Horn case
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models used for generalized stable models
---

Abductive logic programming (ALP) adds hypotheses to a logic program. Some atoms are declared *abducible*: no rule defines them, and the reasoner may assume them. A query is answered by a set of abducibles that, added to the program, makes the query true and keeps a set of integrity constraints satisfied. Kakas, Kowalski and Toni (1992) surveyed the framework and its semantics, and it is the logic programming form of [abductive reasoning](/abductive-reasoning/), with [negation as failure](/negation-as-failure/) in the rules.

## The machine

An *abductive framework* is a triple $\langle P, A, IC \rangle$ (Kakas, Kowalski and Toni 1992).

- $P$ is a normal logic program, a set of rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$.
- $A$ is a set of *abducible* atoms (or predicates, whose ground atoms are abducible). Usually no abducible is the head of a rule in $P$, so the program says nothing about them.
- $IC$ is a set of *integrity constraints*. Here they are denials $\leftarrow l_1, \ldots, l_r$ over literals with $\mathit{not}$, which a model satisfies when not all $l_i$ hold.

The semantics used on this page is that of *generalized stable models*. For $\Delta \subseteq A$, a set $M$ of atoms is a generalized stable model of $\langle P, A, IC \rangle$ for $\Delta$ if $M$ is a [stable model](/stable-model-semantics/) of $P \cup \Delta$, where each element of $\Delta$ is added as a fact, and $M$ satisfies every constraint of $IC$. Other semantics replace stable models by the completion, as in the IFF procedure (Fung and Kowalski 1997), or by the well-founded model.

This is the propositional case. With variables, $P$, $A$ and $IC$ stand for their ground instances over the Herbrand universe, as for normal programs.

## What it counts

An *observation* or query is a set $G$ of ground literals. A set $\Delta \subseteq A$ is an *abductive explanation* of $G$ if some generalized stable model $M$ for $\Delta$ satisfies $G$. This is the credulous reading; the sceptical reading asks that every such model satisfies $G$ and that one exists. An explanation is *minimal* if no proper subset is an explanation. Abduction answers "why?" with a set of hypotheses, while deduction answers "is it true?" with a proof.

*Example.* Let $P$ be the four rules $\mathit{wet} \leftarrow \mathit{rain}$, $\mathit{wet} \leftarrow \mathit{sprinkler}$, $\mathit{puddle} \leftarrow \mathit{rain}$ and $\mathit{dry\_road} \leftarrow \mathit{not}\ \mathit{rain}$, let $A = \{\mathit{rain}, \mathit{sprinkler}\}$, and let $IC$ be the single constraint $\leftarrow \mathit{sprinkler}, \mathit{pump\_off}$.

| Observation | Extra fact | Explanations | Minimal explanations |
| --- | --- | --- | --- |
| $\mathit{wet}$ | none | $\{\mathit{rain}\}$, $\{\mathit{sprinkler}\}$, $\{\mathit{rain}, \mathit{sprinkler}\}$ | $\{\mathit{rain}\}$, $\{\mathit{sprinkler}\}$ |
| $\mathit{wet}$ | $\mathit{pump\_off}$ | $\{\mathit{rain}\}$ | $\{\mathit{rain}\}$ |
| $\mathit{wet}, \mathit{dry\_road}$ | none | $\{\mathit{sprinkler}\}$ | $\{\mathit{sprinkler}\}$ |
| $\mathit{wet}, \mathit{dry\_road}$ | $\mathit{pump\_off}$ | none | none |

For $\Delta = \{\mathit{rain}\}$ the model is $\{\mathit{puddle}, \mathit{rain}, \mathit{wet}\}$, and for $\Delta = \{\mathit{sprinkler}\}$ it is $\{\mathit{dry\_road}, \mathit{sprinkler}, \mathit{wet}\}$. The third row shows the effect of negation as failure: adding the observation $\mathit{dry\_road}$ removes the explanation $\{\mathit{rain}\}$, because assuming rain blocks the rule for $\mathit{dry\_road}$. The second row shows the effect of a constraint: the new fact $\mathit{pump\_off}$ removes every explanation with $\mathit{sprinkler}$.

Points to watch when using the relation:

- **Non-minimal explanations.** Supersets of an explanation are often explanations too, as $\{\mathit{rain}, \mathit{sprinkler}\}$ is in the first row. Applications usually ask for minimal ones, which can be many.
- **Explanations are not monotone.** With negation in $P$, a superset of an explanation need not be an explanation, and more observations can remove explanations, as in the third row.
- **Abducibles with rules.** If an abducible is also the head of a rule, the distinction between assuming and deriving it is lost. Frameworks rename it with a new abducible and a rule.
- **Integrity constraints are not rules.** A constraint never derives an atom; it only rejects models. A missing rule cannot be repaired by a constraint.

## Relation to other models

- **Answer set programming.** Replace each abducible $a$ by a [choice rule](/choice-rule/) $\{a\} \leftarrow$, add $IC$ as constraints, and add $\leftarrow \mathit{not}\ g$ for each atom $g$ of $G$ and $\leftarrow g$ for each literal $\mathit{not}\ g$ of $G$. The answer sets of the result are the generalized stable models that satisfy $G$, and their abducible parts are the explanations, so an [ASP](/answer-set-programming/) solver computes explanations. Minimal explanations need minimization by subset.
- **Proof procedures.** Top-down procedures extend [SLDNF resolution](/sldnf-resolution/): a selected abducible goal is added to $\Delta$, and the constraints are checked against it. Examples are the IFF procedure (Fung and Kowalski 1997), which is sound for the completion semantics, and SLDNFA (Denecker and De Schreye 1998).
- **Logic-based abduction.** In the propositional abduction of Eiter and Gottlob (1995), the theory is a set of clauses and an explanation must be consistent with it and entail the observation. ALP replaces classical entailment by the stable model semantics, so negation as failure and defaults are available.
- **Diagnosis.** In [consistency-based diagnosis](/consistency-based-diagnosis/) the hypotheses are abnormal components and a diagnosis is a minimal [hitting set](/hitting-set/) of conflicts. With abducibles $\mathit{ab}(c)$ and rules that describe the normal behaviour of each component, an ALP framework expresses the same task.
- **Default reasoning.** Hypotheses that are assumed unless they lead to inconsistency play the role of defaults, as in [default logic](/default-logic/), and the [ATMS](/assumption-based-truth-maintenance/) records which sets of assumptions derive each atom.

## Known results in the model

- **Explanation existence is NP-complete.** For finite propositional frameworks with a normal program under generalized stable models, deciding whether $G$ has an explanation is NP-complete. A certificate is a pair $(\Delta, M)$, checked in polynomial time by the reduct test of [stable models](/stable-model-np-completeness/). Hardness holds already with $A$, $G$ and $IC$ empty, since then $\emptyset$ is an explanation exactly when $P$ has a stable model. Eiter, Gottlob and Leone (1997) classify the complexity of abduction from logic programs under the stable and other semantics, for existence, relevance and necessity of hypotheses.
- **Horn theories.** For propositional Horn theories with constraints, deciding whether an explanation exists is NP-complete, and for definite Horn theories without constraints it is polynomial (Eiter and Gottlob 1995). In the definite case, $A$ itself is an explanation whenever any set is one, so one least model computation decides it.
- **Proof procedures.** Fung and Kowalski (1997) prove the soundness of the IFF procedure with respect to the completion semantics, and Denecker and De Schreye (1998) prove soundness and completeness results for SLDNFA with respect to a completion semantics. These results do not cover the generalized stable model semantics.
- **Negation as failure is abduction.** Kakas, Kowalski and Toni (1992) describe how $\mathit{not}\ p$ can be read as an abducible $p^*$ with the constraints $\leftarrow p, p^*$ and a requirement that one of $p$ and $p^*$ holds. Under this reading the stable models of a normal program correspond to certain abductive solutions.

## References
