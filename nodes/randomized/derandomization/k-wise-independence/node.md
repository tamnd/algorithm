---
tag: A9E01Z
kind: definition
slug: k-wise-independence
name: k-wise independence
aliases:
- k-wise independent random variables
- k-independence
- d-wise independence
- k-wise independent sample space
area: randomized/derandomization
level: core
summary: A family of random variables in which every subset of at most k variables is mutually independent.
prereqs: [independent-random-variables, random-variable, pairwise-independence]
see_also: [limited-independence, sample-space-reduction, k-independent-hashing, small-bias-sample-space, bch-code, hadamard-code, polynomial-interpolation, vandermonde-matrix]
sources:
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 16, Section 16.2 (d-wise independent random variables in small sample spaces)
  - paper: doi:10.1016/0196-6774(86)90019-2
    title: Noga Alon, László Babai and Alon Itai, A fast and simple randomized parallel algorithm for the maximal independent set problem, Journal of Algorithms 7(4), 1986
    locator: pages 567 to 583 (the BCH sample space and the lower bound on the size of k-wise independent sample spaces)
  - paper: doi:10.1109/sfcs.1985.55
    title: Benny Chor, Oded Goldreich, Johan Håstad, Joel Friedman, Steven Rudich and Roman Smolensky, The bit extraction problem or t-resilient functions, FOCS 1985
    locator: pages 396 to 407 (the lower bound on the size of t-wise independent sample spaces)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 3, Section 3.5 (pairwise independence and k-wise independent hash functions)
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pages 1036 to 1053 (pairwise independent choices in a polynomial size sample space)
---

Random variables $X_1, \ldots, X_n$ are **$k$-wise independent** when every $k$ of them are mutually independent, although the whole family may be far from independent. The property is the weak form of independence that many probabilistic proofs need, and it can be met by sample spaces of size about $n^{\lfloor k/2 \rfloor}$, in place of the $2^n$ points of $n$ fully independent bits. A random polynomial of degree less than $k$ over a finite field gives such variables, and a lower bound of Alon, Babai and Itai (1986) and of Chor, Goldreich, Håstad, Friedman, Rudich and Smolensky (1985) shows that the size $n^{\lfloor k/2 \rfloor}$ cannot be improved by much for constant $k$.

## Definition

Notation. $\Pr$ is probability over one random point of a sample space $\Omega$. $[n] = \{1, \ldots, n\}$. $k \ge 1$ is an integer.

**Definition.** Random variables $X_1, \ldots, X_n$ on the same probability space are *$k$-wise independent* if for every set $I \subseteq [n]$ with $|I| \le k$ and all values $(x_i)_{i \in I}$,

$$\Pr\left[\bigwedge_{i \in I} X_i = x_i\right] = \prod_{i \in I} \Pr[X_i = x_i].$$

For $n \ge k$ it is enough to check the sets with $|I| = k$, since a sum over the values of the other variables gives the smaller sets. *Pairwise independence* is the case $k = 2$, see [pairwise independence](/pairwise-independence/). Full independence is the case $k = n$.

The variables are *$k$-wise independent and uniform over $D$* if, in addition, each $X_i$ is uniform on a finite set $D$. Then every $k$ of them are uniform on $D^k$. A *$k$-wise independent sample space* is a multiset $\Omega \subseteq D^n$ such that the coordinates of a uniform random point of $\Omega$ are $k$-wise independent and uniform. The number of random bits needed to pick a point is $\log_2 |\Omega|$.

**Parities.** For bits, the variables are $k$-wise independent and uniform if and only if every parity $\bigoplus_{i \in S} X_i$ with $1 \le |S| \le k$ is 0 with probability exactly $1/2$. One direction holds because the parity of uniform independent bits is uniform. For the other, the [Fourier expansion](/fourier-analysis-of-boolean-functions/) of the distribution of $(X_i)_{i \in I}$, $|I| \le k$, has a coefficient for each $S \subseteq I$ equal to the bias of the parity over $S$; if all coefficients with $S \ne \emptyset$ are 0, the distribution is uniform. Asking only for parities of bias at most $\varepsilon$ gives [small-bias sample spaces](/small-bias-sample-space/).

