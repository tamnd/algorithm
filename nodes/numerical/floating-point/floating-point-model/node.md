---
tag: 4A95CM
kind: model
slug: floating-point-model
name: Standard model of floating-point arithmetic
aliases:
- standard model
- rounding model
- standard model of floating-point arithmetic
area: numerical/floating-point
level: core
summary: Each operation returns fl(x op y) = (x op y)(1+δ) with |δ| ≤ u.
prereqs: [floating-point-arithmetic, relative-error]
see_also: [backward-error-analysis, forward-error-analysis, rounding-error-analysis, machine-epsilon, ulp, real-ram, error-free-transformations, floating-point-summation]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.2, Model of Arithmetic (the standard model and its variant with division by 1 + δ); Section 3.1 and Section 3.4, Notation for Error Analysis (Lemma 3.1, the γ_n bound); Section 27.7 on models of arithmetic for non-IEEE machines
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.3.1, Relative error due to rounding (the bound u/(1 + u)); Section 5.1, Preliminaries (5.1.1 floating-point arithmetic models, 5.1.2 notation for error analysis)
  - paper: "J. H. Wilkinson, Error analysis of floating-point computation, Numerische Mathematik 2 (1960), 319-340"
    title: J. H. Wilkinson, Error analysis of floating-point computation
    locator: the rule fl(x op y) = (x op y)(1 + ε) as the basis of the analysis
  - paper: "W. S. Brown, A simple but realistic model of floating-point computation, ACM Transactions on Mathematical Software 7(4) (1981), 445-480"
    title: W. S. Brown, A simple but realistic model of floating-point computation, ACM Transactions on Mathematical Software 7(4) (1981), 445-480
    locator: the axioms of the model and their use for machines that do not round correctly
  - paper: "Claude-Pierre Jeannerod and Siegfried M. Rump, On relative errors of floating-point operations, optimal bounds and applications, Mathematics of Computation 87(310) (2018), 803-819"
    title: Claude-Pierre Jeannerod and Siegfried M. Rump, On relative errors of floating-point operations, optimal bounds and applications, Mathematics of Computation 87(310) (2018), 803-819
    locator: the bound u/(1 + u) and sharper forms of γ_n
---

The standard model of floating-point arithmetic is the rule that each basic operation returns its exact result times $1 + \delta$, with $|\delta|$ at most the unit roundoff $u$, as long as no underflow or overflow occurs. It forgets almost all the structure of [floating-point arithmetic](/floating-point-arithmetic/) and keeps one inequality, and this inequality is enough to prove error bounds for summation, dot products, polynomial evaluation and the main algorithms of linear algebra. It was the basis of Wilkinson's [backward error analysis](/backward-error-analysis/) and is the model of most of Higham's book. IEEE 754 arithmetic satisfies it, and also has properties that the model does not see, which [error-free transformations](/error-free-transformations/) use.

## The machine

**Values.** The machine holds a finite set $\mathbb{F}$ of reals: a floating-point system with base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$. The default is binary64, with $\beta = 2$ and $p = 53$. The unit roundoff is $u = \tfrac12 \beta^{1-p}$, which is $2^{-53}$ for binary64 with rounding to nearest. [Machine epsilon](/machine-epsilon/) is $\varepsilon = 2u$; this page does not use it. $\mathrm{fl}(\cdot)$ is the computed result of an expression. The [ulp](/ulp/) of a real $x$ with $\beta^{e} \le |x| < \beta^{e+1}$ is $\beta^{\max(e, e_{\min}) - p + 1}$ (Muller et al., Section 2.3.2). We write $\gamma_n = nu/(1 - nu)$ for $nu < 1$.

**Steps.** One step applies $\mathbin{op} \in \{+, -, \times, /\}$ to two values $x, y \in \mathbb{F}$, or takes $\sqrt{x}$. The model gives no exact result. It says only that

$$\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta), \qquad |\delta| \le u, \tag{SM}$$

and $\mathrm{fl}(\sqrt{x}) = \sqrt{x}(1 + \delta)$ with $|\delta| \le u$, where $\delta$ may depend on $x$, $y$ and the operation and is otherwise unknown. Each step has its own $\delta$. The hypothesis is that the exact result $x \mathbin{op} y$ is zero or lies in the normal range: its magnitude is at least $\beta^{e_{\min}}$ (no underflow) and at most the largest finite float (no overflow). A second form is also valid, and is sometimes more convenient:

