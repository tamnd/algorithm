---
tag: G3VDNR
kind: algorithm
slug: verbs-and-adverbs
name: Verbs and adverbs motion interpolation
aliases:
- verbs and adverbs
area: graphics-and-signals/character-animation
level: advanced
summary: Interpolate a set of example motions over a space of control parameters with radial basis functions plus a linear term.
model: real-ram
complexity:
  vars: {n: the number of examples, a: the number of adverbs, q: the number of values per example}
  time: {fit: O(n^3 + n^2 (a + q)), evaluate: O(n (a + q))}
  space: {model: O(n (n + q))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1998
  people: [Charles Rose, Michael F. Cohen, Bobby Bodenheimer]
  note: "Rose, Cohen and Bodenheimer described verbs and adverbs in IEEE Computer Graphics and Applications in 1998."
prereqs: [motion-blending, radial-basis-function-interpolation]
see_also: [pose-space-deformation, registration-curves, least-squares-problem, gaussian-elimination, b-spline, gaussian-process, style-based-inverse-kinematics, motion-matching]
sources:
  - paper: doi:10.1109/38.708559
    title: "Charles Rose, Michael F. Cohen and Bobby Bodenheimer, Verbs and adverbs, multidimensional motion interpolation, IEEE Computer Graphics and Applications 18(5), 1998, 32 to 40"
    locator: "the verbs and adverbs, the time alignment by keytimes, the interpolation by a linear part plus radial basis functions, and the verb graph"
  - paper: doi:10.2312/SCA03/214-224
    title: "Lucas Kovar and Michael Gleicher, Flexible automatic motion blending with registration curves, ACM SIGGRAPH/Eurographics Symposium on Computer Animation, 2003, 214 to 224"
    locator: the automatic time alignment of example motions for a weighted blend
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: the material on motion capture data and its processing
---

Verbs and adverbs makes a new motion for any point in a space of control parameters from a small set of example motions.
A verb is an action, such as walk or reach.
Its adverbs are the numbers that describe how it is done, such as the speed and the turn of a walk, or the target of a reach.
Each of the $n$ examples has an adverb point $p_i$ and the values $y_i$ of its time aligned joint curves.
The interpolant is

$$y(p) = c_0 + C p + \sum_{i=1}^{n} w_i\, R_i(|p - p_i|),$$

a linear part fitted by least squares, plus [radial basis functions](/radial-basis-function-interpolation/) that pass exactly through the examples.
The linear part gives a sensible trend between and beyond the examples; the radial part adds the detail that the linear part misses, and it is zero far from all examples.
Rose, Cohen and Bodenheimer (1998) presented the method with a verb graph that joins verbs by transitions.

## In plain words

You have captured a few walks: slow, fast, turning left, turning right, and some in between.
Each walk has a label with its speed and its turn.
Now you want a walk with a speed and turn that you did not capture.
The method first finds the straight line trend: how the joint curves change, on average, as the speed or the turn goes up.
That trend alone does not go through each captured walk exactly.
So the method adds small bumps, one at each captured walk, that fix the difference there and fade away with distance.
The new walk is the trend plus the bumps.

## The problem

The input is $n$ example motions of one verb, all time aligned to a common structure of keytimes (for a walk: heel strike, toe off, the next heel strike), so that frame $u$ of the normalized time means the same moment of the step in every example.
Each example $i$ has an adverb vector $p_i \in \mathbb{R}^a$ and a value vector $y_i \in \mathbb{R}^q$: for example the control points of the [B-spline](/b-spline/) curves of all joints, and the keytimes.
The task is a function $y(p)$ that reproduces every example, $y(p_i) = y_i$, is smooth, and stays close to a linear trend away from the examples.

The output for a query $p$ is a value vector; rebuilding the joint curves from it and playing them over the interpolated keytimes gives the motion.
The interpolation acts on each value separately: all values use the same radial functions, and each value has its own coefficients.

## The algorithm

```pseudo id=main
FIT-VERB(P, Y)                                   ▷ adverb points pᵢ, value vectors yᵢ
L1  X ← the rows (1, pᵢ)                         ▷ an n × (a + 1) matrix
L2  [c₀; C] ← (XᵀX)⁻¹ XᵀY                        ▷ the least squares linear part
L3  eᵢ ← yᵢ - (c₀ + C pᵢ) for every example      ▷ the residuals
L4  αᵢ ← 2 · min over k ≠ i of |pᵢ - pₖ|         ▷ the support of Rᵢ, a choice of the code
L5  K[r][i] ← Rᵢ(pᵣ) = B(2 |pᵣ - pᵢ| / αᵢ)       ▷ B is the cubic B-spline, zero beyond 2
L6  W ← K⁻¹ E                                    ▷ the radial weights, one row per example
EVALUATE(p)
L7  return c₀ + C p + Σᵢ wᵢ Rᵢ(p)
```

The radial function is the uniform cubic B-spline $B(s) = 2/3 - s^2 + s^3/2$ for $0 \le s < 1$, $B(s) = (2 - s)^3 / 6$ for $1 \le s < 2$, and $0$ beyond.
So $R_i$ is $2/3$ at $p_i$ and zero at the distance $\alpha_i$ and beyond.
The paper uses radial cubic B-splines with a width that depends on the spacing of the examples; the rule of line L4, twice the distance to the nearest other example, is the choice of the code.
Because the $\alpha_i$ differ, $K$ is not symmetric, and the code solves it by [Gaussian elimination](/gaussian-elimination/) with partial pivoting.

The interpolant is linear in the example values, so it can also be written as $y(p) = \sum_i b_i(p)\, y_i$ with weights $b_i(p)$ that depend only on the adverb points: a weighted [blend](/motion-blending/) of the examples.
This form is how the method drives a blend of motions directly.

## Example

**By hand.**
One adverb, three examples $p = 0, 1, 2$ with the scalar values $y = 0, 1, 0$.
Line L2: the mean of $p$ is 1 and the mean of $y$ is $1/3$, and $\sum (p - 1)(y - 1/3) = 1/3 + 0 - 1/3 = 0$, so the slope is 0 and the linear part is the constant $1/3$.
Line L3: the residuals are $-1/3$, $2/3$, $-1/3$.
Line L4: every example has its nearest neighbor at distance 1, so every $\alpha_i = 2$ and $R_i(p) = B(|p - p_i|)$.
Line L5: $B(0) = 2/3$, $B(1) = 1/6$ and $B(2) = 0$, so

$$K = \begin{pmatrix} 2/3 & 1/6 & 0 \\ 1/6 & 2/3 & 1/6 \\ 0 & 1/6 & 2/3 \end{pmatrix}, \qquad K w = \begin{pmatrix} -1/3 \\ 2/3 \\ -1/3 \end{pmatrix}.$$

By symmetry $w_1 = w_3 = s$ and $w_2 = t$, with $\tfrac23 s + \tfrac16 t = -\tfrac13$ and $\tfrac13 s + \tfrac23 t = \tfrac23$, so $s = -6/7$ and $t = 10/7$.
At $p = 0.5$: $B(0.5) = 0.479167$ for the first two examples and $B(1.5) = 0.020833$ for the third, and

$$y(0.5) = \tfrac13 + \left(-\tfrac67 + \tfrac{10}{7}\right)(0.479167) - \tfrac67 (0.020833) = 0.589286 .$$

At $p = 1$ the value is 1, the example.
At $p = 3$ only the third radial function reaches, $R_3 = B(1) = 1/6$, and $y(3) = 1/3 - 1/7 = 0.190476$.
At $p = -2$ no radial function reaches, and $y = 1/3$, the linear part.

**A measured case.**
The test uses two adverbs, a speed in $[0.5, 2.5]$ and a turn in $[-1, 1]$, and 8 values per example from a smooth nonlinear function.
With 25 random examples (seed 5) and 200 random test points, the squared error, summed over the 8 values and averaged over the test points, is 0.0026 for the full interpolant and 0.0171 for the linear part alone.
This is a measurement on one function, not a bound.

## Correctness

The proof file works under two hypotheses: (H1) the adverb points do not all lie on one hyperplane, so $X^T X$ is nonsingular; (H2) the matrix $K$ is nonsingular.
H2 is not proved for these radial functions; the code raises an error if $K$ is singular.
Under them it shows:

- Lines L1 to L3 give the least squares linear part, and the residuals are orthogonal to the constant and to every adverb.
- The interpolant reproduces every example exactly (Theorem 1).
- If the examples come from a linear function, the radial weights are zero and the interpolant is that linear function everywhere (Theorem 2).
- Beyond the distance $\alpha_i$ from every example, only the linear part is left.

How well the interpolant matches motion that was not captured is only measured.
The choice of adverbs, the time alignment, and the radial widths are tuning, and that an interpolated walk looks natural is a visual heuristic.

## Complexity

The linear part needs $X^T X$ and $X^T Y$ in $O(n a (a + q))$ and a solve in $O(a^3 + a^2 q)$.
The matrix $K$ costs $O(n^2 a)$, and its solve costs $O(n^3 + n^2 q)$.
With $a < n$, fitting costs $O(n^3 + n^2 (a + q))$ time.
Evaluation costs $O(a q)$ for the linear part and $O(n (a + q))$ for the radial part.
The model stores $K$ during the fit and the weights, $O(n (n + q))$ space.
The paper uses tens of examples per verb, so the cost is small; the values $q$ (control points of all joints) dominate.

## Properties

- **Exact at the examples.** Under H1 and H2, every example is reproduced.
- **Linear far away.** Outside the supports of all radial functions, the result is the linear trend, which keeps extrapolation sane for a small distance.
- **Linear in the values.** The result is a weighted sum of the example values, with weights that depend only on the adverb points.
- **Not convex.** Weights can be negative, so the result is not always between the examples; the hand example has a negative radial weight.

## Variants and improvements

- **Pseudo examples.** Later work by Rose, Sloan and Cohen adds examples made from the interpolant itself to make the weights better behaved over the space.
- **Weights per example.** Precompute the cardinal weights $b_i(p)$ on a grid of adverbs and blend the examples with them, as in a [blend](/motion-blending/) tree.
- **Other kernels.** Gaussian, thin plate or polyharmonic radial functions with a polynomial part; a [Gaussian process](/gaussian-process/) gives the same form with a statistical reading.
- **Pose space deformation.** [Pose space deformation](/pose-space-deformation/) uses the same radial interpolation for corrective shapes of a mesh over joint angles instead of motions over adverbs.
- **Automatic alignment.** [Registration curves](/registration-curves/) replace the hand set keytimes by an automatic timewarp.

## When to use it

Use verbs and adverbs when a few captured or hand made examples must cover a continuous range of a parameter, such as walk speed or reach target, and when exact reproduction of the examples matters.
It needs good time alignment of the examples, and a sensible choice of adverbs.
For a large database with no parameterization, [motion matching](/motion-matching/) searches the data instead.

## Pitfalls

- **Bad time alignment.** If the keytimes do not match, the interpolant blends different phases, and the feet slide.
- **Points on a line.** If all examples vary only in speed, there is no information about the turn; the fit is singular in that direction (H1 fails).
- **Close examples.** Two examples very close in adverb space but with different values make $K$ ill conditioned and the weights large.
- **Extrapolation.** Far outside the examples, only the linear trend is left; a walk at three times the fastest example speed is a linear guess.
- **The name.** "Motion interpolation" is also an alias of [motion blending](/motion-blending/), which mixes clips with weights given by the user.

## Implementations

## History

Charles Rose, Michael F. Cohen and Bobby Bodenheimer described verbs and adverbs in 1998, with the keytime alignment, the radial interpolation with a linear part, and a verb graph whose edges are transitions between verbs.
Peter-Pike Sloan, Charles Rose and Michael Cohen later used the same interpolation for shapes, and Rose, Sloan and Cohen applied it to inverse kinematics from examples.
Radial basis function interpolation itself is older and comes from the interpolation of scattered data.

## References
