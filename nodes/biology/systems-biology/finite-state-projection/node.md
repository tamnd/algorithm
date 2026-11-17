---
tag: 62X0PG
kind: algorithm
slug: finite-state-projection
name: Finite state projection
aliases:
- FSP
area: biology/systems-biology
level: research
summary: Solves the chemical master equation on a finite set of states, with a certified bound on the error from the probability that leaves the set.
model: real-ram
complexity:
  vars: {s: the number of states in the final projection, m: the number of reactions, R: the number of rounds of growth, q: the largest total propensity on the projection, t: the end time, epsilon: the error tolerance}
  time: {worst: O(R s m (q t + 1))}
  space: {extra: Θ(s m)}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2006
  people: [Brian Munsky, Mustafa Khammash]
  note: Munsky and Khammash gave the finite state projection and its error bound in the Journal of Chemical Physics in 2006.
prereqs: [chemical-master-equation, matrix-exponential]
see_also: [gillespie-algorithm, krylov-subspace, arnoldi-iteration, sparse-matrix, markov-chain, stationary-distribution, moment-closure, linear-noise-approximation]
sources:
  - paper: doi:10.1063/1.2145882
    title: Brian Munsky and Mustafa Khammash, The finite state projection algorithm for the solution of the chemical master equation, Journal of Chemical Physics 124(4), 2006, 044104
    locator: the projection of the master equation onto a finite set of states, the bound on the error by the lost probability, and the algorithm that grows the set
  - paper: doi:10.1007/s00285-006-0034-x
    title: Tobias Jahnke and Wilhelm Huisinga, Solving the chemical master equation for monomolecular reaction systems analytically, Journal of Mathematical Biology 54(1), 2007, 1-26
    locator: closed form solutions for first order networks, useful as test cases
  - book: isbn:9781138549289
    title: Darren J. Wilkinson, Stochastic Modelling for Systems Biology, 3rd edition, CRC Press, 2018
    locator: the chapter on Markov processes in continuous time (the generator and the matrix exponential)
---

Finite state projection (FSP) computes the probabilities of the [chemical master equation](/chemical-master-equation/) directly, without sampling. The master equation $\dot P = AP$ is linear, but its state space is usually infinite, or finite and far too large to list. FSP keeps only a finite set $J$ of states, solves the master equation restricted to $J$ with the [matrix exponential](/matrix-exponential/), and lets the probability that flows out of $J$ disappear. Munsky and Khammash (2006) proved that this is safe in a precise sense: the computed values are never above the true probabilities, and the total error, measured in the L1 norm over all states, equals exactly the probability that was lost. So the sum of the computed values certifies its own accuracy. If the lost mass is larger than the tolerance, the algorithm adds the states that the reactions reach from $J$ and solves again. It is the method of choice for small networks such as models of one or two genes, where it gives the full distribution with an error of $10^{-6}$ or less.

## In plain words

The exact equation tracks the chance of every possible count of molecules, and there are endlessly many counts. But most of them are so unlikely that they do not matter.

So pick a list of counts that you think matter, and track only those. Chance that would move to a count outside the list is simply dropped. At the end, add up what is left. If the total is 0.999999, you know that you lost at most one part in a million, and that no answer is off by more than that in total.

If too much was lost, the list was too short. Add the counts that can be reached in one reaction from the list, and solve again. Repeat until the loss is small enough.

## The problem

**Input.** A network with change vectors $\nu_j$ and propensities $a_j(x)$; a start state $x_0$ (or a start distribution with finite support); a time $t$; a tolerance $\epsilon > 0$.

**Output.** A finite set $J$ of states and a vector $p$ on $J$ such that

$$0 \le p(x) \le P(x, t) \text{ for } x \in J, \qquad \sum_{x \in J} |P(x, t) - p(x)| + \sum_{x \notin J} P(x, t) \le \epsilon,$$

where $P$ solves the master equation. The second sum is the L1 distance between $P(\cdot, t)$ and $p$ extended by 0.