$$\mathrm{fl}(x \mathbin{op} y) = \frac{x \mathbin{op} y}{1 + \delta}, \qquad |\delta| \le u.$$

**Why IEEE 754 arithmetic satisfies (SM).** In IEEE 754 each of these operations is correctly rounded (Clause 5.4.1), so $\mathrm{fl}(x \mathbin{op} y)$ is the exact real $x \mathbin{op} y$ rounded once. The rounding bound on the page [floating-point arithmetic](/floating-point-arithmetic/) gives $|\delta| \le u$ for round to nearest, under the same hypothesis on the range. With a directed rounding, (SM) holds with $u$ replaced by $2u = \beta^{1-p}$. The second form holds for round to nearest because $|\mathrm{fl}(z) - z| \le \tfrac12 \beta^{e-p+1} = u\beta^{e} \le u |\mathrm{fl}(z)|$ when $\beta^{e} \le |z| < \beta^{e+1}$: the float $\beta^{e}$ is at most $|z|$, so rounding gives $|\mathrm{fl}(z)| \ge \beta^{e}$.

**A sharper constant.** With round to nearest, $|\delta| \le u/(1+u)$. *Proof.* Let $\beta^{e} \le |z| < \beta^{e+1}$ with $z$ in the normal range. If $|z| \ge \beta^{e}(1 + u)$, then $|\mathrm{fl}(z) - z| \le \tfrac12\beta^{e-p+1} = u\beta^{e}$ and so the relative error is at most $u\beta^{e}/(\beta^{e}(1+u)) = u/(1+u)$. If $\beta^{e} \le |z| < \beta^{e}(1+u)$, then $|z|$ is closer to $\beta^{e}$ than to the next float $\beta^{e}(1 + 2u)$, or at equal distance with $\beta^e$ even, so $|\mathrm{fl}(z)| = \beta^{e}$ and the relative error is $1 - \beta^{e}/|z| < 1 - 1/(1+u) = u/(1+u)$. At $z = \beta^{e}(1 + u)$ with ties to even, $\mathrm{fl}(z) = \beta^e$ and the bound is attained. $\square$ (Muller et al., Section 2.3.1; Jeannerod and Rump.)

**Underflow.** When the result may be subnormal, the model becomes $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta) + \eta$ with $|\delta| \le u$, $|\eta| \le \tfrac12 \beta^{e_{\min} - p + 1}$ and $\delta\eta = 0$. For addition and subtraction with gradual underflow, $\eta = 0$ always: a sum of two floats whose magnitude is below $\beta^{e_{\min}}$ is a multiple of $\beta^{e_{\min}-p+1}$ that is smaller than $\beta^{e_{\min}}$, so it is itself a subnormal float and is exact. Overflow has no such repair; the model then does not apply.

## What it counts

The model counts two things. The first is the number of floating-point operations (flops), each with unit cost, as in the [real RAM](/real-ram/). The second, which is the point of the model, is the accumulated relative error, as a function of $u$ and the problem size. Bounds are stated with $\gamma_n$, because of this lemma.

**Lemma (Higham, Lemma 3.1).** If $|\delta_i| \le u$ and $\rho_i \in \{+1, -1\}$ for $i = 1, \ldots, n$, and $nu < 1$, then

$$\prod_{i=1}^{n} (1 + \delta_i)^{\rho_i} = 1 + \theta_n, \qquad |\theta_n| \le \gamma_n = \frac{nu}{1 - nu}.$$

*Proof.* Each factor lies in $[1 - u, 1 + u]$ if $\rho_i = 1$, and in $[1/(1+u), 1/(1-u)]$ if $\rho_i = -1$. Since $1 - u \le 1/(1+u)$ and $1 + u \le 1/(1-u)$, each factor lies in $[1 - u, 1/(1-u)]$, so the product $P$ satisfies $(1-u)^n \le P \le (1-u)^{-n}$. Bernoulli's inequality gives $(1-u)^n \ge 1 - nu$. So $P - 1 \le 1/(1 - nu) - 1 = \gamma_n$ and $1 - P \le nu \le \gamma_n$. $\square$

