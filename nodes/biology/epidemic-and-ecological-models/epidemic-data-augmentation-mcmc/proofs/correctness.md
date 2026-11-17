---
title: The complete-data likelihood, the full conditionals and the invariance of the sampler
proves: [correctness]
status: full
---

**Setting.** A closed population of $N$ people follows the Markov SIR model: when $S$ people are susceptible and $I$ are infectious, each susceptible is infected at rate $\beta I / N$, and each infectious person is removed at rate $\gamma$. The epidemic is complete. The $n \ge 1$ people who were ever infected have the labels $1, \ldots, n$, known removal times $r_1, \ldots, r_n$ and unknown infection times $i_1, \ldots, i_n$. The other $N - n$ people are never infected; we write $i_k = \infty$ for them. Let $\kappa$ be the person with the earliest infection time, the initial case, and let $I(t-)$ be the number infectious just before $t$. We call the vector $\mathbf i = (i_1, \ldots, i_n)$ **valid** if $i_j < r_j$ for all $j$ and $I(i_j-) \ge 1$ for every $j \ne \kappa$. The priors are $\beta \sim \operatorname{Gamma}(a_\beta, \text{rate } b_\beta)$, $\gamma \sim \operatorname{Gamma}(a_\gamma, \text{rate } b_\gamma)$, independent, and a flat prior on $i_\kappa$.

**Claim 1 (the complete-data likelihood).** For a valid $\mathbf i$, the density of the infection and removal times given $\beta$, $\gamma$ and $i_\kappa$ is
$$L(\beta, \gamma; \mathbf i) = \Big(\frac{\beta}{N}\Big)^{n-1} \prod_{j \ne \kappa} I(i_j-)\ \gamma^n \exp\Big(-\frac{\beta}{N} A - \gamma D\Big),$$
with $A = \int S(t) I(t)\, dt$ and $D = \sum_j (r_j - i_j)$. It is 0 for a vector that is not valid.

*Proof.* Between events the state is constant, and the labelled process is a Markov chain in which person $k$ is infected at rate $\beta I / N$ while susceptible and removed at rate $\gamma$ while infectious. The density of a path of a Markov chain with finitely many events is the product of the rates of the events that happen, times the exponential of minus the integral of the total rate of all possible events. The $n - 1$ infections after the first one contribute $\beta I(i_j-) / N$ each, the $n$ removals contribute $\gamma$ each, and the total rate is $\frac{\beta}{N} S(t) I(t) + \gamma I(t)$. Its integral is $\frac{\beta}{N} A + \gamma \int I(t)\, dt$, and $\int I(t)\, dt = \sum_j (r_j - i_j) = D$, since person $j$ is infectious exactly on $[i_j, r_j)$. If $I(i_j-) = 0$ for some $j \ne \kappa$, the rate of that infection is 0, so the density is 0. $\square$

The function `log_likelihood` returns the logarithm of this expression. The test compares it with a sweep over the events that adds the log rate of each event and subtracts the integral of the total rate between events.

**Claim 2 (the pair form of $A$).** $A = \sum_{j=1}^{n} \sum_{k \ne j} \big(\min(r_j, i_k) - \min(i_j, i_k)\big)$, where $k$ runs over all $N$ people. For $k \le n$ the term equals $\max(0, \min(r_j, i_k) - i_j)$, and each of the $N - n$ people who are never infected adds $r_j - i_j$. So `pressure_integral` computes $A$.

*Proof.* $S(t) I(t)$ counts the pairs $(j, k)$ with $j$ infectious and $k$ susceptible at time $t$. So $A$ is the sum over pairs of the length of the time when both hold, which is the length of $[i_j, r_j) \cap (-\infty, i_k)$. That length is $\max(0, \min(r_j, i_k) - i_j)$, which equals $\min(r_j, i_k) - \min(i_j, i_k)$, and it is $r_j - i_j$ when $i_k = \infty$. $\square$

**Claim 3 (the update of $A$).** If only $i_j$ changes, $A$ changes by the change of `pair_terms(j, ...)`.

*Proof.* By Claim 2, $A$ is a sum of terms indexed by pairs. The terms that depend on $i_j$ are those with $j$ as the infector (the pairs $(j, k)$, including the $N - n$ terms $r_j - i_j$) and those with $j$ as the susceptible (the pairs $(k, j)$). `pair_terms` adds exactly these terms, and every other term is the same before and after the change. $\square$

**Claim 4 (the infection term).** `log_infection_term` returns $\sum_{j \ne \kappa} \log I(i_j-)$ for a vector with $i_j < r_j$ for all $j$, or $-\infty$ if some $j \ne \kappa$ has $I(i_j-) = 0$.

*Proof.* The sweep visits the $2n$ times in increasing order with a counter that starts at 0, adds 1 at each infection and subtracts 1 at each removal. Since every person is infectious exactly on $[i_j, r_j)$, the counter just before an event at time $t$ equals $I(t-)$, the number with $i_k < t \le r_k$ processed so far. The first infection is that of $\kappa$ and is skipped. At every later infection the code adds $\log I(i_j-)$, or returns $-\infty$ if the counter is 0. Event times are distinct with probability 1 under the proposal, which has a continuous density. $\square$

