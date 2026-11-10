---
tag: 7A5KY6
kind: technique
slug: adaptive-rejection-sampling
name: Adaptive rejection sampling
aliases:
- ARS
- Gilks-Wild sampler
area: randomized/sampling
level: advanced
summary: Rejection sampling for log-concave densities whose envelope is refined from rejected points.
prereqs: [rejection-sampling, convex-function, inverse-transform-sampling]
see_also: [rejection-sampling, ratio-of-uniforms, gibbs-sampling, random-variate-generation, slice-sampling, metropolis-hastings, ziggurat-method]
sources:
  - paper: doi:10.2307/2347565
    title: Walter R. Gilks and Pascal Wild, Adaptive rejection sampling for Gibbs sampling, Journal of the Royal Statistical Society, Series C (Applied Statistics) 41(2), 1992
    locator: pages 337 to 348
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter VII, Section 2 (log-concave densities)
  - paper: "Walter R. Gilks, Nicky G. Best and K. K. C. Tan, Adaptive rejection Metropolis sampling within Gibbs sampling, Journal of the Royal Statistical Society, Series C (Applied Statistics) 44(4), 1995"
    locator: pages 455 to 472
---

Adaptive rejection sampling (ARS) is [rejection sampling](/rejection-sampling/) for a log-concave density $f \propto e^{h}$, with an envelope that builds itself. The tangents to the concave function $h$ at a set $T$ of points lie above $h$, so their minimum $u_T$ gives the envelope $e^{u_T}$, a piecewise exponential density that is easy to sample. The chords between neighbouring points lie below $h$ and give a cheap squeeze. Each time the squeeze fails and $h$ is evaluated, the point joins $T$ and the envelope gets tighter. Gilks and Wild introduced it in 1992 for the one-dimensional conditional densities of [Gibbs sampling](/gibbs-sampling/). Every output has density exactly $f$, whatever $T$ is, so the outputs are independent even though the envelope depends on the past.

## In plain words

Rejection sampling needs a curve that sits above the density everywhere, and finding a good one by hand is the hard part.

For a density whose logarithm is a hill with no dips, there is an easy way to get one. Draw straight lines that touch the hill at a few points. Each line stays above the hill everywhere, so the lowest of the lines at each place is a roof over the hill. Straight lines in the log picture are exponential curves in the real picture, and those are easy to sample from.

Every time you have to check a sample against the true curve, you have learned the height of the hill at a new place. Add a touching line there. The roof comes down closer to the hill, and fewer samples are rejected. After a few dozen checks, almost nothing is rejected or checked.

## When it applies

- The target density on an interval $D \subseteq \mathbb{R}$ is $f = e^{h}/Z$ with $h$ concave (log-concave $f$), and $Z$ may be unknown.
- $h$ and its derivative $h'$ can be evaluated. A derivative-free form uses chords instead of tangents.
- Many variates are needed from the same density, or the density changes from call to call and no hand-made method exists, as in Gibbs sampling.
- The starting points: if $D$ is unbounded on the left, the leftmost point needs $h' > 0$, and if it is unbounded on the right, the rightmost point needs $h' < 0$, so that the envelope has finite mass.

Many common densities are log-concave: the normal, the exponential, the gamma and Weibull with shape at least 1, the beta with both parameters at least 1, the logistic, and the posteriors of many generalized linear models. The Student t and Cauchy densities are not.

## The template

