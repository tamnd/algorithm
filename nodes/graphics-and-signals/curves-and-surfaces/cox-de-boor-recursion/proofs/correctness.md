---
title: BASIS-FUNCTIONS returns the p + 1 nonzero B-spline values on a span
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The knot vector is $t_0 \le \cdots \le t_{n+p+1}$, the B-splines $N_{i,r}$ are defined by the recursion with the rule that a term $\omega_{j,r} N_{j,r-1}$ or $(1 - \omega_{j,r}) N_{j,r-1}$ is $0$ when $t_{j+r} = t_j$, and $\omega_{j,r}(u) = (u - t_j)/(t_{j+r} - t_j)$ otherwise.

**Claim.** Let $p \le \mu \le n$ with $t_\mu < t_{\mu+1}$, and let $t_\mu \le u < t_{\mu+1}$. Then BASIS-FUNCTIONS$(t, p, \mu, u)$ returns $N[s] = N_{\mu-p+s,p}(u)$ for $s = 0, \ldots, p$, and $N_{i,p}(u) = 0$ for every other $i$. With $u = t_{\mu+1}$ it returns the limits $\lim_{v \to u^-} N_{\mu-p+s,p}(v)$.

**Lemma 1 (the rule is consistent).** If $t_{j+r} = t_j$, then $N_{j,r-1}$ is the zero function. So the value given to the weight does not change the product.

*Proof.* This follows from Lemma 2 with $r - 1$ in place of $r$: $N_{j,r-1}(u) \ne 0$ needs $t_j \le u < t_{j+r}$, and this interval is empty. $\square$

**Lemma 2 (support).** For all $r \ge 0$, all $i$ and all $u$: if $N_{i,r}(u) \ne 0$, then $t_i \le u < t_{i+r+1}$.

*Proof.* By [induction](/induction/) on $r$. For $r = 0$ it is the definition. For $r \ge 1$, $N_{i,r}(u)$ is a sum of a multiple of $N_{i,r-1}(u)$ and a multiple of $N_{i+1,r-1}(u)$. If it is nonzero, one of the two is nonzero. By the induction hypothesis, $t_i \le u < t_{i+r}$ or $t_{i+1} \le u < t_{i+r+1}$. In both cases $t_i \le u < t_{i+r+1}$, because the knots do not decrease. $\square$

By Lemma 2, for $u \in [t_\mu, t_{\mu+1})$ a nonzero $N_{i,r}(u)$ needs $t_i \le u$, so $i \le \mu$ (the knots after $\mu$ are at least $t_{\mu+1} > u$), and $u < t_{i+r+1}$, so $i + r + 1 \ge \mu + 1$, that is $i \ge \mu - r$. So only $N_{\mu-r,r}, \ldots, N_{\mu,r}$ can be nonzero at $u$. This proves the second part of the claim for $r = p$.

**Invariant.** After line L1, and after line L8 in pass $r$, the array $N$ has $r + 1$ entries, with

$$N[s] = N_{\mu-r+s,r}(u), \qquad s = 0, \ldots, r,$$

where $r = 0$ after line L1.

*Initialization.* After line L1, $N[0] = 1 = N_{\mu,0}(u)$, because $t_\mu \le u < t_{\mu+1}$.

*Maintenance.* Assume the invariant for $r - 1$, with $1 \le r \le p$. Line L3 sets $M$ to $r + 1$ zeros. Fix $s$ with $0 \le s \le r - 1$ and let $j = \mu - r + 1 + s$, so $N[s] = N_{j,r-1}(u)$ by the hypothesis. Line L5 divides by $t_{j+r} - t_j$. We have $j \le \mu$ and $j + r = \mu + 1 + s \ge \mu + 1$, so $t_{j+r} - t_j \ge t_{\mu+1} - t_\mu > 0$. So the division is defined and $a = \omega_{j,r}(u)$.

Now take $i = \mu - r + q$ with $0 \le q \le r$. By the recursion,

$$N_{i,r}(u) = \omega_{i,r}(u) N_{i,r-1}(u) + \bigl(1 - \omega_{i+1,r}(u)\bigr) N_{i+1,r-1}(u).$$

- For $q = 0$, $i = \mu - r$, and $N_{\mu-r,r-1}(u) = 0$ by the remark after Lemma 2 (applied with $r - 1$). The first term is $0$, whatever its weight, by Lemma 1 if the weight is $0/0$. The second term is $(1 - \omega_{j,r}) N[0]$ with $j = \mu - r + 1$, that is $s = 0$. Line L6 with $s = 0$ adds exactly this to $M[0]$, and no other line adds to $M[0]$.
- For $q = r$, $i = \mu$, and $N_{\mu+1,r-1}(u) = 0$ in the same way. The first term is $\omega_{\mu,r} N[r-1]$, and line L7 with $s = r - 1$ adds exactly this to $M[r]$. No other line adds to $M[r]$.
- For $1 \le q \le r - 1$, the first term is $\omega_{i,r} N_{i,r-1}(u)$ with $i = \mu - r + 1 + (q - 1)$, that is $s = q - 1$, and line L7 for $s = q - 1$ adds it to $M[q]$. The second term is $(1 - \omega_{i+1,r}) N_{i+1,r-1}(u)$ with $s = q$, and line L6 for $s = q$ adds it to $M[q]$. No other step adds to $M[q]$.

So after the inner loop, $M[q] = N_{\mu-r+q,r}(u)$ for $q = 0, \ldots, r$, and line L8 makes the invariant true for $r$.

*Termination.* Both loops have fixed bounds, so the algorithm stops after $p$ passes, and line L9 returns $N[s] = N_{\mu-p+s,p}(u)$ for $s = 0, \ldots, p$. This is the first part of the claim.

**The closed end of the span.** For $v \in [t_\mu, t_{\mu+1})$, the computation does the same operations for every $v$, and each weight of line L5 is a polynomial of degree 1 in $v$ with a fixed nonzero denominator. So each output $N[s]$ is a polynomial $q_s(v)$, and $q_s(v) = N_{\mu-p+s,p}(v)$ on the half-open span. A polynomial is continuous, so running the same operations with $v = t_{\mu+1}$ gives $q_s(t_{\mu+1}) = \lim_{v \to t_{\mu+1}^-} N_{\mu-p+s,p}(v)$. This is the last part of the claim.

**Cost.** Pass $r$ runs the inner loop $r$ times, so the number of steps of lines L5 to L7 is $\sum_{r=1}^{p} r = p(p + 1)/2$, and the extra space is the two arrays of at most $p + 1$ entries. $\blacksquare$
