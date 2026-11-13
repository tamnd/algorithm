---
tag: WC1PNH
kind: technique
slug: causal-graph-heuristic
name: Causal graph heuristic
aliases:
- causal graph
area: games-and-search/planning
level: research
summary: Heuristic computed from the causal graph of state variables in a finite-domain representation.
prereqs: [sas-plus, dijkstra, heuristic-function]
see_also: [h-add-heuristic, relaxed-plan-heuristic, landmark-heuristic, fast-forward-planner, strongly-connected-components, feedback-arc-set-problem, greedy-best-first-search, pattern-database]
sources:
  - paper: "Malte Helmert, A planning heuristic based on causal graph analysis, Proceedings of the 14th International Conference on Automated Planning and Scheduling (ICAPS 2004), AAAI Press"
    locator: pp. 161 to 170 (the first description of the heuristic, and the NP-completeness of its local subproblems; general locator)
  - paper: doi:10.1613/jair.1705
    title: "Malte Helmert, The Fast Downward planning system, Journal of Artificial Intelligence Research 26 (2006)"
    locator: pp. 191 to 246; Section 5.1 and Definition 5 (domain transition graphs), Section 5.2 and Definition 6 (causal graphs), Observation 7, Section 5.2.2 (pruning to an acyclic graph), Section 6.1 with Figures 17 and 18 (the heuristic), Section 6.1.3 (infinite values), Section 6.1.4 (helpful transitions)
  - paper: "Malte Helmert and Hector Geffner, Unifying the causal graph and additive heuristics, Proceedings of the 18th International Conference on Automated Planning and Scheduling (ICAPS 2008), AAAI Press"
    locator: pp. 140 to 147 (the context-enhanced additive heuristic, which needs no acyclic graph; general locator)
---

The causal graph heuristic $h_{CG}$ of Helmert (2004) estimates the goal distance of a state in a [SAS+](/sas-plus/) task, where each state variable has a finite domain. It looks at two graphs. The *domain transition graph* $DTG(v)$ of a variable $v$ shows how the value of $v$ can change, and under which conditions on other variables. The *causal graph* has an arc from $u$ to $v$ when a change of $v$ can depend on $u$. For each goal variable, $h_{CG}$ estimates the cost of moving it from its current value to its goal value by a shortest path search in its domain transition graph; each transition costs 1 plus the cost of setting up its conditions, which the same procedure computes one level down. The heuristic sums these costs. It was the heuristic of Fast Downward, which won the classical track of the 4th International Planning Competition in 2004 (Helmert 2006). Unlike the [relaxed plan heuristic](/relaxed-plan-heuristic/), it sees that a vehicle must drive to a parcel before it can drive the parcel away. It is not admissible, and it can be $\infty$ in a state from which the goal is reachable.

## In plain words

Think of a parcel and a truck. The parcel cannot move by itself; it moves only when the truck is at the right place. So the problem has layers: the truck at the bottom, the parcel above it.

To guess how far the parcel is from its goal, plan the parcel's route step by step. Each step costs one move, plus the moves the truck needs to be where that step wants it. Remember where the truck ends up after each step, and start the next truck trip from there. This gives a good count for one parcel.

For many goals, do this for each goal on its own and add the results. That can count the same truck trip twice, so the guess can be too high.

## When it applies

- The task is a SAS+ task, or a [STRIPS](/strips/) task that a translator has turned into one by finding groups of facts of which at most one is true at a time.
- The causal graph is acyclic or close to it. Arcs that are cut to make it acyclic are conditions that the heuristic ignores, so many cycles give weak estimates.
- Plans need not be optimal. The heuristic goes with [greedy best-first search](/greedy-best-first-search/), as in Fast Downward.
- The task has transport or other chains of dependent moves, where the order of the moves of a lower variable matters. The delete relaxation lets a truck be at many places at once and misses this.

## The template

```pseudo id=main
CAUSAL-GRAPH-HEURISTIC(Π, s)
L1  build DTG(v) for each variable v and the causal graph CG; order the variables to cut CG to an acyclic graph   ▷ hole: the order
L2  in each DTG(v), drop the conditions on variables above v in the order   ▷ once per task
L3  for each goal v = g: cost_v(s(v), g) by Dijkstra on DTG(v); a transition costs 1 plus cost_u(e, e') for each condition u = e', where e is the value of u in the local state   ▷ hole: the solver of the local subproblem
L4  if some cost is ∞ then return ∞
L5  return the sum of the costs over the goal variables
```

