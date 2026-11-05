---
title: The Kosaraju-Sharir algorithm labels each strongly connected component with its own number
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph, where parallel arcs and loops are allowed. Write $u \leadsto v$ when $G$ has a directed path from $u$ to $v$, and let the components be the classes of the relation "$u \leadsto v$ and $v \leadsto u$". Let $d[v]$ and $f[v]$ be the discovery and finish times of the DFS of line L1. For a set $C$ of vertices, let $d(C) = \min_{v \in C} d[v]$ and $f(C) = \max_{v \in C} f[v]$. We use three facts from the [depth-first search](/depth-first-search/) pages: the times are distinct; $w$ is a proper descendant of $x$ exactly when $d[x] < d[w] < f[w] < f[x]$ (the [parenthesis theorem](/parenthesis-theorem/)); and the [white-path theorem](/white-path-theorem/).

**Lemma 1.** Let $C \ne D$ be components, and let $G$ have an arc $(c, e)$ with $c \in C$ and $e \in D$. Then $f(C) > f(D)$.

*Proof.* Let $x$ be the vertex of $C \cup D$ that is discovered first, so $d[x] = d(C \cup D)$.

*Case $x \in C$.* Just before $d[x]$, every vertex of $C \cup D$ is white. Each $y \in D$ is reachable from $x$ by a path that goes inside $C$ from $x$ to $c$, takes the arc $(c, e)$, and goes inside $D$ from $e$ to $y$. The paths inside a component stay in the component (see [strongly connected components](/strongly-connected-components/)), so this path is white, and by the white-path theorem $y$ is a descendant of $x$. As $y \ne x$, the parenthesis theorem gives $f[y] < f[x]$. So $f(D) < f[x] \le f(C)$.

*Case $x \in D$.* As above, each vertex of $D$ is a descendant of $x$, so $f(D) = f[x]$. No vertex $z$ of $C$ is reachable from $x$: else $e \leadsto x \leadsto z \leadsto c \to e$, and $C$ and $D$ would be one component. A descendant of $x$ is reachable from $x$ by the tree path, so no vertex of $C$ is a descendant of $x$. Let $z \in C$. Then $d[z] > d[x]$, by the choice of $x$. If $d[z] < f[x]$, the intervals $[d[x], f[x]]$ and $[d[z], f[z]]$ would meet, so by the parenthesis theorem one would contain the other, and as $d[x] < d[z]$ the vertex $z$ would be a descendant of $x$. So $d[z] > f[x]$, and $f[z] > d[z] > f[x]$. Hence $f(C) > f[x] = f(D)$. $\square$

In $G^{\mathsf T}$ the arc $(c, e)$ becomes $(e, c)$, and $G^{\mathsf T}$ has the same components as $G$, because $u \leadsto v$ in $G$ exactly when $v \leadsto u$ in $G^{\mathsf T}$. So Lemma 1 reads:

**Corollary 2.** If $G^{\mathsf T}$ has an arc from a component $D$ to another component $C$, then $f(C) > f(D)$.

**Lemma 3 (what ASSIGN labels).** Let $U$ be the set of vertices with $comp = $ NIL just before a call ASSIGN$(G^{\mathsf T}, u, k)$ from line L7, with $u \in U$. When the call returns, the vertices labelled $k$ are exactly the vertices $v$ that $G^{\mathsf T}$ has a path from $u$ to with all its vertices in $U$. No other label changes.

