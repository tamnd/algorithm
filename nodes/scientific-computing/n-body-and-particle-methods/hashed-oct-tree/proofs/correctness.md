---
title: Keys name cells one to one, and each stored cell holds exactly the bodies of its cube
proves: [correctness]
status: full
---

Fix the depth $L$ and the root cube $R = \mathbf{lo} + [0, S)^3$. A cell at level $l$, $0 \le l \le L$, is the cube $\mathbf{lo} + S 2^{-l} \left([i, i+1) \times [j, j+1) \times [k, k+1)\right)$ with integers $0 \le i, j, k < 2^l$. Write $i = (i_{l-1} \ldots i_0)_2$ and the same for $j$ and $k$. The key of the cell is the integer with binary digits $1\, k_{l-1} j_{l-1} i_{l-1}\, \ldots\, k_0 j_0 i_0$, as in lines L2 to L4.

**Lemma 1 (keys are one to one).** The map from $(l, i, j, k)$ to the key is one to one, and its inverse is computed from the key alone.

*Proof.* The key has $3l + 1$ bits, with a leading $1$, so $l = (\text{bit length} - 1)/3$. The remaining $3l$ bits are the digits $k_b j_b i_b$ in a fixed order, so they give $i$, $j$ and $k$. $\square$

**Lemma 2 (parent and children).** The parent of the cell $(l, i, j, k)$, the cell of level $l - 1$ whose cube contains it, has the key $\text{key} \gg 3$. The eight children have the keys $8\,\text{key} + c$, $c = 0, \ldots, 7$.

*Proof.* The parent cube has the coordinates $(\lfloor i/2 \rfloor, \lfloor j/2 \rfloor, \lfloor k/2 \rfloor)$, whose binary digits are those of $i$, $j$, $k$ without the last one. Removing the last digit of each removes the last three bits of the key. The children are the cells whose parent is the given cell, and by Lemma 1 and the first part these are the keys $8\,\text{key} + c$. $\square$

**Lemma 3 (prefixes).** Let $\mathbf{p} \in R$ and let $K$ be its key at level $L$ (line L1 and lines L2 to L4). For each $l \le L$, the key of the cell of level $l$ whose cube contains $\mathbf{p}$ is $K \gg 3(L - l)$.

*Proof.* Line L1 sets $q_d = \lfloor 2^L (p_d - lo_d) / S \rfloor$. The cell of level $l$ that contains $\mathbf{p}$ has coordinates $\lfloor q_d / 2^{L-l} \rfloor$, the integers $q_d$ without their last $L - l$ digits. Applying Lemma 2 $L - l$ times gives the claim. $\square$

**Lemma 4 (cells are intervals).** After line L5 the keys $K_1 \le K_2 \le \ldots \le K_N$ of the bodies are sorted. For each cell $Q$ of level $l$, the bodies in the cube of $Q$ are those with $K_n \gg 3(L - l) = \text{key}(Q)$, and they form one contiguous range of positions.

*Proof.* The first statement is Lemma 3. All keys of level $L$ have the same bit length, so $K \gg 3(L - l)$ is a nondecreasing function of $K$, and the set of positions where it equals a given value is an interval. $\square$

**Theorem (the table).** After the build, the table holds the keys of exactly the cells that the octree with leaves of at most $B$ bodies (the `leaf_size`) has, except that splitting stops at level $L$. Each key maps to the range of the sorted bodies that lie in its cube.

*Proof.* Invariant of the stack of line L6: each entry $(\text{key}, a, b)$ names a nonempty cell $Q$, and positions $a$ to $b - 1$ are the bodies of $Q$. It holds for the root, which holds all bodies. Line L7 stores the entry. If line L8 splits $Q$ (more than $B$ bodies and level below $L$), it groups the positions $a$ to $b - 1$ by the digit $c = (K \gg 3(L - l - 1)) \,\&\, 7$. By Lemma 4 applied at level $l + 1$, each group is contiguous, and by Lemma 3 it is the set of bodies of the child with key $8\,\text{key} + c$. So the pushed entries satisfy the invariant, and only nonempty children are pushed. A cell is stored exactly when its parent was split, which is the rule of the octree. $\square$

**Consequences.** A lookup of a key is one hash table access (line L9). The parent and the child keys are computed with shifts (line L10), with no pointers. The deepest stored cell that contains a point is found by testing the prefixes of the point's key from the root down, one hash access each.

**Cost.** Line L5 sorts $N$ keys of $3L + 1$ bits; on the word RAM with $3L + 1$ at most the word size, this costs $O(N \log N)$ by comparison sorting, or $O(N L)$ by a radix sort on the octal digits. Each body lies in at most $L + 1$ stored cells, and the scans of line L8 touch each body once per level, so the build costs $O(N L)$ after sorting. The table holds at most $N (L + 1)$ keys. For well-spread bodies most cells have several nonempty children, and the number of keys is $O(N)$. With a hash table that has $O(1)$ expected time per access, a lookup costs $O(1)$ expected time. $\square$
