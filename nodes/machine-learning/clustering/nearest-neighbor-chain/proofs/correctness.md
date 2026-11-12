---
title: For a reducible linkage, the nearest-neighbor chain gives the greedy hierarchy
proves: [correctness]
status: full
---

**Setting.** A *state* is a partition $P$ of the points into clusters, each with its sub-hierarchy. For the five linkages (single, complete, average, weighted, Ward), the value $\mathcal{L}(A, B)$ that the Lance-Williams updates give for two clusters depends only on $A$ and $B$ with their sub-hierarchies, not on the order of other merges. For single, complete and average linkage it is the least, largest or mean dissimilarity between $A$ and $B$. For Ward on squared Euclidean distances it is twice the increase of the sum of squares. For weighted linkage it is $\sum_{a \in A, b \in B} 2^{-\delta_A(a) - \delta_B(b)} D(a, b)$, where $\delta_A(a)$ is the depth of the leaf $a$ in the sub-hierarchy of $A$. An *RNN pair* of $P$ is a pair $A \ne B$ in $P$ such that each is the nearest neighbor of the other. A merge of $A$, $B$ at height $\mathcal{L}(A, B)$ turns $P$ into $P_{AB}$.

**Reducibility.** For disjoint $I$, $J$, $K$: if $\mathcal{L}(I, J) \le \min(\mathcal{L}(I, K), \mathcal{L}(J, K))$, then $\mathcal{L}(I \cup J, K) \ge \min(\mathcal{L}(I, K), \mathcal{L}(J, K))$. The five linkages are reducible: the new value is the minimum (single), the maximum (complete), a mean with positive weights (average, weighted) of $\mathcal{L}(I, K)$ and $\mathcal{L}(J, K)$, so it is at least their minimum. For Ward, see Lemma 4 of the [Ward proof](/ward-method/).

**No ties.** We assume that the values $\mathcal{L}(A, B)$ that the algorithms compare are all different. Then each cluster has one nearest neighbor, and two different RNN pairs are disjoint.

**Lemma 1 (an RNN pair survives other merges).** Let $(A, B)$ and $(I, J)$ be two different RNN pairs of $P$. Then $(A, B)$ is an RNN pair of $P_{IJ}$.

*Proof.* The pairs are disjoint. In $P_{IJ}$, only the values to $I \cup J$ are new. Since $(I, J)$ is an RNN pair, $\mathcal{L}(I, J) \le \min(\mathcal{L}(I, A), \mathcal{L}(J, A))$, so by reducibility $\mathcal{L}(I \cup J, A) \ge \min(\mathcal{L}(I, A), \mathcal{L}(J, A))$. Both values on the right exceed $\mathcal{L}(A, B)$, because $B$ is the only nearest neighbor of $A$ in $P$. So $\mathcal{L}(A, I \cup J) > \mathcal{L}(A, B)$, and $B$ is still the nearest neighbor of $A$. The same holds for $B$. $\square$

**Lemma 2 (any order of RNN merges gives the same hierarchy).** Call a run from a state $P$ an *RNN run* if each of its merges joins an RNN pair of the current state, until one cluster is left. Then all RNN runs from $P$ make the same set of merges, with the same heights. Call this set $R(P)$.

*Proof.* Induction on $|P|$. For $|P| = 1$ there are no merges. Let $|P| > 1$, and take two RNN runs that start with the pairs $(A, B)$ and $(I, J)$. By induction, the first run makes $\{(A, B)\} \cup R(P_{AB})$ and the second makes $\{(I, J)\} \cup R(P_{IJ})$. If the pairs are the same, we are done. If not, by Lemma 1, $(I, J)$ is an RNN pair of $P_{AB}$ and $(A, B)$ is an RNN pair of $P_{IJ}$. Both lead to the same state $P_{AB, IJ}$, and the heights $\mathcal{L}(A, B)$ and $\mathcal{L}(I, J)$ do not depend on the order. By induction on $P_{AB}$ and $P_{IJ}$, $R(P_{AB}) = \{(I, J)\} \cup R(P_{AB, IJ})$ and $R(P_{IJ}) = \{(A, B)\} \cup R(P_{AB, IJ})$. So the two sets are equal. $\square$

**Corollary.** The greedy method is an RNN run: the pair with the least value over all pairs is an RNN pair. So $R(\text{the singletons})$ is the greedy hierarchy.

**Lemma 3 (the chain invariant).** At the start of each round of line L3, the chain $c_1, \ldots, c_r$ holds distinct active clusters, $c_{t+1}$ is the nearest neighbor of $c_t$ in the current state for $t < r$, and $\mathcal{L}(c_1, c_2) > \mathcal{L}(c_2, c_3) > \cdots > \mathcal{L}(c_{r-1}, c_r)$.

