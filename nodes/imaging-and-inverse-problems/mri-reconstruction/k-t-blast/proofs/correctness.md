---
title: The x-f aliasing of lattice sampling and the exactness of the k-t BLAST unfolding
proves: [correctness]
status: full
---

The setting is that of the algorithm. A series $x(y, t)$ has $n$ pixels and $n_t$ frames. Coil $c$ has the map $c(y)$; with one coil, $c = 1$. The unitary DFT along $y$ is $K(k) = n^{-1/2} \sum_y x(y) e^{-2\pi i k y / n}$, and the unitary DFT along $t$ is $\rho(y, f) = n_t^{-1/2} \sum_t x(y, t) e^{-2\pi i f t / n_t}$. All indices are taken modulo $n$ or $n_t$. The acceleration $R$ divides $n$ and $n_t$, and the shift $s$ is prime to $R$. Frame $t$ keeps the lines $k$ with $k \equiv s t \pmod R$.

## 1. Aliasing in x-f space

**Theorem 1.** Let $\rho_c$ be the x-f signal of $c\, x$. Zero fill the sampled k-t data of coil $c$, apply the unitary inverse DFT along $k$ and the unitary DFT along $t$. The result is

$$\rho_{\text{alias}, c}(y, f) = \frac1R \sum_{j=0}^{R-1} \rho_c\Big(y + \frac{jn}{R},\ f + \frac{j s n_t}{R}\Big).$$

*Proof.* The mask is $m(k, t) = \frac1R \sum_{j=0}^{R-1} e^{2\pi i j (k - s t)/R}$, because the sum over $j$ is $R$ when $k - st \equiv 0 \pmod R$ and 0 otherwise. Write $e^{2\pi i j k / R} = e^{2\pi i k (jn/R) / n}$. Multiplying a k-space line by $e^{2\pi i k a / n}$ shifts its unitary inverse DFT: the result is $x(y + a)$. Write $e^{-2\pi i j s t / R} = e^{-2\pi i (j s n_t / R) t / n_t}$. Multiplying a time series by $e^{-2\pi i b t / n_t}$ shifts its unitary DFT: the result is $\rho(f + b)$. The three transforms are linear, so the term $j$ of the mask gives $\frac1R \rho_c(y + jn/R, f + j s n_t / R)$. $\square$

**Lemma 2.** The groups $G(y_0, f_0) = \{(y_0 + jn/R,\ f_0 + j s n_t / R) : j = 0, \ldots, R-1\}$ for $0 \le y_0 < n/R$ and $0 \le f_0 < n_t$ partition the x-f grid into $n n_t / R$ sets of $R$ points, and $\rho_{\text{alias}, c}(y_0, f_0)$ depends only on the values of $\rho$ in $G(y_0, f_0)$.

*Proof.* A point $(y, f)$ lies in the group with $j = \lfloor y / (n/R) \rfloor$, $y_0 = y - jn/R$ and $f_0 = f - j s n_t / R$, and in no other, because $j$ and $y_0$ are fixed by $y$. The groups have $R$ distinct points, because their $y$ values differ. The second claim is Theorem 1. $\square$

So, for each group, the data are $v = A \rho_G$, where $v_c = \rho_{\text{alias}, c}(y_0, f_0)$ and $A$ is the $n_c \times R$ matrix $A_{c j} = c(y_0 + jn/R) / R$. With one coil, $A = \frac1R (1, \ldots, 1)$.

## 2. The unfolding is a Wiener estimate

Let $P = \operatorname{diag}(p_1, \ldots, p_R)$ with $p_j \ge 0$ and $\psi \ge 0$. The code computes

$$\hat\rho_G = P A^H (A P A^H + \psi I)^{-1} v,$$

and returns 0 when $P = 0$.

**Lemma 3.** If $\rho_G$ is a random vector with mean 0 and covariance $P$, and $v = A \rho_G + e$ with noise $e$ of mean 0 and covariance $\psi I$, uncorrelated with $\rho_G$, and $A P A^H + \psi I$ is invertible, then $\hat\rho_G = W v$ with $W = P A^H (A P A^H + \psi I)^{-1}$ minimizes the mean squared error $\mathbb{E} \|W v - \rho_G\|^2$ over all matrices $W$.

*Proof.* The error is $\mathbb{E}\|W v - \rho_G\|^2 = \operatorname{tr}(W C W^H) - 2 \operatorname{Re} \operatorname{tr}(W A P) + \operatorname{tr} P$ with $C = A P A^H + \psi I$, because $\mathbb{E}[v v^H] = C$ and $\mathbb{E}[v \rho_G^H] = A P$. Write $W = W_0 + \Delta$ with $W_0 = P A^H C^{-1}$. Since $W_0 C = P A^H$, the terms linear in $\Delta$ cancel, and the error is the error of $W_0$ plus $\operatorname{tr}(\Delta C \Delta^H) \ge 0$. $\square$

