---
tag: 9TVS4B
kind: technique
slug: inverse-lithography-technology
name: Inverse lithography technology
aliases:
- ILT
- pixel-based mask optimization
area: eda/power-reliability-and-manufacturability
level: research
summary: Treats mask design as an inverse problem and optimizes mask pixels by gradient methods so the printed image matches the target, beyond rule- or model-based OPC.
prereqs: [sum-of-coherent-systems, gradient-descent]
see_also: [optical-proximity-correction, hopkins-imaging-model, level-set-method, total-variation-denoising, tikhonov-regularization, projected-gradient-descent, automatic-differentiation, phase-retrieval]
sources:
  - paper: doi:10.1109/TIP.2006.891332
    title: Amyn Poonawala and Peyman Milanfar, Mask design for optical microlithography, an inverse imaging problem, IEEE Transactions on Image Processing 16(3), 774 to 788, 2007
    locator: mask design posed as an inverse imaging problem over a pixel mask, with a sigmoid model of the resist, analytic gradients and regularization terms
  - paper: doi:10.1016/j.mee.2007.02.005
    title: Amyn Poonawala and Peyman Milanfar, A pixel-based regularization approach to inverse lithography, Microelectronic Engineering 84(12), 2837 to 2852, 2007
    locator: Section 2 (sigmoid resist and the L2 cost), equation (19) for the transformation m = (1 + cos theta)/2, equation (21) for the gradient with two convolutions, and Section 3.2 for the discretization, complexity and aerial image penalty terms
  - paper: doi:10.1117/12.7972810
    title: Bahaa E. A. Saleh and Soheil I. Sayegh, Reduction of errors of microphotographic reproductions by optimal corrections of original masks, Optical Engineering 20(5), 781 to 784, 1981
    locator: an image restoration algorithm that computes the optimal correction of a mask for a diffraction-limited system and a highly nonlinear film, with serifs computed for corners
  - paper: doi:10.1364/OE.17.023690
    title: Yijiang Shen, Ngai Wong and Edmund Y. Lam, Level-set-based inverse lithography for photomask synthesis, Optics Express 17(26), 23690 to 23701, 2009
    locator: a complete level set formulation of inverse lithography with an efficient numerical solution, compared against pixel gradient methods
---

Inverse lithography technology, or ILT, designs a photomask by solving an inverse problem: find the mask whose printed pattern is closest to the target layout under a model of the optics and the resist. The mask is a grid of pixels, each a variable, and the cost is minimized by gradient methods. Where [optical proximity correction](/optical-proximity-correction/) moves the edges of the existing shapes, ILT may put light anywhere, so assist features and curved shapes come out of the optimization rather than from rules. The image model is the [Hopkins model](/hopkins-imaging-model/), in practice in its [sum of coherent systems](/sum-of-coherent-systems/) form, which also gives the gradient cheaply. Saleh and Sayegh posed the problem in 1981; the pixel formulation with a sigmoid resist and regularization terms used below is that of Poonawala and Milanfar (2007).

## In plain words

A lens blurs the mask, so a mask drawn exactly like the wanted pattern prints the wrong shapes. Small lines print too thin, lines in a crowd print differently from lines alone, and corners come out round.

Inverse lithography starts from the result. It asks which mask would print the wanted pattern, and it searches for that mask directly. The mask is cut into many tiny squares, each either clear or dark. A computer model predicts what each choice prints. The method then nudges every square a little in the direction that makes the print look more like the target, and repeats.

Extra penalty terms keep each square close to fully clear or fully dark and keep the shapes simple enough to make. The masks it finds often have odd curves and small extra shapes beside the real ones, which help the real shapes print but do not print themselves.

## When it applies

- The forward model is known and differentiable: an imaging model with fixed source and pupil, and a smooth model of the resist.
- The patterns are near the resolution limit, where edge-based correction does not reach the target or needs assist features that rules cannot place well.
- The compute budget allows many forward and gradient evaluations. This held first for hot spots and small cells, and with fast hardware it reaches larger areas.
- The mask writer can make the result, or the result is simplified to shapes it can write. Curved shapes need a mask writer that supports them.

