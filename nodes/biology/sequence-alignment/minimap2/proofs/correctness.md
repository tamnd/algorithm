---
title: What minimap2's seeding and chaining guarantee
proves: [correctness]
status: full
---

Minimap2 is a heuristic, so there is no theorem that it finds the best alignment. This file proves the guarantees of its parts: the sketch is the set of window minimizers, a shared piece of $w + k - 1$ bases yields an anchor, the exact chaining computes the chaining recurrence, and the limited chaining never overstates a score.

Write $h_0, h_1, \ldots, h_{L-1}$ for the hashes of the canonical k-mers of a sequence, in order of position, skipping the k-mers with a letter outside $\{A, C, G, T\}$ and those equal to their own reverse complement. Window $i$ is the list $h_i, \ldots, h_{i+w-1}$, and its minimizer is the index $\mu(i) = \arg\min_{i \le p < i + w} (h_p, p)$.

**Lemma 1 (sliding-window minimum).** The procedure `sketch` returns the entries $\mu(0), \mu(1), \ldots, \mu(L - w)$, each distinct index once, in increasing order.

*Proof.* The procedure keeps a list $D[\mathit{head} \ldots]$ of indices. Invariant, after step $i$ (for $i \ge 0$): the indices in $D[\mathit{head} \ldots]$ are increasing, lie in $[i - w + 1, i]$, have non-decreasing hashes, and include, for each $p$ in $[i - w + 1, i]$, the index $\mu$ of the suffix $[p, i]$, that is, the leftmost index of minimal hash among $p, \ldots, i$. Step $i$ removes from the back the indices with a hash larger than $h_i$. Such an index $q$ can never again be the leftmost minimum of a range that contains $i$, since $h_i < h_q$; and a range that does not contain $i$ ends before $i$ and is no longer needed. Indices with a hash equal to $h_i$ stay, so the leftmost of equal values is kept. Then $i$ is appended, and if the head is $i - w$ it is removed; at most one index leaves the window per step. So the invariant holds, and the head is the leftmost minimum of $[i - w + 1, i]$, which is $\mu(i - w + 1)$. The minimizer indices never decrease (as in the proof on the minimizer page, with ties broken to the left), so recording the head only when it changes lists each distinct one once, in order. $\square$

**Lemma 2 (canonical k-mers).** Let $\overline{s}$ be the reverse complement of $s$. The canonical k-mer that ends at position $e$ of $s$ is the same as the canonical k-mer that starts at position $|s| - 1 - e$ of $\overline{s}$. So the hash sequences of $s$ and $\overline{s}$ are reverses of each other, and so are their sketches, as sets of k-mer positions.

*Proof.* The k-mer of $\overline{s}$ at that position is the reverse complement of $s[e - k + 1 \ldots e]$. A k-mer and its reverse complement have the same canonical form, the smaller of the two codes. The skipped k-mers are the same in both. The windows of $\overline{s}$ are the windows of $s$ read backwards, and the minimum of a window is the same set element; with distinct hashes in each window, the choice of minimizer is the same. $\square$

When a window holds two equal smallest hashes, the leftmost rule picks different copies on the two strands, but both copies are the same canonical k-mer, so they still produce an anchor with the same hash.

**Lemma 3 (shared pieces give anchors).** If $Q$ and $R$, or $\overline{Q}$ and $R$, share a substring $u$ of length $w + k - 1$ whose $w$ k-mers are all kept (none has a letter outside the alphabet or is its own reverse complement), and no minimizer is dropped for being too frequent, then the anchor list holds an anchor whose two intervals lie inside the two copies of $u$.

*Proof.* The $w$ k-mers of $u$ form a full window of each sequence, with the same hashes in the same order, so by the argument of Property 1 on the minimizer page both windows choose the same offset, and both sketches hold that k-mer with the same hash. Lemma 2 covers the reverse-complement case. The lookup of line L2 pairs the two entries, which makes the anchor. $\square$

**Lemma 4 (exact chaining).** Let the anchors $a_1, \ldots, a_N$ be sorted by $x$, and run lines L4 to L9 with $h \ge N$ and $G$ larger than every gap. Then $f(i)$ is the largest score of a chain that ends at $a_i$, where a chain $a_{j_1}, \ldots, a_{j_r}$ with $j_1 < \cdots < j_r$ and finite $\beta$ for each consecutive pair scores $w_{j_1} + \sum_{t \ge 2} (\alpha(j_{t-1}, j_t) - \beta(j_{t-1}, j_t))$.

*Proof.* By induction on $i$. The chain $(a_i)$ alone scores $w_i$, which line L5 takes. A longer chain that ends at $a_i$ has a previous anchor $a_j$ with $j < i$, and its score is the score of its prefix, at most $f(j)$ by induction, plus $\alpha(j, i) - \beta(j, i)$. Line L6 visits every $j < i$, so line L7 sees the largest of these values, and each is attained by the best chain that ends at $a_j$ followed by $a_i$. $\square$

**Lemma 5 (limited chaining).** For any $h \ge 1$ and any $G$, the value $\tilde f(i)$ computed with the limits satisfies $\tilde f(i) \le f(i)$, and $\tilde f(i)$ is the score of an actual chain, the one found by following $P$.

*Proof.* By induction on $i$. The value $\tilde f(i)$ is $w_i$ or $\tilde f(j) + \alpha(j, i) - \beta(j, i)$ for some $j < i$ with finite $\beta$, and $\tilde f(j) \le f(j)$, so it is at most a value that the exact recurrence also considers. Following $P$ from $i$ gives anchors with finite $\beta$ for each consecutive pair, and the scores add up to $\tilde f(i)$ by the same induction. $\square$

So the chain that minimap2 reports is a valid chain, and its score is a lower bound on the best chain score; it is equal to the best score whenever the limits never cut off a predecessor that the exact recurrence uses along some best chain.
