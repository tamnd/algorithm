---
tag: NW29JR
kind: algorithm
slug: htn-decomposition
name: HTN decomposition planner
aliases:
- SHOP
- SHOP2
area: games-and-search/planning
level: advanced
summary: Plans by replacing compound tasks with the subtasks of their methods, in the order the plan will run, so it always knows the current state. Backtracks over task and method choices.
solves: [htn-planning]
model: word-ram
complexity:
  vars: {N: "the number of task nodes created on one search branch, at most t (d + 1) k^d for t initial tasks, k subtasks per method and depth bound d", m: the largest number of methods for one task, f: the number of facts}
  time: {worst: O((N^2 + f) (N m)^N)}
  space: {extra: O(N^3 + N f)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1999
  people: [Dana Nau, Yue Cao, Amnon Lotem, Héctor Muñoz-Avila]
  note: SHOP (1999) introduced ordered task decomposition for totally ordered methods; SHOP2 (2001, described in JAIR 2003) allowed partially ordered methods and interleaves their subtasks.
prereqs: [htn-planning, task-network]
see_also: [hierarchical-task-network, forward-state-space-search, chronological-backtracking, depth-first-search, pop-partial-order-planning, state-space-planning, macro-operators, pddl]
sources:
  - paper: doi:10.1613/jair.1141
    title: "Dana Nau, Tsz-Chiu Au, Okhtay Ilghami, Ugur Kuter, J. William Murdock, Dan Wu and Fusun Yaman, SHOP2: an HTN planning system, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 379 to 404 (the SHOP2 procedure, partially ordered methods, if-then-else methods and the 2002 planning competition)
  - paper: "Dana Nau, Yue Cao, Amnon Lotem and Héctor Muñoz-Avila, SHOP: Simple Hierarchical Ordered Planner, Proceedings of IJCAI-99, Morgan Kaufmann"
    locator: the paper starting on p. 968 (ordered task decomposition; general locator, the end page differs between sources)
  - paper: "Kutluhan Erol, James Hendler and Dana Nau, UMCP: a sound and complete procedure for hierarchical task-network planning, Proceedings of AIPS-94, AAAI Press"
    locator: pp. 249 to 254 (the first provably sound and complete HTN procedure)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 11 (the TFD and PFD procedures for total-order and partial-order forward decomposition, with soundness and completeness)
---

An HTN decomposition planner solves an [HTN planning](/htn-planning/) task by forward search. It keeps a current state and a [task network](/task-network/) of tasks still to do. At each step it picks a task that nothing has to precede. A primitive task is an action: the planner applies it if its precondition holds, and moves on to the next state. A compound task is replaced by the subtasks of one of its methods, if the method's precondition holds now. When the network is empty, the actions applied so far are the plan. This is ordered task decomposition, the method of SHOP and SHOP2. Because tasks are handled in the order they will run, the planner always knows the full current state.

## In plain words

You have a to-do list. Some items are simple actions, like "walk to the stop". Others are big jobs, like "travel to the park", and the domain tells you a few recipes for each big job.

Work from the front of the list. If the front item is an action and you can do it now, do it and look at the world again. If it is a big job, pick a recipe that makes sense in the world as it is now, and write its smaller items in place of the big job.

If you get stuck, go back to your last choice and try another recipe. When the list is empty, the actions you did are the plan.

Some items need not come in a fixed order. Then you may take any item that nothing must come before.

## The problem

The input is an HTN domain over a set $F$ of ground facts, an initial state $s_0 \subseteq F$, an initial task network $w_0$ and a depth bound $d$. Each primitive task names a [STRIPS](/strips/) operator $o$ with $\mathit{pre}(o)$, $\mathit{add}(o)$ and $\mathit{del}(o)$. Each method $\mu$ for a compound task has a precondition $\mathit{pre}(\mu) \subseteq F$ and a task network of subtasks with ordering constraints among them. A task network $w$ is a finite set of nodes, each labelled by a task and a depth, with a strict partial order $\prec$ on the nodes. The nodes of $w_0$ have depth 0.

Decomposing node $u$ by method $\mu$ removes $u$ and adds a fresh node for each subtask of $\mu$, with depth one more than $u$. Each new node inherits every ordering of $u$: if $v \prec u$ then $v$ precedes each new node, and if $u \prec v$ each new node precedes $v$. The orderings of $\mu$ hold among the new nodes. The bound $d$ forbids decomposing a node of depth $d$ or more.

The output is a sequence of operators that the search below can reach, or failure. The [correctness proof](proofs/correctness.md) shows that these sequences are exactly the solutions under a declarative reading: expand every compound node, put a marker for each method precondition before its subtasks, and run a linearization in which every operator applies and every marker holds.

## The algorithm

```pseudo id=main
HTN-PLAN(s, w, D, d)                ▷ state s, task network w, domain D, bound d
L1  if w has no node then return the empty plan
L2  for each node u of w with no predecessor in w do      ▷ choice point
L3      if task(u) is primitive, with operator o, then
L4          if pre(o) ⊆ s then
L5              π ← HTN-PLAN((s \ del(o)) ∪ add(o), w without u, D, d)
L6              if π ≠ failure then return o · π
L7      else if depth(u) < d then
L8          for each method μ for task(u) with pre(μ) ⊆ s do    ▷ choice point
L9              π ← HTN-PLAN(s, w with u decomposed by μ, D, d)
L10             if π ≠ failure then return π
L11 return failure
```

Line L2 is where partial order enters. In SHOP all networks are totally ordered, so exactly one node has no predecessor and L2 makes no choice. In SHOP2 the subtasks of a method may be unordered, and L2 lets the planner interleave subtasks of different methods. Line L5 removes $u$ but keeps its orderings by transitivity: every predecessor of $u$ still precedes every successor. Line L8 tests the method precondition in the current state, the state that the actions before this point have produced. This is the main gain of forward decomposition. A precondition may depend on any fact of the current state, and the planner may also compute with that state, as SHOP does for numbers and external calls.

The depth bound makes the search finite. Real HTN domains are often recursive, for example "move all the crates" decomposes into "move one crate" and "move all the crates" again, so SHOP and SHOP2 run without a bound and rely on the domain author to write methods that stop.

## Example

Take a trip from home to the park. The facts are at-home, at-stop, at-park, park-is-near, have-coin, have-cash, have-ticket, taxi-at-home and owe-driver. The initial state is $\{$at-home, have-cash$\}$. The compound task travel has three methods, tried in this order:

- by-foot, with precondition park-is-near and subtask walk;
- by-bus, with no precondition and subtasks go-to-stop, buy-ticket, ride-bus;
- by-taxi, with precondition have-cash and subtasks call-taxi, ride-taxi, pay-driver.

Buying a ticket needs have-coin, riding the taxi needs at-home and taxi-at-home, and paying needs owe-driver and have-cash. The search with $d = 1$ makes 7 calls:

| call | state | network | choice |
|---|---|---|---|
| 1 | at-home, have-cash | travel | by-foot fails its precondition; try by-bus |
| 2 | at-home, have-cash | go-to-stop, buy-ticket, ride-bus | apply go-to-stop |
| 3 | at-stop, have-cash | buy-ticket, ride-bus | buy-ticket needs have-coin: failure |
| 4 | at-home, have-cash | call-taxi, ride-taxi, pay-driver | calls 2 and 3 failed, so call 1 tried by-taxi; apply call-taxi |
| 5 | at-home, have-cash, taxi-at-home | ride-taxi, pay-driver | apply ride-taxi |
| 6 | have-cash, at-park, owe-driver | pay-driver | apply pay-driver |
| 7 | at-park | empty | return the empty plan |

The plan is call-taxi, ride-taxi, pay-driver. The bus method passed its own precondition, so it was tried. It failed two levels down, and the planner backtracked to the last choice, the method in call 1. With park-is-near in the initial state the first method works and the plan is walk.

A second example shows the current-state test. A method for task $T$ needs fact $g$ and has the subtask $p$. Operator $o$ adds $g$. If the network is $o \prec T$, the plan is $o, p$. If it is $T \prec o$, there is no plan, because $T$ must be decomposed before $o$ runs. If $T$ and $o$ are unordered, the planner first takes $T$, finds that the method does not apply, then takes $o$, and then $T$ applies: the plan is again $o, p$.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). Fix a domain, a bound $d$ and an initial pair $(s_0, w_0)$.