*Proof.* ASSIGN is a depth-first search of $G^{\mathsf T}$ that treats labelled vertices as already visited. Line L9 labels each vertex it is called on, line L11 calls it only on unlabelled vertices, so each vertex of $U$ is labelled at most once and the run stops after at most $|U|$ calls, each with a finite loop. Every labelled vertex is joined to $u$ by the chain of calls, which is a path inside $U$. Conversely, let $u = y_0, y_1, \ldots, y_j$ be a path of $G^{\mathsf T}$ inside $U$, and assume, for a contradiction, that some $y_i$ is not labelled $k$ at the end. Take the least such $i$; then $i \ge 1$, and $y_{i-1}$ was labelled $k$ by a call that scanned $\mathrm{Adj}^{\mathsf T}[y_{i-1}]$. At that moment $y_i$ was either unlabelled, and line L11 labelled it, or already labelled. A label set before the call is impossible, as $y_i \in U$, and a label set during the call is $k$. Both contradict the choice of $i$. $\square$

**Theorem.** KOSARAJU-SHARIR stops, and when it returns, $comp[u] = comp[v]$ if and only if $u$ and $v$ are in the same component. Moreover the labels $1, 2, \ldots$ are given to the components in decreasing order of $f(C)$, so $comp[u] \le comp[v]$ for each arc $(u, v)$ of $G$.

*Proof.* Lines L1 and L2 stop, and the loop of line L4 has $n$ steps, each of which stops by Lemma 3. We prove by induction on the steps of line L4 the invariant:

> **(K)** The labelled vertices are the union of whole components $C_1, \ldots, C_k$, where $C_i$ is exactly the set labelled $i$, and every component $C$ that is not labelled has $f(C) < f(C_i)$ for each $i \le k$. Also, every vertex $w$ that line L4 has already passed is labelled.

At the start, $k = 0$, no vertex is labelled and no vertex is passed, so (K) holds. Consider a step with vertex $u$. If $u$ is labelled, nothing changes and $u$ becomes passed, so (K) holds. Else let $C$ be the component of $u$. By (K), $C$ is not labelled at all, because the labelled set is a union of whole components and misses $u$. We first show that $f[u] = f(C)$ and that $C$ has the largest $f$ among the unlabelled components. Line L4 takes the vertices in decreasing order of $f$, and every vertex with a larger finish time than $u$ is passed and so labelled. So each unlabelled vertex $w$ has $f[w] \le f[u]$. Applied to the vertices of $C$ this gives $f(C) = f[u]$, and applied to an unlabelled component $D$ it gives $f(D) \le f[u] = f(C)$, with equality only if $D = C$, as the times are distinct.

Now we show that ASSIGN labels exactly $C$. Every vertex of $C$ is unlabelled and joined to $u$ by a path of $G^{\mathsf T}$ inside $C$, so by Lemma 3 it gets the label $k + 1$. Assume that some vertex outside $C$ gets this label. By Lemma 3, a path of $G^{\mathsf T}$ from $u$ inside the unlabelled set reaches it, so this path has a first arc $(y, z)$ with $y \in C$ and $z$ in another component $D$, and $z$ is unlabelled. By (K), $D$ is then a whole unlabelled component, so $f(D) < f(C)$ by the paragraph above. But $(y, z)$ is an arc of $G^{\mathsf T}$ from the component $C$ to the component $D$, so Corollary 2 gives $f(D) > f(C)$. This is a contradiction. So the set labelled $k + 1$ is exactly $C$, which we call $C_{k+1}$, and every remaining unlabelled component $D$ has $f(D) < f(C) = f(C_{k+1})$. Together with (K) for $C_1, \ldots, C_k$, which still holds because $C$ itself was unlabelled, the invariant holds after the step.

When the loop ends, every vertex is passed and so labelled, and by (K) each label class is exactly one component. This proves the first claim. By (K), $f(C_1) > f(C_2) > \cdots$. For an arc $(u, v)$ of $G$ with $u$ and $v$ in different components $C_i \ni u$ and $C_j \ni v$, Lemma 1 gives $f(C_i) > f(C_j)$, so $i < j$. If they are in the same component, the labels are equal. $\blacksquare$

**Remark on the second search.** Lemma 3 holds for any search that labels exactly the vertices reachable from $u$ inside $U$, so the theorem holds when ASSIGN is a breadth-first search or a search with an explicit stack, as in the Python implementation.
