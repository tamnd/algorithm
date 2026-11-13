---
title: Burg's reflection coefficients minimize the forward-backward error, lie in the closed unit disk, and give a minimum-phase prediction filter
proves: [correctness]
status: full
---

The notation is that of the page. $x[0], \dots, x[N-1]$ is the record, and the order-$m$ filter is $A_m(z) = \sum_{i=0}^{m} a_m[i] z^{-i}$ with $a_m[0] = 1$. At order $m$ the forward and backward errors are defined for $m \le t \le N-1$.

**Lemma 1 (the errors are filter outputs).** After stage $m$ of the loop of line L2, for every $t$ with $m \le t \le N-1$,

$$f_m[t] = \sum_{i=0}^{m} a_m[i]\, x[t-i], \qquad b_m[t] = \sum_{i=0}^{m} \overline{a_m[i]}\, x[t-m+i].$$

*Proof.* By induction on $m$. For $m = 0$, line L1 sets $f_0 = b_0 = x$ and $a_0 = (1)$. Assume the claim for $m - 1$. Line L6 sets $f_m[t] = f_{m-1}[t] + k_m b_{m-1}[t-1]$. By the hypothesis, $b_{m-1}[t-1] = \sum_i \overline{a_{m-1}[i]}\,x[t-m+i]$; with $j = m - i$ this is $\sum_j \overline{a_{m-1}[m-j]}\,x[t-j]$. So the coefficient of $x[t-j]$ in $f_m[t]$ is $a_{m-1}[j] + k_m\overline{a_{m-1}[m-j]}$, with $a_{m-1}[m] = 0$, which is the update of line L5. In the same way $b_m[t] = b_{m-1}[t-1] + \overline{k_m} f_{m-1}[t]$ has the coefficient $\overline{a_{m-1}[i]} + \overline{k_m}\,a_{m-1}[m-i] = \overline{a_m[i]}$ at $x[t-m+i]$. $\square$

**Lemma 2 (the choice of $k_m$).** Write $F = \sum_{t=m}^{N-1} |f_{m-1}[t]|^2$, $B = \sum_{t=m}^{N-1} |b_{m-1}[t-1]|^2$ and $C = \sum_{t=m}^{N-1} f_{m-1}[t]\,\overline{b_{m-1}[t-1]}$, and assume $F + B > 0$. Then the value $k_m = -2C/(F + B)$ of line L4 is the unique minimizer over $k \in \mathbb{C}$ of

$$J(k) = \sum_{t=m}^{N-1} \left|f_{m-1}[t] + k\, b_{m-1}[t-1]\right|^2 + \left|b_{m-1}[t-1] + \overline{k}\, f_{m-1}[t]\right|^2,$$

the total energy of the order-$m$ forward and backward errors. Moreover $|k_m| \le 1$, with equality only if $f_{m-1}[t] = \lambda\, b_{m-1}[t-1]$ for all $t$ in the range and one constant $\lambda$ with $|\lambda| = 1$.

*Proof.* Expanding both squares, with $f = f_{m-1}[t]$ and $b = b_{m-1}[t-1]$: $|f + kb|^2 = |f|^2 + |k|^2|b|^2 + 2\operatorname{Re}(\overline{k} f \overline{b})$, and $|b + \overline{k}f|^2 = |b|^2 + |k|^2|f|^2 + 2\operatorname{Re}(k \overline{f} b) = |b|^2 + |k|^2|f|^2 + 2\operatorname{Re}(\overline{k} f\overline{b})$. Summing,

$$J(k) = (1 + |k|^2)(F + B) + 4\operatorname{Re}(\overline{k}\, C) = (F + B)\left|k + \frac{2C}{F + B}\right|^2 + (F + B) - \frac{4|C|^2}{F + B}.$$

The first term is zero exactly at $k = -2C/(F+B)$ and positive elsewhere. For the bound, the Cauchy-Schwarz inequality gives $|C| \le \sqrt{FB}$, and $2\sqrt{FB} \le F + B$ by the inequality of the arithmetic and geometric means. So $|k_m| = 2|C|/(F+B) \le 1$. Equality needs equality in both steps: $f = \lambda b$ termwise for one $\lambda$ (Cauchy-Schwarz), and $F = B$, which forces $|\lambda| = 1$. $\square$

When $F + B = 0$ all errors are zero, every $k$ gives $J = 0$, and line L4 takes $k_m = 0$.

**Lemma 3 (minimum phase).** If $|k_j| < 1$ for $j = 1, \dots, m$, then every zero of $A_m(z)$ lies in the open unit disk $|z| < 1$, so the all-pole model $1/A_m(z)$ is causal and stable.

*Proof.* Let $P_m(z) = z^m A_m(z) = \sum_j a_m[j] z^{m-j}$, a monic polynomial of degree $m$ with the same nonzero zeros as $A_m$, and let $P_m^*(z) = \sum_i \overline{a_m[i]}\, z^{i}$ be its reversed conjugate. The update of line L5 reads $P_m(z) = z\,P_{m-1}(z) + k_m P_{m-1}^*(z)$, by splitting $a_m[j]$ into its two terms and putting $i = m - j$ in the second. On the circle $|z| = 1$, $\overline{z} = 1/z$ gives $|P_{m-1}^*(z)| = |z^{m-1}\overline{P_{m-1}(z)}| = |P_{m-1}(z)|$. By induction $P_{m-1}$ has all $m - 1$ zeros inside the disk, so $P_{m-1}(z) \ne 0$ on the circle, and there $|k_m P_{m-1}^*(z)| = |k_m|\,|P_{m-1}(z)| < |z P_{m-1}(z)|$. By Rouché's theorem $P_m$ has as many zeros in the disk as $z P_{m-1}(z)$, that is $m$, which is all of them. The base case $P_0 = 1$ has no zeros. $\square$

**Theorem.** For a record with $F + B > 0$ at every stage, the algorithm returns the coefficients $a_p$ of the filter whose forward and backward errors are given by Lemma 1, with each $k_m$ minimizing the stage energy of Lemma 2 given the earlier stages. All $|k_m| \le 1$, and if all are strictly less than 1, which holds unless the errors at some stage are proportional with a unit-modulus factor, the model $E_p / |A_p(e^{i\omega})|^2$ comes from a stable all-pole filter.

*Proof.* Lemmas 1 to 3, applied at each stage of the loop of line L2. Line L7 updates the error power by $E_m = (1 - |k_m|^2)E_{m-1}$, which is the Levinson relation that holds exactly for the Yule-Walker solution; for Burg it is the conventional estimate of the noise power and stays nonnegative because $|k_m| \le 1$. $\blacksquare$
