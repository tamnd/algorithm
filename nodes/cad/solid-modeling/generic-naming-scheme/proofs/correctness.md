---
title: Generic names resolve to the images of an entity under every label-preserving isomorphism, and naming terminates
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. A model $M$ is a finite set of cycles. Cycle $C$ has a length $L_C \ge 1$ and a sequence of labels $C[0], \dots, C[L_C - 1]$, with indices taken modulo $L_C$. An edge is a pair $(C, i)$, and its successor is $\mathrm{next}(C, i) = (C, i + 1)$. A vertex is a pair $(a, \mathrm{next}(a))$ of an edge and its successor.

The window of radius $r$ of $e = (C, i)$ is
$$\mathrm{window}_r(e) = \bigl(\lambda_r(L_C),\ (C[i - r], C[i - r + 1], \dots, C[i + r])\bigr),$$
where $\lambda_r(L) = L$ if $2r + 1 > L$ and $\lambda_r(L) = 0$ otherwise. Let $T(M)$ be the largest cycle length of $M$.

An *isomorphism* $\sigma : M \to M'$ is a bijection $\pi$ from the cycles of $M$ onto those of $M'$, together with a shift $s_C$ for each cycle $C$ of $M$, such that $L_{\pi(C)} = L_C$ and $\pi(C)[i + s_C] = C[i]$ for all $i$. It acts on edges by $\sigma(C, i) = (\pi(C), i + s_C)$ and on vertices by $\sigma(a, b) = (\sigma(a), \sigma(b))$. An isomorphism from $M$ to itself is an *automorphism*. Isomorphisms compose, and their inverses are isomorphisms.

**Lemma 1 (windows are invariant).** For every isomorphism $\sigma$, every edge $e$ and every $r \ge 0$, $\mathrm{window}_r(\sigma(e)) = \mathrm{window}_r(e)$. Also $\sigma(\mathrm{next}(e)) = \mathrm{next}(\sigma(e))$.

*Proof.* Let $e = (C, i)$. Then $\sigma(e) = (\pi(C), i + s_C)$, and $L_{\pi(C)} = L_C$, so the first components agree. For $-r \le d \le r$, the label at offset $d$ is $\pi(C)[i + s_C + d] = C[i + d]$. The second claim is $(\pi(C), i + 1 + s_C) = \mathrm{next}(\pi(C), i + s_C)$. $\square$

**Lemma 2 (the top window determines the orbit).** Let $R \ge T(M)$, and let $e$ and $f$ be edges of $M$. Then $\mathrm{window}_R(e) = \mathrm{window}_R(f)$ if and only if $\alpha(e) = f$ for some automorphism $\alpha$ of $M$.

*Proof.* If $\alpha(e) = f$, the windows are equal by Lemma 1. Conversely, let $e = (C, i)$ and $f = (D, j)$ have equal windows. Since $2R + 1 > R \ge L_C$, the first component of $\mathrm{window}_R(e)$ is $L_C$, and likewise for $f$, so $L_C = L_D = L$. The offsets $0, 1, \dots, L - 1$ all lie in $[-R, R]$, so $C[i + d] = D[j + d]$ for $0 \le d < L$, and so for all $d$ by periodicity. Define $\alpha$ as follows. If $C = D$, it shifts $C$ by $j - i$ and fixes the other cycles. If $C \ne D$, it maps $C$ to $D$ with shift $j - i$, maps $D$ to $C$ with shift $i - j$, and fixes the other cycles. In both cases each shifted cycle keeps its labels, by the identity $C[i + d] = D[j + d]$. So $\alpha$ is an automorphism with $\alpha(e) = f$. $\square$

**Lemma 3 (levels).** Line L4 gives each edge $e$ of $M$ a level $\ell(e) \le T(M)$. Either $\mathrm{window}_{\ell(e)}(e)$ occurs exactly once among the edges of $M$, or $\ell(e) = T(M)$.

*Proof.* The loop of lines L1 to L4 runs $r = 0, 1, \dots$ while some edge is pending and $r \le T(M)$. At $r = T(M)$, line L4 assigns a level to every pending edge. So every edge gets a level, the loop stops after at most $T(M) + 1$ rounds, and the level is the first $r$ at which the window was unique or the top was reached. $\square$

**Theorem 1 (edge names resolve to the images).** Let $\sigma_0 : M \to M'$ be an isomorphism, and let $e$ be an edge of $M$ with name $(r, w)$, where $r = \ell(e)$ and $w = \mathrm{window}_r(e)$. Then line L6 returns
$$\mathrm{RESOLVE}((r, w), M') = \{\sigma(e) : \sigma \text{ an isomorphism from } M \text{ to } M'\}.$$
If $w$ occurs once in $M$, this set is the single edge $\sigma_0(e)$.

