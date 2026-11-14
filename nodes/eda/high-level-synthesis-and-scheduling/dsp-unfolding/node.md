---
tag: SNB59C
kind: technique
slug: dsp-unfolding
name: Unfolding transformation
aliases:
- loop unfolding of data flow graphs
- Parhi-Messerschmitt unfolding
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Parhi and Messerschmitt's transformation that copies a data flow graph J times with redistributed delays so one iteration processes J samples, reaching the iteration bound.
prereqs: [iteration-bound, retiming]
see_also: [dsp-folding, synchronous-dataflow, loop-unrolling, software-pipelining, iir-filter, fir-filter, sdc-modulo-scheduling, karp-minimum-mean-cycle]
sources:
  - paper: doi:10.1109/12.73588
    title: Keshab K. Parhi and David G. Messerschmitt, Static rate-optimal scheduling of iterative data-flow programs via optimum unfolding, IEEE Transactions on Computers 40(2), 1991
    locator: the unfolding of a data flow graph, perfect-rate graphs, and rate-optimal schedules after unfolding by the optimum factor
  - book: isbn:9780471241867
    title: Keshab K. Parhi, VLSI Digital Signal Processing Systems, Design and Implementation, Wiley, 1999
    locator: Chapter 5 (5.2 an algorithm for unfolding, 5.3 properties of unfolding, 5.4 critical path, unfolding and retiming, 5.5 applications)
  - paper: "Markku Renfors and Yrjö Neuvo, The maximum sampling rate of digital filters under hardware speed constraints, IEEE Transactions on Circuits and Systems CAS-28(3), 196 to 202, 1981"
    title: Markku Renfors and Yrjö Neuvo, The maximum sampling rate of digital filters under hardware speed constraints, IEEE Transactions on Circuits and Systems CAS-28(3), 196 to 202, 1981
    locator: the iteration bound that unfolding lets a clocked design reach
---

Unfolding turns a data flow graph that handles one sample per iteration into an equivalent graph that handles $J$ consecutive samples per iteration. Each node $U$ becomes $J$ copies $U_0, \ldots, U_{J-1}$, where copy $U_i$ computes what $U$ computed for sample $Jk + i$, and each edge with $w$ delays becomes $J$ edges whose delays add up to $w$ again. The new graph is a parallel design: it takes $J$ inputs and gives $J$ outputs per clock. Parhi and Messerschmitt (1991) used it to reach the [iteration bound](/iteration-bound/) with a clocked circuit when the bound is not an integer, which [retiming](/retiming/) alone cannot do. It is the hardware form of [loop unrolling](/loop-unrolling/) for loops that carry values from one iteration to the next.

## In plain words

Suppose a machine makes one cake per hour, and the slowest part of the recipe is a chain of steps that takes an hour and a half but only has to be redone every second cake. One machine cannot use that slack, because its clock ticks once per cake. Build two machines side by side, one for the even cakes and one for the odd cakes, and let each pass its half-finished batter to the other. Now one tick of 3 hours makes two cakes, so each cake costs an hour and a half, which is the true limit. Unfolding is this trick for a filter: copy the circuit, and rewire each delay so that every copy reads its past values from the right copy.

## When it applies

- The graph is a data flow graph in the sense of the [iteration bound](/iteration-bound/) page: nodes run once per iteration, edges carry $w(e)$ delays, and every cycle has a delay.
- The iteration bound $T_\infty$ is not an integer number of clock cycles, so a clocked one-sample-per-cycle design wastes time on the critical loop. Unfolding by a $J$ with $J T_\infty$ an integer removes the rounding.
- The design must take several samples per clock: a block of $J$ parallel inputs, as in a parallel filter that runs at a clock $J$ times slower than the sample rate.
- A bit-serial design should become digit-serial, or a word-level design should process several words at once.

## The template

The input is a graph $G$ with nodes $V$, edges $(U, V, w)$ and the factor $J \ge 1$. A host node $X$ that reads the input sample $x(k)$ in iteration $k$ is treated like any other node; its copy $X_i$ reads $x(Jk + i)$.

```pseudo id=main
UNFOLD(G, J)
L1  for each node U of G and each i in 0, ..., J − 1: make the node U_i
L2  for each edge U → V of G with w delays, in the order of the input slots of V, do
L3      for i ← 0 to J − 1 do
L4          j ← (i + w) mod J
L5          add the edge U_i → V_j with ⌊(i + w) / J⌋ delays
L6  give each host copy X_i the input x(Jk + i) and each output copy Y_i the output y(Jk + i)
L7  return the new graph G_J
```

