---
tag: 6Z28SF
kind: algorithm
slug: parallel-replica-dynamics
name: Parallel replica dynamics
area: scientific-computing/multiscale-methods
level: advanced
summary: Runs copies of a system in one basin on many processors and adds their times up to the first escape. Exact when escapes are exponential after dephasing.
model: real-ram
complexity:
  vars: {m: the number of replicas, c: the dephasing and decorrelation length in steps, s: the mean escape time in steps, G: the cost of one step, d: the number of coordinates}
  time: {expected: O((m c + s) G)}
  space: {extra: O(m d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: true, parallel: true}
history:
  year: 1998
  people: [Arthur F. Voter]
  note: Voter gave the method in 1998. Le Bris, Lelievre, Luskin and Perez gave the mathematical analysis with the quasi-stationary distribution in 2012.
prereqs: [molecular-dynamics, markov-chain]
see_also: [hyperdynamics, temperature-accelerated-dynamics, kinetic-monte-carlo, langevin-dynamics, euler-maruyama-method, ergodicity]
sources:
  - paper: doi:10.1103/PhysRevB.57.R13985
    title: Arthur F. Voter, Parallel replica method for dynamics of infrequent events, Physical Review B 57(22), 1998, R13985
    locator: the dephasing stage, the parallel stage with the summed clock, and the decorrelation stage for correlated events
  - paper: doi:10.1515/mcma-2012-0003
    title: Claude Le Bris, Tony Lelievre, Mitchell Luskin and Danny Perez, A mathematical formalization of the parallel replica dynamics, Monte Carlo Methods and Applications 18(2), 2012
    locator: the quasi-stationary distribution, the exponential exit law and the error of the dephasing
  - paper: doi:10.1093/amrx/abu005
    title: David Aristoff, Tony Lelievre and Gideon Simpson, The parallel replica method for simulating long trajectories of Markov chains, Applied Mathematics Research eXpress 2014(2), 2014, 332-352
    locator: the version for discrete-time Markov chains and its time accounting
---

Parallel replica dynamics accelerates a simulation of a system that moves by rare escapes from basins, by using many processors on one trajectory. It runs $m$ independent copies, the replicas, of the system in the current basin. When the first replica escapes, the physical clock advances by the sum of the times of all replicas, and the trajectory continues from the escaped replica. If the escape law is exponential once the replicas have forgotten their starting point, which takes a short dephasing run, the output has the same law as one long serial run. The method needs no knowledge of the exits and no transition state theory. The parallel speedup, at most $m$, is a measured property of each run.

## In plain words

You wait for a rare event, such as a lamp that fails at random with no memory of its age. One lamp may take a year. Light a hundred lamps at once and the first one fails after a few days on average. A hundred lamps for a few days is the same amount of lamp time as one lamp for a year, so the sum of the times of all lamps is the real waiting time, and the lamp that failed shows how it failed.

The trick only works for events with no memory. A system that just entered a basin does have a memory of where it came from. So each copy first runs a short time in the basin to forget it, and only then the race starts.

## The problem

The input is a dynamics given as one time step of length $h$, a map from a point to the label of its basin, the number $m$ of replicas, and a correlation length $c$ in steps. The output is the sequence of basins visited and the time of each change, with the law of a serial run. The method assumes that the dynamics is Markov, that escapes are rare compared with the time $c h$ that a trajectory needs to lose the memory of its entry into a basin, and that the replicas are statistically independent.

## The algorithm

```pseudo id=main
PARALLEL-REPLICA-DYNAMICS(x, step, state_of, m, c, h)
L1  t ← 0;  s ← state_of(x)
L2  repeat
L3      run x serially, t ← t + h per step, until x has stayed c steps in one basin
L4      every change of basin s → s' in L3 is a transition at time t (a correlated event)
L5      dephase: start m replicas at x; run each until it stays c steps in s, restarting it at x when it leaves (t does not change)
L6      run all replicas one step at a time, in parallel
L7      at the first step w at which some replica leaves s, take the smallest such index j
L8      t ← t + (m (w - 1) + j) h
L9      x ← replica j;  record the transition s → state_of(x) at time t;  s ← state_of(x)
L10 until enough transitions;  return the transitions and t
```

Lines L3 and L4 are the *decorrelation stage*. After an escape the system can recross into the old basin or move on to a third one at once; these correlated events are not exponential, so they are followed by one serial trajectory with the true clock. Line L5 is the *dephasing stage*: each replica runs in the basin until it has forgotten its starting point, and a replica that leaves is restarted. These steps cost work but do not advance the clock. Lines L6 to L9 are the *parallel stage*. The clock in line L8 counts the trials of all replicas in the order (step, replica) up to the first escape. In continuous time the same rule is $t \leftarrow t + m\, t_{\mathrm{first}}$.

## Example

**The clock by hand.** Take a chain with one basin $A$ and two exits: from $A$ it goes to $B$ with probability 0.15 and to $C$ with probability 0.05 per step. Let $m = 3$ and $c = 1$. The decorrelation step stays in $A$ and adds 1 to the clock. Each replica dephases for 1 step and stays. In the first parallel step no replica leaves. In the second, replica 2 goes to $B$ and replica 3 goes to $C$. Replica 2 is the first, so the clock advances by $m (w - 1) + j = 3 \cdot 1 + 2 = 5$, to $t = 6$, and the next state is $B$. The work is 10 steps and the elapsed time on 3 processors is 4 steps.

**Exactness.** For this chain the serial escape time is geometric with mean $1 / 0.2 = 5$ steps and the exit is $B$ with probability 0.75. With $c = 5$ and 2000 transitions from `random.Random(2)` for each $m$:

| $m$ | mean time | standard error | fraction to $B$ |
|---|---|---|---|
| 1 | 5.047 | 0.100 | 0.760 |
| 4 | 4.997 | 0.101 | 0.761 |
| 16 | 4.971 | 0.098 | 0.760 |

All agree with the serial law. Here the escape is so fast that the dephasing costs more than the race saves.

**A measurement of the speedup.** Take Brownian dynamics $dx = -V'(x)\, dt + \sqrt{2 k_B T}\, dW$ in the double well $V = (x^2 - 1)^2$ with $k_B T = 1/3$, Euler-Maruyama steps $h = 0.01$, the basins $x < 0$ and $x \ge 0$, and $c = 50$ steps. From $x = -1$, 300 first transitions for each $m$, `random.Random(1)`:

| $m$ | mean escape time | standard error | elapsed steps | measured speedup | efficiency |
|---|---|---|---|---|---|
| 1 | 14.18 | 0.84 | 440321 | 0.97 | 0.97 |
| 4 | 14.41 | 0.94 | 135304 | 3.19 | 0.80 |
| 16 | 13.17 | 0.69 | 57237 | 6.90 | 0.43 |
| 64 | 12.90 | 0.71 | 44321 | 8.73 | 0.14 |

The mean times agree within the errors. The mean first passage time of the continuous dynamics is 12.70 by quadrature; the Euler steps see the crossing late, which makes the serial value of this discrete chain larger. The speedup is the physical time over the elapsed time: it is a measurement, and it saturates because the 50 dephasing steps and the 50 decorrelation steps per transition are not divided by $m$, while the mean escape takes only about 1300 steps.

## Correctness

The proof is in the correctness proof of this page. Its core is a property of the *quasi-stationary distribution* (QSD) $\nu$ of the basin, the law of a long trajectory that has not left: from $\nu$, the exit step is geometric (exponential in continuous time) and the exit point is independent of the exit step. For $m$ independent replicas from $\nu$, the count $m (w - 1) + j$ of line L8 then has the same geometric law, and the exit of replica $j$ has the same law as a serial exit. So the parallel stage is exact if the replicas start from $\nu$. The approximation is that the dephasing and decorrelation stages reach $\nu$ only in the limit, with an error that decays exponentially in $c$ at the rate of the spectral gap of the dynamics killed outside the basin. For a chain with the same escape probability from every point of the basin, as in the first example, every distribution is a QSD and the method is exact.

## Complexity

Per transition, the decorrelation costs about $c$ steps, the dephasing $m c$ steps or more with restarts, and the parallel stage about $s$ steps of work for a mean escape time of $s$ steps, so the work is $O((m c + s) G)$ and the elapsed time on $m$ processors is $O((c + s / m) G)$ in the [real RAM](/real-ram/) model, with $O(m d)$ memory. The speedup approaches $m$ only when $s \gg m c$, that is, when the escapes are much rarer than the dephasing time times the number of replicas. The speedup of a run is a measurement.

## Properties

- **Exact for exponential escapes.** If the replicas are in the QSD, the output has the law of the serial dynamics. No transition state theory and no harmonic approximation is used.
- **No knowledge of the exits.** The escapes are found by the dynamics itself, so unexpected mechanisms are found as well.
- **Parallel in time.** Unlike domain decomposition, it parallelizes the time axis of a small system.
- **Randomized.** The output is one sample path of the state-to-state dynamics.

## Variants and improvements

- **Continuous time.** With exponential escapes the clock advances by $m\, t_{\mathrm{first}}$; Voter's paper of 1998 states it in this form.
- **Discrete-time accounting.** The count $m (w - 1) + j$ of line L8 is exact for geometric escapes; the version for Markov chains of Aristoff, Lelievre and Simpson in 2014 uses it.
- **Fleming-Viot dephasing.** Instead of restarting a replica that leaves at the starting point, restart it at the position of another replica. This samples the QSD with an interacting particle system, and the spread of the replicas gives a test of convergence.
- **Combination with [hyperdynamics](/hyperdynamics/).** Each replica can run biased dynamics, and the clock of each replica is then its hyper time.
- **Asynchronous replicas.** Replicas on different processors need not be in step; in continuous time the times of all replicas are added up to the first escape.

## When to use it

Use parallel replica dynamics when many processors are available, escapes are rare compared with the correlation time in a basin, and transition state theory or a bias for [hyperdynamics](/hyperdynamics/) is not reliable, for example for complex rearrangements at moderate temperature. Use [kinetic Monte Carlo](/kinetic-monte-carlo/) when the catalog of events is known, and [temperature accelerated dynamics](/temperature-accelerated-dynamics/) when harmonic TST holds and the boost of parallel replicas is not enough.

## Pitfalls

- **Too short dephasing.** If the replicas still remember the entry into the basin, the first escape is biased towards the early, correlated exits. The error decays only like $e^{-\lambda c h}$ with the gap $\lambda$ of the killed dynamics.
- **Basins with internal barriers.** If a basin has slow internal motion, the QSD is reached slowly and the escape is not exponential. Define the states so that each is one well.
- **Correlated replicas.** The replicas need independent random streams. Copies of the same seed give the same trajectory.
- **Discrete clocks.** Advancing the clock by $m w$ steps for discrete time makes every time a multiple of $m$; use the count of line L8.
- **Expecting a speedup of $m$.** The dephasing and decorrelation stages are serial in time, so the speedup saturates, as in the example.

## Implementations

## History

Voter gave parallel replica dynamics in 1998 as the second of his accelerated molecular dynamics methods, after [hyperdynamics](/hyperdynamics/) in 1997. The justification was the exponential escape law of transition state theory, with a dephasing and a decorrelation time chosen from the physics. In 2012 Le Bris, Lelievre, Luskin and Perez gave the mathematical analysis: the dephased replicas approach the quasi-stationary distribution of the basin, and from it the escape is exactly exponential and independent of the exit point. Aristoff, Lelievre and Simpson gave the version for Markov chains in 2014.

## References
