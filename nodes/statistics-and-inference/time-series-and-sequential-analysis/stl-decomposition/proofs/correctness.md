---
title: STL's components add up, the map is linear without robustness, and a line plus a zero-sum periodic season is decomposed exactly
proves: [correctness, termination]
status: full
---

STL is defined by its steps, so we prove the properties that pin down what it computes. Lemma 1: LOESS of degree 1 reproduces a line at every position, inside or outside the data. Lemma 2: the moving averages of line L5 map a line plus a zero-sum season to the line, at the right times. Theorem 3: a line plus a zero-sum periodic season is split exactly. Proposition 4: the components add up, the map is linear without robustness passes, and the robust map is scale equivariant. Lemma 5: the robustness weights. We do not prove any statistical property, such as the bias, the variance or the frequency response of the filters (Cleveland et al. 1990, Section 5 onward, study these by computation). Throughout, spans are odd integers $q \ge 3$ and $m \ge 2$.

**Lemma 1 (LOESS reproduces lines).** Let $y_i = a + bi$ for $i = 1..N$, let $x$ be any real number, let $q \ge 3$, and let the robustness weights be positive. Then the LOESS value at $x$ is $a + bx$.

*Proof.* Let $P$ be the set of window positions with positive weight $w_i$. If $P$ has two or more points, the weighted least squares line through $(i, y_i)$, $i \in P$, is unique because the positions are distinct, so $\sum_P w_i(i - \bar x)^2 > 0$. The line $a + bi$ fits these points with zero residuals, so it is the minimizer, and its value at $x$ is $a + bx$. In the code, $\bar y = a + b\bar x$ and $S_{xy}/S_{xx} = b$, so $\bar y + (S_{xy}/S_{xx})(x - \bar x) = a + bx$.

Now suppose $P$ has one point. With positive robustness weights, position $i$ has positive weight exactly when $|i - x| < \lambda_q(x)$. If $q > N$, then $\lambda_q(x) = (q/N)\max_i|i - x| > \max_i|i - x|$, so all $N \ge 2$ points are in $P$. Otherwise the window is the $q \ge 3$ consecutive positions nearest $x$, and $\lambda_q(x)$ is the distance to the farther end. Every position strictly between the two ends is closer than that end, so at least $q - 2 \ge 1$ interior positions are in $P$, and so is the nearer end unless both ends are at distance $\lambda_q(x)$. So $P$ has one point only when $q = 3$ and $x$ is the middle position, and then the code returns $y_x = a + bx$. $\square$

A constant is a line with $b = 0$, so a LOESS of a constant sequence returns the constant at every position. The fit is a weighted average of the $y_i$ with weights that depend only on the positions, $x$ and the robustness weights, so for fixed robustness weights it is linear in $y$.

**Lemma 2 (the low-pass filter).** Let $c_t = a + bt + \sigma_t$ for $t = 1 - m..n + m$, where $\sigma_{t + m} = \sigma_t$ and $\sum_{j=1}^m\sigma_j = 0$. Then $\mathrm{MA}_3(\mathrm{MA}_m(\mathrm{MA}_m(c)))$ has $n$ terms, and its $t$-th term is $a + bt$.

*Proof.* A moving average of length $k$ maps a sequence of length $\ell$ to one of length $\ell - k + 1$, so the lengths are $n + 2m \to n + m + 1 \to n + 2 \to n$. The mean of a line over $k$ consecutive times is the line at the mean time, which is the first time plus $(k - 1)/2$. The mean of $\sigma$ over $m$ consecutive times is $\frac{1}{m}\sum_{j=1}^m\sigma_j = 0$, because any $m$ consecutive times hit each residue class once. So the first average is the line, with its first term at time $1 - m + (m - 1)/2$, and has no seasonal part left. The next two averages keep a line a line. The first term of the result sits at time $1 - m + (m - 1)/2 + (m - 1)/2 + 1 = 1$, and the terms are at consecutive times, so the $t$-th term is $a + bt$. $\square$

**Theorem 3 (exact recovery).** Let $Y_t = a + bt + \sigma_t$ for $t = 1..n$, with $\sigma$ periodic of period $m$ and summing to 0 over a period, and $n \ge 2m$. Then for any spans, any $n_i \ge 1$ and any $n_o \ge 0$, STL returns $S_t = \sigma_t$, $T_t = a + bt$ and $R_t = 0$.

