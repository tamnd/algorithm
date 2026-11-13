---
tag: 3Y3JQ2
kind: algorithm
slug: backward-state-space-search
name: Backward state-space search (regression)
aliases:
- regression planning
area: games-and-search/planning
level: core
summary: Searches from the goal of a STRIPS task through relevant actions, regressing subgoals until the initial state contains one. Breadth-first order gives a plan with the fewest actions.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of actions, u: the number of subgoals reached (at most 2^n)}
  time: {worst: O(u m n), best: O(n)}
  space: {extra: O(u n)}
properties: {deterministic: true}
prereqs: [state-space-planning, goal-regression, strips, breadth-first-search]
see_also: [forward-state-space-search, hsp-planner, h-add-heuristic, mutex-relation, bidirectional-search, means-ends-analysis, graphplan, duplicate-detection]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4, Section 4.3 (the Backward-search procedure on relevant actions and regression sets, its soundness and completeness)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.2 (backward search for planning with relevant actions)
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (the HSPr planner, regression search with the additive heuristic and mutex pruning)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapters on classical planning and on heuristic search planning (general locator)
---

Backward state-space search, or regression, solves a [STRIPS](/strips/) planning task by search from the goal. A node is a subgoal: a set of facts that stands for every state that contains it. The search starts at the goal $G$. From a subgoal $g$ it takes each action that adds a fact of $g$ and deletes no fact of $g$, and it [regresses](/goal-regression/) $g$ through the action to the subgoal that must hold just before it. It stops when the initial state $I$ contains a subgoal. The actions on the path, read from that subgoal back to $G$, are a plan. It is the backward direction of [state-space planning](/state-space-planning/); the forward direction is [forward state-space search](/forward-state-space-search/). It only looks at actions that help with the goal, but many of its subgoals hold in no reachable state, and on most benchmark tasks it visits far more nodes than forward search.

## In plain words

You want a package to be at B. Ask what the last step could be: unload it at B. For that step, the truck must be at B with the package inside. Now ask the same question about this new wish list, and go on. You stop when the wish list is already true at the start.

At each step you only think about moves that make some wish come true and spoil none. You write each wish list in a notebook so you never look at the same one twice, and you take the lists in the order you wrote them. The moves you found, read from the last list back to the first, are your plan, and it has as few moves as possible. Some lists you write can never come true, for example "the truck is at A and at B".

## The problem

The input is a ground STRIPS task $(F, A, I, G)$: a finite set $F$ of facts, a finite set $A$ of actions, an initial state $I \subseteq F$ and a goal $G \subseteq F$. Each action $a$ has a precondition $\mathit{pre}(a)$, an add list $\mathit{add}(a)$ and a delete list $\mathit{del}(a)$, subsets of $F$ with $\mathit{add}(a) \cap \mathit{del}(a) = \emptyset$. The action $a$ is applicable in a state $s$ when $\mathit{pre}(a) \subseteq s$, and then the next state is $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. A plan is a sequence of actions that is applicable from $I$ and ends in a state that contains $G$. The output is a plan, or *failure* when no plan exists. With breadth-first order the plan has the fewest actions. Write $n = |F|$, $m = |A|$, and $u$ for the number of subgoals the search reaches, so $u \le 2^n$.

An action $a$ is *relevant* for a subgoal $g$ when $\mathit{add}(a) \cap g \ne \emptyset$ and $\mathit{del}(a) \cap g = \emptyset$. The *regression* of $g$ through $a$ is
$$ \mathit{regress}(g, a) = (g \setminus \mathit{add}(a)) \cup \mathit{pre}(a). $$
The key fact is that for $\mathit{del}(a) \cap g = \emptyset$ and every state $s$, $s \supseteq \mathit{regress}(g, a)$ holds exactly when $a$ is applicable in $s$ and $s[a] \supseteq g$.

## The algorithm

