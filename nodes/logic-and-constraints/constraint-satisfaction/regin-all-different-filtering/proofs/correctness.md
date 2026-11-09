---
title: Régin's filter removes exactly the values that belong to no solution
proves: [correctness]
status: full
---

We use the pseudocode of the page. $X = \{x_1, \ldots, x_n\}$ is the set of variables, $V$ the set of values that occur in some domain, and $G$ the value graph. A matching *covers* a vertex if the vertex is an end of one of its edges. A vertex that a matching $M$ does not cover is *$M$-free*. An *$M$-alternating* path or cycle uses edges that are in $M$ and not in $M$ in turn.

**Lemma 1 (solutions are matchings).** The solutions of all-different$(x_1, \ldots, x_n)$ are in one-to-one correspondence with the matchings of $G$ that cover $X$. The solution $(a_1, \ldots, a_n)$ corresponds to $\{\{x_i, a_i\}\}$. So $a \in D(x)$ has a support if and only if some matching that covers $X$ holds the edge $\{x, a\}$.

*Proof.* A tuple with $a_i \in D(x_i)$ gives $n$ edges of $G$, one at each variable. The values are pairwise different if and only if no two of these edges share a value, that is, if and only if the edges form a matching. Each matching that covers $X$ has exactly one edge at each $x_i$, so it gives such a tuple. $\square$

A matching that covers $X$ has size $n$, and no matching is larger, because each edge has one end in $X$. So if some matching covers $X$, the maximum matchings are exactly the matchings that cover $X$. This proves that line L3 is correct: it returns failure if and only if no matching covers $X$, that is, by Lemma 1, if and only if the constraint has no solution. From here on, $|M| = n$, so $M$ covers $X$ and every $M$-free vertex is a value.

**Lemma 2 (Berge).** Let $M$ be a maximum matching of a graph and $e \notin M$ an edge. Then $e$ is in some maximum matching if and only if $e$ is on an $M$-alternating cycle, or on an $M$-alternating path of even length whose first vertex is $M$-free.

*Proof.* (If.) Let $P$ be such a cycle or path. On a cycle, the edges of $P$ in $M$ and not in $M$ alternate, and an alternating cycle has even length, so $P$ has as many edges in $M$ as outside. On an even path whose first vertex $u$ is $M$-free, the first edge is not in $M$, so again $P$ has as many edges in $M$ as outside. In both cases $M' = M \triangle P$ is a matching: inside $P$ each vertex keeps at most one edge, and a vertex of $P$ that is covered by an edge of $M$ outside $P$ is impossible, because each inner vertex of $P$ has its $M$-edge on $P$, $u$ is free, and the last vertex of the even path has its $M$-edge on $P$ (the last edge is in $M$). So $|M'| = |M|$, $M'$ is maximum, and $e \in M'$.

(Only if.) Let $M'$ be a maximum matching with $e \in M'$. In $H = M \triangle M'$ each vertex has degree at most 2, so each component of $H$ is a path or a cycle, and its edges alternate between $M$ and $M'$. Let $C$ be the component that holds $e$. If $C$ is a cycle, it is an $M$-alternating cycle through $e$. If $C$ is a path with more edges of $M'$ than of $M$, then $M \triangle C$ is a matching larger than $M$, which is not possible. If $C$ has more edges of $M$ than of $M'$, then $M' \triangle C$ is larger than $M'$, also not possible. So $C$ is a path with equally many edges of $M$ and $M'$, so its length is even and its two end edges are one in $M$ and one in $M' \setminus M$. Let $u$ be the end whose edge on $C$ is in $M' \setminus M$. If $u$ were covered by an edge $f \in M$, then $f \notin C$ (the only edge of $C$ at $u$ is not in $M$), so $f \notin H$, so $f \in M'$. Then $u$ has two edges of $M'$, namely $f$ and its edge on $C$, which is not possible. So $u$ is $M$-free, and $C$, read from $u$, is an even $M$-alternating path from an $M$-free vertex through $e$. $\square$

**Lemma 3 (the oriented graph).** Orient $G$ as in line L4. Then:

1. Each directed path or directed cycle is $M$-alternating.
2. An edge $e = \{x, a\} \notin M$ is on an $M$-alternating cycle if and only if $x$ and $a$ are in the same strongly connected component.
3. An edge $e = \{x, a\} \notin M$ is on an even $M$-alternating path whose first vertex is $M$-free, or on an $M$-alternating cycle, if and only if $a$ is reachable from a free value or $x$ and $a$ are in the same strongly connected component.