The holes are the factor $J$ of L1, the conversion of L6 (a serial-to-parallel converter at the input and a parallel-to-serial converter at the output), and what is done with $G_J$ afterwards: usually a [retiming](/retiming/) to a clock period equal to its iteration bound, or a [folding](/dsp-folding/) onto fewer units.

**Why L4 and L5 are right.** Let copy $U_i$ in iteration $k$ of $G_J$ compute $U$ in iteration $Jk + i$ of $G$. In $G$, iteration $n$ of $V$ reads iteration $n - w$ of $U$. Take $n = Jk + j$ and let $i$ be the copy of $U$ that holds iteration $n - w$, so $i \equiv j - w \pmod J$, that is $j = (i + w) \bmod J$. Write $i + w = J \lfloor (i + w) / J \rfloor + j$. Then
$$n - w = Jk + j - w = J\left(k - \left\lfloor \frac{i + w}{J} \right\rfloor\right) + i,$$
which is iteration $k - \lfloor (i + w) / J \rfloor$ of $U_i$. So $V_j$ must read $U_i$ through exactly $\lfloor (i + w)/J \rfloor$ delays, which is L5. For each $j$ there is exactly one $i$, so each copy $V_j$ gets exactly one copy of each input edge of $V$, and keeping the order of L2 keeps the input slots of non-commutative nodes in order. By induction on the iterations, and inside one iteration on the edges with no delay, every copy computes the value claimed. The delays that start at zero stand for samples before time 0 in both graphs.

**Delays are kept.** Write $w = aJ + r$ with $0 \le r < J$. Then $\lfloor (i + w)/J \rfloor$ is $a$ for the $J - r$ values $i < J - r$ and $a + 1$ for the other $r$ values, so the $J$ new edges carry $J a + r = w$ delays in total. This is the case $x = w / J$ of Hermite's identity $\sum_{i=0}^{J-1} \lfloor x + i/J \rfloor = \lfloor J x \rfloor$. So $G_J$ has $J |V|$ nodes, $J |E|$ edges and the same total number of delays as $G$. An edge with $w < J$ delays has $J - w$ copies with no delay and $w$ copies with one delay, and an edge with $w \ge J$ has at least one delay on every copy.

