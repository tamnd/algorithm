---
tag: F1YZ07
kind: problem
slug: baseball-elimination
name: Baseball elimination problem
aliases:
- sports elimination
area: graphs/flows-and-cuts
level: core
summary: Decide whether a team is eliminated, reduced to a max-flow feasibility test.
prereqs: [max-flow-problem, flow-integrality-theorem, max-flow-min-cut-theorem]
see_also: [circulation-problem, bipartite-matching, survey-design-problem, dinic, min-cut-problem, airline-scheduling]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.12, Baseball Elimination (the flow network, the certificate of elimination, and its proof)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (baseball elimination)
  - paper: doi:10.1137/1008062
    title: Benjamin L. Schwartz, Possible winners in partially completed tournaments, SIAM Review 8(3), 302 to 308 (1966)
    locator: the whole paper (the flow model of elimination)
---

The baseball elimination problem asks whether a team can still finish a season with the most wins, given the current standings and the games that remain. A team that cannot is *eliminated*. The answer is not just a comparison of win counts: a team can be out because the teams ahead of it must play each other, and some of them must win those games. One [maximum flow](/max-flow-problem/) decides the question for one team, and a [minimum cut](/min-cut-problem/) gives a short proof of elimination: a set of teams that will win too many games on average.

## In plain words

Your team is behind, but it still has games to play. Imagine it wins all of them, which gives it a target number of wins. Is there some way to decide every other remaining game so that no other team passes that target?

Each remaining game hands out one win. Think of the wins as water. Each game sends its wins to one of its two teams, and each team can take only as many more wins as keep it at or below the target. If all the wins can be handed out without overfilling any team, your team still has a chance. If not, some group of teams has more wins coming from games among themselves than the group can absorb, and that group is the proof that your team is out.

## Definition

**Input.** A set $T$ of $k$ teams; for each team $i$ the number of wins so far $w_i$; for each pair $i \ne j$ the number $g_{ij} = g_{ji} \ge 0$ of games left between them. Each game ends with one winner, no ties. Let $r_i = \sum_j g_{ij}$ be the games left for team $i$. All numbers are integers.

**Output.** For a team $x$: is there an outcome of all remaining games in which no team has more wins than $x$? If not, $x$ is eliminated.

**The reduction.** Let $W = w_x + r_x$; it is never worse for $x$ to win all its own games. If $w_i > W$ for some $i$, $x$ is eliminated trivially. Otherwise build a directed network:

- a source $s$, a sink $t$, a node for each pair $\{i, j\}$ of teams other than $x$ with $g_{ij} > 0$, and a node for each team $i \ne x$;
- an edge from $s$ to the pair node $\{i, j\}$ with capacity $g_{ij}$;
- edges from $\{i, j\}$ to $i$ and to $j$ with capacity $\infty$ (or $g_{ij}$, which is the same);
- an edge from team $i$ to $t$ with capacity $W - w_i \ge 0$.

All capacities are integers and the network is directed; it has no antiparallel edges, since every edge goes from $s$ to a pair, from a pair to a team, or from a team to $t$. Let $g^* = \sum g_{ij}$ over the pairs not containing $x$.

**Theorem.** Team $x$ is not eliminated if and only if $w_i \le W$ for all $i$ and the maximum flow has value $g^*$.

*Proof.* An outcome in which no team passes $W$ gives a flow: send from $s$ to $\{i, j\}$ the $g_{ij}$ games, on to $i$ the games $i$ wins and to $j$ the rest, and from $i$ to $t$ the total wins of $i$ in these games, at most $W - w_i$. Its value is $g^*$. Conversely, a flow of value $g^*$ can be taken integral by the [integrality theorem](/flow-integrality-theorem/); it saturates every edge out of $s$, and reading the flow from $\{i, j\}$ to $i$ as the wins of $i$ against $j$ gives an outcome in which each team $i \ne x$ ends with at most $w_i + (W - w_i) = W$ wins. $\square$

**The certificate.** If $x$ is eliminated nontrivially, let $S$ be the source side of a minimum cut and $R$ the set of teams in $S$. Then
$$\frac{\sum_{i \in R} w_i + \sum_{\{i, j\} \subseteq R} g_{ij}}{|R|} > W,$$
so the teams of $R$ have, on average, more than $W$ wins at the end, and one of them ends above $W$. Conversely, such a set $R$ proves elimination. The proof (Kleinberg and Tardos) uses that a minimum cut never cuts an infinite edge, so a pair node in $S$ has both of its teams in $R$. A cut whose team set is $R$ therefore has capacity at least $g^* - g(R) + \sum_{i \in R} (W - w_i)$, where $g(R)$ is the number of games left inside $R$, with equality when all pairs inside $R$ are in $S$. So the minimum cut is below $g^*$ exactly when some $R$ satisfies the inequality.

