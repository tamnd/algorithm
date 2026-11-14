---
tag: Z81JVX
kind: technique
slug: scoap
name: SCOAP testability measures
aliases:
- SCOAP
- Sandia controllability observability analysis
area: eda/timing-and-verification
level: core
summary: Goldstein's counts of how hard it is to set each line to 0 or 1 and to observe it at an output, used to guide test generation and test point insertion.
prereqs: [stuck-at-fault-model, boolean-circuit]
see_also: [podem, d-algorithm, automatic-test-pattern-generation, scan-design, built-in-self-test, arrival-and-required-time, observability-dont-care]
sources:
  - paper: doi:10.1109/TCS.1979.1084687
    title: L. H. Goldstein, Controllability/observability analysis of digital circuits, IEEE Transactions on Circuits and Systems 26(9), 685 to 693, 1979
    locator: the six measures, combinational and sequential controllability to 0 and to 1 and observability, and their rules for gates and flip-flops
  - paper: doi:10.1145/800139.804528
    title: L. H. Goldstein and E. L. Thigpen, SCOAP, Sandia controllability/observability analysis program, Proceedings of the 17th Design Automation Conference, 190 to 196, 1980
    locator: the program that computes the measures on gate-level circuits
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Testability Measures (SCOAP controllability and observability, sequential measures), and the use of the measures in the chapter Combinational Circuit Test Generation
---

SCOAP, from Goldstein (1979), gives each line $\ell$ of a gate-level circuit three numbers: $CC0(\ell)$ and $CC1(\ell)$, the cost of setting $\ell$ to 0 or to 1 from the primary inputs, and $CO(\ell)$, the cost of carrying the value of $\ell$ to a primary output. The cost counts the lines that must be set on the way, so a large number marks a line that is hard to control or to observe. All three numbers come from one forward pass and one backward pass over the circuit, in $O(L + P)$ time for $L$ lines and $P$ gate input pins. They are estimates, not exact counts: they treat the branches of a fanout stem as independent, so they can be finite for a value that no input can produce. This is an EDA page, for test of digital circuits under the [stuck-at fault model](/stuck-at-fault-model/). Test generators such as [PODEM](/podem/) use the numbers to order their choices, and test engineers use them to find lines that need test points or [scan](/scan-design/).

## In plain words

A test generator often has to pick one of several gate inputs to work on. A good pick saves a lot of search. SCOAP gives it a cheap guess.

Each wire gets three numbers. One says how hard it is to make the wire 0, one says how hard it is to make it 1, and one says how hard it is to see the wire at an output.

An input pin costs 1 to set. An AND gate gives 0 if any input is 0, so its 0 cost is the cheapest input plus 1. It gives 1 only if all inputs are 1, so its 1 cost is the sum plus 1. To see one input of an AND gate at its output, the other inputs must be 1, so their costs add on.

The numbers are fast to compute. They are guesses, not exact counts.

## When it applies

- A test generator such as [PODEM](/podem/) or the [D-algorithm](/d-algorithm/) makes choices whose order changes the speed of the search but not its result. Good guesses about which input is easy to set, and which gate is easy to observe, cut the backtracks.
- Before test generation, a designer wants a list of lines that are hard to control or to observe, to add control points, observation points or [scan](/scan-design/) flip-flops there.
- The circuit is large, and exact measures cost too much. Exact measures are hard: the tests of the fault $z$/0 on an output $z$ are exactly the inputs that satisfy $z$, so counting the tests of a fault is as hard as counting the satisfying inputs of a circuit, which is #P-hard. SCOAP takes linear time.

The page uses the single stuck-at fault model. The faulty circuit of $\ell/v$ has the line $\ell$ fixed to $v$, and a test must set $\ell$ to $\lnot v$ and make some output depend on $\ell$. So the usual SCOAP cost of the fault $\ell$/0 is $CC1(\ell) + CO(\ell)$, and the cost of $\ell$/1 is $CC0(\ell) + CO(\ell)$.

## The template

Each net that feeds two or more places is a stem with one branch per place, as on the [stuck-at fault model](/stuck-at-fault-model/) page. Every other line is a primary input or a gate output.

```pseudo id=main
SCOAP(C)
L1  for each line ℓ of C in topological order do
L2      if ℓ is a primary input then CC0(ℓ) ← 1; CC1(ℓ) ← 1
L3      else if ℓ is a branch of the stem s then CC0(ℓ) ← CC0(s); CC1(ℓ) ← CC1(s)
L4      else (CC0(ℓ), CC1(ℓ)) ← CTRL(the gate of ℓ, CC0 and CC1 of its inputs)
L5  for each line ℓ of C do CO(ℓ) ← ∞
L6  for each primary output ℓ of C do CO(ℓ) ← 0
L7  for each line ℓ of C in reverse topological order do
L8      if ℓ is a stem then CO(ℓ) ← min(CO(ℓ), the CO of each branch of ℓ)
L9      else if ℓ is the input i of a gate with output y then CO(ℓ) ← OBS(the gate, i, CO(y), CC0 and CC1 of the other inputs)
L10 return CC0, CC1, CO
```

