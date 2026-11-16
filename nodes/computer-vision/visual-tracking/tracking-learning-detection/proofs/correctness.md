---
title: The parts of tracking-learning-detection that can be proved exactly, the median flow estimates, the constant-time variance filter, the similarity ranges, and the stability condition of P-N learning
proves: [correctness]
status: full
---

Notation as on the page. TLD as a whole is a heuristic: it has no guarantee that the box it outputs covers the object. What can be proved is that each part computes what it says it computes, and, under the model of Kalal, Mikolajczyk and Matas, when the errors of P-N learning go down. The claims below do that.

## Claim 1: the variance filter is exact and costs constant time per window

Let $S(x, y) = \sum_{u < x,\, v < y} I(u, v)$ and $S_2$ the same sum of $I(u, v)^2$, with $S(0, \cdot) = S(\cdot, 0) = 0$. For the integer box $B = [x_1, x_2) \times [y_1, y_2)$ with $n$ pixels,

$$
\sum_{(u, v) \in B} I(u, v) = S(x_2, y_2) - S(x_1, y_2) - S(x_2, y_1) + S(x_1, y_1),
$$

and the same holds for $S_2$. Then the variance of the pixels of $B$ is $E[I^2] - E[I]^2$ with both means read from these sums.

*Proof.* $S(x_2, y_2)$ counts every pixel with $u < x_2$ and $v < y_2$. Subtracting $S(x_1, y_2)$ and $S(x_2, y_1)$ removes the pixels with $u < x_1$ or $v < y_1$, but removes the pixels with $u < x_1$ and $v < y_1$ twice, and adding $S(x_1, y_1)$ restores them once. So each pixel of $B$ is counted once and every other pixel zero times. The variance identity is $\frac1n \sum (I - m)^2 = \frac1n \sum I^2 - 2 m \frac1n \sum I + m^2 = E[I^2] - m^2$ with $m = E[I]$. Four reads from each table and a few operations give the value, so line L8 costs $O(1)$ per window after $O(P)$ work to build the tables. $\square$

## Claim 2: median flow is exact for a translation and robust to a minority of bad points

Let the points $p_i$ of line L1 move to $q_i = p_i + d_i$, and let $d_m$ be the median (taken coordinate by coordinate) of the displacements of the kept points of line L4.

(a) If every kept point has $d_i = d$, then line L5 gives $d_m = d$, and every distance ratio of line L7 is 1, so the box moves by $d$ and keeps its size.

(b) If the points obey a similarity, $q_i = s R p_i + t$ with $R$ a rotation and $s > 0$, then every ratio $|q_i - q_j| / |p_i - p_j|$ equals $s$, so line L7 gives exactly $s$.

(c) If more than half of the kept displacements have their first coordinate in an interval $[a, b]$, then the first coordinate of $d_m$ is in $[a, b]$; the same holds for the second coordinate.

*Proof.* (a) The median of equal numbers is that number, and $|q_i - q_j| = |p_i - p_j|$. (b) $|q_i - q_j| = |s R (p_i - p_j)| = s |p_i - p_j|$ because a rotation keeps lengths. (c) Sort the $k$ values as $v_1 \le \dots \le v_k$. Fewer than $k/2$ values are outside $[a, b]$, so fewer than $k/2$ are below $a$, and therefore $v_j \ge a$ for every $j \ge k/2$. In the same way fewer than $k/2$ are above $b$, so $v_j \le b$ for every $j \le k/2 + 1$. The median is $v_{(k+1)/2}$ for odd $k$, or the mean of $v_{k/2}$ and $v_{k/2 + 1}$ for even $k$; in both cases the values used have indices in $[k/2, k/2 + 1]$, so they are in $[a, b]$, and so is their mean. $\square$

So a few points on an occluder or on the background cannot move the box far, as long as most kept points follow the object. Lines L3 and L4 try to make this true by dropping the points with a large forward-backward error or a low NCC, but this is a heuristic: a point can be wrong and still have a small forward-backward error.

## Claim 3: the similarities are in [0, 1] and are monotone in the right direction

For normalized patches $a$, $b$ (zero mean, unit norm), $\mathrm{NCC}(a, b) = \langle a, b \rangle \in [-1, 1]$ by the Cauchy-Schwarz inequality, so $S(a, b) = \frac12 (\mathrm{NCC} + 1) \in [0, 1]$, with 1 only for $b = a$ and 0 only for $b = -a$. Let $S^+$ and $S^-$ be the largest similarities to a positive and to a negative patch. Then $S^r = S^+ / (S^+ + S^-) \in [0, 1]$ grows with $S^+$ and falls with $S^-$, and $S^c \le S^r$.

