---
tag: F1WZPY
kind: definition
slug: observation-operator
name: Observation operator
aliases:
- forward observation operator
area: scientific-computing/data-assimilation
level: intro
summary: "The map H from the model state to the observed quantities, such as interpolation to a station or a radiative transfer model for satellite data."
prereqs: [data-assimilation-problem]
see_also: [forward-operator, adjoint-model, optimal-interpolation, three-dimensional-variational-assimilation, bilinear-interpolation, automatic-differentiation, background-error-covariance, nudging]
sources:
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the observation operator H, its linearization and the notation used here
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Chapter 5 (the observation operator in the least squares and variational analysis)
  - book: isbn:9781611974539
    title: M. Asch, M. Bocquet and M. Nodet, Data Assimilation, Methods, Algorithms, and Applications, SIAM, 2016
    locator: Chapter 1 (the observation operator as the forward map of an inverse problem)
---

The observation operator of a data assimilation system is the map $H$ that takes a model state $x$ to the values that the instruments would measure if the state were true. It lets the system compare the model with observations of any kind, in the space of the observations: a thermometer between grid points, a wind speed, a satellite radiance or a radio occultation bending angle. Its linearization $\mathbf H$ and the transpose $\mathbf H^\top$ (the adjoint) are needed by every method that computes a gain or a gradient, and the differences $y^o - H(x)$ between the observations and the model values are the departures that drive the analysis.

## Definition

Let the model state be $x \in \mathbb R^n$ and let there be $p$ observations $y^o \in \mathbb R^p$ at one time. An **observation operator** is a map $H : \mathbb R^n \to \mathbb R^p$ such that

$$y^o = H(x^t) + \varepsilon^o,$$

where $x^t$ is the true state, projected on the model grid, and $\varepsilon^o$ is the **observation error**. The observation error has two parts: the error of the instrument, and the **representation error**, which comes from scales and processes that the model state does not resolve and from errors in $H$ itself. Its covariance is $R$. This is the notation of Ide, Courtier, Ghil and Lorenc (1997).

For a differentiable $H$:

- The **tangent linear observation operator** at a state $x^b$ is the Jacobian $\mathbf H = \partial H/\partial x\,(x^b)$, a $p \times n$ matrix, so that $H(x^b + \delta x) \approx H(x^b) + \mathbf H\,\delta x$.
- The **adjoint observation operator** is its transpose $\mathbf H^\top$, which maps a vector of sensitivities to the observations to a vector of sensitivities to the state.
- The **innovation**, or observation minus background, is $d = y^o - H(x^b)$.

The operator is **linear** if $H(x) = \mathbf H x$ for a fixed matrix. When the observations are spread over a time window, $H_k$ acts on the state at the time $t_k$ of each observation. In 4D methods the operator from the initial state is the composition $H_k \circ M_{0 \to k}$ with the model.

## Examples and non-examples

**Example (point value).** If the observation is the value at grid point $j$, $H$ is row $j$ of the identity matrix, and $\mathbf H = H$.

**Example (linear interpolation).** A station lies at the position $2.25$ on a grid with spacing 1, between grid points 2 and 3, where the model has $x_2 = 10$ and $x_3 = 14$. The weights are $0.75$ and $0.25$, so $H(x) = 0.75 \cdot 10 + 0.25 \cdot 14 = 11$. The row of $\mathbf H$ is zero except for $0.75$ and $0.25$ in the columns 2 and 3. In two dimensions this is [bilinear interpolation](/bilinear-interpolation/) from the four grid points around the station.

**Example (wind speed, nonlinear).** The state holds the wind components $u$ and $v$ at a point, and an instrument measures the speed, $H(u, v) = \sqrt{u^2 + v^2}$. At $(u, v) = (3, 4)$ the speed is 5 and the tangent linear operator is the row $(u/s, v/s) = (0.6, 0.8)$. A change of the wind perpendicular to $(3, 4)$ does not change the speed to first order. The adjoint maps a sensitivity $\bar s$ to the speed to $(0.6\,\bar s, 0.8\,\bar s)$.

**Example (satellite radiance).** A sounding channel measures radiation emitted by a deep layer of the atmosphere. Its observation operator is a radiative transfer model that integrates the temperature and humidity profile with a weighting function. Linearized about a profile, one row of $\mathbf H$ is that weighting function over the model levels, so one observation constrains a weighted mean of many state values.

**Example (column total).** The total water vapour of a column is $H(x) = \sum_l q_l\,\Delta p_l/g$, a sum over the model levels of specific humidity times the pressure thickness, divided by gravity. It is linear in $q$ if the pressures are fixed.

**Non-example (retrieval).** A temperature profile retrieved from radiances by an inversion is not an observation operator. It is itself an estimate, with errors correlated with a prior that the retrieval used. Assimilating the radiances with a radiative transfer operator avoids this.

**Non-example (the gain).** The map from observations back to the grid, such as the gain $K$ of [optimal interpolation](/optimal-interpolation/), goes the other way. $H$ maps state to observations; the analysis maps observations to state.

**Non-example (an inverse of $H$).** $H$ usually has many more inputs than outputs ($p \ll n$), so it has no inverse. The background and its covariance $B$ supply the missing information.

## Related definitions

- [Forward operator](/forward-operator/): the same object in the language of inverse problems.
- [Adjoint model](/adjoint-model/): the transpose of a tangent linear model. $\mathbf H^\top$ is the adjoint of the observation operator, and its correctness is checked by the dot product test $\langle \mathbf H u, w\rangle = \langle u, \mathbf H^\top w\rangle$.
- [Background error covariance](/background-error-covariance/): $\mathbf H B \mathbf H^\top$ is the background error covariance in observation space, and $B\mathbf H^\top$ spreads the information of an observation over the grid.
- [Data assimilation problem](/data-assimilation-problem/): the observation equation $y^o_k = H_k(x_k) + \varepsilon^o_k$ is half of its definition.
- [Automatic differentiation](/automatic-differentiation/): a way to produce $\mathbf H$ and $\mathbf H^\top$ from the code of $H$.

## References
