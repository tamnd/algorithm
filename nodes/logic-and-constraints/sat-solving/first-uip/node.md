---
tag: XNV2KH
kind: concept
slug: first-uip
name: First unique implication point
aliases:
- 1UIP
- first UIP cut
- first UIP clause
area: logic-and-constraints/sat-solving
level: advanced
summary: The unique implication point nearest to the conflict in the implication graph. The cut there gives the standard learned clause of CDCL, with one literal of the conflict level.
prereqs: [implication-graph, unit-propagation]
see_also: [clause-learning, cdcl, non-chronological-backtracking, dominator-tree, clause-minimization, binary-resolution, drat-proof, cdcl-simulates-resolution]
sources:
  - paper: "João P. Marques-Silva and Karem A. Sakallah, GRASP, a new search algorithm for satisfiability, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1996"
    locator: pages 220 to 227 (unique implication points of the conflict level and the clauses learned at them)
  - paper: "Lintao Zhang, Conor F. Madigan, Matthew W. Moskewicz and Sharad Malik, Efficient conflict driven learning in a Boolean satisfiability solver, Proceedings of ICCAD 2001, pages 279 to 285"
    locator: the learning schemes as cuts of the implication graph, the first UIP, second UIP, all UIP and decision schemes, and their measured comparison
  - paper: doi:10.1613/jair.1410
    title: Paul Beame, Henry Kautz and Ashish Sabharwal, Towards understanding and harnessing the potential of clause learning, Journal of Artificial Intelligence Research 22, 2004
    locator: pages 319 to 351 (cuts, asserting clauses and the first UIP scheme as a learning scheme)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (conflict analysis, UIPs and the first UIP clause)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (conflict clauses by resolution, UIPs and asserting clauses)
---

The first unique implication point (first UIP) of a conflict is the node of the conflict level, in the [implication graph](/implication-graph/) of a SAT search, that lies on every path from that level's decision to the conflict and is the nearest such node to the conflict. The first UIP cut separates the first UIP and everything before it from the nodes between it and the conflict, and the clause read from this cut has exactly one literal of the conflict level. So after a backjump the clause is unit and forces a new literal at once. This clause is the one that [clause learning](/clause-learning/) in [CDCL](/cdcl/) solvers adds after almost every conflict.

## In plain words

When a solver hits a dead end, it can blame the last guess and everything it set before. That is true, but long. A better reason often sits closer to the dead end. Look at the chain of forced values that the last guess started. Sometimes every chain from the guess to the dead end passes through one single value. That value is a choke point: whatever the guess was, the trouble passes through it.

The first choke point is the one nearest to the dead end. The solver blames this value together with the older values from earlier guesses that fed into the chain after it. The new rule says "not all of these at once". It has only one value from the last guess, so after the solver goes back, the rule forces a new value at once.

## The idea

**Setting.** A search keeps a trail of true literals with decision levels, and a reason clause for each forced literal, as on the [implication graph](/implication-graph/) page. Assume that [unit propagation](/unit-propagation/) is complete before each decision. A clause $K$ of the formula is false, and the conflict level $d \ge 1$ is the largest level of the literals of $K$; as in standard CDCL, $d$ is also the current level, so no node has a level above $d$. The node $\kappa$ has an edge from $\neg q$ for each $q \in K$. Write $\delta_d$ for the decision of level $d$, and $\mathrm{pos}(v)$ for the trail position of $v$.

**UIPs.** A node $u$ of level $d$ is a *unique implication point* when every path from $\delta_d$ to $\kappa$ passes through $u$. The decision $\delta_d$ is always a UIP, so at least one exists. The UIPs are the [dominators](/dominator-tree/) of $\kappa$ in the level-$d$ part of the graph with root $\delta_d$, so every path from $\delta_d$ to $\kappa$ meets all of them in the same order. The *first UIP* $u_1$ is the UIP with the largest trail position, that is, the immediate dominator of $\kappa$.

