---
tag: K47MCJ
kind: technique
slug: state-space-planning
name: State-space planning
aliases:
- state-based planning
area: games-and-search/planning
level: intro
summary: Planning by search in the graph whose nodes are world states (progression from the initial state) or goal descriptions (regression from the goal).
prereqs: [strips, classical-planning, state-space-search]
see_also: [forward-state-space-search, backward-state-space-search, goal-regression, plan-space-planning, delete-relaxation, hsp-planner, bidirectional-search, planning-as-model-checking]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4 (state-space planning; Section 4.2 forward search, Section 4.3 backward search, Section 4.4 the STRIPS algorithm)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.2 (forward state-space search and backward search for planning) and Section 11.3 (heuristics for planning)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapters on classical planning and on heuristic search planning (general locator)
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (forward search in HSP and HSP2, regression search in HSPr, and why the two directions are not symmetric)
---

State-space planning solves a [classical planning](/classical-planning/) task by search in a graph whose nodes stand for sets of world states. In progression, or [forward search](/forward-state-space-search/), a node is one state, the search starts at the initial state, and an edge applies an action. In regression, or [backward search](/backward-state-space-search/), a node is a goal description, a set of facts that stands for all states that contain it, the search starts at the goal, and an edge is one step of [goal regression](/goal-regression/). The rest of the method is a choice of a search strategy, a heuristic and a rule for duplicates. The general search problem is on [state-space search](/state-space-search/); this page is about how a [STRIPS](/strips/) task becomes such a problem in the two directions. It differs from [plan-space planning](/plan-space-planning/), whose nodes are partial plans and not states.

## In plain words

You want to plan a trip. One way is to start where you are and ask: what can I do now, and where does it take me? You keep trying moves until you are at the destination. That is forward planning.

The other way starts at the end. You ask: what must be true just before I arrive? Perhaps "I am on the train to the city". Then: what must be true before that? You keep going back until the condition is already true where you are now. That is backward planning.

Both ways explore a map of situations, and both need a rule for which situation to look at next. Forward planning only sees situations that can really happen. Backward planning only looks at moves that help with the goal, but some of the situations it imagines can never happen.

## When it applies

- The task is a ground STRIPS task, or a task that [grounding](/grounding/) makes into one: a finite set $F$ of facts, a finite set $A$ of actions with preconditions, add lists and delete lists, an initial state $I \subseteq F$ and a goal $G \subseteq F$.
- The world is deterministic, fully observable and static, and the plan is a sequence of actions. With nondeterministic actions or partial observability the nodes become belief states; see [belief space](/belief-space/).
- The task is small enough to search, or a good heuristic exists. The state graph has up to $2^{|F|}$ nodes, so blind search works only on small tasks, and large tasks need a heuristic such as those of the [delete relaxation](/delete-relaxation/).

## The template

```pseudo id=main
STATE-SPACE-PLAN(F, A, I, G, direction, frontier, h)
L1  if direction = forward then start ← I; done(n) ≡ G ⊆ n
L2  else start ← G; done(n) ≡ n ⊆ I                  ▷ backward
L3  parent ← { start ↦ nil }; frontier.insert(start, h(start))
L4  while frontier is not empty do
L5      n ← frontier.remove()                         ▷ hole: the strategy
L6      if done(n) then return the actions on the path to n, in execution order
L7      for each a in A do
L8          if direction = forward and pre(a) ⊆ n then m ← (n \ del(a)) ∪ add(a)
L9          else if direction = backward and add(a) ∩ n ≠ ∅ and del(a) ∩ n = ∅ then
L10             m ← (n \ add(a)) ∪ pre(a)
L11         else continue
L12         if m not in parent then                   ▷ hole: duplicate detection
L13             parent[m] ← (n, a); frontier.insert(m, h(m))
L14 return failure
```

