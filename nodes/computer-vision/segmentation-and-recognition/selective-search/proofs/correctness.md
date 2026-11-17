---
title: Selective search merges each connected part down to one region, keeps exact boxes, histograms and neighbors, and its heap gives the same merges as a full scan
proves: [correctness]
status: full
---

Let $R_0$ be the $n$ starting regions, given by a label map on an image of $p$ pixels with $m$ channels, and let $G_0$ be the neighbor graph: two starting regions are joined when a pixel of one is 4-connected to a pixel of the other. Let $c$ be the number of connected parts of $G_0$. The proofs follow lines L1 to L10 of the page and the Python code, where line L7 is done lazily: a popped pair with a region that is no longer alive is skipped.

For a region $t$ that the run has made, let $M(t) \subseteq R_0$ be the starting regions below it: $M(r) = \{r\}$ for $r \in R_0$, and $M(t) = M(i) \cup M(j)$ when line L6 makes $t$ from $i$ and $j$. Let $P(t)$ be the set of pixels whose label is in $M(t)$. A region is alive from the moment it is made until it is merged. For pixels $P$ let $h(P)$ be the count vector of the histogram, with $25m$ bins, so that the histogram of the page is $C(P) = h(P) / (m |P|)$, which sums to 1.

**Invariant.** Before each pass of line L4, with $A$ the set of alive regions:

1. the sets $M(t)$ for $t \in A$ partition $R_0$;
2. for every $t \in A$, the size of $t$ is $|P(t)|$, its box is the bounding box of $P(t)$, and its histogram is $C(P(t))$;
3. for every $t \in A$, the neighbor set of $t$ is the set of $u \in A$, $u \ne t$, such that some region of $M(t)$ is joined in $G_0$ to some region of $M(u)$;
4. for every pair $u < v$ of alive neighbors the heap holds exactly one entry $(-s(u, v), u, v)$ whose regions are both alive, and the heap holds no other entry whose regions are both alive.

*Proof.* By induction on the passes.

*Start.* Line L1 reads each pixel and its right and lower neighbor, which visits every 4-connected pair of pixels once. The code first makes an empty record for every label and only then adds neighbors, in both directions, so the neighbor sets are those of $G_0$ and are symmetric; this is item 3. Items 1 and 2 hold since each record counts exactly the pixels of its label and the code divides the counts by $m$ times the size. Line L2 pushes one entry for each pair $i < j$ of neighbors, which is item 4.

*Step.* If the popped entry has a region that is not alive, nothing changes except that a stale entry leaves the heap, and items 1 to 4 still hold. Otherwise the entry is $(-s(i, j), i, j)$ with $i, j \in A$, and by item 4 they are neighbors. Line L6 makes $t$ with a new id, larger than every id so far.

- Item 1: $M(t) = M(i) \cup M(j)$ replaces $M(i)$ and $M(j)$, which keeps a partition.
- Item 2: $M(i)$ and $M(j)$ are disjoint, so $P(t) = P(i) \cup P(j)$ is a disjoint union and $|P(t)| = |P(i)| + |P(j)|$. The bounding box of a union of two sets is the box that spans both of their boxes, which is $BB_{ij}$. For the histogram, $h(P(t)) = h(P(i)) + h(P(j))$, so with $s_i = |P(i)|$ and $s_j = |P(j)|$,

$$\frac{s_i C(P(i)) + s_j C(P(j))}{s_i + s_j} = \frac{h(P(i)) / m + h(P(j)) / m}{s_i + s_j} = \frac{h(P(t))}{m |P(t)|} = C(P(t)).$$

