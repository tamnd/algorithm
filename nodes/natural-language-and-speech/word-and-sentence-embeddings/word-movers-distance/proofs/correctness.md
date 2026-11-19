---
title: Successive shortest paths compute WMD exactly, and WCD and RWMD are lower bounds
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The first document has the distinct words $1, \ldots, m$ with the shares $d_i > 0$, and the second has the words $1, \ldots, n$ with the shares $d'_j > 0$. Both lists of shares are rationals that sum to 1. The cost is $c(i, j) = \|x_i - x'_j\|_2 \ge 0$. WMD is the optimum of the linear program

$$\min_{T \ge 0} \sum_{i,j} T_{ij} c(i, j) \quad \text{subject to} \quad \sum_j T_{ij} = d_i, \ \sum_i T_{ij} = d'_j.$$

**Scaling.** Let $L$ be the least common multiple of the denominators of all the shares (line L3), and $a_i = d_i L$, $b_j = d'_j L$. These are positive integers with $\sum a_i = \sum b_j = L$. A matrix $T$ is feasible for the program above if and only if $F = L T$ is feasible for the same program with $a$ and $b$, and the costs differ by the factor $L$. So it is enough to solve the integer program and divide by $L$ (line L9).

**The network.** Build a source $s$, a sink $t$, an arc $s \to i$ of capacity $a_i$ and cost 0, an arc $i \to j$ of infinite capacity and cost $c(i, j)$, and an arc $j \to t$ of capacity $b_j$ and cost 0. A flow of value $L$ from $s$ to $t$ is the same as a feasible $F$. The residual network of a flow $F$ has the arcs $s \to i$ while $i$ still has supply, every arc $i \to j$, an arc $j \to i$ of cost $-c(i, j)$ while $F_{ij} > 0$, and $j \to t$ while $j$ still has demand. This is the network that line L6 searches.

**Lemma 1 (optimality condition).** A flow of a given value has the least cost among the flows of that value if and only if its residual network has no cycle of negative cost. This is the negative cycle optimality condition of minimum cost flow (Ahuja, Magnanti and Orlin 1993, chapter 9).

**Lemma 2 (invariant).** Before each round of line L5, the residual network has no negative cycle.

*Proof.* At the start $F = 0$ and the only arcs with a cost are the arcs $i \to j$, whose costs are at least 0, so no cycle is negative.

Assume the invariant before a round. Then Bellman-Ford finds exact shortest path distances $\pi(v)$ from $s$ to every node $v$ that $s$ reaches, and a shortest path $P$ to $t$. Let $R$ be the set of nodes that $s$ reaches. For every residual arc $u \to v$ with $u \in R$, $v \in R$ and $\pi(v) \le \pi(u) + \text{cost}(u, v)$, so the reduced cost $\text{cost}(u, v) + \pi(u) - \pi(v)$ is at least 0. On $P$ the reduced costs are 0, since $P$ is a shortest path. Line L8 pushes $\delta$ along $P$. This can remove arcs of $P$ and can add the reversal of an arc of $P$, whose reduced cost is $-0 = 0$. All other arcs stay. After the push, no arc leaves $R$: no arc left $R$ before, and the new arcs join two nodes of $P \subseteq R$. So every cycle lies inside $R$ or inside its complement. A cycle inside $R$ has a cost equal to the sum of its reduced costs, because the terms $\pi(u) - \pi(v)$ cancel around a cycle, and that sum is at least 0. A cycle inside the complement uses only arcs that did not change, so it was not negative before and is not negative now. $\square$

**Lemma 3 (a path exists).** While some $a_i$ is not yet sent, line L6 finds a path from $s$ to $t$.

*Proof.* The totals of the remaining supply and the remaining demand are equal, since each round reduces both by $\delta$. So some supply word $i$ and some demand word $j$ still have something left, and $s \to i \to j \to t$ is a residual path, because the arc $i \to j$ has infinite capacity. $\square$

**Theorem 1.** Line L9 returns WMD, and the loop of line L5 ends after at most $L$ rounds.

*Proof.* Every capacity and every flow value is an integer, so the bottleneck $\delta$ of line L7 is a positive integer, and each round sends at least one more unit. The total to send is $L$, so there are at most $L$ rounds (Lemma 3 shows that the loop does not stop early). At the end, the flow has value $L$, so $F$ is feasible. By Lemma 2 its residual network has no negative cycle, so by Lemma 1 it has the least cost of all the flows of value $L$. By the scaling argument, $\sum F_{ij} c(i, j) / L$ is the optimum of the original program. $\square$

**Theorem 2 (WCD is a lower bound).** $\|\sum_i d_i x_i - \sum_j d'_j x'_j\|_2 \le \mathrm{WMD}$.

*Proof.* Let $T$ be optimal. Then $\sum_i d_i x_i = \sum_{i,j} T_{ij} x_i$ and $\sum_j d'_j x'_j = \sum_{i,j} T_{ij} x'_j$, by the two sets of constraints. So the left side is $\|\sum_{i,j} T_{ij}(x_i - x'_j)\| \le \sum_{i,j} T_{ij} \|x_i - x'_j\| = \mathrm{WMD}$, by the triangle inequality and $T \ge 0$. $\square$

**Theorem 3 (RWMD is a lower bound).** Let $\ell_1 = \sum_i d_i \min_j c(i, j)$ and $\ell_2 = \sum_j d'_j \min_i c(i, j)$. Then $\ell_1$ is the optimum of the program without the column constraints, $\ell_2$ is the optimum without the row constraints, and $\max(\ell_1, \ell_2) \le \mathrm{WMD}$.

*Proof.* For any $T \ge 0$ with row sums $d_i$, $\sum_{i,j} T_{ij} c(i, j) \ge \sum_i \sum_j T_{ij} \min_k c(i, k) = \sum_i d_i \min_k c(i, k) = \ell_1$, and moving all of $d_i$ to a nearest word attains it. The case of $\ell_2$ is the same with the roles swapped. Each relaxed program has a larger feasible set than the full one, so its optimum is at most WMD, and so is the larger of the two. $\square$

**Theorem 4 (the assignment case).** If both documents have $n$ distinct words with the share $1/n$ each, then $\mathrm{WMD} = \frac{1}{n} \min_{\sigma} \sum_i c(i, \sigma(i))$ over the permutations $\sigma$ of $\{1, \ldots, n\}$.

*Proof.* The feasible set is $\{T / n : T \text{ doubly stochastic}\}$. By the Birkhoff-von Neumann theorem, the doubly stochastic matrices are the convex hull of the permutation matrices. A linear function on a polytope attains its minimum at a vertex, and the vertex of the permutation $\sigma$ has the cost $\frac{1}{n} \sum_i c(i, \sigma(i))$. $\square$

**Theorem 5 (pruned search is exact).** In the k-nearest search of the code, a skipped document has RWMD at least the current $k$-th smallest WMD, so by Theorem 3 its WMD is at least that value too. The $k$-th smallest value never increases during the search, so a skipped document cannot be closer than the final $k$-th neighbor. Only a document with exactly the same distance as the $k$-th neighbor can be left out, which changes the result only on ties. $\blacksquare$