## The template

Let $z^*$ be the target, a binary pixel image. Let the optics be given by kernels $\phi_j$ with weights $\lambda_j \ge 0$, so the aerial image of a mask $m$ is $I(m) = \sum_j \lambda_j |\phi_j * m|^2$, the [sum of coherent systems](/sum-of-coherent-systems/). The resist is the sigmoid $\operatorname{sig}(u) = 1/(1 + e^{-a(u - t_r)})$, a smooth stand-in for a threshold $t_r$, and the printed pattern is $z = \operatorname{sig}(I(m))$. The cost is

$$ C(m) = \|z - z^*\|_2^2 + \gamma_{\mathrm{dis}} R_{\mathrm{dis}}(m) + \gamma_{\mathrm{TV}} R_{\mathrm{TV}}(m), $$

with the discretization penalty $R_{\mathrm{dis}}(m) = \sum_k 4 m_k (1 - m_k)$, which is zero exactly on binary masks, and the complexity penalty $R_{\mathrm{TV}}(m) = \|Q_x m\|_1 + \|Q_y m\|_1$, the sum of the absolute differences of neighboring pixels, as in [total variation denoising](/total-variation-denoising/). To keep $m_k \in [0, 1]$ without constraints, write $m_k = (1 + \cos \theta_k)/2$ with free variables $\theta_k$.

```pseudo id=main
INVERSE-LITHOGRAPHY(target z*, kernels (λ_j, φ_j), threshold t_r, steepness a, weights γ, step s)
L1  θ_k ← arccos(2 z*_k − 1) for each pixel k, with z* clipped into (0, 1)
L2  repeat
L3      m ← (1 + cos θ) / 2
L4      E_j ← φ_j * m for each kernel j;  I ← Σ_j λ_j |E_j|^2
L5      z ← sig(I)
L6      g ← ∇_m C(m), with two convolutions per kernel for the data term
L7      θ ← θ + s · g ⊙ sin θ / 2
L8  until the cost stops falling or an iteration limit is reached
L9  return the mask m rounded to {0, 1}, then cleaned to meet the mask rules
```

The holes are the imaging model in line L4, the resist model in line L5, the penalties and their weights in line L6, the step rule in line L7, and the cleanup in line L9. Line L7 is a [gradient descent](/gradient-descent/) step in $\theta$: since $\partial m_k / \partial \theta_k = -\frac12 \sin \theta_k$, the gradient in $\theta$ is $-\frac12 g \odot \sin\theta$.

**Claim 1 (the gradient of the data term).** Let $F(m) = \sum_x (z(x) - z^*(x))^2$ for a real mask $m$, and let $w = (z - z^*) \odot z \odot (1 - z)$. Then

$$ \nabla_m F = 4a \sum_j \lambda_j \operatorname{Re}\big( \tilde\phi_j * (w \odot E_j) \big), \qquad \tilde\phi_j(x) = \overline{\phi_j(-x)}. $$

*Proof.* The sigmoid has $\operatorname{sig}' = a \operatorname{sig}(1 - \operatorname{sig})$, so $\partial F / \partial m(y) = \sum_x 2 (z - z^*)\, a z (1 - z)\, \partial I(x) / \partial m(y) = 2a \sum_x w(x)\, \partial I(x)/\partial m(y)$. Since $E_j(x) = \sum_{y'} \phi_j(x - y') m(y')$ is linear in $m$, $\partial |E_j(x)|^2 / \partial m(y) = 2 \operatorname{Re}\big(\overline{E_j(x)}\, \phi_j(x - y)\big)$ for real $m$. So $\partial F/\partial m(y) = 4a \sum_j \lambda_j \operatorname{Re} \sum_x w(x) E_j(x) \overline{\phi_j(x - y)}$, using $\operatorname{Re} \bar c = \operatorname{Re} c$, and $\sum_x \overline{\phi_j(x - y)}\, (w E_j)(x) = (\tilde\phi_j * (w E_j))(y)$. $\square$

