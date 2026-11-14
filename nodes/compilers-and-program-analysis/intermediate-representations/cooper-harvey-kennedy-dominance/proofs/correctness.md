---
title: The Cooper-Harvey-Kennedy algorithm computes the immediate dominators in at most d + 2 passes
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a directed graph with start vertex $r$. Let $R$ be the set of vertices that $r$ reaches. A vertex outside $R$ gets no postorder number in line L1, is never visited in line L7 and stays Undefined, so line L10 skips it as a predecessor. An edge from a vertex outside $R$ lies on no path from $r$, so it changes no dominator. From here on, all vertices are in $R$ and "predecessor" means a predecessor in $R$. $T$ is the DFS tree of line L1, $po$ its postorder numbering, and the visit order of line L7 is decreasing $po$. $D(v)$ is the set of dominators of $v$. The DFS tree is used only through these facts: a proper $T$-ancestor of $v$ has a larger $po$ than $v$, and the tree path from $r$ to $v$ contains exactly the $T$-ancestors of $v$.

For a defined vertex $y$, $chain(y)$ is the set of vertices on $y, doms[y], doms[doms[y]], \ldots$. Lemma 1 shows this sequence reaches $r$, where it stops, since $doms[r] = r$.

**Lemma 0 (the dominator equation).** For $b \ne r$, $D(b) = \{b\} \cup \bigcap_{p} D(p)$, the intersection over the predecessors $p$ of $b$. Also $D(r) = \{r\}$.

*Proof.* Let $x \in D(b)$ with $x \ne b$, and let $p$ be a predecessor. If $x = p$ then $x \in D(p)$. Otherwise a path from $r$ to $p$ that avoids $x$, followed by the edge $(p, b)$, would avoid $x$, so $x \in D(p)$. Conversely, let $x \ne b$ be in every $D(p)$. A path from $r$ to $b$ has at least one edge, since $b \ne r$, so its last but one vertex is a predecessor $p$, and the part up to $p$ contains $x$. The vertex $r$ is a path from $r$ to $r$ by itself, so $D(r) = \{r\}$. $\square$

**Lemma 1 (the guesses form a tree).** At all times: every defined $y \ne r$ has $doms[y]$ defined and a proper $T$-ancestor of $y$, and $chain(y)$ is a set of $T$-ancestors of $y$. A vertex that is defined stays defined.

*Proof.* At the start only $r$ is defined. Line L12 never writes Undefined. Assume the claim before an update of $b$ in line L12. In pass 1 every vertex visited before $b$ was given a value when it was visited, by induction along the visit order, and the DFS parent $q$ of $b$ comes before $b$ because $po(q) > po(b)$. So $q$ is defined, line L8 finds a predecessor, and the defined predecessors include $q$. Lemma 2 below, applied to the current tree, shows that the value $c$ that lines L8 to L10 compute is a vertex of $chain(q)$, and by the claim $chain(q)$ consists of $T$-ancestors of $q$. So $c$ is defined and a proper $T$-ancestor of $b$. After the update, $chain(b) = \{b\} \cup chain(c)$; the old chain of $c$ does not contain $b$, because it consists of $T$-ancestors of $c$, and $b$ is not one of them, so it is not changed by the update. For another vertex $y$, either $b \notin chain(y)$ and nothing changes, or $chain(y)$ is the part from $y$ up to just below $b$, which is unchanged, together with the new $chain(b)$. Since $b \in chain(y)$, $b$ is a $T$-ancestor of $y$, and the new $chain(b)$ consists of $T$-ancestors of $b$, so of $y$. $\square$

So following $doms$ strictly raises $po$ until it reaches $r$: the defined vertices form a tree with root $r$ and parent array $doms$, and $chain(y)$ is the set of ancestors of $y$ in that tree. The vertex of $chain(y)$ with the smallest $po$ is $y$, so the chain determines $y$.

**Lemma 2 (INTERSECT).** In a tree with root $r$ whose parent array is $doms$ and in which every parent has a larger $po$ than its child, INTERSECT$(b_1, b_2)$ stops and returns the nearest common ancestor $c$ of $b_1$ and $b_2$. Moreover $chain(c) = chain(b_1) \cap chain(b_2)$.

