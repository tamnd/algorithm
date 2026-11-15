---
tag: QKK97P
kind: model
slug: hammerstein-wiener-model
name: Hammerstein-Wiener model
aliases:
- block-oriented model
- Hammerstein model
- Wiener model
area: control/modeling-and-identification
level: advanced
summary: A nonlinear model made of static nonlinear blocks in series with a linear dynamic block, before it, after it or both.
prereqs: [linear-time-invariant-system, transfer-function, system-identification]
see_also: [arx-model, output-error-model, describing-function, block-diagram-reduction, least-squares-arx-identification, prediction-error-method, singular-value-decomposition, sindy]
sources:
  - paper: doi:10.1109/tac.1966.1098387
    title: "K. S. Narendra and P. G. Gallman, An iterative method for the identification of nonlinear systems using a Hammerstein model, IEEE Transactions on Automatic Control 11(3), 546-550, 1966"
    locator: the series connection of a static polynomial nonlinearity and a linear system, and the iteration that fits the two parts in turn
  - paper: doi:10.1109/tac.1981.1102761
    title: "P. Stoica, On the convergence of an iterative algorithm used for Hammerstein system identification, IEEE Transactions on Automatic Control 26(4), 967-969, 1981"
    locator: the example in which the iteration of Narendra and Gallman does not converge
  - paper: doi:10.1016/s0005-1098(97)00198-2
    title: "Er-Wei Bai, An optimal two-stage identification algorithm for Hammerstein-Wiener nonlinear systems, Automatica 34(3), 333-338, 1998"
    locator: the overparametrized least squares step and the SVD step that recovers the parameters of the blocks
  - book: doi:10.1007/978-1-84996-513-2
    title: "Fouad Giri and Er-Wei Bai (editors), Block-oriented Nonlinear System Identification, Lecture Notes in Control and Information Sciences 404, Springer, 2010"
    locator: the survey chapters on the structures with static nonlinearities and linear blocks, and on their identification
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: the chapter on models for time-varying and nonlinear systems (nonlinear models built from linear blocks and static nonlinearities)
---

A Hammerstein-Wiener model is a nonlinear dynamic model made of three blocks in series: a static nonlinearity $f$ on the input, a [linear time-invariant system](/linear-time-invariant-system/) $G$, and a static nonlinearity $g$ on the output. The two static blocks have no memory, so all the dynamics are in the linear block, and all the nonlinearity is in the static blocks. With $g$ equal to the identity it is a Hammerstein system, which describes, for example, an actuator with a nonlinear gain in front of a linear plant. With $f$ equal to the identity it is a Wiener system, which describes a linear plant read by a nonlinear sensor. The model is a small step away from a linear model: the linear block can be an [ARX model](/arx-model/) or an [output error model](/output-error-model/), and the nonlinear blocks are curves of one variable. It is a common member of the block-oriented structures, which also include the Wiener-Hammerstein sandwich (linear, static nonlinear, linear) and feedback connections.

## The machine

**Signals.** Time is discrete, with sampling period $h$. The input is $u_k$ and the output is $y_k$. In the basic form both are scalars; for several inputs and outputs, $f$ and $g$ act on each channel and $G$ is a transfer function matrix.

**The blocks.** The model is

$$w_k = f(u_k), \qquad z_k = G(q)\, w_k, \qquad y_k = g(z_k) + e_k,$$

where $q$ is the shift operator, $G(q) = B(q)/F(q)$ is a rational transfer function or a state-space model $x_{k+1} = A x_k + B w_k$, $z_k = C x_k + D w_k$, and $e_k$ is measurement noise. The intermediate signals $w$ and $z$ are not measured.

**Parametrization.** The static blocks are written as sums of known basis functions, $f(u) = \sum_{l=1}^{r} c_l \varphi_l(u)$ and $g(z) = \sum_{l=1}^{s} d_l \psi_l(z)$, for example polynomials, piecewise linear functions with fixed break points, or a saturation and a dead zone with unknown limits. Some methods parametrize the inverse $g^{-1}$ instead, which needs $g$ to be invertible.

**Normalization.** The blocks are not unique. For every $\alpha \ne 0$, the pair $(\alpha f, G / \alpha)$ gives the same $z$, and for every $\beta \ne 0$, $(\beta G, z \mapsto g(z / \beta))$ gives the same $y$. Constant offsets can also move between blocks. A model is fixed by a normalization, such as $c_1 = 1$ or $\lVert c \rVert = 1$ with a sign rule, and the same for $g$, or a unit static gain of $G$.

## What it counts

