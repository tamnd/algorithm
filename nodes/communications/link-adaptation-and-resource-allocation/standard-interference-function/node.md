---
tag: 0TZQAR
kind: theorem
slug: standard-interference-function
name: Yates standard interference function theorem
aliases:
- standard interference function
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "A standard interference function is positive, monotone and scalable. Yates showed it has at most one fixed point, and if any power vector meets all targets, p <- I(p) converges to it from every start."
prereqs: [fixed-point-iteration, foschini-miljanic-power-control]
see_also: [foschini-miljanic-power-control, max-min-sinr-power-control, geometric-programming-power-control, perron-frobenius-theorem, banach-fixed-point-theorem, knaster-tarski-theorem, near-far-problem, max-min-fairness]
sources:
  - paper: doi:10.1109/49.414651
    title: "Roy D. Yates, A framework for uplink power control in cellular radio systems, IEEE Journal on Selected Areas in Communications 13(7), 1995, pages 1341 to 1347"
    locator: "the definition of a standard interference function (positivity, monotonicity, scalability), the theorem that a fixed point is unique, the synchronous and asynchronous convergence theorems, and the examples (fixed assignment, minimum power base station assignment, macro diversity, power limits)"
  - paper: doi:10.1109/25.260747
    title: "Gerard J. Foschini and Zoran Miljanic, A simple distributed autonomous power control algorithm and its convergence, IEEE Transactions on Vehicular Technology 42(4), 1993, pages 641 to 646"
    locator: "Section III (the linear iteration that is the first example of a standard interference function)"
---

A standard interference function maps a vector of transmit powers to the powers that each link would need, given the interference that these powers cause. Yates' theorem says that if such a map is positive, monotone and scalable, it has at most one fixed point, and when some power vector meets all the targets, the plain iteration $p \leftarrow I(p)$ reaches that fixed point from every start, also when the links update at different times. The fixed point is the least power vector that meets the targets. The theorem is the common proof behind [Foschini-Miljanic power control](/foschini-miljanic-power-control/), which is its linear case, and behind its variants with power limits and base station choice. [Max-min SINR power control](/max-min-sinr-power-control/) and [power control by geometric programming](/geometric-programming-power-control/) solve other problems on the same SINR model.

## Statement

There are $K$ links. A power vector is $p \in \mathbb{R}^K$ with $p \ge 0$. All inequalities between vectors are entrywise, and $p > 0$ means that every entry is positive. An *interference function* is a map $I : \mathbb{R}^K_{\ge 0} \to \mathbb{R}^K$, where $I_i(p)$ is the power that link $i$ needs to meet its target when the other links use $p$.

**Definition.** $I$ is a *standard interference function* if for all $p, p' \ge 0$:

1. *Positivity:* $I(p) > 0$.
2. *Monotonicity:* if $p \ge p'$, then $I(p) \ge I(p')$.
3. *Scalability:* for every $\alpha > 1$, $\alpha I(p) > I(\alpha p)$.

A power vector $p \ge 0$ is *feasible* if $p \ge I(p)$, that is, if each link has at least the power it needs. The *standard iteration* is $p(t+1) = I(p(t))$. In the *asynchronous iteration*, at each time $t$ only links in a set $U(t)$ update, and link $i \in U(t)$ sets $p_i(t+1) = I_i(x)$, where $x_j = p_j(\tau_{ij}(t))$ is a value of link $j$ from some earlier time $\tau_{ij}(t) \le t$. Each link must update at infinitely many times, and $\tau_{ij}(t) \to \infty$ as $t \to \infty$ (old values are eventually not used).

**Theorem (Yates 1995).** Let $I$ be a standard interference function.

1. $I$ has at most one fixed point.
2. A fixed point exists if and only if a feasible vector exists. Then the fixed point $p^*$ is positive, and $p^* \le p$ for every feasible $p$.
3. If a feasible vector exists, the standard iteration converges to $p^*$ from every start $p(0) \ge 0$. From $p(0) = 0$ it increases in every entry; from a feasible start it decreases and every iterate is feasible.
4. If a feasible vector exists, the asynchronous iteration converges to $p^*$ from every start.
5. If no feasible vector exists, the standard iteration from $p(0) = 0$ is unbounded.