- **Termination.** Each call removes one node from the network, either a primitive one at L5 or a compound one at L9, and no node is removed twice. A branch therefore has at most $N$ calls, where $N$ counts the nodes created on it, and each call has finitely many children.
- **Soundness.** Every returned plan applies from $s_0$: each operator is applied at L4 only when its precondition holds. It also comes from a full decomposition of $w_0$: the decompositions made on the path, with a marker at each, form a primitive network, and the order of the calls is a linearization of it in which every marker holds.
- **Completeness.** Conversely, take a full decomposition of $w_0$ within the bound and a linearization in which every operator applies and every marker holds. Its first element has no predecessor, so it is a primitive node of the current network or the marker of a node of it, and L2 can choose that node. Then L4 or L8 accepts it, and the rest is a solution of the smaller pair. By induction the search can follow the whole linearization.

So the set of plans the search can reach is the set of solutions, and the first plan in backtracking order exists exactly when a solution exists.

## Complexity

Let $t$ be the number of tasks in $w_0$ and $k$ the largest number of subtasks of a method. A branch has at most $t k^i$ nodes of depth $i$, so it creates at most $N \le t (d + 1) k^d$ nodes, and it has at most $N$ calls. A call chooses a node at L2 and possibly a method at L8, so it has at most $N m$ children. The search tree has $O((N m)^N)$ calls. Each call does $O(N^2)$ work on the order relation and $O(f)$ work on the state.

