---
title: The cleanup and fixup procedures keep all shortest paths
proves: [correctness]
status: full
---

This proof is for the version on the page: CLEANUP and FIXUP over a store of paths, without smoothing. Edge weights are nonnegative.

**Order on walks.** Each edge $e$ has a distinct number $\mathrm{id}(e)$. The key of a walk $\pi$ is $k(\pi) = \big(w(\pi), \mu(\pi)\big)$ with $\mu(\pi) = \sum 2^{\mathrm{id}(e)}$ over the edges of $\pi$ with repetition, compared in lexicographic order. Keys add up when walks are joined, and each edge adds a positive amount to $\mu$.

**Lemma 1.** If some walk goes from $x$ to $y \ne x$, there is a unique walk $\pi^*_{xy}$ of least key. It is a simple path, and each of its subpaths with at least one edge is the least walk between its ends.

*Proof.* A walk that repeats a vertex contains a closed subwalk with at least one edge; removing it gives a walk with a smaller key, because the closed subwalk has $w \ge 0$ and $\mu > 0$. So a least walk, if one exists, is a simple path. There are finitely many simple paths, and two different simple paths from $x$ to $y$ have different edge sets, so different values of $\mu$. So the least one is unique. If a subpath were not least, replacing it by a lighter walk would give a lighter walk from $x$ to $y$. $\square$

We call $\pi^*_{xy}$ the shortest path, and the key order on paths "lighter". For a stored path $P$ with at least one edge, $l(P)$ and $r(P)$ are as on the page; for an edge, they are the one-vertex paths, which are fixed objects.

**Invariants.** Between updates:

- (I1) Each stored path is a simple path from $x$ to $y \ne x$ in the current graph, with its key computed from current weights.
- (I2) For a stored path $P$ with at least two edges, $l(P)$ and $r(P)$ are stored, $P \in L_{ext}(l(P))$ and $P \in R_{ext}(r(P))$.
- (I3) For each edge of the graph, its edge path is stored.
- (I4) No two stored paths have the same vertex sequence.
- (I5) $\mathrm{SP}[x, y] = \pi^*_{xy}$ for each pair with a path from $x$ to $y$, and $\mathrm{SP}[x, y]$ is empty otherwise. The paths in the lists $L^*$ and $R^*$ are exactly the values of $\mathrm{SP}$, each in $L^*(r(\sigma))$ and $R^*(l(\sigma))$.
- (I6) For any two values $a, b$ of $\mathrm{SP}$ with $r(a) = l(b)$ and $x(a) \ne y(b)$, the path with $l = a$ and $r = b$ is stored.

At the start the graph has no edges and the store is empty, so all invariants hold.

**Lemma 2 (CLEANUP).** After line L1, the stored paths are exactly the old stored paths that do not pass through $v$, and (I2), (I4), (I6) hold, with $\mathrm{SP}$ cleared for each pair whose shortest path passed through $v$ and unchanged for the other pairs.

*Proof.* A stored path with at least two edges is the union of $l(P)$ and $r(P)$, so by induction on its length, each edge of $P$ lies in $l(P)$ or in $r(P)$. A stored path through $v$ contains an edge at $v$. By (I2), following $L_{ext}$ and $R_{ext}$ from the edge path of that edge reaches $P$ by induction on length, so line L8 puts $P$ into $Q$. Conversely, each path that enters $Q$ is an edge path at $v$ or extends a path through $v$, so it passes through $v$. Line L7 clears exactly the removed values of $\mathrm{SP}$ and their list entries. (I2) holds because a path whose $l$ or $r$ was removed was itself removed. (I4) holds for a subset. For (I6): if $a$ and $b$ remain values of $\mathrm{SP}$, they avoid $v$, so their combination avoids $v$, was stored, and was not removed. $\square$

Line L2 changes only edges at $v$, and no remaining stored path uses such an edge. So (I1) holds for the new graph $G'$, and (I3) holds for every edge of $G'$ that does not touch $v$. Line L9 stores the edge paths of the edges at $v$, so (I3) holds for $G'$, and (I4) still holds, since no edge path at $v$ remained. Each path that COMBINE creates satisfies (I1): its parts are values of $\mathrm{SP}$, so by induction they are simple paths of $G'$, $r(a) = l(b)$ makes them overlap in all but one edge at each end, and line L18 or L19 checks that its two ends differ, so it is a simple path with the key $k(a)$ plus the key of one edge. COMBINE keeps (I2) by line L22, and (I4): two stored paths with the same vertex sequence of at least two edges would have $l$ parts with the same sequence and $r$ parts with the same sequence, so by induction the same $l$ and $r$, and line L20 prevents a second copy.