*Proof.* We show that one inner pass (lines L3 to L8) started from any linear trend $T_t = a' + b't$ (including $T = 0$ of line L1), with all robustness weights equal to 1, returns $S = \sigma$ and $T_t = a + bt$. Line L3 gives $D_t = (a - a') + (b - b')t + \sigma_t$. On the cycle-subseries $j$, the $k$-th value ($k = 1, 2, \dots$) is at time $t = j + (k - 1)m$, so it equals $(a - a') + (b - b')(j + (k - 1)m) + \sigma_j$, a line in $k$. By Lemma 1, line L4 returns the same line at $k = 0..N_j + 1$, so $C_t = (a - a') + (b - b')t + \sigma_t$ for all $t = 1 - m..n + m$ (each time in this range is in exactly one subseries at exactly one of these positions). By Lemma 2 the moving averages give the line $(a - a') + (b - b')t$ on $t = 1..n$, and by Lemma 1 the LOESS of line L5 leaves it unchanged. Line L6 gives $S_t = C_t - L_t = \sigma_t$. Line L7 gives $H_t = a + bt$, and by Lemma 1 line L8 gives $T_t = a + bt$.

By induction over the inner passes, every pass starts from a linear trend and ends with $S = \sigma$ and $T = a + bt$. Line L9 then gives $R = 0$. If $n_o > 0$, line L10 sees $R = 0$; then $h = 0$ and the implementation sets every weight to 1, so the next outer pass repeats the same computation. $\square$

**Proposition 4 (additivity, linearity, equivariance).** (a) $S_t + T_t + R_t = Y_t$ for all $t$. (b) With $n_o = 0$, the map $Y \mapsto (S, T, R)$ is linear. (c) For any $n_o$ and any $c \neq 0$, STL applied to $cY$ returns $(cS, cT, cR)$ and the same weights.

*Proof.* (a) is line L9. (b) Every line of the inner loop is a subtraction, a LOESS with weights that depend only on positions (Lemma 1, last remark), a moving average, or a restriction to times $1..n$; each is linear, and so is their composition, starting from the linear $T = 0$. Line L9 is linear. (c) By induction over the steps: if every input to a step is multiplied by $c$ and the robustness weights are the same, every LOESS, moving average and difference is multiplied by $c$. So $R$ is multiplied by $c$, the median of $|R|$ by $|c|$, and $|cR_t|/(6\,\mathrm{median}|cR|) = |R_t|/(6\,\mathrm{median}|R|)$, so line L10 gives the same weights. $\square$

**Lemma 5 (robustness weights).** The weights of line L10 satisfy $0 \le \rho_t \le 1$, $\rho_t = 1$ exactly when $R_t = 0$ (if $h > 0$), $\rho_t$ decreases in $|R_t|$, and $\rho_t = 0$ exactly when $|R_t| \ge 6\,\mathrm{median}|R|$.

*Proof.* For $0 \le u < 1$, $B(u) = (1 - u^2)^2 \in (0, 1]$, with $B(0) = 1$, and $B$ is strictly decreasing there because $1 - u^2$ is decreasing and positive. For $u \ge 1$, $B(u) = 0$. Apply this with $u = |R_t|/h$. $\square$

So a point whose remainder is at least six times the typical size has no influence on the next pass, and the outer loop is an iteratively reweighted fit in the sense of Cleveland (1979). Whether the weights converge is not proved; the method runs a fixed number of passes.

**Exact arithmetic.** Every step uses additions, multiplications, divisions, comparisons and a median, and the tricube and bisquare functions are polynomials. With rational data the outputs are rational, and the implementation computes them exactly when given Fractions. The tests check Lemma 1 against a direct rational computation at positions $0..N + 1$, Lemma 2, Theorem 3 for two spans with and without robustness passes, Proposition 4(a), and Lemma 5.

**Termination.** The outer loop runs $n_o + 1$ times and the inner loop $n_i$ times per outer pass. Each inner pass computes a fixed number of LOESS values, each from at most $\max(q, N)$ points, and three moving averages, and line L10 sorts $n$ numbers. So STL stops after finitely many operations, $\Theta(n_i(n_o + 1)n(n_s + n_t + n_l) + n_on\log n)$ as counted on the main page.
