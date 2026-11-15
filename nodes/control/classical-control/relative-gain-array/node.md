---
tag: EVRS3T
kind: technique
slug: relative-gain-array
name: Relative gain array
aliases:
- Bristol relative gain array
area: control/classical-control
level: core
summary: A matrix of ratios of open-loop to closed-loop gains that tells which input should control which output in a multivariable plant.
prereqs: [transfer-function-matrix, feedback-control-loop]
see_also: [transfer-function-matrix, condition-number, singular-value-decomposition, pid-controller, internal-model-control, transmission-zero, model-predictive-control, h-infinity-loop-shaping]
sources:
  - paper: doi:10.1109/TAC.1966.1098266
    title: Edgar H. Bristol, On a new measure of interaction for multivariable process control, IEEE Transactions on Automatic Control 11(1) (1966) 133-134
    locator: the whole paper (the definition of the relative gain)
  - paper: doi:10.1021/i100018a015
    title: Pierre Grosdidier, Manfred Morari and Bradley R. Holt, Closed-loop properties from steady-state gain information, Industrial and Engineering Chemistry Fundamentals 24(2) (1985) 221-235
    locator: the whole paper (negative relative gains and integral control)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, second edition, Wiley, 2005
    locator: Section 3.4, pp. 82-91 (the RGA, its properties and Example 3.9)
---

The relative gain array (RGA) of a square plant with the gain matrix $G$ is the matrix

$$\Lambda(G) = G \circ (G^{-1})^T, \qquad \lambda_{ij} = g_{ij} \, [G^{-1}]_{ji},$$

where $\circ$ is the elementwise product. Bristol (1966) defined $\lambda_{ij}$ as the gain from input $u_j$ to output $y_i$ with all other inputs fixed, divided by the same gain when all other outputs are held constant by perfect control. If $\lambda_{ij} = 1$, closing the other loops does not change what $u_j$ does to $y_i$. The RGA is used to choose the pairing of inputs and outputs for a set of single loops, mostly with the steady-state gain $G(0)$. It also flags plants that are hard to control: large elements mean that the plant is close to singular in a way that small errors in the model can change.

## In plain words

A plant with several inputs and several outputs is often run with simple single loops: one controller per output, each moving one input. The question is which input goes with which output. The relative gain asks, for one input and one output: how much does this input move this output when the other inputs stay still, and how much when the other loops are closed and hold their outputs? If the two answers are the same, the other loops do not disturb this pair, and the pair is a good choice. If the second answer has the opposite sign, closing the other loops reverses the effect of this input, and the pair must not be used. Very large values warn that the plant is hard to control with any simple scheme.

## When it applies

- The plant is square, with $n$ inputs and $n$ outputs, and its gain matrix $G(0)$ is known and nonsingular, for example from step tests.
- Decentralized control (one single loop per output) is planned, and the pairing must be chosen.
- A first check is wanted of how hard the plant is to control, before a multivariable design.
- For dynamic questions, the same formula applies to $G(j\omega)$ at each frequency, mostly near the planned crossover.

## The template

1. **Get the gain matrix** $G = G(0)$, or $G(j\omega)$ near the crossover.
2. **Compute** $\Lambda = G \circ (G^{-1})^T$. For $2 \times 2$,
   $$\lambda_{11} = \frac{1}{1 - \dfrac{g_{12} g_{21}}{g_{11} g_{22}}}, \qquad \Lambda = \begin{bmatrix} \lambda_{11} & 1 - \lambda_{11} \\ 1 - \lambda_{11} & \lambda_{11} \end{bmatrix}.$$
3. **Discard pairings with a negative steady-state element** $\lambda_{ij}(0) < 0$ (a theorem, below).
4. **Prefer pairings with elements near 1**, mostly at the crossover frequency. This is a rule of thumb, not a theorem.
5. **Check the size.** Large elements, say much larger than 1, mean that one pairing cannot avoid strong interaction and that the model must be very accurate. Consider decoupling or a multivariable controller.
6. **Tune and test** the single loops, then test the full loop with all loops closed and with each loop opened.

Computing $\Lambda$ costs one matrix inverse, $O(n^3)$. Choosing a pairing is a choice among $n!$ permutations, which is easy by enumeration for the small $n$ of practice.

**Properties (theorems).**

- *Rows and columns sum to 1.* Since $G G^{-1} = I$, $\sum_j g_{ij} [G^{-1}]_{ji} = 1$, and the same for columns from $G^{-1} G = I$.
- *Scaling does not change it.* $\Lambda(D_1 G D_2) = \Lambda(G)$ for nonsingular diagonal $D_1$, $D_2$, so units do not matter.
- *Permutations.* Swapping rows or columns of $G$ swaps the same rows or columns of $\Lambda$.
- *Triangular plants.* If $G$ is triangular, $\Lambda = I$: the interaction runs one way only, and the diagonal pairing is free of it at steady state.
- *Meaning.* With all other outputs held by perfect control, the gain from $u_j$ to $y_i$ is $1/[G^{-1}]_{ji}$, so $\lambda_{ij}$ is the ratio of the open-loop gain $g_{ij}$ to this closed-loop gain.
- *Sensitivity to one element.* If $g_{ij}$ alone changes to $g_{ij}(1 - 1/\lambda_{ij})$, then $G$ becomes singular. Proof: $\det G$ is linear in $g_{ij}$ with the cofactor $C_{ij}$ as slope, and $\lambda_{ij} = g_{ij} C_{ij}/\det G$, so the change $-g_{ij}/\lambda_{ij}$ changes $\det G$ by $-\det G$. A large $\lambda_{ij}$ means a small relative error makes the plant singular.
- *Negative elements (Grosdidier, Morari and Holt 1985).* If a pairing has $\lambda_{ii}(0) < 0$ and every loop has integral action, then at least one of these is not asymptotically stable: the full closed loop, loop $i$ alone, or the other loops with loop $i$ open.

