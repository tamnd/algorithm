---
tag: KSWASX
kind: technique
slug: relaxed-plan-heuristic
name: Relaxed plan heuristic
aliases:
- FF heuristic
area: games-and-search/planning
level: advanced
summary: Heuristic given by the length of a relaxed plan extracted from the relaxed planning graph.
prereqs: [delete-relaxation, relaxed-planning-graph, heuristic-function]
see_also: [fast-forward-planner, enforced-hill-climbing, h-add-heuristic, h-max-heuristic, hsp-planner, landmark-heuristic, greedy-best-first-search, admissible-heuristic]
sources:
  - paper: doi:10.1613/jair.855
    title: "Joerg Hoffmann and Bernhard Nebel, The FF planning system: fast plan generation through heuristic search, Journal of Artificial Intelligence Research 14 (2001)"
    locator: pp. 253 to 302; Section 4 and Equation 3 (the heuristic as the size of a relaxed plan), Section 4.2 (no-ops first, the difficulty rule, linearization), Section 6.1 and Equation 5 (helpful actions)
  - paper: doi:10.1613/jair.1747
    title: "Joerg Hoffmann, Where ignoring delete lists works: local search topology in planning benchmarks, Journal of Artificial Intelligence Research 24 (2005)"
    locator: pp. 685 to 758 (the topology of the search space under h+ in the benchmark domains; general locator)
  - paper: doi:10.1613/jair.2972
    title: "Silvia Richter and Matthias Westphal, The LAMA planner: guiding cost-based anytime planning with landmarks, Journal of Artificial Intelligence Research 39 (2010)"
    locator: the cost-sensitive FF heuristic used together with landmarks (general locator)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on classical planning heuristics (relaxed plans and their relation to h_max and h_add; general locator)
---

The relaxed plan heuristic, or FF heuristic $h_{FF}$, estimates the distance from a state $s$ to the goal by the number of actions in one relaxed plan: a plan for the task with all delete lists removed, as in the [delete relaxation](/delete-relaxation/). The plan is found greedily on the [relaxed planning graph](/relaxed-planning-graph/) built from $s$, in time polynomial in the task. The optimal relaxed plan length $h^+$ is admissible but NP-hard to compute, and $h_{FF}$ is an upper bound on $h^+$, so $h_{FF}$ is not admissible. It is $0$ exactly at goal states and $\infty$ exactly when the goal is unreachable without deletes, which proves a dead end. Unlike the sum of the costs of the goals in [$h^{\mathrm{add}}$](/h-add-heuristic/), a relaxed plan counts a shared subgoal once. Hoffmann and Nebel (2001) introduced it in the [Fast-Forward planner](/fast-forward-planner/), together with the helpful actions that the same extraction yields.

## In plain words

To guess how far a state is from the goal, solve an easier puzzle in which nothing ever gets undone. In that world, a fact once made true stays true, so planning is easy: just keep firing actions. Find a plan in this easy world, without trying to make it the best one, and count its actions. That count is the guess.

The guess is often good, because the easy plan still has to do most of the real work. It can be too low, because the real world forces you to redo things. It can also be too high, because the quick search for the easy plan may pick more actions than needed. As a bonus, the first actions of the easy plan point to good first moves.

## When it applies

- The task is a [STRIPS](/strips/) task, or a finite-domain task that compiles to one, and a forward search needs a goal-distance estimate in each state.
- Plans need not be optimal. For optimal plans, use an [admissible](/admissible-heuristic/) heuristic such as [$h^{\max}$](/h-max-heuristic/) or an admissible [landmark heuristic](/landmark-heuristic/).
- The main difficulty of the task is in its positive interactions, many goals that share subgoals, rather than in resources that actions use up. Delete effects are what the relaxation ignores, so tasks whose hardness comes from deletes get weak estimates.

## The template

