---
tag: 67C0ZW
kind: concept
slug: soft-error-masking
name: Soft error masking
aliases:
- logical masking
- electrical masking
- latching-window masking
area: eda/power-reliability-and-manufacturability
level: advanced
summary: The three effects that stop a particle-induced pulse from becoming an error, namely no sensitized path, attenuation along the path, and missing the latch window.
prereqs: [signal-probability-propagation, static-timing-analysis]
see_also: [fault-simulation, stuck-at-fault-model, glitch-power, bdd-switching-activity-estimation, monte-carlo-integration, black-equation]
sources:
  - paper: "Premkishore Shivakumar, Michael Kistler, Stephen W. Keckler, Doug Burger and Lorenzo Alvisi, Modeling the effect of technology trends on the soft error rate of combinational logic, International Conference on Dependable Systems and Networks (DSN), 389 to 398, 2002"
    title: Premkishore Shivakumar, Michael Kistler, Stephen W. Keckler, Doug Burger and Lorenzo Alvisi, Modeling the effect of technology trends on the soft error rate of combinational logic, Proceedings of the International Conference on Dependable Systems and Networks, 389 to 398, 2002
    locator: the three masking effects of combinational logic, the model of the soft error rate with each of them, and the projection that the soft error rate of logic per chip grows with technology scaling and deeper pipelines
  - paper: doi:10.1109/TDMR.2005.853449
    title: Robert C. Baumann, Radiation-induced soft errors in advanced semiconductor technologies, IEEE Transactions on Device and Materials Reliability 5(3), 305 to 316, 2005
    locator: the sources of soft errors (alpha particles, high-energy neutrons, thermal neutrons and boron-10), the charge collection at a struck node, the critical charge, and the scaling trends of memory and logic
---

A *soft error* is a wrong value in a chip caused by a particle strike, without damage to the hardware. A strike on a node of combinational logic makes a short voltage pulse, a *single event transient*. Most such pulses never become an error, because three effects can stop them on their way to a storage element. This page states the three effects, shows how they combine into the probability that a strike causes an observed error, and says when the common product formula is exact and when it is only an approximation.

## In plain words

A particle from space or from the chip's own package can hit a transistor and leave a small electric charge on a wire. For a short moment the wire carries a wrong value.

That wrong value matters only if it reaches a flip-flop, which stores values at each tick of the clock, and is stored there. Three things can stop it on the way.

First, the logic may block it. An AND gate whose other input is 0 gives 0, whatever this input does.

Second, the pulse may fade. Each gate on the path is a little slow, and a very short pulse gets shorter or weaker at every gate until it disappears.

Third, the timing may be wrong. A flip-flop looks at its input only during a short moment around the clock tick. A pulse that comes before or after that moment is ignored.

## The idea

**The source.** An ionizing particle crossing a junction frees charge, and part of it is collected at the struck node. If the collected charge exceeds the node's *critical charge*, the node's value flips for a time set by the charge and the drive strength of the gate that holds the node. In a storage cell the flip can stay, a single event upset. In logic, the driver restores the value and the result is a pulse of some width $w_0$. The rate of strikes depends on the particle flux (alpha particles from package materials, neutrons from cosmic rays and thermal neutrons that react with boron-10) and on the sensitive area.

**Three masks.** For a pulse that starts at node $n$ to become an observed error, three events must all happen.

- $L$: there is a *sensitized path* from $n$ to a flip-flop input. Every gate on the path has its side inputs at non-controlling values, so a change at $n$ changes the flip-flop input. This depends on the input vector of that cycle.
- $E$: the pulse arrives at the flip-flop input with enough height and width. Each gate filters the pulse like a low-pass filter. A pulse much wider than the gate delay passes almost unchanged, and a pulse narrower than the gate delay is attenuated and can vanish.
- $W$: the pulse is present at the flip-flop input for the whole setup and hold window around a clock edge, so the flip-flop stores the wrong value.

**The product, and what it needs.** The observed error event is the intersection $L \cap E \cap W$. By the chain rule of probability, exactly,

$$ P(\text{error} \mid \text{strike at } n) = P(L)\; P(E \mid L)\; P(W \mid L \cap E). $$

This is a product of three numbers, one per mask, and it is exact with no assumption. The common formula $P(L)\, P(E)\, P(W)$, where each factor is computed on its own, needs more. It is exact if the three events are independent, which is an assumption about the circuit and the workload, not a fact. It fails when the sensitized path decides how many gates the pulse goes through, so that $E$ depends on which path $L$ opened, and when the width that survives $E$ decides the chance of $W$. The example below shows such a case.

