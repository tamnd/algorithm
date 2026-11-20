---
tag: 9XBV35
kind: concept
slug: background-error-covariance
name: Background error covariance
aliases:
- B matrix
area: scientific-computing/data-assimilation
level: core
summary: "The covariance of errors in the prior forecast, which spreads observation information in space and between variables; too large to store, it is modeled."
prereqs: [data-assimilation-problem, covariance-matrix]
see_also: [optimal-interpolation, three-dimensional-variational-assimilation, control-variable-transform, covariance-localization, gaspari-cohn-function, ensemble-kalman-filter, hybrid-ensemble-variational, desroziers-diagnostics]
sources:
  - paper: doi:10.1002/qj.339
    title: R. N. Bannister, A review of forecast error covariance statistics in atmospheric variational data assimilation. I, Characteristics and measurements of forecast error covariances, Quarterly Journal of the Royal Meteorological Society 134(637) (2008) 1951-1970
    locator: the role of B, its structure, and the methods to estimate it
  - paper: doi:10.1002/qj.340
    title: R. N. Bannister, A review of forecast error covariance statistics in atmospheric variational data assimilation. II, Modelling the forecast error covariance statistics, Quarterly Journal of the Royal Meteorological Society 134(637) (2008) 1971-1996
    locator: control variable transforms, balance and spatial covariance models
  - paper: doi:10.1175/1520-0493(1992)120<1747:TNMCSS>2.0.CO;2
    title: D. F. Parrish and J. C. Derber, The National Meteorological Center's spectral statistical-interpolation analysis system, Monthly Weather Review 120(8) (1992) 1747-1763
    locator: B estimated from differences of forecasts valid at the same time (the NMC method)
  - paper: doi:10.1034/j.1600-0870.1999.t01-2-00003.x
    title: J. Derber and F. Bouttier, A reformulation of the background error covariance in the ECMWF global data assimilation system, Tellus A 51(2) (1999) 195-221
    locator: the multivariate formulation of B through balance operators
  - book: isbn:9780521382151
    title: Roger Daley, Atmospheric Data Analysis, Cambridge University Press, 1991
    locator: the chapters on covariance modeling for statistical interpolation
---

The background error covariance $B$ is the covariance matrix of the errors of the background $x^b$, the prior estimate of the state that a data assimilation system corrects with new observations. It sets how much the analysis trusts the background compared with the observations, and, more important, how the information of an observation spreads: to the grid points around it, and to the other variables, such as from a pressure observation to the wind. In a weather model $B$ would have about $10^{16}$ or more entries, so it is never stored. It is modeled by a sequence of operators, estimated from statistics of past forecasts or from an ensemble, and its quality is often the main limit of the analysis.

## In plain words

A forecast is never exactly right, and its errors have a pattern. If the forecast is too warm at one place, it is probably too warm nearby as well, and the wind that goes with the temperature is probably wrong in a matching way. The background error covariance describes this pattern: for every pair of model values, how strongly their errors go together, and how large each error usually is. When an observation shows that the forecast is wrong at one place, this pattern decides how the correction spreads to the places and the quantities that were not observed. A good pattern turns a few observations into a sensible correction of the whole field.

## The idea

**Definition.** With the background error $\varepsilon^b = x^b - x^t$, which is assumed to have zero mean,

$$B = \mathbb E\big[\varepsilon^b (\varepsilon^b)^\top\big], \qquad B_{ij} = \sigma_i \sigma_j\,C_{ij},$$

where $\sigma_i^2 = B_{ii}$ is the error variance of the value $i$ and $C$ is the correlation matrix. $B$ is symmetric and positive semidefinite, and the methods need it positive definite. Here $n$ is the state dimension.

**How $B$ shapes the analysis.** For a linear observation operator $H$, the analysis increment of [optimal interpolation](/optimal-interpolation/) or [3D-Var](/three-dimensional-variational-assimilation/) is

$$x^a - x^b = B H^\top (H B H^\top + R)^{-1} d,$$

so it lies in the space spanned by the columns of $B H^\top$ (a theorem). For a single observation of the value $j$ with error variance $r$ and innovation $d$, the increment is

$$x^a - x^b = \frac{d}{B_{jj} + r}\,B_{:,j},$$

a multiple of column $j$ of $B$. So the columns of $B$ are the shapes of the corrections. A "single observation experiment" with a real system shows these shapes, and it is the standard way to look at a model of $B$.

**Why it must be modeled.** $B$ has $n(n + 1)/2$ independent entries. For $n = 10^8$ that is $5 \times 10^{15}$, too many to store and far too many to estimate from data. Variational systems write $B = U U^\top$ with $U$ a product of simple operators (Bannister 2008, Part II):

- a *balance operator* that builds the wind and mass parts of the increment from a few uncorrelated control variables, for example geostrophic balance between pressure and wind;
- a *vertical transform*, for example onto the eigenvectors of a vertical covariance;
- a *horizontal transform*, often spectral, in which a homogeneous and isotropic correlation is diagonal;
- the standard deviations $\sigma_i$, as a diagonal scaling.

