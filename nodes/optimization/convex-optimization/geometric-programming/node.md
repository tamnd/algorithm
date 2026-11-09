---
tag: B2HTAM
kind: problem
slug: geometric-programming
name: Geometric programming
aliases:
- GP
- geometric program
- posynomial programming
area: optimization/convex-optimization
level: advanced
summary: Minimize posynomials subject to posynomial constraints, convex after a change of variables.
prereqs: [convex-optimization-problem]
see_also: [convex-optimization-problem, log-sum-exp-trick, monomial, jensens-inequality, interior-point-method, linear-programming-problem, lagrangian-duality, shannon-entropy]
sources:
  - paper: doi:10.1073/pnas.47.4.537
    title: Clarence Zener, A mathematical aid in optimizing engineering designs, Proceedings of the National Academy of Sciences 47(4), 1961
    locator: pages 537 to 539
  - paper: doi:10.1287/opre.10.5.668
    title: R. J. Duffin, Cost minimization problems treated by geometric means, Operations Research 10(5), 1962
    locator: pages 668 to 675
  - paper: doi:10.1007/s11081-007-9001-7
    title: Stephen Boyd, Seung-Jean Kim, Lieven Vandenberghe and Arash Hassibi, A tutorial on geometric programming, Optimization and Engineering 8(1), 2007
    locator: pages 67 to 127
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.5 (geometric programming), Section 5.7 (examples of duals, including the unconstrained geometric program)
  - paper: doi:10.1007/BF02614382
    title: K. O. Kortanek, Xiaojie Xu and Yinyu Ye, An infeasible interior-point algorithm for solving primal and dual geometric programs, Mathematical Programming 76, 1997
    locator: pages 155 to 181
  - paper: doi:10.1287/opre.1050.0254
    title: Stephen P. Boyd, Seung-Jean Kim, Dinesh D. Patil and Mark A. Horowitz, Digital circuit optimization via geometric programming, Operations Research 53(6), 2005
    locator: pages 899 to 932
  - paper: doi:10.1109/TWC.2007.05960
    title: Mung Chiang, Chee Wei Tan, Daniel P. Palomar, Daniel O'Neill and David Julian, Power control by geometric programming, IEEE Transactions on Wireless Communications 6(7), 2007
    locator: pages 2640 to 2651
  - paper: doi:10.1007/s11590-019-01422-z
    title: Akshay Agrawal, Steven Diamond and Stephen Boyd, Disciplined geometric programming, Optimization Letters 13(5), 2019
    locator: pages 961 to 976
---

A geometric program (GP) minimizes a posynomial, a sum of terms $c\,x_1^{a_1}\cdots x_n^{a_n}$ with $c > 0$ and real exponents, over positive variables, subject to upper bounds on posynomials and equations between [monomials](/monomial/). In the variables $x$ the problem is usually not convex. After the change of variables $x_j = e^{u_j}$ and taking logarithms, every posynomial becomes a log-sum-exp function, which is convex, and every monomial becomes a linear function. So a GP is a [convex optimization problem](/convex-optimization-problem/) in disguise and can be solved to global optimality by [interior-point methods](/interior-point-method/). The name comes from the inequality between the arithmetic and the geometric mean, which gives the dual problem. GPs model sizes, rates and powers in circuit design, wireless networks, aircraft design and inventory models.

## In plain words

Many design costs are sums of terms like "a constant times width times height divided by length". Such a cost can curve in awkward ways, so a search can get stuck. A geometric program is a problem built only from such terms, with all quantities positive. The trick is to measure every quantity on a log scale, the way a slide rule does. On that scale, a product turns into a sum, and the cost turns into a smooth bowl. A bowl has only one lowest point, so a good method finds the true best design and can prove it.

## Definition

**Monomials and posynomials.** For $x \in \mathbb{R}^n_{>0}$, a monomial is $g(x) = c\,x_1^{a_1}x_2^{a_2}\cdots x_n^{a_n}$ with $c > 0$ and $a \in \mathbb{R}^n$. A posynomial is a sum of monomials, $f(x) = \sum_{k=1}^K c_kx^{a_k}$. Products and positive powers of posynomials are posynomials, and the quotient of a posynomial by a monomial is a posynomial.

**Input.** Posynomials $f_0, \dots, f_p$ and monomials $g_1, \dots, g_q$, given by their coefficients and exponent vectors.

**Problem.**

