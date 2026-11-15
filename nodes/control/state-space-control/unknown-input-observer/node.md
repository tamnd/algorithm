---
tag: A7P4SP
kind: algorithm
slug: unknown-input-observer
name: Unknown input observer
aliases:
- UIO
area: control/state-space-control
level: advanced
summary: An observer whose error does not depend on some unmeasured inputs, under a rank condition on how those inputs enter.
solves: [state-estimation]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of known inputs, p: the number of outputs, N: the number of updates}
  time: {worst: "O(p n^4 + N n (n + m + p))"}
  space: {extra: "O(n (n + p))"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1994
  people: [Mohamed Darouach, Michel Zasadzinski, Shi Jie Xu]
  note: "Kudva, Viswanadham and Ramakrishna gave existence conditions for observers with unknown inputs in 1980, Hautus related them to strong detectability in 1983, and Darouach, Zasadzinski and Xu gave the full-order design with H = E (CE)^+ in 1994."
prereqs: [luenberger-observer, observability, detectability, transmission-zero]
see_also: [luenberger-observer, disturbance-observer, state-observer, reduced-order-observer, sliding-mode-observer, transmission-zero, disturbance-decoupling-problem, minimum-phase]
sources:
  - paper: doi:10.1109/9.280770
    title: Mohamed Darouach, Michel Zasadzinski and Shi Jie Xu, Full-order observers for linear systems with unknown inputs, IEEE Transactions on Automatic Control 39(3), 606-609, 1994
    locator: the observer z' = F z + G u + K y, x_hat = z + H y, its design equations and its existence conditions
  - paper: doi:10.1016/0024-3795(83)90061-7
    title: M. L. J. Hautus, Strong detectability and observers, Linear Algebra and its Applications 50, 353-368, 1983
    locator: strong detectability and its relation to observers for systems with unknown inputs
  - paper: doi:10.1109/tac.1980.1102245
    title: P. Kudva, N. Viswanadham and A. Ramakrishna, Observers for linear systems with unknown inputs, IEEE Transactions on Automatic Control 25(1), 113-115, 1980
    locator: the existence conditions, with rank(CE) = rank(E)
---

An unknown input observer estimates the state of

$$\dot x = Ax + Bu + Ed, \qquad y = Cx,$$

where $u$ is measured and $d$ is not. Its error goes to 0 for every signal $d$, with no model of $d$ at all. A [Luenberger observer](/luenberger-observer/) for the same system has the error equation $\dot e = (A - LC)e + Ed$, so $d$ drives the error and the estimate is biased. The unknown input observer makes the error equation $\dot e = Fe$ by a projection that removes the direction $E$ before the correction. This is possible when $\operatorname{rank}(CE) = \operatorname{rank}(E)$, that is, when every unknown input shows up in the output at once, and the error can be made stable when the invariant zeros of $(A, E, C)$ are stable. The design on this page is the full-order observer of Darouach, Zasadzinski and Xu. A [disturbance observer](/disturbance-observer/) solves a different task: it estimates $d$ itself, usually in a limited frequency band, so that a controller can cancel it. The [state observer](/state-observer/) page compares the observers of this area.

## In plain words

A machine is pushed by forces that nobody measures, such as wind or load changes. An ordinary observer copies the machine's model, but its copy does not feel these forces, so its guess drifts away from the truth. An unknown input observer is built so that these forces cannot affect its error at all. It does this by using the sensors twice: once to correct the guess, and once to see in which way the unknown forces have just moved the machine, so that it can ignore that direction. This works only when the sensors see each unknown force at once, and when the machine has no hidden dynamics that the forces can excite without any trace in the output.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, $E \in \mathbb{R}^{n \times q}$ with $\operatorname{rank} E = q$, and a monic real polynomial $\alpha$ of degree $n$. Output: matrices $F, G, K, H$ such that the observer

$$\dot z = Fz + Gu + Ky, \qquad \hat x = z + Hy$$

has $x(t) - \hat x(t) = e^{Ft}(x(0) - \hat x(0))$ for every input $u$ and every unknown input $d$, with $\det(sI - F) = \alpha(s)$.

Darouach, Zasadzinski and Xu showed that an observer of this form with a stable $F$ exists if and only if

1. $\operatorname{rank}(CE) = \operatorname{rank}(E)$, and
2. $\operatorname{rank} \begin{bmatrix} sI - A & -E \\ C & 0 \end{bmatrix} = n + \operatorname{rank}(E)$ for all $s$ with $\operatorname{Re} s \ge 0$.

The second condition says that $(A, E, C)$ has no invariant zeros in the closed right half plane. Condition 1 needs $q \le p$: there must be at least as many outputs as unknown inputs. All eigenvalues of $F$ can be chosen freely if and only if $(A, E, C)$ has no invariant zeros at all. This implementation covers that case and raises an error otherwise. In discrete time the observer is $z_{k+1} = Fz_k + Gu_k + Ky_k$ with the same matrices, and the zeros must lie inside the unit circle.

## The algorithm

```pseudo id=main
UIO(A, B, C, E, alpha)
L1  if rank(C E) < rank(E): fail                      ▷ some d is not seen in y at once
L2  H ← E ((C E)^T (C E))^(-1) (C E)^T                 ▷ then H C E = E
L3  T ← I - H C;  A1 ← T A;  G ← T B                   ▷ T E = 0
L4  K1 ← PLACE(A1^T, C^T, alpha)^T                     ▷ fails if (A, E, C) has invariant zeros
L5  F ← A1 - K1 C;  K ← K1 + F H
L6  return F, G, K, H
UPDATE(z, u, y)
L7  z' ← F z + G u + K y                               ▷ derivative, or next value in discrete time
L8  x_hat ← z + H y
```

Line L2 uses the left inverse of $CE$, which exists by line L1, so $HCE = E$ and the matrix $T = I - HC$ of line L3 annihilates $E$. The observer state $z$ estimates $Tx$, and the term $Hy = HCx$ adds back the part of $x$ that $T$ removes. Line L4 is the observer pole placement of the [Luenberger observer](/luenberger-observer/) applied to the pair $(C, TA)$: Heymann's lemma in the form of Hautus, then [Ackermann's formula](/ackermann-formula/). Line L5 chooses $K$ so that the terms in $x$ cancel in the error equation.

