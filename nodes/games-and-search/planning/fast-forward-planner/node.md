---
tag: RWBN9P
kind: algorithm
slug: fast-forward-planner
name: Fast-Forward (FF) planner
aliases:
- FF
area: games-and-search/planning
level: advanced
summary: Heuristic forward planner combining the relaxed-plan heuristic with enforced hill climbing.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of reachable states, b: the largest number of applicable actions in a state, k: the heuristic value of the initial state, e: the time of one relaxed plan extraction}
  time: {first-phase: O(k n b e), second-phase: O(n b (e + log n))}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 2000
  people: [Joerg Hoffmann, Bernhard Nebel]
  note: FF took part in the planning competition at AIPS 2000, where it was the fastest of the fully automatic planners, and Hoffmann and Nebel described it in full in 2001.
prereqs: [relaxed-plan-heuristic, enforced-hill-climbing, greedy-best-first-search]
see_also: [hsp-planner, relaxed-planning-graph, h-add-heuristic, graphplan, satplan, landmark-heuristic, international-planning-competition, sussman-anomaly]
sources:
  - paper: doi:10.1613/jair.855
    title: "Joerg Hoffmann and Bernhard Nebel, The FF planning system: fast plan generation through heuristic search, Journal of Artificial Intelligence Research 14 (2001)"
    locator: pp. 253 to 302; Section 2 and Figure 1 (the architecture), Section 4 (the heuristic), Section 5 (enforced hill climbing and the best-first fallback), Section 6.1 and Equation 5 (helpful actions), Section 6.2 (added goal deletion and the goal agenda), Section 7 (ADL), Section 8.1 (the AIPS 2000 competition)
  - paper: "Joerg Hoffmann, A heuristic for domain independent planning and its use in an enforced hill-climbing algorithm, Proceedings of the 12th International Symposium on Methodologies for Intelligent Systems (ISMIS 2000), Springer"
    locator: pp. 216 to 227 (the first description of the heuristic and the search)
  - paper: doi:10.1613/jair.1144
    title: "Joerg Hoffmann, The Metric-FF planning system: translating ignoring delete lists to numeric state variables, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 291 to 341 (the extension of FF to numeric state variables)
  - paper: doi:10.1613/jair.1747
    title: "Joerg Hoffmann, Where ignoring delete lists works: local search topology in planning benchmarks, Journal of Artificial Intelligence Research 24 (2005)"
    locator: pp. 685 to 758 (why the search of FF works on the benchmark domains; general locator)
---

The Fast-Forward planner, FF for short, is a planner for [STRIPS](/strips/) tasks, and in its full form for ADL tasks, by Hoffmann and Nebel. It searches forward from the initial state. It rates each state by the [relaxed plan heuristic](/relaxed-plan-heuristic/): the length of a plan for the task with all deletes ignored, extracted from a [relaxed planning graph](/relaxed-planning-graph/). It moves by [enforced hill climbing](/enforced-hill-climbing/), which runs a breadth-first search from the current state to the nearest strictly better state. Two pruning rules that come from the same relaxed plan make this fast: only *helpful actions* are tried, and a state is dropped when its relaxed plan undoes a goal that was just reached. If this first phase fails, FF starts again with a complete greedy best-first search and no pruning. So FF returns a plan exactly when one exists, but not a shortest one. At the planning competition of AIPS 2000 it was the fastest of the fully automatic planners.

## In plain words

FF plans like a person in a hurry. In each situation it asks a simpler question: if nothing I did could ever be undone, how many steps would I need? The answer is quick to compute, and it is the guide. FF also notes which first moves that quick answer used, and it tries only those moves.

It keeps taking moves that make the guide's number smaller. When no move helps right away, it looks a few moves ahead until something helps. It never goes back, so it can walk into a trap. In that case it throws the attempt away and does a slower, careful search that tries all moves and cannot get trapped.

## The problem

The input is a STRIPS task: a finite set of facts, a set $A$ of actions with preconditions, add lists and delete lists, an initial state $I$, and a goal $G$. The output is a sequence of actions that leads from $I$ to a state that contains $G$, or "no plan" when there is none. There is no bound on the plan length, and FF does not try to minimize it. This is satisficing [classical planning](/classical-planning/).

## The algorithm

```pseudo id=main
FF(A, I, G)
L1  π ← ENFORCED-HILL-CLIMBING(I) on h_FF, with SUCCESSORS-EHC as the successor function
L2  if π ≠ failure then return π
L3  return GREEDY-BEST-FIRST(I) on h_FF, with all successors and no pruning

SUCCESSORS-EHC(s)
L4  (ρ, G_1) ← the relaxed plan from s and the subgoals it needs at level 1
L5  H ← the actions a applicable in s with add(a) ∩ G_1 ≠ ∅   ▷ helpful actions
L6  for each a in H do t ← the result of a in s
L7      if the relaxed plan from t deletes a goal of add(a) ∩ G then skip t   ▷ added goal deletion
L8      else yield (a, t)

GREEDY-BEST-FIRST(I)
L9  if h_FF(I) = ∞ then return no plan ; open ← {I} ; seen ← {I}
L10 while open is not empty do
L11     s ← remove from open a state with the least h_FF
L12     if G ⊆ s then return the path to s
L13     for each successor t of s with t ∉ seen do add t to seen ; if h_FF(t) < ∞ then add t to open
L14 return no plan
```

