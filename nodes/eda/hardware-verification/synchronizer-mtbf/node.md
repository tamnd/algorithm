---
tag: EVBTDW
kind: definition
slug: synchronizer-mtbf
name: Synchronizer mean time between failures
aliases:
- synchronizer MTBF
- metastability MTBF
area: eda/hardware-verification
level: core
summary: MTBF = e^(t/tau) / (T_w f_c f_d), the mean time between metastability failures of a flip-flop synchronizer with resolution time t and clock and data rates f_c and f_d.
prereqs: [setup-and-hold-constraints, poisson-distribution]
see_also: [clock-domain-crossing-verification, setup-and-hold-constraints, poisson-distribution, black-equation, static-timing-analysis]
sources:
  - paper: doi:10.1109/JSSC.1980.1051359
    title: H. J. M. Veendrick, The behavior of flip-flops used as synchronizers and prediction of their failure rate, IEEE Journal of Solid-State Circuits SC-15(2), 169 to 176, 1980
    locator: the small-signal analysis of the cross-coupled latch, in which the imbalance grows exponentially with a time constant set by the capacitance and the transconductance, and the resulting prediction of the failure rate of a synchronizer, compared with measurements
  - paper: doi:10.1109/T-C.1973.223730
    title: T. J. Chaney and C. E. Molnar, Anomalous behavior of synchronizer and arbiter circuits, IEEE Transactions on Computers C-22(4), 421 to 422, 1973
    locator: the observation that a flip-flop driven by asynchronous inputs can stay in a metastable state for an unbounded time
  - paper: doi:10.1109/MDT.2011.113
    title: R. Ginosar, Metastability and synchronizers, a tutorial, IEEE Design and Test of Computers 28(5), 23 to 35, 2011
    locator: the derivation of the failure rate from the exponential resolution law, the parameters tau and T_W and their measurement, and the two-flip-flop synchronizer
  - book: isbn:9780470510827
    title: D. J. Kinniment, Synchronization and Arbitration in Digital Systems, Wiley, 2008
    locator: the chapters on metastability, its models and measurement, and synchronizer reliability
---

When a flip-flop samples a signal that is not synchronized to its clock, it sometimes samples the signal while it changes. The flip-flop then starts in a balanced state between 0 and 1 and needs extra time to fall to one side. A synchronizer gives it a fixed *resolution time* $t_r$ before the next stage reads its output. It fails when the flip-flop has not settled by then. The *mean time between failures* (MTBF) of the synchronizer is

$$\mathrm{MTBF} = \frac{e^{t_r / \tau}}{T_W \, f_c \, f_d},$$

where $f_c$ is the clock rate, $f_d$ is the rate of data transitions, and $\tau$ and $T_W$ are parameters of the flip-flop. The formula follows exactly from a simple model of how a latch leaves its balanced state, which this page derives. The model is an approximation of the circuit, and $\tau$ and $T_W$ are not computed from first principles but fitted to measurements. The structural rules that make a crossing between clock domains safe are on [clock domain crossing verification](/clock-domain-crossing-verification/).

## Definition

A flip-flop is clocked with period $T_c = 1 / f_c$. Its data input changes at random times with a mean of $f_d$ transitions per second. The flip-flop's output is read by the next stage $t_r$ seconds after the clock edge, where $t_r$ is the clock period minus the clock-to-output delay and the setup time of the next stage. A *synchronization failure* is a transition after which the output has not settled to a valid 0 or 1 within $t_r$. If failures occur at a long-run rate of $\lambda$ per second, the *MTBF* is $1 / \lambda$, the mean time between failures.

Some authors write $f_d$ as a data frequency with two transitions per period. Here it is the number of transitions per second. With the other convention the formula has an extra factor of 2.

**The exponential resolution model.** It makes four assumptions.

- **(M1) Linear start.** A data transition at time offset $\Delta t$ from the balance point of the clock edge leaves the latch with an initial voltage imbalance $v_0 = K \, \Delta t$, for a constant $K$. The balance point is the offset at which the latch is exactly balanced.
- **(M2) Exponential growth.** While $\lvert v \rvert < V_1$, the imbalance obeys $dv / dt = v / \tau$. This is the small-signal model of two cross-coupled inverters, with $\tau$ about the node capacitance divided by the transconductance. So $v(t) = v_0 \, e^{t / \tau}$.
- **(M3) Threshold.** The output is valid when $\lvert v \rvert \ge V_1$.
- **(M4) Uniform phase.** The offset of each data transition from the nearest clock edge is uniform over one clock period, because the data is not synchronized to the clock.

**Derivation.** By (M2) and (M3), a latch that starts at $0 < \lvert v_0 \rvert < V_1$ settles after the time $t_s$ with $\lvert v_0 \rvert e^{t_s / \tau} = V_1$, that is

$$t_s = \tau \ln \frac{V_1}{\lvert v_0 \rvert},$$

and a latch with $\lvert v_0 \rvert \ge V_1$ is valid at once. The function $t_s$ decreases in $\lvert v_0 \rvert$, so $t_s > t_r$ exactly when $\lvert v_0 \rvert < V_1 e^{-t_r / \tau}$. By (M1) this is the condition

$$\lvert \Delta t \rvert < \frac{V_1}{K} \, e^{-t_r / \tau}.$$