*Proof.* The common ancestors of $b_1$ and $b_2$ are $chain(b_1) \cap chain(b_2)$. They form the path from $c$ up to $r$, which gives the second claim. We show that $finger_1$ is always a descendant of $c$ (possibly $c$), and the same for $finger_2$. This holds at the start. Line L16 moves $finger_1$ only when $po(finger_1) < po(finger_2)$. If $finger_1 = c$, then $finger_2$ is a descendant of $c$, so $po(finger_2) \le po(c) = po(finger_1)$, and there is no move. So $finger_1$ is a proper descendant of $c$, and its parent is still a descendant of $c$. Line L17 is the same. Each move raises the $po$ of one finger, so the inner loops stop. In an outer iteration with $finger_1 \ne finger_2$ the numbers differ, since $po$ is one to one, so one of the inner loops moves; hence the outer loop stops too. At the end both fingers are the same vertex $f$, which is an ancestor of $b_1$ and of $b_2$ and a descendant of $c$. Every common ancestor is an ancestor of $c$, so $f = c$. $\square$

The nearest common ancestor is associative, so lines L8 to L10 compute the nearest common ancestor $c$ of all defined predecessors $p$ of $b$, and $chain(c) = \bigcap_p chain(p)$. By Lemma 1, the update of line L12, or the decision not to update, gives

$$chain'(b) = \{b\} \cup \bigcap_{p \text{ defined}} chain(p). \qquad (\ast)$$

**Lemma 3 (soundness).** At all times, $D(y) \subseteq chain(y)$ for every defined $y$.

*Proof.* At the start, $D(r) = \{r\} = chain(r)$. Assume the claim before an update of $b$.

*At $b$.* Let $x \in D(b)$ with $x \ne b$. By Lemma 0, $x \in D(p) \subseteq chain(p)$ for every defined predecessor $p$, so $x \in chain'(b)$ by $(\ast)$. And $b \in chain'(b)$.

*Below $b$.* Let $y \ne b$ have $b \in chain(y)$, and let $x \in D(y)$. The new chain of $y$ is the old part from $y$ to $b$ together with $chain'(b)$. If $x$ is in the old part, we are done. Otherwise $x \in chain(y)$ by the claim, and $x$ is above $b$ in the old chain, so it is in the old $chain(doms[b])$ and is a proper $T$-ancestor of $b$ by Lemma 1. Also $b$ is a $T$-ancestor of $y$. Then $x$ dominates $b$: if a path from $r$ to $b$ avoided $x$, it could be continued by the tree path from $b$ to $y$, which contains only $T$-descendants of $b$ and so not $x$, and this would be a path to $y$ that avoids $x$. So $x \in D(b) \subseteq chain'(b)$ by the case above.

The chains of all other vertices do not change. $\square$

**Theorem 1 (partial correctness).** If the loop of line L5 stops, then $doms[y] = \mathrm{idom}(y)$ for every $y \ne r$.

*Proof.* If $R = \{r\}$, there is nothing to show. Otherwise pass 1 sets a value for every vertex, which changes $doms$, so the last pass is pass 2 or later, and in it every vertex and every predecessor is defined. The last pass changes nothing, so by $(\ast)$, at its end, $chain(b) = \{b\} \cup \bigcap_p chain(p)$ over all predecessors, for all $b \ne r$, and $chain(r) = \{r\}$.

Let $x \in chain(y)$ and suppose $x \notin D(y)$. Then there is a path $r = v_0, v_1, \ldots, v_k = y$ that avoids $x$, and $x \ne r$. We show $x \notin chain(v_i)$ for all $i$. For $v_0 = r$ the chain is $\{r\}$. If $x \notin chain(v_i)$ and $v_{i+1} \ne r$, then $x$ is not in the intersection over the predecessors of $v_{i+1}$, which include $v_i$, and $x \ne v_{i+1}$, so $x \notin chain(v_{i+1})$. If $v_{i+1} = r$, its chain is $\{r\}$. So $x \notin chain(y)$, a contradiction. Hence $chain(y) \subseteq D(y)$, and with Lemma 3, $chain(y) = D(y)$.

