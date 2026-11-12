---
title: What BLAST reports, and when it finds a segment pair
proves: [correctness]
status: full
---

BLAST is a heuristic, so we prove what holds: the neighborhood is exact, the reported scores are true, the extension is optimal when $X = \infty$, the drop-off loses nothing under a stated condition, and in one-hit mode with no drop-off and no skip, every segment pair of score at least $S$ that contains a hit is matched. Line numbers refer to the pseudocode on the page.

**Notation.** The score of the word pair at $(i, j)$ is $W(i, j) = \sum_{k=0}^{w-1} s(q[i+k], y[j+k])$. A segment pair $(i, j, L)$ has the score $\sigma(i, j, L) = \sum_{k=0}^{L-1} s(q[i+k], y[j+k])$. On a fixed diagonal, the pair at $(i + k, j + k)$ is at offset $k$.

**Lemma 1 (the neighborhood is exact).** For each query position $i$, line L1 lists $i$ under the word $u$ if and only if $\sum_{k=0}^{w-1} s(q[i+k], u_k) \ge T$.

*Proof.* Let $b_k = \max_c s(q[i+k], c)$ and $r_k = \sum_{t \ge k} b_t$, the best score that positions $k, \ldots, w-1$ can add. The construction extends a prefix $u_0 \cdots u_{k-1}$ with score $p$ by a letter $c$ only if $p + s(q[i+k], c) + r_{k+1} \ge T$, and lists every word of length $w$ that it reaches. If a full word $u$ scores at least $T$, then for each $k$ its prefix of length $k+1$ has score $p_{k+1}$ with $p_{k+1} + r_{k+1} \ge p_{k+1} + \sum_{t > k} s(q[i+t], u_t) \ge T$, so no prefix of $u$ is cut, and $u$ is listed. If $u$ is listed, it was reached at length $w$ with $p_w + r_w = p_w \ge T$, since $r_w = 0$. $\square$

So a hit at $(i, j)$ in line L4 is exactly a word pair with $W(i, j) \ge T$.

**Lemma 2 (scores are true).** EXTEND$(q, y, i, j, X)$ returns a segment pair $(i - \ell, j - \ell, \ell + w + r, v)$ with $v = \sigma(i - \ell, j - \ell, \ell + w + r)$. Each segment pair that line L9 reports has score at least $S$.

*Proof.* EXTEND adds $W(i, j)$, the running total of the right walk at the chosen right length $r$, and the running total of the left walk at the chosen left length $\ell$. These three sums cover the pairs at offsets $-\ell, \ldots, w + r - 1$ of the diagonal, each one time, so their sum is $\sigma$ of the returned segment pair. Line L9 reports only when this value is at least $S$. $\square$

**Lemma 3 (extension with $X = \infty$).** With $X = \infty$, EXTEND returns a segment pair of the highest score among the segment pairs on diagonal $j - i$ that contain the word pair at $(i, j)$.

*Proof.* A segment pair on the diagonal that contains the word pair is fixed by its left length $\ell' \ge 0$ and right length $r' \ge 0$, within the ends of $q$ and $y$. Its score is $R(r') + W(i, j) + G(\ell')$, where $R(r')$ is the sum of the $r'$ pairs to the right of the word and $G(\ell')$ the sum of the $\ell'$ pairs to the left. The two parts are independent, so the maximum is $\max_{r'} R(r') + W(i, j) + \max_{\ell'} G(\ell')$. With $X = \infty$ the right walk never stops before the end of a sequence, it starts with $R(0) = 0$ as its best, and it records each strictly larger running total, so it returns $\max_{r'} R(r')$, at the smallest $r'$ that reaches it. The left walk does the same for $G$. By Lemma 2 the returned score is this maximum. $\square$

**Lemma 4 (the drop-off).** Let $r^*$ be the smallest right length with $R(r^*) = \max_{r'} R(r')$. If for every $t < r^*$ the running total satisfies $R(t) \ge \max_{u \le t} R(u) - X$, then the right walk with drop-off $X$ returns the same right length $r^*$ as with $X = \infty$. The same holds on the left.

*Proof.* The walk with drop-off $X$ stops after step $t$ only if $R(t) < \max_{u \le t} R(u) - X$. By the condition this does not happen for $t < r^*$, so the walk reaches step $r^*$ and records $R(r^*)$ as its best. No later total is strictly larger, so the recorded best is not replaced, whether the walk stops later or not. $\square$

When the condition fails, the walk can stop in a dip before $r^*$ and return a shorter segment pair with a lower score. This is the loss that $X$ trades for speed.

**Theorem (completeness in one-hit mode).** Run BLAST in one-hit mode with $X = \infty$ and without the skip of line L6. Let $(i, j, L)$ be a segment pair of score $\sigma \ge S$ that contains a hit, that is, an offset $k$ with $0 \le k \le L - w$ and $W(i + k, j + k) \ge T$. Then BLAST reports a segment pair on diagonal $j - i$ that contains the word pair at $(i + k, j + k)$ and has score at least $\sigma$.

*Proof.* By Lemma 1, $i + k$ is listed under the word $y[j + k \ldots j + k + w - 1]$, so when line L3 reaches $j + k$, line L4 yields $i + k$. Without the skip and the two-hit rule, line L8 extends this hit. The segment pair $(i, j, L)$ lies on the same diagonal and contains the word pair, so by Lemma 3 the extension returns a segment pair that contains the word pair, with score at least $\sigma \ge S$. Line L9 reports it. $\blacksquare$

**Corollary (the MSP).** With $w = 1$ and $T \le \min_{a,b} s(a, b)$, every letter pair is a hit. If the maximal segment pair has score $\sigma^* \ge S$, the theorem applies to it, and by Lemma 2 no reported score exceeds $\sigma^*$. So the best reported score equals $\sigma^*$.

**What each shortcut can lose.**

- *A segment pair with no hit.* The theorem needs a word pair of score at least $T$ inside the segment pair. Without one, line L4 never yields a position on it. The page shows a DNA pair with ungapped score 42 and no shared 11-mer.
- *The skip of line L6.* A later hit inside a covered region is not extended. With a finite $X$ the earlier extension may have stopped short of a better end, and even with $X = \infty$ the best segment pair through the later hit can start after a deep dip that the earlier one included, and then has a higher score. Both are then lost.
- *The two-hit rule.* A segment pair whose only hit is isolated on its diagonal, with no other non-overlapping hit at most $A$ before it, is not extended.
- *A finite $X$.* Lemma 4 gives the condition under which nothing is lost. Its failure loses score.

**Termination.** Line L1 explores a finite tree of prefixes of length at most $w$. The loops of lines L2 to L4 are over finite sets, and each walk of EXTEND moves one step at a time toward the end of a sequence. So BLAST stops on every input.
