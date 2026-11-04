---
tag: VJAPMM
kind: concept
slug: martingale
name: Martingale
aliases:
- Doob martingale
area: foundations/probabilistic-analysis
level: advanced
summary: A sequence of random variables whose expected next value, given the whole past, equals the current value; the base of the optional stopping theorem and of Azuma's inequality.
prereqs: [conditional-expectation, expected-value, random-variable, independent-random-variables]
see_also: [azuma-inequality, optional-stopping-theorem, walds-equation, concentration-of-measure, hoeffding-inequality, method-of-conditional-expectations, markov-chain, 2-sat]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 13, Martingales (Section 13.1, Martingales, with the Doob martingale and the edge and vertex exposure martingales; Section 13.2, Stopping Times)
  - book: isbn:9780521406055
    title: David Williams, Probability with Martingales, Cambridge University Press, 1991
    locator: Chapter 9, Conditional Expectation, and Chapter 10, Martingales (definition, examples, stopping times, the stopped process)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 7, Martingales and Tight Concentration (Section 7.1, Definitions, the edge and vertex exposure martingales)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 4, Tail Inequalities, Section 4.4, Martingales
---

A martingale is a sequence of [random variables](/random-variable/) $X_0, X_1, X_2, \ldots$ in which the [conditional expectation](/conditional-expectation/) of the next value, given all that is known so far, equals the current value. It is the mathematical form of a fair game: on average, the next bet neither wins nor loses. In the analysis of algorithms, martingales give exact hitting probabilities and expected running times through the [optional stopping theorem](/optional-stopping-theorem/), and tail bounds for functions of many random choices through [Azuma's inequality](/azuma-inequality/), even when the steps are not [independent](/independent-random-variables/).

## In plain words

Think of a gambler who plays a fair game, one round after another, and writes down the money after each round. Before a round, the best guess of the money after the round is the money now. The list of amounts is a martingale.

The same idea fits a randomized algorithm. Fix a quantity that depends on all the random choices, for example the number of colors that a random graph needs. Make the choices one at a time, and after each one write down the best guess of the final quantity. The first guess is the plain average. The last guess is the true value. Each guess is, on average, equal to the one before it. If one choice can move the guess only a little, then the final value stays close to the first guess with high probability. This is how many concentration results for algorithms are proved.

## The idea

**Information that grows.** Fix a [probability space](/probability-space/) $(\Omega, \mathcal F, \Pr)$. A *filtration* is a sequence of $\sigma$-algebras $\mathcal F_0 \subseteq \mathcal F_1 \subseteq \cdots \subseteq \mathcal F$. The events in $\mathcal F_n$ are the events that are decided at time $n$. In the discrete settings of algorithm analysis, $\mathcal F_n = \sigma(Z_1, \ldots, Z_n)$ is the information in the first $n$ random choices $Z_1, \ldots, Z_n$, and an $\mathcal F_n$-measurable random variable is a function of $Z_1, \ldots, Z_n$.

**Definition.** A sequence $(X_n)_{n \ge 0}$ of real random variables is a *martingale with respect to* $(\mathcal F_n)$ when, for each $n \ge 0$:

1. $X_n$ is $\mathcal F_n$-measurable (the sequence is *adapted*),
2. $\mathbb E|X_n| < \infty$,
3. $\mathbb E[X_{n+1} \mid \mathcal F_n] = X_n$ almost surely.

It is a *submartingale* if 3 holds with $\ge$, and a *supermartingale* if 3 holds with $\le$. A supermartingale is a game that is unfavourable to the player: it tends to go down. When no filtration is named, it is $\mathcal F_n = \sigma(X_0, \ldots, X_n)$. A martingale with respect to some filtration $(\mathcal F_n)$ is also a martingale with respect to $\mathcal G_n = \sigma(X_0, \ldots, X_n)$: since $\mathcal G_n \subseteq \mathcal F_n$, the tower property gives $\mathbb E[X_{n+1} \mid \mathcal G_n] = \mathbb E[\mathbb E[X_{n+1} \mid \mathcal F_n] \mid \mathcal G_n] = \mathbb E[X_n \mid \mathcal G_n] = X_n$.

**First consequences.** Let $(X_n)$ be a martingale with respect to $(\mathcal F_n)$.

- *The mean is constant.* Taking expectations of condition 3 gives $\mathbb E[X_{n+1}] = \mathbb E[X_n]$, so $\mathbb E[X_n] = \mathbb E[X_0]$ for each fixed $n$.
- *Every later value.* For $m \ge n$, $\mathbb E[X_m \mid \mathcal F_n] = X_n$. By induction on $m$: $\mathbb E[X_{m+1} \mid \mathcal F_n] = \mathbb E[\mathbb E[X_{m+1} \mid \mathcal F_m] \mid \mathcal F_n] = \mathbb E[X_m \mid \mathcal F_n]$, because $\mathcal F_n \subseteq \mathcal F_m$.
- *Differences.* The differences $D_n = X_n - X_{n-1}$ satisfy $\mathbb E[D_n \mid \mathcal F_{n-1}] = 0$. They form a *martingale difference sequence*. Conversely, partial sums of a martingale difference sequence form a martingale.
- *Orthogonal differences.* If $\mathbb E[X_n^2] < \infty$ for each $n$, then $\mathbb E[D_j D_k] = 0$ for $j < k$: $D_j$ is $\mathcal F_{k-1}$-measurable, the product is integrable by the Cauchy-Schwarz inequality, and $\mathbb E[D_j D_k] = \mathbb E[D_j\, \mathbb E[D_k \mid \mathcal F_{k-1}]] = 0$. So $\operatorname{Var}(X_n) = \operatorname{Var}(X_0) + \sum_{k=1}^n \mathbb E[D_k^2]$, the same rule as for a sum of independent terms, although the differences need not be independent.
- *Convex functions.* If $\varphi$ is convex and each $\varphi(X_n)$ is integrable, then $\varphi(X_n)$ is a submartingale, by the conditional form of [Jensen's inequality](/jensens-inequality/): $\mathbb E[\varphi(X_{n+1}) \mid \mathcal F_n] \ge \varphi(\mathbb E[X_{n+1} \mid \mathcal F_n]) = \varphi(X_n)$. Examples are $X_n^2$ and $|X_n|$.

**Stopping times.** A *stopping time* is a random variable $T$ with values in $\{0, 1, 2, \ldots\} \cup \{\infty\}$ such that the event $\{T = n\}$ is in $\mathcal F_n$ for each $n$. In words, the decision to stop at time $n$ uses only the information up to time $n$. The first time that a random walk hits a level is a stopping time. The first time that a randomized search finds a solution is a stopping time. The last visit of a walk to 0 before time 100, and the time at which the walk reaches its maximum over the first 100 steps, are not: each needs the future. The *stopped process* $X_{n \wedge T}$ is again a martingale, and under conditions on $T$ the mean at the random time is the mean at the start, $\mathbb E[X_T] = \mathbb E[X_0]$. The exact conditions and their proofs are on the page of the [optional stopping theorem](/optional-stopping-theorem/).

**The Doob martingale.** Let $Y$ be a random variable with $\mathbb E|Y| < \infty$, and let $(\mathcal F_n)$ be a filtration. Then $Y_n = \mathbb E[Y \mid \mathcal F_n]$ is a martingale: $Y_n$ is $\mathcal F_n$-measurable, $\mathbb E|Y_n| \le \mathbb E|Y|$ by the conditional Jensen inequality, and $\mathbb E[Y_{n+1} \mid \mathcal F_n] = \mathbb E[\mathbb E[Y \mid \mathcal F_{n+1}] \mid \mathcal F_n] = \mathbb E[Y \mid \mathcal F_n] = Y_n$ by the tower property. In the usual use, $Y = f(Z_1, \ldots, Z_n)$ is a function of $n$ random choices, $\mathcal F_0$ is trivial and $\mathcal F_k = \sigma(Z_1, \ldots, Z_k)$. Then $Y_0 = \mathbb E[Y]$ and $Y_n = Y$: the martingale starts at the mean and ends at the actual value, and it reveals one choice at each step. If revealing one choice moves the conditional expectation by at most $c_k$, then [Azuma's inequality](/azuma-inequality/) bounds $\Pr(|Y - \mathbb E Y| \ge t)$. This is the *method of bounded differences*, see [concentration of measure](/concentration-of-measure/).

### Pitfalls

- **A constant mean is not enough.** Let $X_0 = 0$, let $X_1 = \pm 1$ with probability $\frac12$ each, and let $X_2 = 2X_1$. Then $\mathbb E[X_0] = \mathbb E[X_1] = \mathbb E[X_2] = 0$, but $\mathbb E[X_2 \mid X_1] = 2X_1 \ne X_1$. The definition asks for the conditional expectation given the whole past, not for equal means.
- **The filtration matters.** The walk $S_n$ below is a martingale for $\mathcal F_n = \sigma(\xi_1, \ldots, \xi_n)$. For the larger filtration $\mathcal F'_n = \sigma(\xi_1, \ldots, \xi_{n+1})$, which sees one step ahead, $\mathbb E[S_{n+1} \mid \mathcal F'_n] = S_{n+1} \ne S_n$. In an analysis, the information at time $n$ must not contain random choices that the algorithm makes later.
- **Integrability is part of the definition.** If $\mathbb E|Y| = \infty$, then $X_n = Y$ for all $n$ satisfies the equation of condition 3 in a formal way, but it is not a martingale, and statements such as $\mathbb E[X_n] = \mathbb E[X_0]$ have no meaning.
- **Uncorrelated is not independent.** The differences of a martingale are uncorrelated, but they can depend on each other strongly. A [Chernoff bound](/chernoff-bound/) needs independence and does not apply. Azuma's inequality is the tool for martingales.
- **Fixed times only.** $\mathbb E[X_n] = \mathbb E[X_0]$ holds at each fixed time $n$. At a random time it can fail: the doubling strategy at a fair game wins 1 with probability 1. See the [optional stopping theorem](/optional-stopping-theorem/).
- **Convergence of the values is not convergence of the means.** The likelihood ratio below has mean 1 at each time and still tends to 0 with probability 1.

## Examples

### The fair gambler

Let $\xi_1, \xi_2, \ldots$ be independent with $\Pr(\xi_i = 1) = \Pr(\xi_i = -1) = \frac12$, let $S_0 = 0$ and $S_n = \xi_1 + \cdots + \xi_n$, and let $\mathcal F_n = \sigma(\xi_1, \ldots, \xi_n)$. Then $\mathbb E[S_{n+1} \mid \mathcal F_n] = S_n + \mathbb E[\xi_{n+1}] = S_n$, because $\xi_{n+1}$ is independent of $\mathcal F_n$. So the simple random walk is a martingale. For a biased walk with $\Pr(\xi_i = 1) = p$ and $\Pr(\xi_i = -1) = q = 1 - p$, two martingales replace it.

- $S_n - (p - q)n$, because $\mathbb E[\xi_{n+1}] = p - q$.
- $r^{S_n}$ with $r = q/p$, because $\mathbb E[r^{\xi_{n+1}}] = pr + q/r = q + p = 1$.

With the optional stopping theorem the second one gives the probability of ruin of a gambler at an unfair table. At American roulette, where a bet on red wins with probability $p = 18/38$, a player who bets 1 at a time and stops on a gain of 10 or a loss of 10 reaches the gain first with probability $0.2585$, and plays $91.76$ rounds on average.

### The squared walk

For the fair walk, $M_n = S_n^2 - n$ is a martingale: $\mathbb E[S_{n+1}^2 \mid \mathcal F_n] = S_n^2 + 2S_n\mathbb E[\xi_{n+1}] + \mathbb E[\xi_{n+1}^2] = S_n^2 + 1$. So $S_n^2$ is a submartingale, as the rule for convex functions says, and $n$ is exactly the amount that it gains on average. With optional stopping, $M_n$ gives the expected duration of the fair game: a gambler with 3 units who plays until a loss of 3 or a gain of 7 reaches the gain first with probability $3/10$ and plays $21$ rounds on average.

### Likelihood ratios

Let $Z_1, Z_2, \ldots$ be independent with distribution $P$ on a countable set, and let $Q$ be a second distribution with $Q(z) = 0$ whenever $P(z) = 0$. Then $L_n = \prod_{i=1}^n Q(Z_i)/P(Z_i)$ is a martingale with mean 1: $\mathbb E[L_{n+1} \mid \mathcal F_n] = L_n \sum_{z : P(z) > 0} P(z)\,Q(z)/P(z) = L_n$. It is the basis of sequential tests. For a fair coin ($P$) and a coin with heads probability $0.6$ ($Q$), each head multiplies $L_n$ by $1.2$ and each tail by $0.8$. After 100 tosses of the fair coin, $\mathbb E[L_{100}] = 1$ exactly, but $\Pr(L_{100} < 1) = 0.864$, and $\Pr(L_{100} \ge 20) = 0.0060$, below the value $1/20$ that [Markov's inequality](/markov-inequality/) allows. After 1000 tosses with 500 heads, $L_{1000} = 0.96^{500} = 1.37 \times 10^{-9}$. By the [law of large numbers](/law-of-large-numbers/), $\frac1n \ln L_n \to \frac12\ln 1.2 + \frac12 \ln 0.8 = -0.0204$ with probability 1, so $L_n \to 0$ almost surely while $\mathbb E[L_n] = 1$ for all $n$. A few rare paths with huge $L_n$ carry the whole mean.

### Pólya's urn

An urn holds one red and one blue ball. At each step, draw a ball uniformly at random and put it back together with one more ball of the same color. After $n$ steps the urn has $n + 2$ balls. Let $R_n$ be the number of red balls and $M_n = R_n/(n+2)$ the fraction of red. Then
$$ \mathbb E[M_{n+1} \mid \mathcal F_n] = \frac{1}{n+3}\left(R_n + \frac{R_n}{n+2}\right) = \frac{R_n (n+3)}{(n+2)(n+3)} = M_n, $$
so the fraction of red is a martingale. Unlike the sums above, it does not concentrate. By induction, $R_n$ is uniform on $\{1, \ldots, n+1\}$: if $\Pr(R_n = r) = \frac1{n+1}$ for each $r$, then $\Pr(R_{n+1} = r) = \frac{1}{n+1}\cdot\frac{(r - 1) + (n + 2 - r)}{n+2} = \frac1{n+2}$ for $1 \le r \le n+2$ (the first term is the draw of red from $r - 1$ red balls, the second the draw of blue with $r$ red balls). After 10 steps each of the values 1 to 11 has probability $1/11$, and the mean fraction is exactly $\frac12$. The change at step $n+1$ is at most $\frac{1}{n+3}$, and the sum of the squares of these bounds stays bounded, so Azuma's inequality gives no concentration here, as it must.

### Exposure martingales on random graphs

Let $G$ be a random graph $G(n, p)$ (the [Erdős-Rényi model](/erdos-renyi-model/)) and $f$ a function of graphs, for example the [chromatic number](/chromatic-number/) $\chi$. Order the $m = \binom n2$ vertex pairs. The *edge exposure martingale* is $X_k = \mathbb E[f(G) \mid$ the presence of the first $k$ pairs$]$, for $k = 0, \ldots, m$. The *vertex exposure martingale* is $X_i = \mathbb E[f(G) \mid$ the edges among vertices $1, \ldots, i]$, for $i = 1, \ldots, n$, plus $X_0 = \mathbb E[f(G)]$. Both are Doob martingales.

For $n = 3$ and $p = \frac12$, with pairs $\{1,2\}, \{1,3\}, \{2,3\}$: the graph has $\chi = 1$ with no edge, $\chi = 3$ for the triangle, and $\chi = 2$ otherwise. So $X_0 = \frac18 \cdot 1 + \frac68 \cdot 2 + \frac18 \cdot 3 = 2$. After the first pair, $X_1 = \frac94$ if it is an edge and $\frac74$ if not. After two pairs, $X_2 = \frac52, 2, 2, \frac32$ for the outcomes (edge, edge), (edge, no), (no, edge), (no, no). Then $X_3 = \chi$. Each value is the average of its two successors, for example $\frac94 = \frac12(\frac52 + 2)$. The vertex exposure martingale here is $2, 2, X_1, \chi$: vertex 1 reveals nothing, vertex 2 reveals the first pair, and vertex 3 reveals the other two pairs at once, so it skips the value $X_2$ of the edge exposure.

Changing the edges at one vertex changes $\chi$ by at most 1, so each step of the vertex exposure martingale moves by at most 1. With Azuma's inequality this gives the theorem of Shamir and Spencer that $\chi(G(n,p))$ lies within $O(\sqrt n)$ of its mean with high probability, without knowing the mean. The numbers are on the page of [Azuma's inequality](/azuma-inequality/).

## Where it is used

- **Concentration.** [Azuma's inequality](/azuma-inequality/) and the method of bounded differences give tail bounds for the number of empty bins in [balls into bins](/balls-into-bins/), the number of occurrences of a pattern in a random string, the chromatic number of a random graph, and many other functions of independent random choices. See [concentration of measure](/concentration-of-measure/).
- **Expected running times.** If a potential $\Phi_t$ of the state of an algorithm makes $\Phi_t + t$ a supermartingale, then the optional stopping theorem bounds the expected running time by the initial potential. This gives the bound of $n^2$ expected steps for the random walk algorithm for [2-SAT](/2-sat/). A random walk of the same kind, with steps toward a fixed solution, is the base of the analysis of [Schöning's algorithm](/schoning-algorithm/) for [k-SAT](/k-sat/).
- **Hitting probabilities.** The gambler's ruin probabilities and expected durations follow from the martingales $S_n$, $S_n^2 - n$ and $r^{S_n}$ above, by optional stopping.
- **Random sums.** [Wald's equation](/walds-equation/) for the cost of a random number of independent trials, such as the restarts of a [Las Vegas algorithm](/las-vegas-algorithm/) or the trials of [rejection sampling](/rejection-sampling/), is optional stopping for the martingale $S_n - n\mu$.
- **Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) follows one path of a Doob martingale. At each step the current conditional expectation is the average of its values over the next choice, so some choice keeps it at least as large. The choice is made by computation instead of by a coin.

## References
