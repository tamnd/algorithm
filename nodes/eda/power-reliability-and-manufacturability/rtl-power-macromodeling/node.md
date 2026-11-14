---
tag: AN9M3C
kind: technique
slug: rtl-power-macromodeling
name: RTL power macromodeling
aliases:
- power macromodels
- power factor approximation
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Characterizes each RTL block once by a table or equation of power versus input statistics, then estimates design power from those models during RTL simulation.
prereqs: [dynamic-power-dissipation, switching-activity, linear-regression]
see_also: [hamming-distance, ordinary-least-squares, overfitting, cross-validation, monte-carlo-power-estimation, glitch-power, high-level-synthesis, ripple-carry-adder]
sources:
  - paper: doi:10.1109/92.386219
    title: Paul E. Landman and Jan M. Rabaey, Architectural power analysis, the dual bit type method, IEEE Transactions on VLSI Systems 3(2), 173 to 187, June 1995
    locator: the dual bit type data model (a region of uniform white noise bits and a region of sign bits, with breakpoints from the word statistics) and the capacitance models of the datapath modules, with their coefficients from characterization
  - paper: "Subodh Gupta and Farid N. Najm, Power modeling for high-level power estimation, IEEE Transactions on VLSI Systems 8(1), 18 to 29, February 2000"
    title: Subodh Gupta and Farid N. Najm, Power modeling for high-level power estimation, IEEE Transactions on VLSI Systems 8(1), 18 to 29, February 2000
    locator: the macromodel as a three-dimensional table indexed by the average input signal probability, the average input transition density and the average output transition density
  - paper: "S. R. Powell and P. M. Chau, Estimating power dissipation of VLSI signal processing chips, the PFA technique, VLSI Signal Processing IV, IEEE Press, 250 to 259, 1990"
    title: S. R. Powell and P. M. Chau, Estimating power dissipation of VLSI signal processing chips, the PFA technique, VLSI Signal Processing IV, IEEE Press, 250 to 259, 1990
    locator: the model of a constant power per operation for each kind of block, scaled by the size of the block
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the part on estimation at the behavioral and register-transfer levels
---

RTL power macromodeling estimates the power of a design described at the register-transfer level, before a gate netlist exists or when gate-level estimation is too slow. Each block of a library (an adder, a multiplier, a multiplexer, a register file) is characterized once: it is simulated at the gate level, or at the circuit level, on many input streams, its power is measured, and a model is fitted that gives the power as a function of a few statistics of the input stream, such as the Hamming distance between consecutive inputs or the signal probability and transition density of the inputs. The model is a table or an equation, and its numbers are fitted, not derived. During RTL simulation the tool computes the same statistics at the ports of each block, evaluates the models and adds the results. A macromodel is fast and good for comparing architectures, but its error is that of a fit: it is right on average for streams like the training streams and can be far off for others.

## In plain words

Simulating every gate of a large chip to find its power is slow. But a chip is made of a few kinds of blocks, such as adders and multipliers, used many times.

So measure each kind of block once. Feed it many kinds of input data, measure the power with a detailed simulation, and write down a simple rule that predicts the power from a few numbers that describe the data, for example how many input bits change per cycle.

Later, when you simulate the whole design at the block level, you count those numbers at each block, look up the rule and add the answers. This is much faster than gate-level simulation.

The rule is only a fit to the data you used to make it. If the real data look different, for example because they are strongly correlated, the answer can be wrong by a large factor.

## When it applies

- The design is built from blocks that are reused, such as datapath operators, memories and controllers, and a gate-level or transistor-level model of each block exists for characterization.
- Power is needed early, to compare architectures, bit widths or schedules in [high-level synthesis](/high-level-synthesis/), or fast, for long software workloads that gate-level simulation cannot cover.
- A relative answer is enough, or an error of some tens of percent is acceptable. Sign-off needs gate-level analysis.
- The power of a block depends mostly on a few statistics of its input stream. This is true of the [dynamic power](/dynamic-power-dissipation/), which follows the [switching activity](/switching-activity/), less so of the glitch part, which depends on delays.

## The template

