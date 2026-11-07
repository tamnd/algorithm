---
tag: 9J0BBH
kind: technique
slug: backward-error-analysis
name: Backward error analysis
aliases:
- Wilkinson analysis
- backward stability
- backward error
area: numerical/floating-point
level: core
summary: Shows the computed result is the exact result for a slightly perturbed input.
prereqs: [floating-point-model, relative-error, condition-number]
see_also: [forward-error-analysis, rounding-error-analysis, numerical-stability, floating-point-summation, gaussian-elimination, householder-reflections, residual, horner-rule]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.5, Backward and Forward Errors; Section 1.6, Conditioning; Chapter 3, Basics (Section 3.1 inner and outer products, Section 3.4 the γ_n notation, Section 3.8 error analysis demystified); Section 7.1 and Section 7.2 (normwise and componentwise backward error of a linear system); Section 9.3 (backward error of LU factorization)
  - paper: "J. H. Wilkinson, Error analysis of floating-point computation, Numerische Mathematik 2 (1960), 319-340"
    title: J. H. Wilkinson, Error analysis of floating-point computation
    locator: the backward analysis of sums, products and the elimination process
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963"
    title: J. H. Wilkinson, Rounding Errors in Algebraic Processes
    locator: Chapter 1 (the fundamental arithmetic operations and the backward analysis of sums and inner products) and Chapter 3 (matrix computations)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 14, Stability, and Lecture 15, More on Stability (backward stability and the accuracy theorem)
---

Backward error analysis is the technique of showing that the result an algorithm computes in [floating-point arithmetic](/floating-point-arithmetic/) is the exact result of the same problem for slightly perturbed data, and of bounding the size of that perturbation. If the perturbation is of the order of the unit roundoff $u$, the algorithm is *backward stable*: it solves a nearby problem exactly, and its error is no worse than the error that the data already have. J. H. Wilkinson developed the method in the 1950s and 1960s and used it to explain why Gaussian elimination with pivoting works. Combined with a [condition number](/condition-number/), a backward error bound gives a bound on the [forward error](/forward-error-analysis/).

## In plain words

When a program computes with rounding, the answer is a little wrong. Forward error analysis asks how far the answer is from the true answer. Backward error analysis asks another question: is the computed answer the exact answer for some input that is very close to the real input?

Often the answer to this second question is yes, and the proof is easier. Then the rounding errors act like a small change of the data. Data from measurements is already uncertain by much more than that, so an algorithm with this property is as good as one can hope for. Whether the answer is then close to the true answer depends on the problem, not on the algorithm: if a tiny change of the input moves the output a lot, no method can be accurate.

## When it applies

- The computation is a sequence of floating-point operations for which the [standard model](/floating-point-model/) $\mathrm{fl}(a \mathbin{op} b) = (a \mathbin{op} b)(1 + \delta)$, $|\delta| \le u$, holds, with no underflow or overflow.
- The problem has data that can absorb perturbations: the entries of a vector or a matrix, the coefficients of a polynomial. A problem with a single scalar input, such as $y = \sin x$, often has too little data to absorb the errors, and then one proves a mixed or a forward bound instead.
- The forward error is hard to bound directly, but a [condition number](/condition-number/) of the problem is known or can be estimated.
- The question is whether the algorithm or the problem is to blame for an inaccurate result.

**Notation.** For a problem $y = f(x)$ and a computed $\hat y$, the (relative, componentwise) backward error is

$$\eta(\hat y) = \min \{\, \epsilon \ge 0 : \hat y = f(x + \Delta x), \ |\Delta x_i| \le \epsilon |x_i| \text{ for all } i \,\},$$

with $\eta = \infty$ if no such $\Delta x$ exists; a normwise version uses $\|\Delta x\| \le \epsilon \|x\|$. An algorithm is backward stable if $\eta(\hat y) \le c\,u$ for every input, with $c$ a modest function of the size of the problem. It is *mixed forward-backward stable* if $\hat y + \Delta y = f(x + \Delta x)$ with $|\Delta y| \le c_1 u |y|$ and $|\Delta x| \le c_2 u |x|$ (Higham, Section 1.5). We use $u = 2^{-53}$ for binary64 with round to nearest and $\gamma_n = nu/(1 - nu)$, as on the page [floating-point arithmetic](/floating-point-arithmetic/).

**The link to the forward error.** If $f$ is differentiable and $\hat y = f(x + \Delta x)$, then to first order $\hat y - y \approx f'(x)\Delta x$, so

