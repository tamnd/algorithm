---
tag: 8T5Z9B
kind: algorithm
slug: karmarkar-algorithm
name: Karmarkar's algorithm
aliases:
- projective scaling algorithm
- Karmarkar's projective method
area: optimization/linear-programming
level: advanced
summary: First practical polynomial-time interior-point method for LP (1984).
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, L: the bit length of the input}
  time: {worst: O(n^3.5 L)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1984
  people: [Narendra Karmarkar]
  note: Karmarkar gave the first interior-point method with a polynomial bound that was also claimed to be fast in practice; it started the field of interior-point methods.
prereqs: [linear-programming-problem, lp-standard-form, gram-schmidt-process]
see_also: [interior-point-method, affine-scaling-method, ellipsoid-method, lp-in-p, central-path, barrier-method, simplex-method, dual-linear-program]
sources:
  - paper: doi:10.1007/BF02579150
    title: Narendra Karmarkar, A new polynomial-time algorithm for linear programming, Combinatorica 4(4), 1984
    locator: pages 373 to 395, the canonical form, the projective transformation, the potential function and the bound of O(n^3.5 L) operations
  - paper: doi:10.1007/BF02592025
    title: Philip E. Gill, Walter Murray, Michael A. Saunders, John A. Tomlin and Margaret H. Wright, On projected Newton barrier methods for linear programming and an equivalence to Karmarkar's projective method, Mathematical Programming 36(2), 1986
    locator: pages 183 to 209, the step of Karmarkar's method as a step of a logarithmic barrier method
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 9, Section 9.3 (potential reduction methods) and the notes at the end of Chapter 9
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 14, the introduction and the notes on the history of interior-point methods
---

Karmarkar's algorithm solves a [linear program](/linear-programming-problem/) by moving through the interior of the feasible region, not along its edges as the [simplex method](/simplex-method/) does. At each step a projective map sends the current point to the center of a simplex, the method takes a fixed fraction of a step down the projected cost inside a ball around the center, and then it maps the new point back. A potential function drops by a constant at each step, so $O(nL)$ steps are enough, and the total is $O(n^{3.5} L)$ arithmetic operations. It appeared in 1984 and started the family of [interior-point methods](/interior-point-method/).

## In plain words

The simplex method walks from corner to corner on the surface of the feasible region. Karmarkar's method goes through the inside instead. Near a wall it can only take a small step, so before each step it changes the scale of the space so that the current point sits in the middle, far from every wall. There it can safely take a long step downhill. Then it changes the scale back.

A single number, the potential, measures progress. It mixes the cost with a penalty for being close to a wall. Each step lowers the potential by at least a fixed amount, so the cost falls by a fixed factor every few steps, and after a number of steps that grows only polynomially with the size of the input, the point is close enough to the optimum to round to it.

## The problem

The algorithm works on a program in *Karmarkar's canonical form*:

$$\text{minimize } c^\top x \quad \text{subject to} \quad Ax = 0, \quad e^\top x = 1, \quad x \ge 0,$$

with $x \in \mathbb{R}^n$, $n \ge 3$, the all-ones vector $e$, two promises: $Ae = 0$, so the center $e/n$ of the simplex is feasible; and the optimal value is $0$. The output is a feasible $x > 0$ with $c^\top x \le \varepsilon \, c^\top (e/n)$. For $\varepsilon = 2^{-O(L)}$, a rounding step then gives an exact optimal vertex.

A general program in [standard form](/lp-standard-form/) can be put in this form: add a new variable to make the constraints homogeneous, scale so that the variables sum to $1$, and shift so that $e/n$ is feasible. If the optimal value is not known, either combine the primal and the [dual](/dual-linear-program/) program into one program with optimal value $0$, or use Karmarkar's *sliding objective*, which updates a guess of the value. These steps are routine, and this page uses the canonical form only.

## The algorithm

Let $X = \operatorname{diag}(x)$. The projective map $T(z) = X^{-1} z / (e^\top X^{-1} z)$ sends $x$ to $e/n$, keeps the simplex, and sends the feasible set to $\{y \ge 0 : AXy = 0, e^\top y = 1\}$. The cost becomes $\bar c^\top y$ with $\bar c = Xc$, up to a positive factor. The ball of radius $r = 1/\sqrt{n(n-1)}$ about $e/n$ in the plane $e^\top y = 1$ lies inside the simplex.

```pseudo id=main
KARMARKAR(A, c, ε, α = 1/4)
L1  x ← e/n;  r ← 1/√(n(n − 1))
L2  while cᵀx > ε · cᵀ(e/n)
L3      X ← diag(x);  c̄ ← Xc;  B ← the matrix with rows AX and eᵀ
L4      p ← (I − Bᵀ(BBᵀ)⁻¹B) c̄              ▷ c̄ projected onto the null space of B
L5      if p = 0 then stop: cᵀx is constant on the feasible set
L6      y ← e/n − α r p / ‖p‖                 ▷ a step in the inscribed ball
L7      x ← X y / (eᵀ X y)                      ▷ map back with T⁻¹
L8  return x
```

The progress measure is *Karmarkar's potential*

$$f(x) = n \ln(c^\top x) - \sum_{j=1}^n \ln x_j.$$

The first term pulls toward a low cost, and the second term pushes away from the walls $x_j = 0$. For $\alpha = 1/4$, each step lowers $f$ by at least $1/8$. Since $\sum_j \ln x_j \le n \ln(1/n)$ for $e^\top x = 1$, this gives $c^\top x_k \le e^{-k/(8n)} \, c^\top x_0$ after $k$ steps.

## Example

Minimize $x_2$ subject to $x_1 + x_2 - 2x_3 = 0$, $x_1 + x_2 + x_3 = 1$, $x \ge 0$. Here $Ae = 1 + 1 - 2 = 0$, the feasible set is the segment with $x_3 = 1/3$ and $x_1 + x_2 = 2/3$, and the optimum is $(2/3, 0, 1/3)$ with value $0$.

At step 0, $x = e/3$, $\bar c = (0, 1/3, 0)$, and the null space of $B$ is spanned by $(1, -1, 0)$, so $p = (-1/6, 1/6, 0)$. The step length is $\alpha r = 1/(4\sqrt 6) \approx 0.102$, so $y = e/3 + 0.102 \cdot (1, -1, 0)/\sqrt 2 \approx (0.4055, 0.2612, 0.3333)$. Since $X = I/3$, the map back gives $x = y$.

| step $k$ | $x$ | $c^\top x$ | potential $f(x)$ |
|---|---|---|---|
| 0 | $(0.3333, 0.3333, 0.3333)$ | $0.3333$ | $0$ |
| 1 | $(0.4055, 0.2612, 0.3333)$ | $0.2612$ | $-0.684$ |
| 2 | $(0.4717, 0.1950, 0.3333)$ | $0.1950$ | $-1.420$ |
| 3 | $(0.5266, 0.1401, 0.3333)$ | $0.1401$ | $-2.191$ |
| 4 | $(0.5687, 0.0980, 0.3333)$ | $0.0980$ | $-2.983$ |

The potential drops by about $0.7$ to $0.8$ per step, well above the guaranteed $1/8$. The cost falls by a factor of about $0.7$ per step. After 19 steps $c^\top x \le 10^{-3} \, c^\top x_0$. Note that the steps in $y$ have the same length, but the steps in $x$ get shorter in the coordinate $x_2$ as it nears its wall, because the map back multiplies by $X$.

## Correctness

The map $T$ changes the potential only by a constant, so the drop of $f$ at a step equals the drop of the transformed potential $g(y) = n \ln(\bar c^\top y) - \sum_j \ln y_j$ from $e/n$ to $y$. The linear term drops by at least $\alpha$: the simplex lies in the ball of radius $R = \sqrt{(n-1)/n}$ about $e/n$ and contains the image of an optimal point, where the cost is $0$, so a step of length $\alpha r$ along $-p$ cuts $\bar c^\top y$ by the factor $1 - \alpha r / R = 1 - \alpha/(n-1)$. The barrier term rises by at most $\beta^2 / (2(1 - \beta))$ with $\beta = \alpha\sqrt{n/(n-1)} \le \alpha \sqrt 2$. For $\alpha = 1/4$ the net drop is at least $0.25 - 0.097 > 1/8$. The proof file has the details.

## Complexity

Model: arithmetic operations on reals have unit cost (the [real RAM](/real-ram/)).

- **Steps.** With the drop $\delta = 1/8$, the bound $c^\top x_k \le e^{-k/(8n)} c^\top x_0$ gives $c^\top x_k \le \varepsilon \, c^\top x_0$ after $8n \ln(1/\varepsilon)$ steps. For $\varepsilon = 2^{-O(L)}$ this is $O(nL)$ steps.
- **One step.** The projection of line L4 solves a linear system with the matrix $AX^2A^\top$, which costs $O(n^3)$ with Gaussian elimination. This gives $O(n^4 L)$ in total.
- **Karmarkar's speedup.** The matrix $X$ changes in all entries at each step, but only a little. Karmarkar keeps an approximation $X'$ of $X$ and updates an entry of $X'$ only when it is off by more than a constant factor, with a rank-one update of the inverse for each changed entry. The steps stay valid. Karmarkar showed that there are $O(\sqrt n)$ such updates per step on average, each costing $O(n^2)$. So a step costs $O(n^{2.5})$ on average, and the total is $O(n^{3.5} L)$ operations.
- **Bits.** The numbers need $O(L)$ bits of precision. The paper states a bound of $O(n^{3.5} L^2 \log L \log\log L)$ bit operations.
- **Space.** $O(n^2)$ for the matrix of line L4, besides the input.

## Properties

- **Interior.** Every point $x$ has $x > 0$; the method never touches the boundary, and it returns an approximate point, not a vertex.
- **Polynomial.** It has a polynomial bound in the bit model, like the [ellipsoid method](/ellipsoid-method/), with a better exponent and much better behavior in practice.
- **Scale invariant.** The projective map removes the effect of the units of the variables.
- **Equivalent to a barrier step.** Gill, Murray, Saunders, Tomlin and Wright (1986) showed that the step direction is that of a projected Newton step for a logarithmic [barrier function](/barrier-method/) with a particular parameter.

## Variants and improvements

- **Line search.** Take the step that minimizes the potential along the direction, not the fixed $\alpha = 1/4$. In practice, steps much longer than $\alpha = 1/4$ are possible, and they cut the number of steps by a large factor.
- **[Affine scaling](/affine-scaling-method/).** Drop the projective part and use the scaling $X$ only; this is simpler, works on the standard form directly, and was found to be a rediscovery of Dikin's 1967 method.
- **Potential reduction methods.** Ye's primal-dual potential function gives $O(\sqrt n L)$ steps, better than the $O(nL)$ steps of Karmarkar.
- **Path-following methods.** Methods that follow the [central path](/central-path/) with Newton steps reach $O(\sqrt n L)$ steps and $O(n^3 L)$ operations, and the primal-dual versions are the basis of modern [interior-point solvers](/interior-point-method/).

## When to use it

In practice, use a modern primal-dual [interior-point method](/interior-point-method/) or the [simplex method](/simplex-method/), not the projective method itself. Study Karmarkar's algorithm for its ideas: the projective map to the center, a potential that drops by a constant, and the amortized update of the factorization. Its history matters too, since it turned the attention of the field to interior-point methods.

## Pitfalls

- **Wrong form.** The method needs $Ae = 0$ and the optimal value $0$. If the optimal value is positive, $f$ cannot fall forever, and the analysis breaks. Line L5 detects one case: if $c^\top x$ is constant on the feasible set, the projected cost is $0$.
- **Dependent rows.** If $A$ does not have full row rank, the matrix $BB^\top$ is singular. Remove the dependent rows first, or project with an orthogonal basis, as the implementation does.
- **The step too long.** With $\alpha$ near $1$, the barrier term of the potential may grow faster than the linear term falls, and with $\alpha r \ge$ the distance to a wall, a coordinate becomes $0$ or negative.
- **Stopping without rounding.** The method returns a point near the optimum, not a vertex. If an exact answer is needed, round with a final step that finds a basis.

## Implementations

The Python version works in floats on the canonical form. It projects with a two-pass Gram-Schmidt orthogonal basis of the rows of $B$, which also handles dependent rows. The tests build random programs in canonical form with a known optimal point and value $0$, check the value $0$ by brute force over the basic feasible solutions, and run the method with $\varepsilon = 10^{-8}$. They check that every point is feasible and positive, that the potential drops by at least $1/8$ at each step, that $c^\top x_k \le e^{-k/(8n)} c^\top x_0$, that the step count is within the bound, and that the projective map changes the potential only by a constant.

## History

Narendra Karmarkar, at Bell Laboratories, presented the algorithm at the ACM Symposium on Theory of Computing in 1984, and the full paper appeared in Combinatorica in the same year. Claims that it was much faster than the simplex method received wide attention, and AT&T obtained a patent on it. The claims led to much work on the simplex method and on interior-point methods. Gill, Murray, Saunders, Tomlin and Wright (1986) related it to the logarithmic barrier methods of Frisch and of Fiacco and McCormick from the 1950s and 1960s. Within a few years, path-following primal-dual methods replaced the projective method in practice.

## References
