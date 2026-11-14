---
tag: N4KVRE
kind: technique
slug: clock-domain-crossing-verification
name: Clock domain crossing verification
aliases:
- CDC verification
- CDC analysis
area: eda/hardware-verification
level: advanced
summary: Finds signals that cross between asynchronous clock domains and checks that each has a proper synchronizer, handshake or FIFO and no reconvergence of synchronized bits.
prereqs: [setup-and-hold-constraints, synchronizer-mtbf]
see_also: [gray-code, cyclic-gray-code, binary-to-gray-conversion, static-timing-analysis, false-path, assertion-based-verification, bounded-model-checking, synchronizer-mtbf]
sources:
  - paper: doi:10.1109/MDT.2011.113
    title: R. Ginosar, Metastability and synchronizers, a tutorial, IEEE Design and Test of Computers 28(5), 23 to 35, 2011
    locator: the two-flip-flop synchronizer, the reasons for not placing logic before it, and the synchronization of multi-bit data by handshakes and by FIFOs with Gray-coded pointers
  - paper: "C. E. Cummings, Simulation and synthesis techniques for asynchronous FIFO design, Synopsys Users Group Conference (SNUG 2002), San Jose, section TB2, 2002"
    title: C. E. Cummings, Simulation and synthesis techniques for asynchronous FIFO design, SNUG San Jose 2002, section TB2
    locator: the FIFO with one more pointer bit than the address, Gray-coded pointers passed through two-flip-flop synchronizers, and the pessimistic full and empty flags
  - book: isbn:9780470510827
    title: D. J. Kinniment, Synchronization and Arbitration in Digital Systems, Wiley, 2008
    locator: the chapters on synchronizers and on the transfer of data between clock domains
---

Clock domain crossing (CDC) verification checks the signals that go from a flip-flop clocked by one clock to a flip-flop clocked by another clock with no fixed phase relation. [Static timing analysis](/static-timing-analysis/) cannot check such a path, because the time between the launch edge and the capture edge is not bounded below. It treats these paths as [false paths](/false-path/). The capture flip-flop will sometimes sample a changing input inside its [setup and hold window](/setup-and-hold-constraints/), and its output can then stay between 0 and 1 for an unbounded time. Correct designs accept that this happens and make it harmless by three kinds of structure. A single control bit goes through a chain of two or more flip-flops in the destination domain. A multi-bit value is either coded so that only one bit changes at a time, as with the Gray-coded pointers of an asynchronous FIFO, or held stable while a synchronized control signal says that it is valid. CDC verification finds every crossing in the netlist, checks that it has one of these structures, and then checks the protocol that the structure needs: no logic in front of a synchronizer, no fanout from its first stage, no reconvergence of separately synchronized bits, one Gray step per source cycle, and data held stable long enough. How often a correct synchronizer still fails is the subject of [synchronizer MTBF](/synchronizer-mtbf/), and this page does not repeat it.

## In plain words

Two parts of a chip run on two clocks that tick at unrelated times. When a signal goes from one part to the other, the receiving flip-flop will sometimes look at it just as it changes. It may then hold a wrong or undecided value for a while.

You cannot stop this. You can only make it safe. Pass a single bit through two flip-flops in a row, so the first has a full clock cycle to make up its mind. Never pass a number made of several bits through separate synchronizers, because each bit may arrive a cycle early or late and the receiver may see a number that never existed. Use a code in which only one bit changes at a time, or hold the data still and send only a "ready" bit across.

A CDC tool finds every crossing and checks these rules.

## When it applies

- The design has two or more clocks, and some pairs are *asynchronous*: they come from different sources, or from one source with frequencies whose ratio is not fixed or with phases that are not controlled. Clocks derived from one source with a known ratio and constrained skew are *synchronous*, and their paths belong to static timing analysis.
- A *crossing* is a pair of flip-flops $(s, d)$ with $s$ in clock domain $A$ and $d$ in an asynchronous domain $B$, such that the data input of $d$ depends on the output of $s$ through combinational logic only.
- The assumption about one flip-flop is the usual one. If its data input is stable during the window from $t_{su}$ before to $t_h$ after the clock edge, it captures the value. If not, its output after the edge is 0 or 1 but which one is not known, and it may need extra time to settle. The chance that it has not settled after a given time is what [synchronizer MTBF](/synchronizer-mtbf/) models. The checks below treat a settled but unknown value as the only effect, which is safe when the MTBF of every synchronizer is long enough.
- The input is a netlist or RTL with the clock of each flip-flop known or traceable to a clock source, and the clock relations given as constraints.

