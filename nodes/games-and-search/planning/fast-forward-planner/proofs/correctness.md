---
title: FF returns a valid plan when the task has one, and reports no plan only when the task has none
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. The task is a STRIPS task $(F, A, I, G)$ with finitely many facts, so the set of states reachable from $I$ is finite; call its size $n$. For a state $s$, $h_{FF}(s)$ is the length of the relaxed plan that the [relaxed planning graph](/relaxed-planning-graph/) extraction returns from $s$, or $\infty$ when the goal is not reachable from $s$ in the delete relaxation. We use two facts proved on the relaxed planning graph page: $h_{FF}(s) = 0$ exactly when $G \subseteq s$, and $h_{FF}(s) = \infty$ exactly when no relaxed plan from $s$ exists.

**Lemma 1 (dead ends).** If $h_{FF}(s) = \infty$, then no plan from $s$ reaches $G$. If moreover $t$ is a successor of $s$, then $h_{FF}(t) = \infty$.

*Proof.* A plan from $s$ is also a relaxed plan from $s$: if an action is applicable after some deletes, it is applicable when nothing is deleted, and the relaxed state always contains the real one. So a plan would give a relaxed plan. For the second part, let $t$ be the result of $a$ in $s$. Every fact of $t$ is in $s$ or in $\mathrm{add}(a)$. A relaxed plan $\rho$ from $t$ would give the relaxed plan $a, \rho$ from $s$. $\square$

**Lemma 2 (the first phase).** If line L1 returns a plan, it leads from $I$ to a state that contains $G$.

*Proof.* The first phase is [enforced hill climbing](/enforced-hill-climbing/) with the successor function of lines L4 to L8. That function yields only pairs $(a, t)$ where $a$ is applicable in $s$ and $t$ is its result (lines L5 and L6), so it is a subset of the real successor function. Theorem 1 of the enforced hill climbing proof uses only that the successors are real, so every path that the phase appends is a real path, and the phase stops only in a goal state. $\square$

**Lemma 3 (the second phase).** GREEDY-BEST-FIRST returns a plan from $I$ to a goal state if one exists, and no plan otherwise. It stops after at most $n$ removals from open.

*Proof.* Each state enters seen at most once (line L13), so at most $n$ states enter open, and the loop stops. A state enters open with a recorded parent $(s, a)$ where $a$ is applicable in $s$, so the parents give a real path from $I$, and line L12 returns only a goal state.

Suppose a plan exists, but the search returns no plan. Let $I = x_0, x_1, \ldots, x_d$ be the states of a plan, with $G \subseteq x_d$. No $x_j$ is a dead end, so $h_{FF}(x_j) < \infty$ by Lemma 1, and $x_0$ enters open at line L9. A state $x_j$ enters seen only together with open, because its value is finite, and open ends empty, so every $x_j$ that enters seen is removed at line L11 at some point. Let $j$ be the largest index such that $x_j$ entered seen. If $j = d$, then line L12 returns when $x_d$ is removed, a contradiction. If $j < d$, then when $x_j$ is removed, either it is a goal state and line L12 returns, or line L13 looks at $x_{j+1}$, which is in seen already or enters it now. Both contradict the assumptions. $\square$

**Theorem (correctness and termination).** FF stops. If the task has a plan, FF returns a plan, and every plan it returns is valid. If the task has no plan, FF returns no plan.

*Proof.* The first phase stops, by Theorem 2 of the enforced hill climbing proof, which needs only a finite state space and integer values. If it returns a plan, the plan is valid by Lemma 2. Otherwise line L3 runs the second phase from $I$, and Lemma 3 gives the rest. If the task has no plan, the first phase cannot return a plan, by Lemma 2, so FF returns the answer of the second phase, which is no plan. $\square$

**Remark (the pruning rules).** Helpful actions and added goal deletion may cut every plan from the first phase, even on tasks with no dead ends. The page gives an example of each, both from Hoffmann and Nebel (2001, Sections 6.1.1 and 6.2.1). The theorem does not depend on them, because the second phase uses neither rule. What the rules lose is speed, not completeness: in the worst case, FF does the work of both phases.

**Remark (no optimality).** Neither phase minimizes the plan length. The first phase commits to each step for good, and the second phase orders states by the estimate alone, not by the cost so far. The page shows a blocks world task where the second phase returns 10 actions and a plan of 6 exists.
