---
tag: MGC5NA
kind: model
slug: strips
name: STRIPS representation
aliases:
- STRIPS
- Stanford Research Institute Problem Solver
- STRIPS formalism
area: games-and-search/planning
level: intro
summary: "A planning model in which a state is a set of true facts and an action has a precondition, an add list and a delete list. Applying the action to s gives (s minus del) union add."
prereqs: [state-space]
see_also: [classical-planning, action-schema, grounding, pddl, sas-plus, conditional-effects, strips-plan-existence-pspace-complete, delete-relaxation]
sources:
  - paper: doi:10.1016/0004-3702(71)90010-5
    title: "Richard E. Fikes and Nils J. Nilsson, STRIPS: A new approach to the application of theorem proving to problem solving, Artificial Intelligence 2(3-4) (1971)"
    locator: pp. 189 to 208 (world models as sets of formulas, operators with a precondition, an add list and a delete list, and the search by means-ends analysis)
  - paper: "Vladimir Lifschitz, On the semantics of STRIPS, in M. P. Georgeff and A. L. Lansky (editors), Reasoning about Actions and Plans: Proceedings of the 1986 Workshop, Morgan Kaufmann, 1987"
    title: Lifschitz 1987
    locator: pp. 1 to 9 (a formal semantics of STRIPS operators and the conditions under which the original system is sound)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.2 (set-theoretic representation) and Section 2.3 (classical representation); Chapter 4, Section 4.4 (the STRIPS algorithm)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.1 (definition of classical planning)
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: pp. 165 to 204 (plan existence is PSPACE-complete, and the effect of limits on the number of preconditions and effects)
  - paper: doi:10.1613/jair.735
    title: "Bernhard Nebel, On the compilability and expressive power of propositional planning formalisms, Journal of Artificial Intelligence Research 12 (2000)"
    locator: pp. 271 to 315 (STRIPS compared with formalisms that have negative preconditions, disjunctions and conditional effects)
---

STRIPS is the standard model of a deterministic planning task. A state is a set of [facts](/closed-world-assumption/) (the facts that are true), and an action has three sets of facts: a precondition that must hold before it, an add list of facts it makes true and a delete list of facts it makes false. The name comes from the Stanford Research Institute Problem Solver of Fikes and Nilsson (1971), the planner of the Shakey robot; today it names the propositional model that their operators reduce to. It is the core of [PDDL](/pddl/) and the base model of [classical planning](/classical-planning/).

## The machine

### Tasks

A STRIPS task is a tuple $\Pi = (F, A, I, G)$:

- $F$ is a finite set of facts (propositions), for example $\mathit{on}(C, A)$ or $\mathit{handempty}$.
- $A$ is a finite set of actions. Each action $a \in A$ has three subsets of $F$: the precondition $\mathit{pre}(a)$, the add list $\mathit{add}(a)$ and the delete list $\mathit{del}(a)$.
- $I \subseteq F$ is the initial state.
- $G \subseteq F$ is the goal. A state $s$ is a goal state when $G \subseteq s$.

A state is a subset $s \subseteq F$. A fact in $s$ is true, and a fact not in $s$ is false: this is the [closed world assumption](/closed-world-assumption/), and it makes a state a complete description of the world. The goal, in contrast, is a partial description: every state that contains $G$ is a goal state, so there can be many of them.

### Semantics

Action $a$ is applicable in state $s$ when $\mathit{pre}(a) \subseteq s$. Its result is

$$\gamma(s, a) = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a).$$

So, for each fact $f$: $f \in \gamma(s, a)$ if and only if $f \in \mathit{add}(a)$, or $f \in s$ and $f \notin \mathit{del}(a)$. The formula deletes first and then adds, so a fact in both lists is true after the action. Some texts forbid that overlap instead; the formula above gives a defined result in all cases.

A plan is a sequence $\pi = a_1, \ldots, a_n$ with states $s_0 = I$ and $s_i = \gamma(s_{i-1}, a_i)$, such that each $a_i$ is applicable in $s_{i-1}$ and $G \subseteq s_n$. The empty sequence is a plan when $G \subseteq I$. The length of $\pi$ is $n$. A plan is optimal when no plan is shorter; with a cost $c(a) \ge 0$ on each action, the cost of a plan is $\sum_i c(a_i)$ and an optimal plan has the least cost. Plans in this model are sequential: one action at each step.

### The state space

