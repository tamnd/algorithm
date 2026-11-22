---
tag: NV7DCA
kind: algorithm
slug: differential-power-analysis
name: Differential power analysis
aliases:
- DPA
- Kocher DPA
area: security-and-privacy/side-channel-attacks
level: core
summary: "Splits many power traces by a predicted intermediate bit under each key guess, and takes the guess whose difference of means shows a peak."
model: real-ram
complexity:
  vars: {m: the number of traces, T: the number of samples in each trace, g: the number of key guesses}
  time: {worst: Θ(g m T), average: Θ(g m T), best: Θ(g m T)}
  space: {extra: Θ(g + T)}
history:
  year: 1999
  people: [Paul Kocher, Joshua Jaffe, Benjamin Jun]
  note: "Kocher, Jaffe and Jun published differential power analysis at CRYPTO 1999 and used it to recover DES keys from the power consumption of smart cards."
prereqs: [side-channel-attack, hamming-weight, s-box]
see_also: [correlation-power-analysis, simple-power-analysis, template-attack, boolean-masking, test-vector-leakage-assessment, welch-t-test, timing-attack, data-encryption-standard]
sources:
  - paper: "Paul Kocher, Joshua Jaffe and Benjamin Jun, Differential power analysis, CRYPTO 1999, LNCS 1666, pages 388 to 397"
    locator: "the sections on DPA (the selection function on one bit of a DES S-box output, and the difference of the two mean traces)"
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 6, Differential Power Analysis, pages 119 to 165 (the attack, the leakage models and the number of traces)"
  - paper: doi:10.1109/TC.2002.1004593
    title: "Thomas S. Messerges, Ezzat A. Dabbish and Robert H. Sloan, Examining smart-card security under the threat of power analysis attacks, IEEE Transactions on Computers 51(5), 2002"
    locator: the signal to noise model of DPA and the multiple-bit attack
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the examples of this page)
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the definitions of the success rate and the guessing entropy
---

Differential power analysis (DPA) finds a key from many power traces of a device that uses the key. For each key guess, it splits the traces into two groups by one bit of an intermediate value that the guess predicts, and it subtracts the mean trace of one group from the mean trace of the other. Under the right guess the split follows the real data, so the difference shows a peak; under a wrong guess the split is close to random and the difference is close to zero. Kocher, Jaffe and Jun (1999) used it against DES on smart cards, and it is the reason why [masking](/boolean-masking/) exists.

## In plain words

A chip uses more power when more of its wires carry a one. The attacker cannot read the wires, but can record the power many times while the chip encrypts known inputs. Take one guess for a small part of the key. With that guess, you can compute one bit of a value inside the chip for each input. Put the recordings where that bit is one in a pile, and the others in a second pile. Average each pile and compare the averages. If the guess is right, the piles really differ in that bit, and the averages differ at the moment the chip handles it. If the guess is wrong, the piles are mixed, and the averages are almost the same. Do this for every guess and keep the guess with the largest difference.

## The problem

The attacker sees $m$ pairs $(p_i, \ell_i)$. Here $p_i$ is a known input nibble and $\ell_i$ is a trace of $T$ real samples. The device holds a fixed key nibble $k$. The page uses the stated leakage model of the area:

$$\ell_i[j^\ast] = \varepsilon \cdot \mathrm{HW}(S(p_i \oplus k)) + N_{ij^\ast}, \qquad \ell_i[j] = N_{ij} \ \text{for } j \ne j^\ast,$$

where $S$ is the 4-bit S-box of PRESENT, $\mathrm{HW}$ is the [Hamming weight](/hamming-weight/), $\varepsilon > 0$ is the leakage per bit, the noise values $N_{ij}$ are independent with law $N(0, \sigma^2)$, and the inputs $p_i$ are independent and uniform. The sample $j^\ast$ is not known to the attacker. The goal is to output $k$. The cost model is the [real RAM](/real-ram/): each addition, division and comparison of two reals costs one unit.

This is a non-profiled attack: the attacker has no copy of the device to learn from, and needs only a guess of what leaks.

## The algorithm

The selection function is bit $b$ of $S(p \oplus g)$. The page uses $b = 1$, for the reason given in the pitfalls.

