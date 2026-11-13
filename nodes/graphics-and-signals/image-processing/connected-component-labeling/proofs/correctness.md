---
title: Two-pass labeling gives the same label to two foreground pixels exactly when they are connected
proves: [correctness]
status: full
---

Fix a binary image $B$ of $W \times H$ pixels and a connectivity $c \in \{4, 8\}$. Let $G$ be the graph whose nodes are the foreground pixels, with an edge between two pixels that are adjacent under $c$. The components of the image are the connected components of $G$. Write $p \prec q$ when $p$ comes before $q$ in raster order, that is, $p$ is in an earlier row, or in the same row and an earlier column.

**Lemma 1 (scanned neighbors).** For a pixel $q = (x, y)$, the set of positions scanned at line L5 is exactly the set of positions $p$ adjacent to $q$ under $c$ with $p \prec q$.

*Proof.* The neighbors of $q$ in its own row are $(x \pm 1, y)$, and only $(x - 1, y)$ comes before $q$. All neighbors in row $y - 1$ come before $q$: that is $(x, y - 1)$ for $c = 4$, and $(x - 1, y - 1)$, $(x, y - 1)$, $(x + 1, y - 1)$ for $c = 8$. No neighbor in row $y + 1$ comes before $q$. These are the positions listed at line L5. $\square$

Let $\mathrm{lab}_1(p)$ be the provisional label of a foreground pixel $p$ when the first pass ends; it is set once, when $p$ is scanned, and not changed in the first pass. Write $a \sim b$ when the labels $a$ and $b$ are in the same set of the forest $F$ at the end of the first pass.

**Lemma 2 (classes are connected).** For every label $a$, the set $P_a$ of foreground pixels $p$ with $\mathrm{lab}_1(p) \sim a$ is connected in $G$.

*Proof.* We show by induction over the scan that, at every moment of the first pass, each current set $T$ of $F$ has the property that the pixels scanned so far whose label is in $T$ form a connected subset of $G$, and that this subset is not empty. At the start $F$ is empty. Consider the step for a foreground pixel $q$.

If line L7 runs, a new set $\{a\}$ is made and only $q$ has label $a$, so the new set has the connected subset $\{q\}$. The other sets do not change.

If line L9 runs, $q$ takes the label $a$ of a scanned neighbor $p$. The subset of the set $T$ of $a$ gains $q$, which is adjacent to $p$, which was already in the subset, so the subset stays connected. Then line L10 unites $T$ with the sets of the other labels $b$ in $S$. Each such $b$ is the label of a scanned neighbor $p_b$ of $q$. The union of two connected subsets that contain the adjacent pixels $q$ and $p_b$ is connected, so after each union the merged set still has a connected subset. Sets not involved do not change. $\square$

**Lemma 3 (adjacent pixels are equivalent).** If $p$ and $q$ are adjacent foreground pixels, then $\mathrm{lab}_1(p) \sim \mathrm{lab}_1(q)$.

*Proof.* Say $p \prec q$. By Lemma 1, $p$ is among the scanned neighbors of $q$, and $p$ is foreground with a label already set, so $\mathrm{lab}_1(p) \in S$ when $q$ is scanned. Since $S$ is not empty, line L9 gives $q$ the first label $a$ of $S$, and line L10 calls UNION($a$, $b$) for every $b \in S$, including $b = \mathrm{lab}_1(p)$. Sets of $F$ are only ever merged, never split, so $a \sim \mathrm{lab}_1(p)$ at the end, and $\mathrm{lab}_1(q) = a$. $\square$

**Theorem.** Two foreground pixels $p$ and $q$ get the same final label if and only if they are in the same component of $G$. The final labels are $1, \ldots, K$, where $K$ is the number of components, in the raster order of the first pixel of each component, and background pixels keep the label 0.

*Proof.* If $p$ and $q$ are in the same component, there is a path $p = r_0, r_1, \ldots, r_k = q$ of adjacent foreground pixels. Lemma 3 gives $\mathrm{lab}_1(r_{i-1}) \sim \mathrm{lab}_1(r_i)$ for each $i$, and $\sim$ is an equivalence relation, so $\mathrm{lab}_1(p) \sim \mathrm{lab}_1(q)$. Conversely, if $\mathrm{lab}_1(p) \sim \mathrm{lab}_1(q)$, both pixels lie in the set $P_a$ of Lemma 2 for $a = \mathrm{lab}_1(p)$, which is connected, so they are in the same component. Hence the classes of $\sim$, restricted to the labels that occur, are in one-to-one correspondence with the components.

The forest does not change in the second pass except by path halving, which keeps every set the same, so FIND at line L12 returns the same root $r$ for two pixels exactly when their provisional labels are equivalent. Lines L13 and L14 give each root one final number, the first time a pixel of its class is met. So two pixels have the same final label exactly when they are in the same component, there are $K$ distinct final labels $1, \ldots, K$, and the components are numbered in the order in which their first pixel appears in the raster scan. Background pixels are skipped by both passes and keep 0. $\square$

**Remark (dual connectivity).** The theorem holds for either choice of $c$, but the two choices define different components. The four foreground pixels $(1, 0)$, $(0, 1)$, $(2, 1)$, $(1, 2)$ around the background pixel $(1, 1)$ of a $3 \times 3$ image form four components under $c = 4$ and one under $c = 8$. The background pixel $(1, 1)$ is cut off from the border under 4-connectivity of the background and joined to the corners under 8-connectivity. Only the pairs (8 for the foreground, 4 for the background) and (4, 8) give a closed curve that encloses a hole, or no curve and no hole.
