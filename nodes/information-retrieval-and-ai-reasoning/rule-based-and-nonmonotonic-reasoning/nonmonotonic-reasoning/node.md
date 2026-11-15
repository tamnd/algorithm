---
tag: HZX73W
kind: concept
slug: nonmonotonic-reasoning
name: Nonmonotonic reasoning
aliases:
- defeasible reasoning
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: intro
summary: Reasoning in which adding premises can withdraw conclusions, as when a default is blocked by new information.
see_also: [default-logic, circumscription, autoepistemic-logic, system-p, rational-closure, abductive-reasoning, closed-world-assumption, negation-as-failure]
sources:
  - paper: doi:10.1016/0004-3702(80)90014-4
    title: Raymond Reiter, A logic for default reasoning, Artificial Intelligence 13(1-2), 81 to 132 (1980)
    locator: Section 1 (the motivation for defaults and the failure of monotonicity) and Section 2 (extensions)
  - paper: doi:10.1016/0004-3702(80)90011-9
    title: John McCarthy, Circumscription, a form of non-monotonic reasoning, Artificial Intelligence 13(1-2), 27 to 39 (1980)
    locator: the definition of circumscription and the discussion of why common-sense reasoning is nonmonotonic
  - paper: doi:10.1016/0004-3702(90)90101-5
    title: Sarit Kraus, Daniel Lehmann and Menachem Magidor, Nonmonotonic reasoning, preferential models and cumulative logics, Artificial Intelligence 44(1-2), 167 to 207 (1990)
    locator: Section 3 (the rules of cumulative and preferential consequence relations)
  - paper: "Michael Thomas and Heribert Vollmer, Complexity of non-monotonic logics, Bulletin of the EATCS 102 (2010), arXiv:1009.1990"
    locator: Theorems 3.5, 4.6 and 6.1 (the complexity of default logic, autoepistemic logic and abduction)
---

Nonmonotonic reasoning draws conclusions that can be taken back when more is learned. Classical logic is *monotonic*: a conclusion that follows from some premises still follows when premises are added. Everyday reasoning is not like this. Told that Tweety is a bird, you conclude that Tweety flies. Told also that Tweety is a penguin, you withdraw that conclusion. Logics that model this behaviour were developed from 1980 on, with [default logic](/default-logic/), [circumscription](/circumscription/) and later [autoepistemic logic](/autoepistemic-logic/). They are the basis of [negation as failure](/negation-as-failure/) in logic programming, of [answer set programming](/answer-set-programming/), of the closed-world reading of databases, and of reasoning about action.

## In plain words

Much of what we know holds "normally" and not always. Birds normally fly. A meeting normally takes place unless it is cancelled. A database lists the flights that exist, and a flight not in the list is taken not to exist. Reasoning with such rules means jumping to a conclusion when nothing speaks against it, and taking the conclusion back when something does. The jump makes the reasoning useful, because we rarely know all exceptions in advance. The taking back is what makes it nonmonotonic: more information can mean fewer conclusions.

## The idea

A *consequence relation* $\vdash$ relates a set of premises to a conclusion. It is **monotonic** when

$$\Gamma \vdash \varphi \ \text{ implies } \ \Gamma \cup \Delta \vdash \varphi \quad\text{for all } \Gamma, \Delta, \varphi.$$

Classical consequence $\models$ has this property, because a model of $\Gamma \cup \Delta$ is a model of $\Gamma$. A *nonmonotonic* consequence relation $\mathrel{|\!\sim}$ lacks it: some $\Gamma \mathrel{|\!\sim} \varphi$ holds while $\Gamma \cup \Delta \mathrel{|\!\sim} \varphi$ fails. Such a relation usually goes beyond classical logic, $\Gamma \models \varphi$ implies $\Gamma \mathrel{|\!\sim} \varphi$, and the extra conclusions are the defeasible ones.

There are four main ways to build such a relation.

