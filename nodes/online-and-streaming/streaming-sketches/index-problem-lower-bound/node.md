---
tag: N46J3W
kind: theorem
slug: index-problem-lower-bound
name: INDEX communication lower bound
aliases:
- INDEX problem lower bound
- one-way lower bound for INDEX
area: online-and-streaming/streaming-sketches
level: advanced
summary: One-way communication lower bound for INDEX that yields many streaming space lower bounds.
prereqs: [index-problem, one-way-communication-complexity, randomized-communication-complexity, shannon-entropy, conditional-entropy, streaming-model]
see_also: [frequency-moment-lower-bounds, frequent-items-problem, distinct-elements-problem, disjointness-problem, gap-hamming-distance, information-complexity, communication-complexity, yao-minimax-principle]
sources:
  - paper: "Ilan Kremer, Noam Nisan and Dana Ron, On randomized one-round communication complexity, Computational Complexity 8(1), 1999"
    locator: the lower bound for the index function and the characterization of one-round complexity by the VC dimension (to check)
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: the chapter on one-way and rounds of communication, with the index function (to check)
  - paper: doi:10.1561/0400000076
    title: Tim Roughgarden, Communication Complexity (for Algorithm Designers), Foundations and Trends in Theoretical Computer Science 11(3-4), 2016
    locator: Lecture 2, lower bounds for one-way communication, the INDEX problem and its use for streaming lower bounds
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 10, Lower bounds for summaries (the INDEX problem and reductions to summaries)
---

In the INDEX problem, Alice holds a string $x \in \{0, 1\}^n$, Bob holds an index $i \in [n]$, and Alice sends one message after which Bob must output $x_i$. The theorem says that any one-way protocol, even a randomized one that errs with probability $\delta < 1/2$, needs about $(1 - H_2(\delta)) n$ bits, where $H_2$ is the binary entropy. This is linear in $n$ for every constant $\delta < 1/2$, while two messages, Bob's index and then the answer, need only $\lceil \log_2 n \rceil + 1$ bits. INDEX is the standard source of space lower bounds for one-pass streaming algorithms: if Alice can turn $x$ into a stream and Bob can turn $i$ into a continuation of that stream, then the memory of a streaming algorithm at the break is a one-way message. This gives, for example, $\Omega(n)$ bits for exact distinct counts and for the exact median, and $\Omega(1/\varepsilon)$ bits for $\varepsilon$-approximate distinct counts and for [frequent items](/frequent-items-problem/).

## Statement

Let $\mathrm{INDEX}_n$ be the problem above: Alice gets $x \in \{0, 1\}^n$, Bob gets $i \in \{1, \ldots, n\}$, only Alice sends a message, and Bob outputs a bit. A protocol may use public random bits $R$, independent of the inputs and seen by both players. It has error $\delta$ if for every $(x, i)$, Bob outputs $x_i$ with probability at least $1 - \delta$ over $R$. Let $H_2(p) = -p \log_2 p - (1 - p) \log_2(1 - p)$.

**Theorem.**

1. Every deterministic one-way protocol for $\mathrm{INDEX}_n$ sends at least $n$ bits on some input.
2. Let $0 \le \delta < 1/2$. Every randomized one-way protocol with error $\delta$ whose messages have at most $c$ bits satisfies
$$ c \ge (1 - H_2(\delta)) \, n - 1 , $$
and $c \ge (1 - H_2(\delta)) n$ if all messages have exactly $c$ bits. The same holds for protocols that are only correct with average error $\delta$ when $x$ and $i$ are uniform.

**Corollary (streaming).** Let $P$ be a streaming problem, and suppose that there are maps from $x$ to a stream $\sigma_A(x)$ and from $i$ to a stream $\sigma_B(i)$, and a map from the answer of $P$ on the stream $\sigma_A(x) \sigma_B(i)$ to $x_i$. Then every one-pass randomized algorithm for $P$ that fails with probability at most $\delta < 1/2$ uses at least $(1 - H_2(\delta)) n$ bits of memory.

## In plain words

Alice has a long row of secret bits, and Bob wants one of them, but Alice does not know which one. If Bob could speak, he would say which bit he wants and Alice would answer. But only Alice can speak, once. Then she must send something that answers every possible question of Bob, and that is nearly the whole row. Even if Bob may sometimes be wrong, the message must still carry most of the row.

