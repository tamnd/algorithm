---
tag: H49EPH
kind: theorem
slug: dinur-nissim-reconstruction-attack
name: Dinur-Nissim reconstruction attack
aliases:
- fundamental law of information recovery
- database reconstruction attack
area: security-and-privacy/differential-privacy
level: core
summary: "If all 2^n subset sums of n secret bits have error o(n), or about n random ones have error o(sqrt n), almost all bits follow from the answers, so no private mechanism is that accurate."
history:
  year: 2003
  people: [Irit Dinur, Kobbi Nissim]
  note: Dinur and Nissim proved the two reconstruction theorems at PODS 2003. They came before differential privacy and were a main reason for its definition.
prereqs: [differential-privacy-definition, approximate-differential-privacy]
see_also: [packing-lower-bound, fingerprinting-codes-lower-bound, private-query-release, gaussian-mechanism, laplace-mechanism, randomized-response, linear-programming-problem, hamming-distance]
sources:
  - paper: doi:10.1145/773153.773173
    title: "Irit Dinur and Kobbi Nissim, Revealing information while preserving privacy, PODS 2003, pages 202 to 210"
    locator: the reconstruction theorems for subset sum queries with error o(n) and o(sqrt n)
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: "Section 5.1: Definition 5.1 (blatant non-privacy), Theorem 5.2 and Corollary 5.3, Definition 5.4 (partial discrepancy), Theorem 5.5, Theorem 5.6 and Lemma 5.7, and the remark on a polynomial-time version with a linear program"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: "Section 8.1: Definition 8.1 (blatant non-privacy), Theorem 8.1 (error E on all subsets gives 4E wrong positions), Theorem 8.2 (a linear number of random queries, robust to a fraction of bad answers)"
  - paper: "Cynthia Dwork and Sergey Yekhanin, New efficient attacks on statistical disclosure control mechanisms, CRYPTO 2008, LNCS 5157, pages 469 to 480"
    locator: explicit query sets with a polynomial-time reconstruction
---

The Dinur-Nissim theorems are lower bounds on the error of every mechanism that protects privacy. A dataset holds one secret bit for each of $n$ people, and a query asks for the number of 1s in a subset of the rows. If a mechanism answers all $2^n$ subset queries with error $o(n)$, or about $n$ random subset queries with error $o(\sqrt n)$, then the answers fix all but a small fraction of the bits. Such a mechanism is "blatantly non-private", and no differentially private mechanism can be that. So too many accurate answers destroy privacy, whatever the method of noise. The result came before [differential privacy](/differential-privacy-definition/) and shaped it: noise of order $\sqrt n$ on each of $n$ counts is needed, and up to log factors it is enough.

## Statement

**Setting.** A dataset is a vector $x \in \{0,1\}^n$, one secret bit for each row. Two datasets are neighbors if they differ in one row (replace). A query is $q \in \{0,1\}^n$, a subset of the rows, with the normalized answer $\langle q, x \rangle / n$. A mechanism $M$ answers a set of queries $q_1, \dots, q_k$ with error $\alpha$ if, with high probability, its outputs $y_j$ satisfy $|y_j - \langle q_j, x \rangle/n| \le \alpha$ for all $j$.

**Definition (blatant non-privacy; Vadhan Definition 5.1, Dwork-Roth Definition 8.1).** $M$ is blatantly non-private if for every $x$, one can compute from $M(x)$ a vector $x'$ that differs from $x$ in at most $n/10$ coordinates, with high probability over the coins of $M$.

**Theorem 1 (all queries; Vadhan Theorem 5.2, Dwork-Roth Theorem 8.1).** If $|y_q - \langle q, x\rangle/n| \le \alpha$ for every $q \in \{0,1\}^n$, then every $x' \in \{0,1\}^n$ with $|y_q - \langle q, x'\rangle/n| \le \alpha$ for all $q$ differs from $x$ in at most $4\alpha n$ coordinates. Such an $x'$ exists, since $x$ is one. So with $\alpha \le 1/40$, $M$ is blatantly non-private (Vadhan Corollary 5.3).

**Theorem 2 (partial discrepancy; Vadhan Theorem 5.5).** Let $Q$ be the $k \times n$ matrix with rows $q_1, \dots, q_k$, and let

$$\mathrm{PDisc}(Q) = \min \{ \|Qz\|_\infty : z \in \{-1, 0, 1\}^n, \|z\|_1 > n/10 \}.$$

