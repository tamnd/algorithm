---
title: Monotonic alignment search returns a monotonic alignment of largest total score, chosen by the tie rule
proves: [correctness]
status: full
---

Fix $n \ge 1$ tokens, $T \ge n$ frames and real scores $v_{i,j}$ for $0 \le i < n$ and $0 \le j < T$. An alignment is a map $a$ from frames to tokens with $a(0) = 0$, $a(T - 1) = n - 1$ and $a(j + 1) - a(j) \in \{0, 1\}$. Its score is $S(a) = \sum_{j} v_{a(j), j}$. The work is in the Viterbi semiring $(\mathbb{R} \cup \{-\infty\}, \max, +, -\infty, 0)$.

## Count

An alignment is fixed by the $n - 1$ frames $j \ge 1$ where $a(j) = a(j - 1) + 1$. Any $n - 1$ of the $T - 1$ frames $1, \ldots, T - 1$ give one, and different sets give different alignments. So there are $\binom{T - 1}{n - 1}$ alignments.

## The table

A partial alignment ending at $(i, j)$ is a map on the frames $0, \ldots, j$ with $a(0) = 0$, steps in $\{0, 1\}$ and $a(j) = i$.

**Lemma 1.** After lines L1 to L5, $Q_{i,j}$ is the largest score of a partial alignment ending at $(i, j)$, and $-\infty$ if there is none.

*Proof.* By induction on $j$. For $j = 0$ the only partial alignment is $a(0) = 0$, and lines L1 and L2 set $Q_{0,0} = v_{0,0}$ and $Q_{i,0} = -\infty$ for $i > 0$. For $j \ge 1$, a partial alignment ending at $(i, j)$ is a partial alignment ending at $(i, j - 1)$ or at $(i - 1, j - 1)$ followed by the frame $j$ on token $i$, and each such extension is allowed. Its score is the score of the prefix plus $v_{i,j}$. Adding a constant keeps the order, so the best one is $v_{i,j}$ plus the larger of the two best prefix scores, which line L5 computes from the induction hypothesis. For $i > j$ there is no partial alignment, because the token index grows by at most one per frame; line L4 skips these cells and they stay $-\infty$. $\square$

**Lemma 2.** If $Q_{i,j}$ is finite and $j \ge 1$, the predecessor chosen by line L9 has a finite value $Q'$ with $Q_{i,j} = v_{i,j} + Q'$.

*Proof.* Line L9 moves to $i - 1$ only when $Q_{i-1,j-1} > Q_{i,j-1}$, and otherwise stays on $i$. In both cases it takes a maximum of the two values of line L5. That maximum is finite because $Q_{i,j}$ is finite. When $i = 0$ only the stay predecessor exists, and when $i = j$ the stay value $Q_{j, j-1}$ is $-\infty$, so the strict test moves down. $\square$

**Theorem 1.** Lines L6 to L11 return an alignment $a$ with $S(a) = \max_{a'} S(a')$, and that score.

*Proof.* A full alignment is a partial alignment ending at $(n - 1, T - 1)$, so by Lemma 1 the maximum is $Q_{n-1,T-1}$, which is finite because $T \ge n$. The traceback starts there. By Lemma 2 each step goes to a finite cell whose value is the current value minus the current score, so after $T - 1$ steps it reaches a finite cell of frame 0, which is $(0, 0)$, and the scores of the visited cells sum to $Q_{n-1,T-1}$. The steps are $0$ or $-1$ in the token index, so $a$ is an alignment. $\square$

**Theorem 2 (tie rule).** Among the alignments of largest score, the returned one is the largest in the lexicographic order of $(a(T - 1), a(T - 2), \ldots, a(0))$.

*Proof.* All optimal alignments have $a(T - 1) = n - 1$. Assume the returned $a$ agrees with the largest optimal sequence on the frames $T - 1, \ldots, j$, with $a(j) = i$. The optimal alignments with this suffix are exactly those whose prefix is an optimal partial alignment ending at $(i, j)$. By Lemma 1 such a prefix can take $a(j - 1) = i$ exactly when $Q_{i,j-1} = \max(Q_{i,j-1}, Q_{i-1,j-1})$, that is when $Q_{i,j-1} \ge Q_{i-1,j-1}$. Line L9 stays on $i$ exactly in that case, so it picks the larger of the possible values of $a(j - 1)$. Induction down to $j = 1$ gives the claim. $\square$

The tests compare the result, ties included, with the best of all $\binom{T - 1}{n - 1}$ alignments under this order, for $n \le 5$ and $T \le 9$.

## Cost

Line L5 runs once for each cell with $i \le j$ and $i < n$, which is $\Theta(n T)$ cells for $T \ge 2n$, each in constant time. The table takes $\Theta(n T)$ space, and the traceback takes $T$ steps.
