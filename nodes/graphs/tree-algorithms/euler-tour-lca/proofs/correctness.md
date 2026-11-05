---
title: LCA by Euler tour and RMQ returns the lowest common ancestor
proves: [correctness, termination]
status: full
---

Let the tree have the vertices $0, \ldots, n - 1$, $n \ge 1$, and the root $r$. Write $depth(x)$ for the number of edges from $r$ to $x$ and $T_x$ for the subtree of $x$, the set of descendants of $x$, including $x$. For vertices $u, v$, $w = \mathrm{lca}(u, v)$ is the deepest vertex with $u, v \in T_w$. The lines L1 to L12 are those of the pseudocode on the page.

**Lemma 1 (termination and the shape of the tour).** The loop of lines L2 to L6 ends after $2n - 1$ iterations. Each vertex $x$ is pushed exactly once, and the entries appended to $E$ while $x$ is on the stack, from index $first[x]$ up to the entry appended when $x$ is popped (exclusive), are exactly one entry for each time a vertex of $T_x$ is entered or returned to. In particular $E$ has $2n - 1$ entries and every entry in $E[first[x] .. last(x)]$ lies in $T_x$, where $last(x)$ is the index of the last entry written while $x$ is on the stack.

*Proof.* A vertex is pushed only in line L5, and only if it has not been entered before, so it is pushed at most once. Each iteration either pushes a vertex (line L5) or pops one (line L6), and a popped vertex is never pushed again, so there are at most $2n$ iterations and the loop ends. Every vertex is pushed: by induction on depth, a vertex $c$ with parent $v$ is pushed while $v$ is on top of the stack, because $v$ is popped only when it has no child left to enter. So there are $n$ pushes and $n$ pops. Each push appends one entry; each pop except the last (the root) appends one entry. That gives $n + (n - 1) = 2n - 1$ entries.

The stack always holds the path from $r$ to its top, since line L5 pushes a child of the top. While $x$ is on the stack, the top is a descendant of $x$, and every entry appended is either a pushed vertex, which is the new top, or the new top after a pop, which is still $x$ or a descendant of $x$ (the last pop with $x$ still on the stack leaves $x$ on top). So all entries from $first[x]$ until $x$ is popped are in $T_x$, and the entry written when $x$ is popped is its parent. $\square$

**Lemma 2 (the range lies in $T_w$).** Let $u, v$ be vertices with $first[u] \le first[v]$ and $w = \mathrm{lca}(u, v)$. Every entry of $E[first[u] .. first[v]]$ lies in $T_w$, so its depth is at least $depth(w)$.

*Proof.* Since $u, v \in T_w$, they are pushed while $w$ is on the stack (each is pushed after its parent, which by induction is after $w$, and before $w$ is popped, since $w$ is popped only after every vertex of $T_w$ has been entered). So $first[w] \le first[u] \le first[v] \le last(w)$, and by Lemma 1 every entry in that range lies in $T_w$. A vertex of $T_w$ has depth at least $depth(w)$. $\square$

**Lemma 3 (the range contains $w$).** Under the assumptions of Lemma 2, $w$ occurs in $E[first[u] .. first[v]]$.

*Proof.* If $u = w$, then $E[first[u]] = w$. If $v = w$, then $first[v] = first[w] \le first[u] \le first[v]$, so $u = v = w$. Otherwise $u \ne w \ne v$, and $u$ and $v$ lie in the subtrees of children $c_1$ and $c_2$ of $w$, with $c_1 \ne c_2$ because $w$ is the deepest common ancestor. Since $first[u] \le first[v]$ and the blocks of $T_{c_1}$ and $T_{c_2}$ are disjoint (each is written while its root is on the stack, and two siblings are never on the stack together), $c_1$ is entered and popped before $c_2$ is entered. When $c_1$ is popped, line L6 appends its parent $w$. That entry comes after $first[u]$, which lies in the block of $c_1$, and before $first[c_2] \le first[v]$. $\square$

**Lemma 4 (the minimum is unique).** Under the same assumptions, $w$ is the only vertex of depth at most $depth(w)$ in $E[first[u] .. first[v]]$.

*Proof.* By Lemma 2 every entry lies in $T_w$, and the only vertex of $T_w$ of depth $depth(w)$ is $w$; all others are deeper. $\square$

**Lemma 5 (the sparse table).** After lines L7 to L9, for every $k$ and $i$ with $i + 2^k \le |E|$, $M[k][i]$ is a vertex of least depth among $E[i], \ldots, E[i + 2^k - 1]$.

*Proof.* By induction on $k$. For $k = 0$, line L7 sets $M[0][i] = E[i]$. For $k \ge 1$, the range of length $2^k$ is the union of the ranges $E[i .. i + 2^{k-1} - 1]$ and $E[i + 2^{k-1} .. i + 2^k - 1]$, whose shallowest vertices are $M[k-1][i]$ and $M[k-1][i + 2^{k-1}]$ by induction; line L9 keeps the shallower one, which is a shallowest vertex of the union. $\square$

**Theorem.** For all vertices $u$ and $v$, LCA$(u, v)$ returns $\mathrm{lca}(u, v)$.

*Proof.* Line L10 sets $l \le h$ to the two first occurrences, so by symmetry we may assume $l = first[u]$ and $h = first[v]$. Let $m = h - l + 1 \ge 1$ and $k = \lfloor \lg m \rfloor$, so $2^k \le m < 2^{k+1}$. The blocks $E[l .. l + 2^k - 1]$ and $E[h - 2^k + 1 .. h]$ lie inside $E[l .. h]$, and they cover it, because $h - 2^k + 1 \le l + 2^k$ follows from $m < 2^{k+1}$. By Lemma 5, line L12 returns a vertex $x$ of least depth in the union, that is, of least depth in $E[l .. h]$. By Lemma 3, $w$ is in the range, so $depth(x) \le depth(w)$, and by Lemma 4, $x = w$. Each query does a fixed number of steps, so it ends. $\blacksquare$
