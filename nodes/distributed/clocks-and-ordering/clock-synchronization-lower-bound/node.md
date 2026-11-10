---
tag: 1YP4C2
kind: theorem
slug: clock-synchronization-lower-bound
name: Clock synchronization lower bound
aliases:
- Lundelius-Lynch bound
- Lundelius and Lynch lower bound
area: distributed/clocks-and-ordering
level: advanced
summary: With n drift-free clocks and message delays known only within an interval of length u, no algorithm can guarantee a skew below (1 − 1/n)u. An averaging algorithm reaches this bound.
history:
  year: 1984
  people: [Jennifer Lundelius, Nancy Lynch]
  note: Lundelius and Lynch proved the lower bound with the shifting argument and gave the matching averaging algorithm in Information and Control in 1984.
prereqs: [clock-synchronization]
see_also: [clock-synchronization, clock-skew, cristian-algorithm, ntp, berkeley-algorithm, asynchronous-model, synchronous-model]
sources:
  - paper: doi:10.1016/S0019-9958(84)80033-9
    title: Jennifer Lundelius and Nancy Lynch, An upper and lower bound for clock synchronization, Information and Control 62(2-3), 1984
    locator: pages 190 to 204 (the shifting lemma, the lower bound and the averaging algorithm)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, the section on clock synchronization (shifting executions and the bound (1 − 1/n)u)
  - paper: doi:10.1145/28869.28876
    title: T. K. Srikanth and Sam Toueg, Optimal clock synchronization, Journal of the ACM 34(3), 1987
    locator: the whole paper (fault-tolerant synchronization with optimal accuracy; DOI to be checked)
  - paper: doi:10.1016/0022-0000(86)90028-0
    title: Danny Dolev, Joseph Y. Halpern and H. Raymond Strong, On the possibility and impossibility of achieving clock synchronization, Journal of Computer and System Sciences 32(2), 1986
    locator: the whole paper (the bound n > 3f without authentication; DOI to be checked)
---

The *clock synchronization lower bound* of Lundelius and Lynch (1984) says that $n$ processes with drift-free clocks, whose message delays are known only to lie in an interval $[d - u, d]$, cannot always bring their clocks closer than $(1 - 1/n)u$. The proof shifts processes in real time without changing anything that they can observe. The bound is tight: if each process estimates the other clocks with the middle delay $d - u/2$ and moves to the average, the skew is at most $(1 - 1/n)u$.

## Statement

**Model.** There are $n \ge 2$ processes $p_0, \dots, p_{n-1}$ on a complete network with reliable channels. Process $p_i$ has a hardware clock $H_i(t) = t + c_i$ with no drift and an unknown offset $c_i$. Each message from $p_i$ to $p_j$ takes a delay in $[d - u, d]$, where $0 \le u \le d$ are known. An execution is *admissible* if all its delays lie in this interval. A process acts only on its *view*: its hardware clock readings and the messages it receives, with their local receipt times. When the algorithm ends, $p_i$ fixes an adjustment $\mathrm{adj}_i$, and its adjusted clock is $C_i(t) = H_i(t) + \mathrm{adj}_i$. Write $A_i = c_i + \mathrm{adj}_i$, so that $C_i(t) = t + A_i$. The *skew* of an execution is $\max_{i,j} |A_i - A_j|$.

**Theorem (lower bound).** For every deterministic algorithm, if every admissible execution has skew at most $\varepsilon$, then
$$\varepsilon \ge \left(1 - \frac{1}{n}\right) u.$$

**Theorem (upper bound).** The averaging algorithm below has skew at most $(1 - 1/n)u$ in every admissible execution.

*Averaging algorithm.* Each process sends its clock value $V$ to every other process. When $p_i$ receives $V$ from $p_j$ at local time $R$, it estimates $H_j - H_i$ as $V + (d - u/2) - R$. Then $p_i$ sets $\mathrm{adj}_i$ to the sum of its $n - 1$ estimates divided by $n$, which is the average of the estimates with its own difference 0 included.

## In plain words

A message can be slow or fast, and the receiver cannot tell which. So a clock that is a little ahead, with a slow message, looks the same as a clock that is a little behind, with a fast message.