```pseudo id=main
BACKWARD-SEARCH(A, I, G)
L1  parent ← { G ↦ nil }
L2  Q ← a FIFO queue that holds G
L3  while Q is not empty do
L4      g ← Q.remove-first()
L5      if g ⊆ I then return PLAN(parent, g)
L6      for each a in A do
L7          if add(a) ∩ g ≠ ∅ and del(a) ∩ g = ∅ then
L8              h ← (g \ add(a)) ∪ pre(a)
L9              if h is not a key of parent then
L10                 parent[h] ← (g, a)
L11                 Q.add-last(h)
L12 return failure

PLAN(parent, g)
L13 π ← the empty sequence
L14 while parent[g] ≠ nil do
L15     (g, a) ← parent[g]
L16     put a at the back of π
L17 return π
```

The table `parent` is a [hash table](/hash-table/) keyed by subgoals. For each subgoal $h$ it holds the subgoal $g$ and the action $a$ that produced it first, so $a$ is the action to execute in a state that contains $h$, and $g$ is what then holds. PLAN starts at the subgoal that $I$ contains and walks toward $G$, so the actions come out in execution order and need no reversal, unlike forward search. Line L9 is the [duplicate detection](/duplicate-detection/). Line L7 is the relevance test: an action that adds no fact of $g$ is not needed as the last step, and an action that deletes a fact of $g$ cannot be the last step.

The goal test of line L5 is containment, not equality: a subgoal is a partial state, and the search stops as soon as $I$ is one of the states it stands for. With a stack in place of the FIFO queue, the same code searches in depth-first order and still returns a valid plan.

## Example

The delivery task of [forward search](/forward-state-space-search/) has one truck, one package and two places, with the facts $t_A$, $t_B$ (the truck is at $A$ or $B$) and $p_A$, $p_B$, $p_T$ (the package is at $A$, at $B$ or in the truck), and the actions drive(A,B), drive(B,A), load(A), load(B), unload(A), unload(B), tried in this order. The initial state is $I = \{t_A, p_A\}$ and the goal is $G = \{p_B\}$. Breadth-first regression runs as follows.

| step | subgoal removed (L4) | relevant actions and regressed subgoals | new keys |
| --- | --- | --- | --- |
| 1 | $\{p_B\}$ | unload(B) gives $\{t_B, p_T\}$ | 1 |
| 2 | $\{t_B, p_T\}$ | drive(A,B) gives $\{t_A, p_T\}$; load(A) gives $\{t_A, t_B, p_A\}$; load(B) gives $\{t_B, p_B\}$ | 3 |
| 3 | $\{t_A, p_T\}$ | drive(B,A) gives $\{t_B, p_T\}$, seen; load(A) gives $\{t_A, p_A\}$; load(B) gives $\{t_A, t_B, p_B\}$ | 2 |
| 4 | $\{t_A, t_B, p_A\}$ | unload(A) gives $\{t_A, t_B, p_T\}$ | 1 |
| 5 | $\{t_B, p_B\}$ | drive(A,B) gives $\{t_A, p_B\}$; unload(B) gives $\{t_B, p_T\}$, seen | 1 |
| 6 | $\{t_A, p_A\}$ | $\{t_A, p_A\} \subseteq I$: stop | |

At step 1, load(B) is not relevant because it deletes $p_B$, and drive(A,B) is not relevant because it adds nothing of the goal. The search expands 5 subgoals, generates 10 and reaches 9. PLAN follows `parent` from $\{t_A, p_A\}$: load(A) leads to $\{t_A, p_T\}$, drive(A,B) to $\{t_B, p_T\}$ and unload(B) to $G$. The plan load(A), drive(A,B), unload(B) has 3 actions, the fewest possible.

Three of the subgoals, $\{t_A, t_B, p_A\}$, $\{t_A, t_B, p_B\}$ and $\{t_A, t_B, p_T\}$, put the truck at two places. No reachable state contains them, but regression cannot see this, and step 4 expands one of them. A planner can prune them with the [mutex](/mutex-relation/) pair $\{t_A, t_B\}$, as HSPr does.

