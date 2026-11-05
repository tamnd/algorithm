---
title: PSRS sorts, and every processor gets at most 2n/p − p keys
proves: [correctness]
status: full
---

Let the $n$ keys be distinct, let $p^2$ divide $n$ and let $w = n/p^2$, so each block has $pw$ keys. Equal keys reduce to this case by pairing each key with its input index and ordering the pairs by key, then index.

## Lemma 1. The output is sorted

*Proof.* Let $y_0 = -\infty$ and $y_p = +\infty$. The samples are sorted, so $y_1 \le \cdots \le y_{p-1}$. Each key $x$ lies in exactly one bucket $j$, the one with $y_j < x \le y_{j+1}$. If $x$ is in bucket $j$ and $x'$ is in bucket $j' > j$, then $x \le y_{j+1} \le y_{j'} < x'$. Each block is sorted, so its keys of bucket $j$ form a sorted, contiguous piece, found on line L4 by binary search. Line L6 merges the pieces of bucket $j$ into a sorted list of all its keys. So the buckets, in order, are the sorted output. $\square$

## Lemma 2. Each bucket contains exactly p samples

*Proof.* The keys are distinct, so the samples are distinct, and $S[0] < S[1] < \cdots < S[p^2 - 1]$. With $y_j = S[jp - 1]$, the samples in bucket $j$ are those with $S[jp - 1] < S[t] \le S[(j+1)p - 1]$, where for $j = 0$ the lower bound is $-\infty$ and for $j = p - 1$ the upper bound is $+\infty$, which is $S[p^2 - 1]$ for the samples. These are $S[jp], \ldots, S[(j+1)p - 1]$, which are $p$ samples. $\square$

## Lemma 3. A stretch of a block with c samples has at most (c + 1)w − 1 keys

Within a sorted block, the samples are at positions $0, w, 2w, \ldots, (p-1)w$. Let a stretch of consecutive positions $L, \ldots, R$ contain $c$ of these positions. Then $R - L + 1 \le (c + 1)w - 1$.

*Proof.* If $c = 0$, the stretch lies between two consecutive sample positions $tw < L \le R < (t+1)w$, or after the last one, $(p-1)w < L \le R \le pw - 1$. In both cases it has at most $w - 1$ positions. If $c \ge 1$, let the sample positions in the stretch be $tw, \ldots, (t + c - 1)w$. The stretch starts after the previous sample position, so $L \ge (t-1)w + 1$, or $L \ge 0 = tw$ if $t = 0$. In both cases $L \ge tw - w + 1$. It ends before the next sample position, so $R \le (t + c)w - 1$, which also holds at the end of the block, where $R \le pw - 1$ and $t + c \le p$. So $R - L + 1 \le (t + c)w - 1 - (tw - w + 1) + 1 = (c + 1)w - 1$. $\square$

## Theorem. Bucket bound

Every bucket has at most $2n/p - p$ keys.

*Proof.* Fix bucket $j$. In block $b$, the keys of bucket $j$ form a stretch of consecutive positions, by Lemma 1. Let $c_b$ be the number of samples of block $b$ in this stretch. The samples of a block lie in the bucket exactly when they lie in this stretch, so by Lemma 2, $\sum_b c_b = p$. By Lemma 3, the bucket has at most

$$\sum_{b=0}^{p-1} \big((c_b + 1) w - 1\big) = (p + p) w - p = 2pw - p = \frac{2n}{p} - p$$

keys. $\square$

The example on the page has $n = 27$ and $p = 3$, and its third bucket has $15 = 2 \cdot 9 - 3$ keys, so for these values of $n$ and $p$ the bound is reached.
