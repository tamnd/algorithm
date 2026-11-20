---
tag: W2ZY5Q
kind: technique
slug: observing-system-simulation-experiment
name: Observing system simulation experiment
aliases:
- OSSE
- twin experiment
area: scientific-computing/data-assimilation
level: core
summary: "Tests an assimilation method or a planned observing network with synthetic observations from a known truth run, and measures how well the analysis recovers that truth."
prereqs: [data-assimilation-problem, lorenz-96-model]
see_also: [nudging, optimal-interpolation, three-dimensional-variational-assimilation, ensemble-kalman-filter, four-dimensional-variational-assimilation, desroziers-diagnostics, observation-operator, bootstrap-method]
sources:
  - book: doi:10.1007/978-3-540-74703-1_24
    title: M. Masutani, T. W. Schlatter, R. M. Errico, A. Stoffelen, E. Andersson, W. Lahoz, J. S. Woollen, G. D. Emmitt, L.-P. Riishøjgaard and S. J. Lord, Observing system simulation experiments, in W. Lahoz, B. Khattatov and R. Ménard (eds), Data Assimilation, Making Sense of Observations, Springer, 2010, 647-679
    locator: Sections 1 to 3 (the method, its history with the same model and with a different model for the nature run, and the nature run) and Section 4 (simulated observation errors)
  - paper: doi:10.1175/1520-0469(1998)055<0399:OSFSWO>2.0.CO;2
    title: E. N. Lorenz and K. A. Emanuel, Optimal sites for supplementary weather observations, simulation with a small model, Journal of the Atmospheric Sciences 55(3) (1998) 399-414
    locator: the 40-variable model and the simulated experiments with supplementary observations at chosen sites
---

An observing system simulation experiment tests a data assimilation method, or an observing network that does not exist yet, against a truth that is known exactly. A long free run of a model, the *nature run*, plays the role of the real atmosphere. Synthetic observations are computed from it with the [observation operator](/observation-operator/) of each instrument, and random errors are added. The assimilation system then processes these observations as if they were real, and its analyses and forecasts are compared with the nature run. With real data the true state is never known, so the analysis error can only be estimated. Here it is computed exactly. This is the standard test of new assimilation methods on small models such as [Lorenz-96](/lorenz-96-model/), and the standard way to estimate the value of a planned satellite before it is built (Masutani et al. 2010).

## In plain words

To know how good a method is, we must compare its answer with the truth, but for the real atmosphere nobody knows the truth. So we make one. We run a model for a long time and call that run the truth. Then we pretend to measure it: we read the values that the instruments would see and add noise of the size that real instruments have. We give these fake measurements to the method and check how close its answer comes to the run we started from. We can repeat this with and without a new instrument and see how much the instrument helps.

## When it applies

- A method is new or changed, and its error must be measured against a known truth, for example to compare it with older methods or to tune a parameter such as a gain, an inflation factor or a localization radius.
- An observing system is planned, and its value must be estimated before it exists, for example a new satellite instrument or a different placement of stations.
- The observation operator and the error statistics of the instrument can be simulated well enough that the synthetic data behave like the real data.
- For the results to carry over to the real system, the nature run must be a realistic model, and the observations of the existing network must be simulated as well as the new ones, because the value of a new observation depends on the others.

## The template

```pseudo id=main
SIMULATION-EXPERIMENT(nature model, assimilation system A, networks S_1..S_m, T, T_s)
L1  run the nature model freely over [0, T] and store the truth x^t(t)
L2  for each network S do
L3      for each observation time t_k and each observation i of S do
L4          y_{k,i} <- H_{k,i}(x^t(t_k)) + a random error from the error model of i
L5      run A over [0, T] with the observations y and a first guess not taken from x^t
L6      e_S <- mean over t_k > T_s of RMSE(x^a(t_k), x^t(t_k))      ▷ also forecast errors
L7  return the errors e_S, to compare between networks and with the observation errors
```

The holes are the nature model (line L1), the observation operators and their error models (line L4), the assimilation system (line L5) and the error measure (line L6). The root mean square error is $\mathrm{RMSE} = \big(\tfrac1n \sum_j (x^a_j - x^t_j)^2\big)^{1/2}$, averaged over the analysis times after a spin-up $T_s$ that removes the effect of the first guess. Two reference values give it a meaning: the observation error standard deviation $\sigma^o$, and the error of a free run without observations. An analysis error well below $\sigma^o$ shows that the model carries information from earlier observations.

In a full experiment for a new instrument, the loop over networks has two members: a control run with the simulated existing observations, and a run that adds the new ones. The difference of the forecast errors is the estimated impact of the instrument (Masutani et al. 2010, Section 1).

