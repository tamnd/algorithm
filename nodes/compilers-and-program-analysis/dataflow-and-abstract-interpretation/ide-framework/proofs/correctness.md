---
title: The IDE algorithm computes the meet over all valid paths for linear constant propagation in O(E D^3) time
proves: [correctness, termination]
status: full
---

**Setting.** $G^*$ is the supergraph of the program, as on the page. Every procedure $p$ has a start node $s_p$ and an exit node $e_p$. A call site has a call node $c$ in some procedure, a return site $r$ and three edges: the call edge $c \to s_q$, the return edge $e_q \to r$ and the call-to-return edge $c \to r$. The facts of $p$ form a finite set $D_p$, and $D = \max_p |D_p|$. $\mathbf{0}$ is a new fact that is in no $D_p$.

The values form the flat lattice $L = \{\top\} \cup \mathbb{Z} \cup \{\bot\}$, with $\bot \sqsubseteq k \sqsubseteq \top$ for every integer $k$ and no order between two integers. The meet is $\sqcap$. This is the meet convention of Kildall: the start value is $\top$ and the result is the greatest solution. In the join convention of Cousot the order flips and the same result is the least solution.

A *micro-function* is one of the forms of the page: $\lambda l.\top$, $\lambda l.\bot$, $\lambda l.k$, $\lambda l.\, a l + b$ with $a \ne 0$, and the point function that maps $l_0$ to $v$ and every other value to $\bot$. All forms map $\top$ to $\top$, the line maps $\bot$ to $\bot$, and the constant maps $\bot$ to $k$. Let $F$ be the set of these functions. Three facts about $F$ are used below, and the tests of the implementation check each of them by brute force on sample points.

- (F1) $F$ is closed under the pointwise meet and under composition, and `meet_fn` and `compose` compute them exactly. For example, the meet of $\lambda l.k$ and $\lambda l.\, a l + b$ agrees with both at $l_0 = (k - b)/a$ when this is an integer, and gives $\bot$ at every other value. So it is the point function $l_0 \mapsto k$, or $\lambda l.\bot$ when $l_0$ is not an integer. The other cases are the same kind of algebra.
- (F2) Every $f \in F$ is distributive: $f(x \sqcap y) = f(x) \sqcap f(y)$. If one of $x, y$ is $\top$, this follows from $f(\top) = \top$. If $x = y$, it is clear. Otherwise $x \sqcap y = \bot$, and $f(\bot)$ is $\bot$, or $k$ when $f$ is the constant $k$, in which case $f(x) = f(y) = k$. So $f$ is also monotone.
- (F3) Each function has one form, and a strictly falling chain in $F$ has at most four elements: $\lambda l.\top$, then a constant or a line, then a point function, then $\lambda l.\bot$. The meet of two different constants, lines or points is lower in this list, and nothing is between $\lambda l.\top$ and the constants and lines.

By (F3), the meet of any set of functions of $F$, even an infinite set, is the meet of a finite subset, so it is in $F$ and it is the pointwise meet. The same holds in $L$, which has height 2.

Every edge $e = (n, m)$ of $G^*$ and every pair $d \in D_n \cup \{\mathbf{0}\}$, $d' \in D_m \cup \{\mathbf{0}\}$ have a micro-function $\varphi_e(d, d')$. The function is $\lambda l.\top$ when there is no exploded edge, and $\varphi_e(\mathbf{0}, \mathbf{0})$ is the identity. An *environment* $\rho$ maps the facts of a procedure to $L$, with $\rho(\mathbf{0}) = \bot$. The edge $e$ has the environment transformer

$$t_e(\rho)(d') = \mathop{\large\sqcap}_{d} \varphi_e(d, d')(\rho(d)).$$

For a path $\pi = e_1 \dots e_k$, $t_\pi = t_{e_k} \circ \dots \circ t_{e_1}$. The start environment $\rho_0$ gives $\bot$ to $\mathbf{0}$, the seed value or $\bot$ to each parameter of main, and $\top$ to the other variables of main. *Valid* and *same-level* paths are defined by matched brackets, as for IFDS. The meet over all valid paths is

