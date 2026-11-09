---
title: The operations of a general BDD are correct
proves: [correctness]
status: full
---

A BDD $B$ has the terminals $0$ and $1$ and inner nodes $u$ with a variable $\mathrm{var}(u)$ and two children $\mathrm{lo}(u)$ and $\mathrm{hi}(u)$. Each child has a smaller id than its parent, so $B$ has no cycle. The function $f_u \in B_n$ of a node is defined by induction on the id: $f_0 = 0$, $f_1 = 1$, and

$$f_u = (\neg x_i \wedge f_{\mathrm{lo}(u)}) \vee (x_i \wedge f_{\mathrm{hi}(u)}), \qquad i = \mathrm{var}(u).$$

Nothing is assumed about the order of the variables on a path, so $f_{\mathrm{lo}(u)}$ and $f_{\mathrm{hi}(u)}$ may depend on $x_i$.

**Lemma 1 (EVAL).** For each node $u$ and each $x \in \{0,1\}^n$, EVAL$(u, x)$ returns $f_u(x)$ after at most $p$ steps of line L2, where $p$ is the number of nodes.

*Proof.* Each step of line L2 moves from a node to one of its children, so the ids on the walk decrease strictly and the walk ends at a terminal after fewer than $p$ steps. The value $f_u(x)$ does not change in a step: if $x_i = 1$, the definition gives $f_u(x) = f_{\mathrm{hi}(u)}(x)$, and line L2 moves to $\mathrm{hi}(u)$; if $x_i = 0$, it gives $f_u(x) = f_{\mathrm{lo}(u)}(x)$, and line L2 moves to $\mathrm{lo}(u)$. At a terminal $t$, $f_t(x)$ is the label of $t$, which line L3 returns. $\square$

**Lemma 2 (FROM-CNF).** For a CNF formula $F = C_1 \wedge \cdots \wedge C_m$, FROM-CNF returns a node $r$ with $f_r = F$. It makes one inner node per literal occurrence, so the result has at most $\ell + 2$ nodes, where $\ell$ is the number of literal occurrences.

*Proof.* Write $G_j = C_j \wedge \cdots \wedge C_m$, with $G_{m+1} = 1$. We show that at line L10 of the round for $j$, $f_t = G_j$. Then at line L11, $f_s = G_1 = F$. The base is line L4: $f_s = 1 = G_{m+1}$.

In the round for $j$, assume $f_s = G_{j+1}$, and let $C_j = \ell_1 \vee \cdots \vee \ell_k$. We claim that after the literals $\ell_k, \ldots, \ell_q$ are done, $f_t = (\ell_q \vee \cdots \vee \ell_k) \wedge G_{j+1}$. Before the first literal, line L6 gives $f_t = 0$, which is the empty disjunction times $G_{j+1}$. For a literal $\ell = \ell_q$, let $D = \ell_{q+1} \vee \cdots \vee \ell_k$, so that the old $t$ has $f_t = D \wedge G_{j+1}$. Lines L8 and L9 make a node whose function sends the inputs with $\ell = 1$ to $s$ and the other inputs to the old $t$. For $\ell = x_v$ this is line L8 with $\mathrm{hi} = s$, and for $\ell = \neg x_v$ it is line L9 with $\mathrm{lo} = s$. In both cases the new function is

$$(\ell \wedge G_{j+1}) \vee (\neg \ell \wedge D \wedge G_{j+1}) = G_{j+1} \wedge (\ell \vee (\neg \ell \wedge D)) = G_{j+1} \wedge (\ell \vee D).$$

After all $k$ literals, $f_t = C_j \wedge G_{j+1} = G_j$. An empty clause leaves $t$ at the terminal 0, which is correct because an empty clause is false. Each literal occurrence calls NODE once, and no other line makes a node. $\square$

**Lemma 3 (IS-FREE).** IS-FREE$(r)$ returns true if and only if no path from $r$ to a terminal tests a variable twice.

*Proof.* Line L12 visits the nodes reachable from $r$ in increasing order of id, so the children of a node are visited before it. By induction on this order, $D[u]$ at line L13 is the set of variables of the inner nodes reachable from $u$, with $u$ included. A terminal reaches no inner node. For an inner node, the reachable inner nodes are $u$ itself and those reachable from $\mathrm{lo}(u)$ or $\mathrm{hi}(u)$.

If line L14 returns false at $u$, then a node $w$ with $\mathrm{var}(w) = \mathrm{var}(u)$ is reachable from a child of $u$. Since $u$ is reachable from $r$, there is a path from $r$ to $u$, then to $w$, then to a terminal, and it tests $\mathrm{var}(u)$ twice. Conversely, let a path from $r$ test $x_i$ at a node $u$ and again at a node $w$ below $u$. Then $w$ is reachable from a child of $u$, so $i \in D[\mathrm{lo}(u)] \cup D[\mathrm{hi}(u)]$, and line L14 returns false at $u$ or at an earlier node. So line L15 is reached only when no path tests a variable twice. $\square$

**Lemma 4 (SAT-FREE).** If no path from $r$ tests a variable twice, then $f_r$ is satisfiable if and only if the terminal 1 is reachable from $r$.

*Proof.* If $f_r(x) = 1$, then by Lemma 1 the walk of EVAL$(r, x)$ ends at the terminal 1, so it is reachable. Conversely, let $P$ be a path from $r$ to the terminal 1. Each variable is tested at most once on $P$, so we can choose $x$ with $x_{\mathrm{var}(u)} = 1$ when $P$ leaves $u$ by its hi-edge and $x_{\mathrm{var}(u)} = 0$ when it leaves by its lo-edge. The other entries of $x$ are arbitrary. The walk of EVAL$(r, x)$ follows $P$ edge by edge, so it ends at 1, and $f_r(x) = 1$ by Lemma 1. $\blacksquare$

**Remark.** The free condition in Lemma 4 is needed. For $F = x_1 \wedge \neg x_1$, FROM-CNF returns a root that tests $x_1$ and goes by its hi-edge to a second node on $x_1$, whose lo-edge goes to the terminal 1. The terminal 1 is reachable, but $f_r = 0$: the only path to 1 asks for $x_1 = 1$ and then $x_1 = 0$.
