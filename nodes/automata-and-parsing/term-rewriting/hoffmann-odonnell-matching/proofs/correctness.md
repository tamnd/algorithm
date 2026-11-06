---
title: The bottom-up matching automaton computes exactly the match sets
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ for the subterm at $p$, and substitutions $\sigma$. The patterns are $p_1, \ldots, p_F$. For a term $l$, $lin(l)$ is $l$ with each variable occurrence replaced by a new variable, all distinct. A pattern $l$ **matches** $u$ if $l\sigma = u$ for some $\sigma$; variables of the subject are treated as constants.

**The pattern forest.** Write $v$ for one wildcard symbol. For a term $l$, let $\bar l$ be $l$ with every variable replaced by $v$. Line L1 builds $PF$, the set of all $\bar q$ for subterms $q$ of the patterns; it contains $v$ when some pattern has a variable, and the code always adds $v$ (id 0). Say that a member $w$ of $PF$ **fits** a term $u$ if $w = v$, or $w = f(w_1, \ldots, w_k)$, $u = f(u_1, \ldots, u_k)$ with the same $f$ and $k$, and each $w_i$ fits $u_i$.

**Lemma 1.** For a term $l$ and a subject term $u$, $\bar l$ fits $u$ if and only if $lin(l)$ matches $u$.

*Proof.* Induction on $l$. If $l$ is a variable, $\bar l = v$ fits every $u$, and $lin(l)$ is a variable, which matches every $u$. If $l = f(l_1, \ldots, l_k)$, then $lin(l) = f(lin(l_1), \ldots, lin(l_k))$ up to renaming, with the variables of the arguments pairwise disjoint. It matches $u$ iff $u = f(u_1, \ldots, u_k)$ and each $lin(l_i)$ matches $u_i$, because the matchers of the arguments have disjoint domains and combine into one substitution. By the induction hypothesis this holds iff each $\bar l_i$ fits $u_i$, that is, iff $\bar l$ fits $u$. $\blacksquare$

For a subject term $u$, its **match set** is $MS(u) = \{ w \in PF : w \text{ fits } u \}$.

**Lemma 2 (one step).** For $u = f(u_1, \ldots, u_k)$, $MS(u) = \{v\} \cup \{ f(w_1, \ldots, w_k) \in PF : w_i \in MS(u_i) \text{ for all } i \}$. For a subject variable or a symbol $f/k$ that no member of $PF$ has at the root, $MS(u) = \{v\}$.

*Proof.* This is the definition of "fits", restricted to the members of $PF$. A member other than $v$ fits $u$ only if its root is the root symbol of $u$ with the same arity, and a subject variable is not the root of any member. $\blacksquare$

The function $\delta_f(M_1, \ldots, M_k) = \{v\} \cup \{ f(w_1, \ldots, w_k) \in PF : w_i \in M_i \}$ is what line L5 computes.

**Lemma 3 (preprocessing).** The loop of lines L3 to L6 stops. When it stops, the set $S$ of states contains $\{v\}$ and is closed under every $\delta_f$: for every symbol $f/k$ at the root of a member of $PF$ and all $M_1, \ldots, M_k \in S$, the table entry $T_f[M_1, \ldots, M_k]$ is defined and equals $\delta_f(M_1, \ldots, M_k) \in S$.

*Proof.* Every state is a subset of $PF$, and $S$ has no repeated sets, so $|S| \le 2^{|PF|}$. Each round either adds an entry to a table or makes no change. The number of possible entries is at most $\sum_f |S|^{k_f}$, which is bounded, so the loop stops after finitely many rounds. In the last round no tuple of states lacks an entry, for every symbol, so every entry is defined; each entry was set to $\delta_f$ of its tuple and added to $S$ (line L6). The state $\{v\}$ is added before the loop. $\blacksquare$

**Theorem.** For every subject $t$ and every position $p$ of $t$, lines L8 to L10 give $p$ the state $MS(t|_p)$. Lines L11 and L12 report the pair $(p, j)$ if and only if $p_j$ matches $t|_p$.

*Proof.* The loop of line L8 handles a node after all its children (a node is pushed again below its children, and handled when it is popped the second time, or at once if it is a leaf). By induction on the height of $t|_p$:

- If $t|_p$ is a variable, or its symbol $f/k$ has no table, line L9 or line L10 gives $\{v\}$, which is $MS(t|_p)$ by Lemma 2.
- Else $t|_p = f(u_1, \ldots, u_k)$, and its children have the states $MS(u_i) \in S$ by the induction hypothesis. By Lemma 3 the entry $T_f[MS(u_1), \ldots, MS(u_k)]$ is defined and equals $\delta_f(MS(u_1), \ldots, MS(u_k))$, which is $MS(t|_p)$ by Lemma 2. A constant is the case $k = 0$.

Line L7 lists, for each state $M$, the patterns $j$ with $\bar p_j \in M$. So line L11 offers $j$ at $p$ iff $\bar p_j$ fits $t|_p$, iff $lin(p_j)$ matches $t|_p$ (Lemma 1). If $p_j$ is linear, $lin(p_j)$ is $p_j$ up to renaming, and the pair is reported. If not, line L12 reports it iff the full matcher finds $\sigma$ with $p_j\sigma = t|_p$. In both cases the pair is reported iff $p_j$ matches $t|_p$: one direction is the check itself, and if $p_j$ matches $t|_p$ then $lin(p_j)$ matches it too, so line L11 offers it. Each pair $(p, j)$ is considered once, because each node has one state and each state lists $j$ at most once. $\blacksquare$

**Remark.** Lemma 3 does not need the closure to be computed by rounds. Any order that sets $T_f$ on every tuple of reachable states gives the same states and tables, because $\delta_f$ depends only on its arguments. The reachable states are exactly the match sets of ground terms over the symbols, together with $\{v\}$, by induction on the round in which a state is first added.
