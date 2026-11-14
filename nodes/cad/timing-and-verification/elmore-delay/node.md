---
tag: JKE68A
kind: definition
slug: elmore-delay
name: Elmore delay
aliases:
- Elmore delay model
area: cad/timing-and-verification
level: core
summary: The delay to a node of an RC tree taken as the sum over resistors on its path of R times the capacitance downstream, the first moment of the impulse response.
prereqs: [rc-tree, impulse-response]
see_also: [rc-tree, asymptotic-waveform-evaluation, prima, van-ginneken-buffer-insertion, tsay-zero-skew, gate-sizing, geometric-programming, expected-value]
sources:
  - paper: doi:10.1063/1.1697872
    title: W. C. Elmore, The transient response of damped linear networks with particular regard to wideband amplifiers, Journal of Applied Physics 19(1), 55 to 63, 1948
    locator: the delay time defined as the first moment (center of gravity) of the impulse response, for networks with a monotone step response
  - paper: doi:10.1109/TCAD.1983.1270037
    title: Jorge Rubinstein, Paul Penfield Jr. and Mark A. Horowitz, Signal delay in RC tree networks, IEEE Transactions on Computer-Aided Design 2(3), 202 to 211, 1983
    locator: the time constants of an RC tree, the Elmore delay as a sum of common path resistances times capacitances, and the upper and lower bounds on the step response
  - paper: "Rohini Gupta, Bogdan Tutuianu and Lawrence T. Pileggi, The Elmore delay as a bound for RC trees with generalized input signals, IEEE Transactions on Computer-Aided Design 16(1), 95 to 104, 1997"
    locator: the proof that the Elmore delay is an upper bound on the 50 percent delay of every node of an RC tree, for step and for more general inputs
  - paper: doi:10.1145/217474.217556
    title: Rohini Gupta, Byron Krauter, Bogdan Tutuianu, John Willis and Lawrence T. Pileggi, The Elmore delay as a bound for RC trees with generalized input signals, Proceedings of the 32nd Design Automation Conference, 364 to 369, 1995
    locator: the conference version of the bound, with the lower bound that uses the second moment
---

The Elmore delay is a simple estimate of the delay from the driver of an [RC tree](/rc-tree/) to one of its nodes. It is the sum, over the resistors on the path from the source to the node, of each resistance times the total capacitance below it. Elmore (1948) defined it as the first moment, the mean, of the impulse response. It is not the exact 50 percent delay, but for an RC tree it is an upper bound on it, and it is cheap, linear in the size of the tree and a simple function of the wire and gate sizes. That makes it the standard delay model inside routing, buffering and sizing algorithms.

## Definition

Let an [RC tree](/rc-tree/) have nodes $1, \ldots, n$ below the source, resistances $R_k$ on the edges and capacitances $C_k$ to ground, and let $R_{ik}$ be the resistance of the common part of the source paths of $i$ and $k$.

**Elmore delay.** The Elmore delay to node $i$ is
$$ T_i = \sum_{k=1}^{n} R_{ik} C_k. $$

**Downstream form.** Let $C^{\downarrow}_k$ be the total capacitance of the subtree of node $k$, including $C_k$. Then
$$ T_i = \sum_{k \text{ on the path from the source to } i} R_k \, C^{\downarrow}_k. $$
*Proof.* $R_{ik}$ is the sum of $R_j$ over the edges $j$ that lie on both source paths, so $T_i = \sum_k C_k \sum_j R_j [j \text{ is above } i \text{ and above } k] = \sum_{j \text{ above } i} R_j \sum_{k \text{ below } j} C_k$, where "above" includes the node itself. $\square$

**Computation in linear time.** One pass from the leaves up (post-order) computes $C^{\downarrow}_k = C_k + \sum_{c \text{ child of } k} C^{\downarrow}_c$. One pass from the source down (pre-order) computes $T_k = T_{p(k)} + R_k C^{\downarrow}_k$ with $T_0 = 0$. Both passes take $O(n)$ time, and give the Elmore delay at all nodes at once.

**First moment.** Let $H_i(s)$ be the transfer function from the source voltage to node $i$, and expand it at $s = 0$ as $H_i(s) = m_0 + m_1 s + m_2 s^2 + \cdots$. Then $m_0 = 1$ and $T_i = -m_1$. Since $H_i(s) = \int_0^\infty h_i(t) e^{-st} \, dt$, this says that $T_i = \int_0^\infty t \, h_i(t) \, dt$ is the mean of the impulse response $h_i$, which on an RC tree is a probability density (see [RC tree](/rc-tree/)). *Proof.* From $C v' = -G v + b u$, the transfer vector is $(G + sC)^{-1} b = G^{-1} b - s \, G^{-1} C G^{-1} b + O(s^2)$. Now $G^{-1} b = \mathbf{1}$ and $G^{-1} = (R_{ik})$, so $-m_1 = (G^{-1} C \mathbf{1})_i = \sum_k R_{ik} C_k$. $\square$

