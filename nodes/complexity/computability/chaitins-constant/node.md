---
tag: FCK6N6
kind: definition
slug: chaitins-constant
name: Chaitin's constant
aliases:
- halting probability
- Omega
area: complexity/computability
level: research
summary: "The probability that a random program for a fixed prefix-free universal machine halts. It is a random real, and its first n bits decide halting for all programs of length at most n."
prereqs: [kolmogorov-complexity, halting-problem, prefix-code]
see_also: [kolmogorov-complexity, halting-problem, busy-beaver-function, uncomputable-function, kraft-inequality, turing-degrees, godel-incompleteness-theorem, universal-turing-machine]
sources:
  - title: Gregory J. Chaitin, A theory of program size formally identical to information theory, Journal of the ACM 22(3) (1975)
    locator: pp. 329 to 340
  - book: isbn:9783030112974
    title: Ming Li and Paul Vitányi, An Introduction to Kolmogorov Complexity and Its Applications, fourth edition, Springer, 2019
    locator: Chapter 3, Algorithmic Prefix Complexity
  - title: Cristian S. Calude, Peter H. Hertling, Bakhadyr Khoussainov and Yongge Wang, Recursively enumerable reals and Chaitin Omega numbers, Theoretical Computer Science 255 (2001)
    locator: pp. 125 to 149
  - title: Antonín Kučera and Theodore A. Slaman, Randomness and recursive enumerability, SIAM Journal on Computing 31(1) (2001)
    locator: pp. 199 to 211
  - paper: doi:10.1145/321356.321363
    title: Gregory J. Chaitin, On the length of programs for computing finite binary sequences, Journal of the ACM 13(4) (1966)
    locator: pp. 547 to 569
---

Chaitin's constant, also called the halting probability and written $\Omega$, is the probability that a program chosen by fair coin flips halts on a fixed universal machine. Gregory Chaitin defined it in 1975, for machines whose programs form a prefix code, so that the coin flips mark where a program ends. It is a single real number between $0$ and $1$ that holds the answer to the [halting problem](/halting-problem/) in a very compact form: its first $n$ bits tell which programs of length at most $n$ halt. For this reason the number cannot be computed, and its bits look like the results of a fair coin. It is the standard example of an algorithmically random real. Its value depends on the machine, so there are many Chaitin constants, one for each universal prefix-free machine, and they all share these properties.

## Definition

Let $U$ be a universal *prefix-free* machine: the set of programs $p$ on which $U$ halts is a [prefix code](/prefix-code/), so no halting program is a prefix of another. The machine $U$ also defines the prefix complexity $K(x)$ of [Kolmogorov complexity](/kolmogorov-complexity/). The *halting probability* of $U$ is
$$\Omega_U = \sum_{p \,:\, U(p) \text{ halts}} 2^{-|p|}.$$
Think of a program as built from fair coin flips, one bit at a time, until the bits so far form a halting program. Then $\Omega_U$ is the probability that this happens. By the [Kraft inequality](/kraft-inequality/), $\Omega_U \le 1$, and for a universal $U$ it lies strictly between $0$ and $1$. Write $\Omega$ for $\Omega_U$ when $U$ is fixed, and $\Omega \upharpoonright n$ for its first $n$ binary digits.

**Approximable from below.** Let $\Omega_t$ be the sum over the programs of length at most $t$ that halt within $t$ steps. Each $\Omega_t$ is a rational number computable from $t$, the sequence increases, and its limit is $\Omega$. A real number with such an increasing computable sequence of rationals is called *left-c.e.* (left computably enumerable). The sequence gives no bound on how far it still is from $\Omega$.

**The first $n$ bits decide halting.** Given $\Omega \upharpoonright n$, read as the rational $w = 0.\Omega_1 \cdots \Omega_n$, we have $w \le \Omega < w + 2^{-n}$. Compute $\Omega_t$ for $t = 1, 2, \ldots$ until $\Omega_t \ge w$; this happens, since $\Omega_t \to \Omega \ge w$, and $\Omega \ne w$ because $\Omega$ is irrational (see below). Now let $p$ be any program with $|p| \le n$ that has not halted within $t$ steps. If $p$ halted later, then
$$\Omega \ge \Omega_t + 2^{-|p|} \ge w + 2^{-n},$$
which is false. So $p$ never halts. Thus $\Omega \upharpoonright n$ decides the halting of every program of length at most $n$.

**Incompressible.** There is a constant $c$ with $K(\Omega \upharpoonright n) \ge n - c$ for all $n$. *Proof.* From $\Omega \upharpoonright n$, the procedure above finds every output of every halting program of length at most $n$. A fixed program can then print the first string $x$ that is not among these outputs, so $K(x) > n$. That program reads a shortest description of $\Omega \upharpoonright n$, so $K(x) \le K(\Omega \upharpoonright n) + c$. Together, $K(\Omega \upharpoonright n) \ge n - c$. $\blacksquare$

**Consequences of the definition.**

