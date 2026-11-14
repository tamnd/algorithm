---
tag: QG61TM
kind: technique
slug: optical-proximity-correction
name: Optical proximity correction
aliases:
- OPC
- model-based OPC
area: cad/timing-and-verification
level: advanced
summary: Distorts mask shapes with biases, serifs and assist features so the pattern printed by diffraction-limited lithography matches the intended layout.
prereqs: [convolution, fast-fourier-transform]
see_also: [singular-value-decomposition, gradient-descent, level-set-method, image-deblurring, tikhonov-regularization, multiple-patterning-decomposition, design-rule-checking]
sources:
  - paper: doi:10.1098/rspa.1953.0071
    title: H. H. Hopkins, On the diffraction theory of optical images, Proceedings of the Royal Society of London A 217(1130), 408 to 432, 1953
    locator: the theory of partially coherent imaging and the transmission cross coefficient, the image model on which model-based OPC rests
  - paper: "Nicolas Bailey Cobb, Fast Optical and Process Proximity Correction Algorithms for Integrated Circuit Manufacturing, PhD thesis, Department of Electrical Engineering and Computer Sciences, University of California at Berkeley, 1998"
    locator: the sum of coherent systems decomposition of the Hopkins image into a few convolution kernels, the edge fragments with control sites, and the iterative correction of the edges by the edge placement error
  - paper: "Amyn Poonawala and Peyman Milanfar, Mask design for optical microlithography, an inverse imaging problem, IEEE Transactions on Image Processing 16(3), 774 to 788, 2007"
    locator: inverse lithography as the optimization of a pixel mask by gradient steps on a smooth model of imaging and resist, with regularization terms
---

Optical proximity correction, or OPC, changes the shapes on a photomask so that the shapes printed on the wafer match the layout. A lithography system is a low-pass filter: it blurs the mask, and the resist turns the blurred image into a pattern by a threshold. Features near the resolution limit then print too narrow, too wide, with round corners and short line ends, and the error of each feature depends on its neighbors, which is the *proximity effect*. OPC moves the edges of the mask shapes, adds serifs and hammerheads, and adds sub-resolution assist features, so that the printed edges land on the target edges. It is a lithography and design-for-manufacturing technique. It is placed in timing-and-verification because it runs after [design rule checking](/design-rule-checking/) and after [multiple patterning decomposition](/multiple-patterning-decomposition/) in the flow from layout to mask. Its core is a feedback loop around a model of the imaging, given below.

## In plain words

Light that goes through a very small hole on the mask spreads out, so the picture on the wafer is blurry. Where the blur is bright enough, the resist prints. A wide line prints close to its true size. A thin line prints thinner than drawn, because its center gets less light. A line with neighbors gets some of their light as well, so it prints differently from the same line alone.

OPC fixes this by drawing the mask "wrong" on purpose. It simulates the picture, measures how far each printed edge is from where it should be, and moves that piece of the mask edge to make up for it. It repeats these steps until all the edges are close enough.

## When it applies

- The features are near or below the wavelength of the light, so the image of a shape depends on its size and on the shapes around it.
- A model of the imaging and the resist exists and has been calibrated on test patterns printed with the same process. The correction is only as good as this model.
- The target is a set of polygons whose edges can be cut into fragments that move one by one. Mask rules limit the result: the mask writer has a minimum feature size, a minimum space and a minimum jog.
- The cost is acceptable: a full chip has billions of fragments, and each iteration needs a simulation of the image over the whole chip.

## The template

```pseudo id=main
MODEL-BASED-OPC(target polygons T, image model, threshold θ, damping α, tolerance τ, iterations K)
L1  M ← T; cut each edge of M into fragments, each with a control site
L2  for k ← 1 to K do
L3      compute the image I of the mask M with the model
L4      for each fragment f: EPE(f) ← the signed distance, along the outer normal at the site of f, from the target edge to the contour I = θ
L5      if |EPE(f)| ≤ τ for every fragment then return M
L6      for each fragment f: move f along its outer normal by −α · EPE(f)
L7      repair M where it breaks a mask rule (width, space, jog)
L8  return M and the remaining EPE values
```