Line L1 is enforced hill climbing (Hoffmann and Nebel 2001, Figure 3). From the current state it runs a breadth-first search for the nearest state with a smaller $h_{FF}$, moves there, and repeats until a goal state is reached or the breadth-first search runs out of states. The search generates successors through lines L4 to L8 only.

Line L4 is one evaluation of the heuristic. It builds the relaxed planning graph from $s$ and extracts a relaxed plan backward from the goals. The length of the relaxed plan is $h_{FF}(s)$, and the facts that the relaxed plan needs one level above $s$ are $G_1$. Line L5 is Equation 5 of the paper: an action is helpful when it is applicable in $s$ and adds a fact of $G_1$. This includes every action of the first layer of the relaxed plan, and also the other applicable actions that could replace them.

Line L7 is added goal deletion (Section 6.2): if the move to $t$ has just added a goal fact, and the relaxed plan from $t$ contains an action that deletes it, the goal was probably reached too early, and $t$ is dropped. Both rules are heuristic, and both can cut every plan, so lines L9 to L14 use neither.

Lines L9 to L14 are the fallback, a [greedy best-first search](/greedy-best-first-search/) that "expands all search nodes by increasing order of goal distance estimation" (Section 5.2). It starts from scratch: the plan prefix of the first phase is thrown away. A state with $h_{FF} = \infty$ is a proved dead end, so it never enters open.

The full planner adds a goal agenda (Section 6.2.2): it splits the goals into an ordered series of subsets and runs the first phase on growing goal sets. The implementation of this page leaves it out.

## Example

**Helpful actions in the gripper domain.** A robot with two hands moves balls between rooms $A$ and $B$. Two balls start in $A$ and must go to $B$. In the state where the robot is in $A$ and holds both balls, three actions apply: move to $B$, or drop either ball in $A$. The relaxed plan is "move to $B$, drop both balls", and $G_1$ is $\{\mathit{at\_robby}(B)\}$. Only the move adds it, so the branching factor drops from 3 to 1 (Hoffmann and Nebel 2001, Section 6.1). On the whole task FF finds the optimal plan of 5 actions after 8 evaluations, and over the states it evaluated, 12 of the 25 applicable actions were helpful. With 3 and 4 balls the counts are 27 of 51 and 38 of 72, and the plans of 9 and 11 actions are optimal.

**Added goal deletion in the blocks world.** In the [blocks world](/blocks-world/) with $A$, $B$, $C$ on the table and the goal $\mathit{on}(A, B)$, $\mathit{on}(B, C)$, stacking $A$ on $B$ first looks good: $h_{FF}$ drops from 4 to 3. But the relaxed plan from there starts with $\mathit{unstack}(A, B)$, which deletes the goal just reached, so line L7 drops the state. The first phase then stacks $B$ on $C$ first, and returns the optimal plan of 4 actions. Without the rule, it returns 8 actions. The same goal order problem is the [Sussman anomaly](/sussman-anomaly/). Measured with the implementation of this page:

| task | plan with the rule | plan without the rule | greedy best-first alone | shortest plan |
|---|---|---|---|---|
| 3 blocks into one tower | 4 | 8 | 4 | 4 |
| 4 blocks into one tower | 6 | 10 | 10 | 6 |
| 5 blocks into one tower | 8 | 16 | 12 | not computed |

**The fallback.** A route of five actions leads from $r_0$ to the goal $g$. A side action leads from $r_0$ to a state $u$ that looks closer: its relaxed plan has 3 actions, against 4 at the start. But both actions that leave $u$ delete $u$, and $g$ needs both of their effects. EHC moves to $u$, finds only states with $h_{FF} = \infty$ around it, and fails. The best-first search then drops those states and finds the 5-action plan along the route. On 600 random STRIPS tasks with 4 to 8 facts, 334 had a plan. The first phase solved 322 of them, and the fallback solved the other 12.

**Pruning can cut every plan.** Hoffmann and Nebel give one example for each rule. In the first (Section 6.1.1), the initial state is $\{B\}$, the goal is $\{A, B\}$, $op_{A1}$ adds $A$ and deletes $B$, $op_{B1}$ adds $B$ and deletes $A$, and the longer routes through $P_A$ and $P_B$ are never helpful. The helpful actions only swap $A$ and $B$. In the second (Section 6.2.1), $op_A$ adds $A$, and $op_B$ needs $A$, adds $B$ and deletes $A$. Every plan must achieve $A$, delete it, and achieve it again, which line L7 forbids. Both tasks have no dead ends, the first phase fails on both, and the fallback solves both.

## Correctness