### The polynomial construction

Let $\mathbb{F}_q$ be a finite field with $q \ge n$ elements, and let $\alpha_1, \ldots, \alpha_n$ be distinct elements. Choose $a_0, \ldots, a_{k-1}$ independently and uniformly from $\mathbb{F}_q$, and set

$$X_i = a_0 + a_1 \alpha_i + a_2 \alpha_i^2 + \cdots + a_{k-1} \alpha_i^{k-1}, \qquad i = 1, \ldots, n.$$

**Claim.** $X_1, \ldots, X_n$ are $k$-wise independent and uniform over $\mathbb{F}_q$. The space has $q^k$ points and uses $k \log_2 q$ random bits.

*Proof.* Take distinct indices $i_1, \ldots, i_k$. The vector $(X_{i_1}, \ldots, X_{i_k})$ equals $V a$, where $a = (a_0, \ldots, a_{k-1})$ and $V$ is the $k \times k$ [Vandermonde matrix](/vandermonde-matrix/) with rows $(1, \alpha_{i_j}, \ldots, \alpha_{i_j}^{k-1})$. The points are distinct, so $\det V = \prod_{j < l} (\alpha_{i_l} - \alpha_{i_j}) \ne 0$, and $a \mapsto V a$ is a bijection of $\mathbb{F}_q^k$. So $V a$ is uniform on $\mathbb{F}_q^k$ when $a$ is, which is the claim for sets of size $k$. Smaller sets follow by summing out. In other words, a polynomial of degree less than $k$ is fixed by its values at $k$ points ([polynomial interpolation](/polynomial-interpolation/)), and each list of $k$ values comes from exactly one polynomial. $\square$

The variables are not $(k+1)$-wise independent when $n > k$: any $k$ of the values fix the polynomial and so fix every other value. For $q = 5$ and $n = 5$, the space is $k$-wise but not $(k+1)$-wise independent for $k = 2$ (25 points) and $k = 3$ (125 points). The same family, seen as a function $i \mapsto X_i$, is the standard [k-independent hash family](/k-independent-hashing/).

For bits, take $q = 2^m \ge n$ and output one fixed bit of each $X_i$. This gives $k$-wise independent uniform bits with $k m \approx k \log_2 n$ random bits. Alon, Babai and Itai (1986) gave a better space from the parity check matrix of [BCH codes](/bch-code/): for $n = 2^m - 1$ and odd $k = 2t + 1$, a space of $2(n + 1)^t$ points, so about $\lfloor k/2 \rfloor \log_2 n$ random bits.

### The lower bound

**Theorem (ABI 1986; CGHFRS 1985).** If $X_1, \ldots, X_n$ are $k$-wise independent and none of them is constant, the support of the distribution has at least

$$\sum_{i=0}^{\lfloor k/2 \rfloor} \binom{n}{i}$$

points. For constant $k$ this is $\Omega(n^{\lfloor k/2 \rfloor})$.

*Proof.* Let $\Omega$ be the support, with probability $p(\omega) > 0$ for each point, and use the inner product $\langle f, g \rangle = \mathrm{E}[f g] = \sum_{\omega} p(\omega) f(\omega) g(\omega)$ on the real functions on $\Omega$, a space of dimension $|\Omega|$. Let $Y_i = (X_i - \mathrm{E} X_i)/\sigma_i$, where $\sigma_i > 0$ is the standard deviation, so $\mathrm{E} Y_i = 0$ and $\mathrm{E} Y_i^2 = 1$. For $S \subseteq [n]$ with $|S| \le k/2$ let $Y_S = \prod_{i \in S} Y_i$, with $Y_\emptyset = 1$. For two such sets $S$ and $T$, the set $S \cup T$ has at most $k$ elements, so its variables are independent and

$$\mathrm{E}[Y_S Y_T] = \prod_{i \in S \cap T} \mathrm{E}[Y_i^2] \prod_{i \in S \triangle T} \mathrm{E}[Y_i].$$

