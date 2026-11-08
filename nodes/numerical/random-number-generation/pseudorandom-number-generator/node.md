---
tag: A03S2V
kind: abstract-type
slug: pseudorandom-number-generator
name: Pseudorandom number generator
aliases:
- PRNG
- PRG
- random number generator
- RNG
area: numerical/random-number-generation
level: intro
summary: A deterministic state machine whose output sequence is statistically random-looking.
prereqs: [random-variable, uniform-distribution, generator-period]
see_also: [seed, true-random-number-generator, cryptographically-secure-prng, statistical-tests-for-randomness, linear-congruential-generator, xoshiro-xoroshiro, pcg-random, pseudorandom-generator]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Chapter 3 (Section 3.1, Introduction, on eventually periodic sequences; Section 3.5, What is a random sequence?)
  - paper: "Pierre L'Ecuyer, Uniform random number generation, Annals of Operations Research 53, 1994, pages 77 to 120"
    locator: Section 2 (the generator as a structure with a finite state space S, a transition function f, an output space and an output function g)
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), article 22, 2007
    locator: Section 2 (the generator model, and why a generator that fails a test is rejected while passing tests proves nothing)
  - paper: "Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984, pages 850 to 864"
    locator: the definition of a cryptographically strong generator by unpredictability of the next bit
  - paper: "Johan Håstad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), 1999, pages 1364 to 1396"
    locator: the main theorem (a pseudorandom generator exists if and only if a one-way function exists)
---

A pseudorandom number generator (PRNG) is a deterministic state machine whose outputs imitate a sequence of independent [uniform](/uniform-distribution/) random numbers. A [seed](/seed/) fixes the start state, so the same seed always gives the same sequence. Because the state space is finite, the sequence is periodic in the end, with a [period](/generator-period/) at most the number of states. This page fixes the notation that all pages on random number generation use.

## In plain words

A computer cannot flip a coin. It can only follow rules. A pseudorandom number generator keeps a small amount of memory, called its state. Each time you ask for a number, it changes the state by a fixed rule and computes a number from the new state.

The numbers look random to a test that does not know the rule. But they are not random: if you start again from the same state, you get the same numbers. This is useful, because a simulation can then be repeated exactly.

The memory is finite, so in the end the generator comes back to a state it had before, and from then on it repeats itself. A good generator repeats only after so many numbers that no program ever reaches that point.

## Operations

The notation is the one of L'Ecuyer (1994), and the other pages of this sub-area use it without change.

| symbol | meaning |
|---|---|
| $S$ | the state space, a finite set |
| $f : S \to S$ | the transition function, $s_{i+1} = f(s_i)$ |
| $g : S \to U$ | the output function, $u_i = g(s_i)$ |
| $s_0$ | the start state, computed from the seed |
| $w$ | the word size in bits (usually 32 or 64) |
| $m, a, c$ | the modulus, the multiplier and the increment of a congruential generator |
| $\rho$ | the period of the state sequence |
| $U(0, 1)$ | the uniform distribution on the interval from 0 to 1 |

The output space $U$ is a set of words $\{0, 1, \ldots, 2^w - 1\}$ or a finite set of numbers in $[0, 1)$ or $(0, 1)$. A real output $u_i$ is meant to imitate a draw from $U(0, 1)$. For sampling methods built on a generator, the pages write $p$ for a target density, $F$ for a target distribution function, $q$ for a proposal density, and they give the acceptance rate. The cost unit is one word operation; the cost of a sampling method counts the uniforms that it uses and its expected number of rejections.

The type has these operations.

| operation | signature | what it does |
|---|---|---|
| `seed(σ)` | seed value $\to S$ | computes the start state $s_0$ |
| `next(s)` | $S \to U \times S$ | returns $u = g(f(s))$ and the new state $f(s)$ |
| `jump(s, k)` | $S \times \mathbb{N} \to S$ | returns $f^k(s)$ without $k$ calls of `next` (optional) |
| `split(s)` | $S \to S \times S$ | returns two states whose sequences are meant to be independent (optional) |

