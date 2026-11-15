---
tag: FYSKQ6
kind: technique
slug: block-diagram-reduction
name: Block diagram reduction
aliases:
- block diagram algebra
area: control/modeling-and-identification
level: intro
summary: "Rules that merge series, parallel and feedback blocks of a linear diagram, and move summing and takeoff points, until one transfer function from the input to the output is left."
prereqs: [transfer-function]
see_also: [masons-gain-formula, signal-flow-graph, feedback-control-loop, transfer-function-matrix, sensitivity-function, linear-fractional-transformation, poles-and-zeros, state-space-representation]
sources:
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 2, Mathematical Modeling of Control Systems (block diagrams and their simplification)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 3.2.1, The Block Diagram, and Section 3.2.2, Block-Diagram Reduction Using Matlab
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 9, Transfer Functions (block diagrams and transfer functions, and the gang of four)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 3, Introduction to Multivariable Control (transfer functions of block diagrams with several inputs and outputs, and the push-through rule)
---

## In plain words

A block diagram shows a linear system as boxes joined by arrows. Each box multiplies its incoming signal by a [transfer function](/transfer-function/), each circle adds or subtracts signals, and each branch point copies a signal. Block diagram reduction replaces small patterns in the diagram by single boxes with the same input-output behaviour: two boxes in a row become their product, two boxes side by side become their sum, and a feedback loop becomes one fraction. When no pattern fits, one moves an adder or a branch point past a box, with a correction box, until a pattern appears. At the end one box is left, and its transfer function is the answer.

## When it applies

