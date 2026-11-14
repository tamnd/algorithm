---
tag: FCFFCV
kind: technique
slug: weighted-random-pattern-testing
name: Weighted random pattern testing
aliases:
- weighted random patterns
- biased random testing
area: eda/test-and-diagnosis
level: advanced
summary: Gives each input its own probability of 1, computed from the circuit, so random-pattern-resistant faults such as wide AND gates are detected in fewer patterns.
prereqs: [built-in-self-test, cop-testability-measure]
see_also: [test-point-insertion, lfsr-reseeding, fault-simulation, union-bound, geometric-distribution, linear-feedback-shift-register, fault-coverage, automatic-test-pattern-generation]
sources:
  - paper: "H. D. Schnurmann, E. Lindbloom and R. G. Carpenter, The weighted random test-pattern generator, IEEE Transactions on Computers C-24(7), 695 to 700, 1975"
    title: H. D. Schnurmann, E. Lindbloom and R. G. Carpenter, The weighted random test-pattern generator, IEEE Transactions on Computers C-24(7), 695 to 700, 1975
    locator: random test patterns in which each input is 1 with its own probability, chosen from the circuit
  - paper: "J. A. Waicukauski, E. Lindbloom, E. B. Eichelberger and O. P. Forlenza, A method for generating weighted random test patterns, IBM Journal of Research and Development 33(2), 149 to 161, 1989"
    title: J. A. Waicukauski, E. Lindbloom, E. B. Eichelberger and O. P. Forlenza, A method for generating weighted random test patterns, IBM Journal of Research and Development 33(2), 149 to 161, 1989
    locator: the computation of input weights for the faults left by random patterns, several weight sets, and the use of the method in production test
  - book: isbn:9780471624639
    title: Paul H. Bardell, William H. McAnney and Jacob Savir, Built-In Test for VLSI, Pseudorandom Techniques, Wiley-Interscience, 1987
    locator: the chapters on random pattern testability and test length (detection probabilities, test length for a set of faults, and weighted patterns)
---

Weighted random pattern testing draws test patterns at random, but sets each input to 1 with its own probability $p_i$, its weight, instead of $1/2$. Some faults are random-pattern resistant: with uniform patterns they need a rare input combination, such as all 16 inputs of an AND gate at 1, and are detected only once in tens of thousands of patterns. A weight close to the needed value makes such a combination common. Schnurmann, Lindbloom and Carpenter (1975) proposed weighted random test pattern generation, and Waicukauski, Lindbloom, Eichelberger and Forlenza (1989) computed the weights from the faults that random patterns leave and used several weight sets per circuit. The method keeps the cheap generation and fault simulation of random patterns, and it works best when the hard faults agree on which way each input should lean.

## In plain words

Random tests are like flipping a fair coin for each input. Some faults are only seen when 16 coins all land heads, which happens about once in 65,000 tries. If we bend the coins so that each lands heads 15 times out of 16, that same event happens about once in three tries.

But bent coins hurt other faults. A fault that needs one particular input to be tails, and all the others heads, is now seen about once in 42 tries, which is still far better than before. A fault that needs many tails becomes very rare. So the bend is chosen from the circuit, and when faults pull in different directions, we use a few different sets of bends in turn.

## When it applies

- The circuit has random-pattern resistant faults: wide AND or OR gates, decoders, comparators, or long chains of gates that all need one value. A [built-in self-test](/built-in-self-test/) with uniform patterns then stalls below the target [fault coverage](/fault-coverage/).
- The patterns are generated on chip or by the tester from a few parameters, so storing deterministic patterns is not wanted.
- The hard faults can be grouped so that, within a group, each input has a preferred value. A group whose faults need opposite values on the same input needs its own weight set.

## The template

```pseudo id=main
WEIGHTED-RANDOM-TEST(C, the fault list F, the patterns per set N)
L1  apply N uniform random patterns and drop the faults they detect
L2  while hard faults remain in F and the budget allows do
L3      compute one weight p_i for each input from the remaining faults
L4      for k ← 1 to N do
L5          draw each input i as 1 with probability p_i, independently
L6          fault simulate the pattern and drop the faults it detects
L7  return the weight sets and the faults left undetected
```

The holes are the weight computation of line L3, the rounding of each $p_i$ to a value the hardware can make, the number of patterns per set, and the stopping rule. Line L6 is ordinary [fault simulation](/fault-simulation/) with fault dropping.

**Computing weights.** Two kinds of methods fill line L3.

- From probabilities: estimate the detection probability of each remaining fault as a function of the weights, with a measure such as [COP](/cop-testability-measure/), and adjust the weights to raise the smallest or the sum of the detection probabilities.
- From tests: generate deterministic test cubes for the remaining faults with [ATPG](/automatic-test-pattern-generation/), and set $p_i$ from the fraction of cubes that need input $i$ at 1 among those that care about it. This is the spirit of the 1989 IBM method.

**Test length for a set of faults.** If fault $f$ is detected by one random pattern with probability $P_f$ and the patterns are independent, the number of patterns until $f$ is detected is [geometric](/geometric-distribution/) with mean $1/P_f$, and $N$ patterns miss it with probability $(1 - P_f)^N$. By the [union bound](/union-bound/), $N$ patterns detect every fault of a set $F$ with probability at least $1 - \varepsilon$ when
$$\sum_{f \in F} (1 - P_f)^N \le \varepsilon, \quad \text{which holds for } N \ge \frac{\ln(|F| / \varepsilon)}{-\ln(1 - P_{\min})}.$$
So the test length grows like $1 / P_{\min}$, the inverse of the hardest detection probability, which is what weights improve.