With two computers, take one run, and then a second run in which one computer is ahead by the full uncertainty and the messages make up for it. Neither computer sees any difference, so both do the same thing in both runs. But the gap between their clocks changes by the full uncertainty, so in one of the two runs the clocks end at least half of it apart.

With more computers, a chain of such runs gives a larger bound, which comes close to the full uncertainty when there are many computers. A simple rule, to guess the middle delay and take the average, reaches this bound exactly.

## Proof

**Shifting.** Let $\alpha$ be an execution and $x = (x_0, \dots, x_{n-1})$ real numbers. The *shift* $\mathrm{shift}(\alpha, x)$ is the execution in which every event of $p_i$ happens $x_i$ earlier in real time, at the same local time. So its offset becomes $c_i' = c_i + x_i$, and a message from $p_i$ to $p_j$ with delay $\delta$ gets the delay $\delta' = \delta + x_i - x_j$, since it is sent $x_i$ earlier and received $x_j$ earlier.

**Lemma 1 (shifting lemma).** In $\mathrm{shift}(\alpha, x)$, every process has the same view as in $\alpha$, and $A_i' = A_i + x_i$.

*Proof.* Each event of $p_i$ happens at the same local time and with the same messages, so the view is the same. The algorithm is deterministic, so $p_i$ chooses the same $\mathrm{adj}_i$. Then $A_i' = c_i + x_i + \mathrm{adj}_i = A_i + x_i$. $\square$

The shift need not be admissible. The proofs below choose $x$ so that every new delay still lies in $[d - u, d]$.

**The case $n = 2$.** Let $\alpha$ be the execution with $c_0 = c_1 = 0$ in which every message from $p_0$ to $p_1$ takes $d - u$ and every message from $p_1$ to $p_0$ takes $d$. Let $\beta = \mathrm{shift}(\alpha, (u, 0))$. In $\beta$, messages from $p_0$ to $p_1$ take $d - u + u - 0 = d$, and messages from $p_1$ to $p_0$ take $d + 0 - u = d - u$. So $\beta$ is admissible. By Lemma 1, $A_0^\beta = A_0^\alpha + u$ and $A_1^\beta = A_1^\alpha$, so
$$(A_0^\beta - A_1^\beta) - (A_0^\alpha - A_1^\alpha) = u.$$
Two real numbers that differ by $u$ cannot both have absolute value below $u/2$. So one of $\alpha$ and $\beta$ has skew at least $u/2 = (1 - 1/2)u$. $\square$

**The general case.** Let $\alpha_0$ be the execution with all $c_i = 0$ in which a message from $p_i$ to $p_j$ takes $d - u$ when $i < j$ and $d$ when $i > j$. For $k = 1, \dots, n-1$, let $\alpha_k = \mathrm{shift}(\alpha_0, x^{(k)})$, where $x^{(k)}_i = u$ for $i < k$ and $x^{(k)}_i = 0$ for $i \ge k$.

**Lemma 2.** Each $\alpha_k$ is admissible.

*Proof.* A message from $p_i$ to $p_j$ gets the new delay $\delta + x_i - x_j$. If $i$ and $j$ are both below $k$ or both at least $k$, then $x_i = x_j$ and the delay does not change. If $i < k \le j$, then $i < j$, so $\delta = d - u$ and the new delay is $d - u + u = d$. If $j < k \le i$, then $i > j$, so $\delta = d$ and the new delay is $d - u$. All delays stay in $[d - u, d]$. $\square$

Now let the algorithm have skew at most $\varepsilon$ in every admissible execution, and write $A_i$ for the offsets in $\alpha_0$. Fix $k$ with $1 \le k \le n - 1$. In $\alpha_k$, by Lemma 1, $p_{k-1}$ has offset $A_{k-1} + u$, since $x^{(k)}_{k-1} = u$, and $p_k$ has offset $A_k$, since $x^{(k)}_k = 0$. The skew bound in $\alpha_k$ gives $A_{k-1} + u - A_k \le \varepsilon$, that is
$$A_k \ge A_{k-1} + u - \varepsilon.$$
Adding these inequalities for $k = 1, \dots, n-1$ gives $A_{n-1} \ge A_0 + (n-1)(u - \varepsilon)$. The skew bound in $\alpha_0$ gives $A_{n-1} - A_0 \le \varepsilon$. So $(n-1)(u - \varepsilon) \le \varepsilon$, which is $n\varepsilon \ge (n-1)u$, and $\varepsilon \ge (1 - 1/n)u$. $\square$

