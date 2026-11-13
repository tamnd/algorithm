---
tag: X17W61
kind: technique
slug: goal-regression
name: Goal regression
aliases: []
area: games-and-search/planning
level: intro
summary: Computes the weakest set of facts that must hold before a STRIPS action so that a goal holds after it, (g minus add) union pre, defined when the action deletes no goal fact.
prereqs: [strips, state-space-planning]
see_also: [backward-state-space-search, weakest-precondition, execution-monitoring, means-ends-analysis, pop-partial-order-planning, mutex-relation, forward-state-space-search, conditional-effects]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4, Section 4.3 (relevant actions and the regression set of a goal through an action)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.2 (regression of a goal description through a relevant action)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on classical planning (regression search; general locator)
---

Goal regression answers one question: what must be true before an action $a$ so that a set of facts $g$ is true after it? For a [STRIPS](/strips/) action the answer is a set of facts again,
$$ \mathit{regress}(g, a) = (g \setminus \mathit{add}(a)) \cup \mathit{pre}(a), $$
and it is defined only when $a$ deletes no fact of $g$. The facts that $a$ adds come for free, the other facts of $g$ must already hold, and the precondition must hold so that $a$ can run. This set is the weakest such condition: a state contains it exactly when $a$ applies in the state and leads to a state that contains $g$. In planning it is the step of [backward state-space search](/backward-state-space-search/), and in program verification it is the [weakest precondition](/weakest-precondition/) of an assignment. Regressing a goal through a whole plan, last action first, gives the condition under which the plan still works, which [execution monitoring](/execution-monitoring/) checks during execution.

## In plain words

You want the cup to be on the table after you put it down. What must be true before you put it down? You must hold the cup. The fact "the cup is on the table" comes from the action itself, so you do not need it before. Any other wish, such as "the door is closed", must already be true, because putting the cup down does not close the door.

One case does not work. If the action destroys one of your wishes, no situation before it can give you that wish after it. Then regression gives no answer. If you regress through a list of actions from the last to the first, you get what must be true at the start for the whole list to work.

## When it applies

- The actions are STRIPS actions, or SAS+ actions, with a precondition, an add list and a delete list, and the add and delete lists of each action are disjoint.
- The goal is a conjunction of facts, so a set of facts. With negative goals, disjunctions or [conditional effects](/conditional-effects/), regression still exists but gives a formula, not a set of facts; see the variations.
- It is useful when the action is *relevant* for $g$: it adds a fact of $g$ and deletes none. An action that adds nothing of $g$ is consistent with $g$ but makes no progress, since its regression contains $g$.

## The template

```pseudo id=main
REGRESS(g, a)
L1  if del(a) ∩ g ≠ ∅ then return ⊥              ▷ no state works
L2  return (g \ add(a)) ∪ pre(a)

REGRESS-PLAN(g, a_1 … a_k)
L3  c ← g
L4  for i ← k down to 1 do
L5      c ← REGRESS(c, a_i)
L6      if c = ⊥ then return ⊥
L7  return c
```

**Why REGRESS is exact.** Let $\mathit{add}(a) \cap \mathit{del}(a) = \emptyset$ and write $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. Claim: for every state $s$, $a$ applies in $s$ and $g \subseteq s[a]$ if and only if REGRESS returns a set $c$ with $c \subseteq s$. Case 1: $a$ deletes a fact $f \in g$. Then $f \notin \mathit{add}(a)$, so $f \notin s[a]$ for every $s$, and no state works; REGRESS returns $\bot$ at line L1. Case 2: $\mathit{del}(a) \cap g = \emptyset$. If $c \subseteq s$, then $\mathit{pre}(a) \subseteq s$, so $a$ applies; a fact of $g \cap \mathit{add}(a)$ is in $s[a]$, and a fact of $g \setminus \mathit{add}(a)$ is in $s$ and not deleted, so it is in $s[a]$. Conversely, if $a$ applies and $g \subseteq s[a]$, then $\mathit{pre}(a) \subseteq s$, and a fact of $g \setminus \mathit{add}(a)$ is in $s[a]$ without being added, so it is in $s$. Hence $c \subseteq s$.