```pseudo id=main
RELAXED-PLAN-HEURISTIC(A, s, G)
L1  build the relaxed planning graph of A from s until G appears or no new fact appears   ▷ hole: unit layers or costs
L2  if some goal of G never appears then return ∞
L3  π ← a relaxed plan extracted backward from G on the graph   ▷ hole: the choice of achiever for each subgoal
L4  H ← the actions applicable in s that add a subgoal of level 1   ▷ optional: helpful actions
L5  return the number of actions of π, and H   ▷ hole: count actions or sum action costs
```

**The holes.** Line L1 can use unit layers, as FF does, or costs from $h^{\max}$ or $h^{\mathrm{add}}$. Line L3 chooses an achiever for each subgoal. FF takes an achiever from the layer just below the subgoal's first level, with the least *difficulty*, the sum of the levels of its preconditions (Hoffmann and Nebel 2001, Equation 4). With costs, the usual choice is the achiever that gives the subgoal its $h^{\mathrm{add}}$ or $h^{\max}$ value. Line L5 counts the actions, or sums their costs when actions have costs.

**Why it is a relaxed plan.** The extraction must order the chosen actions so that each one comes after a supplier of each of its preconditions. The [relaxed planning graph](/relaxed-planning-graph/) page gives the extraction with the need positions and proves that the result is a relaxed plan with no action twice. This is the fact behind every claim below.

**Bounds.** Let $h^+(s)$ be the length of a shortest relaxed plan from $s$, and $h^*(s)$ the real goal distance.

1. $h^+(s) \le h^*(s)$, since a real plan is a relaxed plan: deleting fewer facts never makes an action inapplicable.
2. $h^+(s) \le h_{FF}(s)$, since the extracted plan is a relaxed plan.
3. $h_{FF}(s) = 0$ if and only if $G \subseteq s$. If $G \subseteq s$, the graph has one level and nothing is extracted. Otherwise some goal is at a level $\ge 1$, and some chosen action adds it.
4. $h_{FF}(s) = \infty$ if and only if $h^+(s) = \infty$, and then $h^*(s) = \infty$, so the state is a dead end.

There is no bound the other way: $h_{FF}$ can exceed $h^*$. In the example below, $h_{FF} = 4$ and $h^* = h^+ = 3$.

**Helpful actions.** Line L4 is Equation 5 of Hoffmann and Nebel (2001). The relaxed plan starts with actions from the first layer, and these are applicable in $s$. The helpful actions are all applicable actions that add a fact the relaxed plan needs at level 1. They include the first action of the relaxed plan, but a real plan may start with an action that is not helpful.

**Cost.** One evaluation builds the graph in $O(k m n)$ time for $k$ layers, $m$ actions and $n$ facts, or in time linear in the task with counters, and extracts in $O(n (m + n))$. Forward search pays this in every evaluated state, so planners cache and prune: FF evaluates only the successors it generates, and with helpful actions it generates fewer.

## Classic examples

### Shared preconditions

Hoffmann and Nebel (2001, Section 4) use three actions: $op_P$ adds $P$, and $op_{G_1}$ and $op_{G_2}$ need $P$ and add $G_1$ and $G_2$. From the empty state, $h^{\mathrm{add}}$ counts $P$ once for each goal and gives 4. The relaxed plan is $op_P, op_{G_1}, op_{G_2}$, so $h_{FF} = 3$, the true distance.

### A greedy choice that overshoots

Let $p_P$ and $p_Q$ add $P$ and $Q$; let $a_1$ need $P$ and add $g_1$, $b$ need $Q$ and add $g_2$, and $x$ need $P$ and $Q$ and add both goals. The difficulty of $a_1$ and $b$ is 1, that of $x$ is 2, so the extraction picks $a_1$ and $b$ and returns $p_P, p_Q, a_1, b$: $h_{FF} = 4$. The plan $p_P, p_Q, x$ shows $h^* = h^+ = 3$. So $h_{FF}$ is not admissible, and it is not $h^+$ either.

### Blocks world

In the [blocks world](/blocks-world/) with three blocks on the table and the goal $\mathit{on}(A, B)$, $\mathit{on}(B, C)$, $h_{FF} = 4 = h^*$ in the initial state. Over the 22 reachable states, $h_{FF}$ is below $h^*$ in 14, equal in 7 and above in 1. With four blocks and the goal of a tower $A, B, C, D$, the counts over the 125 states are 107 below, 15 equal and 3 above. These are measured on the implementation of this page. The relaxation loses the cost of unstacking blocks that are in the way, so most estimates are low.

