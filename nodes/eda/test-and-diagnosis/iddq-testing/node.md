---
tag: MDQQDT
kind: technique
slug: iddq-testing
name: IDDQ testing
aliases:
- quiescent current testing
area: eda/test-and-diagnosis
level: core
summary: Measures the quiescent supply current of a CMOS chip after each vector, since a bridge or leak raises it far above the near-zero current of a good circuit.
prereqs: [bridging-fault-model, stuck-at-fault-model]
see_also: [cell-aware-test, leakage-power, set-cover, greedy-set-cover, fault-coverage, n-detect-test, williams-brown-defect-level, static-test-compaction]
sources:
  - paper: "J. M. Soden, C. F. Hawkins, R. K. Gulati and W. Mao, IDDQ testing: a review, Journal of Electronic Testing: Theory and Applications 3(4), 291 to 303, 1992"
    title: "J. M. Soden, C. F. Hawkins, R. K. Gulati and W. Mao, IDDQ testing: a review, Journal of Electronic Testing: Theory and Applications 3(4), 291 to 303, 1992"
    locator: the review of the method, the defects that raise the quiescent current, and the choice of measurement vectors
  - paper: "T. W. Williams, R. H. Dennard, R. Kapur, M. R. Mercer and W. Maly, IDDQ test: sensitivity analysis of scaling, Proceedings of the IEEE International Test Conference, 786 to 792, 1996"
    title: "T. W. Williams, R. H. Dennard, R. Kapur, M. R. Mercer and W. Maly, IDDQ test: sensitivity analysis of scaling, Proceedings of the IEEE International Test Conference, 786 to 792, 1996"
    locator: how the background leakage grows with scaling and reduces the margin between good and defective currents
  - paper: "E. J. McCluskey and C.-W. Tseng, Stuck-fault tests vs. actual defects, Proceedings of the IEEE International Test Conference, 336 to 343, 2000"
    title: E. J. McCluskey and C.-W. Tseng, Stuck-fault tests vs. actual defects, Proceedings of the IEEE International Test Conference, 336 to 343, 2000
    locator: the comparison, on test chips, of stuck-fault test sets with the defects actually found
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on IDDQ testing
---

IDDQ testing finds defects in a CMOS chip by measuring its supply current instead of its outputs. After a test vector is applied and the logic has settled, a good static CMOS circuit has no path from the supply VDD to ground, so it draws only a small leakage current, the quiescent current $I_{DDQ}$. A short between two nets that are driven to opposite values, a gate-oxide short, or a transistor that is always on creates such a path, and the current rises. The tester compares the current with a threshold. A vector only has to put the defect into a state where current flows: the effect does not have to travel to an output. This page proves when a vector activates a bridge, shows that IDDQ catches resistive bridges that no static logic test sees, gives a lower bound on the number of measurement vectors, and explains why the growing leakage of small transistors limits the method.

## In plain words

A good CMOS gate connects its output either to the supply or to ground, never to both, once the inputs have stopped changing. So a good chip at rest draws almost no current. If two wires are shorted and one is driven high and the other low, current flows from the supply through the short to ground.

The tester applies a vector, waits until the chip is quiet, and measures the current. A large current means a defect. It does not matter whether the outputs are right. The cost is time: a current measurement is much slower than a logic test, so only a few vectors are measured.

## When it applies

- Static CMOS logic, in which no good state of the circuit has a path from the supply to ground. Pull-up resistors, analog blocks, some memory circuits and dynamic logic draw current on purpose and must be turned off or kept out of the measurement.
- The background leakage of the whole chip is small compared with the current that a defect adds, and its spread from chip to chip is small enough to set a threshold between them.
- Defects that change the current more than the logic: resistive bridges, gate-oxide shorts, transistors that leak or are always on. Many of these pass logic tests and fail later in the field.

## The template

```pseudo id=main
IDDQ-TEST(chip, T, θ)
L1  for each vector v in the measurement set T
L2      apply v
L3      wait until the switching current has died down
L4      measure the supply current I(v)
L5      if I(v) > θ then return fail
L6  return pass
```

The holes are the measurement set $T$, chosen in advance by fault simulation from a larger logic test set, the wait at line L3, and the threshold $\theta$. In the variants below, line L5 compares the current with values derived from the other measurements of the same chip instead of a fixed number.