The task defines a [state space](/state-space/): a directed graph with the vertex set $2^F$ and an edge $s \to \gamma(s, a)$, labelled $a$, for each action $a$ applicable in $s$. Plans are exactly the paths from $I$ to a goal state, so planning is [state-space search](/state-space-search/) on a graph that is given implicitly by $(F, A)$. The graph has $2^{|F|}$ vertices, but most of them are not reachable from $I$, and many describe impossible worlds (two blocks on top of each other, a hand that is empty and holds a block).

### A worked example

Take three blocks in the four-operator [blocks world](/blocks-world/): the facts are $\mathit{on}(x, y)$ for $x \ne y$, $\mathit{ontable}(x)$, $\mathit{clear}(x)$, $\mathit{holding}(x)$ and $\mathit{handempty}$, so $|F| = 6 + 3 + 3 + 3 + 1 = 16$. The action $\mathit{unstack}(C, A)$ has

- $\mathit{pre} = \{\mathit{on}(C, A), \mathit{clear}(C), \mathit{handempty}\}$,
- $\mathit{add} = \{\mathit{holding}(C), \mathit{clear}(A)\}$,
- $\mathit{del} = \{\mathit{on}(C, A), \mathit{clear}(C), \mathit{handempty}\}$.

In the state $s = \{\mathit{on}(C, A), \mathit{ontable}(A), \mathit{ontable}(B), \mathit{clear}(C), \mathit{clear}(B), \mathit{handempty}\}$ the precondition holds, and

$$\gamma(s, a) = \{\mathit{ontable}(A), \mathit{ontable}(B), \mathit{clear}(B), \mathit{holding}(C), \mathit{clear}(A)\}.$$

Three facts are not in either list, and they keep their values. The domain has $2 \cdot 3 + 2 \cdot 3 \cdot 2 = 18$ ground actions, and in general $2n^2$ for $n$ blocks. Of the $2^{16} = 65536$ subsets of $F$, only 22 are reachable from $s$: the 13 ways to arrange three blocks in stacks, and the 9 states with one block in the hand and the other two arranged in one of 3 ways. With four blocks, $|F| = 25$ and 125 of the $2^{25} = 33554432$ subsets are reachable.

### The STRIPS assumption

An action changes exactly the facts in its add and delete lists; every other fact keeps its value. This rule is often called the STRIPS assumption. It is how STRIPS avoids the [frame problem](/frame-problem/): a logical description of actions must state, for each action, which facts it does not change, while a STRIPS action lists only its changes. The price is expressive power. An effect that depends on the state (a briefcase that moves its contents) needs [conditional effects](/conditional-effects/), and an indirect effect (a block that is no longer clear) must be written into each action by hand, which is the [ramification problem](/ramification-problem/).

### The original system and the modern model

The 1971 system was more general than the model above. Its world model was a set of first-order formulas, a precondition was a formula, and a resolution theorem prover tested preconditions and found the differences that guided a search by [means-ends analysis](/means-ends-analysis/), in the manner of GPS. Its operators were schemas with parameters, the [action schemas](/action-schema/) of PDDL. Lifschitz (1987) gave the first formal semantics of STRIPS operators and showed that the original system is sound only under restrictions on the formulas in the world model and in the add lists. The propositional model on this page is the restriction in which all facts are ground atoms and all preconditions are conjunctions of atoms. A lifted task becomes a propositional one by [grounding](/grounding/).

### Common mistakes

- Applying an action without testing its precondition. The formula $\gamma$ is defined for any $s$, but the result is meaningful only when $a$ is applicable.
- Assuming that a goal is a full state. A goal is a set of facts that must hold; the other facts are free. A goal state test is $G \subseteq s$, not $G = s$.
- Expecting negative preconditions. Plain STRIPS cannot require that a fact is false. One adds a fact $\mathit{not}\text{-}f$ and keeps it in step with $f$ in every action, or uses a language with negative preconditions.
- Ordering adds and deletes differently. With "add, then delete", a fact in both lists is false afterwards. Planners and validators must agree on one order.

## What it counts

The size of a task is $|F|$, $|A|$ and the total size $\|\Pi\| = |I| + |G| + \sum_{a} (|\mathit{pre}(a)| + |\mathit{add}(a)| + |\mathit{del}(a)|)$. With states stored as hash sets, an applicability test and a successor cost $O(|\mathit{pre}(a)| + |\mathit{add}(a)| + |\mathit{del}(a)|)$ set operations. The complexity results below are in terms of $\|\Pi\|$, for an encoding of $\Pi$ as a list of its sets.