*Proof.* (1) The only edge that leaves a variable $x$ is $x \to M(x)$, which is in $M$. Each edge that leaves a value is not in $M$. A directed path goes from variables to values by edges of $M$ and from values to variables by edges not in $M$, so it alternates.

(2) If $x$ and $a$ are in the same component, there is a directed path $Q$ from $x$ to $a$, and we can take $Q$ simple. Then $Q$ followed by the edge $a \to x$ is a simple directed cycle through $e$, and by (1) it is $M$-alternating. Conversely, an $M$-alternating cycle through $e$ is a directed cycle in the orientation: around the cycle, each vertex enters by one kind of edge and leaves by the other, and at a variable the edge of $M$ is the one that leaves, at a value the edge of $M$ is the one that enters. Going around the cycle in the direction of the arc $a \to x$, every edge is traversed in its own direction. So $x$ and $a$ are on a common directed cycle, hence in one component.

(3) Assume $a$ is reachable from a free value $f$. Take a shortest directed path $Q$ from $f$ to $a$ (if $a = f$, $Q$ is empty). If $x$ is on $Q$, then $Q$ goes from $x$ to $a$ through part of itself, and with $a \to x$ this gives a directed cycle, so $x$ and $a$ are in one component, and $e$ is on an alternating cycle by (2). If $x$ is not on $Q$, consider $M(x)$. A value other than $f$ is entered on a directed path only by its matched edge, so if $M(x)$ were on $Q$, then $x$ would be on $Q$ just before it. Also $M(x) \ne f$, since $f$ is free. So $M(x)$ is not on $Q$, and $Q$, then $a \to x$, then $x \to M(x)$, is a simple directed path. By (1) it is $M$-alternating. It starts at the free vertex $f$ and ends with an edge of $M$, so it has even length. It contains $e$.

Conversely, let $P$ be an even $M$-alternating path through $e$ whose first vertex $u$ is $M$-free. Then $u$ is a value, since $M$ covers $X$. The first edge of $P$ is not in $M$ and goes from $u$ to a variable, so $P$, read from $u$, follows the orientation, as in the proof of (2). The edge $e$ is traversed as $a \to x$, so the part of $P$ before $x$ is a directed path from $u$ to $a$, and $a$ is reachable from a free value. The cycle case is (2). $\square$

**Theorem.** If the constraint has no solution, REGIN-FILTER returns failure. Otherwise it returns domains $D'$ with $a \in D'(x)$ if and only if $a \in D(x)$ and some solution gives $a$ to $x$.

*Proof.* Failure is handled by the remark after Lemma 1. Assume $|M| = n$. Fix an edge $e = \{x, a\}$ of $G$. Line L8 keeps $e$ if and only if $e \in M$, or $a \in R$, or $x$ and $a$ are in the same component. By Lemma 3(3), for $e \notin M$ the last two conditions hold if and only if $e$ is on an even alternating path from an $M$-free vertex or on an alternating cycle, which by Lemma 2 holds if and only if some maximum matching contains $e$. For $e \in M$, $M$ itself is such a matching. So line L8 keeps $e$ if and only if some maximum matching contains $e$. Maximum matchings are the matchings that cover $X$, so by Lemma 1 this holds if and only if $a$ has a support in $D(x)$. Line L5 computes the set of vertices reachable from free values, as in the statement of Lemma 3, and line L6 the components. $\blacksquare$

**Corollary (strength).** After REGIN-FILTER, each binary constraint $x_i \ne x_j$ is arc consistent, and there are domains where REGIN-FILTER fails or removes values while arc consistency on all the constraints $x_i \ne x_j$ removes nothing.

*Proof.* Let $a \in D'(x_i)$. Some solution $(a_1, \ldots, a_n)$ has $a_i = a$, and by the theorem $a_j \in D'(x_j)$. Since $a_j \ne a$, the value $a$ has the support $a_j$ on $x_i \ne x_j$. For the second part, take $D(x_1) = D(x_2) = D(x_3) = \{1, 2\}$. Each value of $x_i$ has a different value in $D(x_j)$, so all six arcs are consistent, but the constraint has no solution, so REGIN-FILTER fails. $\blacksquare$
