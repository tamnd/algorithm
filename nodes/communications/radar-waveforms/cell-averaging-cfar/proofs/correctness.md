---
title: The running sum of CA-CFAR equals the window sum, and its false alarm probability is (1 + tau)^(-N) for every noise power
proves: [correctness]
status: full
---

The notation is that of the page. The input is $x[0], \dots, x[n-1]$, one power value per range cell. $N = 2h$ is the even number of reference cells, $G \ge 0$ the number of guard cells on each side and $\tau > 0$ the factor on the sum. For a cell $i$ with $G + h \le i \le n - 1 - G - h$, the reference window is

$$W_i = \{i - G - h, \dots, i - G - 1\} \cup \{i + G + 1, \dots, i + G + h\},$$

and the window sum is $Z_i = \sum_{c \in W_i} x[c]$. The detector reports cell $i$ if and only if $x[i] > \tau Z_i$. Write $f = G + h$ and $\ell = n - 1 - G - h$ for the first and the last cell that has a full window.

**Lemma 1 (the running sum).** If $f \le \ell$, then at the start of the iteration for cell $i$ of the loop in line L3, $z = Z_i$.

*Proof.* By induction on $i$.

*Base, $i = f$.* Line L2 sets $z$ to the sum of $x[f - G - h], \dots, x[f - G - 1]$ and $x[f + G + 1], \dots, x[f + G + h]$. These are the cells of $W_f$, so $z = Z_f$. All indices are inside $0, \dots, n-1$, because $f - G - h = 0$ and $f + G + h = 2f \le f + \ell \le n - 1$.

*Step.* Assume $z = Z_i$ at the start of the iteration for $i$, with $i < \ell$. The lagging part of $W_{i+1}$ is $\{i + 1 - G - h, \dots, i - G\}$. It is the lagging part of $W_i$ without $i - G - h$ and with $i - G$. The leading part of $W_{i+1}$ is $\{i + G + 2, \dots, i + G + h + 1\}$. It is the leading part of $W_i$ without $i + G + 1$ and with $i + G + h + 1$. So

$$Z_{i+1} = Z_i + x[i - G] - x[i - G - h] + x[i + G + h + 1] - x[i + G + 1].$$

Line L6 adds the first difference and line L7 the second, so at the start of the iteration for $i + 1$, $z = Z_{i+1}$. Line L7 reads $x[i + G + h + 1]$, and $i + 1 \le \ell$ gives $i + G + h + 1 \le n - 1$, so the index is valid. Line L6 reads $x[i - G - h]$, and $i \ge f$ gives $i - G - h \ge 0$. $\square$

**Theorem 1 (the output).** For every input, the detector reports exactly the cells $i$ with $f \le i \le \ell$ and $x[i] > \tau Z_i$, in increasing order, and it gives no decision for the other cells.

*Proof.* The loop of line L3 visits $i = f, \dots, \ell$ in increasing order, once each. By Lemma 1 line L4 computes $t = \tau Z_i$, and line L5 reports $i$ exactly when $x[i] > \tau Z_i$. If $f > \ell$, no cell has a full window and the loop does not run. $\square$

With integer or rational cells and a rational $\tau$, each value of $z$ is exact, so Theorem 1 holds with no rounding. With floating point cells, the running sum can differ from a fresh sum by rounding, which the page discusses under Pitfalls.

**Lemma 2 (the Laplace transform of a gamma sum).** Let $Y_1, \dots, Y_N$ be independent and exponential with mean $\mu$, that is with density $e^{-y/\mu}/\mu$ on $y \ge 0$, and $Z = Y_1 + \dots + Y_N$. Then for every $s \ge 0$, $E\, e^{-sZ} = (1 + s\mu)^{-N}$.

*Proof.* For one cell, $E\, e^{-sY} = \int_0^\infty e^{-sy} e^{-y/\mu}\, dy / \mu = \frac{1/\mu}{s + 1/\mu} = (1 + s\mu)^{-1}$. The cells are independent, so the transform of the sum is the product of $N$ equal factors. $\square$

**Theorem 2 (constant false alarm rate).** Assume the homogeneous noise model: the cell under test and its $N$ reference cells are independent and exponential with the same mean $\mu > 0$. This is the output of a square-law detector, $|w|^2$, for circular complex Gaussian noise $w \sim \mathcal{CN}(0, \mu)$. Then

$$P(x[i] > \tau Z_i) = (1 + \tau)^{-N},$$

which does not depend on $\mu$. So $\tau = P_{fa}^{-1/N} - 1$ gives the false alarm probability $P_{fa}$ for every noise power.

*Proof.* The cell under test $X = x[i]$ is independent of $Z = Z_i$. Given $Z = z$, $P(X > \tau z) = e^{-\tau z/\mu}$, because $X$ is exponential with mean $\mu$. Take the expectation over $Z$ and use Lemma 2 with $s = \tau/\mu$:

$$P(X > \tau Z) = E\, e^{-(\tau/\mu) Z} = (1 + (\tau/\mu)\mu)^{-N} = (1 + \tau)^{-N}.$$

The value $\mu$ cancels. Solving $(1 + \tau)^{-N} = P_{fa}$ for $\tau > 0$ gives $\tau = P_{fa}^{-1/N} - 1$. $\square$

**Theorem 3 (detection of a Swerling 1 target).** In the same model, let the cell under test hold a Swerling 1 target of mean signal to noise ratio $S$, so that $X$ is exponential with mean $\mu(1 + S)$ and independent of the reference cells. Then

$$P_d = P(X > \tau Z) = \left(1 + \frac{\tau}{1 + S}\right)^{-N}.$$

*Proof.* As in Theorem 2, $P(X > \tau z) = e^{-\tau z / (\mu(1 + S))}$. Lemma 2 with $s = \tau / (\mu(1 + S))$ gives $(1 + \tau/(1 + S))^{-N}$. $\square$

**Theorem 4 (scale invariance).** If every cell is multiplied by the same $c > 0$, the detector reports the same cells.

*Proof.* $Z_i$ is linear in the cells, so $c\, x[i] > \tau\, c Z_i$ holds exactly when $x[i] > \tau Z_i$. By Theorem 1 the output depends only on these comparisons. $\square$

Theorem 4 is the reason for the constant false alarm rate. Theorem 2 needs the exponential model, but Theorem 4 holds for every input, so a change of the noise power alone never changes a decision. $\blacksquare$
