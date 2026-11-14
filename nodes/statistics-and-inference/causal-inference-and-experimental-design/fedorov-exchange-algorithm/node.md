---
tag: 75MV1N
kind: algorithm
slug: fedorov-exchange-algorithm
name: Fedorov exchange algorithm
aliases:
- Fedorov algorithm
- point exchange algorithm
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Builds an exact D-optimal design by swapping a design point for a candidate point whenever the swap increases the determinant of the information matrix.
model: real-ram
complexity:
  vars: {n: the number of candidate points, N: the number of runs, p: the number of model parameters, T: the number of exchanges made}
  time: {worst: "O((T + 1)(p^3 + n p^2 + N n p))", best: "Θ(p^3 + n p^2 + N n p)"}
  space: {extra: "Θ(n + p^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1972
  people: [Valerii V. Fedorov]
  note: Fedorov's book on the theory of optimal experiments gave the exchange of one design point for one candidate point, with the closed-form ratio of the determinants, for designs with a fixed number of runs.
prereqs: [optimal-experimental-design, kiefer-wolfowitz-equivalence-theorem, sherman-morrison-formula, determinant, hill-climbing]
see_also: [khachiyans-algorithm, minimum-volume-enclosing-ellipsoid, response-surface-methodology, factorial-design, local-search-problem, woodbury-identity]
sources:
  - book: "V. V. Fedorov, Theory of Optimal Experiments, translated and edited by W. J. Studden and E. M. Klimko, Academic Press, 1972"
    locator: The whole book (the exchange procedure for designs with a fixed number of runs and the determinant ratio of one exchange; general locator)
  - paper: doi:10.1080/00401706.1980.10486162
    title: "R. Dennis Cook and Christopher J. Nachtsheim, A comparison of algorithms for constructing exact D-optimal designs, Technometrics 22(3), 1980, pp. 315 to 324"
    locator: The whole paper (the comparison of exchange algorithms and the modified Fedorov algorithm)
  - paper: "Toby J. Mitchell, An algorithm for the construction of D-optimal experimental designs, Technometrics 16(2), 1974, pp. 203 to 210"
    locator: The whole paper (the DETMAX algorithm and its excursions)
  - paper: doi:10.1080/00401706.1995.10485889
    title: "Ruth K. Meyer and Christopher J. Nachtsheim, The coordinate-exchange algorithm for constructing exact optimal experimental designs, Technometrics 37(1), 1995, pp. 60 to 69"
    locator: The whole paper (exchange of one coordinate at a time without a candidate list)
  - paper: doi:10.1214/aoms/1177696809
    title: "Henry P. Wynn, The sequential generation of D-optimum experimental designs, Annals of Mathematical Statistics 41(5), 1970, pp. 1655 to 1664"
    locator: The whole paper (adding the point of largest variance; the approximate design version)
  - book: isbn:9780199296606
    title: A. C. Atkinson, A. N. Donev and R. D. Tobias, Optimum Experimental Designs, with SAS, Oxford University Press, 2007
    locator: Chapter 12 (algorithms for the construction of exact D-optimum designs)
---

The Fedorov exchange algorithm builds a D-optimal design with a fixed number of runs $N$, chosen from a finite list of candidate settings. It starts from any design whose information matrix $M = X^\top X$ is nonsingular. In each pass it looks at every pair of a design point $x_i$ and a candidate $x$, and computes in closed form the factor $1 + \Delta(x_i, x)$ by which $\det M$ would change if $x$ replaced $x_i$. It makes the best exchange and repeats until no exchange raises the determinant. It is a local search, a form of [hill climbing](/hill-climbing/), on a problem that is NP-hard in general (see [optimal experimental design](/optimal-experimental-design/)), so the result is a local optimum. In practice it is run from several random starts.

## In plain words

You have a budget of runs and a list of settings you could use. You start with any plan that lets the model be fitted. Then you look for one swap: take out one run and put in a run at another setting, so that the plan gets better. There is a quick formula that says how much better each swap would make the plan, so you do not need to refit anything to compare swaps. You do the best swap and look again. When no swap helps, you stop. The plan you end with cannot be improved by one swap, but a better plan that needs several swaps at once can still exist, so people restart from several plans and keep the best.

## The problem

**Input.** A list of $n$ candidate vectors $f(c_1), \dots, f(c_n) \in \mathbb R^p$ (the regression functions at the candidate settings), a number of runs $N \ge p$, a starting design: a list of $N$ candidate indices whose $X^\top X$ is nonsingular, and a threshold $\varepsilon \ge 0$.

**Output.** A design $x_1, \dots, x_N$ (repeats allowed) from which no single exchange of a design point for a candidate raises $\det X^\top X$ by a factor larger than $1 + \varepsilon$.

**Notation.** $M = X^\top X = \sum_{i=1}^Nf(x_i)f(x_i)^\top$, $A = M^{-1}$, $d(u, v) = f(u)^\top Af(v)$ and $d(u) = d(u, u)$. Here $d(x)\sigma^2$ is the variance of the fitted mean at $x$, and $d(x_i)$ is the leverage of the design point $x_i$. Exchanging $x_i$ for $x$ multiplies the determinant by

$$\frac{\det M'}{\det M} = 1 + \Delta(x_i, x), \qquad \Delta(x_i, x) = d(x) - d(x_i) - \bigl(d(x)d(x_i) - d(x, x_i)^2\bigr).$$

The first two terms say: bring in a point of high variance, take out a point of low variance. The bracket corrects for the overlap of the two points. It is at least 0 by the Cauchy-Schwarz inequality in the inner product given by $A$.

## The algorithm

```pseudo id=main
FEDOROV-EXCHANGE(F[1..n], start[1..N], ε)
L1  D ← start;  M ← Σ_{i=1..N} F[D[i]] F[D[i]]ᵀ        ▷ must be nonsingular
L2  repeat
L3      A ← M⁻¹
L4      for each design position i and candidate j:
            Δ(i, j) ← d(j) - d(D[i]) - (d(j)·d(D[i]) - d(j, D[i])²)   ▷ d(u, v) = F[u]ᵀ A F[v]
L5      (i*, j*) ← a pair with the largest Δ
L6      if Δ(i*, j*) ≤ ε: return D
L7      M ← M - F[D[i*]] F[D[i*]]ᵀ + F[j*] F[j*]ᵀ;  D[i*] ← j*
```

Line L4 computes $d(j)$ once per candidate and $AF[D[i]]$ once per design point, so each $\Delta$ costs one dot product of length $p$. Line L3 can be replaced by two Sherman-Morrison updates of $A$ after each exchange, which cost $\Theta(p^2)$ instead of $\Theta(p^3)$.

## Example

Quadratic regression, $f(x) = (1, x, x^2)$, $p = N = 3$, candidates $-1, -\frac34, \dots, 1$ (9 points), $\varepsilon = 0$, start $\{-\frac12, 0, \frac12\}$. Then $\det M = 1/16$ (the square of the Vandermonde determinant $\frac12 \cdot 1 \cdot \frac12$) and

$$A = M^{-1} = \begin{pmatrix} 1 & 0 & -4 \\ 0 & 2 & 0 \\ -4 & 0 & 24 \end{pmatrix}.$$

With $N = p$, every design point has leverage $d(x_i) = 1$, so $\Delta(x_i, x) = d(x, x_i)^2 - 1$, and $d(x, x_i)$ is the Lagrange basis polynomial of $x_i$ through the design points. For $x_i = -\frac12$ it is $2x(x - \frac12)$:

| candidate $x$ | $-1$ | $-\frac34$ | $-\frac12$ | $-\frac14$ | $0$ | $\frac14$ | $\frac12$ | $\frac34$ | $1$ |
|---|---|---|---|---|---|---|---|---|---|
| $\Delta(-\frac12, x)$ | 8 | 161/64 | 0 | $-55/64$ | $-1$ | $-63/64$ | $-1$ | $-55/64$ | 0 |

The largest $\Delta$ over all pairs is 8. It is reached by four pairs; the scan order picks $-\frac12 \to -1$, and $\det M$ becomes $9 \cdot \frac1{16} = \frac9{16}$. In the second pass, for the design $\{-1, 0, \frac12\}$, the best exchange is $\frac12 \to 1$ with $\Delta = 55/9$, and $\det M$ becomes $\frac9{16} \cdot \frac{64}9 = 4$. In the third pass every $\Delta \le 0$, and the algorithm returns $\{-1, 0, 1\}$. An exhaustive search over the 165 multisets of 3 candidates confirms that 4 is the largest determinant, and $3\,d(x) = 3 - \frac92x^2(1 - x^2) \le 3$ on $[-1, 1]$, which is the equivalence condition of the [Kiefer-Wolfowitz theorem](/kiefer-wolfowitz-equivalence-theorem/) for the approximate design with weights $1/3$.

**A local optimum.** For the second-order model in two factors, $f = (1, x_1, x_2, x_1x_2, x_1^2, x_2^2)$, with $N = 6$ runs on the grid $\{-1, 0, 1\}^2$, the best design has $\det X^\top X = 256$ (by exhaustive search over 3003 designs). The design $\{(-1, 1), (0, 1), (-1, 0), (0, -1), (1, 1), (1, 0)\}$ has $\det X^\top X = 64$, and no single exchange improves it, so the algorithm stops there when it reaches it. From 100 random nonsingular starts (seed 20261114), 94 runs ended at 256 and 6 at 64, with at most 3 exchanges per run. For $N = 7$ all 100 runs reached the best value 960.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By the matrix determinant lemma (the [Sherman-Morrison formula](/sherman-morrison-formula/) page) applied twice, adding $f(x)$ multiplies $\det M$ by $1 + d(x)$, and removing $f(x_i)$ from the result multiplies it by $1 - d(x_i) + d(x, x_i)^2/(1 + d(x))$; the product is $1 + \Delta(x_i, x)$. So the algorithm makes an exchange only when it multiplies $\det M$ by more than $1 + \varepsilon \ge 1$. The determinant stays positive, so $M$ stays invertible. A design cannot appear twice because the determinant strictly increases, and there are finitely many designs, so the loop stops. When it stops, no single exchange raises the determinant by more than the factor $1 + \varepsilon$. For $\varepsilon > 0$ the number of exchanges is at most $\log(D_{\max}/D_0)/\log(1 + \varepsilon)$, where $D_0$ and $D_{\max}$ are the starting and the largest determinants.

The algorithm does not prove global optimality. The certificate for that is the approximate theory: if $\max_xN\,d(x) = p$ over the region, the exact design is also an optimal approximate design and therefore globally D-optimal among exact designs with $N$ runs; otherwise, the D-efficiency $(\det(X^\top X/N)/\det M^*)^{1/p}$ against the approximate optimum $M^*$ is a lower bound for its efficiency among exact designs with $N$ runs.

## Complexity

One pass costs $\Theta(p^3)$ for $A$, $\Theta(np^2)$ for $d(x)$ at all candidates, $\Theta(Np^2)$ for $Af(x_i)$ at the design points, and $\Theta(Nnp)$ for all $Nn$ cross terms: $\Theta(p^3 + np^2 + Nnp)$ with $N \le n$. With Sherman-Morrison updates instead of line L3, the $p^3$ term drops to $p^2$ per exchange. The number of passes $T + 1$ has no good bound in general; in exact arithmetic it is at most the number of designs, $\binom{n + N - 1}N$, and with a threshold $\varepsilon$ it is at most $1 + \log(D_{\max}/D_0)/\log(1 + \varepsilon)$. In practice it is small: in the runs above, at most 4. Extra space is $\Theta(p^2)$ for $A$ and $\Theta(n)$ for the values $d(x)$.

## Properties

- **Monotone.** $\det M$ strictly increases at every exchange.
- **Invariant to the parametrization.** Replacing $f$ by $Tf$ with $T$ nonsingular multiplies every determinant by $(\det T)^2$, so the ratios $1 + \Delta$ and the whole run do not change.
- **Local optimality.** The result is optimal with respect to one exchange. It depends on the start and on the order in which ties are broken.
- **Exact arithmetic.** With rational candidates and $\varepsilon = 0$, every quantity is rational and the run is exact, as in the implementation.
- **No refitting.** The responses are not used. The whole run depends only on the candidate vectors, the start and $\varepsilon$.

## Variants and improvements

- **Modified Fedorov (Cook and Nachtsheim 1980).** Visit the design points in turn and make the best exchange for each, so that one pass can make up to $N$ exchanges. It needs about the same work per pass and fewer passes.
- **Wynn-Mitchell and DETMAX (Mitchell 1974).** Add the point of largest variance and then remove the point of smallest variance; DETMAX allows longer excursions through designs of $N \pm k$ points before it returns to $N$.
- **$k$-exchange.** Consider only the $k$ design points of lowest leverage for removal, which cuts the cost of a pass.
- **Coordinate exchange (Meyer and Nachtsheim 1995).** Change one coordinate of one design point at a time over its levels, without a candidate list. The candidate list grows exponentially with the number of factors, so this is the method used in most design software for many factors.
- **Approximate designs.** Adding weight at the point of largest variance, without removing a point, is the vertex direction method of Wynn (1970) and Fedorov (1972), the same iteration as [Khachiyan's algorithm](/khachiyans-algorithm/) for the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/). It converges to the approximate optimum.
- **Other criteria.** The same exchange idea works for A-, I- and other criteria, with an update formula for each.

## When to use it

Use it when the region is irregular, the model is not one of the standard ones, or the run budget does not fit a classical design: a constrained region, a mixture with bounds, a model with selected interaction terms, or an odd number of runs. For a first-order model on a cube or a standard second-order model, classical designs such as a [factorial design](/factorial-design/) or the central composite designs of [response surface methodology](/response-surface-methodology/) are already D-optimal or close to it. With many factors, use coordinate exchange instead of a candidate list.

## Pitfalls

- **Local optima.** One run proves nothing about global optimality. Use many random starts, and compare with the approximate optimum.
- **Singular starts.** The start must have a nonsingular $X^\top X$; with $N$ close to $p$ random starts are often singular and must be redrawn.
- **The candidate list.** The result is only as good as the list. A coarse grid misses the optimum: for a cubic model on $[-1, 1]$ the D-optimal support is $\pm1$ and $\pm1/\sqrt5$, which a grid of step $0.1$ cannot contain.
- **Floating point.** With floats, Δ values near 0 can make the loop cycle between designs of equal determinant. Use $\varepsilon > 0$, such as $10^{-9}$.
- **Model dependence.** The design is optimal for the assumed model only. The D-optimal 3-run design for a quadratic model, $\{-1, 0, 1\}$, leaves no degrees of freedom to detect a cubic term or to estimate $\sigma^2$.

## Implementations

## History

The approximate theory of Kiefer (1959) and Kiefer and Wolfowitz (1960) gave the optimality conditions. Wynn (1970) and Fedorov (1972) turned them into the iteration that adds the point of largest variance, and Fedorov (1972) gave the exchange for a fixed number of runs, with the closed-form ratio of determinants. Mitchell (1974) gave DETMAX, Cook and Nachtsheim (1980) compared the exchange methods and gave the modified Fedorov algorithm, and Meyer and Nachtsheim (1995) gave coordinate exchange.

## References
