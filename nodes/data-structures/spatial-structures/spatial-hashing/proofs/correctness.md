---
title: Spatial hashing keeps one entry per box and cell, and a query reports each box that meets it exactly once
proves: [correctness, termination]
status: full
---

Write $C(b)$ for the set of cells that the closed box $b$ meets, and $\operatorname{cell}(p)$ for the cell of the point $p$. For a closed box $b = [x_1, x_2] \times [y_1, y_2]$, a cell $(i, j)$ is in $C(b)$ exactly when $\lfloor x_1/h \rfloor \le i \le \lfloor x_2/h \rfloor$ and $\lfloor y_1/h \rfloor \le j \le \lfloor y_2/h \rfloor$; this is the set of cells of the points of $b$, since the cell index is a monotone function of each coordinate and takes every integer value between its values at the two ends. In particular, if $p \in b$ then $\operatorname{cell}(p) \in C(b)$.

**Invariant (S).** For each stored box $(id, b)$ and each $(i, j) \in C(b)$, bucket $H(i, j)$ holds the entry $(i, j, id, b)$ exactly once, and there are no other entries.

**INSERT.** Lines L1 and L2 add the entry $(i, j, id, b)$ to bucket $H(i, j)$ for each $(i, j) \in C(b)$ and for no other cell. If $(id, b)$ was not stored before, this gives (S) for the new set. $C(b)$ is finite, so INSERT stops.

**DELETE.** By (S), for each $(i, j) \in C(b)$ the bucket $H(i, j)$ holds the entry $(i, j, id, b)$ once, and line L9 removes it; moving the last entry of the list into the free place does not change the multiset of the other entries. After the loop, no entry of $(id, b)$ is left and the others are kept, so (S) holds for the set without $(id, b)$. If the box was not stored, no entry matches, and nothing changes.

**QUERY.** *Soundness.* An id is reported in line L7 only for an entry $(i, j, id, b)$ that passed line L6, so $b$ meets $q$, and by (S) $(id, b)$ is stored.

*Each stored box that meets $q$ is reported.* Let $(id, b)$ be stored with $b \cap q \ne \emptyset$. The intersection of two closed boxes that meet is the closed box $[\max(q_{x1}, b_{x1}), \min(q_{x2}, b_{x2})] \times [\max(q_{y1}, b_{y1}), \min(q_{y2}, b_{y2})]$, so its lower left corner $p = (\max(q_{x1}, b_{x1}), \max(q_{y1}, b_{y1}))$ lies in both $b$ and $q$. Let $(i, j) = \operatorname{cell}(p)$. Since $p \in q$, $(i, j) \in C(q)$, and line L4 visits it. Since $p \in b$, $(i, j) \in C(b)$, and by (S) bucket $H(i, j)$ holds $(i, j, id, b)$. Line L5 meets this entry, line L6 lets it pass, and the test of line L7 holds, so $id$ is reported.

*Each is reported once.* Line L4 visits each cell of $C(q)$ once. In a visited cell $(i', j')$, by (S) bucket $H(i', j')$ holds at most one entry $(i', j', id, b)$ for the box, so the box can be reported at most once per cell, and only when $\operatorname{cell}(p) = (i', j')$. The point $p$ has exactly one cell, so the box is reported in at most one cell.

*Termination.* $C(q)$ is finite and each bucket is a finite list.

**CLOSE PAIRS.** For each cell, the code tests each pair of distinct entries of that cell, and reports the pair when the boxes meet and the lower left corner of their intersection lies in the cell. The argument above, with $b_1$ in place of $q$ and $b_2$ in place of $b$, shows that each pair of stored boxes that meet has both entries in the cell of that corner, and that the corner has one cell, so each such pair is reported exactly once, and no other pair is reported. $\blacksquare$
