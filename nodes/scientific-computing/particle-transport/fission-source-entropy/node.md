---
tag: TND134
kind: technique
slug: fission-source-entropy
name: Shannon entropy of the fission source
aliases:
- source entropy diagnostic
area: scientific-computing/particle-transport
level: advanced
summary: Diagnoses source convergence in Monte Carlo criticality runs by tracking the entropy of the binned fission sites over generations.
prereqs: [monte-carlo-criticality, shannon-entropy]
see_also: [monte-carlo-criticality, shannon-entropy, kullback-leibler-divergence, histogram, power-iteration, k-eigenvalue-problem, mcmc-autocorrelation, effective-sample-size]
sources:
  - paper: "Taro Ueki and Forrest B. Brown, Stationarity and source convergence diagnostics in Monte Carlo criticality calculation, Proceedings of M&C 2003, ANS Topical Meeting, Gatlinburg, Tennessee, April 2003"
    locator: the Shannon entropy of the binned fission source as a diagnostic of stationarity
  - paper: doi:10.13182/NSE04-15
    title: Taro Ueki and Forrest B. Brown, Stationarity modeling and informatics-based diagnostics in Monte Carlo criticality calculations, Nuclear Science and Engineering 149(1), 2005, 38-50
    locator: the relative entropy diagnostics, the test on a two-component problem with a dominance ratio of 0.993, and the criterion from the data compression limit
  - paper: "Forrest B. Brown, On the use of Shannon entropy of the fission distribution for assessing convergence of Monte Carlo criticality calculations, PHYSOR-2006, Vancouver, Los Alamos report LA-UR-06-3737, 2006"
    locator: the entropy of the source on a mesh in MCNP, its plot over the cycles, and the choice of the inactive cycles from it
  - paper: "Forrest B. Brown, K-effective of the world and other concerns for Monte Carlo eigenvalue calculations, Progress in Nuclear Science and Technology 2, 2011, 738-742"
    locator: the cases where the source converges slowly, and the need to check the source as well as k
---

The fission source entropy is a number that a [Monte Carlo criticality](/monte-carlo-criticality/) code computes once per cycle to see whether the distribution of the fission sites has stopped changing. The code lays a mesh of $B$ bins over the fissile region, counts the fraction $p_b$ of the banked sites in each bin, and computes the [Shannon entropy](/shannon-entropy/) $H = -\sum_b p_b \log_2 p_b$. Plotted against the cycle number, $H$ moves from the value of the first guess toward the value of the fundamental mode and then stays in a band of noise. The cycles before $H$ reaches that band should be inactive. The value of $k$ often settles much earlier than the source, so a plot of $H$ catches problems that a plot of $k$ misses. Ueki and Brown introduced the diagnostic around 2003, and Brown (2006) described its use in MCNP. It is a diagnostic: a flat entropy is necessary for convergence, but it does not prove it.

## In plain words

A criticality run starts with a guess of where the fissions are, and each cycle improves the guess. The run should only start to count once the guess has stopped changing. But a whole map of fissions is hard to watch, cycle by cycle.

The entropy turns the map into one number. If all fissions are in one small spot, the number is small. If they are spread evenly over all bins, the number is at its largest. While the map is still changing, the number usually goes up or down; once the map is stable, the number only shakes a little. So you watch one curve, and you start counting when it is flat.

## When it applies

- A power iteration over generations, such as [Monte Carlo criticality](/monte-carlo-criticality/), where the source of each cycle comes from the bank of the previous one.
- The question is when to end the inactive cycles, or whether a run has converged at all.
- The system is large or loosely coupled, so the dominance ratio is close to 1 and the source converges much more slowly than $k$.
- The idea works for any Markov chain whose state is a set of points: the entropy of their [histogram](/histogram/) is a cheap summary of the state.

## The template

```pseudo id=main
FISSION-SOURCE-ENTROPY(bank of cycle g)
L1  c_b ← the number of sites of the bank in bin b, for b = 1, ..., B      ▷ hole: the mesh, B bins over the fissile region
L2  p_b ← c_b / (c_1 + ... + c_B)
L3  H_g ← -Σ_{b : p_b > 0} p_b log2 p_b
L4  add H_g to the series H_1, ..., H_g, and plot it
L5  if the series stays in one band of noise from some cycle on, end the inactive cycles there      ▷ hole: the test for the band
```

**The range.** This is a theorem. $0 \le H \le \log_2 B$, with $H = 0$ when all sites are in one bin and $H = \log_2 B$ exactly when they are spread uniformly. Also $\log_2 B - H = D(p \,\|\, u)$, the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of $p$ from the uniform distribution $u$ on the bins. So $H$ measures how far the source is from uniform. It does not measure how far the source is from the fundamental mode.

**The noise floor.** This is an asymptotic theorem (the Miller-Madow correction for the plug-in entropy). With $n$ sites drawn independently from a fixed $p$ with $m$ nonzero bins, the expected value of $H$ is about $H(p) - (m - 1)/(2n \ln 2)$ bits for large $n$, and its standard deviation is of order $1/\sqrt{n}$. With $n = 2000$ and $m = 20$ the shift is $0.0069$ bits. Sites of one bank are not independent, so in a real run the noise band is a measurement.

## Classic examples

**The entropy by hand.** A bank of 8 sites has the counts $4, 2, 1, 1$ in 4 bins. Then $p = (1/2, 1/4, 1/8, 1/8)$ and
$$H = \tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac18 \cdot 3 + \tfrac18 \cdot 3 = 1.75 \text{ bits},$$
below the maximum $\log_2 4 = 2$. The divergence from uniform is $0.25$ bits.