If $M$ answers $q_1, \dots, q_k$ with error $\alpha < \mathrm{PDisc}(Q)/(2n)$, then $M$ is blatantly non-private.

**Theorem 3 (few queries; Vadhan Theorem 5.6 with Lemma 5.7).** There is a constant $c > 0$ such that, with high probability, $n$ uniformly random queries $q_1, \dots, q_n$ have $\mathrm{PDisc}(Q) \ge 2c\sqrt n$. Then every mechanism that answers them with error below $c/\sqrt n$ is blatantly non-private. In counts, the error must be at least $c\sqrt n$ on some query.

**Theorem 4 (private mechanisms are not blatantly non-private).** Let $X = \{0,1\}$ and let $M$ be $(\varepsilon, \delta)$-DP. For a uniformly random $x$ and any rule that guesses $x$ from $M(x)$, the expected fraction of correct bits is at most $(e^{\varepsilon} + \delta)/(1 + e^{\varepsilon})$. For $\varepsilon = 1$ and $\delta = 0.1$ this is below $0.76$, so $M$ cannot reach $0.9 n$ correct bits with probability above $0.85$.

**The lesson.** By Theorems 1, 3 and 4, a $(1, 0.1)$-DP mechanism has error above $1/40$ on some subset query, and error at least $c/\sqrt n$ on some of $n$ random subset queries. Every private method of data release must pay this error.

## In plain words

Each person in a table has one secret yes or no. You may ask "how many of these people said yes?" for any group you like, and you get an answer that is a little wrong.

If you may ask about every group and each answer is wrong by much less than $n$, then only a table close to the true one fits all the answers: ask about the people who said no, and about those who said yes, and a wrong guess shows up. If you ask about only $n$ random groups, a far table still fails some random group by about $\sqrt n$. So answers wrong by much less than $\sqrt n$ let anyone rebuild almost all secrets. A private method must make its answers wrong by at least about $\sqrt n$.

## Proof

All four parts are proved here, except Lemma 5.7 of Vadhan in Theorem 3, which is a marked sketch.

**Theorem 1.** Fix $x'$ that is consistent with all answers. By the triangle inequality, $|\langle q, x' - x\rangle| \le 2\alpha n$ for every $q$. Take $q_0$, the set of rows with $x_i = 0$. Then $\langle q_0, x \rangle = 0$, and $\langle q_0, x' \rangle$ is the number of rows with $x_i = 0$ and $x'_i = 1$, so there are at most $2\alpha n$ such rows. Take $q_1$, the set of rows with $x_i = 1$. Then $\langle q_1, x - x' \rangle$ is the number of rows with $x_i = 1$ and $x'_i = 0$, again at most $2\alpha n$. So $x$ and $x'$ differ in at most $4\alpha n$ rows, which is at most $n/10$ for $\alpha \le 1/40$. $\blacksquare$

**Theorem 2.** Let $x'$ be consistent with the answers to $q_1, \dots, q_k$ (the true $x$ is one), and let $z = x - x' \in \{-1, 0, 1\}^n$. By the triangle inequality, $\|Qz\|_\infty \le 2\alpha n < \mathrm{PDisc}(Q)$. By the definition of $\mathrm{PDisc}$, this forces $\|z\|_1 \le n/10$, so $x'$ differs from $x$ in at most $n/10$ rows. $\blacksquare$

**Theorem 3 (sketch of Lemma 5.7).** This is a sketch; the full argument is Vadhan, the proof sketch of Lemma 5.7, with the anticoncentration bound he cites there. Fix $z \in \{-1, 0, 1\}^n$ with $\|z\|_1 > n/10$. Then $z$ has more than $n/20$ entries of the same sign, so for a random $q$ the value $\langle q, z \rangle$ is a difference of two independent binomial sums, one with more than $n/20$ fair terms. By anticoncentration, $|\langle q, z \rangle| \ge t\sqrt n$ with probability at least $1 - O(t)$. For $n$ independent queries, all fail with probability at most $O(t)^n$. A union bound over at most $3^n$ vectors $z$ gives $3^n O(t)^n < 1$, and in fact small, for a small constant $t$. So $\mathrm{PDisc}(Q) \ge t\sqrt n$ with high probability, and Theorem 2 applies with $c = t/2$. $\blacksquare$