**The projection.** Let $A_J$ be the generator restricted to the rows and columns in $J$: $(A_J)_{xx} = -a_0(x)$ and $(A_J)_{yx} = a_j(x)$ when $y = x + \nu_j$, for $x, y \in J$. Its columns sum to 0 or less: the deficit in column $x$ is the rate at which probability leaves $J$ from $x$. The projected solution is $p(t) = e^{A_J t} p(0)$.

## The algorithm

```pseudo id=main
FSP(x0, ν, a, t, ε)
L1  J ← {x0}
L2  loop
L3      build the sparse matrix A_J on J
L4      p ← exp(A_J t) e_x0
L5      if 1 - Σ_{x ∈ J} p(x) ≤ ε then return (J, p)
L6      J ← J ∪ {x + ν_j : x ∈ J, a_j(x) > 0}
```

Line L4 is the action of the matrix exponential on a vector. The implementation uses uniformization: with $q \ge \max_{x \in J} a_0(x)$ and $Q = I + A_J/q$, $e^{A_J t} = \sum_k e^{-qt} \frac{(qt)^k}{k!} Q^k$, where every term is $\ge 0$. It splits $t$ into pieces with $q\,\delta t \le 10$ so that the Poisson weights stay in floating point range. Large problems use a Krylov method instead. Line L6 adds every state that one reaction reaches from $J$, so after $N$ rounds $J$ holds every state reachable in at most $N$ reactions.

## Example

Take immigration-death, $\emptyset \to X$ at rate 10 and $X \to \emptyset$ at rate $x$, from $x_0 = 0$ to $t = 1$. The exact law is Poisson$(10(1 - e^{-1}))$ = Poisson$(6.321206)$. Here line L6 adds one state per round, so $J = \{0, \ldots, s - 1\}$ after $s$ rounds.

| tolerance $\epsilon$ | states in $J$ | lost mass |
|---|---|---|
| $10^{-2}$ | 15 | $4.2 \times 10^{-3}$ |
| $10^{-4}$ | 19 | $7.0 \times 10^{-5}$ |
| $10^{-6}$ | 23 | $5.19 \times 10^{-7}$ |
| $10^{-8}$ | 26 | $8.3 \times 10^{-9}$ |
| $10^{-12}$ | 32 | $8.1 \times 10^{-13}$ |

Each factor of 100 in the tolerance costs only a few more states, because the Poisson tail falls faster than geometrically.

A projection that is too small shows how the bound works. With $J = \{0, \ldots, 5\}$:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| FSP $p(x)$ | 0.001761 | 0.010878 | 0.032807 | 0.062846 | 0.081337 | 0.063639 |
| exact $P(x, 1)$ | 0.001798 | 0.011364 | 0.035917 | 0.075680 | 0.119598 | 0.151201 |

Every value is below the exact one, as the theorem says. The lost mass is 0.746732, which is larger than the true tail $P(X > 5) = 0.604442$: the projection also loses the paths that leave $J$ and come back. The sum of the errors in $J$, $0.746732 - 0.604442 = 0.142290$, plus the tail is the lost mass, as the identity says.

## Correctness

The key fact is that $e^{A_J s}$ has entries $\ge 0$, because $A_J + qI$ has entries $\ge 0$. Write the rows of the full master equation for the states in $J$ as $\dot P_J = A_J P_J + f$, where $f \ge 0$ is the flow into $J$ from outside. By variation of constants, $P_J(t) = e^{A_J t} P_J(0) + \int_0^t e^{A_J(t-s)} f(s)\, ds \ge e^{A_J t} P_J(0) = p(t)$. So $p \le P$ on $J$, every error term in $J$ is $P(x, t) - p(x)$, and the L1 error adds up to $1 - \sum p$. A larger $J$ gives larger values, so the lost mass only goes down as $J$ grows. The loop stops: $J_N$ holds all states reachable in $N$ reactions, the lost mass is at most the probability of more than $N$ jumps in $[0, t]$, and this tends to 0 if the process does not explode. Cutting the uniformization series keeps the bound, since every term is $\ge 0$. The full proof is below.

## Complexity