*Proof.* Let $E_w = \{f \in M : \mathrm{window}_r(f) = w\}$. By Lemma 1, applied to $\sigma_0$ and to $\sigma_0^{-1}$, the edges of $M'$ with window $w$ at radius $r$ are exactly $\sigma_0(E_w)$. So line L6 returns $\sigma_0(E_w)$.

Every isomorphism $\sigma : M \to M'$ has the form $\sigma_0 \circ \alpha$ with $\alpha = \sigma_0^{-1} \circ \sigma$ an automorphism of $M$, and every such composition is an isomorphism. So the right side is $\sigma_0(O_e)$, where $O_e = \{\alpha(e) : \alpha \text{ an automorphism of } M\}$. It remains to show $E_w = O_e$. By Lemma 3 there are two cases.

*The window is unique.* Then $E_w = \{e\}$. By Lemma 1 every automorphism keeps the window of $e$, so it maps $e$ into $E_w$, and $O_e = \{e\}$.

*The level is the top.* Then $r = T(M)$, and Lemma 2 gives $E_w = O_e$ directly.

In both cases line L6 returns $\sigma_0(O_e)$, which is the set of images. In the unique case it is $\{\sigma_0(e)\}$. $\square$

**Corollary 1 (vertices).** Under the same hypothesis, let $v = (a, b)$ be a vertex of $M$, so $b = \mathrm{next}(a)$. Then line L8 returns $\{\sigma(v) : \sigma \text{ an isomorphism from } M \text{ to } M'\}$.

*Proof.* By Theorem 1, the two resolved sets are $A = \{\sigma(a)\}$ and $B = \{\sigma(b)\}$, each over all isomorphisms $\sigma$. Line L8 returns the vertices $(x, \mathrm{next}(x))$ of $M'$ with $x \in A$ and $\mathrm{next}(x) \in B$. For any $\sigma$, the vertex $\sigma(v) = (\sigma(a), \sigma(b))$ equals $(\sigma(a), \mathrm{next}(\sigma(a)))$ by Lemma 1, and its two edges lie in $A$ and $B$. Conversely, if $x = \sigma(a) \in A$, then $\mathrm{next}(x) = \sigma(b)$ by Lemma 1, so the returned vertex is $\sigma(v)$. $\square$

**Corollary 2 (order-preserving edits).** Let $M'$ be built from the same history as $M$ by a change of coordinates that keeps the strict order of all $x$ values and of all $y$ values. Then the identity on grid positions is an isomorphism. So each edge name resolves to a set that contains the edge at the same grid position, and to that edge alone when the name was unique in $M$.

*Proof.* The construction depends on the coordinates only through comparisons. The owner of each value is fixed by the history, and the sorted lists $xs$ and $ys$ list the same owners in the same order. A grid cell $(i, j)$ is inside when its doubled centre $xs[i] + xs[i + 1]$ lies strictly between $2a$ and $2c$ for the base, and not for any cut $(a, b, c, d)$, and likewise in $y$. For a grid value $a$, the test $2a < xs[i] + xs[i + 1]$ holds exactly when $a \le xs[i]$, since $a$ is not strictly between consecutive grid values. So it is a comparison of ranks, and the same holds for the other three tests. The set of inside cells is therefore the same in index space. The directed unit segments, their labels and the tracing by turn rank use only indices, so they produce the same cycles in the same order. The identity on $(C, i)$ is then an isomorphism, and Theorem 1 applies with $\sigma_0$ the identity. $\square$

**Termination.** Lemma 3 bounds the naming loop by $T(M) + 1$ rounds of $O(n)$ windows each. Tracing a cycle marks each directed unit segment as used once, and the walk stops when it returns to a used segment. Each walk starts at an unused segment, so the number of steps is the number of segments. The merge loop advances $k$ while consecutive keys agree. That loop stops, because a boundary cycle of an axis-parallel region turns at least four times, so not all keys are equal. Resolution scans the edges or vertices once. $\square$

**What is not claimed.** If no isomorphism from $M$ to $M'$ exists, the topology has changed, and the theorems say nothing. A name may then resolve to nothing, to one edge or to several, and whether that edge is "the same" is a question of the designer's intent. The proof is also about labelled cycles only. Two models with isomorphic labelled boundaries but different shapes are treated as the same, which is the generative view the scheme takes.