**Cuts and their clauses.** A cut is a split of the nodes into a reason side $A$, which holds all decisions, and a conflict side $B$, which holds $\kappa$. Let $R$ be the set of nodes of $A$ with an edge into $B$. The clause of the cut is $\{\neg v : v \in R\}$. The *first UIP cut* puts in $B$ the node $\kappa$ and every node of level $d$ that comes after $u_1$ on the trail and has a path to $\kappa$. Its clause is $\neg u_1$ together with the negations of the lower-level nodes that have an edge into $B$.

**Lemma 1 (a cut clause is implied).** Let $F'$ be $F$ together with the clauses learned so far, each implied by $F$. Setting every literal of the cut clause false, that is, every $v \in R$ true, and running unit propagation on $F'$ ends in a conflict. So $F \models \{\neg v : v \in R\}$. *Proof.* Suppose that propagation ends without a conflict. Then no clause of $F'$ is unit or false. Take the nodes of $B \setminus \{\kappa\}$ in trail order. Each one is forced, because the decisions are in $A$. Each of its predecessors is in $R$ or is an earlier node of $B$, by the definition of $R$, and so it is true by induction. So the reason clause of the node has all its other literals false, and since that clause is not unit or false, the node is true. Then every literal of $K$ is false, which is a contradiction. Every model of $F$ satisfies $F'$, so it cannot make all of $R$ true, and it satisfies the clause. $\blacksquare$

The second part says that the clause has the reverse unit propagation property, which is what a [DRAT](/drat-proof/) checker tests for each learned clause.

**Computing it by resolution.** Solvers find the first UIP clause without building the graph. They start from the false clause and resolve away the latest literal of the conflict level until one is left:

$$C \leftarrow K; \quad \text{while } C \text{ has two or more literals of level } d: \ t \leftarrow \text{the latest trail literal with } \neg t \in C, \ C \leftarrow (C \setminus \{\neg t\}) \cup (\mathrm{reason}(t) \setminus \{t\}).$$

Each step is one [binary resolution](/binary-resolution/) on the variable of $t$, because $\neg t \in C$ and $t \in \mathrm{reason}(t)$.

**Theorem.** The loop stops. At the stop, the only literal of level $d$ in $C$ is $\neg u_1$, and $C$ is the clause of the first UIP cut. Every literal of $C$ is false on the trail, $C$ is implied by $F$ and the reason clauses, and $C$ is asserting: if $b$ is the largest level of the other literals of $C$ (or 0 when there are none), then $b < d$, and after removing every level above $b$, the clause $C$ is unit with the literal $\neg u_1$.

*Proof.* Let $N(C)$ be the set of level-$d$ nodes $v$ with $\neg v \in C$. Three facts hold before each step.

1. *Every literal of $C$ is false on the trail.* It holds for $K$. A step removes $\neg t$ and adds the literals of $\mathrm{reason}(t)$ other than $t$, which are false because they made the reason unit. Two complementary literals cannot both be false, so no resolvent is a tautology and each step resolves on one variable only.
2. *(Cut) Every path from $\delta_d$ to $\kappa$ meets $N(C)$.* A node reachable from $\delta_d$ has level at least $d$, since levels do not decrease along edges, and so exactly $d$. So the last node before $\kappa$ on such a path is a level-$d$ predecessor of $\kappa$, which is in $N(K)$. A step removes $t$ from $N$ and adds the level-$d$ predecessors of $t$. The node $t$ is not $\delta_d$, because $t$ has the largest position in $N$, $N$ has two or more nodes, and $\delta_d$ has the smallest position of level $d$. So a path through $t$ enters $t$ from a level-$d$ predecessor, which is now in $N$.
3. *(Path) Each $v \in N(C)$ has a path to $\kappa$ whose inner nodes have all been resolved.* It holds for $N(K)$ with the direct edge. A predecessor $w$ added when $t$ is resolved has the edge $w \to t$ followed by the path of $t$.

