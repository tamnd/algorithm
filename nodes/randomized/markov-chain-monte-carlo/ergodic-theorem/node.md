---
tag: D502BV
kind: theorem
slug: ergodic-theorem
name: Ergodic theorem for Markov chains
aliases:
- law of large numbers for Markov chains
area: randomized/markov-chain-monte-carlo
level: advanced
summary: For an irreducible finite Markov chain and any start, the average of f(X_s) over time tends to the mean of f under π with probability 1. Aperiodicity is not needed.
prereqs: [irreducibility, stationary-distribution, law-of-large-numbers]
see_also: [ergodicity, central-limit-theorem, mcmc-autocorrelation, effective-sample-size, burn-in, monte-carlo-integration, gelman-rubin-diagnostic, martingale]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Appendix C, Theorem C.1 (Ergodic Theorem); Section 1.5, Lemma 1.13 and Proposition 1.19 (Kac)
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.4, Strong Markov property; Section 1.10, Ergodic theorem
  - paper: doi:10.1214/154957804100000051
    title: Galin L. Jones, On the Markov chain central limit theorem, Probability Surveys 1, 2004
    locator: pp. 299 to 320; the conditions for a CLT under uniform and geometric ergodicity, and the form of the asymptotic variance
  - paper: doi:10.1007/BF01210789
    title: C. Kipnis and S. R. S. Varadhan, Central limit theorem for additive functionals of reversible Markov processes and applications to simple exclusions, Communications in Mathematical Physics 104(1), 1986
    locator: pp. 1 to 19; the CLT for reversible chains started from π
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 6, Markov Chains (ergodic theorems and the central limit theorem)
---

The ergodic theorem for Markov chains is the strong [law of large numbers](/law-of-large-numbers/) for the states of a [Markov chain](/markov-chain/). For an [irreducible](/irreducibility/) chain on a finite state space, with [stationary distribution](/stationary-distribution/) $\pi$, the average $\frac1t\sum_{s<t} f(X_s)$ tends to $\mathbb E_\pi f = \sum_x \pi(x)f(x)$ with probability 1, from any start. Unlike the convergence theorem on the page [ergodicity](/ergodicity/), it does not need aperiodicity, because it is about the average along one path and not about the law of one $X_t$. It is the theorem that justifies Markov chain Monte Carlo estimates, and a Markov chain [central limit theorem](/central-limit-theorem/) gives their error.

## Statement

Let $P$ be a transition matrix on a finite set $\mathcal X$, let $\pi$ be a stationary distribution, and let $f : \mathcal X \to \mathbb R$. Write $\bar f_t = \frac1t\sum_{s=0}^{t-1} f(X_s)$ and $\mathbb E_\pi f = \sum_x \pi(x)f(x)$.

**Theorem 1 (ergodic theorem; LPW Theorem C.1).** If $P$ is irreducible, then for each initial distribution $\mu$,
$$
\Pr_\mu\Bigl[\lim_{t \to \infty} \bar f_t = \mathbb E_\pi f\Bigr] = 1.
$$
With $f = \mathbf 1\{\cdot = y\}$: the fraction of the times $s < t$ with $X_s = y$ tends to $\pi(y)$ with probability 1.

**Theorem 2 (Markov chain central limit theorem, finite state space).** If $P$ is irreducible and aperiodic, then for each initial distribution,
$$
\sqrt t\,\bigl(\bar f_t - \mathbb E_\pi f\bigr) \ \xrightarrow{\ d\ }\ \mathcal N(0, \sigma_f^2), \qquad
\sigma_f^2 = \operatorname{Var}_\pi f + 2\sum_{k \ge 1}\operatorname{Cov}_\pi\bigl(f(X_0), f(X_k)\bigr),
$$
where $\operatorname{Cov}_\pi$ is the covariance of the stationary chain ($X_0 \sim \pi$). The series converges absolutely, because the convergence theorem makes its terms fall at a geometric rate. When $\sigma_f^2 = 0$ the limit is the point mass at 0.

We prove Theorem 1 in full. We state Theorem 2 with its hypotheses and cite it (Jones 2004 surveys the proofs). For general state spaces, Jones gives these sufficient conditions: a uniformly ergodic chain with $\mathbb E_\pi f^2 < \infty$, or a geometrically ergodic chain with $\mathbb E_\pi|f|^{2+\delta} < \infty$ for some $\delta > 0$. Kipnis and Varadhan (1986) prove a CLT for reversible chains started from $\pi$, for each $f$ with $\mathbb E_\pi f^2 < \infty$ and a finite limit variance. For a finite irreducible periodic chain a CLT also holds, with $\sigma_f^2$ given through the solution of the Poisson equation, but we do not use that form here.

## In plain words

Follow one run of a random process that moves between a finite number of states, where each state can reach each other one. Count how often the run visits each state. In the long run these fractions settle down to fixed numbers, and these numbers do not depend on where the run started. The same holds for the average of any score that you give to the states. This is why one long run of a well-made random process can estimate an average over a complex set. The run does not have to settle in the sense of "forget its start at each fixed time". It only has to keep visiting all the states. The error of the estimate shrinks like one over the square root of the run length, but it is larger than for independent samples when the steps of the run are strongly related.