Some libraries apply $g$ before $f$, that is, they return $g(s)$ and then advance. The two conventions differ only by one step of the sequence. Each generator page states which one it uses, because published reference outputs depend on it.

## Laws

Each implementation meets these laws.

1. **Determinism.** `next` is a function of the state alone: if $s = s'$ then `next`$(s)$ = `next`$(s')$. So the seed determines the full output sequence $u_1, u_2, \ldots$.
2. **The step law.** `next`$(s) = (g(f(s)), f(s))$.
3. **The jump law.** `jump`$(s, 0) = s$ and `jump`$($`jump`$(s, j), k) =$ `jump`$(s, j + k) = f^{j+k}(s)$.
4. **Eventual periodicity.** For each $s_0$ there are integers $\mu \ge 0$ and $\rho \ge 1$ with $s_{i + \rho} = s_i$ for all $i \ge \mu$, and $\mu + \rho \le |S|$.
5. **Pure periodicity for a bijection.** If $f$ is a bijection of $S$, then $\mu = 0$: the start state is on the cycle.

*Proof of law 4.* The states $s_0, s_1, \ldots, s_{|S|}$ are $|S| + 1$ elements of a set of size $|S|$, so by the [pigeonhole principle](/pigeonhole-principle/) two of them are equal, say $s_\mu = s_{\mu + \rho}$ with $\mu + \rho \le |S|$ and $\rho \ge 1$. By determinism $s_{i+1} = f(s_i)$, so induction on $i$ gives $s_{i + \rho} = s_i$ for all $i \ge \mu$. $\square$

*Proof of law 5.* Take $\mu$ minimal. If $\mu > 0$, then $f(s_{\mu - 1}) = s_\mu = s_{\mu + \rho} = f(s_{\mu + \rho - 1})$, and $f$ is injective, so $s_{\mu - 1} = s_{\mu - 1 + \rho}$. This contradicts the minimality of $\mu$. $\square$

The outputs repeat with the states, so the output sequence has a period that divides $\rho$. The laws say nothing about quality. Quality is a property of a particular $f$ and $g$, and it is of two kinds:

- **Proved properties.** The period, the structure of the points $(u_i, \ldots, u_{i+t-1})$ (a lattice for congruential generators, a vector space over GF(2) for linear generators over GF(2)), and [equidistribution](/equidistribution/) are theorems about $f$ and $g$.
- **Empirical properties.** Passing the batteries of [statistical tests](/statistical-tests-for-randomness/), such as TestU01 BigCrush or PractRand, is evidence and not proof. A failure rejects a generator; a pass only shows that those tests did not find a defect.

### A small example

The [linear congruential generator](/linear-congruential-generator/) with $S = \{0, \ldots, 15\}$, $f(s) = (5s + 3) \bmod 16$ and $g(s) = s$, from $s_0 = 7$, gives

$$7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4, 7, \ldots$$

Here $f$ is a bijection, $\mu = 0$ and $\rho = 16 = |S|$. The lowest bit alternates $1, 0, 1, 0, \ldots$, so a full period does not mean good quality. The map $f(s) = (s^2 + 1) \bmod 16$ is not a bijection: from $s_0 = 3$ it gives $3, 10, 5, 10, 5, \ldots$, with $\mu = 1$ and $\rho = 2$.

### Statistical and cryptographic generators

The type covers two different goals.

- A **statistical PRNG** (for simulation and [Monte Carlo integration](/monte-carlo-integration/)) must be fast, have a long period, and have no defect that a simulation could detect. Linear generators such as the [Mersenne Twister](/mersenne-twister/) and [xorshift](/xorshift/) are of this kind. Their state can be computed from a few outputs by solving a linear system, so they are not secure.
- A **cryptographic PRG**, in the sense of Blum and Micali (1984) and Yao (1982), is a function $G : \{0,1\}^k \to \{0,1\}^{\ell(k)}$ with $\ell(k) > k$ such that no probabilistic polynomial-time algorithm distinguishes $G(x)$, for a uniform $x$, from a uniform string of length $\ell(k)$ with non-negligible advantage. See [computational indistinguishability](/computational-indistinguishability/) and [cryptographically secure PRNG](/cryptographically-secure-prng/). No generator is proved secure without an assumption: Håstad, Impagliazzo, Levin and Luby (1999) proved that such a $G$ exists if and only if a [one-way function](/one-way-function/) exists, and the existence of one-way functions implies $P \ne NP$, which is open.