- **Not computable.** A computable real has $K(\text{first } n \text{ bits}) \le K(n) + c$, which is about $\log_2 n$, far below $n - c$. In particular $\Omega$ is irrational and transcendental, since every algebraic number is computable.
- **Random.** By the theorem of Levin, Schnorr and Chaitin, a real whose prefixes satisfy $K(\Omega \upharpoonright n) \ge n - c$ is Martin-Löf random: it passes every effective statistical test. So its bits are, for example, $0$ and $1$ with limit frequency $\tfrac{1}{2}$ each.
- **Same degree as halting.** Halting is decidable from $\Omega$ by the procedure above, and $\Omega$ is computable from the halting problem, since a halting oracle decides each comparison of $\Omega$ with a rational. So $\Omega$ has [Turing degree](/turing-degrees/) $\mathbf{0}'$.
- **Few bits are provable.** For a consistent formal theory $T$ with a c.e. set of axioms that proves only true statements about $\Omega$, there is an $N$ such that $T$ determines at most $N$ bits of $\Omega$. Otherwise $T$ would give short descriptions of long prefixes. This is a form of [Gödel's incompleteness theorem](/godel-incompleteness-theorem/).

**Which reals are Chaitin constants.** Every $\Omega_U$ is left-c.e. and random. The converse also holds: every left-c.e. random real in $(0, 1)$ equals $\Omega_U$ for some universal prefix-free machine $U$. This follows from the work of Calude, Hertling, Khoussainov and Wang (2001) and of Kučera and Slaman (2001).

## Examples and non-examples

**A toy halting probability.** For a real universal machine no bit of $\Omega$ can be found by hand, so here is a finite model with the same structure. Code a two-state Turing machine, in the model of the [busy beaver](/busy-beaver-function/) page, by $16$ bits: $4$ transitions of $4$ bits each, one bit for the symbol to write, one bit for the move, and two bits for the next state, where $0$ and $1$ mean states $A$ and $B$ and $2$ and $3$ mean halt. Pick the $16$ bits by fair coin flips and run the machine on a blank tape. Of the $65{,}536$ codes, $42{,}416$ halt, so the halting probability is
$$\frac{42{,}416}{65{,}536} = \frac{2651}{4096} = 0.647216796875.$$
The approximations from below, by the number of steps allowed, are:

| steps $t$ | codes that halt in exactly $t$ steps | probability of halting within $t$ steps |
|---|---|---|
| 1 | 32,768 | 0.5 |
| 2 | 8192 | 0.625 |
| 3 | 1024 | 0.640625 |
| 4 | 320 | 0.6455078125 |
| 5 | 32 | 0.64599609375 |
| 6 | 80 | 0.647216796875 |
| 7 | 0 | 0.647216796875 |

A run with a limit of $50$ steps gave these counts. No code halts after step $6$, which matches the busy beaver value $S(2) = 6$. Here the limit is computable because the model is not universal: $S(2)$ is known, so the search knows when to stop. For a universal machine the sums $\Omega_t$ also increase step by step, but no computable bound says when a digit has become final.

**Non-example: a plain machine.** Without the prefix-free condition the sum $\sum 2^{-|p|}$ over halting programs diverges for a universal machine, since there are $2^n$ programs of each length $n$ and a fixed fraction of them halt. The prefix-free condition, through the Kraft inequality, is what makes $\Omega$ a probability.

**Non-example: a computable real that looks complex.** The binary digits of $\pi$ pass many statistical tests, but $\pi$ is computable, so the prefix complexity of its first $n$ bits is at most about $\log_2 n$. It is not random in the sense above, and it holds no information about halting.

**Non-example: the halting set as a real.** The real $h = \sum_{e \in H} 2^{-e-1}$, where $H$ is the set of programs that halt,, whose $e$-th bit says whether program $e$ halts, has the same Turing degree as $\Omega$. But $h$ is not random: its first $n$ bits can be computed from the number of halting programs among the first $n$, which takes only about $\log_2 n$ bits. $\Omega$ packs the same information exponentially more densely.

## Related definitions

- **Prefix complexity.** $K(x)$, the length of a shortest program for $x$ on a prefix-free machine; see [Kolmogorov complexity](/kolmogorov-complexity/). The randomness of $\Omega$ is stated in terms of $K$.
- **Algorithmic probability.** The probability that $U$ outputs a given string $x$ is $\sum_{U(p) = x} 2^{-|p|}$. Summing over all $x$ gives $\Omega$. By the coding theorem of Levin and Chaitin, the probability of $x$ is $2^{-K(x)}$ up to a constant factor.
- **Busy beaver function.** The [busy beaver function](/busy-beaver-function/) is another uncomputable object that encodes halting. From $\Omega \upharpoonright n$ the procedure above also gives the largest running time of a halting program of length at most $n$, which is a busy beaver function for $U$.
- **Uncomputable functions and reals.** $\Omega$ is the standard example of an [uncomputable](/uncomputable-function/) real number with a simple definition, alongside the halting set itself.

## References