$$\frac{|\hat y - y|}{|y|} \lesssim \mathrm{cond}(f, x) \cdot \eta(\hat y), \qquad \mathrm{cond}(f, x) = \left| \frac{x f'(x)}{f(x)} \right|.$$

This rule of thumb, forward error $\lesssim$ condition number $\times$ backward error, is exact in the limit of small perturbations, and for many problems it has a rigorous non-asymptotic form (for linear systems, Higham, Section 7.1).

## The template

```pseudo id=main
BACKWARD-ERROR-ANALYSIS(algorithm A for y = f(x))
L1  for each operation k of A: write its result as (exact op)(1 + δ_k), |δ_k| ≤ u
L2  expand the final result as an exact formula in the data and the δ_k
L3  group the factors on each data item: (1 + δ_a)(1 + δ_b)⋯ = 1 + θ_m, |θ_m| ≤ γ_m
L4  ASSIGN each factor 1 + θ to one data item     ▷ hole: the choice of which data absorb the error
L5  read off ŷ = f(x + Δx) with |Δx| ≤ c u |x| + O(u^2)
L6  ▷ optional: multiply by COND(f, x) for a forward error bound
```

Line L1 is the [standard model](/floating-point-model/). Line L2 is algebra: the computed result is an explicit expression. Line L3 uses Lemma 3.1 of Higham: a product of $m$ factors $(1 + \delta)^{\pm 1}$ with $|\delta| \le u$ is $1 + \theta_m$ with $|\theta_m| \le \gamma_m$. Line L4 is the creative step: the factors must be pushed onto the data in a way that makes the expression equal to $f$ applied to the perturbed data. For a sum or a dot product this is immediate; for a matrix factorization one pushes them onto the entries of $A$. Line L5 gives the backward error, and line L6 converts it into a forward error.

**The template on recursive summation.** Let $\hat s_1 = x_1$ and $\hat s_k = \mathrm{fl}(\hat s_{k-1} + x_k)$. By L1, $\hat s_k = (\hat s_{k-1} + x_k)(1 + \delta_k)$. By induction on $n$ (L2 and L3), $\hat s_n = \sum_{i=1}^n x_i (1 + \theta^{(i)})$ where $x_1$ and $x_2$ carry the $n - 1$ factors $\delta_2, \ldots, \delta_n$, and $x_i$ for $i \ge 3$ carries the $n - i + 1$ factors $\delta_i, \ldots, \delta_n$. So $|\theta^{(1)}|, |\theta^{(2)}| \le \gamma_{n-1}$ and $|\theta^{(i)}| \le \gamma_{n-i+1}$. By L4 and L5,

$$\hat s_n = \sum_{i=1}^n x_i(1 + \theta^{(i)}) = \sum_{i=1}^n (x_i + \Delta x_i), \qquad |\Delta x_i| \le \gamma_{n-1} |x_i|.$$

So recursive summation is backward stable with $\eta \le \gamma_{n-1} \approx (n-1)u$. L6 gives the forward bound $|\hat s_n - s_n| \le \gamma_{n-1} \sum |x_i|$, which is the bound on the page [floating-point summation](/floating-point-summation/).

**A number.** In binary64, adding $\mathrm{fl}(0.1)$ ten times from left to right gives $0.9999999999999999$. The exact sum of the ten stored values is $10\,\mathrm{fl}(0.1) = 1.000000000000000055\ldots$, so the relative forward error is $-1.5u \approx -1.67 \times 10^{-16}$. All terms are positive, so the condition number of the sum is $1$, and the smallest componentwise backward error is also $1.5u$, far below the proved bound $\gamma_9 \approx 9.99 \times 10^{-16}$.

## Classic examples

- **[Floating-point summation](/floating-point-summation/).** As above: $\eta \le \gamma_{n-1}$ for recursive summation and $\eta \le \gamma_{\lceil \lg n \rceil}$ for [pairwise summation](/pairwise-summation/).
- **[Dot product](/dot-product/).** $\mathrm{fl}(x^T y) = (x + \Delta x)^T y$ with $|\Delta x| \le \gamma_n |x|$ (Higham, Section 3.1): each product adds one more factor. The perturbation can be put on $x$ alone, or on $y$ alone.
- **[Horner's rule](/horner-rule/).** The computed value of $p(x) = \sum a_i x^i$ is the exact value of the polynomial with coefficients $a_i(1 + \theta_{2i+1})$ for $i < n$ and $a_n(1 + \theta_{2n})$, so each relative perturbation is at most $\gamma_{2n}$ (Higham, Section 5.1). The data that absorb the error are the coefficients, not $x$.
- **[Back substitution](/back-substitution/).** The computed solution of $Tx = b$ satisfies $(T + \Delta T)\hat x = b$ with $|\Delta T| \le \gamma_n |T|$ (Higham, Chapter 8): the perturbation goes on the matrix, and each row absorbs its own errors.
- **[Gaussian elimination](/gaussian-elimination/).** The computed factors satisfy $\hat L \hat U = A + \Delta A$ with $|\Delta A| \le \gamma_n |\hat L||\hat U|$ (Higham, Section 9.3). This is Wilkinson's main result: elimination is backward stable as long as $|\hat L||\hat U|$ is not much larger than $|A|$, which [partial pivoting](/partial-pivoting/) almost always ensures; the ratio is controlled by the [growth factor](/growth-factor/).
- **[Householder QR](/householder-reflections/).** The computed $\hat R$ is the exact $R$ factor of $A + \Delta A$ with $\|\Delta A\|_F \le c\, n\, u \|A\|_F$ for a small constant $c$ (Higham, Chapter 19; Trefethen and Bau, Lecture 16).

## Variations

- **Normwise and componentwise.** A normwise backward error measures $\|\Delta x\|/\|x\|$; a componentwise one measures $\max_i |\Delta x_i|/|x_i|$ and also keeps zeros and the sparsity of the data. For a linear system $Ax = b$ and an approximate $\hat x$ with [residual](/residual/) $r = b - A\hat x$, both are computable: the normwise backward error is $\|r\|/(\|A\|\|\hat x\| + \|b\|)$ (Rigal and Gaches, 1967) and the componentwise one is $\max_i |r_i|/(|A||\hat x| + |b|)_i$ (Oettli and Prager, 1964). See Higham, Sections 7.1 and 7.2.
- **Mixed forward-backward error.** When the data cannot absorb all errors, one shows $\hat y + \Delta y = f(x + \Delta x)$ with both perturbations small. A library function with a small relative error, $\hat y = f(x)(1 + \delta)$, is of this kind with $\Delta x = 0$.
- **A posteriori analysis.** Instead of a worst-case a priori bound, compute the backward error of the result actually produced, from the residual; this is the basis of the stopping tests of iterative solvers and of [iterative refinement](/iterative-refinement/).
- **Running error analysis.** Accumulate a bound on the error alongside the computation, at the cost of about one more operation per step (Higham, Section 3.3).
- **Structured backward error.** Require that the perturbed data keep a structure, such as symmetry or a Toeplitz form. The structured backward error can be much larger than the unstructured one.

## Pitfalls

- **Backward stable does not mean accurate.** A backward stable algorithm on an ill-conditioned problem can give a result with no correct digit. For a linear system with $\kappa(A) \approx 10^{16}$ in binary64, Gaussian elimination with pivoting gives a tiny residual and a useless $\hat x$. The fault is in the problem, and only more precision or a reformulation helps.
- **Not every simple algorithm is backward stable.** The computed outer product $\mathrm{fl}(x y^T)$ has each entry correct to a relative error $u$, but it is in general not of rank one, so it is not the exact outer product of any perturbed vectors (Higham, Section 3.1). And $\mathrm{fl}(1 + x)$ for $|x| < u$ returns $1 = f(x + \Delta x)$ only with $\Delta x = -x$, a relative backward error of $1$, though the forward error is tiny. Such results are forward stable, not backward stable.
- **Forgetting the assumptions.** The bounds assume no underflow and no overflow, and for the standard model also round to nearest (or $2u$ in place of $u$ for directed rounding). A computation that underflows to zero can lose all accuracy in the affected terms.
- **Constants are worst cases.** The bound $\gamma_{n-1}$ for summation is attained only in contrived cases; with random rounding errors the error usually grows like $\sqrt{n}\,u$. Do not read the constant as a prediction.
- **First order is not a proof.** "Forward error $\lesssim$ cond $\times$ backward error" drops terms of order $u^2$ and higher. For a rigorous bound, use a perturbation theorem that holds for finite perturbations, with its conditions (for example $\kappa(A) \|\Delta A\|/\|A\| < 1$ for linear systems).

## Exercises

1. Show that $\mathrm{fl}(x^T y)$, computed from left to right, equals $\sum_i x_i y_i (1 + \theta^{(i)})$ with $|\theta^{(1)}| \le \gamma_n$ and $|\theta^{(i)}| \le \gamma_{n - i + 2}$ for $i \ge 2$. Conclude that the dot product is backward stable with all the perturbation on $x$.
2. Show that $\mathrm{fl}(a/b)$ and $\mathrm{fl}(\sqrt{a})$ are backward stable in each of their inputs, and that $\mathrm{fl}(a - b)$ is backward stable with the perturbation on both $a$ and $b$ but not, in general, on $a$ alone.
3. For $x = [1, 10^{-16}, -1]$ in binary64, find the computed sum from left to right, its forward error, and its smallest componentwise backward error. Compare with $\gamma_2 \sum |x_i|$. (The sum is $0$, the exact sum is $10^{-16}$, the forward error is total, yet the backward error is at most about $10^{-16}$.)

## References
