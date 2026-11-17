---
title: The chain DP is optimal, every returned alignment is real and above the threshold, and an exact read is always returned with the top score
proves: [correctness]
status: full
---

We use the pseudocode of the page. A read $R$ has length $L \ge k$. For a strand, $q$ is $R$ or its reverse complement. An anchor $(x, y)$ on a target $t$ means $q[x..x + k - 1] = t[y..y + k - 1]$, an exact k-mer match. Its diagonal is $y - x$. The scores are $\mathrm{MATCH} > 0$ for a match and negative values for a mismatch and a gap. The band is $b \ge 0$, and the two fractions are $\tau', \tau \in [0, 1]$. Positions here are 0-based, as in the code.

## 1. The chain DP

An anchor $j$ may follow $i$ when $x_i < x_j$, $y_i < y_j$ and $g_{ij} = |(y_j - x_j) - (y_i - x_i)| \le b$. A chain is a sequence of anchors in which each one may follow the one before it. Its score is

$$\sigma(a_1, \ldots, a_m) = k + \sum_{j=1}^{m-1} \bigl(\min(x_{j+1} - x_j,\ y_{j+1} - y_j,\ k) - g_{j,j+1}\bigr).$$

The function CHAIN sorts the distinct anchors by $(y, x)$ and computes $f(j) = \max\bigl(k,\ \max_{i < j,\ i \to j} f(i) + \min(x_j - x_i, y_j - y_i, k) - g_{ij}\bigr)$.

**Lemma 1.** $f(j)$ is the best score of a chain that ends at anchor $j$, and CHAIN returns a chain of the best score over all chains.

*Proof.* By induction on $j$ in the sorted order. If $i$ may precede $j$ then $y_i < y_j$, so $i$ comes before $j$ in the order, and $f(i)$ is already final. A chain that ends at $j$ is either $j$ alone, with score $k$, or a chain that ends at some $i$ that may precede $j$, followed by $j$. Its score is the score of that prefix plus the step term, and the step term depends only on $i$ and $j$. So the best score is the larger of $k$ and the best value of $f(i)$ plus the step term, which is the formula. The back pointers record the $i$ that gives the maximum, so following them from the best $j$ spells a chain of score $f(j)$. $\square$

**Lemma 2.** Every chain has $\sigma \le L$. A chain has $\sigma = L$ only if $q$ occurs in $t$ at position $y_1 - x_1$ with no error.

*Proof.* Each step term is at most $x_{j+1} - x_j$, as the minimum is at most this value and $g \ge 0$. So $\sigma \le k + x_m - x_1 \le k + (L - k) - 0 = L$. Equality needs $x_1 = 0$, $x_m = L - k$, and in every step $g = 0$ and $\min(x_{j+1} - x_j, y_{j+1} - y_j, k) = x_{j+1} - x_j$. Then every anchor is on one diagonal $d = y_1 - x_1 = y_1$, and $x_{j+1} - x_j \le k$, so the read intervals $[x_j, x_j + k)$ cover $[0, L)$ with no hole. Each position $p$ of the read is in some anchor, so $q[p] = t[d + p]$. Hence $q = t[d..d + L - 1]$. $\square$

## 2. Soundness

**Theorem 1 (soundness).** Every hit that the algorithm returns is on a transcript, not on a decoy. Its score is the score of a real semiglobal alignment of $q$ to a substring of the target that starts at the reported position, so it is at most the best semiglobal score of $q$ against the whole target. And the score is at least $\tau \cdot \mathrm{MATCH} \cdot L$.

*Proof.* Line L10 returns only hits on non-decoy targets. Each hit comes from line L7, which runs the semiglobal alignment of $q$ against the window $t[lo..hi - 1]$ and adds $lo$ to the start, so the score is that of an alignment of all of $q$ to a substring of $t$. An alignment to a substring of $t$ is also a semiglobal alignment to $t$, because the ends of $t$ are free, so the score is at most the best one on $t$. Line L8 keeps only the hits with score at least $\tau \cdot \mathrm{MATCH} \cdot L$. $\square$

**Theorem 2 (decoy rule).** If the best valid score on a decoy is strictly greater than every valid score on a transcript, the read gets no hit. Otherwise the decoy hits are dropped and all the valid transcript hits are returned.

*Proof.* This is line L9, then line L10. $\square$

## 3. Completeness for exact reads

**Theorem 3.** Suppose $\tau' \le 1$, $\tau \le 1$, and $R$ or its reverse complement occurs with no error in a transcript $t$. Then the algorithm returns a hit on $t$ with the top score $\mathrm{MATCH} \cdot L$.

*Proof.* Let $q$ be the strand that occurs in $t$ at position $d$. All $L - k + 1$ k-mers of $q$ are in the index, at the anchors $(x, d + x)$, so $t$ has hits and gets a candidate in line L4. The chain of the anchors with $x = 0, k, 2k, \ldots$ and then $x = L - k$ has all anchors on the diagonal $d$, steps of at most $k$ and no gap, so its score is $L$. By Lemma 1 the chain of $t$ has score at least $L$, and by Lemma 2 at most $L$, so it is exactly $L$. By Lemma 2 again, no chain anywhere has a higher score, so the best chain score $S$ of line L5 is $L$, and the candidate of $t$ passes line L6 because $L \ge \tau' L$.

The chain that CHAIN returns for $t$ may be another chain of score $L$. By Lemma 2 it shows an exact occurrence of $q$ at its diagonal $d' = y_1 - x_1$. The window of line L7 is $[\max(0, d' - b), \min(|t|, d' + L + b))$, since $x_1 = 0$ and $x_m = L - k$ give $y_m + (L - x_m) = d' + L$. The occurrence $[d', d' + L)$ lies in $t$, so it lies in the window. Each letter of $q$ adds at most $\mathrm{MATCH}$ to a semiglobal score and gaps only subtract, so the best score is at most $\mathrm{MATCH} \cdot L$, and the exact occurrence reaches it. So the score of line L7 is $\mathrm{MATCH} \cdot L$, which passes line L8 because $\tau \le 1$.

No target can score more than $\mathrm{MATCH} \cdot L$, so no decoy score is strictly greater than this transcript score, and line L9 does not discard the read. Line L10 returns the hit. $\square$

## 4. What is not proved

The chain filter of line L6 is a heuristic. A read with errors can have its true location chained with a lower score than a false one, and then the true location is not aligned. Theorem 3 rules this out only for reads without errors. The tests measure that most reads with 2 percent errors are still found, which is a measurement and not a theorem. $\blacksquare$
