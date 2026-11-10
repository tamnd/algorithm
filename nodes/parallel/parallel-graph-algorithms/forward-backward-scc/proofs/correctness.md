---
title: Forward-backward SCC outputs the strongly connected components, and each level costs linear work
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V_0, A)$ is a directed graph with $n$ vertices and $m$ arcs. For $X \subseteq V_0$, $G[X]$ is the subgraph induced by $X$. "$u$ reaches $v$ in $X$" means there is a directed path from $u$ to $v$ with all its vertices in $X$. An SCC of $G$ is a class of the relation "$u$ reaches $v$ and $v$ reaches $u$" in $V_0$.

**Lemma 1 (paths inside an SCC).** If $u$ and $v$ are in the same SCC $C$ of $G$, every vertex on every path from $u$ to $v$ is in $C$.

*Proof.* Let $x$ be on such a path. Then $u$ reaches $x$, and $x$ reaches $v$, which reaches $u$. So $x$ and $u$ reach each other, and $x \in C$. $\square$

**Lemma 2 (closed parts).** Call $X$ closed if it is a union of SCCs of $G$. If $X$ is closed, the SCCs of $G[X]$ are exactly the SCCs of $G$ contained in $X$.

*Proof.* Let $C \subseteq X$ be an SCC of $G$ and $u, v \in C$. A path from $u$ to $v$ in $G$ stays in $C \subseteq X$ by Lemma 1, so $u$ and $v$ reach each other in $X$. Conversely, if $u, v \in X$ reach each other in $X$, they reach each other in $G$ and are in the same SCC of $G$. $\square$

**Lemma 3 (trimming).** Let $X$ be closed and let $v \in X$ have no arc from $X \setminus \{v\}$ into $v$, or no arc from $v$ into $X \setminus \{v\}$. Then $\{v\}$ is an SCC of $G$, and $X \setminus \{v\}$ is closed.

*Proof.* Say $v$ has no in-arc from $X \setminus \{v\}$. If $u \ne v$ were in the SCC of $v$, then $u \in X$ since $X$ is closed, and by Lemma 2 there would be a path from $u$ to $v$ inside $X$; its last arc enters $v$ from $X \setminus \{v\}$, a contradiction. The case of no out-arc is symmetric. Removing one whole SCC from a union of SCCs leaves a union of SCCs. $\square$

**Lemma 4 (the four sets).** Let $X$ be closed, $p \in X$, $F$ the set of vertices that $p$ reaches in $X$, and $B$ the set of vertices that reach $p$ in $X$. Then $F \cap B$ is the SCC of $p$, and for every SCC $C \subseteq X$: if $C \cap F \ne \emptyset$ then $C \subseteq F$, and if $C \cap B \ne \emptyset$ then $C \subseteq B$. So $F \setminus B$, $B \setminus F$ and $X \setminus (F \cup B)$ are closed.

*Proof.* By Lemma 2, reachability inside $X$ between vertices of one SCC of $G$ in $X$ holds in both directions. $v \in F \cap B$ means that $p$ and $v$ reach each other in $X$, which by Lemma 2 means that $v$ is in the SCC of $p$. Let $x \in C \cap F$ and $y \in C$. Then $p$ reaches $x$ in $X$, and $x$ reaches $y$ in $C \subseteq X$ by Lemma 2, so $p$ reaches $y$ in $X$, and $y \in F$. The case of $B$ is symmetric. So each SCC in $X$ is inside $F$ or disjoint from it, and inside $B$ or disjoint from it, and the three sets are unions of SCCs. $\square$

**Theorem 1 (correctness and termination).** FW-BW$(V_0)$ outputs every SCC of $G$ exactly once, and stops.

*Proof.* By induction on $|X|$, show: for a closed $X$, FW-BW$(X)$ stops and outputs exactly the SCCs of $G$ contained in $X$, each once. If $X$ is empty, nothing is output. Otherwise, by Lemma 3 applied once per removed vertex, line L1 outputs only true SCCs and leaves a closed set $X'$; it removes at least one vertex per round, so it stops. If $X' = \emptyset$, all SCCs of $X$ were output. Otherwise line L6 outputs the SCC of $p$, by Lemma 4. The SCCs of $X'$ other than this one are each in exactly one of the three closed sets of line L7, which are smaller than $X$ because they miss $p$. By induction, the three calls output exactly those SCCs, each once. $\blacksquare$

**Theorem 2 (work per level).** Run the recursion level by level, where level $j$ holds all calls at recursion depth $j$. The calls of one level have pairwise disjoint parts, and a level costs $O(n + m)$ work. So the total work is $O((n + m) d)$, where $d$ is the number of levels.

*Proof.* The three parts made by one call are disjoint and inside its part, and the parts of the first level form one set; by induction, the parts of each level are disjoint. In one call with part $X$, trimming computes the in-degree and the out-degree inside $X$ by scanning the arcs at $X$, and each removal decrements the counts along the arcs of the removed vertex once. The two searches scan each arc at a vertex of $F$ or $B$ once, and the split looks at each vertex of $X$ once. So the call costs $O(|X| + a(X))$, where $a(X)$ is the number of arcs with an end in $X$. Every arc has at most two ends, so over disjoint parts this adds up to $O(n + m)$. $\blacksquare$

**Theorem 3 (span per level).** A level has span $O((t + r) \log n)$, where $t$ is the largest number of trimming rounds and $r$ the largest number of BFS rounds of a call in the level. Since $t + r \le 2n$, $S = O(n\, d \log n)$.

*Proof.* The calls of a level run in parallel. A trimming round and a BFS round each consist of independent updates over the current set and a pack of the next set, which takes $O(\log n)$ span. A BFS round adds at least one vertex of the part, and a trimming round removes at least one, so each happens at most $n$ times in a call. $\blacksquare$
