---
tag: E31RHQ
kind: technique
slug: deep-image-prior
name: Deep image prior
aliases:
- DIP
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: "Fit an untrained convolutional network with random input to the measured data and stop early, using the network structure itself as the prior."
prereqs: [gradient-descent, backpropagation, semi-convergence]
see_also: [landweber-iteration, early-stopping, compressed-sensing-generative-models, image-denoising, image-inpainting, super-resolution, adam, regularization-by-denoising]
sources:
  - paper: doi:10.1109/CVPR.2018.00984
    title: "Dmitry Ulyanov, Andrea Vedaldi and Victor Lempitsky, Deep image prior, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2018"
    locator: "pages 9446 to 9454 (the method, the observation that the network fits natural images faster than noise, and the denoising, super-resolution and inpainting experiments)"
  - paper: doi:10.1007/s11263-020-01303-4
    title: "Dmitry Ulyanov, Andrea Vedaldi and Victor Lempitsky, Deep image prior, International Journal of Computer Vision 128(7), 2020"
    locator: pages 1867 to 1888 (the journal version of the method and experiments)
---

The deep image prior (DIP) reconstructs an image from data $y = Ax + e$ without any training data. Take a convolutional generator $G_\theta$ with weights $\theta$, fix a random input $z$, and run a gradient method on

$$\min_\theta\ \|AG_\theta(z) - y\|^2,$$

starting from random weights. Stop after a chosen number of steps $K$ and return $\hat x = G_{\theta_K}(z)$. Ulyanov, Vedaldi and Lempitsky (2018) observed that such a network fits the structure of a natural image in fewer steps than it fits noise. So the iterates first become a plausible image and only later fit the noise in $y$. The prior is the network architecture together with the stopping step; there is no explicit regularizer.

## In plain words

Take a network that turns a fixed random pattern into an image, and that has never seen an image. Adjust its weights, step by step, so that the image it makes, when blurred or masked in the same way as the measurement, matches the measurement. Such a network finds it easy to make smooth regions and edges, and hard to make random speckle. So it makes the clean parts of the picture first. If you stop at the right time, you have the picture without most of the noise. If you go on, the network learns the noise too.

## When it applies

**Setting.** A forward map $A$ with its adjoint, data $y$, a generator $G_\theta(z)$ that is differentiable in $\theta$, and a fixed input $z$. The cost of one step is one call to $G$, one backpropagation through $G$, one call to $A$ and one to $A^T$.

**Fact 1 (a linear generator is Landweber).** Let $G_W(z) = Wz$ with a weight matrix $W$. The gradient of $\|AWz - y\|^2$ in $W$ is $2A^T(AWz - y)z^T$. A gradient step with step $\eta$ changes the image $x = Wz$ to

$$x_{k+1} = x_k - 2\eta\|z\|^2A^T(Ax_k - y),$$

which is the Landweber iteration with step $\omega = 2\eta\|z\|^2$. This is a theorem, and it shows the mechanism in its simplest form: with $W_0 = 0$ the iterates stay in the range of $A^T$, and the number of steps acts as the regularization parameter, with [semi-convergence](/semi-convergence/) when $y$ is noisy.

**Fact 2 (the network bias).** For convolutional networks of the kind used by Ulyanov et al., fitting a natural image takes fewer steps than fitting noise or a scrambled image. This is a measurement on their images. Later analyses prove a version of it for simple models, such as a two-layer convolutional generator in a regime where it behaves like a linear model, but there is no theorem for the networks used in practice. Treat the choice of $K$ as a heuristic.

Use DIP when there is no training data for the task, when the forward map changes from case to case, or as a baseline that needs only $A$ and $A^T$. Do not use it when a trained method is available and fast reconstruction matters: each image needs thousands of network steps.

## The template

```pseudo id=main
DIP(A, y, G, z, θ_0, η, K)
L1  θ ← θ_0
L2  for k = 1 to K                              ▷ hole: the stopping step K
L3      x ← G_θ(z)                              ▷ hole: the generator, a given function
L4      r ← A x - y
L5      g ← ∇_θ ⟨2 A^T r, G_θ(z)⟩               ▷ one backpropagation through G
L6      θ ← θ - η g                             ▷ hole: the optimizer
L7  return G_θ(z)
```

