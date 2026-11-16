---
tag: C5NE6Z
kind: definition
slug: kolmogorov-complexity
name: Kolmogorov complexity
aliases:
- algorithmic information content
area: complexity/computability
level: advanced
summary: "The length of the shortest program that prints a given string on a fixed universal machine. It depends on the machine only up to an additive constant, and it is not computable."
prereqs: [universal-turing-machine, uncomputable-function, prefix-code]
see_also: [incompressibility-method, chaitins-constant, uncomputable-function, shannon-entropy, kraft-inequality, minimum-description-length, busy-beaver-function, incompressibility-argument]
sources:
  - paper: doi:10.1016/S0019-9958(64)90223-2
    title: Ray J. Solomonoff, A formal theory of inductive inference, Part I, Information and Control 7(1) (1964)
    locator: pp. 1 to 22
  - title: Andrei N. Kolmogorov, Three approaches to the quantitative definition of information, Problems of Information Transmission 1(1) (1965)
    locator: pp. 1 to 7
  - paper: doi:10.1145/321356.321363
    title: Gregory J. Chaitin, On the length of programs for computing finite binary sequences, Journal of the ACM 13(4) (1966)
    locator: pp. 547 to 569
  - title: Gregory J. Chaitin, A theory of program size formally identical to information theory, Journal of the ACM 22(3) (1975)
    locator: pp. 329 to 340 (prefix complexity)
  - book: isbn:9783030112974
    title: Ming Li and Paul Vitányi, An Introduction to Kolmogorov Complexity and Its Applications, fourth edition, Springer, 2019
    locator: Chapter 2, Algorithmic Complexity (Section 2.1, the invariance theorem); Chapter 3, Algorithmic Prefix Complexity
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 6.4, A definition of information
---

The Kolmogorov complexity of a string is the length of the shortest program that prints it and halts. A string with a pattern, such as a million zeros, has a short program and so low complexity. A string with no pattern needs a program about as long as the string itself, which just contains the string. Solomonoff (1964), Kolmogorov (1965) and Chaitin (1966) defined it independently. The value depends on the programming language, but by the invariance theorem two universal languages give values that differ by at most a constant, so the notion is robust. The function is not computable, and no formal theory can prove that any particular string has complexity above a fixed bound. The page on the [incompressibility method](/incompressibility-method/) shows how the counting facts below are used to prove lower bounds. The term is not related to *descriptive complexity*, the study of complexity classes through logic.

## Definition

Fix a universal machine $U$ that takes a binary program $p$ and may output a binary string $U(p)$. The *plain Kolmogorov complexity* of a string $x$ with respect to $U$ is
$$C_U(x) = \min \{ |p| : U(p) = x \},$$
the length of a shortest program that makes $U$ print $x$ and halt. The *conditional complexity* $C_U(x \mid y)$ is the same with $y$ given to $U$ as extra input.

**Invariance theorem.** There is a machine $U$ such that for every machine $V$ there is a constant $c_V$ with
$$C_U(x) \le C_V(x) + c_V \quad \text{for all } x.$$
Any two machines $U$ and $U'$ with this property satisfy $|C_U(x) - C_{U'}(x)| \le c$ for a constant $c$ and all $x$.

*Proof.* Let $V_1, V_2, \ldots$ list all machines. Let $U$ read its input as $1^{i} 0\, p$ and run $V_i$ on $p$. If $V_i(p) = x$ with $|p| = C_{V_i}(x)$, then $U(1^i 0 p) = x$, so $C_U(x) \le C_{V_i}(x) + i + 1$. For the second claim, apply the first with $V = U'$ and with the roles swapped. $\blacksquare$

From now on fix such a $U$ and write $C(x)$. Statements about $C$ hold up to an additive constant.

**Basic facts.**

- **Upper bound.** $C(x) \le |x| + c$, since a program can contain $x$ and print it.
- **Counting.** There are $2^m - 1$ binary programs of length less than $m$, and each prints at most one string. So for every $n$ and $k$, fewer than $2^{n-k}$ strings of length $n$ have $C(x) < n - k$. In particular, every length $n$ has a string with $C(x) \ge n$, called *incompressible*, and at most a fraction $2^{-k}$ of the strings of length $n$ can be compressed by $k$ or more bits.
- **Not computable.** Suppose $C$ were computable. For each $n$, let $Q_n$ be the program "find the first string $x$, in order of length and then of value, with $C(x) \ge n$, and print it". By counting, such an $x$ exists. The program $Q_n$ needs to store only $n$, so $|Q_n| \le \log_2 n + c$, and it prints a string with $C(x) \ge n$. Then $n \le C(x) \le \log_2 n + c$, which is false for large $n$. This is a precise form of Berry's paradox, "the smallest number not definable in fewer than twenty words".
- **Approximable from above.** Run all programs in parallel. Each time one halts with output $x$, record its length if it is shorter than any before. These guesses decrease and reach $C(x)$, but no algorithm can tell when the last decrease has happened.
- **Unprovable lower bounds (Chaitin).** For a consistent formal theory $T$ with a c.e. set of axioms, there is a constant $L_T$ such that $T$ proves no statement "$C(x) > L_T$" about a specific $x$, even though all but finitely many strings satisfy it. The proof is the same search, run through the theorems of $T$.

