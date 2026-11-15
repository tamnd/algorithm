---
tag: 3BXD4W
kind: algorithm
slug: reduced-order-observer
name: Reduced-order observer
aliases:
- minimal-order observer
- Luenberger reduced-order observer
area: control/state-space-control
level: core
summary: Estimates only the part of the state that the outputs do not measure, with an observer of order n minus the number of outputs.
solves: [state-estimation]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, p: the number of outputs, N: the number of updates}
  time: {worst: "O(n^3 + p (n - p)^4 + N n (n + m))"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1964
  people: [David G. Luenberger, Bhaskar Gopinath]
  note: "Luenberger showed in 1964 and 1966 that observers of order less than n are enough when outputs are measured; Gopinath gave in 1971 the construction in the coordinates [y; w] with the gain on the unmeasured part."
prereqs: [luenberger-observer, observability, state-space-representation]
see_also: [luenberger-observer, state-observer, separation-principle, unknown-input-observer, kalman-filter, observable-canonical-form, minimal-realization, pole-placement-problem]
sources:
  - paper: doi:10.1109/tme.1964.4323124
    title: David G. Luenberger, Observing the state of a linear system, IEEE Transactions on Military Electronics 8(2), 74-80, 1964
    locator: the observers of reduced dynamic order, n minus the number of outputs
  - paper: doi:10.1109/tac.1966.1098323
    title: David G. Luenberger, Observers for multivariable systems, IEEE Transactions on Automatic Control 11(2), 190-197, 1966
    locator: the observers of reduced order for systems with several outputs
  - paper: doi:10.1002/j.1538-7305.1971.tb01896.x
    title: Bhaskar Gopinath, On the control of linear multiple input-output systems, Bell System Technical Journal 50(3), 1063-1081, 1971
    locator: the construction of the reduced-order observer from a partition of the state into measured and unmeasured parts
  - paper: doi:10.1109/tac.1971.1099826
    title: David G. Luenberger, An introduction to observers, IEEE Transactions on Automatic Control 16(6), 596-602, 1971
    locator: the reduced-order observer and its error equation
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.4.1, Reduced-Dimensional State Estimator
---

A reduced-order observer estimates the state of $\dot x = Ax + Bu$, $y = Cx$ when $C \in \mathbb{R}^{p \times n}$ has full row rank. The $p$ outputs already give $p$ independent combinations of the state without error, so the observer has only $n - p$ states. It is also called a minimal-order observer. The [Luenberger observer](/luenberger-observer/) of full order estimates all $n$ states and filters the measured ones too. The reduced-order observer trusts the measurement and passes it directly to the estimate. Both are deterministic: for noisy outputs, the [Kalman filter](/kalman-filter/) is the usual choice. The [state observer](/state-observer/) page defines observers in general.

## In plain words

A machine has some quantities that sensors read directly and others that no sensor reads. A full observer estimates all of them, even the ones that are measured. A reduced-order observer does not. It takes the measured quantities as they are and builds a small model only for the missing ones. It watches how the measured quantities change, because that change depends on the missing quantities, and it corrects its guess from that. A trick in the design avoids taking the rate of change of a noisy signal. The result is a smaller observer that needs less computation. The price is that sensor noise goes straight into the estimate, with no smoothing.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ with $\operatorname{rank} C = p < n$, and a monic real polynomial $\alpha$ of degree $n - p$. Output: matrices $F, G, H, L$ and $T^{-1}$ such that the system

$$\dot z = Fz + Gy + Hu, \qquad \hat x = T^{-1} \begin{bmatrix} y \\ z + Ly \end{bmatrix}$$

gives $\hat x(t) - x(t) \to 0$ for every initial state and every input, with $\det(sI - F) = \alpha(s)$. A solution exists for every $\alpha$ if and only if $(C, A)$ is [observable](/observability/). In discrete time the observer is $z_{k+1} = F z_k + G y_k + H u_k$ with the same matrices, and $F$ must be Schur.

## The algorithm

```pseudo id=main
REDUCED-ORDER-OBSERVER(A, B, C, alpha)
L1  V ← unit rows that complete the rows of C to a basis; T ← [C; V]
L2  [A11 A12; A21 A22] ← T A T^(-1); [B1; B2] ← T B      ▷ split after p rows and columns
L3  L ← PLACE(A22^T, A12^T, alpha)^T                     ▷ fails if (C, A) is not observable
L4  F ← A22 - L A12; G ← F L + A21 - L A11; H ← B2 - L B1
L5  return F, G, H, L, T^(-1)
UPDATE(z, u, y)
L6  z' ← F z + G y + H u                                 ▷ derivative, or next value in discrete time
L7  x_hat ← T^(-1) [y; z + L y]
```

Line L1 picks new coordinates $Tx = [y; w]$: the first $p$ are the outputs, and $w$ holds $n - p$ other coordinates. Line L2 writes the system in these coordinates:

$$\dot y = A_{11} y + A_{12} w + B_1 u, \qquad \dot w = A_{21} y + A_{22} w + B_2 u.$$

The second equation is a system with state $w$ and known inputs $y$ and $u$. The first equation says that $A_{12} w = \dot y - A_{11} y - B_1 u$ is a measured output of it. An observer for $w$ with this output would need $\dot y$. The variable $z = \hat w - Ly$ removes the derivative: the term $L\dot y$ cancels, and line L4 collects what is left. Line L3 is pole placement for the dual pair, as in the [Luenberger observer](/luenberger-observer/). The implementation uses the same PLACE routine: Heymann's lemma in the form of Hautus, then [Ackermann's formula](/ackermann-formula/).

## Example