## Implementations

| generator | state size | period $\rho$ | cost per output | status |
|---|---|---|---|---|
| [Park-Miller minimal standard](/park-miller-minimal-standard/) | 31 bits | $2^{31} - 2$ | 1 multiplication mod $2^{31} - 1$ | weak, short period |
| [RANDU](/randu/) | 31 bits | $2^{29}$ | 1 multiplication mod $2^{31}$ | broken: 15 planes in 3 dimensions |
| [MRG32k3a](/mrg32k3a/) | 192 bits | about $2^{191}$ | 4 products mod a 32-bit prime | good, used for parallel streams |
| [multiply-with-carry](/multiply-with-carry/) | $w$ to $4096w$ bits | the order of $b$ modulo $ab^r - 1$ | 1 multiplication | good with care |
| [Mersenne Twister](/mersenne-twister/) MT19937 | 19937 bits | $2^{19937} - 1$ | a few shifts and XORs | fails linearity tests |
| [WELL512a](/well-rng/) | 512 bits | $2^{512} - 1$ | a few shifts and XORs | fails linearity tests |
| [xorshift](/xorshift/) | 32 to 128 bits | $2^w - 1$ or $2^{128} - 1$ | 3 shifts and 3 XORs | fails linearity tests |
| [xoshiro256**](/xoshiro-xoroshiro/) | 256 bits | $2^{256} - 1$ | about 11 operations | passes BigCrush |
| [PCG32](/pcg-random/) | 64 bits plus an increment | $2^{64}$ | 1 multiplication and a permutation | passes BigCrush |
| [SplitMix64](/splitmix64/) | 64 bits | $2^{64}$ | 2 multiplications | passes BigCrush |
| [Philox4x32-10](/philox/) | 128-bit counter, 64-bit key | $2^{128}$ per key | 20 multiplications per 4 outputs | passes BigCrush, not a cipher |
| [Threefry4x64-20](/threefry/) | 256-bit counter, 256-bit key | $2^{256}$ per key | 20 rounds of 2 add-rotate-XOR steps per 4 outputs | passes BigCrush, not proved secure |
| [ChaCha20](/chacha20/) | 512-bit block | $2^{32}$ blocks per key and nonce (RFC 8439) | 20 rounds per 64 bytes | cryptographic (no known attack) |
| [Blum Blum Shub](/blum-blum-shub/) | the size of the modulus | depends on the modulus | 1 modular squaring per bit or few bits | secure if factoring is hard |

The "status" column for linear and statistical generators reports empirical test results from the sources of each page, and is not a theorem.

## Lower bounds

- **Period.** A generator with $k$ bits of state has $\rho \le 2^k$, by law 4. A generator whose $f$ is linear over GF(2) has $\rho \le 2^k - 1$, because the zero state is fixed.
- **No statistical perfection.** Let the state have $k$ bits and let $G(s_0)$ be the first $n$ output bits. The outputs take at most $2^k$ values, so the set $A$ of possible outputs has at least $2^n - 2^k$ strings outside it. A uniform string falls outside $A$ with probability at least $1 - 2^{k - n}$, and $G(s_0)$ never does. So the statistical distance between $G(s_0)$ and the uniform distribution is at least $1 - 2^{k-n}$. For $n > k$ a generator can only be *computationally* close to uniform, never statistically.
- **No repeated values in a bijective output.** If $g$ is a bijection from $S$ to the $w$-bit words and $|S| = 2^w$, then no output repeats within a period. Among $n$ truly uniform $w$-bit words a repeat appears with probability near $1 - e^{-n^2 / 2^{w+1}}$ (the [birthday paradox](/birthday-paradox/)). So a test that looks for repeats detects such a generator after about $2^{w/2}$ outputs. This is why a 32-bit generator with 32 bits of state cannot be good.

## References