So one gradient costs one convolution per kernel for $E_j$, which line L4 has already done, and one more for $\tilde\phi_j * (w E_j)$. With the [fast Fourier transform](/fast-fourier-transform/) on $n$ pixels this is $O(K n \log n)$ per iteration for $K$ kernels. For one coherent kernel, this is the gradient of Poonawala and Milanfar, whose cost has two convolutions and is $O(n \log n)$. The penalties add $O(n)$: $\nabla R_{\mathrm{dis}} = 4(1 - 2m)$, and $R_{\mathrm{TV}}$ uses the signs of the differences, a subgradient, or a smoothed absolute value. A finite difference check on a random $32$-pixel mask with three kernels agrees with the formula to $10^{-9}$.

**Claim 2 (the problem is not convex).** Allow phase-shifting masks, with $m_k \in [-1, 1]$. If a mask $m \ne 0$ has a lower cost $F$ than the dark mask $0$, then $F$ is not convex.

*Proof.* $E_j$ is linear in $m$, so $I(-m) = I(m)$ and $F(-m) = F(m)$. The midpoint of $m$ and $-m$ is $0$. A convex $F$ would give $F(0) \le \frac12 F(m) + \frac12 F(-m) = F(m)$, which is false. $\square$

Even for binary masks the data term is a quartic polynomial in $m$ before the sigmoid, and Poonawala and Milanfar note that it has many local minima. Gradient methods find a good local minimum, not a certified global one, and the start of line L1 matters.

## Classic examples

**Assist features appear by themselves.** Take one dimension, a period of $8$ in units of $\lambda/\mathrm{NA}$, and $128$ pixels of size $\frac{1}{16}$, with pixel $k$ centered at $x = k/16$. The source has five points evenly spaced on $[-\frac12, \frac12]$, the pupil is ideal, and the eigendecomposition gives five kernels. The target has an isolated line of $6$ pixels, $k = 16, \dots, 21$, so the edges are at $0.969$ and $1.344$, and three dense lines of $6$ pixels at a pitch of $12$ pixels, $k = 70$ to $75$, $82$ to $87$ and $94$ to $99$. So all lines have width $0.375$, and the dense pitch is $0.75$. The threshold is $t_r = 0.25$ of the clear field, $a = 25$, the step is $s = 1$, and no penalties are used. A scratch computation with the code of the [sum of coherent systems](/sum-of-coherent-systems/) page gave these results.

- With the mask equal to the target, $5$ of the $128$ sample points print wrong. The largest edge placement error is $0.056$, at the left edge of the middle dense line.
- After $300$ steps of the template, the gray mask prints with no wrong sample points, and the largest edge placement error falls to $0.006$. The cost falls from $2.44$ to $1.03$.
- The optimized mask has a new peak of transmission up to $0.82$ near $x = 2$, about $0.6$ to the right of the isolated line. No rule asked for it. It is an assist feature: it adds light that makes the isolated line behave more like a dense one, and it is too small to print.
- Rounding the gray mask at $\frac12$ keeps the assist feature but gives $2$ wrong sample points and a largest edge placement error of $0.041$. The gap between the gray and the rounded result is the reason for the discretization penalty.

**Why the cost does not reach zero.** In the same run the cost stays near $1.03$ although every sample prints right. The image is band-limited, so $z$ passes smoothly from $0$ to $1$ near each of the $8$ edges, and the samples next to an edge keep a residual. The pixel cost measures this residual as well as the edge position. Edge placement at control sites, the measure of [optical proximity correction](/optical-proximity-correction/), is the better report of the result.

**Serifs at corners.** Saleh and Sayegh (1981) used image restoration methods to compute the best correction of a mask for a diffraction-limited system with a strongly nonlinear film. For corners, the computed correction is a serif, the same kind of small square that rule-based correction adds at corners.

