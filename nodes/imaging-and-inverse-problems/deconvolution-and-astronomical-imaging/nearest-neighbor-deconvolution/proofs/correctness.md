---
title: Nearest neighbor deconvolution is the first-order Neumann approximation of the inverse, exact up to second-order terms, and it cannot restore the axial position of the mean intensity
proves: [correctness]
status: full
---

**Setting.** A stack has planes $j = 0, \dots, n_z - 1$, each an image with a periodic border. The imaging model is

$$y_j = \sum_k h_{j-k} \ast x_k,$$

with $\ast$ the periodic 2D convolution and $h_d$ the PSF of a source $d$ planes away; planes outside the stack are empty. Write the blur as $\mathcal A = \mathcal A_0 + \mathcal E + \mathcal R$, where $(\mathcal A_0 x)_j = h_0 \ast x_j$, $(\mathcal E x)_j = h_{+1} \ast x_{j-1} + h_{-1} \ast x_{j+1}$ (terms outside the stack are $0$), and $\mathcal R$ holds the offsets $|d| \ge 2$. Lines L1 to L5 compute

$$\hat x = (\mathcal I - c\,\mathcal E)\, y.$$

Line L6 applies a linear filter $\mathcal W$ plane by plane, and line L7 clips.

**Claim 1 (linearity).** Without line L7, $y \mapsto \hat x$ is linear.

*Proof.* Lines L3 to L5 are convolutions and linear combinations of the planes of $y$, and $\mathcal W$ is linear. $\square$

**Claim 2 (exact error formula).** For every stack $x$ and $y = \mathcal A x$,

$$\hat x = (\mathcal I - c\mathcal E)(\mathcal A_0 + \mathcal E + \mathcal R)\, x.$$

In the ideal case $h_0 = \delta$ and $\mathcal R = 0$ this is

$$\hat x = x + (1 - c)\,\mathcal E x - c\,\mathcal E^2 x,$$

and for $c = 1$, $\hat x - x = -\mathcal E^2 x$.

*Proof.* Substitute $y = \mathcal A x$ into $\hat x = (\mathcal I - c\mathcal E)y$ and expand $(\mathcal I - c\mathcal E)(\mathcal I + \mathcal E) = \mathcal I + (1 - c)\mathcal E - c\,\mathcal E^2$. $\square$

The test checks the second formula in exact rational arithmetic.

**Claim 3 (first-order Neumann approximation).** In the ideal case, if $\|\mathcal E\| < 1$ in some operator norm, then $\mathcal A = \mathcal I + \mathcal E$ is invertible, $\mathcal A^{-1} = \sum_{k \ge 0} (-\mathcal E)^k$, and the method with $c = 1$ is this series cut after the linear term. Its error satisfies $\|\hat x - x\| \le \|\mathcal E\|^2 \|x\|$.

*Proof.* The Neumann series converges for $\|\mathcal E\| < 1$, and $(\mathcal I + \mathcal E)\sum_{k<K} (-\mathcal E)^k = \mathcal I - (-\mathcal E)^K$ tends to $\mathcal I$. The first two terms are $\mathcal I - \mathcal E$. The bound follows from Claim 2 and $\|\mathcal E^2\| \le \|\mathcal E\|^2$. $\square$

For $c \ne 1$ the error has the first-order term $(1 - c)\mathcal E x$, and a value $c < 1$ trades this term against the second-order term $c\,\mathcal E^2 x$.

**Claim 4 (the mean intensity).** Suppose every $h_d$ is nonnegative with $\sum h_{\pm 1} = 1$ (the defocused PSF of a widefield microscope keeps the energy of the source). If $y$ is a constant $v$ on every plane, then $\hat x_j = (1 - 2c)\,v$ on every interior plane $0 < j < n_z - 1$, and $\hat x_j = (1 - c)\,v$ on the two end planes (before L6 and L7).

*Proof.* The convolution of a constant image with a kernel of sum $1$ is the same constant. An interior plane has two neighbors, an end plane one. $\square$

In Fourier terms, at lateral frequency $0$ the operator $\mathcal E$ multiplies by the neighbor sums of the plane values, with weight $1$ on each side, so its norm there is close to $2$ for a long stack and Claim 3 does not apply. The method subtracts a fixed fraction of the neighbors and does not find which plane the light came from. At high lateral frequencies the defocused OTFs are small, $\|\mathcal E\|$ is small there, and Claim 3 makes the method accurate. So nearest neighbor deconvolution removes the fine detail of out-of-focus planes and leaves a scaled mean.

**Claim 5 (no positivity).** $\hat x$ can be negative for a nonnegative $y$.

*Proof.* Take $c = 1/2$, one interior plane $j$ of zeros and both neighbors constant $1$. Then $\hat x_j = 0 - \tfrac12 (1 + 1) = -1$. $\square$

This is why line L7 clips; with clipping the method is no longer linear. $\blacksquare$