## Example

Take $n = 3$, two outputs and one unknown input that acts on the first state:

$$A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -1 & -3 & -3 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}, \quad E = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}.$$

Here $CE = [1; 0]$ has rank 1, so line L1 passes, and lines L2 and L3 give

$$H = \begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix}, \quad T = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}, \quad TA = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 1 \\ -1 & -3 & -3 \end{bmatrix}.$$

The system has no invariant zeros: a vector with $Cv = 0$ is $v = (0, 0, v_3)$, and $(sI - A)v = Ew$ needs $-v_3 = 0$ in the second row. So $(C, TA)$ is observable. For $\alpha(s) = (s + 2)(s + 3)(s + 4)$ the implementation returns

$$F = \begin{bmatrix} -6 & 1 & 0 \\ -5 & 0 & 1 \\ 9 & -3 & -3 \end{bmatrix}, \qquad K = \begin{bmatrix} 0 & -1 \\ 0 & 0 \\ -1 & 0 \end{bmatrix}.$$

A simulation with $u = \sin t$, the unknown input $d(t) = 0.5 \sin 5t$ plus a unit step at $t = 1$, the initial state $(0.5, 0.3, -0.2)$ and the estimates started at 0 gives the largest error over the three states below. The Luenberger observer has the same poles, from $L = \operatorname{PLACE}(A^T, C^T, \alpha)^T$.

| $t$ | 1 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|
| unknown input observer | 0.048 | 0.0050 | 0.00057 | 7.1e-5 | 1.2e-6 |
| Luenberger observer | 0.070 | 0.68 | 0.69 | 0.55 | 0.64 |

The error of the unknown input observer follows $e^{Ft}$ exactly, whatever $d$ does. The Luenberger observer keeps an error of the size of $d$.

**A system with a zero.** Change $A$ to $\begin{bmatrix} 0 & 1 & 1 \\ 0 & 0 & 0 \\ 1 & -1 & 1 \end{bmatrix}$. Now $v = (0, 0, 1)$ satisfies $Cv = 0$ and $(I - A)v = (-1, 0, 0) = E \cdot (-1)$, so $s = 1$ is an invariant zero. Then $TAv = v$ and $Cv = 0$, so 1 is an eigenvalue of $F = TA - K_1 C$ for every $K_1$, and no stable unknown input observer exists. The input $d(t) = -e^t$ with $x(0) = v$ gives $x(t) = e^t v$ and $y = 0$: a growing state that leaves no trace in the output.

## Correctness

