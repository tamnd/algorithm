---
tag: FJ0MZ4
kind: algorithm
slug: temperature-accelerated-dynamics
name: Temperature accelerated dynamics
area: scientific-computing/multiscale-methods
level: research
summary: Finds transitions at high temperature and extrapolates their times to low temperature with harmonic transition state theory.
model: real-ram
complexity:
  vars: {n: the number of high temperature escapes before the stop, S: the cost of one escape (molecular dynamics and a saddle search)}
  time: {expected: O(n S)}
  space: {extra: O(n)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true}
history:
  year: 2000
  people: [Mads R. Sorensen, Arthur F. Voter]
  note: Sorensen and Voter gave TAD in 2000, with the extrapolation of each event time by harmonic transition state theory and the stop time from a minimum prefactor and a confidence level.
prereqs: [harmonic-transition-state-theory, molecular-dynamics]
see_also: [hyperdynamics, parallel-replica-dynamics, kinetic-monte-carlo, nudged-elastic-band, dimer-method, parallel-tempering]
sources:
  - paper: doi:10.1063/1.481576
    title: Mads R. Sorensen and Arthur F. Voter, Temperature-accelerated dynamics for simulation of infrequent events, The Journal of Chemical Physics 112(21), 2000, 9599-9606
    locator: the extrapolation of the event times, the stop time with the minimum prefactor and the confidence level, and the reflection back into the basin
  - paper: doi:10.1146/annurev.matsci.32.112601.141541
    title: Arthur F. Voter, Francesco Montalenti and Timothy C. Germann, Extending the time scale in atomistic simulation of materials, Annual Review of Materials Research 32, 2002, 321-346
    locator: the section on temperature accelerated dynamics and its assumptions
---

Temperature accelerated dynamics (TAD) finds the next escape of a system from an energy basin at a low temperature $T_{\mathrm{low}}$ by running molecular dynamics at a high temperature $T_{\mathrm{high}}$, where escapes are frequent. Each time the system escapes, the saddle of the escape is found, the system is put back into the basin, and the time of the escape is extrapolated to the low temperature with [harmonic transition state theory](/harmonic-transition-state-theory/). The event with the shortest extrapolated time is the next event at the low temperature. The high temperature run can stop early, at a time that bounds, with a chosen confidence, the extrapolated time of any event not seen yet. The method assumes HTST at both temperatures and a known lower bound on the prefactors. The boost is a measurement of each run.

## In plain words

At room temperature a system waits a long time before each change. Heat it, and the changes come much faster. But heat does not speed up every change by the same factor: a change over a high barrier speeds up more than a change over a low one. So the first change in the hot system may not be the first change in the cold one.

TAD keeps a list. Each time the hot system makes a change, it measures how high the barrier was, puts the system back, and works out when that change would have happened in the cold system. The change with the earliest cold time wins. After a while, any change not seen yet would have a cold time too late to win, with high confidence, and the search stops.

## The problem

The input is a basin, a dynamics at a temperature $T_{\mathrm{high}}$, a way to find the saddle energy $E_a$ of an escape (a [nudged elastic band](/nudged-elastic-band/) or a [dimer](/dimer-method/) search), the low temperature $T_{\mathrm{low}}$, a lower bound $\nu_{\min}$ on the HTST prefactors, and a confidence level $1 - \delta$. The output is the next event at $T_{\mathrm{low}}$ and its time. The method assumes that every event has the HTST rate $\nu_i e^{-E_i / k_B T}$, with the same prefactor $\nu_i \ge \nu_{\min}$ and barrier $E_i$ at both temperatures.

## The algorithm

```pseudo id=main
TAD(basin, T_low, T_high, ν_min, δ)
L1  t_high ← 0;  t_short ← ∞;  t_stop ← ∞
L2  while t_high < t_stop
L3      run MD at T_high to the next escape, or to t_stop;  t_high ← t_high + its time
L4      if the escape is a new event: find its saddle energy E_a;  put the system back in the basin
L5          t_low ← t_high exp(E_a (1/(k_B T_low) - 1/(k_B T_high)))
L6          if t_low < t_short:  t_short ← t_low;  best ← this event
L7              t_stop ← (ln(1/δ)/ν_min) (ν_min t_short / ln(1/δ))^(T_low/T_high)
L8  return best, t_short
```