A streaming algorithm reads its input once and keeps only its memory. If the first part of a stream comes from Alice's bits and the rest from Bob's question, the memory in the middle is a message from Alice to Bob. So an algorithm that can answer Bob's question needs about as much memory as the message.

## Proof

**Part 1.** Suppose a deterministic protocol sends fewer than $n$ bits on every input. There are fewer than $2^n$ messages of fewer than $n$ bits, since $\sum_{\ell < n} 2^\ell = 2^n - 1$. So two inputs $x \ne x'$ get the same message. Let $j$ be a position with $x_j \ne x'_j$. On index $j$, Bob sees the same message for both inputs and gives the same output, so he is wrong on one of them.

**Part 2.** We use these facts about entropy $H$, which hold for discrete random variables:

- (a) If $X$ is uniform on $\{0, 1\}^n$, then $H(X) = n$.
- (b) If $M$ takes at most $K$ values, then $H(M \mid R) \le H(M) \le \log_2 K$.
- (c) Subadditivity: $H(X_1, \ldots, X_n \mid Y) \le \sum_j H(X_j \mid Y)$.
- (d) Mutual information: $I(X; M \mid R) = H(X \mid R) - H(X \mid M, R) = H(M \mid R) - H(M \mid X, R) \le H(M \mid R)$.

**Lemma (Fano for one bit).** Let $B$ be a bit and $Y$ a random variable, and let $g(Y)$ be a guess of $B$ with $\Pr[g(Y) \ne B] = p$. Then $H(B \mid Y) \le H_2(p)$.

*Proof.* Let $E = 1[g(Y) \ne B]$. Given $Y$ and $E$, the bit $B$ is fixed: $B = g(Y)$ if $E = 0$ and $B = 1 - g(Y)$ if $E = 1$. So $H(B \mid Y) \le H(B, E \mid Y) = H(E \mid Y) + H(B \mid E, Y) = H(E \mid Y) \le H(E) = H_2(p)$. $\square$

Now fix a randomized protocol with error $\delta$. Bob's private coins, if any, can be made part of $R$. Let $X$ be uniform on $\{0, 1\}^n$ and independent of $R$, and let $M$ be Alice's message, a function of $X$ and $R$. For each $j$, Bob's output on index $j$ is a function $g_j(M, R)$, and since the error is at most $\delta$ for every input, $p_j = \Pr[g_j(M, R) \ne X_j] \le \delta$. By the lemma with $Y = (M, R)$, $H(X_j \mid M, R) \le H_2(p_j) \le H_2(\delta)$, because $H_2$ is increasing on $[0, 1/2]$. By (c),
$$ H(X \mid M, R) \le \sum_{j=1}^n H(X_j \mid M, R) \le n H_2(\delta) . $$
Since $X$ is independent of $R$, $H(X \mid R) = H(X) = n$ by (a). By (d),
$$ H(M \mid R) \ge I(X; M \mid R) = H(X \mid R) - H(X \mid M, R) \ge (1 - H_2(\delta)) n . $$
A message of at most $c$ bits takes at most $2^{c+1} - 1 < 2^{c+1}$ values, and a message of exactly $c$ bits takes at most $2^c$ values. By (b), $H(M \mid R) < c + 1$ in the first case and $H(M \mid R) \le c$ in the second. This gives both bounds.

For the average version, let $p_j$ be the error on index $j$ with $X$ uniform, so that $\frac{1}{n} \sum_j p_j \le \delta$. If each $p_j \le 1/2$, then by the concavity of $H_2$, $\sum_j H_2(p_j) \le n H_2(\delta)$, and the rest is the same. If some $p_j > 1/2$, Bob can flip his output on index $j$, which lowers $p_j$ to $1 - p_j$ and the average. $\square$

**Corollary.** Let $A$ be a streaming algorithm for $P$ with $s$ bits of memory and failure probability $\delta$. Alice runs $A$ on $\sigma_A(x)$ with the public random bits as the random bits of $A$, and sends the memory state, exactly $s$ bits. Bob continues the run on $\sigma_B(i)$, reads the answer and maps it to a bit. The run is the run of $A$ on $\sigma_A(x)\sigma_B(i)$, so Bob outputs $x_i$ with probability at least $1 - \delta$. By Part 2, $s \ge (1 - H_2(\delta)) n$. $\blacksquare$

## Consequences

Each reduction below fits the corollary, so each problem needs $\Omega(n)$ bits for the given $n$ and constant $\delta < 1/2$. The tests run each reduction on every input with $n \le 6$.

