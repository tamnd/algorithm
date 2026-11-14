---
tag: D7CR16
kind: algorithm
slug: bdd-switching-activity-estimation
name: BDD-based switching activity estimation
aliases:
- Ghosh-Devadas-Keutzer-White estimation
- symbolic switching activity
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Ghosh, Devadas, Keutzer and White's exact estimate of average switching under zero or gate delays, built from BDDs of each node's transitions over two input vectors.
model: word-ram
complexity:
  vars: {G: the number of gates, P: the number of gate input pins, B: the largest number of nodes of a BDD built during the run, n: the number of primary inputs}
  time: {worst: "O(P B^2)", best: "O(P + n)"}
  space: {extra: "O(P B^2)"}
properties: {deterministic: true, exact: true, recursive: true, online: false}
history:
  year: 1992
  people: [Abhijit Ghosh, Srinivas Devadas, Kurt Keutzer, Jacob White]
  note: Ghosh, Devadas, Keutzer and White built Boolean functions for the transitions of each gate over two consecutive input vectors, with zero or general gate delays, and computed their probabilities with BDDs, so reconvergent fanout and glitches were handled exactly.
prereqs: [switching-activity, reduced-ordered-bdd, bdd-satisfy-count]
see_also: [signal-probability-propagation, transition-density, monte-carlo-power-estimation, glitch-power, shannon-expansion, bdd-apply, variable-ordering, inertial-and-transport-delay]
sources:
  - paper: doi:10.1109/DAC.1992.227826
    title: Abhijit Ghosh, Srinivas Devadas, Kurt Keutzer and Jacob White, Estimation of average switching activity in combinational and sequential circuits, Proceedings of the 29th ACM/IEEE Design Automation Conference, 253 to 259, 1992
    locator: the symbolic simulation of the circuit over two input vectors under zero and general delay models, and the BDD computation of the probabilities of the resulting transition functions
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the section on probabilistic techniques, which compares BDD-based methods with signal probability and transition density
  - paper: "Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677 to 691, 1986"
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677 to 691, August 1986
    locator: reduced ordered BDDs and the apply operation that the method uses
---

BDD-based switching activity estimation computes the exact expected number of transitions of every node of a combinational circuit in one clock cycle, given the joint law of each input's values in two consecutive cycles. It builds, with [reduced ordered BDDs](/reduced-ordered-bdd/), the Boolean function of the event "the node changes" over two copies of the inputs, one for the old vector and one for the new, and then sums the probabilities of the paths of that BDD, as in the weighted form of [BDD satisfy-count](/bdd-satisfy-count/). Ghosh, Devadas, Keutzer and White (1992) did this for zero delay and, by symbolic simulation over time steps, for general gate delays, so that glitches are counted too. The result is exact for any circuit, reconvergent fanout included, as long as the inputs are independent of each other. The price is the size of the BDDs, which can grow exponentially with the number of inputs.

## In plain words

To know how often a wire switches, ask a yes or no question about two clock cycles: is its value now different from its value before? That question is itself a logic function, of the old inputs and the new inputs.

A BDD stores a logic function as a decision graph and makes the chance that the function is true easy to compute: walk the graph once, weighting each branch by the chance of the input value it tests.

So the method builds, for each wire, the graph of the old value, the graph of the new value, and their XOR. The chance that the XOR is true is the switching activity. Nothing is guessed about how wires depend on each other, because the graphs keep the full logic.

## The problem

