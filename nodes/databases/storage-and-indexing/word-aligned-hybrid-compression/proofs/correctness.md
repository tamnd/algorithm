---
title: COMPRESS is lossless and writes M - G words, and WAH-OP computes the compressed form of X op Y in O(p + q) steps
proves: [correctness]
status: full
---

We use the notation of the page: words of $w = 32$ bits, groups of 31 bits, $M = \lfloor N / 31 \rfloor$ full groups and a tail of $N - 31M$ bits. For a list of regular words $Z$, let $D(Z)$ be the sequence of groups it stands for: a literal stands for its own group, and a fill of bit $f$ and count $k$ stands for $k$ groups of 31 copies of $f$. We assume that no count reaches $2^{30} - 1$; Lemma 1 of the paper shows this for $N \le 2^{32}$. A list is *canonical* if no literal is all 0 or all 1 and no two adjacent fills have the same bit.

**Lemma 1 (the append procedures).** Let $Z$ be canonical. After APPEND-LITERAL$(Z, g)$, $D(Z)$ is the old $D(Z)$ followed by $g$, and $Z$ is canonical. After APPEND-FILL$(Z, f, k)$, $D(Z)$ is the old $D(Z)$ followed by $k$ groups of $f$, and $Z$ is canonical.

*Proof.* APPEND-FILL either adds $k$ to the count of a last fill of bit $f$ (L12), which appends $k$ groups of $f$ to $D(Z)$, or appends a new fill (L13), which does the same. In the first case no new word appears. In the second case the last word was not a fill of bit $f$, so no two adjacent fills share a bit. APPEND-LITERAL sends an all-0 or all-1 group to APPEND-FILL with $k = 1$ (L8, L9), and appends any other group as a literal (L10), which is not all 0 or all 1. In every case the claim holds. $\square$

**Claim 1 (COMPRESS is lossless and canonical).** COMPRESS returns a canonical list $Z$ with $D(Z) = (g_0, \ldots, g_{M-1})$, the full groups of $b$ in order, and an active word that holds the last $N - 31M$ bits.

*Proof.* By induction on the loop of L3 to L5 with Lemma 1: after round $i$, $D(Z) = (g_0, \ldots, g_i)$ and $Z$ is canonical. The empty list of L1 is canonical. L6 stores the tail. $\square$

**Claim 2 (Theorem 3 of the paper).** Let $G$ be the number of indices $i < M - 1$ such that $g_i$ and $g_{i+1}$ are both all-0 or both all-1. Then $|Z| = M - G$.

*Proof.* Split $g_0, \ldots, g_{M-1}$ into maximal runs of groups that are all-0, maximal runs that are all-1, and single mixed groups. By Claim 1 and canonicity, each mixed group is one literal word and each maximal run of $l$ fill groups is exactly one fill word: the run is merged by L12, and two different maximal runs of the same bit are never adjacent, because something else lies between them. A run of length $l$ contains $l - 1$ pairs counted by $G$, and no pair counted by $G$ crosses two runs. So the number of words is the sum over runs of $l - (l - 1) = 1$, plus one per literal, which is $M - G$. $\square$

**Claim 3 (size and set bits).** If the full groups contain $h$ set bits, then $|Z| \le 2h + 1$.

*Proof.* At most $h$ groups are not all-0. The all-0 groups form at most one more maximal run than there are groups that are not all-0, so at most $h + 1$ runs. Each group that is not all-0 gives at most one word, and each all-0 run gives one word. $\square$

**Claim 4 (WAH-OP is exact).** Let $X$ and $Y$ be canonical, both with $M$ groups. WAH-OP returns a canonical list $Z$ with $D(Z) = (x_0 \circ y_0, \ldots, x_{M-1} \circ y_{M-1})$, where $x_t$ and $y_t$ are the groups of $X$ and $Y$, and the active word of $X \circ Y$.

*Proof.* Let $t$ be the number of groups consumed. The invariant at L16 is: (a) $D(Z) = (x_0 \circ y_0, \ldots, x_{t-1} \circ y_{t-1})$ and $Z$ is canonical; (b) word $i$ of $X$ covers the groups $t, \ldots, t + nx - 1$ that are still unconsumed, and the value $x$ is the group $x_t$ (and equals each of these groups when word $i$ is a fill); (c) the same holds for $Y$, $j$, $ny$ and $y$.

It holds before the loop with $t = 0$ (L14, L15). In one step, $k = \min(nx, ny) \ge 1$ (L17). If both words are fills, the $k$ groups $x_t, \ldots, x_{t+k-1}$ all equal $x$, and the same holds for $y$, so the next $k$ groups of the result all equal $x \circ y$, which is all-0 or all-1. L18 appends them by Lemma 1. Otherwise one of the words is a literal, so its remaining count is 1 and $k = 1$, and L19 appends $x_t \circ y_t$ by Lemma 1. Now $t$ grows by $k$, and L20 to L22 lower both remaining counts by $k$ and move to the next word when a count reaches 0, which restores (b) and (c).

Both lists cover exactly $M$ groups, so by (b) and (c), $nx = 0$ and $ny = 0$ happen at the same $t$ when $t = M$, and $i = |X|$ and $j = |Y|$ hold together. The loop stops there with (a) for $t = M$. The tails are combined bit by bit at L23, and the mask removes any bit above the tail length. $\square$

By Claims 1 and 4, the result of WAH-OP is the same list that COMPRESS gives on the bits of $X \circ Y$: both are canonical lists for the same group sequence, and a canonical list is determined by its group sequence (its words are the maximal runs and the mixed groups, in order).

**Claim 5 (the number of steps).** If $M \ge 1$, the loop runs $s$ times with $\max(|X|, |Y|) \le s \le \min(|X| + |Y| - 1, M)$.

*Proof.* In each step, $k$ equals the remaining count of at least one of the two words, so at least one of $i$ and $j$ grows. In the last step both grow, since both lists end together. So $s \le |X| + |Y| - 1$. Each step consumes $k \ge 1$ groups and there are $M$, so $s \le M$. Each step moves $i$ and $j$ by at most one each, and $i$ must reach $|X|$ and $j$ must reach $|Y|$, so $s \ge \max(|X|, |Y|)$. $\square$

Each step does a constant number of word operations, including the work of Lemma 1, so WAH-OP takes $O(|X| + |Y|)$ time and writes at most $|X| + |Y| - 1$ regular words. This is Theorem 7 of the paper.

The tests check Claims 1 to 5 on random bitmaps of three shapes and several lengths, the example of Fig. 2 of the paper, and the split of a fill at the largest count.