```pseudo id=main
CHARACTERIZE(block B, statistic s, training streams S_1, ..., S_m)
L1  for each training stream S_j do
L2      simulate B at gate level on S_j and measure its average power P_j
L3      compute the statistic x_j ← s(S_j) at the inputs of B
L4  fit a model M to the pairs (x_j, P_j), as a table of means or by least squares
L5  return M with its error on streams not used in the fit

ESTIMATE(design D at RTL, input stream S)
L6  simulate D at RTL on S and record the values at the ports of each block
L7  for each block instance B do P_B ← M_B(s(stream at the ports of B))
L8  return the sum of P_B, plus the estimates for wires, clock and control
```

The holes are the statistic $s$ (line L3), the form of the model (line L4) and the granularity: the statistic can be computed per cycle, for a cycle-accurate power trace, or as an average over the stream. The numbers of $M$, the coefficients or the table entries, are fitted to the measured power; they inherit the delay model, the library and the process corner of the gate-level simulation of line L2.

**Two facts about the fit.** Let the training data be pairs $(x, P)$ from some distribution, for example one pair per cycle.

1. *The table of means is the best function of $x$.* Among all functions $g$, the mean squared error $E[(P - g(x))^2]$ is smallest for $g(x) = E[P \mid x]$, the mean of $P$ over the training cycles with that value of $x$. Proof: for any $g$, $E[(P - g(x))^2] = E[(P - E[P \mid x])^2] + E[(E[P \mid x] - g(x))^2]$, because the cross term has mean zero given $x$. So a table indexed by $x$ that stores the means is the limit of any model that uses $x$ alone, and the remaining error is the variance of $P$ given $x$, which no fit can remove.
2. *Linear models can be averaged, other models cannot.* If $M(x) = c_0 + c_1 x$, the mean of the per-cycle predictions is $M$ of the mean statistic, so a linear model can be evaluated once on the average statistic. For a concave table, Jensen's inequality gives $M(E[x]) \ge E[M(x)]$, so evaluating a table on average statistics overestimates. The least-squares line with an intercept also passes through the point of the means, so on the training distribution it gives the right average power, whatever its error per cycle.

**Worked example.** Take a 4-bit [ripple-carry adder](/ripple-carry-adder/) of 17 gates (a half adder of XOR and AND at bit 0, and at bits 1 to 3 an XOR and an AND for propagate and generate, then an XOR, an AND and an OR for the sum and the carry) and give every gate output the same capacitance, so the power per cycle is proportional to the number of gate transitions. Characterize it under the zero-delay model on all $2^{16}$ pairs of consecutive input vectors, with the statistic $x$ the [Hamming distance](/hamming-distance/) between the two 8-bit input vectors. The mean power is $1875/256 \approx 7.32$ transitions per cycle. The exact means per Hamming distance are:

| Hamming distance | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| mean transitions | 0 | 3.95 | 5.93 | 7.13 | 7.73 | 7.96 | 7.91 | 7.80 | 7.75 |
| linear model | 5.13 | 5.68 | 6.23 | 6.78 | 7.32 | 7.87 | 8.42 | 8.97 | 9.52 |

The least-squares line, by [ordinary least squares](/ordinary-least-squares/) over all pairs, is $P \approx c_0 + c_1 x$ with the fitted values $c_0 = 1313/256 \approx 5.13$ and $c_1 = 281/512 \approx 0.55$. It explains only 7 percent of the variance ($R^2 \approx 0.07$), and the root mean square error per cycle is 2.8 transitions. The table is a better model by fact 1: the power grows fast for the first changed bits and then stays near 7.8, because once a few bits change most gates already switch about as often as under random inputs. Both models are exact on average for these training data, as fact 2 says. Evaluating the table at the average distance 4 gives 7.73, not the true 7.32.

## Classic examples

