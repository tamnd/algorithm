---
tag: YG1S6A
kind: theorem
slug: adleman-theorem
name: Adleman's theorem
aliases:
- BPP in P/poly
area: complexity/complexity-classes
level: advanced
summary: Every language in BPP has polynomial-size Boolean circuits. Amplify the error below 2^-n and a union bound shows that one random string is good for all inputs of length n.
prereqs: [bpp, p-poly, union-bound, error-amplification]
see_also: [bpp, rp, p-poly, karp-lipton-theorem, sipser-gacs-theorem, non-uniform-computation, impagliazzo-wigderson-theorem, boolean-circuit]
sources:
  - paper: doi:10.1109/SFCS.1978.37
    title: Leonard Adleman, Two theorems on random polynomial time, 19th Annual Symposium on Foundations of Computer Science, 75 to 83 (1978)
    locator: the theorem that random polynomial time (one-sided error) has polynomial-size circuits
  - paper: doi:10.1137/0210008
    title: Charles H. Bennett and John Gill, Relative to a random oracle A, P^A != NP^A != co-NP^A with probability 1, SIAM Journal on Computing 10(1), 96 to 113 (1981)
    locator: the two-sided form (a finite majority of random strings is correct on all inputs of a given length)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (BPP in P/poly)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 6, Randomness and counting (BPP and non-uniform circuits)
---

Adleman's theorem says that every language in [BPP](/bpp/) has Boolean circuits of polynomial size: $\mathsf{BPP} \subseteq \mathsf{P/poly}$. The proof amplifies the error of a BPP machine below $2^{-n}$ and then counts: fewer than all random strings are bad for some input of length $n$, so one string is good for every input of that length, and a circuit can contain it. Adleman proved the one-sided form, for [RP](/rp/), in 1978, and Bennett and Gill gave the two-sided form in 1981. The theorem says that randomness can be replaced by [non-uniform advice](/non-uniform-computation/), but it gives no efficient way to find the advice.

## Statement

**Theorem.** $\mathsf{BPP} \subseteq \mathsf{P/poly}$. That is, for every language $L \in \mathsf{BPP}$, decided by a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/), there are a polynomial $s$ and a family of [Boolean circuits](/boolean-circuit/) $\{C_n\}$ such that $C_n$ has size at most $s(n)$ and $C_n(x) = L(x)$ for every $x \in \{0,1\}^n$.

The same proof gives $\mathsf{RP} \subseteq \mathsf{P/poly}$ and $\mathsf{coRP} \subseteq \mathsf{P/poly}$, and a single string $r_n$ per input length as the advice.

## In plain words

Take a randomized algorithm that is right with high probability on each input. Run it many times and take the majority, so that on each input the chance of an error is smaller than one divided by the number of inputs of that size. Now look at all coin sequences together. Each input spoils only a tiny share of them, and all the spoiled shares together still do not cover everything. So at least one coin sequence is right for every input of that size. A circuit for that size can contain this sequence as fixed bits. The circuit is small, but nobody needs to know how to find the good sequence, so this does not give a fast deterministic algorithm.

## Proof

Let $L \in \mathsf{BPP}$, decided by a machine $M(x, r)$ with error at most $1/3$.

*Step 1: amplify.* By [error amplification](/error-amplification/), run $M$ for $k = O(n)$ times with independent coins and take the majority. The Chernoff-Hoeffding bound gives a machine $M'(x, r)$ with coin strings $r \in \{0,1\}^{m(n)}$, $m$ a polynomial, such that for every $x$ of length $n$:

$$\Pr_r[M'(x, r) \ne L(x)] < 2^{-n}.$$

With error $1/3$ per run, the bound $e^{-k/18} < 2^{-n}$ holds for $k > 18 n \ln 2 \approx 12.5\, n$.

*Step 2: count.* For each $x \in \{0,1\}^n$ let $B_x = \{r : M'(x, r) \ne L(x)\}$, the coin strings that are bad for $x$. Then $|B_x| < 2^{-n} \cdot 2^m$. By the [union bound](/union-bound/),

$$\Big| \bigcup_{x \in \{0,1\}^n} B_x \Big| \le \sum_x |B_x| < 2^n \cdot 2^{-n} \cdot 2^m = 2^m.$$

So some string $r_n \in \{0,1\}^m$ is in no $B_x$: $M'(x, r_n) = L(x)$ for every $x$ of length $n$.

*Step 3: build the circuit.* A deterministic machine that runs in time $T(n)$ has, for each $n$, a circuit of size $O(T(n)^2)$ that computes its output on inputs of length $n$ (the tableau construction of the [Cook-Levin theorem](/cook-levin-theorem/)). Apply this to $M'$ with inputs $x$ and $r$, and fix the $r$ inputs to the bits of $r_n$. The result is a circuit $C_n$ of polynomial size with $C_n(x) = L(x)$ for all $x \in \{0,1\}^n$. So $L \in \mathsf{P/poly}$, with $r_n$ as the advice string. $\square$

For RP, Step 1 needs only the OR of $k = n + 1$ runs, which gives error at most $2^{-(n+1)}$ on yes-instances and $0$ on no-instances.

**Example.** Take as inputs the odd numbers from $3$ to $1023$, of $10$ bits, and the test: pick a base $a$ uniformly from $\{1, \ldots, 1023\}$; if $a \bmod x \ne 0$ and $a$ is a witness of compositeness for $x$ in the [Miller-Rabin test](/miller-rabin-primality-test/), answer "composite", else answer "prime". A prime is never called composite. Among the $340$ odd composites in this range, the worst one is $x = 9$, where $340$ of the $1023$ bases make the test say "prime", an error of $0.332$. With $k$ independent bases, the union bound over the $340$ composites gives the probability that some composite is called prime as at most $340 \cdot (340/1023)^k$. This is $1.38$ for $k = 5$ and $0.458$ for $k = 6$. So some list of $6$ bases from $\{1, \ldots, 1023\}$ is correct on every input in the range, and it is advice for $10$-bit inputs. The union bound is loose here: the single base $a = 2$ already works, and it is the only single base in $\{1, \ldots, 1023\}$ that does. The first odd composite that base $2$ calls prime is $2047 = 23 \cdot 89$.

## Consequences

- *If NP is in BPP, the polynomial hierarchy collapses.* $\mathsf{NP} \subseteq \mathsf{BPP}$ gives $\mathsf{NP} \subseteq \mathsf{P/poly}$, and the [Karp-Lipton theorem](/karp-lipton-theorem/) then gives $\mathsf{PH} = \Sigma_2^p$. So NP-complete problems are believed not to have efficient randomized algorithms.
- *Circuit lower bounds and randomness.* Superpolynomial circuit lower bounds for a language prove that it is not in BPP. In the other direction, strong enough lower bounds for exponential time give $\mathsf{P} = \mathsf{BPP}$ ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/)).
- *Other classes.* The same argument gives $\mathsf{RP} \subseteq \mathsf{P/poly}$ and, with the space-bounded machine in place of the circuit, $\mathsf{BPL} \subseteq \mathsf{L/poly}$ for [randomized logspace](/randomized-logspace/). It relativizes: $\mathsf{BPP}^A \subseteq \mathsf{P}^A/\mathsf{poly}$ for every oracle $A$.
- *Random oracles.* Bennett and Gill (1981) used the same counting with a random oracle in place of advice: relative to a random oracle $A$, $\mathsf{P}^A = \mathsf{BPP}^A$ with probability $1$.

## Tightness

- *The inclusion is strict.* $\mathsf{P/poly}$ contains undecidable languages, such as the unary language $\{1^n : $ the $n$-th Turing machine halts on empty input$\}$, which needs only one advice bit per length. Every BPP language is decidable, so $\mathsf{BPP} \ne \mathsf{P/poly}$.
- *The error threshold of the counting step.* Step 1 needs error strictly below $2^{-n}$, and error equal to $2^{-n}$ is not enough for the one-string argument. Let a machine use $n$ coins and be wrong on $x$ exactly when $r = x$. Its error on each input is exactly $2^{-n}$, and every coin string is bad for exactly one input, so no single string is good for all inputs. A majority over several strings still works for such a machine, so this shows the limit of the one-string argument, not of the theorem.
- *Uniformity.* The proof shows that a good string exists but gives no polynomial-time method to find it. Whether $\mathsf{BPP} = \mathsf{P}$, the uniform version, is open.

## History

Adleman (1978) introduced the counting argument for random polynomial time with one-sided error, the class now called RP. Bennett and Gill (1981) extended it to two-sided error, so to BPP, in their paper on random oracles; they showed that a finite majority of random strings is correct on all inputs of a given length. Later texts, such as Arora and Barak, give the version above with one amplified string.

## References