Two consequences follow from the definition: $\gamma_m \le \gamma_n$ for $m \le n$, and $\gamma_m + \gamma_n + \gamma_m \gamma_n \le \gamma_{m+n}$ (Higham, Lemma 3.3), so the $\theta$ terms of two sub-computations combine. The bound $\gamma_n \approx nu$ is a worst case. It is proved for every input and every choice of the $\delta_i$; in practice the errors partly cancel, and the observed error usually grows like $\sqrt{n}\, u$ (Higham, Section 2.8), but this is not a theorem about any given input.

## Relation to other models

- **The [real RAM](/real-ram/).** Same operations and unit costs, but exact results. An algorithm that is correct on the real RAM can fail in floating point; the standard model measures by how much.
- **IEEE 754 correct rounding.** Strictly stronger. It fixes $\mathrm{fl}(x \mathbin{op} y)$ exactly, so it also gives facts that (SM) cannot express: the [Sterbenz lemma](/sterbenz-lemma/) ($y/2 \le x \le 2y$ makes $x - y$ exact), the exactness of the [error-free transformations](/error-free-transformations/) such as [Fast2Sum](/fast-two-sum/), and the representability of the error of $+$ and $\times$. Proofs of such algorithms work in this stronger model, not in (SM).
- **Weaker models.** Some old machines (Cray, and machines with no guard digit) did not satisfy (SM) for subtraction. Higham, Section 2.4, and Brown (1981) give the weaker rule $\mathrm{fl}(x \pm y) = x(1 + \alpha) \pm y(1 + \beta)$, $|\alpha|, |\beta| \le u$, which still supports most backward error results.
- **Models with FMA.** With a [fused multiply-add](/fused-multiply-add/), one more step $\mathrm{fl}(xy + z) = (xy + z)(1 + \delta)$ with $|\delta| \le u$ is allowed, and it counts as one rounding.
- **The [word RAM](/word-ram/).** A float is a word of 64 bits, and the integer view of its bit pattern is used by algorithms such as the [fast inverse square root](/fast-inverse-square-root/); the standard model has no such view.

## Known results in the model

Each bound below assumes the standard model (SM) with no underflow and no overflow, and $nu < 1$. They are proved worst-case bounds; the observed errors are usually much smaller.

| computation | proved bound | where |
|---|---|---|
| product $x_1 x_2 \cdots x_n$, left to right | $\mathrm{fl} = x_1 \cdots x_n (1 + \theta_{n-1})$ | Lemma 3.1 |
| recursive [summation](/floating-point-summation/) of $n$ terms | $\lvert \hat s - s \rvert \le \gamma_{n-1} \sum_i \lvert x_i \rvert$ | Higham, Section 4.2 |
| [pairwise summation](/pairwise-summation/) | $\lvert \hat s - s \rvert \le \gamma_{\lceil \lg n \rceil} \sum_i \lvert x_i \rvert$ | Higham, Section 4.2 |
| [Kahan summation](/kahan-summation/) | $\lvert \hat s - s \rvert \le (2u + O(nu^2)) \sum_i \lvert x_i \rvert$ | Higham, Section 4.3 |
| [dot product](/dot-product/) $x^T y$ | $\lvert \hat s - x^T y \rvert \le \gamma_n \lvert x \rvert^T \lvert y \rvert$ | Higham, Section 3.1 |
| [Horner's rule](/horner-rule/), degree $n$ | $\lvert \hat p(x) - p(x) \rvert \le \gamma_{2n} \sum_i \lvert a_i \rvert \lvert x \rvert^i$ | Higham, Section 5.1 |
| [Gaussian elimination](/gaussian-elimination/) $A = LU$ | $\hat L \hat U = A + \Delta A$, $\lvert \Delta A \rvert \le \gamma_n \lvert \hat L \rvert \lvert \hat U \rvert$ | Higham, Section 9.3 |

**An example of one step.** In binary64, $\mathrm{fl}(0.1 + 0.2) = 0.30000000000000004$, which exceeds the exact sum of the two stored inputs by the relative amount $\delta \approx 9.25 \times 10^{-17} \approx 0.833u$. For $\mathrm{fl}(1/3)$, $\delta = -u/2$ exactly, about $-5.55 \times 10^{-17}$. The sum $1 + 2^{-53}$ is a tie that rounds to $1$, so $\delta = -2^{-53}/(1 + 2^{-53}) = -u/(1+u)$: the sharper bound is attained.

## References
