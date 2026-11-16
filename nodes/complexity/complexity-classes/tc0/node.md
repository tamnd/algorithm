---
tag: 4XRRSZ
kind: definition
slug: tc0
name: TC0
aliases:
- TC^0
- threshold circuits
area: complexity/complexity-classes
level: advanced
summary: The problems decided by constant-depth, polynomial-size circuits with majority gates of unbounded fan-in. It contains parity, multiplication and division, and it lies inside NC1.
prereqs: [boolean-circuit, ac0]
see_also: [ac0, nc, circuit-complexity, perceptron, integer-division, natural-proofs-barrier, permanent-computation, pseudorandom-function]
sources:
  - paper: doi:10.1137/0213028
    title: Ashok K. Chandra, Larry Stockmeyer and Uzi Vishkin, Constant depth reducibility, SIAM Journal on Computing 13(2), 423 to 439 (1984)
    locator: constant-depth circuits with majority gates for iterated addition and multiplication
  - paper: doi:10.1016/0022-0000(93)90001-D
    title: András Hajnal, Wolfgang Maass, Pavel Pudlák, Mario Szegedy and György Turán, Threshold circuits of bounded depth, Journal of Computer and System Sciences 46(2), 129 to 154 (1993)
    locator: the exponential lower bound for inner product mod 2 on depth-2 majority circuits
  - paper: doi:10.1137/0215070
    title: Paul W. Beame, Stephen A. Cook and H. James Hoover, Log depth circuits for division and related problems, SIAM Journal on Computing 15(4), 994 to 1003 (1986)
    locator: P-uniform circuits for division, iterated multiplication and powering
  - paper: doi:10.1016/S0022-0000(02)00025-9
    title: William Hesse, Eric Allender and David A. Mix Barrington, Uniform constant-depth threshold circuits for division and iterated multiplication, Journal of Computer and System Sciences 65(4), 695 to 716 (2002)
    locator: the main theorem (division in DLOGTIME-uniform TC0)
  - paper: doi:10.1016/0022-0000(90)90022-D
    title: David A. Mix Barrington, Neil Immerman and Howard Straubing, On uniformity within NC1, Journal of Computer and System Sciences 41(3), 274 to 306 (1990)
    locator: DLOGTIME uniformity and the logical characterization of uniform TC0
  - paper: "Eric Allender, The permanent requires large uniform threshold circuits, Chicago Journal of Theoretical Computer Science 1999, article 7"
    locator: the main theorem
  - paper: doi:10.1145/972639.972643
    title: Moni Naor and Omer Reingold, Number-theoretic constructions of efficient pseudo-random functions, Journal of the ACM 51(2), 231 to 262 (2004)
    locator: pseudorandom functions computable in TC0 under number-theoretic assumptions
  - book: isbn:9783540643104
    title: Heribert Vollmer, Introduction to Circuit Complexity, A Uniform Approach, Springer (1999)
    locator: the chapter on threshold circuits
---

TC0 is the class of decision problems that have [Boolean circuits](/boolean-circuit/) of constant depth and polynomial size, built from majority gates of unbounded fan-in together with AND, OR and NOT. It is [AC0](/ac0/) with the power to count: a single majority gate compares the number of ones in its input with a threshold, which no AC0 circuit can do. Integer addition of many numbers, multiplication, division and sorting are all in TC0, and TC0 is contained in $\mathsf{NC}^1$. Threshold circuits are also the circuit model of feedforward neural networks with step activations, and they are the frontier of circuit lower bounds: no superpolynomial lower bound against TC0 is known for any problem in NEXP.

## Definition

**Gates.** A majority gate with inputs $y_1, \ldots, y_m$ outputs $1$ if and only if $\sum_i y_i \ge m/2$. A threshold gate with integer weights $w_1, \ldots, w_m$ and threshold $t$ outputs $1$ if and only if $\sum_i w_i y_i \ge t$. A threshold gate whose weights are bounded by a polynomial in $m$ is a majority gate with each input repeated $|w_i|$ times, negated when $w_i < 0$, and padded with constants to move the threshold. So the two gate types give the same class when the weights are polynomial. Threshold gates with arbitrary integer weights can also be simulated, at the cost of one more layer of depth.

**Definition.** A language $L \subseteq \{0,1\}^*$ is in $\mathsf{TC}^0$ if there are a constant $d$, a polynomial $s$ and a circuit family $\{C_n\}$ such that, for every $n$:

- *size*: $C_n$ has at most $s(n)$ gates,
- *depth*: every input-to-output path has at most $d$ gates,
- *gate set and fan-in*: majority, AND and OR of unbounded fan-in, NOT of fan-in 1,
- *correctness*: $C_n(x) = 1$ if and only if $x \in L$, for every $x \in \{0,1\}^n$.

The class $\mathsf{TC}^0_d$ is the same with depth at most $d$.

**Uniformity.** As written, the definition is non-uniform. The standard uniform version is DLOGTIME-uniform TC0, in which a machine with random access to its input answers questions about gate types and wires of $C_n$ in time $O(\log n)$. Barrington, Immerman and Straubing (1990) proved that DLOGTIME-uniform TC0 equals the languages definable in first-order logic with order, BIT and majority quantifiers. P-uniform TC0, in which a polynomial-time machine prints $C_n$, is a weaker condition, and some results were first proved only for it.

