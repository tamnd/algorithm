---
title: Path relaxation computes the lexicographically first DFS in h + 1 rounds
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a directed graph with ordered adjacency lists (an undirected graph is the directed graph with both arcs of each edge). The sequential DFS from $s$ scans each list from the first entry to the last. A sequence $x = (x_0, \ldots, x_{k-1})$ of nonnegative integers spells at most one walk from $s$: start at $s$ and, at step $j$, move to entry $x_j$ of the list of the current vertex. Write $x \cdot i$ for $x$ followed by $i$, $|x|$ for the length, and $<$ for the lexicographic order, in which a proper prefix comes before its extensions. Write $x \sqsupseteq y$ when $x = y$, or when there is a $j < \min(|x|, |y|)$ with $x_t = y_t$ for $t < j$ and $x_j > y_j$. Then $x \sqsupseteq y$ implies $x \ge y$.

Let $T(v)$ be the sequence that spells the tree path of the DFS from $s$ to $v$, for each reachable $v$, and let $\operatorname{depth}(v) = |T(v)|$ and $h = \max_v \operatorname{depth}(v)$. Let $P_r[v]$ be the label after round $r$, with $P_0[s] = ()$ and $P_0[v] = nil$ for $v \ne s$. Line L5 gives, for $v \ne s$,

$$P_{r+1}[v] = \min \big( \{P_r[v]\} \cup \{ P_r[u] \cdot i : v \text{ is entry } i \text{ of } adj[u],\ P_r[u] \ne nil \} \big),$$

where $nil$ entries are left out of the set, and $P_{r+1}[s] = ()$.

**Lemma 1 (DFS facts).** Let $u$ be reachable, let $v \ne s$ be entry $i$ of $adj[u]$, and let $t = T(u) \cdot i$. Then exactly one of these holds: (a) $t = T(v)$; (b) $t \sqsupseteq T(v)$ and $t \ne T(v)$; (c) $T(v)$ is a proper prefix of $t$.

*Proof.* When the DFS at $u$ reads entry $i$, the vertex $v$ is either new (white) or not. If it is white, $v$ becomes the child of $u$ through entry $i$, so $T(v) = t$, case (a). Else $v$ was discovered before this moment. There are three cases.

- $v$ is a proper descendant of $u$. Then $v$ was discovered while $u$ scanned an entry $j$ before $i$, inside the subtree of the child of $u$ through entry $j$. So $T(v)$ begins with $T(u) \cdot j$, $j < i$, and $t$ and $T(v)$ first differ at position $|T(u)|$, where $t$ is larger. Case (b).
- $v$ is $u$ or an ancestor of $u$. Then $T(v)$ is a prefix of $T(u)$, so a proper prefix of $t$. Case (c).
- $v$ is neither. By the [parenthesis theorem](/parenthesis-theorem/), a vertex discovered while $u$ is active is a descendant of $u$, so $v$ was discovered before $u$. Let $z$ be the deepest common ancestor of $u$ and $v$. Neither is an ancestor of the other, so $T(u)$ and $T(v)$ agree up to $z$ and then take different entries $b$ and $a$ of the list of $z$. The DFS explores the whole subtree through an entry of $z$ before it reads the next entry, and $v$ came first, so $a < b$. So $t$ and $T(v)$ first differ at that position and $t$ is larger. Case (b). $\square$

**Lemma 2 (preorder).** For reachable $v \ne w$, the DFS discovers $v$ before $w$ if and only if $T(v) < T(w)$.

*Proof.* If $v$ is a proper ancestor of $w$, then $T(v)$ is a proper prefix of $T(w)$ and $v$ is discovered first. If neither is an ancestor of the other, the last paragraph of the proof of Lemma 1 shows that the one discovered first has the smaller entry at the first difference. $\square$

**Lemma 3 (labels).** For every $r$ and $v$ with $P_r[v] \ne nil$: (i) $P_r[v]$ spells a walk from $s$ that ends at $v$; (ii) $|P_r[v]| \le r$; (iii) for every prefix $x$ of $P_r[v]$, with end vertex $w$, there is an $r' \le r$ with $P_{r'}[w] = x$; (iv) $P_{r+1}[v] \le P_r[v]$.

*Proof.* Part (iv) holds because $P_r[v]$ is in the set of the minimum. Parts (i) to (iii) go by induction on $r$. For $r = 0$, only $P_0[s] = ()$ is defined. For $r + 1$, if $P_{r+1}[v] = P_r[v]$ the claims hold by induction. Else $P_{r+1}[v] = P_r[u] \cdot i$ with $v$ entry $i$ of $adj[u]$: by induction $P_r[u]$ spells a walk to $u$ of length at most $r$, so $P_r[u] \cdot i$ spells a walk to $v$ of length at most $r + 1$; its prefixes are the prefixes of $P_r[u]$, covered by induction, and the whole sequence, which is $P_{r+1}[v]$. $\square$