**Double integrator.** A cart has position $y = x_1$ and velocity $v = x_2$, with $\dot x_1 = x_2$, $\dot x_2 = u$. The position is measured. Here $T = I$, $A_{11} = 0$, $A_{12} = 1$, $A_{21} = 0$, $A_{22} = 0$, $B_1 = 0$, $B_2 = 1$. For the observer pole $-3$, $\alpha(s) = s + 3$, and $A_{22} - L A_{12} = -L$ gives $L = 3$. Line L4 gives

$$F = -3, \qquad G = F L + A_{21} - L A_{11} = -9, \qquad H = B_2 - L B_1 = 1.$$

The observer is one equation:

$$\dot z = -3z - 9y + u, \qquad \hat v = z + 3y.$$

To check it, let $z^\ast = v - 3y$. Then $\dot z^\ast = u - 3v = -3z^\ast - 9y + u$, so $z^\ast - z$ obeys $\frac{d}{dt}(z^\ast - z) = -3(z^\ast - z)$, and $v - \hat v = e^{-3t}(v(0) - \hat v(0))$. The position estimate is $y$ itself, with no error. A full-order observer for the same cart has two states.

**Deadbeat in discrete time.** With $\alpha(z) = z^{n-p}$, $F$ is nilpotent and the estimate is exact after $n - p$ samples. For the sampled cart, one sample is enough, against two for the full-order deadbeat observer.

## Correctness

Let $w$ be the lower part of $Tx$ and $z^\ast = w - Ly$. Then

$$\dot z^\ast = A_{21} y + A_{22} w + B_2 u - L(A_{11} y + A_{12} w + B_1 u) = (A_{22} - L A_{12}) w + (A_{21} - L A_{11}) y + (B_2 - L B_1) u.$$

Substitute $w = z^\ast + Ly$: $\dot z^\ast = F z^\ast + (FL + A_{21} - L A_{11}) y + Hu = F z^\ast + Gy + Hu$. So $z^\ast$ obeys the same equation as $z$, and $\varepsilon = z^\ast - z$ obeys $\dot \varepsilon = F\varepsilon$. The estimate error is $x - \hat x = T^{-1} [0; \varepsilon]$. Line L3 makes $\det(sI - F) = \alpha(s)$, which is possible for every $\alpha$ because $(A_{12}, A_{22})$ is observable when $(C, A)$ is. The full proof is in [proofs/correctness.md](proofs/correctness.md). The tests check that the estimate error equals $T^{-1}[0; F^k \varepsilon_0]$ exactly in rational arithmetic, that a simulated continuous observer follows $e^{Ft}$, and that the deadbeat version is exact after $n - p$ steps.

## Complexity

Lines L1 and L2 cost $O(n^3)$: rank tests to complete the basis, one inverse and two products. Line L3 is pole placement of size $n - p$ with $p$ columns, which costs $O(p (n - p)^4)$ with the simple rank tests of the implementation. Line L4 costs $O(n^3)$. Each update costs $O((n - p)(n + m))$ for line L6 and $O(n^2)$ for line L7.

## Properties

- **Order $n - p$.** The observer has $p$ fewer states than the full-order observer, and its error has $n - p$ eigenvalues, all of which are free to choose.
- **Direct feedthrough.** The measured part of $\hat x$ is $y$ itself. This is exact for exact data, but the noise of $y$ goes into $\hat x$ without filtering, through $T^{-1}$ and $L$.
- **No derivative.** The observer uses $y$ and $u$, not $\dot y$.
- **Separation.** Feedback $u = -K\hat x$ gives the closed-loop eigenvalues of $A - BK$ together with those of $F$; see [separation principle](/separation-principle/).
- **Exact arithmetic.** With rational data, the implementation is exact.

## Variants and improvements

- **Other choices of $T$.** Any $V$ that makes $T$ invertible works, and the error eigenvalues do not depend on the choice. A $V$ with orthonormal rows that are orthogonal to the rows of $C$ is the numerically safer choice.
- **Functional observers.** If only $Kx$ is needed, for feedback, an observer of even lower order can estimate $Kx$ directly. Luenberger's 1971 tutorial discusses such observers.
- **Unknown inputs.** If some inputs are not measured, see [unknown input observer](/unknown-input-observer/).
- **Noisy outputs.** If the measured outputs are noisy, a full-order [Kalman filter](/kalman-filter/) smooths them, while the reduced-order observer does not.

## When to use it

Use a reduced-order observer when some outputs are accurate, the computing budget is small, and the model is good: for example, with an encoder that measures position precisely, to estimate the velocity of a motor. Use the full-order [Luenberger observer](/luenberger-observer/) or a Kalman filter when the outputs are noisy.

## Pitfalls

- **Noise in the estimate.** Large $L$ amplifies the noise of $y$ in $\hat w = z + Ly$ directly. Check the gain from $y$ to $\hat x$ at high frequency.
- **Rank of $C$.** If $C$ does not have full row rank, remove dependent outputs first.
- **Unobservable modes.** If $(C, A)$ is not observable, $(A_{12}, A_{22})$ is not observable either, and some eigenvalues of $F$ are fixed.
- **Model errors.** The cancellation that removes $\dot y$ uses the model; a wrong $A$ or $B$ gives a bias.

## Implementations

## History

Luenberger's papers of 1964 and 1966 showed that the measured outputs reduce the order of the observer that is needed to reconstruct the state. Gopinath (1971) gave the construction in the coordinates $[y; w]$ with the gain $L$ on the unmeasured part, which is the form on this page. Luenberger's tutorial of 1971 gave an account of both the full-order and the reduced-order observer.

## References
