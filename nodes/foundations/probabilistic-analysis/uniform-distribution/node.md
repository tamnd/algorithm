---
tag: 1TSW7X
kind: definition
slug: uniform-distribution
name: Uniform distribution
aliases:
- discrete uniform distribution
area: foundations/probabilistic-analysis
level: intro
summary: Every outcome of a finite set is equally likely; the model behind random choices and random permutations.
prereqs: [probability-space, discrete-probability-distribution, random-variable]
see_also: [random-permutation, fisher-yates-shuffle, uniform-random-integer-generation, rejection-sampling, permute-by-sorting, simple-uniform-hashing, uniform-hashing-assumption, independent-random-variables]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2, Probability (the uniform probability distribution on a finite sample space); Chapter 5, Section 5.3, Randomized algorithms (uniform random permutations and the in-place shuffle)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 8.2, The Uniform Distribution (the continuous case and its properties)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.2, Random Sampling and Shuffling (Algorithm P)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter I, The Sample Space, and Chapter II, Elements of Combinatorial Analysis (equally likely outcomes)
---

The uniform distribution on a finite nonempty set gives each element of the set the same probability, one over the size of the set. It is the model of "pick one at random" in the analysis of [randomized algorithms](/randomized-algorithm/): a random pivot, a random hash value, a [random permutation](/random-permutation/) of the input. Under it, probability is counting: the probability of an event is the number of its outcomes divided by the number of all outcomes. The continuous uniform distribution on an interval is the analogue for real numbers.

## Definition

**Discrete uniform distribution.** Let $S$ be a finite nonempty set. A [random variable](/random-variable/) $X$ with values in $S$ is uniform on $S$ when
$$ \Pr[X = s] = \frac{1}{|S|} \quad \text{for each } s \in S. $$
Then for each set $A \subseteq S$,
$$ \Pr[X \in A] = \frac{|A|}{|S|}. $$
A [probability space](/probability-space/) with a finite sample space $S$ is uniform when each elementary event has probability $1/|S|$.

**Uniform on $\{1, \ldots, n\}$.** For $n \ge 1$,
$$ \mathrm{E}[X] = \frac{n+1}{2}, \qquad \mathrm{Var}[X] = \frac{n^2 - 1}{12}. $$
*Derivation.* $\mathrm{E}[X] = \frac1n \sum_{i=1}^{n} i = \frac1n \cdot \frac{n(n+1)}{2} = \frac{n+1}{2}$. Also $\mathrm{E}[X^2] = \frac1n \sum_{i=1}^{n} i^2 = \frac{(n+1)(2n+1)}{6}$. So
$$ \mathrm{Var}[X] = \mathrm{E}[X^2] - \mathrm{E}[X]^2 = \frac{(n+1)(2n+1)}{6} - \frac{(n+1)^2}{4} = \frac{(n+1)\big(2(2n+1) - 3(n+1)\big)}{12} = \frac{(n+1)(n-1)}{12}. $$
A uniform variable on the integers $\{a, \ldots, b\}$ is $a - 1 + X$ with $n = b - a + 1$, so its mean is $(a+b)/2$ and its variance is $((b - a + 1)^2 - 1)/12$. For a fair die, $n = 6$, the mean is $3.5$ and the variance is $35/12 = 2.9167$.

**Continuous uniform distribution.** For real numbers $a < b$, a random variable $U$ is uniform on $[a, b]$ when it has the [density](/probability-density-function/) $f(x) = 1/(b - a)$ for $a \le x \le b$ and $f(x) = 0$ elsewhere. Then $\Pr[U \in [c, d]] = (d - c)/(b - a)$ for $a \le c \le d \le b$, and each single point has probability 0. Its mean is $\int_a^b \frac{x}{b-a}\,dx = \frac{a+b}{2}$. Its second moment is $\int_a^b \frac{x^2}{b-a}\,dx = \frac{a^2 + ab + b^2}{3}$, so its variance is $\frac{a^2 + ab + b^2}{3} - \frac{(a+b)^2}{4} = \frac{(b-a)^2}{12}$.

