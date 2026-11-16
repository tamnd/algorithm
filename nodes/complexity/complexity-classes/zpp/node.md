---
tag: QA3Z6S
kind: definition
slug: zpp
name: ZPP
aliases:
- zero-error probabilistic polynomial time
area: complexity/complexity-classes
level: advanced
summary: The decision problems that a probabilistic machine decides with no error in expected polynomial time. ZPP equals RP intersected with coRP and is the class of Las Vegas algorithms.
prereqs: [rp, co-rp, markov-inequality, las-vegas-algorithm]
see_also: [rp, co-rp, bpp, las-vegas-algorithm, monte-carlo-algorithm, primality-testing, aks-primality-test, markov-inequality]
sources:
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4), 675 to 695 (1977)
    locator: the definition of ZPP and its characterization by machines that may answer "don't know"
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (zero-sided error and ZPP = RP intersected with coRP)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 1, Introduction (Las Vegas and Monte Carlo algorithms and the class ZPP)
  - book: isbn:9783540553083
    title: Leonard M. Adleman and Ming-Deh A. Huang, Primality Testing and Abelian Varieties over Finite Fields, Lecture Notes in Mathematics 1512, Springer (1992)
    locator: the main theorem (a random polynomial-time algorithm that proves primality)
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2), 781 to 793 (2004)
    locator: the main theorem
---

ZPP (zero-error probabilistic polynomial time) is the class of decision problems that a [probabilistic Turing machine](/probabilistic-turing-machine/) decides with no error in expected polynomial time. The machine always gives the right answer, and only its running time depends on the coins. These are the [Las Vegas algorithms](/las-vegas-algorithm/). ZPP has three equivalent definitions, and one of them is $\mathsf{ZPP} = \mathsf{RP} \cap \mathsf{coRP}$.

## Definition

**Model.** The machine is a probabilistic [multitape Turing machine](/multitape-turing-machine/) that flips fair coins. Unlike for [BPP](/bpp/) and [RP](/rp/), its running time is a random variable that depends on the coins, and it can be long on some coin sequences.

**Definition 1 (expected time; Gill 1977).** A language $L$ is in $\mathsf{ZPP}$ if there are a probabilistic machine $M$ and a polynomial $T$ such that for every input $x$:

- every halting computation of $M$ on $x$ gives the right answer $L(x)$, and
- the expected running time of $M$ on $x$ is at most $T(|x|)$, where the expectation is over the coins of $M$.

The machine halts with probability $1$, because its expected time is finite. The expectation is over the coins for each fixed input. An algorithm that is deterministic and fast on average over random inputs, but slow on some input, does not satisfy this definition.

**Definition 2 (a "don't know" answer).** A language $L$ is in $\mathsf{ZPP}$ if there is a probabilistic machine $M$ with worst-case polynomial running time and three outputs $1$, $0$ and $?$, such that for every $x$: $M$ never outputs the wrong answer $1 - L(x)$, and $\Pr[M(x) = ?] \le 1/2$.

**Definition 3.** $\mathsf{ZPP} = \mathsf{RP} \cap \mathsf{coRP}$, where [coRP](/co-rp/) is the class of complements of RP languages.

**Theorem.** The three definitions give the same class.