**Why REGRESS-PLAN is exact.** Let $c_k = g$ and $c_{i-1} = \mathit{regress}(c_i, a_i)$, the value of $c$ after the pass for $i$. By induction on $k - i$: a state $s$ contains $c_i$ exactly when $a_{i+1}, \ldots, a_k$ applies from $s$ and ends in a state that contains $g$. For $i = k$ the sequence is empty. For the step, $s \supseteq c_{i-1}$ holds exactly when $a_i$ applies in $s$ and $s[a_i] \supseteq c_i$, by the exactness of REGRESS, and by the hypothesis $s[a_i] \supseteq c_i$ holds exactly when the rest of the plan works from $s[a_i]$. If some step gives $\bot$, no state works for the rest of the plan, so no state works for the whole plan. In particular, the plan solves a task with initial state $I$ exactly when $c_0 \ne \bot$ and $c_0 \subseteq I$.

**Monotonicity.** If $g \subseteq g'$ and REGRESS is defined on $g'$, then $\mathit{regress}(g, a) \subseteq \mathit{regress}(g', a)$, since both sets add the same $\mathit{pre}(a)$ to $g \setminus \mathit{add}(a) \subseteq g' \setminus \mathit{add}(a)$. A smaller goal never asks for more. Backward search uses this to prune a subgoal that contains a subgoal it has already reached.

**Cost.** With sets as bit vectors or sorted lists, REGRESS takes $O(n)$ time for $n$ facts, and REGRESS-PLAN takes $O(k n)$ time for a plan of $k$ actions.

## Classic examples

### One delivery step

In the delivery task of [forward search](/forward-state-space-search/), unload(B) has the precondition $\{t_B, p_T\}$, the add list $\{p_B\}$ and the delete list $\{p_T\}$. Then
$$ \mathit{regress}(\{p_B\}, \mathrm{unload(B)}) = (\{p_B\} \setminus \{p_B\}) \cup \{t_B, p_T\} = \{t_B, p_T\}: $$
to have the package at B after unloading, the truck must be at B with the package inside. The action load(B) deletes $p_B$, so $\mathit{regress}(\{p_B\}, \mathrm{load(B)}) = \bot$. The action drive(A,B) deletes only $t_A$, so its regression is defined, $\{t_A, p_B\}$, but it is not relevant: it adds nothing of the goal, and the regressed goal still contains $p_B$.

### The conditions along the Sussman plan

In the [blocks world](/blocks-world/) with the operators pickup, putdown, stack and unstack, take the [Sussman](/sussman-anomaly/) start: C on A, A and B on the table, the hand empty. The goal is $g = \{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$, and the plan is unstack(C,A), putdown(C), pickup(B), stack(B,C), pickup(A), stack(A,B). REGRESS-PLAN gives these conditions; $c_i$ is what must hold before step $i + 1$ for the rest of the plan to reach $g$.

| $i$ | next action | $c_i$ |
| --- | --- | --- |
| 6 | (none) | on(A,B), on(B,C) |
| 5 | stack(A,B) | holding(A), clear(B), on(B,C) |
| 4 | pickup(A) | clear(A), ontable(A), handempty, clear(B), on(B,C) |
| 3 | stack(B,C) | clear(A), ontable(A), holding(B), clear(C) |
| 2 | pickup(B) | clear(A), ontable(A), clear(B), ontable(B), handempty, clear(C) |
| 1 | putdown(C) | clear(A), ontable(A), clear(B), ontable(B), holding(C) |
| 0 | unstack(C,A) | on(C,A), clear(C), handempty, ontable(A), clear(B), ontable(B) |

The start state contains $c_0$, so the plan works. In this example $c_0$ is the whole start state, but in general it is smaller, and every state that contains it is a start from which the plan works. The table is a version of the triangle table of the PLANEX system: an executor checks before each step $i + 1$ that the current state contains $c_i$. If a block falls and the check fails for $c_i$ but holds for a later $c_j$, the executor can skip ahead to step $j + 1$; if it fails for all of them, it must [replan](/replanning/).

### A regressed goal that no state contains

Regress the same goal through stack(A,B) and then stack(B,C). The first step gives $\{\mathrm{holding}(A), \mathrm{clear}(B), \mathrm{on}(B,C)\}$. The action stack(B,C) is relevant for it, because it adds on(B,C) and clear(B) and deletes holding(B) and clear(C), none of which is in the set. The second step gives
$$ \{\mathrm{holding}(A), \mathrm{holding}(B), \mathrm{clear}(C)\}. $$
The hand holds one block at most, so no reachable state contains this set. Regression is exact about the action, but it knows nothing about which states can occur, so backward search can waste time on such sets. Planners remove them with [mutex](/mutex-relation/) pairs such as $\{\mathrm{holding}(A), \mathrm{holding}(B)\}$.

## Variations

- **Lifted regression.** With action schemas, regress a goal with variables through a schema whose effect unifies with a goal atom, and keep the bindings as constraints. This avoids [grounding](/grounding/), and it is the way the STRIPS system and [partial-order planners](/pop-partial-order-planning/) choose actions for open goals.
- **Negative literals and conditional effects.** For a literal goal $\ell$ and an action with conditional effects, $\ell$ holds after the action exactly when the precondition holds and either some effect that makes $\ell$ true fires, or $\ell$ holds before and no effect that makes it false fires. The result is a formula; the set rule above is the case with no conditions and no negations.
- **SAS+ regression.** With multi-valued variables, a partial assignment is regressed by removing the variables that the action sets, adding its precondition, and failing when the action sets a variable of the goal to another value or when the precondition conflicts with the rest of the goal.
- **Regression of formulas in logic.** In the situation calculus, Reiter's regression rewrites a formula about the situation after an action into a formula about the situation before it, with successor state axioms. The STRIPS rule is the special case in which these axioms say that a fact holds after the action if the action adds it, or if it held before and the action does not delete it.
- **Weakest preconditions.** Dijkstra's predicate transformer $\mathit{wp}(S, Q)$ is the same idea for programs: the weakest condition before the statement $S$ that makes $Q$ true after it. For an assignment it substitutes the expression for the variable in $Q$.

## Pitfalls

- **Regressing through a deleting action.** If $a$ deletes a fact of $g$, the formula $(g \setminus \mathit{add}(a)) \cup \mathit{pre}(a)$ still gives a set, but it is wrong: no state before $a$ gives $g$ after it. Test the delete list first.
- **Overlapping add and delete lists.** If $a$ adds and deletes the same fact $f$, the result of $a$ depends on the order of the effects. Under the rule $(s \setminus \mathit{del}) \cup \mathit{add}$ the fact holds after $a$; remove $f$ from the delete list before regressing, or the delete test gives $\bot$ where an answer exists.
- **Confusing defined with relevant.** A regression through an action that adds nothing of $g$ is defined, but it gives a superset of $g$, and a search that uses such actions makes no progress.
- **Reading the regressed set as a state.** It is a partial description, and it can be contained in no reachable state, as in the third example.
- **Regressing in the wrong order.** A plan is regressed from its last action to its first. Regressing $g$ through $a_1$ first gives the condition for the reversed plan.

## Exercises

1. In the delivery task, regress $G = \{p_B\}$ through the plan load(A), drive(A,B), unload(B), and check that the result is contained in $I = \{t_A, p_A\}$.
2. Prove that if $a$ is relevant for $g$, then $\mathit{regress}(g, a)$ does not contain $g$ unless $\mathit{pre}(a)$ contains the facts of $g \cap \mathit{add}(a)$.
3. Show that two different relevant actions can give the same regressed set, and that a regressed set can contain a fact of $\mathit{del}(a)$. Why is the second fact not a problem?
4. Give a task with 4 facts and an action $a$ such that $\mathit{regress}(g, a)$ is contained in no reachable state, although $a$ is applicable in some reachable state.
5. Extend REGRESS to goals that contain negative literals $\neg f$, for actions without conditional effects. When is the result $\bot$?

## References