**Prefix complexity.** In the plain definition a program's end is marked from outside, so $C$ is not additive: $C(xy)$ can exceed $C(x) + C(y)$ by a logarithmic term. If the programs of $U$ must form a [prefix code](/prefix-code/), where no program is a prefix of another, the result is the *prefix complexity* $K(x)$ (Chaitin 1975, and Levin). It satisfies $C(x) \le K(x) + c$ and $K(x) \le C(x) + 2 \log_2 C(x) + c$. By the [Kraft inequality](/kraft-inequality/), $\sum_x 2^{-K(x)} \le 1$. Prefix complexity is the form used for [Chaitin's constant](/chaitins-constant/) and for algorithmic probability.

## Examples and non-examples

**Upper bounds from a compressor.** A compressor gives an upper bound on $C$: if a fixed decompressor turns the compressed string $z$ into $x$, then $C(x) \le |z| + c$, where $c$ covers the decompressor. With zlib at level $9$:

| string of 10,000 bytes | compressed size |
|---|---|
| all zero bytes | 33 bytes |
| `0123456789` repeated 1000 times | 54 bytes |
| pseudo-random bytes | 10,011 bytes |

The first two have short descriptions. For the third, zlib finds no pattern and adds a little overhead. Yet the pseudo-random bytes come from a seeded generator, so a short program that stores the generator and its seed prints them: their true complexity is small, and a compressor cannot see it. A compressor only bounds $C$ from above.

**A string of zeros.** $C(0^n) \le \log_2 n + c$, since a program needs only $n$. For most $n$ this is close to the truth, since $C(0^n) \ge C(n) - c$ and most numbers $n$ are incompressible as strings.

**Digits of pi.** The first million binary digits of $\pi$ pass statistical tests for randomness, but a short program computes them, so their complexity is about $\log_2$ of a million plus a constant. Low complexity does not mean easy to spot.

**Most strings are incompressible.** For $n = 20$ there are $2^{20} = 1{,}048{,}576$ strings and only $1{,}048{,}575$ programs shorter than $20$ bits, so at least one string of length $20$ has no shorter program. Only $4095$ programs are shorter than $12$ bits, so at most $4095$ strings of length $20$, fewer than $1$ in $256$, can be compressed by $8$ bits or more.

**Non-example: Shannon entropy.** [Shannon entropy](/shannon-entropy/) is a property of a probability distribution, not of a single string. The two notions meet in the mean: for a computable distribution $P$, the expected value of $K(x)$ under $P$ equals the entropy of $P$ up to an additive term that depends on the complexity of $P$ itself.

**Non-example: running time.** $C$ ignores time. A string printed by a short program that runs for $10^{100}$ steps has low complexity. Resource-bounded versions, which limit the time of the program, are used in complexity theory.

## Related definitions

- **Incompressibility method.** Pick an incompressible input and show that a fast or small algorithm would compress it. See the [incompressibility method](/incompressibility-method/) and the [incompressibility argument](/incompressibility-argument/) of data compression.
- **Chaitin's constant.** The probability that a random prefix-free program halts, $\Omega = \sum_{U(p) \text{ halts}} 2^{-|p|}$. Its first $n$ bits have prefix complexity at least $n - c$. See [Chaitin's constant](/chaitins-constant/).
- **Randomness of infinite sequences.** An infinite binary sequence is Martin-Löf random if and only if the prefix complexity of its first $n$ bits is at least $n - c$ for some constant $c$ and all $n$ (Levin, Schnorr, Chaitin).
- **Minimum description length.** The [MDL principle](/minimum-description-length/) chooses the model that gives the shortest total description of model and data, a computable stand-in for Kolmogorov complexity and a form of [Occam's razor](/occams-razor/).
- **Busy beaver.** The [busy beaver function](/busy-beaver-function/) and $C$ are linked: knowing the largest running time of programs of length at most $n$ would make $C$ computable for strings with complexity at most $n$.

## References
