---
tag: YM0D58
kind: technique
slug: dual-decomposition
name: Dual decomposition
aliases:
- Lagrangian relaxation for MAP
- price decomposition
- Lagrangian decomposition
area: optimization/convex-optimization
level: advanced
summary: Decompose a coupled problem into subproblems coordinated through dual variables.
prereqs: [dual-ascent, lagrangian-duality]
see_also: [lagrangian-relaxation, admm, dantzig-wolfe-decomposition, benders-decomposition, network-utility-maximization, map-inference, bundle-method, shadow-price]
sources:
  - paper: doi:10.1287/opre.11.3.399
    title: Hugh Everett III, Generalized Lagrange multiplier method for solving problems of optimum allocation of resources, Operations Research 11(3), 1963
    locator: pages 399 to 417
  - paper: doi:10.1287/opre.8.1.101
    title: George B. Dantzig and Philip Wolfe, Decomposition principle for linear programs, Operations Research 8(1), 1960
    locator: pages 101 to 111
  - paper: doi:10.1561/2200000016
    title: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011
    locator: Section 2.2 (dual decomposition)
  - paper: doi:10.1109/JSAC.2006.879350
    title: Daniel P. Palomar and Mung Chiang, A tutorial on decomposition methods for network utility maximization, IEEE Journal on Selected Areas in Communications 24(8), 2006
    locator: pages 1439 to 1451
  - paper: doi:10.1057/palgrave.jors.2600523
    title: Frank Kelly, Aman Maulloo and David Tan, Rate control for communication networks, shadow prices, proportional fairness and stability, Journal of the Operational Research Society 49(3), 1998
    locator: pages 237 to 252
  - paper: doi:10.1109/TPAMI.2010.108
    title: Nikos Komodakis, Nikos Paragios and Georgios Tziritas, MRF energy minimization and beyond via dual decomposition, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(3), 2011
    locator: pages 531 to 552
  - paper: doi:10.1613/jair.3680
    title: Alexander M. Rush and Michael Collins, A tutorial on dual decomposition and Lagrangian relaxation for inference in natural language processing, Journal of Artificial Intelligence Research 45, 2012
    locator: pages 305 to 362
  - paper: doi:10.1137/070708111
    title: Angelia Nedić and Asuman Ozdaglar, Approximate primal solutions and rate analysis for dual subgradient methods, SIAM Journal on Optimization 19(4), 2009
    locator: pages 1757 to 1780
  - paper: doi:10.1007/s101070050090
    title: Torbjörn Larsson, Michael Patriksson and Ann-Brith Strömberg, Ergodic, primal convergence in dual subgradient schemes for convex programming, Mathematical Programming 86, 1999
    locator: pages 283 to 312
---

Dual decomposition solves a problem that would split into independent parts if a few coupling constraints were removed. It moves the coupling constraints into the objective with prices $y$, the [Lagrange multipliers](/lagrange-multiplier/). For fixed prices the [Lagrangian](/lagrangian-function/) is a sum of terms in separate variables, so each part is solved alone, often in parallel. A master step then changes the prices to reduce the violation of the coupling constraints, by a gradient or subgradient step on the [dual function](/lagrangian-duality/). Every price vector gives a lower bound on the optimal value, so the method always knows how far it can be from the optimum. The method is the basis of distributed resource allocation, network rate control, [Lagrangian relaxation](/lagrangian-relaxation/) of integer programs and MAP inference in graphical models.

## In plain words

Several teams share a resource, for example a budget. A central office could plan for all teams at once, but that is a large job. Instead, the office sets a price for the resource. Each team plans alone and pays for what it uses. If the teams together ask for more than there is, the office raises the price. If they ask for less, it lowers the price. The teams plan again, and the process repeats. When the total demand matches the supply, the plans together are the best joint plan. The office never needs to know how each team plans, only how much each team asks for. At each round, the plans give a bound that the best joint plan cannot beat.

## When it applies

