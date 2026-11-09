---
tag: 4K3VJ5
kind: definition
slug: one-sided-error
name: One-sided error
aliases:
- one-sided error probability
- RP-type error
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Error that occurs on only one answer, so one outcome is always correct and the other is wrong with bounded probability.
prereqs: [monte-carlo-algorithm, randomized-algorithm]
see_also: [two-sided-error, error-amplification, rp, co-rp, miller-rabin-primality-test, freivalds-algorithm, polynomial-identity-testing, las-vegas-to-monte-carlo-conversion]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.2 (Monte Carlo algorithms with one-sided error) and Section 1.5 (the classes RP and co-RP)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 7, Randomized computation (the definitions of RP and co-RP, and error reduction for one-sided error)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (verifying polynomial identities and matrix multiplication, with error on one side only, and repetition)
---

A [Monte Carlo algorithm](/monte-carlo-algorithm/) for a decision problem has one-sided error when one of its two answers is always correct and only the other answer can be wrong. The [Miller-Rabin test](/miller-rabin-primality-test/) is the standard example: when it says "composite", the number is composite, and only "prime" can be wrong. Repetition with an OR of the answers drives the error down as $\delta^k$, which is simpler and faster than the majority vote needed for [two-sided error](/two-sided-error/). In polynomial time, one-sided error defines the classes [RP](/rp/) and [co-RP](/co-rp/).

## Definition

Notation on this page: $n = |x|$ is the input size, $\delta$ is the error probability, and $\Pr$ is over the random bits of the algorithm for one fixed input.

Let $L$ be a language (a decision problem) and $A$ a randomized algorithm that stops on every input and every random string and answers "yes" or "no". $A$ has **one-sided error $\delta$ on the "no" side**, or *RP-type error*, if for every input $x$:

$$x \in L \implies \Pr[A(x) = \text{yes}] \ge 1 - \delta, \qquad x \notin L \implies \Pr[A(x) = \text{yes}] = 0.$$

So the answer "yes" is always correct, and the answer "no" is wrong with probability at most $\delta$. $A$ has **one-sided error on the "yes" side**, or *co-RP-type error*, if the roles swap: "no" is always correct, and on $x \notin L$ the answer "yes" appears with probability at most $\delta$. An algorithm with one kind of error for $L$ is an algorithm with the other kind for the complement of $L$.

The classes: $L \in$ [RP](/rp/) if an algorithm with RP-type error $\delta \le 1/2$ runs in polynomial time on every input and every random string; $L \in$ [co-RP](/co-rp/) if the complement of $L$ is in RP.

### Facts

**The constant does not matter.** Let $A$ have RP-type error $\delta < 1$. Run it $k$ times with independent bits and say "yes" if some run says "yes". On $x \notin L$ no run says "yes", so the answer is right. On $x \in L$ the answer is wrong only if all $k$ runs say "no", which has probability at most $\delta^k$. This also works when the success probability is as small as $1/q(n)$ for a polynomial $q$: after $k = \lceil q(n) \ln(1/\delta') \rceil$ runs the error is at most $(1 - 1/q(n))^k \le e^{-k/q(n)} \le \delta'$. [Error amplification](/error-amplification/) gives the exact number of rounds for each target.

**A "yes" answer is a certificate.** If $A$ has RP-type error $\delta < 1$, then $x \in L$ if and only if some random string $r$ makes $A(x, r)$ say "yes": no string does so when $x \notin L$, and a set of strings of probability at least $1 - \delta > 0$ does when $x \in L$. If $A$ runs in polynomial time, $r$ has polynomial length and $A(x, r)$ checks it, so RP $\subseteq$ [NP](/np/), and co-RP $\subseteq$ [co-NP](/co-np/). In most natural algorithms the certificate is a short *witness*: the base $a$ for Miller-Rabin, the vector $r$ for Freivalds.

**One-sided implies two-sided.** An algorithm with RP-type error $1/2$, run twice with an OR, has error at most $1/4 < 1/3$ on "yes" inputs and 0 on "no" inputs, so RP $\subseteq$ [BPP](/bpp/).

## Examples and non-examples

- **Miller-Rabin.** For $L$ = the odd composite numbers, the [Miller-Rabin test](/miller-rabin-primality-test/) says "composite" only when it has found a witness, so it has RP-type error, and at most $1/4$ for each round. PRIMES is therefore in co-RP. On the [Carmichael number](/carmichael-number/) 561, a base from $\{2, \ldots, 559\}$ is a strong liar with probability $8/558$, so three rounds miss with probability $(8/558)^3 \approx 2.95 \times 10^{-6}$.
- **Freivalds' algorithm.** For $L = \{(A, B, C) : AB \ne C\}$, [Freivalds' algorithm](/freivalds-algorithm/) says "not equal" only when it has found $r$ with $A(Br) \ne Cr$. It has RP-type error at most $1/2$ for each vector from $\{0, 1\}^n$.
- **Polynomial identity testing.** For $L$ = the circuits that compute a nonzero polynomial, evaluation at a random point says "nonzero" only when it sees a nonzero value. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) the error is at most $d/|S|$. See [polynomial identity testing](/polynomial-identity-testing/).
- **Karger's contraction, one-sided in value.** [Karger's algorithm](/karger-min-cut/) returns a cut whose size is never below the minimum. Its error is "too large", never "too small", so the smallest of many runs can only get better.
- **Bloom filter.** A [Bloom filter](/bloom-filter/) answers "not in the set" only for keys that were never inserted. Its error is false positives only, with a probability that depends on the random hash functions.
- **Non-example: the Fermat test.** The [Fermat test](/fermat-primality-test/) also never rejects a prime, but it has no error bound $\delta < 1$ that holds for every composite input. On a Carmichael number every base coprime to it passes; for 8911 a random base from $\{2, \ldots, 8909\}$ passes with probability $7126/8908 \approx 0.80$. A one-sided error bound must hold on each input.
- **Non-example: a majority vote of noisy tests.** An estimator that compares a sample mean with a threshold can be wrong on both sides. Its error is [two-sided](/two-sided-error/).
- **Non-example: a Las Vegas algorithm.** It has no error at all, on either side. In the form with the answer $\bot$, a ZPP algorithm can be turned into one with one-sided error on either side by a fixed answer on time-out, see [Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).

## Related definitions

- **[Two-sided error](/two-sided-error/).** Both answers can be wrong; the error must be below $1/2$ by a gap, and amplification needs a majority vote.
- **[Error amplification](/error-amplification/).** The OR of $k$ runs for one-sided error, with $k = \lceil \ln(1/\delta)/\ln(1/\delta_0) \rceil$ rounds to go from error $\delta_0$ to $\delta$.
- **[RP](/rp/), [co-RP](/co-rp/) and [ZPP](/zpp/).** One-sided error in polynomial time, on each side; ZPP is their intersection.
- **[Monte Carlo algorithm](/monte-carlo-algorithm/)** and **[Las Vegas algorithm](/las-vegas-algorithm/).** The general kinds of randomized algorithms; one-sided error is a property of some Monte Carlo algorithms for decision problems.
- **[Compositeness witness](/compositeness-witness/).** The certificate behind the one-sided error of primality tests.

## References
