---
title: The Yoshimura-Kuh merging keeps groups of disjoint nets and an acyclic constraint graph, so the final left-edge scan gives a legal routing
proves: [disjoint groups, acyclicity, correctness, termination, cost of a merge]
status: full
---

Let the zones be $Z_k = S(c_k)$ for columns $c_1 < c_2 < \cdots < c_m$, where $S(c)$ is the set of nets whose closed interval holds $c$. Then net $x$ lies in $Z_k$ exactly when $l_x \le c_k \le r_x$, so the zones that hold $x$ are a run of consecutive indices, from $\mathrm{first}(x)$ to $\mathrm{last}(x)$. Every set $S(c)$ is contained in some zone, by the definition of maximal sets. The first and last zone of a group are those of its first and its last net.

**Lemma 1 (order of merged nets).** Let $a$ be a net with $\mathrm{last}(a) \le i$ and $b$ a net with $\mathrm{first}(b) = i + 1$. Then $r_a < l_b$.

*Proof.* Since $a \in Z_{\mathrm{last}(a)}$ and $\mathrm{last}(a) \le i$, $l_a \le c_i$. Since $a \notin Z_{i+1}$ and $l_a \le c_i < c_{i+1}$, $r_a < c_{i+1}$. Since $b \in Z_{i+1}$, $c_{i+1} \le r_b$, and since $b \notin Z_i$ while $c_i < c_{i+1} \le r_b$, $c_i < l_b$. Suppose the intervals share a column $c$. Then $S(c)$ holds $a$ and $b$ and lies in some zone $Z_k$, so $l_b \le c_k \le r_a$. From $c_k \le r_a < c_{i+1}$ we get $k \le i$, and from $c_k \ge l_b > c_i$ we get $k \ge i + 1$, a contradiction. So the intervals are disjoint, and $l_a \le c_i < l_b$ puts $a$ on the left. $\square$

**Lemma 2 (groups).** At every moment, the nets of a group have pairwise disjoint intervals, and in the order of their left ends each ends before the next starts. The last net of the group has the last zone of the group, and every group in $R$ is a single net.

*Proof.* By induction over the merges. A group made by a merge has the first zone of its oldest net, which is at most $i$ at boundary $i$, so a group with first zone $i + 1$ was never merged and is one net. A merge at boundary $i$ joins a group $a \in L$, whose last net $a'$ has $\mathrm{last}(a') \le i$, with a single net $b$ with $\mathrm{first}(b) = i + 1$. By Lemma 1, $r_{a'} < l_b$, and by the induction every other net of $a$ ends before $a'$ starts. So $b$ comes after all nets of $a$, and it becomes the last net, with the last zone of the new group. $\square$

**Lemma 3 (acyclic).** If $G_v$ is acyclic and $a$ and $b$ have no path between them, the graph made by merging $b$ into $a$ is acyclic.

*Proof.* A cycle in the new graph that avoids the merged node is a cycle of $G_v$. A cycle through it leaves along an edge of $a$ or of $b$ and comes back along an edge into $a$ or into $b$. If it leaves from $a$ and returns into $a$, or leaves from $b$ and returns into $b$, the path between avoids the merged node, so it is a cycle of $G_v$. Otherwise it gives a path of $G_v$ from $a$ to $b$ or from $b$ to $a$, which is excluded. $\square$

**Lemma 4 (cost).** After the merge of $a$ and $b$, the longest path through the merged node has $\max(u(a), u(b)) + \max(d(a), d(b)) - 1$ nodes.

*Proof.* A path through the merged node is a path that ends at $a$ or $b$, followed by a path that starts at $a$ or $b$, sharing the merged node. The parts before and after do not change, because no path joins $a$ and $b$, so no longest path into $a$ passes through $b$ and the other way. The longest choices give the formula. $\square$

**Theorem 1 (legal routing).** If $G_v$ is acyclic, the algorithm returns tracks that form a legal routing without doglegs.

*Proof.* By Lemma 3, applied at every merge, the graph of groups stays acyclic. Line L10 is the left-edge scan on the groups, with the span of a group from its first left end to its last right end. By Lemmas 3 and 1 of the left-edge proof, it places every group, groups on one track have disjoint spans, and every edge of the graph of groups goes from a higher track to a lower one. By Lemma 2, the nets inside a group are disjoint and lie inside its span, so two nets on one track never share a column. An edge $a \to b$ of $G_v$ between nets in different groups is an edge between their groups, so $t(a) < t(b)$. Nets $a$ and $b$ with an edge are never in one group, because a merge needs no path between them, and later merges keep the edge between their groups. Theorem 2 of the left-edge proof then gives a legal routing in the reserved two-layer model. $\square$

**Theorem 2 (termination).** The algorithm stops.

*Proof.* Each merge lowers the number of groups by one, so at boundary $i$ the loop of lines L7 to L9 runs at most $N$ times. There are $m - 1$ boundaries, and the scan of line L10 stops on an acyclic graph. $\square$

**Lower bound.** Every result has at least $\max(d, k)$ tracks, with $k$ the number of nets on a longest path of the original $G_v$, since both bounds hold for every routing without doglegs.

**Tests.** The tests compare the implementation with two exhaustive searches over all maps from nets to tracks, one with a geometric checker of the wires and one with the rules of disjoint intervals and vertical constraints, on channels with up to 7 nets. They check that the result is legal, never below the optimum, that merged nets are disjoint, and that the zones equal those found by comparing all sets $S(c)$.