**The latch window.** Let the clock period be $T$, the setup time $t_s$ and the hold time $t_h$, and let the pulse of width $w$ arrive at a time uniformly distributed over one period, independently of the clock. The flip-flop captures the wrong value if the pulse covers the whole interval from $t_s$ before the clock edge to $t_h$ after it. If the pulse starts at $a$ and the edge is at $c$, this needs $a \le c - t_s$ and $a + w \ge c + t_h$. That is an interval of start times of length $w - t_s - t_h$, so

$$ P(W \mid \text{width } w) = \frac{(w - t_s - t_h)^+}{T}, \qquad w \le T + t_s + t_h . $$

A pulse that only overlaps the window can make the flip-flop metastable or capture the wrong value. A conservative model counts every overlap, which gives the larger value $(w + t_s + t_h)/T$. Both models show that a shorter clock period raises the latch probability: faster designs catch more pulses.

**Rates.** The soft error rate of a circuit sums over nodes the strike rate times the probability of an observed error. It is usually given in FIT, failures per $10^9$ device-hours. Shivakumar and coauthors used a model of all three masks to project the soft error rate of combinational logic. They found that the masks become weaker as technology scales and pipelines get deeper: pulses are wider relative to gate delays, paths have fewer gates, and clock periods are shorter. They projected that the logic soft error rate per chip would grow to be comparable to that of unprotected memory.

## Examples

**Logic only.** A pulse at one input of a 2-input AND gate passes if the other input is 1. If that input is 1 with probability 1/2, $P(L) = 1/2$. Through three AND gates in series whose side inputs are independent and each 1 with probability 1/2, $P(L) = 1/8$. Signal probabilities like these come from [signal probability propagation](/signal-probability-propagation/), which also assumes independence of the inputs.

**Latch window.** With $T = 400$ ps and $t_s + t_h = 20$ ps, a 60 ps pulse is captured with probability $40/400 = 0.10$ by the containment model and $80/400 = 0.20$ by the overlap model. A 15 ps pulse has probability 0 by containment and $35/400 \approx 0.09$ by overlap.

**When the product of separate masks is wrong.** A strike at node $s$ makes a 100 ps pulse. Node $s$ reaches one flip-flop through a multiplexer with select line $q$:

- if $q = 0$, through an AND gate with side input $b$ and then the multiplexer, 2 gates;
- if $q = 1$, through 4 buffers and then the multiplexer, 5 gates.

Let $q$ and $b$ be independent and each 1 with probability 1/2. For illustration, take a toy attenuation in which each gate takes 20 ps off the width. Then the short path delivers 60 ps and the long path delivers 0 ps. Use the latch values above, so a 60 ps pulse is captured with probability 1/10.

- $L$: the path is sensitized if $q = 1$, or if $q = 0$ and $b = 1$. So $P(L) = 1/2 + 1/4 = 3/4$.
- $E$: the pulse survives only on the short path, so $P(E) = P(q = 0) = 1/2$. Given $L$, the short path is the open one with probability $(1/4)/(3/4) = 1/3$, so $P(E \mid L) = 1/3$.
- $W$: given $L \cap E$, the width is 60 ps and $P(W \mid L \cap E) = 1/10$.

The exact probability is $3/4 \times 1/3 \times 1/10 = 1/40 = 0.025$. The product of the separate factors gives $3/4 \times 1/2 \times 1/10 = 3/80 = 0.0375$, which is 1.5 times too large. The cause is that the long path is both easier to open and sure to kill the pulse, so $L$ and $E$ are dependent. An analysis that follows each sensitized path with its own width, as the chain rule asks, gets the exact value.

## Where it is used

- **Soft error rate estimation.** Tools estimate the rate of each node by combining the strike rate with the three masks. The logic factor comes from signal probabilities, from [binary decision diagrams](/bdd-switching-activity-estimation/) for exact sensitization probabilities on small cones, or from random vectors with [fault simulation](/fault-simulation/) and [Monte Carlo integration](/monte-carlo-integration/). The pulse widths come from circuit simulation or from tables per gate. The path delays and the clock period come from [static timing analysis](/static-timing-analysis/).
- **Selective hardening.** Designers protect only the nodes and flip-flops with the highest unmasked rate, by upsizing gates (more critical charge), by hardened flip-flops, or by duplication.
- **Pulse filtering in flip-flops.** Some flip-flops add a delay element that rejects pulses shorter than a set width, which strengthens the latch window mask at the cost of a longer setup time.
- **Relation to glitches.** The same low-pass filtering by gates that attenuates particle pulses also removes short functional glitches, see [glitch power](/glitch-power/).
- **Memories.** Strikes on memory cells are not masked by logic, so memories use error correcting codes and interleaving. Masking analysis is about the logic between storage elements.

## References
