---
tag: CTK403
kind: definition
slug: min-wise-independent-hashing
name: Min-wise independent hashing
aliases:
- min-wise independent permutations
- min-wise hash family
- minwise independence
- epsilon-min-wise independent family
area: randomized/random-hashing
level: advanced
summary: Every subset of keys has each member equally likely to hash to the minimum value; used for estimating set resemblance.
prereqs: [k-independent-hashing, jaccard-similarity, random-permutation]
see_also: [minhash, jaccard-similarity, locality-sensitive-hashing, kmv-sketch, k-independent-hashing, pairwise-independence, tabulation-hashing, prime-number-theorem]
sources:
  - paper: doi:10.1006/jcss.1999.1690
    title: Andrei Z. Broder, Moses Charikar, Alan M. Frieze and Michael Mitzenmacher, Min-wise independent permutations, Journal of Computer and System Sciences 60(3), 630 to 659, 2000
    locator: the definitions of exact and approximately min-wise independent families, the resemblance estimate, Theorem 1 (the lower bound lcm(1, ..., n) on the size of an exact family) and Theorem 2 (a family of size less than 4^n)
  - paper: doi:10.1006/jagm.2000.1131
    title: Piotr Indyk, A small approximately min-wise independent family of hash functions, Journal of Algorithms 38(1), 84 to 90, 2001
    locator: the main theorem (O(log(1/ε))-wise independent functions are ε-approximately min-wise independent)
  - paper: doi:10.1145/2716317
    title: Mihai Pătrașcu and Mikkel Thorup, On the k-independence required by linear probing and minwise independence, ACM Transactions on Algorithms 12(1), article 8, 2016
    locator: the lower bound that Ω(log(1/ε))-independence is needed for ε-approximate min-wise independence
---

A family of permutations or hash functions is min-wise independent when, for every set $X$ of keys and every $x \in X$, a random member of the family makes $x$ the element of $X$ with the least value with probability exactly $1/|X|$. Broder, Charikar, Frieze and Mitzenmacher defined the property in 1998 (journal version 2000) because it is exactly what the [MinHash](/minhash/) estimate of set resemblance needs: under such a family, two sets $A$ and $B$ have the same minimum with probability equal to their [Jaccard similarity](/jaccard-similarity/) $|A \cap B|/|A \cup B|$. They also showed that exact families must be huge, of size at least $\operatorname{lcm}(1, \ldots, n) = e^{n - o(n)}$ on a universe of $n$ keys. So practice uses $\varepsilon$-approximate families, and Indyk (2001) showed that any $O(\log(1/\varepsilon))$-wise [independent](/k-independent-hashing/) family will do, which Pătrașcu and Thorup proved is tight. Pairwise independence is not enough.

## Definition

Let $[n] = \{0, \ldots, n-1\}$ be the universe, and let $\mathcal{F}$ be a finite nonempty multiset of permutations of $[n]$, with $\pi$ drawn uniformly from $\mathcal{F}$. For $X \subseteq [n]$ write $\min \pi(X) = \min\{\pi(y) : y \in X\}$.

**Min-wise independent.** $\mathcal{F}$ is *min-wise independent* when
$$\forall X \subseteq [n],\ X \ne \emptyset,\ \forall x \in X: \qquad \Pr_\pi\big[\pi(x) = \min \pi(X)\big] = \frac{1}{|X|}.$$
The set of all $n!$ permutations has this property, by symmetry.

**Approximately min-wise independent.** For $\varepsilon \ge 0$, $\mathcal{F}$ is *$\varepsilon$-approximately min-wise independent* when
$$\left|\Pr_\pi\big[\pi(x) = \min \pi(X)\big] - \frac{1}{|X|}\right| \le \frac{\varepsilon}{|X|}$$
for all such $X$ and $x$. Some papers also restrict this to sets of size at most a given $k$.

**Hash functions instead of permutations.** For a family of functions $h : [n] \to [m]$, ties are possible. The same definitions are used with the event "$h(x) < h(y)$ for all $y \in X \setminus \{x\}$", and with $m$ large enough compared with the set sizes that ties are rare. This is the form used in practice, where $h$ is a hash function with a large range.

**Theorem (resemblance).** If $\mathcal{F}$ is min-wise independent, then for all sets $A, B \subseteq [n]$ with $A \cup B \ne \emptyset$,
$$\Pr_\pi\big[\min \pi(A) = \min \pi(B)\big] = \frac{|A \cap B|}{|A \cup B|}.$$
If $\mathcal{F}$ is $\varepsilon$-approximately min-wise independent, the probability is within $\varepsilon \cdot |A \cap B|/|A \cup B|$ of this value.

*Proof.* Let $X = A \cup B$, and let $x^*$ be the element of $X$ with the least value $\pi(x^*)$. It is unique because $\pi$ is a permutation. If $x^* \in A \cap B$, then $x^*$ attains both $\min \pi(A)$ and $\min \pi(B)$, so they are equal. If $x^* \in A \setminus B$, then $\min \pi(A) = \pi(x^*) < \pi(y)$ for each $y \in B$, so they differ, and the case $x^* \in B \setminus A$ is the same. So the minima are equal exactly when $x^* \in A \cap B$, and
$$\Pr[\min \pi(A) = \min \pi(B)] = \sum_{x \in A \cap B} \Pr[\pi(x) = \min \pi(X)] = |A \cap B| \cdot \frac{1}{|X|}.$$
In the approximate case each of the $|A \cap B|$ terms is within $\varepsilon/|X|$ of $1/|X|$. $\blacksquare$