The holes are the gate rules CTRL and OBS. For a gate with output $y$ and inputs $i_1, \ldots, i_r$:

| gate | $CC0(y)$ | $CC1(y)$ | OBS: $CO(i_k)$ |
|---|---|---|---|
| AND | $\min_j CC0(i_j) + 1$ | $\sum_j CC1(i_j) + 1$ | $CO(y) + \sum_{j \ne k} CC1(i_j) + 1$ |
| NAND | $\sum_j CC1(i_j) + 1$ | $\min_j CC0(i_j) + 1$ | $CO(y) + \sum_{j \ne k} CC1(i_j) + 1$ |
| OR | $\sum_j CC0(i_j) + 1$ | $\min_j CC1(i_j) + 1$ | $CO(y) + \sum_{j \ne k} CC0(i_j) + 1$ |
| NOR | $\min_j CC1(i_j) + 1$ | $\sum_j CC0(i_j) + 1$ | $CO(y) + \sum_{j \ne k} CC0(i_j) + 1$ |
| NOT | $CC1(i_1) + 1$ | $CC0(i_1) + 1$ | $CO(y) + 1$ |
| BUF | $CC0(i_1) + 1$ | $CC1(i_1) + 1$ | $CO(y) + 1$ |
| XOR of $a, b$ | $\min(CC0(a) + CC0(b), CC1(a) + CC1(b)) + 1$ | $\min(CC0(a) + CC1(b), CC1(a) + CC0(b)) + 1$ | $CO(y) + \min(CC0, CC1)$ of the other input $+ 1$ |

The rule for a gate with a controlling value reads the same way each time. One input at the controlling value fixes the output, so that output value costs the cheapest such input. The other output value needs every input at the non-controlling value, so it costs the sum. To observe one input, every other input must hold the non-controlling value. An XOR with more than two inputs is a chain of two-input XOR gates, or a small dynamic program over the parity of the inputs seen so far. A fanout branch costs nothing more than its stem, and a stem is as easy to observe as its easiest branch.

**Cost.** Lines L1 to L4 visit each line once and each input pin once, and so do lines L7 to L9. The whole computation takes $O(L + P)$ time and $O(L)$ space. It has the shape of [arrival and required times](/arrival-and-required-time/) in static timing: controllability flows forward from the inputs like an arrival time, and observability flows backward from the outputs like a required time.

**What the numbers mean.** Unfold the circuit into a tree: for each stem, give each branch its own copy of the cone of logic that drives the stem, with its own copies of the primary inputs. In the tree, call a set of lines a justification of $\ell = v$ when it holds $\ell$, and for each gate output $y$ in the set with its value, either one input at a controlling value or all inputs at values that force $y$, recursively down to primary inputs. Count primary inputs and gate outputs, not branches. Then $CCv(\ell)$ is the fewest lines in a justification of $\ell = v$ in the tree. Proof by induction in topological order: a primary input justifies itself with one line. For an AND output $y = 0$, one input at 0 is enough and the cheapest choice costs $\min_j CC0(i_j)$ lines, plus $y$ itself. For $y = 1$, all inputs must be 1, the input cones of the tree are disjoint, so the smallest union is the sum of the smallest parts, plus $y$. The other gates are the same up to inversion, and the XOR rule takes the cheaper of the two ways to get each parity. In the same way, $CO(\ell)$ is the fewest lines that must be set to carry $\ell$ along one path to an output in the tree: one per gate on the path, plus a justification of the non-controlling value on each side input. In a fanout-free circuit the tree is the circuit, so the numbers are exact there. With fanout, the copies of a stem must agree in the real circuit, and SCOAP does not see this.

**Example.** Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$.

| line | $CC0$ | $CC1$ | $CO$ | how |
|---|---|---|---|---|
| $a, b, c, b_g, b_h$ | 1 | 1 | 5 | inputs and branches; $CO(a) = CO(g) + CC1(b_g) + 1$ |
| $g$ | 3 | 2 | 3 | $CC0(g) = CC1(a) + CC1(b_g) + 1$, $CC1(g) = \min(CC0(a), CC0(b_g)) + 1$, $CO(g) = CO(z) + CC1(h) + 1$ |
| $h$ | 3 | 2 | 3 | the same as $g$ |
| $z$ | 5 | 4 | 0 | $CC0(z) = CC1(g) + CC1(h) + 1$, $CC1(z) = \min(CC0(g), CC0(h)) + 1$ |

The fault costs follow. The fault $z$/0 costs $CC1(z) + CO(z) = 4$, and it has 3 tests of the 8 vectors: 011, 110 and 111. The faults $g$/0 and $h$/0 cost 5, and each has 5 tests. Every input and branch fault costs 6. Most of them have 1 or 2 tests, so the ranking is right in the large, but $b$/0 also costs 6 and has 3 tests, as many as $z$/0. In [PODEM](/podem/), the objective $h = 1$ for the fault $h$/0 needs one input of $h$ at 0, so the backtrace takes the input with the smaller $CC0$. Here both inputs cost 1, and the tie is broken by order.

