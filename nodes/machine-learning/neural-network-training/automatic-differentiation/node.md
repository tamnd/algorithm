---
tag: 9QSEWQ
kind: technique
slug: automatic-differentiation
name: Automatic differentiation
aliases:
- autodiff
- algorithmic differentiation
area: machine-learning/neural-network-training
level: core
summary: "Exact derivatives of a program by the chain rule on its trace. Forward mode gives J v per run; reverse mode gives u^T J per run, so a gradient costs a few evaluations."
prereqs: [computational-graph, gradient]
see_also: [backpropagation, backpropagation-through-time, gradient-checking, gradient-checkpointing, straight-line-program, finite-differences, hamiltonian-monte-carlo, taylor-series-method]
sources:
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, Principles and Techniques of Algorithmic Differentiation, second edition, SIAM, 2008
    locator: Chapter 3 (forward and reverse mode), Chapter 4 (memory and complexity bounds; Section 4.6 for the gradient bound) and Chapter 12 (reversal schedules and checkpointing)
  - paper: doi:10.1016/0304-3975(83)90110-X
    title: Walter Baur and Volker Strassen, The complexity of partial derivatives, Theoretical Computer Science 22(3), 1983
    locator: pp. 317 to 330 (a function and all its partial derivatives in at most 3 times the multiplications and divisions of the function)
  - paper: "Atilim Gunes Baydin, Barak A. Pearlmutter, Alexey Andreyevich Radul and Jeffrey Mark Siskind, Automatic differentiation in machine learning: a survey, Journal of Machine Learning Research 18(153), 2018"
    locator: Section 2 (AD versus symbolic and numerical differentiation), Section 3 (forward mode, dual numbers, reverse mode, the evaluation trace of ln(x1) + x1 x2 - sin(x2)) and Section 4 (AD and backpropagation)
  - paper: "Andreas Griewank, Who invented the reverse mode of differentiation?, Documenta Mathematica, Extra Volume ISMP, 2012"
    locator: pp. 389 to 400 (history from Linnainmaa 1970 and Ostrowski, the bound OPS of the gradient at most omega times OPS of f, omega = 3 for multiplications, and memory proportional to the operation count)
  - paper: doi:10.1007/BF01931367
    title: "Seppo Linnainmaa, Taylor expansion of the accumulated rounding error, BIT 16(2), 1976"
    locator: pp. 146 to 160 (the reverse accumulation of first order error coefficients, from his 1970 master's thesis)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.5 (back-propagation and other differentiation algorithms; 6.5.9 differentiation outside the deep learning community, 6.5.10 higher order derivatives)
  - paper: doi:10.1162/neco.1994.6.1.147
    title: "Barak A. Pearlmutter, Fast exact multiplication by the Hessian, Neural Computation 6(1), 1994"
    locator: pp. 147 to 160 (Hessian vector products at the cost of a few gradients)
---

Automatic differentiation (AD) computes the derivatives of a function that is given as a program. It applies the chain rule to each primitive operation of one run of the program, the nodes of its [computational graph](/computational-graph/), so the result is exact up to floating point rounding. *Forward mode* carries a directional derivative along with each value and gives one Jacobian vector product $J v$ per run. *Reverse mode* records the run on a tape and walks it backward, and gives one vector Jacobian product $u^\top J$ per backward sweep. For a scalar loss, reverse mode gives the whole [gradient](/gradient/) for a small constant times the cost of the loss, whatever the number of parameters; [backpropagation](/backpropagation/) is this case for neural networks.

## In plain words

A program that computes a number is a long chain of small steps: sums, products, sines, logarithms. For each small step you know the rule for its rate of change. Automatic differentiation uses only these rules and joins them while the program runs.

There are two ways to join them. In the first way, every value carries a second number: how fast it changes when one chosen input moves. One run then gives the rate for that one input. In the second way, you first run the program and write down every step. Then you go through the list backward and ask, for each value, how much the final result depends on it. One backward pass answers this for all inputs at once. A model with a million weights and one loss needs only the second way, once.

## When it applies

- The function is a program built from primitives whose derivatives are known: arithmetic, $\exp$, $\log$, the trigonometric functions, matrix products, and library kernels with hand-written derivative rules. Loops and branches are allowed. AD differentiates the path that one run takes.
- You need derivative values at given points, not a formula. *Symbolic differentiation* builds an expression for the derivative; it can grow much larger than the program (expression swell), and it does not handle loops of data-dependent length. *Numerical differentiation* by [finite differences](/finite-differences/) needs one or two runs per input and has truncation and rounding error; it serves as a check ([gradient checking](/gradient-checking/)). AD is neither: it evaluates a derivative program built from the same trace, with no step size.
- Let $F : \mathbb{R}^p \to \mathbb{R}^m$ and let $\mathrm{OPS}(F)$ be the cost of one evaluation. Forward mode gives the full Jacobian with $p$ runs, reverse mode with $m$ sweeps. Use forward mode when $p \le m$ and reverse mode when $m \ll p$. Training a network has $m = 1$ and $p$ in the millions.
- Reverse mode needs memory for the tape, proportional to $\mathrm{OPS}(F)$. If that does not fit, use [gradient checkpointing](/gradient-checkpointing/).

## The template

The program, run on $x = (x_1, \ldots, x_p)$, produces a trace $v_1, \ldots, v_N$. The inputs and the constants are entries with no parents. Each other entry is $v_i = \varphi_i\big((v_j)_{j \in \mathrm{pa}(i)}\big)$ for a primitive $\varphi_i$, and its *local partials* are $c_{ij} = \partial \varphi_i / \partial v_j$ at the current values. The holes are the set of primitives with their partial rules and the output weights $u \in \mathbb{R}^m$.

```pseudo id=main
REVERSE-MODE(f, x, u)                       ▷ returns f(x) and uᵀ J_f(x)
L1  run f on x; for each operation i push (pa(i), (c_ij) for j ∈ pa(i)) on the tape
L2  v̄_i ← 0 for every tape entry i
L3  v̄_{y_k} ← v̄_{y_k} + u_k for each output y_k
L4  for i ← N down to 1 do
L5      for each (j, c_ij) in entry i do
L6          v̄_j ← v̄_j + v̄_i · c_ij
L7  return f(x) and (v̄_{x_1}, ..., v̄_{x_p})
```

The adjoint $\bar v_j$ is $\partial (u^\top y) / \partial v_j$. Line L6 is the chain rule on the graph, proved on the [computational graph](/computational-graph/) page: when the sweep reaches entry $i$, all children of $i$ have larger indices and have already added their share, so $\bar v_i$ is final. A value used twice gets two additions, one per use. With $u = e_k$ the result is row $k$ of the Jacobian; with $m = 1$ and $u = 1$ it is the gradient.

Forward mode needs no tape. It replaces each number $a$ by a *dual number* $a + \dot a\,\varepsilon$ with $\varepsilon^2 = 0$. Then $(a + \dot a \varepsilon)(b + \dot b \varepsilon) = ab + (\dot a b + a \dot b)\varepsilon$ and $g(a + \dot a \varepsilon) = g(a) + g'(a)\dot a\,\varepsilon$, so the $\varepsilon$ part follows the derivative.

```pseudo id=forward
FORWARD-MODE(f, x, v)                       ▷ returns f(x) and J_f(x) v
F1  x_k ← x_k + v_k ε for k = 1, ..., p
F2  for i ← 1 to N do
F3      v_i ← φ_i(parents);  v̇_i ← Σ_{j ∈ pa(i)} c_ij · v̇_j
F4  return the real parts and the ε parts of the outputs
```

**Cost.** Assume every primitive has at most two arguments and that computing its value and its local partials costs at most a constant $\kappa$ times its own cost; for $+$, $-$, $\times$, $/$ the partials cost at most one extra division. Then:

- *Forward mode.* Line F3 does at most two multiply-adds more than the primitive itself. One run costs at most $(\kappa + 4)\,\mathrm{OPS}(F)$ operations and $O(1)$ extra memory per live value. The full Jacobian costs $p$ runs.
- *Reverse mode.* Line L1 costs at most $\kappa\, \mathrm{OPS}(F)$, and lines L4 to L6 do at most two multiply-adds per entry. So one vector Jacobian product costs at most $(\kappa + 4)\,\mathrm{OPS}(F)$ operations, a bound that does not depend on $p$. The price is memory: the tape holds $N = \Theta(\mathrm{OPS}(F))$ entries.

This is the *cheap gradient principle*. The sharp constants depend on the cost model. Baur and Strassen (1983) proved that a rational function and all its partial derivatives can be computed with at most 3 times the multiplications and divisions of the function; with every arithmetic operation counted the factor is 5. Griewank and Walther (2008, Chapter 4) give $\mathrm{OPS}\{f, \nabla f\} \le 4\, \mathrm{OPS}\{f\}$ in their operation count model, and older statements of the principle, such as their 2000 paper on revolve, use 5 for run time with memory moves counted. There is no cheap Jacobian: for $F(x) = b \sin(a^\top x)$ with $a \in \mathbb{R}^p$ and $b \in \mathbb{R}^m$, the function costs about $p + m$ multiplications and its Jacobian has $pm$ entries, which are in general distinct (Griewank 2012).

### Worked example

Take $f(x_1, x_2) = \ln x_1 + x_1 x_2 - \sin x_2$ at $(2, 5)$, from Baydin et al. (2018). The trace and the two modes:

| entry | value | forward $\dot v$ with $v = (1, 0)$ | reverse adjoint $\bar v$ |
|---|---|---|---|
| $x_1 = v_{-1}$ | 2 | 1 | 5.5 |
| $x_2 = v_0$ | 5 | 0 | 1.716338 |
| $v_1 = \ln v_{-1}$ | 0.693147 | $\dot v_{-1} / v_{-1} = 0.5$ | 1 |
| $v_2 = v_{-1} v_0$ | 10 | $\dot v_{-1} v_0 + v_{-1} \dot v_0 = 5$ | 1 |
| $v_3 = \sin v_0$ | $-0.958924$ | $\cos(v_0)\, \dot v_0 = 0$ | $-1$ |
| $v_4 = v_1 + v_2$ | 10.693147 | 5.5 | 1 |
| $v_5 = v_4 - v_3$ | 11.652071 | 5.5 | 1 |

Forward mode gives $\partial f / \partial x_1 = 5.5$ in one run and needs a second run with $v = (0, 1)$ for $\partial f / \partial x_2 = 2 - \cos 5 = 1.716338$. Reverse mode gives both from one sweep over 7 tape entries. The input $x_1$ gets $\bar v_{-1} = \bar v_1 \cdot \tfrac12 + \bar v_2 \cdot 5$, one term for each of its two uses.

## Classic examples

- [Backpropagation](/backpropagation/): reverse mode on a layered network, with the matrix product and the activation as primitives. One backward pass costs about two forward passes.
- [Backpropagation through time](/backpropagation-through-time/): reverse mode on a recurrent network unfolded over the sequence. The tape grows with the sequence length.
- [Gradient checking](/gradient-checking/): compares an AD or hand-written gradient with central differences; forward mode with dual numbers is a second exact check.
- [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/): needs the gradient of a log density at every leapfrog step, which reverse mode gives at a fixed multiple of the density cost.
- [Newton's method for systems](/newton-method-for-systems/): needs the square Jacobian; forward mode builds it column by column with $p$ runs.
- The [Taylor series method](/taylor-series-method/) for ODEs propagates truncated Taylor series instead of dual numbers: forward mode of higher order.
- [Straight-line programs](/straight-line-program/): the Baur and Strassen theorem is reverse mode on an arithmetic circuit, and it transfers lower bounds from a function to its gradient.

## Variations

- **Vector modes.** Carry $q$ tangents at once in forward mode, or $q$ adjoints in reverse mode, to get $J V$ or $U^\top J$ with one pass over the trace.
- **Hessian vector products.** Apply forward mode to the reverse mode program. This gives $\nabla^2 f(x)\, v$ for a small constant times the cost of $f$ (Pearlmutter 1994). Truncated Newton methods and curvature estimates use it.
- **Operator overloading versus source transformation.** A tape built at run time (the implementation on this page, PyTorch, JAX tracing) or a derivative program generated by a compiler (Tapenade, Enzyme). The first is simpler; the second can optimize the adjoint code.
- **Checkpointing.** Store only some states of the forward run and run parts again during the backward sweep. Binomial checkpointing (Griewank 1992, revolve) makes memory and extra work grow only logarithmically in the length of the run; see [gradient checkpointing](/gradient-checkpointing/).
- **Nonsmooth primitives.** For $\max$, $\lvert \cdot \rvert$ and [ReLU](/relu/), AD uses one fixed one-sided derivative at the kink. The result can differ from every element of the Clarke subdifferential at that point (see the pitfalls).
- **Implicit functions and fixed points.** For $x^\star$ defined by $g(x^\star, \theta) = 0$, differentiate the equation instead of the iterations: $\partial x^\star / \partial \theta = -(\partial_x g)^{-1} \partial_\theta g$.

## Pitfalls

- **Kinks give a derivative of the program, not of the function.** With the convention $\mathrm{relu}'(0) = 0$, the program $\mathrm{relu}(x) - \mathrm{relu}(-x)$ computes $x$, but AD returns $0$ at $x = 0$ instead of $1$.
- **Differentiating an iteration.** The derivative of a loop that converges to a fixed point need not converge to the derivative of the fixed point at the same rate, and differentiating a stopping test or a branch gives zero. Prefer the implicit rule above.
- **Mutation after recording.** A tape stores references to values for the backward sweep. Changing such a value in place after it was recorded gives a silently wrong gradient; frameworks check a version counter for this reason.
- **Memory.** The tape of a long run (a deep network on a large batch, a long sequence, a time stepping solver) can exceed memory long before time is a problem. The cost bound above is in operations, not in bytes.
- **Undefined derivatives at valid points.** $\sqrt{x}$ at $x = 0$ has the local partial $1/(2\sqrt x) = \infty$. Even if the adjoint that reaches it is 0, the product $0 \cdot \infty$ gives NaN. Guard such primitives or use a safe form.
- **Perturbation confusion.** When forward mode is nested (a derivative inside a function that is itself differentiated), the two $\varepsilon$ must be distinct; one shared $\varepsilon$ mixes the two derivatives.

## Exercises

1. Derive the dual number rule for division, $(a + \dot a \varepsilon)/(b + \dot b \varepsilon) = a/b + \frac{\dot a - (a/b) \dot b}{b} \varepsilon$ for $b \ne 0$, from $\varepsilon^2 = 0$.
2. For $F(x) = A x$ with $A \in \mathbb{R}^{m \times p}$, show that forward mode with direction $v$ returns $A v$ and reverse mode with weights $u$ returns $A^\top u$. Count the operations of the full Jacobian in each mode.
3. Let $f(x) = \sum_{i=1}^p x_i^2$ be computed by a loop. Count the tape entries and the multiply-adds of one reverse sweep, and compare them with the operations of $p$ forward mode runs.
4. Show that $u^\top (J v) = (u^\top J) v$ for the results of the two modes at the same point. Use this identity as a test that needs no reference gradient.

## References
