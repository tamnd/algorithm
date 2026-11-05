---
title: MWIS-TREE returns a maximum-weight independent set
proves: [correctness, termination]
status: full
---

Root the tree at $r$. For a vertex $v$, let $C(v)$ be its set of children and $\mathrm{sub}(v)$ its set of descendants, $v$ included. A set $I$ of vertices is *independent* if no edge of the tree has both ends in $I$. Define

$$A(v) = \max\{ w(I) : I \subseteq \mathrm{sub}(v) \text{ independent}, v \in I \}, \qquad B(v) = \max\{ w(I) : I \subseteq \mathrm{sub}(v) \text{ independent}, v \notin I \}.$$

Both maxima are over non-empty finite families ($\{v\}$ and $\emptyset$), so they exist.

**Lemma 1 (recurrence).** For each vertex $v$,
$A(v) = w(v) + \sum_{c \in C(v)} B(c)$ and $B(v) = \sum_{c \in C(v)} \max(A(c), B(c))$.

*Proof.* The sets $\mathrm{sub}(c)$, $c \in C(v)$, together with $\{v\}$, partition $\mathrm{sub}(v)$. The only edges of the tree inside $\mathrm{sub}(v)$ are the edges inside some $\mathrm{sub}(c)$ and the edges $\{v, c\}$ for $c \in C(v)$: an edge between $\mathrm{sub}(c)$ and $\mathrm{sub}(c')$ for $c \ne c'$ would close a cycle through $v$.

So a set $I \subseteq \mathrm{sub}(v)$ with $v \in I$ is independent if and only if each $I_c = I \cap \mathrm{sub}(c)$ is independent and $c \notin I_c$. Its weight is $w(v) + \sum_c w(I_c)$, and the $I_c$ can be chosen separately, so the maximum is $w(v) + \sum_c B(c)$.

A set $I \subseteq \mathrm{sub}(v)$ with $v \notin I$ is independent if and only if each $I_c$ is independent, with no condition on $c$. The maximum of $w(I_c)$ over such $I_c$ is $\max(A(c), B(c))$, and again the choices are separate. $\square$

**Lemma 2 (first pass).** After the loop of lines L2 to L4, $in[v] = A(v)$ and $out[v] = B(v)$ for each $v$.

*Proof.* In reverse BFS order, each vertex comes after all of its descendants, since BFS lists a parent before its children. We show by induction along this order: when line L3 processes $v$, $in[v] = \sum_{c \in C(v)} B(c)$ and $out[v] = \sum_{c \in C(v)} \max(A(c), B(c))$, and after line L3, $in[v] = A(v)$ and $out[v] = B(v)$.

Both arrays start at 0. The only writes to $in[v]$ and $out[v]$ before $v$ is processed are the writes of line L4 for the children $c$ of $v$, one for each child, and each of them happens after $c$ is processed, when by the induction hypothesis $in[c] = A(c)$ and $out[c] = B(c)$. So when $v$ is reached, the two sums are as claimed. Line L3 adds $w(v)$ to $in[v]$, and by Lemma 1 the values are now $A(v)$ and $B(v)$. Later steps write only to the entries of parents, never again to $v$'s own entries. $\square$

So line L5 sets $best = \max(A(r), B(r))$, the maximum weight of an independent subset of $\mathrm{sub}(r) = V$.

**Lemma 3 (second pass).** Let $S$ be the set built by lines L6 to L8. Then $S$ is independent, and for each vertex $v$:
(a) if $v = r$ or $p(v) \notin S$, then $w(S \cap \mathrm{sub}(v)) = \max(A(v), B(v))$;
(b) if $p(v) \in S$, then $v \notin S$ and $w(S \cap \mathrm{sub}(v)) = B(v)$.

*Proof.* In BFS order the parent of $v$ is decided before $v$, so the test of line L7 is well defined. If $p(v) \in S$, line L7 keeps $v$ out. So no edge $\{p(v), v\}$ has both ends in $S$, and $S$ is independent.

We prove (a) and (b) by induction on the height of $v$, the length of the longest path from $v$ down to a leaf. Write $S_v = S \cap \mathrm{sub}(v)$.

*Case (b).* $v \notin S$, and each child $c$ has $p(c) = v \notin S$, so (a) holds for $c$ by the induction hypothesis. Hence $w(S_v) = \sum_c \max(A(c), B(c)) = B(v)$ by Lemma 1.

*Case (a), $in[v] > out[v]$.* Line L8 puts $v$ in $S$. Each child $c$ then has $p(c) \in S$, so by (b) for $c$, $w(S_c) = B(c)$. Hence $w(S_v) = w(v) + \sum_c B(c) = A(v) = \max(A(v), B(v))$, using Lemma 2.

*Case (a), $in[v] \le out[v]$.* Line L8 leaves $v$ out, and as in case (b), $w(S_v) = B(v) = \max(A(v), B(v))$.

A leaf has no children, and the same three cases apply with empty sums. $\square$

**Theorem.** MWIS-TREE returns $best = \max\{ w(I) : I \text{ independent} \}$ and an independent set $S$ with $w(S) = best$. It stops after $\Theta(n)$ steps.

*Proof.* By Lemma 2, $best = \max(A(r), B(r))$, and every independent set of the tree either contains $r$ or not, so $best$ is the maximum. By Lemma 3(a) with $v = r$, $S$ is independent and $w(S) = w(S \cap \mathrm{sub}(r)) = \max(A(r), B(r)) = best$. The BFS visits each vertex once and each edge twice, and each of the two loops visits each of the $n$ vertices once with $O(1)$ work, so the algorithm stops after $\Theta(n)$ steps. $\blacksquare$