*Proof.* The first part is Cauchy-Schwarz, with equality only for parallel vectors; unit norm leaves $b = \pm a$. $S^r$ has the derivative $S^- / (S^+ + S^-)^2 \ge 0$ in $S^+$ and $-S^+ / (S^+ + S^-)^2 \le 0$ in $S^-$. The conservative similarity uses $S^+_{50\%}$, the largest similarity to the older half of the positives, which is a subset, so $S^+_{50\%} \le S^+$ and by monotony $S^c \le S^r$. $\square$

A consequence that the example on the page shows: a patch identical to a positive has $S^r = 1 / (1 + S^-)$, so $S^r$ can be well below 1 when one negative is a little similar. The threshold $\theta_{\text{NN}}$ must be set with this in mind.

## Claim 4: the ensemble posterior is an average of empirical frequencies

For fern $f$ and code $c$ with $p$ positive and $n$ negative training counts, line L9 uses $P_f(c) = p / (p + n)$ (0 if $p + n = 0$), and the ensemble value is the mean over the ferns. Each $P_f(c) \in [0, 1]$, so the mean is in $[0, 1]$; a window is passed if the mean is above $1/2$. This is the definition, and the tests check the counts. Whether the frequencies estimate a true posterior depends on the training samples, which is not claimed.

## Claim 5: the stability condition of P-N learning

This is the analysis of Kalal, Mikolajczyk and Matas (Section 4.2). Let $\alpha(k)$ and $\beta(k)$ be the numbers of false positives and false negatives of the classifier after iteration $k$. The P-expert outputs $n^+_c(k)$ correct and $n^+_f(k)$ false positive labels, the N-expert $n^-_c(k)$ correct and $n^-_f(k)$ false negative labels, and every label changes the classifier's decision on that example. Assume the four quality measures are constant:

$$
P^+ = \frac{n^+_c}{n^+_c + n^+_f}, \quad R^+ = \frac{n^+_c}{\beta}, \quad P^- = \frac{n^-_c}{n^-_c + n^-_f}, \quad R^- = \frac{n^-_c}{\alpha}.
$$

Then $x(k) = (\alpha(k), \beta(k))^{\mathsf T}$ obeys $x(k + 1) = M x(k)$ with

$$
M = \begin{pmatrix} 1 - R^- & \frac{1 - P^+}{P^+} R^+ \\[2pt] \frac{1 - P^-}{P^-} R^- & 1 - R^+ \end{pmatrix},
$$

and $x(k) \to 0$ for every start if and only if both eigenvalues of $M$ have absolute value below 1.

*Proof.* A correct positive label fixes a false negative and a false positive label creates a false positive, so $\alpha(k+1) = \alpha(k) - n^-_c(k) + n^+_f(k)$ and $\beta(k+1) = \beta(k) - n^+_c(k) + n^-_f(k)$. From the definitions, $n^+_c = R^+ \beta$, $n^+_f = n^+_c (1 - P^+) / P^+ = \frac{1 - P^+}{P^+} R^+ \beta$, $n^-_c = R^- \alpha$ and $n^-_f = \frac{1 - P^-}{P^-} R^- \alpha$. Substituting gives the two rows of $M$. For a linear recursion $x(k) = M^k x(0)$, and $M^k \to 0$ if and only if the spectral radius of $M$ is below 1 (write $M$ in Jordan form: a block with eigenvalue $\lambda$ has entries $\binom{k}{j} \lambda^{k - j}$, which go to 0 if and only if $|\lambda| < 1$). $\square$

**The symmetric case.** With $P^+ = R^+ = P^- = R^- = 1 - \varepsilon$, every entry of $M$ is $\varepsilon$, so the eigenvalues are $0$ and $2\varepsilon$ (the all-ones $2 \times 2$ matrix has eigenvectors $(1, 1)$ and $(1, -1)$ with eigenvalues 2 and 0). The errors go to 0 if and only if $\varepsilon < 1/2$: experts that are right more often than wrong are enough, because the errors of the two experts partly cancel.

The real experts of TLD do not have constant quality, and their labels are not independent of the classifier, so this claim explains why the method can improve but does not prove that the implemented tracker does.

## What is not claimed

The integrator (line L13) picks the candidate with the largest conservative similarity; nothing proves it is the object. The rule of line L14, which keeps a trajectory reliable while the tracker has not failed, can keep learning from an occluder for some frames. The failure tests of line L4 and line L6 can miss a failure and can stop on a good frame. All thresholds are heuristics.
