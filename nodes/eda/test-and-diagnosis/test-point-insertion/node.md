---
tag: W3SQNB
kind: technique
slug: test-point-insertion
name: Test point insertion
aliases:
- control and observation point insertion
area: eda/test-and-diagnosis
level: advanced
summary: Adds control points that force lines and observation points that expose them, placed by testability analysis, so random BIST patterns reach high fault coverage.
prereqs: [cop-testability-measure, built-in-self-test]
see_also: [scoap, fault-coverage, weighted-random-pattern-testing, scan-design, fault-simulation, linear-feedback-shift-register, static-timing-analysis, automatic-test-pattern-generation]
sources:
  - paper: "J. P. Hayes and A. D. Friedman, Test point placement to simplify fault detection, IEEE Transactions on Computers C-23(7), 727 to 735, 1974"
    title: J. P. Hayes and A. D. Friedman, Test point placement to simplify fault detection, IEEE Transactions on Computers C-23(7), 727 to 735, 1974
    locator: the selection of an optimal set of test points in fanout-free networks by branch and bound, to reduce the number of tests
  - paper: doi:10.1145/37888.38000
    title: B. Krishnamurthy, A dynamic programming approach to the test point insertion problem, Proceedings of the 24th Design Automation Conference, 1987
    locator: the dynamic program over a fanout-free circuit that places test points to optimize a random-pattern testability measure
  - paper: "N. A. Touba and E. J. McCluskey, Test point insertion based on path tracing, Proceedings of the IEEE VLSI Test Symposium, 2 to 8, 1996"
    title: N. A. Touba and E. J. McCluskey, Test point insertion based on path tracing, Proceedings of the IEEE VLSI Test Symposium, 2 to 8, 1996
    locator: finding the faults that resist random patterns by fault simulation and placing control points by tracing paths from them
  - paper: "Franc Brglez, On testability analysis of combinational networks, Proceedings of the IEEE International Symposium on Circuits and Systems (ISCAS), vol. 1, 221 to 225, 1984"
    title: F. Brglez, On testability analysis of combinational networks, Proc. ISCAS 1984, vol. 1, 221 to 225
    locator: the COP controllability and observability probabilities that guide where test points go
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on built-in self-test (random pattern resistant faults and test points)
---

Test point insertion changes a circuit so that random patterns test it well. Some faults are detected by only a tiny fraction of the input vectors, for example a stuck-at 0 at the output of a wide AND gate, which needs every input to be 1. Pseudo-random patterns from a [built-in self-test](/built-in-self-test/) generator then need a very long test to hit them. A **control point** is an extra gate that, in test mode, forces a line toward 0 or 1 more often. An **observation point** is an extra output, usually an extra scan cell or an input of the response compactor, that makes a line visible. A testability measure such as [COP](/cop-testability-measure/) estimates the detection probability of every fault, and the method places a few points where they raise the lowest probabilities the most. This page proves that observation points never hurt, shows with exact numbers that control points can, and gives the greedy method that tools use.

## In plain words

Some faults are like a lock with many tumblers: only one key in thousands opens it, and random keys rarely work. You can change the lock. You can add a window that lets you see a part deep inside, so you no longer need the whole key to reach the end. Or you can add a lever that holds some tumblers in place half the time, so fewer must line up by chance.

The window is an observation point. It only adds a way to see, so it never makes anything harder. The lever is a control point. It helps the faults behind it, but while it holds a line, it also hides what happens on that line, so it can make other faults harder. The method picks a few windows and levers that help the most.

## When it applies

- The circuit is tested by random or pseudo-random patterns: logic BIST with an [LFSR](/linear-feedback-shift-register/) generator, or a design that wants fewer deterministic patterns. With full [scan](/scan-design/), the logic between scan cells is combinational.
- A fault list, usually stuck-at faults, has **random pattern resistant** faults, whose detection probability under uniform random vectors is too low for the planned test length.
- The design can afford a few extra gates and scan cells, and a little delay on the lines that get control points.
- In functional mode the test points must do nothing: a control point is held at its neutral value and an observation point only adds a load.

A **control-1 point** on line $\ell$ replaces $\ell$ by $\ell \lor t$, and a **control-0 point** replaces it by $\ell \land \lnot t$. The signal $t$ is 0 in functional mode, and random in test mode, usually 1 with probability $1/2$ or less. An **observation point** adds $\ell$ as an extra output.