## Proof

We use two facts from other pages. For an irreducible finite chain, $\mathbb E_x\tau_z^+ < \infty$ for all $x, z$, where $\tau_z^+ = \min\{t \ge 1 : X_t = z\}$ (LPW Lemma 1.13, proved on [irreducibility](/irreducibility/)). And for a fixed state $z$, the expected number of visits to $y$ during one excursion from $z$ is
$$
\tilde\pi(y) = \mathbb E_z\Bigl[\sum_{s=0}^{\tau_z^+ - 1}\mathbf 1\{X_s = y\}\Bigr] = \frac{\pi(y)}{\pi(z)}, \qquad \mathbb E_z\tau_z^+ = \frac{1}{\pi(z)},
$$
which is part 4 of the theorem on [stationary distribution](/stationary-distribution/) (Kac's formula). We also use the *strong Markov property* (Norris, Section 1.4): at a stopping time $\tau$ with $X_\tau = z$, the chain $(X_{\tau + s})_{s \ge 0}$ is a Markov chain with matrix $P$ started at $z$, independent of $X_0, \ldots, X_\tau$.

*Proof of Theorem 1.* Fix a state $z$ and the start $\mu$. Let $\tau_0 = \min\{t \ge 0 : X_t = z\}$ and, for $k \ge 1$, $\tau_k = \min\{t > \tau_{k-1} : X_t = z\}$. Each $\tau_k$ is finite with probability 1, because $\mathbb E_x\tau_z^+ < \infty$ for each $x$.

*Step 1: the excursions are independent.* For $k \ge 1$ let
$$
L_k = \tau_k - \tau_{k-1}, \qquad Y_k = \sum_{s = \tau_{k-1}}^{\tau_k - 1} f(X_s).
$$
By the strong Markov property at $\tau_{k-1}$, the excursion $(X_{\tau_{k-1}}, \ldots, X_{\tau_k - 1})$ has the law of the excursion of the chain started at $z$ up to $\tau_z^+$, and it is independent of what came before. So the pairs $(L_k, Y_k)$, $k \ge 1$, are independent and identically distributed.

*Step 2: their means.* $\mathbb E L_k = \mathbb E_z\tau_z^+ = 1/\pi(z)$. Also $|Y_k| \le \|f\|_\infty L_k$, so $\mathbb E|Y_k| < \infty$, and
$$
\mathbb E Y_k = \mathbb E_z\Bigl[\sum_{s < \tau_z^+} f(X_s)\Bigr] = \sum_y f(y)\,\tilde\pi(y) = \frac{\mathbb E_\pi f}{\pi(z)}.
$$

*Step 3: the strong law.* By the strong law of large numbers for independent identically distributed variables, with probability 1,
$$
\frac1n\sum_{k=1}^n Y_k \to \frac{\mathbb E_\pi f}{\pi(z)}, \qquad \frac{\tau_n}{n} = \frac{\tau_0}{n} + \frac1n\sum_{k=1}^n L_k \to \frac{1}{\pi(z)}.
$$
The second limit also gives $L_n/n = \tau_n/n - \tau_{n-1}/n \to 0$.

*Step 4: from excursions to all times.* For $t > \tau_1$ let $N_t = \max\{n : \tau_n \le t\}$, so $\tau_{N_t} \le t < \tau_{N_t + 1}$, and $N_t \to \infty$ as $t \to \infty$. Split the sum:
$$
\sum_{s=0}^{t-1} f(X_s) = \sum_{s < \tau_0} f(X_s) + \sum_{k=1}^{N_t} Y_k + R_t, \qquad |R_t| \le \|f\|_\infty L_{N_t + 1}.
$$
The first term is a fixed finite number for the path. Divide by $N_t$: the first term over $N_t$ tends to 0, the middle term over $N_t$ tends to $\mathbb E_\pi f/\pi(z)$ by Step 3, and $|R_t|/N_t \le \|f\|_\infty \frac{L_{N_t+1}}{N_t + 1}\cdot\frac{N_t + 1}{N_t} \to 0$. From $\tau_{N_t} \le t < \tau_{N_t + 1}$ we get
$$
\frac{\tau_{N_t}}{N_t} \le \frac{t}{N_t} < \frac{\tau_{N_t + 1}}{N_t + 1}\cdot\frac{N_t + 1}{N_t},
$$
and both sides tend to $1/\pi(z)$, so $N_t/t \to \pi(z)$. Hence
$$
\bar f_t = \frac{N_t}{t}\cdot\frac{1}{N_t}\sum_{s=0}^{t-1} f(X_s) \to \pi(z)\cdot\frac{\mathbb E_\pi f}{\pi(z)} = \mathbb E_\pi f
$$
with probability 1. $\square$

Nothing in the proof uses aperiodicity. The same regeneration argument, with the i.i.d. central limit theorem in Step 3, is one standard route to Theorem 2.

## Consequences

**Markov chain Monte Carlo is consistent.** To estimate $\mathbb E_\pi f$, build an irreducible chain with stationary distribution $\pi$ (for example by [Metropolis-Hastings](/metropolis-hastings/) or [Gibbs sampling](/gibbs-sampling/)), run it, and average $f$ along the path. Theorem 1 says the estimate converges for any start. The start and a [burn-in](/burn-in/) period change the error for a finite run, not the limit.

**The error and the effective sample size.** Theorem 2 gives an approximate confidence interval $\bar f_t \pm 1.96\,\sigma_f/\sqrt t$, where $\sigma_f^2$ must itself be estimated, for example by batch means. The ratio $t\operatorname{Var}_\pi f/\sigma_f^2$ is the [effective sample size](/effective-sample-size/): the number of independent draws from $\pi$ that give the same variance. The covariances in $\sigma_f^2$ are the [autocorrelations](/mcmc-autocorrelation/) of the chain.

**A worked example.** Take the two-state chain $P = \begin{pmatrix} 3/4 & 1/4 \\ 1/2 & 1/2 \end{pmatrix}$, so $a = 1/4$, $b = 1/2$, $\pi = (2/3, 1/3)$, and the second eigenvalue is $\lambda = 1 - a - b = 1/4$. Let $f$ be the indicator of the second state. Then $\mathbb E_\pi f = 1/3$ and $\operatorname{Var}_\pi f = \tfrac13\cdot\tfrac23 = 2/9$. For this chain $\operatorname{Cov}_\pi(f(X_0), f(X_k)) = \lambda^k\operatorname{Var}_\pi f$, so
$$
\sigma_f^2 = \operatorname{Var}_\pi f\Bigl(1 + \frac{2\lambda}{1 - \lambda}\Bigr) = \frac29\cdot\frac{1 + \lambda}{1 - \lambda} = \frac29\cdot\frac53 = \frac{10}{27}.
$$
In general for two states, $\sigma_f^2 = ab(2 - a - b)/(a + b)^3$. A run of length $t$ is worth $3t/5$ independent draws for this $f$.

**Periodic chains.** The walk that alternates between two states has period 2. The law of $X_t$ does not converge, but by Theorem 1 the fraction of time in each state tends to $1/2$. Time averages are valid estimates for periodic chains.

**Frequencies estimate $\pi$.** With indicator functions, the empirical frequencies of the states converge to $\pi$. This is how one reads off $\pi$ from a long simulation, and how [PageRank](/pagerank/) can be estimated by random surfers.

## Tightness

**Irreducibility is needed.** Let states 1 and 3 be absorbing, and let state 2 move to each with probability $1/2$. From state 2, the fraction of time in state 1 tends to 1 with probability $1/2$ and to 0 with probability $1/2$. The limit exists but is random, and it is not $\mathbb E_\pi f$ for a single $\pi$. In general, for a reducible finite chain the limit is $\mathbb E_{\pi_C} f$, where $C$ is the closed class that the path enters, and $\pi_C$ its stationary distribution.

**Finiteness (or positive recurrence) is needed.** For the simple random walk on the integers, the fraction of time at 0 tends to 0 with probability 1, and there is no stationary distribution to compare with. On infinite spaces the theorem needs positive recurrence (Norris, Section 1.10).

**No rate from Theorem 1.** The strong law gives no speed. The speed depends on the chain: by Theorem 2 the error is of order $\sigma_f/\sqrt t$, and $\sigma_f^2$ can be huge when the chain has a bottleneck. For a reversible aperiodic chain with [spectral gap](/spectral-gap/) $\gamma = 1 - \lambda_2$, the spectral form $\sigma_f^2 = \sum_{j \ge 2}\frac{1 + \lambda_j}{1 - \lambda_j}\langle f, f_j\rangle_\pi^2$ gives $\sigma_f^2 \le \frac{2}{\gamma}\operatorname{Var}_\pi f$. See [conductance](/conductance/) and [mixing time](/mixing-time/).

**Diagnostics cannot prove convergence.** The theorem says that the average converges; it does not tell when the average is already close. Tools such as the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) can show that a run has not converged, but they cannot prove that it has. A chain with a deep bottleneck can look stable for a very long time in one part of the space.

## History

Andrei Markov introduced chains in 1906 to show that the law of large numbers holds for some dependent variables. George D. Birkhoff (1931) proved the pointwise ergodic theorem for measure-preserving maps, and John von Neumann (1932) the mean ergodic theorem; for an irreducible chain started from $\pi$, Birkhoff's theorem gives Theorem 1. The proof by excursions between visits to a fixed state is the one in textbooks such as Norris (Section 1.10). Kipnis and Varadhan (1986) proved the CLT for reversible processes, and Jones (2004) surveyed the conditions for the CLT that are used in Markov chain Monte Carlo.

## References
