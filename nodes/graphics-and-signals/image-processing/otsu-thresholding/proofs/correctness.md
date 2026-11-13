---
title: Otsu's scan returns the smallest threshold of largest between-class variance, which is also the best two-group least squares split
proves: [correctness]
status: full
---

Fix an image with $N \ge 1$ pixels and integer values in $\{0, \ldots, L-1\}$, with histogram $h_i$ and $p_i = h_i/N$. For a threshold $t \in \{0, \ldots, L-2\}$ let $C_0 = \{p : I(p) \le t\}$ and $C_1 = \{p : I(p) > t\}$, with sizes $n_0, n_1$, shares $\omega_0 = \omega = n_0/N$ and $\omega_1 = 1 - \omega$, and means $\mu_0, \mu_1$. The threshold is valid when $n_0 > 0$ and $n_1 > 0$. Let $\mu_T$ be the mean of all pixel values and

$$\sigma_T^2 = \frac{1}{N}\sum_p (I(p) - \mu_T)^2, \quad \sigma_W^2(t) = \frac{1}{N}\sum_{k=0}^{1} \sum_{p \in C_k} (I(p) - \mu_k)^2, \quad \sigma_B^2(t) = \sum_{k=0}^{1} \omega_k (\mu_k - \mu_T)^2.$$

**Claim 1 (total variance).** For every valid $t$, $\sigma_W^2(t) + \sigma_B^2(t) = \sigma_T^2$.

*Proof.* Write $I(p) - \mu_T = (I(p) - \mu_k) + (\mu_k - \mu_T)$ for $p \in C_k$ and expand the square. The cross term is $2(\mu_k - \mu_T)\sum_{p \in C_k}(I(p) - \mu_k) = 0$, because $\mu_k$ is the mean of $C_k$. So $\sum_p (I(p) - \mu_T)^2 = \sum_k \sum_{p \in C_k} (I(p) - \mu_k)^2 + \sum_k n_k (\mu_k - \mu_T)^2$. Divide by $N$. $\square$

Since $\sigma_T^2$ does not depend on $t$, a valid $t$ maximizes $\sigma_B^2$ if and only if it minimizes $\sigma_W^2$, and the ratios $\lambda = \sigma_B^2/\sigma_W^2$, $\kappa = \sigma_T^2/\sigma_W^2$ and $\eta = \sigma_B^2/\sigma_T^2$ are increasing functions of $\sigma_B^2$ (when $\sigma_W^2 > 0$), so they have the same maximizers.

**Claim 2 (the closed form).** With $\mu(t) = \sum_{i \le t} i p_i$, for a valid $t$

$$\sigma_B^2(t) = \omega_0 \omega_1 (\mu_1 - \mu_0)^2 = \frac{(\mu_T\, \omega - \mu(t))^2}{\omega(1 - \omega)} = \frac{(S n_0 - N s_0)^2}{N^2 n_0 (N - n_0)},$$

where $S = \sum_i i h_i$ and $s_0 = \sum_{i \le t} i h_i$.

*Proof.* $\mu_T = \omega_0 \mu_0 + \omega_1 \mu_1$, so $\mu_0 - \mu_T = \omega_1(\mu_0 - \mu_1)$ and $\mu_1 - \mu_T = \omega_0(\mu_1 - \mu_0)$. Then $\sigma_B^2 = \omega_0 \omega_1^2 d^2 + \omega_1 \omega_0^2 d^2 = \omega_0 \omega_1 d^2$ with $d = \mu_1 - \mu_0$. Next, $\mu_0 = \mu(t)/\omega$ and $\mu_1 = (\mu_T - \mu(t))/(1 - \omega)$, so $d = (\omega \mu_T - \mu(t))/(\omega(1-\omega))$, and $\omega(1-\omega) d^2$ is the second form. For the third, put $\omega = n_0/N$, $\mu(t) = s_0/N$ and $\mu_T = S/N$: the numerator is $(S n_0 - N s_0)^2/N^4$ and the denominator is $n_0(N - n_0)/N^2$. $\square$

**Claim 3 (the scan).** OTSU returns the smallest valid $t$ that maximizes $\sigma_B^2(t)$, and NIL if no $t$ is valid.

*Proof.* By induction on the loop, after line L6 in the pass for $t$, $n_0 = \sum_{i \le t} h_i$ and $s_0 = \sum_{i \le t} i h_i$: both start at 0 (line L4) and line L6 adds the terms for $i = t$. A threshold is valid exactly when $0 < n_0 < N$, which is the test of line L7. For a valid $t$, line L8 computes $\sigma_B^2(t)$ by Claim 2. Every valid value is at least 0, and $best$ starts at $-1$, so the first valid $t$ is stored. After that, lines L9 and L10 replace the stored pair only by a strictly larger value. So after the pass for $t$, $best$ is the largest value over the valid thresholds up to $t$, and $t^\ast$ is the first threshold where it occurs. At the end this holds for all thresholds. If none is valid, $t^\ast$ keeps its initial NIL. $\square$

