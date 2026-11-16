---
title: Why integral flows in the tracking network are sets of disjoint tracks, and why successive shortest paths stopped at the first nonnegative path give the track set of least cost
proves: [correctness]
status: full
---

Notation as on the page. The network $G$ has the nodes $s$, $t$, $u_i$, $v_i$ for $i = 1, \ldots, n$, and the edges $u_i \to v_i$ (cost $c_i$), $s \to u_i$ (cost $c_{\text{en}}$), $v_i \to t$ (cost $c_{\text{ex}}$) and $v_i \to u_j$ for each allowed link (cost $c_{ij}$), all of capacity 1. Links go from an earlier frame to a later one. A track is a sequence of detections $i_1, \ldots, i_r$ with $r \ge 1$ in which each $(i_q, i_{q+1})$ is an allowed link. Its cost is $c_{\text{en}} + \sum_q c_{i_q} + \sum_q c_{i_q i_{q+1}} + c_{\text{ex}}$. A track set is a set of tracks with no detection in common.

## Claim 1: integral flows of value k are track sets of k tracks

Every track set with $k$ tracks gives an integral flow of value $k$ with the same cost, and every integral flow of value $k$ gives a track set with $k$ tracks and the same cost.

*Proof.* A track $i_1, \ldots, i_r$ is the $s$-$t$ path $s, u_{i_1}, v_{i_1}, u_{i_2}, \ldots, v_{i_r}, t$, and the cost of the path is the cost of the track. Disjoint tracks use disjoint edges $u_i \to v_i$ and so disjoint edges overall, since every other edge touches one $u_i$ or $v_i$ of a single track. So the sum of the paths is a flow with values 0 or 1, of value $k$, and its cost is the sum of the track costs.

Conversely, take an integral flow $f$ of value $k$. All capacities are 1, so $f$ is 0 or 1 on each edge. The graph $G$ has no directed cycle: number the nodes by frame and put $u_i$ before $v_i$, then every edge other than those at $s$ and $t$ goes from a node of a frame to a later node. By [flow decomposition](/flow-decomposition/), a flow in a graph with no cycle is a sum of $k$ $s$-$t$ paths, each with flow 1. Node $u_i$ has a single outgoing edge, of capacity 1, so at most one path passes through $u_i$, and any path through $u_i$ continues to $v_i$. Node $v_i$ has a single incoming edge, so a path that reaches $v_i$ came from $u_i$. So each path has the form $s, u_{i_1}, v_{i_1}, \ldots, v_{i_r}, t$ with allowed links in between, which is a track, and no two paths share a detection. The cost of $f$ is the sum of the path costs, which is the cost of the track set. $\square$

The empty track set is the zero flow, of cost 0. So the least cost over all track sets is $\min_k F(k)$, where $F(k)$ is the least cost of an integral flow of value $k$ (and $F(k) = \infty$ if no flow of value $k$ exists).

## Claim 2: each augmentation keeps the flow optimal for its value

Let $f_k$ be the flow after $k$ augmentations. Then $f_k$ has the least cost among all flows of value $k$, the residual graph $G_{f_k}$ has no cycle of negative cost, and $f_k$ is integral.

*Proof.* By induction on $k$. The zero flow is the only flow of value 0, and $G_{f_0} = G$ has no cycle at all. Assume the claim for $k$. A flow of value $k$ is of least cost if and only if its residual graph has no cycle of negative cost (the negative cycle optimality condition of the [min-cost flow problem](/min-cost-flow-problem/)). Since $G_{f_k}$ has no negative cycle, Bellman-Ford computes correct shortest distances from $s$, and the path $P$ it returns is a shortest $s$-$t$ path. The [successive shortest path](/successive-shortest-path/) theorem says that augmenting a flow of least cost for its value along a shortest path of the residual graph gives a flow of least cost for the new value. So $f_{k+1}$ is of least cost for value $k + 1$, and by the optimality condition $G_{f_{k+1}}$ has no negative cycle. All residual capacities are integers and the path carries one unit, so $f_{k+1}$ is integral. $\square$

## Claim 3: the cost is convex in the number of tracks, so the stopping rule is right

Let $d_{k+1}$ be the cost of the shortest path found in step $k + 1$. Then $F(k + 1) = F(k) + d_{k+1}$, and $F$ is convex on the values $k$ for which a flow exists. So $d_1 \le d_2 \le \ldots$, and if the method stops before step $k + 1$ because $d_{k+1} \ge 0$ or no path exists, then $F(k) = \min_j F(j)$.

*Proof.* By Claim 2, $F(k + 1) = \operatorname{cost}(f_{k+1}) = \operatorname{cost}(f_k) + d_{k+1} = F(k) + d_{k+1}$.

For convexity, let $\bar F(x)$ be the least cost of a flow of value $x$ with real flows allowed, the optimal value of a linear program whose constraints are $A f = x b$, $0 \le f \le 1$, with $A$ the node-edge incidence matrix and $b$ the vector with $1$ at $s$ and $-1$ at $t$. If $f$ and $g$ are optimal for the values $x$ and $y$, then $\theta f + (1 - \theta) g$ is feasible for the value $\theta x + (1 - \theta) y$, so $\bar F(\theta x + (1 - \theta) y) \le \theta \bar F(x) + (1 - \theta) \bar F(y)$, and $\bar F$ is convex. The incidence matrix of a directed graph is totally unimodular, so for an integer value $k$ the linear program has an integral optimal solution ([flow integrality](/flow-integrality-theorem/)), and $\bar F(k) = F(k)$. So $F$ restricted to the integers is convex: $F(k + 1) - F(k) \ge F(k) - F(k - 1)$, which is $d_{k+1} \ge d_k$.

If $d_{k+1} \ge 0$, then $F(j + 1) - F(j) = d_{j+1} \ge 0$ for every $j \ge k$, so $F(j) \ge F(k)$ for all $j \ge k$. For $j < k$, $F(k) - F(j) = d_{j+1} + \ldots + d_k < 0$, because every path that was augmented had negative cost. If no path exists, no flow of value $k + 1$ exists, and by the same argument for $j < k$ the minimum is at $k$. $\square$

Together, the three claims give the result: the method stops after at most $n + 1$ searches, since each track uses at least one detection, and the flow decomposition of line L7 returns a track set of least cost over all track sets.
