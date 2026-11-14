---
title: Lazy and hybrid cycle detection merge only nodes with equal least sets, so the result is Andersen's least solution
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set of $m$ statements in the four forms over $n$ variables, each variable also a location. $L$ is the least solution of the subset constraints of [Andersen's analysis](/andersen-analysis/): `p = &a` gives $a \in L(p)$, `p = q` gives $L(q) \subseteq L(p)$, `p = *q` gives $L(a) \subseteq L(p)$ for $a \in L(q)$, and `*p = q` gives $L(q) \subseteq L(a)$ for $a \in L(p)$. $L$ lies inside every solution. The solver keeps a union-find forest over the variables; $[v]$ is the root of the class of $v$, and each root $r$ has a set $pts(r)$, successors $succ(r)$, the loads and stores of its members, and the table entries $H$ of its members. The result is $S(v) = pts([v])$.

The *offline graph* has a node $v$ and a *ref node* $*v$ for each variable $v$, and the edges $q \to p$ for `p = q`, $*q \to p$ for `p = *q`, and $q \to *p$ for `*p = q`. For each strongly connected component $C$ of it with a ref node $*a$ and a variable node $b$, line L4 adds the entry $(b, R)$ to $H(a)$, where $R$ is the set of the pointers $c \ne a$ with $*c \in C$.

**Lemma 1 (a walk of the offline graph gives inclusions).** Let $\sigma$ map each variable node $v$ of the offline graph to $v$, and each ref node $*c$ to some location $\sigma(*c) \in L(c)$. Then for every offline edge $u \to w$, $L(\sigma(u)) \subseteq L(\sigma(w))$.

*Proof.* For a copy edge $q \to p$, this is the copy constraint. For a load edge $*q \to p$, $\sigma(*q) \in L(q)$, so the load constraint gives $L(\sigma(*q)) \subseteq L(p)$. For a store edge $q \to *p$, $\sigma(*p) \in L(p)$, so the store constraint gives $L(q) \subseteq L(\sigma(*p))$. $\square$

**Lemma 2 (every merge joins nodes with one least set).** At every moment, all members of a class have the same $L$, $pts(r) \subseteq L(r)$ for every root $r$, and every edge $r \to w$ of the solver has $L(r) \subseteq L(w)$.

*Proof.* The edges and the growth of the sets are those of Andersen's solver, with the loads and stores of a class read on its root, and they keep the last two parts as in the proof for [online cycle elimination](/online-cycle-elimination/). It remains to check the three kinds of merge.

- *Offline merges (line L2).* The members of a strongly connected component of the copy graph lie on cycles of copy constraints, so their $L$ is the same.
- *Hybrid merges (line L9).* Line L8 runs only when $pts([c]) \ne \emptyset$ for every $c \in R$, and line L9 merges $b$ with an $x \in pts(n)$, where $a$ is a member of the class $n$. Since the sets are inside $L$ and $L$ is the same on the class, $x \in L(a)$ and $L(c) \ne \emptyset$ for every $c \in R$. Let $\sigma(*a) = x$ and let $\sigma(*c)$ be any element of $L(c)$ for $c \in R$. The component $C$ has a path from $b$ to $*a$ and one from $*a$ back to $b$, and all their nodes are in $C$, so every ref node on them is $*a$ or $*c$ with $c \in R$. By Lemma 1, $L$ does not shrink along either path under $\sigma$, so $L(b) \subseteq L(x) \subseteq L(b)$.
- *Lazy merges (line L14).* The set $C$ holds the roots on some path from $w$ to $n$ in the solver's graph, and the edge $n \to w$ is in the graph. So every member of $C$ lies on a cycle of solver edges, and by the third part $L$ is the same on all of it. $\square$

The condition of line L8 is needed. In the statements `a = &x`, `b = &w`, `b = *a`, `*c = b`, `q = *c` and `*a = q`, the component $\{*a, b, *c, q\}$ gives the entry $(b, \{c\})$ for $a$, but $c$ has no target, so $L(x) = \emptyset$ and $L(b) = \{w\}$.

**Lemma 3 (what is done stays done).** Every root that is not on the worklist has, for every $a \in pts(r)$, the edges for the loads and stores of its class, and $pts(r) \subseteq pts(w)$ for every edge $r \to w$.

*Proof.* As for online cycle elimination: a root whose set grows is pushed, a root made by a merge is pushed, and an edge from a root that is not on the worklist is added with its set (in ADD-EDGE) or lies inside a merge. When a root is taken from the worklist, lines L10 to L15 add the edges for all its elements and send its set along all its edges, except along an edge whose ends line L14 merges, and that merged root is pushed again. $\square$

**Theorem 1 (correctness).** The algorithm stops, and $S = L$.

*Proof.* Each push comes from a set that grew or from a merge; there are at most $n$ growths per root and at most $n - 1$ merges, so the loop stops. Line L12 starts at most one search per ordered pair of variables, since it marks the pair. When the loop stops, every root meets Lemma 3, and as for Andersen's analysis this makes $S$ a solution, so $L \subseteq S$. By Lemma 2, $S(v) = pts([v]) \subseteq L([v]) = L(v)$. $\square$

The hybrid and lazy merges are only ways to store fewer sets. Missing one costs time, not precision: the proof does not need any merge to happen.

**Theorem 2 (time).** The offline part (lines L1 to L4) takes $O(n + m)$ time. With each find counted as one step, the solver takes $O(n^4 + n^2 m)$ time in the worst case and $O(n^2 + m)$ space.

*Proof.* The offline graph has $2n$ nodes and $m$ edges, and Tarjan's algorithm takes $O(n + m)$ time; the table has at most one entry per ref node and component. Each root is processed $O(n)$ times, as in the proof for online cycle elimination, which gives $O(n^2 m + n^4)$ for the edges and the transfers of sets. A class has at most $n$ table entries, each with at most $n$ pointers, so lines L8 and L9 cost $O(n^2)$ per processing, plus the cost of the real merges, of which there are at most $n - 1$ in all. With $O(n^2)$ processings, this is $O(n^4)$. There are at most $n^2$ lazy searches, each in $O(n + n^2)$ time. $\square$

The worst case is not the point of the method. Its gain is that it searches far less often than online cycle elimination, only on edges that already carry equal sets, and that the hybrid merges need no search at all.