### Larger tasks

The table compares the implementation on this page with breadth-first [forward search](/forward-state-space-search/) on the same tasks. The [blocks world](/blocks-world/) has the operators pickup, putdown, stack and unstack. The [Sussman](/sussman-anomaly/) task starts from C on A with B on the table. The full goal is the complete state of the tower A on B on C with an empty hand, and the short goal is only on(A,B) and on(B,C). In the [Tower of Hanoi](/tower-of-hanoi/) the goal is the tower on the third peg.

| task | plan | backward: expanded, generated, reached | forward: expanded, generated, reached |
| --- | --- | --- | --- |
| delivery | 3 | 5, 10, 9 | 4, 7, 5 |
| Sussman, 4-fact goal (A on B, B on C, C on the table, A clear) | 6 | 2540, 11127, 4775 | 21, 41, 22 |
| Sussman, 2-fact goal | 6 | 1059, 4909, 2315 | 21, 41, 22 |
| Hanoi, 1 disk | 1 | 1, 2, 3 | 2, 4, 3 |
| Hanoi, 2 disks | 3 | 88, 492, 212 | 5, 14, 9 |
| Hanoi, 3 disks | 7 | 19796, 155554, 24583 | 25, 73, 27 |

The 3-block world has only 22 reachable states, but from the 4-fact goal regression can reach 17,253 different subgoals, and only 23 of them are contained in some reachable state. The others combine facts that never hold together, such as holding(A) and holding(B). On 3-disk Hanoi regression reaches about 900 times as many nodes as there are reachable states. This is the main reason why modern planners search forward, and why the regression planners that work well prune subgoals with mutexes or state invariants.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). They rest on the exactness of regression: for an action that deletes no fact of $g$, a state contains $\mathit{regress}(g, a)$ exactly when $a$ applies in it and leads to a state that contains $g$. By induction along `parent`, the actions that PLAN returns for a subgoal $h$ take every state that contains $h$ to a state that contains $G$; so a returned sequence is a plan (soundness). The keys are distinct subsets of $F$, so the loop stops after at most $2^n$ passes. For completeness and optimality, take any plan and walk it backward from $G$, keeping a subgoal that the current state contains: an action that adds no fact of the subgoal can be skipped, and every other action is relevant. This gives a path of relevant regressions from $G$ to a subgoal of $I$ that is no longer than the plan. So the regression graph has such a path exactly when a plan exists, its shortest one has the length of a shortest plan, and breadth-first search finds it.

## Complexity

**Time.** At most $u$ subgoals are expanded. Expanding one tests $m$ actions for relevance and regresses the relevant ones, each in $O(n)$ time with sets held as bit vectors or sorted lists, and each hash lookup costs $O(n)$. The time is $O(u m n)$, and $O(2^n m n)$ since $u \le 2^n$. The best case is $G \subseteq I$, one test in $O(n)$ time.

**Space.** The table holds up to $u$ subgoals of $O(n)$ bits, so the space is $O(u n)$.

**Comparison with forward search.** Forward search is bounded by the number $r$ of reachable states, regression by the number $u$ of subgoals reachable from $G$. Neither bound dominates. Regression wins when the goal is small and few actions are relevant to it while many actions apply in each state; forward search wins when most subgoals combine facts that never hold together, which is the usual case in benchmark domains, as the table above shows.

## Properties

- **Sound.** Every returned sequence is a plan, in every order of the queue.
- **Complete on finite tasks.** Duplicate detection makes it stop, with a plan when one exists and failure when none does.
- **Step optimal in breadth-first order.** Dropping irrelevant actions never makes a plan longer, so the restriction to relevant actions keeps the shortest plans.
- **Visits subgoals, not states.** A node can stand for many states, so the space of subgoals can be smaller than the state space, but it can also be much larger, because it includes sets of facts that hold in no reachable state.
- **Goal directed.** Only actions that add a fact of the current subgoal are tried, which helps on tasks with many actions that are irrelevant to the goal.
- **Deterministic.** The result depends on the order of the actions only through ties.

