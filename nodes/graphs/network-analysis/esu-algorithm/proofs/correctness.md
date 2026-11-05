---
title: ESU outputs every connected induced subgraph of k vertices exactly once, and stops
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $V = \{0, \dots, n-1\}$, and $k \ge 1$. For $S \subseteq V$, let $N(S) = \{u \notin S : u \text{ has a neighbour in } S\}$ and $N[S] = S \cup N(S)$. A *call* is a call EXTEND($sub$, $ext$, $v$); for a call made at line L10 inside a call $c$, we say it is a *child* of $c$. The calls made at line L3 are the *roots*. Line L8 may remove the vertices of $ext$ in any order; the proof holds for every order.

**Lemma 1 (invariants).** Every call EXTEND($sub$, $ext$, $v$) satisfies:
(a) $G[sub]$ is connected, $v \in sub$, and every other vertex of $sub$ is larger than $v$;
(b) $ext \subseteq N(sub)$, and every vertex of $ext$ is larger than $v$;
(c) $|sub|$ is one more than the depth of the call, where a root has depth 0.

*Proof.* At line L3, $sub = \{v\}$ and $ext = \{u \in N(v) : u > v\} \subseteq N(\{v\})$, so (a), (b) and (c) hold. Let a call with $(sub, ext)$ satisfy them, and let it make a child at line L10 with the vertex $w$ removed at line L8. Write $R$ for the set $ext$ after the removal, so $R \subseteq ext \setminus \{w\}$, and $X = \{u \in N(w) : u > v,\ u \notin N[sub]\}$; the child has $sub' = sub \cup \{w\}$ and $ext' = R \cup X$.
(a) $w \in ext \subseteq N(sub)$, so $w \notin sub$ and $w$ has a neighbour in $sub$, so $G[sub']$ is connected; $w > v$ by (b).
(b) A vertex of $R$ is in $N(sub)$, so it is outside $sub$, differs from $w$, and has a neighbour in $sub \subseteq sub'$; so it is in $N(sub')$. A vertex $u \in X$ is adjacent to $w \in sub'$, is not in $sub$ since $u \notin N[sub]$, and is not $w$ since $G$ has no loops; so $u \in N(sub')$. Both kinds are larger than $v$.
(c) $|sub'| = |sub| + 1$. $\square$

**Lemma 2 (termination).** The run stops, and every output is a connected set of exactly $k$ vertices whose smallest vertex is the $v$ of its call.

*Proof.* By Lemma 1(c), a call at depth $k - 1$ has $|sub| = k$ and returns at line L6 without making children, so the depth is at most $k - 1$. Each call makes one child per pass of its loop, and each pass removes one vertex from the finite set $ext$ and adds none to it, so each call makes finitely many children. A finitely branching tree of bounded depth is finite. The second part is Lemma 1(a) at line L6. $\square$

**Lemma 3 (excluded vertices stay out).** Let a call $c$ with $(sub, ext)$ remove the vertex $w_j$ at line L8, and later, in the same call, remove $w_i$. Then no call in the subtree of the child of $w_i$ (that child included) has $w_j$ in its $sub$.

*Proof.* We show that every call $d$ in that subtree, with $(sub_d, ext_d)$, has $sub \subseteq sub_d$, $w_j \notin sub_d$ and $w_j \notin ext_d$. For the child of $w_i$: $sub_d = sub \cup \{w_i\}$ and $w_i \ne w_j$, and $w_j \notin sub$ since $w_j \in ext \subseteq N(sub)$. Its $ext_d = R \cup X$, where $R$ is what is left of $ext$ after $w_i$ was removed; $w_j$ was removed earlier, so $w_j \notin R$; and $w_j \in N(sub) \subseteq N[sub]$, so $w_j \notin X$. Now let $d$ satisfy the claim and let $d'$ be a child of $d$ with the vertex $w$ removed from $ext_d$. Then $w \ne w_j$ because $w_j \notin ext_d$, so $w_j \notin sub_{d'} = sub_d \cup \{w\}$. The set $ext_{d'}$ is a part of $ext_d$, which does not hold $w_j$, together with vertices outside $N[sub_d]$. Since $sub \subseteq sub_d$ and $w_j \in N(sub)$, either $w_j \in sub_d$, which is excluded, or $w_j \in N(sub_d)$; in both cases $w_j \in N[sub_d]$, so $w_j \notin ext_{d'}$. By induction on depth the claim holds in the whole subtree. $\square$