The input is a combinational circuit $C$ with primary inputs $x_1, \ldots, x_n$ and gates in topological order, and for each input $i$ a joint law $J_i(v, v') = P(x_i = v, x_i' = v')$ for $v, v' \in \{0, 1\}$, where $x_i$ is the value in one cycle and $x_i'$ the value in the next. The pairs $(x_i, x_i')$ of different inputs are independent; the two values of one input can be correlated, which is how the model expresses that an input changes rarely or often. Each node $y$ computes a Boolean function $f_y$, so its value is $f_y(x)$ in the first cycle and $f_y(x')$ in the second.

Under the zero-delay model a node changes at most once per cycle, and the output is the **switching activity**

$$ \alpha(y) \;=\; P\big(f_y(x) \ne f_y(x')\big) \;=\; P\big(f_y(x) \oplus f_y(x') = 1\big) $$

for every node $y$. Under a delay model with gate delays, the output is the expected number of transitions of $y$ in the cycle, glitches included.

## The algorithm

The BDDs use the variable order $x_1, x_1', x_2, x_2', \ldots, x_n, x_n'$, so the two copies of an input are next to each other. PAIR-PROB is a memoized traversal; a node of the BDD of $f$ that tests $x_i$ stands for a function of $x_i, x_i', \ldots, x_n, x_n'$ only.

```pseudo id=main
BDD-SWITCHING-ACTIVITY(C, J)
L1  for each primary input x_i do
L2      F[x_i] ← the BDD of the variable x_i; F'[x_i] ← the BDD of the variable x_i'
L3  for each gate y = kind(z_1, …, z_k) in topological order do
L4      F[y] ← kind(F[z_1], …, F[z_k]) and F'[y] ← kind(F'[z_1], …, F'[z_k]) by APPLY
L5      A ← F[y] XOR F'[y]
L6      α[y] ← PAIR-PROB(A, J)
L7  return α

PAIR-PROB(u, J)
L8  if u is a terminal then return its value (0 or 1)
L9  if u tests x_i then return Σ_{v, v'} J_i(v, v') · PAIR-PROB(u with x_i = v and x_i' = v', J)
L10 if u tests x_i' then return Σ_{v'} (J_i(0, v') + J_i(1, v')) · PAIR-PROB(u with x_i' = v', J)
```

At line L9 the cofactor "u with $x_i = v$ and $x_i' = v'$" is found by taking the $v$ child of $u$ and then, if that child tests $x_i'$, its $v'$ child; if it does not test $x_i'$, the function does not depend on $x_i'$ and the child itself is used. Line L10 handles a node whose function does not depend on $x_i$, with the marginal law of $x_i'$. Each BDD node is visited once, thanks to the memo.

For a delay model with integer gate delays, the same idea runs over time. The inputs change from $x$ to $x'$ at time 0, and the value of a gate with delay $d$ at time $t$ is the gate function of its fanins at time $t - d$. This *symbolic simulation* builds a BDD $F_t[y]$ for each node and each time step $t$ up to the latest arrival time. The expected number of transitions of $y$ is then $\sum_t \text{PAIR-PROB}(F_t[y] \oplus F_{t-1}[y], J)$.

## Example

Take $u = \mathrm{AND}(a, b)$, $v = \mathrm{AND}(a, c)$ and $y = \mathrm{OR}(u, v)$, so $y = a(b \lor c)$, the reconvergent circuit of [signal probability propagation](/signal-probability-propagation/).

**Fresh random vectors.** Let every input be a fresh fair coin in each cycle, so $J_i(v, v') = 1/4$ for all four pairs. Then $f_y(x)$ and $f_y(x')$ are independent with $P(y = 1) = 3/8$, and the algorithm returns $\alpha(y) = 2 \cdot \frac{3}{8} \cdot \frac{5}{8} = 15/32$. Propagating numbers by independence would give $P(y = 1) = 7/16$ and $\alpha(y) = 2 \cdot \frac{7}{16} \cdot \frac{9}{16} = 63/128$, which is wrong because of the reconvergence at $y$.

**Slowly changing inputs.** Let every input keep its value with probability $3/4$ and have $P = 1/2$, so $J_i(0, 0) = J_i(1, 1) = 3/8$ and $J_i(0, 1) = J_i(1, 0) = 1/8$. Each input switches in $1/4$ of the cycles, and the algorithm returns $\alpha(u) = \alpha(v) = 7/32$ and $\alpha(y) = 69/256 \approx 0.27$, compared with $15/32 \approx 0.47$ for fresh vectors. By hand: $P(y = y' = 1) = P(a = a' = 1) \cdot P(b \lor c = 1, b' \lor c' = 1) = \frac{3}{8} \cdot \frac{41}{64}$, so $P(y = 1, y' = 0) = \frac{3}{8} - \frac{123}{512} = \frac{69}{512}$, and $\alpha(y)$ is twice that. The BDD of $F[y] \oplus F'[y]$ in the order $a, a', b, b', c, c'$ has 13 internal nodes.

**Unequal delays.** With unit delay on every gate, both paths to $y$ have the same length and the symbolic simulation gives $15/32$ transitions per cycle for fresh vectors, the same as zero delay. If $v$ has delay 2, a change of $a$ can reach $y$ through $u$ one step before it arrives through $v$, and the result is $1/2$ transition per cycle: $1/32$ more, which is the expected number of glitch transitions.

## Correctness

Under the zero-delay model, a node changes in the cycle exactly when $f_y(x) \ne f_y(x')$, so $\alpha(y)$ is the probability that $A = F[y] \oplus F'[y]$ is 1. Lines L2 to L5 build the BDD of $A$ by [APPLY](/bdd-apply/), which is exact by induction over the gates.

PAIR-PROB returns $P(f_u = 1)$ for every BDD node $u$, by induction on the BDD from the terminals. For a node that tests $x_i$, the [Shannon expansion](/shannon-expansion/) on $x_i$ and then on $x_i'$ writes $f_u$ as a sum over the four values $(v, v')$ of the indicator of $(x_i, x_i') = (v, v')$ times a cofactor. Because of the variable order, each cofactor depends only on the pairs $(x_j, x_j')$ with $j > i$, which are independent of the pair $(x_i, x_i')$. So the probability of each term is $J_i(v, v')$ times the probability of the cofactor, and line L9 adds them. Line L10 is the same with only $x_i'$ present. For the delay model, the number of transitions of $y$ is $\sum_t [F_t[y] \ne F_{t-1}[y]]$, and the expectation of a sum is the sum of the probabilities, each computed exactly. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Let $B$ be the largest number of nodes of a BDD built during the run. APPLY on two BDDs of sizes $b_1$ and $b_2$ costs $O(b_1 b_2)$, a gate with $k$ inputs needs $k - 1$ APPLY calls for each copy and one XOR, and PAIR-PROB costs $O(B)$ with the memo. So the run costs $O(P B^2)$ time, and the unique table can hold that many nodes. When all BDDs stay small, as for a chain of gates in a good order, the cost is $O(P + n)$. In the worst case $B$ is exponential in $n$: a BDD over $2n$ variables can have about $2^{2n} / n$ nodes, and [multipliers need exponential BDDs](/multiplier-bdd-lower-bound/) in every order. Exact signal probability reduces to this problem: keep every input constant over the cycle, with $J_i(v, v) = P(x_i = v)$, add one input $t$ with $J_t(0, 1) = 1$, and the activity of $\mathrm{AND}(y, t)$ is $P(y = 1)$. Exact signal probability is #P-hard, so no exact method avoids such a cost in general unless every #P function is easy. The delay version multiplies the cost by the number of time steps.

## Properties

- **Exact.** For any circuit and any laws $J_i$, the result is the exact expected number of transitions under the stated delay model. Reconvergent fanout and the correlation between the two cycles of each input are handled.
- **Independence between inputs is still assumed.** Pairs of different inputs are independent. Correlated inputs need a joint model, for example a BDD or a Markov chain over the input vectors.
- **Temporal correlation of inputs.** With fresh independent vectors, $\alpha(y) = 2 P(y)(1 - P(y))$, so the activity follows from the signal probability. With correlated $J_i$ it does not, and the full pair model is needed.
- **Glitches need the delay model.** The zero-delay result counts at most one transition per node per cycle. The symbolic simulation counts every transition that transport delay passes; it does not filter short pulses as inertial delay would.
- **Order matters.** The size of the BDDs, and so the cost, depends on the [variable order](/variable-ordering/). Keeping $x_i$ and $x_i'$ adjacent keeps the XOR of the two copies small; putting all old variables before all new ones can make it large.

## Variants and improvements

- **Sequential circuits.** In a finite state machine, the present-state lines are not independent inputs. The paper of Ghosh et al. (1992) also treats sequential circuits. There the state lines need the probabilities of the states, which are the [stationary distribution](/stationary-distribution/) of the state [Markov chain](/markov-chain/), and the next-state logic gives the pairs of consecutive states.
- **Partitioning.** For a circuit too large for global BDDs, build BDDs over cut points, use independence across the cuts, and accept an approximation at the cuts.
- **Probabilistic simulation.** Track at each node the probabilities of the four transition types 0 to 0, 0 to 1, 1 to 0 and 1 to 1 under independence, gate by gate. This is fast and approximate, like [transition density](/transition-density/).
- **Inertial filtering.** Remove pulses shorter than the gate delay from the symbolic waveforms, to model [inertial delay](/inertial-and-transport-delay/).
- **Sampling.** When the BDDs are too large, estimate by [Monte Carlo power estimation](/monte-carlo-power-estimation/), which has no size limit but gives only an interval.

## When to use it

Use it when an exact activity is needed for a circuit or a cone whose BDDs fit in memory: to check faster estimators, for control logic with few inputs, or for the parts of a design whose input statistics are known and strongly correlated in time. For large datapaths such as multipliers the BDDs explode, and simulation is the practical choice.

## Pitfalls

- **Wrong order.** An order with all $x$ before all $x'$ often blows up the XOR of the two copies. Interleave them.
- **Mismatched marginals.** In steady state the law of $x_i$ and the law of $x_i'$ should be the same. A $J_i$ whose marginals differ describes a single cycle, not an average over many cycles.
- **Zero delay is not real power.** The zero-delay activity misses glitches, which can be a large part of the power in arithmetic circuits, see [glitch power](/glitch-power/).
- **Exact under the model only.** The result is exact for the stated input laws and delay model. If the inputs are correlated with each other, or the delays are not the integer delays of the model, the error of the model remains.

## Implementations

## History

Ghosh, Devadas, Keutzer and White presented the method at the 1992 Design Automation Conference. They wrote, for each gate, the Boolean conditions under which it switches between two input vectors, under zero delay and under a general delay model by symbolic simulation, and evaluated the probabilities of these conditions with BDDs. This handled the reconvergent fanout that broke earlier propagation methods, and it covered sequential circuits through state probabilities. The method was one of the probabilistic techniques compared in Najm's 1994 survey, where its strength (exact results) and its weakness (BDD size) were already clear.

## References
