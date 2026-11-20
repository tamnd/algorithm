---
tag: THXH29
kind: algorithm
slug: variational-network-mri
name: Variational network
aliases:
- variational network for MRI
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: An unrolled gradient scheme for MRI whose regularizer filters and activation functions are learned from pairs of undersampled and full data.
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {T: the number of stages, a: the cost of one call to A plus one call to its adjoint, g: the cost of one call to the learned regularizer of a stage (outside this page), c: the number of coils, n: the number of pixels}
  time: {worst: O(T (a + g))}
  space: {extra: O(c n)}
properties: {deterministic: true, iterative: true, learned: true, exact: false}
history:
  year: 2018
  people: [Kerstin Hammernik, Teresa Klatzer, Erich Kobler, Michael P. Recht, Daniel K. Sodickson, Thomas Pock, Florian Knoll]
  note: Hammernik and coauthors unrolled ten gradient steps on a fields of experts energy, learned the filters, the activation functions and the data weights of each step from clinical knee data, and reconstructed multi-coil accelerated MRI in a fraction of a second per slice.
prereqs: [total-variation-denoising, gradient-descent, sense]
see_also: [algorithm-unrolling, learned-primal-dual, lista, landweber-iteration, compressed-sensing-mri, fista, plug-and-play-priors, bilevel-learning-of-regularizers]
sources:
  - paper: doi:10.1002/mrm.26977
    title: Kerstin Hammernik, Teresa Klatzer, Erich Kobler, Michael P. Recht, Daniel K. Sodickson, Thomas Pock and Florian Knoll, Learning a variational network for reconstruction of accelerated MRI data, Magnetic Resonance in Medicine 79(6), 2018, 3055 to 3071 (arXiv 1704.00447)
    locator: in the arXiv version 1704.00447v1, Eq. 4 to 6 for the energy and the stage update, the Methods section for the filters, the activation functions, the coil maps and the training, and Table 1 for the measured MSE and SSIM against CG SENSE and PI-CS TGV
  - paper: doi:10.1109/TPAMI.2016.2596743
    title: Yunjin Chen and Thomas Pock, Trainable nonlinear reaction diffusion, a flexible framework for fast and effective image restoration, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017
    locator: pages 1256 to 1272 (the gradient steps with learned filters and influence functions per step that the variational network builds on)
  - paper: doi:10.1007/s11263-008-0197-6
    title: Stefan Roth and Michael J. Black, Fields of experts, International Journal of Computer Vision 82(2), 2009
    locator: pages 205 to 229 (the fields of experts prior, a sum of potentials of filter responses)
  - paper: "Jure Zbontar and coauthors, fastMRI, an open dataset and benchmarks for accelerated MRI, arXiv 1811.08839, 2018"
    locator: the knee data set and the baseline measurements (general locator)
---

The variational network (VN) reconstructs an image from undersampled MRI data with a fixed number $T$ of steps, each of which looks like one step of [gradient descent](/gradient-descent/) on a regularized energy. In each step, a learned regularizer applies a set of filters to the image, passes the responses through learned activation functions and filters them back, and a learned weight scales the gradient of the data term. Hammernik et al. (2018) trained the filters, activations and weights of all steps together on pairs of undersampled and fully sampled knee scans. In [compressed sensing MRI](/compressed-sensing-mri/), the regularizer is chosen by hand, such as a wavelet $\ell_1$ norm or [total variation](/total-variation-denoising/), and the iteration runs until it converges. In the VN, the regularizer is learned and the number of steps is fixed, as in other [unrolled algorithms](/algorithm-unrolling/). With a fixed derivative activation, a step is a gradient step on a known energy. For a trained network there is no such energy, and the quality is measured.

## In plain words

Compressed sensing MRI fills in missing k-space data by asking for an image that fits the data and looks "simple", for example one with few edges. The measure of "simple" is chosen by a person, and the solver needs many steps.

The variational network keeps the shape of that solver but runs only about ten steps. In each step, it measures local patterns in the image with a set of small filters. It then pushes the image away from the patterns it was trained to dislike, such as aliasing streaks, and pulls the image back toward the measured data. The filters, the push in each step and the pull strength are learned from scans where the full data are known. After training, a reconstruction is a fast fixed sequence of steps.

