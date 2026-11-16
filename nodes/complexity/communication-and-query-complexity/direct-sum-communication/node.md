---
tag: 5CHJKQ
kind: theorem
slug: direct-sum-communication
name: Direct sum theorem for communication
aliases:
- direct sum for communication complexity
area: complexity/communication-and-query-complexity
level: research
summary: "Information complexity is exactly additive over independent copies. For communication, k copies need about sqrt(k) times one copy in general, and about k times under product distributions."
prereqs: [information-complexity, randomized-communication-complexity]
see_also: [information-complexity, corruption-bound, simultaneous-message-model, disjointness-problem, equality-problem, parallel-repetition-theorem, randomized-communication-complexity, discrepancy-method]
sources:
  - paper: "Tomás Feder, Eyal Kushilevitz, Moni Naor and Noam Nisan, Amortized communication complexity, SIAM Journal on Computing 24(4) (1995), 736-750"
    locator: the deterministic direct sum bound, the nondeterministic case, and the equality example; conference version FOCS 1991
  - paper: "Amit Chakrabarti, Yaoyun Shi, Anthony Wirth and Andrew Chi-Chih Yao, Informational complexity and the direct sum problem for simultaneous message complexity, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001)"
    locator: the first direct sum theorem proved through information cost
  - paper: "Boaz Barak, Mark Braverman, Xi Chen and Anup Rao, How to compress interactive communication, SIAM Journal on Computing 42(3) (2013), 1327-1363"
    locator: the additivity of internal information cost and the compression that gives the sqrt(k) direct sum; conference version STOC 2010
  - paper: "Mark Braverman and Anup Rao, Information equals amortized communication, IEEE Transactions on Information Theory 60(10) (2014)"
    locator: amortized distributional communication equals internal information complexity; conference version FOCS 2011
  - paper: "Anat Ganor, Gillat Kol and Ran Raz, Exponential separation of information and communication, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014)"
    locator: a task whose information complexity is exponentially below its distributional communication, which limits direct sum results for communication
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 7, Compressing Communication, section Direct Sums in Randomized Communication Complexity
---

A direct sum theorem says that solving $k$ independent copies of a problem costs about $k$ times as much as solving one. For [information complexity](/information-complexity/) this holds exactly: the internal information cost of $k$ copies is $k$ times the cost of one. For communication it holds only in weaker forms. With the compression results of Barak, Braverman, Chen and Rao, $k$ copies need about $\sqrt{k}$ times the communication of one copy in general, and about $k$ times under product distributions; the full factor $k$ fails for distributional communication by the separation of Ganor, Kol and Raz.

## Statement

Let $f : X \times Y \to Z$ and let $\mu$ be a distribution on $X \times Y$. The problem $f^k$ takes inputs $\mathbf{x} = (x_1, \ldots, x_k)$ and $\mathbf{y} = (y_1, \ldots, y_k)$ and asks for all $k$ values $f(x_j, y_j)$. Protocols are two-way, with public coins and private coins. Say that a protocol for $f^k$ has error $\varepsilon$ under $\mu^k$ if each output $j$ is wrong with probability at most $\varepsilon$ when the inputs are drawn from $\mu^k$. Let $\mathrm{IC}_\mu(f, \varepsilon)$ be the infimum of the internal information cost $I(\Pi; X \mid Y) + I(\Pi; Y \mid X)$ over protocols for $f$ with error $\varepsilon$ under $\mu$.

**Theorem (additivity of information).** For every $f$, $\mu$, $\varepsilon$ and $k \ge 1$,

$$\mathrm{IC}_{\mu^k}(f^k, \varepsilon) = k \cdot \mathrm{IC}_\mu(f, \varepsilon).$$

**Corollaries for communication.** Let $D^\mu_\varepsilon$ be the distributional communication cost.

