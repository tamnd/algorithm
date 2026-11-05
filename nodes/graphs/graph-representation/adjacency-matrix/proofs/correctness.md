---
title: The operations of an adjacency matrix keep the invariant and store the edge set of the graph type
proves: [correctness, termination]
status: full
---

Write $E$ for the edge set that the [graph](/graph/) type prescribes after a sequence of operations: it starts empty, add-edge$(u, v)$ adds the edge of $u$ and $v$, and remove-edge$(u, v)$ removes it if it is there. For a directed graph the edge of $u$ and $v$ is the pair $(u, v)$; for an undirected graph it is the set $\{u, v\}$ with $u \ne v$. The array $A$ stands for the edge set $E(A)$ of the page: the pairs $(u, v)$ with $A[u][v] = 1$ when the graph is directed, and the sets $\{u, v\}$ with $u < v$ and $A[u][v] = 1$ when it is undirected. Invariant (M) is empty in the directed case and is (M1) symmetry and (M2) a zero diagonal in the undirected case.

**Lemma 1.** If (M1) holds, then for $u \ne v$, $\{u, v\} \in E(A)$ if and only if $A[u][v] = 1$, in either order of $u$ and $v$.

*Proof.* If $u < v$ this is the definition. If $u > v$, then $\{u, v\} = \{v, u\}$ with $v < u$, so it is in $E(A)$ if and only if $A[v][u] = 1$, which is $A[u][v] = 1$ by (M1). $\square$

**Theorem.** Assume that before an operation (M) holds and $E(A) = E$. Then after the operation (M) holds, $E(A)$ equals the new $E$, the queries return the answers of the graph type for $E$, and the operation stops.

*Proof.* We take the operations in turn.

*NEW (line L1).* All cells are 0, so $E(A) = \emptyset = E$. A zero array is symmetric with a zero diagonal, so (M) holds.

*ADD-EDGE (lines L2 and L3).* In the directed case line L2 sets exactly the cell $(u, v)$, so $E(A)$ becomes $E \cup \{(u, v)\}$. In the undirected case $u \ne v$ is required, and lines L2 and L3 set the two cells $(u, v)$ and $(v, u)$ to 1. These two cells are mirror images, so symmetry still holds; neither is on the diagonal, so (M2) holds. By Lemma 1 the set $E(A)$ gains $\{u, v\}$ and no other set, since no other cell changed. If the edge was already present the cells were already 1, and nothing changes, which matches $E \cup \{e\} = E$.

*REMOVE-EDGE (lines L4 and L5).* The same argument with 0 in place of 1 gives $E(A) = E \setminus \{e\}$. In the undirected case with $u = v$, line L4 writes 0 on the diagonal, where (M2) already has 0, so nothing changes, and $E$ has no edge $\{u, u\}$ to remove.

*ADJACENT (line L6).* In the directed case $A[u][v] = 1$ if and only if $(u, v) \in E(A) = E$. In the undirected case with $u \ne v$ this is Lemma 1, and with $u = v$ the cell is 0 by (M2), which is the right answer, as $E$ has no loops.

*NEIGHBORS and DEGREE (lines L7 to L9).* The loop of line L7 visits each $v$ from $0$ to $n - 1$ once, in increasing order, and line L8 outputs $v$ exactly when $A[u][v] = 1$. By the case for ADJACENT, these are exactly the $v$ that are out-neighbours of $u$ (directed) or neighbours of $u$ (undirected). Line L9 counts the same set, so it returns the out-degree or the degree. The loop has $n$ steps, so it stops.

*ADD-VERTEX (lines L10 to L13).* Line L11 copies each cell $(i, j)$ with $i, j < n$ to the same place of $B$, and the cells in row $n$ or column $n$ stay 0. So after line L12 the edges among the old vertices are unchanged, and the new vertex $n$ has no edges, which is what the graph type prescribes. $B$ restricted to the old cells is symmetric with a zero diagonal when $A$ was, and the new row and column are zero, so (M) holds. Line L13 returns the number of the new vertex. Lines L10 and L11 run over finitely many cells, so they stop.

Each operation keeps (M) and the equality $E(A) = E$, so by induction on the number of operations, these hold after each sequence of operations that starts with NEW, and each query answers for the current edge set. $\blacksquare$
