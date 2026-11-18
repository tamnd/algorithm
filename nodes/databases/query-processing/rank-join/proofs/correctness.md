---
title: The hash rank join outputs the join in non-increasing order of a monotone score, so its first k results are a top-k answer
proves: [correctness, termination, time.average]
status: full
---

We use the line numbers of the pseudocode. $L$ has $n$ tuples and $R$ has $m$ tuples, each sorted by score from high to low. We treat each stored tuple as a distinct occurrence, so the join $J = L \bowtie R$ is a bag of pairs $(l, r)$ with equal keys that are not NULL, and the score of a pair is $f(l, r) = f(\mathit{score}(l), \mathit{score}(r))$, also written $f(x)$ for a pair $x$. The function $f$ is *monotone*: $f(x, y) \le f(x', y')$ when $x \le x'$ and $y \le y'$. We write $\mathit{top}_L$ for the score of the first tuple of $L$ and $\mathit{bot}_L$ for the score of the last tuple read from $L$, and the same for $R$. An input is *exhausted* when all its tuples have been read.

**Lemma 1 (each pair is formed once).** A pair $(l, r) \in J$ enters the queue exactly once, at the read of whichever of $l$ and $r$ is read later, and never before.

*Proof.* Say $l$ is read after $r$. When $l$ is read (line L5), $r$ is already in the table of $R$, under its key, because line L5 inserts every tuple with a key that is not NULL when it is read. So line L6 finds $r$ among the tuples of the table of $R$ with the key of $l$ and inserts $(l, r)$ in the queue. At the earlier read of $r$, $l$ was not in the table of $L$, so that read did not form the pair. A tuple is read only once, so no other read forms it. A tuple with a NULL key is not inserted and does not probe, which matches the join. The case where $r$ is read later is the same. $\square$

So at any time each pair of $J$ is in exactly one of three states: *output*, *queued* or *unformed*, and a pair is unformed exactly when at least one of its tuples is not yet read.

**Lemma 2 (threshold).** After line L7, every unformed pair has score at most $T$.

*Proof.* Take an unformed pair $(l, r)$. Suppose first that $l$ is not read. Then $L$ is not exhausted, and since $L$ is sorted, $\mathit{score}(l) \le \mathit{bot}_L$ if some tuple of $L$ has been read, and $\mathit{score}(l) \le \mathit{top}_L$ in any case. Also $\mathit{score}(r) \le \mathit{top}_R$. If both inputs have been read at least once, the term $f(\mathit{bot}_L, \mathit{top}_R)$ is part of $T$, and monotonicity gives $f(l, r) \le f(\mathit{bot}_L, \mathit{top}_R) \le T$. If one input has not been read at all, the term $f(\mathit{top}_L, \mathit{top}_R)$ is part of $T$, and $f(l, r) \le f(\mathit{top}_L, \mathit{top}_R)$. The case where $r$ is not read is symmetric, with the term $f(\mathit{top}_L, \mathit{bot}_R)$. If both inputs are exhausted, no pair is unformed and $T = -\infty$ is correct. $\square$

**Lemma 3 (output step).** When a pair $x$ is output, at line L8 or line L9, every pair of $J$ that is not yet output has score at most $f(x)$.

*Proof.* Pairs that are queued have score at most $f(x)$, because $x$ is the maximum of the queue. At line L8, $f(x) \ge T$, so by Lemma 2 every unformed pair has score at most $f(x)$. At line L9 both inputs are exhausted, so no pair is unformed. $\square$

**Theorem 1 (correctness).** Let $x_1, x_2, \dots$ be the output. Then each pair of $J$ appears at most once, $f(x_1) \ge f(x_2) \ge \dots$, and for each $j$ the pairs $x_1, \dots, x_j$ have the $j$ largest scores of $J$: no pair of $J$ outside them has a larger score than $f(x_j)$. The output has $\min(k, |J|)$ pairs, and with $k$ unbounded it is all of $J$.

*Proof.* A pair is output only after it is queued, it is removed from the queue when it is output, and by Lemma 1 it is queued once, so it is output at most once. Lemma 3 at the output of $x_j$ says that every pair not among $x_1, \dots, x_{j-1}$, and in particular $x_{j+1}$, has score at most $f(x_j)$. This gives both the order and the top-$j$ property. For the count: the loop of line L3 ends when $k$ pairs are output or both inputs are exhausted. In the second case every pair of $J$ is formed by Lemma 1, so line L9 outputs from the queue until $k$ pairs are output or the queue is empty, that is, until $\min(k, |J|)$ pairs are output. $\blacksquare$

The proof uses only that $f$ is monotone. For a function that is not monotone, an unread tuple with a low score can still give a high combined score, Lemma 2 fails, and no threshold that uses only the scores read so far is safe.

**Theorem 2 (termination and cost).** The algorithm stops after at most $n + m$ iterations of the loop of line L3. Let $d_L$ and $d_R$ be the number of tuples read from each input when it stops, and let $J_d$ be the number of pairs in the join of these two prefixes. With hash tables in expected $O(1)$ time per operation and a binary heap for the queue, the expected work is $O((d_L + d_R) + J_d \log(J_d + 2) + k \log(J_d + 2))$ and the space is $O(d_L + d_R + J_d)$.

*Proof.* Each iteration reads one new tuple at line L5, so there are at most $n + m$ iterations, and line L9 pops at most $J_d$ pairs. Each read costs one insertion and one lookup. Line L6 forms each of the $J_d$ pairs once (Lemma 1) and pushes it in $O(\log(J_d + 2))$ time. Line L7 costs $O(1)$ evaluations of $f$. Each output is one pop, and at most $k$ pops happen. The tables hold the $d_L + d_R$ tuples read and the queue holds at most $J_d$ pairs. $\blacksquare$

The depths $d_L$ and $d_R$ depend on the data. If the tuples with high scores do not join, the algorithm can read both inputs to the end for $k = 1$: take $L$ with scores $n, n - 1, \dots, 1$ and keys $1, 2, \dots, n$, and $R$ with scores $m, \dots, 1$ and keys $-1, \dots, -(m - 1)$ and a last tuple with key $n$. The only pair is formed at the last read of $R$, so $d_L + d_R = n + m$.