**Claim 4 (best two-group split).** Suppose the image has at least two distinct values. For any partition of the pixels into two nonempty groups $A, B$ (not necessarily by a threshold) with means $a, b$, let $Q(A, B) = \sum_{p \in A}(I(p) - a)^2 + \sum_{p \in B}(I(p) - b)^2$. Then there is a valid threshold $t$ with $N \sigma_W^2(t) \le Q(A, B)$. Hence Otsu's threshold attains the least $Q$ over all two-group partitions.

*Proof.* If $a = b$, then $Q(A, B) = \sum_p (I(p) - a)^2 \ge N \sigma_T^2 \ge N \sigma_W^2(t)$ for any valid $t$, by Claim 1, and a valid $t$ exists because there are two distinct values. Otherwise name the groups so that $a < b$, and let $m = (a + b)/2$. Put $A' = \{p : I(p) \le m\}$ and $B' = \{p : I(p) > m\}$. $A$ contains a value at most its mean $a < m$, so $A' \ne \emptyset$, and $B$ contains a value at least $b > m$, so $B' \ne \emptyset$. Since the values are integers, $A', B'$ is the split of the threshold $t = \lfloor m \rfloor$, which is valid. Each pixel is in $A'$ exactly when $(I(p) - a)^2 \le (I(p) - b)^2$, so

$$\sum_{p \in A'} (I(p) - a)^2 + \sum_{p \in B'} (I(p) - b)^2 = \sum_p \min\bigl((I(p) - a)^2, (I(p) - b)^2\bigr) \le Q(A, B).$$

Replacing $a$ and $b$ by the means of $A'$ and $B'$ does not increase the left side, because the mean of a group minimizes the sum of squared distances to a single number. The result is $N \sigma_W^2(t)$. $\square$

**Claim 5 (midpoint property).** Let $t^\ast$ be any valid maximizer of $\sigma_B^2$, with class means $\mu_0 < \mu_1$ and $m = (\mu_0 + \mu_1)/2$. Then every value in $C_0$ is at most $m$ and every value in $C_1$ is at least $m$.

*Proof.* $\mu_0 < \mu_1$ holds because every value in $C_0$ is smaller than every value in $C_1$. Suppose a pixel $q \in C_0$ has $I(q) > m$. Then $(I(q) - \mu_1)^2 < (I(q) - \mu_0)^2$. If $C_0 = \{q\}$ then $\mu_0 = I(q) > m > \mu_0$, which is impossible, so $A = C_0 \setminus \{q\}$ is not empty. With $B = C_1 \cup \{q\}$, keeping the old means gives a sum strictly smaller than $N\sigma_W^2(t^\ast)$, and changing to the new means does not increase it, so $Q(A, B) < N \sigma_W^2(t^\ast)$. Claim 4 then gives a valid $t$ with $\sigma_W^2(t) < \sigma_W^2(t^\ast)$, which contradicts Claim 1 and the choice of $t^\ast$. The case of a pixel in $C_1$ below $m$ is the same with the classes exchanged. $\square$

**Claim 6 (multilevel form).** For $M$ classes given by thresholds $t_1 < \cdots < t_{M-1}$, with $n_k$ pixels and value sum $s_k$ in class $k$, the between-class variance $\sum_k \omega_k (\mu_k - \mu_T)^2$ equals $\frac{1}{N^2}\sum_{n_k > 0} s_k^2 / n_k - \mu_T^2$, and the dynamic program of the implementation maximizes it.

*Proof.* Expand: $\sum_k \omega_k \mu_k^2 - 2\mu_T \sum_k \omega_k \mu_k + \mu_T^2 \sum_k \omega_k = \sum_k \omega_k \mu_k^2 - \mu_T^2$, since $\sum_k \omega_k \mu_k = \mu_T$ and $\sum_k \omega_k = 1$, and $\omega_k \mu_k^2 = s_k^2/(N^2 n_k)$; an empty class contributes 0. The objective is a sum over classes of a term that depends only on the first and last level of the class. Let $f(c, j)$ be the best sum for splitting the levels $0, \ldots, j-1$ into $c$ consecutive ranges of at least one level each. Then $f(0, 0) = 0$ and $f(c, j) = \max_{c-1 \le i < j} f(c-1, i) + g(i, j)$, with $g(i, j)$ the term of the range $i, \ldots, j-1$, because the last range of an optimal split is some $i, \ldots, j-1$ and the rest must be an optimal split of $0, \ldots, i-1$ into $c-1$ ranges (otherwise replace it and gain). The table has $O(ML)$ entries with $O(L)$ work each, which gives $O(ML^2)$. $\square$
