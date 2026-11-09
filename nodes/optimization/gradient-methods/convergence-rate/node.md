---
tag: G31YFA
kind: concept
slug: convergence-rate
name: Convergence rate
aliases:
- linear convergence
- sublinear convergence
- order of convergence
- rate of convergence of an optimization method
area: optimization/gradient-methods
level: intro
summary: How fast the error of an iterative method goes to zero, classified as sublinear (like 1/k), linear (like q^k), superlinear or quadratic. The class sets the number of steps for accuracy ε.
prereqs: [order-of-convergence]
see_also: [order-of-convergence, quadratic-convergence, gradient-descent-convergence-theorem, linear-convergence-strongly-convex, condition-number-of-an-optimization-problem, first-order-lower-bound, nesterov-accelerated-gradient, bfgs]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.3, Convergence of sequences of real numbers (q-linear, q-superlinear and q-order convergence)
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Chapter 9, Rates of convergence, general (Q-factors, R-factors, Q-order and R-order)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 1 and Chapter 2 (the sublinear and linear rates of gradient methods, and the matching lower bounds)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 3, Line search methods, Section 3.3, Rate of convergence (steepest descent, Newton and quasi-Newton methods)
---

The convergence rate of an iterative method says how fast an error measure $e_k$ goes to zero as the step count $k$ grows. In optimization $e_k$ is most often $f(x_k) - f^*$, $\|x_k - x^*\|$ or $\|\nabla f(x_k)\|$. The main classes are *sublinear* ($e_k \le C/k^p$), *linear* ($e_k \le C q^k$ with $q < 1$), *superlinear* ($e_{k+1}/e_k \to 0$) and *quadratic* ($e_{k+1} \le M e_k^2$). The class gives the number of steps for accuracy $\varepsilon$: order $1/\varepsilon$ or $1/\sqrt{\varepsilon}$ for sublinear rates, order $\log(1/\varepsilon)$ for linear rates, and order $\log\log(1/\varepsilon)$ for quadratic rates.

## In plain words

An iterative method makes a guess, improves it, and repeats. The rate tells how the remaining error shrinks from one round to the next.

With a slow rate, each new correct digit costs more rounds than the last one: going from one correct digit to six can take a million rounds. With a linear rate, each round removes the same fraction of the error, so each new correct digit costs the same number of rounds. With a quadratic rate, the number of correct digits doubles each round, so a handful of rounds is enough once the guess is close. A method with a faster rate can still be slower in total if each round costs much more work.

## The idea

Let $e_k \ge 0$ be an error measure of the iterate $x_k$, with $e_k \to 0$.

**Sublinear rates.** The bound $e_k \le C/k^p$ for some $p > 0$, with $e_{k+1}/e_k \to 1$ allowed. To reach $e_k \le \varepsilon$ it is enough to take $k \ge (C/\varepsilon)^{1/p}$. [Gradient descent](/gradient-descent/) on convex $L_f$-smooth functions has $f(x_k) - f^* \le L_f R^2/(2k)$ ([convergence theorem](/gradient-descent-convergence-theorem/)), and [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/) has $2 L_f R^2/(k+1)^2$. Subgradient methods on nonsmooth convex functions have $O(1/\sqrt{k})$.

**Linear rates.** The sequence converges *Q-linearly* with factor $q \in (0, 1)$ if $e_{k+1} \le q\, e_k$ for all large $k$, and *R-linearly* with factor $q$ if $e_k \le C q^k$ for a constant $C$. Q-linear implies R-linear; the converse fails (see the examples). With $e_k \le C q^k$, accuracy $\varepsilon$ needs

$$k \ge \frac{\ln(C/\varepsilon)}{\ln(1/q)}, \quad \text{and } \frac{1}{1 - q}\ln\frac{C}{\varepsilon} \text{ steps are always enough,}$$

because $\ln(1/q) \ge 1 - q$. For gradient descent on a $\mu$-strongly convex function, $q = 1 - 1/\kappa$ with the [condition number](/condition-number-of-an-optimization-problem/) $\kappa = L_f/\mu$, so the count is $\kappa \ln(C/\varepsilon)$ ([linear convergence theorem](/linear-convergence-strongly-convex/)). Accelerated methods have $q = 1 - 1/\sqrt{\kappa}$ and need about $\sqrt{\kappa}\ln(C/\varepsilon)$ steps. Some authors call a linear rate "geometric" or "exponential", since $q^k = e^{-k\ln(1/q)}$.