The holes are the image model in line L3, the cutting of the edges into fragments in line L1, the step $\alpha$ in line L6, and the mask rules in line L7. EPE is the *edge placement error*: positive when the printed edge lies outside the target, so line L6 pulls the mask edge in.

**The image model.** In the model of Hopkins (1953) for partially coherent light, the image is a quadratic form in the mask transmission $m$, with a kernel called the transmission cross coefficient. This kernel is Hermitian and positive semidefinite, so its eigendecomposition, which is its [singular value decomposition](/singular-value-decomposition/), gives the *sum of coherent systems* form that Cobb (1998) used:
$$I(x) \approx \sum_{j=1}^{J} \lambda_j \,\bigl| (\phi_j * m)(x) \bigr|^2 ,$$
with a few kernels $\phi_j$ and weights $\lambda_j \ge 0$. Each term is a [convolution](/convolution/), computed with the [fast Fourier transform](/fast-fourier-transform/) on a grid, or by table lookups of the kernels on the edges of the polygons. A resist model, often a threshold with corrections, turns $I$ into the printed contour.

**Why the step must be damped.** Take one fragment and let $P(w)$ be the printed position as a function of the mask position. Near the solution $w^*$ with $P(w^*) = t$, line L6 maps the error $e = w - w^*$ to about $(1 - \alpha m) e$, where $m = P'(w^*)$ is the *mask error enhancement factor*, MEEF. So the loop converges near $w^*$ if $0 < \alpha < 2 / m$, and it diverges when $\alpha > 2 / m$. For one fragment this is proved by the mean value theorem. For many fragments the factor $m$ becomes a matrix of the effects of each fragment on each site, and convergence of the loop is checked by experiment, not proved.

**Example.** Use a 1D model: an opening of width $w$ centered at $c$ gives the image $\Phi((x - c + w/2)/\sigma) - \Phi((x - c - w/2)/\sigma)$, where $\Phi$ is the standard normal distribution function, so the blur is a Gaussian with $\sigma = 40$. The images of the openings add, the threshold is $\theta = 0.5$, and the target width is $60$. A scratch script computed all the numbers below by bisection on the contour.

- A very wide opening prints at its true size, because the image of a single edge is $\Phi(x/\sigma)$, which is $0.5$ at the edge.
- With the mask equal to the target, a width of $60$ prints $60$ at pitch $120$ (equal lines and spaces, which print to size by symmetry), $42.58$ at pitch $140$, and $37.20$ when isolated, where the center gets only $0.547$. This is the proximity effect: one mask width, three printed widths.
- Each fragment is one edge, so a step moves both edges and the width changes by $-2 \alpha \cdot \mathrm{EPE}$.

With $\alpha = 1$, the isolated line gives the mask widths $60, 82.8, 64.4, 76.0, 67.0, 73.2, \dots$, which swing about the answer and close in slowly. For lines at pitch $140$, it gives $60, 77.4, 47.9, 107.9, 27.9, 87.9, \dots$: at $47.9$ the lines do not print at all, at $107.9$ they merge into one, and the loop never settles. The MEEF at the solution is $1.73$ for the isolated line and $2.61$ for the dense lines, so $\alpha = 1$ is below $2/m$ only in the first case.

With $\alpha = 0.5$:

| iteration | isolated mask | isolated EPE | dense mask | dense EPE |
| --- | --- | --- | --- | --- |
| 0 | 60.00 | $-11.40$ | 60.00 | $-8.71$ |
| 1 | 71.40 | $0.87$ | 68.71 | $3.37$ |
| 2 | 70.53 | $0.13$ | 65.33 | $-0.96$ |
| 3 | 70.39 | $0.02$ | 66.30 | $0.30$ |
| 4 | 70.38 | $0.00$ | 66.00 | $-0.09$ |
| 7 | 70.37 | $0.00$ | 66.07 | $0.00$ |

Both converge, the dense one with a sign change at each step, since $1 - 0.5 \cdot 2.61 < 0$. The final masks differ: $70.37$ for the isolated line and $66.07$ for the dense lines, for the same printed width $60$. A rule-based table would have to store exactly these biases for each pitch.

## Classic examples

