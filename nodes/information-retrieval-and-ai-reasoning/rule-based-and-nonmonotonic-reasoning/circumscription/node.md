---
tag: 8AEYF7
kind: model
slug: circumscription
name: Circumscription
aliases:
- McCarthy circumscription
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Entails what holds in all models that minimize the extension of chosen predicates, such as abnormality, with others fixed or varying.
prereqs: [nonmonotonic-reasoning]
see_also: [default-logic, closed-world-assumption, yale-shooting-problem, system-p, frame-problem, consistency-based-diagnosis, default-logic-complexity]
sources:
  - paper: doi:10.1016/0004-3702(80)90011-9
    title: John McCarthy, Circumscription, a form of non-monotonic reasoning, Artificial Intelligence 13(1-2), 27 to 39 (1980)
    locator: the circumscription schema for a predicate and its model-theoretic reading as truth in all minimal models
  - paper: doi:10.1016/0304-3975(93)90073-3
    title: Thomas Eiter and Georg Gottlob, Propositional circumscription and extended closed-world reasoning are Pi2P-complete, Theoretical Computer Science 114(2), 231 to 245 (1993)
    locator: the main theorem (inference from propositional circumscription with minimized, fixed and varying atoms is Pi2P-complete); addendum in Theoretical Computer Science 118, 315 (1993), doi:10.1016/0304-3975(93)90113-8
  - paper: "Marco Cadoli, The complexity of model checking for circumscriptive formulae, Information Processing Letters 44(3), 113 to 118 (1992)"
    locator: the coNP-completeness of deciding whether a model is minimal
  - paper: doi:10.1016/0004-3702(87)90043-9
    title: Steve Hanks and Drew McDermott, Nonmonotonic logic and temporal projection, Artificial Intelligence 33(3), 379 to 412 (1987)
    locator: the Yale shooting scenario and its two minimal models under circumscription of abnormality
---

Circumscription is the logic of "nothing is abnormal unless it has to be". McCarthy (1980) proposed it to formalize common-sense rules such as "birds fly": write $\mathit{bird} \wedge \neg\mathit{ab} \supset \mathit{flies}$ and then keep only the models in which the predicate $\mathit{ab}$ is as small as the facts allow. A formula follows by circumscription when it is true in all these minimal models. Adding facts can make more things abnormal and so remove conclusions, which makes the logic nonmonotonic. In the propositional case, inference is $\Pi_2^p$-complete (Eiter and Gottlob 1993).

## The machine

For a logic, the machine is its syntax and its semantics. This section gives the propositional case, which is the one with exact complexity results. McCarthy's original form is first-order, with the minimization written as a second-order axiom.

**Syntax.** An input is a finite set $A$ of propositional formulas and a partition of its atoms into three sets:

- $P$, the atoms to *minimize* (typically the abnormality atoms),
- $Z$, the atoms that may *vary* during the minimization,
- $Q$, the atoms that stay *fixed*.

The circumscription is written $\mathrm{Circ}(A; P; Z)$.

**Semantics.** Identify a model with the set of atoms that it makes true. For two models $M$ and $N$ of $A$, write $M <_{P;Z} N$ when

$$M \cap Q = N \cap Q \quad\text{and}\quad M \cap P \subsetneq N \cap P.$$

The atoms of $Z$ may differ freely. A model $M$ of $A$ is $(P;Z)$-*minimal* when no model $N$ of $A$ has $N <_{P;Z} M$. The models of $\mathrm{Circ}(A; P; Z)$ are the $(P;Z)$-minimal models of $A$. In the first-order case the same condition is the second-order formula