1. (Braverman and Rao) $\lim_{k \to \infty} D^{\mu^k}_\varepsilon(f^k)/k = \mathrm{IC}_\mu(f, \varepsilon)$ for $\varepsilon > 0$.
2. (Barak, Braverman, Chen and Rao) $D^{\mu^k}_\varepsilon(f^k) \cdot \mathrm{polylog} \ge \Omega(\sqrt{k})\, D^\mu_{\varepsilon'}(f)$ for a slightly larger error $\varepsilon'$, and $\Omega(k)$ in place of $\Omega(\sqrt{k})$ when $\mu$ is a product distribution.

The polylogarithmic factors and the change of error are stated in the paper and are not repeated here.

## In plain words

Suppose Alice and Bob must solve many unrelated copies of the same small task. One might hope to save by mixing the copies together. For the amount that the players learn about each other's inputs, no saving is possible: the learning for all copies is exactly the sum of the learning for each copy.

The number of bits sent is a different matter. A talk can be longer than what it teaches, and many copies let the players pack the teaching into fewer bits. So the cost in bits of many copies is close to the number of copies times the learning for one copy, which can be less than the number of copies times the bits for one copy.

## Proof

Write $\mathbf{X} = (X_1, \ldots, X_k)$ and $\mathbf{Y} = (Y_1, \ldots, Y_k)$ with $(X_j, Y_j)$ independent and each distributed as $\mu$. Write $X_{<i} = (X_1, \ldots, X_{i-1})$ and $Y_{>i} = (Y_{i+1}, \ldots, Y_k)$.

**A fact.** If $I(A; C \mid B) = 0$, then $I(\Pi; A \mid B) \le I(\Pi; A \mid B, C)$. Indeed, by the chain rule $I(\Pi C; A \mid B)$ equals both $I(C; A \mid B) + I(\Pi; A \mid B C) = I(\Pi; A \mid BC)$ and $I(\Pi; A \mid B) + I(C; A \mid B \Pi) \ge I(\Pi; A \mid B)$.

**$\le$: run copies.** Take a protocol $\pi$ for $f$ with error $\varepsilon$ under $\mu$ and internal cost within $\delta$ of $\mathrm{IC}_\mu(f, \varepsilon)$. Run $k$ copies of $\pi$ on the $k$ coordinates with independent coins. Each output has error $\varepsilon$. The triples $(X_j, Y_j, \Pi_j)$ are independent, so $I(\Pi_1 \cdots \Pi_k; \mathbf{X} \mid \mathbf{Y}) = \sum_j I(\Pi_j; X_j \mid Y_j)$, and the same for the other term. So the cost is at most $k(\mathrm{IC}_\mu(f, \varepsilon) + \delta)$ for every $\delta > 0$.

**$\ge$: embed one copy.** Let $\Pi$ be the transcript, with public coins, of a protocol $\pi$ for $f^k$ with error $\varepsilon$ under $\mu^k$. For each $i$ build a protocol $\pi_i$ for one copy of $f$ on input $(x, y)$:

1. With public coins, draw $X_{<i}$ and $Y_{>i}$ from their marginals.
2. Alice, with private coins, draws each $X_j$ for $j > i$ from $\mu$ conditioned on $Y_j$. Bob, with private coins, draws each $Y_j$ for $j < i$ from $\mu$ conditioned on $X_j$.
3. Both put $X_i = x$ and $Y_i = y$, run $\pi$, and output the $i$-th answer.

If $(x, y) \sim \mu$, the joint input is distributed exactly as $\mu^k$, so $\pi_i$ has error $\varepsilon$ under $\mu$. The transcript of $\pi_i$ is $(\Pi, X_{<i}, Y_{>i})$, and its first term is

$$I(\Pi X_{<i} Y_{>i}; X_i \mid Y_i) = I(\Pi; X_i \mid X_{<i}, Y_{\ge i}) \le I(\Pi; X_i \mid X_{<i}, \mathbf{Y}).$$

The equality holds because $X_{<i} Y_{>i}$ is independent of $(X_i, Y_i)$. The inequality is the fact with $A = X_i$, $B = (X_{<i}, Y_{\ge i})$ and $C = Y_{<i}$, which are independent given $B$. Summing over $i$ and using the chain rule,

$$\sum_{i=1}^{k} I(\Pi X_{<i} Y_{>i}; X_i \mid Y_i) \le \sum_{i=1}^{k} I(\Pi; X_i \mid X_{<i}, \mathbf{Y}) = I(\Pi; \mathbf{X} \mid \mathbf{Y}).$$

In the same way, with the chain rule over $Y_k, Y_{k-1}, \ldots, Y_1$ and $C = X_{>i}$, the second terms sum to at most $I(\Pi; \mathbf{Y} \mid \mathbf{X})$. So $\sum_i \mathrm{IC}_\mu(\pi_i) \le \mathrm{IC}_{\mu^k}(\pi)$, and some $i$ has $\mathrm{IC}_\mu(\pi_i) \le \mathrm{IC}_{\mu^k}(\pi)/k$. Taking the infimum over $\pi$ gives $k \cdot \mathrm{IC}_\mu(f, \varepsilon) \le \mathrm{IC}_{\mu^k}(f^k, \varepsilon)$. $\blacksquare$

The sampling in step 2 must use private coins, because $X_j$ and $Y_j$ are correlated when $\mu$ is not a product distribution. Internal information is the measure for which this private sampling costs nothing, which is why the clean statement is about internal information.

**From information to communication.** A protocol for $f^k$ with $C$ bits has internal cost at most $C$, so by the theorem some $\pi_i$ solves $f$ with internal cost at most $C/k$ and communication $C$. The compression of Barak, Braverman, Chen and Rao turns this into a protocol for $f$ with about $\sqrt{C \cdot C/k} = C/\sqrt{k}$ bits, up to logarithmic factors. So $C \gtrsim \sqrt{k}\, D^\mu(f)$. For a product distribution the internal and external costs are equal, and the external compression to about $C/k$ bits gives $C \gtrsim k\, D^\mu(f)$.

## Consequences

- **Amortized communication.** Braverman and Rao (2011) showed that information complexity is exactly the communication per copy for many copies, the interactive form of Shannon's source coding theorem.
- **Lower bounds through one small copy.** The bound for [disjointness](/disjointness-problem/) is the theorem applied to the AND function, with the extra condition that protocols are correct on every input. See [information complexity](/information-complexity/).
- **Deterministic protocols.** Feder, Kushilevitz, Naor and Nisan (1995) proved that $k$ copies need about $k\sqrt{D^{cc}(f)}$ bits deterministically, up to lower-order terms, and that the nondeterministic cost obeys a direct sum up to such terms.
- **Private coins.** The theorem does not hold for worst-case communication with private coins. For [equality](/equality-problem/) with private coins, one copy needs $\Theta(\log n)$ bits. For $k$ copies, run the public-coin protocol with error $1/3$ on each copy, at $O(k)$ bits, and then remove the public coins by Newman's theorem on inputs of $kn$ bits, at $O(\log(kn))$ extra bits. The total $O(k + \log(kn))$ is far below $k \cdot \Theta(\log n)$ when $k$ is large and $n$ is much larger. This example is from Feder, Kushilevitz, Naor and Nisan.
- **Other models.** Chakrabarti, Shi, Wirth and Yao (2001) proved a direct sum theorem in the [simultaneous message model](/simultaneous-message-model/). The [corruption bound](/corruption-bound/) obeys a strong direct product theorem by Beame, Pitassi, Segerlind and Wigderson (2006).

## Tightness

- **Information.** The theorem is an equality, so it is tight.
- **Distributional communication.** Ganor, Kol and Raz (2014) gave a task with information complexity $O(k)$ and distributional communication $2^{\Omega(k)}$. By corollary 1, many copies of it cost about $O(k)$ bits per copy. So the communication of many copies can be far below the number of copies times the communication of one copy, and a direct sum with the full factor $k$ fails for distributional communication.
- **The $\sqrt{k}$ factor.** For a general distribution, the $\sqrt{k}$ bound comes from the $\sqrt{C \cdot I}$ compression. The separation of Ganor, Kol and Raz shows that compression of one copy to a length polynomial in $I$ is not possible in general.
- **Product distributions.** Here the factor $k$ holds up to logarithmic factors.

## History

Karchmer, Raz and Wigderson (1991) asked for direct sum results for relations, as a route to lower bounds on circuit depth. Feder, Kushilevitz, Naor and Nisan (FOCS 1991, journal 1995) settled the deterministic and nondeterministic cases up to a square root and found the equality example. Chakrabarti, Shi, Wirth and Yao (2001) introduced information cost to prove direct sums in the simultaneous model, and Bar-Yossef, Jayram, Kumar and Sivakumar (2002) used it for disjointness. Barak, Braverman, Chen and Rao (2010) defined internal information cost for general distributions and proved the compression results. Braverman and Rao (2011) proved that information equals amortized communication, and Ganor, Kol and Raz (2014) showed that information and communication can be exponentially far apart.

## References
