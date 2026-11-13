---
title: Each call of COMPUTE-SHORTEST-PATH gives the robot its distance to the goal on the current map, and the robot reaches the goal when it can be reached
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The map is a finite directed graph with no self-loops and edge costs that are positive or $\infty$. The heuristic satisfies $h(a, b) \ge 0$, $h(a, b) \le \mathrm{dist}(a, b)$, and $h(a, c) \le h(a, b) + h(b, c)$ for all vertices, where $\mathrm{dist}$ is the distance on every version of the map. Write $\mathrm{dist}(s)$ for the distance from $s$ to $s_{goal}$ on the current map. Keys are pairs compared in lexicographic order.

The proof reduces one call to a call of [Lifelong planning A*](/lifelong-planning-a-star/) and uses the correctness proof of that page, which we call the LPA* proof.

**Fact 1 (the reversed problem).** Reverse every edge of the map: the edge $(u, v)$ of cost $c(u, v)$ becomes $(v, u)$ of the same cost. In the reversed graph, the start distance from $s_{goal}$ of a vertex $s$ is $\mathrm{dist}(s)$. During a call, fix the robot position $s_{start}$ and the value $k_m$, and let $h'(s) = h(s_{start}, s) + k_m$. Then the rhs-values of D* Lite (line L6) are the rhs-values of LPA* on the reversed graph with start $s_{goal}$, and $h' - k_m$ is a consistent heuristic there for the LPA* goal $s_{start}$.

*Proof.* The predecessors of $u$ in the reversed graph are its successors in the map, which is what line L6 uses. For consistency, $h(s_{start}, s_{start}) \le \mathrm{dist}(s_{start}, s_{start}) = 0$, and for a reversed edge $(v, u)$ of cost $c(u, v)$, the triangle inequality and $h \le \mathrm{dist}$ give
$$ h(s_{start}, v) \le h(s_{start}, u) + h(u, v) \le h(s_{start}, u) + c(u, v) . $$
Adding the constant $k_m$ to every first component of every key changes no comparison between keys. $\square$

So in a call, the *true key* of a vertex, CALCULATE-KEY of line L1 with the current $s_{start}$ and $k_m$, orders the vertices exactly as the LPA* key with the heuristic $h(s_{start}, \cdot)$.

**Fact 2 (stored keys are lower bounds).** Every key computed by line L1 uses the current values of $s_{start}$ and $k_m$. At any time, the key stored for a vertex in $U$ is at most its true key, and equal to it when it was computed in the current call or after the last change of $k_m$.

*Proof.* Keys are computed only in lines L8, L9 and L11, inside UPDATE-VERTEX and COMPUTE-SHORTEST-PATH, and these run only after line L27 set $s_{last} = s_{start}$, or before the robot first moves. Let $s^0, s^1, \ldots$ be the successive values of $s_{last}$. After the $j$-th update, $k_m = \sum_{l=1}^{j} h(s^{l-1}, s^l)$. A key stored when $s_{last} = s^i$ is $[x + h(s^i, s) + k_m^{(i)}; x]$, where $x = \min(g(s), \mathrm{rhs}(s))$ did not change since, because a change of $g$ or rhs recomputes the key. Its true key at the time of $s^j$ is $[x + h(s^j, s) + k_m^{(j)}; x]$. By the triangle inequality, applied $j - i$ times,
$$ h(s^i, s) \le h(s^i, s^j) + h(s^j, s) \le \sum_{l=i+1}^{j} h(s^{l-1}, s^l) + h(s^j, s) = k_m^{(j)} - k_m^{(i)} + h(s^j, s) . $$
So the stored first component is at most the true one, and the second components are equal. $\square$

**Fact 3 (the invariants of LPA*).** At line L9, $\mathrm{rhs}(s_{goal}) = 0$, every other rhs-value is the minimum of line L6, and $U$ holds exactly the vertices with $g \ne \mathrm{rhs}$.

*Proof.* As in Fact 1 of the LPA* proof, with predecessors and successors exchanged: a change of $c(u, v)$ changes only $\mathrm{rhs}(u)$, which line L30 recomputes, and a change of $g(u)$ at line L13 or line L16 changes only the rhs-values of the predecessors of $u$ and the consistency of $u$, which lines L14 and L17 update. Line L11 changes no value. The robot moves at line L22 change no $g$ or rhs. $\square$

