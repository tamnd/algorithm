---
title: The loops of repeated strongly connected components form a forest that breaks every cycle, and on a reducible graph they are the natural loops
proves: [correctness, termination]
status: full
---

**Setting.** A flow graph is $G = (V, E, r)$ with a root $r \in V$. Let $V_r$ be the set of vertices that $r$ reaches, and keep only the edges whose source is in $V_r$; their targets are then in $V_r$ too. All paths, cycles and predecessors below are in this graph. A path may have length 0. For $R \subseteq V_r$, $G[R]$ is the subgraph induced by $R$. A strongly connected component $S$ of $G[R]$ is *nontrivial* if $|S| > 1$ or $S = \{v\}$ with a self-loop $(v, v)$. Note that a set is nontrivial exactly when it holds a cycle.

**Definition.** The forest is built by $\mathrm{SPLIT}(V_r, \bot)$, where $\mathrm{SPLIT}(R, p)$ does this for each nontrivial strongly connected component $S$ of $G[R]$: it makes $S$ a loop with parent $p$ and header set
$$H(S) = \{v \in S : v = r \text{ or some predecessor of } v \text{ lies outside } S\},$$
and then calls $\mathrm{SPLIT}(S \setminus H(S), S)$. Lines L1 to L9 of the code do exactly this, with a stack of pending regions in place of the recursion. The regions are handled one at a time and the result for one region does not depend on the others, so the order of the stack does not matter. The components come from Tarjan's algorithm, which is cited, not proved here; the tests check them against mutual reachability.

**Lemma 1 (termination and size).** Every loop $S$ has $H(S) \neq \emptyset$. So every call works on a smaller region than its parent call, the recursion stops, and the depth of the forest is at most $|V_r|$. Each vertex is a header of at most one loop, so there are at most $|V_r|$ loops.

*Proof.* If $r \in S$ then $r \in H(S)$. Otherwise take $v \in S$ and a path from $r$ to $v$. It starts outside $S$ and ends in $S$, so it has an edge $(u, w)$ with $u \notin S$ and $w \in S$, and $w \in H(S)$. So $|S \setminus H(S)| < |S| \le |R|$. A header $h$ of $S$ is not in $S \setminus H(S)$, so no loop below $S$ contains it, and loops made in the same call are disjoint, as components are. $\square$

**Lemma 2 (laminar family).** Any two loops are disjoint or one contains the other. The loops that contain a loop $L$ are exactly $L$ and its ancestors, so the parent of $L$ is the smallest loop that strictly contains it. A child of $L$ lies in $L \setminus H(L)$.

*Proof.* By the definition, every loop below $S$ lies in $S \setminus H(S)$. Take two loops $A \ne B$. If one is an ancestor of the other, it contains the other. Otherwise take the deepest call that lies on both of their paths from the top call. $A$ lies in (or is) one component of that call and $B$ in another, so they are disjoint. Now let $L' \supseteq L$ with $L' \ne L$. $L'$ is not disjoint from $L$, so it is an ancestor or a descendant of $L$, and a descendant lies in $L \setminus H(L)$, which is strictly smaller than $L$. So $L'$ is an ancestor. $\square$

**Theorem 1 (the forest breaks every cycle).** Let $C$ be the set of edges $(u, h)$ such that $u \in L$ and $h \in H(L)$ for some loop $L$. Then the graph $(V_r, E \setminus C)$ has no cycle. Each loop also holds a cycle through each of its headers, so every loop is used.

*Proof.* We show, by induction on $|R|$, that for every region $R$ on which $\mathrm{SPLIT}$ is called, $G[R]$ without the edges of $C$ has no cycle. With $R = V_r$ this is the theorem. Let $Z$ be a cycle in $G[R] \setminus C$. Its vertices reach each other inside $R$, so they lie in one component $S$ of $G[R]$, and $S$ is nontrivial because it holds a cycle. So $S$ is a loop. If $Z$ passes a header $h \in H(S)$, the edge of $Z$ into $h$ comes from a vertex of $Z \subseteq S$, so it is in $C$, which is false. So $Z$ lies in $S \setminus H(S)$, and $\mathrm{SPLIT}$ is called on this smaller region, where by induction no such cycle exists. For the last claim: $S$ is strongly connected and nontrivial, so each $h \in S$ lies on a cycle inside $S$. $\square$

**Reducible graphs.** An edge $(u, v)$ is a *back edge* if $v$ dominates $u$; let $B$ be the set of back edges. $G$ is reducible if $(V_r, E \setminus B)$ has no cycle. A self-loop is a back edge. The natural loop of a back edge $(u, h)$ is $N(u, h) = \{h\} \cup \{w : \text{some path from } w \text{ to } u \text{ avoids } h\}$.

