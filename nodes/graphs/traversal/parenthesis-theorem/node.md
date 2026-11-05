---
tag: 6VVQ3F
kind: theorem
slug: parenthesis-theorem
name: Parenthesis theorem
aliases:
- parenthesis structure theorem
area: graphs/traversal
level: core
summary: The discovery-finish intervals of any two DFS vertices are either nested or disjoint.
prereqs: [discovery-and-finish-times, depth-first-search]
see_also: [white-path-theorem, edge-classification, dfs-forest, depth-first-orders, topological-sort, euler-tour-technique]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the parenthesis theorem and the corollary on nesting of descendants' intervals)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.3, Theorem 22.7 (Parenthesis theorem) and Corollary 22.8 (Nesting of descendants' intervals)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.2 (the property of the previsit and postvisit numbers that the intervals are disjoint or nested)
---

The parenthesis theorem says that in each [depth-first search](/depth-first-search/), the intervals $[d[u], f[u]]$ between the [discovery and finish times](/discovery-and-finish-times/) of two vertices are either disjoint or nested, and that they are nested exactly when one vertex is a descendant of the other in the [depth-first forest](/dfs-forest/). If each discovery is written as an opening bracket and each finish as a closing bracket, the record of a DFS is a well-formed bracket word. The theorem turns questions about the forest into comparisons of four numbers, and it is the first step in the proofs of the [white-path theorem](/white-path-theorem/), of [edge classification](/edge-classification/) and of [topological sort](/topological-sort/).

## Statement

Let $G = (V, E)$ be a directed or undirected graph, and run the full procedure DFS$(G)$ of the [depth-first search](/depth-first-search/) page, with any order of the vertices and of the adjacency lists. Let $d[u]$ and $f[u]$ be the discovery and finish times, and call $v$ a *descendant* of $u$ if $u$ lies on the path from the root to $v$ in the depth-first forest; each vertex is a descendant of itself.

**Theorem (parenthesis theorem).** For any two vertices $u \ne v$, exactly one of the following holds:

1. the intervals $[d[u], f[u]]$ and $[d[v], f[v]]$ are disjoint, and neither vertex is a descendant of the other;
2. $[d[v], f[v]] \subset [d[u], f[u]]$, and $v$ is a descendant of $u$;
3. $[d[u], f[u]] \subset [d[v], f[v]]$, and $u$ is a descendant of $v$.

