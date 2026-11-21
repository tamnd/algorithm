---
tag: 2FTZ83
kind: concept
slug: inverse-problem
name: Inverse problem
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: intro
summary: Recover hidden causes, such as an image or a model, from indirect and noisy measurements of their effects through a known forward model y = A x + e.
model: real-ram
prereqs: [least-squares-problem]
see_also: [forward-operator, well-posed-problem, fredholm-integral-equation-first-kind, regularization-method, tikhonov-regularization, bayesian-inverse-problem, tomographic-reconstruction-problem, image-deblurring]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: "Chapter 1, Introduction: Examples of Inverse Problems"
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 1, Introduction and Motivation, and Chapter 2, Meet the Fredholm Integral Equation of the First Kind
  - book: "Albert Tarantola, Inverse Problem Theory and Methods for Model Parameter Estimation, SIAM, 2005"
    locator: Chapter 1, The General Discrete Inverse Problem
  - paper: doi:10.1145/321105.321114
    title: David L. Phillips, A technique for the numerical solution of certain integral equations of the first kind, Journal of the ACM 9(1), 1962, 84 to 97
    locator: the first-kind integral equation whose plain discretization gives a useless solution, and the smoothing that repairs it
---

An inverse problem asks for the cause $x$ of measured data $y$, when a known forward model maps each cause to its data: given $y = A x + e$ with a known operator $A$ and an unknown noise $e$, find $x$. The direct (forward) problem computes $A x$ from $x$; the inverse problem goes the other way. In most problems of interest the forward map smooths, so it loses the fine detail of $x$, and a direct inversion amplifies the noise without bound. This page is about the task as a whole. The map $A$ itself is the [forward operator](/forward-operator/), the test of whether the task is stable is [well-posedness](/well-posed-problem/), and the main continuous example is the [Fredholm integral equation of the first kind](/fredholm-integral-equation-first-kind/).

## In plain words

You see the effect and you want the cause. A blurred photo is the effect of a sharp scene and a shaking camera. A CT scan measures how much X-ray light the body absorbs along many lines, and you want the body inside. Going from the cause to the effect is easy: you only simulate the physics. Going back is hard for two reasons. First, the physics often blurs or averages, so different causes give almost the same effect. Second, every measurement has noise. When you undo the blur, you also undo it on the noise, and the small noise becomes large errors. So you cannot simply invert. You must add some extra knowledge about the cause, for example that it is smooth or small, and accept an answer that is close to the truth instead of exact.

## The idea

**The setting.** The forward model is $y = A x + e$. Here $A: X \to Y$ is a bounded linear operator between Hilbert spaces, $x \in X$ is the unknown, $y \in Y$ is the data, and $e$ is the noise. In the continuous setting $X = L^2(\Omega)$ and $A$ is often an integral operator. In the discrete setting $X = \mathbb{R}^n$, $Y = \mathbb{R}^m$ and $A$ is an $m \times n$ matrix. Two noise models are common. In the deterministic model only a bound is known, $\|e\| \le \delta$, and the noisy data are written $y^\delta$. In the statistical model $e$ is a random vector with a known law, for example white noise with $E\|e\|^2 = m \sigma^2$.

**Three questions.** For each inverse problem, ask:

1. Does a solution exist for the data that you have? Noisy data are usually not in the range of $A$.
2. Is it unique? If $A$ has a null space, data cannot see the part of $x$ in it.
3. Is it stable? A small change of $y$ must give a small change of $x$.

Hadamard called a problem well posed if all three answers are yes. The usual way to repair the first two is the minimum norm least squares solution $x^\dagger = A^\dagger y$ (see [pseudoinverse](/pseudoinverse/)). The third question is the hard one, and it is the reason for this whole sub-area.

