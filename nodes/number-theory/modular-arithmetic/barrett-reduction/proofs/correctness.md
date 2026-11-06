---
title: Barrett reduction returns x mod n after at most two corrections
proves: [correctness]
status: full
---

**Claim.** Let $n \ge 1$ have $k$ binary digits, so $2^{k-1} \le n < 2^k$, and let $\mu = \lfloor 4^k / n \rfloor$ (lines L1 and L2). For every integer $x$ with $0 \le x < 4^k$, let $Q = \lfloor x/n \rfloor$ and $R = x - Qn$, so $0 \le R < n$. Then the estimate $q$ of line L3 satisfies $Q - 2 \le q \le Q$, the loop of line L5 subtracts $n$ exactly $Q - q \le 2$ times, and line L6 returns $R = x \bmod n$.

**Notation.** Let $a = x / 2^{k-1}$ and $b = 4^k / n$, two non-negative rationals, and let $x_1 = \lfloor a \rfloor$, so that line L3 computes $q = \lfloor x_1 \mu / 2^{k+1} \rfloor$ with $\mu = \lfloor b \rfloor$. Then
$$\frac{ab}{2^{k+1}} = \frac{x \cdot 4^k}{2^{k-1} \cdot n \cdot 2^{k+1}} = \frac{x}{n}.$$

**Bounds on the factors.** Since $x < 4^k$, $a < 2^{2k}/2^{k-1} = 2^{k+1}$. Since $n \ge 2^{k-1}$, $\mu \le b \le 2^{2k}/2^{k-1} = 2^{k+1}$. Also $0 \le a - x_1 < 1$ and $0 \le b - \mu < 1$.

**Upper bound.** $x_1 \le a$ and $\mu \le b$, with all four numbers non-negative, so $x_1 \mu \le ab$ and $x_1\mu / 2^{k+1} \le x/n$. Taking floors, $q \le \lfloor x/n \rfloor = Q$.

**Lower bound.** Write
$$ab - x_1 \mu = a(b - \mu) + \mu(a - x_1).$$
The first term is at most $a < 2^{k+1}$, because $0 \le b - \mu < 1$ and $a \ge 0$. The second term is less than $\mu \le 2^{k+1}$ when $\mu > 0$, because $0 \le a - x_1 < 1$, and it is $0$ when $\mu = 0$. If $x = 0$, then $q = 0 = Q$ and there is nothing to prove; otherwise $a > 0$ and the first term is less than $a$. In all cases $ab - x_1\mu < 2^{k+1} + 2^{k+1} = 2^{k+2}$. Dividing by $2^{k+1}$,
$$\frac{x_1 \mu}{2^{k+1}} > \frac{x}{n} - 2 \ge Q - 2.$$
The integer $Q - 2$ is strictly less than $x_1\mu / 2^{k+1}$, so it is at most the floor of this number: $Q - 2 \le q$.

**The corrections.** Line L4 sets $r = x - qn = (Q - q)n + R$. By the two bounds, $Q - q \in \{0, 1, 2\}$, so $0 \le r < 3n$ and $r \equiv x \pmod n$. Each pass of the loop in line L5 keeps $r \equiv x \pmod n$ and lowers $r$ by $n$; the loop stops at the first value below $n$. Starting from $(Q - q)n + R$ with $0 \le R < n$, it makes exactly $Q - q \le 2$ passes and ends with $r = R$. Line L6 returns $R = x \bmod n$.

**Products of residues.** For $0 \le a', b' < n$, the product satisfies $a'b' \le (n - 1)^2 < 4^k$, so line L7 is within the range of the claim and returns $a'b' \bmod n$. $\blacksquare$
