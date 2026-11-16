---
tag: RSPZBR
kind: problem
slug: gap-hamming-distance
name: Gap Hamming distance problem
aliases:
- GHD
area: complexity/communication-and-query-complexity
level: research
summary: "Alice and Bob hold n-bit strings and decide if their Hamming distance is at least n/2 + sqrt n or at most n/2 - sqrt n. It costs Theta(n) bits, even two-way with public coins."
prereqs: [randomized-communication-complexity, hamming-distance, index-problem]
see_also: [index-problem, corruption-bound, frequency-moment-lower-bounds, distinct-elements-problem, streaming-model, round-elimination, one-way-communication-complexity, hamming-distance]
sources:
  - paper: "Piotr Indyk and David Woodruff, Tight lower bounds for the distinct elements problem, Proceedings of the 44th IEEE Symposium on Foundations of Computer Science (FOCS 2003)"
    locator: the problem and its use for the Omega(1/epsilon^2) space bound for approximate distinct elements
  - paper: "T. S. Jayram, Ravi Kumar and D. Sivakumar, The one-way communication complexity of Hamming distance, Theory of Computing 4 (2008)"
    locator: the reduction from index that gives the one-way Omega(n) bound
  - paper: "Amit Chakrabarti and Oded Regev, An optimal lower bound on the communication complexity of gap-Hamming-distance, SIAM Journal on Computing 41(5) (2012)"
    locator: the two-way randomized Omega(n) bound; conference version STOC 2011
  - paper: "Alexander A. Sherstov, The communication complexity of gap Hamming distance, Theory of Computing 8 (2012)"
    locator: a short proof of the two-way bound by the corruption bound and a concentration inequality of Talagrand
  - paper: "Thomas Vidick, A concentration inequality for the overlap of a vector on a large set, with application to the communication complexity of the Gap-Hamming-Distance problem, Chicago Journal of Theoretical Computer Science (2012)"
    locator: a second simplified proof of the two-way bound
  - paper: doi:10.1561/0400000076
    title: "Tim Roughgarden, Communication Complexity (for Algorithm Designers), Foundations and Trends in Theoretical Computer Science 11(3-4), 2016"
    locator: Lecture 2, the one-way bound for gap Hamming by reduction from index and its use for streaming
---

In the gap Hamming distance problem $\mathrm{GHD}_n$, Alice and Bob hold strings $x, y \in \{0,1\}^n$ and are promised that the [Hamming distance](/hamming-distance/) $\Delta(x, y)$ is either at least $n/2 + \sqrt{n}$ or at most $n/2 - \sqrt{n}$; they must say which. Random sampling solves it with $O(n)$ bits, and Chakrabarti and Regev (2011) proved that $\Omega(n)$ bits are needed even by two-way protocols with public coins. The one-way form came first and is the main tool for $\Omega(1/\varepsilon^2)$ space bounds for $(1 \pm \varepsilon)$ approximations in [streaming](/streaming-model/), for example for [distinct elements](/distinct-elements-problem/).

## In plain words

Alice and Bob each hold a long row of bits. They are told that the rows either differ in a little more than half the places or in a little less than half the places, and they must find out which.

Random rows differ in about half the places, with an error of about the square root of the length. The gap in the question is of that same size. So a short look at a few random places does not help: the players must look at a fixed fraction of all the places, and the talk is long.

## Definition

Let $\Delta(x, y) = |\{ j : x_j \ne y_j \}|$. The partial function is

$$\mathrm{GHD}_n(x, y) = \begin{cases} 1 & \text{if } \Delta(x, y) \ge n/2 + \sqrt{n}, \\ 0 & \text{if } \Delta(x, y) \le n/2 - \sqrt{n}, \end{cases}$$

and it is not defined for other pairs. A protocol may give any output on those pairs.

**Instance:** strings $x \in \{0,1\}^n$, known only to Alice, and $y \in \{0,1\}^n$, known only to Bob, with $|\Delta(x, y) - n/2| \ge \sqrt{n}$.

**Question:** is $\Delta(x, y) \ge n/2 + \sqrt{n}$?

