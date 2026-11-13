---
title: Overlap-save computes the linear convolution
proves: [correctness]
status: full
---

We write $x[i] = 0$ for $i < 0$ and $i \ge L$, and $h[k] = 0$ for $k < 0$ and $k \ge M$. The target is $y[n] = \sum_{k=0}^{M-1} h[k]\, x[n-k]$ for $0 \le n \le L + M - 2$. We assume $N \ge M$, so $B = N - M + 1 \ge 1$ by line L1, and the FFTs of lines L2 and L7 are exact, as in the real RAM. Line L3 defines $x'[t] = x[t - (M - 1)]$ for all integers $t$, which is zero outside $M - 1 \le t \le L + M - 2$, and in particular for $t < M - 1$ and for $t \ge L + M - 1$.

**Lemma (the kept samples are exact).** Fix a start $s$ of the loop of line L5, and let $u[j] = x'[s + j]$ for $0 \le j \le N - 1$, as in line L6. If $M - 1 \le j \le N - 1$, then the vector $v$ of line L7 satisfies $v[j] = y[s + j - (M - 1)]$.

*Proof.* By the convolution theorem for the DFT of length $N$, line L7 gives the circular convolution $v[j] = \sum_{k=0}^{N-1} h[k]\, u[(j - k) \bmod N]$, with $h$ padded with zeros to length $N$. Only $0 \le k \le M - 1$ contributes. For these $k$ and $M - 1 \le j \le N - 1$, we have $0 \le j - (M - 1) \le j - k \le j \le N - 1$, so $(j - k) \bmod N = j - k$ and no index wraps. Hence

$$v[j] = \sum_{k=0}^{M-1} h[k]\, x'[s + j - k] = \sum_{k=0}^{M-1} h[k]\, x[s + j - k - (M - 1)] = y[s + j - (M - 1)]. \qquad \square$$

**Lemma (the kept samples tile the output).** For a start $s$, the loop of line L8 writes the indices $t = s + j - (M - 1)$ with $M - 1 \le j \le N - 1$, that is, the interval $I_s = [s, s + B - 1]$, cut at $L + M - 2$ by the test of line L9. The starts are $s = 0, B, 2B, \ldots$ with $s < L + M - 1$. Each output index $0 \le t \le L + M - 2$ lies in exactly one interval $I_s$.

*Proof.* The intervals $[qB, qB + B - 1]$ for $q = 0, 1, 2, \ldots$ partition the integers $t \ge 0$. The interval that holds $t \le L + M - 2$ has its start $qB \le t < L + M - 1$, so the loop of line L5 reaches it. No interval with a start $s \ge L + M - 1$ holds an output index. $\square$

**Theorem.** OVERLAP-SAVE$(x, h, N)$ returns $y = x * h$ of length $L + M - 1$.

*Proof.* By the second lemma, each output index $t$ is written exactly once, in the pass with the start $s$ such that $t \in I_s$, with $j = t - s + (M - 1)$, and line L9 sets $y[t] \leftarrow v[j]$. Since $M - 1 \le j \le N - 1$, the first lemma gives $v[j] = y[s + j - (M - 1)] = y[t]$, the true sample. Line L4 makes $y$ of length $L + M - 1$, and the test of line L9 drops only indices $t \ge L + M - 1$. So line L10 returns the full linear convolution. $\blacksquare$

**The discarded samples.** For $0 \le j \le M - 2$, the circular sum reads $u[(j - k) \bmod N]$ with $j - k < 0$ for $k > j$, that is, the samples $u[N + j - k]$ at the end of the block. These outputs mix the start and the end of the block, and in general they differ from any sample of $y$. That is why line L8 starts at $j = M - 1$.

**Floating point.** With a floating-point FFT, the first lemma holds up to the rounding error of one FFT pair, and each output sample comes from exactly one block.
