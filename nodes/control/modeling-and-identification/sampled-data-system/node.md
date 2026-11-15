---
tag: V0E4FG
kind: model
slug: sampled-data-system
name: Sampled-data system
aliases:
- sampled-data control system
- computer-controlled system
area: control/modeling-and-identification
level: core
summary: A continuous plant controlled by a digital controller through a sampler and a hold, so the loop mixes continuous and discrete time.
prereqs: [zero-order-hold-discretization, state-space-representation]
see_also: [zero-order-hold-discretization, controller-discretization, sampling-theorem, aliasing, z-transform, deadbeat-control, event-triggered-control, minimum-phase]
sources:
  - book: isbn:9780486486130
    title: Karl J. Åström and Björn Wittenmark, Computer-Controlled Systems, Theory and Design, third edition, Prentice Hall, 1997 (Dover reprint, 2011)
    locator: Section 2.3, Sampling a Continuous-Time State-Space System; Section 2.8, Poles and Zeros; Section 2.9, Selection of Sampling Rate; Section 3.4, Controllability, Reachability, Observability, and Detectability; Chapter 7, Section 7.3, Sampling and Reconstruction, and Section 7.4, Aliasing or Frequency Folding
  - book: isbn:9783540199496
    title: Tongwen Chen and Bruce A. Francis, Optimal Sampled-Data Control Systems, Springer, 1995
    locator: the treatment of the continuous-time behaviour of sampled-data systems, their stability, and the lifting technique for H2 and H-infinity design
  - paper: "R. E. Kalman, Y. C. Ho and K. S. Narendra, Controllability of linear dynamical systems, Contributions to Differential Equations 1, 189-213, 1963"
    locator: the section on the loss of controllability and observability due to sampling
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.7, Controllability After Sampling
  - paper: doi:10.1016/0005-1098(84)90062-1
    title: Karl J. Åström, Per Hagander and Jan Sternby, Zeros of sampled systems, Automatica 20(1), 31-38, 1984
    locator: the limits of the zeros of the sampled system as h goes to 0, and the unstable sampling zeros for relative degree above 2
---

A sampled-data system is a feedback loop in which a physical plant that evolves in continuous time is controlled by a computer that works in discrete time. A sampler (an analog-to-digital converter) reads the plant output every $h$ seconds, the controller computes a new input from the samples, and a hold (a digital-to-analog converter) keeps that input constant until the next update. Almost every modern controller is of this kind. At the sampling instants the loop is exactly a discrete-time linear system, given by [zero-order hold discretization](/zero-order-hold-discretization/), so the theory of discrete systems applies to the samples. Between the samples the plant runs open loop, and the analysis must say what happens there as well.

## The machine

**Parts.** With sampling period $h > 0$ and instants $t_k = kh$:

- *Plant*, in continuous time: $\dot x = A x + B u$, $y = C x$, with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $y \in \mathbb{R}^p$. A nonlinear plant $\dot x = f(x, u)$ works the same way, without the closed forms.
- *Sampler*: $y_k = y(kh)$. In practice it is preceded by an analog anti-aliasing filter.
- *Digital controller*, a discrete-time system: $\xi_{k+1} = F \xi_k + G y_k$, $u_k = H \xi_k + J y_k$, or the static case $u_k = -K x_k$ when the state is measured.
- *Hold*, the zero-order hold: $u(t) = u_k$ for $kh \le t < (k + 1) h$.

**Exact model at the samples (theorem).** Over one period the input is constant, so the [variation of constants formula](/variation-of-constants-formula/) gives

$$x_{k+1} = \Phi x_k + \Gamma u_k, \qquad \Phi = e^{Ah}, \qquad \Gamma = \int_0^h e^{As}\, ds\, B,$$

exactly, with no approximation (Åström and Wittenmark, Section 2.3). The closed loop at the samples is the discrete system with state $(x_k, \xi_k)$ and matrix

$$\mathcal{A}_{\text{cl}} = \begin{bmatrix} \Phi + \Gamma J C & \Gamma H \\ G C & F \end{bmatrix}.$$

**Between the samples.** For $0 \le \tau < h$,

$$x(kh + \tau) = e^{A\tau} x_k + \int_0^\tau e^{As}\, ds\, B\, u_k.$$

The state between samples is a fixed linear function of $x_k$ and $u_k$, so it is bounded by a constant times $\|x_k\| + \|u_k\|$.

**Computation delay.** If the new input is applied $\tau$ seconds after the sample, with $0 < \tau \le h$, the input over one period has two constant pieces, $u_{k-1}$ and then $u_k$, and the model becomes

$$x_{k+1} = \Phi x_k + \Gamma_0 u_k + \Gamma_1 u_{k-1}, \qquad \Gamma_0 = \int_0^{h - \tau} e^{As}\, ds\, B, \qquad \Gamma_1 = e^{A(h - \tau)} \int_0^{\tau} e^{As}\, ds\, B.$$

The extra state $u_{k-1}$ makes the order $n + m$.

**Example: a stable loop that sampling makes unstable.** The plant $\dot x = u$ with the continuous feedback $u = -k x$, $k > 0$, is stable for every $k$. With a sampler and a hold, $\Phi = 1$, $\Gamma = h$, and $x_{k+1} = (1 - kh) x_k$. The samples converge if and only if $0 < kh < 2$. At $kh = 1$ the state reaches zero in one step, and for $kh > 2$ the loop diverges, oscillating in sign.

## What it counts

At the samples, the model predicts the state and the output sequence exactly, and it gives the pulse transfer function $H(z) = C (zI - \Phi)^{-1} \Gamma$ (see [z-transform](/z-transform/)). Between the samples, it predicts the continuous trajectory by the formula above. The two views differ in what they can see:

