---
title: Correctness and properties of ranked pairs
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$, let $P$ be a profile of $n$ full rankings, and let $g(x, y) = n_P(x, y) - n_P(y, x)$ be the margins. Fix the tie-break ranking $t$. Order all ordered pairs $(x, y)$ with $x \ne y$ by the key $(-g(x, y), t(x), t(y))$, where $t(a)$ is the place of $a$ in $t$. This is a strict total order, which we call priority: a pair with a smaller key has higher priority. The list $L$ of line L2 is the set of pairs with $g \ge 0$, in priority order. Write $x \to y$ for a locked pair, and $R$ for the matrix of lines L3 to L6.

**Claim 1 (invariant).** Before and after each pass of the loop of lines L4 to L6, the locked pairs form an acyclic directed graph $G$, and $R[u][v]$ holds exactly when $G$ has a path from $u$ to $v$ (of length 0 when $u = v$).

*Proof.* At the start $G$ has no edges and $R$ is the identity, by line L3. Take a pass for the pair $(x, y)$. If $R[y][x]$, the pair is skipped and nothing changes. Otherwise the edge $x \to y$ is added. The new graph is acyclic: a cycle would use the new edge and a path from $y$ to $x$ in the old graph, but $R[y][x]$ is false. A path in the new graph from $z$ to $w$ either avoids the new edge, or it is a path from $z$ to $x$, then the edge, then a path from $y$ to $w$; a path that uses the edge twice repeats $x$, which is impossible in an acyclic graph. So the new reach set of $z$ is the old one, together with the reach set of $y$ when $z$ reaches $x$. Line L6 adds exactly this for the rows $z$ with $R[z][x]$ and not $R[z][y]$. For a row $z$ with $R[z][x]$ and $R[z][y]$, the reach set of $y$ is already contained in that of $z$, because reach is transitive, so nothing needs to be added. Line L6 reads row $y$ while it changes other rows. Row $y$ itself is not changed in this pass: changing it would need $R[y][x]$, which is false. So all rows get the right set.

**Claim 2 (correctness).** At the end, $R$ is a linear order on $A$, and line L7 lists $A$ in this order, best first.

*Proof.* For $x \ne y$, one of $g(x, y)$ and $g(y, x)$ is at least 0, so one of $(x, y)$ and $(y, x)$ is in $L$, say $(x, y)$. When it is processed, either $R[y][x]$ already holds, or the edge $x \to y$ is locked and $R[x][y]$ holds from then on. Entries of $R$ never go from true to false. So at the end $R[x][y]$ or $R[y][x]$ for every pair. By Claim 1, $R$ is the reach relation of an acyclic graph, so it is reflexive, transitive and antisymmetric. A reflexive, transitive, antisymmetric and total relation is a linear order. In a linear order of $m$ elements, the element in place $k$ from the top is above exactly $m - k$ others, so it reaches $m - k + 1$ candidates, itself included. These counts differ, so sorting by them in line L7 lists the order. Line L8 returns its top.

**Claim 3 (time).** RANKED-PAIRS runs in $O(n m^2 + m^3)$ time and $O(m^2)$ extra space.

*Proof.* Line L1 visits the $m(m - 1)/2$ ordered pairs of each ballot once, in $O(n m^2)$ time. Line L2 sorts at most $m(m - 1)$ pairs in $O(m^2 \log m)$ time. Each pass of the loop does $O(1)$ work in line L5 and scans $m$ rows in line L6, which is $O(m^3)$ over at most $m^2$ passes. A row $z$ gets the inner $O(m)$ loop only when $R[z][y]$ is false before the pass, and the update makes it true. Each of the $m^2$ entries goes from false to true at most once, so the inner loops take $O(m^3)$ time in all. Line L7 counts $m^2$ entries and sorts $m$ numbers. The matrices $g$ and $R$ and the list $L$ have $O(m^2)$ entries.

**Claim 4 (Smith set on top).** Let $S$ be the Smith set, the smallest nonempty set of candidates each of whom beats every candidate outside it. Then the ranking puts every member of $S$ above every candidate outside $S$. In particular, a Condorcet winner, whose Smith set is $\{c\}$, wins.