The set of offsets that fail is an interval of length $T_W e^{-t_r / \tau}$, where $T_W = 2 V_1 / K$ is called the *window*. By (M4), as long as this length is at most $T_c$, a single transition fails with probability

$$p = \frac{T_W e^{-t_r / \tau}}{T_c} = T_W \, f_c \, e^{-t_r / \tau}.$$

In a time $L$ there are on average $f_d L$ transitions. By linearity of expectation the mean number of failures is $f_d L \, p$, so the failure rate is

$$\lambda = T_W \, f_c \, f_d \, e^{-t_r / \tau},$$

and the MTBF is $1 / \lambda$, the formula of this page. Linearity needs no independence between transitions. If in addition the transitions form a Poisson process and their phases are independent, the failures are a thinned Poisson process of rate $\lambda$. Then the time between failures has the exponential distribution with mean $1 / \lambda$, and the number of failures in time $L$ has the [Poisson distribution](/poisson-distribution/) with mean $\lambda L$. A Monte Carlo run of the model with $10^6$ uniform offsets, $\tau = T_W = 20$ ps, $T_c = 1$ ns and $t_r = 0.1$ ns gave a failure fraction of $1.48 \times 10^{-4}$, against the predicted $p = 1.35 \times 10^{-4}$, which is within the sampling error of about $1.2 \times 10^{-5}$.

**What is proved and what is measured.** Given (M1) to (M4), the formula is exact. The constants are not derived. $\tau$ and $T_W$ are found by measurement: run the synchronizer with asynchronous data, count the outputs that are still not valid at several delays $t$ after the clock, and fit a straight line to $\ln \lambda(t) = \ln(T_W f_c f_d) - t / \tau$. The slope gives $\tau$ and the intercept gives $T_W$. Veendrick (1980) did this analysis and compared it with measurements on real flip-flops, and Ginosar (2011) describes the procedure. The assumptions are approximations that this page does not prove. (M1) and (M2) hold only near the balance point and once the latch is in its small-signal region, so the exponential law fits large $t_r$ well and small $t_r$ poorly. Real flip-flops have a master and a slave latch, and the measured $T_W$ depends on how the master hands an imbalance to the slave. $\tau$ grows at low supply voltage and changes with temperature and process corner, so the worst corner sets the MTBF.

## Examples and non-examples

- **A two-flip-flop synchronizer.** Take $\tau = 20$ ps, $T_W = 20$ ps, $f_c = 1$ GHz and $f_d = 10^8$ transitions per second. The denominator is $T_W f_c f_d = 2 \times 10^{6}$ per second. Each 20 ps of extra resolution time multiplies the MTBF by $e$.

| $t_r$ | $e^{t_r / \tau}$ | MTBF |
|---|---|---|
| 0.2 ns | $2.2 \times 10^{4}$ | 0.011 s |
| 0.5 ns | $7.2 \times 10^{10}$ | $3.6 \times 10^{4}$ s, about 10 hours |
| 0.9 ns | $3.5 \times 10^{19}$ | $1.7 \times 10^{13}$ s, about 550,000 years |
| 1.8 ns | $1.2 \times 10^{39}$ | $6.1 \times 10^{32}$ s |

With $t_r = 0.9$ ns, nearly a full clock period for the first flip-flop to settle, one transition fails with probability $p = 5.7 \times 10^{-22}$. The row for 1.8 ns is about what a third stage adds. That a chain of $N$ flip-flops gives $t_r \approx (N - 1)(T_c - t_{pd} - t_{su})$ is a common approximation, since a later stage that samples a slowly settling input can itself become balanced. It is not a consequence of the model.

- **Many synchronizers.** A chip with $n$ independent synchronizers fails at the sum of their rates, by linearity of expectation. Its MTBF is $1 / \sum_i \lambda_i$, so 1,000 synchronizers of the 10-hour row give an MTBF of 36 s.

- **Non-example: a synchronous path.** If the data comes from the same clock and [static timing analysis](/static-timing-analysis/) shows that the [setup and hold constraints](/setup-and-hold-constraints/) are met, the offset never falls near the balance point. (M4) fails, and the model predicts no failures. The formula does not apply.

- **Non-example: a fixed bad phase.** Two clocks with the same frequency and a fixed but unknown phase also break (M4). If the phase happens to put each data change near the balance point, every transition is at risk, and the MTBF can be far shorter than the formula says. Such clocks need a scheme that measures or adjusts the phase.

- **Non-example: wear-out.** The mean time to failure of a wire under electromigration, given by [Black's equation](/black-equation/), is a lifetime of a part that wears out. A synchronizer does not wear out. Its failures are random events at a constant rate.

## Related definitions

- [Setup and hold constraints](/setup-and-hold-constraints/) define the window around the clock edge where the data must be stable. A metastable flip-flop is one whose data changed in this window. $T_W$ is usually much smaller than the setup time plus the hold time, because most changes inside that window still resolve quickly.
- [Clock domain crossing verification](/clock-domain-crossing-verification/) checks that every crossing has a synchronizer and that the design is safe when the synchronizer adds one cycle of latency. The MTBF says how often the synchronizer itself breaks that assumption.
- The [Poisson distribution](/poisson-distribution/) gives the number of failures in a fixed time when transitions are independent.
- Chaney and Molnar (1973) showed that the time to leave the balanced state is not bounded. No synchronizer has an infinite MTBF. A design can only choose $t_r$ to make it long enough.

## References
