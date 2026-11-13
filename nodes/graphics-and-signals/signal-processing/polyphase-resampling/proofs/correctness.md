---
title: The polyphase resampler outputs exactly the samples of the upsample, filter and downsample form
proves: [correctness]
status: full
---

Let $x[0 \ldots N-1]$ be the input, with $x[s] = 0$ for $s < 0$ and $s \ge N$. Let $h[0 \ldots K-1]$ be the filter, with $h[k] = 0$ outside $0 \le k < K$, and let $L, M \ge 1$. The upsampled signal is $u[t] = x[t/L]$ if $L$ divides $t$ and $u[t] = 0$ otherwise. The three-stage output is $y^{*}[n] = \sum_{k} h[k]\, u[nM - k]$ for $0 \le n \le n_{\max} = \lfloor (K + LN - 2)/M \rfloor$. The phases are $e_r[i] = h[iL + r]$ for $0 \le r < L$ and $i \ge 0$.

**Lemma 1 (the phase counter).** At line L4 of step $n$, $nM = qL + r$ and $0 \le r < L$.

*Proof.* By induction on $n$. For $n = 0$, line L2 sets $q = r = 0$. Assume the claim for $n$. Line L7 sets $r' = r + M$ and $q' = q + \lfloor r'/L \rfloor$, and line L8 sets $r'' = r' \bmod L$. Then $q'L + r'' = qL + L\lfloor r'/L \rfloor + (r' \bmod L) = qL + r' = qL + r + M = (n + 1)M$, and $0 \le r'' < L$. $\square$

**Theorem 2.** For each $n$ with $0 \le n \le n_{\max}$, line L6 sets $y[n] = y^{*}[n]$.

*Proof.* Fix $n$ and let $nM = qL + r$ as in Lemma 1. In the sum for $y^{*}[n]$, the term of index $k$ is $h[k]\, u[nM - k]$. If $nM - k$ is not a multiple of $L$, then $u[nM - k] = 0$ and the term is zero. If $nM - k = sL$, then $k = nM - sL = (q - s)L + r$, so $k \equiv r \pmod L$. Write $i = q - s$, so $k = iL + r$. Since $0 \le r < L$, $k \ge 0$ holds exactly when $i \ge 0$, and then $h[k] = e_r[i]$ and $u[nM - k] = u[(q - i)L] = x[q - i]$. Every $k$ with $k \equiv r \pmod L$ and $k \ge 0$ arises from exactly one $i \ge 0$. So

$$y^{*}[n] = \sum_{i \ge 0} e_r[i]\, x[q - i].$$

Here $e_r[i] = 0$ for $iL + r \ge K$, and $x[q - i] = 0$ unless $0 \le q - i < N$. Lines L4 and L5 add $e_r[i]\, x[q - i]$ for exactly the taps $i$ of $e_r$ with $0 \le q - i < N$, so they add all the nonzero terms, and line L6 stores the sum. $\square$

**Theorem 3 (the number of outputs).** The loop of line L3 produces the same number of samples as the three-stage form, which keeps the samples $nM$ of the full convolution $h * u$, of length $K + LN - 1$.

*Proof.* The full convolution has indices $0, \ldots, K + LN - 2$. The kept indices $nM$ with $nM \le K + LN - 2$ are $n = 0, \ldots, \lfloor (K + LN - 2)/M \rfloor = n_{\max}$, which is the range of line L3. $\square$

**Corollary 4 (special cases).** For $M = 1$ the algorithm is the polyphase interpolator: $q = \lfloor n/L \rfloor$ and $r = n \bmod L$. For $L = 1$, there is one phase $e_0 = h$, $r = 0$ and $q = nM$, so $y[n] = \sum_i h[i]\, x[nM - i]$, the filter output at the times $nM$.

*Proof.* For $M = 1$, Lemma 1 gives $n = qL + r$ with $0 \le r < L$. For $L = 1$, it gives $nM = q$ and $r = 0$, and $e_0[i] = h[i]$. Theorem 2 gives the formulas. $\square$

**Cost.** Each output uses the taps of one phase, and the phase $e_r$ has $\lceil (K - r)/L \rceil \le \lceil K/L \rceil$ taps. So each output costs at most $\lceil K/L \rceil$ multiplies, against $K$ per high-rate sample and $KM$ per kept output for the three-stage form. $\blacksquare$
