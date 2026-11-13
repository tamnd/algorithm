---
tag: SVVVV7
kind: technique
slug: landmark-heuristic
name: Landmark heuristic
aliases:
- landmark counting
area: games-and-search/planning
level: research
summary: Estimates cost by counting facts or actions that every plan must achieve.
prereqs: [delete-relaxation, relaxed-planning-graph, admissible-heuristic]
see_also: [relaxed-plan-heuristic, h-max-heuristic, causal-graph-heuristic, fast-forward-planner, hitting-set, linear-programming-problem, a-star-search, sas-plus]
sources:
  - paper: doi:10.1613/jair.1492
    title: "Joerg Hoffmann, Julie Porteous and Laura Sebastia, Ordered landmarks in planning, Journal of Artificial Intelligence Research 22 (2004)"
    locator: pp. 215 to 278; Section 3.1 with Definition 1 (landmarks) and Theorem 1 (deciding a landmark is PSPACE-complete), Section 4.1 and Proposition 1 (the test by the delete relaxation), Section 5 (landmarks as intermediate goals)
  - paper: doi:10.1613/jair.2972
    title: "Silvia Richter and Matthias Westphal, The LAMA planner: guiding cost-based anytime planning with landmarks, Journal of Artificial Intelligence Research 39 (2010)"
    locator: pp. 127 to 177; Section 4 (landmarks and their orderings), Section 4.2 (how LAMA finds them), Section 5 and Algorithm 3 (the landmark count heuristic with accepted and required again landmarks)
  - paper: "Erez Karpas and Carmel Domshlak, Cost-optimal planning with landmarks, Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI 2009)"
    locator: pp. 1728 to 1733 (admissible landmark heuristics by cost partitioning; general locator)
  - paper: "Lin Zhu and Robert Givan, Landmark extraction via planning graph propagation, ICAPS 2003 Doctoral Consortium"
    locator: pp. 156 to 160 (fact and action landmarks by propagation in the planning graph; general locator)
  - paper: "Emil Keyder, Silvia Richter and Malte Helmert, Sound and complete landmarks for and/or graphs, Proceedings of the 19th European Conference on Artificial Intelligence (ECAI 2010), IOS Press"
    locator: pp. 335 to 340 (the landmarks of the delete relaxation as a fixed point; general locator)
  - paper: "Malte Helmert and Carmel Domshlak, Landmarks, critical paths and abstractions: what's the difference anyway?, Proceedings of the 19th International Conference on Automated Planning and Scheduling (ICAPS 2009)"
    locator: pp. 162 to 169 (disjunctive action landmarks and the LM-cut heuristic; general locator)
---

A landmark of a planning task is a fact that is true at some point on every plan, or an action that occurs in every plan. A landmark heuristic estimates the distance from a state to the goal by the landmarks that a plan from this state must still achieve. The plain version counts them, as the LAMA planner does (Richter and Westphal 2010); it is fast and informative, but not [admissible](/admissible-heuristic/), because one action can achieve several landmarks. If each action's cost is split among the landmarks it achieves, the sum of the cheapest shares is admissible (Karpas and Domshlak 2009). To decide if a fact is a landmark is PSPACE-complete (Hoffmann, Porteous and Sebastia 2004, Theorem 1), so planners find landmarks in the [delete relaxation](/delete-relaxation/), where the test is polynomial and every landmark found is a real one.

## In plain words

Some steps are part of every solution. To fly a parcel to another city, it must at some point be in the plane, whatever else the plan does. Such a step is a landmark. If you know the landmarks, you can count how many are still ahead of you, and use that count as a guess of the distance to the goal.

The count can be too high, because one move can reach two landmarks at once. To fix this, give each move one unit of cost and split it among the landmarks it reaches; then add up the cheapest share of each landmark. That sum is never too high.

Finding every landmark is very hard. A simpler version of the task, where nothing is ever undone, gives many of them quickly, and each one it gives is a true landmark.

## When it applies

- The task is a [STRIPS](/strips/) or [SAS+](/sas-plus/) task, and a forward search needs a goal-distance estimate in each state.
- For plans without an optimality guarantee, the count goes with [greedy best-first search](/greedy-best-first-search/), often together with the [relaxed plan heuristic](/relaxed-plan-heuristic/).
- For optimal plans, a cost-partitioned version goes with [A*](/a-star-search/).
- The heuristic helps most when the task has long chains of forced subgoals, such as transport through fixed hubs. It helps least when most facts can be reached in many different ways, because then few facts are landmarks.

## The template