**The iteration bound grows by exactly $J$.** Follow a cycle $C'$ of $G_J$. Each edge moves the copy index from $i$ to $(i + w) \bmod J$ and carries $\lfloor (i + w)/J \rfloor = (i + w - j)/J$ delays. Around a closed cycle the terms $i$ and $j$ cancel, so $w(C') = w(W)/J$, where $W$ is the closed walk of $G$ under $C'$, and $t(C') = t(W)$. So $t(C')/w(C') = J \, t(W)/w(W) \le J T_\infty$, since a closed walk has no larger ratio than the best cycle. Conversely, lift a cycle $C$ of $G$ with $w(C)$ delays from copy $i$: after one turn the index is $(i + w(C)) \bmod J$, and after $m = J / \gcd(J, w(C))$ turns it is back at $i$. The lift is a cycle $C'$ with $t(C') = m \, t(C)$ and $w(C') = m \, w(C) / J$, so its ratio is $J \, t(C) / w(C)$. Hence
$$T_\infty(G_J) = J \cdot T_\infty(G).$$
An iteration of $G_J$ handles $J$ samples, so the bound per sample is unchanged: unfolding never makes the bound worse and never makes it better. What it changes is that $J T_\infty$ can be an integer when $T_\infty$ is not.

**Unfolding twice.** Unfolding by $a$ and then by $b$ gives the same graph as unfolding by $ab$, up to the names of the copies: copy $m$ of copy $i$ is copy $i + a m$.

## Classic examples

**A recursive filter with a fractional bound.** Take $y(n) = x(n) + 3 y(n - 2) + 5 y(n - 3)$ with an adder $A$ of time 1 and multipliers $B$ (by 3) and $C$ (by 5) of time 2. The edges are $X \to A$ (0 delays), $A \to B$ (0), $B \to A$ (2), $A \to C$ (1) and $C \to A$ (2). The loops have ratios $3/2$ and $3/3$, so $T_\infty = 3/2$. The critical path is $X \to A \to B$, of time 3, and retiming brings the clock period down to 2, not to 1.5. Unfolding by $J = 2$ gives these edges:

| edge of $G$ | $w$ | copy $i = 0$ | copy $i = 1$ |
| --- | --- | --- | --- |
| $X \to A$ | 0 | $X_0 \to A_0$, 0 | $X_1 \to A_1$, 0 |
| $A \to B$ | 0 | $A_0 \to B_0$, 0 | $A_1 \to B_1$, 0 |
| $B \to A$ | 2 | $B_0 \to A_0$, 1 | $B_1 \to A_1$, 1 |
| $A \to C$ | 1 | $A_0 \to C_1$, 0 | $A_1 \to C_0$, 1 |
| $C \to A$ | 2 | $C_0 \to A_0$, 1 | $C_1 \to A_1$, 1 |

The 5 delays of $G$ are still 5. The loop $A_0 \to B_0 \to A_0$ has time 3 and 1 delay, and the loop $A_0 \to C_1 \to A_1 \to C_0 \to A_0$ has time 6 and 3 delays, so $T_\infty(G_2) = 3 = 2 \cdot 3/2$. The longest path with no delay is 3 ($X_i \to A_i \to B_i$, or $A_0 \to C_1$), so the unfolded circuit runs with a clock period of 3 and takes 2 samples per clock: 1.5 time units per sample, the iteration bound, with no retiming at all.

**Parallel FIR filters.** A [FIR filter](/fir-filter/) has no loop, so its iteration bound is 0 and unfolding is used only for throughput: unfolding by $J$ gives a block filter with $J$ inputs and $J$ outputs per clock and $J$ times the multipliers. Each delay of the tapped line is shared out among the copies by L5.

**Rate-optimal schedules.** Parhi and Messerschmitt unfold by a factor that makes the graph perfect rate, in which every loop of the unfolded graph has one delay. For a single loop $C$ this happens when $w(C)$ divides $J$, since the lift then has $m = J / w(C)$ turns and $w(C') = 1$. Such a graph can be scheduled to reach its iteration bound, so the original program runs at its bound per sample.

**Compilers.** [Loop unrolling](/loop-unrolling/) of a loop with a recurrence is the same operation on a program, and [software pipelining](/software-pipelining/) and [SDC modulo scheduling](/sdc-modulo-scheduling/) meet the same bound in a different way: they overlap iterations instead of copying them, which needs a fractional initiation interval or unrolling when the recurrence bound is not an integer.

## Variations

- **Unfolding and retiming.** A path of $G_J$ with no delay lies over a path of $G$ with at most $J - 1$ delays, since each edge it uses has $i + w < J$. So the critical path of $G_J$ is the longest such path of $G$, and a retiming of $G_J$ is usually needed to bring it down to $J T_\infty$. Parhi's book (Chapter 5.4) treats how the two steps combine. On the example above, unfolding alone already reaches the bound.
- **Unfolding and folding.** The two transformations compose: folding $G_J$ by a factor $N$ gives hardware that takes $J$ samples every $N$ clock cycles, so the ratio $J / N$ sets the throughput and $N$ sets how many operations share a unit.
- **Multirate graphs.** In a [synchronous dataflow](/synchronous-dataflow/) graph the analogue of unfolding is the expansion with $q_a$ copies of actor $a$, which makes one period of the multirate graph into one iteration of a homogeneous graph.
- **Look-ahead pipelining.** Rewriting a recursion, such as $y(n) = a y(n-1) + x(n)$ into $y(n) = a^2 y(n-2) + a x(n-1) + x(n)$, changes the algorithm and so the iteration bound. Unfolding never does that.

## Pitfalls

- **Wrong copy index.** The edge goes from $U_i$ to $V_{(i + w) \bmod J}$, not to $V_{(i - w) \bmod J}$. With the wrong sign the copy reads a future sample.
- **Ceiling instead of floor.** The delay count is $\lfloor (i + w)/J \rfloor$. With a ceiling the delays no longer add up to $w$ and the copies read samples from the wrong iteration.
- **Expecting a shorter critical path.** Unfolding does not shorten the longest path with no delay; it copies it $J$ times. A path of $G$ with fewer than $J$ delays can even turn into a longer delay-free path of $G_J$ through several copies. The gain is per sample, and usually needs a retiming of $G_J$.
- **A node slower than the target.** A node is never split, so the clock period of $G_J$ is at least the largest node time $t_{\max}$. If $t_{\max} > J T_\infty$, the clock cannot be $J T_\infty$, and only a larger $J$ or a pipelined node helps.
- **Cost.** $G_J$ has $J$ times the units. Unfolding by more than the least $J$ that makes $J T_\infty$ an integer buys no speed per sample.

## Exercises

1. Unfold the filter of the example by $J = 3$. List the edges and check that the delays still add up to 5 and that $T_\infty(G_3) = 9/2$.
2. Show that if every edge of $G$ has $w(e) \ge J$ delays, then every edge of $G_J$ has at least one delay.
3. Show that the unfolded graph of a strongly connected graph need not be strongly connected. Hint: take one cycle with 2 delays and $J = 2$.
4. Prove that unfolding by $a$ and then by $b$ gives the graph of unfolding by $ab$, with copy $m$ of $U_i$ named $U_{i + am}$.

## References
