---
tag: FY3PHK
kind: algorithm
slug: triad-method
name: TRIAD method
aliases:
- TRIAD algorithm
area: robotics/localization-and-slam
level: core
summary: Builds an attitude from exactly two vector observations by forming an orthonormal triad in each frame.
solves: [wahba-problem]
model: real-ram
complexity:
  vars: {n: "the number of vector pairs, which is 2 for TRIAD"}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1964
  people: [Harold D. Black]
  note: Black built an orthonormal frame from two measured directions and the same frame from their known reference directions, and took the rotation between the two frames as the satellite attitude.
prereqs: [wahba-problem, special-orthogonal-group]
see_also: [davenport-q-method, quest-algorithm, attitude-estimation, kabsch-algorithm, rodrigues-rotation-formula, condition-number]
sources:
  - paper: doi:10.2514/3.2555
    title: "Harold D. Black, A passive system for determining the attitude of a satellite, AIAA Journal 2(7), 1964, pages 1350 to 1351"
    locator: "the construction of the attitude from two vector measurements by two orthonormal triads"
  - paper: doi:10.2514/3.19717
    title: "M. D. Shuster and S. D. Oh, Three-axis attitude determination from vector observations, Journal of Guidance and Control 4(1), 1981, pages 70 to 77"
    locator: "the TRIAD algorithm and its error analysis, compared with the optimal QUEST solution"
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 5 (static attitude determination), the TRIAD section"
---