- **Parameters.** The linear block has $n_b + n_f$ parameters, or the entries of a state-space model of order $n$. The static blocks have $r$ and $s$ parameters. Two of these are fixed by the normalization.
- **Cost of a simulation.** One step costs one evaluation of $f$, one update of the linear block, and one evaluation of $g$: $O(n + r + s)$ operations in the [real RAM](/real-ram/).
- **Identification cost.** It depends on the method. A linear regression with products of parameters costs one least squares problem with $(n_b r + n_f)$ unknowns and an SVD of an $r \times n_b$ matrix. A prediction error fit costs an iterative search, with one simulation of $N$ samples per evaluation of the criterion.
- **Data.** Identification needs an input with enough amplitude levels to show the curve $f$, and enough frequency content to show $G$. A binary input shows only two points of $f$.

## Relation to other models

- **Linear models.** If $f$ and $g$ are linear, the model is the linear system $G$ with a gain. The [describing function](/describing-function/) of a static nonlinearity is a way to treat it as a gain that depends on the amplitude.
- **Order matters.** The blocks do not commute. A static nonlinearity before a linear system is a different input-output map from the same nonlinearity after it, unless the nonlinearity is linear. Ordinary [block diagram reduction](/block-diagram-reduction/) holds only for linear blocks.
- **Wiener-Hammerstein and other structures.** A static nonlinearity between two linear blocks gives the sandwich structure. A static nonlinearity in a feedback loop around a linear block gives a Lur'e system, used in absolute stability theory.
- **Volterra series.** A Hammerstein system with a polynomial $f$ of degree $r$ has a Volterra series with kernels of order up to $r$ that are nonzero only on the diagonal. A Wiener system with a polynomial $g$ has kernels that are products of the impulse response of $G$.
- **Nonlinear state-space and NARX models.** The model is a special case of a nonlinear state-space model with linear state dynamics. A Hammerstein system with an ARX linear block is a special NARX model that is linear in products of parameters.
- **Sparse regression.** [SINDy](/sindy/) fits nonlinear state equations from a library of functions; a Hammerstein system with a polynomial $f$ is such a model with a library of powers of the input.

## Known results in the model

- **Steady state (theorem).** If $G$ is asymptotically stable with static gain $G(1)$ and the input is constant at $a$, the output tends to $g(G(1) f(a))$. So a steady-state test shows only the composite curve, not the blocks.
- **Step responses (theorem).** In a Hammerstein system, the response to a step of height $a$ from rest is $f(a)$ times the step response of $G$, so the shape does not depend on $a$; only the size does. In a Wiener system, the shape changes with $a$ when $g$ is not linear. This gives a simple test to tell the two apart.
- **Separation by correlation (theorem).** If the input has zero mean and independent, identically distributed samples, and the noise is independent of the input, the cross-correlation of $u$ and the output of a Hammerstein system is $E[u_{k-\tau} y_k] = E[u f(u)] \cdot \gamma_\tau$, where $\gamma_\tau$ is the impulse response of $G$. So the impulse response is found up to scale without knowing $f$. For a Wiener system with a Gaussian input, Bussgang's theorem gives the same proportionality with the factor $E[g'(z)]$.
- **Overparametrization (theorem).** For a Hammerstein system with an ARX block and $f = \sum_l c_l \varphi_l$, the output is linear in the products $b_j c_l$ and in the coefficients of $F$. Least squares on these $n_b r$ products, followed by the best rank one approximation of the $n_b \times r$ matrix of products by the [SVD](/singular-value-decomposition/), gives $b$ and $c$ up to scale. Bai (1998) gives this two-stage method for Hammerstein-Wiener systems with an invertible output nonlinearity.
- **Alternating fits can fail (theorem).** Narendra and Gallman (1966) fit the linear block with $f$ fixed and $f$ with the linear block fixed, in turn. Stoica (1981) gave an example in which this iteration does not converge.
- **Nonconvex criterion.** The prediction error or output error criterion is not convex in the parameters, so a search can stop at a local minimum. A good starting value from a correlation or overparametrization method helps.
- **Identifiability.** Without a normalization, only the composite input-output map can be identified. With one, and with an input rich enough in amplitude and in frequency, the usual parametrizations of the blocks can be identified.

**Example.** Take $f(u) = \tanh(u)$ and $G(q) = 0.5\, q^{-1} / (1 - 0.8\, q^{-1})$, with static gain $2.5$. In the Hammerstein case ($g$ the identity), a step of height $a$ gives $y_k = 2.5 \tanh(a) (1 - 0.8^k)$. After one, two and three steps the output is $0.2$, $0.36$ and $0.488$ times its final value for every $a$.

In the Wiener case with the same $G$ and $g = \tanh$, the output after one step is $0.2157$ times its final value for $a = 0.2$, $0.2887$ times for $a = 0.5$, and $0.7617$ times for $a = 2$. The large step drives $z$ into the flat part of $\tanh$, so the output looks much faster. The final values are $\tanh(2.5 a)$: $0.46212$, $0.84828$ and $0.99991$.

## References