**A point source in a bare slab.** In the 20 cm slab of the [criticality](/monte-carlo-criticality/) page ($\Sigma_t = 1$, $\Sigma_s = 0.9$, $\nu\Sigma_f = 0.12$), all $2000$ first neutrons start at $x = 1$, and the mesh has 20 bins of 1 cm (`random.Random(3)`):

| cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $k_g$ | 0.734 | 0.835 | 0.956 | 0.994 | 1.078 | 1.093 | 1.141 | 1.102 | 1.134 | 1.142 |
| $H_g$ | 2.512 | 3.118 | 3.387 | 3.663 | 3.801 | 3.869 | 3.951 | 3.989 | 4.058 | 4.117 |

The fission source of the fundamental mode, from the discrete ordinates flux of the [k-eigenvalue](/k-eigenvalue-problem/) page binned on the same mesh, has $H = 4.185$, below $\log_2 20 = 4.322$ because the cosine shape is not uniform. The run reaches $4.15$ at cycle 18 and then stays between $4.145$ and $4.231$, with the mean $4.192$, over cycles 21 to 60. From cycle 7 on, $k$ is within the noise of the converged values, but $H$ shows that the source is still moving until about cycle 15. These are measurements for this seed.

**A thick slab: $k$ converges long before the source.** In a 100 cm slab of the same material, $k_{\mathrm{eff}} = 1.19617$ from discrete ordinates, the dominance ratio is about $0.99$ in diffusion theory, and the fundamental mode has $H = 4.136$ on 20 bins of 5 cm. A run with $1000$ neutrons per cycle started at $x = 5$ (`random.Random(6)`) gives, with $\bar k$ the mean over the last 5 cycles:

| cycle | 1 | 10 | 25 | 50 | 100 | 150 | 200 | 250 | 300 |
|---|---|---|---|---|---|---|---|---|---|
| $H_g$ | 1.207 | 2.107 | 2.582 | 3.013 | 3.580 | 3.625 | 3.901 | 3.958 | 3.644 |
| $\bar k$ | 1.160 | 1.127 | 1.175 | 1.194 | 1.186 | 1.209 | 1.172 | 1.186 | 1.176 |

By cycle 50 the values of $k$ are near the answer, but $H$ is still far below 4.136 after 300 cycles. With few neutrons in a large system the source also clusters: it falls back from 3.958 to 3.644 between cycles 250 and 300. A run that used the plot of $k$ alone would have counted a source that had not converged. This is a measurement for one seed, and it agrees with the slow power iteration that the [power iteration](/power-iteration/) page predicts for a dominance ratio near 1.

**A source that the entropy cannot see.** In the same 20 cm slab, start one run at $x = 1$ and another at $x = 19$. By symmetry the two entropy series have the same law, and their first value is the same, but the sources are mirror images. The entropy is unchanged under any permutation of the bins, so a source that has the right spread in the wrong place can have the right $H$. In a symmetric core with two loosely coupled halves, the share of the two halves can drift for many cycles while $H$ stays almost flat.

## Variations

- **Relative entropy.** Ueki and Brown (2005) compare the source of each cycle with a reference, for example the mean source of the later cycles, by the [Kullback-Leibler divergence](/kullback-leibler-divergence/), which does see a permutation of the bins.
- **The center of mass.** The mean position of the sites, in each coordinate, is a cheap second diagnostic that sees a drift between the halves of a symmetric system.
- **Tests for stationarity.** Instead of a look at the plot, a code can compare the mean and the spread of $H$ over two windows of cycles, or use the data compression criterion of Ueki and Brown (2005).
- **Mesh choice.** A coarse mesh averages out small details of the shape; a fine mesh with few sites per bin has a large noise floor. Codes choose the mesh from the number of neutrons per cycle, so that each bin gets some sites on average.
- **Other quantities.** The same series can be computed for local tallies, such as the power in each fuel assembly, which are often the slowest to converge.

## Pitfalls

- **Taking a flat curve as a proof (line L5).** A flat $H$ is necessary, not sufficient. The thick slab and the mirror examples show sources that are wrong while $H$ looks settled or has the right value.
- **A mesh that is too fine (line L1).** With many bins and few sites, the noise band is wide and its level is shifted down, so it hides the trend. Keep the number of bins well below the number of sites per cycle.
- **A mesh that covers non-fissile regions (line L1).** Bins with no fuel are always empty. They do not change $H$, but they make the scale of the plot and the maximum $\log_2 B$ misleading.
- **Too few cycles to see the band (line L5).** In a system with a dominance ratio near 1, the source can change so slowly that $H$ looks flat over a short window. Look at the whole series, and at more than one diagnostic.
- **Watching only $k$.** $k$ is a global average and is often near its final value while the shape is still wrong, as both examples show. The entropy plot is there because the $k$ plot is not enough.

## Exercises

1. Compute $H$ for the counts $5, 3, 0, 0$ in 4 bins, and the divergence from uniform.
2. Prove that $0 \le H \le \log_2 B$, with equality on the right exactly for the uniform distribution, and that $\log_2 B - H$ is the divergence from the uniform distribution.
3. Show that $H$ does not change under a permutation of the bins, and give a source in the 20 cm slab that has the entropy of the fundamental mode but is not the fundamental mode.
4. For $n$ independent sites with the true probabilities $p$ on $m$ bins, derive the first-order bias $-(m - 1)/(2n\ln 2)$ of the plug-in entropy from a second-order Taylor expansion.
5. Explain why, in power iteration, $k$ can be close to its limit while the source is still far from the fundamental mode. Use an expansion of the source in eigenfunctions and the fact that the second eigenfunction of the slab is odd.

## References