**The upper bound.** Run the averaging algorithm in any admissible execution. The value $V = H_j(s)$ that $p_j$ sends at real time $s$ reaches $p_i$ at real time $s + \delta_{ji}$, when $p_i$ reads $R = s + \delta_{ji} + c_i$. So the estimate is
$$V + d - \tfrac{u}{2} - R = (c_j - c_i) + e_{ji}, \qquad e_{ji} = d - \tfrac{u}{2} - \delta_{ji} \in \left[-\tfrac{u}{2}, \tfrac{u}{2}\right].$$
Then $A_i = c_i + \frac{1}{n}\sum_{j \ne i} (c_j - c_i + e_{ji}) = \bar c + \frac{1}{n}\sum_{j \ne i} e_{ji}$, where $\bar c$ is the mean of the $c_j$. For two processes $p_i$ and $p_k$,
$$n(A_i - A_k) = (e_{ki} - e_{ik}) + \sum_{j \notin \{i, k\}} (e_{ji} - e_{jk}).$$
This is a sum of $1 + (n - 2) = n - 1$ terms, each a difference of two numbers in $[-u/2, u/2]$, so each of absolute value at most $u$. Hence $|A_i - A_k| \le (n-1)u/n$. $\square$

The code of this page builds the executions $\alpha_0, \dots, \alpha_{n-1}$, checks that every process has the same view in all of them, and checks both bounds for the averaging algorithm and for other algorithms in seeded runs.

## Consequences

- **The uncertainty, not the delay, limits precision.** The bound depends on $u$, not on $d$. A long but fixed delay costs nothing, which is why [PTP](/precision-time-protocol/) works hard to remove the variable part of the delay.
- **Two processes.** For a client and a server, the best guarantee is $u/2$. [Cristian's algorithm](/cristian-algorithm/) and [NTP](/ntp/) reach the matching bound $\delta/2$ for one round trip, where the round trip itself gives the uncertainty.
- **More processes help only a little.** The bound grows from $u/2$ for two processes toward $u$ for many. Averaging cannot remove the uncertainty of the delays.
- **External synchronization.** A reference clock is just one more process whose adjustment is 0, so the same shifting argument applies to it.
- **Fault tolerance costs more.** With $f$ Byzantine processes, Dolev, Halpern and Strong (1986) show that $n > 3f$ is needed without authentication, and Srikanth and Toueg (1987) give algorithms with optimal accuracy under drift and faults. These results are cited, not proved here.

## Tightness

The averaging algorithm reaches the bound exactly. In the execution $\alpha_0$ of the proof, $e_{ji} = d - u/2 - (d - u) = u/2$ when $j < i$, and $e_{ji} = -u/2$ when $j > i$. So $p_0$ gets $n(A_0 - \bar c) = -(n-1)u/2$ and $p_{n-1}$ gets $n(A_{n-1} - \bar c) = (n-1)u/2$, and the skew is $(n-1)u/n$.

**Example.** Let $n = 3$, $d = 10$, $u = 4$, with offsets $c = (0, 2, -1)$ and delays (rows are senders) $(\cdot, 8, 9)$, $(10, \cdot, 6)$, $(7, 10, \cdot)$. The middle delay is 8, so $e_{ji} = 8 - \delta_{ji}$. Process $p_0$ gets $e_{10} = -2$ and $e_{20} = 1$; $p_1$ gets $e_{01} = 0$ and $e_{21} = -2$; $p_2$ gets $e_{02} = -1$ and $e_{12} = 2$. With $\bar c = 1/3$, the offsets are $A = (0, -1/3, 2/3)$, so the skew is 1, below the bound $(1 - 1/3) \cdot 4 = 8/3$.

## History

Jennifer Lundelius and Nancy Lynch published the bound and the averaging algorithm in Information and Control in 1984. Their shifting argument became a standard tool for lower bounds in partly synchronous systems. Attiya and Welch present it in Chapter 6 of their textbook. Work on fault-tolerant clock synchronization in the same years, among it Dolev, Halpern and Strong (1986) and Srikanth and Toueg (1987), studied the cost of faults and of drift.

## References
