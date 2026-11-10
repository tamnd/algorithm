---
tag: VHQVGW
kind: definition
slug: small-bias-sample-space
name: Small-bias sample space
aliases:
- epsilon-biased sample space
- epsilon-biased space
- epsilon-biased distribution
- small-bias distribution
area: randomized/derandomization
level: advanced
summary: A distribution over bit strings whose every nonempty parity (XOR of a subset of bits) has bias at most epsilon.
prereqs: [k-wise-independence, fourier-analysis-of-boolean-functions, linear-code]
see_also: [small-bias-generator, sample-space-reduction, limited-independence, hadamard-code, walsh-hadamard-transform, total-variation-distance, pseudorandom-generator, expander-walk-sampler]
sources:
  - paper: doi:10.1137/0222053
    title: Joseph Naor and Moni Naor, Small-bias probability spaces, efficient constructions and applications, SIAM Journal on Computing 22(4), 1993 (STOC 1990)
    locator: pages 838 to 856 (the definition of epsilon-biased spaces, the first construction and the application to almost k-wise independence)
  - paper: doi:10.1002/rsa.3240030308
    title: Noga Alon, Oded Goldreich, Johan Håstad and René Peralta, Simple constructions of almost k-wise independent random variables, Random Structures and Algorithms 3(3), 1992
    locator: pages 289 to 304 (the powering, LFSR and quadratic character constructions, and the link between bias and almost k-wise independence)
  - paper: doi:10.1145/3055399.3055408
    title: Amnon Ta-Shma, Explicit, almost optimal, epsilon-balanced codes, STOC 2017
    locator: pages 238 to 251 (epsilon-biased spaces of size n over epsilon to the power 2 + o(1))
---

A **small-bias sample space** is a distribution on $\{0,1\}^n$ in which the XOR of every nonempty set of coordinates is almost unbiased: 0 and 1 have probabilities within $\varepsilon$ of each other. Naor and Naor (1990) defined these spaces and built them with $O(\log n + \log(1/\varepsilon))$ random bits, and Alon, Goldreich, Håstad and Peralta (1992) gave simple algebraic constructions of size about $(n/\varepsilon)^2$. Small bias implies that every $k$ coordinates are close to uniform, which makes small-bias spaces the standard source of almost $k$-wise independent bits when $k$ is not a constant. An $\varepsilon$-biased space of size $N$ is the same object as a linear code of length $N$ in which every nonzero codeword has relative weight between $(1 - \varepsilon)/2$ and $(1 + \varepsilon)/2$.

## Definition

Notation. $X = (X_1, \ldots, X_n)$ is a random string in $\{0,1\}^n$. For $a \in \{0,1\}^n$, $\langle a, X \rangle = \bigoplus_{i : a_i = 1} X_i$ is the parity of the coordinates in the set $\{i : a_i = 1\}$. $\Pr$ and $\mathrm{E}$ are over $X$, and $U_n$ is the uniform distribution on $\{0,1\}^n$.

**Definition.** The *bias* of $X$ on the test $a \ne 0$ is

$$\mathrm{bias}_a(X) = \big| \Pr[\langle a, X \rangle = 0] - \Pr[\langle a, X \rangle = 1] \big| = \big| \mathrm{E}\big[(-1)^{\langle a, X \rangle}\big] \big|.$$

$X$ is *$\varepsilon$-biased* if $\mathrm{bias}_a(X) \le \varepsilon$ for every nonzero $a \in \{0,1\}^n$. A multiset $\Omega \subseteq \{0,1\}^n$ is an *$\varepsilon$-biased sample space* if a uniform random element of $\Omega$ is $\varepsilon$-biased. It costs $\log_2 |\Omega|$ random bits to pick a point.

Some authors measure the bias as $|\Pr[\langle a, X \rangle = 1] - 1/2|$, which is half of the value above. This page uses the definition above, as Naor and Naor and AGHP do.

The uniform distribution $U_n$ is 0-biased, and by the XOR lemma below it is the only 0-biased distribution. The quantity $\mathrm{E}[(-1)^{\langle a, X \rangle}]$ is, up to the factor $2^n$, the [Walsh-Hadamard transform](/walsh-hadamard-transform/) of the probability function of $X$ at $a$. So $\varepsilon$-bias says that every nonzero Fourier coefficient of the distribution is small.

### Small bias gives almost k-wise independence

**Lemma (XOR lemma, in the form of Vazirani and of AGHP).** Let $X$ be $\varepsilon$-biased and let $I$ be a set of $k$ coordinates. The restriction $X_I$ satisfies

$$\big| \Pr[X_I = z] - 2^{-k} \big| \le \varepsilon \quad \text{for every } z \in \{0,1\}^k, \qquad \Delta(X_I, U_k) \le \frac{\varepsilon}{2} \sqrt{2^k - 1},$$

where $\Delta$ is the [total variation distance](/total-variation-distance/).

*Proof.* Let $D(z) = \Pr[X_I = z]$ and $b_S = \mathrm{E}[(-1)^{\langle S, X_I \rangle}]$ for $S \subseteq I$, so $b_\emptyset = 1$ and $|b_S| \le \varepsilon$ otherwise, since a parity over $S \subseteq I$ is a parity of $X$. Fourier inversion on $\{0,1\}^k$ gives

$$D(z) - 2^{-k} = 2^{-k} \sum_{S \ne \emptyset} b_S (-1)^{\langle S, z \rangle}.$$

The first bound follows from $|b_S| \le \varepsilon$ and the $2^k - 1$ terms. For the second, Parseval gives $\sum_z (D(z) - 2^{-k})^2 = 2^{-k} \sum_{S \ne \emptyset} b_S^2$, and Cauchy-Schwarz over the $2^k$ points gives