**Place among other classes.**

$$\mathsf{AC}^0 \subsetneq \mathsf{TC}^0 \subseteq \mathsf{NC}^1 \subseteq \mathsf{L}.$$

The first inclusion is strict because parity is in TC0 and not in AC0. The second holds because one majority gate of fan-in $m$ is computed in depth $O(\log m)$ with fan-in 2 gates: add the inputs in binary with a tree of carry-save adders, which reduce three numbers to two in constant depth, and finish with one addition. Whether $\mathsf{TC}^0 = \mathsf{NC}^1$ is open. Whether TC0 contains NP, or even NEXP, is open in the non-uniform setting.

## Examples and non-examples

**Parity in depth 2.** Let $s = x_1 + \cdots + x_n$. The first layer has $n$ threshold gates $g_k = [s \ge k]$ for $k = 1, \ldots, n$, so $g_1, \ldots, g_n$ is $s$ ones followed by zeros. The output gate is

$$[\, g_1 - g_2 + g_3 - g_4 + \cdots \ge 1 \,],$$

a threshold gate with weights $\pm 1$. The alternating sum is $1$ if $s$ is odd and $0$ if $s$ is even. For $x = 101101$, $s = 4$, the first layer gives $1, 1, 1, 1, 0, 0$, the alternating sum is $0$, and the output is $0$. The circuit has $n + 1$ gates. The same idea computes any symmetric function, that is any function of $s$ alone, in depth 2.

**Arithmetic.** Each item is in TC0, with the uniformity stated.

- *Counting and iterated addition.* The sum of $n$ numbers of $n$ bits each is in TC0 (Chandra, Stockmeyer and Vishkin 1984), with circuits that are DLOGTIME-uniform. Bit $j$ of a sum of single bits is a symmetric function of them, and a sum of long numbers is split into blocks of $O(\log n)$ bits whose column sums are short.
- *Multiplication.* The product of two $n$-bit numbers is the sum of $n$ shifted copies of one of them, so it is an iterated addition. By the [AC0](/ac0/) page, multiplication is not in AC0, so TC0 is the smallest of these classes that contains it.
- *Sorting.* The rank of each of $n$ numbers is the number of numbers smaller than it, a sum of $n$ comparison bits with ties broken by position, and each output position selects the number with that rank by an OR of ANDs.
- *Division, iterated multiplication and powering.* Beame, Cook and Hoover (1986) gave P-uniform TC0 circuits, through the [Chinese remainder theorem](/chinese-remainder-theorem/) with many small primes. Hesse, Allender and Barrington (2002) made them DLOGTIME-uniform. So [integer division](/integer-division/) is in uniform TC0.

**Inner product mod 2: depth 2 against depth 3.** Let $\mathrm{IP}(x, y) = \bigoplus_{i=1}^n x_i y_i$. It is in $\mathsf{TC}^0_3$: one layer of AND gates for the products, then the parity circuit above. Hajnal, Maass, Pudlák, Szegedy and Turán (1993) proved that every depth-2 majority circuit for IP has exponential size. So depth 3 is strictly stronger than depth 2 for majority circuits of polynomial size. For larger depths no separation is known: it is open whether every TC0 language has polynomial-size majority circuits of depth 3.

**The permanent.** The [permanent](/permanent-computation/) of a 0-1 matrix is #P-complete. Allender (1999) proved that it has no DLOGTIME-uniform threshold circuits of constant depth and polynomial size, by a diagonal argument over uniform circuits. For non-uniform TC0 this is open.

**Non-examples.** Few are proved. Every language outside [NC](/nc/)$^1$ is outside TC0, but no explicit language in NP is known to be outside $\mathsf{NC}^1$. For uniform TC0, the time and space hierarchy theorems give languages in [PSPACE](/pspace/) that are not in DLOGTIME-uniform TC0, because uniform TC0 is in [logspace](/logspace/). Problems that are complete for $\mathsf{NC}^1$ under AC0 reductions, such as evaluation of Boolean formulas and the word problem of the group $S_5$, are believed not to be in TC0.

**Neural networks and pseudorandomness.** A feedforward network of [perceptrons](/perceptron/) with step activations and polynomially bounded weights is a threshold circuit, and constant-depth networks of polynomial size compute exactly TC0. Naor and Reingold (1997, journal version 2004) built [pseudorandom functions](/pseudorandom-function/) computable in TC0, secure if the decisional Diffie-Hellman problem or factoring is hard. By the [natural proofs barrier](/natural-proofs-barrier/), a natural proof cannot then show that a problem is outside TC0. This is one reason TC0 lower bounds stall.

## Related definitions

- [AC0](/ac0/): the same depth and size, without majority gates.
- [NC](/nc/): $\mathsf{TC}^i$ allows depth $O(\log^i n)$, and $\mathsf{AC}^i \subseteq \mathsf{TC}^i \subseteq \mathsf{NC}^{i+1}$.
- AC0[$m$] and ACC0: AC0 with counting modulo $m$, a class between AC0 and TC0.
- [Circuit complexity](/circuit-complexity/): the general study of circuit lower bounds.

## References