$$\mathrm{MVP}(n)(d) = \mathop{\large\sqcap} \{ t_\pi(\rho_0)(d) : \pi \text{ a valid path from } s_{main} \text{ to } n \}.$$

The *exploded supergraph* $G^\#$ has a node $\langle n, d \rangle$ for every node $n$ and fact $d$, and an edge $\langle n, d \rangle \to \langle m, d' \rangle$ labelled $\varphi_e(d, d')$ for every edge $e = (n, m)$ with $\varphi_e(d, d') \ne \lambda l.\top$. For a path $\sigma$ of $G^\#$, $\varphi_\sigma$ is the composition of its labels, and the identity for the empty path. No label is $\lambda l.\top$, and a composition is $\lambda l.\top$ only if one of its parts is. So $\varphi_\sigma \ne \lambda l.\top$.

We use the lines L1 to L23 of the pseudocode. $J(n, d_1, d_2)$ is the jump function of $(n, d_1, d_2)$, $T(c, d_1, d_5)$ is the function of line L10, $S(c, d_4, d_5)$ is the summary function, and $\mathrm{val}(n, d)$ is the value of Phase II. A missing function is $\lambda l.\top$, and a missing value is $\top$.

**Lemma 1 (one path, many facts).** For a path $\pi$ of $G^*$ from $n$ to $m$, an environment $\rho$ and a fact $d'$,

$$t_\pi(\rho)(d') = \mathop{\large\sqcap} \{ \varphi_\sigma(\rho(d)) : \sigma \text{ a path of } G^\# \text{ that follows } \pi \text{ from some } \langle n, d \rangle \text{ to } \langle m, d' \rangle \}.$$

*Proof.* Induction on the length of $\pi$. For the empty path the only $\sigma$ is the empty path from $\langle n, d' \rangle$, and both sides are $\rho(d')$. Let $\pi = \pi' e$. By induction and by (F2),