The TRIAD method computes the attitude of a body from two measured directions, such as the Sun and the Earth's magnetic field, whose directions in a reference frame are known. It builds an orthonormal frame, a triad, from the two measured vectors and the same kind of frame from the two reference vectors, and returns the rotation that carries one frame onto the other. It costs a few cross products. The result matches the first pair exactly and uses the second pair only to fix the rotation about the first, so with noise it is not the least-squares solution of [Wahba's problem](/wahba-problem/); [Davenport's q-method](/davenport-q-method/) and [QUEST](/quest-algorithm/) are. The [Kabsch algorithm](/kabsch-algorithm/) solves the same fitting problem for many points by an SVD and is optimal; TRIAD is the cheap exact-for-two-vectors cousin.

## In plain words

Imagine you can see the Sun and also feel which way a compass needle points. Each gives you one direction. One direction alone leaves you free to spin about it. The second direction stops that spin. TRIAD takes the first direction as the main axis, uses the second only to decide which way is "up" around that axis, and adds a third axis at right angles to both. It does the same with the map directions. The rotation that lines up the two sets of axes is your attitude. The first direction is matched perfectly and all the noise of both sensors goes into the second one, so you should put the more trusted sensor first.

## The problem

Given body vectors $b_1, b_2$ and reference vectors $r_1, r_2$ in $\mathbb{R}^3$, nonzero and not parallel within each pair, find a rotation $A \in SO(3)$ with $A r_i \approx b_i$. The convention is that of Wahba's problem: $A = R_{bs} = R_{sb}^T$ maps reference coordinates to body coordinates. TRIAD imposes the extra condition $A r_1 / |r_1| = b_1 / |b_1|$ exactly.

## The algorithm

```pseudo id=main
TRIAD(b_1, b_2, r_1, r_2)                 ▷ returns A with A r_1 ∥ b_1
L1  for each pair (v_1, v_2) in ((b_1, b_2), (r_1, r_2)) do t_1 ← v_1 / |v_1|
L2      c ← v_1 × v_2
L3      if |c| ≤ τ |v_1| |v_2| then error "the vectors are parallel"
L4      t_2 ← c / |c|
L5      t_3 ← t_1 × t_2
L6  return A ← Σ_{k=1}^{3} t_{b,k} t_{r,k}^T          ▷ T_b T_r^T
```

Lines L1 to L5 build the triad $T(v_1, v_2) = (t_1, t_2, t_3)$ for each pair: $t_1$ along the first vector, $t_2$ normal to the plane of the pair, and $t_3$ in the plane, completing a right-handed frame. Line L6 is the product $T_b T_r^T$ of the body triad with the transpose of the reference triad, so $A t_{r,k} = t_{b,k}$ for each $k$. The tolerance $\tau$ is relative; the code uses $\tau = 10^{-12}$.

## Example

Take the data of the [Wahba's problem](/wahba-problem/) page: $r_1 = e_1$, $r_2 = e_2$, and the true attitude $A$ with rows $(0, 1, 0)$, $(0, 0, 1)$, $(1, 0, 0)$, so $b_1 = (0, 0, 1)$ and $b_2 = (1, 0, 0)$.

- Reference triad: $t_{r,1} = e_1$, $t_{r,2} = e_1 \times e_2 = e_3$, $t_{r,3} = t_{r,1} \times t_{r,2} = e_1 \times e_3 = -e_2$.
- Body triad: $t_{b,1} = (0, 0, 1)$, $t_{b,2} = (0, 0, 1) \times (1, 0, 0) = (0, 1, 0)$, $t_{b,3} = (0, 0, 1) \times (0, 1, 0) = (-1, 0, 0)$.
- $A = t_{b,1} e_1^T + t_{b,2} e_3^T - t_{b,3} e_2^T$ has columns $A e_1 = (0, 0, 1)$, $A e_2 = (1, 0, 0)$, $A e_3 = (0, 1, 0)$. These are the columns of the true $A$, so the answer is exact.

Now tilt $b_2$ by $2$ degrees toward $b_1$: $b_2 = (0.999391, 0, -0.034899)$. With $b_1$ first, the body triad does not change, because $t_{b,2}$ is still the normal $(0, 1, 0)$ of the same plane. TRIAD returns the true $A$ again, $b_1$ is matched exactly, and $b_2$ is missed by $2$ degrees. The Wahba loss is $6.0917 \times 10^{-4}$, twice the optimal $3.0461 \times 10^{-4}$, where each vector is missed by $1$ degree. With the order swapped, $b_2$ is matched exactly and the attitude is $2$ degrees off the true one, at the same loss.

## Correctness

The output is always a rotation: each triad is orthonormal with determinant $1$, and a product of rotations is a rotation. It matches the first pair exactly, and the second pair lands in the plane of $b_1$ and $b_2$ at the reference angle from $b_1$. For noise-free data $b_i = A_0 r_i$, the rule $(Q x) \times (Q y) = Q (x \times y)$ for a rotation $Q$ gives $T_b = A_0 T_r$, so TRIAD returns $A_0$. These are theorems under the stated hypotheses; the full statements and proofs are in [the correctness proof](proofs/correctness.md). With noise, TRIAD does not minimize the Wahba loss: the example above has twice the optimal loss.

## Complexity

In the [real RAM](/real-ram/) model, TRIAD performs four cross products, four normalizations and one $3 \times 3$ outer-product sum: a fixed number of arithmetic operations and square roots, so $O(1)$ time and $O(1)$ extra memory. It does no iteration and needs no eigensolver.

## Properties

- **Exact for noise-free data (theorem).** Two non-parallel exact pairs give the true attitude.
- **First vector exact (theorem).** $A r_1$ points along $b_1$ for any valid input, with or without noise.
- **Not optimal (theorem by example).** With noise its Wahba loss is in general higher than the minimum, as in the example.
- **Order dependent (measurement).** With noise, swapping the pairs changes the answer; in the tests a swap moved the attitude by more than $10^{-3}$ rad for noise of a few hundredths of a radian.
- **Scale free.** Only the directions of the inputs matter, so the vectors need not be unit.
- **Sensitive near parallel vectors (measurement).** With a fixed noise level of $0.01$ rad, the mean attitude error grew as the angle between the reference vectors fell from $90$ degrees to $17$ degrees to $3$ degrees.

## Variants and improvements

- **Best sensor first (heuristic).** Since the first pair is matched exactly, put the more accurate measurement first. Shuster and Oh (1981) analyze the error of TRIAD in terms of the two sensor accuracies.
- **Bisector triad (measurement).** Build both triads from $v_1 + v_2$ and $v_1 - v_2$ instead of $v_1$ and $v_2$. The two pairs are then treated alike. In 200 random noisy draws with equal weights, this gave the same rotation as the q-method to $10^{-14}$.
- **Optimal methods.** For more than two vectors, or for unequal weights done right, use the [q-method](/davenport-q-method/), [QUEST](/quest-algorithm/) or the SVD of the attitude profile matrix.

## When to use it

Use TRIAD when there are exactly two directions, one of them much better than the other, and the cost must be minimal, for example a small satellite with a Sun sensor and a magnetometer, or a quick first guess for a filter. Use an optimal solver of [Wahba's problem](/wahba-problem/) when the two sensors are of similar quality, when there are more than two directions, or when a covariance of the result is needed.

## Pitfalls

- **Nearly parallel vectors.** When the two directions are close, $v_1 \times v_2$ is small and its direction is dominated by noise. The attitude error grows roughly like the noise divided by the sine of the angle between the vectors (heuristic, from the proof). A tolerance test only rejects the exact case.
- **Frame conventions.** TRIAD returns $A = R_{bs}$, which maps reference coordinates to body coordinates. The attitude of the body in the reference frame is $A^T$. Mixing the two is the most common bug.
- **Mixed pairs.** $b_1$ must be the measurement of $r_1$, and $b_2$ of $r_2$. Swapping only one side gives a wrong rotation with no warning.
- **No uncertainty.** TRIAD returns no covariance. The error depends on the order, on the angle between the vectors and on both sensor noises.

## Implementations

## History

Black (1964) described the method for a satellite with two passive sensors, one year before Wahba posed the least-squares problem. The name TRIAD refers to the two triads it builds. Shuster and Oh (1981) analyzed its errors and compared it with the optimal solution of Wahba's problem by their QUEST algorithm. Markley and Crassidis (2014) present it with the other static methods of attitude determination.

## References
