---
tag: MA8AJC
kind: model
slug: situation-calculus
name: Situation calculus
aliases:
- McCarthy-Hayes situation calculus
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: core
summary: A logical language for change in which situations are histories of actions and fluents are relations whose truth depends on the situation; reasoning about actions is entailment.
prereqs: [frame-problem, classical-planning]
see_also: [successor-state-axioms, situation-calculus-regression, event-calculus, yale-shooting-problem, strips, goal-regression, qualification-problem, ramification-problem]
sources:
  - paper: "John McCarthy and Patrick J. Hayes, Some philosophical problems from the standpoint of artificial intelligence, in Bernard Meltzer and Donald Michie (eds.), Machine Intelligence 4, Edinburgh University Press, 1969, pages 463 to 502"
    locator: situations, fluents and the function result for the situation after an action, and the statement of the frame problem (general locator)
  - book: isbn:9780262182188
    title: Raymond Reiter, Knowledge in Action, Logical Foundations for Specifying and Implementing Dynamical Systems, MIT Press, 2001
    locator: Chapter 3 from page 17 (the language), Chapter 4 from page 45 (the foundational axioms, basic action theories and regression)
  - paper: doi:10.1145/316542.316545
    title: Fiora Pirri and Raymond Reiter, Some contributions to the metatheory of the situation calculus, Journal of the ACM 46(3), 1999, pages 325 to 361
    locator: the foundational axioms, basic action theories, the relative satisfiability theorem and the regression theorem (general locator)
  - paper: doi:10.1016/S0004-3702(96)00044-6
    title: Fangzhen Lin and Raymond Reiter, How to progress a database, Artificial Intelligence 92(1-2), 1997, pages 131 to 167
    locator: progression of a basic action theory, which in general needs second-order logic, and first-order special cases (general locator)
  - book: isbn:9780444522115
    title: Frank van Harmelen, Vladimir Lifschitz and Bruce Porter (eds.), Handbook of Knowledge Representation, Elsevier, 2008
    locator: Chapter 16, Situation Calculus, by Fangzhen Lin (general locator)
---

The situation calculus is a logical language for describing a world that changes through actions. A *situation* is a term that names a finite history of actions, starting from the initial situation $S_0$, and a *fluent* is a relation whose truth depends on the situation. McCarthy and Hayes (1969) introduced it, and Reiter and his colleagues later fixed its form as a set of axioms with clear metatheory. Questions about actions, such as "is the door open after these three actions?", are questions of entailment from the axioms. The [frame problem](/frame-problem/) page explains why describing what does not change is hard and how the solutions compare; the [successor state axioms](/successor-state-axioms/) page gives the form of the axioms that solve it here; and the [regression](/situation-calculus-regression/) page gives the main reasoning procedure. This page is the language and its foundations.

## The machine

**Syntax.** The language is many-sorted, with sorts for actions, situations and ordinary objects. It has

- the constant $S_0$, the initial situation, and the function $do(a, s)$, the situation that results from doing action $a$ in situation $s$;
- action functions, such as $pickup(x)$ or $open$;
- relational fluents $F(\vec{x}, s)$, whose last argument is a situation, such as $Holding(x, s)$;
- the predicate $Poss(a, s)$, "action $a$ can be done in situation $s$";
- the order $s \sqsubset s'$, "$s'$ is reached from $s$ by one or more actions", with $s \sqsubseteq s'$ for $s \sqsubset s' \vee s = s'$.

A situation term such as $do(pickup(A), do(open, S_0))$ names the history "open, then pick up $A$". McCarthy and Hayes (1969) thought of a situation as the complete state of the world at an instant. In the axiomatization of Reiter (2001), a situation is a history, so two different situations can agree on every fluent: $do(close, do(open, S_0))$ and $S_0$ are different situations even if the door is closed in both.

**Foundational axioms.** The axioms $\Sigma$ (Reiter 2001, Chapter 4; Pirri and Reiter 1999) make the situations exactly the finite action sequences:

