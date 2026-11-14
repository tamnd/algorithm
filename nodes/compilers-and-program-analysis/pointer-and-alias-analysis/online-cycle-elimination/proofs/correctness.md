---
title: Collapsing cycles online keeps the least solution of the subset constraints, and the graph of classes stays acyclic
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set of $m$ statements in the four forms over $n$ variables, each variable also a location. $L$ is the least solution of the subset constraints of [Andersen's analysis](/andersen-analysis/): `p = &a` gives $a \in L(p)$, `p = q` gives $L(q) \subseteq L(p)$, `p = *q` gives $L(a) \subseteq L(p)$ for $a \in L(q)$, and `*p = q` gives $L(q) \subseteq L(a)$ for $a \in L(p)$. $L$ lies inside every solution. The algorithm keeps a union-find forest over the variables. For a variable $v$, $[v]$ is the root of its class. Each root $r$ has a set $pts(r)$, a set of successors $succ(r)$, and the loads and stores of all members of its class. An edge $r \to w$ is read on the roots, as $[r] \to [w]$. The result is $S(v) = pts([v])$. For a class $c$ we write $L(c) = L(v)$ for a member $v$; Lemma 1 shows that this does not depend on the member.

**Lemma 1 (every step is forced).** At every moment:

1. all members of a class have the same $L$;
2. $pts(r) \subseteq L(r)$ for every root $r$;
3. every edge $r \to w$ has $L(r) \subseteq L(w)$.

*Proof.* At the start every class has one member, all sets are empty and there are no edges. Take each step.

- Line L2 puts $a$ into $pts(p)$ for a statement `p = &a`, and $a \in L(p)$.
- Line L3 adds the edge $[q] \to [p]$ for `p = q`, and $L(q) \subseteq L(p)$.
- Line L7 adds $[a] \to [p]$, where $a \in pts(r)$ and `p = *y` is a statement with $y$ in the class $r$. By part 2, $a \in L(r) = L(y)$, so the load constraint gives $L(a) \subseteq L(p)$.
- Line L8 adds $[q] \to [a]$ for `*y = q` with $y$ in the class $r$ and $a \in pts(r) \subseteq L(y)$, so the store constraint gives $L(q) \subseteq L(a)$.
- Lines L9 and L15 copy $pts(u)$ into $pts(v)$ along an edge $u \to v$. By parts 2 and 3, $pts(u) \subseteq L(u) \subseteq L(v)$.
- Line L14 merges the set $C$ of roots that lie on some path from $v$ to $u$, just after line L12 added the edge $u \to v$. Every $x \in C$ lies on the cycle $u \to v \to^* x \to^* u$. By part 3, $L$ cannot shrink along an edge, so it is the same on the whole cycle: $L(x) = L(u)$ for every $x \in C$. So part 1 holds for the new class, the union of the old sets is inside this common $L$, and the edges keep their ends' $L$. $\square$

**Lemma 2 (the graph of classes has no cycle).** After every call of ADD-EDGE, the graph of roots and edges has no cycle, other than edges from a root to itself, which are dropped.

*Proof.* By induction. Suppose the graph has no cycle before ADD-EDGE adds $u \to v$. A cycle in the new graph must use the new edge, so it is a path from $v$ to $u$, and all its nodes are in $C$. If there is no such path, there is no cycle. Otherwise line L14 merges $C$ into one root $r$. Suppose the merged graph has a cycle. It must go through $r$, since every other cycle was there before. So there are $x, y \in C$ and roots $a, b$ outside $C$ with $x \to a \to^* b \to y$. Now $v \to^* x$ and $y \to^* u$, because $x$ and $y$ are on paths from $v$ to $u$. So $v \to^* a \to^* u$, and $a$ is on a path from $v$ to $u$, which means $a \in C$, a contradiction. A merge does not add other edges: the successors of $r$ are the successors of the members of $C$, read on the roots. $\square$

**Lemma 3 (what is done stays done).** Call a root $r$ *finished* if (A) for every $a \in pts(r)$, the edges $[a] \to [p]$ for the loads `p = *y` and $[q] \to [a]$ for the stores `*y = q` with $y$ in the class $r$ are in the graph, and (B) $pts(r) \subseteq pts(w)$ for every edge $r \to w$. Every root that is not on the worklist is finished.

*Proof.* A root that is not finished got that way in one of these steps: its set grew, it became the root of a merge, or an edge left it. When its set grows (lines L9, L15), it is pushed. When it becomes the root of a merge, line L14 pushes it. When ADD-EDGE adds $u \to v$ and no cycle forms, line L15 makes $pts(u) \subseteq pts(v)$ at once; when a cycle forms, the edge disappears into the merged root, which is pushed. The set of a successor only grows, so (B) cannot break that way. Each root is taken off the worklist before lines L6 to L9 run for it, and those lines make (A) and (B) true for the set it has then. If the set grows during those lines, the root is pushed again. $\square$

**Theorem 1 (correctness).** The algorithm stops, and $S = L$.

*Proof.* Each push comes from a set that grew or from a merge. A set can grow at most $n$ times per root and there are at most $n - 1$ merges, so there are at most $n^2 + n$ pushes, and the loop stops. When it stops, the worklist is empty, so every root is finished by Lemma 3. Take each statement form. For `p = &a`, $a \in pts([p])$ since sets only grow and merges take the union. For `p = q`, the edge $[q] \to [p]$ is in the graph, or $[q] = [p]$, and (B) gives $S(q) \subseteq S(p)$. For `p = *y` and $a \in S(y)$, (A) gives the edge $[a] \to [p]$, so $S(a) \subseteq S(p)$. For `*y = q` and $a \in S(y)$, (A) gives $[q] \to [a]$, so $S(q) \subseteq S(a)$. So $S$ is a solution and $L \subseteq S$. By Lemma 1, $S(v) = pts([v]) \subseteq L([v]) = L(v)$. So $S = L$. $\square$

So merging a cycle never changes the answer. It is only a way to store fewer sets and to move each fact along fewer edges.

**Theorem 2 (time).** With a full search for each new edge, and with each find of the union-find forest counted as one step, the algorithm runs in $O(n^4 + n^2 m)$ time and $O(n^2 + m)$ space. The finds add at most a factor of $O(\log n)$, since the forest uses path compression.

*Proof.* There are at most $n^2$ distinct edges. Each new edge starts one search, which visits each root and each edge once, in $O(n + n^2)$ time, so the searches cost $O(n^4)$. A merge of $C$ costs $O(|C| (n + m))$ for the unions of the sets, the edges and the tables, and each variable stops being a root once, so the merges cost $O(n (n + m))$. Each root is processed once per push, and by the proof of Theorem 1 each variable is pushed $O(n)$ times as a root. One processing of $r$ makes $|pts(r)| \cdot (l_r + s_r) \le n (l_r + s_r)$ calls of ADD-EDGE, where $l_r$ and $s_r$ count the loads and stores of the class, and copies $pts(r)$ along at most $n$ edges in $O(n^2)$ time. A call of ADD-EDGE that finds the edge already there costs $O(1)$; the others are the new edges, counted above. Summed over all processings, this is $O(n \cdot (n m + n^3)) = O(n^2 m + n^4)$. The sets, the edges and the tables need $O(n^2 + m)$ space. $\square$

The bound is weaker than the $O(n^3)$ bound of plain Andersen's analysis with difference propagation, because this version moves full sets and searches the whole graph for every new edge. Online cycle elimination is a practical method: it pays when the graph has large cycles, as the graphs of real C programs do. The partial search of Fähndrich, Foster, Su and Aiken looks at much less of the graph per edge and may miss some cycles; Theorem 1 still holds for it, since it merges only nodes that are on a cycle, and Lemma 1 needs nothing more.
