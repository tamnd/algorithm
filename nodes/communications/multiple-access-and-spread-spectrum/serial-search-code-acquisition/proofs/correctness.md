---
title: Serial search returns the true code phase, and its mean acquisition time
proves: [correctness]
status: full
---

The model has $q$ cells, numbered $0, \ldots, q - 1$, and one of them, $\tau$, is the true code phase. Each dwell at a cell $k$ uses a fresh block of $N$ chips
$$r[n] = \sqrt{E_s}\, c[(n - \tau) \bmod N] + w[n], \qquad w[n] \sim \mathcal{CN}(0, N_0) \text{ independent},$$
with a code of unit energy, $\sum_n |c[n]|^2 = 1$. The dwell computes $z = \sum_n \overline{c[(n - k) \bmod N]}\, r[n]$ (L3) and compares $|z|^2$ with a threshold $\gamma$ (L4). A crossing goes to a verification (L5). We assume that the verification is perfect: it accepts the true cell and rejects every other cell, and a rejection costs $K$ further dwells. Time is counted in dwells. Write $P_d$ for the probability that a dwell at the true cell crosses the threshold and $P_{fa}$ for the probability that a dwell at a wrong cell crosses it.

**Lemma 1 (law of one dwell).** $z \sim \mathcal{CN}\big(\sqrt{E_s}\, R(\tau - k),\ N_0\big)$, where $R(s) = \sum_n \overline{c[n]}\, c[(n - s) \bmod N]$ is the periodic autocorrelation of the code. The outputs of different dwells are independent.

*Proof.* Substitute $r$ into $z$. The signal part is $\sqrt{E_s} \sum_n \overline{c[(n - k) \bmod N]}\, c[(n - \tau) \bmod N]$; the substitution $n \to n + k$ turns it into $\sqrt{E_s}\, R(\tau - k)$. The noise part $\sum_n \overline{c[(n - k) \bmod N]}\, w[n]$ is a fixed linear combination of independent $\mathcal{CN}(0, N_0)$ variables with squared coefficients summing to $1$, so it is $\mathcal{CN}(0, N_0)$. Each dwell uses its own block, so the noise parts of different dwells are independent. $\square$

For an m-sequence with unit energy, $R(0) = 1$ and $R(s) = -1/N$ for $s \ne 0$. So all wrong cells have the same $P_{fa}$.

**Lemma 2 (detection and false alarm probabilities).** If $z \sim \mathcal{CN}(\mu, N_0)$, then
$$P(|z|^2 > \gamma) = Q_1\Big(\sqrt{2 |\mu|^2 / N_0},\ \sqrt{2 \gamma / N_0}\Big),$$
where $Q_1(a, b) = \sum_{j \ge 0} e^{-a^2/2} \frac{(a^2/2)^j}{j!}\; e^{-b^2/2} \sum_{i=0}^{j} \frac{(b^2/2)^i}{i!}$ is the Marcum Q function of order 1. So $P_d = Q_1(\sqrt{2 E_s/N_0}, \sqrt{2\gamma/N_0})$, and $P_{fa}$ is the same with $E_s R(s)^2$ in place of $E_s$.

*Proof.* Write $z = \sqrt{N_0/2}\,(X + iY)$ with $X, Y$ independent real Gaussians of variance 1 and means whose squares add to $a^2 = 2|\mu|^2/N_0$. Then $X^2 + Y^2 = 2|z|^2/N_0$ has the noncentral chi-square law with 2 degrees of freedom and noncentrality $a^2$. This law is a Poisson mixture: with $J \sim \mathrm{Poisson}(a^2/2)$, it is the law of a central chi-square variable with $2 + 2J$ degrees of freedom, that is, twice a $\mathrm{Gamma}(J + 1, 1)$ variable. For an integer $m$, $P(\mathrm{Gamma}(m, 1) > x) = e^{-x} \sum_{i < m} x^i / i!$, the probability that a Poisson process of rate 1 has fewer than $m$ points in $[0, x]$. The event $|z|^2 > \gamma$ is $X^2 + Y^2 > b^2$ with $b^2 = 2\gamma/N_0$, that is, $\mathrm{Gamma}(J + 1, 1) > b^2/2$. Averaging over $J$ gives the series. $\square$

**Lemma 3 (the result is the true cell).** If $P_d > 0$, the search stops with probability 1, and when it returns a cell, that cell is $\tau$.

*Proof.* The search returns only from L5, and only when the verification accepts the cell, which by assumption happens only at $\tau$. L6 moves the cell by one modulo $q$, so the true cell is visited once in every $q$ consecutive dwells. Each visit is a fresh dwell (Lemma 1) that crosses the threshold with probability $P_d$, independently of the earlier visits. The probability that the first $m$ visits all miss is $(1 - P_d)^m \to 0$. $\square$

**Lemma 4 (mean time from a fixed start).** Let $j \in \{1, \ldots, q\}$ be the position of $\tau$ in the visiting order from the start cell, so $j - 1 = (\tau - \mathrm{start}) \bmod q$. Write $m = 1 + K P_{fa}$. Then
$$E[T \mid j] = (j - 1)\, m + 1 + \frac{1 - P_d}{P_d}\,\big(1 + (q - 1)\, m\big).$$

*Proof.* Let $M$ be the number of visits to $\tau$ that miss before the first hit. By Lemma 3 and the independence of the dwells, $P(M = i) = (1 - P_d)^i P_d$, so $E[M] = (1 - P_d)/P_d$. The search makes $M + 1$ dwells at $\tau$, each of cost 1, and $W = (j - 1) + M (q - 1)$ dwells at wrong cells. A wrong dwell costs $1 + K X$, where $X$ is the indicator of a false alarm, with $E[X] = P_{fa}$. The variables $X$ at the wrong dwells are independent of the outcomes at $\tau$, hence of $M$ and $W$. By Wald's identity the expected total cost of the wrong dwells is $E[W]\, m$. So
$$E[T \mid j] = E[M] + 1 + \big((j - 1) + E[M](q - 1)\big)\, m,$$
which is the stated formula after grouping the terms with $E[M]$. $\square$

**Theorem (mean acquisition time).** If the start cell is uniform and independent of $\tau$, then
$$E[T] = \frac{2 + (2 - P_d)(q - 1)(1 + K P_{fa})}{2 P_d}\ \text{dwells}.$$

*Proof.* With a uniform start, $j - 1$ is uniform on $\{0, \ldots, q - 1\}$, so $E[j - 1] = (q - 1)/2$. Averaging Lemma 4 over $j$,
$$E[T] = \frac{(q - 1)\, m}{2} + 1 + \frac{1 - P_d}{P_d}\big(1 + (q - 1)\, m\big) = \frac{1}{P_d}\Big(1 + (q - 1)\, m \Big(\frac{P_d}{2} + 1 - P_d\Big)\Big),$$
since $P_d + (1 - P_d) = 1$. The last bracket is $(2 - P_d)/2$, which gives the formula. $\square$

**Checks.** With $P_d = 1$ and $P_{fa} = 0$, $E[T] = (q + 1)/2$, the mean position of a uniform cell. With $q = 1$, $E[T] = 1/P_d$, the mean of a geometric variable.

**Cost.** Each dwell computes one correlation of $N$ products, so the expected number of operations is $\Theta(N)$ times $E[T]$, with $\Theta(1)$ space beyond the block of chips.
