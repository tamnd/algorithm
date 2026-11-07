---
title: Correctness of the Jenkins-Traub algorithm
proves: [correctness, termination, convergence-rate]
status: full
---

This page proves, in exact arithmetic, the key identity behind the method, the linear convergence of stage 2, and the order $1 + \varphi$ of stage 3 near a root. It also proves termination of the reference code. The global statement that the full three-stage scheme converges is due to Jenkins and Traub (1970), and it is cited rather than reproved.

## Setting

Let $p$ be monic of degree $n \ge 2$ with $p(0) \ne 0$ (zero roots are stripped at L1). Let its distinct roots be $\alpha_1, \dots, \alpha_r$, with multiplicities $m_1, \dots, m_r$. Put $P_i(z) = p(z)/(z - \alpha_i)$. Each $P_i$ is monic of degree $n - 1$, and $P_i(\alpha_j) = 0$ for $j \ne i$ while $P_i(\alpha_i) \ne 0$ when $m_i = 1$. For any polynomial $H$ of degree at most $n - 1$ and any $s$ with $p(s) \ne 0$, define
$$T_s H(z) = \frac{1}{z - s}\left(H(z) - \frac{H(s)}{p(s)}p(z)\right).$$
The bracket vanishes at $z = s$, so $T_sH$ is a polynomial of degree at most $n - 1$.

## Lemma 1 (the weights)

$T_sP_i = P_i/(\alpha_i - s)$. Hence, if $H = \sum_i c_iP_i$, then $T_sH = \sum_i c_iP_i/(\alpha_i - s)$.

*Proof.* $P_i(z) - \dfrac{P_i(s)}{p(s)}p(z) = p(z)\left(\dfrac{1}{z - \alpha_i} - \dfrac{1}{s - \alpha_i}\right) = p(z)\dfrac{s - z}{(z - \alpha_i)(s - \alpha_i)}.$ Dividing by $z - s$ gives $P_i(z)/(\alpha_i - s)$. Linearity gives the second claim. $\square$

Also $p'(z) = \sum_i m_iP_i(z)$, by logarithmic differentiation. So $H^{(0)} = p'/n$ has weights $m_i/n > 0$. After $M$ steps with $s = 0$ the weights are proportional to $m_i\alpha_i^{-M}$, all nonzero, and normalising $H$ (dividing by its leading coefficient $\sum_i c_i$) only rescales them. In floating point, the normalisation keeps the numbers in range.

## The estimate

For $H = \sum c_iP_i$ with $C = \sum_i c_i \ne 0$, let $\bar H = H/C$ and $t = s - p(s)/\bar H(s)$. Since $P_i(s) = p(s)/(s - \alpha_i)$,
$$t - s = -\frac{C}{\sum_i c_i/(s - \alpha_i)}. \tag{1}$$
If only $c_1 \ne 0$, then $t - s = \alpha_1 - s$, so $t = \alpha_1$ exactly. This is why the quotient $P_1$ is the target of the iteration.

## Theorem 1 (stage 2 converges linearly)

Fix $s$, and suppose that $\alpha_1$ is the unique root closest to $s$: $|\alpha_1 - s| < |\alpha_i - s|$ for $i \ge 2$. Let $t_\lambda$ be the estimate after $\lambda$ fixed-shift steps. Then $t_\lambda \to \alpha_1$, and
$$|t_\lambda - \alpha_1| = O(\theta^\lambda), \qquad \theta = \max_{i \ge 2}\frac{|\alpha_1 - s|}{|\alpha_i - s|} < 1.$$

*Proof.* By Lemma 1, after $\lambda$ steps $c_i = c_i^{(0)}(\alpha_i - s)^{-\lambda}$ with $c_i^{(0)} \ne 0$. The ratios $\rho_i = c_i/c_1$ satisfy $|\rho_i| = O(\theta^\lambda)$. Put $d = s - \alpha_1$. Dividing the numerator and denominator of (1) by $c_1$,
$$t - \alpha_1 = d - \frac{1 + \sum_{i \ge 2}\rho_i}{1/d + \sum_{i \ge 2}\rho_i/(s - \alpha_i)} = d\,\frac{\sum_{i \ge 2}\rho_i\left(\frac{d}{s - \alpha_i} - 1\right)}{1 + d\sum_{i \ge 2}\rho_i/(s - \alpha_i)}.$$
The numerator is $O(\theta^\lambda)$, and the denominator tends to 1. $\square$