So the indicator of "equal minima" is an unbiased estimate of the Jaccard similarity $J$. The mean of $k$ independent copies has variance $J(1 - J)/k$, which is what the [MinHash](/minhash/) signature uses.

**Theorem (Broder, Charikar, Frieze and Mitzenmacher).** Every min-wise independent family of permutations of $[n]$ has size divisible by $\operatorname{lcm}(1, 2, \ldots, n)$, so of size at least $e^{n - o(n)}$.

*Proof.* Fix $k \le n$ and a set $X$ of $k$ elements. For each $x \in X$, the number of $\pi \in \mathcal{F}$ with $\pi(x) = \min \pi(X)$ is $|\mathcal{F}|/k$, counted with multiplicity, and it is an integer. So $k$ divides $|\mathcal{F}|$ for each $k = 1, \ldots, n$, and $\operatorname{lcm}(1, \ldots, n)$ divides $|\mathcal{F}|$. Finally, $\ln \operatorname{lcm}(1, \ldots, n) = \sum_{p^j \le n} \ln p$ is the Chebyshev function $\psi(n)$, and $\psi(n) = n(1 + o(1))$ is a form of the [prime number theorem](/prime-number-theorem/). $\blacksquare$

The same paper shows that a min-wise independent family of size less than $4^n$ exists. Both bounds are exponential in $n$, so storing one exact permutation takes about $n$ bits or more, and exact families are of no practical use for large universes.

## Examples and non-examples

**All permutations, exact numbers.** Let $n = 5$, $A = \{0, 1, 2\}$ and $B = \{1, 2, 3, 4\}$. Over all $120$ permutations, the minima agree for $48$, a probability of $2/5 = |\{1, 2\}|/|\{0, 1, 2, 3, 4\}|$, as the theorem says.

**The lcm bound in numbers.** $\operatorname{lcm}(1, \ldots, n)$ for $n = 1, \ldots, 12$ is $1, 2, 6, 12, 60, 60, 420, 840, 2520, 2520, 27720, 27720$. For $n = 3$ it equals $3! = 6$, so no proper subfamily of the permutations of 3 elements is min-wise independent. For $n = 12$, the bound $27720$ is far below $12! = 479001600$, but it still grows like $e^n$.

**Non-example: linear permutations.** Over $\mathbb{Z}_p$, the $p(p-1)$ maps $x \mapsto (ax + b) \bmod p$ with $a \ne 0$ are pairwise independent as permutations: each pair of distinct keys goes to each pair of distinct values with the same probability. They are not min-wise independent. For $p = 7$ and $X = \{0, 1, 2\}$, the middle key $1$ is the minimum with probability $2/7$, not $1/3$. For $A = \{0, 1, 2\}$ and $B = \{1, 2, 3\}$, the minima agree with probability $10/21$, while $J = 1/2$. The largest relative error $|\,|X| \Pr - 1|$ over all sets and keys is $1/10$ for $p = 5$, $1/7$ for $p = 7$ and $1/5$ for $p = 11$. So pairwise independence does not give approximate min-wise independence with small $\varepsilon$.

**Positive example: k-independent hashing.** Indyk (2001) showed that a family of hash functions that is $O(\log(1/\varepsilon))$-wise independent, into a range large compared with the set size, is $\varepsilon$-approximately min-wise independent. A random polynomial of degree $O(\log(1/\varepsilon))$ over a prime field, as in [k-independent hashing](/k-independent-hashing/), is such a family, with $O(\log n \log(1/\varepsilon))$ random bits. Pătrașcu and Thorup (2016) showed that $\Omega(\log(1/\varepsilon))$-wise independence is also necessary in general.

**Practical families.** Fast hash functions are used for MinHash in practice, and their guarantees are proved family by family. For example, Dahlgaard and Thorup (2014) proved that twisted [tabulation hashing](/tabulation-hashing/) is approximately min-wise independent. A family with no such proof, such as plain multiply-shift, may still work on typical data, but it has no guarantee.

**Non-example: ties in a small range.** A hash function into a small range has ties. If ties are broken by the key, as in "least $(h(x), x)$", smaller keys win more often, so the family is not min-wise independent and the resemblance estimate can be biased. Use a range much larger than the sets, for example 64-bit hash values.

## Related definitions

- [MinHash](/minhash/). The algorithm that uses a min-wise family to sketch sets and estimate Jaccard similarity, with banding for [locality-sensitive hashing](/locality-sensitive-hashing/).
- [Jaccard similarity](/jaccard-similarity/). The quantity $|A \cap B|/|A \cup B|$ that the resemblance theorem estimates.
- [KMV sketch](/kmv-sketch/). Keeps the $k$ least hash values of a set, the bottom-$k$ form, to estimate the number of distinct elements and, with two sketches, the resemblance from one hash function.
- [k-independent hashing](/k-independent-hashing/). The source of approximately min-wise families, with $k = O(\log(1/\varepsilon))$.
- [Pairwise independence](/pairwise-independence/). Not enough for min-wise independence, as the linear permutations show.
- [Random permutation](/random-permutation/). The family of all permutations, the exact but expensive min-wise family.

## References