**From target to start.** Line L1 sets $\theta_k = 0$ on target pixels and $\pi$ elsewhere, the mask equal to the target. These are stationary points of $\theta_k$, since $\sin \theta_k = 0$ there. So the target must be clipped into $(0, 1)$ before the arc cosine, or the iteration cannot move. Poonawala and Milanfar start from $\theta^0 = \cos^{-1}(2 z^* - 1)$.

## Variations

- **Level set ILT.** Represent the mask boundary as the zero set of a function $\psi$ and move it with the [level set method](/level-set-method/), with a speed taken from the gradient of the cost. The mask stays binary at every step, and shapes can split or merge. Shen, Wong and Lam (2009) gave a complete level set formulation and report better results than pixel gradient methods.
- **Phase-shifting masks.** Allow pixel values in $\{-1, 0, 1\}$, or complex values, with penalties that favor the allowed levels. With few coherent kernels, mask design becomes close to [phase retrieval](/phase-retrieval/), which Pati and Kailath used.
- **Process window.** Sum the cost over several focus and dose settings, each with its own kernels, so the mask prints well under process variation. Shen, Jia, Wong and Lam (2011) weighted the level set cost by random process conditions in this way and showed results that take defocus into account.
- **Other solvers.** Box constraints $0 \le m \le 1$ can be kept directly by [projected gradient descent](/projected-gradient-descent/) instead of the cosine transformation. Conjugate gradient and quasi-Newton methods take fewer steps. The gradient of any differentiable resist model follows from [automatic differentiation](/automatic-differentiation/).
- **Source and mask together.** Source-mask optimization also treats the source intensities $J(s)$ as variables. The TCC then changes at every step, so the forward model is often computed by Abbe's method over source points.
- **Regularization.** Besides the discretization and complexity penalties, an aerial image penalty $\|z^* - I(m)\|_2^2$ pushes for high contrast, and quadratic penalties in the spirit of [Tikhonov regularization](/tikhonov-regularization/) smooth the mask.

## Pitfalls

- **Gray masks.** Without the discretization penalty the optimum has values strictly between $0$ and $1$, which a binary mask cannot make. Rounding afterwards can undo much of the gain, as in the example.
- **Manufacturability.** Pixel masks can have tiny islands, jagged edges and curves. Mask rules on the smallest width, space and area must be enforced after line L9, or as penalties, or the mask cannot be written and inspected.
- **Model limits.** ILT optimizes against its model. A thin mask and scalar imaging, the assumptions of the Hopkins model, miss thick-mask and vector effects, so the gain can disappear on the wafer. Truncating the kernels, see the [sum of coherent systems](/sum-of-coherent-systems/), is a further model error.
- **Steep sigmoid.** A large $a$ approaches a true threshold but makes the gradient vanish away from the contour and the cost harder to minimize. Raising $a$ over the iterations is common.
- **Step size.** Too large a step makes the cost oscillate; the same damping issue appears in edge-based correction. A line search on the cost is safer than a fixed step.
- **Local minima.** Different starts give different masks. Compare masks by the printed result over the process window, not by the cost alone.

## Exercises

1. Show that $R_{\mathrm{dis}}(m) = \sum_k (1 - (2 m_k - 1)^2)$, and that it is zero on $[0, 1]^n$ exactly at binary masks. Compute its gradient in $\theta$ under $m = (1 + \cos\theta)/2$.
2. For one coherent kernel $\phi$, write the gradient of Claim 1 in the frequency domain with the [discrete Fourier transform](/discrete-fourier-transform/), and count the transforms per iteration.
3. Show that every binary mask is a stationary point of the cost as a function of $\theta$. Explain why line L1 clips the target.
4. Give a one-dimensional example, with one coherent kernel and a mask allowed values in $[-1, 1]$, where the image is the same for two different masks. Relate it to Claim 2.
5. The level set variant moves the boundary with a speed $v$. Explain why its mask is binary at every step, and what replaces the discretization penalty.

## References