Line L4 matters twice. Only the first occurrence of each event is extrapolated, because a repeat says nothing new. And the system is put back into the basin after an escape, so that the high temperature run continues to sample escapes from the same basin; then the escapes of each event form a Poisson process. Line L5 is the HTST ratio of the rates at the two temperatures: the prefactor cancels, and only the barrier is needed. Line L7 is the stop rule: an event not seen by $t_{\mathrm{stop}}$ has, with confidence $1 - \delta$, a rate at $T_{\mathrm{high}}$ so small that its extrapolated time is longer than $t_{\mathrm{short}}$, because its prefactor is at least $\nu_{\min}$. After the return, the low temperature clock advances by $t_{\mathrm{short}}$, the system moves to the end state of the event `best`, and TAD starts again in the new basin.

## Example

**By hand.** Take $k_B T_{\mathrm{low}} = 1$, $k_B T_{\mathrm{high}} = 2$, $\nu_{\min} = 1$ and $\delta = e^{-1}$, so $\ln(1/\delta) = 1$ and line L7 reads $t_{\mathrm{stop}} = t_{\mathrm{short}}^{1/2}$. The first escape is event $a$ with $E_a = 2$ at $t_{\mathrm{high}} = 1$: $t_{\mathrm{low}} = 1 \cdot e^{2 (1 - 0.5)} = e = 2.718$, and $t_{\mathrm{stop}} = e^{1/2} = 1.649$. The next escape is event $b$ with $E_a = 0.4$ at $t_{\mathrm{high}} = 1.5$: $t_{\mathrm{low}} = 1.5\, e^{0.2} = 1.832$, which is shorter, so $b$ is the best event and $t_{\mathrm{stop}} = 1.832^{1/2} = 1.354$. Now $t_{\mathrm{high}} = 1.5 > t_{\mathrm{stop}}$ and the run stops. The result is event $b$ at the low temperature time 1.832. Event $a$ came first at the high temperature, but $b$ comes first at the low one, because its barrier is lower.

**A catalog.** Take three events with prefactors $\nu = 1, 5, 10\ \mathrm{ps}^{-1}$ and barriers $E = 0.50, 0.55, 0.60$ eV, $T_{\mathrm{low}} = 300$ K and $T_{\mathrm{high}} = 600$ K. The high temperature run is the race of the three HTST Poisson processes (a stand-in for MD that satisfies the assumptions exactly). At 600 K the event frequencies are 0.230, 0.437 and 0.333 and the mean escape time is 3645 ps. At 300 K the exact probabilities are 0.518, 0.374 and 0.108, and the mean time is $1.299 \times 10^8$ ps. 2000 runs of TAD, `random.Random(4)`:

| $\nu_{\min}$ (1/ps) | $\delta$ | event $a$ | event $b$ | event $c$ | mean $t_{\mathrm{short}}$ (ps) | mean $t_{\mathrm{high}}$ (ps) | measured boost | escapes per run |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.001 | 0.516 | 0.368 | 0.116 | $1.248 \times 10^8$ | 26092 | 4782 | 8.13 |
| 1 | 0.05 | 0.514 | 0.375 | 0.111 | $1.298 \times 10^8$ | 17462 | 7434 | 5.76 |
| 1 | 0.3 | 0.500 | 0.388 | 0.113 | $1.300 \times 10^8$ | 11164 | 11650 | 4.01 |
| 20 | 0.001 | 0.378 | 0.479 | 0.144 | $1.470 \times 10^8$ | 6439 | 22830 | 2.63 |
| 100 | 0.001 | 0.258 | 0.460 | 0.282 | $2.049 \times 10^8$ | 4104 | 49930 | 1.69 |

The standard error of a fraction is about 0.011, and of the mean time about $3 \times 10^6$ ps. With $\nu_{\min} = 1$, a true lower bound, the fractions and the mean time agree with the exact law for every $\delta$ shown; the bound of the proof is not tight. With $\nu_{\min} = 20$ or 100, above the prefactor of event $a$, the run stops before the slow event $a$ is seen, and the result is wrong. The boost, the low temperature time over the high temperature time, is a measurement; it grows as the assumptions are weakened.