**Lemma 4 (at most once).** No two distinct calls have the same $sub$. In particular, no set is output twice.

*Proof.* Take two distinct calls $d_1$ and $d_2$. If they lie under different roots $\{v_1\}$ and $\{v_2\}$ with $v_1 \ne v_2$, their sets have the different smallest vertices $v_1$ and $v_2$ by Lemma 1(a). If one is an ancestor of the other, their sets have different sizes by Lemma 1(c). Otherwise let $c$ be their last common ancestor, and let $d_1$ lie under the child of $c$ made with $w_j$ and $d_2$ under the child made with $w_i$, where $w_j$ was removed first. By Lemma 1, the set of every call under the child of $w_j$ contains $sub_c \cup \{w_j\}$, since sets only grow along a branch; so $w_j \in sub_{d_1}$. By Lemma 3, $w_j \notin sub_{d_2}$. So $sub_{d_1} \ne sub_{d_2}$. $\square$

**Lemma 5 (at least once).** Every set $S \subseteq V$ with $|S| = k$ and $G[S]$ connected is output.

*Proof.* Let $v = \min S$. Call a call with $(sub, ext)$ and root $v$ *good* if $sub \subseteq S$ and $(S \setminus sub) \cap N(sub) \subseteq ext$. The root $\{v\}$ is good: every vertex of $S \setminus \{v\}$ is larger than $v$, so each one adjacent to $v$ is in $ext$ by line L2.

Let a call with $(sub, ext)$ be good and $|sub| < k$. Since $G[S]$ is connected and $\emptyset \ne sub \subsetneq S$, some edge of $G[S]$ joins $sub$ to $S \setminus sub$, so $(S \setminus sub) \cap N(sub)$ is not empty, and it is a part of $ext$. So the loop of lines L7 to L10 removes at least one vertex of $S$. Let $w_1, \dots, w_r$ be the vertices removed, in order, and $w_i$ the first one in $S$. Its child has $sub' = sub \cup \{w_i\} \subseteq S$ and $ext' = \{w_{i+1}, \dots, w_r\} \cup X$ with $X$ as in Lemma 1. Let $x \in (S \setminus sub') \cap N(sub')$.
- If $x \in N(sub)$, then $x \in ext$ because the call is good, so $x$ is some $w_l$. It is not $w_i$ since $x \notin sub'$, and not $w_l$ with $l < i$ since those are not in $S$. So $l > i$ and $x \in ext'$.
- If $x \notin N(sub)$, then $x \notin sub$, so $x \notin N[sub]$; and $x$ has a neighbour in $sub'$ but not in $sub$, so $x$ is adjacent to $w_i$. Also $x \in S \setminus \{v\}$, so $x > v$. Hence $x \in X \subseteq ext'$.

So the child is good and its $sub$ has one more vertex. Starting from the root and repeating, we reach a good call with $|sub| = k$ and $sub \subseteq S$, so $sub = S$, and line L6 outputs $S$. $\square$

**Theorem.** ESU($G$, $k$) stops and outputs exactly the sets $S \subseteq V$ with $|S| = k$ and $G[S]$ connected, each exactly once.

*Proof.* Lemma 2 gives termination and shows that every output is such a set. Lemma 5 shows that every such set is output, and Lemma 4 that it is output only once. $\square$

**Corollary (the size of the tree).** By Lemma 4 and Lemma 1(a), the calls of EXTEND have distinct connected sets $sub$ of at most $k$ vertices, so there are at most $s$ of them, where $s$ is the number of such sets in $G$. Each pass of line L8 makes one call, so the number of passes is also at most $s$.

∎
