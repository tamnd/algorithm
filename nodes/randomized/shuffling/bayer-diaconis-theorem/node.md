---
tag: 1507MX
kind: theorem
slug: bayer-diaconis-theorem
name: Bayer-Diaconis theorem
aliases:
- seven shuffles theorem
- 3/2 log2 n theorem
- dovetail shuffle theorem
area: randomized/shuffling
level: advanced
summary: Under the riffle-shuffle model, about (3/2) log2 n shuffles make an n-card deck close to uniform, with a sharp cutoff; for 52 cards the distance is 0.33 after 7 shuffles, then halves each time.
prereqs: [gilbert-shannon-reeds-model, total-variation-distance, eulerian-numbers]
see_also: [gilbert-shannon-reeds-model, card-shuffling, strong-uniform-time, mixing-time, top-to-random-shuffle, random-transposition-shuffle, descents, stirling-approximation]
sources:
  - paper: "Dave Bayer and Persi Diaconis, Trailing the dovetail shuffle to its lair, Annals of Applied Probability 2(2), 1992"
    locator: pp. 294 to 313; the exact formula for an a-shuffle, the asymptotic theorem for k = (3/2) log2 n + θ, and the table for n = 52 (theorem and table numbers to be checked)
  - paper: "David Aldous, Random walks on finite groups and rapidly mixing Markov chains, Séminaire de Probabilités XVII, Lecture Notes in Mathematics 986, Springer, 1983"
    locator: the riffle shuffle and the order (3/2) log2 n (pages to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 4 (riffle shuffles) (to be checked)
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, Markov Chains and Mixing Times, second edition, 2017
    locator: Section 8.3 (riffle shuffles) and the notes to Chapter 8 (section numbers to be checked)
---

The Bayer-Diaconis theorem gives the exact law of a deck after $k$ riffle shuffles in the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/), and from it the sharp number of shuffles needed to mix: about $\frac32 \log_2 n$ for $n$ cards. The [total variation distance](/total-variation-distance/) to uniform stays near 1 until about that point and then falls by a factor of about 2 with each shuffle. For a deck of 52 cards, $\frac32 \log_2 52 \approx 8.55$, and the exact distance is $0.92$ after 5 shuffles, $0.61$ after 6, $0.33$ after 7 and $0.17$ after 8. This is the source of the popular rule that seven riffle shuffles are needed to mix a deck. Bayer and Diaconis published the result in 1992; Aldous had shown in 1983 that $\frac32 \log_2 n$ is the right order.

## Statement

Let $P^k$ be the law of a deck of $n$ cards after $k$ GSR shuffles from a fixed order, $\pi$ the uniform law, and $d(k) = \|P^k - \pi\|_{TV}$.

**Theorem 1 (the exact law).** For every order $\sigma$ with $r$ rising sequences,
$$P^k(\sigma) = \binom{2^k + n - r}{n} \Big/ 2^{kn}.$$
Hence, with $A(n, r)$ the number of orders with $r$ rising sequences (an [Eulerian number](/eulerian-numbers/)),
$$d(k) = \frac12 \sum_{r=1}^{n} A(n, r) \left| \binom{2^k + n - r}{n} 2^{-kn} - \frac{1}{n!} \right|.$$

**Theorem 2 (the cutoff).** Let $k = \frac32 \log_2 n + \theta$. Then
$$d(k) = 1 - 2\,\Phi\!\left( -\frac{2^{-\theta}}{4\sqrt3} \right) + O(n^{-1/4}),$$
where $\Phi$ is the standard normal distribution function. The error term is uniform in $\theta$ as stated by Bayer and Diaconis (the exact form of the error term is to be checked). In particular, $d(\frac32 \log_2 n + \theta) \to 1$ as $\theta \to -\infty$ and $\to 0$ as $\theta \to \infty$, uniformly in large $n$: a cutoff at $\frac32 \log_2 n$ with a window of constant width.

## In plain words

When you riffle a deck, the cards from each half stay in their order, so the new deck is made of two runs of cards that rise in their old order. After two riffles it has at most four such runs, after three at most eight, and so on. A well mixed deck has about half as many runs as cards. So until the number of runs that the shuffles allow is much more than that, the deck is clearly not mixed.

Bayer and Diaconis found the exact chance of each order after any number of riffles: it depends only on the number of rising runs. With it they showed that a deck of n cards needs about one and a half times the base-two logarithm of n riffles. For 52 cards that is about seven to nine riffles, and after that each riffle halves what is left.