## Variants and improvements

- **Heuristic regression (HSPr).** Bonet and Geffner's HSPr computes the additive costs of [h-add](/h-add-heuristic/) once, forward from $I$, and then evaluates each subgoal by a sum over its facts, with no new computation per node. This is the main gain of regression for heuristic search: the heuristic for forward search must be recomputed for every state. HSPr uses weighted A* and prunes subgoals that contain a mutex pair.
- **Mutex and invariant pruning.** Remove every subgoal that contains a pair of [mutex](/mutex-relation/) facts, or that breaks a state invariant such as "the truck is at one place". This removes all three bad subgoals of the delivery example.
- **Subsumption.** If a reached subgoal $g$ is a subset of a new subgoal $h$, every state that contains $h$ also contains $g$, so $h$ can be pruned when only plan existence matters.
- **Lifted regression.** Regress over action schemas with variables, binding only the variables that the subgoal needs, as in the original STRIPS system and in partial-order planners. This avoids [grounding](/grounding/) but needs unification.
- **Regression in the planning graph.** [Graphplan](/graphplan/) extracts plans by a backward search over the levels of the [planning graph](/planning-graph/), which prunes subgoals with mutexes.
- **Bidirectional search.** [Bidirectional search](/bidirectional-search/) runs progression and regression together and stops when a state contains a subgoal.

## When to use it

Use regression when the goal mentions few facts and most actions are irrelevant to it, when the same goal must be planned from many initial states, since the subgoals do not depend on $I$, or when a heuristic must be cheap per node, as in HSPr. Do not use plain regression on domains with strong state invariants, such as the blocks world, unless the subgoals are pruned with mutexes: the table above shows thousands of subgoals where forward search needs a few dozen states. For a reference planner on small tasks, breadth-first forward search is simpler and usually faster.

## Pitfalls

- **Forgetting the delete test.** An action that deletes a fact of $g$ cannot be the last step toward $g$. Without the test in line L7, regression produces subgoals whose plans fail; in the delivery task, load(B) would regress $\{p_B\}$ to $\{t_B, p_B\}$ and the plan would end by removing the package from $B$.
- **Testing equality with the initial state.** The test is $g \subseteq I$, since a subgoal is a partial description.
- **Reversing the plan.** PLAN walks from the subgoal of $I$ toward $G$, so the actions are already in execution order. Reversing them, as forward search does, gives a wrong plan.
- **Trusting the subgoals.** A subgoal can hold in no reachable state, for example $\{\mathrm{holding}(A), \mathrm{holding}(B), \mathrm{clear}(C)\}$ in the 3-block world. A heuristic or a test that treats every subgoal as a real situation can be wrong.
- **Actions that add and delete the same fact.** The rule $\mathit{regress}(g, a) = (g \setminus \mathit{add}(a)) \cup \mathit{pre}(a)$ and the relevance test assume disjoint add and delete lists; with the rule $(s \setminus \mathit{del}) \cup \mathit{add}$ such a fact holds after the action, and it must be removed from the delete list first.

## Implementations

## History

The STRIPS system of Fikes and Nilsson (1971) worked backward from the goal, in the style of [means-ends analysis](/means-ends-analysis/), and Waldinger (1977) made regression of goals through actions precise in his work on [goal regression](/goal-regression/). For a long time backward search was preferred to forward search because it is goal directed. Ghallab, Nau and Traverso (2004) present it as the second basic state-space planner, with relevant actions and regression sets, and prove it sound and complete. In heuristic search planning Bonet and Geffner built HSPr (1999), a regression planner that computes its heuristic only once, and Haslum and Geffner (2000) used regression to compute the admissible $h^m$ heuristics. The large number of subgoals that hold in no reachable state, which mutexes only partly remove, is the main reason why forward search took over in later planners.

## References