### Sliding tile puzzle

In the STRIPS form of the [sliding tile puzzle](/sliding-tile-puzzle/), an action moves tile $t$ from cell $c$ to an adjacent blank cell $e$: it needs $\mathit{at}(t, c)$ and $\mathit{blank}(e)$, adds $\mathit{at}(t, e)$ and $\mathit{blank}(c)$, and deletes the two preconditions. Without deletes, each tile must still walk to its goal cell one cell per action, so $h^+$ is at least the Manhattan distance. On the 360 states of the $2 \times 3$ puzzle, measured here, $h_{FF}$ is never below the Manhattan distance and is above it in 279 states. It is above $h^*$ in 43 states. The hardest state has $h^* = 21$, and there $h_{FF} = h^+ = 7$ and the Manhattan distance is 5: the relaxation lets the blank be in many places at once.

### Search algorithms that use it

- The [Fast-Forward planner](/fast-forward-planner/) runs [enforced hill climbing](/enforced-hill-climbing/) on $h_{FF}$ with helpful actions, and falls back to best-first search.
- [Greedy best-first search](/greedy-best-first-search/) with $h_{FF}$ and helpful actions as preferred operators is the core of many later satisficing planners. LAMA (Richter and Westphal 2010) combines a cost-aware $h_{FF}$ with a landmark heuristic.
- [Weighted A*](/weighted-a-star/) with $h_{FF}$ gives plans of better quality at a higher cost, with no bound, since $h_{FF}$ is not admissible.

## Variations

- **Costs.** With action costs, build the graph by $h^{\mathrm{add}}$ or $h^{\max}$ costs, pick for each subgoal its best supporter, and sum the costs of the relaxed plan. LAMA uses such a version.
- **Plan length versus parallel steps.** FF counts actions. Counting the layers of the relaxed plan gives the unit-cost $h^{\max}$ of the goal set, a weaker but admissible estimate.
- **Optimal relaxed plans.** Computing $h^+$ exactly is NP-hard (Bylander 1994; see [delete relaxation](/delete-relaxation/)). It is admissible and is used in optimal planning on small tasks.
- **Partial relaxations.** Keeping some deletes, through conjunctions of facts or red and black variables, sits between $h^+$ and $h^*$ and fixes some of the blind spots of the delete relaxation.
- **Linearization.** Hoffmann and Nebel (2001, Section 4.2.3) note that the order of actions inside one layer can save subgoals, but that choosing the best order is NP-complete, so FF uses the order of selection.

## Pitfalls

- **Treating $h_{FF}$ as admissible.** A* with $h_{FF}$ need not return optimal plans, as the overshoot example shows.
- **Marking add effects too early.** If an added fact counts as achieved for actions that come earlier in the order, the result is not a relaxed plan and can be shorter than $h^+$. The relaxed planning graph page gives a four-action example.
- **Pruning to helpful actions only.** A real plan can need an action that is not helpful. FF prunes to helpful actions in hill climbing and drops the pruning in its complete fallback.
- **Ignoring dead ends.** $h_{FF} = \infty$ proves a dead end, but a finite $h_{FF}$ does not prove the opposite. In the sliding tile puzzle with the wrong parity, every state has a finite $h_{FF}$ and no plan.
- **Comparing values across tie-breaking rules.** Two correct extractions can return relaxed plans of different lengths. A test that expects one exact value must fix the order of goals and achievers.

## Exercises

1. Show that $h_{FF}(s) \ge \max_{g \in G} \mathrm{level}(g)$ for the unit-cost levels of the relaxed planning graph.
2. Give a task in which $h_{FF}(s) < h^*(s)$ by a factor that grows with the size of the task. (Hint: a resource that must be returned after each use.)
3. In the overshoot example, change the difficulty rule so that the extraction prefers achievers that add more open goals. What is $h_{FF}$ then, and is the new rule always better?

## References