Now take any $v \in N(C)$ with $\mathrm{pos}(v) < \mathrm{pos}(u_1)$. With complete propagation, every level-$d$ node is reachable from $\delta_d$, as the [implication graph](/implication-graph/) page shows. Join such a path to the path of fact 3. The nodes of the first part have positions at most $\mathrm{pos}(v) < \mathrm{pos}(u_1)$, and $u_1$ is on the joined path, so $u_1$ is an inner node of the second part and has been resolved. Hence, while $u_1$ is not resolved, every node of $N(C)$ has position at least $\mathrm{pos}(u_1)$. The loop resolves the node of largest position, and only when $|N(C)| \ge 2$. If it ever chose $u_1$, then all of $N(C)$ would have positions in the range from $\mathrm{pos}(u_1)$ to $\mathrm{pos}(u_1)$, so $N(C) = \{u_1\}$, a contradiction. So $u_1$ is never resolved.

*Termination.* Let $p$ be the largest position in $N(C)$. A step removes the node at $p$ and adds predecessors, whose positions are smaller than $p$. So $p$ drops by at least 1 at each step, and $p \ge \mathrm{pos}(u_1)$ throughout. The loop makes at most as many steps as there are level-$d$ nodes after $u_1$.

*The stop.* By fact 2, $N(C)$ is never empty, so at the stop $N(C) = \{v\}$ for one node $v$. By fact 2, $v$ is on every path from $\delta_d$ to $\kappa$, so $v$ is a UIP, and by the paragraph above $\mathrm{pos}(v) \ge \mathrm{pos}(u_1)$. The first UIP has the largest position among the UIPs, so $v = u_1$.

*The cut.* A resolved node has a position above $\mathrm{pos}(u_1)$ and, by fact 3, a path to $\kappa$. Conversely, let $w$ be a level-$d$ node after $u_1$ with a path to $\kappa$. Walk the path back from $\kappa$. The last node before $\kappa$ enters $N$ at the start. A node that enters $N$ and lies after $u_1$ is not in the final $N = \{u_1\}$, so it was resolved, and then its predecessor on the path entered $N$. So $w$ was resolved. The resolved nodes are therefore exactly the level-$d$ nodes of the conflict side of the first UIP cut. The lower-level literals of $C$ come from $K$ and from the reasons of the resolved nodes, so they are the negations of the lower-level nodes with an edge into that side, and $C$ is the cut clause.

*Implied and asserting.* Each step resolves $C$ with a clause of the formula or an earlier learned clause, and a resolvent is implied by its two premises; by induction, $C$ is implied. Every literal of $C$ other than $\neg u_1$ is the negation of a node of level below $d$, so $b < d$. After the levels above $b$ are removed, those literals stay false, and the variable of $u_1$, of level $d > b$, is unassigned. So $C$ is unit with $\neg u_1$. $\blacksquare$

The same resolution loop, continued while a literal of level $d$ has a reason, stops at the decision $\delta_d$ and gives the decision cut clause. The first UIP clause is never longer. Both clauses have one literal of level $d$. The conflict side of the first UIP cut is a subset of the conflict side of the decision cut, so every lower-level node with an edge into the first is also a node with an edge into the second.

**Why the first UIP.** Any UIP gives an asserting clause, and the first one is the closest to the conflict. Zhang, Madigan, Moskewicz and Malik (2001) compared the first UIP, second UIP, all UIP, decision and GRASP schemes in Chaff and found that the first UIP scheme performed best on their benchmarks. They and later authors explain this by locality: the clause holds the literals that took part in the conflict most directly, and it is often short. This is a measured result, not a theorem. Beame, Kautz and Sabharwal (2004) formalized learning schemes as cuts and asserting clauses, and the proofs that [CDCL simulates resolution](/cdcl-simulates-resolution/) need only that each learned clause is asserting.

**Cost.** The loop visits each node of level $d$ at most once, as the termination argument shows, and reads its reason once. With a mark per variable for the literals already in $C$, and a counter of the level-$d$ literals in $C$ in place of the set $N$, the time is $O(s + e)$ for $s$ nodes of level $d$ with $e$ in-edges in total, plus the length of $K$. This is the loop of MiniSat's conflict analysis.

## Examples

**A first UIP that is not the decision.** Take the formula of the [CDCL](/cdcl/) page:

