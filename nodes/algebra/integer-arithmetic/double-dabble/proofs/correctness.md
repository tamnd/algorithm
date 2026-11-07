---
title: Double dabble produces the decimal digits of its input
proves: [correctness, termination]
status: full
---

Let $x = \sum_{k=0}^{n-1} x_k 2^k$ with $x_k \in \{0, 1\}$, and $d \ge 1$ with $2^n - 1 < 10^d$; the choice $d$ = the number of decimal digits of $2^n - 1$ satisfies this. For $0 \le k \le n$ let

$$X_k = \left\lfloor \frac{x}{2^{n-k}} \right\rfloor = \sum_{m=0}^{k-1} x_{n-1-m} \, 2^{k-1-m},$$

the number formed by the first $k$ bits. Then $X_0 = 0$, $X_{k+1} = 2X_k + x_{n-1-k}$ and $X_n = x$.

**Invariant.** After $k$ passes of the loop of line L2: (I1) $0 \le D[i] \le 9$ for each $i$, and (I2) $\sum_{i=0}^{d-1} D[i]\, 10^i = X_k$.

*Initialization.* Line L1 sets all digits to 0, and $X_0 = 0$.

*Maintenance.* Assume (I1) and (I2) after $k$ passes, and let $D$ be the digits at that moment and $b = x_{n-1-k}$ the next bit. Lines L3 and L4 set $E[i] = D[i] + 3$ if $D[i] \ge 5$ and $E[i] = D[i]$ otherwise; by (I1), $0 \le E[i] \le 12$. Lines L5 to L8 compute, for $i = 0, \ldots, d - 1$, with $c_0 = b$,

$$t_i = 2E[i] + c_i, \qquad D'[i] = t_i \bmod 16, \qquad c_{i+1} = \lfloor t_i / 16 \rfloor .$$

We show by cases that $c_i \in \{0, 1\}$ for each $i$ and that

$$D'[i] + 10\, c_{i+1} = 2D[i] + c_i, \qquad 0 \le D'[i] \le 9 . \tag{$*$}$$

Assume $c_i \in \{0, 1\}$, which holds for $i = 0$.

- If $D[i] \le 4$, then $E[i] = D[i]$ and $t_i = 2D[i] + c_i \le 9 < 16$, so $D'[i] = t_i$ and $c_{i+1} = 0$, and $(*)$ holds.
- If $D[i] \ge 5$, then $E[i] = D[i] + 3$ and $t_i = 2D[i] + c_i + 6$. From $5 \le D[i] \le 9$ we get $16 \le t_i \le 25 < 32$, so $c_{i+1} = 1$ and $D'[i] = t_i - 16 = 2D[i] + c_i - 10$, which lies in $\{0, \ldots, 9\}$ because $10 \le 2D[i] + c_i \le 19$. Then $D'[i] + 10 c_{i+1} = 2D[i] + c_i$, and $(*)$ holds.

In both cases $c_{i+1} \in \{0, 1\}$, so the induction on $i$ goes through. Multiply $(*)$ by $10^i$ and sum over $i = 0, \ldots, d-1$:

$$\sum_{i=0}^{d-1} D'[i]\, 10^i + \sum_{i=0}^{d-1} c_{i+1} 10^{i+1} = 2\sum_{i=0}^{d-1} D[i]\, 10^i + \sum_{i=0}^{d-1} c_i 10^i .$$

The carry terms with $1 \le i \le d - 1$ cancel, which leaves

$$\sum_{i=0}^{d-1} D'[i]\, 10^i + c_d 10^d = 2X_k + b = X_{k+1} .$$

Since $X_{k+1} \le x \le 2^n - 1 < 10^d$ and the sum on the left is nonnegative, $c_d = 0$. So $\sum_i D'[i]\, 10^i = X_{k+1}$, and (I1) holds for $D'$ by $(*)$.

*Termination.* The loop of line L2 runs once for each of the $n$ bits, and the inner loops run $d$ times each, so the algorithm stops after $n$ passes.

**Theorem.** DOUBLE-DABBLE returns digits $D[0], \ldots, D[d-1] \in \{0, \ldots, 9\}$ with $\sum_i D[i]\, 10^i = x$, which are the decimal digits of $x$, padded with zeros to $d$ places.

*Proof.* After $n$ passes, (I1) and (I2) give $\sum_i D[i]\, 10^i = X_n = x$ with digits in $\{0, \ldots, 9\}$. The decimal representation with $d$ digits is unique, so these are the decimal digits of $x$. $\blacksquare$
