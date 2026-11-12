---
title: Clustering features give exact statistics, and CF tree insertion keeps the tree invariants
proves: [correctness]
status: full
---

We use the pseudocode of the page. Points are vectors in $\mathbb{R}^d$. The clustering feature of a finite nonempty set $P$ is $\mathrm{CF}(P) = (N, \mathrm{LS}, \mathrm{SS})$ with $N = |P|$, $\mathrm{LS} = \sum_{x \in P} x$ (a vector) and $\mathrm{SS} = \sum_{x \in P} \|x\|^2$ (a number).

**Lemma 1 (additivity).** For disjoint $P$ and $Q$, $\mathrm{CF}(P \cup Q) = \mathrm{CF}(P) + \mathrm{CF}(Q)$, added in each component.

*Proof.* Each component is a sum over the points. $\square$

**Lemma 2 (statistics).** Let $\mu = \mathrm{LS}/N$ be the centroid. Then
$$R^2 = \frac{1}{N}\sum_{x \in P}\|x - \mu\|^2 = \frac{\mathrm{SS}}{N} - \|\mu\|^2,$$
and for $N \ge 2$
$$D^2 = \frac{1}{N(N-1)}\sum_{x \in P}\sum_{y \in P}\|x - y\|^2 = \frac{2N\,\mathrm{SS} - 2\|\mathrm{LS}\|^2}{N(N-1)}.$$

*Proof.* For the radius, $\sum_x \|x - \mu\|^2 = \sum_x \|x\|^2 - 2\langle \mu, \sum_x x\rangle + N\|\mu\|^2 = \mathrm{SS} - 2N\|\mu\|^2 + N\|\mu\|^2 = \mathrm{SS} - N\|\mu\|^2$. For the diameter, the terms with $x = y$ are zero, so the double sum is over the $N(N-1)$ ordered pairs of distinct points, and $\sum_x\sum_y \|x - y\|^2 = \sum_x\sum_y (\|x\|^2 + \|y\|^2 - 2\langle x, y\rangle) = 2N\,\mathrm{SS} - 2\|\mathrm{LS}\|^2$. $\square$

The distance between the centroids of two entries is also a function of their CFs. So each test of the insertion uses only CFs.

**The invariants.** Let the tree have parameters $B \ge 2$, $L \ge 2$ and threshold $T$. We claim that after each insertion:

1. (sums) each nonleaf entry is the sum of the entries of its child;
2. (balance) all leaves are at the same depth;
3. (capacity) a leaf has at most $L$ entries, a nonleaf node at most $B$ entries, each node has at least one entry, and a nonleaf root has at least two;
4. (threshold) each leaf entry has $R \le T$;
5. (partition) the leaf entries are the CFs of the parts of a partition of the inserted points (or of the inserted CFs, for a rebuild).

**Theorem.** INSERT keeps the invariants 1 to 5.

*Proof.* The empty tree is one leaf with no entries; after the first insertion it has one entry, and all claims hold.

Consider an insertion of a CF $c$ (a point $x$ is the CF $(1, x, \|x\|^2)$). Lines L1 and L2 follow one path from the root to a leaf.

*At the leaf.* If line L4 merges $c$ into the entry $e$, the new entry is $e + c$, which by Lemma 1 is the CF of the union of the two parts, and its radius is at most $T$ by the test. Otherwise line L5 adds $c$ as a new entry; a single point has $R = 0 \le T$, and a CF from an old tree with a smaller threshold has $R \le T$ already. So 4 and 5 hold. If the leaf now has $L + 1 \ge 3$ entries, line L6 splits it into two leaves; the two seeds go to different sides, so both are nonempty, and each has at most $L$ entries.

*On the way up.* At a nonleaf node, if the child did not split, line L7 adds $c$ to the entry of the child; the child's entries grew by $c$ in total, so 1 holds by Lemma 1. If the child split into two nodes, line L8 replaces its entry by two entries, each the sum of the entries of one half, so 1 holds again. The node then has at most $B + 1$ entries, and if it has $B + 1$ it splits like a leaf into two nonempty nodes with at most $B$ entries each. The children move with their entries, so 1 still holds in both halves.

*At the root.* If the root splits, line L9 makes a new root with the two halves as children and their sums as entries, so the root has two entries and 1 holds.

A split makes a sibling at the same depth, and only a root split adds a level, which adds one to the depth of every leaf at once. So 2 holds. The entries of the nodes off the path do not change. $\blacksquare$

**Corollary.** The sum of the entries of the root is $\mathrm{CF}$ of all inserted points, so the root gives $N$, the centroid and the radius of the whole data set in $O(Bd)$ time.

*Proof.* By invariant 1 and induction on the height, the entries of a node add up to the sum of the leaf entries below it; by invariant 5 that is $\mathrm{CF}$ of all points, by Lemma 1. $\square$

**Rebuild.** Rebuilding with a threshold $T' \ge T$ inserts the old leaf entries into an empty tree. Each old entry has $R \le T \le T'$, so invariant 4 holds for the new tree by the theorem, and the new tree has at most as many leaf entries as the old one, because each old entry either becomes one new entry or is merged into one.