## The template

```pseudo id=main
CDC-CHECK(netlist, clock sources, clock relations)
L1  give each flip-flop the domain of the clock source that its clock pin traces back to through buffers, gates and multiplexers
L2  for each flip-flop d and each flip-flop s that reaches the data pin of d through logic only, with dom(s) and dom(d) asynchronous do record the crossing (s, d)
L3  for each crossing (s, d) that is a single control bit do
L4      require that the data pin of d is driven by s directly, with no logic between them
L5      require that d feeds exactly one flip-flop of dom(d), with no logic and no other fanout, for a chain of at least two stages
L6  for each set of crossings whose synchronized outputs meet again in logic of dom(d) do report reconvergence, unless the source is a recognized code
L7  for each multi-bit crossing require a scheme: a Gray-coded counter that steps at most once per source cycle, or data qualified by a synchronized control signal
L8  write the protocol of each scheme as assertions: one bit changes per cycle, data stable while its control is in flight, levels held long enough
L9  prove or simulate the assertions with each synchronizer allowed to add zero or one extra destination cycle at each change
```

Lines L1 and L2 are structural. Line L1 is one traversal of the clock network. Line L2 searches backward from the data pin of each flip-flop and stops at flip-flops, which costs $O(F m)$ in the worst case for $F$ flip-flops and $m$ nets, and much less when the logic cones are small. Lines L3 to L7 match patterns on the result. Lines L8 and L9 are functional and use the tools of [assertion-based verification](/assertion-based-verification/), such as simulation with assertion monitors or [bounded model checking](/bounded-model-checking/).

**Why a chain of flip-flops.** The first flip-flop $d_1$ may sample its input in the window. Its output then settles to 0 or 1 at some time in the next cycle. The second flip-flop $d_2$ samples it one destination period later, so it sees a settled value unless $d_1$ took almost a whole period to settle. The logic of domain $B$ reads only $d_2$. Line L5 forbids fanout from $d_1$ because two loads of a slowly settling node can read it as different values, and forbids logic between $d_1$ and $d_2$ because that logic eats into the time that $d_1$ has to settle. The cost is a latency of two destination cycles, and the gain is that every value that reaches domain $B$ is a clean 0 or 1 that the source held either just before or just after the sample.

**Why no logic before the synchronizer.** Let $x$ and $y$ be flip-flops of domain $A$ that change at the same edge, $x$ from 1 to 0 and $y$ from 0 to 1, and let the crossing signal be $x \wedge y$. Its value is 0 before and after the edge. If the path from $y$ is faster than the path from $x$, the gate output is 1 for a short time. A destination edge at that moment captures 1, a value that the function never had. Line L4 requires a flip-flop of domain $A$ to drive the crossing, so the crossing signal changes at most once per source cycle and has no glitches.

**Why separately synchronized bits must not reconverge.** Each synchronizer passes a change to domain $B$ either at the first destination edge after the change or one edge later, depending on where in the window the change fell. Take a 2-bit binary state $s_1 s_0$ in domain $A$ that steps from $01$ to $10$, and synchronize the two bits separately. The pair in domain $B$ can be $01$, then $00$ or $11$ for one cycle, then $10$. Both $00$ and $11$ are states that domain $A$ did not have in that step. For a 3-bit step $011 \to 100$ all 8 values are possible. Logic in domain $B$ that decodes the pair can act on such a value. The same holds when one bit of domain $A$ fans out to two synchronizers and the two copies meet in domain $B$: for one cycle they can disagree. Line L6 finds the meeting point by a forward search from the synchronizer outputs.

**Gray codes are safe.** In a [Gray code](/gray-code/), consecutive values differ in one bit. Suppose (a) the source counter steps at most once per source cycle, (b) the skew between the bits of the bus at the first synchronizer stage, plus the sampling window, is less than one source period, and (c) each first-stage flip-flop that samples a changing bit captures its old or its new value. Then at each destination edge at most one bit of the bus is changing, by (a) and (b). The captured word is therefore the code of the old value or of the new value, by (c), so it is a value that the counter really held at about the time of the sample. The proof is two lines, and it fails when (a) or (b) fails. A counter that steps twice in one source cycle, or a bus with more skew than a source period, gives words that are neither.

