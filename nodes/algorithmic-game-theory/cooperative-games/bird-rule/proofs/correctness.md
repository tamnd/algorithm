---
title: Bird's rule charges the cost of a minimum spanning tree and gives a core allocation
proves: [correctness]
status: full
---

**Setting.** The vertex set is $V = N \cup \{0\}$ with $N = \{1, \ldots, n\}$. The cost $c(u, v) = c(v, u)$ is given for every pair of distinct vertices. For a coalition $S \subseteq N$, the cost $c(S)$ is the cost of a minimum spanning tree of the complete graph on $S \cup \{0\}$, with $c(\emptyset) = 0$. An allocation $x \in \mathbb{R}^N$ is in the core of the cost game if $x(N) = c(N)$ and $x(S) \le c(S)$ for every $S \subseteq N$, where $x(S) = \sum_{i \in S} x_i$.

**The output.** Lines L1 to L6 are Prim's algorithm from the source 0 on the complete graph on $V$. Line L4 adds the vertex $v$ outside the tree with the smallest $d[v]$, and $d[v] = c(p[v], v)$ is the cheapest edge from the tree to $v$, by the updates of line L6. So each player $v$ enters the tree by the edge $e_v = (p[v], v)$, and line L5 sets $x_v = c(e_v)$. Let $T$ be the tree with the edges $e_1, \ldots, e_n$. Every vertex other than 0 has exactly one parent edge, and a parent enters the tree before its child, so $T$ is a spanning tree of $V$ rooted at 0. Prim's algorithm returns a minimum spanning tree (see [Prim's algorithm](/prim/)), so $T$ is a minimum spanning tree and

$$x(N) = \sum_{v \in N} c(e_v) = c(T) = c(N).$$

The rest of the proof uses only the fact that $T$ is a minimum spanning tree of the complete graph on $V$. So the result holds for every minimum spanning tree, also when ties make it not unique.

**Lemma 1 (cycle property).** Let $a, b \in V$ be distinct, and let $f$ be an edge on the path from $a$ to $b$ in $T$. Then $c(f) \le c(a, b)$.

*Proof.* If $(a, b)$ is an edge of $T$, the path is this edge and the claim holds. Otherwise remove $f$ from $T$. This splits $T$ into two components, one with $a$ and one with $b$, because $f$ is on the only path between them. Adding the edge $(a, b)$ joins them again, so $T - f + (a, b)$ is a spanning tree. Its cost is $c(T) - c(f) + c(a, b)$, and it is at least $c(T)$ because $T$ is a minimum spanning tree. So $c(f) \le c(a, b)$. $\square$

**Lemma 2.** Let $S \subseteq N$ be nonempty, and let $T_S$ be a minimum spanning tree on $S \cup \{0\}$. Let $W \subseteq S$. Call an edge $(a, b)$ of $T_S$ a *witness* for the player $v$ if $e_v$ is on the path from $a$ to $b$ in $T$. Then at least $|W|$ edges of $T_S$ are witnesses for some player of $W$.

*Proof.* Remove the $|W|$ edges $e_v$, $v \in W$, from $T$. A tree with $|W|$ edges removed has $|W| + 1$ components. Each component contains a vertex of $S \cup \{0\}$. The component of 0 contains 0. Any other component $K$ does not contain the root, so its vertex $v$ that is nearest to 0 in $T$ has its parent edge $e_v$ removed; therefore $v \in W \subseteq S$.

So the components split $S \cup \{0\}$ into $|W| + 1$ nonempty classes. The tree $T_S$ connects all vertices of $S \cup \{0\}$. If we contract each class to one point, the edges of $T_S$ still connect the $|W| + 1$ points, so at least $|W|$ edges of $T_S$ join two different classes. Let $(a, b)$ be such an edge. Then $a$ and $b$ are in different components of $T$ without the edges $e_v$, $v \in W$, so the path from $a$ to $b$ in $T$ contains a removed edge $e_v$ with $v \in W$. So $(a, b)$ is a witness for $v$. $\square$

**Theorem.** For every $S \subseteq N$, $x(S) \le c(S)$. Together with $x(N) = c(N)$, the allocation $x$ is in the core.

*Proof.* For $S = \emptyset$ both sides are 0. Let $S$ be nonempty, and let $T_S$ be a minimum spanning tree on $S \cup \{0\}$, so $c(T_S) = c(S)$ and $T_S$ has $|S|$ edges. Build the bipartite graph with the players of $S$ on one side and the edges of $T_S$ on the other side, and join $v$ to each edge of $T_S$ that is a witness for $v$. By Lemma 2, every set $W \subseteq S$ has at least $|W|$ neighbours. By [Hall's theorem](/hall-theorem/), there is a matching that covers $S$. As both sides have $|S|$ elements, the matching is a bijection $\varphi$ from $S$ to the edges of $T_S$.

The edge $\varphi(v) = (a, b)$ is a witness for $v$, so $e_v$ is on the path from $a$ to $b$ in $T$. By Lemma 1, $x_v = c(e_v) \le c(a, b) = c(\varphi(v))$. Sum over $v \in S$:

$$x(S) = \sum_{v \in S} x_v \le \sum_{v \in S} c(\varphi(v)) = c(T_S) = c(S).$$

$\square$

**Cost.** Line L1 takes $O(n)$ time. The loop of line L3 runs $n$ times, and lines L4 and L6 scan $n$ vertices each, so the time is $O(n^2)$. The arrays $d$, $p$, $x$ and the tree flags take $O(n)$ extra space.

**Remark.** The tests in `impl/python/test_bird_rule.py` check the sum against Kruskal's algorithm with a union-find, check that the parent edges form a spanning tree, and check $x(S) \le c(S)$ for all coalitions of 600 random games with at most 6 players, with integer costs (many ties) and with fractional costs. $\blacksquare$
