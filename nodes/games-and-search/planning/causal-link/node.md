---
tag: 3AWZJ1
kind: concept
slug: causal-link
name: Causal link
aliases:
- producer-consumer link
area: games-and-search/planning
level: core
summary: A record in a partial-order plan that step i supplies fact p to a later step j. A step that deletes p and may fall between them threatens it, and an ordering or other repair resolves the threat.
prereqs: [partial-order-plan]
see_also: [pop-partial-order-planning, snlp, ucpop, tweak, plan-space-planning, sussman-anomaly, least-commitment-principle, goal-regression]
sources:
  - paper: "David McAllester and David Rosenblitt, Systematic nonlinear planning, Proceedings of AAAI-91"
    locator: pp. 634 to 639 (causal links as plan constraints, threats by steps that add or delete the linked fact, and their resolution by ordering)
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (causal links, threats, demotion, promotion, separation and confrontation)
  - paper: "Austin Tate, Generating project networks, Proceedings of IJCAI-77"
    locator: pp. 888 to 893 (NONLIN and the goal structure that records which node supports which condition)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (causal links, threats and their resolvers in plan-space planning)
---

A causal link $i \xrightarrow{p} j$ is a part of a [partial-order plan](/partial-order-plan/). It says that step $i$ adds the fact $p$, that step $j$ needs $p$, and that the plan relies on $i$, not on some other step, to supply it. The link orders $i$ before $j$ and asks that $p$ stay true in between. A step $k$ *threatens* the link if it deletes $p$ and the orderings let it fall between $i$ and $j$. A threat is resolved by demotion, ordering $k$ before $i$, or by promotion, ordering $k$ after $j$. A plan in which every precondition has a link and no link is threatened is a solution: all of its linearizations are valid plans.

## In plain words

A causal link is a note in a plan: "this step is here to give that later step the thing it needs". It also says that the giver comes first.

The note is a promise. What it carries must stay true from the giver to the taker. A third step that could undo it, and that the plan still allows to run in the gap, is a threat.

To remove a threat, move the third step out of the gap. Put it before the giver, or after the taker. With extra tools a planner can also make the third step harmless.

If every need of every step has a note and no note is threatened, the plan works in every order it allows. The notes also explain the plan: each one says why a step is there.

## The idea

Let $P$ be a partial-order plan over [STRIPS](/strips/) actions, with an ordering relation $\prec$ and a START step that adds the initial state. A causal link $i \xrightarrow{p} j$ requires

- $p \in \mathit{add}(i)$ and $p \in \mathit{pre}(j)$, and
- $i \prec j$.

It is *protected* in a linearization if no step strictly between $i$ and $j$ deletes $p$. A step $k \notin \{i, j\}$ with $p \in \mathit{del}(k)$ is a *threat* to the link if some linearization puts $k$ between the ends. Because the linearizations are the topological orders of $\prec$, this happens exactly when neither $k \prec i$ nor $j \prec k$ follows from the orderings; see the proof on the [partial-order plan](/partial-order-plan/) page.

The link turns a global question into local ones. "Does $p$ hold when $j$ starts, in every linearization?" asks about every way to order the plan and every step that might come before $j$. With links the question splits into two checks that a planner can make one at a time and keep up to date as the plan grows: does the link exist, and does any step threaten it? A new step only needs to be tested against the existing links, and a new link only against the existing steps. This is how [POP](/pop-partial-order-planning/) knows that a plan is complete when its list of flaws is empty.

Ways to resolve a threat $(k, i \xrightarrow{p} j)$:

- **Demotion**: add $k \prec i$.
- **Promotion**: add $j \prec k$.
- **Separation**: for lifted actions, add a binding constraint so that the fact $k$ deletes cannot unify with $p$.
- **Confrontation**: when the delete is a conditional effect of $k$, add the negation of its condition as a new goal of $k$, as in [UCPOP](/ucpop/).

Each resolution keeps exactly the linearizations in which the link is safe from $k$: the demoted plan has those with $k$ before $i$, the promoted one those with $k$ after $j$. So trying every resolution loses no solution.

A link is a stronger commitment than an ordering. It fixes the producer. If a later step $k$ deletes $p$, the planner must keep $k$ out of the gap, even when another step after $k$ would add $p$ back in time. A planner without links, such as [TWEAK](/tweak/), would accept that second step as a "white knight". This is the price of links: some plans that would work need a different link, so the planner may have to try more producers. The gain is that a plan with links says exactly why it works.

**Systematic links.** [SNLP](/snlp/) also counts a step that *adds* $p$ as a threat. Then the link $i \xrightarrow{p} j$ says that $i$ is the *last* step before $j$ that touches $p$. With this rule two different complete plans in the search tree never share a linearization, so no work is repeated.

## Examples

**The Sussman anomaly.** In the [Sussman anomaly](/sussman-anomaly/), take three steps $S_C = \mathit{move}(C, A, \mathit{table})$, $S_B = \mathit{move}(B, \mathit{table}, C)$ and $S_A = \mathit{move}(A, \mathit{table}, B)$, and the links

- START $\xrightarrow{\mathit{clear}(C)}$ $S_C$,
- START $\xrightarrow{\mathit{clear}(B)}$ $S_B$,
- $S_C \xrightarrow{\mathit{clear}(A)}$ $S_A$.

$S_B$ deletes $\mathit{clear}(C)$ and nothing keeps it out of the first gap, so it threatens the first link. $S_A$ deletes $\mathit{clear}(B)$ and threatens the second. Demotion would put a step before START, so only promotion is possible: $S_C \prec S_B$ for the first threat, then $S_B \prec S_A$ for the second. The plan now has one linearization, $S_C, S_B, S_A$, the shortest plan. The two threats chose the order of the goals, which a planner that works on one goal at a time gets wrong.

**A threat that is not a threat.** Take a link $i \xrightarrow{p} j$, a step $k$ that deletes $p$, and a step $m$ with the links $j \xrightarrow{q} m$ and $m \xrightarrow{r} k$. Then $j \prec m \prec k$, so $j \prec k$ is forced by a chain, and $k$ cannot fall between $i$ and $j$, and there is no threat. A test that looks only at the stored ordering pairs, and not at chains of them, would report one here.

**Systematic threat.** A link $i \xrightarrow{p} j$ and a step $k$ that also adds $p$, unordered with both ends. For POP this is harmless. For SNLP it is a threat, and SNLP orders $k$ before $i$ or after $j$. A plan in which $k$ supplies $p$ is then reached on a different branch, the one that linked $p$ from $k$.

## Where it is used

- **Plan-space planners.** POP, SNLP, UCPOP and their descendants, such as VHPOP, represent plans with causal links, and the flaws they repair are open preconditions, which lack a link, and threats.
- **HTN planners.** NONLIN, SIPE, O-Plan and UMCP record the support of conditions in plans that they also decompose; Tate's goal structure in NONLIN is the origin of the idea.
- **Plan explanation and repair.** A link is a reason for a step. When a step fails during execution, the links show which later steps lose their support, so only that part of the plan has to be replanned.
- **Deordering.** A sequential plan can be turned into a partial-order plan by computing links from the last earlier adder of each precondition and keeping only the orderings needed to protect them.
- **Theory of refinement planning.** Kambhampati, Knoblock and Yang treat a link as a constraint on the set of candidate sequences, and use it to compare the planners above.

## References