- **Rule-based OPC.** Tables, indexed by the width of a feature and the space to its neighbor, give the bias of each edge, and fixed shapes are added: serifs at outer corners, cut-outs at inner corners, and hammerheads at line ends. It is fast, but it covers only the cases in the tables.
- **Model-based OPC with sum of coherent systems kernels.** The loop of the template, with the image from a few kernels by [convolution](/convolution/) and the [fast Fourier transform](/fast-fourier-transform/), and the kernels from the eigendecomposition of the Hopkins kernel by the [singular value decomposition](/singular-value-decomposition/). This is the form that full-chip OPC tools take.
- **Inverse lithography.** Treat the mask as a grid of pixels and minimize the difference between the printed pattern and the target by [gradient descent](/gradient-descent/) on a smooth model of the resist (Poonawala and Milanfar 2007), with penalty terms in the spirit of [Tikhonov regularization](/tikhonov-regularization/) that push the pixels to 0 or 1 and the shapes to simple forms. The [level set method](/level-set-method/) is another way to move the mask boundary. It finds masks with curved shapes and assist features of its own.
- **Image deblurring.** OPC looks like [image deblurring](/image-deblurring/), since both undo a blur. They differ in the goal: deblurring estimates an unknown image from a measured blurred one, while OPC designs an input whose blurred image, after a threshold, has a given shape, and the input must be a mask that can be made.
- **Assist features.** Thin bars next to an isolated line, too narrow to print, make the light around it look like that around a dense line, so that one bias works for both.

## Variations

- **Process window OPC.** Simulate at several focus and dose values and minimize the worst EPE, or a weighted sum, not only the error at the nominal values.
- **Process and etch effects.** Add models of the resist, of etch and of the mask writer to the image model, so that the loop corrects the final pattern and not only the light.
- **Hierarchical OPC.** Correct a cell once and reuse the result where the surroundings of the cell are the same within the optical range.
- **Retargeting.** Change the target itself before OPC, for example widen lines that are too thin to print well, within the design rules.
- **Verification after OPC.** Simulate the corrected mask over the whole chip and report the places where EPE, pinching or bridging is still too large, a check like [design rule checking](/design-rule-checking/) on the predicted wafer image.

## Pitfalls

- **Undamped steps.** A full step oscillates or diverges where the MEEF is above $2$, as the dense lines of the example show. Tools use damping, or a step that comes from the estimated sensitivity matrix.
- **Coarse or fine fragments.** Long fragments cannot follow the image near corners and line ends. Very short ones make the mask hard to write and the loop slow.
- **Mask rule breaks.** Edges that move freely can come too close, or form tiny jogs. Line L7 must repair them, and the repair can undo some of the correction.
- **Trust in the model.** The result is right only where the calibrated model is right. Patterns far from the calibration set can print badly while the model says that they are fine.
- **Printing assist features.** An assist bar that is too wide, or that falls where the light of neighbors adds up, prints on the wafer.
- **Corners.** A low-pass system cannot print a sharp corner. Serifs reduce the rounding but cannot remove it, so the tolerance near corners must be looser.
- **Run time.** One model evaluation over a full chip is a large computation, and the loop needs several. The kernels, the grid and the number of iterations are a trade-off between accuracy and time that is measured, not proved.

## Exercises

1. In the 1D model, show that for equal lines and spaces of width $w$ at pitch $2w$ the image is exactly $0.5$ at each edge. Hint: the image of the spaces is $1 - I$, and it is $I$ shifted by $w$.
2. Find the printed width of an isolated opening of width $60$ with $\sigma = 40$ and $\theta = 0.5$ by bisection, and check that it is about $37.2$.
3. For the one-fragment loop $w \leftarrow w - \alpha (P(w) - t)$ with $P'(w^*) = m > 0$, show that the error near $w^*$ is multiplied by about $1 - \alpha m$ at each step. For $m = 2.61$, which of $\alpha = 1$ and $\alpha = 0.5$ converges, and does the error change sign?
4. Show that the sum of coherent systems form with $J$ kernels needs $J$ products in the frequency domain and $J$ inverse fast Fourier transforms per image, for a mask on an $n \times n$ grid, and give the total cost.
5. Explain why the isolated line of the example needs a larger mask bias than the dense lines, in terms of the light that the neighbors add.

## References