```pseudo id=main
LANDMARK-HEURISTIC(A, s, G, π)
L1  L ← the fact landmarks of the task, found in the delete relaxation   ▷ hole: the finder; from s, or once from I
L2  if some goal of G is not reachable from s in the delete relaxation then return ∞
L3  N ← the landmarks of L that s still has to achieve   ▷ hole: not true in s, or not accepted on the path π, plus the required again
L4  c(l) ← a cost for each l in N   ▷ hole: 1 for each, or a share of the cost of its achievers
L5  return the sum of c(l) over N
```

**Line L1: a finder in the delete relaxation.** Let $s$ be the state. For each fact $f$, let $LM(f)$ be the set of facts that every relaxed derivation of $f$ from $s$ passes through. It is the greatest solution of

$$LM(f) = \{f\} \text{ for } f \in s, \qquad LM(f) = \{f\} \cup \bigcap_{a : f \in \mathrm{add}(a)} \; \bigcup_{p \in \mathrm{pre}(a)} LM(p) \text{ otherwise},$$

over the achievers $a$ that are relaxed reachable. Start every unreached fact at the set of all facts and apply the equations until nothing changes. The landmarks are $L = \bigcup_{g \in G} LM(g)$. This is the propagation of Zhu and Givan (2003), in the form of Keyder, Richter and Helmert (2010). On the tests of this page, $L \setminus s$ is exactly the set of facts that are goals or that every relaxed plan uses as a precondition: the causal landmarks of the relaxed task.

**Why the finder is sound.** A real plan is also a relaxed plan, and after $i$ steps the relaxed state is the union of the real states $0, \ldots, i$. Take $l \in LM(f)$ and a relaxed run that makes $f$ true. Look at the first action that adds $f$. It is one of the achievers in the equation, and its preconditions were true earlier, so by induction on the run each fact of $LM(p)$, for each of its preconditions $p$, was true earlier. So $l$ is true at some point before $f$ or $l = f$, and in a real plan, $l$ is true in some real state. For the same reason, $l \in LM(m)$ gives a natural ordering: $l$ is true at some point before $m$ first becomes true.

**A second test.** Hoffmann, Porteous and Sebastia (2004, Proposition 1) remove every action that adds $f$ and check whether the relaxed task is still solvable. If it is not, $f$ is a landmark. This test also finds facts that come only as side effects of needed actions, which the fixed point does not find. The converse fails: a real landmark can fail the test, because the relaxation may reach the goal without it.

**Line L3: what is still open.** The code of this page recomputes $L$ from each state and counts the landmarks not true in $s$. LAMA finds $L$ once, from the initial state, and keeps a set of *accepted* landmarks along the path $\pi$ to $s$ (Richter and Westphal 2010, Section 5):

$$L(s, \pi) = (L \setminus \mathrm{Accepted}(s, \pi)) \cup \mathrm{ReqAgain}(s, \pi).$$

A landmark is accepted when it becomes true after all landmarks ordered before it are accepted. An accepted landmark is required again if it is false in $s$ and is a goal, or must be true just before a landmark that is not yet accepted. The value depends on the path, and LAMA computes it once per state, when the state is first reached.

**Line L4: count or partition.** Counting gives $h_{LM}(s) = |N|$. Uniform cost partitioning gives each action $a$ the share $1 / |\mathrm{add}(a) \cap N|$ for each open landmark it adds, and $c(l)$ is the least share of $l$ over its achievers.

**Admissibility of the partition.** Let $\rho$ be a plan from $s$. Each $l \in N$ is false in $s$ and is true at some point on $\rho$, so some action $a_l$ of $\rho$ adds $l$. Then

$$|\rho| \ \ge \sum_{a \in \rho} \ \sum_{l \in \mathrm{add}(a) \cap N} \frac{1}{|\mathrm{add}(a) \cap N|} \ \ge \ \sum_{l \in N} c(l),$$

since each action of $\rho$ gives out a total of at most 1, and each $l$ gets at least its least share from $a_l$. The same argument on relaxed plans gives $\sum c(l) \le h^+(s)$.

**Values at the ends.** If $G \subseteq s$, then $LM(g) = \{g\}$ for each goal, so $N$ is empty and both versions return 0. If some goal is false in $s$, it is in $N$, and both are positive. If the goal is not relaxed reachable, line L2 returns $\infty$, and the state is a dead end.

**Cost.** Each round of the fixed point looks at every action once and unites the sets of its preconditions, in $O(m p n)$ time for $m$ actions, at most $p$ preconditions per action and $n$ facts. Each round that changes something reaches a new fact or removes a fact from some set, so there are at most $n^2 + n + 1$ rounds. LAMA pays this once, from the initial state; the code of this page pays it in every state.

## Classic examples

### Logistics

