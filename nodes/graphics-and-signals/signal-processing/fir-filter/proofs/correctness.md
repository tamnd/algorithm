---
title: The FIR filter computes the convolution sum, is stable, and has linear phase when its taps are symmetric
proves: [correctness]
status: full
---

We write $x[i] = 0$ for $i < 0$, and $P = M + 1$ for the length of the delay line. All indices of $B$ are taken modulo $P$.

**Lemma 1 (the delay line).** At the start of the step for the input $x[n]$, that is just before line L3, we have $p = n \bmod P$, and $B[(p - k) \bmod P] = x[n-k]$ for $k = 1, \ldots, M$.

*Proof.* By induction on $n$. For $n = 0$, line L1 sets $p = 0$ and all cells to 0, and $x[-k] = 0$ for $k \ge 1$, so the statement holds. Assume it holds at the start of step $n$. Line L3 writes $x[n]$ to $B[p]$. The cells $B[(p - k) \bmod P]$ for $k = 1, \ldots, M$ are the $M$ other cells, because the residues $p - k$ for $k = 0, \ldots, M$ are $P$ distinct values modulo $P$. So after line L3, $B[(p - k) \bmod P] = x[n-k]$ for $k = 0, \ldots, M$. Lines L4 to L8 do not write to $B$. Line L9 sets $p' = (p + 1) \bmod P = (n+1) \bmod P$. For $k = 1, \ldots, M$, the cell $B[(p' - k) \bmod P] = B[(p - (k-1)) \bmod P]$ holds $x[n - (k-1)] = x[(n+1) - k]$. This is the statement for step $n + 1$. $\square$

**Theorem 1 (the output).** Line L8 of the step for $x[n]$ outputs $y[n] = \sum_{k=0}^{M} h[k]\, x[n-k]$.

*Proof.* By Lemma 1 and the write of line L3, during lines L4 to L7 the cell $B[(p - k) \bmod P]$ holds $x[n-k]$ for $k = 0, \ldots, M$. Line L4 sets $acc = h[0]\, x[n]$. Line L6 computes $j = (p - k) \bmod P$, so line L7 adds $h[k]\, x[n-k]$. After the loop of line L5, $acc = \sum_{k=0}^{M} h[k]\, x[n-k]$. $\square$

**Theorem 2 (stability).** If $|x[n]| \le X$ for all $n$, then $|y[n]| \le X \sum_{k=0}^{M} |h[k]|$ for all $n$, and some bounded input reaches this bound.

*Proof.* By Theorem 1 and the triangle inequality, $|y[n]| \le \sum_k |h[k]|\, |x[n-k]| \le X \sum_k |h[k]|$. For real taps, the input with $x[M-k] = X \operatorname{sign}(h[k])$ for $k = 0, \ldots, M$ gives $y[M] = X \sum_k |h[k]|$. $\square$

**Theorem 3 (linear phase).** If $h[k] = h[M-k]$ for all $k$ and the taps are real, then $H(e^{i\omega}) = e^{-i\omega M/2} A(\omega)$ with the real function $A(\omega) = \sum_{k=0}^{M} h[k] \cos(\omega(M/2 - k))$. If $h[k] = -h[M-k]$, then $H(e^{i\omega}) = i\, e^{-i\omega M/2} A(\omega)$ with the real function $A(\omega) = \sum_{k=0}^{M} h[k] \sin(\omega(M/2 - k))$.

*Proof.* Write $H(e^{i\omega}) = e^{-i\omega M/2} \sum_{k=0}^{M} h[k]\, e^{i\omega(M/2 - k)}$. The map $k \mapsto M - k$ is a bijection of $\{0, \ldots, M\}$ and sends $M/2 - k$ to $-(M/2 - k)$. In the symmetric case, the sum is therefore equal to its own image under $k \mapsto M - k$, which is $\sum_k h[k]\, e^{-i\omega(M/2 - k)}$. The average of the two forms is $\sum_k h[k] \cos(\omega(M/2 - k))$. In the antisymmetric case, the sum is equal to $-\sum_k h[k]\, e^{-i\omega(M/2 - k)}$, and the average of the two forms is $i \sum_k h[k] \sin(\omega(M/2 - k))$. In both cases $A$ is real because the taps are real. $\blacksquare$

**Corollary (group delay).** Where $A(\omega) \ne 0$, the phase of $H$ is $-\omega M/2$ plus a constant that is a multiple of $\pi$ (or $\pi/2$ in the antisymmetric case) on each interval where $A$ keeps its sign. So the group delay $-\frac{d}{d\omega} \arg H$ is $M/2$ at every such frequency.

**Corollary (forced zeros).** For a symmetric filter of odd order, $M/2 - k$ is a half-integer for each $k$, so $\cos(\pi(M/2 - k)) = 0$ and $A(\pi) = 0$. For an antisymmetric filter, $\sin(0) = 0$ gives $A(0) = 0$, and for even $M$ also $\sin(\pi(M/2 - k)) = 0$ gives $A(\pi) = 0$.