This is the [control variable transform](/control-variable-transform/), and it never forms $B$ or $B^{-1}$.

**Valid correlation models.** A function $c(r)$ of distance defines a valid correlation on a homogeneous grid only if every matrix $[c(|r_i - r_j|)]$ is positive semidefinite. By the theorem of Bochner this holds exactly when the Fourier transform of $c$ is nonnegative. The exponential $e^{-r/L}$, the Gaussian $e^{-r^2/(2L^2)}$ and the compactly supported [Gaspari-Cohn function](/gaspari-cohn-function/) are valid in one to three dimensions. An arbitrary function that falls to zero is not.

**How it is estimated.**

- *Differences of forecasts.* Use the differences between forecasts of different lengths that are valid at the same time, for example 48 hours minus 24 hours, as a stand-in for background errors (the NMC method, Parrish and Derber 1992). This is a heuristic: the differences have the wrong size and somewhat the wrong structure, and they are rescaled.
- *Ensembles of assimilations.* Run several assimilation cycles with perturbed observations and use the spread of the backgrounds. This also gives a flow dependent $B$.
- *Innovation statistics.* The covariance of the innovations is $HBH^\top + R$ when both are correct. Its dependence on the distance between observations separates the correlated background part from the uncorrelated observation part, and [Desroziers diagnostics](/desroziers-diagnostics/) check $B$ and $R$ after the analysis.

**Static and flow dependent.** A static $B$ is the same every day. The errors of the day depend on the weather: they are larger and differently shaped near a developing storm. Ensemble methods estimate $B$ from $N_e$ members as $X'X'^\top$, where the columns of $X'$ are $(x_i - \bar x)/\sqrt{N_e - 1}$. This matrix has rank at most $N_e - 1$ and shows spurious correlations at long distances, so it is multiplied entry by entry with a correlation of compact support ([covariance localization](/covariance-localization/)). By the Schur product theorem the product is still positive semidefinite. [Hybrid methods](/hybrid-ensemble-variational/) combine both.

## Examples

**Single observation, one dimension.** On 6 grid points take $B_{ij} = (1/2)^{|i - j|}$, unit variances and a correlation that halves with each grid step. One observation of point 1 has $r = 1/4$ and the innovation $d = 1$. The increment is $\tfrac{1}{1 + 1/4} B_{:,1} = 0.8\,(0.5, 1, 0.5, 0.25, 0.125, 0.0625)$, that is

$$x^a - x^b = (0.4,\ 0.8,\ 0.4,\ 0.2,\ 0.1,\ 0.05).$$

The observed point moves by 0.8 of the innovation, and the correction decays away from it with the shape of the correlation. With $B_{ij} = 0$ for $i \ne j$ only point 1 would move.

**Two variables.** Two values with $B = \begin{pmatrix} 1 & 1/2 \\ 1/2 & 1 \end{pmatrix}$, $x^b = (10, 12)$, and an observation $11$ of the first one with $r = 1$. The increment is $\tfrac12 (1, 1/2)$, so $x^a = (10.5, 12.25)$. The second value was not observed but moves by $0.25$, because its error is correlated with the first. If the two values are pressure and wind, this is how a pressure observation corrects the wind.

**An invalid correlation.** On three points in a line, take the correlation $0.9$ for neighbours and $0$ for the two end points. The matrix $\begin{pmatrix} 1 & 0.9 & 0 \\ 0.9 & 1 & 0.9 \\ 0 & 0.9 & 1 \end{pmatrix}$ has the determinant $1 \cdot 0.19 - 0.9 \cdot 0.9 = -0.62 < 0$, so it is not a covariance matrix. A correlation that falls from $0.9$ to $0$ in two steps is too steep. An analysis with this "$B$" can increase the error.

**Rank of an ensemble estimate.** Three members in a state of 6 values give a sample covariance $X'X'^\top$ of rank at most 2. Any increment from it lies in a plane spanned by the two independent member deviations, whatever the observations. Localization raises the rank.

## Where it is used

- [Optimal interpolation](/optimal-interpolation/) and [3D-Var](/three-dimensional-variational-assimilation/): $B$ is the static prior covariance, and its model is the main design choice.
- [4D-Var](/four-dimensional-variational-assimilation/): $B$ is the covariance at the start of the window, and the model evolves it implicitly over the window.
- [Control variable transform](/control-variable-transform/): the factor $U$ with $B = UU^\top$ is the way $B$ is coded.
- [Ensemble Kalman filter](/ensemble-kalman-filter/): the forecast covariance is estimated from the ensemble, with [localization](/covariance-localization/) and [inflation](/covariance-inflation/).
- [Hybrid ensemble-variational](/hybrid-ensemble-variational/) methods: a weighted sum of a static and an ensemble covariance.
- [Desroziers diagnostics](/desroziers-diagnostics/): consistency checks of $B$ and $R$ from innovation statistics.
- [Kriging](/kriging/) and [Gaussian processes](/gaussian-process/): the same role is played by the covariance function of the field.

## References
