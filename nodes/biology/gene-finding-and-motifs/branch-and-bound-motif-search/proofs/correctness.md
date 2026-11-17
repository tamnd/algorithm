---
title: Both branch and bound searches return an optimum
proves: [correctness]
status: full
---

Let $s_1, \ldots, s_n$ be sequences, each with $W \ge 1$ windows of length $L$. For a tuple of starts $p = (p_1, \ldots, p_i)$ of the first $i$ sequences, let $c^{p}_j(a)$ be the number of the $i$ windows with letter $a$ in column $j$, and let $S(p) = \sum_{j=1}^{L} (i - \max_a c^{p}_j(a))$, the partial score. For $i = n$ this is the motif score. For a string $u$ of length $k \le L$, let $B(u) = \sum_i \min_{1 \le q \le W} d_H(u, s_i[q .. q + k - 1])$. For $k = L$ this is the total distance $D(u)$.

**Lemma 1 (the partial score never drops).** If $p'$ extends $p$ by one start, then $S(p') \ge S(p)$.

*Proof.* Let $p$ fix $i$ rows. The new row adds one letter to each column, so for each $j$ the number of rows grows by 1 and $\max_a c_j(a)$ grows by 0 or 1. So each term $i - \max_a c_j(a)$ grows by 1 or stays. $\square$

By induction, $S(p) \le S(r)$ for every complete tuple $r$ that extends $p$.

**Lemma 2 (the prefix bound never drops).** If $u'$ is $u$ followed by one letter, then $B(u') \ge B(u)$. So $B(u) \le D(v)$ for every string $v$ of length $L$ with prefix $u$.

*Proof.* For each $i$ and $q$, $d_H(u', s_i[q .. q + k]) = d_H(u, s_i[q .. q + k - 1]) + [u'_{k+1} \ne s_i[q + k]] \ge d_H(u, s_i[q .. q + k - 1])$. A minimum over $q$ of larger terms is at least as large, and the sum over $i$ keeps the order. Apply this $L - k$ times. $\square$

**Lemma 3 (the table).** When EXTEND$(u, k)$ starts, $m[i][q] = d_H(u, s_i[q .. q + k - 1])$ for all $i$ and $q$. So line L17 computes $B(u)$.

*Proof.* By induction on the calls. At the first call, $u$ is empty and line L14 sets every entry to 0, which is the distance of two empty strings. Suppose the claim holds when EXTEND$(u, k)$ starts. Before the call EXTEND$(ua, k + 1)$, line L21 adds 1 to $m[i][q]$ exactly when $s_i[q + k] \ne a$, which is the mismatch in column $k + 1$ (with 1-based columns of the window), so the claim holds for $ua$. That call and its own calls end with the table as it was at their start, by induction on the depth of the recursion, and line L23 then removes what line L21 added. So the table is again the table of $u$ when the next letter is tried. $\square$

The counts $c$ of the position search satisfy the same kind of invariant: when SEARCH$(i)$ starts, $c$ holds the letters of the windows of $p_1, \ldots, p_{i-1}$. Line L10 adds the window of $p_i$ and line L12 removes it. So line L11 computes $S(p_1, \ldots, p_i)$ and line L6 computes the score of the complete tuple.

**Lemma 4 (no better leaf is cut).** Let $b$ be the value of $best$ at some moment, and let a subtree be cut at that moment. Then no leaf of the subtree has a score below $b$.

*Proof.* In the position search, the cut is the failed test of line L11, so $S(p_1, \ldots, p_i) \ge b$, and by Lemma 1 every complete tuple below has a score at least $b$. In the prefix search, the cut is line L18, so $B(u) \ge b$, and by Lemma 2 every string below has $D \ge b$. $\square$

**Theorem.** BB-MOTIF returns a tuple of starts with the smallest motif score, and BB-MEDIAN returns a string with the smallest total distance $D$. In each case the result is the first optimum in the order of the tree.

*Proof.* We give the proof for BB-MEDIAN; the proof for BB-MOTIF is the same with Lemma 1 in place of Lemma 2 and line L7 in place of line L19.

The value of $best$ only decreases, and when it changes at line L19 it becomes $D(u)$ of a leaf $u$ by Lemma 3, with $bestv = u$. The first leaf of the tree, AA...A, is reached: on its path every bound is at most $nL < nL + 1$, the start value. So at the end $best = D(bestv)$ for some string $bestv$.

Let $D^*$ be the smallest total distance and $v^*$ the first string in tree order with $D(v^*) = D^*$. Suppose $v^*$ is not reached as a leaf with $B = D^*$ and the test of line L18 passed. Then some node on its path, a prefix $u$, was cut at line L18 with $B(u) \ge best$ at that moment, or $v^*$ was cut at line L18 itself. At that moment $best$ is the distance of a leaf before $v^*$ in tree order, which is larger than $D^*$ by the choice of $v^*$. So $B(u) \le D(v^*) = D^* < best$ by Lemma 2, and the cut could not happen. So $v^*$ is reached, its bound $D^*$ is below $best$, and line L19 sets $best = D^*$ and $bestv = v^*$.

After that, $best = D^*$, and no later leaf can pass line L18, since its bound is its distance, at least $D^*$. So the result is $v^*$ with distance $D^*$. $\square$

**Corollary (the equivalence check).** The score returned by BB-MOTIF equals the distance returned by BB-MEDIAN, by the equivalence theorem of the median string problem. The tests check this on random inputs, and check both results against brute force over all tuples of starts and all $4^L$ strings.
