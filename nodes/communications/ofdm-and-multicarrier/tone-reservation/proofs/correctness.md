---
title: Tone reservation leaves the data subcarriers unchanged, puts the whole correction on the reserved set, and clips each selected peak exactly to the threshold
proves: [correctness]
status: full
---

Let $N$ be the number of subcarriers, $L$ the oversampling factor and $R \subset \{0, \ldots, N-1\}$ the reserved set, with $X[k] = 0$ for $k \in R$. The subcarrier $k$ has the integer frequency $f_k = k$ for $k < N/2$ and $f_k = k - N$ for $k \ge N/2$. Write $T$ for the map of line L1 from $N$ subcarrier values to the oversampled symbol, $T(Y) = \sqrt L\, F_{LN}^H Z(Y)$, where $Z(Y)$ puts $(L - 1)N$ zeros in the middle of $Y$. Written out,

$$T(Y)[t] = \frac{1}{\sqrt N} \sum_{k=0}^{N-1} Y[k]\, e^{j 2\pi f_k t / (LN)}, \qquad t = 0, \ldots, LN - 1.$$

Say that a vector $Y \in \mathbb{C}^N$ is *on $R$* if $Y[k] = 0$ for every $k \notin R$. We work in exact arithmetic, and all indices of time samples are taken modulo $LN$.

**Lemma 1 (the kernel).** The kernel of line L2 is $p = (\sqrt N / |R|)\, T(1_R)$, where $1_R$ is the indicator of $R$. It satisfies

$$p[t] = \frac{1}{|R|} \sum_{k \in R} e^{j 2\pi f_k t/(LN)}, \qquad p[0] = 1, \qquad |p[t]| \le 1 \text{ for every } t.$$

*Proof.* Put $Y = 1_R$ in the formula for $T$ and multiply by $\sqrt N / |R|$. At $t = 0$ every term is 1, so $p[0] = |R|/|R| = 1$. For every $t$ the sum has $|R|$ terms of magnitude 1, so the triangle inequality gives $|p[t]| \le 1$. $\square$

**Lemma 2 (a shift stays on $R$).** For every integer $m$, the shifted kernel $s_m[t] = p[t - m]$ is $T(D_m)$ with

$$D_m[k] = \frac{\sqrt N}{|R|}\, e^{-j 2\pi f_k m/(LN)} \text{ for } k \in R, \qquad D_m[k] = 0 \text{ for } k \notin R.$$

So $D_m$ is on $R$.

*Proof.* Each $f_k$ is an integer, so $e^{j 2\pi f_k (t - m)/(LN)}$ does not change when $t - m$ changes by a multiple of $LN$. The circular shift is therefore well defined, and

$$p[t - m] = \frac{1}{|R|} \sum_{k \in R} e^{-j 2\pi f_k m/(LN)}\, e^{j 2\pi f_k t/(LN)} = \frac{1}{\sqrt N} \sum_{k} D_m[k]\, e^{j 2\pi f_k t/(LN)} = T(D_m)[t].$$

A delay in time is a modulation in frequency, and a modulation changes only the phase of each subcarrier. $\square$

**Lemma 3 (invariant).** At the start of every pass through line L4, there is a vector $C$ on $R$ with $c = T(C)$.

*Proof.* By induction on the number of passes. Line L3 sets $c = 0 = T(0)$, and $0$ is on $R$. Suppose $c = T(C)$ with $C$ on $R$, and the pass reaches line L8 with the index $m$ and the factor $\alpha$. Line L8 replaces $c$ by $c - \alpha s_m$. By Lemma 2 and the linearity of $T$, this equals $T(C - \alpha D_m)$, and $C - \alpha D_m$ is on $R$ because both $C$ and $D_m$ are on $R$. $\square$

**Lemma 4 (one step).** Suppose a pass reaches line L7, so the largest sample $v = x[m] + c[m]$ has $|v| > a$. After line L8, the sample $m$ of $x + c$ equals $a\, v/|v|$: it has magnitude exactly $a$ and the phase of $v$.

*Proof.* Line L7 sets $\alpha = v(1 - a/|v|)$. Line L8 changes the sample $m$ by $-\alpha\, p[0] = -\alpha$ by Lemma 1. So the new sample is $v - v(1 - a/|v|) = a\, v/|v|$. $\square$

The other samples change by $-\alpha\, p[t - m]$, and $|\alpha\, p[t - m]| \le |v| - a$ by Lemma 1. A sample can therefore grow, so the peak need not fall at every step. This is why line L5 searches for the largest sample again on each pass.

**Theorem.** Let $y$ and $\hat C$ be the outputs of line L9. Then:

1. $y = T(X + C)$ for a vector $C$ on $R$, and $\hat C = C$;
2. the data subcarriers are unchanged: the in-band values of $y$ equal $X[k]$ for every $k \notin R$;
3. if the loop ends at line L6, then $|y[t]| \le a$ for every $t$; otherwise the loop ends after the given number of passes, and each pass clipped its selected sample exactly to $a$;
4. the energy of $y$ is $L\,(\lVert X \rVert^2 + \lVert C \rVert^2)$, so the correction adds the mean power $\lVert C \rVert^2 / N$ and nothing else.

*Proof.* By Lemma 3, at line L9 the correction is $c = T(C)$ with $C$ on $R$, and $x = T(X)$ by line L1, so $y = x + c = T(X + C)$ by linearity. The map that keeps the $N$ in-band values of $F_{LN}\, y$ and divides by $\sqrt L$ is a left inverse of $T$, because $F_{LN}$ is unitary and $Z$ only places values. Applied to $c$ it returns $C$, which is item 1. For $k \notin R$, $C[k] = 0$, so the in-band value of $y$ at $k$ is $X[k]$, which is item 2. Line L6 ends the loop only when the largest magnitude is at most $a$, and the other exit is the end of the counted loop; Lemma 4 gives the rest of item 3. For item 4, $\lVert T(Y) \rVert^2 = L\, \lVert Z(Y) \rVert^2 = L\, \lVert Y \rVert^2$ because $F_{LN}^H$ is unitary. $X$ and $C$ have disjoint supports, so $\lVert X + C \rVert^2 = \lVert X \rVert^2 + \lVert C \rVert^2$. $\square$

**The receiver.** After the cyclic prefix is removed and the channel $H$ is equalized, the receiver sees $X[k] + C[k]$ plus noise on each subcarrier $k$. On the data subcarriers this is $X[k]$ plus noise, exactly as without tone reservation, so the receiver ignores $R$ and needs no side information.

**What is not claimed.** The best correction solves the problem of minimizing $\max_t |x[t] + T(C)[t]|$ over the vectors $C$ on $R$. It is a convex problem, because each $|x[t] + T(C)[t]|$ is a convex function of $C$ and a maximum of convex functions is convex. It can be written as a second-order cone program. The greedy loop of lines L4 to L8 gives a valid correction for any number of passes, by the theorem, but it does not in general reach the minimum of that problem.
