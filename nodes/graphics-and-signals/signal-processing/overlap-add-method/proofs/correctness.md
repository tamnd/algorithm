---
title: Overlap-add computes the linear convolution
proves: [correctness]
status: full
---

We write $x[i] = 0$ for $i < 0$ and $i \ge L$, and $h[k] = 0$ for $k < 0$ and $k \ge M$. The target is $y[n] = \sum_{k} h[k]\, x[n-k]$ for $0 \le n \le L + M - 2$. We assume $N \ge M$, so $B = N - M + 1 \ge 1$ by line L1, and the FFTs of lines L2 and L6 are exact, as in the real RAM.

**Lemma (one block).** For a start $s$, let $u_s[j] = x[s + j]$ for $0 \le j \le B - 1$ and $u_s[j] = 0$ for $B \le j \le N - 1$, as in line L5. Then the vector $v$ of line L6 satisfies $v[j] = \sum_k h[k]\, u_s[j - k]$ for $0 \le j \le N - 1$, with $u_s[i] = 0$ for $i < 0$, and $\sum_k h[k]\, u_s[j - k] = 0$ for $j \ge N$.

*Proof.* By the convolution theorem for the DFT of length $N$, line L6 gives the circular convolution $v[j] = \sum_{k=0}^{N-1} u_s[k]\, h[(j - k) \bmod N]$, where $h$ is padded with zeros to length $N$. Let $w = u_s * h$ be the linear convolution. The block $u_s$ is zero outside $[0, B - 1]$ and $h$ is zero outside $[0, M - 1]$, so $w$ is zero outside $[0, B + M - 2] = [0, N - 1]$. The circular convolution of length $N$ is the time-aliased linear one, $v[j] = \sum_{r \ge 0} w[j + rN]$. For $0 \le j \le N - 1$ and $r \ge 1$, the index $j + rN \ge N$ is outside the support of $w$, so $v[j] = w[j]$. $\square$

**Lemma (the blocks cover $x$).** The starts of line L4 are $s = 0, B, 2B, \ldots$ with $s < L$. For each $i$ with $0 \le i \le L - 1$ there is exactly one start $s$ with $s \le i \le s + B - 1$, and $x[i] = u_s[i - s]$. So $x[i] = \sum_s u_s[i - s]$ for every integer $i$, with $u_s$ extended by zeros outside $[0, N - 1]$.

*Proof.* The intervals $[s, s + B - 1]$ for $s = 0, B, 2B, \ldots$ partition the integers $i \ge 0$. The last start is the largest multiple of $B$ below $L$, so the intervals with $s < L$ cover $[0, L - 1]$. Positions $s + j$ with $s + j \ge L$ get $u_s[j] = x[s + j] = 0$ by the convention, and positions $B \le j \le N - 1$ get $u_s[j] = 0$ from the padding. So each $x[i]$ with $0 \le i \le L - 1$ appears in exactly one block, and the sum over the blocks is zero outside $[0, L - 1]$. $\square$

**Theorem.** OVERLAP-ADD$(x, h, N)$ returns $y = x * h$ of length $L + M - 1$.

*Proof.* Line L3 sets $y$ to zeros. By the loop of lines L7 and L8, after all passes each $y[n]$ with $0 \le n \le L + M - 2$ equals $\sum_s v_s[n - s]$, summed over the starts $s$ with $0 \le n - s \le N - 1$, where $v_s$ is the vector $v$ of the pass with start $s$. The test of line L8 only removes indices $n \ge L + M - 1$, which are not part of the output. By the first lemma, $v_s[j] = (u_s * h)[j]$ for $0 \le j \le N - 1$, and $(u_s * h)[j] = 0$ for $j \ge N$ and for $j < 0$. So

$$y[n] = \sum_s (u_s * h)[n - s] = \sum_s \sum_k h[k]\, u_s[n - s - k] = \sum_k h[k] \sum_s u_s[(n - k) - s] = \sum_k h[k]\, x[n - k],$$

where the sums are finite, the exchange of the two sums is allowed, and the last step is the second lemma with $i = n - k$. This is the linear convolution. $\blacksquare$

**Floating point.** With a floating-point FFT, line L6 returns $v$ up to a rounding error, and the error of each output sample is the sum of the errors of at most $\lceil (M - 1)/B \rceil + 1$ blocks that overlap at that sample. The structure of the proof does not change; only the equality of the first lemma becomes an approximation.