## The template

For a fault $f$, let $p_f$ be its detection probability under uniform random vectors. With COP, $p_f = C(\ell) \cdot O(\ell)$ for $\ell/0$ and $(1 - C(\ell)) \cdot O(\ell)$ for $\ell/1$, in the notation of the COP page.

```pseudo id=main
TEST-POINT-INSERTION(C, budget k, threshold θ)
L1  compute C(ℓ) and O(ℓ) for every line ℓ
L2  H ← the faults with estimated detection probability below θ
L3  while H is not empty and fewer than k points are placed
L4      for each candidate point (line ℓ, type observe, control-0 or control-1)
L5          gain ← the drop in Σ over f in H of a cost such as 1/p_f, with C and O recomputed near ℓ
L6      insert the candidate with the largest gain
L7      recompute C and O, and recompute H
L8  return the changed circuit
```

The holes are the measure at line L1, the cost at line L5 and the set of candidates at line L4. COP is cheap, linear in the circuit size, but inexact under reconvergent fanout. Fault simulation of a sample of random vectors gives better estimates at a higher cost. The cost $1/p_f$ is the expected number of random vectors to detect $f$, so the sum estimates how long the hard faults keep the test going.

**Test length.** If a fault has detection probability $p$ and the vectors are independent and uniform, $L$ vectors miss it with probability $(1 - p)^L$. To detect it with probability at least $1 - \varepsilon$ needs
$$L \ \ge\ \frac{\ln(1/\varepsilon)}{-\ln(1 - p)} \ \approx\ \frac{\ln(1/\varepsilon)}{p}$$
vectors. For $\varepsilon = 0.01$ this is 1177 vectors at $p = 1/256$, 276 at $p = 17/1024$ and 72 at $p = 1/16$. Halving the lowest $p$ doubles the test, so test points aim at the minimum.

**Why an observation point never hurts.** Adding $\ell$ as an output leaves every old output and every line value unchanged, for the good circuit and for every faulty one. A vector that detected a fault made some old output differ, and it still does. So the detection set of every old fault can only grow, and so can its probability. The new branches of $\ell$ add a few new faults, but no old fault gets harder.

**Why a control point can hurt.** A control-1 point makes $\ell \lor t$ equal to 1 whenever $t = 1$, whatever $\ell$ is. A fault whose effect must pass through $\ell$ is then blocked on those vectors. So the control point raises the probability that $\ell$ is 1, which helps faults that need $\ell = 1$ to propagate, and lowers the observability of $\ell$ itself, which hurts faults in the cone of $\ell$. The example below shows both effects.

**Example.** Take an 8-input AND built as $g_1 = a_1 a_2 a_3 a_4$, $g_2 = a_5 a_6 a_7 a_8$ and $z = g_1 g_2$, with the output $z$. It has 11 lines and 22 stuck-at faults. Every fault except $z$/1 needs all 8 inputs fixed: $a_1$/0 needs all ones, and $a_1$/1 needs $a_1 = 0$ and the other seven at 1. So 21 faults have $p = 1/256$. The circuit is fanout-free, so the COP values are exact here, as proved on the COP page. The table gives the exact detection probabilities, found by enumerating all input vectors, with each $t_i$ uniform:

| test points | lines | faults | $a_1$/0 | $a_5$/0 | $a_1$/1 | $z$/0 | lowest $p$ | faults with $p < 1/50$ |
|---|---|---|---|---|---|---|---|---|
| none | 11 | 22 | 1/256 | 1/256 | 1/256 | 1/256 | 1/256 | 19 |
| observe $g_1$ and $g_2$ | 15 | 30 | 1/16 | 1/16 | 1/16 | 1/256 | 1/256 | 3 |
| control-1 on $g_2$ | 13 | 26 | 17/512 | 1/512 | 17/512 | 17/512 | 1/512 | 9 |
| control-1 on $g_2$, observe $g_2$ | 15 | 30 | 17/512 | 1/16 | 17/512 | 17/512 | 1/512 | 1 |
| control-1 on $g_1$ and $g_2$, observe both | 19 | 38 | 1/16 | 1/16 | 1/16 | 289/1024 | 17/1024 | 2 |