- The problem has the form $\min \sum_{i=1}^N f_i(x_i)$ subject to $x_i \in X_i$ and $\sum_{i=1}^N A_ix_i = b$ (or $\le b$), where the blocks $x_i$ are linked only by the coupling rows.
- Each subproblem $\min_{x_i \in X_i} f_i(x_i) + y^\top A_ix_i$ is much easier than the whole problem, for example because it is small, has a closed form, or is a shortest path, a tree or a knapsack.
- There are few coupling constraints compared with the number of variables.
- A problem with one shared variable, $\min f_1(x) + f_2(x)$, fits after you copy the variable: $\min f_1(x_1) + f_2(x_2)$ subject to $x_1 - x_2 = 0$.
- For exact convergence of the primal values, the problem must be convex with a zero [duality gap](/lagrangian-duality/). For a nonconvex or integer problem, the method still gives a valid lower bound.

## The template

```pseudo id=main
DUAL-DECOMPOSITION(f₁..f_N, X₁..X_N, A₁..A_N, b, y, α)
L1  repeat for k = 0, 1, 2, ...
L2      for i = 1 to N in parallel
L3          x_i ← argmin over x_i ∈ X_i of  f_i(x_i) + yᵀA_i x_i      ▷ hole: the subproblem solver
L4      r ← Σ_i A_i x_i − b                                           ▷ a supergradient of the dual at y
L5      g ← Σ_i (f_i(x_i) + yᵀA_i x_i) − yᵀb                         ▷ the dual value, a lower bound
L6      x̂ ← a feasible point built from x₁..x_N                       ▷ hole: primal recovery
L7      if f(x̂) − max of all g so far ≤ ε then return x̂
L8      y ← y + α_k r                                                 ▷ hole: the price update
```

**The holes.** Line L3 is any exact solver for the small problem, and the $N$ calls are independent. Line L6 can take the running average of the $x$ values, project $x$ onto the coupling constraints, or run a repair heuristic. Line L8 is a gradient or subgradient step on the dual function. For rows with $\le$, the prices must stay nonnegative, so the update is $y \leftarrow \max(0, y + \alpha_kr)$. The update can also be a [bundle method](/bundle-method/) or a [cutting-plane method](/cutting-plane-method/) on the dual.

**The analysis.** Let $f(x) = \sum_i f_i(x_i)$, let $p^*$ be the optimal value, and let $d(y) = \min_{x \in X} f(x) + y^\top(\sum_iA_ix_i - b)$ be the dual function. Assume that each $X_i$ is convex and compact, each $f_i$ is convex, the constraints are equalities, $d$ has a maximizer $y^*$, and $d(y^*) = p^*$.

1. *Separability.* For a fixed $y$, the term $y^\top b$ is a constant and $f(x) + y^\top\sum_iA_ix_i = \sum_i(f_i(x_i) + y^\top A_ix_i)$. So the minimum over $X = X_1 \times \dots \times X_N$ is the sum of the $N$ separate minima, and line L5 computes $g = d(y)$.
2. *Lower bound.* For each feasible $x$, $d(y) \le f(x) + y^\top \cdot 0 = f(x)$. So $d(y) \le p^*$ for each $y$, which is [weak duality](/lagrangian-duality/). With a feasible $\hat{x}$, the test at line L7 bounds the true error $f(\hat x) - p^*$.
3. *The residual is a supergradient.* For each $y'$, $d(y') \le f(x) + y'^\top r = d(y) + (y' - y)^\top r$, where $x$ is the point from line L3. So line L8 is a step of the subgradient method for the concave function $d$.
4. *Smooth case.* If each $f_i$ is $\mu$-[strongly convex](/strong-convexity/), the point $x$ is unique, $d$ is differentiable with gradient $r$, and the gradient is Lipschitz with constant $\|A\|^2/\mu$ for $A = [A_1 \cdots A_N]$. A fixed step $\alpha = \mu/\|A\|^2$ gives $d^* - d(y_k) = O(1/k)$, as shown on the [dual ascent](/dual-ascent/) page.
5. *Nonsmooth case.* Let $\|r\| \le G$ at every step and $R = \|y_0 - y^*\|$. From fact 3 with $y' = y^*$, $\|y_{k+1} - y^*\|^2 \le \|y_k - y^*\|^2 - 2\alpha_k(d^* - d(y_k)) + \alpha_k^2G^2$. Summing gives
   $$d^* - \max_{j < k} d(y_j) \le \frac{R^2 + G^2\sum_{j<k}\alpha_j^2}{2\sum_{j<k}\alpha_j},$$
   which is $RG/\sqrt{k}$ for the fixed step $\alpha = R/(G\sqrt{k})$.