Now $chain(doms[y]) = D(y) \setminus \{y\}$, so $doms[y]$ is a strict dominator of $y$, and every strict dominator of $y$ lies in $chain(doms[y]) = D(doms[y])$, that is, it dominates $doms[y]$. This is the definition of $\mathrm{idom}(y)$. $\square$

**The set iteration.** To bound the passes we compare with the set version $S$ of the same loop. Let $S(r) = \{r\}$ and $S(v) = R$ for $v \ne r$ at the start, and let $S$ visit the vertices in the same order as CHK, one pass at a time, doing $S(b) \leftarrow \{b\} \cup \bigcap_p S(p)$ over all predecessors. We run the two side by side, so each step of one is matched by a step of the other at the same vertex. In pass 1, a vertex is Undefined in CHK exactly when it has not been visited yet, which is exactly when its $S$ is still $R$. So intersecting over all $S(p)$ is the same as intersecting over the defined $p$, since $R$ changes no intersection.

- **(S1) $S$ only shrinks.** Each value is the same monotone function of the current $S$, the current $S$ is at most the earlier one by induction, and the first values are $R$.
- **(S2) $D \subseteq S$.** By induction with Lemma 0: $\{b\} \cup \bigcap_p S(p) \supseteq \{b\} \cup \bigcap_p D(p) = D(b)$.

**Lemma 4.** At all times, if $b \in S(y)$, then $S(b) \subseteq S(y)$.

*Proof.* At the start, $S(y) = R$ for $y \ne r$, and $S(r) = \{r\}$. Consider an update at $z$ that gives $S'(z)$. Take $b \in S'(y)$.
If $y \ne z$ and $b \ne z$, nothing involved has changed.
If $y = b = z$, the claim is trivial.
If $y = z \ne b$, then $b \in S(p)$ for every predecessor $p$ of $z$, so $S(b) \subseteq S(p)$ for every $p$, and $S'(b) = S(b) \subseteq \bigcap_p S(p) \subseteq S'(z)$.
If $y \ne z = b$, then $z \in S(y)$ gives $S(z) \subseteq S(y)$, and $S'(z) \subseteq S(z)$ by (S1), so $S'(z) \subseteq S'(y)$. $\square$

**Lemma 5.** At all times, $chain(y) \subseteq S(y)$ for every defined $y$.

*Proof.* At the start both are $\{r\}$ at $r$. At an update of $b$: by $(\ast)$ and the remark on Undefined vertices, $chain'(b) = \{b\} \cup \bigcap_{p \text{ defined}} chain(p) \subseteq \{b\} \cup \bigcap_p S(p) = S'(b)$. For $y \ne b$ with $b \in chain(y)$: the new chain of $y$ is the old part from $y$ to $b$, which is in $chain(y) \subseteq S(y)$, together with $chain'(b) \subseteq S'(b) \subseteq S(b)$. Since $b \in chain(y) \subseteq S(y)$, Lemma 4 gives $S(b) \subseteq S(y)$. And $S'(y) = S(y)$. The other chains do not change. $\square$

**Lemma 6 (paths).** For a path $P$ from $r$, let $ret(P)$ be the number of its edges $(u, v)$ that are retreating, that is, $po(v) \ge po(u)$. If pass $k \ge 1$ has finished, then $S(v) \subseteq$ the vertex set of $P$ for every path $P$ from $r$ to $v$ with $ret(P) \le k - 1$.

*Proof.* Let $P = v_0, \ldots, v_j$ with $v_0 = r$, and let $k_i = 1 + $ the number of retreating edges among the first $i$ edges. We show: by the end of pass $k_i$, $S(v_i) \subseteq \{v_0, \ldots, v_i\}$, and by (S1) it stays so. For $i = 0$, $S(r) = \{r\}$ at all times. For the step, let $e = (v_i, v_{i+1})$; if $v_{i+1} = r$ there is nothing to show.
If $e$ is not retreating, $v_{i+1}$ comes after $v_i$ in the visit order, so in pass $k_{i+1} = k_i$ it is visited after $v_i$ was visited (or, for $v_i = r$, at a time when $S(r) = \{r\}$). So when $v_{i+1}$ is visited, $S(v_i) \subseteq \{v_0, \ldots, v_i\}$, and the new $S(v_{i+1}) \subseteq \{v_{i+1}\} \cup S(v_i) \subseteq \{v_0, \ldots, v_{i+1}\}$.
If $e$ is retreating, $k_{i+1} = k_i + 1$, and in pass $k_i + 1$ the vertex $v_{i+1}$ is visited after pass $k_i$ has ended, so the same argument applies. $\square$

