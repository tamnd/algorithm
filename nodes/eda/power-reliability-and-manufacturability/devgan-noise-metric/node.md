---
tag: 6FQBVC
kind: algorithm
slug: devgan-noise-metric
name: Devgan noise metric
aliases:
- Devgan coupled noise estimate
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Devgan's upper bound on crosstalk noise peak in an RC tree, the Elmore-like sum of resistances times coupling currents, computable in linear time.
model: word-ram
complexity:
  vars: {n: the number of nodes of the victim tree, m: the number of coupling capacitors}
  time: {worst: "O(n + m)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1997
  people: [Anirudh Devgan]
  note: Devgan proposed at ICCAD 1997 to bound the crosstalk noise of an RC victim net by the steady state that an aggressor of constant slope would cause, a sum of resistances times coupling currents in the form of the Elmore delay, and to compute it in linear time for noise checks of whole chips.
prereqs: [rc-tree, elmore-delay, crosstalk-noise]
see_also: [miller-coupling-factor, parasitic-extraction, static-timing-analysis, asymptotic-waveform-evaluation, prima, backward-euler-method, matrix-exponential, positive-definite-matrix]
sources:
  - paper: "Anirudh Devgan, Efficient coupled noise estimation for on-chip interconnects, IEEE/ACM International Conference on Computer-Aided Design, 147 to 151, November 1997"
    title: Anirudh Devgan, Efficient coupled noise estimation for on-chip interconnects, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 147 to 151, 1997
    locator: the metric for RC trees and its claim to be an upper bound for RC circuits (DBLP gives pages 147 to 151, and some citations give 147 to 153; the section numbers were not checked)
  - paper: "Kenneth L. Shepard and Vinod Narayanan, Noise in deep submicron digital design, IEEE/ACM International Conference on Computer-Aided Design, 524 to 531, November 1996"
    title: Kenneth L. Shepard and Vinod Narayanan, Noise in deep submicron digital design, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 524 to 531, 1996
    locator: the static noise analysis setting in which a fast noise bound per net is used
  - paper: "Takayasu Sakurai, Closed-form expressions for interconnection delay, coupling, and crosstalk in VLSIs, IEEE Transactions on Electron Devices 40(1), 118 to 124, January 1993"
    title: Takayasu Sakurai, Closed-form expressions for interconnection delay, coupling, and crosstalk in VLSIs, IEEE Transactions on Electron Devices 40(1), 118 to 124, January 1993
    locator: the closed-form crosstalk height of two coupled distributed RC lines, an earlier estimate for one pair of lines
---

The Devgan noise metric is a fast upper bound on the crosstalk noise that switching neighbor wires couple into a quiet victim net. The victim is an [RC tree](/rc-tree/) held at 0 by its driver, and each aggressor couples into it through coupling capacitors. The metric at node $i$ is $V_i = \sum_k R_{ik} I_k$, where $I_k$ is the coupling capacitance at node $k$ times the aggressor slew rate and $R_{ik}$ is the resistance shared by the paths from the driver to $i$ and to $k$. It has the shape of the [Elmore delay](/elmore-delay/) with currents in place of capacitances, and the same two tree passes compute it in linear time. Under the stated linear model it is a proved upper bound on the peak noise for every aggressor waveform whose slope stays within the given rate.

## In plain words

When a wire switches, it pushes a small current into its quiet neighbor through the capacitance between them. That current flows through the neighbor's wire back to its driver and raises the voltage on the way. The bump is crosstalk noise.

The bump is largest when the switching wire keeps changing at its fastest rate for a long time. Then each current is constant, and the bump settles at the current times the resistance it crosses. The metric takes this settled level as the answer.

A real switching wire stops after a short time, so the real bump is lower. The metric is always on the safe side, often by a lot for fast edges. It costs only two passes over the wire, so a tool can check millions of nets and keep the few dangerous ones for an exact analysis.

## The problem

The input is a victim tree with nodes $0, \ldots, n-1$, where node 0 is the driver output and $p(k) < k$ is the parent of node $k \ge 1$. The value $r_0$ is the holding resistance of the quiet driver to ground, and $r_k$ is the wire resistance from $p(k)$ to $k$. Node $k$ has a capacitance $c_k$ to ground and coupling capacitances $C_{k,a}$ to aggressors $a$, and each aggressor voltage $u_a(t)$ has slope at most $s_a$ in absolute value. For a ramp of swing $V_{DD}$ and rise time $t_r$, $s_a = V_{DD} / t_r$.

With ideal aggressor sources, Kirchhoff's current law gives the linear system

$$ C v'(t) + G v(t) = B u'(t), \qquad v(0) = 0, $$

where $G$ is the conductance matrix of the tree, $C$ is the diagonal matrix of total node capacitance (ground plus coupling), and $B_{k,a} = C_{k,a}$. The output is a vector $V$ with $|v_i(t)| \le V_i$ for all $t$ and $i$, computed without solving the system in time.

## The algorithm

```pseudo id=main
DEVGAN-NOISE(p, r, Cc, s)
L1  for k ← 0 to n − 1 do I[k] ← Σ over couplings (C, a) of node k of C · s[a]
L2  for k ← n − 1 downto 1 do            ▷ children before parents, since p(k) < k
L3      I[p(k)] ← I[p(k)] + I[k]
L4  V[0] ← r[0] · I[0]                    ▷ the whole coupling current crosses the driver
L5  for k ← 1 to n − 1 do                 ▷ parents before children
L6      V[k] ← V[p(k)] + r[k] · I[k]
L7  return V
```

After line L3, $I[k]$ is the total coupling current injected in the subtree of $k$, which is the current that crosses the resistance $r_k$ in the settled state. Line L6 adds the drop across that resistance to the voltage of the parent. This is exactly the downstream form of the Elmore delay, with injected currents in place of downstream capacitances.

## Example

Units are kΩ, fF, ps and V, so a current in fF V/ps is in mA. The victim has a driver node 0 with $r_0 = 1$ and $c_0 = 5$, a branch node 1 with $r_1 = 0.5$ and $c_1 = 10$, and two sinks, node 2 under node 1 with $r_2 = 0.5$ and $c_2 = 10$, and node 3 under node 1 with $r_3 = 1$ and $c_3 = 15$. One aggressor couples 10 fF into node 1 and 10 fF into node 2. It rises by 1 V in $t_r = 50$ ps, so $s = 0.02$ V/ps.

| step | node 0 | node 1 | node 2 | node 3 |
|---|---|---|---|---|
| L1: $I_k = C_{k} s$ | 0 | 0.2 | 0.2 | 0 |
| L2 to L3: subtree current | 0.4 | 0.4 | 0.2 | 0 |
| L4 to L6: $V$ | $1 \cdot 0.4 = 0.4$ | $0.4 + 0.5 \cdot 0.4 = 0.6$ | $0.6 + 0.5 \cdot 0.2 = 0.7$ | $0.6 + 1 \cdot 0 = 0.6$ |

The exact peak of $|v_i(t)|$ comes from the exact solution of the linear system, piece by piece over the ramp and after it. The table compares it with the metric for four rise times. The metric scales as $1 / t_r$.

| $t_r$ (ps) | metric at node 2 (V) | exact peak at nodes 0, 1, 2, 3 (V) | peak / metric |
|---|---|---|---|
| 10 | 3.5 | 0.223, 0.364, 0.458, 0.233 | 0.08 to 0.13 |
| 50 | 0.7 | 0.170, 0.260, 0.318, 0.217 | 0.36 to 0.45 |
| 200 | 0.175 | 0.088, 0.133, 0.156, 0.130 | 0.87 to 0.89 |
| 1000 | 0.035 | 0.020, 0.030, 0.035, 0.030 | 1.00 |

The Elmore delay of node 2, with total node capacitances 5, 20, 20 and 15 fF, is 97.5 ps. For a rise time much longer than that, the metric is almost exact. For a rise time much shorter, it is pessimistic by a large factor: at 10 ps the metric at node 2 is 3.5 V, while the true peak is 0.46 V, and a step can never couple more than the charge sharing limit $C_c / (C_c + C_g)$ of the supply. Node 3 has no coupling of its own, yet its noise is nonzero, because the current of the other nodes crosses the shared resistance $r_0 + r_1$.

## Correctness

The [full proof](proofs/correctness.md) has four parts.

**The bound.** The matrix $-C^{-1}G$ has nonnegative entries off the diagonal, so $e^{-C^{-1}G t}$ has nonnegative entries for every $t \ge 0$. The solution is $v(t) = \int_0^t e^{-C^{-1}G(t - \tau)} C^{-1} B u'(\tau)\, d\tau$. Replacing $|u'|$ by its bound $s$ and extending the integral to infinity can only increase each entry, and $\int_0^\infty e^{-C^{-1}G\sigma} d\sigma = G^{-1} C$. So $|v(t)| \le G^{-1} B s$ entry by entry. With one rising aggressor, also $v(t) \ge 0$.

**The tree form.** $G^{-1}$ is the matrix of shared path resistances $R_{ik}$, so $G^{-1} B s = \sum_k R_{ik} I_k$, and the two passes compute this sum by the same exchange of sums that proves the downstream Elmore formula.

**Tightness.** For an aggressor whose slope stays at $s$ forever, $v(t) = (I - e^{-C^{-1}Gt}) V$ tends to $V$. So no bound that uses only the slopes can be smaller. For one node and a ramp of rise time $t_r$, the peak is exactly $V (1 - e^{-t_r / \tau})$ with $\tau = r_0 (c_0 + C_c)$.

**Discrete version.** Backward Euler with any step $h$ keeps the bound exactly. The matrix $C + hG$ is strictly diagonally dominant with nonpositive entries off the diagonal, so its inverse has nonnegative entries, and $|v_j| \le V$ implies $|v_{j+1}| \le (C + hG)^{-1}(CV + hGV) = V$.

What is proved is the bound under the linear model. What is measured is the tightness. On 80 random trees of 1 to 5 nodes with two aggressors (seed 1997, toy inputs, not benchmark results), the ratio of exact peak to metric stayed below 0.2 for rise times of 1/50 of the time constant scale, and reached above 0.95 for rise times 50 times that scale.

## Complexity

Line L1 reads each coupling capacitor once, and lines L2 to L6 do constant work per node, so the time is $O(n + m)$ for $n$ nodes and $m$ coupling capacitors. The extra space is the two arrays $I$ and $V$, $O(n)$. For a chip, the cost is linear in the size of the extracted parasitic network, which is why the metric can screen every net. An exact transient solve of one net costs a sparse factorization and one solve per time step, and a moment-matching model such as [AWE](/asymptotic-waveform-evaluation/) or [PRIMA](/prima/) costs a few solves with the full network.

## Properties

- **Upper bound, not an estimate.** Under the linear model with ideal aggressors, $|v_i(t)| \le V_i$ for all $t$, with no condition on alignment of aggressors, their direction or the shape of their waveform, other than the slope bound.
- **Linear in the aggressors.** $V$ is a sum of one term per coupling capacitor, so the metric of several aggressors is the sum of their separate metrics, which is the worst case when they switch at the same time in the worst directions.
- **Insensitive to grounded capacitance.** $c_k$ does not enter $V$. Adding ground capacitance slows the response and lowers the true peak, but not the bound.
- **Monotone in resistance and coupling.** $V$ grows with every $r_k$ and every $C_{k,a}$, and grows as $1 / t_r$.
- **Exact for slow aggressors.** When $t_r$ is much longer than the time constants of the victim, the true peak is close to $V$.

## Variants and improvements

- **RC meshes.** The bound $|v| \le G^{-1} B s$ holds for any resistive network with grounded capacitors and a path to ground, for example a net with a loop. It then needs one linear solve with $G$ in place of the two passes.
- **Finite rise time corrections.** Many later metrics multiply $V_i$ by a factor such as $1 - e^{-t_r / T_i}$ with an Elmore time constant $T_i$, or fit two poles to the first moments. These are closer to the true peak for fast edges. They are estimates, and they are no longer proved bounds in general.
- **Pulse width.** Noise checks also need the width of the bump, because a gate filters a short pulse. Moment-based metrics estimate the width; the Devgan metric gives only the height.
- **Exact reduced models.** [PRIMA](/prima/) gives a passive reduced model of the coupled network, and its transient solve gives the waveform with an error that can be controlled, at a much higher cost.
- **Timing windows.** In a [static timing analysis](/static-timing-analysis/) flow, aggressors that cannot switch together inside the victim's sensitive window are dropped from the sum, which removes much of the pessimism of the worst case alignment.
- **Effect on delay.** When the victim also switches, coupling changes its delay. That effect is usually modeled with the [Miller coupling factor](/miller-coupling-factor/) and is a different question.

## When to use it

Use it as the first filter in a chip-level noise check: compute $V$ for every net from the extracted parasitics, accept the nets whose bound is below the noise margin of their receivers, and send only the others to a more accurate analysis. Use it also inside routing and buffering tools, where a cheap and safe measure guides spacing, shielding and repeater insertion. Do not use it to sign off a net that fails the bound: the failure may be only pessimism, especially for fast aggressors on long couplings.

## Pitfalls

- **Fast edges.** The bound grows as $1 / t_r$ without limit, while the real peak cannot exceed the charge sharing level. With sharp edges the metric can report several times the supply voltage, as in the example at 10 ps.
- **The driver is not a resistor.** The holding resistance $r_0$ is a linearization of a transistor. A weak driver or a driver in a state with high output resistance gives much larger noise, and the bound is only as good as $r_0$.
- **Ideal aggressors.** The model treats aggressor voltages as given. In reality the victim loads the aggressor, which usually lowers the noise, so this is a safe simplification, but a model that drives the aggressor through its own resistance needs a different analysis.
- **Inductance.** For long wide wires the response can overshoot, and an RC bound does not apply.
- **Noise on noise.** The metric gives the noise at the victim wire. Whether the noise flips a latch depends on the receiver, the pulse width and the propagation through gates, which this metric does not model.
- **Units.** Coupling capacitance times slew rate is a current. Mixing fF with ns and kΩ gives values off by factors of 1000.

## Implementations

## History

Before the metric, designers bounded coupling noise by the charge sharing ratio $C_c / (C_c + C_g)$, which ignores the driver that holds the victim, or by closed forms for one pair of uniform lines such as those of Sakurai (1993). Shepard and Narayanan (1996) described the static noise analysis of whole chips, which needs a fast and safe measure for each net. Devgan (1997) gave the metric for RC trees, explained it as the steady state of an infinitely long ramp, and noted that it is an upper bound for RC circuits that is pessimistic for fast aggressors. The metric became a standard screen in noise analysis tools, and later work refined it with time constants and pulse widths.

## References
