---
title: S2 cell ids name the cells of the hierarchy, PARENT, CHILDREN and CONTAINS follow the hierarchy, and FROM-POINT returns the leaf that contains the point
proves: [correctness, termination]
status: full
---

Let $L = 30$. A *cell of level $k$* on face $f$ is a pair of blocks $I \times J$ of leaf coordinates, $I = [a 2^{L-k}, (a+1) 2^{L-k})$ and $J = [b 2^{L-k}, (b+1) 2^{L-k})$, with $0 \le a, b < 2^k$. Its children are the four cells of level $k + 1$ inside it. We treat the face projection and the quadratic map as given functions from points to $(f, i, j)$: they are computed by closed formulas, so they stop, and we prove the claims about ids.

**Orientations.** An orientation is $o \in \{0, 1, 2, 3\}$, with bit 1 for swap and bit 2 for invert. The table IJ-TO-POS$[o]$ maps the four bit pairs $(i_b, j_b)$ to positions 0 to 3. For each $o$ the row is a permutation of $\{0, 1, 2, 3\}$, as the four rows $(0, 1, 3, 2)$, $(0, 3, 1, 2)$, $(2, 3, 1, 0)$ and $(2, 1, 3, 0)$ show, and POS-TO-IJ$[o]$ is its inverse.

**Lemma 1 (the encoding names one cell per level).** Let FROM-POINT reach $(f, i, j)$, and let $q_1, \ldots, q_L$ be the positions computed at line L6, in order. For each $k$, the first $k$ positions and $f$ are determined by the cell of level $k$ that contains $(i, j)$, and distinct cells of level $k$ on face $f$ give distinct sequences $q_1, \ldots, q_k$.

*Proof.* By induction on $k$. The orientation $o_1$ before the first step is $f \bmod 2$, fixed by $f$. Suppose the orientation $o_k$ before step $k$ is a function of the cell $C_{k-1}$ of level $k - 1$ that contains $(i, j)$. The bits at step $k$ (bit $L - k$ of $i$ and of $j$) say which of the four children of $C_{k-1}$ contains $(i, j)$, so $q_k = \text{IJ-TO-POS}[o_k][\cdot]$ is a function of $C_k$, and $o_{k+1} = o_k \oplus \text{POS-TO-ORIENTATION}[q_k]$ is a function of $C_k$ too. For distinctness: two cells of level $k$ on face $f$ with the same $q_1, \ldots, q_{k}$ have, by induction, the same parent cell and so the same $o_k$, and since row $o_k$ of the table is a permutation, the same $q_k$ means the same bit pair, so the same child. $\square$

So the map from cells of level $k$ to the numbers $f \cdot 2^{2k} + \sum_l q_l 4^{k-l}$ is injective, and since both sets have $6 \cdot 4^k$ elements, it is a bijection.

**Definition.** The id of a cell $C$ of level $k$ with face $f$ and positions $q_1, \ldots, q_k$ is $\text{id}(C) = f 2^{61} + \sum_{l=1}^{k} q_l 2^{61 - 2l} + 2^{60 - 2k}$. Its lowest set bit is $2^{60 - 2k}$, since the sum has no bits below $2^{61 - 2k}$; so the level is recovered from the id as $(60 - z)/2$, where $z$ is the number of trailing zeros.

**Lemma 2 (FROM-POINT).** Line L8 returns the id of the leaf cell $\{i\} \times \{j\}$.

*Proof.* After the loop, $\text{pos} = \sum_{l=1}^{L} q_l 4^{L-l}$, so $f 2^{61} + 2\,\text{pos} + 1 = f 2^{61} + \sum_l q_l 2^{61 - 2l} + 2^{0}$, which is the definition for $k = L$. The loop runs $L$ times, so it stops. $\square$

**Lemma 3 (ranges).** For a cell $C$ of level $k$, the ids of the leaf cells inside $C$ are exactly the odd numbers in $[\text{id}(C) - 2^{60-2k} + 1, \ \text{id}(C) + 2^{60-2k} - 1]$.