$$t_\pi(\rho)(d') = \mathop{\large\sqcap}_d \varphi_e(d, d')\Big(\mathop{\large\sqcap}_{\sigma'} \varphi_{\sigma'}(\rho(d_0))\Big) = \mathop{\large\sqcap}_d \mathop{\large\sqcap}_{\sigma'} \varphi_e(d, d')(\varphi_{\sigma'}(\rho(d_0))),$$

where $\sigma'$ runs over the paths that follow $\pi'$ and end at $\langle \cdot, d \rangle$. An empty meet is $\top$, and every micro-function maps $\top$ to $\top$, so empty meets do no harm. A term with $\varphi_e(d, d') = \lambda l.\top$ is $\top$ and drops out. The other terms are exactly the paths $\sigma = \sigma' e$ of $G^\#$. $\square$

The brackets of a path of $G^\#$ are those of its shadow in $G^*$. So Lemma 1 gives:

**Corollary 2.** $\mathrm{MVP}(n)(d)$ is the meet of $\varphi_\rho(\rho_0(d_0))$ over all valid paths $\rho$ of $G^\#$ from some $\langle s_{main}, d_0 \rangle$ to $\langle n, d \rangle$.

A path that starts at $\langle s_{main}, d_0 \rangle$ for a variable $d_0$ of main that is not a parameter has the value $\top$ and drops out. So from now on $d_0$ is $\mathbf{0}$ or a parameter of main.

**Decomposition.** Cut a valid path of $G^\#$ from $\langle s_{main}, d_0 \rangle$ at its last call edge that is never closed. This gives $\alpha \cdot \sigma$, where $\alpha$ is empty or ends with that call edge, and $\sigma$ is a same-level path from some $\langle s_p, d_1 \rangle$. We call $\alpha$ an *entry path* to $\langle s_p, d_1 \rangle$ and $d_1$ the *entry fact*. Let

$$\mathrm{SL}(n, d_1, d_2) = \mathop{\large\sqcap} \{ \varphi_\sigma : \sigma \text{ same-level from } \langle s_p, d_1 \rangle \text{ to } \langle n, d_2 \rangle \}, \qquad \mathrm{EN}(p, d_1) = \mathop{\large\sqcap} \{ \varphi_\alpha(\rho_0(d_0)) : \alpha \text{ an entry path to } \langle s_p, d_1 \rangle \}.$$

By Corollary 2, (F2) and the remark after (F3),

$$\mathrm{MVP}(n)(d_2) = \mathop{\large\sqcap}_{d_1} \mathrm{SL}(n, d_1, d_2)(\mathrm{EN}(p, d_1)). \qquad (\ast)$$

**Phase I.**

**Lemma 3 (Phase I is sound).** Every function that the algorithm stores as $J(n, d_1, d_2)$ is a finite meet of $\varphi_\sigma$ over same-level paths $\sigma$ from $\langle s_p, d_1 \rangle$ to $\langle n, d_2 \rangle$. Every $T(c, d_1, d_5)$ is a finite meet of $g \circ \varphi_\sigma$, where $\sigma$ is same-level from $\langle s_q, d_1 \rangle$ to some $\langle e_q, d_2 \rangle$ and $g$ is the label of a return edge $\langle e_q, d_2 \rangle \to \langle r, d_5 \rangle$ of the site $c$. Every $S(c, d_4, d_5)$ is a finite meet of $\varphi_\tau$ over same-level paths $\tau$ from $\langle c, d_4 \rangle$ to $\langle r, d_5 \rangle$ that start with the call edge of $c$ and end with its return edge. So, at every time, $J \sqsupseteq \mathrm{SL}$.

*Proof.* Induction on time. A new value is the meet of the old value and one new term, so it is enough to look at the terms. By (F2) and the pointwise meet, $g \circ (f_1 \sqcap f_2) = (g \circ f_1) \sqcap (g \circ f_2)$ and $(f_1 \sqcap f_2) \circ h = (f_1 \circ h) \sqcap (f_2 \circ h)$, so a composition of finite meets of path functions is a finite meet of the functions of the joined paths.

- L2 and L6 give the identity to $(s, d, d)$, the function of the empty path.
- L7 and L14 give $g \circ J(n, d_1, d_2)$ for an exploded edge with label $g$. The joined paths are same-level.
- L7 also gives $S(c, d_2, d_3) \circ J(c, d_1, d_2)$, and L13 gives $S(c, d_4, d_5) \circ J(c, d_3, d_4)$. A same-level path followed by a call, a same-level path in the callee and the matching return is same-level.
- L10 gives $g \circ J(e_q, d_1, d_2)$ for a return edge of $c$ with label $g$.
- L12 gives $T(c, d_1, d_5) \circ h$ for a call edge $\langle c, d_4 \rangle \to \langle s_q, d_1 \rangle$ with label $h$. $\square$

A key $(n, d_1, d_2)$ *exists* once $J(n, d_1, d_2) \ne \lambda l.\top$. Every key is put on the worklist when its function changes, unless it is on the worklist already, and L4 reads the current function when it takes the key off. Also, L4 takes the key off the worklist before the key can be added again. So every key that exists at the end was taken off at least once after its last change, and at that time L5 to L14 saw its final function. Write $J$, $T$, $S$ for the final functions. Since stored functions only go down, this gives the following constraints at the end.

- (C1) For every exploded edge $\langle n, d_2 \rangle \to \langle m, d_3 \rangle$ with label $g$ that is intraprocedural or a call-to-return edge, $J(m, d_1, d_3) \sqsubseteq g \circ J(n, d_1, d_2)$ when $(n, d_1, d_2)$ exists.
- (C2) If $(c, d_1, d_2)$ exists and the call edge of $c$ goes from $\langle c, d_2 \rangle$ to $\langle s_q, d_3 \rangle$, then $J(s_q, d_3, d_3) \sqsubseteq \mathrm{id}$.
- (C3) If $(e_q, d_1, d_2)$ exists, then $T(c, d_1, d_5) \sqsubseteq g \circ J(e_q, d_1, d_2)$ for every call site $c$ of $q$ and every return edge $\langle e_q, d_2 \rangle \to \langle r, d_5 \rangle$ of $c$ with label $g$.
- (C4) $S(c, d_4, d_5) \sqsubseteq T(c, d_1, d_5) \circ h$ for every call edge $\langle c, d_4 \rangle \to \langle s_q, d_1 \rangle$ with label $h$. When L10 lowers $T$, L11 and L12 meet $S$ with the new $T \circ h$ at once. When $T$ does not change, the old step still holds.
- (C5) $J(r, d_3, d_5) \sqsubseteq S(c, d_4, d_5) \circ J(c, d_3, d_4)$ whenever $(c, d_3, d_4)$ exists.

*Proof of (C5).* Let $t_S$ be the time when $S(c, d_4, d_5)$ got its final value, $t_J$ the time of the last change of $J(c, d_3, d_4)$, and $t_P > t_J$ the time of the last removal of $(c, d_3, d_4)$ from the worklist. If $t_P > t_S$, then L7 sees the final $S$ and the final $J$ at $t_P$. If $t_P < t_S$, then $t_J < t_S$, so at $t_S$ the key already exists, $d_3$ is among the sources of $\langle c, d_4 \rangle$, and L13 meets $J(r, d_3, d_5)$ with $S \circ J$ for the final $S$ and $J$. $\square$

**Lemma 4 (Phase I is complete).** Let $\alpha \sigma$ be a valid path of $G^\#$ from some $\langle s_{main}, d_0 \rangle$, where $d_0$ is $\mathbf{0}$ or a parameter of main, cut as in the decomposition, with $\sigma$ from $\langle s_p, d_1 \rangle$ to $\langle n, d_2 \rangle$. Then at the end $J(n, d_1, d_2) \sqsubseteq \varphi_\sigma$. In particular the key exists.

*Proof.* Strong induction on the length of $\alpha \sigma$.

- $\sigma$ is empty. If $\alpha$ is empty, L2 gives the identity to $(s_{main}, d_0, d_0)$. Otherwise $\alpha$ ends with a call edge from $\langle c, d_4 \rangle$ to $\langle s_p, d_1 \rangle$, and the path without this edge is shorter. By induction, the key of $c$ for this shorter path exists, and (C2) gives $J(s_p, d_1, d_1) \sqsubseteq \mathrm{id}$.
- The last edge of $\sigma$ is intraprocedural or a call-to-return edge with label $g$, from $\langle m, d' \rangle$. By induction $J(m, d_1, d') \sqsubseteq \varphi_{\sigma'}$, where $\sigma'$ is $\sigma$ without its last edge. By (C1) and (F2), $J(n, d_1, d_2) \sqsubseteq g \circ J(m, d_1, d') \sqsubseteq g \circ \varphi_{\sigma'} = \varphi_\sigma$.
- The last edge of $\sigma$ is a return edge. Then $\sigma = \sigma_1 \cdot \mathit{call} \cdot \sigma_2 \cdot \mathit{ret}$, where the call edge goes from $\langle c, d_4 \rangle$ to $\langle s_q, d_1' \rangle$ with label $h$, $\sigma_2$ is same-level from $\langle s_q, d_1' \rangle$ to $\langle e_q, d_2' \rangle$, and the return edge has label $g$. The path $\alpha \sigma_1 \cdot \mathit{call} \cdot \sigma_2$ is shorter and has the entry fact $d_1'$, so $J(e_q, d_1', d_2') \sqsubseteq \varphi_{\sigma_2}$. The path $\alpha \sigma_1$ is shorter, so $J(c, d_1, d_4) \sqsubseteq \varphi_{\sigma_1}$. By (C3), (C4) and (C5),

  $$J(n, d_1, d_2) \sqsubseteq S(c, d_4, d_2) \circ J(c, d_1, d_4) \sqsubseteq g \circ J(e_q, d_1', d_2') \circ h \circ J(c, d_1, d_4) \sqsubseteq g \circ \varphi_{\sigma_2} \circ h \circ \varphi_{\sigma_1} = \varphi_\sigma.$$

  Each step uses that composition is monotone in both places, which holds by (F2). $\square$

**Corollary 5.** If some entry path reaches $\langle s_p, d_1 \rangle$, then $J(n, d_1, d_2) = \mathrm{SL}(n, d_1, d_2)$ at the end, for every $n$ in $p$ and every $d_2$. Otherwise no key $(n, d_1, d_2)$ exists.

*Proof.* The first part is Lemma 3 and Lemma 4, with the remark after (F3) for the infinite meet. For the second part, a key with the source $d_1$ is first made by L2 or L6, and both need an entry path to $\langle s_p, d_1 \rangle$, by Lemma 3 applied to the key of the call node. $\square$

**Phase II.**

By Corollary 5, Phase II works with $J = \mathrm{SL}$. Let $\mathcal{K}$ be the set of start nodes and call nodes.

**Lemma 6 (Phase II is sound).** Every value that L23 stores as $\mathrm{val}(n, d)$ with $n \in \mathcal{K}$ is a finite meet of values $\varphi_\rho(\rho_0(d_0))$ of valid paths $\rho$ of $G^\#$ to $\langle n, d \rangle$. So $\mathrm{val}(n, d) \sqsupseteq \mathrm{MVP}(n)(d)$.

*Proof.* Induction on time. L15 uses the empty path. L18 applies $J(m, d, d_2)$, a finite meet of same-level path functions, to a finite meet of values of valid paths to $\langle s_p, d \rangle$. By (F2) the result is a finite meet of values of the joined paths, and a valid path followed by a same-level path is valid. L19 appends a call edge to a valid path, and the result is valid. $\square$

The Phase II worklist has the same property as the Phase I worklist: each pair is taken off after its last change. So at the end of L19 the values satisfy the following constraints.

- (V1) $\mathrm{val}(s_{main}, d_0) \sqsubseteq \rho_0(d_0)$ for $\mathbf{0}$ and the parameters of main.
- (V2) $\mathrm{val}(m, d_2) \sqsubseteq J(m, d, d_2)(\mathrm{val}(s_p, d))$ for every $m \in \{s_p\} \cup \mathrm{calls}(p)$ and every key $(m, d, d_2)$.
- (V3) $\mathrm{val}(s_q, d_3) \sqsubseteq h(\mathrm{val}(c, d))$ for every call edge $\langle c, d \rangle \to \langle s_q, d_3 \rangle$ with label $h$.

**Lemma 7 (Phase II is complete on $\mathcal{K}$).** For every valid path $\rho$ of $G^\#$ from some $\langle s_{main}, d_0 \rangle$ to $\langle n, d \rangle$ with $n \in \mathcal{K}$, $\mathrm{val}(n, d) \sqsubseteq \varphi_\rho(\rho_0(d_0))$.

*Proof.* Induction on the number $k$ of call edges of $\rho$ that are never closed. Cut $\rho = \alpha \sigma$, with $\sigma$ from $\langle s_p, d_1 \rangle$. First we show $\mathrm{val}(s_p, d_1) \sqsubseteq \varphi_\alpha(\rho_0(d_0))$. If $k = 0$, then $\alpha$ is empty and (V1) gives it. If $k > 0$, then $\alpha = \alpha' \cdot \mathit{call}$, where the call edge goes from $\langle c, d_4 \rangle$ to $\langle s_p, d_1 \rangle$ with label $h$. The path $\alpha'$ ends at a call node and has $k - 1$ open calls, so by induction $\mathrm{val}(c, d_4) \sqsubseteq \varphi_{\alpha'}(\rho_0(d_0))$, and (V3) with (F2) gives the claim. Now $n$ is $s_p$ or a call node of $p$, so by (V2), Lemma 4 and (F2),

$$\mathrm{val}(n, d) \sqsubseteq J(n, d_1, d)(\mathrm{val}(s_p, d_1)) \sqsubseteq \varphi_\sigma(\varphi_\alpha(\rho_0(d_0))) = \varphi_\rho(\rho_0(d_0)). \qquad \square$$

**Theorem (correctness).** At the end, $\mathrm{val}(n, d) = \mathrm{MVP}(n)(d)$ for every node $n$ and every fact $d$. So the result $V$ of line L21 is the meet over all valid paths.

*Proof.* For $n \in \mathcal{K}$, this is Lemma 6, Lemma 7 and Corollary 2. For another node $n$ of $p$, L20 sets

$$\mathrm{val}(n, d_2) = \mathop{\large\sqcap}_{d_1} J(n, d_1, d_2)(\mathrm{val}(s_p, d_1)) = \mathop{\large\sqcap}_{d_1} \mathrm{SL}(n, d_1, d_2)(\mathrm{MVP}(s_p)(d_1)).$$

Keys that do not exist give $\top$ and drop out. We show that the right side is $\mathrm{MVP}(n)(d_2)$. Every entry path to $\langle s_p, d_1 \rangle$ is a valid path, so $\mathrm{MVP}(s_p)(d_1) \sqsubseteq \mathrm{EN}(p, d_1)$, and by $(\ast)$ and monotonicity the right side is at most $\mathrm{MVP}(n)(d_2)$. For the other direction, $(\ast)$ for $s_p$ gives $\mathrm{MVP}(s_p)(d_1) = \mathop{\large\sqcap}_{d_1'} \mathrm{SL}(s_p, d_1', d_1)(\mathrm{EN}(p, d_1'))$. A same-level path to $\langle s_p, d_1 \rangle$ followed by one from $\langle s_p, d_1 \rangle$ to $\langle n, d_2 \rangle$ is same-level, so $\mathrm{SL}(n, d_1, d_2) \circ \mathrm{SL}(s_p, d_1', d_1) \sqsupseteq \mathrm{SL}(n, d_1', d_2)$. With (F2), the right side is at least $\mathop{\large\sqcap}_{d_1'} \mathrm{SL}(n, d_1', d_2)(\mathrm{EN}(p, d_1')) = \mathrm{MVP}(n)(d_2)$. $\square$

**Lemma 8 (termination).** The algorithm stops.

*Proof.* By (F3), each $J$, $T$ and $S$ changes at most three times. There are finitely many keys, and each change puts at most one key on the worklist. So Phase I takes finitely many keys off the worklist, and each removal does a finite amount of work. In Phase II each value changes at most twice, from $\top$ to an integer and from there to $\bot$. So each pair enters the worklist at most twice. L20 is one pass over the keys. $\square$

**Theorem (cost).** Let $N$ be the number of nodes of $G^*$, $E$ its number of edges and $C$ its number of call sites. Assume that the meet, the composition and the application of micro-functions take constant time, as they do with integers of bounded size, and use hash tables with constant expected cost per operation. Then the algorithm runs in $O(E D^3)$ time and uses $O(N D^2 + C D^2)$ space.

*Proof.* Write $D' = D + 1$. A node has at most $D'^2$ keys, and each is taken off at most three times, once per change.

- An ordinary node $n$ with $\deg(n)$ successors gives at most $\deg(n) D'$ calls of PROPAGATE per removal. In total $3 D'^3 \deg(n)$, and $O(E D'^3)$ over all nodes.
- A call node gives at most $3 D'$ calls per removal at L6 and L7, since a pair $(c, d_2)$ has at most $D'$ summary functions. In total $9 D'^3$ per call site.
- An exit node gives at most $D'$ meets at L10 per removal and per call site. In total $3 D'^3$ per call site, since each call site calls one procedure. Each $T(c, d_1, d_5)$ changes at most three times, there are $D'^2$ of them per site, and each change runs L11 over at most $D'$ facts: $3 D'^3$ per site. Each $S(c, d_4, d_5)$ changes at most three times, and each change runs L13 over at most $D'$ sources: $3 D'^3$ per site.
- Phase II takes each pair at a start node or a call node off at most twice. A start node of $p$ runs L18 over at most $(1 + \mathrm{calls}(p)) D'$ keys per removal, which is $O((N + C) D'^2)$ in total. A call node runs L19 over at most $D'$ facts per removal, which is $O(C D'^2)$. L20 is one pass over at most $N D'^2$ keys.

A call site has three edges in $E$, so $C \le E$, and the total is $O(E D'^3) = O(E D^3)$. The keys, their functions and the source and target indexes take $O(N D'^2)$ space. The summary functions, the functions $T$ and the inverse call maps take $O(D'^2)$ per call site, and the values take $O(N D')$. $\square$

Without the functions $T$, the exit case would compose every key of $e_q$ with every call edge into $\langle s_q, d_1 \rangle$ and with every source of the call node. That is $D'^4$ steps per call site in the worst case. The functions $T$ keep this case at $D'^3$.
