---
tag: 0AJ2E4
kind: algorithm
slug: mersenne-twister
name: Mersenne Twister
aliases:
- MT19937
- MT
area: numerical/random-number-generation
level: core
summary: A GF(2)-linear generator with 624 words of state and period 2^19937 - 1, built on a twisted generalized feedback shift register with a tempering output.
model: word-ram
complexity:
  vars: {t: the number of outputs, n: the number of state words (624)}
  time: {worst: Θ(t + n), average: Θ(t + n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1998
  people: [Makoto Matsumoto, Takuji Nishimura]
  note: Matsumoto and Nishimura published MT19937 in ACM TOMACS in 1998 and replaced its seeding routine in 2002.
prereqs: [linear-feedback-shift-register, primitive-polynomial, generator-period]
see_also: [equidistribution, jump-ahead, xorshift, well-rng, statistical-tests-for-randomness, cryptographically-secure-prng, mersenne-prime, berlekamp-massey]
sources:
  - paper: doi:10.1145/272991.272995
    title: Makoto Matsumoto and Takuji Nishimura, Mersenne Twister, a 623-dimensionally equidistributed uniform pseudo-random number generator, ACM Transactions on Modeling and Computer Simulation 8(1), 1998, pages 3 to 30
    locator: Section 2 (the recurrence, the twist matrix A and the tempering), Section 3 (the period and the primitivity test), Section 4 (k-distribution to v-bit accuracy) and the C code with the parameters of MT19937
  - url: http://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/MT2002/emt19937ar.html
    title: Makoto Matsumoto and Takuji Nishimura, mt19937ar.c, the 2002 version with the initialization init_genrand and init_by_array
    locator: the code and the test output mt19937ar.out (the first outputs for the key 0x123, 0x234, 0x345, 0x456)
  - url: https://eel.is/c++draft/rand.predef
    title: ISO C++ working draft, [rand.predef], predefined random number engines
    locator: the requirement that the 10000th invocation of a default-constructed std::mt19937 produces 4123659995
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007
    locator: Section 6, the tables of results (MT19937 fails the linear complexity tests of Crush and BigCrush)
  - paper: "Francois Panneton, Pierre L'Ecuyer and Makoto Matsumoto, Improved long-period generators based on linear recurrences modulo 2, ACM Transactions on Mathematical Software 32(1), 2006, pages 1 to 16"
    locator: the dimension defects of MT19937 and the slow escape from states with many zero bits
  - paper: "Hiroshi Haramoto, Makoto Matsumoto, Takuji Nishimura, Francois Panneton and Pierre L'Ecuyer, Efficient jump ahead for F2-linear random number generators, INFORMS Journal on Computing 20(3), 2008, pages 385 to 390"
    locator: the jump-ahead method by polynomial arithmetic, with MT19937 as an example
  - paper: "Makoto Matsumoto and Yoshiharu Kurita, Twisted GFSR generators, ACM Transactions on Modeling and Computer Simulation 2(3), 1992"
    locator: the twisted generalized feedback shift register that the Mersenne Twister extends
---

The Mersenne Twister is a [pseudorandom number generator](/pseudorandom-number-generator/) whose state is 624 words of 32 bits, updated by a linear recurrence over GF(2), with a bijective *tempering* map applied to each output word. Its standard version MT19937 has [period](/generator-period/) $2^{19937} - 1$, a [Mersenne prime](/mersenne-prime/), and its outputs are 623-dimensionally [equidistributed](/equidistribution/) to 32-bit accuracy. It is the default generator of Python, R, MATLAB, Ruby and the C++ class `std::mt19937`. It is fast and statistically good for simulation, but it is not a [cryptographic generator](/cryptographically-secure-prng/): 624 outputs reveal the state.

## In plain words

The generator keeps a table of 624 numbers. To refill the table, it walks through it and replaces each number by a mix of three others: its neighbour, the number 397 places further on, and its own top bit. The mix uses only shifts and the exclusive-or of bits, so it is very fast. When asked for a number, it takes the next entry of the table and stirs its bits once more, so that nearby bits are less related, and returns it.

Because the rule is so regular, mathematicians can prove how long the sequence runs before it repeats: a number with about six thousand digits. They can also prove that every combination of values in up to 623 consecutive outputs comes up equally often over the cycle. The price of the regular rule is that anyone who sees 624 outputs can rebuild the table and predict everything after.

## The problem

In the notation of the random-number-generation pages, the generator is $(S, f, g, s_0)$ with $S = \mathrm{GF}(2)^{19937}$ (the 624 words minus 31 bits that never affect the future), a GF(2)-linear transition $f$, and an output $g$ that tempers one word. The goal is a long stream of 32-bit words, or of uniforms $u_i \in [0, 1)$, that behaves like independent uniform draws in simulations, with a proved period and proved high-dimensional equidistribution. The cost model counts word operations per output on a [word RAM](/word-ram/) with $w = 32$.

Matsumoto and Nishimura use their own parameter names, which this page keeps: degree $n = 624$, middle offset $m = 397$ (an index, not a modulus), separation point $r = 31$, twist constant $\mathbf a = $ `0x9908B0DF`, tempering shifts $u = 11$, $s = 7$, $t = 15$, $l = 18$ and tempering masks $\mathbf b = $ `0x9D2C5680`, $\mathbf c = $ `0xEFC60000`. For a word $x$, $x^u$ is its top bit and $x^l$ its low 31 bits. The recurrence is

$$x_{k+n} = x_{k+m} \oplus \left(x_k^u \mid x_{k+1}^l\right) A, \qquad y A = \begin{cases} y \gg 1 & \text{if } y \text{ is even,} \\ (y \gg 1) \oplus \mathbf a & \text{if } y \text{ is odd.} \end{cases}$$

## The algorithm

```pseudo id=main
MT-TWIST()                           ▷ x[0 .. 623] are 32-bit words
L1  for k ← 0 to n − 1 do
L2      y ← (x[k] AND 0x80000000) OR (x[(k + 1) mod n] AND 0x7FFFFFFF)
L3      v ← x[(k + m) mod n] XOR (y >> 1)
L4      if y is odd then
L5          v ← v XOR a
L6      x[k] ← v
L7  i ← 0

MT-NEXT()
L8  if i ≥ n then
L9      MT-TWIST()
L10 y ← x[i], i ← i + 1
L11 y ← y XOR (y >> 11)
L12 y ← y XOR ((y << 7) AND 0x9D2C5680)
L13 y ← y XOR ((y << 15) AND 0xEFC60000)
L14 y ← y XOR (y >> 18)
L15 return y
```

**Seeding.** The 2002 routine `init_genrand(seed)` sets $x[0] = $ seed and $x[i] = (1812433253 \cdot (x[i-1] \oplus (x[i-1] \gg 30)) + i) \bmod 2^{32}$ for $i = 1, \ldots, 623$, then sets $i = n$ so that the first call twists. The routine `init_by_array(key)` mixes a key of any length into the table and sets $x[0] = $ `0x80000000`, which makes the 19937-bit state nonzero. Python seeds with `init_by_array` on the 32-bit pieces of the seed.

**Floating point.** The routine `genrand_res53` uses two outputs: $(a \cdot 2^{26} + b) / 2^{53}$ with $a$ the top 27 bits of the first and $b$ the top 26 bits of the second. This is Python's `random.random()`.

## Example

With `init_genrand(5489)`, the default seed of the C++ class, the first three outputs are 3499211612, 581869302 and 3890346734, and the 10000th output is 4123659995. With `init_by_array` on the key `0x123, 0x234, 0x345, 0x456`, the first five outputs are 1067595299, 955945823, 477289528, 4107218783 and 4228976476, the start of the authors' test file.

**One step of the twist.** After `init_genrand(5489)`, $x[0] = 5489$, $x[1] = 1301868182$ and $x[397] = 3183906156$. In the first iteration of the twist, line L2 takes the top bit of $x[0]$ (it is 0) and the low 31 bits of $x[1]$, so $y = 1301868182$. This $y$ is even, so line L5 does not run, and line L3 gives $x[0] = 3183906156 \oplus 650934091 = 2601187879$. Tempering this word gives the first output 3499211612.

**Tempering one word.** Tempering is a bijection on 32-bit words. Each step XORs a word with a masked shift of itself, and each step can be undone bit by bit, from the unchanged end. So `untemper(3499211612)` gives back the raw state word, and 624 consecutive outputs give back the full table. After that, the copy produces the same outputs as the original forever.

## Correctness

The twist works in place. When iteration $k$ reads $x[(k+1) \bmod n]$ and $x[(k+m) \bmod n]$, an index below $k$ already holds the new value and an index above $k$ still holds the old one, and in each case this is the word the recurrence needs: $x_{K+1}$ and $x_{K+m}$ for $K = jn + k$. The 19937-bit state is linear over GF(2), and its transition is a bijection because the top bit of $\mathbf a$ is 1, so $A$ is injective. Tempering is a bijection, so the outputs determine the states and the output period equals the state period. The full proofs are below.

**Period (proved by an exact computation).** Matsumoto and Nishimura (1998, Section 3) verified that the characteristic polynomial of the 19937-dimensional transition matrix is primitive. Since $2^{19937} - 1$ is prime, primitivity is the same as irreducibility here, which they checked with their inversive-decimation method. By the same argument as for an [LFSR](/linear-feedback-shift-register/), every nonzero state has period exactly $2^{19937} - 1$.

**Equidistribution (proved by an exact computation).** The output is $k$-distributed to $v$-bit accuracy when, over a full period, each pattern of the top $v$ bits of $k$ consecutive outputs appears equally often (the all-zero pattern once less). For $v = 32$ the best possible $k$ is $\lfloor 19937 / 32 \rfloor = 623$, and MT19937 reaches it. The tempering was chosen to raise $k(v)$ for smaller $v$. Panneton, L'Ecuyer and Matsumoto (2006) show that $k(v)$ is below the bound $\lfloor 19937 / v \rfloor$ for many $v$.

## Complexity

- **Time.** A twist does $n = 624$ iterations of $O(1)$ word operations, and each output costs four shifts, four XORs and two ANDs. Over $t$ outputs this is $\Theta(t + n)$ word operations: $\Theta(1)$ amortized per output, with a pause of $\Theta(n)$ at every 624th call.
- **Space.** $n = 624$ words, about 2.5 kilobytes. This matters on GPUs and when each of many streams needs its own state.
- **Jump-ahead.** Jumping $J$ steps ahead multiplies the state by $f^J$; Haramoto and others (2008) do it with polynomial arithmetic modulo the characteristic polynomial, in $O(p^2)$ bit operations for $p = 19937$, after a precomputation for each $J$. See [jump-ahead](/jump-ahead/).

## Properties

- **Proved.** Period $2^{19937} - 1$ from each nonzero state; 623-dimensional equidistribution to 32-bit accuracy.
- **Empirical.** MT19937 passes most tests of the TestU01 batteries but fails the linear complexity tests of Crush and BigCrush, which detect any GF(2)-linear generator (L'Ecuyer and Simard 2007). In typical simulations this defect does not show.
- **Linear.** Each output bit is a GF(2)-linear function of the seed state. Its linear complexity is 19937: the Berlekamp-Massey algorithm recovers the recurrence from about 40000 bits.
- **Slow escape from zero-heavy states.** From a state with very few one-bits, the outputs contain far more zeros than ones for many thousands of steps, because each step mixes only a few bits (Panneton, L'Ecuyer and Matsumoto 2006). Proper seeding avoids such states.
- **Not cryptographic.** See below.

## Variants and improvements

- **MT19937-64.** A 64-bit version with $n = 312$ and the same period; the C++ class `std::mt19937_64` requires the 10000th output 9981545732273789042 for the default seed.
- **SFMT.** The SIMD-oriented Fast Mersenne Twister of Saito and Matsumoto uses 128-bit operations and is faster on processors with SIMD instructions; its outputs differ from MT19937.
- **WELL.** The [WELL generators](/well-rng/) of Panneton, L'Ecuyer and Matsumoto mix the state more per step, escape from zero-heavy states faster and have better equidistribution.
- **TinyMT and small states.** TinyMT has a 127-bit state for parallel use.
- **Smaller and faster alternatives.** [Xorshift](/xorshift/) variants and their scrambled successors give comparable statistical quality with one to four words of state.

## When to use it

Use MT19937 when you must reproduce results that were computed with it, for example with Python's `random` or R's default. For new simulation code, a generator with a smaller state, cheap jump-ahead and no linear-complexity failures is a better default. Never use it for keys, tokens, nonces or any other secret.

## Pitfalls

- **Prediction from outputs.** After 624 consecutive 32-bit outputs, an attacker inverts the tempering and knows the state, so tokens or passwords made with it can be predicted.
- **Seeding with small integers.** Seeds such as 0, 1, 2 give unrelated-looking but fixed streams. Many processes seeded with consecutive integers are not proved to be independent; give each stream its own region by [jump-ahead](/jump-ahead/) or use a generator designed for streams.
- **The 1998 seeding routine.** The first published seeding used a linear congruential generator to fill the table; the 2002 routines `init_genrand` and `init_by_array` replaced it. Reference values depend on which one you use.
- **Different floating-point conversions.** `genrand_real2` returns $a / 2^{32}$ from one output, with only 32 bits of resolution; `genrand_res53` uses two outputs. Two programs with the same seed can give different floating-point streams.
- **Masking in languages without 32-bit types.** In Python or JavaScript, mask each word to 32 bits after a left shift and after the multiplication in the seeding, or the values diverge from the reference.

## Implementations

## History

Matsumoto and Kurita introduced the twisted GFSR in 1992 and improved it in 1994: a word-wide shift register with a twist matrix that reaches the maximal period of its state. Matsumoto and Nishimura (1998) replaced the full words of the recurrence by an incomplete array, chose the degree 19937 so that $2^{19937} - 1$ is a Mersenne prime and primitivity is easy to check, and added the tempering. In 2002 they published new seeding routines. MT19937 became the default generator of many languages and libraries in the 2000s.

## References