**The asynchronous FIFO is safe.** The FIFO has $D = 2^n$ entries. The write pointer $w$ and the read pointer $r$ count with $n + 1$ bits, so they run modulo $2D$, and each steps by one per operation in its own domain. Each is converted to a [cyclic Gray code](/cyclic-gray-code/), stored in a flip-flop of its domain, and sent through a two-stage synchronizer to the other domain. A $(n + 1)$-bit reflected Gray code is cyclic, so the wrap from $2D - 1$ to 0 is also one bit. Let $w'$ be the write pointer as the read domain sees it and $r'$ the read pointer as the write domain sees it, each decoded with [Gray-to-binary conversion](/gray-to-binary-conversion/). The read side reports empty when $r = w'$, and the write side reports full when $w - r' = D$ modulo $2D$. In Gray code this is the test that the two top bits differ and the other bits agree.

The claim is that the reader never reads an entry that is not written and the writer never overwrites an entry that is not read. Treat $w$ and $r$ as counts that never wrap, and $w'$ and $r'$ likewise. By the Gray argument, $w'$ is a value that $w$ held at some time, and since the destination period is longer than the window, later samples give values that are not smaller. So $w' \le w$ at all times, and in the same way $r' \le r$. The reader reads only when $r < w'$, so $r < w$ and entry $r$ was written. The writer writes only when $w - r' < D$, so $w - r < D$ and there is a free entry. Both differences stay in $[0, D]$: $w - r' \le D$ because a write needs $w - r' < D$ and $r'$ only grows, and $0 \le w' - r \le w - r \le D$ because the reader reads only up to $w'$. A difference in $[0, D]$ is fixed by its value modulo $2D$, so the comparisons on $n + 1$ bits are exact. The flags are pessimistic: empty or full may stay on after the other side has moved, until the new pointer value has passed the synchronizer, but they are never wrong in the unsafe direction.

**Level-based control.** A level that crosses from a fast domain to a slow one can be missed if it is too short. If a level is stable during an interval of length $T_B + t_{su} + t_h$, where $T_B$ is the destination period, then some destination edge $e$ lies in the interval $[t_0 + t_{su}, t_0 + t_{su} + T_B]$, and the window $[e - t_{su}, e + t_h]$ lies inside the interval, so $e$ captures the level cleanly. A shorter pulse can fall between two edges and be lost. Line L8 writes this as an assertion in source cycles. The same bound gives the least spacing of toggles in a toggle synchronizer, which turns each source pulse into a change of a level and recovers the pulse in domain $B$ by comparing two consecutive synchronized values.

**Example.** Domain $A$ has flip-flops $a_0, a_1$ that form a binary counter and an enable flip-flop $e$. Domain $B$ has flip-flops $p_1 p_2$, $q_1 q_2$ and $u_1 u_2$, each a two-stage chain. The netlist has $a_0 \to p_1$, $a_1 \to q_1$, and $a_0 \wedge e \to u_1$, and the logic of domain $B$ computes $z = p_2 \wedge q_2$.

| crossing | line | result |
|---|---|---|
| $(a_0, p_1)$ | L4, L5 | direct, two stages: passes |
| $(a_1, q_1)$ | L4, L5 | direct, two stages: passes |
| $(a_0, u_1)$, $(e, u_1)$ | L4 | AND gate before $u_1$: logic before a synchronizer |
| $p_2, q_2$ meet in $z$ | L6 | reconvergence of two bits of one binary counter |

The tool reports two errors. The reconvergence is real: on the step $01 \to 10$ of the counter, $z$ can be 1 for one cycle although the counter is never 3 in that step. The fix is to send the counter in Gray code through one synchronized bus, or to send it as data with a synchronized valid bit. For the first fix, line L8 adds the assertion that the Gray word changes in at most one bit per source cycle. In a timed simulation of a 4-entry FIFO with random clock periods between 1 and 3, a window of 0.2 and a bit skew of up to 0.3, 30 runs of 40,000 clock edges took 579,822 samples of the write pointer. With Gray pointers every sample was a value that the pointer had held. With binary pointers 13,581 samples were values that it never held.