A parcel is at $A$, a truck is at $A$, and a plane is at the airport $E$ of another city. The truck can drive between $A$ and the airport $B$; the plane can fly between $B$ and $E$. The goal is the parcel at $E$. Besides the facts of the initial state, the fixed point finds six landmarks: the parcel in the truck, the truck at $B$, the parcel at $B$, the plane at $B$, the parcel in the plane and the parcel at $E$. The orderings say that the parcel is in the truck before it is at $B$, and at $B$ before it is in the plane. The count is 6, equal to $h^+$; the optimal plan has 7 actions, because the plane must fly to $B$ and back, and the relaxation keeps it at $E$ too. LAMA's paper opens Section 4 with this kind of task.

### One action, two landmarks

Let the action $ab$ add $p$ and $q$, and let $g$ need $p$ and $q$ and add the goal $g$. The landmarks are $p$, $q$ and $g$, so the count is 3, and the optimal plan has 2 actions. The count is not admissible. The partition gives $ab$ the share $\frac{1}{2}$ for each of $p$ and $q$, and the result is $\frac{1}{2} + \frac{1}{2} + 1 = 2$.

### Blocks world

In the [blocks world](/blocks-world/) with three blocks on the table and the goal $\mathit{on}(A, B)$, $\mathit{on}(B, C)$, the landmarks outside the initial state are $\mathit{holding}(A)$, $\mathit{holding}(B)$ and the two goals. The count is 4, which is the optimal plan length. Over the 22 reachable states, measured on the code of this page, the count is below the goal distance in 13 states, equal in 5 and above in 4. The cost partition is never above, and is equal in 4 states.

### A landmark that the relaxation misses

Let $\mathit{work}$ need $\mathit{home}$, add $\mathit{job}$ and delete $\mathit{home}$; let $\mathit{call}$ need $\mathit{job}$ and add $\mathit{taxi}$; and let $\mathit{ride}$ need $\mathit{taxi}$ and add $\mathit{home}$. From $\{\mathit{home}\}$ with the goal $\{\mathit{job}, \mathit{home}\}$, every plan calls the taxi, so $\mathit{taxi}$ is a landmark. In the relaxation, $\mathit{home}$ is never deleted, the plan $\mathit{work}$ suffices, and neither finder reports $\mathit{taxi}$. Over 299 solvable random tasks in the tests, exact search finds 433 landmarks outside the initial state, Proposition 1 finds 428 and the fixed point finds 359.

## Variations

- **Action landmarks.** An action is a landmark of the relaxed task if the relaxed task without it is unsolvable. Zhu and Givan (2003) find action and fact landmarks together.
- **Disjunctive landmarks.** A set of facts, or of actions, such that every plan contains at least one of them. LM-cut (Helmert and Domshlak 2009) finds disjunctive action landmarks by cuts in the justification graph of [$h^{\max}$](/h-max-heuristic/), and gives each cut the cost of its cheapest action. It is admissible and is among the strongest heuristics for optimal planning.
- **Better partitions.** The uniform split is simple but often weak. A [linear program](/linear-programming-problem/) can find the best partition of the action costs among the landmarks, and the cost of a minimum [hitting set](/hitting-set/) of a set of disjunctive action landmarks is also admissible and is at least the best partition of the same landmarks.
- **Path information.** Karpas and Domshlak (2009) note that when several paths reach a state, a landmark counts as accepted only if every known path achieved it, so the intersection of the accepted sets can be used.
- **Landmarks as subgoals.** Hoffmann, Porteous and Sebastia (2004, Section 5) give the landmarks to a planner as a sequence of intermediate goals. This can lead to dead ends and lose completeness, which a heuristic does not.
- **Other finders.** LAMA uses back-chaining through the shared preconditions of first achievers, and also the domain transition graphs of a finite-domain task (Richter and Westphal 2010, Section 4.2).

## Pitfalls

- **Using the count with A\*.** The count is not admissible, as the example with $ab$ shows. Use a partition or LM-cut for optimal plans.
- **Trusting a path-based value at a goal state.** With reasonable orderings, LAMA's count can be positive in a goal state, because a plan may ignore the orderings (Richter and Westphal 2010, Section 5). Test the goal directly.
- **Treating the relaxed finder as complete.** The finder misses landmarks that depend on deletes, as the taxi example shows. Fewer landmarks only make the estimate weaker, never wrong.
- **Calling facts of the initial state open.** A fact that is true in $s$ is a landmark trivially, and counting it would give positive values at goal states.
- **Forgetting the required again set.** A path-based count without it drops to 0 too early: a goal that was achieved and then deleted is still needed.

## Exercises

1. Show that every fact of $L \setminus s$ passes the test of Proposition 1.
2. Give a task where a fact passes Proposition 1 but is not in $\bigcup_{g} LM(g)$. (Hint: an action that the goal needs and that has a second add effect.)
3. Show that the uniform partition is at most the count. When are they equal?

## References
