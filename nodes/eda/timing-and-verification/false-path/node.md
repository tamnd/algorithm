---
tag: 0HPS9J
kind: definition
slug: false-path
name: False path
aliases:
- unsensitizable path
area: eda/timing-and-verification
level: advanced
summary: A path of the timing graph that no input vector can sensitize, so its delay does not matter, but static analysis counts it unless told.
prereqs: [static-timing-analysis, boolean-circuit, np-complete]
see_also: [timing-graph, arrival-and-required-time, setup-and-hold-constraints, circuit-sat, automatic-test-pattern-generation, d-algorithm, critical-path]
sources:
  - paper: doi:10.1145/74382.74475
    title: David H. C. Du, Steve H. C. Yen and S. Ghanta, On the general false path problem in timing analysis, Proceedings of the 26th Design Automation Conference, 555 to 560, 1989
    locator: false paths, static sensitization and its limits
  - paper: doi:10.1145/74382.74476
    title: Patrick C. McGeer and Robert K. Brayton, Efficient algorithms for computing the longest viable path in a combinational network, Proceedings of the 26th Design Automation Conference, 561 to 567, 1989
    locator: the viability criterion and the monotone speedup property
  - paper: "H. C. Chen and David H. C. Du, Path sensitization in critical path problem, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 12(2), 196 to 207, 1993"
    locator: the floating mode of operation and the sensitization condition for it
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 8, Timing Verification (false paths as timing exceptions)
---

A false path is a path of the [timing graph](/timing-graph/) along which no change of the inputs can ever travel to the output. [Static timing analysis](/static-timing-analysis/) does not look at the logic functions of the gates. It takes the longest path in the graph as the delay, so a long false path makes the reported delay larger than any delay the circuit can show. The term has two uses. In theory, a path is false under a *sensitization criterion*, a rule that says when a vector of input values lets an event pass along the path. In practice, "false path" is also a timing exception: the designer tells the tool that a path does not need to meet its constraint, and the tool removes it from the analysis.

## Definition

Let $N$ be a combinational [Boolean circuit](/boolean-circuit/) of AND, OR, NAND, NOR, NOT and buffer gates, with a fixed delay $d(g) \ge 0$ at each gate $g$. A *path* $P = (g_0, g_1, \ldots, g_k)$ starts at a primary input $g_0$ and ends at an output $g_k$, and each $g_{j-1}$ is an input of $g_j$. Its length is $d(P) = d(g_1) + \cdots + d(g_k)$. At gate $g_j$, the input $g_{j-1}$ is the *on-input* and the other inputs are the *side inputs*. The *controlling value* of AND and NAND is 0, and that of OR and NOR is 1: one input at this value fixes the output. The other value is *non-controlling*.

**Static sensitization.** An input vector $x$ *statically sensitizes* $P$ if, in the steady state under $x$, every side input of every gate on $P$ has its non-controlling value. Then a change of $g_0$ alone changes every gate on $P$.

**False path (static).** $P$ is *statically false* if no input vector statically sensitizes it. The *static delay* of $N$ is the largest length of a path that is not statically false.

**Floating mode.** In the floating mode, the circuit is in an unknown state when the vector $x$ is applied at time 0. Under $x$, define the time $t_x(g)$ after which gate $g$ is stable: $t_x(g_0) = 0$ at the primary inputs, and at a gate $g$ with inputs $I(g)$,

- if some input has the controlling value of $g$, then $t_x(g) = d(g) + \min\{t_x(i) : i \in I(g), \; i \text{ controlling}\}$,
- else $t_x(g) = d(g) + \max\{t_x(i) : i \in I(g)\}$.

The *floating delay* of $N$ is $\max_x t_x(\text{out})$. A path $P$ is *true* in the floating mode if, for some $x$, each on-input $g_{j-1}$ is an input at which the min or the max above is attained for $g_j$, so that $t_x(g_j) = t_x(g_{j-1}) + d(g_j)$ all along $P$. Otherwise $P$ is *false* in the floating mode. Chen and Du (1993) study this mode and give a condition on the side inputs of a path for it.

**Timing exception.** In a constraint file in the SDC format, the command `set_false_path -from A -to B` marks all paths from $A$ to $B$ as false. The tool then does not check them. Typical uses are paths between clocks that are not related, and paths through test or configuration logic that is static in normal operation. The tool does not prove that these paths are false; the designer asserts it.

**Basic facts.**

- *Floating delay is at most the STA delay.* By induction in topological order, $t_x(g) \le \mathrm{AT}(g)$, the [arrival time](/arrival-and-required-time/) with all inputs at 0, because a min over a subset and a max over all inputs are both at most the max over all inputs.
- *Floating delay is safe.* Whatever the state before time 0, gate $g$ does not change after $t_x(g)$, with transport delays. A gate with a controlling input $i$ is fixed once $i$ is stable, and a gate without one is fixed once all its inputs are stable. So the floating delay is an upper bound on the delay of every input transition that ends in $x$.
- *Static delay is not safe.* The second example below has a static delay of 2 and an input transition whose output changes at time 3.

**Theorem (NP-completeness).** Given $N$ and a path $P$, deciding whether $P$ is statically sensitizable is [NP-complete](/np-complete/). Given $N$ and a number $D$, deciding whether the floating delay is at least $D$ is NP-complete.

*Proof.* Both are in NP: for a given vector $x$, the steady state, the side input test and all $t_x(g)$ take time linear in the size of $N$. For hardness, reduce from [circuit satisfiability](/circuit-sat/). Let $C$ be a circuit with output $z$, and let $L$ be larger than the longest path of $C$, with unit gate delays. Build $N$ from $C$, a new input $w$, a chain of buffers of total delay $L$ from $w$ to a node $w'$, and an output gate $y = \mathrm{AND}(w', z)$ of delay 1. Let $P$ be the path from $w$ through the buffers to $y$.