**Bound theorem (Gupta, Tutuianu and Pileggi 1997).** At every node of an RC tree driven by a step, the 50 percent delay $t_{50}$, the time at which the step response reaches half its final value, satisfies $t_{50} \le T_i$. The bound also holds for a class of input signals that includes ramps, and the gap closes as the input rise time grows.

*Proof sketch, from the source.* The 50 percent delay of the step response is the median of the density $h_i$, and $T_i$ is its mean. Gupta and his colleagues show that $h_i$ is unimodal at every node of an RC tree and that it is skewed to the right enough that its median is at most its mean. The proof uses the tree structure. This page does not reproduce it.

## Examples and non-examples

**One section.** A single resistor $R$ to a capacitor $C$ has $T = RC$ and step response $1 - e^{-t/RC}$, so $t_{50} = RC \ln 2 \approx 0.693\,RC$. The Elmore delay is 44 percent too large.

**A ladder of three sections.** With $R_k = C_k = 1$, the Elmore delays at nodes 1, 2, 3 are 3, 5 and 6 (for node 3: $1 \cdot 3 + 1 \cdot 2 + 1 \cdot 1$ in the downstream form). The 50 percent delays, from the matrix exponential, are about 1.12, 3.40 and 4.50. The ratio $t_{50} / T_i$ is 0.37 at the node next to the source and 0.75 at the far end. The estimate is worst near the driver, where the response has a fast start and a long tail.

**A branching tree.** Node 1 below the source with $R_1 = 2$, $C_1 = 1$, and nodes 2 and 3 below node 1 with $R_2 = 1$, $C_2 = 2$ and $R_3 = 3$, $C_3 = 1$. The downstream capacitances are $C^{\downarrow}_1 = 4$, $C^{\downarrow}_2 = 2$, $C^{\downarrow}_3 = 1$, so $T_1 = 8$, $T_2 = 8 + 2 = 10$ and $T_3 = 8 + 3 = 11$. The 50 percent delays are about 4.65, 6.92 and 8.08, all below the bound.

**Non-example: an RLC circuit.** A series resistor $R = 0.1$ and inductor $L = 1$ into a capacitor $C = 1$ has $H(s) = 1 / (LC s^2 + RC s + 1)$. Its first moment gives "Elmore delay" $RC = 0.1$. The circuit is underdamped: the step response overshoots to about 1.85 and first reaches 0.5 at $t \approx 1.07$. So the 50 percent delay is more than ten times the first moment, and the bound fails. The impulse response takes negative values, so it is not a density and its first moment is not a mean of anything.

**Not covered: RC meshes.** For an RC network with loops and grounded capacitors, $T_i = (G^{-1} C \mathbf{1})_i$ is still the first moment of a non-negative impulse response, and it is still easy to compute. The proof of the bound theorem uses the tree, so it does not cover meshes, and this page makes no claim about them. As a measurement only: on 3000 random RC networks with 3 to 5 nodes, most of them with loops, and with conductances and capacitances spread over six decades (Python `random.Random(11)`), the step response at time $T_i$ was always at least 0.58, and a local search that tried to lower it did not go below 0.58 either. So $t_{50} \le T_i$ held in every case we tried, but this is not a proof.

**Non-example: delay through a gate.** The Elmore delay of a net models the wire and the load. The delay of the driving gate itself depends on the input slew and the load in a non-linear way and is taken from a [nonlinear delay model](/nonlinear-delay-model/) table, or from an effective resistance in the simplest models.

## Related definitions

- **Higher moments.** $m_2, m_3, \ldots$ refine the estimate. [AWE](/asymptotic-waveform-evaluation/) fits a few poles to $2q$ moments, and [PRIMA](/prima/) matches moments by a projection that keeps passivity. Two-moment metrics use $m_1$ and $m_2$ to estimate the median.
- **Rubinstein-Penfield-Horowitz bounds.** Three time constants of the tree, one of them the Elmore delay, give an upper and a lower bound on the whole step response at each node.
- **Use in optimization.** With wire widths and gate sizes as variables, the Elmore delay is a posynomial, so delay-constrained sizing is a [geometric program](/geometric-programming/) (see [gate sizing](/gate-sizing/)). [Van Ginneken buffer insertion](/van-ginneken-buffer-insertion/) and the [zero-skew clock tree](/tsay-zero-skew/) also compute Elmore delays bottom up.
- **Mean of a distribution.** The Elmore delay is the [expected value](/expected-value/) of the density $h_i$, and the 50 percent delay is its median.

## References
