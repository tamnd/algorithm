---
title: What annealing-based sizing returns, when its penalty is exact, and what is not proved
proves: [correctness]
status: partial
---

Notation. The variables take values on a finite grid $X = X_1 \times \cdots \times X_d$, with $X_j$ the allowed values of variable $j$ (a width, a length, a current). The performance of a point $x$ is a vector $p(x)$, computed by an evaluator: AWE and device models in ASTRX/OBLX, a closed-form square-law model in the code of this page. A specification is a bound $p_i(x) \ge t_i$ with $t_i > 0$. Its relative violation is $v_i(x) = \max(0, (t_i - p_i(x)) / t_i)$. The point is *feasible* if every $v_i(x) = 0$. The objective is $f(x) \ge 0$, and the cost is

$$C(x) = f(x) + \sum_i w_i v_i(x), \qquad w_i > 0.$$

ANNEAL-SIZE is the pseudocode of the page, lines L1 to L10.

**Lemma 1 (the returned value).** ANNEAL-SIZE returns a point $b \in X$ and the number $C(b)$, and $C(b) \le C(x)$ for every point $x$ that the run visited.

*Proof.* Invariant: after line L1 and after each pass of lines L5 to L8, $x \in X$, $c = C(x)$, and $\mathit{best}$ is a visited point of least cost so far, with $\mathit{best}_c = C(\mathit{best})$. It holds after L1. Line L5 builds $y$ from $x$ by changing one index and clamping it to the range, so $y \in X$. Line L6 sets $\delta = C(y) - c = C(y) - C(x)$. If line L7 accepts, the new $c$ is $c + \delta = C(y)$, and $x = y$. Otherwise nothing changes. Line L8 updates $\mathit{best}$ whenever the current point is cheaper. The loop ends because $T$ is multiplied by $\alpha < 1$ in line L9 and stops below $T_{\min} > 0$. $\square$

In floating point, $c + \delta$ may differ from $C(y)$ by rounding. The code returns the cost it carried, and the tests recompute $C(b)$ and compare.

**Corollary 2 (it never beats exhaustive search).** $C(b) \ge \min_{x \in X} C(x)$. The test compares the run with this minimum, found by evaluating $C$ at every point of the grid.

**Lemma 3 (an exact penalty on a finite grid).** Let the feasible set $F \subseteq X$ be nonempty, let $f^* = \min_{x \in F} f(x)$, and let

$$\nu = \min \{ v_i(x) : x \in X, \ v_i(x) > 0 \}$$

be the least positive violation on the grid. If $w_i > f^* / \nu$ for every $i$, then every minimum of $C$ over $X$ is feasible, and it minimizes $f$ over $F$.

*Proof.* $X$ is finite, so $\nu$ is a minimum of finitely many positive numbers and $\nu > 0$. Let $x \notin F$. Some $v_i(x) \ge \nu$, so $C(x) \ge f(x) + w_i \nu > 0 + f^*$, because $f \ge 0$. A feasible minimizer $x^*$ of $f$ has $C(x^*) = f^*$. So no infeasible point is a minimum of $C$. On $F$, $C = f$. $\square$

The bound needs the grid. With continuous variables the violation can be as small as we like, and the minimum of $C$ can sit just outside $F$, trading a small violation for a smaller $f$. ASTRX/OBLX also changes the weights during the run; this page does not model that.

**What is not proved.** The run does not in general return $\min_X C$.

1. The [Metropolis rule](/metropolis-criterion/) of line L7 makes the Boltzmann distribution $\pi_T(x) \propto e^{-C(x)/T}$ stationary at a fixed $T$ when the proposal is symmetric. The proposal of line L5 is not symmetric at the edges of the grid, where a step is clamped, and its reach shrinks with $T$. So the chain of the code is not shown to have $\pi_T$ as its stationary law.
2. The [convergence theorem](/simulated-annealing-convergence/) of annealing needs a schedule like $T_k = c / \log(k+1)$ with $c$ at least the depth of the deepest trap, and an unbounded run. Line L9 cools geometrically and stops after a fixed number of steps, as ASTRX/OBLX and most practical annealers do, so the theorem does not apply.
3. The cost is a property of the evaluator. A minimum of $C$ is a best design for the model of the circuit, not for the circuit.

**What is measured.** On the toy common-source stage of the code (a grid of $41 \times 41 \times 201$ points, with the constants and specifications of the code), the exhaustive search finds the grid optimum $W \approx 2.233$ µm, $L = 1.05$ µm, $I \approx 4.786$ µA. The grid has 31 local minima under moves of one step in one variable. With $T_0 = 1$, $\alpha = 0.95$, 100 moves per temperature and $T_{\min} = 10^{-4}$, the runs with seeds 0 to 39 of `random.Random` reached the grid optimum in 38 of 40 runs, and the other two were within 0.018 in cost. With $\alpha = 0.5$ and 10 moves per temperature, none of the 40 runs did. These are runs of the code of this page on a toy input; they are not benchmark results.
