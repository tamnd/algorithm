---
title: The tabulation algorithm computes the meet over all valid paths in O(E D^3) time
proves: [correctness, termination]
status: full
---

**Setting.** $G^*$ is the supergraph of the program, as on the page. Every procedure $p$ has a start node $s_p$ and an exit node $e_p$. A call site has a call node $c$ and a return site $r$, and three edges: the call edge $c \to s_q$, the return edge $e_q \to r$ and the intraprocedural call-to-return edge $c \to r$. The facts of $p$ form a finite set $D_p$, and $D = \max_p |D_p|$. $\mathbf{0}$ is a new fact that is in no $D_p$. Every edge $e$ of $G^*$ has a flow function, given pointwise as a map $F_e$ from $D_{src} \cup \{\mathbf{0}\}$ to subsets of $D_{dst} \cup \{\mathbf{0}\}$ with $\mathbf{0} \in F_e(\mathbf{0})$ and $\mathbf{0} \notin F_e(d)$ for $d \ne \mathbf{0}$. It stands for the function

$$f_e(X) = \bigcup_{d \in X \cup \{\mathbf{0}\}} F_e(d) \setminus \{\mathbf{0}\}.$$

These functions are exactly the functions with $f(X \cup Y) = f(X) \cup f(Y)$: given such an $f$, take $F(\mathbf{0}) = f(\emptyset) \cup \{\mathbf{0}\}$ and $F(d) = f(\{d\})$. For a path $\pi = e_1 \dots e_k$, $f_\pi = f_{e_k} \circ \dots \circ f_{e_1}$, and the empty path gives the identity. $S \subseteq D_{main}$ is the set of seed facts at $s_{main}$.