## Proof

**Theorem 1.** By the composition rule on the [GSR model](/gilbert-shannon-reeds-model/) page, $k$ GSR shuffles have the law of one $a$-shuffle with $a = 2^k$: an inverse $a$-shuffle sorts the deck stably by uniform labels in $\{0, \ldots, a-1\}$, and $k$ inverse 2-shuffles sort stably by $k$ fair bits, which form such a label. An $a$-shuffle is a uniform word $w \in \{0, \ldots, a-1\}^n$: the packets are consecutive blocks of the start order, and position $p$ of the new deck gets the next card of packet $w_p$.

Fix $\sigma$ with $r$ rising sequences. The packets are split at $a - 1$ cut points $0 \le c_1 \le \cdots \le c_{a-1} \le n$ in the start order. Each packet appears in $\sigma$ in increasing positions, so $\sigma$ comes from $w$ exactly when every place where a rising sequence of $\sigma$ ends is a cut point. There are $r - 1$ such places. The other $a - r$ cut points are a multiset of the $n + 1$ places, which can be chosen in $\binom{n + a - r}{a - r} = \binom{a + n - r}{n}$ ways, and the cut points and $\sigma$ together fix $w$. Each word has probability $a^{-n}$. Summing $|P^k(\sigma) - 1/n!|$ by classes of equal $r$ gives the formula for $d(k)$. ∎

**Theorem 2, the main steps.** Write $a = 2^k = c\, n^{3/2}$, so $c = 2^\theta$. The factor that compares $P^k$ with uniform is
$$n! \, P^k(\sigma) = \frac{(a + n - r)(a + n - r - 1) \cdots (a + 1 - r)}{a^n} = \prod_{i=1}^{n} \left( 1 + \frac{i - r}{a} \right).$$
Put $r = \frac n2 + h$. Take logarithms and expand $\ln(1 + x) = x - \frac{x^2}{2} + O(x^3)$. The sum of $i - r$ over $i = 1, \ldots, n$ is $-nh + \frac n2$, and the sum of $(i - r)^2$ is $\frac{n^3}{12} + O(n h^2 + n^2)$. With $a = c n^{3/2}$, for $h = O(\sqrt n)$,
$$\ln\bigl(n! \, P^k(\sigma)\bigr) = -\frac{h}{c \sqrt n} - \frac{1}{24 c^2} + O(n^{-1/2}).$$
Since $P^k(\sigma)$ falls as $r$ grows, $d(k) = \sum_\sigma (P^k(\sigma) - \frac{1}{n!})^+ = E\bigl[(n! P^k(R) - 1)^+\bigr]$, where $R$ is the number of rising sequences of a *uniform* order. $R - 1$ is the number of [descents](/descents/) of a uniform order, with mean $\frac{n-1}{2}$ and variance $\frac{n+1}{12}$, and it satisfies a central limit theorem: $R = \frac n2 + \sqrt{n/12}\, Z + O(1)$ with $Z$ close to standard normal. Substitute $h = \sqrt{n/12}\, Z$ and put $s = \frac{1}{c\sqrt{12}}$; then $\frac{1}{24 c^2} = \frac{s^2}{2}$ and
$$n! \, P^k(R) \approx e^{-sZ - s^2/2}.$$
For a standard normal $Z$, the formula for a lognormal variable gives $E[(e^{-sZ - s^2/2} - 1)^+] = \Phi(\frac s2) - \Phi(-\frac s2) = 1 - 2\Phi(-\frac s2)$. Finally $\frac s2 = \frac{1}{4\sqrt3\, c} = \frac{2^{-\theta}}{4\sqrt3}$. Bayer and Diaconis make each approximation exact up to $O(n^{-1/4})$, using a local limit theorem for the Eulerian numbers and the tails where $h$ is large; those estimates are not repeated here. ∎

**The lower bound alone, by counting.** A short argument gives $d(k) \to 1$ for $k \le (1 - \varepsilon) \log_2 n$. After $k$ shuffles the deck has at most $2^k$ rising sequences, and a uniform order has $R > 2^k$ with probability $1 - o(1)$ when $2^k = o(n)$, because $R$ has mean $\frac{n+1}{2}$ and standard deviation $O(\sqrt n)$. The extra factor $\frac32$ needs the finer computation above.

## Consequences

