---
title: The autocorrelation start, the fixed point property, and when the support update keeps the support
proves: [correctness]
status: full
---

Images have $n_1 \times n_2$ pixels, and indices are taken modulo $n_1$ and $n_2$. The DFT is $F(k) = \sum_t f(t)\, e^{-2\pi i \langle t, k \rangle}$ with $\langle t, k \rangle = t_1 k_1 / n_1 + t_2 k_2 / n_2$, and the inverse has the factor $1/(n_1 n_2)$. The data are $A = |F|$. Arithmetic is exact. There is no claim that shrinkwrap converges; what is proved is that each part does what the algorithm uses it for.

**Lemma 1 (the start is the autocorrelation).** Line L1 computes $\mathrm{IDFT2}(A^2)$, and this is the periodic autocorrelation

$$c(t) = \sum_r f(r + t)\, \overline{f(r)} .$$

*Proof.* Take the DFT of $c$ and put $s = r + t$:

$$\sum_t c(t) e^{-2\pi i \langle t, k \rangle} = \sum_r \overline{f(r)} e^{2\pi i \langle r, k \rangle} \sum_s f(s) e^{-2\pi i \langle s, k \rangle} = \overline{F(k)}\, F(k) = A(k)^2 .$$

The inverse DFT of $A^2$ is therefore $c$. $\square$

So the start needs only the data.

**Lemma 2 (the autocorrelation holds a shifted support).** Let $f \ge 0$ and let $r_0$ be a pixel with $f(r_0) > 0$. Then $c(t) > 0$ for every $t$ with $f(r_0 + t) > 0$. So the set $\{t : c(t) > 0\}$ contains the support of $f$ shifted by $-r_0$.

*Proof.* Every term of $c(t) = \sum_r f(r + t) f(r)$ is at least $0$, and the term $r = r_0$ is $f(r_0 + t) f(r_0) > 0$. $\square$

The algorithm thresholds $|c|$ at a fraction (4 percent) of its maximum. Lemma 2 is about the set where $c > 0$; the threshold makes the start tighter and is a tuned choice, so the thresholded start need not hold a shifted support. A shift of the object does not change $A$, so a shifted support is as good as the true one.

**Lemma 3 (fixed points).** Let $z \ge 0$ have $|\mathrm{DFT2}(z)| = A$, and let the current support $S$ contain the support of $z$. Then the HIO step of line L4 maps $z$ to $z$, and the estimate $P_S(\mathrm{Re}\, P_M z)$ is $z$.

*Proof.* $z$ already has the Fourier magnitude $A$, so $P_M z = z$ (the magnitude step keeps the phase and sets the magnitude, which is already $A$), and $g' = z$ is real. On $S$, $g'(r) = z(r) \ge 0$, so the step keeps $z(r)$. Off $S$, $z(r) = 0$ because $S$ holds the support of $z$, and the step gives $z(r) - \beta \cdot 0 = 0$. So the new image is $z$. The estimate keeps the nonnegative real part on $S$, which is $z$. $\square$

**Lemma 4 (when the update keeps the support).** Let $z \ge 0$, let $k$ be the Gaussian kernel of line L6 (nonnegative, sum 1, value $k(0)$ at the center), and let $\tau \in (0, 1)$ be the threshold. If $k(0) \min\{z(r) : z(r) > 0\} \ge \tau \max_r z(r)$, then the new support $\{r : (k * z)(r) \ge \tau \max (k * z)\}$ contains the support of $z$.

*Proof.* All terms of $(k * z)(r) = \sum_q k(q) z(r - q)$ are at least $0$, so $(k * z)(r) \ge k(0) z(r)$. Also $(k * z)(r) \le \max z \sum_q k(q) = \max z$, so $\max(k * z) \le \max z$. For $r$ with $z(r) > 0$,

$$(k * z)(r) \ge k(0) z(r) \ge k(0) \min_{z > 0} z \ge \tau \max z \ge \tau \max(k * z). \qquad \square$$

**Corollary.** If an iterate reaches a solution $z \ge 0$ while the support holds the support of $z$, and the condition of Lemma 4 holds for the current $\sigma$ and $\tau$, then every later step and every later update keeps $z$ and a support that holds the support of $z$.

*Proof.* Lemma 3 for the steps, Lemma 4 for the updates (the update is applied to the estimate, which is $z$ by Lemma 3), and induction. $\square$

**What is not claimed.** There is no theorem that shrinkwrap reaches a solution, that the support shrinks to the true support, or that it stays near it. The condition of Lemma 4 is sufficient, not necessary; for an object with a large range of values it fails, and a weak pixel at the edge of the object can then drop out of the support. The thresholds 4 and 20 percent, the update every 20 steps and the widths of the Gaussian are tuned values. The tests check Lemmas 1 to 4 and one reconstruction as a measurement.
