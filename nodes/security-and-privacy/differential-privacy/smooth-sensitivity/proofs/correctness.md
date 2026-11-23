---
title: The smooth sensitivity of the median has a closed form, and noise scaled to it gives differential privacy
proves: [correctness]
status: partial
---

We use the pseudocode of the page. A dataset is a list $x$ of $n$ values in $[0, \Lambda]$, with $n$ odd and $m = (n+1)/2$. We sort it as $x_1 \le \dots \le x_n$ and set $x_i = 0$ for $i \le 0$ and $x_i = \Lambda$ for $i > n$. Two datasets are neighbors if one value is replaced by another, and $d(x, y)$ is the number of replacements that turn $x$ into $y$. The median is $f(x) = x_m$. The local sensitivity is $LS(y) = \max_{y' : d(y, y') = 1} |f(y) - f(y')|$, and the $\beta$-smooth sensitivity is $S^*(x) = \max_y e^{-\beta d(x, y)} LS(y)$ (NRS Definition 2.2).

**Claim 1 (local sensitivity).** $LS(x) = \max(x_m - x_{m-1}, x_{m+1} - x_m)$.

*Proof.* One replacement moves at most one value across the median, so the new median is one of $x_{m-1}, x_m, x_{m+1}$. Replacing a value at or above position $m$ by 0 gives the median $x_{m-1}$, and replacing a value at or below position $m$ by $\Lambda$ gives $x_{m+1}$. $\square$

**Claim 2 (the ball, NRS Proposition 3.4).** Let $A(k, x) = \max_{y : d(x, y) \le k} LS(y)$. Then $A(k, x) = \max_{0 \le t \le k+1} (x_{m+t} - x_{m+t-k-1})$.

*Proof.* Upper bound. Let $d(x, y) \le k$, so $y$ is $x$ with at most $k$ values removed and the same number added. Sort $y$. By Claim 1, $LS(y)$ is $y_{m+1} - y_m$ or $y_m - y_{m-1}$. Take $g = y_{m+1} - y_m > 0$ (if $g = 0$ there is nothing to prove). Let $p = \max\{i \ge 0 : x_i \le y_m\}$ and $q = \min\{i \le n+1 : x_i \ge y_{m+1}\}$, with the padding. The values of $x$ with indices $p+1, \dots, q-1$ lie strictly between $y_m$ and $y_{m+1}$, and $y$ has no value there, so they were all removed: $q - p \le k + 1$. At least $m$ values of $y$ are at most $y_m$, and they are kept values of $x$ with index at most $p$ or added values, so $m \le p + k$. At least $n - m$ values of $y$ are at least $y_{m+1}$, so in the same way $n - m \le (n - q + 1) + k$, that is $q \le m + k + 1$. The ranges $[q - k - 1, p]$ and $[m - k - 1, m]$ then meet, so pick $p'$ in both and set $q' = p' + k + 1 \ge q$. Since $x$ is sorted, $g \le x_q - x_p \le x_{q'} - x_{p'}$, which is the term $t = p' - m + k + 1 \in [0, k+1]$. The case $g = y_m - y_{m-1}$ is the same with $m - 1$ in place of $m$ in the counts, and it gives $p \ge m - k - 1$ and $q \le m + k$, so the ranges meet again.

Lower bound. Fix $t$ with $1 \le t \le k + 1$. The real values with indices from $m + t - k$ to $m + t - 1$ are at most $k$. Replace them: put just enough of them at 0 so that exactly $m$ values of $y$ are at most $x_{m+t-k-1}$, and put the rest at $\Lambda$. Then $y_m = x_{m+t-k-1}$ and $y_{m+1} = x_{m+t}$, with the padding, so $LS(y) \ge x_{m+t} - x_{m+t-k-1}$. For $t = 0$, put the values with indices $m - k$ to $m - 1$ at 0. Then $y_{m-1} \le x_{m-k-1}$ and $y_m = x_m$. The count works in each case because the gap holds at most $k$ real values. The test file checks this formula against the definition on every dataset with $n = 5$ and $\Lambda = 3$. $\square$

**Claim 3 (the closed form).** $S^*(x) = \max_{0 \le k \le n} e^{-k\beta} A(k, x)$, which is lines L1 to L3.

*Proof.* Group the $y$ in the definition by $k = d(x, y)$: $S^*(x) = \max_k e^{-k\beta} \max_{d(x,y) = k} LS(y)$. Since $e^{-k\beta}$ falls with $k$, replacing "$= k$" by "$\le k$" does not change the maximum, which gives $\max_k e^{-k\beta} A(k, x)$. For $k \ge n$, $A(k, x) \le \Lambda = A(n, x)$, so the terms with $k > n$ are not larger than the term $k = n$. The test file checks the result against the definition by brute force on all datasets of the grid $\{0, \dots, \Lambda\}^n$ for $n \le 5$ and $\Lambda \le 4$. $\square$

**Claim 4 (a smooth bound).** $S^*(x) \ge LS(x)$, and $S^*(x) \le e^{\beta} S^*(x')$ for neighbors $x, x'$.

*Proof.* The term $y = x$ gives the first part. For the second, $d(x, y) \le d(x', y) + 1$ by the triangle inequality, so $e^{-\beta d(x, y)} LS(y) \le e^{\beta} e^{-\beta d(x', y)} LS(y)$ for each $y$. $\square$

**Claim 5 (pure DP with Cauchy noise, NRS Lemma 2.3 and Corollary 2.4).** Let $Z$ have the density $h(z) = 1/(\pi(1 + z^2))$, let $\beta = \varepsilon/6$ and let $s(x) = 6 S^*(x)/\varepsilon$. The output $x_m + s(x) Z$ of line L4 is $\varepsilon$-DP.

*Proof.* The output density is $p_x(z) = h((z - f(x))/s(x))/s(x)$. For neighbors, write $\Delta = f(x') - f(x)$ and $\lambda = \ln(s(x')/s(x))$. By Claim 4, $|\Delta| \le LS(x) \le S^*(x)$, so $|\Delta| \le (\varepsilon/6) s(x)$, and $|\lambda| \le \beta = \varepsilon/6$. Go from $p_x$ to $p_{x'}$ in two steps: first move the center from $f(x)$ to $f(x')$ with the scale $s(x)$, then change the scale from $s(x)$ to $s(x')$ with the center $f(x')$.

