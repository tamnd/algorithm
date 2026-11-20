---
title: Successive shortest paths on the marginal costs minimize Rosenthal's potential, and the minimizer is a pure Nash equilibrium
proves: [correctness]
status: full
---

The input is a directed graph $G = (V, E)$ with $v = |V|$ and $m = |E|$, two vertices $s \ne t$, a number of players $n \ge 1$, and for each edge $e$ the costs $c_e(1), \ldots, c_e(n)$, which are nonnegative and nondecreasing. All players have the same strategy set, the simple directed $s$-$t$ paths. In a profile $P = (P_1, \ldots, P_n)$ the load of $e$ is $x_e(P) = |\{i : e \in P_i\}|$, player $i$ pays $c_i(P) = \sum_{e \in P_i} c_e(x_e(P))$, and Rosenthal's potential is

$$\Phi(x) = \sum_{e \in E} \sum_{j=1}^{x_e} c_e(j).$$

The same formula defines $\Phi(x)$ for any integral vector $x$ with $0 \le x_e \le n$. We write $\Phi(P)$ for $\Phi(x(P))$. A flow of value $k$ is an integral vector $x$ with $0 \le x_e \le n$ such that the net outflow is $k$ at $s$, $-k$ at $t$ and 0 at every other vertex.

## Step 1. The potential is a min-cost flow cost

Build the expanded network $H$. Replace each edge $e = (u, v)$ by $n$ parallel arcs $e^1, \ldots, e^n$ from $u$ to $v$, each with capacity 1, where $e^j$ has cost $c_e(j)$. An integral flow $y$ in $H$ maps to the flow $x$ in $G$ with $x_e = \sum_j y(e^j)$, and every flow of $G$ is the image of some $y$. Among the $y$ that map to a given $x$, the cost $\sum_{e, j} c_e(j)\, y(e^j)$ is a sum of $x_e$ distinct values from the list $c_e(1) \le \cdots \le c_e(n)$ for each $e$, so it is at least $\sum_{j \le x_e} c_e(j)$, with equality for the prefix flow that uses $e^1, \ldots, e^{x_e}$. So the least cost of an integral flow of value $k$ in $H$ equals $\min \Phi(x)$ over the flows $x$ of value $k$ in $G$, and a prefix flow of least cost gives a minimizer.

## Step 2. Lines L1 to L4 run successive shortest paths on $H$

Let the residual graph $R(x)$ of the code be as in line L3: for each edge $e = (u, v)$ it has the arc $u \to v$ of cost $c_e(x_e + 1)$ if $x_e < n$, and the arc $v \to u$ of cost $-c_e(x_e)$ if $x_e > 0$. Let $y$ be the prefix flow of $x$. In the residual graph $H_y$ of $H$, the forward arcs of $e$ are the unused copies $e^{x_e+1}, \ldots, e^n$, and the cheapest of them costs $c_e(x_e + 1)$; the backward arcs are the reverses of $e^1, \ldots, e^{x_e}$, of costs $-c_e(j)$, and the cheapest costs $-c_e(x_e)$. So $R(x)$ is $H_y$ with only the cheapest copy kept between each ordered pair of endpoints for each edge.

A simple path in $H_y$ uses at most one arc out of each vertex. Replacing each arc by the cheapest copy of the same edge and direction does not increase its length and gives a path of $R(x)$. Conversely, each arc of $R(x)$ is an arc of $H_y$. So the shortest $s$-$t$ distance is the same in both graphs, and a shortest path $Q$ of $R(x)$ is a shortest path of $H_y$. The same map sends a cycle of $R(x)$ to a cycle of $H_y$ of equal cost, because the arc $u \to v$ of $e$ and the arc $v \to u$ of $e$ come from the distinct copies $e^{x_e+1}$ and $e^{x_e}$. Pushing one unit along $Q$ in $H$ uses the copy $e^{x_e+1}$ on a forward arc and frees the copy $e^{x_e}$ on a backward arc, so the new flow is again a prefix flow, and it is the prefix flow of the vector that line L4 computes.

Now use the successive shortest path theorem (Ahuja, Magnanti and Orlin, Chapter 9): if a flow has no negative cycle in its residual graph, then pushing flow along a shortest $s$-$t$ path, by at most its bottleneck, gives a flow of least cost for its new value, and its residual graph again has no negative cycle. At the start, $y = 0$ and every arc of $H$ has cost $c_e(j) \ge 0$, so there is no negative cycle. Each residual capacity in $H$ is 1, so one unit is within the bottleneck. By induction, after $k$ rounds of line L2 the prefix flow has least cost among the integral flows of value $k$ in $H$, so by Step 1 the vector $x$ minimizes $\Phi$ over the flows of value $k$ in $G$.