- Every block is linear and time invariant, with a transfer function (a rational function, or one with a delay factor $e^{-s\tau}$). The result is the transfer function of the system at rest, with zero initial conditions.
- The diagram is well posed, so that each signal is uniquely defined. For proper blocks and a negative feedback loop with loop gain $L = GH$, this is $1 + L(\infty) \ne 0$.
- The diagram is small enough to reduce by hand, with a few nested loops. For a tangled diagram with many interlocking loops, [Mason's gain formula](/masons-gain-formula/) is shorter, and for numeric work a state-space interconnection is safer.
- With several inputs and outputs, the blocks are matrices and the order of products matters. The same rules hold with the matrix forms below.

## The template

The three merge rules, for scalar blocks:

| pattern | replaced by |
|---|---|
| $G_1$ then $G_2$ in series | $G_2 G_1$ |
| $G_1$ and $G_2$ in parallel into an adder | $G_1 \pm G_2$ |
| forward block $G$, feedback block $H$, negative feedback | $G / (1 + G H)$ |
| forward block $G$, feedback block $H$, positive feedback | $G / (1 - G H)$ |

The four move rules, which keep every signal that leaves the diagram unchanged:

| move | correction |
|---|---|
| adder from after $G$ to before $G$ | the side input passes through $1/G$ |
| adder from before $G$ to after $G$ | the side input passes through $G$ |
| branch point from after $G$ to before $G$ | the branch passes through $G$ |
| branch point from before $G$ to after $G$ | the branch passes through $1/G$ |

```pseudo id=main
BLOCK-DIAGRAM-REDUCE(D, r, y)
L1  name every signal of D; check that each block is LTI and that D is well posed
L2  repeat
L3      merge every pair of blocks in series, and every pair in parallel
L4      pick a LOOP of D with no outside adder input or branch point between its blocks
L5      if such a loop exists then replace it by G / (1 + G H), with the SIGN of its adder
L6      else move one ADDER OR BRANCH POINT past one block by the move rules, to free a loop
L7  until D is one block from r to y
L8  write the block as N(s)/D(s), cancel common factors, and list each factor cancelled
L9  return the block
```

The holes are the choice of LOOP at L4 (innermost loops first keeps the algebra small), the SIGN convention at each adder, and the choice of ADDER OR BRANCH POINT to move at L6. Line L8 matters: each factor cancelled there is a mode that the input-output map does not show, and the pitfalls below explain when it is dangerous.

**Why the feedback rule holds.** With negative feedback, $e = r - H y$ and $y = G e$, so $y = G r - G H y$ and $y (1 + G H) = G r$. When $1 + G H \ne 0$, $y = G/(1 + GH)\, r$.

**A worked example.** Take the diagram with the signals

$$e_1 = r - c, \quad e_2 = e_1 + H_1 x_2, \quad x_1 = G_1 e_2, \quad e_3 = x_1 - H_2 c, \quad x_2 = G_2 e_3, \quad c = G_3 x_2.$$

No loop is free: the loop through $H_2$ starts at $c$, after $G_3$, and ends before $G_2$, so the branch point of $x_2$ for $H_1$ sits inside it. Move the branch point for $H_2$ from $c$ back to $x_2$; by the move rules the branch now passes through $G_3$, so the feedback block becomes $G_3 H_2$. Now the loop around $G_2$ alone is free, and it becomes $G_2/(1 + G_2 G_3 H_2)$. In series with $G_1$, inside the positive loop through $H_1$, this gives

$$\frac{G_1 G_2}{1 + G_2 G_3 H_2 - G_1 G_2 H_1}.$$

In series with $G_3$ and closed by the unity feedback of $e_1$:

$$\frac{C}{R} = \frac{G_1 G_2 G_3}{1 - G_1 G_2 H_1 + G_2 G_3 H_2 + G_1 G_2 G_3}.$$

With $G_1 = 1/(s + 1)$, $G_2 = 1/(s + 2)$, $G_3 = 1/s$, $H_1 = 1$ and $H_2 = 2$, multiplying the top and the bottom by $s(s + 1)(s + 2)$ gives $C/R = 1/(s^3 + 3s^2 + 3s + 3)$. Mason's formula gives the same result in one step: the three loops $G_1 G_2 H_1$, $-G_2 G_3 H_2$ and $-G_1 G_2 G_3$ all pass through $x_2$, so they all touch, and the one forward path touches all of them.

## Classic examples

- **The unity feedback loop.** In the [feedback control loop](/feedback-control-loop/) with controller $C$ and plant $P$, the reference-to-output map is $T = PC/(1 + PC)$, and the disturbance at the plant input reaches the output through $P/(1 + PC)$. Both are one application of the feedback rule.
- **Cascade control.** In [cascade control](/cascade-control/), an inner loop with controller $C_2$ around the plant part $P_2$ is reduced first, to $T_2 = C_2 P_2/(1 + C_2 P_2)$. The outer loop then sees $T_2 P_1$, and the reference-to-output map is $C_1 T_2 P_1 /(1 + C_1 T_2 P_1)$.
- **The Smith predictor.** In the [Smith predictor](/smith-predictor/), the controller $C$ has an inner feedback through the model $P_0 (1 - e^{-s\tau})$. The feedback rule gives the equivalent controller $C/(1 + C P_0 (1 - e^{-s\tau}))$. With the plant equal to the model $P_0 e^{-s\tau}$, the reference-to-output map reduces to $C P_0 e^{-s\tau}/(1 + C P_0)$, so the delay leaves the characteristic equation.
- **Internal model control.** In [internal model control](/internal-model-control/), the controller $Q$ acts on the error between the output and a model $P_0$ driven by the same input. The feedback rule turns this into an ordinary feedback controller $C = Q/(1 - Q P_0)$.
- **Two degrees of freedom.** In [two-degree-of-freedom control](/two-degree-of-freedom-control/), $u = C (F r - y)$ with a prefilter $F$. The series rule and the feedback rule give $y = F\, PC/(1 + PC)\, r$: $F$ shapes the response to $r$ without changing the loop.

## Variations

- **Mason's gain formula.** The [gain formula](/masons-gain-formula/) on the [signal-flow graph](/signal-flow-graph/) of the diagram gives the result with no moves, from the paths and the loops.
- **Several inputs and outputs.** With matrix blocks, series is $G_2 G_1$ (the later block on the left), and negative feedback gives $(I + G H)^{-1} G$. The push-through rule $G (I + H G)^{-1} = (I + G H)^{-1} G$ moves a matrix past a loop. See [transfer function matrix](/transfer-function-matrix/).
- **State-space interconnection.** Software connects the realizations of the blocks into one state-space model and reduces it to a [minimal realization](/minimal-realization/) only at the end. This keeps every mode in view and is the safe form for numeric work.
- **Linear fractional transformations.** A [linear fractional transformation](/linear-fractional-transformation/) writes any interconnection as one feedback loop between a fixed block and the part of interest, for example an uncertainty block.

## Pitfalls

- **Cancellation hides modes.** A reduced transfer function can be stable while the system is not internally stable. With $P = 1/(s - 1)$ and $C = (s - 1)/(s + 1)$, the reference-to-output map is $1/(s + 2)$, but the map from a disturbance at the plant input is $(s + 1)/((s - 1)(s + 2))$, which is unstable (see [poles and zeros](/poles-and-zeros/)). Check the four maps $S$, $PS$, $CS$ and $T$ of a loop (the gang of four), not one, where $S$ is the [sensitivity function](/sensitivity-function/).
- **Signs.** Write the sign at each adder before reducing. A positive feedback loop gives $1 - GH$ in the denominator; a wrong sign here changes the closed-loop poles completely.
- **Order of matrix products.** With matrices, $G_2 G_1 \ne G_1 G_2$ in general, and $(I + G K)^{-1}$ is not $(I + K G)^{-1}$; they even have different sizes when $G$ is not square.
- **Algebraic loops.** If $1 + G(\infty) H(\infty) = 0$ for a loop, the signals are not defined, although the formula $G/(1 + GH)$ can still give a rational function. A loop around a constant gain $-1$ is the plainest case.
- **Moves through $1/G$.** The move rules that use $1/G$ need $G \ne 0$. If $G$ is strictly proper or has zeros in the right half plane, the intermediate diagram has an improper or an unstable block. This is fine as algebra, but that intermediate diagram is not a system one can build or simulate.
- **Initial conditions.** The result holds only for a system at rest. A response to initial conditions needs the state-space model or the Laplace transform with the initial values.

## Exercises

1. Two blocks $G_1$ and $G_2$ in parallel are closed by a negative feedback block $H$. Show that the closed-loop map is $(G_1 + G_2)/(1 + (G_1 + G_2) H)$.
2. In the worked example, set $H_1 = 0$ and keep the other blocks. Show that $C/R = 1/(s^3 + 3s^2 + 4s + 3)$.
3. Reduce the worked example a second way: first move the adder of $H_1$ from before $G_1$ to after $G_1$. Check that the result is the same.
4. Show the push-through rule $G (I + H G)^{-1} = (I + G H)^{-1} G$ for matrices of compatible sizes, when both inverses exist. Hint: multiply $(I + G H) G = G (I + H G)$ on both sides.
5. For the internal model control structure, show that if $Q$ is stable and the plant equals the stable model $P_0$, the reference-to-output map is $P_0 Q$.

## References