This is 1 if $S = T$ and 0 otherwise. So the functions $Y_S$ are orthonormal, hence linearly independent, and their number is at most the dimension $|\Omega|$. $\square$

For odd $k$ a slightly larger bound holds, and the BCH space above has size within a constant factor of the bound when $k$ is a constant. So $k$-wise independent bits need about $\frac{k}{2} \log_2 n$ random bits, and no cleverer construction can do much better.

## Examples and non-examples

- **Pairwise independent bits from a few seed bits (Hadamard space).** Pick $y \in \{0,1\}^m$ uniformly and set $X_a = \langle a, y \rangle \bmod 2$ for every nonzero $a \in \{0,1\}^m$. Two distinct nonzero vectors are linearly independent over $\mathrm{GF}(2)$, so any two of the $n = 2^m - 1$ bits are uniform on $\{0,1\}^2$. The space has $2^m = n + 1$ points, equal to the lower bound $1 + n$ for $k = 2$. For $m = 3$ there are 7 bits from 3 seed bits. These are the coordinates of a random codeword of the [Hadamard code](/hadamard-code/), without the 0 coordinate.
- **The same space is not 3-wise independent.** $X_a \oplus X_{a'} \oplus X_{a \oplus a'} = 0$ always. In the $m = 3$ space, the number of ones is 0 for $y = 0$ and 4 for the other 7 seeds, far from the binomial distribution of 7 independent bits.
- **3-wise independent bits.** Use the vectors $(1, v)$ for all $v \in \{0,1\}^m$ in place of the nonzero vectors: $X_v = y_0 \oplus \langle v, y' \rangle$. Any three of these vectors are linearly independent (two sum to a vector with first coordinate 0 that is not zero, three sum to a vector with first coordinate 1). So $n = 2^m$ bits are 3-wise independent with $2n$ points. For $n = 8$ this is 16 points. Four vectors $v_1, v_2, v_3, v_1 \oplus v_2 \oplus v_3$ sum to zero, so the bits are not 4-wise independent.
- **The general linear rule.** If $y$ is uniform in $\{0,1\}^m$ and $X_i = \langle h_i, y \rangle$, the bits are $k$-wise independent and uniform exactly when every $k$ of the vectors $h_i$ are linearly independent, that is when the $h_i$ are the columns of the parity check matrix of a [linear code](/linear-code/) with minimum distance greater than $k$.
- **Pairwise but not 3-wise.** With $X, Y$ fair independent bits, the three bits $X, Y, X \oplus Y$ are pairwise independent, but the third is fixed by the first two.
- **Not even pairwise.** $n$ copies of one fair bit are 1-wise independent and uniform, but no two of them are independent.
- **Moments.** For $k$-wise independent variables, every moment of a sum of degree at most $k$ equals its value under full independence. For $n$ uniform $\pm 1$ variables that are 4-wise independent, $\mathrm{E}[S^4] = n + 3n(n-1)$, as for independent ones (40 for $n = 4$, 96 for $n = 6$). This is what makes Chebyshev and higher moment bounds work, see [limited independence](/limited-independence/).

## Related definitions

- [Pairwise independence](/pairwise-independence/): the case $k = 2$.
- [k-independent hashing](/k-independent-hashing/): a hash family where the values at any $k$ distinct keys are $k$-wise independent and uniform.
- **Almost $k$-wise independence.** Every $k$ coordinates are within statistical distance $\varepsilon$ of uniform, or within $\varepsilon$ at every point. Alon, Goldreich, Håstad and Peralta (1992) build such spaces with $O(\log \log n + k + \log(1/\varepsilon))$ random bits, from [small-bias sample spaces](/small-bias-sample-space/) and [small-bias generators](/small-bias-generator/).
- [Limited independence](/limited-independence/): the tail bounds that hold for sums of $k$-wise independent variables.
- [Sample space reduction](/sample-space-reduction/): the method that replaces random choices by a $k$-wise independent space and tries all its points.
- [Independent random variables](/independent-random-variables/): the full notion, which is $n$-wise independence.

## References
