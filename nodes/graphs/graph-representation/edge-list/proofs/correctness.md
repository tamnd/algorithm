---
title: The operations of an edge list keep the invariant and store the edge set of the graph type
proves: [correctness, termination]
status: full
---

Write $E$ for the edge set that the [graph](/graph/) type prescribes after a sequence of operations: it starts empty, add-edge adds the edge of $u$ and $v$, and remove-edge removes it if it is there. The edge of $u$ and $v$ is $(u, v)$ for a directed graph and $\{u, v\}$ with $u \ne v$ for an undirected graph. Write $e(x, y)$ for the edge that an entry $(x, y)$ stands for, and $E(L) = \{e(x, y) : (x, y) \in L\}$. The invariant (E) is (E1), the entries are pairs of vertices with $x \ne y$ when undirected, and (E2), no two entries match.

**Lemma 1 (MATCH).** MATCH$((x, y), u, v)$ is true if and only if $e(x, y) = e(u, v)$.

*Proof.* For a directed graph, $e(x, y) = e(u, v)$ means $(x, y) = (u, v)$, which is the first test of line L6. For an undirected graph, $\{x, y\} = \{u, v\}$ holds exactly when $(x, y) = (u, v)$ or $(x, y) = (v, u)$, which are the two tests of line L6. $\square$

So (E2) says that distinct entries stand for distinct edges, and then $|L| = |E(L)|$.

**Theorem.** Assume that before an operation (E) holds and $E(L) = E$, and that ADD-EDGE is called only on an edge not in $E$. Then after the operation (E) holds, $E(L)$ equals the new $E$, the queries return the answers of the graph type for $E$, and the operation stops.

*Proof.* We take the operations in turn.

*NEW (line L1).* $L$ is empty, so $E(L) = \emptyset = E$, and (E) holds trivially.

*ADD-EDGE (line L2).* The entry $(u, v)$ is valid, with $u \ne v$ when undirected, so (E1) holds. Its edge is not in $E = E(L)$, so by Lemma 1 it matches no entry, and (E2) holds. The new set is $E(L) \cup \{e(u, v)\} = E \cup \{e(u, v)\}$.

*REMOVE-EDGE (lines L3 to L5).* The scan of line L3 visits the finitely many entries, so it stops. If no entry matches, then by Lemma 1 the edge is not in $E(L) = E$, and nothing needs to change. Otherwise, by (E2) the matching entry at index $i$ is the only entry for the edge $e(u, v)$. Lines L4 and L5 replace it by the last entry and drop the last index; as in the deletion from an unordered array, the multiset of entries loses exactly the entry at $i$. So $E(L)$ loses $e(u, v)$ and no other edge, and the remaining entries still satisfy (E1) and (E2).

*ADJACENT (line L7).* By Lemma 1, some entry matches $(u, v)$ if and only if $e(u, v) \in E(L) = E$.

*NEIGHBORS and DEGREE (lines L8 to L11).* An entry $(x, y)$ stands for an edge at $u$ with other end $z$ exactly when $x = u$ and $z = y$, or, for an undirected graph, $y = u$ and $z = x$. Lines L9 and L10 output $z$ in these cases, and at most once per entry, since L10 runs only when L9 does not; for an undirected graph both cannot hold, as $x \ne y$ by (E1). By (E2) distinct entries at $u$ stand for distinct edges, and in a graph without parallel edges distinct edges at $u$ have distinct other ends. So the output lists each neighbour of $u$ exactly once, and line L11 returns the degree. The loop is over a finite list, so it stops.

*ADD-VERTEX (line L12).* $L$ is unchanged, so the new vertex has no edges, and (E1) still holds since $n$ only grew.

By induction on the number of operations, starting with NEW, (E) and $E(L) = E$ hold after each operation, and each query answers for the current edge set. $\blacksquare$