1. **Fixed points of belief.** A belief set is acceptable when it is exactly what the premises and the rules it does not block produce. This gives the [extensions](/default-extension/) of default logic, the stable expansions of autoepistemic logic and the [stable models](/stable-model-semantics/) of logic programs. A theory can have several acceptable belief sets or none.
2. **Minimal models.** Keep only the models of the premises in which certain things, such as abnormalities, are as false as possible. This is [circumscription](/circumscription/) and, in its simplest form, the [closed-world assumption](/closed-world-assumption/).
3. **Preference orders on situations.** Conclude $\beta$ from $\alpha$ when the most normal situations that satisfy $\alpha$ satisfy $\beta$. This is the semantics of [System P](/system-p/), and with ranked orders of [rational closure](/rational-closure/) and [System Z](/system-z/).
4. **Explanation.** Accept hypotheses that explain an observation, as in [abduction](/abductive-reasoning/) and [diagnosis](/consistency-based-diagnosis/). A new fact can remove an explanation.

When a theory has several acceptable belief sets, there are two ways to read off conclusions. A **credulous** reasoner accepts what holds in some belief set. A **skeptical** reasoner accepts only what holds in all of them.

**What survives of monotonicity.** Kraus, Lehmann and Magidor (1990) asked which weaker rules a sensible relation should keep. *Cautious Monotonicity* says that adding a conclusion you already draw does not remove other conclusions. Together with Cut and a few other rules it forms the core of [System P](/system-p/). Some systems, such as skeptical default logic, fail even this weak rule.

**Cost.** The extra conclusions have a price. Classical propositional entailment is coNP-complete. For propositional default logic, autoepistemic logic, circumscription and abduction, the main tasks are complete for the second level of the [polynomial hierarchy](/polynomial-hierarchy/), $\Sigma_2^p$ or $\Pi_2^p$ (Thomas and Vollmer 2010; see [the complexity of default logic](/default-logic-complexity/)). The second quantifier comes from the test "nothing speaks against it", which is itself a satisfiability question inside the search for a belief set. Restricted languages, such as normal logic programs and Horn theories, bring the cost down to NP or to polynomial time.

## Examples

- **Tweety.** From "birds normally fly" and "Tweety is a bird", conclude "Tweety flies". Add "Tweety is a penguin" and "penguins do not fly", and the conclusion goes away. The default $\mathit{bird} : \mathit{flies} / \mathit{flies}$ in default logic and the circumscription of $\mathit{ab}$ in $\mathit{bird} \wedge \neg\mathit{ab} \supset \mathit{flies}$ both behave this way.
- **The Nixon diamond.** Quakers are normally pacifists, Republicans are normally not, and Nixon is both. Default logic gives two extensions, one with each conclusion. A credulous reasoner may pick either one. A skeptical reasoner concludes neither, and circumscription gives the same skeptical answer.
- **A flight database.** A table of flights lists the flights from Boston to Paris. A query "is there a flight at 9:00?" is answered "no" when no such row exists. Adding a row changes the answer from "no" to "yes". This is the [closed-world assumption](/closed-world-assumption/), and in Prolog it is [negation as failure](/negation-as-failure/).
- **Persistence.** "A fact stays true unless an action changes it" solves most of the [frame problem](/frame-problem/), but the naive version fails on the [Yale shooting problem](/yale-shooting-problem/), where minimizing change gives an unintended model.
- **Diagnosis.** Assume every component of a circuit works. When the outputs contradict this, give up the fewest such assumptions. More measurements can change which components are blamed.

## Where it is used

- **Logic programming and answer set programming:** [negation as failure](/negation-as-failure/), [stable models](/stable-model-semantics/), the [well-founded semantics](/well-founded-semantics/) and [answer set programming](/answer-set-programming/).
- **Databases:** the [closed-world assumption](/closed-world-assumption/) for queries with negation.
- **Reasoning about action:** inertia in the [situation calculus](/situation-calculus/), the [event calculus](/event-calculus/) and [successor state axioms](/successor-state-axioms/).
- **Truth maintenance:** [justification-based](/justification-based-truth-maintenance/) and [assumption-based](/assumption-based-truth-maintenance/) truth maintenance systems keep track of which conclusions depend on which assumptions.
- **Diagnosis and explanation:** [consistency-based diagnosis](/consistency-based-diagnosis/) and [abduction](/abductive-reasoning/).
- **Belief change and argumentation:** [belief revision](/belief-revision/) and [abstract argumentation frameworks](/abstract-argumentation-framework/), where new information or new arguments can defeat old conclusions.
- **Ontologies:** defeasible extensions of [description logics](/description-logic/) use [rational closure](/rational-closure/) to add typicality.

## References