**The graphs.** Let $o$ be an operator with precondition $\mathrm{pre}$ that sets $v$ to $d'$. If $\mathrm{pre}$ has $v = d$, then $DTG(v)$ has an arc from $d$ to $d'$ with the label $\mathrm{pre} \setminus \{v = d\}$. If $\mathrm{pre}$ says nothing about $v$, then $DTG(v)$ has an arc from every $d \ne d'$ to $d'$ with the label $\mathrm{pre}$ (Helmert 2006, Definition 5). The causal graph $CG$ has the variables as vertices and an arc $(u, v)$, for $u \ne v$, when some label of $DTG(v)$ has a condition on $u$, or when some operator changes both $u$ and $v$ (Definition 6). The second kind of arc makes every operator with two effects create a cycle.

**Line L1: pruning.** The heuristic needs an acyclic graph. Fast Downward cuts the cycles inside each [strongly connected component](/strongly-connected-components/) with a greedy order. Give each arc a weight, the number of operators that induce it. Put at the lowest level the variable whose incoming arcs from the rest of the component weigh least, remove it, and repeat (Section 5.2.2). Only the arcs from lower to higher levels stay. To cut the least total weight is the NP-hard [feedback arc set problem](/feedback-arc-set-problem/), so the greedy order is a heuristic choice.