Let $e = x - \hat x = (I - HC)x - z = Tx - z$. Then

$$\dot e = TAx + TBu + TEd - Fz - Gu - KCx.$$

Line L3 gives $TE = 0$ and $G = TB$, so $d$ and $u$ drop out. With $z = Tx - e$, $\dot e = Fe + (TA - FT - KC)x$. Line L5 gives $FT + KC = F - FHC + K_1 C + FHC = F + K_1 C = TA$, so $\dot e = Fe$. Line L4 gives $\det(sI - F) = \alpha(s)$. The eigenvalues of $TA$ that no $K_1$ moves are the invariant zeros of $(A, E, C)$, which is why the second existence condition appears. The full proof is in [proofs/correctness.md](proofs/correctness.md). The tests check $FT + KC = TA$, $TE = 0$ and the exact error $F^k e_0$ for random discrete-time systems driven by random unknown inputs, and the fixed eigenvalue at an invariant zero.

## Complexity

Lines L1 to L3 cost $O(n^2 p + p^3)$, because $CE$ has only $q \le p$ columns. Line L4 is pole placement of size $n$ with $p$ columns, $O(p n^4)$ with the simple rank tests of the implementation. Each update costs $O(n(n + m + p))$.

## Properties

- **Exact decoupling.** The error does not depend on $d$ at all, for any signal: steps, ramps, or noise without a model.
- **Full order.** The observer has $n$ states, although the part $HCx$ of the estimate comes from $y$ directly.
- **Direct feedthrough.** The term $Hy$ passes measurement noise into $\hat x$ without filtering.
- **Estimating $d$.** If $CE$ has full column rank, $d$ can be recovered from $\hat x$ and $\dot y$ by $d = (CE)^+(\dot y - CA\hat x - CBu)$ once the error has decayed. This needs a derivative of $y$.
- **Relation to zeros.** Strong detectability in the sense of Hautus is the condition that the state can be estimated with an error that goes to 0 for every unknown input. With $\operatorname{rank}(CE) = \operatorname{rank}(E)$, the existence condition 2 says that the system from $d$ to $y$ is [minimum phase](/minimum-phase/).

## Variants and improvements

- **Reduced-order unknown input observers.** As for the [reduced-order observer](/reduced-order-observer/), the part of the state that $y$ gives directly need not be estimated, and observers of lower order exist under similar conditions.
- **Fault detection.** Decoupling the error from disturbances while keeping its sensitivity to faults gives residuals that react only to faults. Model-based fault diagnosis uses unknown input observers widely for this purpose.
- **When rank$(CE) <$ rank$(E)$.** Derivatives of $y$, or a sliding-mode term, can restore the decoupling; see [sliding mode observer](/sliding-mode-observer/).
- **Discrete time.** The same matrices work for $x_{k+1} = Ax_k + Bu_k + Ed_k$, with $y_k = Cx_k$.

## When to use it

Use an unknown input observer when a disturbance or an unknown input acts through a known direction $E$, when the outputs see it directly, and when no model of the disturbance is available or wanted. Examples are unknown loads in mechanical systems and unknown inflows in process models. If the disturbance has a known model, such as a constant or a sinusoid, an augmented Luenberger observer or a [disturbance observer](/disturbance-observer/) is often simpler and filters noise better.

## Pitfalls

- **Rank condition.** If an unknown input does not affect $y$ at once ($CE$ rank deficient), no observer of this form exists. Adding a sensor in the direction of $E$ is the usual remedy.
- **Non-minimum-phase zeros.** An invariant zero of $(A, E, C)$ in the right half plane is a fixed unstable eigenvalue of $F$. No gain fixes it.
- **Noise.** The projection $T$ and the term $Hy$ can amplify measurement noise, because the observer trusts $y$ fully in the direction of $CE$.
- **Model error.** The decoupling is exact only for the exact $E$ and $C$. An error in $E$ lets $d$ leak into $e$.

## Implementations

## History

Observers for systems with unknown inputs were studied in the 1970s. Kudva, Viswanadham and Ramakrishna (1980) gave existence conditions with $\operatorname{rank}(CE) = \operatorname{rank}(E)$. Hautus (1983) introduced strong detectability and related it to observers whose error converges for every unknown input. Darouach, Zasadzinski and Xu (1994) gave the full-order observer with $H = E(CE)^+$ and showed that their two conditions are necessary and sufficient for it to exist.

## References
