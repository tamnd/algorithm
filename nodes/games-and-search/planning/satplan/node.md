---
tag: WT1M0J
kind: algorithm
slug: satplan
name: SATPLAN
aliases:
- planning as satisfiability
area: games-and-search/planning
level: advanced
summary: Encodes bounded-length planning as a propositional SAT instance and solves it.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of ground actions, k: the horizon in parallel steps}
  time: {encode: O(k m (n + m)), solve: O(2^(k (n + m)) k^2 m (n + m)^2)}
  space: {formula: O(k m (n + m))}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1992
  people: [Henry Kautz, Bart Selman]
  note: Kautz and Selman proposed planning as satisfiability at ECAI 1992, and showed in 1996 that SAT encodings with a stochastic SAT solver beat the best planners of the time on hard benchmarks.
prereqs: [strips, sat, frame-problem]
see_also: [graphplan, planning-graph, mutex-relation, cdcl, incremental-sat, bounded-model-checking, bounded-plan-existence-np-complete, optimal-planning]
sources:
  - paper: "Henry Kautz and Bart Selman, Planning as satisfiability, Proceedings of ECAI 1992, Wiley"
    locator: pp. 359 to 363 (plans as models of a propositional formula)
  - paper: "Henry Kautz and Bart Selman, Pushing the envelope: planning, propositional logic, and stochastic search, Proceedings of AAAI 1996"
    locator: pp. 1194 to 1201 (encodings of a fixed horizon solved with stochastic local search)
  - paper: "Henry Kautz, David McAllester and Bart Selman, Encoding plans in propositional logic, Proceedings of KR 1996, Morgan Kaufmann"
    locator: pp. 374 to 385 (a comparison of encodings, with explanatory frame axioms)
  - paper: "Henry Kautz and Bart Selman, Unifying SAT-based and graph-based planning, Proceedings of IJCAI 1999"
    locator: pp. 318 to 325 (Blackbox, which translates the planning graph to SAT)
  - paper: doi:10.1016/j.artint.2006.08.002
    title: "Jussi Rintanen, Keijo Heljanko and Ilkka Niemelä, Planning as satisfiability: parallel plans and algorithms for plan search, Artificial Intelligence 170(12-13) (2006)"
    locator: pp. 1031 to 1080 (the forall-step and exists-step semantics of parallel plans, and the search over several horizons at once)
  - paper: doi:10.1016/j.artint.2012.08.001
    title: "Jussi Rintanen, Planning as satisfiability: heuristics, Artificial Intelligence 193 (2012)"
    locator: pp. 45 to 86 (planning-specific branching heuristics in a SAT solver)
  - paper: "Henry Kautz, Bart Selman and Jörg Hoffmann, SatPlan: planning as satisfiability, Abstracts of the 5th International Planning Competition, 2006"
    locator: the planner description (SatPlan06, built on the planning graph)
---

SATPLAN finds a plan for a [STRIPS](/strips/) task with a [SAT solver](/sat/). For a horizon $k$, it writes a propositional formula in [conjunctive normal form](/conjunctive-normal-form/) whose variables say which facts hold at each time $0, \ldots, k$ and which actions run at each step $1, \ldots, k$. The clauses state the initial state, the goal, the preconditions and effects of the actions, frame axioms that explain every change of a fact, and the exclusion of actions that interfere. The models of the formula are exactly the parallel plans of $k$ steps. SATPLAN tries $k = 0, 1, 2, \ldots$ and decodes the first model that it finds. So it returns a plan with the fewest parallel steps. Kautz and Selman (1992, 1996) introduced the method, and their SatPlan won the optimal track of the planning competition of 2004 and shared first place in it in 2006.

## In plain words

Fix how many steps the plan may have. Then write down, as a long list of yes-or-no rules, everything a plan of that length must obey. The start is as given. The goals hold at the end. An action can run only when what it needs is true. What it adds is true after it, and what it removes is false. Nothing changes unless some action changes it. Two actions that spoil each other do not run at the same step.