The observation points split the problem: a fault inside $g_1$ now needs only 4 inputs, so $p = 1/16$, but $z$/0 still needs all 8. The control point on $g_2$ (the gate $c_2 = g_2 \lor t_2$) helps the faults of $g_1$: $a_1$/0 needs $g_1 = 1$ and $c_2 = 1$, so $p = \frac{1}{16} \cdot \left(\frac12 + \frac12 \cdot \frac1{16}\right) = \frac{17}{512}$. It hurts the faults of $g_2$: $a_5$/0 now also needs $t_2 = 0$, so $p = \frac{1}{16} \cdot \frac{1}{2} \cdot \frac{1}{16} = \frac{1}{512}$, half of what it was. An observation point on $g_2$ repairs that. The last row has two control points and two observation points. Its two hardest faults are the stuck-at 0 faults on the branches from $g_i$ into the control gate $c_i$, at $p = \frac{1}{16} \cdot \frac{1}{2} \cdot \frac{17}{32} = \frac{17}{1024}$. The test length for 99% confidence on the hardest fault drops from 1177 vectors to 276.

**Cost.** Line L1 takes $O(L + P)$ time for $L$ lines and $P$ gate input pins. A naive loop tries $3L$ candidates and recomputes the measure for each, so it takes $O(k L (L + P))$ time for $k$ points. Tools recompute only the fanout cone of the candidate for controllability and the fanin cone for observability, and they keep only candidates near the hard faults. Fault simulation instead of COP multiplies the cost by the number of sample vectors.

## Classic examples

- **Hayes and Friedman (1974).** Test points in fanout-free networks, chosen by branch and bound to reduce the number of tests that a deterministic test set needs.
- **Krishnamurthy (1987).** A dynamic program over a fanout-free circuit that places test points for random-pattern testability. A dynamic program fits because, in a tree, two subtrees interact only through the gate that joins them.
- **Touba and McCluskey (1996).** Fault simulation finds the faults that random patterns miss, and paths traced from each such fault give sets of control points that would make it detectable. Points are then chosen to serve many of these faults at once.
- **Logic BIST flows.** Logic BIST flows insert observation points and control points before scan stitching, guided by a COP-like measure, so that the planned number of pseudo-random patterns reaches the target coverage.

## Variations

- **Observation points only.** They never hurt any fault and add no delay on functional paths, only a load, so some flows use only them.
- **Control point probability.** Driving $t$ with probability $1/4$ or $1/8$ instead of $1/2$ blocks the line less often and still raises its controllability.
- **Shared drivers.** Several control points share one $t$ signal, or an observation point XORs several lines into one scan cell, to save area. This adds correlation, which COP does not model.
- **Test points for compression.** Test points can also reduce the number of deterministic patterns from [ATPG](/automatic-test-pattern-generation/) and their care bits, which helps test compression.
- **Weighted patterns instead.** [Weighted random patterns](/weighted-random-pattern-testing/) bias the inputs instead of changing the circuit. They need no extra logic but cannot reach a line whose hardness comes from conflicts between inputs.

## Pitfalls

- **Control points on critical paths.** The extra gate adds delay. Use [static timing analysis](/static-timing-analysis/) to exclude lines on critical paths from the candidates.
- **Trusting COP under reconvergence.** COP is inexact when fanout reconverges, as the COP page proves, and it can point to the wrong lines. Check the result by [fault simulation](/fault-simulation/) of real pseudo-random patterns.
- **Control points that hide faults.** A control point lowers the observability of its own line and of the faults behind it, as the example shows. Pair it with an observation point or score both effects at line L5.
- **Greedy is not optimal.** The points interact, so the best single point at each step need not give the best set. Exact methods exist only for fanout-free circuits.
- **Counting new faults.** Test points add lines and so faults of their own. Coverage must be counted on the new fault list, or the new faults must be excluded on purpose.

## Exercises

1. In the example with control-1 points on $g_1$ and $g_2$ and no observation points, compute the detection probability of $a_1$/0 and of $z$/0 by hand.
2. A control point can hurt even a fault whose effect never reaches the controlled line. Give a small circuit and such a fault whose detection probability a control-1 point lowers. (Hint: let the controlled line be a side input of an OR gate on the path of the fault.)
3. For a 16-input AND built as four 4-input AND gates feeding one 4-input AND gate, find the fewest observation points that make every fault on the 16 inputs detectable with probability at least $1/16$, and prove that fewer do not suffice.

## References