**The model.** Take a combinational circuit of static CMOS gates, with nets as on the [bridging fault model](/bridging-fault-model/) page. In a good circuit at rest, each driver connects its net to exactly one rail. A bridge between nets $x$ and $y$ is non-feedback if neither net is in the fanout cone of the other. The model assumes that a bridge draws current exactly when its two drivers connect it to different rails, and that the current then exceeds $\theta$ together with the background. Whether the second part holds is a question of resistances and leakage, treated below.

**When a vector activates a bridge.** Claim: a vector $v$ activates a non-feedback bridge $\{x, y\}$ exactly when $x(v) \ne y(v)$ in the good circuit. Proof: the drivers of $x$ and $y$ take their inputs from nets outside the fanout cones of $x$ and $y$, since the bridge is non-feedback, so the bridge does not change those inputs, and the drivers produce the good values $x(v)$ and $y(v)$. If the values differ, one driver connects the bridge to VDD and the other to ground, so current flows. If they are equal, both connect it to the same rail, and no path from VDD to ground passes through the bridge. Compare with logic detection: the bridging fault model page proves that a vector detects the wired-AND bridge only if $x(v) \ne y(v)$ and, in addition, the error reaches an output, and the wired-OR case is the same with 0 and 1 exchanged. So every vector that detects a non-feedback wired-AND or wired-OR bridge by logic also activates it for IDDQ, and IDDQ needs no propagation.

**Resistive bridges.** Let the bridge have resistance $R_b$, and let $x$ be driven high through a pull-up of resistance $R_p$ while $y$ is driven low through a pull-down of resistance $R_n$, all linear resistors. The current through the bridge is $V_{DD} / (R_p + R_b + R_n)$, which is positive for every finite $R_b$. The voltage of $x$ is $V_{DD} (R_b + R_n)/(R_p + R_b + R_n)$, which falls below $V_{DD}/2$ exactly when $R_b < R_p - R_n$. The voltage of $y$ is $V_{DD} R_n/(R_p + R_b + R_n)$, which rises above $V_{DD}/2$ exactly when $R_b < R_n - R_p$. So, with gate switching thresholds at $V_{DD}/2$, the bridge can give a static logic error only when $R_b < |R_p - R_n|$, while it draws current for every $R_b$. A bridge whose resistance is larger than the difference of the driver strengths is invisible to a static logic test and visible to IDDQ as long as its current stands out from the background. The resistances and the threshold of $V_{DD}/2$ are model choices; real gates have different thresholds, which the bridging fault model page discusses.

**How many vectors.** For a set $T$ of vectors, the signature of a net is the string of its values over $T$. By the claim above, $T$ activates every bridge of a list exactly when every listed pair of nets has different signatures. If $m$ nets must be pairwise different, for example $m$ primary inputs with every pair on the list, their $m$ signatures are distinct strings of length $|T|$, so $2^{|T|} \ge m$ and $|T| \ge \lceil \log_2 m \rceil$. For primary inputs the bound is reached: give the inputs distinct binary codes of length $\lceil \log_2 m \rceil$. So a logarithmic number of vectors can activate a quadratic number of bridges, which is why a few current measurements go a long way. Choosing a smallest measurement set from given vectors is a [set cover](/set-cover/) problem, with the bridges as elements, and tools solve it with [greedy set cover](/greedy-set-cover/) or by fault simulation in vector order.

**Example.** Take $z = ab$ and $y = c + d$ with outputs $z$ and $y$, the circuit of the [N-detect](/n-detect-test/) example. It has 11 non-feedback pairs of nets. The 4 inputs are pairwise on the list, so $|T| \ge 2$. The two vectors $abcd = 0101$ and $1100$ give the signatures $a = 01$, $b = 11$, $c = 00$, $d = 10$, $z = 01$, $y = 10$, and every one of the 11 pairs differs (the equal pairs $a, z$ and $d, y$ are fanout pairs, not on the list). So 2 measurements activate all 11 bridges. By logic, the wired-AND bridge of $a$ and $b$ has no test at all, since it leaves $z = ab$ unchanged, and the wired-AND bridge of $b$ and $c$ has 4 tests out of 16 vectors, while 8 vectors activate it for IDDQ. A short that never changes the logic can still be a reliability risk, and only the current shows it.