**Line L3: the local subproblem.** For $v$ and a start value $d$, the procedure of Figure 18 of Helmert (2006) runs [Dijkstra's algorithm](/dijkstra/) on $DTG(v)$. Each value $x$ that it reaches carries a *local state*: the values of the immediate predecessors of $v$ after the cheapest path to $x$. A transition from $x$ with condition $u = e'$ costs $\mathrm{cost}_u(e, e')$, where $e$ is the value of $u$ in the local state of $x$, and this cost comes from a recursive call on $u$. After the transition, the local state has $u = e'$. The calls on $u$ start from the value of $u$ in $s$ and use $s$ for the predecessors of $u$. The recursion goes down the levels, so it stops, and a cache makes each pair $(u, e)$ cost one search per state.

**Values at the ends.** Each transition costs at least 1, so $\mathrm{cost}_v(d, d') \ge 1$ for $d \ne d'$ and $\mathrm{cost}_v(d, d) = 0$. Hence $h_{CG}(s) = 0$ exactly when $s$ satisfies the goal, and $h_{CG}(s)$ is at least the number of goal variables with a wrong value.

**One variable.** If the task has one variable, there are no conditions, and $h_{CG}$ is the shortest path length in $DTG(v)$, which is the true distance.

**Acyclic and strongly connected.** If $CG$ is acyclic and every $DTG(v)$ is strongly connected, the task has a plan from every state (Helmert 2006, Observation 7). Then $h_{CG}$ is finite everywhere: by induction up the levels, every condition has a finite cost, so Dijkstra reaches every value.

**Why it can be $\infty$.** Dijkstra commits to the cheapest path to each value of $v$, and the local state of that path may leave a predecessor where the next condition cannot be met, while a dearer path would work. Helmert (2004) shows that plan existence for the local subproblems is NP-complete, so a greedy solver is a deliberate choice. Fast Downward treats states with $h_{CG} = \infty$ as dead ends, checks this with a sound test when the whole frontier is such states, and restarts with the FF heuristic if the test fails (Section 6.1.3).

**Helpful transitions.** After computing $\mathrm{cost}_v(s(v), g)$, follow the first transition of the path that gave it. If its operator is applicable, it is helpful; if not, look for helpful transitions in the graphs of its unmet conditions. Fast Downward uses these as preferred operators, as FF uses helpful actions (Section 6.1.4).

**Cost.** For one state, there is at most one search for each pair of a variable $v$ and a value $d$. A search on $DTG(v)$ with $t$ transitions and at most $c$ conditions per transition costs $O(t (c + \log t))$ with a binary heap, apart from the recursive searches, which the cache pays for once.

## Classic examples

### A truck and a parcel

A truck drives on a line of cells $0, 1, 2, 3$ and starts at cell 3. A parcel is at cell 0 and must go to cell 2. The parcel variable has a value for each cell and one for "in the truck". Its transitions need the truck at the cell, so the causal graph has the arc from the truck to the parcel, and the truck is at the lower level. The search on the parcel's graph finds: load at 0, which costs 1 plus 3 truck moves, leaving the truck at 0; then unload at 2, which costs 1 plus 2 truck moves from 0. So $h_{CG} = 7$, the true distance. The relaxed plan length is $h^+ = 5$, since the relaxed truck is at cell 0 and cell 2 at once.

### Two parcels

With two parcels at cell 0 that must both go to cell 2, each goal is costed on its own with the truck at cell 3, so $h_{CG} = 7 + 7 = 14$. The true distance is 9, as one trip carries both parcels, and $h^+ = 7$. So $h_{CG}$ is not admissible: it counts shared work once for each goal.

### A greedy dead end

Let $u$ have values $0$ to $3$, with moves $0 \to 1$, $0 \to 3$ and $3 \to 2$. Let $v$ go from 0 to 1 when $u = 1$ or when $u = 2$, and from 1 to 2 when $u = 2$. The goal is $v = 2$, from $u = 0$, $v = 0$. Dijkstra reaches $v = 1$ most cheaply through $u = 1$, at cost 2, and commits to the local state $u = 1$. From $u = 1$, the value $u = 2$ is unreachable, so $h_{CG} = \infty$. The plan $0 \to 3$, $3 \to 2$, then the two moves of $v$, has 4 steps.

### Logistics

In Logistics, the causal graph is acyclic: trucks and planes are at the bottom and packages above them, and the domain transition graphs are strongly connected, so no arc is cut (Helmert 2006, Section 5.2.3). This is the case where $h_{CG}$ is at its best.

### Measured on random tasks

On the 2645 reachable states of 600 random SAS+ tasks with up to four variables, measured on the code of this page, $h_{CG}$ equals the true distance in 1184 of the 1396 states with a plan, is above it in 98 and below it in 114. Most of these tasks have cycles, because their operators often change two variables.

## Variations

- **Context-enhanced additive heuristic.** Helmert and Geffner (2008) show that $h_{CG}$ is the additive heuristic [$h^{\mathrm{add}}$](/h-add-heuristic/) plus context: the cost of a condition depends on the values that the plan so far has set. Their $h^{\mathrm{cea}}$ works on any causal graph, with no pruning.
- **Other orders.** Any acyclic subgraph of the causal graph gives a valid heuristic. The greedy weight order of Fast Downward is one choice.
- **Multi-heuristic search.** Fast Downward can run greedy best-first search with two open lists, one for $h_{CG}$ and one for the FF heuristic (Helmert 2006, Section 6.4).
- **Abstractions.** [Pattern databases](/pattern-database/) and merge-and-shrink also project the task onto a few variables, but they solve the projection exactly and give admissible values.
- **Landmarks.** LAMA replaced $h_{CG}$ in Fast Downward with a [landmark heuristic](/landmark-heuristic/), and finds some landmarks in the domain transition graphs.

## Pitfalls

- **Using it with A\* for optimal plans.** It counts shared work for each goal and is not admissible, as the two parcel example shows.
- **Trusting $\infty$.** A state with $h_{CG} = \infty$ may still have a plan. Pruning such states without a sound check makes the search incomplete.
- **Forgetting co-occurring effects.** Without the arcs between variables that one operator changes together, the subproblem of a variable can change variables outside its ancestors and undo goals already costed.
- **Leaving the cut conditions in.** After pruning, the conditions on higher variables must leave the labels. Otherwise the recursion can call itself on a cycle and never stop.
- **Reusing the cache across states.** The values of $\mathrm{cost}_v$ depend on the values in $s$ of the ancestors of $v$. Fast Downward shares a global cache only for variables with few ancestors.

## Exercises

1. Show that in a task where every operator has one effect and no conditions on other variables, $h_{CG}$ is the sum of the shortest path lengths in the domain transition graphs of the goal variables, and that it is then admissible.
2. Change the two parcel example so that the parcels start at different cells. Compute $h_{CG}$, $h^+$ and the true distance.
3. Give a task with an acyclic causal graph whose domain transition graphs are not strongly connected and in which $h_{CG}$ is finite in a dead-end state.

## References