```pseudo id=main
DPA(traces (p_1, l_1) .. (p_m, l_m), S-box S, bit b)    ▷ each l_i has T samples
L1  best ← none, top ← -∞
L2  for each key guess g = 0 .. |S| - 1 do
L3      for each trace (p, l) do
L4          if bit b of S(p ⊕ g) is 1 then add l to group G1
L5          else add l to group G0
L6      if G1 or G0 is empty then score(g) ← -∞
L7      else Δ ← mean(G1) - mean(G0)               ▷ the differential trace, T values
L8           score(g) ← max over j of Δ[j]
L9      if score(g) > top then
L10         best ← g, top ← score(g)
L11 return best and the list of scores
```

Lines L3 to L5 keep, for each group, a running sum of the traces and a count, so a group never holds the traces themselves. Line L7 divides each sum by its count, sample by sample. Line L8 takes the largest value of the differential trace. It does not take the absolute value: in this model a right guess gives a positive peak, and the sign is part of the signal. Line L9 uses a strict test, so the first guess with the top score wins.

## Example

Take $k = \texttt{B}$ (hex), $\varepsilon = 1$, no noise, one sample in each trace, and each of the 16 inputs once. The table gives the value in the device and its bit 1.

| p | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S(p ⊕ B) | 8 | F | E | 3 | 2 | 1 | 7 | 4 | B | 6 | 5 | C | D | A | 0 | 9 |
| trace value (HW) | 1 | 4 | 3 | 2 | 1 | 1 | 3 | 1 | 3 | 2 | 2 | 2 | 3 | 2 | 0 | 2 |
| bit 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

Under the right guess $g = \texttt{B}$, group G1 holds the inputs 1, 2, 3, 4, 6, 8, 9 and D, with mean $20/8 = 2.5$. Group G0 has mean $12/8 = 1.5$. The score is $1.0$. The other scores are:

| guess | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| score | 0.75 | 0 | 0.25 | -0.25 | 0 | 0.5 | -1.0 | -0.25 | -0.5 | 0.25 | 0 | **1.0** | -0.25 | -1.25 | 0.75 | 0 |

The right guess wins by $0.25$. The guesses 0 and E are its closest rivals. The guess D has the largest absolute value, $1.25$, but with the wrong sign. With noise, the margin of $0.25 \varepsilon$ is what the averages must resolve.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/): after guess $g$, the value top is the largest score of the guesses $0 \ldots g$, and best is the first guess with that score. So line L11 returns the first argmax of the scores. The attack is also consistent in the model: as $m$ grows, by the [law of large numbers](/law-of-large-numbers/), the score of a guess $g$ tends to $\varepsilon \cdot D_b(g \oplus k)$, where $D_b(\delta)$ is the expected difference of $\mathrm{HW}(S(X))$ between the two groups of bit $b$ of $S(X \oplus \delta)$. The samples with noise only tend to 0. For $b = 1$ and the PRESENT S-box, $D_1(0) = 1$ and $D_1(\delta) \le 0.75$ for every $\delta \ne 0$, so the right key wins with a probability that tends to 1. This is a theorem in the stated model. The [proof](proofs/correctness.md) gives both parts in full.

## Complexity

For each of the $g$ guesses, lines L3 to L5 add each of the $m$ traces of $T$ samples to one running sum, which costs $\Theta(mT)$. Lines L7 and L8 cost $\Theta(T)$. So the time is $\Theta(g m T)$ in every case, and the extra space is $\Theta(T)$ for the two sums and $\Theta(g)$ for the list of scores. For a 4-bit S-box, $g = 16$.

The number of traces that the attack needs depends on the noise. In the model, the variance of the leaking sample inside one group is $\varepsilon^2 \cdot 3/4 + \sigma^2$, because the three other bits of $S(p \oplus k)$ still vary. The difference of two group means of about $m/2$ traces each has a standard deviation of about $2\sqrt{(0.75\varepsilon^2 + \sigma^2)/m}$, and it must resolve the margin $0.25\varepsilon$. So the number of traces grows as $\sigma^2/\varepsilon^2$. A measurement in the model, with 200 seeded runs for each cell, $\varepsilon = 1$, one sample in each trace and a random key in each run:

| traces m | 50 | 100 | 200 | 400 | 800 | 1600 |
|---|---|---|---|---|---|---|
| success rate, σ = 0.5 | 0.69 | 0.79 | 0.90 | 0.975 | 1.0 | 1.0 |
| success rate, σ = 1 | 0.555 | 0.705 | 0.76 | 0.925 | 0.985 | 1.0 |