$$\min_{x > 0}\ f_0(x) \quad\text{s.t.}\quad f_i(x) \le 1\ (i = 1, \dots, p), \qquad g_j(x) = 1\ (j = 1, \dots, q).$$

**Output.** An optimal $x^*$ to a given accuracy, or a certificate that the problem is infeasible. The infimum need not be attained, for example for $\min 1/x$.

**The convex form.** Put $x_j = e^{u_j}$, and write the terms of $f_i$ as $e^{a_{ik}^\top u + b_{ik}}$ with $b_{ik} = \log c_{ik}$. Taking logarithms gives

$$\min_u\ \log\sum_ke^{a_{0k}^\top u + b_{0k}} \quad\text{s.t.}\quad \log\sum_ke^{a_{ik}^\top u + b_{ik}} \le 0, \qquad G u + h = 0.$$

The function $\log\sum_ke^{z_k}$ is convex (see the [log-sum-exp trick](/log-sum-exp-trick/)), and convexity is kept by an affine change of the argument. So the problem is convex. A GP whose posynomials are all monomials becomes a linear program in $u$.

**The dual.** For an unconstrained GP $\min_x\sum_{k=1}^Kc_kx^{a_k}$, the dual is

$$\max_\delta\ \prod_{k=1}^K\Big(\frac{c_k}{\delta_k}\Big)^{\delta_k} \quad\text{s.t.}\quad \delta \ge 0,\ \sum_k\delta_k = 1,\ \sum_k\delta_ka_k = 0.$$