A path of $G^*$ is *valid* if its call and return edges, read as brackets $(_c$ and $)_c$, form a prefix of a word in which every $)_c$ closes the last open $(_c$. A path is *same-level* if it is valid and every $(_c$ is closed in it. A same-level path starts and ends in the same procedure. The meet over all valid paths is

$$\mathrm{MVP}(n) = \bigcup \{ f_\pi(S) : \pi \text{ a valid path from } s_{main} \text{ to } n \}.$$

Sets of facts are ordered by $\supseteq$, so union is the meet and $\emptyset$ is $\top$, as in Kildall's convention. In Cousot's join convention the order flips and the same set is the least solution.

The *exploded supergraph* $G^\#$ has a node $\langle n, d \rangle$ for every node $n$ of $G^*$ in procedure $p$ and every $d \in D_p \cup \{\mathbf{0}\}$. For every edge $e = (n, m)$ of $G^*$ and every $d' \in F_e(d)$, it has the edge $\langle n, d \rangle \to \langle m, d' \rangle$ of the same kind as $e$. Valid and same-level paths of $G^\#$ are defined by the same brackets.

We use the lines L1 to L16 of the pseudocode. A *path edge* $(n, d_1, d_2)$ stands for $\langle s_p, d_1 \rangle \to \langle n, d_2 \rangle$, where $p$ is the procedure of $n$. A *summary edge* $(c, d_4, d_5)$ stands for $\langle c, d_4 \rangle \to \langle r, d_5 \rangle$. $\mathit{Through}$ is the set of triples of line L10, and $\mathit{inv}_c(d_1) = \{ d_4 : d_1 \in F_c(d_4) \}$ for the call edge of $c$.

**Lemma 1 (one path, many facts).** For a path $\pi$ of $G^*$ from $n$ to $m$ and a set $X$, the facts $d'$ such that $G^\#$ has a path that follows $\pi$ from some $\langle n, d \rangle$ with $d \in X \cup \{\mathbf{0}\}$ to $\langle m, d' \rangle$ are exactly $f_\pi(X) \cup \{\mathbf{0}\}$.

*Proof.* Induction on the length $k$ of $\pi$. For $k = 0$ both sides are $X \cup \{\mathbf{0}\}$. Let $\pi = \pi' e$. By induction, the facts reached after $\pi'$ are $Y \cup \{\mathbf{0}\}$ with $Y = f_{\pi'}(X)$. One more edge reaches $\bigcup_{d \in Y \cup \{\mathbf{0}\}} F_e(d)$. This contains $\mathbf{0}$, because $\mathbf{0} \in F_e(\mathbf{0})$, and without $\mathbf{0}$ it is $f_e(Y)$. So it is $f_e(Y) \cup \{\mathbf{0}\} = f_\pi(X) \cup \{\mathbf{0}\}$. $\square$

A path of $G^\#$ is valid exactly when its shadow in $G^*$ is valid, since the brackets are the same. So Lemma 1 gives:

**Corollary 2 (MVP is reachability).** Let $\mathit{Reach}$ be the set of nodes of $G^\#$ that a valid path reaches from some $\langle s_{main}, d_0 \rangle$ with $d_0 \in S \cup \{\mathbf{0}\}$. Then for every $d \ne \mathbf{0}$, $d \in \mathrm{MVP}(n)$ if and only if $\langle n, d \rangle \in \mathit{Reach}$.

**Decomposition.** Cut a valid path $\pi$ of $G^\#$ from $\langle s_{main}, d_0 \rangle$ at its call edges that are never closed. The part after the last such call edge (or all of $\pi$, if there is none) is a same-level path. It starts at $\langle s_p, d_1 \rangle$, where $p$ is the procedure of the end of $\pi$, and $d_1$ is $d_0$ or the target fact of that call edge. We call $d_1$ the *entry fact* of $\pi$.

Let $\mathit{PE}$ be the set of path edges at the end and $\mathit{SE}$ the set of summary edges at the end.

**Lemma 3 (path edges are sound).** Every path edge $(n, d_1, d_2)$ that L16 inserts has a valid path of $G^\#$ from some $\langle s_{main}, d_0 \rangle$, $d_0 \in S \cup \{\mathbf{0}\}$, to $\langle n, d_2 \rangle$ whose entry fact is $d_1$. Every summary edge $(c, d_4, d_5)$ that L12 inserts has a same-level path $\langle c, d_4 \rangle \to \langle s_q, d_1 \rangle \leadsto \langle e_q, d_2 \rangle \to \langle r, d_5 \rangle$ in $G^\#$.

*Proof.* Induction on the order of insertion. The claim for a path edge says: $\langle s_p, d_1 \rangle$ is reached by a valid path $\alpha$ that is empty or ends with a call edge that is never closed, and a same-level path $\sigma$ goes from $\langle s_p, d_1 \rangle$ to $\langle n, d_2 \rangle$.

- L2 inserts $(s_{main}, d, d)$ with $d \in S \cup \{\mathbf{0}\}$. Take the empty path.
- L6 inserts $(s_q, d_3, d_3)$ while it handles a path edge $(c, d_1, d_2)$, with $d_3 \in F_c(d_2)$ for the call edge. By induction, $\alpha \sigma$ reaches $\langle c, d_2 \rangle$. Add the call edge. It is never closed, so it is the last open call, and the new entry fact is $d_3$. $\sigma$ is now empty.
- L7 extends $\sigma$ for $(c, d_1, d_2)$ by the call-to-return edge, which is intraprocedural, or by a summary edge from $\langle c, d_2 \rangle$. By induction, the summary edge stands for a same-level path. Either way $\sigma$ stays same-level and the entry fact stays $d_1$.
- L14 extends $\sigma$ by one intraprocedural edge.
- L13 inserts $(r, d_3, d_5)$ from a path edge $(c, d_3, d_4)$ and a new summary edge $(c, d_4, d_5)$. Both are older, and the same argument as for L7 applies.
- L12 inserts $(c, d_4, d_5)$ when L10 meets a new triple $(c, d_1, d_5)$. At that time a path edge $(e_q, d_1, d_2)$ exists with $d_5 \in F(d_2)$ for the return edge of $c$, and L11 chose $d_4$ with $d_1 \in F(d_4)$ for the call edge of $c$. By induction, $\sigma$ for this path edge is a same-level path from $\langle s_q, d_1 \rangle$ to $\langle e_q, d_2 \rangle$. The call edge, $\sigma$ and the return edge of the same site $c$ form a same-level path. $\square$

**Lemma 4 (path edges are complete).** If a valid path $\pi$ of $G^\#$ goes from some $\langle s_{main}, d_0 \rangle$, $d_0 \in S \cup \{\mathbf{0}\}$, to $\langle n, d_2 \rangle$ and has the entry fact $d_1$, then $(n, d_1, d_2) \in \mathit{PE}$.

*Proof.* Strong induction on the number of edges of $\pi$. Every path edge that L16 inserts is put on the worklist, and the loop runs until the worklist is empty (L3). So every path edge in $\mathit{PE}$ is taken off once, at L4.

- $\pi$ is empty. Then $n = s_{main}$ and $d_1 = d_2 = d_0$, and L2 inserts the edge.
- The last edge is a call edge from $\langle c, d_4 \rangle$. The prefix is shorter and reaches $\langle c, d_4 \rangle$ with some entry fact $d'$, so $(c, d', d_4) \in \mathit{PE}$. When it is taken off, L6 inserts $(s_q, d_2, d_2)$, and $d_1 = d_2$.
- The last edge is intraprocedural, from $\langle m, d' \rangle$. The prefix is shorter and has the same entry fact $d_1$, so $(m, d_1, d') \in \mathit{PE}$. When it is taken off, L14 or (for a call-to-return edge) L7 inserts $(n, d_1, d_2)$.
- The last edge is a return edge $\langle e_q, d_2' \rangle \to \langle r, d_2 \rangle$ of a call site $c$. It must close an open call edge $\langle c, d_4 \rangle \to \langle s_q, d_1' \rangle$, so $\pi = \alpha \cdot \mathit{call} \cdot \beta \cdot \mathit{ret}$ with $\beta$ same-level. The path $\alpha \cdot \mathit{call} \cdot \beta$ is shorter and has the entry fact $d_1'$, so $(e_q, d_1', d_2') \in \mathit{PE}$. The path $\alpha$ is shorter and has the entry fact $d_1$, since $\mathit{call} \cdot \beta \cdot \mathit{ret}$ is same-level. So $(c, d_1, d_4) \in \mathit{PE}$.

  First, $(c, d_4, d_2) \in \mathit{SE}$. When $(e_q, d_1', d_2')$ is taken off, L9 looks at the site $c$ and at $d_2 \in F(d_2')$ for its return edge. If the triple $(c, d_1', d_2)$ is new, L11 runs over $\mathit{inv}_c(d_1')$, which contains $d_4$, and L12 inserts $(c, d_4, d_2)$ unless it is there already. If the triple is old, the run of L11 that added it did the same.

  Next, the path edge $(c, d_1, d_4)$ was inserted at some time $t_1$ and taken off at a later time $t_2$. The summary edge $(c, d_4, d_2)$ was inserted at a time $t_s$. If $t_s < t_2$, L7 sees the summary edge at $t_2$. If $t_s > t_1$, then $d_1$ is among the sources of $\langle c, d_4 \rangle$ at $t_s$, and L13 uses it. One of the two holds, since $t_1 < t_2$. Either way $(r, d_1, d_2)$ is inserted. $\square$

**Theorem (correctness).** At the end, for every node $n$, the set $X_n$ of line L15 is $\mathrm{MVP}(n)$.

*Proof.* By Lemma 3, every path edge $(n, d_1, d_2)$ gives a valid path to $\langle n, d_2 \rangle$, so $\langle n, d_2 \rangle \in \mathit{Reach}$. By the decomposition, every node of $\mathit{Reach}$ has a valid path with some entry fact, and Lemma 4 gives a path edge to it. So $\{ \langle n, d \rangle : (n, d_1, d) \in \mathit{PE} \text{ for some } d_1 \} = \mathit{Reach}$. Leave out $\mathbf{0}$ and use Corollary 2. $\square$

**Lemma 5 (termination).** The algorithm stops.

*Proof.* L16 inserts each path edge at most once, and there are at most $(D+1)^2$ of them per node. So the loop of L3 runs at most $\sum_n (D_{p(n)}+1)^2$ times. Each run does a finite amount of work, since each set it loops over is finite. $\square$

**Theorem (cost).** Let $N$ be the number of nodes of $G^*$, $E$ its number of edges, and $\mathit{Call}$ the number of call sites. With hash sets of constant expected cost per operation, the algorithm runs in $O(E D^3)$ time and uses $O(N D^2 + \mathit{Call}\, D^2)$ space.

*Proof.* Write $D' = D + 1$. Each PROPAGATE is $O(1)$. Count the work by the kind of node that the taken-off path edge ends in. A node has at most $D'^2$ path edges ending in it, and each is taken off once.

- An ordinary node $n$ with $\deg(n)$ successors. Each path edge gives at most $\deg(n) \cdot D'$ calls of PROPAGATE at L14. In total $D'^3 \deg(n)$. The sum over all nodes is at most $E D'^3$.
- A call node $c$. Each path edge gives at most $D'$ calls at L6, $D'$ at L7 for the call-to-return edge, and $D'$ at L7 for the summary edges, since $\mathit{SE}$ has at most $D'$ edges out of $\langle c, d_2 \rangle$. In total $3 D'^3$ per call site.
- An exit node $e_q$. Each path edge and each call site $c$ of $q$ give at most $D'$ tests at L10. In total $D'^3$ per call site, since each call site calls one procedure. A triple $(c, d_1, d_5)$ passes L10 only once, there are at most $D'^2$ of them per site, and each runs L11 over at most $D'$ facts: $D'^3$ per site. A summary edge is inserted at L12 only once, there are at most $D'^2$ per site, and each runs L13 over at most $D'$ sources: $D'^3$ per site.

The set $\mathit{inv}_c$ takes $O(D'^2)$ time per site to build. A call site has three edges in $E$, so $\mathit{Call} \le E$, and the total is $O(E D'^3) = O(E D^3)$, since $D \ge 1$. The path edges and their index of sources take $O(N D'^2)$ space. The summary edges, the triples and the sets $\mathit{inv}_c$ take $O(D'^2)$ per call site. $\square$

Without L10, the exit case would combine every path edge of $e_q$ with every $d_4 \in \mathit{inv}_c(d_1)$ and every source of $\langle c, d_4 \rangle$. That is $D'^4$ steps per call site in the worst case. The set of triples is what keeps this case at $D'^3$.
