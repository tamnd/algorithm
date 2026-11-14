---
title: LTS is least squares on the best h-subset, and the C-step never increases the trimmed objective
proves: [correctness]
status: full
---

**Setting.** The data are rows $x_1, \ldots, x_n \in \mathbb{R}^p$ of the design $X$ and responses $y_1, \ldots, y_n$, in the notation $y = X b + e$. For a coefficient vector $b$, $r_i(b) = y_i - x_i^\top b$, and the squared residuals sorted are $r^2_{(1)}(b) \le \cdots \le r^2_{(n)}(b)$. For $1 \le h \le n$ the LTS objective is
$$Q(b) = \sum_{k=1}^{h} r^2_{(k)}(b),$$
and for a set $H$ of rows, $\mathrm{RSS}_H(b) = \sum_{i \in H} r_i(b)^2$.

## Part 1. LTS as a search over subsets

**Lemma 1.** For every $b$, $Q(b) = \min_{|H| = h} \mathrm{RSS}_H(b)$, and the minimum is attained by the $h$ rows with the smallest squared residuals.

*Proof.* Any $h$ of the numbers $r_i(b)^2$ sum to at least the sum of the $h$ smallest, and the $h$ smallest attain it. $\square$

**Theorem 2.** $\min_b Q(b) = \min_{|H| = h} \min_b \mathrm{RSS}_H(b)$. If $H^*$ attains the outer minimum, the least squares fit on $H^*$ is an LTS fit.

*Proof.* By Lemma 1, $\min_b Q(b) = \min_b \min_H \mathrm{RSS}_H(b)$, and two minima can be swapped. For a fixed $H$, the inner minimum over $b$ is the least squares fit on the rows of $H$. If $b^*$ is that fit for $H^*$, then $Q(b^*) \le \mathrm{RSS}_{H^*}(b^*) = \min_b Q(b)$. $\square$

So the enumeration over all $\binom nh$ subsets in the test file returns the exact LTS fit, when every subset has a full-rank design. When a subset is rank deficient, its least squares fit is not unique, but its minimum value is still well defined; the code skips such subsets, which is safe when the data have distinct design rows in the needed sense, as in the tests.

## Part 2. The concentration step

The C-step of lines L8 and L9 takes $b$, lets $H$ be the $h$ rows with the smallest $r_i(b)^2$, and returns the least squares fit $b'$ on $H$.

**Theorem 3 (Rousseeuw and Van Driessen).** $Q(b') \le Q(b)$, with equality only if $b$ is itself a least squares fit on $H$ (when the fit on $H$ is unique, only if $b' = b$).

*Proof.* By Lemma 1, $Q(b') \le \mathrm{RSS}_H(b')$. Since $b'$ minimizes $\mathrm{RSS}_H$, $\mathrm{RSS}_H(b') \le \mathrm{RSS}_H(b)$. And $\mathrm{RSS}_H(b) = Q(b)$ by the choice of $H$. So
$$Q(b') \le \mathrm{RSS}_H(b') \le \mathrm{RSS}_H(b) = Q(b).$$
If $Q(b') = Q(b)$, the middle inequality is an equality, so $b$ also minimizes $\mathrm{RSS}_H$. $\square$

**Corollary 4 (termination).** The loop of lines L3 to L5 stops after at most $\binom nh$ C-steps.

*Proof.* Let $b_1, b_2, \ldots$ be the fits made by the C-steps, and $H_1, H_2, \ldots$ the subsets they were fitted on. Line L9 computes the fit from the subset alone, so $H_i = H_j$ gives $b_i = b_j$. While the loop runs, $Q(b_1) > Q(b_2) > \cdots$ strictly, so the fits are all different, and so are the subsets. There are $\binom nh$ subsets. $\square$

In practice the loop stops after a few steps. When it stops, $b$ is a fixed point in value: the $h$ rows it fits best are a subset on which it is a least squares fit. Theorem 2 shows that the global minimizer is such a fixed point, but there can be other fixed points. The example on the page has one, which is why FAST-LTS uses many random starts and returns the best of them. FAST-LTS is therefore a heuristic: the value it returns is an upper bound on $\min_b Q$, and it is exact when one of its starts lies in the basin of the global minimum.

## Part 3. Cost

A C-step computes $n$ residuals in $O(np)$ time, selects the $h$ smallest in $O(n)$ expected time (or $O(n \log n)$ by sorting, as in the code), and solves the normal equations in $O(np^2 + p^3)$ time. With $S$ starts and at most $c$ steps each, FAST-LTS takes $O(S c (n p^2 + p^3 + n \log n))$ time.

## What is cited, not proved

The breakdown point $(n - h + 1)/n$ for data in general position, which is $(\lfloor (n - p)/2 \rfloor + 1)/n$ for $h = \lfloor (n + p + 1)/2 \rfloor$ (Rousseeuw and Leroy 1987), and the $\sqrt n$ rate with asymptotic normality (Víšek 2006) are cited on the page. They are not proved here.