- **Time.** $O((N^2 + f) (N m)^N)$ in the worst case. In SHOP's total-order setting the factor $N m$ drops to $m$, since L2 has one choice.
- **Space.** $O(N^3 + N f)$: a recursion stack of depth $N$, each frame holding a network with $O(N^2)$ order pairs and a state.

This is not a weakness of this algorithm only. HTN plan existence with partially ordered networks and recursion is undecidable, and even the ground totally ordered case is EXPTIME-complete; see [HTN planning](/htn-planning/). In practice the methods carry the domain knowledge, and with good methods SHOP-style planners rarely backtrack.

## Properties

- **Sound and complete for the bound.** Every plan it returns is a solution, and it finds one if a solution with decomposition depth at most $d$ exists.
- **Not systematic.** With unordered tasks, the same plan can be reached through different choices at L2, so the same partial result can be explored more than once.
- **Total state knowledge.** Every method precondition and every operator precondition is tested in a fully known state, so preconditions can be arbitrary programs over the state.
- **Not optimal.** The first plan found depends on the order of the methods, not on its length or cost.

## Variants and improvements

- **SHOP.** Total order only. L2 always takes the first task of a list.
- **SHOP2.** Partial order, so L2 may take any task without a predecessor. A task marked as immediate is taken first. A method may list several precondition and subtask pairs, and only the first pair whose precondition holds is used, like an if-then-else. SHOP2 also has axioms, numeric fluents and calls to external code, and is lifted: preconditions are evaluated to bindings of the method's variables.
- **TFD and PFD.** Ghallab, Nau and Traverso give total-order and partial-order forward decomposition as clean textbook procedures, the same search as this page without SHOP2's extensions.
- **Plan-space HTN planning.** UMCP, NOAH, NONLIN, SIPE and O-Plan decompose tasks but keep a partial order of actions and repair it with [causal links](/causal-link/) and threat resolution as in [POP](/pop-partial-order-planning/). They do not know the state at each step, and they pay for it with constraint reasoning.
- **Heuristic and compiled HTN planners.** Progression search with heuristics, compilation to SAT, and grounding with reachability analysis are used by recent HTN planners, which compete in the hierarchical track of the International Planning Competition.

## When to use it

Use it when the domain comes with procedural knowledge: standard ways to do each job, written as methods. Logistics, military operations, manufacturing and game agents are typical. Methods cut the search to the plans the author considers sensible, and forward decomposition lets their preconditions use the full state. If no methods are known, use a classical planner such as [forward state-space search](/forward-state-space-search/); an HTN planner without good methods is just a slow form of it.

## Pitfalls

- **Left recursion.** A method whose first subtask is the task itself makes an unbounded search. SHOP-style planners have no bound by default, so write recursive methods with the recursive call last and a base case that applies first.
- **Method order is search control.** The first applicable method is tried first. Putting an expensive or rarely useful method first slows the search but does not change the set of plans.
- **Preconditions tested too early.** In a partially ordered network the precondition of a method is tested when it is decomposed, not right before its first subtask runs. Another unordered task may run in between and break it. Order the tasks if this matters.
- **Incompleteness from the domain.** The planner finds only plans that the methods describe. A goal reachable by actions but not by the methods has no solution in the HTN sense.

## Implementations

## History

Task decomposition began with Sacerdoti's NOAH (1975) and Tate's NONLIN (1977), followed by SIPE (Wilkins, 1988) and O-Plan (Currie and Tate, 1991). These systems decomposed tasks inside a partial-order plan. Erol, Hendler and Nau gave HTN planning a formal semantics and the sound and complete procedure UMCP in 1994. Nau, Cao, Lotem and Muñoz-Avila introduced SHOP in 1999. It decomposed tasks in the order they would be executed, so the state was always known, and on their test domains it was much faster than the planners of the time. SHOP2 (2001) allowed partially ordered methods. It received one of the awards for distinguished performance at the 2002 International Planning Competition and was described in JAIR in 2003.

## References