**Measurement on Lorenz-96.** Nature run: [Lorenz-96](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with $\Delta t = 0.01$, after a spin-up of 20 time units. All 40 variables are observed every 0.05 time units with Gaussian errors of standard deviation $\sigma^o$ (fixed seed). The assimilation is [nudging](/nudging/) with the gain $g$ on every variable, toward the observations interpolated linearly in time, from a first guess with errors of standard deviation 3. The table gives the RMSE averaged over $t = 10$ to $30$, with the reference code of the nudging page.

| assimilating model | $\sigma^o$ | $g = 2$ | $g = 5$ | $g = 10$ |
|---|---|---|---|---|
| $F = 8$ (the nature model) | 0.5 | 0.42 | 0.20 | 0.23 |
| $F = 8$ (the nature model) | 1 | 0.72 | 0.40 | 0.46 |
| $F = 8$ (the nature model) | 2 | 1.06 | 0.80 | 0.91 |
| $F = 7$ | 1 | 0.78 | 0.44 | 0.46 |
| $F = 9$ | 1 | 1.29 | 0.46 | 0.47 |

A free run without observations has an RMSE of about 5.1 over the same period. With the best gain the analysis error is about $0.4\,\sigma^o$, and it scales with $\sigma^o$. A wrong forcing in the assimilating model, a simple model error, makes every error larger: the experiment with the nature model itself is optimistic.

## Classic examples

- **Tests of new filters on small models.** Most papers on the [ensemble Kalman filter](/ensemble-kalman-filter/), the [local ensemble transform Kalman filter](/local-ensemble-transform-kalman-filter/) and [particle filters](/particle-filter/) report the time mean analysis RMSE on Lorenz-96 with 40 variables against $\sigma^o$, as a function of the ensemble size.
- **Tuning of free parameters.** The gain of [nudging](/nudging/), the length scales of the [background error covariance](/background-error-covariance/) in [optimal interpolation](/optimal-interpolation/) and [3D-Var](/three-dimensional-variational-assimilation/), the [covariance inflation](/covariance-inflation/) factor and the [localization](/covariance-localization/) radius are chosen where the RMSE against the truth is smallest.
- **Supplementary observations at chosen sites.** Lorenz and Emanuel (1998) introduced the 40-variable model to test, by simulation, where extra observations should be placed to improve analyses and forecasts most.
- **Planned satellite instruments.** Weather centers simulate the observations of a proposed instrument, such as a space-borne wind lidar, from a nature run of a high quality global model, and measure the change of forecast skill when they are added to the simulated existing network (Masutani et al. 2010).
- **Checks of diagnostics.** [Desroziers diagnostics](/desroziers-diagnostics/) and other estimates of $B$ and $R$ are checked on synthetic data, where the true error covariances are known.

## Variations

- **Same model or a different model.** If the nature run and the assimilation use the same model, there is no model error, and only the errors of the initial state are tested. This is the usual setting for tests of methods on small models. For estimates of the value of real instruments, the nature run comes from a model that is clearly different from the assimilating model, ideally from another center, so that the experiment has realistic model errors (Masutani et al. 2010, Section 2).
- **Different resolution.** The nature run has a finer grid than the assimilating model. The unresolved scales then give a representation error in the observations without any extra modeling.
- **Perfect or simulated observation errors.** The simplest choice adds independent Gaussian errors with the covariance $R$ that the assimilation assumes. A more realistic choice adds correlated errors, biases, and errors from the simplified observation operator.
- **Data denial with real observations.** Remove an existing observation type from the real data and compare the forecast skill with the full system. This uses no nature run, so it can only measure instruments that already exist. Its results for existing instruments are used to calibrate the simulation: the simulated impact of an existing type should match its impact in the data denial runs (Masutani et al. 2010, Section 2).
- **Ensembles of experiments.** Repeat the experiment with several seeds for the observation errors and the first guess, and report the spread of the error statistics, as with a [bootstrap](/bootstrap-method/) estimate.

## Pitfalls

- **Too optimistic with the same model.** With no model error the background is too good and the departures of the observations from the background are too small, so the forecast skill is too high. The simulated observations also fit the dynamics of the model exactly, so few observations seem enough (Masutani et al. 2010, Section 2). The rows $F = 7$ and $F = 9$ of the table show the effect on a small scale.
- **Errors drawn from the assumed $R$.** If the synthetic errors have exactly the statistics that the method assumes, the method is tested in its most favourable case. Test also with errors that the method does not expect.
- **First guess from the truth.** Starting the assimilation from the nature run, or from the truth plus small noise, hides the behaviour of the method when it must recover from a large error. Use a first guess from another time of the run or with large errors, and leave out a spin-up period.
- **Short runs and one seed.** In a chaotic model the error statistics vary from one period to the next. Average over a long period and several seeds before ranking two methods that differ by a few percent.
- **Verifying against the analysis.** The point of the experiment is that the truth is known. Errors computed against the analysis of the system itself, as must be done with real data, measure consistency and not accuracy.

## Exercises

1. In the scalar cycle of the [data assimilation problem](/data-assimilation-problem/), a random walk with $Q = 1$ observed with $R = 1$, show that the analysis variance tends to $(\sqrt 5 - 1)/2 \approx 0.618$. Then simulate the cycle with a fixed seed, compute the mean square error of the analysis against the simulated truth, and check that it approaches the same value.
2. Repeat the measurement above with only every second variable observed, and compare the error of the observed and of the unobserved variables for the gains 2, 5 and 10.

## References
