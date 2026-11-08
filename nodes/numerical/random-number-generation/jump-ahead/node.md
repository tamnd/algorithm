---
tag: CRH15P
kind: algorithm
slug: jump-ahead
name: Jump-ahead function
aliases:
- skip-ahead
- leapfrog
- jump polynomial
area: numerical/random-number-generation
level: advanced
summary: Computes the state n steps ahead of a linear generator in time logarithmic in n, by powering an affine map or by reducing x^n modulo the characteristic polynomial.
model: word-ram
complexity:
  vars: {n: the jump distance, k: the degree of the characteristic polynomial, w: the word size}
  time: {worst: O(k^2 log(n) / w + k^2 / w)}
  space: {extra: Θ(k / w)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1991
  people: [Pierre L'Ecuyer, Serge Côté]
  note: L'Ecuyer and Côté built a generator package with many disjoint streams and substreams reached by jumping ahead in a combined LCG.
prereqs: [linear-congruential-generator, binary-exponentiation, gf2-polynomial-arithmetic, cayley-hamilton-theorem]
see_also: [berlekamp-massey, matrix-exponentiation, mrg32k3a, xoshiro-xoroshiro, mersenne-twister, pcg-random, philox, linear-feedback-shift-register]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1, the closed formula for X_(n+k) in terms of X_n, a^k and c
  - paper: "Pierre L'Ecuyer and Serge Côté, Implementing a random number package with splitting facilities, ACM Transactions on Mathematical Software 17(1), 1991, pages 98 to 111"
    locator: the computation of a^(2^e) mod m for jumping ahead to the start of streams and substreams
  - paper: "Pierre L'Ecuyer, Richard Simard, E. Jack Chen and W. David Kelton, An object-oriented random-number package with many long streams and substreams, Operations Research 50(6), 2002, pages 1073 to 1075"
    locator: the jump-ahead matrices of MRG32k3a for streams of length 2^127 and substreams of length 2^76
  - paper: "Hiroshi Haramoto, Makoto Matsumoto, Takuji Nishimura, François Panneton and Pierre L'Ecuyer, Efficient jump ahead for F2-linear random number generators, INFORMS Journal on Computing 20(3), 2008, pages 385 to 390"
    locator: the method that computes x^n mod the characteristic polynomial and evaluates it at the transition by Horner's rule
  - url: https://prng.di.unimi.it/
    title: David Blackman and Sebastiano Vigna, xoshiro / xoroshiro generators and the PRNG shootout
    locator: the jump() and long_jump() functions of xoshiro256 with their published constants
---

A jump-ahead function moves a [pseudorandom number generator](/pseudorandom-number-generator/) from state $s_i$ to state $s_{i+n}$ without producing the $n$ outputs in between. For a linear generator this takes $O(\log n)$ steps of arithmetic instead of $n$: an affine map $s \mapsto (a s + c) \bmod m$ is raised to the $n$-th power by repeated squaring, and an $\mathbb{F}_2$-linear map with characteristic polynomial $\varphi$ is replaced by the polynomial $x^n \bmod \varphi(x)$. Jumping ahead by a fixed large distance, such as $2^{128}$, splits one long period into many disjoint streams for parallel simulations. The same coefficients give the *leapfrog* subsequence $s_j, s_{j+p}, s_{j+2p}, \ldots$.

## In plain words

A generator walks along a very long loop of states, one step per number. Sometimes you need the state a trillion steps later, for example to give each of a thousand processors its own stretch of the loop. Walking there would take far too long.

For generators built from multiplying, adding and exclusive-or, one step is a simple rule, and two steps are again a rule of the same shape. So the rule for two steps, four steps, eight steps and so on can be computed by combining a rule with itself. Any distance is a sum of such powers of two, so a few dozen combinations reach any point of the loop.

## The problem

A generator is a tuple $(S, f, g, s_0)$ with state space $S$, transition $f$, $s_{i+1} = f(s_i)$, output $u_i = g(s_i)$ and seed $s_0$. Given a state $s$ and an integer $n \ge 0$, compute $f^n(s)$, the state $n$ steps later. Two linear cases cover most generators in use:

- **Affine modulo $m$.** $S = \{0, \ldots, m - 1\}$ and $f(s) = (a s + c) \bmod m$, as in the [linear congruential generator](/linear-congruential-generator/). The same method works for vectors and matrices, which covers [multiple recursive generators](/multiple-recursive-generator/) such as [MRG32k3a](/mrg32k3a/).
- **Linear over $\mathbb{F}_2$.** $S = \mathbb{F}_2^k$ and $f(s) = A s$ for a $k \times k$ binary matrix $A$, as in the [LFSR](/linear-feedback-shift-register/), [xorshift](/xorshift/), [xoshiro](/xoshiro-xoroshiro/) and the [Mersenne Twister](/mersenne-twister/). The state is packed into $\lceil k / w \rceil$ words, and $f$ is computed by the generator's own code, not by a matrix.

The cost model counts word operations on a [word RAM](/word-ram/) with word size $w$.

## The algorithm

```pseudo id=main
LCG-JUMP(s, n)                       ▷ f(s) = (a s + c) mod m; returns f^n(s)
L1  (A, C) ← (1, 0)                  ▷ the map s ↦ A s + C, now the identity
L2  (B, D) ← (a, c)                  ▷ the map f^(2^i), now f
L3  while n > 0
L4      if n is odd then (A, C) ← (B·A mod m, (B·C + D) mod m)
L5      (B, D) ← (B·B mod m, (B·D + D) mod m)
L6      n ← ⌊n / 2⌋
L7  return (A·s + C) mod m

F2-JUMP(s, n, φ)                     ▷ f linear over F2, φ(A) = 0, deg φ = k
L8  r ← x^n mod φ(x)                 ▷ square and multiply in F2[x]
L9  t ← 0                            ▷ the zero state
L10 for j ← deg r downto 0           ▷ Horner's rule for r(A) s
L11     t ← f(t)
L12     if r_j = 1 then t ← t ⊕ s
L13 return t
```

**Affine case.** The pair $(A, C)$ stands for the map $s \mapsto (A s + C) \bmod m$. Composing $(B, D)$ after $(A, C)$ gives $(B A, B C + D)$, and composing $(B, D)$ with itself gives $(B^2, B D + D)$. Lines L3 to L6 are [binary exponentiation](/binary-exponentiation/) in this monoid of affine maps. Because all the maps are powers of $f$, they commute, so the order of composition does not matter. The result $(A, C) = (a^n \bmod m, \, c(1 + a + \cdots + a^{n-1}) \bmod m)$ also gives the leapfrog generator: the subsequence $s_j, s_{j+p}, \ldots$ is the LCG with multiplier $a^p$ and increment $c(1 + \cdots + a^{p-1})$.

**$\mathbb{F}_2$-linear case.** If $\varphi(A) = 0$, for example when $\varphi$ is the characteristic polynomial of $A$ ([Cayley-Hamilton](/cayley-hamilton-theorem/)), then $x^n = q(x) \varphi(x) + r(x)$ gives $A^n = r(A)$, a polynomial of degree less than $k$. Line L8 computes $r$ with $O(\log n)$ multiplications modulo $\varphi$ ([GF(2) polynomial arithmetic](/gf2-polynomial-arithmetic/)). Lines L9 to L12 evaluate $r(A) s = \sum_j r_j A^j s$ by Horner's rule, using only calls to $f$ and exclusive-or. When $\varphi$ is not published, it is found by running [Berlekamp-Massey](/berlekamp-massey/) on $2k$ output bits. For a fixed distance such as $2^{128}$, $r$ is computed once and stored as a constant: the jump() function of xoshiro256 is this loop with $r$ in four 64-bit words.

## Example

**Affine.** Take $m = 16$, $a = 5$, $c = 3$, seed $s = 7$ and $n = 11 = 1011_2$.

| $n$ at L3 | bit | $(A, C)$ before | $(B, D)$ before |
|---|---|---|---|
| 11 | 1 | $(1, 0)$ | $(5, 3)$ |
| 5 | 1 | $(5, 3)$ | $(9, 2)$ |
| 2 | 0 | $(13, 13)$ | $(1, 4)$ |
| 1 | 1 | $(13, 13)$ | $(1, 8)$ |

The final map is $(13, 5)$, so $f^{11}(7) = (13 \cdot 7 + 5) \bmod 16 = 96 \bmod 16 = 0$. Stepping directly gives $7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0$, and the twelfth value, $s_{11}$, is 0. The row $(9, 2)$ is $f^2(s) = 25 s + 18 \equiv 9 s + 2$.

**$\mathbb{F}_2$-linear.** Take the 4-bit Galois LFSR $t \mapsto x t \bmod \varphi$ with $\varphi = x^4 + x^3 + 1$, and jump $n = 10$ from $s = 0110_2$. Line L8 gives $r = x^{10} \bmod \varphi = x^3 + x$, bits $1010_2$. The Horner loop runs:

| $j$ | $r_j$ | $t$ after L11 and L12 |
|---|---|---|
| 3 | 1 | $0 \oplus 0110 = 0110$ |
| 2 | 0 | $f(0110) = 1100$ |
| 1 | 1 | $f(1100) \oplus 0110 = 0001 \oplus 0110 = 0111$ |
| 0 | 0 | $f(0111) = 1110$ |

So $f^{10}(0110) = 1110_2 = 14$, which agrees with ten single steps.

**Published constants.** For the linear engine of xoshiro256, Berlekamp-Massey on 512 output bits gives a characteristic polynomial of degree 256, and $x^{2^{128}} \bmod \varphi$ and $x^{2^{192}} \bmod \varphi$ equal, bit for bit, the JUMP and LONG_JUMP constants published by Blackman and Vigna (`0x180ec6d33cfd0aba`, ... and `0x76e15d3efefdcbbf`, ...). Reference check values for the affine case: a jump of 10000 from seed 1 in the minimal standard generator ($a = 16807$, $m = 2^{31} - 1$) gives 1043618065, the value of Park and Miller.

## Correctness

The proof page gives the details. For LCG-JUMP the loop keeps the invariant that, with $n_0$ the original distance and $i$ the number of completed iterations, $(A, C)$ represents $f^{n_0 \bmod 2^i}$, $(B, D)$ represents $f^{2^i}$ and $n = \lfloor n_0 / 2^i \rfloor$; at exit $n = 0$ so $(A, C)$ represents $f^{n_0}$. For F2-JUMP, $\varphi(A) = 0$ gives $A^n = r(A)$, and the Horner loop keeps $t = \sum_{i \ge j} r_i A^{i-j} s$ after the iteration with index $j$, which at $j = 0$ is $r(A) s = A^n s$. If $\varphi$ comes from Berlekamp-Massey, it equals the characteristic polynomial when that polynomial is irreducible and the observed bit sequence is not identically zero, because the minimal polynomial of the sequence divides it and is not 1.

## Complexity

For the affine case, L3 to L6 run $\lfloor \log_2 n \rfloor + 1$ times with a constant number of multiplications modulo $m$ each, so the time is $\Theta(\log n)$ word operations when $m \le 2^w$. A $k \times k$ matrix version for multiple recursive generators costs $O(k^3 \log n)$.

For the $\mathbb{F}_2$ case, each multiplication modulo $\varphi$ costs $O(k^2 / w)$ word operations with shift-and-add, so L8 costs $O(k^2 \log(n) / w)$; with a precomputed $r$ this part disappears. The Horner loop calls $f$ $k$ times and does at most $k$ exclusive-ors of $\lceil k/w \rceil$ words, so it costs $O(k^2 / w)$ when $f$ costs $O(k / w)$. For the Mersenne Twister, $k = 19937$, so a jump costs on the order of $k^2 / w \approx 1.2 \cdot 10^7$ word operations, compared with a matrix power that would cost $O(k^3)$ per squaring. Extra space is a constant number of states and polynomials, $\Theta(k / w)$ words.

## Properties

- Exact: the result is the same state that $n$ single steps would reach, for any $n$, including $n$ larger than the period.
- Works for any affine generator modulo any $m$, prime or not, invertible multiplier or not.
- The F2 method needs only the generator's transition function and $\varphi$; it never builds the $k \times k$ matrix.
- Jumps compose: $f^{n_1 + n_2} = f^{n_2} \circ f^{n_1}$, so a stored jump of $2^{128}$ applied $j$ times gives the start of stream $j$.

## Variants and improvements

- **Streams and substreams.** RngStreams and its successors start stream $j$ at $f^{j \cdot 2^{127}}(s_0)$ and substream $\ell$ at a further $\ell \cdot 2^{76}$, with the jump matrices precomputed (L'Ecuyer et al. 2002).
- **Leapfrog.** Processor $j$ of $p$ uses $s_j, s_{j+p}, \ldots$, a generator with transition $f^p$. For LCGs this is again an LCG; for $\mathbb{F}_2$-linear generators each step costs a full jump, so blocks of consecutive outputs are preferred.
- **Sliding window method.** Haramoto et al. evaluate $r(A) s$ with a table of precomputed states, cutting the number of calls to $f$ when the same $\varphi$ is used many times.
- **Counter-based generators.** [Philox](/philox/) and [Threefry](/threefry/) compute output $i$ directly from a counter, so jumping is free.
- **Nonlinear output, linear state.** [PCG](/pcg-random/) has an LCG state and a nonlinear output, so the affine jump moves its state; the output function is applied afterwards.
- **Trapdoor jumps.** For [Blum-Blum-Shub](/blum-blum-shub/), $x_n = x_0^{2^n \bmod \lambda(N)} \bmod N$ with the [Carmichael function](/carmichael-function/) $\lambda$, which needs the factorization of $N$.

## When to use it

Use it to give parallel processes, threads or replications disjoint stretches of one long-period generator, to restart a simulation at a checkpoint, and to test a generator by comparing a jump against direct stepping. Prefer counter-based generators when outputs are needed in random order or on GPUs with very many threads.

## Pitfalls

- A jump moves the state, not the output buffer. Generators that produce outputs in blocks, such as the Mersenne Twister with its array of 624 words and index, must be jumped at a block boundary or have the index handled separately.
- Streams obtained by jumping are disjoint but still correlated in the sense of the generator's linear structure; seeding streams with unrelated random seeds instead risks overlap but avoids that structure. Long jumps of a well-tested generator are the standard choice.
- The polynomial $\varphi$ must annihilate the transition. A Berlekamp-Massey result from a sequence that is identically zero, or from too few bits, is not a valid $\varphi$.
- Overflow in L4 and L5: with $m = 2^{64}$ the products need 128-bit intermediates or wrapping arithmetic modulo $2^{64}$, which is exact here.
- For the leapfrog of an LCG with $m = 2^w$, the new multiplier $a^p$ may have bad lattice structure even when $a$ is good.

## Implementations

## History

The closed form $X_{n+k} = (a^k X_n + (a^k - 1) c / (a - 1)) \bmod m$ for LCGs is classical; Knuth gives it in Section 3.2.1. L'Ecuyer and Côté (1991) built a package with streams and substreams on a combined LCG using powers $a^{2^e} \bmod m$, and L'Ecuyer, Simard, Chen and Kelton (2002) extended it to MRG32k3a. For $\mathbb{F}_2$-linear generators with huge state, Haramoto, Matsumoto, Nishimura, Panneton and L'Ecuyer (2008) introduced the polynomial method above, which made jumping practical for the Mersenne Twister. Blackman and Vigna publish jump constants with each xoshiro and xoroshiro generator.

## References
