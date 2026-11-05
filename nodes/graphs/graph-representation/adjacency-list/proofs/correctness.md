---
title: The operations of an adjacency list keep the invariant and store the edge set of the graph type
proves: [correctness, termination]
status: full
---

Write $E$ for the edge set that the [graph](/graph/) type prescribes after a sequence of operations: it starts empty, add-edge adds the edge of $u$ and $v$, and remove-edge removes it if it is there. The edge of $u$ and $v$ is $(u, v)$ for a directed graph and $\{u, v\}$ with $u \ne v$ for an undirected graph. The lists stand for the set $E(\mathit{Adj})$ of the edges $(u, v)$, or $\{u, v\}$, with $v \in \mathit{Adj}[u]$. The invariant (L) is (L1), no list holds a vertex twice, and (L2), for an undirected graph $v \in \mathit{Adj}[u] \iff u \in \mathit{Adj}[v]$ and no list $\mathit{Adj}[u]$ holds $u$.

**Lemma 1 (DELETE).** Let $L$ be a list with no repeated entry. DELETE$(L, x)$ stops, and afterwards $L$ holds exactly the entries it held before, less $x$, with no repeated entry.

*Proof.* Line L6 scans the finitely many indices of $L$, so it stops. If no entry is $x$, the list is unchanged. Otherwise let $i$ be the index found and $\ell$ the last index. Line L7 writes the entry $L[\ell]$ at index $i$, and line L8 removes index $\ell$. If $i = \ell$, the net effect is to remove $L[\ell] = x$. If $i < \ell$, the entry at index $i$, which was $x$, is now $L[\ell]$, and index $\ell$ is gone, so the entries of $L$ are the old ones less one copy of $x$. By (L1) that was the only copy of $x$, so $x$ is no longer in $L$, and since no new value entered $L$, no entry is repeated. $\square$

**Theorem.** Assume that before an operation (L) holds and $E(\mathit{Adj}) = E$, and that ADD-EDGE is called only on an edge not in $E$. Then after the operation (L) holds, $E(\mathit{Adj})$ equals the new $E$, the queries return the answers of the graph type for $E$, and the operation stops.

*Proof.* We take the operations in turn.

*NEW (line L1).* All lists are empty, so $E(\mathit{Adj}) = \emptyset = E$, and (L) holds trivially.

*ADD-EDGE (lines L2 and L3).* The edge is not in $E = E(\mathit{Adj})$, so $v \notin \mathit{Adj}[u]$, and, for an undirected graph, $u \notin \mathit{Adj}[v]$ by (L2). Line L2 appends $v$ to $\mathit{Adj}[u]$ and, for an undirected graph, line L3 appends $u$ to $\mathit{Adj}[v]$. No list gets a repeated entry, so (L1) holds. In the undirected case the two new entries are a matching pair, and $u \ne v$, so (L2) holds. The new entries stand for the new edge only, so $E(\mathit{Adj}) = E \cup \{e\}$.

*REMOVE-EDGE (lines L4 and L5).* By Lemma 1, line L4 removes $v$ from $\mathit{Adj}[u]$ and nothing else. In the undirected case line L5 removes $u$ from $\mathit{Adj}[v]$; the pair of entries goes away together, so (L2) holds. If the edge was absent, by (L2) neither entry is there and nothing changes. In each case $E(\mathit{Adj}) = E \setminus \{e\}$, and (L1) holds by Lemma 1.

*ADJACENT (line L9).* It returns true exactly when $v \in \mathit{Adj}[u]$, that is, when the edge of $u$ and $v$ is in $E(\mathit{Adj}) = E$. For an undirected graph this does not depend on the order of $u$ and $v$, by (L2).

*NEIGHBORS and DEGREE (lines L10 and L11).* The neighbours of $u$ in $E$, or its out-neighbours, are exactly the entries of $\mathit{Adj}[u]$. Line L10 outputs each entry once, so by (L1) each neighbour once. Line L11 returns the length of the list, which by (L1) is the number of distinct neighbours, the degree. The loop of line L10 runs over a finite list, so it stops.

*ADD-VERTEX (lines L12 and L13).* The new list is empty, so the new vertex has no edges, the old lists are unchanged, and (L) holds.

By induction on the number of operations, starting with NEW, (L) and $E(\mathit{Adj}) = E$ hold after each operation, and each query answers for the current edge set. $\blacksquare$