Notation: $T = \{x_1 < \dots < x_k\}$ is the current set of points. The upper hull $u_T(x) = \min_j \bigl(h(x_j) + (x - x_j) h'(x_j)\bigr)$ is piecewise linear; neighbouring tangents meet at

$$z_j = \frac{h(x_{j+1}) - h(x_j) - x_{j+1} h'(x_{j+1}) + x_j h'(x_j)}{h'(x_j) - h'(x_{j+1})}.$$

The lower hull $l_T$ is the chord between neighbours on $[x_1, x_k]$ and $-\infty$ outside. The envelope density is $s_T = e^{u_T}/Z_T$ with $Z_T = \int_D e^{u_T}$. The holes are $h$, $h'$, the domain and the starting set $T$.

```pseudo id=main
ARS(h, h′, T, n)
L1  S ← an empty list
L2  while |S| < n do
L3      X ← a sample from s_T ∝ exp(u_T)        ▷ pick a piece by its mass, then invert in it
L4      W ← a uniform real in [0, 1)
L5      if W ≤ exp(l_T(X) − u_T(X)) then append X to S; continue      ▷ squeeze: no h
L6      evaluate h(X) and h′(X)
L7      if W ≤ exp(h(X) − u_T(X)) then append X to S
L8      T ← T ∪ {X}; rebuild u_T, l_T and the piece masses          ▷ after the test
L9  return S
```

Line L3 is [inverse transform sampling](/inverse-transform-sampling/) twice: choose piece $j$ with probability proportional to its mass $\int_{z_{j-1}}^{z_j} e^{u_T}$, then invert the exponential distribution function on that piece. Line L8 runs only when $h$ was evaluated, whether the point was accepted or not.

### Example

Take the standard normal, $h(x) = -x^2/2$, $h'(x) = -x$, and $T = \{-1, 0.5, 2\}$. The tangent at $a$ is $a^2/2 - ax$, and two tangents at $a$ and $b$ meet at $(a + b)/2$, so $z_1 = -0.25$ and $z_2 = 1.25$.

| piece | interval | $u_T(x)$ | mass $\int e^{u_T}$ |
|---|---|---|---|
| 1 | $(-\infty, -0.25]$ | $0.5 + x$ | $e^{0.25} = 1.2840$ |
| 2 | $[-0.25, 1.25]$ | $0.125 - 0.5x$ | $2(e^{0.25} - e^{-0.5}) = 1.3550$ |
| 3 | $[1.25, \infty)$ | $2 - 2x$ | $e^{-0.5}/2 = 0.3033$ |

The envelope has mass $Z_T = 2.9423$, against $\int e^{h} = \sqrt{2\pi} = 2.5066$, so a try is accepted with probability $0.8519$. With $T = \{-1, 1\}$ the envelope is $e^{1/2 - |x|}$, a Laplace shape, and the acceptance probability is $\sqrt{2\pi}/(2e^{1/2}) = 0.7602$. At $X = 0$ with $T = \{-1, 0.5, 2\}$, the squeeze is the chord value $l_T(0) = -0.25$ and $u_T(0) = 0.125$, so line L5 accepts if $W \le e^{-0.375} = 0.687$ without computing $h$. Starting from $T = \{-1, 1\}$, one run of the implementation evaluated $h$ 18 times for the first 100 outputs and 101 times for 40,000 outputs.

### Why it is correct

**Lemma 1 (hulls).** If $h$ is concave and differentiable on $D$, then $l_T \le h \le u_T$ on $D$. If $T \subseteq T'$, then $u_{T'} \le u_T$.

*Proof.* A concave function lies below each of its tangent lines, so $h \le$ each tangent, and $h \le u_T$, their minimum. On $[x_j, x_{j+1}]$ a concave function lies above its chord, so $l_T \le h$ there, and $l_T = -\infty$ elsewhere. Adding points adds lines to the minimum, which can only lower it. $\square$

**Lemma 2 (one try).** Fix the history up to the start of a try, and so the set $T$. The try appends a value in a set $A$ with probability $\frac{Z}{Z_T} \int_A f$, where $Z = \int_D e^{h}$.

*Proof.* $X$ has density $e^{u_T}/Z_T$ and $W$ is uniform and independent. By Lemma 1, $e^{l_T - u_T} \le e^{h - u_T} \le 1$, so the try appends $X$ exactly when $W \le e^{h(X) - u_T(X)}$, through line L5 or line L7. Hence the probability is $\int_A \frac{e^{u_T(x)}}{Z_T} e^{h(x) - u_T(x)}\,dx = \frac{1}{Z_T}\int_A e^{h} = \frac{Z}{Z_T}\int_A f$. $\square$

**Theorem.** If $h$ is concave on $D$ and the starting set gives $Z_{T_0} < \infty$, ARS returns $n$ independent variates with density $f$, and it stops with probability 1.

*Proof.* By Lemma 1, $Z_T \le Z_{T_0}$ for all later $T$, so by Lemma 2 each try appends a value with probability at least $p_0 = Z/Z_{T_0} > 0$, whatever the history. The number of tries for each output is then dominated by a geometric variable with mean $1/p_0$, so the loop stops with probability 1.

Let $Y_1, Y_2, \ldots$ be the outputs and $\mathcal{F}_t$ the history before try $t$. For sets $A$ and $B$, write the event $\{(Y_1, \ldots, Y_{m-1}) \in B,\ Y_m \in A\}$ as a disjoint union over $t$ of the events "the first $m - 1$ outputs are in $B$, try $t$ is the first try after them to append, and it appends a value in $A$". The first two parts are determined by $\mathcal{F}_t$ together with "try $t$ appends". By Lemma 2, given $\mathcal{F}_t$, try $t$ appends a value in $A$ with probability $\frac{Z}{Z_{T_t}}\int_A f$ and appends at all with probability $\frac{Z}{Z_{T_t}}$, so the value is in $A$ with conditional probability $\int_A f$ given that it appends. Summing over $t$ gives $\Pr[(Y_1, \ldots, Y_{m-1}) \in B,\ Y_m \in A] = \Pr[(Y_1, \ldots, Y_{m-1}) \in B] \int_A f$. By induction on $m$, the outputs are independent with density $f$. $\blacksquare$