## The problem

The input is the undersampled k-space data $f$ of one image with $n$ pixels, from $c$ coils, and the forward operator $A u = (M F (s_j u))_{j=1}^c$ of [SENSE](/sense/), with the unitary 2D DFT $F$, the sampling mask $M$ and the coil maps $s_j$. The other input is a trained network: a list of $T$ stages. Stage $t$ has a regularizer function $r_t$ and a data weight $\mu_t \ge 0$. In the VN, $r_t$ has the form of the gradient of a fields of experts energy (Roth and Black 2009),

$$r_t(u) = \sum_{i=1}^{N_k} (K_i^t)^T \phi_i^{t\prime}(K_i^t u),$$

where $K_i^t$ is a filter that maps the complex image to a real image, $(K u)(p) = \sum_o k^{\text{re}}_o \operatorname{Re} u(p + o) + k^{\text{im}}_o \operatorname{Im} u(p + o)$, and $\phi_i^{t\prime}$ is a learned activation applied pixel by pixel. The output is the image $u_T$. The problem that the network tries to solve is the [MRI reconstruction problem](/mri-reconstruction-problem/): find the image that produced $f$. The network does not minimize a stated objective; it is trained so that $u_T$ is close to the fully sampled image on the training data.

## The algorithm

```pseudo id=main
VARIATIONALNETWORK(f, A, A*, stages (r_1, mu_1), ..., (r_T, mu_T))
L1  u <- A* f                         ▷ the zero filled, coil combined image
L2  for t = 1 to T do
L3      r <- r_t(u)                   ▷ learned: sum_i K_i^T phi_i'(K_i u)
L4      g <- A*(A u - f)              ▷ gradient of (1/2)||A u - f||^2
L5      u <- u - r - mu_t g
L6  return u
```

This is Eq. 6 of Hammernik et al. A step size is not shown, because it is absorbed into the activations and into $\mu_t$. Compare it with one gradient step on $E(u) = \sum_i \sum_p \phi_i((K_i u)(p)) + \frac{\lambda}{2}\|A u - f\|^2$ with the step $\alpha$:

$$u \leftarrow u - \alpha \sum_i K_i^T \phi_i'(K_i u) - \alpha \lambda A^*(A u - f).$$

The two are the same if $r_t$ uses the activations $\alpha \phi_i'$ and $\mu_t = \alpha \lambda$. With no regularizer, the scheme is the [Landweber iteration](/landweber-iteration/). The VN unties the parameters: each stage has its own filters, activations and weight, so it is no longer a gradient method on one energy. The same idea, applied to image denoising, is the trainable reaction diffusion of Chen and Pock (2017).

In the paper, $u_0$ is the zero filled image, the coil maps are computed from the fully sampled k-space center, $T = 10$, and each stage has $N_k = 48$ filters of size $11 \times 11$ on the real and imaginary parts. Each activation is a weighted sum of 31 Gaussian radial basis functions on $[-150, 150]$. The filters have zero mean and unit norm. The network has 131,050 parameters. They were trained on 200 images (20 slices from each of 10 patients) to minimize the mean squared error of smoothed magnitude images, with mini-batches of 10 for 1000 epochs. The training uses [backpropagation](/backpropagation/) through all ten stages.

## Example

This example shows what the gradient step form of a stage does, without training. Take the modified Shepp-Logan phantom on $16 \times 16$ pixels, one coil and the 7 phase encoding rows 0, 1, 8, 9, 13, 14 and 15 of the unshifted k-space (rows 0, 1, 14 and 15 are the lowest frequencies). Use the four forward difference filters on the real and imaginary parts and the smooth absolute value $\phi(z) = \sqrt{z^2 + \varepsilon^2}$ for all of them. Then $E$ is a smoothed total variation energy. Theorem 5 below allows the step $\alpha = 1/(8/\varepsilon + \lambda)$. The table gives the relative error of $u_T$ and the energy $E(u_T)$ (measured with the code below).