$$A(P, Z) \wedge \neg \exists P' \exists Z' \bigl(A(P', Z') \wedge P' < P\bigr),$$

where $P' < P$ says that the predicates $P'$ have strictly smaller extensions than $P$.

With finitely many atoms the order is well-founded, so every model of $A$ lies above a minimal one. Thus $\mathrm{Circ}(A; P; Z)$ is consistent whenever $A$ is.

## What it counts

The central task is **inference**: given $A$, $P$, $Z$ and a formula $\varphi$, decide whether $\varphi$ is true in every $(P;Z)$-minimal model of $A$, written $\mathrm{Circ}(A; P; Z) \models \varphi$. The secondary task is **model checking**: decide whether a given model of $A$ is minimal. Costs are measured as usual for propositional reasoning, in the size of $A$ and $\varphi$, with SAT as the basic oracle.

## Relation to other models

- **Classical logic.** Every model of the circumscription is a model of $A$, so circumscription only adds conclusions: $\mathrm{Th}(A) \subseteq \mathrm{Th}(\mathrm{Circ}(A;P;Z))$.
- **[Closed-world assumption](/closed-world-assumption/).** Minimizing all atoms with $Z = Q = \emptyset$ is minimal-model reasoning. For a set of Horn clauses it gives the unique least model, which is what the CWA gives. For $A = \{a \vee b\}$ the CWA adds $\neg a$ and $\neg b$ and becomes inconsistent, while circumscription gives the two minimal models $\{a\}$ and $\{b\}$ and so concludes $\neg(a \wedge b)$. Extended closed-world reasoning is propositional circumscription under another name, which is why Eiter and Gottlob treat both together.
- **[Default logic](/default-logic/).** Default logic gives several extensions and lets the reasoner choose, while circumscription always gives one theory. The default $\mathit{bird} : \mathit{flies} / \mathit{flies}$ and the circumscription of $\mathit{ab}$ in $\mathit{bird} \wedge \neg\mathit{ab} \supset \mathit{flies}$ draw the same conclusions on simple inputs, and skeptical default reasoning and circumscription agree on the Nixon diamond below. They do not agree in general.
- **Preferential models.** For a fixed $A$, $P$ and $Z$, define $\alpha \mathrel{|\!\sim} \beta$ to mean $\mathrm{Circ}(A \cup \{\alpha\}; P; Z) \models \beta$. The models of $A$, ordered by $<_{P;Z}$, form a preferential model in which each state is a model, and the order is smooth because it is a strict partial order on a finite set. So this relation satisfies all the rules of [System P](/system-p/). It need not satisfy Rational Monotonicity, because the order is not ranked.
- **[Stable models](/stable-model-semantics/).** Every stable model of a normal logic program is a minimal model of the program read as classical clauses, but not every minimal model is stable. Stable models add a groundedness condition that minimal models lack.
- **[Diagnosis](/consistency-based-diagnosis/).** Minimizing the atoms $\mathit{AB}(c)$ in a system description and observations, with all other atoms varying, gives exactly the minimal diagnoses as the $P$-parts of the minimal models.

## Known results in the model

- **Inference is $\Pi_2^p$-complete** for propositional circumscription (Eiter and Gottlob 1993). The upper bound: $\varphi$ fails exactly when some model $M$ of $A$ falsifies $\varphi$ and no model $N$ of $A$ has $N <_{P;Z} M$, which is an NP guess followed by a coNP check. The lower bound holds by a reduction from $\forall\exists$ quantified Boolean formulas, see [QBF](/qbf/).
- **Model checking is coNP-complete** (Cadoli 1992). A model $M$ is not minimal exactly when a smaller model exists, which is an NP question.
- **Minimal models exist and the logic is consistent** in the finite case, as shown above. So, unlike default logic, there is no existence problem.
- **First-order circumscription is second-order.** In general the circumscription axiom is not equivalent to any first-order formula. For some classes of theories it is, and then a first-order theorem prover can be used.
- **The [Yale shooting problem](/yale-shooting-problem/).** Hanks and McDermott (1987) showed that minimizing abnormality over all time points gives an unintended minimal model in a simple action scenario. The fixes, such as chronological minimization and the separation of causal and inertial rules, changed how circumscription is used for the [frame problem](/frame-problem/).

### Examples

**Tweety.** $A = \{\mathit{bird},\ \mathit{bird} \wedge \neg\mathit{ab} \supset \mathit{flies}\}$, $P = \{\mathit{ab}\}$, $Z = \{\mathit{flies}\}$. The minimal models have $\mathit{ab}$ false, so they make $\mathit{flies}$ true, and $\mathrm{Circ}(A; P; Z) \models \mathit{flies}$. Add $\neg\mathit{flies}$ to $A$. Now every model has $\mathit{ab}$ true, and $\mathit{flies}$ no longer follows. If $\mathit{flies}$ were fixed instead of varying, the model with $\mathit{ab}$ and $\neg\mathit{flies}$ could not be compared with the one with $\neg\mathit{ab}$ and $\mathit{flies}$, and the conclusion would be lost. The choice of $Z$ matters.

**Nixon diamond.** $A = \{q,\ r,\ q \wedge \neg\mathit{ab}_1 \supset p,\ r \wedge \neg\mathit{ab}_2 \supset \neg p\}$ with $P = \{\mathit{ab}_1, \mathit{ab}_2\}$ and $Z = \{p\}$. No model has both abnormality atoms false. The minimal models have $\mathit{ab}$-parts $\{\mathit{ab}_1\}$ (with $\neg p$) and $\{\mathit{ab}_2\}$ (with $p$). So the circumscription entails $\mathit{ab}_1 \vee \mathit{ab}_2$ and $\neg(\mathit{ab}_1 \wedge \mathit{ab}_2)$, and it entails neither $p$ nor $\neg p$.

## References