**Theorem 2 (termination).** Let $d$ be the largest $ret(P)$ over the simple paths $P$ from $r$. The loop of line L5 stops after at most $d + 2$ passes.

*Proof.* A vertex $x$ dominates $v$ if and only if $x$ is on every simple path from $r$ to $v$, since every path from $r$ to $v$ contains a simple one, with a subset of its vertices, obtained by cutting out cycles. If pass $d + 1$ runs, then after it Lemma 6 gives $S(v) \subseteq$ the vertex set of each simple path from $r$ to $v$, so $S(v) \subseteq D(v)$, and $S = D$ by (S2). By Lemmas 3 and 5, $D \subseteq chain \subseteq S = D$, so every chain is $D$. In pass $d + 2$, by $(\ast)$ and Lemma 0, each visit computes $chain'(b) = \{b\} \cup \bigcap_p D(p) = D(b) = chain(b)$, so the new value has the same chain as the old one, so it is the same vertex, and nothing changes. The loop stops after pass $d + 2$ or earlier. A simple path has at most $|R| - 1$ edges, so $d + 2 \le |R| + 1$. $\square$

**Corollary (reducible graphs).** Call an edge $(t, h)$ a back edge if $h$ dominates $t$, and call $G$ reducible if $G$ without its back edges has no cycle. If $G$ is reducible, the loop stops after at most 2 passes.

*Proof.* First, every retreating edge $(u, v)$ is a back edge. For $u = v$ this is clear. Otherwise, in a DFS an edge $(u, v)$ with $po(v) > po(u)$ goes to a $T$-ancestor $v$ of $u$, because tree edges, forward edges and cross edges all go to a smaller $po$. A tree edge $(x, y)$ is never a back edge, since the tree path from $r$ to $x$ avoids its proper descendant $y$. So if $(u, v)$ were not a back edge, the tree path from $v$ to $u$ and the edge $(u, v)$ would form a cycle without back edges.

Next, let $P$ be a path from $r$ to $v$ with a retreating edge $(t, h)$. Then $h$ dominates $t$, so $h$ appears in $P$ before $t$; cutting out the part of $P$ from that earlier $h$ to the $h$ after $t$ gives a shorter path from $r$ to $v$, made of edges of $P$, with a subset of its vertices. Repeating this gives a path with no retreating edge. So $D(v)$ is the intersection of the vertex sets of the paths from $r$ to $v$ with $ret = 0$, and by Lemma 6 with $k = 1$, $S = D$ after pass 1. As in Theorem 2, every chain is $D$ after pass 1, and pass 2 changes nothing. $\square$

The proof of Lemma 6 shows more: on a reducible graph, $S(b) = D(b)$ already at the moment $b$ is first visited, so every guess is final when it is set, and in pass 1 every chain is a path of the final dominator tree.

**Cost.** Line L1 is $\Theta(n + m)$. In a pass, line L7 visits each vertex once, lines L8 to L10 look at each edge once, and each call of INTERSECT moves each finger along one chain, raising its $po$ each time, so it makes at most $2|R|$ moves. A pass costs $O(n + m n)$, and with Theorem 2 the total is $O(n + m + (d + 2)(n + m n))$, which is $O((d + 2)\, n (n + m))$. On a reducible graph a chain has at most $h + 1$ vertices in every pass, where $h$ is the height of the dominator tree, so a pass costs $O(n + m h)$.

**What is measured and what is proved.** Theorems 1 and 2 and the corollary are proved above. The timings in the paper and the pass counts of the seeded experiment on the page are measurements. The tests check the result against dominators computed by the definition (delete a vertex, test reachability) on random graphs and on toy IR control flow graphs, and check the bounds of Theorem 2 and of the corollary against a brute-force count of retreating edges on simple paths.