| stages | $\varepsilon$ | $\lambda$ | step | relative error | $E(u_T)$ |
|---|---|---|---|---|---|
| 0 (zero filling) | 0.05 | 50 | | 0.6165 | 96.62 |
| 10 | 0.05 | 50 | $\alpha$ | 0.5942 | 84.17 |
| 300 | 0.05 | 50 | $\alpha$ | 0.5086 | 83.02 |
| 10 | 0.05 | 200 | $\alpha$ | 0.5907 | |
| 300 | 0.05 | 200 | $\alpha$ | 0.4476 | |
| 10 | 0.1 | 50 | $\alpha$ | 0.5910 | |
| 300 | 0.1 | 50 | $\alpha$ | 0.5447 | |
| 10 | 0.05 | 50 | $5\alpha$ | 0.7645 | 272 |
| 10 | 0.05 | 50 | $20\alpha$ | diverges | |

With the safe step, the energy goes down at every stage (96.62 to 90.42 after the first one) as Theorem 5 says. But ten safe stages hardly improve on zero filling, because the safe step is small. Larger fixed steps make the energy go up, and twenty times the safe step diverges. A trained VN learns a separate step, filter set and activation for each stage, which lets ten stages do the work of hundreds. The quality of a trained network is not a property of this scheme. Hammernik et al. measured it on clinical knee data.

## Correctness

For a trained network there is no correctness theorem: no energy that decreases, no convergence and no bound on the error. The network outputs whatever the ten stages compute, and its quality is a measurement on test data. What is proved, in full below, is this:

- **A stage is a gradient step.** If the activations of stage $t$ are $\alpha \phi_i'$ for potentials $\phi_i$ and $\mu_t = \alpha\lambda$, the stage is $u - \alpha \nabla E(u)$ for the fields of experts energy $E$ above (Theorem 2). Every activation is the derivative of its integral, so each trained stage is a gradient step on its own energy; but the energy changes from stage to stage.
- **Safe steps decrease the energy.** For the forward difference filters, $\|\sum_i K_i^T K_i\| \le 8$. With $\phi(z) = \sqrt{z^2 + \varepsilon^2}$ and $\|A\| \le 1$, the gradient of $E$ is Lipschitz with the constant $8/\varepsilon + \lambda$, and for $\alpha \le 1/(8/\varepsilon + \lambda)$ every stage lowers $E$ by at least $\|u_{t+1} - u_t\|^2 / (2\alpha)$ (Theorem 5).
- **Landweber.** With $r_t = 0$, the scheme is the Landweber iteration. With one coil, $u_0 = A^* f$ already fits the data, so the data term alone never changes the zero filled image.

Hammernik et al. report that the trained VN has a lower MSE and a higher SSIM than CG SENSE and a combined parallel imaging and compressed sensing reconstruction with total generalized variation (PI-CS TGV), on all tested knee sequences, for $R = 3$ and $R = 4$ with regular and variable density random sampling. These are measurements on their data. Larger benchmarks, such as fastMRI (Zbontar et al. 2018), are also measurements.

## Complexity

The model is real-ram. Line L1 calls $A^*$ once. Each of the $T$ stages calls the regularizer $r_t$ once, $A$ once and $A^*$ once. So the time is $O(T(a + g))$, where $a$ is the cost of one call to $A$ and one to $A^*$, and $g$ is the cost of one regularizer. For $c$ coils with the FFT, $a = O(c\, n \log n)$. The cost of the regularizer depends on the network and is outside this page. For $N_k$ filters of size $s \times s$ applied directly, and activations made of $N_w$ basis functions, it is $O(N_k (s^2 + N_w) n)$. The extra space is $O(c\, n)$ for the residual in k-space. Training needs the gradient through all $T$ stages, which costs a constant times the forward pass and stores all $T$ intermediate images. Hammernik et al. report 193 ms per slice on one GPU (measurement).

## Properties