*Proof.* From Definition 1 to Definition 2: run $M$ for $2T(n)$ steps. If it halts, give its answer, which is right. If not, output $?$. Let $\tau$ be the running time. By [Markov's inequality](/markov-inequality/), $\Pr[\tau > 2T(n)] \le \mathbb{E}[\tau]/(2T(n)) \le 1/2$.

From Definition 2 to Definition 1: run $M$ with fresh coins until the output is not $?$. Each round ends the loop with probability at least $1/2$, so the number of rounds is at most a geometric random variable with mean $2$. The expected time is at most twice the time of one round, and the final answer is right.

From Definition 2 to Definition 3: the machine that accepts when $M$ outputs $1$ and rejects otherwise never accepts a no-instance and accepts a yes-instance with probability at least $1/2$, so $L \in \mathsf{RP}$. The machine that rejects when $M$ outputs $0$ and accepts otherwise shows $L \in \mathsf{coRP}$ in the same way.

From Definition 3 to Definition 2: let $A$ be an RP machine and $B$ a coRP machine for $L$. Run both. If $A$ accepts, output $1$; this is right, because $A$ never accepts a no-instance. Else, if $B$ rejects, output $0$; this is right, because $B$ never rejects a yes-instance. Else output $?$. On a yes-instance the output is $?$ only if $A$ rejects, which has probability at most $1/2$. On a no-instance it is $?$ only if $B$ accepts, which also has probability at most $1/2$. $\square$

**Tail of the running time.** If each round of the loop ends it with probability exactly $1/2$, the number of rounds $X$ has $\Pr[X \ge k] = 2^{-(k-1)}$. So the mean is $2$, $\Pr[X \ge 4] = 1/8$ and $\Pr[X \ge 21] < 10^{-6}$. Markov's inequality alone gives only $\Pr[X \ge 4] \le 1/2$. So for an algorithm that works in independent rounds, the tail of the running time falls exponentially.

**Basic properties.**

- $\mathsf{P} \subseteq \mathsf{ZPP} \subseteq \mathsf{RP} \subseteq \mathsf{NP}$, and in the same way $\mathsf{ZPP} \subseteq \mathsf{coRP} \subseteq \mathsf{coNP}$. So $\mathsf{ZPP} \subseteq \mathsf{NP} \cap \mathsf{coNP}$.
- ZPP is closed under complement (swap the answers), union and intersection.
- If $\mathsf{P} = \mathsf{BPP}$, then $\mathsf{P} = \mathsf{ZPP}$, because $\mathsf{ZPP} \subseteq \mathsf{BPP}$. Whether $\mathsf{P} = \mathsf{ZPP}$ is open.

## Examples and non-examples

**Examples.**

- *Every problem in P*, with a machine that ignores its coins.
- *Primality.* The [Miller-Rabin test](/miller-rabin-primality-test/) puts PRIMES in coRP: it can wrongly say "prime" but never wrongly says "composite". Adleman and Huang (1992) gave a random polynomial-time algorithm that proves primality and never wrongly says "prime", which puts PRIMES in RP. So PRIMES was in $\mathsf{RP} \cap \mathsf{coRP} = \mathsf{ZPP}$ ten years before the [AKS test](/aks-primality-test/) put it in P. The Las Vegas algorithm runs both tests until one of them gives a certain answer.
- *[Randomized quicksort](/randomized-quicksort/).* It always sorts correctly, and its expected number of comparisons is $O(n \log n)$ on every input. Sorting is not a decision problem, but the algorithm has exactly the form of Definition 1 and is the standard example of a Las Vegas algorithm.

**Non-examples.**

- *Monte Carlo tests.* The Miller-Rabin test alone is not a ZPP algorithm, because it can be wrong. To turn a Monte Carlo test into a Las Vegas one, a test with error on the other side is also needed.
- *Polynomial identity testing.* The [Schwartz-Zippel](/schwartz-zippel-lemma/) test puts the language of zero polynomials in coRP, but no RP algorithm for it is known, so it is not known to be in ZPP.
- *Average-case fast algorithms.* Deterministic [quicksort](/quicksort/) with the first element as pivot takes $O(n \log n)$ comparisons on average over random inputs, but $\Theta(n^2)$ on a sorted input. Its expected time is over inputs, not over coins, so it does not fit Definition 1.
- *Unbounded expected time.* A machine that stops with probability $1$ but whose expected running time is not polynomial does not show membership. An example is a loop that ends in each round with probability $2^{-n}$: its expected number of rounds is $2^n$.

## Related definitions

- [RP](/rp/) and [coRP](/co-rp/): one-sided error in worst-case polynomial time.
- [BPP](/bpp/): two-sided error. $\mathsf{ZPP} \subseteq \mathsf{RP} \subseteq \mathsf{BPP}$.
- [Las Vegas algorithm](/las-vegas-algorithm/) and [Monte Carlo algorithm](/monte-carlo-algorithm/): the algorithm-level names for zero error with random time and bounded error with fixed time.

## References
