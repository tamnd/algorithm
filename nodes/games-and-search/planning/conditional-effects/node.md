---
tag: DWVFYP
kind: definition
slug: conditional-effects
name: Conditional effects
area: games-and-search/planning
level: advanced
summary: "Action effects of the form \"when c, add A and delete D\", which take place only if the condition c holds in the state where the action is applied."
prereqs: [strips]
see_also: [pddl, action-schema, grounding, graphplan, goal-regression, ramification-problem, frame-problem, planning-graph]
sources:
  - paper: "Edwin P. D. Pednault, ADL: Exploring the middle ground between STRIPS and the situation calculus, Proceedings of the First International Conference on Principles of Knowledge Representation and Reasoning (KR), Morgan Kaufmann, 1989"
    title: Pednault 1989
    locator: pp. 324 to 331 (ADL, with conditional effects and their regression)
  - paper: doi:10.1093/logcom/4.5.467
    title: "Edwin P. D. Pednault, ADL and the state-transition model of action, Journal of Logic and Computation 4(5) (1994)"
    locator: pp. 467 to 512
  - paper: doi:10.1613/jair.735
    title: "Bernhard Nebel, On the compilability and expressive power of propositional planning formalisms, Journal of Artificial Intelligence Research 12 (2000)"
    locator: Section 5.1, Theorem 11 (no compilation with linear growth of plans) and Section 6.2, Theorem 22 (compilation with polynomial growth of plans)
  - paper: "B. Cenk Gazen and Craig A. Knoblock, Combining the expressivity of UCPOP with the efficiency of Graphplan, Recent Advances in AI Planning, 4th European Conference on Planning (ECP 1997), Lecture Notes in Artificial Intelligence 1348, Springer, 1997"
    title: Gazen and Knoblock 1997
    locator: pp. 221 to 233 (compiling conditional effects and quantifiers into STRIPS actions before Graphplan)
  - paper: "Corin R. Anderson, David E. Smith and Daniel S. Weld, Conditional effects in Graphplan, Proceedings of the Fourth International Conference on Artificial Intelligence Planning Systems (AIPS), AAAI Press, 1998"
    title: Anderson, Smith and Weld 1998
    locator: pp. 44 to 53 (full expansion against factored expansion)
  - paper: "Jana Koehler, Bernhard Nebel, Jörg Hoffmann and Yannis Dimopoulos, Extending planning graphs to an ADL subset, Recent Advances in AI Planning, 4th European Conference on Planning (ECP 1997), Lecture Notes in Artificial Intelligence 1348, Springer, 1997"
    title: Koehler et al. 1997
    locator: pp. 273 to 285 (conditional effects handled directly in the planning graph of IPP)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.4.2 (conditional operators)
---

A conditional effect is a part of an action's effect that takes place only when a condition holds: "when $c$, add $A$ and delete $D$". The condition is tested in the state where the action is applied, and an action is applicable even when the condition is false; then that part of the effect does nothing. Conditional effects came into planning with Pednault's ADL (1989) and are the `when` construct of [PDDL](/pddl/). They let one action have an effect that depends on the state, such as a briefcase that carries whatever is inside it, which plain [STRIPS](/strips/) can express only with many more actions or longer plans.

## Definition

Let $F$ be a set of facts. A conditional effect is a triple $e = (c, A, D)$ of subsets of $F$: the condition, the add set and the delete set. An unconditional effect is the special case $c = \emptyset$. An action with conditional effects is a pair $a = (\mathit{pre}(a), E(a))$ of a precondition and a finite set of effects.

Action $a$ is applicable in state $s \subseteq F$ when $\mathit{pre}(a) \subseteq s$. The effects that fire in $s$ are $E_s(a) = \{(c, A, D) \in E(a) : c \subseteq s\}$, and the result is

$$\gamma(s, a) = \Big(s \setminus \bigcup_{(c, A, D) \in E_s(a)} D\Big) \cup \bigcup_{(c, A, D) \in E_s(a)} A.$$

All conditions are read in the old state $s$, and all the fired effects take place at once. An effect does not see the changes made by the other effects of the same action. If one fired effect adds a fact and another deletes it, the formula makes the fact true, as for a fact in both lists of a STRIPS action; some languages call such an action ill defined instead.

In PDDL, with the requirement `:conditional-effects`, an effect can contain `(when c e)`, and usually `(forall (?x) (when c e))`, which grounds to one conditional effect for each object. Conditions can also contain negations, disjunctions and quantifiers in full ADL.

## Examples and non-examples

### Examples

- Pednault's briefcase. Locations $l_1, \ldots, l_L$, objects $o_1, \ldots, o_O$, and the facts $\mathit{at\text{-}b}(l)$ (where the briefcase is), $\mathit{at}(o, l)$, $\mathit{in}(o)$ and $\mathit{out}(o)$. The action $\mathit{move}(l, m)$ has precondition $\mathit{at\text{-}b}(l)$, the unconditional effect "add $\mathit{at\text{-}b}(m)$, delete $\mathit{at\text{-}b}(l)$", and for each object $o$ the effect "when $\mathit{in}(o)$, add $\mathit{at}(o, m)$ and delete $\mathit{at}(o, l)$". The actions $\mathit{put\text{-}in}(o, l)$ and $\mathit{take\text{-}out}(o)$ are plain STRIPS actions.

  In the state $\{\mathit{at\text{-}b}(l_1), \mathit{at}(o_1, l_1), \mathit{in}(o_1), \mathit{at}(o_2, l_1), \mathit{out}(o_2)\}$, the action $\mathit{move}(l_1, l_2)$ fires the effect for $o_1$ and not the one for $o_2$, and gives $\{\mathit{at\text{-}b}(l_2), \mathit{at}(o_1, l_2), \mathit{in}(o_1), \mathit{at}(o_2, l_1), \mathit{out}(o_2)\}$.

  With 3 locations and 2 objects, $o_1$ at $l_1$, $o_2$ at $l_2$ and the briefcase at $l_1$, the goal "both objects at $l_3$" has a shortest plan of 4 actions: $\mathit{put\text{-}in}(o_1, l_1)$, $\mathit{move}(l_1, l_2)$, $\mathit{put\text{-}in}(o_2, l_2)$, $\mathit{move}(l_2, l_3)$. The task has 48 reachable states: 3 places for the briefcase, and for each object 3 locations or the inside of the briefcase.