The success rate is the probability that the best guess is the key, as defined by Standaert, Malkin and Yung (2009).

## Properties

- **Non-profiled.** It needs the inputs (or the outputs) and a selection function, but no model of the exact power of the device.
- **First order.** It works on the mean of each group at one sample. If each intermediate value is split into random shares, as in [Boolean masking](/boolean-masking/), the mean of each group at each sample is the same for every key, and the attack fails. A higher-order attack that combines samples is then necessary.
- **One bit at a time.** Only one bit of the intermediate value sets the groups. The other bits act as noise, so the attack uses the signal less well than [correlation power analysis](/correlation-power-analysis/), which uses all bits.
- **Divide and conquer.** Each key nibble or byte is found on its own, so the work is a sum and not a product over the parts of the key.
- **Deterministic.** For fixed traces, the result does not depend on any random choice.

## Variants and improvements

- **Multiple-bit DPA.** Messerges, Dabbish and Sloan (2002) set the groups by several bits at a time, for example all bits one against all bits zero, and showed that this raises the signal to noise ratio.
- **Correlation instead of two groups.** [Correlation power analysis](/correlation-power-analysis/) replaces the two groups by the Pearson correlation with the Hamming weight of the whole value. It uses all bits of the value, so in the Hamming weight model it gets a larger signal from the same traces.
- **Mutual information.** [Mutual information analysis](/mutual-information-analysis/) needs no linear relation between the model and the power.
- **Profiling.** With a copy of the device, a [template attack](/template-attack/) learns the full distribution of the traces for each value. With exact templates its maximum likelihood decision has the highest success rate of all attacks on the same traces (a theorem).
- **Precomputed classes.** Sum the traces for each of the 16 input values once, in $\Theta(mT)$ time. Then each guess combines 16 class sums, and the total time becomes $\Theta(mT + 16 g T)$.
- **Key rank instead of the top guess.** Keep the full list of scores and give it to [key rank estimation](/side-channel-key-rank-estimation/), which tells how much search remains after a partial success.

## When to use it

DPA is the simplest attack that shows whether a device leaks in a way that depends on the data, and it is the standard first example in a course or in a design review. For a real evaluation, use [CPA](/correlation-power-analysis/) when the leakage is close to the Hamming weight, a [template attack](/template-attack/) when a profiling device exists, and a [leakage test](/test-vector-leakage-assessment/) when the question is only "does it leak", with no key recovery.

## Pitfalls

- **Taking the absolute value.** If line L8 is score(g) ← max over j of |Δ[j]|, then on bit 1 of the PRESENT S-box the guess $k \oplus 6$ scores $1.25$ and beats the right key, which scores $1$. This happens with no noise at all, so more traces do not help. Keep line L8 signed, as above, when the sign of the leakage is known.
- **A bad selection bit.** On bit 0, three wrong guesses tie with the right one at $D_0 = 1$, even with the signed score, so line L4 with $b = 0$ cannot tell them apart. Compute the table $D_b(\delta)$ of the S-box first and choose a bit where the right guess wins by a margin, as $b = 1$ does here.
- **A bit of the S-box input.** If line L4 tests bit $b$ of $p \oplus g$ instead of bit $b$ of $S(p \oplus g)$, the split depends on only one bit of $g$, and 8 guesses give the same groups. The selection function must pass through the nonlinear S-box.
- **An empty group.** With few traces, a group can be empty for some guess, and line L7 then divides by zero. Line L6 gives that guess the score $-\infty$.

## Implementations

The code of this page is an abstract model on synthetic data. Its traces come from the leakage model of "The problem", drawn with a seeded `random.Random` by the function `simulate_traces`; the code never reads a device, a file or a clock. The tests check the example above, the exact table $D_b$ for every key and bit, the agreement with a direct difference of means on 500 random inputs, and the success rate with noise.

## History

Kocher, Jaffe and Jun described simple and differential power analysis in a paper at CRYPTO 1999 and showed DES keys recovered from smart cards with a selection function on one S-box output bit. Messerges, Dabbish and Sloan studied the signal to noise ratio of the attack and its multiple-bit form (2002). Brier, Clavier and Olivier replaced the difference of means by a correlation with a leakage model (2004). The countermeasures of the same years, masking (Chari, Jutla, Rao and Rohatgi 1999; Goubin and Patarin 1999), were made to remove exactly the first-order difference that DPA measures.

## References
