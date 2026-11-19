---
title: The Luhn procedure computes the significant words, the cluster scores and the top sentences of the definition
proves: [correctness]
status: full
---

Fix a document $D = (s_1, \ldots, s_n)$, a key function $\kappa$, a set of stop keys, cut offs $lo \le hi$, a gap limit $g \ge 0$ and $k \ge 0$. The definitions are those of the page: $f(v)$ is the number of words $w$ of $D$ with $\kappa(w) = v$ and $v$ not a stop key, $\mathrm{Sig} = \{v : lo \le f(v) \le hi\}$, and in a sentence with significant positions $p_1 < \cdots < p_r$ a cluster is a maximal index interval $[a, b]$ with $p_{t+1} - p_t - 1 \le g$ for all $a \le t < b$. Its score is $(b - a + 1)^2 / (p_b - p_a + 1)$, and the sentence score is the maximum over the clusters, or 0 when $r = 0$.

**Lemma 1 (counts).** After line L2, $f(v)$ equals the definition for every key $v$, and line L3 returns $\mathrm{Sig}$.

*Proof.* Line L1 starts every count at 0. Line L2 visits each word occurrence of $D$ once and adds 1 to $f(\kappa(w))$ exactly when $\kappa(w)$ is not a stop key. So $f(v)$ is the number of such occurrences with key $v$. Line L3 keeps a key exactly when its count lies in $[lo, hi]$. $\square$

**Lemma 2 (clusters).** The clusters of a sentence partition $\{1, \ldots, r\}$ into consecutive intervals, and the cut points are exactly the indices $t$ with $p_{t+1} - p_t - 1 > g$.

*Proof.* Call $t$ a cut if $p_{t+1} - p_t - 1 > g$. An interval with no cut inside satisfies the gap condition, and an interval that contains a cut $t$ with $a \le t < b$ does not. So the intervals with the gap condition are the intervals that lie between two consecutive cuts, and the maximal ones are exactly the intervals from one cut (or the start) to the next cut (or the end). These intervals are disjoint and cover $\{1, \ldots, r\}$. $\square$

**Lemma 3 (the loop).** For one sentence, lines L6 to L11 set $\mathrm{score}(s)$ to the sentence score of the definition.

*Proof.* Invariant at the start of the iteration for $b$: (i) $a$ is the first index of the cluster that contains $b$, and (ii) $\mathrm{score}(s)$ is the maximum of 0 and the scores of all clusters that end before $a$. Before the first iteration $a = 1$ and the score is 0, and index 1 starts a cluster by Lemma 2, so both hold. In the iteration for $b$, line L8 tests whether $b$ is the last index or a cut. By Lemma 2 this holds exactly when $b$ ends the cluster that starts at $a$. If it holds, lines L9 and L10 compute the score of the cluster $[a, b]$ and take the maximum, and line L11 sets $a = b + 1$, which starts the next cluster by Lemma 2; so (i) and (ii) hold for $b + 1$. If it does not hold, $b + 1$ is in the same cluster as $b$, and nothing changes, so both still hold. After the last iteration every cluster has ended and been scored once, so by (ii) the score is the maximum over all clusters. If $r = 0$, the loop does not run and the score is 0, as defined. $\square$

**Theorem.** The procedure returns the indices of $k$ sentences with the highest scores, with ties broken by the earlier index and sentences with score 0 left out, in increasing order.

*Proof.* By Lemmas 1 and 3 every sentence gets its score of the definition. Line L12 sorts the indices by the key (score descending, index ascending), which is a total order, takes the first $k$, drops those with score 0 and sorts the rest by index. Every kept index $i$ and every index $j$ not kept with a positive score satisfy $(-\mathrm{score}_i, i) < (-\mathrm{score}_j, j)$, which is the claim. $\blacksquare$

**Remark (bounds).** A cluster with $m$ significant words spans $\ell$ words with $m \le \ell \le m + (m - 1) g$, because each of the $m - 1$ gaps holds at most $g$ words. So its score $m^2 / \ell$ satisfies $m / (g + 1) < m^2 / \ell \le m$ when $m \ge 2$, and equals 1 when $m = 1$. The tests check that a sentence score is 0 or at least $1/(g + 1)$, and at most the number of significant words of the sentence.

**Remark (complexity).** Lines L1 to L3 touch each word once with an expected $O(1)$ hash operation, and the loop of lines L5 to L11 touches each position of each sentence a constant number of times. Line L12 sorts $n$ keys. The total is $O(N + n \log n)$ expected time for $N$ words, with $O(N)$ space for the counts and the positions.
