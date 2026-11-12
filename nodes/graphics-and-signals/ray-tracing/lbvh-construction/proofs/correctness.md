---
title: The Karras hierarchy is the binary radix tree of the sorted keys, and the LBVH boxes are correct
proves: [correctness]
status: full
---

Let $k_0 < k_1 < \cdots < k_{n-1}$ be the sorted distinct keys of $w$ bits, $n \ge 2$. For $0 \le a, b < n$ let $\delta(a, b)$ be the length of the common prefix of $k_a$ and $k_b$, and $\delta(a, b) = -1$ if $b$ is out of range. Let $D_c = \delta(c, c + 1)$ for $0 \le c \le n - 2$, and $D_{-1} = D_{n-1} = -1$.

**Lemma 1.** For $a < b$, $\delta(a, b) = \min_{a \le c < b} D_c$.

*Proof.* Let $p = \delta(a, b)$. Since the keys are sorted, every key between $k_a$ and $k_b$ has the same first $p$ bits, so $D_c \ge p$ for $a \le c < b$. Bit $p$ (counted from the top) is 0 in $k_a$ and 1 in $k_b$, so it changes from 0 to 1 at some $c$, and there $D_c = p$. $\square$

**Lemma 2.** In each range $[f, l]$ with $f < l$, the bit at position $\delta(f, l)$ changes exactly once, so exactly one $m \in [f, l - 1]$ has $D_m = \delta(f, l)$, and all other $D_c$ in the range are larger.

*Proof.* All keys of the range share the first $\delta(f, l)$ bits and are sorted, so the next bit goes from 0 to 1 once and never back. A position with $D_c = \delta(f, l)$ is exactly a position where that bit changes. $\square$

The *binary radix tree* splits $[0, n - 1]$, and then each range $[f, l]$ with $f < l$, at this $m$ into $[f, m]$ and $[m + 1, l]$. Call its ranges with $f < l$ the *internal ranges*. There are $n - 1$ of them.

**Lemma 3 (the internal ranges).** $[f, l]$ with $f < l$ is an internal range if and only if $D_c > \max(D_{f-1}, D_l)$ for all $c \in [f, l - 1]$.

*Proof.* ($\Rightarrow$) By induction from the root, for which $D_{-1} = D_{n-1} = -1$. If $[F, L]$ has the property and splits at $m$, then $D_m$ is the least value inside, by Lemma 2, so the children $[F, m]$ and $[m + 1, L]$ have the property, with the new end values $D_m$ and the old ones $D_{F-1}$, $D_L$. ($\Leftarrow$) Let $[f, l]$ have the property, and let $[F, L]$ be the least internal range that contains it. If $[F, L] \ne [f, l]$, then $D_{f-1}$ or $D_l$ is a value of $[F, L]$, and the least value $D_m$ of $[F, L]$ is at most that value, so $m \notin [f, l - 1]$ and a child of $[F, L]$ contains $[f, l]$, which contradicts the choice. $\square$

**Lemma 4 (what node $i$ computes).** For $0 \le i \le n - 2$, line L5 sets $d = +1$ if $D_i > D_{i-1}$ and $d = -1$ otherwise, and $D_i \ne D_{i-1}$. Lines L6 to L8 set $j$ to the farthest index in direction $d$ with $\delta(i, j) > \delta_{min} = \delta(i, i - d)$. Lines L9 and L10 set $\gamma$ to the unique $m$ of Lemma 2 for the range $R_i$ between $i$ and $j$.

