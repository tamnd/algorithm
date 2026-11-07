---
title: Correctness of Bernoulli's method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(x) = a_0x^n + \cdots + a_n$ with $a_0 \ne 0$, $n \ge 1$, and distinct roots $r_1, \dots, r_s$ with multiplicities $m_1, \dots, m_s$, so $p(x) = a_0\prod_i (x - r_i)^{m_i}$. Let $s_k = \sum_i m_ir_i^k$ be the power sums, with $s_0 = n$. Statements are in exact arithmetic.

## Lemma 1 (the computed sequence is the power sums)

The window of line L1 is $(s_0, \dots, s_{n-1})$, and the terms produced at L3 are, up to one common positive factor per step, $s_n, s_{n+1}, \dots$. In particular each ratio of L6 equals $s_{j+1}/s_j$ for the corresponding $j$.

*Proof.* Newton's identities state $a_0s_k + a_1s_{k-1} + \cdots + a_{k-1}s_1 + ka_k = 0$ for $1 \le k \le n$, so L1 computes $s_1, \dots, s_{n-1}$ correctly. For $k \ge n$,
$$\sum_{j=0}^{n} a_js_{k-j} = \sum_i m_ir_i^{k-n}\sum_{j=0}^{n}a_jr_i^{n-j} = \sum_i m_ir_i^{k-n}p(r_i) = 0,$$
so the power sums satisfy the recurrence of L3, and a sequence satisfying it is determined by any $n$ consecutive terms. The rescaling at L4 multiplies the whole window by $1/c$ for some $c > 0$; since the recurrence is linear, every later term is multiplied by the same factor, and a ratio of two terms of one window is unchanged. Line L6 divides the new term by the last term of the window it was computed from, before that window is rescaled, so the ratio is $s_{j+1}/s_j$. $\square$

## Theorem 1 (convergence to the dominant root)

Suppose $r_1$ is the only distinct root of largest modulus and $r_1 \ne 0$, and let $\lambda = \max_{i \ge 2}|r_i|/|r_1| < 1$ (with $\lambda = 0$ when $s = 1$). Then $r_1$ is real, $s_j \ne 0$ for all large $j$, and
$$\frac{s_{j+1}}{s_j} - r_1 = \frac{1}{1 + \varepsilon_j}\sum_{i \ge 2}\frac{m_i}{m_1}(r_i - r_1)\Bigl(\frac{r_i}{r_1}\Bigr)^j, \qquad \varepsilon_j = \sum_{i \ge 2}\frac{m_i}{m_1}\Bigl(\frac{r_i}{r_1}\Bigr)^j,$$
so $|s_{j+1}/s_j - r_1| \le 2n|r_1|\lambda^j/(1 - n\lambda^j)$ once $n\lambda^j < 1$. If moreover $r_2$ is the only distinct root of modulus $\lambda|r_1|$, the errors $E_j = s_{j+1}/s_j - r_1$ satisfy $E_{j+1}/E_j \to r_2/r_1$.

*Proof.* If $r_1$ were not real, $\bar r_1 \ne r_1$ would be a root of the same modulus, since the coefficients are real; so $r_1$ is real. Write $s_j = m_1r_1^j(1 + \varepsilon_j)$. Since $|r_i/r_1| \le \lambda$ for $i \ge 2$ and $\sum_i m_i = n$, $|\varepsilon_j| \le n\lambda^j/m_1 \le n\lambda^j$, which tends to 0, so $s_j \ne 0$ once $n\lambda^j < 1$. Then
$$s_{j+1} - r_1s_j = \sum_{i \ge 2} m_i r_i^j (r_i - r_1),$$
and dividing by $s_j$ gives the identity. Using $|r_i - r_1| \le 2|r_1|$ and $\sum_{i \ge 2}m_i \le n$ gives the bound. For the last claim, the terms with $|r_i| < |r_2|$ are $o(|r_2/r_1|^j)$, so $E_j = \frac{m_2}{m_1}(r_2 - r_1)(r_2/r_1)^j(1 + o(1))$, with $r_2$ real by the same conjugation argument, and $E_{j+1}/E_j \to r_2/r_1$. $\square$

So the method converges linearly with rate $\lambda$ for every multiplicity $m_1$; since the power sums contain no factors polynomial in $j$, a multiple dominant root does not slow it. If $r_1 = 0$ is the only root, $p = a_0x^n$, the window becomes all zeros after $n$ steps and L4 returns 0, which is correct.

## Ties for the largest modulus

The hypothesis cannot be dropped. For $p = x^2 - 1$ the power sums are $2, 0, 2, 0, \dots$, so every other ratio is undefined and the others are 0. For a dominant conjugate pair $re^{\pm i\theta}$ with $0 < \theta < \pi$ and no other root of that modulus, $s_j = 2m|r|^j\cos(j\theta) + o(|r|^j)$, and the ratios $|r|\cos((j+1)\theta)/\cos(j\theta)$ do not converge. In both cases the method only stops at the cap.

## Termination

Each pass of the loop L2 either returns at L4 or L7 or ends with $k$ increased; L8 returns after $K$ passes. The rescaling keeps the window's largest entry equal to 1 in absolute value, so no term overflows. When the run stops at L7, the theorem gives an error bound only through $\lambda$, which the method does not know: a small change of the ratio is evidence of convergence, not a proof, and the page's pitfalls give the estimate $|\rho_k - \rho_{k-1}|\lambda/(1 - \lambda)$ that holds asymptotically when $r_2$ is the only subdominant root. In floating point the recurrence and the rounded coefficients add noise to the ratios; its size is observed in the tests, not bounded here.
