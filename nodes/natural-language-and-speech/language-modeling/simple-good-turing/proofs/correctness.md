---
title: Simple Good-Turing gives a proper distribution, switches once, and discounts every count when the slope is below -1
proves: [correctness]
status: full
---

We write $c(x) \ge 1$ for the count of a seen type $x$, $N = \sum_x c(x)$, $N_r$ for the number of seen types with $c(x) = r$, and $r_1 < r_2 < \cdots < r_m$ for the counts with $N_r > 0$. We assume $m \ge 2$, which the implementation requires.

**Lemma 1 (the fit is defined).** The least squares line of line L4 exists and is unique.

*Proof.* Each $Z_{r_j} > 0$: we have $N_{r_j} \ge 1$ and $r_{j+1} - r_{j-1} > 0$, since $r_0 = 0 < r_1$, the $r_j$ increase, and $r_{m+1} = 2 r_m - r_{m-1} > r_m$ because $r_m > r_{m-1}$. So every $\log Z_{r_j}$ is defined. The points $\log r_1 < \cdots < \log r_m$ are distinct and $m \ge 2$, so $\sum_j (\log r_j - \overline{\log r})^2 > 0$, and the normal equations have the single solution $b = \sum_j (\log r_j - \overline{\log r})(\log Z_{r_j} - \overline{\log Z}) / \sum_j (\log r_j - \overline{\log r})^2$, $a = \overline{\log Z} - b \, \overline{\log r}$. $\square$

**Lemma 2 (one switch).** There is an index $s$ with $1 \le s \le m$ such that line L10 sets $r^* = x_{r_j} = (r_j + 1) N_{r_j + 1} / N_{r_j}$ for $j < s$ and $r^* = y_{r_j}$ for $j \ge s$. For every $j < s$, $N_{r_j + 1} > 0$.

*Proof.* The flag *smoothed* starts false in line L6. Line L9 can set it to true and nothing sets it back. Let $s$ be the first index at which line L9 sets it, if any. For $j < s$ the flag is false at line L10, and for $j \ge s$ it is true, which gives the two cases. For $j < s$, the test of line L9 failed, so $N_{r_j + 1} \ne 0$, and $x_{r_j}$ is defined and positive. The index $s$ exists: if the flag is still false at $j = m$, then $N_{r_m + 1} = 0$ because $r_m$ is the largest count, so line L9 sets it at $j = m$. $\square$

**Theorem 3 (a proper distribution).** The output satisfies $0 \le P_0 \le 1$, $p(x) > 0$ for every seen type when $P_0 < 1$, and $P_0 + \sum_x p(x) = 1$.

*Proof.* $P_0 = N_1 / N \in [0, 1]$. By Lemma 2 every $r^*$ is either a positive $x_r$ or $y_r = (r+1) S(r+1) / S(r)$, a ratio of two values of the exponential function, which is positive. So $N' = \sum_r N_r r^* > 0$ in line L11 and $p(x) = (1 - P_0) r^*_{c(x)} / N' > 0$ when $P_0 < 1$. Grouping the types by count, $\sum_x p(x) = (1 - P_0) \sum_r N_r r^* / N' = 1 - P_0$. $\square$

**Theorem 4 (the smoothed counts).** For every $r > 0$, $y_r = r (1 + 1/r)^{b+1}$. If $b < -1$, then with $c = -(b+1) > 0$:

1. $y_r < r$;
2. $y_r$ is strictly increasing in $r$;
3. $r - y_r \to c$ as $r \to \infty$, and $r - y_r < c$ for every $r$.

*Proof.* $S(r) = e^{a} r^{b}$, so $y_r = (r+1) \bigl((r+1)/r\bigr)^b = r \bigl((r+1)/r\bigr)^{b+1} = r (1 + 1/r)^{b+1}$.

(1) $1 + 1/r > 1$ and $b + 1 < 0$, so $(1 + 1/r)^{b+1} < 1$.

(2) $\log y_r = \log r - c \log(1 + 1/r)$. Its derivative in $r$ is $1/r + c / (r(r+1)) > 0$.

(3) Let $u = 1/r$. Then $r - y_r = \bigl(1 - (1+u)^{-c}\bigr)/u$. The function $g(u) = 1 - (1+u)^{-c}$ is concave on $u > 0$ with $g(0) = 0$ and $g'(0) = c$, so $g(u) < c u$ for $u > 0$, which gives $r - y_r < c$. As $u \to 0$, $g(u)/u \to g'(0) = c$. $\blacksquare$

So when the fitted slope is below $-1$, every count from the switch on is discounted, the order of the counts is kept, and the discount grows toward the constant $-(b+1)$. Below the switch the Turing estimates are used, and the method makes no claim about their order. If $b \ge -1$, statement (1) fails, which is why the method assumes $b < -1$.