Give the rules to a program that finds yes-or-no values that obey them all. If it finds values, read off which actions are set to yes at each step: that is the plan. If no values exist, no plan of that length exists, so allow one more step and try again.

## The problem

The input is a STRIPS task $(F, A, I, G)$ with $n$ facts and $m$ ground actions, where $\mathrm{add}(a)$ and $\mathrm{del}(a)$ are disjoint for each action. Two distinct actions interfere when one deletes a precondition or an add effect of the other. A step is a set of actions that are applicable in the current state and pairwise do not interfere, and its result is the state minus all deletes plus all adds. The empty step is allowed. A parallel plan of $k$ steps is a sequence of $k$ steps from $I$ that ends in a state that contains $G$. This is the plan notion of [GRAPHPLAN](/graphplan/). The output is a parallel plan with the fewest steps, or "no plan" when no plan has at most a given number of steps.

## The algorithm

```pseudo id=main
SATPLAN(F, A, I, G, K)
L1  for k ← 0, 1, ..., K do
L2      Φ ← ENCODE(k)
L3      σ ← SAT(Φ)   ▷ hole: the SAT solver
L4      if σ ≠ unsatisfiable then return the steps S_t = {a : σ(a_t) = true} for t = 1, ..., k
L5  return no plan

ENCODE(k)   ▷ a variable f_t for each fact and time 0..k, and a_t for each action and step 1..k
L6  for each fact f: the clause f_0 if f ∈ I, else ¬f_0
L7  for each goal g: the clause g_k
L8  for each t and a: ¬a_t ∨ p_{t-1} for p ∈ pre(a); ¬a_t ∨ f_t for f ∈ add(a); ¬a_t ∨ ¬f_t for f ∈ del(a)
L9  for each t and f: ¬f_{t-1} ∨ f_t ∨ (some a_t with f ∈ del(a)); f_{t-1} ∨ ¬f_t ∨ (some a_t with f ∈ add(a))
L10 for each t and each pair of interfering actions a, b: ¬a_t ∨ ¬b_t
```

Lines L6 and L7 fix the start and the end. The initial state is complete: a fact that is not in $I$ is false at time 0. Line L8 holds the precondition and effect axioms. Each is a clause of two literals: "if $a$ runs at step $t$, then $p$ held before" and "then $f$ holds after".

Line L9 holds the explanatory frame axioms. The first clause says that if $f$ was true and became false, some action that deletes $f$ ran. The second says that if $f$ became true, some action that adds $f$ ran. Without them, a model could change facts at no cost. These clauses solve the [frame problem](/frame-problem/) with one clause per fact and step, not one per fact and action.

Line L10 forbids two interfering actions in the same step. With it, every order of the actions of a step is a valid sequential order, and all orders give the same state.

Line L3 is the hole: any complete SAT solver fits. The implementation here uses a small [DPLL](/dpll/) solver with [unit propagation](/unit-propagation/). Kautz and Selman (1996) used the local search solver [WalkSAT](/walksat/), and later SatPlan versions use [CDCL](/cdcl/) solvers. A local search solver can find a plan but can never prove that a horizon is unsatisfiable, so with it the plan need not have the fewest steps.

The bound $K$ in line L1 makes the loop finite. The value $K = 2^n - 1$ is always enough, because a shortest sequential plan never visits a state twice. In practice the loop starts at the first level of the [planning graph](/planning-graph/) where the goals hold without mutex, and a time or memory limit stops it.

## Example

