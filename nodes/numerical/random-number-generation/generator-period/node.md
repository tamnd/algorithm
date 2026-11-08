---
tag: DX5XKR
kind: definition
slug: generator-period
name: Period of a generator
aliases:
- cycle length
- period length
area: numerical/random-number-generation
level: intro
summary: The length of the cycle that the state sequence of a deterministic generator enters, after which its outputs repeat.
prereqs: [congruence]
see_also: [pseudorandom-number-generator, seed, floyd-cycle-detection, brent-cycle-detection, multiplicative-order, primitive-polynomial, jump-ahead, equidistribution]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.1 (eventually periodic sequences, the period length and the start of the cycle, with the exercises on cycle detection) and Section 3.2.1 (period of the linear congruential method)
  - paper: "Pierre L'Ecuyer, Uniform random number generation, Annals of Operations Research 53, 1994, pages 77 to 120"
    locator: Section 2 (definition of a generator as a structure with a finite state space, a transition function and an output function, and the period)
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007
    locator: Section 2 (the generator model and the role of the period length)
  - paper: "Pierre L'Ecuyer and Richard Simard, On the performance of birthday spacings tests with certain families of random number generators, Mathematics and Computers in Simulation 55, 2001, pages 131 to 137"
    locator: the results for linear congruential generators (failure at a sample size of the order of the cube root of the period)
---

The period of a deterministic [pseudorandom number generator](/pseudorandom-number-generator/) is the length of the cycle that its state sequence enters. Because the state space is finite, each state sequence repeats in the end, and the outputs repeat with it. A long period is necessary for a good generator, but it is not sufficient: many generators with a huge period fail simple statistical tests.

## Definition

We use the notation of the random-number-generation pages. A generator is a tuple $(S, f, g, s_0)$: a finite state space $S$, a transition function $f : S \to S$, an output function $g$ from $S$ to an output set, and an initial state $s_0 \in S$ (the [seed](/seed/) sets it). The states are $s_{i+1} = f(s_i)$ for $i \ge 0$ and the outputs are $u_i = g(s_i)$.

**Eventual periodicity.** For each $s_0 \in S$ there are unique integers $\mu \ge 0$ and $\rho \ge 1$ such that

1. the states $s_0, s_1, \ldots, s_{\mu + \rho - 1}$ are pairwise distinct, and
2. $s_{i + \rho} = s_i$ for each $i \ge \mu$.

The number $\rho$ is the *period* (Knuth writes $\lambda$) and $\mu$ is the length of the *tail* (the preperiod). The states $s_\mu, \ldots, s_{\mu+\rho-1}$ form the *cycle*. The sequence is *purely periodic* when $\mu = 0$. From the definition, $\rho \le \mu + \rho \le |S|$.

*Proof of existence and uniqueness.* The $|S| + 1$ states $s_0, \ldots, s_{|S|}$ cannot all be distinct, so there is a least index $j$ such that $s_j = s_\mu$ for some $\mu < j$, and this $\mu$ is unique because $s_0, \ldots, s_{j-1}$ are distinct. Put $\rho = j - \mu \ge 1$. Then part 1 holds by the choice of $j$. For part 2, $s_{\mu + \rho} = s_\mu$, and if $s_{i+\rho} = s_i$ then $s_{i+1+\rho} = f(s_{i+\rho}) = f(s_i) = s_{i+1}$, so part 2 holds by induction on $i \ge \mu$. Any pair $(\mu', \rho')$ with properties 1 and 2 makes $j' = \mu' + \rho'$ the first index whose state repeats an earlier state, so $j' = j$ and $\mu' = \mu$. $\square$

**Bijective transition.** If $f$ is a bijection of $S$, then $\mu = 0$ for every seed. Indeed, if $\mu \ge 1$, then $f(s_{\mu - 1}) = s_\mu = s_{\mu+\rho} = f(s_{\mu+\rho-1})$ with $s_{\mu-1} \ne s_{\mu+\rho-1}$ by part 1, which contradicts injectivity. Most good generators (linear congruential with $\gcd(a, m) = 1$, linear generators over GF(2) with an invertible matrix, counter-based generators) have a bijective $f$.

**Output period.** The output sequence $u_i = g(s_i)$ satisfies $u_{i+\rho} = u_i$ for $i \ge \mu$, so it is eventually periodic too. Let its *output period* $\rho_u$ be the least $p \ge 1$ such that $u_{i+p} = u_i$ for all large enough $i$. Then $\rho_u$ divides $\rho$. Proof: let $d = \gcd(\rho_u, \rho)$ and pick integers $\alpha, \beta \ge 0$ with $\alpha \rho_u - \beta \rho = d$ (they exist because we may add $\rho$ to $\alpha$ and $\rho_u$ to $\beta$). For each $i \ge \mu$, $u_{i+d} = u_{i+d+\beta\rho} = u_{i+\alpha\rho_u} = u_i$. So $d$ is a period of the output, and $d \ge \rho_u$ by minimality, which forces $d = \rho_u$, that is, $\rho_u \mid \rho$. The output period can be much smaller than $\rho$ when $g$ discards information, as the example of the low bits below shows.

**Terms used with the period.**

