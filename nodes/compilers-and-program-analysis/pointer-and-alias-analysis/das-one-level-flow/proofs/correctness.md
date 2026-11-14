---
title: One-level flow gives a solution of the subset constraints, so its sets contain Andersen's, in O(n (n + m)) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set of $m$ statements in the four forms over $n$ variables, each variable also a location. $L$ is the least solution of the subset constraints of [Andersen's analysis](/andersen-analysis/); it lies inside every solution. The algorithm keeps a union-find forest of value nodes. At the end, for a node $u$ write $[u]$ for its root, $base(u)$ for the base set of $[u]$, and $D(u)$ for the root of the deref node of $[u]$, when there is one. The flow edges are read on the roots: an edge recorded as $(u, v)$ is the edge $[u] \to [v]$. The result is

$$S(x) = C([V(x)]), \qquad C(r) = \bigcup \{ base(w) : w \to^* r \},$$

the union of the base sets of all roots that reach $r$ along flow edges, $r$ included.

**Lemma 1 (merges keep derefs together).** If two nodes $u$ and $u'$ end in one class and both classes had a deref node at some moment, those deref nodes end in one class. If $u$ had a deref node $d$ at some moment, then $[u]$ has a deref node at the end and $D(u) = [d]$.

*Proof.* A deref is set only on a root with none (line L9), or in UNIFY. When UNIFY merges roots $x$ and $y$ with derefs $d_x$ and $d_y$, the new root keeps $d_x$ (or $d_y$ if $x$ had none), and if both are set it queues the pair $(d_x, d_y)$ in line L13, which the same call of UNIFY merges before it returns. So, by induction on the merges, the deref of a class stays in the class of every deref that any of its nodes had. $\square$

**Lemma 2 (the two invariants).** At the end:

1. if $a \in base(r)$ for a root $r$, then $r$ has a deref node and $[V(a)] = D(r)$;
2. for every flow edge $u \to v$, both ends have deref nodes and $D(u) = D(v)$.

*Proof.* Line L3 puts $a$ into the base set of the root of $V(x)$ and unifies $V(a)$ with the deref node of that root, which line L9 makes if needed. Base sets move to the new root when classes merge (line L12), and by Lemma 1 the deref node of the new root is in the class of the old one. So part 1 holds at the end. Each flow edge is added by FLOW (line L7), which unifies the deref nodes of its two ends in line L8, and Lemma 1 again carries this to the end. $\square$

**Lemma 3 (sets in a closure share one deref class).** If $a \in C(r)$, then $[V(a)] = D(r)$.

*Proof.* There is a path $w = w_0 \to w_1 \to \cdots \to w_k = r$ of flow edges with $a \in base(w)$. By part 1, $[V(a)] = D(w_0)$, and by part 2, $D(w_0) = D(w_1) = \cdots = D(w_k)$. $\square$

**Theorem 1 (the result is a solution).** $S$ meets every subset constraint.

*Proof.* Take each statement form.

- `x = &a`. Line L3 puts $a$ into $base(V(x))$, so $a \in S(x)$.
- `x = y`. Line L4 adds the edge $V(y) \to V(x)$, and every root that reaches $[V(y)]$ also reaches $[V(x)]$, so $S(y) \subseteq S(x)$.
- `x = *y`. Line L5 adds the edge $d \to V(x)$, where $d$ is the deref node of $V(y)$ at that time; by Lemma 1, $[d] = D(V(y))$ at the end. Let $a \in S(y) = C([V(y)])$. By Lemma 3, $[V(a)] = D(V(y)) = [d]$, so $S(a) = C([d]) \subseteq C([V(x)]) = S(x)$.
- `*x = y`. Line L6 adds the edge $V(y) \to d$, with $[d] = D(V(x))$ at the end. Let $a \in S(x)$. By Lemma 3, $[V(a)] = [d]$, so $S(y) \subseteq C([d]) = S(a)$. $\square$

**Corollary (containment).** $L(v) \subseteq S(v)$ for every variable $v$, since $L$ is the least solution. So the result is sound for every run that executes the statements in any order.

**Equality on one level.** Suppose the program has only statements `x = &a` and `x = y`, and no variable whose address is taken is on the left of a statement. Call such variables targets and the others pointers. UNIFY only ever merges deref nodes and value nodes of targets, so the value node of each pointer stays alone in its class, and the flow edges join only pointer nodes. A target node has no base set and no incoming edge, so $S(t) = \emptyset = L(t)$ for a target $t$, and $S(x)$ for a pointer $x$ is the set of addresses that reach $x$ along copy edges, which is $L(x)$. So in this case the result is exactly Andersen's, and the loss of precision comes from the levels below the top.

**Theorem 2 (time).** Phase 1 (lines L1 to L13) takes $O((n + m)\,\alpha(n + m))$ time if base sets are merged in $O(1)$, for example as linked lists; phase 2 (lines L14 to L16) takes $O(n (n + m))$ time. The space is $O(n + m)$ for phase 1 and $O(n^2 + m)$ for the sets.

*Proof.* There are $n$ value nodes for the variables, and line L9 makes at most one node per call of DEREF, at most $3m$ in total, so there are $N \le n + 3m$ nodes. Each statement makes $O(1)$ calls of UNIFY and at most one flow edge. Each pair that UNIFY takes from its queue either finds one class, or merges two classes and queues at most one more pair, and there are at most $N - 1$ merges. So phase 1 does $O(N + m)$ finds and unions, which cost $O((N + m)\,\alpha(N + m))$, and $O(N + m)$ other work. In phase 2, each location $a$ starts one search from the roots whose base set holds it; the search visits each root and each of the at most $m$ edges once. With at most $n$ locations, phase 2 costs $O(n (N + m)) = O(n (n + m))$. $\square$

The implementation merges base sets as Python sets, at a cost of the size of the moved set at each merge, so its phase 1 can cost $O(n (n + m))$ in the worst case, the same order as phase 2.