**Recomputed table.** The values below were recomputed with exact rational arithmetic from Theorem 1, and checked against brute force over all orders for $n \le 6$ (see the tests of the GSR model page). They agree with the table of Bayer and Diaconis to the shown digits as far as the writer could compare (to be checked against the paper).

| $n$ | $\frac32 \log_2 n$ | $d(k)$ for $k = 4, 5, \ldots, 12$ |
|---|---|---|
| 13 | 5.55 | 0.3558, 0.1750, 0.0850, 0.0416, 0.0206, 0.0102, 0.0051, 0.0025, 0.0013 |
| 26 | 7.05 | 0.8040, 0.4692, 0.2345, 0.1223, 0.0618, 0.0310, 0.0155, 0.0078, 0.0039 |
| 52 | 8.55 | 1.0000, 0.9237, 0.6135, 0.3341, 0.1672, 0.0854, 0.0429, 0.0215, 0.0108 |
| 104 | 10.05 | 1.0000, 1.0000, 0.9877, 0.7718, 0.4538, 0.2373, 0.1187, 0.0600, 0.0301 |
| 208 | 11.55 | 1.0000, 1.0000, 1.0000, 0.9996, 0.9137, 0.6027, 0.3288, 0.1682, 0.0841 |

**The asymptotic formula is already good at 52 cards.** For $n = 52$ and $k = 4$ to 12, $1 - 2\Phi(-2^{-\theta}/(4\sqrt3))$ gives $0.9993, 0.9092, 0.6023, 0.3276, 0.1674, 0.0842, 0.0422, 0.0211, 0.0105$, within about $0.015$ of the exact values.

**Seven shuffles.** For 52 cards the distance is still $0.61$ after 6 shuffles and $0.33$ after 7. Seven is the first number of shuffles below $\frac12$; it is not a point where the deck becomes "random". The deck is within $0.1$ of uniform after 9 shuffles ($0.085$) and within $0.01$ after 13 ($0.0054$). Doubling the deck adds about $\frac32$ shuffles: a 104-card deck first drops below $\frac12$ at 8 shuffles and below $0.1$ at 11.

**Each shuffle halves the distance** past the cutoff, since $1 - 2\Phi(-x) \approx 2x \varphi(0)$ for small $x$, and $x = 2^{-\theta}/(4\sqrt3)$ halves when $\theta$ grows by 1.

**Separation needs more.** The separation distance after $k$ shuffles is $1 - \prod_{i=1}^{n-1}(1 - i/2^k)$, which needs about $2 \log_2 n$ shuffles; for 52 cards it is $0.48$ after 11 shuffles and $0.28$ after 12. See [strong uniform time](/strong-uniform-time/).

**Practical meaning.** Games that use the order of a deck that was riffled too few times can be exploited, because rising sequences survive; Bayer and Diaconis describe a card trick of this kind based on the number of rising sequences (to be checked).

## Tightness

- **The constant $\frac32$ is sharp.** Theorem 2 gives $d(\frac32 \log_2 n + \theta) \to 1 - 2\Phi(-2^{-\theta}/(4\sqrt3))$, which is close to 1 for $\theta \ll 0$. So no smaller multiple of $\log_2 n$ suffices.
- **The window is of constant width** in the number of shuffles: going from $d \approx 0.9$ to $d \approx 0.1$ takes about 4 shuffles for every $n$, as the table shows.
- **The measure matters.** For separation the threshold is $2 \log_2 n$, and other measures, such as the entropy of the deck or the gain in specific guessing games, give smaller numbers of shuffles; see [card shuffling](/card-shuffling/). The theorem is about total variation.
- **The model matters.** Real shuffles are not exactly GSR. Neat shuffles that interleave more evenly are closer to the [faro shuffle](/faro-shuffle/) and can mix more slowly. The theorem says nothing about [overhand shuffles](/overhand-shuffle-model/), which need far more steps.

## History

Gilbert and Shannon proposed the riffle model in 1955, and Reeds studied it in 1981, with the inverse shuffle and a strong uniform time that needs about $2 \log_2 n$ shuffles. Aldous showed in 1983 that $\frac32 \log_2 n$ shuffles are necessary and sufficient to first order. Bayer and Diaconis found the exact formula and the precise cutoff in "Trailing the dovetail shuffle to its lair", published in 1992. The result was widely reported in the press as "seven shuffles suffice" for a deck of 52 cards.

## References