$$\Delta(X_I, U_k) = \frac{1}{2} \sum_z |D(z) - 2^{-k}| \le \frac{1}{2} \sqrt{2^k \sum_z (D(z) - 2^{-k})^2} = \frac{1}{2} \sqrt{\sum_{S \ne \emptyset} b_S^2} \le \frac{\varepsilon}{2} \sqrt{2^k - 1}. \quad \square$$

So an $\varepsilon 2^{-k/2}$-biased space is $\varepsilon$-close to [k-wise independent](/k-wise-independence/) in statistical distance on every $k$ coordinates. Naor and Naor and AGHP use this, together with a linear map that keeps $k$-wise independence, to get $\varepsilon$-almost $k$-wise independent spaces with $O(k + \log \log n + \log(1/\varepsilon))$ random bits. For $\varepsilon = 0$ the lemma is the exact statement: bits are $k$-wise independent and uniform if and only if every parity of between 1 and $k$ of them is unbiased.

### The equivalence with balanced codes

Write the $N$ points of $\Omega$ as the rows of an $N \times n$ matrix $M$. For $a \ne 0$, the vector $c_a = M a$ over $\mathrm{GF}(2)$ lists the test $\langle a, \omega \rangle$ for every point $\omega$, and

$$\mathrm{bias}_a = \left| 1 - \frac{2\,\mathrm{wt}(c_a)}{N} \right|,$$

where $\mathrm{wt}$ is the number of ones. So $\Omega$ is $\varepsilon$-biased if and only if every nonzero codeword of the [linear code](/linear-code/) $\{M a\}$ has weight between $(1 - \varepsilon) N/2$ and $(1 + \varepsilon) N/2$, an *$\varepsilon$-balanced code* of length $N$ and dimension $n$ (the dimension is $n$ because no nonzero $a$ gives $c_a = 0$ when $\varepsilon < 1$). The [Hadamard code](/hadamard-code/) is the 0-balanced case, with $N = 2^n$.

### Size

A random multiset of $N = O(n/\varepsilon^2)$ points of $\{0,1\}^n$ is $\varepsilon$-biased with high probability: each of the $2^n - 1$ tests has bias above $\varepsilon$ with probability $e^{-\Omega(\varepsilon^2 N)}$ by the [Chernoff bound](/chernoff-bound/), and the [union bound](/union-bound/) covers all tests. Lower bounds from coding theory show that, for $\varepsilon$ not too small, every $\varepsilon$-biased space has $\Omega(n/(\varepsilon^2 \log(1/\varepsilon)))$ points. So the optimal seed length is $\log_2 n + 2\log_2(1/\varepsilon)$ up to lower order terms.

Explicit constructions:

| construction | size of the space | seed length |
|---|---|---|
| Naor and Naor (1990) | $n \cdot \mathrm{poly}(1/\varepsilon)$ | $O(\log n + \log(1/\varepsilon))$ |
| AGHP powering, LFSR, quadratic characters (1992) | about $(n/\varepsilon)^2$ | $2 \log_2(n/\varepsilon) + O(1)$ |
| Ta-Shma (2017) | $n/\varepsilon^{2 + o(1)}$ | $\log_2 n + (2 + o(1)) \log_2(1/\varepsilon)$ |

The powering construction and the proof of its bias are on the page [small-bias generator](/small-bias-generator/).

## Examples and non-examples

- **The uniform distribution** on $\{0,1\}^n$ is 0-biased, with $2^n$ points.
- **The powering space with $m = 3$, $n = 4$.** The seed is $(x, y) \in \mathrm{GF}(8)^2$ and bit $i$ is $\langle x^i, y \rangle$ for $i = 0, \ldots, 3$. The 64 points have bias at most $(n - 1)/2^m = 3/8$ on every nonzero test, and some test reaches $3/8$. For larger $n$ the space has far fewer than $2^n$ points: with $m = 17$ and $n = 1000$ the bias is at most $999/2^{17} < 0.01$, and the seed has 34 bits.
- **A $k$-wise independent space is not small-biased in general.** In the Hadamard pairwise space $X_a = \langle a, y \rangle$, the parity $X_a \oplus X_{a'} \oplus X_{a \oplus a'}$ is always 0, so its bias is 1. A $k$-wise independent space has bias 0 on tests of weight at most $k$ but can have bias 1 on heavier tests.
- **A small-bias space is not $k$-wise independent in general.** Tests of small weight have bias up to $\varepsilon$, not 0.
- **A distribution on few strings.** If $X$ is uniform on $N$ distinct strings, Parseval gives $\sum_{a} \mathrm{bias}_a^2 = 2^n \sum_x \Pr[X = x]^2 = 2^n/N$. The test $a = 0$ contributes 1, so some nonzero test has bias at least $\sqrt{(2^n/N - 1)/(2^n - 1)}$, close to $1/\sqrt{N}$ when $N$ is much smaller than $2^n$. So an $\varepsilon$-biased space has at least about $1/\varepsilon^2$ points, whatever $n$ is.

## Related definitions

- [Small-bias generator](/small-bias-generator/): the function from a short seed to the points of an $\varepsilon$-biased space.
- [k-wise independence](/k-wise-independence/): exact independence for every $k$ coordinates; small bias gives an approximate version for all $k$ at once.
- **$\varepsilon$-biased spaces over larger alphabets.** The same definition with the characters of $\mathbb{Z}_p^n$ or $\mathbb{F}_q^n$ in place of parities.
- **Linear tests and [pseudorandom generators](/pseudorandom-generator/).** An $\varepsilon$-biased space is a pseudorandom generator against the class of linear functions over $\mathrm{GF}(2)$ (parity tests).
- [Expander walks](/expander-walk-sampler/): Ta-Shma's construction and earlier ones reduce the bias of a space by walks on expanders.

## References
