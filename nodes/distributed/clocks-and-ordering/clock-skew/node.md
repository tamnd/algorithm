---
tag: 75906Q
kind: definition
slug: clock-skew
name: Clock skew
aliases:
- clock offset
area: distributed/clocks-and-ordering
level: intro
summary: The difference between the readings of two clocks at the same real time. Precision bounds the skew between any two clocks; accuracy bounds the error of each clock against a time standard.
prereqs: [clock-drift]
see_also: [clock-drift, clock-synchronization, clock-synchronization-lower-bound, cristian-algorithm, berkeley-algorithm, ntp, truetime, monotonic-clock]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6 (the skew of adjusted clocks and the lower bound on it)
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.3 (skew, drift, and internal versus external synchronization)
  - paper: doi:10.1007/BF01784024
    title: Flaviu Cristian, Probabilistic clock synchronization, Distributed Computing 3(3), 1989
    locator: the synchronization condition and the drift model
---

*Clock skew* is the difference between the readings of two clocks at the same real time. It is a value error between two clocks. [Clock drift](/clock-drift/), its pair, is a rate error of one clock. Two bounds on skew name the two goals of [clock synchronization](/clock-synchronization/): *precision* bounds the skew between any two clocks of a system, and *accuracy* bounds the error of each clock against a time standard such as UTC.

## Definition

**Model.** There are $n$ processes. Real time $t$ is not visible to them. Process $i$ reads an adjusted clock $C_i(t)$, made from a hardware clock with a drift bound $\rho$ (see [clock drift](/clock-drift/)) and an adjustment that the synchronization algorithm sets.

**Skew.** The skew of clocks $i$ and $j$ at real time $t$ is
$$\sigma_{ij}(t) = C_i(t) - C_j(t).$$
Its absolute value is the distance between the two readings. Many texts call $\sigma_{ij}$ the *offset* of $C_i$ relative to $C_j$. NTP uses the word offset in this sense, for the difference between a server clock and the client clock.

**Precision (internal synchronization).** The clocks have precision $\pi$ over a time interval $I$ when
$$|C_i(t) - C_j(t)| \le \pi \quad \text{for all } i, j \text{ and all } t \in I.$$

**Accuracy (external synchronization).** The clocks have accuracy $\alpha$ over $I$ against a reference time $S(t)$ when
$$|C_i(t) - S(t)| \le \alpha \quad \text{for all } i \text{ and all } t \in I.$$
Often $S(t) = t$, or $S$ is UTC.

**Lemma 1.** Accuracy $\alpha$ implies precision $2\alpha$. The converse is false.

*Proof.* By the triangle inequality, $|C_i(t) - C_j(t)| \le |C_i(t) - S(t)| + |S(t) - C_j(t)| \le 2\alpha$. For the converse, let every clock read $S(t) + 3600$. The precision is 0, but no accuracy below 3600 s holds. $\square$

**Lemma 2 (skew between resynchronizations).** Assume that all clocks are $\rho$-bounded, that a resynchronization every $R$ seconds of real time sets the adjusted clocks of all processes at the same real time $t_k$, and that right after it $|C_i(t_k) - C_j(t_k)| \le \varepsilon$ for all $i, j$. Between resynchronizations the adjustments do not change. Then the precision is
$$\pi = \varepsilon + 2\rho R.$$

*Proof.* Let $t_k \le t < t_k + R$. Between $t_k$ and $t$ the adjustments are constant, so $C_i(t) - C_i(t_k) = H_i(t) - H_i(t_k)$, and the same for $j$. By the divergence lemma on the page [clock drift](/clock-drift/), the skew changes by at most $2\rho(t - t_k) < 2\rho R$. So $|C_i(t) - C_j(t)| \le \varepsilon + 2\rho R$. $\square$

Real protocols do not reset all clocks at the same real time. If the resets of one round fall in a window of length $W$, the same argument adds a term of at most $2\rho W$ and the error of the round itself. The formula above is the part that comes from drift alone.

## Examples and non-examples

- **Skew, precision and accuracy at one moment.** At real time $t = 10.001$ s, three clocks read $10.000$, $10.004$ and $9.997$. The largest skew is $10.004 - 9.997 = 0.007$ s. The largest error against real time is $0.004$ s (the third clock). The precision $0.007$ is within the $2 \cdot 0.004 = 0.008$ of Lemma 1.
- **Choosing the period.** With $\varepsilon = 1$ ms and $\rho = 15$ ppm, a period $R = 64$ s gives $\pi = 1 + 2 \cdot 15 \cdot 10^{-6} \cdot 64 \cdot 1000 = 2.92$ ms. To keep $\pi \le 5$ ms, the period must satisfy $2\rho R \le 4$ ms, that is $R \le 133.3$ s.
- **The bound is tight.** If one clock runs at rate $1 + \rho$ and the other at $1 - \rho$, and they start 1 ms apart with the fast one ahead, then after 64 s they are exactly 2.92 ms apart.
- **Non-example: synchronized but wrong.** All clocks of a cluster agree to within 1 ms, but all of them are one hour behind UTC. The precision is good and the accuracy is bad. Internal synchronization, as in the [Berkeley algorithm](/berkeley-algorithm/), gives only this.
- **Non-example: drift.** Two clocks that read the same value now but run at different rates have zero skew now and nonzero drift. Their skew will grow.

## Related definitions

- **[Clock drift](/clock-drift/).** A rate error of one clock. Drift makes skew grow by at most $2\rho$ per second.
- **[Clock synchronization](/clock-synchronization/).** The problem of keeping the skew (internal) or the error against a standard (external) below a bound.
- **[Lower bound on skew](/clock-synchronization-lower-bound/).** With message delays known only to lie in an interval of width $u$, no algorithm can guarantee a skew below $(1 - 1/n)\,u$ for $n$ drift-free clocks (Lundelius and Lynch 1984).
- **The uncertainty $\varepsilon$ of [TrueTime](/truetime/).** A bound on the accuracy of one server clock, made visible to the program as an interval.
- **[Monotonic clock](/monotonic-clock/).** A clock that the system corrects by slewing, so a skew is removed slowly and never by a step back.

## References
