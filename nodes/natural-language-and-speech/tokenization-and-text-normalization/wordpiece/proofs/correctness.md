---
title: WordPiece training takes the merge of largest likelihood gain, and the encoder returns the greedy longest-match pieces
proves: [correctness, termination]
status: full
---

Notation. The corpus is a map $C$ from distinct words to positive counts. A segmentation $S$ gives each word $w$ a list of units whose concatenation, after the prefix "##" is removed from every unit but the first, is $w$. The unit count is $c(x) = \sum_w C(w) \cdot \#\{t : S(w)_t = x\}$ and $N = \sum_x c(x)$. All logs are natural logs. Write $F(x) = x \log x$ with $F(0) = 0$. The unigram log likelihood of the corpus with maximum likelihood probabilities $c(x)/N$ is

$$\mathcal{L}(S) = \sum_x c(x) \log \frac{c(x)}{N} = \sum_x F(c(x)) - F(N) \qquad (\log \text{ base } e).$$

The second form holds because $\sum_x c(x) \log N = N \log N$, and units with $c(x) = 0$ add $F(0) = 0$ to both sides.

**Lemma 1 (the pair count).** Let $k$ be the number of occurrences of $(a, b)$ that MERGE replaces, counted with the word counts, and let $ab$ be the joined unit. After the merge, $c(ab)$ grows by $k$, $N$ drops by $k$, and $c(a)$ and $c(b)$ each drop by $k$ if $a \ne b$, while $c(a)$ drops by $2k$ if $a = b$. No other count changes.

*Proof.* Each replacement removes one unit $a$ and one unit $b$ at two adjacent places and puts one unit $ab$ there. The replaced occurrences do not overlap, because the scan in MERGE moves two places after each replacement, so the $k$ replacements remove $2k$ distinct unit occurrences. If $a = b$ these are $2k$ copies of $a$. The joined unit $ab$ is longer than $a$ and than $b$, so $ab$ is neither of them, and its count grows by exactly $k$. The number of units drops by one per replacement. $\square$

**Lemma 2 (the closed form of the gain).** With $k$, $a$, $b$ as in Lemma 1, the change $\mathcal{L}(S') - \mathcal{L}(S)$ is

$$g = F(c_{ab} + k) - F(c_{ab}) + F(c_a - k) - F(c_a) + F(c_b - k) - F(c_b) - F(N - k) + F(N)$$

when $a \ne b$, and the same with $F(c_a - 2k) - F(c_a)$ in place of the two middle differences when $a = b$. This is what merge_gain returns.

*Proof.* Apply the second form of $\mathcal{L}$ before and after the merge. By Lemma 1 every term $F(c(x))$ with $x \notin \{a, b, ab\}$ is the same in both sums and cancels. The remaining terms are the ones written. $\square$

**Theorem 1 (training).** WORDPIECE-TRAIN stops after at most $K$ passes. In each pass, the pair it merges has the largest likelihood gain among all adjacent pairs of the current segmentation, and among pairs with the same gain it is the smallest in string order. The returned vocabulary holds every initial unit and every merged unit.

*Proof.* The loop of line L3 runs at most $K$ times, and line L5 can stop it earlier. Each pass computes the counts of line L4 from the current segmentation. Line L6 gives each pair present in the corpus the value $g$ of Lemma 2, which by that lemma is the exact change of $\mathcal{L}$. Line L7 takes the pair with the largest $g$, with ties broken by the pair itself. Line L8 applies the merge to every word, so the next pass starts from the segmentation that the gain was computed for. Line L2 puts every initial unit into $V$ and line L9 adds each merged unit. $\square$

Theorem 1 says that each merge is the best single step for the likelihood. It does not say that the $K$ merges together give the largest likelihood among all vocabularies of that size. No such claim is made: a greedy sequence of best single steps need not be a best sequence, and for the related objective of compression the search for the best merge sequence is NP-hard.

**Theorem 2 (encoder).** For a word $w$ of $n \le$ max_chars characters and a vocabulary $V$, WORDPIECE-ENCODE returns [UNK] if some step finds no piece. Otherwise it returns $u_1, \ldots, u_r$ with these properties: $u_1 = w[0 \ldots p_1)$ and $u_t = \#\#\, w[p_{t-1} \ldots p_t)$ for $t \ge 2$; each $u_t \in V$; $p_r = n$; and each $p_t$ is the largest $j > p_{t-1}$ for which the piece that starts at $p_{t-1}$ and ends at $j$ is in $V$. It stops after at most $n(n + 1)/2$ tests of line E7.

*Proof.* Inner loop: at the test of line E5, every end $j$ with end $< j \le n$ has been tried and its piece is not in $V$. This holds at line E4, where end $= n$ and the range is empty. Line E8 lowers end by 1 only after line E7 has failed for it, which keeps the invariant. If line E7 succeeds, the piece of length end $-$ start is in $V$ and every longer one is not, so it is the longest. If the loop ends with end $=$ start, no piece starts at this position, and line E9 returns [UNK].

Outer loop: at the test of line E3, out holds $u_1, \ldots, u_t$ with the stated form and start $= p_t$. Line E10 appends the longest piece at $p_t$ and sets start to its end. The prefix "##" is added by line E6 exactly when start $> 0$, which is the case for $t \ge 1$. Since each piece has length at least 1, start grows by at least 1 in each pass, so the outer loop runs at most $n$ times and ends with start $= n$.

Count: at position start $= p$, line E7 runs at most $n - p$ times. The sum over $p = 0, \ldots, n - 1$ is at most $n + (n - 1) + \cdots + 1 = n(n + 1)/2$. $\blacksquare$