**Lemma 3 (the top loops of a reducible graph).** Let $G$ be reducible and let $S$ be a nontrivial component of $G[V_r]$. Let $h$ be the first vertex of $S$ in a topological order of $(V_r, E \setminus B)$. Then:

(a) every edge $(u, h)$ with $u \in S$ is a back edge;
(b) $h$ dominates every vertex of $S$;
(c) $H(S) = \{h\}$;
(d) every back edge $(u, h)$ has $u \in S$, and $S$ is the union of $N(u, h)$ over these back edges.

*Proof.* (a) If $(u, h)$ were not a back edge, $u$ would come before $h$ in the order, but $h$ is the first vertex of $S$. (A self-loop is a back edge anyway.)

(b) Let $w \in S$, $w \ne h$, and suppose a path $P$ from $r$ to $w$ avoids $h$. Take a path $Q$ from $w$ to $h$ inside $S$ and let $u$ be the vertex just before the first $h$ on $Q$. Then $u \in S$, and $P$ followed by the part of $Q$ up to $u$ is a path from $r$ to $u$ that avoids $h$. But $(u, h)$ is a back edge by (a), so $h$ dominates $u$, which is false.

(c) First, $H(S)$ is not empty by Lemma 1. Let $x \in H(S)$. If $x = r$, then $r$ dominates $h$ and $h$ dominates $r$ by (b), so $x = r = h$. Otherwise $x$ has a predecessor $y \notin S$. Suppose $x \ne h$. A path from $r$ to $y$, followed by the edge $(y, x)$, passes $h$ by (b), and $h \ne x$, so $h$ lies on the part up to $y$. Then $h$ reaches $y$, $y$ reaches $x$, and $x$ reaches $h$ inside $S$, so $y \in S$, which is false. So $x = h$.

(d) Let $(u, h)$ be a back edge. Every path from $r$ to $u$ passes $h$, so $h$ reaches $u$, and $u$ reaches $h$ by the edge, so $u \in S$. Let $w \in N(u, h)$ with $w \ne h$, and let $P$ be a path from $w$ to $u$ that avoids $h$. If a path from $r$ to $w$ avoided $h$, then with $P$ it would give a path from $r$ to $u$ that avoids $h$; so $h$ dominates $w$, $h$ reaches $w$, and $w$ reaches $h$ through $u$. So $w \in S$. Conversely, let $w \in S$, $w \ne h$, take a path from $w$ to $h$ inside $S$, and let $u$ be the vertex just before its first $h$. Then $(u, h)$ is a back edge by (a), and the path up to $u$ avoids $h$, so $w \in N(u, h)$. $\square$

**Lemma 4 (the graph inside a top loop).** In the setting of Lemma 3, let $G'$ have the vertices $S$, the edges of $G[S]$ except those that end at $h$, and the root $h$. Then:

(a) $h$ reaches every vertex of $S$ in $G'$;
(b) for $a, b \in S$, $a$ dominates $b$ in $G'$ if and only if $a$ dominates $b$ in $G$;
(c) $G'$ is reducible, its back edges are the back edges of $G$ inside $S$ that do not end at $h$, and for such a back edge $(u, y)$ the natural loop in $G'$ equals the natural loop in $G$;
(d) the loops of $G'$ are exactly the loops of $G$ below $S$, with the same header sets.

*Proof.* (a) Let $w \in S$. A path from $r$ to $w$ passes $h$ by Lemma 3(b). Its part after the last $h$ does not return to $h$, and each of its vertices $z$ is reached from $h$ and reaches $w$, which reaches $h$, so $z \in S$. So this part is a path of $G'$.

(b) Suppose $a$ dominates $b$ in $G'$, and let $P$ be a path in $G$ from $r$ to $b$. As in (a), the part of $P$ after its last $h$ is a path of $G'$ from $h$ to $b$, so it passes $a$, and so does $P$. Conversely, suppose $a$ dominates $b$ in $G$, and let $Q$ be a path in $G'$ from $h$ to $b$. If $a = h$, $Q$ passes $a$. Otherwise take a path $P_0$ in $G$ from $r$ to the first $h$ it meets. $P_0$ followed by $Q$ is a path of $G$ to $b$, so it passes $a$. If $a$ were on $P_0$, it would be before $h$, and the part of $P_0$ up to $a$ would reach $a \in S$ without passing $h$, against Lemma 3(b). So $a$ is on $Q$.