**Why stability fails.** Take the integration operator $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$. Its inverse is differentiation. Its singular values are $\sigma_k = 2/((2k-1)\pi)$, with left singular functions $u_k(s) = \sqrt2 \sin((k - \tfrac12)\pi s)$ (see [singular value expansion](/singular-value-expansion/)). Add the noise $e = \delta\, u_k$ to exact data. Its norm is $\delta$, but it changes the solution by $A^\dagger e = (\delta/\sigma_k) v_k$, whose norm is $\delta (k - \tfrac12)\pi$. With $\delta = 10^{-3}$ and $k = 1000$, a data error of $0.001$ gives a solution error of $3.140$. Since $k$ can be any integer, no bound of the form $\|x - x'\| \le C \|y - y'\|$ holds. This is the typical case: a compact operator with an infinite-dimensional range has an unbounded pseudoinverse.

**Discretization does not remove the problem.** A matrix has a bounded inverse, so a discretized problem is well posed in the strict sense. But its condition number grows with the grid size. The rectangle-rule matrix of the integration operator ($h = 1/n$ on and below the diagonal) has condition number $10.65$ for $n = 8$, $20.92$ for $n = 16$, $41.34$ for $n = 32$ and $82.1$ for $n = 64$. Finer grids resolve more singular values of the operator, and so they also inherit more of its instability. Hansen calls such a system a discrete ill-posed problem: the matrix is ill conditioned and its singular values decay with no clear gap.

**Two ways to add knowledge.** A [regularization method](/regularization-method/) replaces $A^\dagger$ by a family of bounded operators $R_\alpha$ and a rule that chooses $\alpha$ from the noise level. [Tikhonov regularization](/tikhonov-regularization/) and the [truncated SVD](/truncated-svd/) are the basic examples. The statistical way puts a prior law on $x$ and computes the posterior law given $y$; see [linear Gaussian inverse problem](/linear-gaussian-inverse-problem/) and [Bayesian inverse problem](/bayesian-inverse-problem/). In both ways the answer depends on an assumption that the data alone cannot check.

**Linear and nonlinear.** Many imaging problems are linear in $x$: deblurring, CT and MRI with known coils. Others are nonlinear: [phase retrieval](/phase-retrieval/), full waveform inversion and electrical impedance tomography. For those the forward model is a map $F(x) = y$, and the linear theory applies to its derivative.

## Examples

- **Numerical differentiation.** Find $x = y'$ from samples of $y$. This is the inverse of the integration operator above, and it is the simplest ill-posed problem.
- **Deblurring.** The data are the image convolved with a [point spread function](/point-spread-function/) plus noise. See [image deblurring](/image-deblurring/). The DFT of the blur is small at high frequencies, so those frequencies are lost in the noise.
- **Computed tomography.** The data are line integrals of the attenuation, the [Radon transform](/radon-transform/). In the Sobolev scale the transform smooths by half a derivative, so its inverse amplifies fine detail only mildly (see [degree of ill-posedness](/degree-of-ill-posedness/)).
- **The backward heat equation.** Find the initial temperature from the temperature at a later time $T$ (see [heat equation](/heat-equation/)). The forward map damps mode $k$ by $\exp(-k^2 \pi^2 T)$, so the problem is severely ill posed.
- **Phillips' problem.** Phillips (1962) showed that the plain discretization of a first-kind integral equation gives a solution that oscillates wildly, and repaired it by a smoothness penalty. His kernel is still a standard test problem.
- **A non-example.** Fitting a straight line to a hundred points by least squares is an inverse problem in name, but it is well posed and well conditioned. Nothing in this sub-area is needed for it.

## Where it is used

Medical imaging (CT, MRI, PET, ultrasound), seismic imaging of the earth, astronomy (deconvolution and radio interferometry), microscopy, non-destructive testing, remote sensing and radar, and the estimation of parameters in differential equations. In statistics and machine learning the same mathematics appears as ill-conditioned regression, where [ridge regression](/ridge-regression/) is Tikhonov regularization under another name.

## References