- Compiling into STRIPS, one action for each set of fired effects. An action with $k$ conditional effects becomes $2^k$ actions: for each subset $X \subseteq E(a)$, the action with precondition $\mathit{pre}(a)$, plus the conditions of the effects in $X$, plus the negations of the conditions of the effects outside $X$, and the effects of $X$ made unconditional. Negated conditions need negative preconditions, or a complement fact $\bar f$ for each $f$ that every action keeps in step. With single-fact conditions the $2^k$ new actions have disjoint preconditions in reachable states, so exactly one of them applies where $a$ applies, and it has the same result. The compiled task has the same reachable states and the same plan lengths. In the briefcase domain, $\mathit{move}(l, m)$ has $O$ conditional effects, so the $L(L-1) + O L + O$ actions become $L(L-1) 2^O + O L + O$. Both tasks have $L (L+1)^O$ reachable states, and the shortest plans have the same lengths:

  | $L$ | $O$ | actions | compiled actions | reachable states |
  |---|---|---|---|---|
  | 2 | 1 | 5 | 7 | 6 |
  | 3 | 2 | 14 | 32 | 48 |
  | 3 | 3 | 18 | 60 | 192 |
  | 4 | 4 | 32 | 212 | 2500 |

- A light switch: $\mathit{toggle}$ has the effects "when $\mathit{on}$, add $\mathit{off}$ and delete $\mathit{on}$" and "when $\mathit{off}$, add $\mathit{on}$ and delete $\mathit{off}$". Both conditions are read in the old state, so exactly one effect fires and the action flips the light. If the effects were applied one after the other, each reading the state left by the one before, the second effect would undo the first and the light would not change.

### Non-examples

- A precondition. "Move $o$ to $m$ if $o$ is in the briefcase" with $\mathit{in}(o)$ as a precondition makes the action inapplicable when $o$ is out; a conditional effect keeps the action applicable and does nothing for $o$.
- A sequence of effects in which a later effect reads the result of an earlier one. That is a macro action, not a set of conditional effects.
- A nondeterministic effect, such as "one of $A_1$ or $A_2$". The result of a conditional effect is fixed by the state; a nondeterministic effect is not, and belongs to nondeterministic or probabilistic planning, such as a [Markov decision process](/markov-decision-process/).
- An indirect effect stated as a domain rule, such as "if $o$ is in the briefcase, then $o$ is where the briefcase is". That is a state constraint, the subject of the [ramification problem](/ramification-problem/). Conditional effects are one way to write its consequences into each action.

## Related definitions

- Expressive power (Nebel 2000). Nebel compares planning formalisms by compilation schemes that translate the domain in polynomial size and the states one fact at a time, and asks how much plans grow. Theorem 11: $\mathcal{S}_{LIC}$ cannot be compiled into $\mathcal{S}_{BI}$ preserving plan size linearly; that is, conditional effects cannot be removed by such a compilation if plans may grow only by a constant factor, even when the target allows Boolean formulas as preconditions. Theorem 22: $\mathcal{S}_{BC}$ compiles into $\mathcal{S}_{B}$ and $\mathcal{S}_{LC}$ into $\mathcal{S}_{L}$ in polynomial time preserving plan size polynomially. So there are two ways to remove conditional effects: exponentially many actions with plans of the same length, as above, or polynomially many actions with longer plans.
- Full expansion and factored expansion. Gazen and Knoblock (1997) compile conditional effects and quantifiers into STRIPS actions before [Graphplan](/graphplan/) runs, at an exponential cost in the worst case. Anderson, Smith and Weld (1998) keep the effects factored and extend Graphplan's mutex rules to them. Koehler and others (1997) handle conditional effects directly in the [planning graph](/planning-graph/) of IPP.
- Regression through conditional effects. Fact $f$ holds after $a$ if an effect that adds $f$ fires, or if $f$ held before and no effect that deletes $f$ fires. Let $C^+_f$ be the disjunction of the conditions of the effects of $a$ that add $f$, and $C^-_f$ the disjunction of the conditions of those that delete it. Then the regression of $f$ through $a$ is $\mathit{pre}(a) \land \big(C^+_f \lor (f \land \lnot C^-_f)\big)$; this is Pednault's regression for ADL, and it is the form that [goal regression](/goal-regression/) takes with conditional effects.
- Conditional effects and the [frame problem](/frame-problem/): each fact still changes only by an effect that mentions it, so the STRIPS assumption holds; the effect lists become state dependent.
- [Grounding](/grounding/): a quantified conditional effect $\forall x\, (\mathrm{when}\ c(x)\ e(x))$ grounds into one conditional effect for each object, so a ground move in the briefcase domain has $O$ of them.

## References