**Cost.** Lines L1 to L7 are at most $O(F m)$, as above, and they find the structural errors. The cost is in the number of reported crossings to review. A large design has many thousands, and most reports are waived after a designer confirms a scheme that the tool does not recognize. Lines L8 and L9 cost what the formal or simulation run costs. The structural checks cannot prove that a protocol is followed, and simulation without line L9 cannot show reconvergence errors, because a zero-delay simulator never makes a synchronizer late.

## Classic examples

- **The two-stage synchronizer.** The basic structure for one bit. Its failure rate falls exponentially with the settling time that the second stage allows, as [synchronizer MTBF](/synchronizer-mtbf/) explains. Three stages are used at high clock rates.
- **The asynchronous FIFO.** Cummings (2002) describes the design with $n + 1$-bit [Gray-coded](/binary-to-gray-conversion/) pointers and two-stage synchronizers, and its full and empty flags. It is the standard way to move a stream of words between domains.
- **Handshakes.** A four-phase handshake sets the data, raises a request, waits for a synchronized acknowledge, then lowers the request and waits for the acknowledge to fall. The data needs no synchronizer, because it is stable whenever the other domain samples it. Each transfer takes four synchronizer delays. A two-phase handshake, which signals with each change of the request, takes two.
- **Reset synchronizers.** An asynchronous reset is asserted at any time but must be released in step with the destination clock. A two-stage chain with asynchronous clear releases it on a clock edge. The release is a crossing that CDC tools check like any other.
- **Clock multiplexers.** Switching between two asynchronous clocks needs a glitch-free multiplexer whose select bits are synchronized in each clock domain. A plain multiplexer on clocks is a structural error that line L1 finds.

## Variations

- **Mesochronous and ratio clocks.** Clocks with the same frequency and an unknown but fixed phase, or with a fixed rational ratio, allow cheaper schemes than full synchronizers, such as a phase-selected sampling point. A tool must know the relation to avoid false reports.
- **Metastability injection.** Line L9 can be done in simulation by replacing each synchronizer with a model that adds an extra cycle at random when its input changes near an edge. Ordinary tests then expose reconvergence and protocol errors that a plain simulation hides.
- **Formal protocol checks.** The assertions of line L8, such as "the data is stable while the request is high and the acknowledge has not returned", are safety properties that model checking can prove for all inputs.
- **Reset domain crossing.** The same analysis applies to paths between flip-flops with different asynchronous resets, where a reset in one domain can corrupt a flip-flop in another.
- **RTL and gate level.** At RTL the clock of each register is clear, but logic synthesis may add logic or duplicate flip-flops. A second check after synthesis catches a synchronizer that was optimized or retimed.

## Pitfalls

- **Binary counters through separate synchronizers.** This is the reconvergence case. It passes every test in a simulator without metastability models.
- **Gray codes that skip.** A Gray counter that steps twice in one source cycle, or a pointer that is Gray coded only after a register that holds a binary value, changes several bits at once. The pointer must be stored in Gray code in a flip-flop of the source domain.
- **Bus skew.** The Gray argument needs the skew of the bus to be under one source period. Static timing does not check false paths, so add an explicit maximum delay or skew constraint for these buses.
- **Synchronizers that are optimized away.** Synthesis can merge the two stages with other logic or retime them. Mark synchronizer cells so that tools keep them.
- **Too many waivers.** A tool reports every crossing that it does not recognize. Waiving reports without checking the protocol hides real errors. Write the protocol as an assertion instead.
- **Ignoring the MTBF.** A structurally correct synchronizer can still fail too often at high clock rates or in slow process corners. Compute its failure rate with the model of [synchronizer MTBF](/synchronizer-mtbf/).

## Exercises

1. Show that two copies of one bit that pass through separate two-stage synchronizers can disagree for at most one destination cycle per change, under assumption (c), when changes are at least two destination periods apart.
2. Prove that the full test $w - r' = D$ modulo $2D$ is the same as "the two top bits of the Gray codes differ and the other bits agree".
3. A source pulse lasts one cycle of a 500 MHz clock, and the destination runs at 100 MHz. Design a toggle synchronizer for it, and give the least spacing between pulses that the bound of this page allows, with $t_{su} = t_h = 0.1$ ns.

## References
