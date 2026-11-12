---
title: The maximum update gives the greedy complete linkage merges, at the diameters
proves: [correctness]
status: full
---

For disjoint clusters, $\mathcal{L}(A, B) = \max_{a \in A, b \in B} D(a, b)$, and $\text{diam}(A) = \max_{a, a' \in A} D(a, a')$, with $\text{diam}(\{a\}) = 0$. We write $C_s$ for the cluster in slot $s$.

**Invariant (C).** At the start of each round of line L2, the clusters $C_s$ of the active slots are the clusters after the merges so far, $\text{size}[s] = |C_s|$, and $D[s, r] = \mathcal{L}(C_s, C_r)$ for active $s \ne r$.

*Proof.* At line L1, each slot holds one point and $D[s, r] = D(s, r) = \mathcal{L}(\{s\}, \{r\})$. Assume (C) at the start of a round, and let line L3 pick $i, j$. For $k \ne i, j$, the pairs of $C_k \times (C_i \cup C_j)$ split into those of $C_k \times C_i$ and those of $C_k \times C_j$, so

$$\mathcal{L}(C_k, C_i \cup C_j) = \max\bigl(\mathcal{L}(C_k, C_i),\ \mathcal{L}(C_k, C_j)\bigr) = \max(D[i, k], D[j, k]),$$

which line L5 stores. Line L5 for one $k$ reads only the entries of $k$, so it reads old values. Line L7 makes slot $i$ hold $C_i \cup C_j$ and drops $j$. The other entries and clusters do not change. So (C) holds again. $\square$

**Theorem.** COMPLETE-LINKAGE returns $n - 1$ merges. Merge $t$ joins two current clusters $A$, $B$ with the smallest $\mathcal{L}(A, B)$ over all pairs of current clusters, at height $h_t = \mathcal{L}(A, B)$. The heights satisfy $h_1 \le h_2 \le \cdots \le h_{n-1}$, and $h_t = \text{diam}(A \cup B)$.

*Proof.* By (C), line L3 picks a pair of current clusters with the smallest linkage value, and records it as $h$. Each round drops one slot, so there are $n - 1$ rounds.

*Monotone.* In round $t$, $h_t = D[i, j] \le D[i, k]$ and $h_t \le D[j, k]$ for each other active $k$, because $i, j$ is the smallest pair. So each new value $\max(D[i, k], D[j, k])$ is at least $h_t$. The values between other slots were at least $h_t$ already. So all values after round $t$ are at least $h_t$, and $h_{t+1} \ge h_t$.

*Diameters.* By induction on $t$, each current cluster made by a merge at height $h_s$ has diameter $h_s$, and each single point has diameter 0. In round $t$, the cluster $A \cup B$ has

$$\text{diam}(A \cup B) = \max\bigl(\text{diam}(A),\ \text{diam}(B),\ \mathcal{L}(A, B)\bigr).$$

The diameters of $A$ and $B$ are 0 or earlier heights, which are at most $h_t = \mathcal{L}(A, B)$ by the monotone order. So $\text{diam}(A \cup B) = h_t$. $\square$

**Corollary (cuts).** For each $h$, the clusters of the merges of height at most $h$ have diameter at most $h$. For each $k$, the cut into $k$ clusters has largest diameter $h_{n-k}$, or 0 when $k = n$.

*Proof.* Each cluster of the cut is a single point or the result of a merge of height at most $h$ (or at most $h_{n-k}$), and its diameter is that height. The largest is the last merge kept. $\square$

**The cut is not always optimal.** On the points $0, 1, 6, 9, 13$ with $D(x, y) = |x - y|$, the merges are $\{0, 1\}$ at 1, $\{6, 9\}$ at 3, $\{6, 9, 13\}$ at 7 (against 9 for $\{0, 1\}$ with $\{6, 9\}$ and 13 for $\{0, 1\}$ with $\{13\}$), and all at 13. The cut at $k = 2$ has largest diameter 7, while $\{0, 1, 6\}$, $\{9, 13\}$ has largest diameter 6. So the theorem gives a greedy bound, not an optimum.

**Running time.** The round with $m$ active slots scans $m(m - 1)/2$ pairs at line L3 and updates $m - 2$ entries at line L5, so the total over $m = n, \ldots, 2$ is $\Theta(n^3)$. The copy of $D$ takes $\Theta(n^2)$ memory.