6. *Primal recovery by averages.* Take a fixed step $\alpha$, $y_0 = 0$, and $\hat x_k = \frac1k\sum_{j<k}x_j$, which lies in $X$. By line L5, $f(x_j) = d(y_j) - y_j^\top r_j \le p^* - y_j^\top r_j$, and $-2\alpha y_j^\top r_j = \|y_j\|^2 - \|y_{j+1}\|^2 + \alpha^2\|r_j\|^2$. Summing and using convexity of $f$:
   $$f(\hat x_k) \le p^* + \frac{\alpha G^2}{2}, \qquad \Big\|\sum_iA_i\hat x_{k,i} - b\Big\| = \frac{\|y_k\|}{k\alpha} \le \frac{2\|y^*\| + \sqrt{k}\,\alpha G}{k\alpha},$$
   where the last step uses $\|y_k - y^*\|^2 \le \|y^*\|^2 + k\alpha^2G^2$ from fact 5. Also $f(\hat x_k) \ge p^* - \|y^*\|\,\|\sum_iA_i\hat x_{k,i} - b\|$. So with $\alpha$ of order $1/\sqrt{k}$, both the objective error and the violation are $O(1/\sqrt{k})$ (Larsson, Patriksson and Strömberg, 1999; Nedić and Ozdaglar, 2009).

### A worked example

Three users share $3$ units of a resource. User $i$ wants the amount $a_i$, with $a = (4, 2, 0)$, and pays $\tfrac12(x_i - a_i)^2$ for a different amount:

$$\min\ \sum_{i=1}^3 \tfrac12(x_i - a_i)^2 \quad\text{s.t.}\quad x_1 + x_2 + x_3 = 3.$$

The answer is $x^* = (3, 1, -1)$ with $p^* = \tfrac32$ and the price $y^* = 1$. For a price $y$, user $i$ solves $\min \tfrac12(x_i - a_i)^2 + yx_i$, so $x_i = a_i - y$. The residual is $r = 3 - 3y$ and the dual value is $d(y) = 3y - \tfrac32y^2$. The dual gradient is Lipschitz with constant $3$. With $y_0 = 0$ and the step $\alpha = \tfrac16$, the update is $y_{k+1} = y_k + \tfrac12(1 - y_k)$, so $y_k = 1 - 2^{-k}$ and $d(y_k) = \tfrac32 - \tfrac32 \cdot 4^{-k}$:

| $k$ | $y_k$ | $x_k$ | residual $r_k$ | lower bound $d(y_k)$ |
|---|---|---|---|---|
| 0 | 0 | (4, 2, 0) | 3 | 0 |
| 1 | 1/2 | (7/2, 3/2, -1/2) | 3/2 | 9/8 |
| 2 | 3/4 | (13/4, 5/4, -3/4) | 3/4 | 45/32 |
| 3 | 7/8 | (25/8, 9/8, -7/8) | 3/8 | 189/128 |
| 4 | 15/16 | (49/16, 17/16, -15/16) | 3/16 | 765/512 |

The users only report their demands, and nobody needs to know the costs of the others. The step $\alpha = \tfrac13$ reaches $y^*$ in one step. Each step $\alpha \ge \tfrac23$ fails: for $\alpha = \tfrac23$ the price jumps between $0$ and $2$ forever.

## Classic examples

- **Resource allocation and [shadow prices](/shadow-price/).** Everett (1963) used one multiplier per shared resource to split allocation problems into one problem per activity. The optimal $y^*$ is the marginal value of one more unit of the resource.
- **[Network utility maximization](/network-utility-maximization/).** Maximize $\sum_s U_s(x_s)$ over source rates $x_s$ subject to link capacities $\sum_{s \ni l}x_s \le c_l$. Each link $l$ keeps a price $y_l \ge 0$ and updates it from its own load, and each source picks the rate that maximizes $U_s(x_s) - x_s\sum_{l \in s}y_l$. Kelly, Maulloo and Tan (1998) studied rate control in communication networks with this model.
- **MAP inference in [Markov random fields](/markov-random-field/).** Split the graph into trees, give each tree a copy of the variables, and require the copies to agree. Each tree is solved exactly by [max-product](/max-product/) or the [Viterbi algorithm](/viterbi-algorithm/), and the prices push the trees toward agreement. The dual is the bound of the local LP relaxation of [MAP inference](/map-inference/) (Komodakis, Paragios and Tziritas, 2011). If the trees agree, the shared answer is an exact MAP assignment. Rush and Collins (2012) used the same idea to combine a parser and a tagger in natural language processing.
- **[Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/).** For a linear program with block structure, a [cutting-plane](/cutting-plane-method/) update of the prices on the dual is the Dantzig-Wolfe method, and the subproblems generate the columns of its master problem.
- **[Multi-commodity flow](/multi-commodity-flow-problem/).** Relax the joint capacity of each arc. For fixed prices, each commodity solves its own shortest-path or min-cost flow problem with arc costs raised by the prices.
- **[Lagrangian relaxation](/lagrangian-relaxation/) of integer programs.** Relax the complicating rows of an integer program, for example the degree constraints of the traveling salesman problem in the [Held-Karp bound](/held-karp-bound/). The best dual value is a lower bound for branch and bound, and it can be strictly below $p^*$.

