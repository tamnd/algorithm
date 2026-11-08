---
title: The second barycentric form returns the interpolating polynomial, with a forward error bounded through the Lebesgue function
proves: [correctness, termination, rounding-error]
status: full
---

We use the notation of the page: distinct nodes $x_0, \ldots, x_n$, data $y_0, \ldots, y_n$, the node polynomial $\omega(x) = \prod_{j=0}^{n} (x - x_j)$, the Lagrange basis $\ell_j(x) = \prod_{k \ne j} (x - x_k)/(x_j - x_k)$ and the weights $w_j = 1/\prod_{k \ne j} (x_j - x_k)$.

## Claim 1: termination and the weights

The loops of lines L1 and L3 run over fixed ranges, so lines L1 to L4 end after $(n + 1)^2$ passes, and the loop of line L6 ends after at most $n + 1$ passes. For a fixed $j$, line L2 sets $w[j] = 1$ and each pass of line L4 with $k \ne j$ divides it by $x_j - x_k \ne 0$. So after the inner loop $w[j] = w_j$.

## Claim 2: the returned value is $p_n(t)$

*Case 1: $t$ is a node.* If $t = x_m$, the loop of line L6 reaches some index $j$ with $x_j = t$ (the first such index, which is $m$ since the nodes are distinct) and line L7 returns $y_m = p_n(x_m)$.

*Case 2: $t$ is not a node.* Then $\omega(t) \ne 0$ and, for every $j$,
$$\ell_j(t) = \frac{\prod_{k \ne j} (t - x_k)}{\prod_{k \ne j} (x_j - x_k)} = \frac{\omega(t)}{t - x_j}\, w_j.$$
Lines L8 and L9 accumulate $\mathit{num} = \sum_j q_j y_j$ and $\mathit{den} = \sum_j q_j$ with $q_j = w_j/(t - x_j) = \ell_j(t)/\omega(t)$. So $\mathit{num} = p_n(t)/\omega(t)$ by the Lagrange form of $p_n$. The constant data $y_j = 1$ are interpolated by the constant polynomial 1, and by the [uniqueness theorem](/interpolating-polynomial-uniqueness/) $\sum_j \ell_j = 1$, so $\mathit{den} = 1/\omega(t) \ne 0$. Line L10 returns $\mathit{num}/\mathit{den} = p_n(t)$.

In particular, if the data are the values of a polynomial of degree at most $n$, the procedure returns that polynomial's value, exactly in exact arithmetic.

## Claim 3: rounding errors

Assume the standard model $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$ for $\circ \in \{+, -, \times, /\}$, no underflow or overflow, the weights computed by lines L1 to L4 from the stored nodes, $t$ not a node, and $(3n + 3) u < 1$. Write $\theta_k$ for any quantity with $|\theta_k| \le \gamma_k = ku/(1 - ku)$; by Higham's Lemma 3.1, a product $\prod_{i=1}^{k} (1 + \delta_i)^{\pm 1}$ with $|\delta_i| \le u$ equals $1 + \theta_k$.

*Weights.* Each pass of line L4 rounds one subtraction and one division, so $\hat w_j = w_j (1 + \theta_{2n})$.

*Terms.* Line L8 rounds the subtraction $t - x_j$ and the division, so $\hat q_j = q_j (1 + \theta_{2n+2})$, and the product in line L9 gives $\mathrm{fl}(\hat q_j y_j) = q_j y_j (1 + \theta_{2n+3})$.

*Sums.* In a running sum started at 0 the first addition is exact, and each term then meets at most $n$ further roundings. So
$$\widehat{\mathit{num}} = \sum_j q_j y_j (1 + \alpha_j), \quad |\alpha_j| \le \gamma_{3n+3}, \qquad \widehat{\mathit{den}} = \sum_j q_j (1 + \beta_j), \quad |\beta_j| \le \gamma_{3n+2}.$$

*Quotient.* Since $q_j = \ell_j(t)/\omega(t)$,
$$\widehat{\mathit{num}} = \frac{p_n(t) + N}{\omega(t)}, \quad N = \sum_j \ell_j(t) y_j \alpha_j, \qquad \widehat{\mathit{den}} = \frac{1 + \varepsilon}{\omega(t)}, \quad \varepsilon = \sum_j \ell_j(t) \beta_j.$$
With $S_y = \sum_j |\ell_j(t) y_j|$ and $S_1 = \sum_j |\ell_j(t)|$ we have $|N| \le \gamma_{3n+3} S_y$ and $|\varepsilon| \le \gamma_{3n+2} S_1 < 1$ by hypothesis. The final division gives $\hat p = \frac{p_n(t) + N}{1 + \varepsilon}(1 + \delta)$ with $|\delta| \le u$. Write $p = p_n(t)$. Then
$$\hat p - p = \frac{(p + N)(1 + \delta) - p(1 + \varepsilon)}{1 + \varepsilon} = \frac{N(1 + \delta) + p\delta - p\varepsilon}{1 + \varepsilon},$$
so
$$|\hat p - p| \le \frac{(1 + u)\gamma_{3n+3} S_y + (u + \gamma_{3n+2} S_1)|p|}{1 - \gamma_{3n+2} S_1}.$$
For $t \in [a, b]$ we have $S_1 \le \Lambda_n$, which gives the bound on the page. $\square$

The bound is a forward error bound. $S_y \le S_1 \max_j |y_j|$, so for nodes with a small Lebesgue constant the computed value is accurate to a few times $nu\Lambda_n \max_j |y_j|$. The test file checks the bound on random data, with $p$, $S_y$ and $S_1$ computed exactly in rational arithmetic from the stored floating-point nodes, data and point.