*Proof.* For $x \in S$ and $y \notin S$, $g(x, y) > 0$, so $g(y, x) < 0$ and $(y, x) \notin L$. So no locked edge goes from outside $S$ into $S$, and no path of $G$ does either: the first edge of such a path that enters $S$ would be such an edge. When $(x, y)$ is processed, $R[y][x]$ is false, since it would need a path from $y \notin S$ to $x \in S$. So $x \to y$ is locked and $x$ is above $y$.

**Claim 5 (Pareto).** If $n \ge 1$ and every voter ranks $a$ above $b$, then $a$ is above $b$ in the ranking.

*Proof.* $g(a, b) = n$, the largest possible margin. Suppose $(a, b)$ is skipped. Then a path $b = u_0 \to u_1 \to \cdots \to u_k = a$ of locked edges exists when it is processed, and every edge of it was processed earlier, so $g(u_{i-1}, u_i) \ge n$, which means $g(u_{i-1}, u_i) = n$: every voter ranks $u_{i-1}$ above $u_i$. By transitivity of each voter's ranking, every voter ranks $b$ above $a$, which contradicts $n \ge 1$. So $(a, b)$ is locked.

**Claim 6 (anonymity, and neutrality with the tie-break).** Reordering the voters does not change the result. For a permutation $\pi$ of $A$, the ranking of $\pi P$ with tie-break $\pi t$ is the image under $\pi$ of the ranking of $P$ with tie-break $t$.

*Proof.* The algorithm reads $P$ only through $g$, which does not depend on the order of the voters. In $\pi P$, $g'(\pi x, \pi y) = g(x, y)$, and the place of $\pi x$ in $\pi t$ is the place of $x$ in $t$. So the key of $(\pi x, \pi y)$ in the renamed instance is the key of $(x, y)$, $L' = \pi L$ pair by pair, and the run on the renamed instance is the image of the run on $P$ under $\pi$. With a fixed tie-break the resolute rule is not neutral: for the ballots $(0, 1)$ and $(1, 0)$, both pairs have margin 0, and $(0, 1)$ comes first and is locked, both for the profile and for its image under the swap of 0 and 1.

**Claim 7 (margins and winning votes).** With full rankings, sorting the pairs of $L$ by $n_P(x, y)$, with the same tie-break, gives the same list as sorting them by $g(x, y)$.

*Proof.* $n_P(x, y) + n_P(y, x) = n$, so $n_P(x, y) = (n + g(x, y))/2$, an increasing function of $g(x, y)$.

**Claim 8 (monotonicity).** Let $r$ be the ranking for $P$ with top $w$, and let $Q$ be $P$ with $w$ moved up one place on one ballot, passing the candidate $x$. Then the ranking for $Q$ with the same tie-break is $r$, so $w$ still wins.

*Proof.* Only the pair $\{w, x\}$ changes: $g_Q(w, x) = g(w, x) + 2$ and $g_Q(x, w) = g(x, w) - 2$. So the priority of $(w, x)$ goes up, the priority of $(x, w)$ goes down, and the relative priority of any two other pairs is the same. Call a pair downward if it agrees with $r$ and upward otherwise. Since $w$ is the top of $r$, $(w, x)$ is downward and $(x, w)$ is upward. Every locked edge of the run on $P$ is downward, by Claim 2.

Consider the run on $Q$, with list $L_Q$. We show by induction over the passes that only downward pairs are locked. Then the closure $R_Q$ is always contained in $r$, so a downward pair is never skipped (that would need the upward reach $R_Q[y][x]$) and ends in $R_Q$. Let $p = (z, y)$ be an upward pair of $L_Q$. Then $p \ne (w, x)$, $g_Q(p) \ge 0$, and $g(p) \ge g_Q(p)$, so $p \in L$ as well. In the run on $P$, $p$ was skipped, so there was a path from $y$ to $z$ of edges locked before $p$, all downward. Each such edge $e$ precedes $p$ in $L_Q$ too: if neither is $(w, x)$ or $(x, w)$, their order is unchanged; if $e = (w, x)$, its priority only went up; if $p = (x, w)$, its priority only went down; and $e \ne (x, w)$ because $e$ is downward. Each $e$ is downward, has $g_Q(e) \ge g(e) \ge 0$, and so, by the induction hypothesis, is in $R_Q$ when $p$ is processed. So $R_Q[y][z]$ holds and $p$ is skipped. At the end, $R_Q$ is a linear order by Claim 2 and is contained in the linear order $r$, so $R_Q = r$. $\blacksquare$