(c) By (b), an edge of $G'$ is a back edge of $G'$ exactly when it is a back edge of $G$. By Lemma 3(a), all the removed edges are back edges, so the edges of $G'$ that are not back edges are edges of $(V_r, E \setminus B)$, and they have no cycle. So $G'$ is reducible. Every back edge $(u, y)$ of $G$ with $y \in S$ has $u \in S$, because $y$ dominates $u$ and so reaches it, and $u$ reaches $y$. Now let $y \ne h$. A path of $G'$ is a path of $G$, so the natural loop in $G'$ lies in the one in $G$. Conversely, let $P$ be a path in $G$ from $w$ to $u$ that avoids $y$. Each vertex $z$ of $P$ is dominated by $y$, since a path from $r$ to $z$ that avoids $y$ would, with the rest of $P$, reach $u$ without $y$. So $y$ reaches $z$, and $z$ reaches $y$ through $u$, so $z \in S$. If $P$ passed $h$, then $y$ would dominate $h$, while $h$ dominates $y$ by Lemma 3(b), so $y = h$, which is false. So $P$ is a path of $G'$.

(d) In $G'$ no edge ends at $h$, so $\{h\}$ is a trivial component, and the other components of $G'$ are the components of $G'[S \setminus \{h\}] = G[S \setminus \{h\}]$, the region of the call $\mathrm{SPLIT}(S \setminus H(S), S)$ in $G$. So both build the same loops at their top level. For the headers, let $S_2$ be such a loop and $x \in S_2$. The root of $G'$ is $h \notin S_2$, and the root $r$ of $G$ is not in $S_2$ either, since $r \in S$ would mean $r = h$ by Lemma 3(c). A predecessor $y$ of $x$ in $G$ lies in $S$, since otherwise $x \ne h$ would be in $H(S)$, against Lemma 3(c). So $x$ has the same predecessors in $G$ and in $G'$, and $H(S_2)$ is the same in both. The calls below $S_2$ then see the same regions and the same predecessors, so the whole subtree is the same. $\square$

**Theorem 2 (reducible graphs).** Let $G$ be reducible. Then every loop $L$ of the forest has exactly one header $h$, $h$ dominates every vertex of $L$, and $L$ is the union of the natural loops of all the back edges that end at $h$. The map from a loop to its header is a one-to-one map from the loops onto the targets of the back edges.

*Proof.* By induction on the number of edges. The loops at the top level satisfy the claims by Lemma 3. A loop $L$ below a top loop $S$ is a loop of $G'$ with the same headers (Lemma 4(d)). $G'$ is reducible and has fewer edges, since $S$ holds an edge into $h$ by Lemma 3(a) and the nontriviality of $S$. So by induction $L$ has one header $h_2$, $h_2$ dominates $L$ in $G'$, and $L$ is the union of the natural loops in $G'$ of the back edges of $G'$ into $h_2$. By Lemma 4(b) and (c), the same holds in $G$, and since $h_2 \ne h$, the back edges of $G'$ into $h_2$ are all the back edges of $G$ into $h_2$.

For the map: each loop $L$ with header $h$ holds an edge from $L$ into $h$, which is a back edge (Lemma 3(a), in $G$ or in $G'$), so $h$ is a back edge target. Different loops have different headers by Lemma 1. Let $y$ be the target of a back edge $(u, y)$. Then $u$ and $y$ lie on a cycle, so $y$ is in a top loop $S$. If $y$ is the header of $S$ we are done. Otherwise $(u, y)$ is a back edge of $G'$ by Lemma 4(c), and by induction $y$ is the header of a loop of $G'$, which is a loop of $G$ by Lemma 4(d). $\square$

**Cost.** Let $n = |V|$, $m = |E|$ and let $d$ be the depth of the forest. The regions of the calls at one depth are disjoint, so all the calls at one depth cost $O(n + m)$ for the components, the header sets and the new regions, counting each edge from its source and from its target. There are at most $d + 1$ depths, so the total is $O((d + 1)(n + m))$, which is $O(n (n + m))$ in the worst case by Lemma 1. The Python code also sorts each region and each loop for a fixed output order, which adds $O(n \log n)$ per depth. The bound is reached: the path $0, 1, \ldots, 2k$ with the back edges $(2k - i, i)$ for $i < k$ has $k$ nested loops, and the call at depth $i$ works on about $2k - 2i$ vertices, so the work is $\Theta(k^2)$ for a graph with $\Theta(k)$ edges.

**What is proved and what is measured.** Lemmas 1 to 4 and Theorems 1 and 2 are proved here, given that the component step is correct. The almost-linear algorithms of Ramalingam for other forests are cited, not proved. The tests compare the code with a direct reading of the definition that finds components by mutual reachability, with the merged natural loops of brute-force dominators on reducible graphs, and with the properties of Lemma 2 and Theorem 1. The running times in the tests and on the page are measurements.