**Corollary (nesting of descendants' intervals).** The vertex $v$ is a proper descendant of $u$ if and only if

$$d[u] < d[v] < f[v] < f[u].$$

## In plain words

Depth-first search is a stack discipline: the vertex that it entered last is the vertex that it leaves first. So if the search enters a vertex while it is still inside another one, it must leave the inner vertex before it leaves the outer one. And the only way to enter a vertex while still inside another one is to go down from it, so the inner vertex lies below the outer one in the search tree.

Write an opening bracket when the search enters a vertex and a closing bracket when it leaves. Then two bracket pairs are never crossed like "( [ ) ]". They sit side by side, or one is inside the other, and the second case means one vertex is below the other in the tree.

## Proof

We use two facts about the procedure DFS. Both follow from the way recursive calls nest: if a call starts while another call is active, it ends before that call ends.

**Lemma A (descendants nest inside).** If $v$ is a proper descendant of $u$, then $d[u] < d[v] < f[v] < f[u]$.

*Proof.* By induction on the number of tree edges from $u$ down to $v$. If there is one, then $u = \pi[v]$, and DFS-VISIT$(v)$ is called at line L9 inside the call DFS-VISIT$(u)$. The call of $u$ set $d[u]$ at line L5 before this, and it sets $f[u]$ at line L10 after the call of $v$ has returned, while the call of $v$ sets $d[v]$ and then $f[v]$. So $d[u] < d[v] < f[v] < f[u]$. If there are more tree edges, let $w = \pi[v]$. Then $w$ is a proper descendant of $u$ with fewer tree edges below $u$, so $d[u] < d[w] < f[w] < f[u]$ by the induction hypothesis, and $d[w] < d[v] < f[v] < f[w]$ by the first case. Together these give the claim. $\square$

**Lemma B (a vertex found while $u$ is gray lies below $u$).** If $d[u] < d[v] < f[u]$, then $v$ is a proper descendant of $u$.

*Proof.* At time $d[v]$ the vertex $u$ is gray, so the call of $u$ is active. Let $g_1, g_2, \ldots, g_k$ be the vertices with an active call just before $v$ is discovered, from the bottom of the call stack to the top. The call of $g_1$ was made at line L4, and each call of $g_{i+1}$ was made at line L9 inside the call of $g_i$, after line L8 set $\pi[g_{i+1}] = g_i$. Because some call is active, $v$ is not discovered at line L4, which runs only when no call is active. So $v$ is discovered at line L9 inside the call at the top, and $\pi[v] = g_k$. The chain of parents from $v$ is then $g_k, g_{k-1}, \ldots, g_1$, and $u$ is one of the $g_i$. So $u$ lies on the tree path from the root $g_1$ to $v$, and $v \ne u$. $\square$

*Proof of the theorem.* The times are distinct, because each of $1, \ldots, 2n$ is used once. So $d[u] \ne d[v]$. By symmetry, assume $d[u] < d[v]$. Then $u$ is not a descendant of $v$, by Lemma A, which would give $d[v] < d[u]$. There are two cases, because $d[v] \ne f[u]$.

- *Case $d[v] < f[u]$.* By Lemma B, $v$ is a proper descendant of $u$, and by Lemma A, $d[u] < d[v] < f[v] < f[u]$. So $[d[v], f[v]] \subset [d[u], f[u]]$, and statement 2 holds.
- *Case $f[u] < d[v]$.* Then $d[u] < f[u] < d[v] < f[v]$, so the intervals are disjoint. If $v$ were a descendant of $u$, Lemma A would give $f[v] < f[u]$, which is false. So neither vertex is a descendant of the other, and statement 1 holds.

In each case exactly one statement holds, because a pair of intervals cannot be both disjoint and nested, and a strict containment cannot go both ways. With the roles of $u$ and $v$ exchanged, the case $d[v] < d[u]$ gives statement 1 or statement 3. $\blacksquare$

*Proof of the corollary.* If $v$ is a proper descendant of $u$, Lemma A gives the inequalities. Conversely, if $d[u] < d[v] < f[v] < f[u]$, the intervals are nested with $v$ inside, so of the three statements only statement 2 can hold, and $v$ is a descendant of $u$, with $v \ne u$. $\blacksquare$

## Consequences

- **Ancestor test in $O(1)$ time.** After one DFS, "is $u$ an ancestor of $v$" is the test $d[u] \le d[v]$ and $f[v] \le f[u]$. The same idea answers subtree queries on rooted trees in the [Euler tour technique](/euler-tour-technique/).
- **Subtree sizes.** The interval of $u$ holds exactly the times of the descendants of $u$, so $u$ has $(f[u] - d[u] + 1)/2$ descendants (see [discovery and finish times](/discovery-and-finish-times/)).
- **[White-path theorem](/white-path-theorem/).** Its proof uses the corollary twice.
- **[Edge classification](/edge-classification/).** The four types of edges of a directed graph are told apart by the order of $d[u], f[u], d[v], f[v]$, and the theorem shows that only the possible orders occur.
- **[Topological sort](/topological-sort/).** For an edge $(u, v)$ that is not a back edge, $f[v] < f[u]$. This is the key step of the proof of the DFS topological sort.
- **[Depth-first orders](/depth-first-orders/).** The preorder lists the opening brackets and the postorder the closing brackets, so each subtree is a contiguous block in both orders.

## Tightness

The theorem depends on the last-in first-out rule of DFS. Define the same two times for [breadth-first search](/breadth-first-search/): $d[u]$ when $u$ enters the queue and $f[u]$ when its scan ends, on one clock. On the directed graph with the edges $0 \to 1$ and $0 \to 2$, from source 0, the events are: 0 enters (time 1), 1 enters (2), 2 enters (3), the scan of 0 ends (4), the scan of 1 ends (5), the scan of 2 ends (6). So $[d[1], f[1]] = [2, 5]$ and $[d[2], f[2]] = [3, 6]$ overlap in part, and the bracket word $(_0 (_1 (_2 )_0 )_1 )_2$ is not well formed.

All three statements of the theorem do occur. In the DFS of the [depth-first search](/depth-first-search/) example, the intervals of 1 and 3 are $[2, 5]$ and $[6, 9]$ (statement 1), and the interval $[7, 8]$ of 4 lies inside the interval $[1, 10]$ of its ancestor 0 (statement 2, or statement 3 with the roles exchanged).

## History

The name "parenthesis theorem" is from Cormen, Leiserson, Rivest and Stein, who state it with the corollary on nested intervals in the section on depth-first search. Dasgupta, Papadimitriou and Vazirani state the same property of the previsit and postvisit numbers.

## References