**A logistics task.** A truck is at $l_1$ with packages $p_1$ and $p_2$, and the goal is both packages at $l_2$. The actions are $\mathit{load}(p, l)$, $\mathit{unload}(p, l)$ and $\mathit{drive}(l, l')$. This gives $n = 8$ facts and $m = 10$ actions, and 19 pairs of interfering actions. Each step adds 18 precondition clauses, 10 add clauses, 10 delete clauses, 16 frame clauses and 19 exclusion clauses, so 73 clauses. The initial state and the goal add 10 clauses.

| horizon $k$ | variables | clauses | satisfiable | models |
|---|---|---|---|---|
| 0 | 8 | 10 | no | 0 |
| 1 | 26 | 83 | no | 0 |
| 2 | 44 | 156 | no | 0 |
| 3 | 62 | 229 | yes | 1 |
| 4 | 80 | 302 | yes | 9 |

The formula for $k = 3$ has exactly one model, which is the plan $\{\mathit{load}(p_1, l_1), \mathit{load}(p_2, l_1)\}$, $\{\mathit{drive}(l_1, l_2)\}$, $\{\mathit{unload}(p_1, l_2), \mathit{unload}(p_2, l_2)\}$. It has 3 steps and 5 actions. The unsatisfiable formulas for $k \le 2$ prove that no plan has fewer steps. The 9 models for $k = 4$ are the 9 plans of 4 steps, which include the same plan with an empty step in each of 4 places.

**Why line L10 is needed.** Let action $a$ need $p$, add $q$ and delete $p$, and let action $b$ need $p$ and add $r$. The initial state is $\{p\}$ and the goal is $\{q, r\}$. Actions $a$ and $b$ interfere, because $a$ deletes a precondition of $b$. So the formula for $k = 1$ is unsatisfiable, and SATPLAN returns $\{b\}, \{a\}$ for $k = 2$. Without the L10 clause, the formula for $k = 1$ has a model with $a$ and $b$ in the same step. In this case the order $b, a$ happens to work, but the order $a, b$ does not, and in general neither order needs to work.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness/). The results are these.

1. **Models are plans.** If $\sigma$ satisfies the formula for horizon $k$, the actions set to true at each step form a parallel plan of $k$ steps, and the fact variables give its states. Preconditions hold by L8, steps have no interfering pair by L10, and the frame clauses of L9 force each fact at time $t$ to be the result of the step.
2. **Plans are models.** Each parallel plan of $k$ steps gives one model, and the action values fix the fact values. So the models and the plans of $k$ steps are in a one-to-one correspondence, and the formula is satisfiable exactly when a plan of $k$ steps exists.
3. **Fewest steps.** An empty step can be appended to any plan, so the formulas become satisfiable at the fewest number of steps $k^*$ and stay satisfiable. SATPLAN stops at $k^*$, and no step of the plan it returns is empty.
4. **Termination and completeness.** The loop runs at most $K + 1$ times, and each SAT call terminates. With $K = 2^n - 1$, SATPLAN returns no plan exactly when the task has no plan.

## Complexity

The formula for horizon $k$ has $n (k + 1) + m k$ variables. Each step adds the clauses of L8 to L10. The precondition and effect clauses have $O(m n)$ literals in total, the frame clauses have $O(n m)$ literals, and there are at most $m^2 / 2$ exclusion clauses. So the formula has $O(k m (n + m))$ literals and is built in that time.

The SAT call dominates. Deciding whether a plan of at most $k$ steps exists is [NP-complete](/bounded-plan-existence-np-complete/) when $k$ is bounded by a polynomial in the input, so no polynomial bound is expected. The unit clauses of line L6 fix the $n$ variables of time 0. DPLL then explores at most $2^{k (n + m)}$ branches, and each call spends $O(k (n + m))$ rounds of propagation over a formula of $O(k m (n + m))$ literals. The crude proved bound is $O(2^{k (n + m)} k^2 m (n + m)^2)$ per horizon, and the sum over the horizons up to $k$ is at most twice that. Deciding whether any plan exists is [PSPACE-complete](/strips-plan-existence-pspace-complete/), and the needed horizon can be exponential in $n$.

The memory is the formula, $O(k m (n + m))$ literals, plus the state of the solver.

## Properties

- **Step optimal.** With a complete solver, the plan has the fewest parallel steps under the same step notion as GRAPHPLAN.
- **Not action optimal.** A plan with fewer steps can have more actions, and a model can also contain actions that the plan does not need.
- **Complete up to the bound.** It returns a plan when one with at most $K$ steps exists, and "no plan" otherwise.
- **Deterministic.** With a deterministic solver, the same task gives the same plan.
- **Solver independent.** Any progress in SAT solvers helps without a change to the planner.