- **Fixed cost.** The number of stages is fixed, so the run time does not depend on the data or on a stopping rule.
- **Data consistency in every stage.** Each stage uses the true operator $A$ with the coil maps, so the network knows the acquisition and does not learn it.
- **Interpretable stages.** The filters and activations of each stage can be plotted, and with derivative activations a stage is a gradient step.
- **Deterministic.** For given weights, the output is a fixed function of the data.
- **Not monotone.** A trained network need not lower any energy from one stage to the next.

## Variants and improvements

- **Trainable reaction diffusion.** Chen and Pock (2017) used the same stage form for denoising, with learned filters and influence functions in each step. The VN adds the MRI forward operator and complex images.
- **Other unrolled schemes.** [Learned primal-dual](/learned-primal-dual/) unrolls a primal-dual method with small networks in place of the proximal steps. [LISTA](/lista/) unrolls ISTA for sparse coding. Later networks for MRI replace the fields of experts regularizer by a general convolutional network and keep the data consistency step. These are described on the [algorithm unrolling](/algorithm-unrolling/) page.
- **Plug and play.** [Plug-and-play priors](/plug-and-play-priors/) put a trained denoiser inside a fixed iteration that runs until it converges, and do not train the steps end to end.
- **Learned energies.** [Bilevel learning of regularizers](/bilevel-learning-of-regularizers/) learns the parameters of one energy that is then minimized to convergence. Then the theorems for gradient methods, such as those of [FISTA](/fista/), apply again.

## When to use it

Use a VN when many scans of the same kind (protocol, anatomy and sampling pattern) are available with fully sampled references, and the reconstruction must be fast. It suits clinical protocols where the same sequence runs many times. When there are no training data, or the scan type differs from the training data, use a hand-made regularizer, such as [compressed sensing MRI](/compressed-sensing-mri/) or [low rank plus sparse MRI](/low-rank-plus-sparse-mri/) for dynamic data.

## Pitfalls

- **Change of distribution.** A network trained on one contrast, field strength, coil array or sampling pattern can fail on another, and the failure may look like a plausible image.
- **Hallucinated detail.** The learned regularizer can add structures that are not in the data, or remove small lesions. Check results against the data residual and against a classical reconstruction.
- **Coil maps.** Errors in the coil maps enter every stage through $A$. In the paper, they come from the fully sampled k-space center.
- **No convergence.** Running more stages than were trained does not converge to anything and usually makes the image worse.
- **Fixed step sizes.** As the example shows, a gradient step that is too large makes the energy go up, and even larger steps diverge. Training learns steps that work for its data, without a guarantee.
- **Quality metrics.** MSE and SSIM of magnitude images do not measure diagnostic value. A lower error on a test set does not show that the images are safe to read.

## Implementations

The network is a given input: the code takes the stages $(r_t, \mu_t)$ as functions and numbers, and the operators $A$ and $A^*$ as functions, and runs lines L1 to L6 around them. It does not train a network, and no weights are downloaded. The tests build the stages by hand from the forward difference filters and the activation $\alpha \phi'$ of $\phi(z) = \sqrt{z^2 + \varepsilon^2}$, or as simple fixed maps. The tests check the adjoint of $A$ with and without coils, the adjoint of a random complex-to-real filter, the bound 8 for the forward difference filters, that one stage equals the gradient step on the known energy (with central differences), the energy decrease of Theorem 5 at every stage, the call counts ($T$ regularizer calls, $T$ calls to $A$, $T + 1$ calls to $A^*$), and the Landweber case.

## History

Roth and Black introduced the fields of experts prior in 2005, with a journal version in 2009: an image energy that is a sum of potentials of the responses of learned filters. Chen and Pock (2015 on arXiv, 2017 in print) unrolled a few gradient steps on such energies, learned the filters and the influence functions of each step separately, and obtained fast and accurate denoising. Hammernik, Klatzer, Kobler, Recht, Sodickson, Pock and Knoll put the MRI forward operator into these steps and trained the result on clinical knee data, first shown at ISMRM 2016 and published in 2018. The fastMRI data set of Zbontar et al. (2018) then gave a common benchmark, and many later unrolled networks for MRI follow the same pattern of learned regularizer steps and data consistency steps.

## References