- **Constant power per operation.** Powell and Chau (1990) gave each kind of operator a power per operation, scaled by its size, as for a multiplier of a given width. It treats the data as random and ignores their statistics.
- **The dual bit type method.** Landman and Rabaey (1995) observed that in two's complement data from signal processing, the low bits behave like uniform white noise, each with activity about $1/2$, while the high bits are copies of the sign and switch only when the sign changes. Between two breakpoints, computed from the mean, variance and correlation of the words, the model passes from one region to the other. The capacitance of a module is a fitted coefficient per white noise bit plus a fitted coefficient per sign transition pattern, weighted by the probabilities of the patterns.
- **Tables of input and output statistics.** Gupta and Najm (2000) index a three-dimensional table by the average input signal probability, the average input transition density and the average output transition density of the block, filled by characterization, and also fit equations to the table.
- **Regression on toggles.** Cycle-accurate models predict the power of each cycle from the Hamming distance, or from one toggle indicator per input bit with its own coefficient, fitted by least squares on gate-level traces. Bogliolo, Benini and De Micheli (2000) studied such regression models and their adaptation to the data at run time.

## Variations

- **Per-bit coefficients.** In the adder above, flipping one input bit costs on average 3.25 transitions for bit 0, 4.75 for bit 1, 4.38 for bit 2 and 3.44 for bit 3. Bit 0 enters a half adder of two gates and bit 3 has no carries above it, while bits 1 and 2 drive full adders and the carries above them. A model with one coefficient per input bit sees this; a model with the Hamming distance alone does not.
- **Output statistics.** Including the activity at the outputs, which the RTL simulation also gives, helps when the inputs alone do not decide the internal activity.
- **Glitch-aware characterization.** Characterizing with a gate-level simulator with real delays includes the [glitch power](/glitch-power/) in the coefficients, for the data and the timing used in the fit.
- **Sampling.** The RTL simulation can be sampled, and the estimate given with a confidence interval as in [Monte Carlo power estimation](/monte-carlo-power-estimation/).
- **Learned models.** Newer methods fit models with many features, such as register toggles, to gate-level traces by machine learning. They are fits of the same kind and need the same care with data outside the training range.

## Pitfalls

- **The training data decide the answer.** In the adder, let input $a$ count up by 1 each cycle and keep $b$ constant. With $b = 0$ the true power is $11/4 = 2.75$ transitions per cycle; with $b = 15$ it is $51/8 \approx 6.38$, because every change of $a$ now ripples through the carries. The input Hamming distances are the same in both, so the linear model gives 6.16 for both. A model fitted on random data is wrong by a factor of 2.2 on the first stream. Characterize with data like those of the application, and check on held-out streams, as in [cross-validation](/cross-validation/).
- **Fitted numbers are not physics.** The coefficients absorb the capacitances, the delay model and the library corner of the characterization. Change the library, the supply voltage or the synthesis options and they must be fitted again.
- **Too many parameters.** Tables with many dimensions and regressions with many terms fit the training data well and generalize badly; see [overfitting](/overfitting/).
- **Averages of nonlinear models.** Evaluating a nonlinear model on average statistics is not the average of the per-cycle values (fact 2).
- **What the blocks do not cover.** Wires between blocks, the clock tree, the control logic and the glue logic made by synthesis are outside the block models and need their own estimates, often the largest error of the whole method.
- **Zero-delay characterization.** A characterization under zero delay misses glitches, which in arithmetic blocks can be a large part of the power.

## Exercises

1. Prove that the least-squares line with an intercept, fitted to pairs $(x_j, P_j)$, has the same mean as the data: $\frac{1}{m} \sum_j (c_0 + c_1 x_j) = \frac{1}{m} \sum_j P_j$.
2. Prove fact 1: for any function $g$, $E[(P - g(x))^2] \ge E[(P - E[P \mid x])^2]$.
3. In the 4-bit adder, explain why flipping bit 1 of an operand costs more on average than flipping bit 3. What is the longest chain of gates that one flip of bit 1 can make switch?
4. A table model $M(x)$ is concave in $x$. Show that $M(E[x]) \ge E[M(x)]$, and find an input distribution for the adder where the two differ by more than 2 transitions per cycle.
5. Take 16-bit two's complement words from a Gaussian source with a small variance, so that most high bits are sign bits. Explain why a model fitted on uniform random words overestimates the power of an adder on this source, and how the dual bit type method corrects it.

## References