**Example: the linear case.** With gains $G_{ij}$, noise powers $\sigma_i > 0$ and SINR targets $\gamma_i > 0$, link $i$ needs $I_i(p) = (\gamma_i / G_{ii}) (\sum_{j \ne i} G_{ij} p_j + \sigma_i)$, so $I(p) = Fp + u$ with $F \ge 0$ and $u > 0$. It is positive since $u > 0$, monotone since $F \ge 0$, and scalable since $\alpha I(p) - I(\alpha p) = (\alpha - 1) u > 0$. The standard iteration is the [Foschini-Miljanic](/foschini-miljanic-power-control/) iteration, and a feasible vector exists exactly when the spectral radius of $F$ is below 1.

## In plain words

Each link asks one question: given what the others transmit now, how much power do I need to reach my goal? The answer is the rule. The theorem says that three plain properties of the rule are enough for a good outcome. Each link always needs some power, because of noise. If the others transmit more, a link never needs less. If everyone multiplies their power by the same factor, each link needs less than that factor times its old need, because the noise does not grow. With these three properties, there is at most one balanced state, and if the goals can be met at all, every link that keeps asking the question and acting on the answer reaches that state. The state uses the least power. It does not matter where the links start or whether they act at the same time.

## Proof

Write $I^n$ for $I$ applied $n$ times. We first collect two facts that follow from the definition.

**Lemma 1 (bounds).** Let $a \ge 1$, $q \ge 0$ and $q / a \le q' \le a q$. Then $I(q)/a \le I(q') \le a\, I(q)$.