- **One round.** $A_J$ has at most $m + 1$ nonzeros per column. Uniformization needs about $qt + O(\sqrt{qt})$ products with $Q$, so a round costs $O(s\, m\, (qt + 1))$. With a Krylov method the number of products is often much smaller than $qt$ for stiff problems.
- **Rounds.** Growth by one reaction step per round needs as many rounds as the number of reactions that typical paths make, $R$ in the bound. Growing $J$ by several steps at a time, or starting with a good guess (for example from a few runs of the [Gillespie algorithm](/gillespie-algorithm/)), cuts $R$ to a few.
- **States.** The main cost is $s$, the size of the final projection. For $n$ species whose counts each range over about $w$ values, $s$ is about $w^n$, so the method is limited to a few species with moderate counts. This is the curse of dimensionality of the master equation.
- **Space.** The sparse matrix with $O(sm)$ nonzeros and a few vectors of length $s$.

## Properties

- **Certified error.** The output carries its own bound: the lost mass is an upper bound on the L1 error, with no sampling noise and no unknown constant.
- **One-sided.** Every computed probability is at most the true one. Sums over sets of states are lower bounds, and adding the lost mass gives upper bounds.
- **Monotone.** A larger projection gives larger values in every state of the smaller one.
- **Deterministic.** The same input gives the same output. The whole distribution comes at once, including the tails and rare states that sampling would almost never visit.
- **Exact for finite closed systems.** If $J$ holds every reachable state, nothing is lost, and $p$ is the exact solution up to the error of the matrix exponential.

## Variants and improvements

- **Krylov methods.** Compute $e^{A_J t} v$ with an [Arnoldi iteration](/arnoldi-iteration/) in a [Krylov subspace](/krylov-subspace/), which works well for the stiff matrices of networks with fast and slow reactions.
- **Time stepping.** Split $[0, t]$ into intervals and allow a different $J$ on each, adding states where the mass moves and dropping states that become negligible (sliding windows). The error bounds of the intervals add up.
- **Aggregation and reduction.** Lump states that behave alike, or reduce the number of states with a reduced basis or a tensor format, at the cost of a bound that is harder to prove.
- **Stationary distributions.** The same truncation idea, with the outflow sent back to a chosen state, gives approximations of the [stationary distribution](/stationary-distribution/), with error bounds under conditions on the drift.
- **Inference.** Because FSP gives exact likelihoods of measured count distributions, it is used to fit gene expression models to single-cell data, for example from smFISH, by maximum likelihood.

## When to use it

Use it when the network has few species and the counts are at most a few hundred, so that the relevant states number up to about $10^6$, and when the full distribution or small probabilities are needed with a guaranteed error: models of a gene that switches between active and inactive, of transcription bursts, or of a small regulatory circuit fit to single-cell counts. For many species or large counts, sample with the [Gillespie algorithm](/gillespie-algorithm/), or approximate with the [linear noise approximation](/linear-noise-approximation/) or [moment closure](/moment-closure/).

## Pitfalls

- **Normalizing the result.** Dividing $p$ by its sum gives a vector that looks better but has no error bound; it can be above the true values. Report the lost mass instead.
- **Lost mass is not the tail.** The lost mass counts paths that left $J$ at any time, not only those outside $J$ at time $t$, so it is larger than the tail probability. A projection can lose much mass even when the final distribution lies inside $J$.
- **Bad growth.** Adding states in all directions in many species makes $J$ huge. Grow along the directions where the mass flows out, or use a shape such as a box or a simplex guided by sample runs.
- **Explosion and infinite time.** The bound needs a process that does not explode on $[0, t]$. As $t \to \infty$ in an open system, nearly all mass leaves any fixed $J$, so stationary laws need the variant with the outflow sent back.
- **Floating point.** For large $qt$, plain uniformization underflows ($e^{-qt}$ is 0), which is why the code splits the time. Rounding errors can also make tiny probabilities slightly negative in other matrix exponential methods; clip them.

## Implementations

## History

Munsky and Khammash introduced the finite state projection and its error bound in 2006, as a way to solve the chemical master equation directly for the small, noisy circuits of systems biology, where Monte Carlo estimates of rare events converge slowly. Many refinements followed in the next years: Krylov methods for the matrix exponential, multiple time intervals with moving sets, sliding windows, and stationary versions. Since about 2013, FSP has been used to fit models of transcription to single-molecule counts of mRNA in single cells, in work by Munsky and others.

## References