The proof is in [the correctness proof](proofs/correctness/). FF always stops. A plan from the first phase is valid, because the pruned successor function yields only real successors. The second phase is complete: a state with $h_{FF} = \infty$ has no plan, since every plan is also a relaxed plan, and all its successors have $h_{FF} = \infty$ too, so dropping such states never loses a plan. So FF returns a plan exactly when the task has one, and the pruning rules affect only the speed.

## Complexity

Let $e$ be the time of one relaxed plan extraction, which is polynomial in the task: $O(l m f)$ for $l$ layers, $m$ actions and $f$ facts, as on the [relaxed planning graph](/relaxed-planning-graph/) page. The first phase makes at most $k + 1$ breadth-first searches, each over at most $n$ states with at most $b$ successors, so it takes $O(k n b e)$ time. The second phase evaluates each reachable state at most once and keeps a heap, so it takes $O(n b (e + \log n))$ time. The space is $O(n)$ states for the seen sets and the cache of relaxed plans. These are proved upper bounds. Deciding whether a STRIPS task has a plan is [PSPACE-complete](/strips-plan-existence-pspace-complete/), so $n$ can be exponential in the size of the task, and no planner avoids that in the worst case.

The speed of FF on benchmarks is an empirical fact. Hoffmann and Nebel (2001, Section 8.1.1) report that in Logistics the breadth-first searches almost always end at depth 1 or 2, and that only 5 to 40 percent of the successors of a state were helpful, fewer in larger tasks. Hoffmann (2005) explains this: in many benchmark domains, the optimal relaxed plan length has no local minima, and a better state is always a bounded number of steps away.

## Properties

- **Complete and sound.** It returns a valid plan when one exists, and "no plan" only when none exists.
- **Not optimal.** Neither phase minimizes the plan length, and the heuristic is not admissible.
- **Deterministic.** The order of the actions and of the goals fixes the run.
- **Two phases.** The first phase is incomplete and fast, and the second is complete and slower. When the first phase fails, its work is lost.
- **Domain independent.** It needs no knowledge beyond the task, and all its guidance comes from the delete relaxation.

## Variants and improvements

- **ADL.** FF compiles ADL tasks with quantifiers and conditional effects into a normal form, and extends the relaxed planning graph to conditional effects (Hoffmann and Nebel 2001, Section 7).
- **Metric-FF.** Hoffmann (2003) extends the relaxation to numeric state variables, by ignoring decreases of numeric variables in the same way as deletes.
- **Best-first search with preferred operators.** Later planners, among them LAMA, drop enforced hill climbing and use greedy best-first search, with the helpful actions as preferred operators that are expanded first but never cut. This keeps much of the gain and stays complete.
- **Other heuristics.** The same scheme works with [h-add](/h-add-heuristic/), as in [HSP](/hsp-planner/), or with a [landmark heuristic](/landmark-heuristic/). FF's contribution was the relaxed plan, which counts shared subgoals once, together with the search and the pruning.
- **The goal agenda.** It helps in domains with goal orders, such as the blocks world, and does nothing when the goals have no order.

## When to use it

Use FF, or a planner built on its ideas, when any plan is good enough and the task is large: it is a strong baseline for satisficing STRIPS and ADL planning. It is at its best in domains with few dead ends and a well-informed relaxation, such as logistics and gripper. For optimal plans, use an admissible heuristic with A*, as in [optimal planning](/optimal-planning/). For the fewest parallel steps, use [GRAPHPLAN](/graphplan/) or [SATPLAN](/satplan/). When the hardness lies in resources that run out, the delete relaxation is weak, and the first phase fails often.

## Pitfalls

- **Treating the failure of the first phase as an answer.** Only the second phase can say "no plan".
- **Keeping the pruning in the fallback.** With helpful actions or added goal deletion, the best-first search is incomplete, as the two examples above show.
- **Reusing the plan prefix of the first phase.** The fallback must start from $I$: the prefix may end in a dead end.
- **Forgetting to cache evaluations.** The same state is evaluated many times, in several breadth-first searches and in the pruning test. A cache of relaxed plans per state saves much of the time.
- **Reading the name FF.** In bin packing, FF is the first-fit rule ([first-fit bin packing](/first-fit-bin-packing/)), not this planner.

## Implementations

## History

Hoffmann (2000) presented the heuristic and enforced hill climbing at ISMIS 2000. FF, by Hoffmann and Nebel, took part in the fully automated track of the second [International Planning Competition](/international-planning-competition/), held with AIPS 2000. It was faster than the other fully automatic planners and was named a "Group A distinguished performance planning system". It also won the Schindler Award for the first place in the Miconic 10 elevator domain, ADL track (Hoffmann and Nebel 2001, Section 8.1). The journal paper of 2001 described the full system. Metric-FF (Hoffmann 2003) took the ideas to numeric planning, and Hoffmann (2005) analysed why they work. The relaxed plan heuristic and helpful actions, as preferred operators, are still part of many satisficing planners.

## References