The only side input on $P$ is $z$ at the AND gate, so $P$ is statically sensitizable if and only if some vector makes $z = 1$, that is, if and only if $C$ is satisfiable.

For the floating mode, take $D = L + 1$. Each $t_x$ in $C$ is less than $L$, and $t_x(w') = L$. If $z = 0$ under $x$, then $z$ is a controlling input of $y$, so $t_x(y) \le t_x(z) + 1 < L + 1$. If $z = 1$ and $w = 0$, then $w'$ is the only controlling input, and $t_x(y) = L + 1$. If $z = 1$ and $w = 1$, no input of $y$ is controlling, and $t_x(y) = \max(L, t_x(z)) + 1 = L + 1$. So the floating delay is at least $L + 1$ if and only if $C$ is satisfiable. Both reductions take polynomial time. $\square$

So the exact delay of a circuit, with the logic taken into account, is hard to compute in the worst case. This is why STA uses the graph alone, and leaves false paths to separate tools and to timing exceptions.

## Examples and non-examples

**Two multiplexers with complementary selects.** Take inputs $x$ and $s$, $n = \mathrm{NOT}(s)$ and a slow buffer $l = \mathrm{BUF}(x)$ with delay 6. All the other gates have delay 1:
$$ m_1 = \mathrm{OR}(\mathrm{AND}(x, n), \; \mathrm{AND}(s, l)), \qquad y = \mathrm{OR}(\mathrm{AND}(m_1, n), \; \mathrm{AND}(s, x)). $$
The first multiplexer passes the slow signal $l$ when $s = 1$, and the second passes $m_1$ only when $s = 0$. The path $x \to l \to \mathrm{AND}(s, l) \to m_1 \to \mathrm{AND}(m_1, n) \to y$ has length $6 + 1 + 1 + 1 + 1 = 10$, the longest in the graph, so STA reports a delay of 10. Static sensitization of this path needs $s = 1$ at the first AND gate and $n = 1$, so $s = 0$, at the third. No vector does both, so the path is statically false. The floating delays of the four vectors $(x, s) = (0,0), (0,1), (1,0), (1,1)$ are 4, 3, 5 and 2, so the floating delay is 5, from the path $s \to n \to \mathrm{AND}(x, n) \to m_1 \to \mathrm{AND}(m_1, n) \to y$. An event simulation with transport delays of all 16 pairs of input vectors gives the same worst case: the output last changes at time 5, for the change from $(0, 1)$ to $(1, 0)$. The circuit computes $y = x$, and a synthesis tool would remove it, but the same structure is common in data paths with shared select signals.

**Static sensitization is too optimistic.** Take $g_0 = \mathrm{AND}(a, b)$ with delay 1, $g_1 = \mathrm{OR}(g_0, a)$ with delay 2 and $g_2 = \mathrm{AND}(g_1, g_0)$ with delay 1, output $g_2$. The longest path $b \to g_0 \to g_1 \to g_2$ has length 4. The output is 1 only for $a = b = 1$. Under this vector, $g_0 = 1$ and $a = 1$ are both controlling at the OR gate, so no path through $g_1$ is statically sensitized, and the only statically sensitized path to $g_2$ is $a \to g_0 \to g_2$, of length 2. Under the other three vectors, $g_0 = 0$ is a controlling side input of $g_2$, so again no path through $g_1$ is statically sensitized, and the paths through $g_0$ alone have length 2. So the static delay is 2. But when the inputs change from $(0, 0)$ to $(1, 1)$, $g_0$ rises at time 1, $g_1$ rises at time 2 (through $a$, the first controlling input to arrive) and $g_2$ rises at time 3. The floating mode gets this right: $t_x(g_1) = \min(0, 1) + 2 = 2$ and $t_x(g_2) = \max(2, 1) + 1 = 3$. The path $a \to g_1 \to g_2$ of length 3 is true in the floating mode and false in the static sense. All the numbers in these two examples were checked by enumeration of all vectors and all pairs of vectors.

**Non-example: a long path that is short in practice.** A path can be true and still never be exercised by the input data that the design receives, for example a carry chain whose longest carry never occurs in the application. It is not a false path in any of the senses above, and treating it as one is a design error.

**Non-example: a path with a hazard.** In the circuit $g = \mathrm{AND}(a, \mathrm{NOT}(a))$ the output is always 0 in the steady state, but a rising $a$ can make a short pulse at $g$. The path through the inverter is statically sensitized by $a = 1$. A sensitization criterion is about when the output becomes stable, not about whether it stays constant.

## Related definitions

- **Viable path.** McGeer and Brayton (1989) define viability, a criterion made for the *monotone speedup* property: the delay it reports stays an upper bound on the real delay when some gates are faster than their stated delays. Real gate delays vary, so a criterion without this property can be wrong for the chip that is built.
- **Transition delay.** The delay of a fixed pair of input vectors, as in the event simulation above. It is at most the floating delay of the second vector.
- **Path delay faults.** In testing, a path delay fault is a path that is too slow. A test for it must sensitize the path, so the same conditions appear in [automatic test pattern generation](/automatic-test-pattern-generation/), for example in the [D-algorithm](/d-algorithm/).
- **Multicycle path.** A timing exception that allows a path several clock cycles instead of one; see [setup and hold constraints](/setup-and-hold-constraints/). A false path is the limit with no constraint at all.
- **Critical path.** The longest path of the timing graph, the path with the worst slack. If it is false, the next longest true path decides the real delay.

## References