**The holes.** Line L5 decides the strategy: a FIFO queue gives [breadth-first search](/breadth-first-search/), a stack gives [depth-first search](/depth-first-search/), a priority queue on path cost gives [uniform-cost search](/uniform-cost-search/), on $g + h$ gives [A*](/a-star-search/), on $g + W h$ gives [weighted A*](/weighted-a-star/) and on $h$ alone gives [greedy best-first search](/greedy-best-first-search/). Line L12 is [duplicate detection](/duplicate-detection/); a search with a cost ordering must also reopen a node that is reached again by a cheaper path. In the backward direction the heuristic estimates the cost from $I$ to a state that contains $n$, not from $n$ to the goal. In the forward direction it estimates the cost from $n$ to the goal.

**Why the template is sound.** In the forward direction, every node is a state reached from $I$ by the actions on its path, so the path is a plan when $G \subseteq n$. In the backward direction, every node $n$ has the property that from any state $s \supseteq n$ the actions on its path, in reverse order of regression, are applicable and reach a state that contains $G$. This is the exactness of regression, proved on [goal regression](/goal-regression/). So the path is a plan when $n \subseteq I$. Both directions are complete with duplicate detection, because each has at most $2^{|F|}$ distinct nodes, and a node enters the frontier at most once. The proofs are on the pages of the two algorithms.

**Cost.** Each direction has at most $2^{|F|}$ distinct nodes. A node costs $O(|A| \cdot |F|)$ set operations to expand and $O(|F|)$ to hash, so blind search takes $O(2^{|F|} |A| |F|)$ time and $O(2^{|F|} |F|)$ space in the worst case. The bound is tight up to the factors $|A|$ and $|F|$: the binary counter on the [STRIPS](/strips/) page and the [Tower of Hanoi](/tower-of-hanoi/) need exponentially long plans. Deciding whether a plan exists is PSPACE-complete ([plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/)), so no method can avoid the exponential worst case unless P = PSPACE.

## Classic examples

### A delivery task in both directions

One truck and one package. The facts are $t_A$, $t_B$ (the truck is at $A$ or $B$) and $p_A$, $p_B$, $p_T$ (the package is at $A$, at $B$ or in the truck). The actions are drive from $A$ to $B$ and back, load at $A$ or $B$, and unload at $A$ or $B$; load at $x$ needs $t_x$ and $p_x$, adds $p_T$ and deletes $p_x$. The initial state is $\{t_A, p_A\}$ and the goal is $\{p_B\}$. Breadth-first search with duplicate detection, actions tried in the order drive(A,B), drive(B,A), load(A), load(B), unload(A), unload(B), gives these counts.

| | forward | backward |
| --- | --- | --- |
| nodes expanded | 4 | 5 |
| nodes generated | 7 | 10 |
| distinct nodes the direction can reach | 6 states | 10 goal descriptions |
| nodes that no reachable state contains | 0 | 3 |
| plan | load(A), drive(A,B), unload(B) | the same |

The 3 bad goal descriptions in the backward search are $\{t_A, t_B, p_A\}$, $\{t_A, t_B, p_B\}$ and $\{t_A, t_B, p_T\}$: the truck at two places at once. For example, regressing $\{t_B, p_T\}$ through load(A) keeps $t_B$ and adds the precondition $\{t_A, p_A\}$. Regression does not know that $t_A$ and $t_B$ exclude each other.

### The Sussman anomaly

In the [blocks world](/blocks-world/) with 3 blocks and the 18 actions pickup, putdown, stack and unstack, start from C on A, with A and B on the table, and take the goal on(A, B), on(B, C), ontable(C), clear(A). Forward breadth-first search reaches all 22 states of the task, expands 21 of them, generates 41 nodes and returns a plan of 6 actions. Backward breadth-first search returns a plan of 6 actions too, but it expands 2540 goal descriptions and generates 11127. From this goal, regression can produce 17,253 distinct goal descriptions, and only 23 of them are contained in some reachable state. The rest describe things such as holding two blocks at once, and the search wastes its time on them.

