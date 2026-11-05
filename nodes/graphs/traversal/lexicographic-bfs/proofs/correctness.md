---
title: LEXBFS computes a LexBFS order, and its reverse is a perfect elimination ordering exactly for chordal graphs
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $n$ vertices. Write $x <_\sigma y$ if $x$ is visited before $y$. For a moment before step $i$, the label of an unvisited $x$ is $\ell(x) = N(x) \cap \{v_1, \ldots, v_{i-1}\}$, and $A \succ B$ means that the first visited vertex of $A \triangle B$ is in $A$. This is a strict total order on the subsets of the visited vertices.

## Part 1: the algorithm follows the LexBFS rule

**Invariant.** At the start of step $i$ (before line L3), the classes of $L$ partition the unvisited vertices; two unvisited vertices are in the same class if and only if they have the same label; and if class $X$ is before class $Y$ in $L$, the labels in $X$ are $\succ$ the labels in $Y$.

*Initialization.* Before step 1, no vertex is visited, every label is empty, and $L$ has one class holding $V$.

*Maintenance.* Step $i$ removes $v = v_i$ from the first class. For an unvisited $w$, the new label is $\ell(w) \cup \{v\}$ if $w \in N(v)$, and $\ell(w)$ otherwise. Take two unvisited vertices $x$ and $y$.

- If they were in the same class $D$, their old labels were equal, $A$ say. If both or neither are adjacent to $v$, the new labels are equal, and lines L5 to L8 leave them in one class: both in $D'$, or both in $D$. If only $x$ is adjacent to $v$, then the new labels are $A \cup \{v\}$ and $A$, with symmetric difference $\{v\}$, so $x$'s label is larger. Line L8 moves $x$ to $D'$, which is just before $D$, where $y$ stays.
- If they were in classes $X$ before $Y$, the old labels have $\ell(x) \succ \ell(y)$, and the first vertex $u$ of $\ell(x) \triangle \ell(y)$ is in $\ell(x)$. The vertex $v$ is visited after $u$, so adding $v$ to one or both labels does not change the first vertex of the symmetric difference, and the new labels still differ, with $x$'s larger. The class of $x$ after the step is $X$ or the new class just before $X$, and that of $y$ is $Y$ or the new class just before $Y$. Both of these are still before $Y$'s classes, because the new class of $Y$ is inserted directly before $Y$ and after $X$ (if $X$ is directly before $Y$, the new class of $Y$ goes between them).

Empty classes are deleted, which does not change the order of the others. So the invariant holds at the start of step $i + 1$.

**Lemma 1.** The order $\sigma$ returned by LEXBFS obeys the LexBFS rule, and its first vertex is $s$.

*Proof.* By the invariant, the first class holds exactly the unvisited vertices with the largest label, and line L3 takes one of them. At step 1, all labels are equal and $s$ is first. $\square$

**Termination.** Each step visits one vertex, the loop of line L2 runs $n$ times, and each step scans one finite list.

## Part 2: the four-point property

**Lemma 2.** Let $\sigma$ be any order that obeys the LexBFS rule. If $a <_\sigma b <_\sigma c$, $ac \in E$ and $ab \notin E$, then there is a vertex $d <_\sigma a$ with $db \in E$ and $dc \notin E$.

*Proof.* Consider the step at which $b$ is chosen. Then $a$ is visited and $c$ is not, and $b$ has a largest label, so $\ell(b) \succeq \ell(c)$. Now $a \in \ell(c)$ and $a \notin \ell(b)$, so the labels differ, and $\ell(b) \succ \ell(c)$. Let $d$ be the first visited vertex of $\ell(b) \triangle \ell(c)$. Then $d \in \ell(b)$ and $d \notin \ell(c)$. Since $a$ is in the symmetric difference, $d \le_\sigma a$, and $d \ne a$ because $a \notin \ell(b)$. So $d <_\sigma a$, $db \in E$ and $dc \notin E$. $\square$

## Part 3: chordal graphs

For a vertex $x$, let $E(x)$ be the set of its neighbours $y <_\sigma x$. The reverse of $\sigma$ is a perfect elimination ordering exactly when $E(x)$ is a clique for every $x$, because the neighbours of $x$ that come after $x$ in the reverse order are those that come before $x$ in $\sigma$.

