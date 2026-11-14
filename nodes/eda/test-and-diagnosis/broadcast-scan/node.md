---
tag: 31X0VE
kind: technique
slug: broadcast-scan
name: Broadcast scan
aliases:
- Illinois scan
area: eda/test-and-diagnosis
level: advanced
summary: Hamzaoglu and Patel's compression in which one tester channel feeds several scan chains at once, with a serial mode kept for patterns that need distinct values.
prereqs: [scan-design, automatic-test-pattern-generation]
see_also: [embedded-deterministic-test, lfsr-reseeding, x-compact, multiple-input-signature-register, soc-test-wrapper-and-tam-design, redundant-fault, graph-coloring, fault-coverage]
sources:
  - paper: "I. Hamzaoglu and J. H. Patel, Reducing test application time for full scan embedded cores, Digest of Papers, 29th International Symposium on Fault-Tolerant Computing, 260 to 267, 1999"
    title: I. Hamzaoglu and J. H. Patel, Reducing test application time for full scan embedded cores, Digest of Papers, 29th International Symposium on Fault-Tolerant Computing, 260 to 267, 1999
    locator: the parallel-serial scan architecture, in which one scan input feeds many short chains in broadcast mode and the chains are joined into one in serial mode
  - paper: "K.-J. Lee, J.-J. Chen and C.-H. Huang, Broadcasting test patterns to multiple circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(12), 1793 to 1802, 1999"
    title: K.-J. Lee, J.-J. Chen and C.-H. Huang, Broadcasting test patterns to multiple circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(12), 1793 to 1802, 1999
    locator: one scan input shared by several circuits or chains, and test generation on a virtual circuit in which the inputs that receive the same bit are tied together
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter Test Compression (broadcast scan and Illinois scan among the stimulus compression methods)
---

Broadcast scan cuts the test data and the shift time of a [scan design](/scan-design/) by feeding several scan chains from one tester channel, so that all of them receive the same bits in the same cycles. Lee, Chen and Huang (1998, 1999) used one scan input to drive several circuits or chains at once. Hamzaoglu and Patel (1999) split one long chain of a core into many short segments that share one input in broadcast mode, and kept a serial mode in which the segments are joined into the original long chain. This parallel-serial scheme is called Illinois scan. In broadcast mode the cells at the same position of every segment always hold equal values, so a pattern can be applied there exactly when its care bits agree at each position. Faults that need conflicting values are tested in serial mode, which costs the full shift length.

## In plain words

Loading a test into a chip means pushing bits one by one into long chains of storage cells. Cut one chain of 1000 cells into 10 chains of 100, and feed all 10 from the same wire. Now loading takes 100 steps, not 1000, and the tester stores 100 bits per test, not 1000.

The catch is that all 10 chains get the same bits, so cell 7 of every chain holds the same value. Most tests only care about a few cells, so this usually does not matter. When a test needs cell 7 of one chain to be 0 and cell 7 of another to be 1, the chip switches back to one long chain for that test.

## When it applies

- The design has full scan, and the scan cells can be split into many short chains.
- Test patterns have few care bits, so most of them agree at each chain position after the free bits are filled. This is the common case for single stuck-at and transition tests.
- A very simple decompressor is wanted: broadcast needs only wires and a mode multiplexer, no XOR network and no state, which makes it easy to verify and to diagnose.
- The responses can be compacted, or the chains can be observed through a small number of outputs, since many chains now produce output in parallel.

## The template

Let the scan cells be split into $k$ chains of length $\ell$, and let $(i, j)$ be cell $j$ of chain $i$.

```pseudo id=main
BROADCAST-SCAN-TEST(the circuit, k, ℓ)
L1  build the broadcast circuit: for each position j, tie the cells (1, j), ..., (k, j) to one new input u_j
L2  run test generation on the broadcast circuit for every fault; keep its tests, ℓ bits each
L3  for each fault left undetected by L2 that is detectable in the original circuit do
L4      run test generation on the original circuit; keep the test, kℓ bits
L5  apply each broadcast test: ℓ shift cycles, one channel feeding all k chains, then capture
L6  apply each serial test: kℓ shift cycles through the chains joined into one, then capture
L7  compact the responses of the k chains and compare with the expected values
```

The holes are the split of the cells into chains, which decides which cells share a value, the number of channels, the response compactor, and the test generator. Line L1 is the virtual circuit of Lee, Chen and Huang: a test of the broadcast circuit is a test of the real circuit in broadcast mode and nothing else.

**Which cubes fit.** A test cube assigns 0, 1 or X to each cell. In broadcast mode the loads that can be applied are exactly those with $v(i, j) = u_j$ for all $i$, for some bits $u_1, \ldots, u_\ell$. So a cube can be applied in broadcast mode exactly when, at every position $j$, its care bits on $(1, j), \ldots, (k, j)$ are all equal. If they are, set $u_j$ to that value, or to anything when the position has no care bit, and every care bit is met. If two care bits at one position differ, no choice of $u_j$ meets both. So the faults that broadcast mode can detect are exactly the faults detectable in the broadcast circuit of line L1, and test generation on it, as in line L2, finds them or proves that they need serial mode.