The code computes this with exact fractions, so the equality holds exactly.
- Item 3: by item 3 for $i$ and for $j$, the set $(N(i) \cup N(j)) \setminus \{i, j\}$ is the set of alive $u \ne i, j$ with a region of $M(u)$ joined to a region of $M(i) \cup M(j) = M(t)$, which is the correct neighbor set of $t$. The relation in item 3 is symmetric, so an alive $k$ is in this set exactly when $i$ or $j$ is in $N(k)$. For such $k$ the code removes $i$ and $j$ from $N(k)$ and adds $t$, which is correct. For any other alive $k$, $N(k)$ holds neither $i$ nor $j$ and gains no new neighbor, so it stays correct. Pairs of alive regions other than $i$ and $j$ keep their member sets, so their relation does not change.
- Item 4: entries with $i$ or $j$ are now stale. For each new neighbor $k$ of $t$ the code pushes $(-s(k, t), k, t)$, with $k < t$ since $t$ is the largest id, and $t$ is new, so this entry is the only live one for that pair. Every other live pair was a live pair before, with the same two regions, so its entry is still there and still correct. $\square$

**Claim 1 (hierarchy).** The loop ends after exactly $n - c$ merges, and returns $2n - c$ boxes. Each box is the bounding box of the pixels of the starting regions below it.

*Proof.* Each pass pops one entry, and only a merge pushes entries, at most $n$ of them, so the loop ends. By item 3, the graph on $A$ whose edges are the neighbor relation is $G_0$ with each set $M(t)$ contracted to one vertex. Contracting a connected set of vertices keeps the number of connected parts, and $M(t)$ is connected in $G_0$ since it is made by joining neighbors. So this graph always has $c$ parts. A merge lowers $|A|$ by 1. The loop ends when the heap is empty, and by item 4 that happens only when no two alive regions are neighbors, that is, when each of the $c$ parts is one region. So $|A| = c$ at the end and there were $n - c$ merges. Line L3 gives $n$ boxes and each merge one more, $2n - c$ in total. The box claim is item 2. $\square$

**Claim 2 (similarity ranges).** For neighbors $r_i$ and $r_j$, each of $s_{colour}$, $s_{size}$ and $s_{fill}$ lies in $[0, 1]$, so $s$ lies in $[0, a_1 + a_3 + a_4]$.

*Proof.* Histograms are nonnegative and sum to 1, so $0 \le \sum_k \min(c_i^k, c_j^k) \le \sum_k c_i^k = 1$. Both regions are nonempty and disjoint, so $2 \le s_i + s_j \le p$ and $0 \le 1 - (s_i + s_j)/p < 1$. The box $BB_{ij}$ holds all pixels of both regions and lies in the image, so $s_i + s_j \le \operatorname{size}(BB_{ij}) \le p$ and the fraction in $s_{fill}$ lies in $[0, 1)$, which puts $s_{fill}$ in $(0, 1]$. $\square$

Item 2 is why these bounds keep holding after merges: the merged region has the features of its pixels, so it is the same as a starting region with those pixels.

**Claim 3 (heap equals scan).** The heap version and the version that scans all current neighbor pairs at each step, with the same tie rule, make the same merges with the same ids and return the same boxes.

*Proof.* The similarity of a pair depends only on the sizes, boxes and histograms of its two regions, and these are set once at line L6 and never changed. So the key of a live entry stays correct for as long as both regions are alive. The scan keeps a table of the live pairs with their similarities and picks the pair with the smallest $(-s, i, j)$, that is the largest $s$, then the smaller $i$, then the smaller $j$. The heap orders its entries by the same tuple. By item 4 its live entries are exactly the live pairs with their correct similarities, and a stale entry is dropped without effect, so the first live entry that leaves the heap is the smallest live tuple, which is the pair the scan picks. Both versions then make the same region with the same next id and update neighbors in the same way, so by induction they agree at every step. $\square$

**Ranking.** With position $q \ge 1$ and an independent RND uniform in $[0, 1]$, the score $\text{RND} \cdot q$ is uniform in $[0, q]$, so a box with a smaller position is more likely to come first, and no order is fixed between strategies. The ranking step then sorts and keeps the first copy of each box, so its output holds each distinct box of the input exactly once. This is the property that the ranking test checks.