**Why leakage limits it.** The background current is the sum of the off-state leakage of all transistors, and its main part is subthreshold current, which, as on the [leakage power](/leakage-power/) page, falls by a factor of 10 for every $S = n v_T \ln 10$ of gate voltage below the threshold voltage $V_T$. Here $v_T \approx 25.9$ mV is the thermal voltage at 300 K and $n \ge 1$ is a slope factor fitted to the device, so $S$ is at least about 60 mV per decade, and values near 70 to 100 mV per decade are typical. Each step down in $V_T$ by $S$ multiplies the leakage per transistor by 10, and the number of transistors grows with each process generation. To see the effect, take an illustrative chip, not a measured one, with $10^7$ transistors that are off, and a bridge current of 100 µA. With 1 pA of leakage per transistor the background is 10 µA, and the bridge raises the current by a factor of 11. With 1 nA per transistor the background is 10 mA, and the bridge adds 1 percent, less than the spread of the background from chip to chip that comes from the variation of $V_T$. Williams and coauthors analysed this loss of margin under scaling. It makes a single fixed threshold hard to use as leakage grows, and it is the reason for the variants below.

**Measured, not proved.** These numbers come from toy inputs, not from benchmark circuits. With `random.Random(11)`, 100 random circuits of 4 or 5 inputs and 4 to 8 gates, there were 3063 non-feedback pairs of nets, of which 3035 have different functions and so can be activated. Of the 6126 wired-AND and wired-OR bridges on the same pairs, 5810 are detectable by logic. Exact minimum sets, by exhaustive search, needed 307 vectors in total to activate all activatable bridges and 481 to detect all detectable bridges by logic. The IDDQ minimum was at most the logic minimum in 99 of the 100 circuits. In the other one it was larger, which by the claim can only come from pairs whose bridges logic cannot detect at all: every logic test set already activates every pair with a logic-detectable bridge. In every circuit, every vector that detected a bridge by logic also activated it, as the claim proves.

**Cost.** A logic vector is applied and checked at the speed of the tester. A current measurement must wait at line L3 until the switching current has settled to the quiescent level, which is far longer. So IDDQ measures a small set $T$ chosen from the logic test set, and the choice of $T$ is the algorithmic part of the method.

## Classic examples

- **Bridges and gate-oxide shorts.** The review of Soden, Hawkins, Gulati and Mao covers the defects that raise the quiescent current and how the measurement vectors are chosen.
- **Reliability screening.** Parts with a raised current but correct outputs are often rejected because the defect may grow in use. This is a policy choice, not a proof that the part would fail.
- **Test-chip experiments.** McCluskey and Tseng compared stuck-fault tests with the defects actually found on test chips. Such experiments, not proofs, are how the value of IDDQ and of other extra tests is measured.

## Variations

- **Delta IDDQ.** Compare the current of each vector with the currents of the other vectors on the same chip. A defect raises some vectors and not others, while the background raises all, so differences separate them better than a fixed threshold.
- **Current ratios and signatures.** Use the ratio of the largest to the smallest current of a chip, or the sorted list of its currents, as the test statistic, so that the decision scales with the leakage of that chip.
- **Built-in current sensors.** Sensors on the chip measure the current of one block at a time. The background of a small block is smaller, so the margin is better, at a cost in area and supply drop.
- **Low temperature and reverse body bias.** Subthreshold leakage falls with temperature and with a higher threshold voltage, so testing cold or with body bias makes the background smaller.

## Pitfalls

- **Static current by design.** Any circuit that draws current at rest, such as a pull-up, a bias circuit or a floating bus, raises the background for every vector. Turn it off in test mode or the measurement means nothing.
- **Waiting too little at line L3.** If the switching current has not died down, good chips read high and fail.
- **One threshold for all chips.** Background leakage varies with process, temperature and supply. A threshold that is safe for the leakiest good chips lets defective low-leakage chips pass. Report escapes and rejected good chips together.
- **Equating raised current with failure.** A raised current proves a path from supply to ground, not a wrong output. Whether to reject such a part is a quality decision.

## Exercises

1. In the example circuit, show that no single vector activates all 11 bridges, and find all pairs of vectors that do.
2. Prove that a bridge between two nets with the same Boolean function can never be activated, and that a bridge between a net and its complement is activated by every vector.
3. For $m = 5$ primary inputs with every pair on the bridge list, give 3 vectors that activate all 10 bridges.
4. In the resistive model, find the largest $R_b$ for which the bridge current exceeds a margin $\Delta$ above the background, and compare it with the bound $|R_p - R_n|$ for a logic error.

## References