The cost of a plan is its length (unit costs), or the sum of the action costs when actions have nonnegative costs; say which. Step optimal (fewest parallel steps, as in [Graphplan](/graphplan/)) is not the same as action optimal (fewest actions). An explicit search such as [breadth-first search](/breadth-first-search/) over the reachable states takes $O(R \cdot |A| \cdot |F|)$ time and $O(R \cdot |F|)$ space, where $R$ is the number of reachable states, which can be as large as $2^{|F|}$.

## Relation to other models

- [State space](/state-space/) and [labelled transition system](/labelled-transition-system/): a STRIPS task is a compact description of a deterministic transition system with $2^{|F|}$ states. The task is exponentially smaller than the graph it describes, and this gap is the source of the hardness results.
- [SAS+](/sas-plus/): finite-domain variables instead of facts. Each fact becomes a binary variable, and each variable value $v = d$ becomes a fact, so the two models translate into each other in polynomial time with the same plans. Planners translate STRIPS into SAS+ because the variables make the mutual exclusions explicit.
- [PDDL](/pddl/): the input language. Its `:strips` fragment is lifted STRIPS: [action schemas](/action-schema/) with typed parameters, which [grounding](/grounding/) turns into the actions of this page.
- ADL and [conditional effects](/conditional-effects/): richer action languages with negative and disjunctive preconditions, quantifiers and effects that depend on the state. Nebel (2000) compares their expressive power with STRIPS by compilation schemes that preserve plan size.
- Situation calculus: a first-order logic of actions. A STRIPS action corresponds to effect axioms plus the assumption that nothing else changes; the [frame problem](/frame-problem/) page explains the link.
- [SAT](/sat/): a bounded plan question for a STRIPS task becomes a propositional formula with one copy of $F$ for each time step ([SATPLAN](/satplan/)).

## Known results in the model

### Plan existence is PSPACE-complete

Deciding whether a STRIPS task has a plan is PSPACE-complete (Bylander 1994). The proof is on [strips-plan-existence-pspace-complete](/strips-plan-existence-pspace-complete/), and the bounded version, a plan of length at most $k$, is on [bounded-plan-existence-np-complete](/bounded-plan-existence-np-complete/). If no action has a delete list, plan existence is polynomial, and this is the base of the [delete relaxation](/delete-relaxation/) heuristics.

### Some plans must have exponential length

The PSPACE bound leaves room for plans of length $2^{|F|}$, and some tasks need plans of length exponential in $|F|$. An $n$-bit counter shows it. Let $F = \{\mathit{on}_i, \mathit{off}_i : 1 \le i \le n\}$, let $I = \{\mathit{off}_1, \ldots, \mathit{off}_n\}$ and $G = \{\mathit{on}_1, \ldots, \mathit{on}_n\}$, and let $\mathit{inc}_i$ have $\mathit{pre} = \{\mathit{off}_i, \mathit{on}_1, \ldots, \mathit{on}_{i-1}\}$, $\mathit{add} = \{\mathit{on}_i, \mathit{off}_1, \ldots, \mathit{off}_{i-1}\}$ and $\mathit{del} = \{\mathit{off}_i, \mathit{on}_1, \ldots, \mathit{on}_{i-1}\}$. Read a reachable state as the binary number with bit $i$ set when $\mathit{on}_i$ holds. By induction on the plan prefix, every reachable state contains exactly one of $\mathit{on}_i$ and $\mathit{off}_i$ for each $i$, since each action adds one of the pair whenever it deletes the other. In such a state, $\mathit{inc}_i$ is applicable exactly when bit $i$ is the lowest bit that is $0$, so at most one action is applicable, and none in the state with all bits 1. That action clears the bits below $i$ and sets bit $i$, which adds 1 to the number. So the reachable states form one path $0, 1, \ldots, 2^n - 1$, and the only plan has $2^n - 1$ actions, with $|F| = 2n$ and $|A| = n$. For $n = 8$ that is 255 actions from 16 facts and 8 actions. The [Tower of Hanoi](/tower-of-hanoi/) gives the same effect with a natural domain.

### Expressive power

STRIPS with negative preconditions compiles into plain STRIPS by the complement facts described above, with the same plan lengths. Conditional effects are different: Nebel (2000) proves that they cannot be compiled into STRIPS so that plan length grows only linearly, while a polynomial growth in plan length is possible. The exact statements are on [conditional effects](/conditional-effects/).

## References
