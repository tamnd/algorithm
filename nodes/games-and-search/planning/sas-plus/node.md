---
tag: 8Z7BSB
kind: model
slug: sas-plus
name: SAS+ finite-domain representation
aliases:
- finite-domain representation
- multi-valued state variables
- FDR
area: games-and-search/planning
level: advanced
summary: A planning model whose states assign a value to each of a few finite-domain variables, and whose operators test and set some of those variables.
prereqs: [strips, grounding]
see_also: [causal-graph-heuristic, classical-planning, pddl, invariant, multi-valued-decision-diagram, constraint-satisfaction-problem, landmark-heuristic, mutex-relation]
sources:
  - paper: doi:10.1111/j.1467-8640.1995.tb00052.x
    title: "Christer Bäckström and Bernhard Nebel, Complexity results for SAS+ planning, Computational Intelligence 11(4) (1995)"
    locator: the definition of SAS+ and the complexity results for its restrictions (general locator)
  - paper: doi:10.1016/j.artint.2008.10.013
    title: "Malte Helmert, Concise finite-domain representations for PDDL planning tasks, Artificial Intelligence 173(5-6) (2009)"
    locator: Section 1.2 (an example of a finite-domain representation), Section 5 (invariant synthesis) and Section 7 (generating the finite-domain variables)
  - paper: doi:10.1613/jair.1705
    title: "Malte Helmert, The Fast Downward planning system, Journal of Artificial Intelligence Research 26 (2006)"
    locator: pp. 191 to 246 (multi-valued planning tasks, domain transition graphs and causal graphs)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.5 (state-variable representation)
---

SAS+ is a planning model in which a state gives a value to each of a set of variables, and each variable has a small finite domain, instead of a truth value to each of a set of facts. An operator tests some variables and sets some variables. Bäckström and Nebel studied it in the early 1990s; the Fast Downward planner, the home of the [causal graph heuristic](/causal-graph-heuristic/), made it the standard internal form of [classical planning](/classical-planning/) tasks, under the name finite-domain representation. A [STRIPS](/strips/) task translates into SAS+ by finding groups of facts of which exactly one is true in every reachable state, and each group becomes one variable.

## The machine

### Tasks

A SAS+ task is a tuple $\Pi = (V, O, s_0, s_\star)$:

- $V$ is a finite set of variables, and each $v \in V$ has a finite domain $D_v$.
- A state is a full assignment $s$, with $s(v) \in D_v$ for each $v$. A partial assignment gives values to some of the variables.
- $O$ is a finite set of operators. Each operator $o$ has a precondition $\mathit{pre}(o)$ and an effect $\mathit{eff}(o)$, both partial assignments.
- $s_0$ is the initial state, and the goal $s_\star$ is a partial assignment.

Operator $o$ is applicable in $s$ when $s$ agrees with $\mathit{pre}(o)$ on every variable that $\mathit{pre}(o)$ assigns. The result $s'$ has $s'(v) = \mathit{eff}(o)(v)$ for each variable that $\mathit{eff}(o)$ assigns, and $s'(v) = s(v)$ for the others. A plan is a sequence of operators, each applicable in turn, from $s_0$ to a state that agrees with $s_\star$. Plans are sequential, and costs are unit unless the task gives an operator cost.

Bäckström and Nebel split the precondition into a part on the variables that the operator changes and a prevail condition on those it leaves unchanged; the definition above merges the two.

### From STRIPS to SAS+

A mutex group is a set of facts of which at most one is true in every reachable state; an exactly-one group has exactly one true fact in every reachable state. Such a group is an [invariant](/invariant/) of the task. The translation:

1. Find mutex groups. A sound test: at most one fact of the group holds in the initial state, and every action that adds a fact of the group adds only one, and either requires that fact already or requires and deletes another fact of the group. By induction on plans, at most one fact of the group then holds in every reachable state: in a state with one true group fact, the action either keeps that fact or replaces it. Helmert (2009) finds such groups for the lifted task by invariant synthesis.
2. Choose groups that cover the facts. A greedy cover takes the largest group first, removes its facts from the others, and repeats.
3. Turn each chosen group $\{f_1, \ldots, f_m\}$ into a variable with domain $\{f_1, \ldots, f_m\}$, plus a value $\bot$ ("none of them") unless the group is exactly-one. Each fact left over becomes a binary variable.
4. Translate each action: a precondition fact $f_i$ becomes $v = f_i$; an added fact $f_i$ becomes the effect $v = f_i$; a deleted fact $f_i$ that the action does not replace by another value of $v$ becomes the effect $v = \bot$.

Step 4 needs every deleted fact to be known true before the action, which holds when the action requires each fact it deletes, as in most domains.

### A worked example

In the four-operator [blocks world](/blocks-world/) with blocks $A$, $B$, $C$, three kinds of exactly-one groups hold:

- where block $x$ is: $\{\mathit{on}(x, y) : y \ne x\} \cup \{\mathit{ontable}(x), \mathit{holding}(x)\}$, with $n + 1 = 4$ facts;
- what is on block $y$: $\{\mathit{on}(x, y) : x \ne y\} \cup \{\mathit{clear}(y), \mathit{holding}(y)\}$, with 4 facts;
- the hand: $\{\mathit{holding}(x)\} \cup \{\mathit{handempty}\}$, with 4 facts.

The greedy cover picks the three "where" groups. They cover every $\mathit{on}$, $\mathit{ontable}$ and $\mathit{holding}$ fact, so the other groups shrink to $\{\mathit{clear}(y)\}$ and $\{\mathit{handempty}\}$, which become binary variables. The result has the variables $\mathit{pos}(A), \mathit{pos}(B), \mathit{pos}(C)$ with 4 values each and four binary variables, so there are $4^3 \cdot 2^4 = 1024$ full assignments, against $2^{16} = 65536$ subsets of the 16 STRIPS facts. In general $n$ blocks give $n$ variables of size $n + 1$ and $n + 1$ binary variables: $(n+1)^n 2^{n+1}$ assignments against $2^{(n+1)^2}$ fact sets.

The action $\mathit{unstack}(C, A)$ becomes the operator with $\mathit{pre} = \{\mathit{pos}(C) = A, \mathit{clear}(C) = \top, \mathit{handempty} = \top\}$ and $\mathit{eff} = \{\mathit{pos}(C) = \mathit{hand}, \mathit{clear}(A) = \top, \mathit{clear}(C) = \bot, \mathit{handempty} = \bot\}$. The STRIPS delete of $\mathit{on}(C, A)$ disappears: setting $\mathit{pos}(C)$ to a new value removes the old one.

The reachable parts of the two state spaces are isomorphic: the map from a STRIPS state to its SAS+ assignment is a bijection between reachable states, and it maps the edges of one onto the edges of the other. Both tasks have 5, 22 and 125 reachable states for 2, 3 and 4 blocks, and every goal has the same shortest plan length in both.

### Domain transition graphs and causal graphs

The domain transition graph of a variable $v$ has the vertex set $D_v$ and an arc $d \to d'$ for each operator that can change $v$ from $d$ to $d'$, labelled by the operator's conditions on other variables. The causal graph of the task has the vertex set $V$ and an arc $u \to v$ when some operator that changes $v$ has a condition on $u$ or also changes $u$. Neither graph has a natural counterpart in STRIPS. The [causal graph heuristic](/causal-graph-heuristic/) of Fast Downward solves the subproblems these graphs define, and many tractable classes are defined by the shape of the causal graph.

## What it counts

The size of a task is $\sum_v |D_v|$ plus the total size of the operators. The number of states is $\prod_{v} |D_v|$, which can be far smaller than $2^{|F|}$ for the STRIPS task with the same reachable states, because the variables encode the mutual exclusions; the reachable state count is the same in both. A state takes $\sum_v \lceil \log_2 |D_v| \rceil$ bits, which is $3 \cdot 2 + 4 = 10$ bits for three blocks against 16 bits in STRIPS.

Plan length and plan cost are the same as for the STRIPS task, since the translation maps plans to plans of the same length.

## Relation to other models

- [STRIPS](/strips/): each STRIPS fact is a binary variable, and each SAS+ value $v = d$ is a STRIPS fact $\langle v, d \rangle$; an effect $v = d$ then adds $\langle v, d \rangle$ and must delete the old value, which needs the old value in the precondition or one action for each possible old value. So the two models describe the same tasks, with translations that are polynomial when the old values are known.
- [PDDL](/pddl/): PDDL tasks are grounded and then translated into SAS+ by planners such as Fast Downward. The translation uses invariants of the lifted domain, found before [grounding](/grounding/).
- [Constraint satisfaction](/constraint-satisfaction-problem/): a state is an assignment to finite-domain variables, and a bounded plan question becomes a CSP with one copy of the variables for each step.
- [Multi-valued decision diagrams](/multi-valued-decision-diagram/): symbolic planners store sets of SAS+ states as decision diagrams over the variables.
- [Mutex relations](/mutex-relation/) in [Graphplan](/graphplan/) detect pairs of facts that cannot hold together; SAS+ variables encode such exclusions in the state itself.

## Known results in the model

- Plan existence for SAS+ is PSPACE-complete, as for STRIPS, since the translations are polynomial and keep plans.
- Bäckström and Nebel (1995) restrict SAS+ by four properties: post-unique (P), unary (U), binary (B) and single-valued (S). They show that optimal plans can be found in polynomial time for SAS+-PUS, and some plan in polynomial time for SAS+-US, and that these are the largest such classes under their restrictions.
- The translation from STRIPS keeps the reachable state space up to isomorphism, so it changes no plan length; it changes the number of possible assignments, from $2^{|F|}$ to $\prod_v |D_v|$, and the size of a stored state.
- Other tractable classes are defined by the shape of the causal graph and the size of the domains; the [causal graph heuristic](/causal-graph-heuristic/) uses the causal graph to split a task into subproblems that it can solve fast.

## References
