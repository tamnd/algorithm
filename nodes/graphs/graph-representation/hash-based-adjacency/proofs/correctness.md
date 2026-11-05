---
title: The operations of hash-based adjacency keep the invariant and store the graph of the graph type
proves: [correctness, termination]
status: full
---

We use only the set semantics of a [hash table](/hash-table/): a hash set stores a finite set, insertion adds an element (and changes nothing if it is present), deletion removes it (and changes nothing if it is absent), membership answers correctly, and iteration lists each element once and stops. A hash map stores a finite set of keys with one value each. Time bounds are a separate matter and are not part of this proof.

The structure stands for the graph $G(S)$ whose vertex set is the key set $K$ of $S$ and whose edges are the pairs $(u, v)$ with $v \in S[u]$ for a directed graph, or the sets $\{u, v\}$ with $v \in S[u]$ for an undirected graph. The invariant (H) is (H1) all elements of the sets are keys, (H2) symmetry without loops when undirected, and (H3) $P$ has the keys of $S$ and mirrors it when directed. Write $V$ and $E$ for the vertex and edge sets that the [graph](/graph/) type prescribes after a sequence of operations: add-vertex adds a vertex, add-edge adds both ends and the edge, remove-edge removes the edge, and remove-vertex removes the vertex and all edges at it.

**Theorem.** Assume that before an operation (H) holds and $G(S) = (V, E)$. Then after the operation (H) holds, $G(S)$ is the new $(V, E)$, the queries return the answers of the graph type, and the operation stops.

*Proof.* *NEW (line L1)* gives empty maps, so $G(S)$ is the empty graph, and (H) holds trivially.

*ADD-VERTEX (line L2).* If $x \in K$ nothing changes, and $x \in V$ already. Otherwise $x$ becomes a key with an empty set, and with an empty in-set when directed. No set gains an element, so (H1) to (H3) hold, and $G(S)$ gains the isolated vertex $x$.

*ADD-EDGE (lines L3 to L5).* After line L3, $u$ and $v$ are keys. In the undirected case $u \ne v$, line L4 adds $v$ to $S[u]$ and line L5 adds $u$ to $S[v]$; both are keys, so (H1) holds, the new elements form a matching pair, so (H2) holds, and no loop is added. In the directed case lines L4 and L5 add $v$ to $S[u]$ and $u$ to $P[v]$, which keeps (H3). In both cases the edge set of $G(S)$ gains exactly the edge of $u$ and $v$, or is unchanged if it was there, which matches $E \cup \{e\}$.

*REMOVE-EDGE (lines L6 and L7).* The two deletions remove a matching pair, or nothing if the edge was absent, by (H2) or (H3). So (H) holds and the edge set becomes $E \setminus \{e\}$.

*ADJACENT (line L8)* returns true exactly when $u \in K$ and $v \in S[u]$, which is the definition of the edge being in $G(S)$; for an undirected graph the order of $u$ and $v$ does not matter, by (H2).

*NEIGHBORS and DEGREE (lines L9 and L10).* $S[u]$ is by definition the set of (out-)neighbours of $u$ in $G(S)$, so iterating it lists each once, and its size is the degree.

*REMOVE-VERTEX (lines L11 to L13).* Let $x \in K$; otherwise nothing changes. Undirected: by (H2) the keys whose sets contain $x$ are exactly the elements $y$ of $S[x]$, and line L11 deletes $x$ from each $S[y]$. After line L13 deletes the key $x$, no set contains $x$, so (H1) holds, and the remaining pairs are still matching, so (H2) holds. Directed: by (H3) the sets $P[y]$ that contain $x$ are those with $y \in S[x]$, and the sets $S[y]$ that contain $x$ are those with $y \in P[x]$. Lines L11 and L12 delete $x$ from all of them, and line L13 deletes the key $x$ from both maps, so (H1) and (H3) hold. In both cases the deleted elements are exactly those that stand for edges at $x$, so $G(S)$ loses $x$ and the edges at $x$ and nothing else. The loops of lines L11 and L12 iterate over copies of finite sets, so they stop even though the sets they delete from may include the set being read, as with a self-loop $x \in S[x]$.

By induction on the number of operations, starting with NEW, (H) holds and $G(S)$ is the graph of the graph type after each operation. $\blacksquare$