**Claim 5 (the Gibbs steps, lines L3 and L4).** Given $\mathbf i$, the posterior of $\beta$ is $\operatorname{Gamma}(a_\beta + n - 1, \text{rate } b_\beta + A/N)$, the posterior of $\gamma$ is $\operatorname{Gamma}(a_\gamma + n, \text{rate } b_\gamma + D)$, and the two are independent.

*Proof.* The joint posterior density is proportional to $L(\beta, \gamma; \mathbf i)\, \pi(\beta)\, \pi(\gamma)$. As a function of $\beta$ and $\gamma$ for a fixed valid $\mathbf i$, it is
$$\beta^{a_\beta - 1 + n - 1} e^{-\beta (b_\beta + A/N)} \cdot \gamma^{a_\gamma - 1 + n} e^{-\gamma (b_\gamma + D)},$$
a product of a gamma kernel in $\beta$ and a gamma kernel in $\gamma$. The code calls `gammavariate` with the shape and the scale $1/\text{rate}$. $\square$

**Claim 6 (the Metropolis-Hastings step, lines L5 to L7).** Given $\beta$ and $\gamma$, one update of $i_j$ leaves the conditional law $p(\mathbf i \mid \beta, \gamma) \propto L(\beta, \gamma; \mathbf i)$ invariant.

*Proof.* The update picks $j$ uniformly and proposes $i_j' = r_j - E$ with $E \sim \operatorname{Exp}(\gamma)$, whatever the current $i_j$. The proposal density is $q(i_j') = \gamma e^{-\gamma (r_j - i_j')}$ on $(-\infty, r_j)$. The [Metropolis-Hastings](/metropolis-hastings/) ratio for moving from $\mathbf i$ to $\mathbf i'$ is
$$\frac{L(\mathbf i')\, q(i_j)}{L(\mathbf i)\, q(i_j')}.$$
In $L$, the factor $e^{-\gamma D}$ changes by $e^{-\gamma[(r_j - i_j') - (r_j - i_j)]}$, and $q(i_j)/q(i_j')$ is $e^{-\gamma[(r_j - i_j) - (r_j - i_j')]}$; the two cancel. The factors $(\beta/N)^{n-1}$ and $\gamma^n$ do not change. So the ratio is
$$\exp\Big(\sum_{k \ne \kappa'} \log I'(i_k'-) - \sum_{k \ne \kappa} \log I(i_k-) - \frac{\beta}{N}(A' - A)\Big),$$
which is `log_ratio` by Claims 3 and 4. If $\mathbf i'$ is not valid, $L(\mathbf i') = 0$ and the ratio is 0, so the code rejects. The test $\log(1 - u) < \text{log\_ratio}$, with $u$ uniform on $[0, 1)$, accepts with probability $\min(1, e^{\text{log\_ratio}})$. This is the Metropolis-Hastings rule, so the kernel satisfies [detailed balance](/detailed-balance/) with respect to $p(\mathbf i \mid \beta, \gamma)$, and a mixture over $j$ of such kernels does too. $\square$

**Claim 7 (invariance of the whole sweep).** One iteration of lines L3 to L7 leaves the joint posterior of $(\beta, \gamma, \mathbf i)$ invariant.

*Proof.* Lines L3 and L4 together draw $(\beta, \gamma)$ from their joint conditional given $\mathbf i$ (Claim 5), which leaves the joint posterior invariant, as every [Gibbs](/gibbs-sampling/) step does. Each update of lines L5 to L7 changes only $\mathbf i$ and leaves $p(\mathbf i \mid \beta, \gamma)$ invariant (Claim 6), so it leaves the joint posterior invariant. A composition of kernels that leave a law invariant leaves it invariant. $\square$

**Claim 8 (a valid start and irreducibility).** Line L1 gives a valid vector, and the chain can move from any valid vector to any open set of valid vectors with positive probability.

*Proof.* Line L1 puts all infections in the interval $[r_{\min} - 1, r_{\min})$ before the first removal, in the order of the removal times. Each infection after the first finds the first case infectious, since nobody is removed before $r_{\min}$. So the vector is valid. For irreducibility, note that moving a case $j$ to a time earlier than every current infection time keeps the vector valid: $j$ becomes the first case and needs no infector, and $j$ is now infectious on a longer interval, so no other case loses its infector. The proposal has a positive density on $(-\infty, r_j)$, so such moves have positive probability. After $n$ such moves, all infections lie before $r_{\min}$, where every ordering is valid, and every vector of that kind can be reached from every other one by single moves. Since each kernel satisfies detailed balance, the moves can also be made in reverse with positive probability, so any valid vector can be reached from any other. The Gibbs steps have positive densities on $(0, \infty)^2$. $\square$

**Conclusion.** The chain has the joint posterior as an invariant law and is irreducible with respect to it, so by the ergodic theorem for Markov chains the averages over the chain converge to the posterior expectations. The test with two cases checks this against the exact posterior of the infection times, where $\beta$ and $\gamma$ are integrated out in closed form:
$$p(\mathbf i \mid \mathbf r) \propto \prod_{j \ne \kappa} I(i_j-)\ \big(b_\beta + A/N\big)^{-(a_\beta + n - 1)} \big(b_\gamma + D\big)^{-(a_\gamma + n)}.$$
