---
title: Aitken's process is exact on geometric errors, accelerates every sequence whose error ratio tends to a limit other than 1, and only halves the error of s + a/k
proves: [correctness, termination, acceleration]
status: full
---

We use the notation of the page: terms $s_k$, limit $s$, errors $e_k = s_k - s$, and for each $k$ the quantities $a = \Delta s_k$, $b = \Delta s_{k+1}$, $d = b - a = \Delta^2 s_k$ of lines L2 to L4.

## Claim 1: termination and the output of lines L5 and L6

The loop of line L1 runs $N - 1$ times (none if $N < 2$), and each pass does a fixed number of operations. Line L6 divides only when $d \ne 0$.

## Claim 2: equivalent forms and affine invariance

If $d \ne 0$, then
$$s_{k+2} - \frac{b^2}{d} = \frac{s_{k+2}(b - a) - b^2}{d} = \frac{s_{k+2}(s_{k+2} - 2s_{k+1} + s_k) - (s_{k+2} - s_{k+1})^2}{d} = \frac{s_k s_{k+2} - s_{k+1}^2}{s_{k+2} - 2s_{k+1} + s_k},$$
where the last step expands the numerator: $s_{k+2}^2 - 2s_{k+1}s_{k+2} + s_k s_{k+2} - s_{k+2}^2 + 2s_{k+1}s_{k+2} - s_{k+1}^2$. The same computation with $s_k - a^2/d$ gives the same fraction. If every term is replaced by $\alpha s_j + \beta$ with $\alpha \ne 0$, then $a, b, d$ are multiplied by $\alpha$ and $t_k = s_{k+2} - b^2/d$ becomes $\alpha s_{k+2} + \beta - \alpha b^2/d = \alpha t_k + \beta$. Taking $\alpha = 1$, $\beta = -s$:
$$t_k - s = \frac{e_k e_{k+2} - e_{k+1}^2}{e_{k+2} - 2e_{k+1} + e_k}. \qquad (*)$$

## Claim 3: exactness on geometric errors, and the kernel

If $e_j = c\lambda^j$ with $c \ne 0$ and $\lambda \notin \{0, 1\}$, then the numerator of $(*)$ is $c^2\lambda^{2k+2} - c^2\lambda^{2k+2} = 0$ and the denominator is $c\lambda^k(\lambda - 1)^2 \ne 0$, so $t_k = s$ for every $k$. Conversely, if $e_k \ne 0$, $d \ne 0$ and $t_k = s$, then $e_k e_{k+2} = e_{k+1}^2$; with $\lambda = e_{k+1}/e_k$ this gives $e_{k+2} = \lambda^2 e_k$, so the three errors are in geometric progression, and $\lambda \ne 1$ because $d \ne 0$. For a constant sequence, $a = b = d = 0$ and line L5 returns $s_{k+2} = s$.

## Claim 4: acceleration when the error ratio has a limit other than 1

Assume $e_j \ne 0$ for all $j$, and $\rho_j = e_{j+1}/e_j \to \lambda$ with $\lambda \ne 1$. Substituting $e_{k+1} = \rho_k e_k$ and $e_{k+2} = \rho_{k+1}\rho_k e_k$ in $(*)$,
$$t_k - s = \frac{e_k^2 \rho_k(\rho_{k+1} - \rho_k)}{e_k(\rho_k\rho_{k+1} - 2\rho_k + 1)}, \qquad \frac{t_k - s}{e_k} = \frac{\rho_k(\rho_{k+1} - \rho_k)}{\rho_k\rho_{k+1} - 2\rho_k + 1}.$$
The denominator tends to $\lambda^2 - 2\lambda + 1 = (\lambda - 1)^2 \ne 0$, so it is nonzero for all large $k$; there $d = e_k(\rho_k\rho_{k+1} - 2\rho_k + 1) \ne 0$ and $t_k$ is defined by line L6. The numerator tends to $\lambda(\lambda - \lambda) = 0$. Hence $(t_k - s)/e_k \to 0$. If $\lambda \ne 0$, then $e_{k+2}/e_k = \rho_{k+1}\rho_k \to \lambda^2 \ne 0$, so also $(t_k - s)/e_{k+2} \to 0$: $t_k$ beats even the newest term it uses. The hypothesis holds for every linearly convergent sequence with a limiting ratio ($0 < |\lambda| < 1$), for alternating series whose terms decrease regularly ($\lambda = -1$), and for divergent sequences with $|\lambda| > 1$, where $t_k$ tends to the anti-limit $s$.

## Claim 5: two geometric modes

Let $e_j = c_1\lambda_1^j + c_2\lambda_2^j$ with $c_1 c_2 \ne 0$, $\lambda_1 \ne 1$ and $|\lambda_1| > |\lambda_2| > 0$. The numerator of $(*)$ is
$$(c_1\lambda_1^k + c_2\lambda_2^k)(c_1\lambda_1^{k+2} + c_2\lambda_2^{k+2}) - (c_1\lambda_1^{k+1} + c_2\lambda_2^{k+1})^2 = c_1 c_2 \lambda_1^k\lambda_2^k(\lambda_1 - \lambda_2)^2,$$
since the squared terms cancel and the cross terms give $c_1c_2\lambda_1^k\lambda_2^k(\lambda_1^2 + \lambda_2^2 - 2\lambda_1\lambda_2)$. The denominator is $c_1\lambda_1^k(\lambda_1 - 1)^2 + c_2\lambda_2^k(\lambda_2 - 1)^2 = c_1\lambda_1^k(\lambda_1 - 1)^2(1 + o(1))$. Therefore
$$t_k - s = c_2 \Big(\frac{\lambda_1 - \lambda_2}{\lambda_1 - 1}\Big)^2 \lambda_2^k (1 + o(1)),$$
so one pass removes the dominant mode and leaves an error of the order of the second.

## Claim 6: logarithmic convergence is not accelerated

Let $s_k = s + a/k$ for $k \ge 1$ with $a \ne 0$. Then $\Delta s_k = -\frac{a}{k(k+1)}$ and $\Delta^2 s_k = \frac{2a}{k(k+1)(k+2)}$, so
$$t_k = s_k - \frac{(\Delta s_k)^2}{\Delta^2 s_k} = s + \frac{a}{k} - \frac{a(k + 2)}{2k(k+1)} = s + \frac{a}{2(k+1)},$$
and $(t_k - s)/(s_k - s) = \frac{k}{2(k+1)} \to \frac12$, not 0. Here $\rho_k = k/(k+1) \to 1$, the case excluded in Claim 4.