*Proof.* $\delta(i, i + 1) = D_i$ and $\delta(i, i - 1) = D_{i-1}$. If they were equal, three keys in a row would share that prefix and the next bit would change twice, against Lemma 2; for $i = 0$, $D_{-1} = -1 < D_0$. By Lemma 1, $\delta(i, i + x d)$ does not increase with $x$, so the test "$\delta(i, i + x d) > \delta_{min}$" holds for $x = 1$ (since $D_i \ne D_{i-1}$ and $d$ points to the larger one) and is true exactly for $x \le l^*$ for some $l^* \ge 1$. Line L6 doubles $l_{max}$ until the test fails, which happens since an index out of range gives $-1 \le \delta_{min}$. Line L7 sets the bits of $l$ from $l_{max}/2$ down to 1, keeping each bit when the test holds; since the test is monotone and $l^* < l_{max}$, the result is $l = l^*$. For line L9, the test "$\delta(i, i + x d) > \delta_{node}$" holds exactly for $x \le s^*$, where the unique $m$ of $R_i$ is $i + s^* d + \min(d, 0)$, by Lemmas 1 and 2. The loop keeps the invariant $s \le s^* < s + t$ with $t$ the last step: it holds at the start with $t = l$, and after a step of $t' = \lceil t/2 \rceil$, either $s$ grows by $t'$ and $s^* < s + (t - t') \le s + t'$, or $s^* < s + t'$. At $t' = 1$, $s = s^*$, so line L10 gives $\gamma = m$. $\square$

**Lemma 5 (a bijection).** $R_i$ is an internal range, and $i \mapsto R_i$ is a bijection from $\{0, \ldots, n - 2\}$ to the internal ranges. $R_0 = [0, n - 1]$.

*Proof.* Take $d = +1$, so $R_i = [i, j]$; the case $d = -1$ is the mirror image. All $D_c$ inside are $> D_{i-1}$ by the choice of $j$, and $D_j \le D_{i-1}$ by its maximality, so $D_c > \max(D_{i-1}, D_j)$ and Lemma 3 applies. For $i = 0$, $\delta_{min} = -1$ and $j = n - 1$. If $R_i = R_{i'}$ with $i < i'$, then $i$ is its left end with $D_j = D_{i'} \le D_{i-1}$, and $i'$ is its right end with $D_{i-1} \le D_{i'}$, so $D_{i-1} = D_{i'}$ while all values between are larger. With $i \ge 1$, that would make the bit at that position change twice, against Lemma 2; with $i = 0$, $D_{i'} = -1$ needs $i' = n - 1$, which is not a node index. So the map is injective, and both sets have $n - 1$ elements. $\square$

**Theorem.** The arrays left and right of line L11 form the binary radix tree with root 0: for each internal node $i$ with range $[lo, hi]$ and split $\gamma$, the left child is leaf $\gamma$ if $lo = \gamma$ and otherwise the internal node whose range is $[lo, \gamma]$, which is $\gamma$; and the right child is leaf $\gamma + 1$ if $hi = \gamma + 1$, and otherwise node $\gamma + 1$ with range $[\gamma + 1, hi]$. After line L12, the box of each internal node is the union of the boxes of the leaves in its range.

*Proof.* If $\gamma > lo$, the range $[lo, \gamma]$ is internal and equals $R_x$ for one $x \in \{lo, \gamma\}$, by Lemma 5. If $x = lo$, then $lo$ has $d = +1$ and $D_\gamma \le D_{lo - 1}$. But $D_{lo-1}$ is less than every value inside $[lo, hi]$, by Lemma 3, and $D_\gamma$ is one of them, a contradiction. So $x = \gamma$. The right child is the mirror case: $hi$ would need $D_\gamma \le D_{hi}$, while $D_{hi}$ is less than all values inside. The leaves are the ranges $[c, c]$, so each key is a leaf once.

For the boxes, each internal node has two children, and line L12 walks up from every leaf. By induction on the height, the walk from the last finished child of a node arrives when the other child already has its box, so the node is visited exactly twice, the second visit finds both child boxes and sets the union, and the walk continues to the parent. The root is reached by the last walk. $\blacksquare$

**Remark.** The augmented keys $\mathrm{code} \cdot 2^b + p$ with $2^b \ge n$ are distinct and sort first by the Morton code, so equal codes do not break the theorem. Leaves with equal codes then form a subtree split on the bits of $p$, with boxes that can overlap fully. Containment and the cover of each primitive by exactly one leaf are what [BVH traversal](/bvh-traversal/) needs.