In $\pm 1$ form, with $u_j = (-1)^{x_j}$ and $v_j = (-1)^{y_j}$, the inner product is $\langle u, v \rangle = n - 2\Delta(x, y)$. So the question is whether $\langle u, v \rangle \le -2\sqrt{n}$ or $\langle u, v \rangle \ge 2\sqrt{n}$.

## Variants

- **Other gaps.** For a gap $g$ with $\sqrt{n} \le g \le n$, decide whether $\Delta \ge n/2 + g$ or $\Delta \le n/2 - g$. The cost is $\Theta(\min(n, n^2/g^2))$. The upper bound is sampling with $O(n^2/g^2)$ coordinates. For the lower bound, take an instance of $\mathrm{GHD}_m$ with $m = n^2/g^2$ and repeat each coordinate $n/m$ times: the distance scales by $n/m$, so the gap $\sqrt{m}$ becomes $(n/m)\sqrt{m} = g$.
- **Threshold other than $n/2$.** A gap around another threshold $t$ reduces to this form by padding the strings with fixed bits.
- **One-way and $k$-round.** The same problem with restricted interaction. The one-way form is the one used for one-pass streaming.
- **Real vectors.** Decide the sign of $\langle u, v \rangle$ for unit vectors under a promise that it is far from 0. This is the form used for sketches of inner products and angles.

## Examples

**A run of the reduction from index.** See the section Reductions. The key number is the bias $\varepsilon_n$ in $\Pr[\operatorname{sign}(\langle x, r \rangle) = x_i r_i] = \tfrac12 + \varepsilon_n$ for uniform $r \in \{\pm 1\}^n$ and odd $n$. By symmetry it equals $\Pr[\operatorname{sign}(r_1 + \cdots + r_n) = r_1]$, and a count gives $\varepsilon_n = \binom{n-1}{(n-1)/2} / 2^n$. A brute-force check over all $r$ agrees with this formula.

| $n$ | $\tfrac12 + \varepsilon_n$ | $\tfrac12 + 1/\sqrt{2\pi n}$ |
|---|---|---|
| 3 | $3/4 = 0.75$ | 0.7303 |
| 5 | $11/16 = 0.6875$ | 0.6784 |
| 11 | $319/512 \approx 0.62305$ | 0.62029 |
| 101 | 0.53979 | 0.53970 |
| 1001 | 0.51261 | 0.51261 |

So the bias is about $1/\sqrt{2\pi n}$, of the same order as the gap in $\mathrm{GHD}$.

**Sampling needs a constant fraction.** With public coins, the players pick $k$ coordinates uniformly with replacement, Alice sends her $k$ bits, and Bob says "far" if more than $k/2$ of the sampled pairs differ. The table gives the exact error on inputs at distance exactly $n/2 + \sqrt{n}$ ("far") and $n/2 - \sqrt{n}$ ("near").

| $n$ | $k$ | error on far | error on near |
|---|---|---|---|
| 64 | 8 | 0.3486 | 0.1374 |
| 64 | 16 | 0.2171 | 0.0999 |
| 64 | 32 | 0.1019 | 0.0520 |
| 64 | 64 | 0.0278 | 0.0152 |
| 64 | 128 | 0.0026 | 0.0015 |
| 1024 | 256 | 0.1737 | 0.1436 |
| 1024 | 1024 | 0.0244 | 0.0210 |
| 4096 | 1024 | 0.1662 | 0.1511 |

With $k = n/4$ the error stays near $0.15$ to $0.17$ as $n$ grows from 1024 to 4096. So a fixed error needs $k$ proportional to $n$, which matches the lower bound.

## Known algorithms

- **Sampling.** The protocol above with $k = Cn$ for a suitable constant $C$ has error at most $1/3$ by a [Chernoff bound](/chernoff-bound/). It is one-way and public-coin, and in fact a public-coin simultaneous protocol, since Bob can also send his sampled bits to a referee. Cost $O(n)$.
- **Sending $x$.** Deterministic, one-way, $n$ bits.
- **Sketches.** With public coins, random projections such as the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) or [SimHash](/simhash/) estimate $\langle u, v \rangle$ to additive error $\varepsilon n$ with $O(1/\varepsilon^2)$ numbers. For the gap $\sqrt{n}$ this is again $O(n)$.