## Correctness

The proof is in the correctness proof of this page. Under HTST the first high temperature time $T_i^h$ of event $i$ is exponential with the rate $k_i^h$, and the factor of line L5 is $k_i^h / k_i^l$, so the extrapolated time is exponential with the low temperature rate $k_i^l$. The events are independent because the system is put back into the basin. So the minimum of the extrapolated times is the race of exponential clocks at $T_{\mathrm{low}}$, which is exact if all events are seen. The stop rule loses an event only if its extrapolated time would beat $t_{\mathrm{short}}$ although it was not seen by $t_{\mathrm{stop}}$; with $\nu_i \ge \nu_{\min}$, this has a probability less than $\delta$ for each event. Both results are theorems in the HTST model. For a real system they are as good as HTST: anharmonic effects and events that matter only at the high temperature are errors that the method does not detect.

## Complexity

For $n$ escapes before the stop, the cost is $n$ high temperature runs to an escape plus one saddle search for each new event, $O(n S)$ in the [real RAM](/real-ram/) model, and $O(n)$ memory for the list of events. The number of escapes grows like $\ln(1/\delta)$ times a factor that depends on the spread of the barriers, and the boost is roughly $(t_{\mathrm{short}} \nu_{\min} / \ln(1/\delta))^{1 - T_{\mathrm{low}} / T_{\mathrm{high}}}$ from line L7; the boost of a run is a measurement.

## Properties

- **Exact under HTST with all events seen.** The extrapolation maps the high temperature law to the low temperature law event by event.
- **Controlled error from the stop.** With a true $\nu_{\min}$, the probability of a wrong event is at most $\delta$ for each event.
- **Needs the barriers.** Unlike [parallel replica dynamics](/parallel-replica-dynamics/), every new event needs a saddle search.
- **Randomized.** The output is one sample of the next event.

## Variants and improvements

- **A known minimum barrier.** If all barriers of the basin are known to be at least $E_{\min}$, the stop rule can use $E_{\min}$ in place of, or with, $\nu_{\min}$, and the run can stop earlier.
- **Synthetic mode.** Once the events of a basin are known, their HTST rates are known, and the high temperature run can be replaced by draws from the catalog, as in the example.
- **Reuse of past visits.** When the system comes back to a basin, the high temperature time already spent there and the events found can be kept.
- **Parallel TAD.** Several high temperature runs of the same basin, or of basins that the system will probably visit next, run at the same time.

## When to use it

Use TAD for solids at low temperature, where HTST is accurate and escapes are much too rare for direct MD, and where saddle searches are affordable, for example for diffusion on metal surfaces and the growth of films. Do not use it when the prefactors depend strongly on the temperature, for soft or entropic systems, or when the high temperature opens events, such as melting, that do not exist at the low one. Use [kinetic Monte Carlo](/kinetic-monte-carlo/) when the catalog is known in advance, and [parallel replica dynamics](/parallel-replica-dynamics/) when HTST is not reliable.

## Pitfalls

- **A prefactor bound that is too high.** The stop comes too early, and slow events with low barriers are missed, as the rows with $\nu_{\min} = 20$ and 100 show. Nothing in the run shows this.
- **Anharmonic effects.** At the high temperature the rates deviate from HTST, and the extrapolation is wrong by the ratio of the true rate to the HTST rate.
- **A high temperature that is too high.** Events with high barriers and large prefactors dominate, the run needs more escapes, and the system may melt or change phase.
- **Forgetting to put the system back.** Without the reflection into the basin, the run leaves the basin and the events no longer race from the same state.
- **Counting repeats.** A repeated event must keep its first time; using a later time biases the extrapolation.

## Implementations

## History

Sorensen and Voter gave temperature accelerated dynamics in 2000, as the third of Voter's accelerated molecular dynamics methods after [hyperdynamics](/hyperdynamics/) in 1997 and [parallel replica dynamics](/parallel-replica-dynamics/) in 1998. The review of Voter, Montalenti and Germann in 2002 compares the three methods.

## References
