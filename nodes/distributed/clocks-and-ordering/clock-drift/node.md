---
tag: SP8EAN
kind: definition
slug: clock-drift
name: Clock drift
aliases:
- clock rate error
area: distributed/clocks-and-ordering
level: intro
summary: The rate error of a hardware clock. A clock with drift bound ρ gains or loses at most ρ seconds per second, so two such clocks move apart by at most 2ρ seconds per second.
prereqs: []
see_also: [clock-skew, monotonic-clock, clock-synchronization, cristian-algorithm, ntp, truetime, lamport-clocks]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6 (hardware clocks and their drift) and Chapter 13 (clock synchronization with drift)
  - paper: doi:10.1007/BF01784024
    title: Flaviu Cristian, Probabilistic clock synchronization, Distributed Computing 3(3), 1989
    locator: the model of the hardware clocks, with the drift bound ρ
  - url: https://www.rfc-editor.org/rfc/rfc5905
    title: David Mills, Jim Martin, Jack Burbank and William Kasch, RFC 5905, Network Time Protocol Version 4, 2010
    locator: the constant PHI (frequency tolerance of 15 ppm) and the dispersion that grows at rate PHI
  - url: https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett
    title: James C. Corbett and others, Spanner, Google's globally distributed database, OSDI 2012
    locator: Section 3 (a worst case drift of 200 microseconds per second, applied between polls 30 seconds apart)
---

*Clock drift* is the difference between the rate of a hardware clock and the rate of real time. A clock with a drift bound $\rho$ gains or loses at most $\rho$ seconds in each second of real time, so two such clocks can move apart by up to $2\rho$ seconds per second. Drift is a rate. [Clock skew](/clock-skew/) is a difference of two clock values at one moment. Drift is the reason that [clock synchronization](/clock-synchronization/) must run again and again, not only once.

## Definition

**Model.** Real time $t$ is a real number that no process can read. Process $i$ of $n$ processes has a *hardware clock* $H_i : \mathbb{R} \to \mathbb{R}$. The process can read $H_i(t)$ at time $t$, but it cannot change $H_i$. A clock that a process can adjust is a separate thing, the *logical* or *adjusted* clock $C_i(t) = H_i(t) + \mathrm{adj}_i(t)$.

**Drift bound.** Let $0 \le \rho < 1$. The clock $H_i$ is *$\rho$-bounded* when, for all real times $s \le t$,
$$(1-\rho)(t-s) \;\le\; H_i(t) - H_i(s) \;\le\; (1+\rho)(t-s).$$
If $H_i$ is differentiable, this is the same as $1 - \rho \le dH_i/dt \le 1 + \rho$ at each time. The *drift* of $H_i$ at time $t$ is $dH_i/dt - 1$, and $\rho$ is a bound on its absolute value. A clock with $\rho = 0$ runs at the rate of real time and is *drift-free*.

The unit is a dimensionless ratio, often given in parts per million (ppm). One ppm is one microsecond per second, about 86.4 ms per day.

Some texts write the lower bound as $(t-s)/(1+\rho)$ instead of $(1-\rho)(t-s)$. The two forms differ by at most $\rho^2 (t-s)$, so for the small values of real clocks the choice does not matter. A page or a paper must say which form it uses.

**Lemma (divergence).** If $H_i$ and $H_j$ are both $\rho$-bounded, then for all $s \le t$,
$$\bigl| (H_i(t) - H_j(t)) - (H_i(s) - H_j(s)) \bigr| \;\le\; 2\rho\,(t-s).$$

*Proof.* The difference on the left is $(H_i(t) - H_i(s)) - (H_j(t) - H_j(s))$. The first term is at most $(1+\rho)(t-s)$ and the second is at least $(1-\rho)(t-s)$, so the difference is at most $2\rho(t-s)$. With $i$ and $j$ exchanged, the same argument gives at least $-2\rho(t-s)$. $\square$

In the same way, $|(H_i(t) - t) - (H_i(s) - s)| \le \rho (t-s)$: the error of one clock against real time grows by at most $\rho$ per second. So after a synchronization that leaves two clocks within $\varepsilon$ of each other, they are within $\varepsilon + 2\rho R$ of each other $R$ seconds later, if nobody corrects them. The page on [clock skew](/clock-skew/) uses this to choose the period of resynchronization.

## Examples and non-examples

- **NTP's tolerance.** [NTP](/ntp/) (RFC 5905) assumes a frequency tolerance $\rho = 15$ ppm, the constant PHI. One such clock can be wrong by up to $15 \cdot 10^{-6} \cdot 86400 = 1.296$ s after one day without correction. Two such clocks can move apart by up to $2.592$ s in a day.
- **Spanner.** The time daemons of Spanner assume a worst case drift of 200 microseconds per second. Between polls 30 s apart, this gives $200 \cdot 10^{-6} \cdot 30 = 6$ ms of possible error, which is the slope of the sawtooth of the uncertainty $\varepsilon$ in [TrueTime](/truetime/).
- **A fast clock.** The clock $H(t) = 1.00002\,t + 5$ has a constant drift of $2 \cdot 10^{-5}$, that is 20 ppm. It is $\rho$-bounded for each $\rho \ge 20$ ppm. At $t = 3600$ its error is $5 + 0.072 = 5.072$ s: 5 s of offset that it had at time 0, and 72 ms that it gained by drift.
- **Non-example: an offset.** The clock $H(t) = t + 5$ is 5 s wrong, but its drift is 0. An offset is a value error, not a rate error. Its relation to other clocks is [clock skew](/clock-skew/).
- **Non-example: a step.** When software sets a clock back by 2 s, the clock is not $\rho$-bounded over that moment for any $\rho < 1$, since $H(t) - H(s)$ is negative. Steps come from adjustment, not from drift. A [monotonic clock](/monotonic-clock/) never steps back.
- **Non-example: a logical clock.** A [Lamport clock](/lamport-clocks/) counts events. It has no rate, so drift does not apply to it.

## Related definitions

- **[Clock skew](/clock-skew/)** is the difference $C_i(t) - C_j(t)$ of two clocks at one real time. Drift is a rate error of one clock. By the lemma above, drift makes skew grow by at most $2\rho$ per second.
- **Offset** of one clock is $C_i(t) - t$, its error against real time.
- **Frequency error and wander.** The rate of a quartz oscillator changes with temperature and age, so the drift is not a constant. The bound $\rho$ covers all of these changes. NTP measures the current frequency error and corrects it, which leaves a smaller residual drift.
- **[Monotonic clock](/monotonic-clock/).** A clock that the system can slow or speed up a little (slewing) but never step back. It still drifts.
- **[Clock synchronization](/clock-synchronization/).** The problem of keeping clocks close in spite of drift and unknown message delays.

## References