The test checks that the ratio of successive errors approaches $\theta$ on an example.

## Theorem 2 (stage 3 has order $1 + \varphi$)

In stage 3, $H^{(\lambda+1)} = T_{s_\lambda}H^{(\lambda)}$ and $s_{\lambda+1} = s_\lambda - p(s_\lambda)/\bar H^{(\lambda+1)}(s_\lambda)$. Let $e_\lambda = s_\lambda - \alpha_1$, and let $\rho_\lambda = \max_{i \ge 2}|c_i/c_1|$ for the weights of $H^{(\lambda)}$. Let $\delta = \min_{i \ge 2}|\alpha_i - \alpha_1|$. If $|e_\lambda| \le \delta/2$ and $\rho_\lambda$ is small enough, then
$$\rho_{\lambda+1} \le \frac{2}{\delta}\,\rho_\lambda|e_\lambda|, \qquad |e_{\lambda+1}| \le K\,|e_\lambda|\,\rho_{\lambda+1},$$
with a constant $K$ depending on the roots and on $r$. Consequently, $(e_\lambda, \rho_\lambda) \to 0$, and the order of $e_\lambda$ is $(3 + \sqrt5)/2 = 1 + \varphi$.

*Proof.* By Lemma 1, $c_i^{(\lambda+1)}/c_1^{(\lambda+1)} = (c_i/c_1)(\alpha_1 - s_\lambda)/(\alpha_i - s_\lambda)$. Here $|\alpha_1 - s_\lambda| = |e_\lambda|$ and $|\alpha_i - s_\lambda| \ge \delta - |e_\lambda| \ge \delta/2$, which gives the first bound. The second follows from the formula in the proof of Theorem 1, with $d = e_\lambda$ and the weights of $H^{(\lambda+1)}$. Its numerator is at most $\sum_{i \ge 2}|\rho_i|(|d|/(\delta/2) + 1) \le 2r\rho_{\lambda+1}$, and its denominator is at least $1/2$ once $\rho$ is small. Taking logarithms, $E_\lambda = -\log|e_\lambda|$ and $R_\lambda = -\log\rho_\lambda$ satisfy, up to additive constants,
$$R_{\lambda+1} \ge R_\lambda + E_\lambda, \qquad E_{\lambda+1} \ge E_\lambda + R_{\lambda+1} \ge 2E_\lambda + R_\lambda.$$
The matrix $\begin{pmatrix}2 & 1\\ 1 & 1\end{pmatrix}$ has dominant eigenvalue $(3 + \sqrt5)/2 \approx 2.618$, so $E_\lambda$ grows like $(1 + \varphi)^\lambda$. Once both quantities are small, the constants are absorbed and the iteration converges. $\square$

Multiple roots fit the same framework. The expansion uses distinct roots only, the weights start at $m_i$, and nothing in Theorems 1 and 2 requires $m_1 = 1$. In floating point, however, $p(s)$ near a root of multiplicity $m$ is dominated by rounding error once $|e| \approx u^{1/m}$, and the stopping rule accepts $s$ at about that distance.

## What is cited

Theorems 1 and 2 are local. The global theorem of Jenkins and Traub states that, if the root closest to the stage 2 shift is unique and stage 2 runs for enough steps, stage 3 converges to that root. The reference code takes stage 2 only until the weak test at L8 passes, so it relies on the fallback: a failed stage 3 returns to stage 2, and after $L \cdot \text{attempt}$ steps a new shift is tried. The bound $\beta$ comes from the [Cauchy bound](/cauchy-root-bound/) applied to $z^np(1/z)$. Every root satisfies $|\alpha| \ge \beta$, because for $|z| < \beta$ the term $|a_n|$ exceeds $\sum_{k<n}|a_k||z|^{n-k}$.

## Termination

Every step of stages 1, 2 and 3 increases the step counter. Stage 2 checks it against $K$ before each step, and stage 3 receives the remaining budget and never exceeds 10 steps. A run of stage 3 that fails returns to stage 2. The loop over attempts is finite ($\le$ max_shifts attempts of at most $L \cdot \text{attempt}$ steps each). Each successful root reduces the degree by one, and the outer loop ends at degree at most 1. So the algorithm stops after at most $K$ steps plus the bounded work of one stage 3 and one deflation, returning status done, failed or max-iter.