**Three facts used in algorithms.** Let $X$ be uniform on a finite set $S$.

1. *Bijections keep uniformity.* If $g : S \to T$ is a bijection, then $g(X)$ is uniform on $T$, since $\Pr[g(X) = t] = \Pr[X = g^{-1}(t)] = 1/|S| = 1/|T|$.
2. *Conditioning keeps uniformity.* For a nonempty $B \subseteq S$ and $s \in B$, $\Pr[X = s \mid X \in B] = \frac{1/|S|}{|B|/|S|} = \frac{1}{|B|}$. So $X$ given $X \in B$ is uniform on $B$. This is why [rejection sampling](/rejection-sampling/) works: draw uniformly from a larger set, and redraw until the value lies in $B$.
3. *Products.* A pair $(X, Y)$ is uniform on $S \times T$ if and only if $X$ is uniform on $S$, $Y$ is uniform on $T$, and $X$ and $Y$ are [independent](/independent-random-variables/). Indeed $\Pr[X = s, Y = t] = \frac{1}{|S||T|} = \frac{1}{|S|} \cdot \frac{1}{|T|}$ in both directions. So $k$ independent fair bits are the same as a uniform value in $\{0, \ldots, 2^k - 1\}$.

## Examples and non-examples

**Examples.**

- *A fair die and a fair coin.* Uniform on $\{1, \ldots, 6\}$ and on $\{\text{heads}, \text{tails}\}$.
- *A uniform random permutation.* The uniform distribution on the $n!$ permutations of $\{1, \ldots, n\}$. Each element lands in each position with probability $(n-1)!/n! = 1/n$, and each fixed set of $k$ positions receives each ordered $k$-tuple of distinct elements with probability $(n-k)!/n!$. The analysis of the [hiring problem](/hiring-problem/) and of [randomized quicksort](/randomized-quicksort/) runs over this distribution.
- *The Fisher-Yates shuffle.* The [Fisher-Yates shuffle](/fisher-yates-shuffle/) makes a uniform permutation of $A[1..n]$: for $i = n$ down to $2$, it swaps $A[i]$ with $A[j]$ for $j$ uniform on $\{1, \ldots, i\}$. The choices $(j_n, \ldots, j_2)$ are uniform on a set of $n \cdot (n-1) \cdots 2 = n!$ sequences, by fact 3. Different sequences give different outputs: the final $A[n]$ is the item that started at position $j_n$, and later steps never touch position $n$, so the output fixes $j_n$; the same argument on $A[1..n-1]$ fixes $j_{n-1}$, and so on. So the map from choice sequences to permutations is one to one between two sets of $n!$ elements, a bijection, and by fact 1 the output is uniform. For $n = 3$, each of the 6 permutations arises from exactly 1 of the 6 choice sequences.
- *Uniform integers by rejection.* To get $X$ uniform on $\{0, \ldots, n-1\}$ from fair bits, let $k = \lceil \lg n \rceil$, read $k$ bits as a number $V$ uniform on $\{0, \ldots, 2^k - 1\}$, and accept $V$ if $V < n$, else read again. By fact 2 the accepted value is uniform. Each round accepts with probability $n/2^k > \frac12$, so the number of rounds is [geometric](/geometric-distribution/) with mean $2^k/n < 2$. For a die, $n = 6$ and $k = 3$: each round accepts with probability $\frac68$, and the mean is $\frac43$ rounds. The page [uniform random integer generation](/uniform-random-integer-generation/) gives faster methods.
- *Uniform hashing models.* The [simple uniform hashing](/simple-uniform-hashing/) assumption says that each key hashes to a slot uniform on $\{0, \ldots, m-1\}$, independently of the other keys. The [uniform hashing assumption](/uniform-hashing-assumption/) says that the probe sequence of each key is a uniform permutation of the slots.

