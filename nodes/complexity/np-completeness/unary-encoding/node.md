---
tag: 460XFB
kind: definition
slug: unary-encoding
name: Unary encoding
aliases:
- unary representation
area: complexity/np-completeness
level: core
summary: Writing a number N as N copies of one symbol, so the input length grows with the value of N and not with its logarithm.
prereqs: [input-size, decision-problem]
see_also: [pseudo-polynomial-time, strong-np-hardness, weak-np-hardness, mahaneys-theorem, input-size, positional-number-system, unary-coding, subset-sum-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 2.1 (encoding schemes and why unary numbers are not a reasonable encoding) and Section 4.2 (number problems and strong NP-completeness)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.1, Polynomial time (encodings, and the remark that a unary encoding changes the running time of an algorithm as a function of the input length)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 2, the NP-complete language TMSAT (certificate length and time bound in unary)
  - paper: Piotr Berman, Relationship between density and deterministic complexity of NP-complete languages, ICALP 1978, Lecture Notes in Computer Science 62
    title: Berman, no NP-complete tally set unless P = NP
    locator: the main theorem
---

The unary encoding of a natural number $N$ is the string of $N$ copies of one symbol, for example $1^N$. Its length is $N$, while the binary encoding of $N$ has only $\lfloor \log_2 N \rfloor + 1$ bits. So a change from binary to unary makes the [input size](/input-size/) exponentially larger, and an algorithm that is slow in terms of the binary length can be fast in terms of the unary length. This is the basis of [pseudo-polynomial time](/pseudo-polynomial-time/) and of [strong NP-hardness](/strong-np-hardness/). Complexity theory also uses the input $1^n$ to give an algorithm the value $n$ together with the right to run for time polynomial in $n$. For the prefix code with the same strings in data compression, see [unary coding](/unary-coding/).

## Definition

**Numbers.** The unary encoding of $N \ge 0$ over the alphabet $\{1\}$ is the string $1^N$, of length $N$. Some texts write $N + 1$ symbols, so that 0 also has a nonempty code; this changes lengths by one symbol.

**Instances.** To encode an instance with several numbers in unary, write each number in unary and put a separator symbol, for example $\#$, between them. The unary length $U(I)$ of an instance $I$ is the length of this string. For example, the [subset sum](/subset-sum-problem/) instance with numbers 3, 5, 9 and target 12 becomes

$$111\#11111\#111111111\#111111111111,$$

a string of 32 symbols. The binary encoding of the same instance needs $2 + 3 + 4 + 4 = 13$ bits for the numbers, plus separators.

**Unary problems.** For a problem $\Pi$ with numbers, the unary version of $\Pi$ is the same problem with instances encoded in unary. An algorithm for $\Pi$ is [pseudo-polynomial](/pseudo-polynomial-time/) if and only if it runs in time polynomial in $U(I)$. So $\Pi$ has a pseudo-polynomial algorithm if and only if its unary version is in P.

**Tally languages.** A language $L \subseteq \{1\}^*$ is a *tally language*, or tally set. It has at most one string of each length, so it is sparse.

**Not a reasonable encoding.** Garey and Johnson (Section 2.1) and CLRS (Section 34.1) define complexity classes with a reasonable encoding, which writes numbers in a base of at least 2. Unary is not reasonable in this sense, because it is exponentially longer than binary. Unary input is used on purpose when the question is whether the hardness of a problem depends on large numbers.

## Examples and non-examples

**Length.** $N = 1000$ takes 1000 symbols in unary and 10 bits in binary. For $N = 2^{64}$ the unary string cannot be stored, while the binary string has 65 bits.

**Subset sum in unary is in P.** The $O(nt)$ dynamic program for subset sum takes time $O(U^2)$ on unary input of length $U$, because $n \le U$ and $t \le U$. The same holds for [partition](/partition-problem/) and knapsack. These problems are [weakly NP-hard](/weak-np-hardness/): their hardness disappears in unary.

**3-partition in unary is NP-complete.** [3-partition](/three-partition/) is strongly NP-complete, so it stays NP-complete with the numbers in unary. A strongly NP-hard problem stays NP-hard in unary, because each instance with polynomially bounded numbers has a unary encoding of polynomial length.

**Primality and factoring in unary.** For a number $N$ given as $1^N$, trial division up to $\sqrt{N}$ takes time polynomial in $N$, so both problems are in P for unary input. For binary input, trial division is exponential in the length.

**Bounded halting.** Arora and Barak (Chapter 2) show that the language TMSAT is NP-complete. It contains the tuples $\langle M, x, 1^n, 1^t \rangle$ such that some certificate $u$ of $n$ bits makes the [Turing machine](/turing-machine/) $M$ accept $\langle x, u \rangle$ within $t$ steps. The bounds $n$ and $t$ are in unary so that a check of one certificate for $t$ steps takes time polynomial in the input length. With $n$ and $t$ written in binary, the same question is complete for [NEXP](/nexptime/).

**The input $1^n$ as a parameter.** In cryptography a [one-way function](/one-way-function/) or a key generator gets the security parameter as $1^n$, so that time polynomial in the input length means time polynomial in $n$. Uniform families of circuits are defined the same way, by a machine that outputs the $n$-th circuit on input $1^n$.

**Non-example: positional systems.** Binary, decimal and every other [positional number system](/positional-number-system/) with base $b \ge 2$ write $N$ with $\Theta(\log N)$ digits. Changing between two such bases changes lengths by a constant factor only, so polynomial time is the same for all of them.

**Non-example: the compression code.** [Unary coding](/unary-coding/) in data compression writes $n$ as a run of $n$ symbols followed by a stop symbol. It is a prefix code for small integers and a part of other codes. It is the same string, but it is used to make data short, not to make an instance long.

## Related definitions

- **Pseudo-polynomial time.** Time polynomial in the unary length; see [pseudo-polynomial time](/pseudo-polynomial-time/).
- **Strong and weak NP-hardness.** A strongly NP-hard problem stays NP-hard in unary; a weakly NP-hard problem is in P in unary. See [strong NP-hardness](/strong-np-hardness/) and [weak NP-hardness](/weak-np-hardness/).
- **Sparse sets and Mahaney's theorem.** Berman (1978) proved that if some tally language is NP-complete, then P = NP. Mahaney extended this to all sparse sets; see [Mahaney's theorem](/mahaneys-theorem/). The unary version of a number problem such as 3-partition is not a tally language, because its strings use separators and list many numbers, so these theorems do not apply to it.
- **Input size.** The [input size](/input-size/) of a number problem is its binary length, unless the unary encoding is stated.

## References