**The wide AND gate.** Take one AND gate with $n$ inputs and the same weight $p$ on every input. The fault "input $i$ stuck at 1" needs input $i$ at 0 and all others at 1, so $P = (1 - p) p^{n-1}$. The output stuck at 0 needs all inputs at 1, $P = p^n$, and the output stuck at 1 needs some input at 0, $P = 1 - p^n$. The input stuck-at-0 faults are equivalent to the output stuck at 0.

- The value $(1 - p) p^{n-1}$ is largest at $p = 1 - 1/n$. Its derivative is $p^{n-2}\big((n - 1) - n p\big)$, positive below $1 - 1/n$ and negative above. The largest value is $\frac{1}{n}(1 - \frac{1}{n})^{n-1} > \frac{1}{e n}$, since $(1 - 1/n)^{n-1} > 1/e$ for $n \ge 2$. Uniform patterns give $2^{-n}$. $\blacksquare$
- For $n = 16$: with $p = 1/2$ each input fault has $P = 2^{-16} \approx 1.5 \cdot 10^{-5}$, and by the bound above, $487{,}479$ patterns are needed to detect all 18 faults with probability $0.99$. With $p = 15/16$ the input faults have $P = 0.02374$, the output faults $0.3561$ and $0.6439$, and 308 patterns suffice for the same guarantee.

**When one weight set cannot work.** Add an OR gate on the same 16 inputs. Its fault "input $i$ stuck at 0" needs input $i$ at 1 and all others at 0, so $P'_i = p_i \prod_{j \ne i} (1 - p_j)$, while the AND fault on the same input has $P_i = (1 - p_i) \prod_{j \ne i} p_j$. For any weights, $P_i P'_i = \prod_{j} p_j (1 - p_j) \le 4^{-16}$, since $p(1 - p) \le 1/4$. So $\min(P_i, P'_i) \le 2^{-16}$: no single weight set beats uniform patterns on this circuit. Two weight sets, $15/16$ for half the patterns and $1/16$ for the other half, give each of these 32 input faults $P = 0.0119$ per pattern, and the output faults more. $\blacksquare$

## Classic examples

- **Wide gates and decoders.** The AND gate above is the standard case: a weight near 1 on its inputs raises the hardest detection probability from $2^{-n}$ to about $1/(e n)$.
- **IBM production test.** Waicukauski, Lindbloom, Eichelberger and Forlenza (1989) computed weights for the faults left by uniform patterns and applied several weight sets in turn, reaching high coverage of large scan designs with random patterns generated by the tester.
- **Weighted BIST.** In [built-in self-test](/built-in-self-test/), weights of the form $k / 2^r$ come from a few [LFSR](/linear-feedback-shift-register/) bits: the OR of 4 independent bits is 1 with probability $15/16$, and the AND of 4 bits with probability $1/16$. A small multiplexer per scan input chooses the weight set.
- **Against test points and reseeding.** [Test point insertion](/test-point-insertion/) changes the circuit so uniform patterns work, and [LFSR reseeding](/lfsr-reseeding/) stores a seed per hard cube. Weights change neither the circuit nor store cubes, but need weight hardware and may need many weight sets.

## Variations

- **Several weight sets.** Group the hard faults by the values they need, compute one weight set per group, and run each for a share of the patterns. The OR and AND example needs two groups.
- **Weights per scan cell.** With scan, the weight must follow the cell that the bit is shifted into, so the weight hardware changes with the shift cycle, or the chains are built so that cells of similar weight are neighbors.
- **Optimizing the weights.** Treat the expected test length $\sum_f (1 - P_f)^N$, with $P_f$ from a testability measure, as a function of the weights and lower it by local search.
- **Rounding.** Hardware weights are usually limited to a few values such as $1/16$, $1/8$, $1/2$, $7/8$ and $15/16$. Rounding the optimal weights to these costs little when the detection probabilities change slowly near the optimum.
- **Mixed with deterministic patterns.** Faults that no weight set handles are left to stored patterns or seeds.

## Pitfalls

- **One weight set for opposite needs.** Faults that need input $i$ at 1 and faults that need it at 0 cannot both gain, as the AND and OR example proves. Look for such conflicts in line L3 and split the faults into groups.
- **Trusting the probability estimates.** Measures like COP assume independent signals, which fails at reconvergent fan-out, so a computed $P_f$ can be far off. Line L6 measures the real coverage; base the stopping rule on it, not on the estimates.
- **Weights near 0 or 1 starve other faults.** With $p = 15/16$ on 16 inputs, a fault that needs four inputs at 0 is detected with probability below $10^{-4}$. Keep uniform patterns or other sets for those faults.
- **Ignoring correlation in the generator.** Weights from neighbor LFSR stages are not independent, and shifted copies feed neighbor scan cells. Build the weight logic from bits that are far apart, or through a phase shifter.
- **Counting patterns, not test time.** Each weight set adds setup and its own fault simulation. A few long sets are often cheaper than many short ones.

## Exercises

1. For an $n$-input OR gate, find the weight that maximizes the smallest detection probability of its single stuck-at faults, and its value for $n = 16$.
2. Show that $\frac{1}{n}(1 - \frac{1}{n})^{n-1}$ decreases with $n$ and tends to $\frac{1}{e n}$ in ratio.
3. Prove that the test length bound $N \ge \ln(|F| / \varepsilon) / (-\ln(1 - P_{\min}))$ implies $\sum_f (1 - P_f)^N \le \varepsilon$.
4. A circuit has an AND gate of 8 inputs and an AND gate of 8 other inputs, with their outputs feeding a 2-input OR gate. Compute the detection probability of an input stuck-at-1 fault of the first AND gate with uniform patterns and with weight $7/8$ on all inputs.

## References