**Non-examples.**

- *The sum of two dice.* It takes the values $2, \ldots, 12$, with $\Pr[\text{sum} = s] = (6 - |s - 7|)/36$: $\frac{1}{36}$ for 2 and 12, $\frac{6}{36}$ for 7. The pair of dice is uniform on 36 outcomes, but the sum is not uniform on its 11 values, because the map from pairs to sums is not one to one.
- *The modulo shortcut.* Reduce 3 fair bits, a value uniform on $\{0, \ldots, 7\}$, modulo 3. The residue 0 comes from $\{0, 3, 6\}$, 1 from $\{1, 4, 7\}$, and 2 from $\{2, 5\}$, so the probabilities are $\frac38, \frac38, \frac28$. In general $V \bmod n$ is uniform only when $n$ divides the number of values of $V$. The bias can be large even with 32 bits: for $n = 3 \cdot 2^{30} = 3221225472$, the $2^{32}$ values cover the residues below $2^{30}$ twice and the others once, so the result is below $2^{30}$ with probability $\frac12$, though these residues are only a third of the range.
- *The naive shuffle.* For $i = 1$ to $n$, swap $A[i]$ with $A[j]$ for $j$ uniform on all of $\{1, \ldots, n\}$. There are $n^n$ equally likely choice sequences, and each permutation arises from an integer number of them. A uniform output needs $n!$ to divide $n^n$, which fails for $n = 3$: 27 sequences cannot split evenly over 6 permutations. On $[1, 2, 3]$ the outputs $[1, 3, 2]$, $[2, 1, 3]$ and $[2, 3, 1]$ each come from 5 sequences, and the other three permutations each come from 4. For $n \ge 3$, $n - 1$ divides $n!$ but is coprime to $n^n$, so the naive shuffle is never uniform.
- *Ties in random priorities.* PERMUTE-BY-SORTING gives each item a random priority in $\{1, \ldots, n^3\}$ and sorts by priority. The output is uniform given that all priorities are distinct, but ties break this. By the [union bound](/union-bound/) over the $\binom{n}{2}$ pairs, a tie has probability at most $\binom{n}{2}/n^3 < 1/(2n)$. For $n = 10$ the bound is $0.045$, and the exact probability of a tie is $0.0441$. See [permute by sorting](/permute-by-sorting/).
- *No uniform distribution on an infinite countable set.* If each natural number had the same probability $p$, the total would be $0$ when $p = 0$ and infinite when $p > 0$, never 1. "A random integer" always needs a finite range or another distribution.
- *Scaling a floating-point number.* If $U$ is a random double in $[0, 1)$ with $2^{53}$ equally likely values, then $\lfloor nU \rfloor$ is uniform on $\{0, \ldots, n-1\}$ only when $n$ divides $2^{53}$, by the same counting as the modulo shortcut. The bias is small for small $n$, but it is not zero.

## Related definitions

- [Discrete probability distribution](/discrete-probability-distribution/): the uniform one is the case of equal weights. Among all distributions on $n$ outcomes it has the largest [Shannon entropy](/shannon-entropy/), $\lg n$ bits.
- [Bernoulli trials](/bernoulli-trials/) with success probability $\frac12$ are uniform on $\{0, 1\}$; $n$ independent ones are uniform on $\{0, 1\}^n$.
- [Random permutation](/random-permutation/): the uniform distribution on the symmetric group, and the input model of average-case analysis.
- [Random sampling](/random-sampling/) and [reservoir sampling](/reservoir-sampling/): uniform distributions on the subsets of a fixed size $k$, each with probability $1/\binom{n}{k}$.
- [Inverse transform sampling](/inverse-transform-sampling/): turns a continuous uniform variable on $[0, 1]$ into a variable with any given distribution function.
- [Independent random variables](/independent-random-variables/): fact 3 above links uniformity on a product set to independence.

## References