**Theorem 4.** Fix a row $i$ and a guess rule $G_i$ for bit $i$. Let $x^{(b)}$ be $x$ with $x_i = b$, for the other rows fixed. Let $a = P[G_i(M(x^{(0)})) = 0]$ and $b = P[G_i(M(x^{(1)})) = 1]$. The two datasets are neighbors, so $b \le e^{\varepsilon}(1 - a) + \delta$ and $a \le e^{\varepsilon}(1 - b) + \delta$. Adding them gives $(a + b)(1 + e^{\varepsilon}) \le 2e^{\varepsilon} + 2\delta$, so the chance $(a + b)/2$ of a correct guess of bit $i$ is at most $(e^{\varepsilon} + \delta)/(1 + e^{\varepsilon})$. Average over the other rows and sum over $i$ for the expected number of correct bits. If $M$ were blatantly non-private with probability $p$, the expected fraction would be at least $0.9p$, which is above $0.76$ for $p > 0.85$. $\blacksquare$

**A hand example of the proof of Theorem 1.** Take $n = 8$ and $x = (1,0,1,1,0,0,1,0)$, with counts that are wrong by at most $E = 0.9$. The candidate $x' = (1,1,1,1,0,1,1,0)$ differs from $x$ in rows 2 and 6. The query $q_0 = \{2, 5, 6, 8\}$ has the true count 0 and the count 2 on $x'$. An answer within 0.9 of 0 is more than 0.9 from 2, so the answer to $q_0$ rules out $x'$. In general, the candidates that survive differ from $x$ in at most $2E$ rows of $q_0$ and $2E$ rows of $q_1$, here at most 1 row each.

## Consequences

- **Error of order $\sqrt n$ is the price of privacy for $n$ counts.** Any $(\varepsilon, \delta)$-DP release of $n$ random subset counts has error of order $\sqrt n$ on some count, for constant $\varepsilon$ and $\delta$.
- **A limit on query release.** A mechanism for [private query release](/private-query-release/) cannot answer all $2^n$ subset queries on $n$ rows with error below $n/40$ in counts. With more rows than the log of the number of queries, as in [SmallDB](/smalldb-mechanism/) and [MWEM](/mwem/), the error can be small.
- **Polynomial time.** A linear program finds a fractional $x' \in [0,1]^n$ that is consistent with the answers, and rounding gives the same conclusion for random queries (Vadhan, the remark after Lemma 5.7). Dwork and Yekhanin give explicit query sets with fast decoding. So the bound does not need a strong adversary.
- **Robustness.** Dwork and Roth Theorem 8.2 shows that a linear number of random $\pm 1$ queries is enough even if only a fraction $\frac{1}{2} + \eta$ of the answers have error at most $\alpha$: the answers then fix all but $(2\alpha/\eta)^2$ entries.
- **Noise is not optional.** The theorems do not depend on how the answers are made. Rounding, sampling or "cell suppression" that keeps all answers accurate falls under them as well. A real release also needs a cryptographic source of randomness and exact sampling for its noise (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Tightness

The bounds are tight up to constants and log factors (theorems). For all $2^n$ queries, error $\Theta(1)$ in normalized form is the right order: answering $1/2$ to every query has error at most $1/2$ and is $(0,0)$-DP. The [Gaussian mechanism](/gaussian-mechanism/) answers $k$ counting queries with normalized error $O(\sqrt{k \log(1/\delta) \log k}/(\varepsilon n))$, and Vadhan Theorem 2.7 lowers $\log k$ to $\log \log k$. For $k = n$ and constant $\varepsilon$ and $\delta$ this is $\tilde O(1/\sqrt n)$, which matches Theorem 3 up to log factors. With $\mathrm{Lap}(b)$ (density $(1/(2b))e^{-|z|/b}$, variance $2b^2$, $P(|Z| > t) = e^{-t/b}$) on each of $k$ counts, the [Laplace mechanism](/laplace-mechanism/) has error of order $k/\varepsilon$ in counts, which is $\varepsilon$-DP but larger than $\sqrt k$.

## History

Dinur and Nissim (PODS 2003) proved the reconstruction theorems, for subset sums with error $o(n)$ on all queries and with error $o(\sqrt n)$ on polynomially many queries, with an efficient decoder for the second. Dwork, McSherry, Nissim and Smith (2006) then defined differential privacy with noise calibrated to sensitivity. Dwork, McSherry and Talwar (2007) and Dwork and Yekhanin (2008) made the attacks robust and fast. Dwork and Roth (2014) and Vadhan (2017) present the results as lower bounds, with the partial discrepancy view. The theorems are often cited as a reason for statistical agencies to protect published tables with formal privacy.

## References
