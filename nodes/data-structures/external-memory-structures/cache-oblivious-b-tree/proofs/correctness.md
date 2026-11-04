---
title: The index stays exact after every update, and the search finds the predecessor
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The PMA has $2^H$ segments of $S$ cells. The index is a complete binary tree with $H + 1$ levels; the node at depth $d$ with path $p$ has the segments $p \cdot 2^{H-d}$ to $(p+1) 2^{H-d} - 1$ below it. Its position in the index array is $\mathrm{POS}(H+1, d, p)$, which is a bijection onto $\{0, \ldots, 2^{H+1} - 2\}$ by the proof on the [van Emde Boas layout](/van-emde-boas-layout/) page, so distinct nodes have distinct cells. The PMA keeps its key sequence strictly increasing and equal to the stored set, and every operation of the PMA ends; both facts are proved on the [packed memory array](/packed-memory-array/) page. We write (C1) for this, and (C2), (C3) for the conditions on the index from the page. For a node $v$, let $K(v)$ be the set of keys in the segments below $v$.

**Lemma 1.** If (C1), (C2) and (C3) hold, then for every node $v$, $\min(v)$ is the smallest element of $K(v)$, or none if $K(v)$ is empty.

*Proof.* By induction on the height of $v$. For a leaf, this is (C2) with (C1): the first key of a segment is its smallest key. For an internal node, $K(v) = K(\text{left}(v)) \cup K(\text{right}(v))$, and by (C1) every key of the left part is smaller than every key of the right part, since the left segments come first. So the smallest element of $K(v)$ is that of the left part if it is not empty, and that of the right part otherwise, which is (C3) with the induction hypothesis. $\square$

**Lemma 2 (UPDATE).** Suppose (C2) and (C3) held, and then the PMA changed only the cells of segments $s_0$ to $s_1$. After UPDATE$(s_0 .. s_1)$, (C2) and (C3) hold.

*Proof.* Call a node *changed* if one of the segments $s_0, \ldots, s_1$ is below it. A node that is not changed has the same segments below it with the same contents, and its children are not changed either; its value was right before and still is, since (C2) and (C3) for it refer only to unchanged things. Line L11 sets every changed leaf by (C2). The changed nodes at depth $d < H$ are exactly those with $p$ from $\lfloor s_0 / 2^{H-d} \rfloor$ to $\lfloor s_1 / 2^{H-d} \rfloor$, which is the range of line L13. Lines L12 and L13 go from depth $H - 1$ up to 0, so when a node at depth $d$ is set, both its children, at depth $d + 1$, already have their final values: they were set in the pass before, or at line L11, or they are not changed. So (C3) holds at each changed node after it is set, and later passes do not change it again. $\square$

**Lemma 3 (BUILD).** After BUILD, (C2) and (C3) hold.

*Proof.* Line L14 calls UPDATE on all segments, so every node is changed and set, leaves first and then by increasing height, as in Lemma 2. $\square$

**Lemma 4 (SEARCH).** If (C1), (C2) and (C3) hold, SEARCH$(k)$ returns the position of the largest key at most $k$, or none if there is none.

*Proof.* If no key is at most $k$, the scan of line L4 finds no key at most $k$ in any segment, so SEARCH returns none, which is right. Otherwise let $\pi$ be the largest key at most $k$. We show the invariant at the start of each pass of line L2: $\pi \in K(v)$. At the root, $K(v)$ holds all keys.

Consider a pass at node $v$ with $\pi \in K(v)$. If $\min(\text{right}(v)) \ne$ none and $\min(\text{right}(v)) \le k$, then by Lemma 1 the right part has a key at most $k$, and every key of the left part is smaller than it by (C1); so $\pi$, the largest key at most $k$, is not in the left part, and $\pi \in K(\text{right}(v))$. Otherwise, by Lemma 1, the right part is empty or all its keys exceed $k$, so $\pi$ is not in it, and $\pi \in K(\text{left}(v))$. In both cases line L3 moves to the child that holds $\pi$.

The loop ends after $H$ passes, since each moves one level down. At the leaf, $\pi$ is in the segment, whose keys are in order by (C1), and no key after $\pi$ in it is at most $k$. So the scan of line L4 returns the position of $\pi$. $\square$

**Lemma 5 (INSERT and DELETE).** If (C1) to (C3) hold before an update, they hold after it, and the set changes as specified.

*Proof.* By Lemma 4, line L5 or L9 finds the predecessor of $k$, which is the position that the PMA insert and delete use; so by the proof of the PMA, (C1) holds after the PMA step and the set changes as specified. If the PMA resized, the index is built again, and Lemma 3 gives (C2) and (C3). Otherwise, the PMA changed only the cells of the window $W$, which is a run of whole segments; for a delete without a rebalance, $W$ is the segment of the deleted cell. Lines L8 and L10 call UPDATE on exactly these segments, and Lemma 2 gives (C2) and (C3). $\square$

**Termination.** SEARCH makes $H$ passes and scans $S$ cells. UPDATE runs over finite ranges. The PMA steps end, by the proof of the PMA. So every operation ends.

The empty structure is built by BUILD, so (C1) to (C3) hold at the start. By Lemma 5 they hold after every update, and by Lemma 4 every predecessor query is right; `contains` and `range` follow from it and from (C1), as for the PMA. $\blacksquare$