### The Tower of Hanoi

The [Tower of Hanoi](/tower-of-hanoi/) with $n$ disks has $3^n$ reachable states, and its shortest plan has $2^n - 1$ moves. With facts on(d, x) and clear(x), forward breadth-first search for $n = 6$ reaches all $729$ states, expands 675 and returns a plan of 63 moves. Backward breadth-first search expands 1 goal description for $n = 1$, 88 for $n = 2$ and 19,796 for $n = 3$, against 25 states for forward search with $n = 3$.

The counts come from the Python implementations on the pages of [forward search](/forward-state-space-search/) and [backward search](/backward-state-space-search/), with the goal tested when a node is removed from the queue.

## Variations

- **Heuristic forward search.** The most common form of the template in practice. [HSP](/hsp-planner/) uses the additive heuristic [h-add](/h-add-heuristic/) with hill climbing or weighted A*, and [FF](/fast-forward-planner/) uses the [relaxed plan heuristic](/relaxed-plan-heuristic/) with [enforced hill climbing](/enforced-hill-climbing/). A heuristic must be computed again in each state.
- **Heuristic regression.** HSPr (Bonet and Geffner 2001) searches backward and computes the costs of single facts from $I$ once, before the search, so each goal description is evaluated by a sum of table entries. It prunes goal descriptions that contain a pair of facts known to be mutually exclusive; see [mutex relation](/mutex-relation/).
- **Bidirectional search.** [Bidirectional search](/bidirectional-search/) runs both directions and stops when a state of the forward search contains a goal description of the backward search.
- **Symbolic search.** The frontier is a set of states held as a [binary decision diagram](/binary-decision-diagram/), and one step applies all actions at once; see [planning as model checking](/planning-as-model-checking/).
- **Lifted search.** Regression over action schemas with variables, which avoids grounding; the goal descriptions then hold variables that unify later.
- **Goal-directed decomposition.** [Means-ends analysis](/means-ends-analysis/) mixes the two directions: it picks a goal fact that does not hold, chooses an action that adds it, and plans recursively for the action's preconditions.

## Pitfalls

- **Treating a goal description as a state.** A node of the backward search stands for every state that contains it, and it can hold facts that no reachable state has together. A test such as "is this node reachable" makes no sense without the initial state.
- **No duplicate detection.** Without it, both directions loop on any task with reversible actions, such as drive from $A$ to $B$ and back.
- **Weak duplicate detection in regression.** Two goal descriptions $g \subseteq g'$ are different nodes, but $g'$ is never easier than $g$. A search that does not prune by subsets wastes time on such pairs; full subset pruning costs more per node.
- **Assuming regression is cheaper because it is goal-directed.** It uses only relevant actions, which is often a smaller branching factor, but it can explore many unreachable goal descriptions, as in the Sussman example above.
- **Mixing up the two optimal criteria.** Breadth-first search gives the fewest actions, which is the cheapest plan only with unit costs. With general costs use uniform-cost search or A* with an admissible heuristic; see [optimal planning](/optimal-planning/).
- **Negative preconditions.** The template assumes positive preconditions and goals, as in STRIPS. With negative literals, a goal description must hold both kinds of literals, and regression must check that an action does not make a negative goal literal false.

## Exercises

1. In the delivery task, list the 10 goal descriptions that regression can reach from $\{p_B\}$, and mark the 3 that no reachable state contains.
2. Show that forward search with duplicate detection on a task with $|F|$ facts expands at most $2^{|F|}$ nodes, and give a task that needs about that many before it can prove that no plan exists.
3. Give a task in which backward search expands fewer nodes than forward search. (Hint: many actions that are applicable in $I$ and have nothing to do with the goal.)
4. A goal description that contains both facts of a mutex pair can be pruned. Prove that the pruning keeps the search complete.
5. In the Sussman task, why does forward breadth-first search reach all 22 states before it stops, while the plan has only 6 actions?

## References
