---
tag: 2XBS61
kind: algorithm
slug: linear-bound-propagation
name: Linear bound propagation
aliases:
- CROWN
area: security-and-privacy/adversarial-machine-learning
level: research
summary: "Bounds each neuron by linear functions of the input through linear relaxations of the activations, which usually gives tighter certificates than intervals."
model: real-ram
complexity:
  vars: {K: the number of layers, n: the width of the widest layer, N: the number of weights, d: the input dimension}
  time: {worst: O(K n N + K n d)}
  space: {extra: O(n^2 + n d + K n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Eric Wong, J. Zico Kolter, Tsui-Wei Weng, Huan Zhang, Gagandeep Singh, Martin Vechev]
  note: "In 2018 Wong and Kolter bounded ReLU networks through the dual of a linear relaxation, Weng et al. gave Fast-Lin, and Zhang et al. gave CROWN for general activations. DeepPoly of Singh et al. (POPL 2019) is the same idea as an abstract domain."
prereqs: [relu, interval-bound-propagation, adversarial-example]
see_also: [interval-bound-propagation, reluplex, neural-network-verification-problem, randomized-smoothing, abstract-interpretation, lagrangian-duality, convex-hull, adversarial-training]
sources:
  - url: https://arxiv.org/abs/1811.00866
    title: Huan Zhang, Tsui-Wei Weng, Pin-Yu Chen, Cho-Jui Hsieh and Luca Daniel, Efficient neural network robustness certification with general activation functions, NeurIPS 2018
    locator: the linear upper and lower bounds of each activation, the adaptive lower bound for ReLU, and the backward computation of the bound of each layer
  - url: https://proceedings.mlr.press/v80/weng18a.html
    title: Tsui-Wei Weng, Huan Zhang, Hongge Chen, Zhao Song, Cho-Jui Hsieh, Luca Daniel, Duane Boning and Inderjit Dhillon, Towards fast computation of certified robustness for ReLU networks, ICML 2018, PMLR 80, pages 5276 to 5285
    locator: Fast-Lin, the linear bounds of ReLU networks with equal upper and lower slopes, and the hardness of the exact minimum distortion
  - url: https://proceedings.mlr.press/v80/wong18a.html
    title: Eric Wong and J. Zico Kolter, Provable defenses against adversarial examples via the convex outer adversarial polytope, ICML 2018, PMLR 80, pages 5286 to 5295
    locator: the convex relaxation of the ReLU, its dual network, and training against the bound
  - paper: "Gagandeep Singh, Timon Gehr, Markus Püschel and Martin Vechev, An abstract domain for certifying neural networks, Proceedings of the ACM on Programming Languages 3, POPL 2019"
    locator: the DeepPoly domain, with one linear lower and one linear upper bound per neuron and back-substitution
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

Linear bound propagation bounds each output of a ReLU network over an input box by a linear function of the input, and then minimizes that linear function over the box in closed form. Each ReLU whose pre-activation $z$ can have both signs on the box, with bounds $l < 0 < u$, is replaced by two lines: the chord $u(z - l)/(u - l)$ above it and a line $\alpha z$ with $0 \le \alpha \le 1$ below it. A backward pass from the output to the input substitutes these lines layer by layer, using the lower line where the coefficient is positive and the upper line where it is negative. CROWN of Zhang et al. (2018) is the best known member of the family; Fast-Lin, the dual network of Wong and Kolter and DeepPoly compute closely related bounds. The bounds are sound and incomplete, and they are usually much tighter than [interval bound propagation](/interval-bound-propagation/).

**Threat model.** The method is a defense, a verifier, so the threat model is the one that the certificate covers. The goal can be untargeted or targeted, since the certificate bounds the margin against every other label. The knowledge is unlimited: the certificate holds against a white-box attacker. The capability is a change at test time within $B_\infty(x, \epsilon) \cap [0,1]^d$.

## In plain words

A ReLU unit is a bent line: flat at zero on the left, rising on the right. Over the inputs that a unit can see, the method traps the bent line between two straight lines, one above and one below.

Once every bent unit is replaced by straight lines, the whole network is trapped between straight functions of the input. The method builds the lower straight function by working back from the output: each time it meets a unit, it picks the line that keeps the result a true lower bound.

A straight function over a box is smallest at a corner, and that corner is easy to find. If the smallest value of the right class minus each other class is positive, the label cannot change. Straight lines keep track of how the units depend on the same inputs, which plain ranges forget.

## The problem

Take a network with layers $(W_1, b_1), \dots, (W_K, b_K)$, a ReLU after every layer except the last, and the pre-activations $z_k = W_k a_{k-1} + b_k$, $a_0 = x$, $a_k = \mathrm{relu}(z_k)$. Given a box $l \le x \le u$ and a matrix $\Lambda$, compute a vector $\underline m$ with $\underline m \le \Lambda z_K(x)$ for every $x$ in the box. For robustness at $x$ with label $y$, the rows of $\Lambda$ are $e_y - e_j$ for $j \ne y$, the box is $B_\infty(x, \epsilon) \cap [0,1]^d$, and the point is certified when every entry of $\underline m$ is positive. This is a relaxation of the [neural network verification problem](/neural-network-verification-problem/), which is NP-complete.

## The algorithm

```pseudo id=main
LBP-BACKWARD(layers, k, Λ, l, u)               ▷ a lower bound of Λ z_k(x) for l <= x <= u
L1  A ← Λ, c ← 0                               ▷ the bound so far is A z_j + c
L2  for j ← k downto 1 do
L3      c ← c + A b_j
L4      A ← A W_j                              ▷ now the bound is A a_{j-1} + c
L5      if j > 1 then                          ▷ a_{j-1} = relu(z_{j-1}), z_{j-1} in [l_{j-1}, u_{j-1}]
L6          for each unit i of layer j - 1 do
L7              (s+, t+, s-, t-) ← RELAX(l_{j-1,i}, u_{j-1,i})
L8              for each row r of A do
L9                  if A[r, i] >= 0 then c_r ← c_r + A[r, i] t-, A[r, i] ← A[r, i] s-
L10                 else c_r ← c_r + A[r, i] t+, A[r, i] ← A[r, i] s+
L11 m_r ← c_r + sum over t of A[r, t] · (l_t if A[r, t] >= 0 else u_t), for each row r
L12 return m
LBP(layers, l, u, Λ)
L13 for k ← 1 to K - 1 do
L14     l_k ← LBP-BACKWARD(layers, k, I, l, u), u_k ← -LBP-BACKWARD(layers, k, -I, l, u)
L15 return LBP-BACKWARD(layers, K, Λ, l, u)
```

RELAX$(l, u)$ returns the slope and intercept of the upper line $(s^+, t^+)$ and of the lower line $(s^-, t^-)$ of the ReLU on $[l, u]$. If $u \le 0$ both lines are $0$. If $l \ge 0$ both are the identity. Otherwise the upper line is the chord, $s^+ = u/(u - l)$ and $t^+ = -s^+ l$, and the lower line is $\alpha z$ with $\alpha = 1$ if $u \ge -l$ and $\alpha = 0$ if not, the adaptive choice of CROWN. Any $\alpha \in [0, 1]$ is sound.

Lines L1 to L4 move the bound through one affine layer, which is exact. Lines L5 to L10 move it through a ReLU layer: a positive coefficient needs a lower bound of the unit (line L9), and a negative coefficient needs an upper bound (line L10). Line L11 minimizes the final linear function of $x$ over the box, one coordinate at a time. Lines L13 and L14 compute the pre-activation bounds that RELAX needs, layer by layer from the input, with the same backward pass.

## Example

Take the network of the [interval bound propagation](/interval-bound-propagation/) page: $W_1 = \begin{pmatrix} 2 & -1 \\ 1 & -2 \end{pmatrix}$, $b_1 = (0, 0.5)$, $W_2 = \begin{pmatrix} 1 & -1 \\ -2 & 2 \end{pmatrix}$, $b_2 = (1, 0)$, the point $x = (0.5, 0.5)$ with $z(x) = (1.5, -1)$ and label $y = 0$, and $\epsilon = 0.25$. The margin is $m = z_0 - z_1 = 3 a_1 - 3 a_2 + 1$, so $\Lambda$ times the last layer has the row $(3, -3)$ and the constant $1$.

Lines L13 and L14 give the first-layer bounds $z_{1,1} \in [-0.25, 1.25]$ and $z_{1,2} \in [-0.75, 0.75]$, the same as the intervals, since one affine layer is exact. Both units are unstable.

| unit | $[l, u]$ | upper line | lower line ($\alpha$) | coefficient | line used |
|---|---|---|---|---|---|
| 1 | $[-0.25, 1.25]$ | $\tfrac56 z + \tfrac{5}{24}$ | $z$ ($u \ge -l$, so $\alpha = 1$) | $3$ | lower (L9) |
| 2 | $[-0.75, 0.75]$ | $\tfrac12 z + 0.375$ | $z$ ($u \ge -l$, so $\alpha = 1$) | $-3$ | upper (L10) |

The backward pass for $\Lambda$ at $k = 2$: line L3 gives $c = 1$ and line L4 gives $A = (3, -3)$. Line L9 keeps $3 z_{1,1}$, and line L10 turns $-3 a_2$ into $-1.5 z_{1,2} - 1.125$, so $c = -0.125$ and $A = (3, -1.5)$. In the next round line L3 adds $A b_1 = -0.75$, so $c = -0.875$, and line L4 gives $A = A W_1 = (4.5, 0)$. The bound is $m \ge 4.5 x_1 - 0.875$: the input $x_2$ cancels. Line L11 puts $x_1 = 0.25$ and gives $\underline m = 0.25 > 0$, so the point is certified.

Interval bound propagation gives $-1.25$ on the same box and fails, and the exact minimum is $1$. For $\epsilon \le 1/6$ the bound is $2.5 - 9\epsilon$ (it is $1.6$ at $\epsilon = 0.1$, equal to the exact minimum), and the same formula holds up to $\epsilon = 5/18 \approx 0.278$, which is the radius that this method certifies. Interval bounds certify $5/36$ and the exact radius is $5/12$.

## Correctness

**Theorem (soundness).** If the bounds $l_j, u_j$ used by RELAX contain every pre-activation $z_j(x)$ for $x$ in the box, then the vector $m$ of line L12 satisfies $m \le \Lambda z_k(x)$ for every $x$ in the box. By induction over the layers in line L13, all intermediate bounds are sound, and so is the result of line L15. If every entry is positive for the margin rows, no point of $B_\infty(x, \epsilon) \cap [0,1]^d$ changes the label.

The proof keeps the invariant $\Lambda z_k(x) \ge A v + c$ for every $x$ in the box, where $v$ is $z_j(x)$ at the top of round $j$ and $a_{j-1}(x)$ after line L4. Lines L3 and L4 are an identity, because $z_j = W_j a_{j-1} + b_j$. Line L9 uses $A_{ri} a_i \ge A_{ri}(s^- z_i + t^-)$ for $A_{ri} \ge 0$, and line L10 uses $A_{ri} a_i \ge A_{ri}(s^+ z_i + t^+)$ for $A_{ri} < 0$; both follow from the two lines of RELAX, which lie below and above the ReLU on $[l, u]$. Line L11 is the exact minimum of a linear function over a box. If the first hidden layer is stable on the box, every line is exact, and the bound equals the true minimum. The full proof is in `proofs/correctness.md`.

## Complexity

- **Time.** One backward pass from layer $k$ with $r$ rows costs $O(r N)$ for lines L3 and L4 over all layers, plus $O(r n)$ per ReLU layer. Line L14 runs it with $r = 2 n_k$ rows for every hidden layer, so the total is $O(K n N)$, plus $O(K n d)$ for line L11. This is about $n$ times more than interval bounds.
- **Space.** The matrix $A$ has $r$ rows and at most $\max(n, d)$ columns, so $O(n^2 + n d)$, plus $O(K n)$ for the stored bounds.
- **Cheaper forms.** Bounding only the last layer with linear bounds and the hidden layers with intervals (CROWN-IBP) costs $O(k N)$ for $k$ logits.

## Properties

- **Sound, not complete.** A positive bound is a proof (a theorem); a negative one proves nothing.
- **A lower bound on robust accuracy.** The certified fraction of a test set is a lower bound, and an attack gives an upper bound.
- **Exact on stable networks.** If no unit is unstable on the box, every substitution is exact and the bound equals the true minimum.
- **Usually tighter than intervals, but not always.** With the adaptive $\alpha$, the bound is not always above the interval bound. On 2000 random networks with 2 inputs and 2 to 6 hidden units at $\epsilon = 0.2$, it was tighter in 1102 cases, equal in 696 and looser in 202 (a measurement made for this page). Taking the larger of the two bounds is always sound.
- **Linear in the margin.** The bound of a sum of rows is at least the sum of the bounds, so folding the margin into $\Lambda$ (as in the example) is better than bounding each logit alone.

## Variants and improvements

- **Fast-Lin.** Weng et al. (2018) use the chord slope for the lower line too, $s^- = s^+$ and $t^- = 0$, which makes the two lines parallel.
- **Optimized slopes.** The lower slope $\alpha$ of each unit can be any number in $[0, 1]$. Choosing it by gradient steps on the final bound (alpha-CROWN, Xu et al. 2021) gives tighter bounds at a higher cost.
- **The dual view.** Wong and Kolter (2018) bound the same relaxation through the [Lagrangian dual](/lagrangian-duality/) of a linear program, and they train networks against the bound.
- **DeepPoly.** Singh et al. (2019) keep one lower and one upper linear bound per neuron, in terms of the previous layer, and back-substitute to the input, as an abstract domain in the sense of [abstract interpretation](/abstract-interpretation/).
- **Branch and bound.** Splitting an unstable unit into its two phases removes its relaxation. Doing this in a search tree, with linear bounds at each node, gives complete verifiers such as beta-CROWN (Wang et al. 2021), which are compared with [Reluplex](/reluplex/) on the same problems.

## When to use it

Use linear bound propagation to verify a network that was trained without a verifier in mind, when interval bounds are too loose and an exact method such as [Reluplex](/reluplex/) is too slow. It is also the bounding step inside most modern complete verifiers. For very large models or large $\ell_2$ radii, [randomized smoothing](/randomized-smoothing/) is the usual alternative.

## Pitfalls

- **The wrong line for the sign.** Line L9 must use the lower line for a positive coefficient and line L10 the upper line for a negative one. Swapping them gives a number that is not a bound at all, and it can certify a point that has an adversarial example.
- **Intermediate bounds from the wrong layer.** RELAX at line L7 needs the bounds of the pre-activation $z_{j-1}$, computed by line L14 before the backward pass reaches it. Using the bounds after the ReLU, or the bounds of another layer, breaks the invariant.
- **An unsound lower slope.** A lower line $\alpha z$ with $\alpha$ outside $[0, 1]$, or the chord used as a lower line with a nonzero intercept, crosses above the ReLU on part of $[l, u]$.
- **Expecting it to beat intervals every time.** As the properties above show, the adaptive $\alpha$ can lose to interval bounds. A verifier that wants the best of both takes the elementwise maximum of the two lower bounds.
- **Floating point.** The theorem is in exact arithmetic. A certificate meant as a proof must round outward in lines L3, L4 and L11.

## Implementations

The code of this page is an abstract model on synthetic data. The verifier runs only on small ReLU networks that the tests build from a fixed seed, either with random weights or from `mlkit.tiny_relu_net`, on seeded random inputs. It never reads real data or touches a real system. The tests check the example and the radius $5/18$, that the two lines of RELAX bound the ReLU, that the first-layer bounds equal the exact intervals, that a point box is exact, soundness on 500 random networks against the exact range from an enumeration of all activation patterns and against sampling, exactness when the first layer is stable, and that no sampled input breaks a certified point.

## History

After adversarial examples were found, exact verifiers such as [Reluplex](/reluplex/) (2017) showed that verification is possible but slow. In 2018 several groups found fast sound bounds from linear relaxations of the ReLU. Wong and Kolter (ICML 2018) used the convex outer bound of the ReLU and its dual network, and trained networks to be provably robust. Weng et al. (ICML 2018) gave Fast-Lin with parallel linear bounds, and Zhang et al. (NeurIPS 2018) gave CROWN, with separate upper and lower lines and support for general activations. Singh et al. described the same kind of bound as the DeepPoly abstract domain (POPL 2019). Later work optimized the slopes and combined the bounds with branch and bound, and verifiers built this way are now the usual tools for complete verification of ReLU networks.

## References
