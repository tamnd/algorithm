---
title: The Lagrange form gives the interpolating polynomial, and its computed value has a small backward error in the data
proves: [correctness, termination, rounding-error]
status: full
---

We use the notation of the page: distinct nodes $x_0, \ldots, x_n$, data $y_0, \ldots, y_n$, and $\ell_i(t) = \prod_{j \ne i} (t - x_j)/(x_i - x_j)$.

## Claim 1: termination and the value in exact arithmetic

The two loops of lines L2 and L4 run over the fixed ranges $0, \ldots, n$, so the procedure ends after $(n + 1)^2$ passes of the inner loop. In the pass for index $i$, line L3 sets $\ell = 1$. Each pass of line L5 with $j \ne i$ multiplies $\ell$ by $(t - x_j)/(x_i - x_j)$; the denominator is not zero because the nodes are distinct. After the inner loop, $\ell = \ell_i(t)$. Line L6 adds $y_i \ell_i(t)$ to $p$, so after the outer loop, by induction on $i$, $p = \sum_{i=0}^{n} y_i \ell_i(t)$. Line L7 returns this value.

## Claim 2: the value is $p_n(t)$

Let $L(x) = \sum_{i=0}^{n} y_i \ell_i(x)$, a function of $x$.

*Degree.* Each $\ell_i$ is a product of $n$ linear factors in $x$, divided by the nonzero constant $\prod_{j \ne i} (x_i - x_j)$. So $\ell_i \in \mathcal{P}_n$, and $L$ is a linear combination of elements of $\mathcal{P}_n$, so $L \in \mathcal{P}_n$.

*Interpolation.* Fix a node $x_k$. For $i \ne k$, the product $\ell_i(x_k)$ has the factor $j = k$, which is $(x_k - x_k)/(x_i - x_k) = 0$. For $i = k$, each factor is $(x_k - x_j)/(x_k - x_j) = 1$. So $\ell_i(x_k) = \delta_{ik}$ and $L(x_k) = y_k$.

*Uniqueness.* If $q \in \mathcal{P}_n$ also has $q(x_k) = y_k$ for all $k$, then $L - q \in \mathcal{P}_n$ has the $n + 1$ distinct roots $x_0, \ldots, x_n$. A nonzero polynomial of degree at most $n$ has at most $n$ roots ([factor theorem](/factor-theorem/)), so $L - q = 0$.

Hence $L = p_n$, the unique interpolating polynomial, and by Claim 1 the procedure returns $p_n(t)$. In particular, when the data come from a polynomial of degree at most $n$, the procedure reproduces that polynomial exactly in exact arithmetic.

## Claim 3: rounding errors

Assume the standard model of [floating-point arithmetic](/floating-point-model/): each operation gives $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$, no underflow or overflow occurs, and $(5n + 1) u < 1$. Write $\gamma_k = k u / (1 - k u)$. Then the computed value $\hat p$ satisfies
$$\hat p = \sum_{i=0}^{n} y_i\, \ell_i(t)\, (1 + \theta_i), \qquad |\theta_i| \le \gamma_{5n+1},$$
and so
$$|\hat p - p_n(t)| \le \gamma_{5n+1} \sum_{i=0}^{n} |y_i\, \ell_i(t)| \le \gamma_{5n+1}\, \Lambda_n \max_i |y_i| \quad \text{for } t \in [a, b].$$

*Proof.* Fix $i$. One pass of line L5 computes $\mathrm{fl}(\mathrm{fl}(\ell \cdot \mathrm{fl}(t - x_j)) / \mathrm{fl}(x_i - x_j))$, which equals
$$\ell \cdot \frac{t - x_j}{x_i - x_j} \cdot \frac{(1 + \alpha)(1 + \beta)(1 + \delta)}{1 + \varepsilon}$$
with $|\alpha|, |\beta|, |\delta|, |\varepsilon| \le u$ (one rounding each for the two subtractions, the product and the quotient). If $t = x_j$, the factor is an exact zero and the claim holds trivially for this $i$. After the $n$ passes, the computed $\hat\ell_i$ is $\ell_i(t)$ times a product of $4n$ factors of the form $(1 + \delta_k)^{\pm 1}$. The product in line L6 adds one more factor. The sum of line L6 starts from $p = 0$, and $\mathrm{fl}(0 + a) = a$, so the term of index $i$ meets at most $n$ further additions, each of which multiplies it by one more factor $1 + \delta_k$ (the usual analysis of recursive summation). So each term carries at most $5n + 1$ factors. By Lemma 3.1 of Higham (Accuracy and Stability, second edition), a product of $k$ factors $(1 + \delta_j)^{\pm 1}$ with $|\delta_j| \le u$ and $ku < 1$ equals $1 + \theta_k$ with $|\theta_k| \le \gamma_k$. This gives the first display, and the second follows by subtracting $p_n(t) = \sum_i y_i \ell_i(t)$ and using $\sum_i |\ell_i(t)| \le \Lambda_n$. $\blacksquare$

The first display says that $\hat p$ is the exact value at $t$ of the interpolant of perturbed data $y_i (1 + \theta_i)$: the method is backward stable with respect to the data, with a componentwise relative perturbation of at most $\gamma_{5n+1}$. Rounding errors in the nodes themselves are not covered; the nodes are taken as exact floating-point numbers.