Two details remain. First, $R(x)$ has no negative cycle, because $H_y$ has none and cycles map to cycles of equal cost. So Bellman-Ford with $v - 1$ rounds of relaxation finds exact distances, and because it updates a label only on a strict decrease, the predecessor pointers form a tree rooted at $s$ (Cormen, Leiserson, Rivest and Stein, Section 24.5, the predecessor-subgraph property), so line L3 reads off a simple path. Second, if $t$ is not reachable from $s$ in $R(x)$, then no flow of value $k + 1$ exists in $H$, and since every $s$-$t$ path of $G$ is a flow of value $n$, there is no strategy at all. The code raises an error in that case, which can only happen in round 1.

After $n$ rounds, $x$ is a flow of value $n$ with $\Phi(x) \le \Phi(z)$ for every flow $z$ of value $n$.

## Step 3. Lines L5 to L9 split the flow into simple paths

Claim: at the start of round $k$ of line L5 the current vector $x$ is a flow of value $n - k + 1$, and round $k$ ends with a simple $s$-$t$ path $P_k$ such that every edge of $P_k$ had $x_e \ge 1$.

Inside a round the code keeps a simple walk $W$ from $s$ to the current vertex $w$ whose edges all have $x_e \ge 1$. If $w \ne t$, some edge out of $w$ has $x_e \ge 1$. For $w = s$ this holds because the net outflow of $s$ is $n - k + 1 \ge 1$. For $w \ne s, t$ the last edge of $W$ enters $w$ with $x_e \ge 1$, so the inflow of $w$ is positive, and by conservation so is its outflow. Take such an edge $e = (w, u)$. If $u$ is not on $W$, line L6 extends $W$ and it stays simple. If $u$ is on $W$, the part of $W$ from $u$ to $w$ together with $e$ is a simple cycle whose edges all have $x_e \ge 1$, and line L7 lowers $x$ by 1 on it and cuts it from $W$. Lowering a flow by 1 on a cycle keeps every net outflow, so $x$ stays a flow of the same value. Each extension makes $W$ longer, and $W$ has at most $v - 1$ edges; each cut lowers $\sum_e x_e$ by at least 1. So the pair ($\sum_e x_e$, $v - |W|$) decreases in lexicographic order at each step, and the round ends, at $w = t$, with a simple $s$-$t$ path. Line L8 lowers $x$ by 1 on it, which gives a flow of value $n - k$. This proves the claim.

The pointer in the code only skips edges with $x_e = 0$. No step of the split raises any $x_e$, so a skipped edge is never needed again.

## Step 4. The output minimizes the potential

Let $x^*$ be the vector after line L4 and let $x'$ be the load vector of the output $(P_1, \ldots, P_n)$. Line L8 removes exactly one unit per path, and line L7 removes extra units on cycles, so $x' \le x^*$ coordinatewise. Each $c_e(j) \ge 0$, so $\Phi(x') \le \Phi(x^*)$. Also $x'$ is a flow of value $n$: it is a sum of $n$ unit $s$-$t$ paths, and each load is at most $n$. By Step 2, $\Phi(x^*) \le \Phi(x')$. So $\Phi(x') = \Phi(x^*)$.

Every profile $P$ of simple $s$-$t$ paths has a load vector $x(P)$ that is a flow of value $n$. So $\Phi(P_1, \ldots, P_n) = \Phi(x^*) \le \Phi(x(P)) = \Phi(P)$ for every profile $P$: the output minimizes Rosenthal's potential over all profiles.

## Step 5. A minimizer of the potential is a pure Nash equilibrium

Let $P$ be a profile, let player $i$ change from $P_i$ to another simple $s$-$t$ path $Q$, and let $P' = (Q, P_{-i})$. Only the edges in exactly one of $P_i$ and $Q$ change load. An edge $e \in Q \setminus P_i$ goes from load $x_e$ to $x_e + 1$, which adds $c_e(x_e + 1)$ to $\Phi$ and is also the cost that player $i$ pays on it in $P'$. An edge $e \in P_i \setminus Q$ goes from $x_e$ to $x_e - 1$, which removes $c_e(x_e)$ from $\Phi$, the cost that player $i$ paid on it in $P$. Edges in both paths keep their load and their cost to player $i$. So

$$\Phi(P') - \Phi(P) = c_i(P') - c_i(P).$$

If $P$ minimizes $\Phi$, the left side is at least 0 for every $i$ and $Q$, so no player gains by a unilateral change. This is [Rosenthal's theorem](/rosenthal-potential-theorem/). Hence $(P_1, \ldots, P_n)$ is a pure Nash equilibrium. $\blacksquare$

References: R. K. Ahuja, T. L. Magnanti and J. B. Orlin, Network Flows: Theory, Algorithms, and Applications, Prentice Hall, 1993, Chapter 9 (successive shortest paths) and Chapter 14 (convex cost flows). T. H. Cormen, C. E. Leiserson, R. L. Rivest and C. Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009, Sections 24.1 and 24.5. A. Fabrikant, C. Papadimitriou and K. Talwar, The complexity of pure Nash equilibria, STOC 2004, 604-612, the polynomial algorithm for the symmetric network case. R. W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67.