Shift: $|d \ln h/du| = 2|u|/(1 + u^2) \le 1$, so moving the center by $|\Delta|/s(x) \le \varepsilon/6$ scaled units changes the log density by at most $\varepsilon/6$.

Scaling: with $u$ the distance to the center in units of $s(x)$, the log ratio of the two densities is $\lambda + \ln((1 + u^2 e^{-2\lambda})/(1 + u^2))$. The second term lies between $-2|\lambda|$ and $2|\lambda|$, so the scaling changes the log density by at most $3|\lambda| \le \varepsilon/2$.

The total is at most $\varepsilon/6 + \varepsilon/2 = 2\varepsilon/3 \le \varepsilon$, in both directions. NRS state this with $\gamma = 2$: noise $2(\gamma + 1) S^*/\varepsilon$ needs $\beta \le \varepsilon/(2(\gamma+1))$. The test file checks the log density ratio on a grid of outputs. $\square$

**Claim 6 (approximate DP with Laplace noise, NRS Corollary 2.4).** With $\beta = \varepsilon/(2 \ln(2/\delta))$ and noise $(2 S^*(x)/\varepsilon) \cdot \mathrm{Lap}(1)$, the output is $(\varepsilon, \delta)$-DP.

*Proof sketch.* This is a sketch. The full proof is NRS Lemma 2.3 with the Laplace case of Corollary 2.4, in Section 2 of the paper. The shift costs at most $\varepsilon/2$, because $\mathrm{Lap}(1)$ has a log density with slope at most 1 and the shift is at most $S^*(x)/s(x) = \varepsilon/2$ in scaled units. The scale ratio is $e^{\lambda}$ with $|\lambda| \le \beta$, and the scaling changes the log density at the scaled point $z$ by at most $|\lambda| + |z|(e^{|\lambda|} - 1)$, which is about $\beta(1 + |z|)$. With $\beta = \varepsilon/(2\ln(2/\delta))$ this is at most about $\varepsilon/2$ unless $|z|$ is of order $\ln(2/\delta)$, an event of probability of order $\delta$ under $\mathrm{Lap}(1)$. NRS make the constants exact. The test file checks the hockey-stick divergence at $e^{\varepsilon}$ by numerical integration. $\square$

**Cost.** Sorting takes $O(n \log n)$. Line L2 takes $O(k)$ for each $k$, so lines L1 to L3 take $O(n^2)$ as written. NRS give an $O(n \log n)$ algorithm by a divide-and-conquer search for the best $t$ for each $k$. Line L4 takes $O(1)$.