## Variants and improvements

- **Encodings from the planning graph.** Blackbox (Kautz and Selman 1999) and SatPlan04 and SatPlan06 build the [planning graph](/planning-graph/) first. Only facts and actions that appear at a level get variables, and the [mutexes](/mutex-relation/) of the graph become extra binary clauses. This makes the formulas smaller and the search faster.
- **Other encodings.** Kautz, McAllester and Selman (1996) compare several encodings, among them ones that remove the action variables or the fact variables and ones that split each action into smaller parts.
- **Sequential plans.** Replace line L10 by "at most one action per step". Then $k$ counts actions, and SATPLAN returns a plan with the fewest actions, with many more horizons to try.
- **Exists-step semantics.** Rintanen, Heljanko and Niemelä (2006) allow a step when some order of its actions is valid, not every order. Plans then have fewer steps. They also give encodings of the exclusion with a linear number of clauses, in place of one clause per pair.
- **Better horizon search.** Rintanen, Heljanko and Niemelä (2006) solve several horizons at once and give each a share of the time, so that a hard unsatisfiable horizon below the first satisfiable one does not block the search. The plans are then no longer step optimal.
- **Incremental solving.** The formula for $k + 1$ contains the formula for $k$ with the goal clauses removed. An [incremental SAT solver](/incremental-sat/) keeps the learned clauses between horizons and puts the goal clauses in as assumptions.
- **Planning heuristics in the solver.** Madagascar (Rintanen 2012) branches on the variables with a rule that follows the goals backward, and it is competitive with heuristic search planners for finding some plan.
- **Model checking.** The same unrolling of a transition system for $k$ steps is [bounded model checking](/bounded-model-checking/).

## When to use it

Use SATPLAN when the plan should have few parallel steps, when the plans are short, and when many actions can run at the same time, as in logistics. Each extra step makes the formula larger, so long sequential plans are a poor fit, and for those a heuristic forward planner such as the [Fast-Forward planner](/fast-forward-planner/) is usually faster. SATPLAN is also a good choice when a strong SAT solver is at hand, or when the task has extra constraints that are easy to state as clauses.

## Pitfalls

- **Missing frame axioms.** Without the clauses of line L9, a fact can become true with no action that adds it, and the decoded plan fails.
- **Missing exclusion clauses.** Without line L10, a step can hold an action that deletes the precondition of another, as in the example above.
- **Partial initial state.** Every fact that is not in $I$ needs the unit clause $\neg f_0$. Without it, the solver can choose the initial state.
- **Add and delete of the same fact.** The encoding assumes that $\mathrm{add}(a)$ and $\mathrm{del}(a)$ are disjoint. If an action both adds and deletes a fact, L8 makes it unusable. Remove the fact from the delete list first, as in the usual STRIPS semantics where the add wins.
- **No stop on unsolvable tasks.** Without a bound, the loop runs forever when no plan exists. The bound $2^n - 1$ is correct but too large to reach in practice.
- **Useless actions.** A model can set to true an action that does no harm and no good. Remove such actions after decoding if the plan is to be short in actions.
- **Local search and optimality.** A local search solver cannot prove a horizon unsatisfiable. Do not claim fewest steps without a complete solver.

## Implementations

## History

Kautz and Selman (1992) proposed to treat planning as satisfiability: a plan is a model of a formula, not a proof as in the deductive planning of the time. In 1996 they showed with SATPLAN and the WalkSAT solver that such encodings solved hard logistics and blocks world tasks many times faster than the best planners then known, including GRAPHPLAN. In the same year, Kautz, McAllester and Selman compared many encodings. Blackbox, which joined the planning graph with SAT, took part in the first planning competition in 1998, and Kautz and Selman described it in 1999. SatPlan04 won the optimal track of the planning competition of 2004, and SatPlan06 shared first place there with MaxPlan in 2006. Rintanen, Heljanko and Niemelä (2006) gave new semantics for parallel steps and new horizon searches, and Madagascar (Rintanen 2012) made SAT planning competitive for finding any plan.

## References