- **Intersample ripple.** A discrete design can make the samples of the output settle while the continuous output still moves between the samples. It happens when the controller makes the input sequence oscillate, for example a design that cancels a sampled zero near $-1$: the input then alternates in sign at each step, and the continuous output ripples between samples that look constant.
- **Hidden oscillations.** For the oscillator $A = \begin{bmatrix} 0 & \omega \\ -\omega & 0 \end{bmatrix}$ with $y = x_1$, sampled with $h = 2\pi / \omega$, $\Phi = I$. A free oscillation $y(t) = \sin(\omega t)$ has every sample equal to 0, so it is invisible to the controller.
- **Aliasing.** A signal at frequency $\omega$ and one at $\omega + 2\pi k / h$ give the same samples. A disturbance above the Nyquist frequency $\pi / h$ appears in the samples as a slow disturbance. See [aliasing](/aliasing/) and the [sampling theorem](/sampling-theorem/).

Performance measures that depend on the continuous signals, such as the $H_2$ or $H_\infty$ norm from a continuous disturbance to a continuous error, need a model that keeps the intersample behaviour. *Lifting* does this: it treats the piece of each continuous signal on $[kh, (k + 1) h)$ as one element of a function space, which gives a time-invariant discrete system with infinite-dimensional input and output spaces (Chen and Francis 1995).

## Relation to other models

- **Discrete-time LTI model.** The samples of a sampled-data loop with an LTI plant form a discrete LTI system. This is the basis of *direct digital design*: discretize the plant with [zero-order hold discretization](/zero-order-hold-discretization/) and design on $(\Phi, \Gamma)$, for example a [deadbeat control](/deadbeat-control/) law.
- **Emulation.** The other route designs a continuous controller and discretizes it, by the [bilinear transform](/bilinear-transform/) or other rules (see [controller discretization](/controller-discretization/)). It is an approximation, and its quality depends on $h$.
- **Periodic time-varying system.** In continuous time, the loop is a [linear time-varying system](/linear-time-varying-system/) with period $h$: shifting the time by $h$ does not change it, but shifting by less does. So it has no ordinary transfer function in continuous time; a sinusoid in gives a sinusoid plus its aliases out.
- **Event-triggered and networked control.** If the controller updates only when an event condition holds, instead of every $h$ seconds, the result is [event-triggered control](/event-triggered-control/). Variable delays from a network give a time-varying $\Gamma_0$ and $\Gamma_1$.
- **Hybrid systems.** A sampled-data loop is a simple hybrid system: continuous flow between samples and a discrete jump of the controller state at each sample.

## Known results in the model

- **Stability (theorem).** For an LTI plant, a zero-order hold and a discrete LTI controller, the continuous-time closed loop is exponentially stable if and only if $\mathcal{A}_{\text{cl}}$ is a Schur matrix, with all eigenvalues inside the unit circle. The intersample bound above gives the "if" part; the samples of a stable continuous trajectory give the "only if" part (Chen and Francis 1995).
- **Fast sampling (theorem).** $\Phi = I + hA + O(h^2)$ and $\Gamma = hB + O(h^2)$. If a continuous LTI controller stabilizes the plant, its emulation by the forward Euler, backward Euler or Tustin rule stabilizes the sampled-data loop for every small enough $h$, by continuity of eigenvalues. The theorem gives no value of $h$. For the plant $\dot x = u$ above, the bound is $h < 2/k$.
- **Controllability after sampling (theorem).** If $(A, B)$ is controllable, and no two eigenvalues of $A$ with the same real part have imaginary parts that differ by a nonzero multiple of $2\pi / h$, then $(\Phi, \Gamma)$ is controllable (Kalman, Ho and Narendra 1963; Chen 1999, Section 6.7). Observability is dual. The condition holds for almost every $h$.
- **Pathological sampling (example).** For the oscillator above with $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, the eigenvalues are $\pm i\omega$, which differ by $2\omega$. With $h = \pi / \omega$,

  $$\Phi = e^{Ah} = -I, \qquad \Gamma = \int_0^{\pi/\omega} \begin{bmatrix} \sin \omega s \\ \cos \omega s \end{bmatrix} ds = \begin{bmatrix} 2/\omega \\ 0 \end{bmatrix},$$

  so $[\Gamma \;\; \Phi \Gamma] = \begin{bmatrix} 2/\omega & -2/\omega \\ 0 & 0 \end{bmatrix}$ has rank 1. The continuous pair is controllable, but the sampled pair is not: the samples can never move the second state component.
- **Sampling zeros (theorem).** The sampled system has, in general, $n - 1$ zeros even when the continuous plant has fewer. As $h \to 0$, the zeros that come from continuous zeros $z_i$ are close to $e^{z_i h}$, and so tend to 1, and the extra ones go to fixed limits that depend only on the relative degree $r$. For $r \ge 3$, some of these limits are outside the unit circle, so the sampled system is not [minimum phase](/minimum-phase/) for small $h$ even when the continuous plant is (Åström, Hagander and Sternby 1984). For $1/s^3$ with a zero-order hold, the zeros are $-3.7321$ and $-0.2679$ for every $h$. A controller that cancels the zero at $-3.7321$ is unstable, and one that cancels a zero near $-1$ gives the ripple described above.
- **Choice of the sampling period (rule of thumb).** Fast sampling makes the loop close to its continuous design but costs computation, and makes the sampled model more sensitive to numerical errors, since $\Phi$ then has all its eigenvalues near 1. Slow sampling loses phase margin through the hold, which acts approximately as a delay of $h/2$, and risks aliasing. Practical rules relate $h$ to the rise time or the crossover frequency of the closed loop; Åström and Wittenmark (Section 2.9) discuss them. They are rules of thumb, not theorems.

## References