1. $do(a_1, s_1) = do(a_2, s_2) \rightarrow a_1 = a_2 \wedge s_1 = s_2$;
2. $\forall P\, \big(P(S_0) \wedge \forall a\, \forall s\, (P(s) \rightarrow P(do(a, s))) \rightarrow \forall s\, P(s)\big)$;
3. $\neg (s \sqsubset S_0)$;
4. $s \sqsubset do(a, s') \leftrightarrow s \sqsubseteq s'$.

The second axiom is an induction axiom in second-order logic. With the first, it makes the situations in every model a tree with root $S_0$, in which each situation has one child for each action.

**Basic action theory.** A domain is described by a basic action theory

$$\mathcal{D} = \Sigma \cup \mathcal{D}_{ss} \cup \mathcal{D}_{ap} \cup \mathcal{D}_{una} \cup \mathcal{D}_{S_0},$$

where

- $\mathcal{D}_{ap}$ has one precondition axiom $Poss(A(\vec{x}), s) \leftrightarrow \Pi_A(\vec{x}, s)$ for each action function $A$;
- $\mathcal{D}_{ss}$ has one [successor state axiom](/successor-state-axioms/) for each fluent;
- $\mathcal{D}_{una}$ has the unique names axioms for actions: different action functions give different actions, and each action function is one-to-one;
- $\mathcal{D}_{S_0}$ is a set of first-order sentences about $S_0$, the initial database.

The formulas $\Pi_A(\vec{x}, s)$ and the right sides of the successor state axioms must be *uniform in $s$*: they mention no situation term other than the variable $s$, and no $Poss$ and no $\sqsubset$.

**Semantics.** A model of $\mathcal{D}$ is a structure of second-order logic. The language has no special semantics of its own; all its meaning comes from the axioms.

**Example.** A robot has a door and objects. The fluents are $Open(s)$ and $Holding(x, s)$, and the actions are $open$, $close$, $pickup(x)$ and $drop(x)$. Two precondition axioms are $Poss(open, s) \leftrightarrow \neg Open(s)$ and $Poss(pickup(x), s) \leftrightarrow Open(s) \wedge \neg \exists y\, Holding(y, s)$. The initial database is $\neg Open(S_0) \wedge \forall x\, \neg Holding(x, S_0)$. With the obvious successor state axioms, $\mathcal{D}$ entails $Holding(A, do(pickup(A), do(open, S_0)))$, and it also entails that this history is executable, because the door is closed at $S_0$ and open after $open$.

## What it counts

Every question is an entailment question $\mathcal{D} \models \varphi$. The main ones are

- **projection:** does a formula hold after a given sequence of actions? $\mathcal{D} \models \varphi(do([a_1, \ldots, a_n], S_0))$;
- **executability:** can the sequence be performed? $\mathcal{D} \models executable(do([a_1, \ldots, a_n], S_0))$, where $executable(s)$ says that every action in the history of $s$ was possible when it was done;
- **planning:** is there a history that reaches a goal? $\mathcal{D} \models \exists s\, (executable(s) \wedge G(s))$, where a witness for $s$ is a plan;
- **queries about all futures:** for example, $\mathcal{D} \models \forall s\, (executable(s) \rightarrow \neg Broken(s))$, which needs induction over situations.

## Relation to other models

- **[STRIPS](/strips/)** and [classical planning](/classical-planning/) describe one complete state and transform it with add and delete lists. A STRIPS domain is the special case of a basic action theory in which $\mathcal{D}_{S_0}$ is a complete set of ground atoms with the [closed-world assumption](/closed-world-assumption/), and each action has unconditional effects. The situation calculus also allows incomplete initial knowledge, conditional effects and quantified preconditions.
- **The [event calculus](/event-calculus/)** uses time points and a narrative of events in place of histories. It handles actions that happen at the same time and continuous change more directly, while the situation calculus is built around branching hypothetical futures.
- **[Goal regression](/goal-regression/)** in STRIPS planning and the [weakest precondition](/weakest-precondition/) of program verification are the same idea as regression in the situation calculus: rewrite a condition on the result of an action as a condition on the situation before it.
- **[Temporal logic](/temporal-logic/)** talks about properties along paths of states with operators such as "always" and "eventually"; the situation calculus talks about named histories with quantifiers over situations.

## Known results in the model

- **Relative satisfiability.** A basic action theory $\mathcal{D}$ is satisfiable if and only if $\mathcal{D}_{una} \cup \mathcal{D}_{S_0}$ is satisfiable (Pirri and Reiter 1999). The axioms for actions, written in the forms above, can never make a consistent initial database inconsistent.
- **Regression.** For a regressable formula $\varphi$, such as a formula about a ground history, $\mathcal{D} \models \varphi$ if and only if $\mathcal{D}_{S_0} \cup \mathcal{D}_{una} \models \mathcal{R}[\varphi]$, where $\mathcal{R}[\varphi]$ is a first-order formula about $S_0$ (Pirri and Reiter 1999; Reiter 2001, Section 4.5). So projection and executability reduce to first-order reasoning about $S_0$, without $\Sigma$ and without the second-order axiom. The [regression](/situation-calculus-regression/) page gives the operator.
- **Undecidability.** Because $\mathcal{D}_{S_0}$ can be any first-order theory, projection is undecidable in general: with no actions at all, it is first-order entailment. In the ground, finite case, where the fluents and actions are propositional, it is decidable, and the regression page shows that it is coNP-complete when the initial database is a propositional formula.
- **Progression is harder.** Updating $\mathcal{D}_{S_0}$ to a database about $do(a, S_0)$, so that the new theory has the same consequences about the future, needs second-order logic in general, and Lin and Reiter (1997) give first-order cases in which it does not.
- **Planning is deduction.** A plan is a witness for an existential query. Since entailment is undecidable in general, so is planning; in the propositional case it is the [classical planning](/classical-planning/) problem.

## References