The holes are the generator and its input, the initial weights, the optimizer and the stopping step. Ulyanov et al. use an encoder-decoder network with skip connections, a uniform random input, and the Adam optimizer; plain gradient steps are the simplest case and the one shown. They fix $K$ for each task by hand. They also add small fresh noise to the input at each step in some tasks, as a further regularizer.

The generator is a given function: the code takes $G$ and its vector-Jacobian product as arguments and runs lines L1 to L7 around them. The tests build $G$ by hand as one linear layer, $G_W(z) = \phi(Wz)$ with $\phi = \tanh$ or the identity and seeded weights, and write its gradient by hand; no convolutional network is trained. They check the gradient against finite differences, Fact 1 step by step on a periodic blur, the check value below, and the semi-convergence example below, and that the loss goes down for the $\tanh$ generator.

## Classic examples

**Check value.** One pixel, $A = 1$, $y = 1$, $z = 1$, $W_0 = 0$ and $\eta = 0.005$. By Fact 1, this is Landweber with $\omega = 0.01$, so $x_k = 1 - 0.99^k$ and $x_{100} = 0.63397$.

**Semi-convergence on a blur.** Take $n = 16$ pixels, the periodic blur with kernel $(0.2, 0.6, 0.2)$, the true signal $x_i = \sin(2\pi i/16) + \tfrac12\cos(4\pi i/16)$ with $\|x\| = \sqrt{10} \approx 3.16$, and Gaussian noise with standard deviation 0.1 from seed 3. Use the linear generator with $z = 1$, $W_0 = 0$ and $\eta = 0.05$, so $\omega = 0.1$. The error $\|x_k - x\|$ is 2.87 after 1 step, 1.20 after 10, 0.48 after 20, smallest at step 32 with 0.316, and then grows again: 0.38 after 50, 0.55 after 100, 0.72 after 200 and 0.87 after 500 steps, when the data misfit is below $10^{-3}$. The late iterates fit the noise. This is a measurement for one seed; seeds 4 and 5 also give the smallest error near step 32 to 35. With a real network, the same shape of curve is what Ulyanov et al. report, but the best step is not known without the true image.

**Image tasks.** Ulyanov et al. apply DIP to denoising, super-resolution, inpainting with large holes, and other restoration tasks, and report results close to those of trained methods on some of them. These are measurements on their test images.

## Variations

- **Extra regularizers.** Add a total variation term or another explicit penalty to the loss, which makes the result less sensitive to the stopping step.
- **Smaller networks.** Decoders with fewer weights than pixels, such as the deep decoder of Heckel and Hand, cannot fit all of the noise, so they need less care with stopping.
- **Bayesian DIP.** Add noise to the weight updates, as in [Langevin dynamics](/langevin-dynamics/), and average the images over the run to get an estimate and an uncertainty.
- **Pretrained start.** Start from weights trained on related images, which reduces the number of steps.
- **Related generative methods.** [CSGM](/compressed-sensing-generative-models/) uses a trained generator and optimizes the input $z$; DIP uses an untrained generator and optimizes the weights.

## Pitfalls

- **Stopping.** The result depends strongly on $K$, and the best $K$ depends on the image, the noise level and the network. Without a rule, the late iterates fit the noise, as in the example.
- **Cost.** Each reconstruction is a full network optimization, many times the cost of a trained method at test time.
- **Randomness.** The result depends on the random input and initial weights. Two runs can give different images, and the method gives no measure of this unless you run it several times.
- **No guarantee.** Fact 1 is the only exact statement, and it is for a linear generator. For real networks, the claim that the network prefers natural images is an observation about the architecture, not a property of the data.

## Exercises

1. Prove Fact 1. What happens if $W_0 \neq 0$?
2. Verify the check value $x_{100} = 0.63397$.
3. For the blur in the example, find the eigenvalues of $A^TA$ and write the Landweber iterate in the Fourier basis. Explain why the error first goes down and then up.
4. For the generator $G_W(z) = \tanh(Wz)$, write the gradient of $\|AG_W(z) - y\|^2$ in $W$, and check it by finite differences.
5. Run the example with noise of standard deviation 0.05 and 0.2. How does the best stopping step change?

## References