*Proof.* It holds for the empty chain at line L2, and after line L4, which makes a chain of one cluster.

*A push.* Line L12 pushes $b$, the nearest neighbor of $a = c_r$, so the new link is right. If $r \ge 2$, then $b \ne c_{r-1}$, so $\mathcal{L}(a, b) < \mathcal{L}(a, c_{r-1})$ by the tie rule of line L6 and the uniqueness of the nearest neighbor. So the values still decrease. The new cluster $b$ is not in the chain: if $b = c_s$ with $s < r - 1$, then $c_{s+1}$ is the nearest neighbor of $b$, so $\mathcal{L}(c_s, c_{s+1}) \le \mathcal{L}(b, a) < \mathcal{L}(c_{r-1}, c_r) \le \mathcal{L}(c_s, c_{s+1})$, which is false.

*A merge.* Lines L7 to L11 merge $a = c_r$ and $b = c_{r-1}$, which are an RNN pair: $b$ is the nearest neighbor of $a$ by line L6, and $a$ is the nearest neighbor of $b$ by the invariant. The chain becomes $c_1, \ldots, c_{r-2}$. For $t \le r - 3$, the cluster $c_{t+1}$ is neither $a$ nor $b$. The only new value for $c_t$ is $\mathcal{L}(c_t, a \cup b)$. By reducibility it is at least $\min(\mathcal{L}(c_t, a), \mathcal{L}(c_t, b))$, which exceeds $\mathcal{L}(c_t, c_{t+1})$. So $c_{t+1}$ is still the nearest neighbor of $c_t$, and the values do not change. $\square$

**Lemma 4 (termination).** The loop ends after at most $3n - 2$ rounds.

*Proof.* By Lemma 3, the chain holds distinct active clusters, so it never has more clusters than there are active ones. Each round ends with a merge (line L8) or with a push at line L12. Each merge removes one active cluster, so there are at most $n - 1$ merges, and the loop ends after the merge that leaves one cluster. Each merge pops two clusters, and at the end the chain holds at most one cluster, so the number of pushes, at lines L4 and L12 together, is at most $2(n - 1) + 1$. So there are at most $(n - 1) + (2n - 1) = 3n - 2$ rounds, and the loop ends with exactly $n - 1$ merges. $\square$

**Theorem.** With no ties, NN-CHAIN$(D, \mathcal{L})$ for a reducible linkage returns the merges of the greedy hierarchy at their heights, in order of height.

*Proof.* By Lemma 3, each merge of the loop joins an RNN pair of the current state, and line L10 gives the values of the new state by the Lance-Williams update. By Lemma 4 the loop ends with one cluster, so the run is an RNN run. By Lemma 2 and the Corollary, its merges are the greedy merges with the same heights. The greedy heights do not decrease: when the greedy method merges the closest pair $I$, $J$, reducibility gives $\mathcal{L}(I \cup J, K) \ge \min(\mathcal{L}(I, K), \mathcal{L}(J, K)) \ge \mathcal{L}(I, J)$ for each other $K$, so all values after the merge are at least its height. So the stable sort of line L13 gives the greedy order. $\square$

**Ties.** With ties, Lemma 3 holds with "a nearest neighbor" in place of "the nearest neighbor" and "do not increase" in place of "decrease". The tie rule of line L6 still makes each push strictly decrease the value, so the loop ends, and each merge joins two clusters that are nearest neighbors of each other.

**Centroid linkage.** Reducibility is needed. Take the points $(0, 3)$, $(8, 6)$, $(1, 11)$, $(8, 1)$ and centroid linkage on squared distances. At the start, $(0, 3)$ and $(1, 11)$ are an RNN pair at 65, and the chain from $(0, 3)$ merges them. The greedy method first merges $(8, 6)$ and $(8, 1)$ at 25. The centroid $(8, 3.5)$ of the union is at $257/4$ from $(0, 3)$, which is less than both 73 and 68, the values for the two parts. So reducibility fails, Lemma 1 fails, and the greedy method never merges $(0, 3)$ with $(1, 11)$ first.

**Running time.** Each round costs $O(n)$: the scan of line L6 reads one row, and line L10 updates one row. With at most $3n - 2$ rounds, the loop takes $O(n^2)$ time. The sort of line L13 takes $O(n \log n)$. The memory is the matrix, $\Theta(n^2)$, and the chain, $O(n)$.