## Classic examples

**The example of Skogestad and Postlethwaite.** For $G = \begin{bmatrix} 1 & 1 \\ 0.4 & -0.1 \end{bmatrix}$ (their Example 3.9), $g_{12} g_{21}/(g_{11} g_{22}) = 0.4/(-0.1) = -4$, so $\lambda_{11} = 1/5 = 0.2$ and

$$\Lambda = \begin{bmatrix} 0.2 & 0.8 \\ 0.8 & 0.2 \end{bmatrix}.$$

The off-diagonal pairing, $u_2$ with $y_1$ and $u_1$ with $y_2$, has elements 0.8, closer to 1.

**A plant that is close to singular.** For $G = \begin{bmatrix} 87.8 & -86.4 \\ 108.2 & -109.6 \end{bmatrix}$, $\lambda_{11} = 1/(1 - 9348.48/9622.88) = 35.07$, and the other elements are $-34.07$. Both pairings are poor: one has the elements 35.07, the other negative elements. A change of $g_{11}$ by $1/35.07 = 2.85$ percent makes $G$ singular. The [condition number](/condition-number/) of $G$ is 141.7, which tells the same story. Such a plant needs a multivariable design and an accurate model.

**A negative element in practice.** Let $G(s) = G_0/(s + 1)$ with $G_0 = \begin{bmatrix} 1 & 2 \\ 1 & 1 \end{bmatrix}$, so $\lambda_{11} = 1/(1 - 2) = -1$ and $\lambda_{12} = 2$. Pair on the diagonal with integral controllers $k_1/s$ and $k_2/s$, with $k_1, k_2 > 0$. Each loop alone has the characteristic polynomial $s^2 + s + k_i$, whose roots have negative real parts. With both loops closed the characteristic polynomial is

$$\det\left(s(s + 1) I + G_0 \operatorname{diag}(k_1, k_2)\right) = (s^2 + s + k_1)(s^2 + s + k_2) - 2 k_1 k_2,$$

whose constant term $-k_1 k_2$ is negative. A polynomial with a positive leading coefficient and a negative constant term has a positive real root, so the full loop diverges for every $k_1, k_2 > 0$. The other pairing gives $\lambda = 2$ and $\det(G_0 \text{ with swapped columns}) = 1 > 0$, and the constant term $k_1 k_2$ is positive.

## Variations

- **Frequency-dependent RGA.** Compute $\Lambda(G(j\omega))$ over frequency. Elements near 1 at the crossover matter most for the interaction of the loops.
- **RGA number.** The sum of $|\Lambda - I|$ over the elements, for the chosen pairing as a permutation, gives one number to compare pairings over frequency.
- **Non-square plants.** With the pseudo-inverse, the row sums show which outputs the inputs can control best, and they help to select outputs.
- **Block pairing.** For blocks of inputs and outputs, a block RGA assigns groups to small multivariable controllers.
- **Decoupling.** If no pairing is good, a decoupler $D$ with $G D$ nearly diagonal is put before the single loops. This works only when the model is accurate, which the large RGA elements often deny.
- **Multivariable design.** For plants with large elements, use [model predictive control](/model-predictive-control/) or [H-infinity loop shaping](/h-infinity-loop-shaping/) instead of single loops.

## Pitfalls

- **Steady state only.** $\Lambda(0)$ says nothing about the dynamics. A pairing that is good at steady state can interact strongly at the crossover.
- **Large elements are not fixed by a pairing.** They show that the plant is close to singular. Inverse-based controllers on such a plant are very sensitive to errors in the input gains.
- **A singular gain matrix.** If $G(0)$ is singular, for example with integrating outputs, the RGA is not defined at $s = 0$. Use $G(j\omega)$ at a low frequency or scale out the integrators.
- **Treating "near 1" as a guarantee.** It is a rule of thumb. The full loop must still be checked, and the negative element test is the only part with a theorem behind it.
- **Model error.** The RGA comes from a model; with large elements, a small model error can change even the signs.

## Exercises

1. Compute $\Lambda$ for $G = \begin{bmatrix} 1 & 1 \\ 0.4 & -0.1 \end{bmatrix}$. (Answer: $\lambda_{11} = 0.2$, so $\Lambda = [0.2, 0.8; 0.8, 0.2]$.)
2. Show that each row of $\Lambda$ sums to 1. (Answer: $\sum_j g_{ij} [G^{-1}]_{ji} = [G G^{-1}]_{ii} = 1$.)
3. Show that $\Lambda = I$ for an upper triangular $G$. (Answer: $G^{-1}$ is upper triangular, so $(G^{-1})^T$ is lower triangular, and the elementwise product keeps only the diagonal, with $g_{ii} \cdot 1/g_{ii} = 1$.)
4. For $G = \begin{bmatrix} 87.8 & -86.4 \\ 108.2 & -109.6 \end{bmatrix}$, which relative change of $g_{11}$ alone makes $G$ singular? (Answer: $-1/\lambda_{11} = -1/35.07$, a decrease of 2.85 percent.)
5. In the negative element example, show that the full loop diverges for all positive gains while each loop alone converges. (Answer: the constant term of the characteristic polynomial is $k_1 k_2 \det G_0 = -k_1 k_2 < 0$, while each single loop has $s^2 + s + k_i$.)

## References