- **Exact distinct elements.** Alice streams the set $S = \{j : x_j = 1\}$. Bob reads $F_0$, adds the item $i$, and reads $F_0$ again. It grows if and only if $x_i = 0$. So exact $F_0$ needs $\Omega(n)$ bits, and so does membership: "has item $i$ occurred?".
- **Approximate distinct elements.** With the same streams, Alice also sends $|S|$ in $O(\log n)$ bits. After Bob's item, $F_0$ is $|S|$ or $|S| + 1$. An estimate within a factor $1 \pm \varepsilon$ is off by at most $\varepsilon(n + 1)$, which is less than $1/2$ if $n < 1/(2\varepsilon) - 1$, and then rounding to the nearer of the two values gives $x_i$. So a $(1 \pm \varepsilon)$ estimate of $F_0$ needs $\Omega(1/\varepsilon)$ bits. The stronger bound $\Omega(1/\varepsilon^2)$ comes from the [gap Hamming problem](/gap-hamming-distance/), which itself reduces from INDEX (Jayram, Kumar and Sivakumar 2008).
- **Exact median.** Indexing from 0, Alice streams the values $2j + 2 + x_j$ for $j = 0, \ldots, n - 1$, which are increasing in $j$. Bob adds $n - 1 - i$ copies of 0 and $i$ copies of a value above all of Alice's. The stream has $2n - 1$ items, and the $n$-th smallest is $2i + 2 + x_i$, whose parity is $x_i$. So the exact median needs $\Omega(n)$ bits in one pass, matching the bound of Munro and Paterson for selection.
- **Frequent items.** Alice streams one copy of each $j$ with $x_j = 1$, and Bob adds many copies of $i$ so that $i$ is above the threshold only if $x_i = 1$. With $n = \Theta(1/\varepsilon)$, this shows that the $\varepsilon$-approximate [frequent items problem](/frequent-items-problem/) needs $\Omega(1/\varepsilon)$ bits; the details are on that page.
- **Lower bounds for sketches.** Since a [linear sketch](/linear-sketch/) is a streaming algorithm, the same bounds hold for the number of bits in any sketch that supports the query.

INDEX gives only one-way bounds, so it does not apply directly to algorithms with several passes. For several passes, reductions use problems that are hard for two-way communication, such as [set disjointness](/disjointness-problem/); see [frequency moment lower bounds](/frequency-moment-lower-bounds/).

## Tightness

- **Deterministic.** Alice sends $x$, $n$ bits, so Part 1 is exact.
- **Randomized.** The bound $(1 - H_2(\delta)) n$ is tight up to lower-order terms. Alice and Bob share a random string $r \in \{0, 1\}^n$ and a random permutation $\pi$ of the positions. Alice computes $z = \pi(x \oplus r)$, finds the nearest word $w$ of a covering code of radius $\delta n$ with $2^{(1 - H_2(\delta)) n + O(\log n)}$ words, and sends its index. Bob outputs $w_{\pi(i)} \oplus r_i$. The string $z$ is uniform and independent of $\pi$, so the set of wrong positions of $w$ is independent of $\pi(i)$, and Bob errs with probability at most $\delta$ for every input.
- **Two-way.** If Bob may speak first, he sends $i$ in $\lceil \log_2 n \rceil$ bits and Alice answers with one bit. So the bound is a property of one-way communication, and of one-pass streaming.
- **The brute-force check.** For $n = 3$ and two-bit messages, the best deterministic protocol under the uniform distribution sends two bits of $x$ and has average error $1/6$, and $(1 - H_2(1/6)) \cdot 3 \approx 1.05 \le 2$.

## History

The index function is one of the basic examples of one-way communication complexity. Its randomized one-way bound appears in work of Ablayev (1996), who used it for space lower bounds of branching programs, and of Kremer, Nisan and Ron (1999), who related one-round randomized complexity to the VC dimension; INDEX is the case with the largest VC dimension. Henzinger, Raghavan and Rajagopalan (1998) were among the first to use communication complexity for lower bounds on data streams, and INDEX reductions are now the standard tool for one-pass space bounds, as in the surveys of Muthukrishnan (2005) and Roughgarden (2016). Jayram, Kumar and Sivakumar (2008) reduced INDEX to gap Hamming, which gave the one-way $\Omega(1/\varepsilon^2)$ bounds for distinct elements and for frequency moments.

## References