By (i), an unreachable vertex never gets a label.

**Lemma 4 (invariant).** For every $r$ and every vertex $v$, $P_r[v] = nil$ or $P_r[v] \sqsupseteq T(v)$.

*Proof.* By induction on $r$. For $r = 0$ it holds, since $P_0[s] = () = T(s)$. Assume it for $r$, take $v \ne s$, and take a candidate $c = P_r[u] \cdot i$. By induction $P_r[u] \sqsupseteq T(u)$. Let $t = T(u) \cdot i$. First we show: $c \sqsupseteq T(v)$, or $T(v)$ is a proper prefix of $c$.

If $P_r[u] = T(u)$, then $c = t$ and Lemma 1 gives the claim. Else $c$ and $t$ first differ at a position $j < |T(u)|$, where $c$ is larger. Use the three cases of Lemma 1.

- (a) $t = T(v)$. Then $c$ and $T(v)$ first differ at $j$, and $c$ is larger.
- (b) $t$ and $T(v)$ first differ at a position $q$, where $t$ is larger. If $j < q$, then $c$ and $T(v)$ agree before $j$ and $c_j > t_j = T(v)_j$. If $j \ge q$, then $c$ and $T(v)$ agree before $q$ and $c_q \ge t_q > T(v)_q$, with $c_q = t_q$ when $j > q$. In both cases $c \sqsupseteq T(v)$.
- (c) $T(v)$ is a proper prefix of $t$, with $\ell = |T(v)|$. If $j < \ell$, then $c$ and $T(v)$ first differ at $j$, and $c$ is larger. If $j \ge \ell$, then $c$ agrees with $t$, so with $T(v)$, on the first $\ell$ positions, and $|c| = |t| > \ell$, so $T(v)$ is a proper prefix of $c$.

Now suppose some candidate $c = P_r[u] \cdot i$ has $T(v)$ as a proper prefix. Then $|P_r[u]| \ge \ell$ and $T(v)$ is a prefix of $P_r[u]$. The sequence $T(v)$ spells the tree path to $v$, so by Lemma 3 (iii) there is an $r' \le r$ with $P_{r'}[v] = T(v)$, and by (iv) $P_r[v] \le T(v)$. By induction $P_r[v] \sqsupseteq T(v)$, so $P_r[v] \ge T(v)$. So $P_r[v] = T(v)$. Every member of the set of the minimum is then at least $T(v)$, and $T(v)$ is a member, so $P_{r+1}[v] = T(v)$.

If no candidate has $T(v)$ as a proper prefix, every candidate is $\sqsupseteq T(v)$, and so is $P_r[v]$ when it is defined. The minimum is one of them, so $P_{r+1}[v] \sqsupseteq T(v)$ or $P_{r+1}[v] = nil$. $\square$

**Lemma 5 (convergence).** For every reachable $v$ and every $r \ge \operatorname{depth}(v)$, $P_r[v] = T(v)$.

*Proof.* By induction on $\operatorname{depth}(v)$. For $s$ it holds for all $r$. Let $v \ne s$ have DFS parent $u$, with $v$ entry $i$ of $adj[u]$, so $T(v) = T(u) \cdot i$. For $r \ge \operatorname{depth}(v)$, induction gives $P_{r-1}[u] = T(u)$, so $T(v)$ is a candidate in round $r$ and $P_r[v] \le T(v)$. Lemma 4 gives $P_r[v] \ge T(v)$. $\square$

**Termination and the number of rounds.** The labels after round $r$ depend only on the labels after round $r - 1$. So if a round makes no change, no later round does. By Lemma 5, $P_h = P_{h+1} = T$, so the round $h + 1$ makes no change, if the loop gets that far. The loop cannot stop at a round $r \le h$: that would mean $P_r = P_{r-1}$, so $P_{r-1} = P_h = T$, but a vertex at depth $h$ has $|T(v)| = h > r - 1 \ge |P_{r-1}[v]|$ by Lemma 3 (ii). So the loop of line L3 runs exactly $h + 1$ rounds.

**Result.** At the exit $P[v] = T(v)$ for each reachable $v$ and $P[v] = nil$ for the others, so line L8 finds the reachable set. By Lemma 2, line L9 lists it in DFS preorder. The parent stored for $v \ne s$ is the vertex $u$ whose candidate $P[u] \cdot i$ gave the final label $T(v)$. Then $P[u]$ is $T(v)$ without its last entry, which spells the tree path to the DFS parent of $v$, and a sequence spells only one walk, so $u$ is the DFS parent. $\blacksquare$