*Proof.* For $a = 1$ this is $q' = q$. Let $a > 1$. By monotonicity and scalability, $I(q') \le I(aq) < a I(q)$. Also $q' \ge q/a$, so $I(q') \ge I(q/a)$, and scalability applied to the vector $q/a$ gives $a I(q/a) > I(q)$, so $I(q') > I(q)/a$. $\square$

**Lemma 2 (limits of monotone sequences).** Let $x_n$ be a sequence with $x_{n+1} = I(x_n)$ that is monotone in every entry (increasing, or decreasing) and converges to a limit $L$. Then $I(L) = L$.

*Proof.* For $n \ge 1$, $x_n = I(x_{n-1}) > 0$. If the sequence increases, then $L \ge x_1 > 0$; if it decreases, assume for now that $L > 0$ (we check this each time we use the lemma). Fix $a > 1$. Since $L > 0$ and $x_n \to L$, for large $n$ we have $L/a \le x_n \le aL$, and Lemma 1 gives $I(L)/a \le I(x_n) = x_{n+1} \le a I(L)$. Let $n \to \infty$: $I(L)/a \le L \le a I(L)$. Since this holds for every $a > 1$, $I(L) = L$. $\square$

**Part 1 (uniqueness).** Let $p$ and $p'$ be fixed points. They are positive, because $p = I(p) > 0$. Suppose $p \ne p'$. After swapping the two if needed, $a = \max_i p_i / p'_i > 1$. (If both maxima were at most 1, we would have $p \le p'$ and $p' \le p$.) Let $j$ be an index with $p_j = a p'_j$. Then $p \le a p'$, and

$$p_j = I_j(p) \le I_j(a p') < a I_j(p') = a p'_j = p_j,$$

by monotonicity and then scalability. This is a contradiction, so $p = p'$.

**Part 2 and part 3 (existence, least power, convergence).** A fixed point is feasible. Conversely, let $p$ be feasible and put $y_n = I^n(p)$. Since $y_1 = I(p) \le p = y_0$, monotonicity and induction give $y_{n+1} \le y_n$: the sequence decreases. Each $y_n$ is feasible, since $y_n \ge y_{n+1} = I(y_n)$. Also $p \ge 0$, so $y_n = I^n(p) \ge I^n(0)$ by monotonicity. The sequence $x_n = I^n(0)$ increases: $x_1 = I(0) \ge 0 = x_0$, and induction with monotonicity gives $x_{n+1} \ge x_n$. For $m \ge n$ we get $y_m \ge x_m \ge x_n$. So $y_n$ is decreasing and bounded below by $x_n$ for each fixed $n$, and it converges to a limit $M$ with $M \ge x_1 = I(0) > 0$. By Lemma 2, $M$ is a fixed point, so $M = p^*$ by Part 1. This proves existence, and $p^* = \lim y_n \le y_0 = p$ proves that $p^*$ is the least feasible vector.

Now $x_n = I^n(0) \le I^n(p^*) = p^*$ by monotonicity, so the increasing sequence $x_n$ is bounded and converges. By Lemma 2 its limit is a fixed point, so it is $p^*$.

Let $q \ge 0$ be any start. Since $p^* > 0$, there is $a > 1$ with $q \le a p^*$. The vector $a p^*$ is feasible, because $I(a p^*) < a I(p^*) = a p^*$, so by the argument above $I^n(a p^*)$ decreases to $p^*$. By monotonicity, $I^n(0) \le I^n(q) \le I^n(a p^*)$ for every $n$. Both bounds converge to $p^*$, so $I^n(q) \to p^*$.

**Part 4 (asynchronous updates).** Let the start be $q \ge 0$ and pick $a > 1$ with $q \le a p^*$. Put $\ell^{(k)} = I^k(0)$ and $h^{(k)} = I^k(a p^*)$, and let $S(k)$ be the box of vectors $x$ with $\ell^{(k)} \le x \le h^{(k)}$. By Part 3, $\ell^{(k)}$ increases to $p^*$ and $h^{(k)}$ decreases to $p^*$, so the boxes are nested, $S(k+1) \subseteq S(k)$, and they shrink to the point $p^*$. If $x \in S(k)$, then monotonicity gives $\ell^{(k+1)} = I(\ell^{(k)}) \le I(x) \le I(h^{(k)}) = h^{(k+1)}$, so in every entry $i$, $I_i(x)$ lies in the $i$th interval of $S(k+1)$.

We show by induction on $k$ that there is a time $t_k$ with $p(t) \in S(k)$ for all $t \ge t_k$. For $k = 0$, take $t_0 = 0$: the start is in $S(0)$, and an update of link $i$ uses a vector $x$ whose entries come from earlier iterates in $S(0)$; since $S(0)$ is a box, $x \in S(0)$, so the new value lies in the $i$th interval of $S(1) \subseteq S(0)$. By induction on $t$, every iterate stays in $S(0)$. For the step from $k$ to $k+1$, choose $t' \ge t_k$ such that $\tau_{ij}(t) \ge t_k$ for all $i, j$ and all $t \ge t'$; this is possible because $\tau_{ij}(t) \to \infty$. Every update at a time $t \ge t'$ uses a vector $x$ whose entries come from iterates in $S(k)$, so $x \in S(k)$, and the new value $p_i(t+1)$ lies in the $i$th interval of $S(k+1)$. Entries that have not been updated since $t'$ still lie in the intervals of $S(k)$. Each link updates at some time after $t'$; let $t_{k+1}$ be a time after which every link has done so. From then on, every entry has its newest value from an update at a time $\ge t'$, so $p(t) \in S(k+1)$ for all $t \ge t_{k+1}$. Since the boxes shrink to $p^*$, $p(t) \to p^*$.

**Part 5 (no feasible vector).** The sequence $x_n = I^n(0)$ increases, as shown in Part 2. If it were bounded, it would converge, and by Lemma 2 its limit would be a fixed point, which is feasible. So with no feasible vector, the sequence is unbounded. $\blacksquare$

## Consequences

- **The linear case.** For $I(p) = Fp + u$ with $F \ge 0$ and $u > 0$, Parts 2 and 3 give the convergence of the [Foschini-Miljanic](/foschini-miljanic-power-control/) iteration with $\beta = 1$ and the least-power property of its limit, with no eigenvalue argument. The map $(1 - \beta) p + \beta I(p)$ is also standard for $\beta \in (0, 1]$, which covers the relaxed iteration.
- **Power limits.** If $I$ is standard and $\bar p > 0$, then $\hat I(p) = \min(\bar p, I(p))$, taken entrywise, is standard. So the iteration with power limits always converges, because $\bar p$ itself is feasible for $\hat I$. Its fixed point meets the targets of all links that are not at their limit.
- **Base station choice.** If each link $i$ can use one of several receivers $k$, each with a standard need $I_i^{(k)}(p)$, then $I_i(p) = \min_k I_i^{(k)}(p)$ is standard. So a mobile that joins, at each round, the base station where it needs the least power, and sets that power, converges together with the others. The minimum and the maximum of standard functions, and positive sums of them, are standard.
- **Macro diversity.** If the signals from several receivers are combined, the need of link $i$ is $\gamma_i$ divided by the sum over the receivers $k$ of its SINR per watt at receiver $k$. This is again standard, because each SINR per watt falls when the other powers rise, and falls by less than the factor $\alpha$ when all powers are scaled by $\alpha$, so the same convergence holds.
- **Feasibility test.** By Part 5, a central controller can test feasibility by running the iteration from zero: it is bounded exactly when the targets can be met.
- **Least power in every entry.** The fixed point is the least feasible vector in every entry at once. So there is no trade-off between the links: no feasible vector gives one link less power at the cost of another, and the total power is also least at $p^*$.

## Tightness

None of the three properties can be dropped. All examples are for one link, $K = 1$.

- **Without scalability, uniqueness fails.** $I(p) = \max(1, p)$ is positive and monotone, and $\alpha I(p) \ge I(\alpha p)$ holds, but only with equality for $p \ge 1$. Every $p \ge 1$ is a fixed point.
- **Without positivity, uniqueness fails.** $I(p) = \sqrt{p}$ is monotone and satisfies $\alpha \sqrt{p} > \sqrt{\alpha p}$ for $p > 0$, but $I(0) = 0$. It has the two fixed points $0$ and $1$. In power control, positivity comes from the receiver noise; without noise the SINR does not depend on the absolute power level, and only the ratios of the powers are determined, as in the noise-free problem of Zander.
- **Without monotonicity, convergence fails.** $I(p) = 10\, e^{-p}$ is positive and scalable, because $I(p)/p$ decreases. Its only fixed point is $p^* \approx 1.7455$. From $p(0) = 0$ the iteration gives $10, 0.00045, 9.9955, 0.00046, 9.9954, \ldots$ and settles on a cycle of length 2 that never comes near $p^*$.
- **Feasibility is needed.** $I(p) = 2p + 1$ is standard, since $\alpha(2p + 1) - (2 \alpha p + 1) = \alpha - 1 > 0$, but $p \ge 2p + 1$ has no solution with $p \ge 0$. The iteration from zero gives $1, 3, 7, 15, \ldots$, as Part 5 says.
- **No rate in general.** The theorem gives convergence but no rate. In the linear case the error falls by about the spectral radius of $F$ per round, which can be as close to 1 as wanted.

## History

Zander (1992) and Foschini and Miljanic (1993) studied the linear case, where the need of each link is an affine function of the other powers, and proved convergence with the Perron-Frobenius theory of nonnegative matrices. Iterations with power limits, or in which a mobile also chooses its base station, are not linear, and each needed its own convergence proof. Yates (1995) saw that all of these needs share three properties, positivity, monotonicity and scalability, and that these alone give uniqueness, least power and convergence, both synchronous and asynchronous. The proof of the asynchronous case given above is the nested-box argument of Bertsekas and Tsitsiklis for asynchronous iterations. The framework became the standard tool for proving that a power control rule converges.

## References