**Superlinear and higher order.** The rate is *Q-superlinear* if $e_{k+1}/e_k \to 0$, and of *Q-order* $p > 1$ if $e_{k+1} \le M e_k^p$ for large $k$. Order 2 is [quadratic convergence](/quadratic-convergence/). With order $p$, the number of correct digits grows by the factor $p$ each step, so the count is about $\log_p \log(1/\varepsilon)$ once the iterates are close. Newton's method has local order 2, the [secant method](/secant-method/) has order $(1 + \sqrt{5})/2 \approx 1.618$, and [BFGS](/bfgs/) is Q-superlinear near a minimizer with a positive definite Hessian. The general theory of orders is on the page on [order of convergence](/order-of-convergence/).

**Which error.** The class can depend on the error measure. For $\mu$-strongly convex and $L_f$-smooth $f$ without constraints,

$$\frac{\mu}{2}\|x - x^*\|^2 \le f(x) - f^* \le \frac{L_f}{2}\|x - x^*\|^2 \quad\text{and}\quad 2\mu (f(x) - f^*) \le \|\nabla f(x)\|^2 \le 2 L_f (f(x) - f^*),$$

so an R-linear rate in one of the three measures gives an R-linear rate with the same factor in the others (for distances, the square root of the factor), but a Q-linear rate need not stay Q-linear. For convex $f$ without strong convexity, a bound on $f(x_k) - f^*$ gives no bound on $\|x_k - x^*\|$ at all.

**Global and local.** A *global* rate holds from every start point, often with constants that depend on the start. A *local* rate holds only after the iterates come near $x^*$. Newton's method and BFGS have fast local rates and need a line search or a trust region for global convergence.

**Rates and lower bounds.** A rate is an upper bound for a method on a class of functions. The [first-order lower bound](/first-order-lower-bound/) shows that on convex $L_f$-smooth functions no first-order method has a rate better than order $L_f R^2/k^2$ in high dimension, so the rate $1/k^2$ of Nesterov's method is optimal for that class.

## Examples

Steps to go from error $1$ to error $10^{-6}$:

| rate | rule or bound | steps |
|---|---|---|
| sublinear, $p = 1$ | $e_k = 1/k$ | $10^6$ |
| sublinear, $p = 2$ | $e_k = 1/k^2$ | $10^3$ |
| linear, $q = 0.9$ | $e_k = 0.9^k$ | $132$ |
| linear, $q = 0.5$ | $e_k = 0.5^k$ | $20$ |
| superlinear, order $1.618$ | $e_{k+1} = e_k^{1.618}$, $e_0 = 0.5$ | $7$ |
| quadratic | $e_{k+1} = e_k^2$, $e_0 = 0.5$ | $5$ |

The quadratic sequence is $0.5, 0.25, 0.0625, 0.0039, 1.5 \cdot 10^{-5}, 2.3 \cdot 10^{-10}$: the count of correct digits roughly doubles each step.

- **R-linear but not Q-linear.** Let $e_{2j} = e_{2j+1} = 4^{-j}$. Then $e_k \le 2 \cdot 2^{-k}$ for all $k$, so the rate is R-linear with factor $1/2$. But the ratio $e_{k+1}/e_k$ takes the values $1$ and $1/4$ in turn, so there is no $q < 1$ with $e_{k+1} \le q e_k$, and the rate is not Q-linear. The function values of [heavy ball momentum](/momentum-method/) and of accelerated methods behave like this: they converge fast but do not decrease at each step.
- **Linear rate on a quadratic.** On $f(x) = \frac12(x_1^2 + 10 x_2^2)$, gradient descent with step $2/11$ multiplies the error by $9/11 \approx 0.818$ in each coordinate at each step, and [exact line search](/exact-line-search/) from $(10, 1)$ multiplies $f(x_k)$ by exactly $(9/11)^2 \approx 0.669$ per step.
- **The cost per step matters.** Newton's method needs a linear solve with the Hessian, $O(n^3)$ arithmetic for a dense $n \times n$ system, at each step. A gradient step costs $O(n)$ beyond the gradient. For large $n$ and moderate accuracy, many cheap linear steps can be faster than a few expensive quadratic ones.

## Where it is used

- The choice of method for [unconstrained smooth minimization](/unconstrained-smooth-minimization/): the rate on the class of the problem (convex, strongly convex, nonconvex) and the cost per step decide.
- Stopping rules: with a known linear factor $q$, the error bound $C q^k$ tells when to stop.
- Complexity theory of optimization: oracle complexity is the inverse of the rate, and lower bounds such as the [first-order lower bound](/first-order-lower-bound/) are statements about the best possible rate.
- Root finding and linear algebra use the same words for [fixed-point iteration](/fixed-point-iteration/), the [Newton-Raphson method](/newton-raphson-method/) and the [conjugate gradient method](/conjugate-gradient-method/).

## References