On the c17 benchmark circuit, the same computation gives controllabilities of at most 5, and the largest observability, 7, is on the input 6 and on the branch of the input 3 into gate 11. These two lines are the hardest to observe, since their value must pass three NAND gates, each with a side input to set.

## Classic examples

- [PODEM](/podem/): when one input of a gate is enough to give the wanted value, the backtrace takes the input that is easiest to set. When all inputs need the value, it takes the hardest one first, so that a conflict shows up early. The D-frontier gate with the smallest $CO$ is propagated first.
- [D-algorithm](/d-algorithm/): the same guides order the choice of the D-frontier gate and of the way to justify each J-frontier line.
- Test point insertion: a line with a large $CC0$ or $CC1$ gets a control point, a gate that a test mode can force, and a line with a large $CO$ gets an observation point, an extra output or a scan cell. The [built-in self-test](/built-in-self-test/) page shows why random patterns need this.
- Partial [scan design](/scan-design/): the sequential measures point to flip-flops that are hard to set or to observe, which are good candidates for scan.
- [Static timing analysis](/static-timing-analysis/) uses the same two passes in topological order, with delays in place of costs.

## Variations

- **Sequential measures.** Goldstein defines three more numbers, $SC0$, $SC1$ and $SO$, that count clock cycles instead of lines. A combinational gate adds 0 to them and a flip-flop adds 1, while the combinational numbers pass through the flip-flop. For a D flip-flop with a free clock and no reset, $CC1(Q) = CC1(D)$ and $SC1(Q) = SC1(D) + 1$, and in the same way $SO(D) = SO(Q) + 1$. Goldstein's rules add terms for the clock and for set and reset inputs. With feedback loops the equations have no topological order, so they are solved by repeated passes from $\infty$ until no value changes, as in [Bellman-Ford](/bellman-ford/). A value that stays $\infty$ marks a line that no sequence of inputs can set or observe.
- **Probability measures.** Replace costs by the probability that a line is 1 under uniform random inputs, and the probability that a change on the line reaches an output. These measures, of which COP is a common one, predict how well random patterns test a circuit, and they use the same two passes with products in place of sums. They also assume independent branches.
- **Weighted costs.** Some tools count a cost per gate type or per transistor, or add a depth term, in place of the unit cost of 1 per gate.
- **Exact measures.** The number of tests of each fault, or its exact detection probability, can be computed with BDDs or with model counting on small circuits. The cost is exponential in the worst case, as shown above.

## Pitfalls

- **Reconvergent fanout counts twice.** For $x = ab$, $y = ac$, $z = xy$, SCOAP gives $CC1(z) = 3 + 3 + 1 = 7$, but $z = 1$ needs exactly $a = b = c = 1$, three inputs and two gates. The cone of $a$ is counted once for $x$ and once for $y$.
- **A finite number does not mean that the value is possible.** For $z = \mathrm{AND}(a, \lnot a)$, SCOAP gives $CC1(z) = 1 + 2 + 1 = 4$, but $z$ is 0 on every input. For the circuit $z = ab + \bar{a}c + bc$ on the [ATPG](/automatic-test-pattern-generation/) page, the redundant fault $r$/0 on the gate $r = bc$ costs $CC1(r) + CO(r) = 3 + 5 = 8$, but it has no test. In a combinational circuit every SCOAP number is finite, so SCOAP never proves that a fault is redundant.
- **A cost is not a count of tests.** In the example, $a$/0 and $b$/0 both cost 6, but $a$/0 has one test and $b$/0 has three. Use the numbers to order choices, not to predict coverage or test length.
- **Stem and branches.** The observability of a stem is the minimum over its branches, not the sum. The controllability of a branch is that of its stem, with no added 1. Treating a stem like a gate input changes all the numbers behind it.
- **XOR gates.** XOR has no controlling value. To observe one input, the other input may hold either value, so the side cost is $\min(CC0, CC1)$ of the other input. Using $CC1$ there, as for AND, gives costs that are too high.
- **Comparing circuits.** The numbers grow with the depth and the width of the logic, and they have no unit outside the circuit. Compare lines of one circuit, not numbers across circuits.

## Exercises

1. Compute the SCOAP numbers of c17, with gates 10 = NAND(1, 3), 11 = NAND(3, 6), 16 = NAND(2, 11), 19 = NAND(11, 7), 22 = NAND(10, 16) and 23 = NAND(16, 19), and check that the largest observability is 7, on input 6 and on the branch of 3 into 11.
2. Prove that in a fanout-free circuit of AND, OR, NAND, NOR, NOT and BUF gates, $CC1(\ell)$ is the smallest number of lines in a justification of $\ell = 1$.
3. Give an $r$-input AND gate the inputs $x_1, \ldots, x_r$. Show that $CC1$ of the output is $r + 1$ and that the probability of 1 under random inputs is $2^{-r}$. Which of the two numbers predicts the test length of the output stuck at 0 under random patterns?
4. Find a circuit with two faults $f$ and $g$ such that $f$ has the smaller SCOAP cost and fewer tests than $g$.

## References