## Variations

- **Better price updates.** The subgradient step is simple but slow. The [bundle method](/bundle-method/) and the [cutting-plane method](/cutting-plane-method/) use all past residuals and also give a stopping test. Smoothing the subproblems with a small strongly convex term makes the dual smooth, and then accelerated gradient steps apply.
- **Augmented Lagrangian and ADMM.** The [augmented Lagrangian method](/augmented-lagrangian-method/) converges with a fixed step and without strong convexity, but its quadratic term couples the blocks. [ADMM](/admm/) restores the split by updating the blocks one after another.
- **Primal decomposition.** Fix how much of each shared resource each block gets, solve the blocks, and let a master problem change the shares using the block multipliers. [Benders decomposition](/benders-decomposition/) is a form of this idea.
- **Consensus form.** For $\min\sum_if_i(x)$, give each term a copy $x_i$ and the constraints $x_i = z$. The prices then measure how much each copy wants to move.
- **Inequality coupling.** For $\sum_iA_ix_i \le b$, project the prices onto $y \ge 0$ after each step. Everything above still holds, and fact 6 bounds the positive part of the violation.

## Pitfalls

- **The subproblem points need not be feasible, even at the optimal price.** Minimize $-x_1 - x_2$ over $x_1, x_2 \in [0, 1]$ subject to $x_1 + x_2 = 1$, so $p^* = -1$ and $y^* = 1$. Each subproblem minimizes $(y - 1)x_i$. At $y = 1$ every $x_i \in [0, 1]$ is a minimizer, and a solver can return $(1, 1)$ or $(0, 0)$, both infeasible. With $y_0 = 0$ and $\alpha = \tfrac14$, the price rises to $1$ and then jumps between $\tfrac34$ and $1$, while $x$ jumps between $(1, 1)$ and $(0, 0)$. Only the averages converge, to $(\tfrac12, \tfrac12)$. Use primal recovery (fact 6) or a final repair step.
- **Linear or flat subproblems make the dual nonsmooth.** Then a fixed step does not converge, and the subgradient method needs about $1/\varepsilon^2$ steps. Use diminishing steps, a bundle method or smoothing.
- **A too large step.** In the smooth case, keep the step below $2\mu/\|A\|^2$. At this bound the method can fail: in the worked example, $\alpha = \tfrac23$ makes the price jump between $0$ and $2$ forever.
- **Duality gap.** For integer or other nonconvex subproblems, $\max_y d(y)$ can be strictly less than $p^*$, and no price makes the subproblem points feasible and optimal. The method then gives a bound and a starting point for a heuristic, not the answer.
- **Unbounded subproblems.** If a subproblem has no minimizer for some prices, for example a linear $f_i$ on an unbounded $X_i$, the dual value is $-\infty$ there. Bound the sets $X_i$.

## Exercises

1. In the worked example, show that the update is $1 - y_{k+1} = (1 - 3\alpha)(1 - y_k)$, and find all steps $\alpha$ for which the price converges.
2. In the worked example, project $x_k$ onto the plane $x_1 + x_2 + x_3 = 3$. Show that the result is $x^*$ for every $k$, and explain why this fails when the users have costs $\tfrac{w_i}{2}(x_i - a_i)^2$ with different $w_i$.
3. Write the dual decomposition of $\min f_1(x) + f_2(x)$ in the consensus form $x_1 = x_2$, and show that the price update is $y \leftarrow y + \alpha(x_1 - x_2)$. What does a large $y_j$ do to the copy $x_1$ in coordinate $j$?

## References
