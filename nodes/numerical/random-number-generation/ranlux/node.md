---
tag: WG0HW1
kind: algorithm
slug: ranlux
name: RANLUX
aliases:
- ranlux24
- ranlux48
- Lüscher generator
- luxury random numbers
- subtract-with-borrow with decimation
area: numerical/random-number-generation
level: advanced
summary: A lagged Fibonacci generator with provable decorrelation for high-energy physics simulation.
model: word-ram
complexity:
  vars: {r: "the long lag, 24", p: "the block length, the luxury level", q: "the values kept per block"}
  time: {worst: Θ(p - q), amortized: Θ(p/q)}
  space: {extra: Θ(r)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [lagged-fibonacci-generator, linear-congruential-generator, multiplicative-order]
see_also: [multiply-with-carry, marsaglia-hyperplane-theorem, spectral-test, statistical-tests-for-randomness, mersenne-twister, mrg32k3a, equidistribution, jump-ahead]
sources:
  - paper: doi:10.1016/0010-4655(94)90232-1
    title: Martin Lüscher, A portable high-quality random number generator for lattice field theory simulations, Computer Physics Communications 79(1), 1994, pages 100 to 110
    locator: the subtract-with-borrow generator with b = 2^24, r = 24, s = 10, its interpretation as a chaotic dynamical system, the decimation that keeps 24 of every p values, and the period (m - 1)/48 with m = 2^576 - 2^240 + 1
  - paper: doi:10.1016/0010-4655(94)90233-X
    title: Frederick James, RANLUX, a Fortran implementation of the high-quality pseudorandom number generator of Lüscher, Computer Physics Communications 79(1), 1994, pages 111 to 114
    locator: the luxury levels 0 to 4 with p = 24, 48, 97, 223 and 389, and the portable code
  - paper: doi:10.1214/aoap/1177005878
    title: George Marsaglia and Arif Zaman, A new class of random number generators, Annals of Applied Probability 1(3), 1991, pages 462 to 480
    locator: the add-with-carry and subtract-with-borrow generators, the modulus b^r - b^s + 1 and the period as the order of b
  - url: https://eel.is/c++draft/rand.predef
    title: Working Draft, Programming Languages C++, the predefined engines
    locator: "the definitions of ranlux24_base, ranlux48_base, ranlux24 and ranlux48, and their required 10000th outputs 7937952, 61839128582725, 9901578 and 249142670248501"
---

RANLUX is Martin Lüscher's 1994 generator for lattice field theory and other simulations in physics. Its core is Marsaglia and Zaman's subtract-with-borrow (SWB) generator, $x_n = (x_{n-10} - x_{n-24} - c_{n-1}) \bmod 2^{24}$, a [lagged Fibonacci generator](/lagged-fibonacci-generator/) with a borrow bit. Alone, the SWB fails statistical tests because every value is tied to two earlier ones. Lüscher showed that the SWB is a discrete version of a chaotic dynamical system, so that correlations decay as the generator runs, and made the output good by *decimation*: produce $p$ values, use the first 24, and throw the rest away. The block length $p$, the *luxury level*, trades speed for quality. RANLUX is in the C++ standard library as `std::ranlux24` and `std::ranlux48`.

## In plain words

The basic generator keeps the last 24 numbers. To make a new one, it subtracts the number from 24 steps ago from the number from 10 steps ago, and subtracts a borrow of 0 or 1 left from the last step. If the result is negative, it wraps around and sets the borrow for the next step. This is fast and has an enormous cycle, but each new number is almost exactly the difference of two older ones, and tests detect that.

RANLUX fixes this by running the basic generator much longer than needed. Out of every block of a few hundred numbers it hands out only the first two dozen and discards the rest. By the time the next block starts, the link to the numbers handed out before has been washed out. A larger block costs more time and gives a larger safety margin.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page with the base $b = 2^w$. The task, as Lüscher posed it for Monte Carlo simulations of quantum field theory, is a portable generator with a period far beyond any run, and with an argument, not only test results, that the outputs carry no correlations of the kind that bias long simulations. The state space $S$ is the last $r$ values and one borrow bit, the transition $f$ is $p$ steps of the SWB generator per block, and the output function $g$ reads the first $q$ values of each block.

## The algorithm

The SWB step with base $b$ and lags $s < r$ is

$$x_n = x_{n-s} - x_{n-r} - c_{n-1}, \quad c_n = 0 \quad \text{if this is} \ge 0, \qquad x_n = x_{n-s} - x_{n-r} - c_{n-1} + b, \quad c_n = 1 \quad \text{otherwise}.$$

Lüscher's parameters are $b = 2^{24}$, $r = 24$, $s = 10$. The decimated generator returns $q$ consecutive SWB values and then skips $p - q$. A counter $k$ counts the values used in the current block.

```pseudo id=main
RANLUX-NEXT()                 ▷ state: x_(n-r..n-1), borrow c, counter k
L1  if k = q then             ▷ the q values of this block are used
L2      repeat p − q times: SWB-STEP()   ▷ discard
L3      k ← 0
L4  k ← k + 1
L5  return SWB-STEP()

SWB-STEP()
L6  d ← x_(n−s) − x_(n−r) − c
L7  if d < 0 then (x_n, c) ← (d + b, 1) else (x_n, c) ← (d, 0)
L8  return x_n
```

The $r$ values live in a circular buffer, so each SWB step is a subtraction, a comparison and an index update. Lüscher keeps $q = 24$ values per block; James's luxury levels 0 to 4 use $p = 24$ (no decimation), 48, 97, 223 and 389. The C++ library fixes `std::ranlux24` as blocks of 223 with $q = 23$, and `std::ranlux48` as the SWB with $b = 2^{48}$, $r = 12$, $s = 5$ and blocks of 389 with $q = 11$.

## Example

A toy SWB in base $b = 10$ with $r = 3$ and $s = 1$, so $x_n = x_{n-1} - x_{n-3} - c_{n-1}$ with wrap-around, from $(x_{-3}, x_{-2}, x_{-1}) = (3, 1, 4)$ and $c_{-1} = 0$:

| $n$ | $x_{n-1} - x_{n-3} - c_{n-1}$ | $x_n$ | $c_n$ | $K_{n+1}$ |
|---|---|---|---|---|
| 0 | $4 - 3 - 0 = 1$ | 1 | 0 | $-140$ |
| 1 | $1 - 1 - 0 = 0$ | 0 | 0 | $-14$ |
| 2 | $0 - 4 - 0 = -4$ | 6 | 1 | $-596$ |
| 3 | $6 - 1 - 1 = 4$ | 4 | 0 | $-456$ |
| 4 | $4 - 0 - 0 = 4$ | 4 | 0 | $-442$ |

The last column is the integer $K$ of the proof: the stored values read as a base-10 number, with a correction for the borrow. It starts at $K_0 = 4 - 413 = -409$ and satisfies $10 K_{n+1} = K_n - 991 x_n$, where $991 = 10^3 - 10 + 1$ is prime. So $K_{n+1} \equiv 10^{-1} K_n \pmod{991}$: the SWB is a multiplicative [linear congruential generator](/linear-congruential-generator/) in disguise, and its period from this seed is the order of 10 modulo 991, which is 495.

At full size, a default-constructed `std::ranlux24_base` starts $15039276, 16323925, 14283486, 7150092, 68089$, and the 10000th outputs of the four standard engines are the values required by the C++ standard; this page's tests reproduce all of them.

## Correctness

Correctness here means the period and the source of the SWB's weakness, proved in full in the proof file.

1. **Three-term relation.** From the step, $x_n - x_{n-s} + x_{n-r} = b c_n - c_{n-1} \in \{-1, 0, b - 1, b\}$. So the triples $(x_{n-r}, x_{n-s}, x_n)/b$ lie on four parallel planes, a far worse lattice than the [Marsaglia hyperplane theorem](/marsaglia-hyperplane-theorem/) bound for a good generator. This is what decimation must hide.
2. **LCG equivalence.** With $m = b^r - b^s + 1$ and $K_n$ as in the example, $b K_{n+1} = K_n - m x_n$ and $x_n = K_n \bmod b$. On every cycle $-m \le K_n \le 0$, and the cycle length is the order of $b$ modulo $m / \gcd(K_n, m)$. If $m$ is prime, every cycle other than the constant outputs 0 and $b - 1$ has length $\operatorname{ord}_m(b)$.
3. **The RANLUX numbers.** For $b = 2^{24}$, $r = 24$, $s = 10$, and also for $b = 2^{48}$, $r = 12$, $s = 5$, $m = 2^{576} - 2^{240} + 1$. The tests prove $m$ prime with Pocklington's criterion, and show that the period of ranlux24_base divides $(m - 1)/48$ and is a multiple of a computed number above $2^{333}$. Lüscher states that it equals $(m - 1)/48 \approx 5 \cdot 10^{171}$.

The claim that decimation removes all correlations is not a theorem in this sense; see Properties.

## Complexity

Each SWB step costs $\Theta(1)$ word operations. RANLUX makes $p$ steps per $q$ outputs, so the amortized cost is $\Theta(p / q)$ per output, about 16 SWB steps per output at $p = 389$, $q = 24$; a single call that starts a new block costs $\Theta(p - q)$. The state is $r + 2$ words. Jumping ahead is possible through the LCG form, as a multiplication of a 576-bit number by a power of $b^{-1}$ modulo $m$.

## Properties

- **Proved:** the LCG equivalence, the period of the SWB as $\operatorname{ord}_m(b)$, and the bad three-term lattice of the raw SWB.
- **Lüscher's argument.** Lüscher viewed the SWB as an approximation of a chaotic dynamical system and measured how fast two nearby states separate. From this he argued that once the number of discarded steps reaches a few hundred, about $p = 389$ for 24 kept values, every correlation is far below detection. This is a strong heuristic backed by computation, not a proof that the outputs are random.
- **Empirical:** the raw SWB fails standard statistical tests, as the three-term relation predicts; with $p = 223$ or 389, RANLUX passes the batteries it has been tested on, and it has been used for decades in physics codes.
- **Slow.** The high luxury levels make it one of the slowest non-cryptographic generators in common use.
- **Not secure.** The state follows from 24 consecutive outputs of a block.

## Variants and improvements

- **Luxury levels.** $p = 24$ (level 0, plain SWB) up to $p = 389$ (level 4), as in James's Fortran RANLUX. Low levels are fast but fail tests.
- **ranlxs and ranlxd.** Lüscher's later C versions give single and double precision outputs from the same SWB, with their own sets of luxury levels.
- **`std::ranlux24` and `std::ranlux48`.** The C++ engines use `subtract_with_carry_engine` and `discard_block_engine`; note that `ranlux24` keeps 23 of 223, not 24.
- **RANLUX++.** Sibidanov (2017) used the LCG equivalence to compute RANLUX blocks with a 576-bit modular multiplication by $b^{-p}$, which is much faster at high luxury levels.
- **Other carry generators.** [Multiply-with-carry](/multiply-with-carry/) replaces the subtraction with a multiplication and has the same kind of LCG equivalence.

## When to use it

Use RANLUX when the field expects it, in high-energy physics and lattice simulations, or when you want a generator whose decorrelation has a published theoretical argument, and can pay a large factor in speed. For general simulation, [Mersenne Twister](/mersenne-twister/), [MRG32k3a](/mrg32k3a/) or [xoshiro](/xoshiro-xoroshiro/) are much faster with good test results. Never use the plain SWB, `ranlux24_base` or `ranlux48_base`, as a final generator; they exist as building blocks. Never use any of them where outputs must be unpredictable.

## Pitfalls

- **Using the base engine.** `std::ranlux24_base` is the raw SWB, which fails statistical tests; use `std::ranlux24`.
- **Too low a luxury level.** Levels 0 and 1 keep enough of the SWB lattice to fail tests; choose $p \ge 223$.
- **Bad seeds.** The all-zero state with borrow 0 and the all-$(b - 1)$ state with borrow 1 are fixed points. Standard seeding routines avoid them; hand-written seeding must too.
- **Wrong lag direction.** The recurrence uses $x_{n-s} - x_{n-r}$, the short lag minus the long lag. Reversing the sign gives a different generator with a different modulus.
- **Mixing kept and discarded values.** Code that reads the buffer directly, instead of through the decimating wrapper, sees discarded values, which are correlated with the kept ones.

## Implementations

## History

Marsaglia and Zaman introduced add-with-carry and subtract-with-borrow generators in 1991 as fast generators with huge periods. Soon after, physicists found that they gave wrong results in Monte Carlo simulations of the Ising model, and Tezuka, L'Ecuyer and Couture explained their poor lattice structure. Lüscher (1994) recast the SWB as a chaotic dynamical system, proposed decimation, and gave a theoretical reason for the choice of $p$. Fred James published the Fortran RANLUX with luxury levels the same year at CERN. The generator entered the CERN libraries, Geant4 and ROOT, and later the C++11 standard.

## References