## Variants

- **All teams at once.** Wayne (2001) showed that the eliminated teams are exactly those with fewer than some threshold of $w_i + r_i$, so a binary search over teams with $O(\log k)$ flows, or a single parametric computation, finds all of them.
- **Elimination numbers.** How many more games must $x$ win to stay alive, or can it lose before being out? Gusfield and Martel studied these with parametric flows.
- **Other scoring rules.** With 2 points for a win and 1 each for a draw, the same flow model works, since each game hands out 2 points split $2{:}0$, $1{:}1$ or $0{:}2$. With 3 points for a win and 1 for a draw, as in football, the question is NP-complete (Kern and Paulusma, 2001).

## Examples

**A nontrivial elimination.** Four teams $A$, $B$, $C$, $D$ with:

| team | wins $w_i$ | left vs $A$ | vs $B$ | vs $C$ | vs $D$ | left $r_i$ |
|---|---|---|---|---|---|---|
| $A$ | 70 | | 3 | 1 | 2 | 6 |
| $B$ | 69 | 3 | | 1 | 1 | 5 |
| $C$ | 66 | 1 | 1 | | 3 | 5 |
| $D$ | 64 | 2 | 1 | 3 | | 6 |

For $x = D$: $W = 64 + 6 = 70$, and no team has more than 70 wins now, so the trivial test does not decide. The network has pair nodes $AB$ (3), $AC$ (1), $BC$ (1), so $g^* = 5$, and team edges to $t$ with capacities $A$: 0, $B$: 1, $C$: 4. The edge from $A$ has capacity 0: $A$ already has 70 wins and must lose every game it has left. A maximum flow sends 1 through $AB \to B$, 1 through $AC \to C$ and 1 through $BC \to C$: value 3, less than 5. So $D$ is eliminated. The minimum cut has $S = \{s, AB, A, B\}$, of capacity $1 + 1 + 0 + 1 = 3$, and $R = \{A, B\}$: these teams have $70 + 69 = 139$ wins and 3 more to come from games between them, $142/2 = 71 > 70$. Whatever happens, $A$ or $B$ ends with at least 71 wins.

**Not eliminated.** For $x = C$: $W = 66 + 5 = 71$. The pairs are $AB$ (3), $AD$ (2), $BD$ (1), $g^* = 6$, and the team capacities are $A$: 1, $B$: 2, $D$: 7. The maximum flow is 6, for example $A$ wins 1 game against $B$, $B$ wins 2 against $A$, and $D$ wins its 3 games against $A$ and $B$. Then $A$ has 71, $B$ has 71, $C$ can reach 71, and $C$ is not eliminated (it can tie for first).

**A trivial elimination.** If $D$ had only 3 games left, $W = 67 < 70 = w_A$, and no flow is needed.

**No games among the others.** If every remaining game involves $x$, there are no pair nodes, $s$ has no edges, and no s-t path exists. Then $g^* = 0$, the maximum flow 0 equals $g^*$, and $x$ is out only if the trivial test says so.

## Known algorithms

- **One maximum flow per team.** The network has $O(k^2)$ nodes and edges. Any maximum flow algorithm works, for instance [Dinic's algorithm](/dinic/) or [Ford-Fulkerson](/ford-fulkerson/), which needs at most $g^*$ augmentations of $O(k^2)$ each.
- **All teams.** Run one flow per team, $k$ flows in total, or use Wayne's threshold property to need far fewer.
- **The certificate** comes from the reachable set of the final residual graph at no extra cost.

## Bounds

The network has $O(k^2)$ nodes and edges, so the problem for one team is solved in the time of one maximum flow on that size, for example $O(k^2 g^*)$ by augmenting paths or $O(k^6)$ by Dinic's bound, and in almost-linear time in $k^2$ by the newest maximum flow algorithms. The input has $\Theta(k^2)$ numbers, a lower bound.

## Reductions

- **To maximum flow**, as above; equivalently to a bipartite transportation problem between games and teams, or to a [circulation with demands](/circulation-problem/).
- **Hall-type condition.** The certificate is a Hall-type condition for the bipartite graph of games and teams, a form of the max-flow min-cut theorem.

## Applications

Sports standings: newspapers and league websites mark teams as mathematically eliminated, and the flow model avoids the error of comparing a team only with the leader. The same model fits any question of whether outcomes of pending pairwise contests can keep every competitor under a cap: tournament design, voting where each pair hands out one point, and the [survey design](/survey-design-problem/) and allocation problems that are bipartite flows.

## References