**Lemma 4 (the second form).** If $\psi > 0$ and all $p_j > 0$, then $P A^H (A P A^H + \psi I)^{-1} = (A^H A / \psi + P^{-1})^{-1} A^H / \psi$. So $\hat\rho_G$ also minimizes $\|v - A \rho\|^2 / \psi + \sum_j |\rho_j|^2 / p_j$.

*Proof.* Multiply both sides on the left by $A^H A/\psi + P^{-1}$ and on the right by $A P A^H + \psi I$. The left side gives $(A^H A P/\psi + I) A^H = A^H (A P A^H + \psi I)/\psi$, which is the right side. The quadratic $\|v - A\rho\|^2/\psi + \rho^H P^{-1} \rho$ has the gradient zero exactly at this point. $\square$

The test file checks Lemma 4 for a random $3 \times 2$ matrix $A$.

## 3. When the unfolding is exact

**Theorem 5.** Let $Q$ be the set of indices $j$ with $p_j > 0$. Suppose that the true $\rho_G$ is zero outside $Q$ and that the columns of $A$ with indices in $Q$ are linearly independent. Then $\hat\rho_G \to \rho_G$ as $\psi \to 0^+$, and $\hat\rho_G = \rho_G$ for $\psi = 0$ if $A P A^H$ is invertible.

*Proof.* Only the columns in $Q$ enter, so write $A_Q$, $P_Q$ and $B = A_Q P_Q^{1/2}$, which has full column rank. With $v = A_Q \rho_Q$,

$$\hat\rho_Q = P_Q^{1/2} B^H (B B^H + \psi I)^{-1} B\, P_Q^{-1/2} \rho_Q = P_Q^{1/2} (B^H B + \psi I)^{-1} B^H B\, P_Q^{-1/2} \rho_Q,$$

using $B^H (B B^H + \psi I)^{-1} = (B^H B + \psi I)^{-1} B^H$. As $\psi \to 0$, $(B^H B + \psi I)^{-1} B^H B \to I$ because $B^H B$ is invertible, and so $\hat\rho_Q \to \rho_Q$. Outside $Q$, $\hat\rho$ is 0 because $p_j = 0$. $\square$

Three cases follow, and the test file checks each.

- **One coil, one signal point per group.** With one coil, every column of $A$ is $1/R$, so $Q$ may hold only one index. If each group holds at most one nonzero point of the dynamic signal and the power is positive exactly there, the unfolding is exact.
- **k-t SENSE with $n_c \ge R$ coils.** If the coil matrix $A$ of every group has full column rank, $Q$ may be the whole group, and the unfolding is exact for every series and every positive $P$ in the limit $\psi \to 0$. This is SENSE unfolding in x-f space.
- **Full sampling.** With $R = 1$, every group has one point and $A = (c)$, so the result is exact.

When two points of one group carry signal and $A$ cannot separate them, Theorem 5 does not apply. The estimate then splits the alias value in proportion to the prior, and its error is measured.

## 4. The baseline

The code takes the mean of the sampled values of each line $k$ as the baseline k-space, then subtracts it from the samples and adds its image back at the end.

**Lemma 6.** The baseline image is $\bar x(y) + n_t^{-1/2} \sum_{j=1}^{R-1} \rho(y + jn/R,\ j s n_t / R)$, where $\bar x$ is the true time average. If the series is static, the baseline is exact and the output equals the series for every $P$ and $\psi$.

*Proof.* Line $k$ is sampled at the $n_t / R$ frames with $k \equiv st$. With the mask expansion of Theorem 1, the mean over these frames is $\frac{R}{n_t} \sum_t m(k, t) K(k, t) = \frac{1}{n_t} \sum_j e^{2\pi i jk/R} \sum_t e^{-2\pi i j s t / R} K(k, t)$. The term $j = 0$ is the time average of $K(k, \cdot)$. The term $j$ is $n_t^{-1/2} e^{2\pi i jk/R}$ times the unitary temporal DFT of $K(k, \cdot)$ at $f = j s n_t / R$, and the inverse DFT along $k$ turns the factor $e^{2\pi i jk/R}$ into the shift $y + jn/R$. For a static series, $\rho(\cdot, f) = 0$ for $f \ne 0$, so the baseline is $\bar x = x$, the data minus the baseline are zero, the unfolding gives $\hat\rho = 0$, and the output is $x$. $\square$

Since $s$ is prime to $R$, the frequencies $j s n_t / R$ for $j = 1, \ldots, R-1$ are the nonzero multiples of $n_t / R$. So the baseline holds, besides the true average, copies of the signal at these temporal frequencies, moved in $y$ by multiples of $n/R$. After the subtraction, the sum over the sampled frames of each line is zero, so the aliased value at $f = 0$ is zero for every $y$, and the unfolding sets every group $G(y_0, 0)$ to zero. The result is exact when the dynamic signal at the multiples of $n_t / R$ is zero, as in the tests. Otherwise this is part of the measured error, and it is small when the signal at those frequencies is weak.