The order in line L8 matters for this proof: the test in line L7 must use the hull from before $X$ joined $T$. With the new hull, $u_T(X) = h(X)$ and line L7 always accepts, so the output has density $s_T$ instead of $f$.

The theorem is for exact arithmetic. In floating point the hull, the piece masses and the inversion in line L3 are rounded, and nearly equal slopes make $z_j$ inaccurate.

### Cost

- **Per try.** Line L3 picks a piece in $O(\log k)$ with prefix sums of the masses, and inverts one exponential.
- **Evaluations of $h$.** Only tries that fail the squeeze evaluate $h$, and each such try adds a point. In practice the number of points stays small: the run above used 101 for 40,000 outputs. This is an observation, not a proved bound.
- **Updates.** Line L8 rebuilds the hull. A sorted array costs $O(k)$ per insert; the pieces change only next to the new point, so a balanced tree with prefix sums of the masses gives $O(\log k)$.
- **For one variate** from a density that changes every call, as in Gibbs sampling, the cost is a few evaluations of $h$ plus the setup from the starting points.

## Classic examples

- **[Gibbs sampling](/gibbs-sampling/) in hierarchical models.** The full conditional of one parameter is often log-concave with no standard form. ARS samples it with a few evaluations, and its outputs are exact draws, so the Gibbs chain keeps its stationary law.
- **Truncated and nonstandard log-concave laws.** A truncated normal, a gamma with shape at least 1, or a posterior of a logistic regression coefficient.
- **Generalized linear models.** Under a log-concave prior and a log-concave likelihood, each coordinate's conditional posterior is log-concave.
- **The fixed-hull special case.** Stop adding points after a while: the result is ordinary [rejection sampling](/rejection-sampling/) with a piecewise exponential envelope, the same idea as the table methods in Devroye's Chapter VIII and in the [ziggurat method](/ziggurat-method/).

## Variations

- **Derivative-free ARS.** Use the extensions of the chords between neighbouring points as the upper hull: for concave $h$, the line through $(x_j, h(x_j))$ and $(x_{j+1}, h(x_{j+1}))$ lies above $h$ outside $[x_j, x_{j+1}]$. Gilks gave this form in 1992. It needs only $h$, at the cost of a looser envelope.
- **Adaptive rejection Metropolis sampling (ARMS).** Gilks, Best and Tan (1995) extend ARS to densities that are not log-concave by adding a [Metropolis-Hastings](/metropolis-hastings/) step. The outputs are then a Markov chain with stationary law $f$, not independent draws.
- **Other concave transforms.** The same construction works when $T(f)$ is concave for other monotone $T$, such as $-1/\sqrt{f}$. This includes some heavy-tailed densities. The [ratio-of-uniforms](/ratio-of-uniforms/) region is convex in that case.
- **[Slice sampling](/slice-sampling/).** Another way to sample a one-dimensional conditional with no hand-made method; it is an MCMC method, not an exact one.

## Pitfalls

- **A density that is not log-concave.** Then the tangents can cross below $h$, $u_T$ is not an envelope, and the output law is wrong without any warning. Check concavity in theory; a numerical test such as $z_j$ out of order catches only some failures.
- **Bad starting points.** On an unbounded domain, if all starting points lie on one side of the mode, the envelope has infinite mass. Start with points on both sides, where $h'$ has both signs.
- **Updating before the test.** Line L7 must use the hull from before $X$ joins $T$, as shown above.
- **Overflow.** $e^{u_T}$ can overflow. Work with $u_T - \max_j h(x_j)$ when computing the masses.
- **Nearly equal slopes.** When $h'(x_j) \approx h'(x_{j+1})$, the formula for $z_j$ divides by a tiny number. Use the midpoint or skip points too close to an existing one.

## Exercises

1. Show that for a concave $h$, the upper hull from tangents at $T$ equals the piecewise linear function with breaks at the points $z_j$.
2. Prove that the derivative-free hull is an upper bound for concave $h$, and give its formula on each piece.
3. For the standard normal with $T = \{-a, a\}$, compute the acceptance probability as a function of $a$ and find the best $a$.
4. Give a density that is not log-concave and a starting set for which $u_T < h$ somewhere, and compute the output law of one try.

## References