**Lemma 3.** Let $\sigma$ obey the LexBFS rule on a chordal graph $G$. Then there are no two non-adjacent vertices $u <_\sigma w$ joined by a path whose internal vertices are all visited after $w$.

*Proof.* Assume such pairs exist, and choose one, $(u, w)$, with $u$ as early in $\sigma$ as possible. Among the paths for this pair, choose a shortest one, $P = u, z, \ldots, w$. It has at least one internal vertex, since $uw \notin E$. It is chordless: a chord would give a shorter path between $u$ and $w$ whose internal vertices are a subset of those of $P$.

Apply Lemma 2 to $u <_\sigma w <_\sigma z$: $uz \in E$ and $uw \notin E$. It gives $d <_\sigma u$ with $dw \in E$ and $dz \notin E$.

The walk $d, w, \ldots, z, u$, which is $d$ followed by $P$ backwards, is a path from $d$ to $u$, because $d$ is not on $P$: every vertex of $P$ is $u$ or after it. Its internal vertices are $w$ and the internal vertices of $P$, and they are all visited after $u$, and $d <_\sigma u$. If $du \notin E$, then $(d, u)$ is a pair of the forbidden kind with $d <_\sigma u$, which contradicts the choice of $u$. So $du \in E$.

Now $d$ is adjacent to $u$ and to $w$, but not to $z$. Walk along $P$ from $u$, and let $y$ be the first vertex after $u$ that is adjacent to $d$. It exists, because $w$ is adjacent to $d$, and $y \ne z$. The cycle $d, u, z, \ldots, y, d$ has at least 4 vertices, because the part of $P$ from $u$ to $y$ has at least 3. It has no chord: the part of $P$ is chordless, $u$ and $y$ are not adjacent because $P$ is chordless and $y \ne z$, and $d$ is adjacent to no vertex strictly between $u$ and $y$ by the choice of $y$. A chordless cycle of length at least 4 contradicts that $G$ is chordal. $\square$

**Theorem 1 (Rose, Tarjan and Lueker).** Let $\sigma$ be an order that obeys the LexBFS rule, in particular the output of LEXBFS. Then $G$ is chordal if and only if the reverse of $\sigma$ is a perfect elimination ordering.

*Proof.* Let $G$ be chordal, and assume that some $E(c)$ contains two non-adjacent vertices $a <_\sigma b$. Then $a, c, b$ is a path between the non-adjacent vertices $a <_\sigma b$ whose only internal vertex $c$ is visited after $b$. Lemma 3 forbids this. So every $E(x)$ is a clique.

Conversely, let every $E(x)$ be a clique, and let $C$ be a cycle of length at least 4. Let $x$ be the vertex of $C$ visited last. Its two neighbours on $C$ are in $E(x)$, so they are adjacent. They are not consecutive on $C$, because $C$ has length at least 4, so this edge is a chord. So $G$ is chordal. $\blacksquare$

**Lemma 4 (the linear-time test).** For each $x$ with $E(x) \ne \emptyset$, let $p(x)$ be the vertex of $E(x)$ visited last. Then every $E(x)$ is a clique if and only if, for every $x$, each vertex of $E(x) \setminus \{p(x)\}$ is adjacent to $p(x)$.

*Proof.* If every $E(x)$ is a clique, the test holds. Conversely, assume the test holds, and show that $E(x)$ is a clique by induction on the position of $x$ in $\sigma$. Take $y \ne z$ in $E(x)$. If one of them is $p(x)$, they are adjacent by the test. If not, both are adjacent to $p(x)$ by the test and are visited before $p(x)$, so both are in $E(p(x))$, which is a clique by the induction hypothesis, since $p(x) <_\sigma x$. $\square$

**Corollary.** LEXBFS followed by the test of Lemma 4 decides in $O(n + m)$ time whether $G$ is chordal, and if it is, the reverse of $\sigma$ is a perfect elimination ordering. This follows from Lemma 1, Theorem 1 and Lemma 4. $\blacksquare$