**Lemma 3 (FIXUP).** FIXUP settles the pairs that are connected in $G'$ in increasing order of the key of their shortest path, and it settles each such pair $(x, y)$ with $\pi = \pi^*_{xy}$.

*Proof.* The keys that leave $H$ do not decrease, because each path inserted at line L23 is heavier than the path $\pi$ of the current step: it contains $\pi$ and one more edge. Every path in $H$ is stored, so by (I1) it is a path of $G'$ and at least as heavy as the shortest path of its pair.

We show by induction over the shortest paths in increasing key order that $P = \pi^*_{xy}$ is in $H$ before any path of key larger than $k(P)$ leaves $H$. Then the first path of the pair $(x, y)$ that leaves $H$ is $P$, since $P$ is strictly lighter than every other path of the pair.

If $P$ is one edge, its edge path is stored by (I3). As the lightest stored path of its pair, it is put into $H$ at line L10.

Let $P$ have at least two edges. By Lemma 1, $A = l(P)$ and $B = r(P)$ are shortest paths, and both are lighter than $P$. By induction, their pairs are settled before any path of key $k(P)$ or more leaves $H$, and after their settling steps, $\mathrm{SP}$ holds them. The paths $r(A)$ and $l(B)$ have the same vertex sequence and are both stored, or both the same one-vertex path, so by (I4) they are the same object. A pair is settled only once in a FIXUP, so once a pair's $\mathrm{SP}$ is set during FIXUP or confirmed at line L15, it does not change again.

- If both $A$ and $B$ were values of $\mathrm{SP}$ before FIXUP and stay so, then by (I6) the path with $l = A$ and $r = B$, which is $P$, was stored before FIXUP. It is the lightest stored path of its pair, so line L10 put it into $H$.
- Otherwise consider the step that executes line L17 for the later of $A$ and $B$ to become a value of $\mathrm{SP}$. At that step the other one is a value of $\mathrm{SP}$: either it was set earlier in this FIXUP, or it was a value before FIXUP and its pair has not been settled with a different path, because its shortest path is still the same object. If the new value is $B$, then $A \in L^*(r(A)) = L^*(l(B))$, so line L18 calls COMBINE$(A, B)$. If the new value is $A$, then $B \in R^*(l(B)) = R^*(r(A))$, so line L19 calls COMBINE$(A, B)$. The ends of $P$ differ, so the test passes. COMBINE either inserts $P$ into $H$ at line L23, or finds it stored. A path that is stored and not yet in $H$ was stored before FIXUP, as paths created in FIXUP enter $H$ when they are created; then it is the lightest stored path of its pair and line L10 put it into $H$.

In both cases $P$ enters $H$ at a step that settles a path lighter than $P$, so before any path of key $k(P)$ or more leaves $H$. $\square$

**Theorem.** After each update, (I1) to (I6) hold, so $\mathrm{dist}(x, y)$ returns $d(x, y)$ and $\mathrm{path}(x, y)$ returns a shortest path.

*Proof.* (I1) to (I4) hold by Lemma 2 and the remarks after it. By Lemma 3, each connected pair has $\mathrm{SP}[x, y] = \pi^*_{xy}$ after FIXUP. If $(x, y)$ is not connected in $G'$, no stored path joins them by (I1), so the pair is never settled; its old value of $\mathrm{SP}$ would be a stored path from $x$ to $y$, so it was cleared by CLEANUP. Lines L16 and L17 keep the lists $L^*$ and $R^*$ equal to the values of $\mathrm{SP}$, which gives (I5). For (I6), take values $a$ and $b$ of $\mathrm{SP}$ after FIXUP with $r(a) = l(b)$ and $x(a) \ne y(b)$. If both were values before FIXUP, (I6) held before and the combination was not removed. Otherwise, as in the proof of Lemma 3, the later of the two to be set at line L17 found the other in $L^*$ or $R^*$ and called COMBINE on them. A path is removed only by CLEANUP, so the combination is still stored. $\blacksquare$