**Lemma 4 (a call is an LPA* call with extra steps).** Consider one call. Each pass of the loop either is a *reinsertion* at line L11, which changes no $g$ or rhs and makes the stored key of $u$ equal to its true key, or it expands a vertex $u$ whose true key is the least true key in $U$. There are at most $n$ reinsertions in a call.

*Proof.* Let line L10 remove $u$ with the stored key $k_{old}$, the least stored key. By Fact 2, $k_{old}$ is at most the true key of $u$. If it is smaller, line L11 puts $u$ back with its true key. If it is equal, every other vertex $s$ in $U$ has true key $\ge$ stored key $\ge k_{old}$, so $u$ has the least true key. A vertex whose key is set in the call gets its true key by Fact 2, and it keeps a true stored key for the rest of the call, so each vertex is reinserted at most once. $\square$

So the expansions of a call are exactly the expansions of an LPA* call on the reversed graph, with the heuristic $h(s_{start}, \cdot)$ and some rule for ties between equal keys. The proof for LPA* allows any rule for ties: it only uses that the removed vertex has a least key. Its Lemma 2 and its Theorem 5 then give at most two expansions of each vertex, and so at most $2n$ expansions and $n$ reinsertions per call.

**Lemma 5 (the stop rule).** When the loop of line L9 stops, $s_{start}$ is consistent and no vertex in $U$ has a true key less than the true key of $s_{start}$.

*Proof.* The loop stops when the least stored key is not less than the key of $s_{start}$, which was computed in this call or is its true key by Fact 2. The true keys are at least the stored keys. $\square$

This is the stop condition used in Theorems 6 and 7 of the LPA* proof. So:

**Theorem 6 (one call).** When a call returns, $g(s_{start}) = \mathrm{dist}(s_{start})$. If it is finite, the walk that starts at $s_{start}$ and always goes to a successor $s'$ that minimizes $c(s, s') + g(s')$ reaches $s_{goal}$, and each vertex $s$ on it is consistent with $g(s) = \mathrm{dist}(s)$, so the walk is a shortest path of the map.

*Proof.* Theorems 6 and 7 of the LPA* proof for the reversed graph. The trace there goes from the LPA* goal $s_{start}$ to predecessors in the reversed graph, which are successors in the map. $\square$

**Theorem 7 (the robot).** Assume that the true costs do not change, that the first map has each edge at a cost at most its true cost, that the robot learns the true cost of each edge out of its position before it leaves the position, and that a sensed cost replaces the map cost. Then MAIN stops. Each move uses an edge of finite true cost. If MAIN reports that there is no known path, the goal cannot be reached from the position of the robot in the true graph. If the goal can be reached in the true graph from every vertex that can be reached from $s_{start}$, for example when the true graph is undirected and the goal can be reached from $s_{start}$, the robot reaches the goal.

*Proof.* The map costs are always at most the true costs, so $\mathrm{dist}$ on the map is at most the true distance. Each edge changes its map cost at most once, when it is first sensed, so line L25 finds changes only finitely often.

Between two calls the map does not change. After a call, Theorem 6 shows that the next vertex $s'$ chosen at line L22 is on a shortest path of the map, with $g(s') = g(s_{start}) - c(s_{start}, s')$, and that $s'$ is consistent with $g(s') = \mathrm{dist}(s')$. So while no change is seen, each move lowers $g(s_{start})$ by a positive cost, the conditions of Theorem 6 still hold at the new position, and the robot reaches $s_{goal}$ after finitely many moves or sees a change. After the last change, it reaches $s_{goal}$ or stops at line L21.

The edge used by each move has a finite map cost, and its true cost was sensed before the move, so its true cost is finite. Line L21 stops only when $g(s_{start}) = \mathrm{dist}(s_{start}) = \infty$ on the map, and then the true distance is $\infty$ too. Under the last assumption, each position of the robot can be reached from the first one along edges of finite true cost, so the goal can be reached from it, and $\mathrm{dist}(s_{start})$ on the map is finite. So line L21 never stops the robot, and it reaches the goal. $\square$