*Proof.* A leaf inside $C$ has the face and the first $k$ positions of $C$, by Lemma 1, since its ancestor of level $k$ is $C$, and any positions $q_{k+1}, \ldots, q_L$; and every such sequence gives a leaf inside $C$, by the bijection. Let $P = f 2^{61} + \sum_{l \le k} q_l 2^{61 - 2l}$. The leaf ids are $P + R + 1$, where $R = \sum_{l > k} q_l 2^{61 - 2l}$ runs over all even numbers from 0 to $2^{61 - 2k} - 2$. So they are the odd numbers from $P + 1$ to $P + 2^{61 - 2k} - 1$. Since $\text{id}(C) = P + 2^{60 - 2k}$, these are the odd numbers from $\text{id}(C) - 2^{60-2k} + 1$ to $\text{id}(C) + 2^{60-2k} - 1$. $\square$

**Theorem.** (a) PARENT$(\text{id}(C), k')$ for $k' \le k$ returns the id of the ancestor of $C$ at level $k'$. (b) CHILDREN$(\text{id}(C))$ for $k < L$ returns the ids of the four children of $C$, in the order of their positions. (c) For cells $A$ and $B$, CONTAINS$(\text{id}(A), \text{id}(B))$ is true if and only if $B \subseteq A$. All three stop after a constant number of word operations.

*Proof.* (a) Line L9 sets $b = 2^{60 - 2k'}$. Clearing the bits of $\text{id}(C)$ below $b$ removes the terms $q_l 2^{61 - 2l}$ with $61 - 2l < 60 - 2k'$, that is $l > k'$, and the marker bit of $C$, which is below $b$ when $k' < k$; when $k' = k$, it removes the marker bit only. What is left is $f 2^{61} + \sum_{l \le k'} q_l 2^{61 - 2l}$, and line L10 adds $b$, which gives the id of the ancestor of level $k'$, whose positions are $q_1, \ldots, q_{k'}$ by Lemma 1.

(b) With $b = 2^{60 - 2k}$ the lowest set bit and $c = b/4 = 2^{60 - 2(k+1)}$, line L12 gives $\text{id}(C) - b + c + 2cq = f 2^{61} + \sum_{l \le k} q_l 2^{61 - 2l} + q\,2^{61 - 2(k+1)} + 2^{60 - 2(k+1)}$, the id of the child at position $q$. By the bijection, the four values of $q$ give the four children.

(c) If $B \subseteq A$, every leaf of $B$ is a leaf of $A$; by Lemma 3 applied to $B$, $\text{id}(B)$ lies in the center of the range of the leaves of $B$, which is inside the range of the leaves of $A$, so $\text{range\_min}(A) \le \text{id}(B) \le \text{range\_max}(A)$, with $\text{range\_min}(A) = \text{id}(A) - (\text{lsb}(A) - 1)$ and $\text{range\_max}(A) = \text{id}(A) + (\text{lsb}(A) - 1)$, which is the range of Lemma 3. Conversely, suppose $\text{id}(B)$ is in the range of $A$. If $B$ is a leaf, $\text{id}(B)$ is odd and, by Lemma 3, a leaf of $A$, so $B \subseteq A$. If $B$ is not a leaf, take the leaf $\lambda$ of $B$ with the first $k_B$ positions of $B$, then position 2 and then all positions 0; its id is $\text{id}(B) + 1$. Since $\text{id}(B)$ is even and $\text{range\_max}(A)$ is odd, $\text{id}(B) + 1 \le \text{range\_max}(A)$, so $\lambda$ is a leaf of $A$. The cells of the hierarchy are nested or disjoint, and $A$ and $B$ share the leaf $\lambda$, so one contains the other. If $A \subsetneq B$, then $\text{lsb}(A) < \text{lsb}(B)$, and the range of $A$ is a proper part of the range of $B$ that does not contain its center $\text{id}(B)$: by Lemma 3, the range of $A$ is the block of leaves of $A$, which lies entirely in the lower half or the upper half of the block of $B$, since the four children of $B$ split its block into four quarters around its center, and $A$ lies inside one child. This contradicts $\text{id}(B)$ in the range of $A$. So $B \subseteq A$.

Each of the three functions does a fixed number of additions, subtractions, ANDs and shifts, so it stops. $\blacksquare$