$$C_1 = \{x_1, x_2\},\ C_2 = \{x_1, x_3, x_7\},\ C_3 = \{\neg x_2, \neg x_3, x_4\},\ C_4 = \{\neg x_4, x_5, x_8\},\ C_5 = \{\neg x_4, x_6, x_9\},\ C_6 = \{\neg x_5, \neg x_6\}.$$

The decisions $\neg x_7$, $\neg x_8$, $\neg x_9$ and $\neg x_1$ open levels 1 to 4. Propagation adds $x_2, x_3, x_4, x_5, x_6$ at level 4, and $C_6$ is false. The UIPs of level 4 are $\neg x_1$ and $x_4$, so the first UIP is $x_4$. The loop runs as follows.

| step | $C$ | level-4 literals in $C$ | resolve on | with |
|---|---|---|---|---|
| 0 | $\{\neg x_5, \neg x_6\}$ | 2 | $x_6$ | $C_5$ |
| 1 | $\{\neg x_4, \neg x_5, x_9\}$ | 2 | $x_5$ | $C_4$ |
| 2 | $\{\neg x_4, x_8, x_9\}$ | 1 | stop | |

The clause $\{\neg x_4, x_8, x_9\}$ has $b = 3$, the level of $\neg x_9$. After the backjump to level 3, it is unit and forces $\neg x_4$ at level 3. If the loop goes on to the decision, three more steps resolve on $x_4$ with $C_3$, on $x_3$ with $C_2$ and on $x_2$ with $C_1$, and give $\{x_1, x_7, x_8, x_9\}$, which is longer.

**A first UIP that is the decision.** Continue the run. At level 3, after $\neg x_4$, nothing else is forced. The solver decides $\neg x_1$ at level 4 again; $C_1$ forces $x_2$, $C_2$ forces $x_3$, and $C_3 = \{\neg x_2, \neg x_3, x_4\}$ is false. Here $x_2$ and $x_3$ both lead from $\neg x_1$ to the conflict on separate paths, so the only UIP is the decision.

| step | $C$ | level-4 literals in $C$ | resolve on | with |
|---|---|---|---|---|
| 0 | $\{\neg x_2, \neg x_3, x_4\}$ | 2 | $x_3$ | $C_2$ |
| 1 | $\{x_1, \neg x_2, x_4, x_7\}$ | 2 | $x_2$ | $C_1$ |
| 2 | $\{x_1, x_4, x_7\}$ | 1 | stop | |

The literal $x_4$ is false at level 3 and $x_7$ at level 1, so $b = 3$, and after the backjump the clause forces $x_1$ at level 3.

**A non-example.** The clause $\{\neg x_4, \neg x_5, x_9\}$ after step 1 of the first table is implied by $F$, and all its literals are false at the conflict, but it has two literals of level 4. After a backjump to any level below 4, both $\neg x_4$ and $\neg x_5$ are open, so it is not unit and does not force anything. A cut that is not at a UIP gives such a clause.

## Where it is used

- **[Clause learning](/clause-learning/) in [CDCL](/cdcl/).** Chaff, MiniSat, Glucose, CaDiCaL and Kissat learn the first UIP clause, often shortened afterwards by [clause minimization](/clause-minimization/), which never removes the UIP literal.
- **[Non-chronological backtracking](/non-chronological-backtracking/).** Because the clause is asserting, its second highest level is the jump target, and the solver asserts $\neg u_1$ there with the learned clause as its reason.
- **Proof logging.** By Lemma 1, each first UIP clause is a reverse unit propagation step, so a solver can write it to a [DRAT](/drat-proof/) or [LRAT](/lrat-proof/) proof as it is learned; the resolution steps of the loop give the hints of LRAT.
- **Proof complexity.** The simulation of resolution by CDCL with restarts, due to Pipatsrisawat and Darwiche, works for any asserting learning scheme, and so for the first UIP scheme.
- **[DPLL(T)](/dpll-t/) and lazy clause generation.** Theory propagations and constraint propagators add nodes with explained reasons, and the same loop finds the first UIP over them. Constraint solvers use it as [nogood learning](/nogood-learning/).

## References