**What it costs.** With $N_b$ broadcast tests and $N_s$ serial tests, the tester stores about $N_b \ell + N_s k \ell$ bits, against $(N_b + N_s) k \ell$ for plain scan, and the shift time falls in the same proportion. The gain is close to $k$ only when $N_s$ is small, which depends on how often care bits conflict. On random circuits of 10 scan cells and 40 gates, split into 2 chains of 5 cells, with seed 3 and 20 circuits, 472 of the 4527 detectable stuck-at faults (10.4%) were undetectable in broadcast mode. That is a measurement on small random netlists; on real designs the fraction depends on the split of cells into chains, and the serial tests that remain can dominate the test time when $k$ is large.

**A model of conflicts.** Suppose a cube has $s$ care bits at distinct cells chosen uniformly at random among the $k \ell$ cells, with independent uniform values. Two given care bits sit at the same position with probability $(k - 1)/(k\ell - 1)$, and then they differ with probability $1/2$. By linearity of expectation the expected number of conflicting pairs is $\binom{s}{2} \frac{k - 1}{2(k\ell - 1)}$, and the cube fits with probability at least one minus this number. So under this model the cubes fit while $s$ is small compared with $\sqrt{\ell}$. Real care bits are not uniform: they cluster in the fan-in cones of the target fault, which is why the split of cells into chains matters.

## Classic examples

- **Illinois scan.** Hamzaoglu and Patel split each long chain into short segments with one shared input and a serial mode, which reduces both the data volume and the test time of cores in a [system on chip](/soc-test-wrapper-and-tam-design/).
- **Broadcast to several circuits.** Lee, Chen and Huang drive the scan inputs of several circuits or cores from one tester channel, and generate tests on the virtual circuit in which the shared inputs are one input.
- **The base of linear decompressors.** Broadcast is the simplest linear decompressor: each cell gets one tester bit. [LFSR reseeding](/lfsr-reseeding/) and [embedded deterministic test](/embedded-deterministic-test/) give each cell an XOR of many tester bits, so that care bits conflict far less often, at the cost of solving linear equations.
- **Response side.** The $k$ chains produce $k$ bits per cycle, which are compacted by an XOR network such as [X-compact](/x-compact/) or by a [multiple-input signature register](/multiple-input-signature-register/).

## Variations

- **Several broadcast groups.** Use $c$ channels, each feeding a group of chains. A conflict at one position is resolved when the two cells are in different groups.
- **Reconfigurable broadcast.** A few control bits per pattern choose one of several maps from channels to chains. A cube that conflicts under one map often fits another, which keeps most tests out of serial mode.
- **Choosing which cells share a position.** Cells that are often specified together with different values should not share a position. Building a conflict graph of cells and splitting it is a form of [graph coloring](/graph-coloring/).
- **Dropping serial mode.** Some schemes test the remaining faults in a reduced mode, for example with half the chains per channel, instead of the full serial chain.

## Pitfalls

- **Counting broadcast tests only.** The serial tests of lines L3 and L4 each cost $k$ times a broadcast test. Ten percent of the faults in serial mode can cancel most of the gain when $k$ is 10 or more. Report the time of both modes.
- **Calling broadcast-undetectable faults redundant.** A fault for which line L2 finds no test may be detectable in the original circuit. It is not a [redundant fault](/redundant-fault/), and dropping it from the fault list lowers the [fault coverage](/fault-coverage/). Line L3 must try the original circuit.
- **Splitting cells by name.** If cells that feed the same gates are placed at the same position of different chains, their values are always equal, and faults that need them to differ are lost. Split by structure, not by netlist order.
- **Forgetting the response side.** Broadcast compresses only the stimuli. If the $k$ chains are still read out on $k$ pins, the pin count and the response data are not reduced.
- **Unknown values in the compactor.** When responses are compacted, an X in one chain can hide the errors of the others at that cycle. Plan the handling of unknown values, by masking or by a compactor such as [X-Compact](/x-compact/), together with the broadcast.

## Exercises

1. Show that the set of loads reachable in broadcast mode with $k$ chains of length $\ell$ is a linear subspace of dimension $\ell$ over GF(2), and write the matrix that maps the tester bits to the cells.
2. A cube has $s$ care bits at uniformly random distinct cells of $k$ chains of length $\ell$, with independent uniform values. Compute the probability that it fits broadcast mode for $k = 2$, $\ell = 5$ and $s = 3$.
3. Give a circuit with two scan cells in two chains of length 1 and a single stuck-at fault that is detectable in serial mode but not in broadcast mode.
4. With $N$ tests, a fraction $f$ of which need serial mode, find the value of $f$ at which broadcast scan with $k$ chains has half the speedup of an ideal $k$-fold compression.

## References