## Bounds

| Measure | Cost of $\mathrm{GHD}_n$ | Method and source |
|---|---|---|
| upper bound, all models below | $O(n)$ | sampling, public coins; sending $x$ deterministically |
| one-way randomized, public coins | $\Theta(n)$ | reduction from [index](/index-problem/): Indyk and Woodruff (2003); the simple reduction of Jayram, Kumar and Sivakumar (2008) |
| $k$ rounds, constant $k$ | $\Theta(n)$ | [round elimination](/round-elimination/): Brody and Chakrabarti (2009), then Brody, Chakrabarti, Regev, Vidick and de Wolf (2010) |
| two-way randomized, public coins | $\Theta(n)$ | Chakrabarti and Regev (2011) by a rectangle bound with a new anti-concentration result; Vidick (2012); Sherstov (2012) by the [corruption bound](/corruption-bound/) with Talagrand's inequality |
| deterministic two-way | $\Theta(n)$ | follows from the randomized bound |

The two-way proofs do not use the plain [discrepancy method](/discrepancy-method/). They show that every large rectangle holds a constant fraction of inputs of the other answer, which is the form of the corruption bound.

## Reductions

**Index to gap Hamming (Jayram, Kumar and Sivakumar).** Let $n$ be odd and write Alice's index string as $x \in \{\pm 1\}^n$ and Bob's index as $i$. With public coins, take $N$ independent uniform $r^1, \ldots, r^N \in \{\pm 1\}^n$. Alice sets $a_j = \operatorname{sign}(\langle x, r^j \rangle)$ and Bob sets $b_j = r^j_i$. By the bias computed above, $\Pr[a_j = b_j] = \tfrac12 + \varepsilon_n$ when $x_i = +1$ and $\tfrac12 - \varepsilon_n$ when $x_i = -1$, independently for each $j$. So the expected distance between $a$ and $b$ is $N/2 \mp \varepsilon_n N$, with fluctuations of order $\sqrt{N}$. With $\varepsilon_n \approx 1/\sqrt{2\pi n}$ and $N = Cn$ for a large constant $C$, the gap $\varepsilon_n N$ is a large multiple of $\sqrt{N}$, so the promise holds with high constant probability. A one-way protocol for $\mathrm{GHD}_N$ then answers $x_i$, and the one-way bound $\Omega(n)$ for index gives $\Omega(N)$ for gap Hamming.

**Gap Hamming to distinct elements.** Alice puts the items $(j, x_j)$ into a stream and Bob adds $(j, y_j)$. The number of distinct items is $n + \Delta(x, y)$. With $n = \Theta(1/\varepsilon^2)$, a $(1 \pm \varepsilon/3)$ approximation of this number tells the two cases apart, since the two cases differ by $2\sqrt{n} = \Theta(\varepsilon n)$. A one-pass algorithm with $s$ bits of memory gives a one-way protocol with $s$ bits, so $s = \Omega(1/\varepsilon^2)$. A $p$-pass algorithm gives a two-way protocol, and the two-way bound gives $s = \Omega(1/(\varepsilon^2 p))$.

**Gap Hamming to frequency moments.** The same encoding with signs gives $\Omega(1/\varepsilon^2)$ bounds for $(1 \pm \varepsilon)$ approximations of the second moment and of other frequency moments. See [frequency moment lower bounds](/frequency-moment-lower-bounds/).

## Applications

- **Streaming space bounds.** The $\Omega(1/\varepsilon^2)$ terms in the space of [HyperLogLog](/hyperloglog/) and the [AMS sketch](/ams-sketch/) are needed, by the reductions above. The two-way bound extends them to algorithms that make a few passes.
- **Sketches of distance and similarity.** A sketch that estimates the Hamming distance of two $n$-bit strings to additive error $\varepsilon n$, with $n = \Theta(1/\varepsilon^2)$, solves gap Hamming. So it needs $\Omega(1/\varepsilon^2)$ bits, and random projections and [locality-sensitive hashing](/locality-sensitive-hashing/) sketches of this size are optimal up to constants in this measure.

## References