Weak duality is the weighted AM-GM inequality, a case of [Jensen's inequality](/jensens-inequality/): for weights $\delta$ with these constraints,

$$\sum_kc_kx^{a_k} = \sum_k\delta_k\frac{c_kx^{a_k}}{\delta_k} \ge \prod_k\Big(\frac{c_kx^{a_k}}{\delta_k}\Big)^{\delta_k} = \prod_k\Big(\frac{c_k}{\delta_k}\Big)^{\delta_k}x^{\sum_k\delta_ka_k} = \prod_k\Big(\frac{c_k}{\delta_k}\Big)^{\delta_k}.$$

Equality holds when all the ratios $c_kx^{a_k}/\delta_k$ are equal, so at an optimum, $\delta_k$ is the share of term $k$ in the optimal cost. The number $K - n - 1$ is the degree of difficulty. When it is $0$ and the exponent vectors are in general position, the dual constraints fix $\delta$, and the problem is solved by linear algebra.

## Variants

- **Generalized GP.** Allow the maximum of posynomials, positive fractional powers of posynomials and compositions of them. They reduce to GPs with extra variables.
- **Signomial programming.** Allow negative coefficients. The problem is no longer convex in log variables. Local methods solve a sequence of GPs, each made by replacing parts of the signomials by monomial approximations.
- **Mixed-integer GP.** Some variables take values in a discrete set, as for gate sizes from a cell library.
- **Robust GP.** The coefficients lie in an uncertainty set, and the constraints must hold for all of them. Some cases reduce to GPs, and others need approximations.

## Examples

**An unconstrained GP.** Minimize $f(x, y) = \frac{4}{xy} + x + 2y$ over $x, y > 0$. The exponent vectors are $(-1, -1)$, $(1, 0)$ and $(0, 1)$, so $K = 3$, $n = 2$ and the degree of difficulty is $0$. The dual constraints are $\delta_1 + \delta_2 + \delta_3 = 1$, $-\delta_1 + \delta_2 = 0$ and $-\delta_1 + \delta_3 = 0$, so $\delta = (\tfrac13, \tfrac13, \tfrac13)$, and the dual value is $(12 \cdot 3 \cdot 6)^{1/3} = 216^{1/3} = 6$. So $f \ge 6$ everywhere. Each term at the optimum is $\delta_k \cdot 6 = 2$, which gives $x = 2$ and $y = 1$, with $f(2, 1) = 2 + 2 + 2 = 6$. The gap is $0$. In $u = \log x$ and $v = \log y$, the function is $4e^{-u - v} + e^u + 2e^v$, and its gradient $(-4e^{-u-v} + e^u,\ -4e^{-u-v} + 2e^v)$ is $0$ at $(\log 2, 0)$.

**Not convex in $x$.** The monomials $\sqrt{x}$ and $xy$ are not convex functions of $x$ and $(x, y)$, and the monomial equation $xy = 1$ defines a hyperbola, which is not a convex set. So a GP can have a nonconvex objective and a nonconvex feasible set. In log variables, $\log\sqrt{x} = \tfrac12u$ and the equation becomes the line $u + v = 0$.

**A constraint.** Minimize $\frac{1}{xy}$ subject to $\frac{x}{2} + \frac{y}{2} \le 1$. The answer is $x = y = 1$ with the value $1$. In the dual with constraints, the objective term has the weight $\delta_0 = 1$, the two constraint terms have the weights $\delta_1 = \delta_2 = 1$ from the equations of the exponents, and the constraint gets the factor $\lambda^\lambda$ with $\lambda = \delta_1 + \delta_2 = 2$. The dual value is $1 \cdot \tfrac12 \cdot \tfrac12 \cdot 2^2 = 1$, which proves optimality.

**Inventory.** The economic order quantity model minimizes the cost per unit time $\frac{KD}{Q} + \frac{hQ}{2}$ of ordering with a fixed cost $K$, a demand rate $D$ and a holding cost $h$. Here $\delta = (\tfrac12, \tfrac12)$, the two costs are equal at the optimum, and the minimum cost is $\sqrt{2KDh}$, at $Q^* = \sqrt{2KD/h}$.

## Known algorithms

- **Interior-point methods on the convex form.** The log-sum-exp constraints have self-concordant barriers through the exponential cone, so path-following methods reach accuracy $\varepsilon$ in a number of Newton steps that grows with the square root of the barrier parameter times $\log(1/\varepsilon)$. Kortanek, Xu and Ye (1997) gave a primal-dual method for the GP and its dual. Commercial and open-source conic solvers handle GPs this way.
- **Dual methods.** Solve the dual GP, which has linear constraints and a concave objective, and recover $x$ from the term shares. With zero degree of difficulty the dual is a linear system (Duffin, 1962).
- **Modeling with disciplined GP.** Modeling tools check that a problem is built from GP rules and do the change of variables automatically (Agrawal, Diamond and Boyd, 2019).
- **Condensation for signomial programs.** Approximate each posynomial denominator by a monomial using the AM-GM inequality at the current point, solve the resulting GP, and repeat. This finds a local solution.

## Bounds

- **Polynomial time to any accuracy.** The convex form has a self-concordant barrier whose parameter is linear in the number of terms, so interior-point methods solve a GP to accuracy $\varepsilon$ in time polynomial in the input size and $\log(1/\varepsilon)$, given bounds on the solution.
- **No exact rational answer in general.** The optimal values are products of powers such as $\sqrt{2KDh}$, so only approximations can be computed in general.
- **Signomial programs are hard.** With negative coefficients, the problem contains the minimization of a quadratic form over the positive part of the simplex, so it is NP-hard in general, by the [Motzkin-Straus theorem](/motzkin-straus-theorem/).

## Reductions

- **GP to convex optimization.** The change of variables $x = e^u$ and the logarithm, as above.
- **LP to GP.** An LP $\min c^\top u$ subject to $a_i^\top u \le b_i$ is the GP $\min x^c$ subject to $e^{-b_i}x^{a_i} \le 1$, with $x = e^u$. Each posynomial has one term.
- **The dual and entropy.** In the logarithm, the dual objective is $\sum_k\delta_k\log c_k - \sum_k\delta_k\log\delta_k$, a linear term plus the [entropy](/shannon-entropy/) of $\delta$. So the GP dual is an entropy maximization problem with linear constraints, and the two are solved together.
- **GP to exponential cone programs.** Each term bound $e^{z_k - t} \le s_k$ is an exponential cone constraint, which is how conic solvers accept GPs.

## Applications

- **Circuit design.** Gate and wire sizing of digital circuits to meet delay, power and area targets, where delays in the RC model are posynomials of the sizes (Boyd, Kim, Patil and Horowitz, 2005). Analog amplifier design also uses GP.
- **Wireless networks.** Power control to maximize the signal-to-interference ratios at high SINR (Chiang, Tan, Palomar, O'Neill and Julian, 2007).
- **Engineering design.** The original use by Zener (1961) and Duffin (1962) was the cost of engineering designs, such as heat exchangers. Aircraft design and structural design follow the same pattern.
- **Operations research.** Inventory models, such as the economic order quantity, and queueing systems.
- **Information theory.** The Lagrange duals of channel capacity and rate distortion problems are GPs (Chiang and Boyd, 2004).

## References