- The *period of the generator* usually means the period from a recommended seed, or the largest period over all seeds.
- The generator has *full period* when $\rho = |S|$ for one seed, so the cycle visits every state. Then $f$ is a single cycle on $S$, and every seed gives $\rho = |S|$.
- For a linear generator over GF(2) with state $\{0, 1\}^k$, the state $0$ is a fixed point, so the best possible is $\rho = 2^k - 1$, called *maximal period*. The [primitive polynomial](/primitive-polynomial/) condition decides when it is reached.

## Examples and non-examples

**A full-period LCG.** The [linear congruential generator](/linear-congruential-generator/) $s_{i+1} = (5 s_i + 3) \bmod 16$ from $s_0 = 0$ gives

$$0, 3, 2, 13, 4, 7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, \ldots$$

so $\mu = 0$ and $\rho = 16 = |S|$. The [Hull-Dobell theorem](/hull-dobell-theorem/) predicts this: $c = 3$ is odd, and $a - 1 = 4$ is a multiple of 4.

**A multiplicative LCG with a short period.** With $c = 0$, $s_{i+1} = 5 s_i \bmod 16$ has $\rho = 4$ from $s_0 = 1$ (states 1, 5, 9, 13) and $\rho = 2$ from $s_0 = 2$ (states 2, 10). The period depends on the seed. For $m = 2^w$ and $c = 0$ the period is at most $2^{w-2}$ (Knuth, Section 3.2.1.2, Theorem C), and it is the [multiplicative order](/multiplicative-order/) of $a$ modulo $2^w$ when the seed is odd.

**The low bits of an LCG.** For $s_{i+1} = (5 s_i + 3) \bmod 2^8$ from $s_0 = 7$, the state period is 256, but bit 0 of the state runs $1, 0, 1, 0, \ldots$ with period 2, and bit 1 runs $1, 1, 0, 0, 1, 1, 0, 0, \ldots$ with period 4. In general bit $j$ of a full-period LCG modulo a power of two has period $2^{j+1}$. This is an output period that is a proper divisor of $\rho$.

**A tail, then a fixed point.** The 4-digit [middle-square method](/middle-square-method/) maps $x$ to the middle four digits of $x^2$, so $f(x) = \lfloor x^2 / 100 \rfloor \bmod 10^4$. From $s_0 = 5772$ it gives $5772, 3159, 9792, 8832, 42, 17, 2, 0, 0, \ldots$, so $\mu = 7$ and $\rho = 1$. From $s_0 = 2916$ it gives the cycle $2916, 5030, 3009, 540, 2916$ with $\mu = 0$ and $\rho = 4$. Over all 10000 seeds the period is always 1 or 4, and the longest $\mu + \rho$ is 111 (seed 6239, $\mu = 107$, $\rho = 4$). Here $f$ is not a bijection, so tails appear.

**Large periods.** The Park-Miller generator $s_{i+1} = 16807 s_i \bmod (2^{31} - 1)$ has $\rho = 2^{31} - 2$ for every seed in $1, \ldots, 2^{31} - 2$, because 16807 is a [primitive root](/primitive-root/) modulo the prime $2^{31} - 1$. The [Mersenne Twister](/mersenne-twister/) MT19937 has $\rho = 2^{19937} - 1$ for each nonzero state.

**Non-example: a period is not a quality.** The generator $s_{i+1} = (s_i + 1) \bmod 2^{64}$ with $u_i = s_i / 2^{64}$ has full period $2^{64}$, yet its outputs increase step by step and fail every test of independence. A long period says nothing about the dependence between nearby outputs.

**Non-example: an unbounded state.** A generator whose state is an integer counter with no bound, or a real number in exact arithmetic, has no finite $S$, so the definition does not apply. The digits of $\pi$ are not known to be periodic, and they come from no finite-state generator.

## Related definitions

- **Finding the period.** Treat $f$ as a function on a finite set and use [Floyd's cycle detection](/floyd-cycle-detection/) or [Brent's cycle detection](/brent-cycle-detection/). Both find $\mu$ and $\rho$ in $O(\mu + \rho)$ evaluations of $f$ and $O(1)$ stored states. This is practical only for small $S$. For algebraic generators the period comes from a theorem instead: the [Hull-Dobell theorem](/hull-dobell-theorem/) for an LCG, the [multiplicative order](/multiplicative-order/) of $a$ for a multiplicative LCG, and the [primitive polynomial](/primitive-polynomial/) condition for an [LFSR](/linear-feedback-shift-register/) or another linear generator over GF(2).
- **Seed and streams.** The [seed](/seed/) picks the starting point on the cycle. To give many processors disjoint parts of one long cycle, use [jump-ahead](/jump-ahead/).
- **Equidistribution.** [Equidistribution](/equidistribution/) measures how evenly the full cycle covers tuples of outputs. It is defined over one whole period, so it needs the period first.
- **Sample size against period.** A generator should be used for far fewer than $\rho$ outputs. Knuth (Section 3.1) gives the general advice. L'Ecuyer and Simard (2001) found that linear congruential generators fail the birthday spacings test once the sample size is of the order of $\rho^{1/3}$, so a period of $2^{32}$ is too short for current simulations. This is an empirical finding, not a theorem.

## References
