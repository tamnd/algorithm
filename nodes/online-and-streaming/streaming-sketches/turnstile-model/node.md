---
tag: 3PXCEV
kind: model
slug: turnstile-model
name: Turnstile model
aliases:
- dynamic stream model
- general turnstile model
- strict turnstile model
- dynamic streams
area: online-and-streaming/streaming-sketches
level: core
summary: Stream updates may both increase and decrease item counts.
prereqs: [cash-register-model, frequency-vector]
see_also: [linear-sketch, count-min-sketch, count-sketch, ams-sketch, l0-sampler, agm-graph-sketch, indyk-p-stable-sketch, dyadic-intervals]
sources:
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: Chapter Data Streaming, Formal Aspects, section Data Stream Models (the turnstile model and the strict turnstile model)
  - paper: doi:10.1145/2591796.2591812
    title: Yi Li, Huy L. Nguyen and David P. Woodruff, Turnstile streaming algorithms might as well be linear sketches, STOC 2014
    locator: pp. 174 to 183
  - paper: doi:10.1145/3357713.3384278
    title: John Kallaugher and Eric Price, Separations and equivalences between turnstile streaming and linear sketching, STOC 2020
    locator: pp. 1223 to 1236
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction (insertion-only and turnstile streams)
---

The turnstile model is the update model of the [streaming model](/streaming-model/) in which an update can both add to and subtract from the count of an item. The stream is a sequence of updates $(i_j, \Delta_j)$ with $i_j \in [n]$ and $\Delta_j \in \mathbb{Z}$, and the [frequency vector](/frequency-vector/) is $f = \sum_j \Delta_j e_{i_j}$. In the general turnstile model $f$ can have negative entries. In the strict turnstile model the stream promises that $f_i \ge 0$ at all times, so a deletion only removes copies that are present. The name, from Muthukrishnan (2005), comes from a gate that counts people who come in and go out. On this page $m$ is the number of updates and $n$ is the universe size.

## The machine

The machine is the streaming machine, with $s$ bits of memory and one pass. The input has this form.

- Each update is $(i, \Delta)$ with $i \in [n]$ and $\Delta$ a nonzero integer.
- There is a known bound $M$ with $|f_i| \le M$ at all times, usually $M = \mathrm{poly}(n)$. So an exact counter for one coordinate needs $O(\log M)$ bits, and a word holds one.
- **General turnstile.** $f$ can be any vector in $\{-M, \ldots, M\}^n$. This covers the difference of two streams: run stream $A$ with $+1$ updates and stream $B$ with $-1$ updates, and $f = f_A - f_B$.
- **Strict turnstile.** $f_i \ge 0$ after each update. This is a database table under inserts and deletes of rows that exist.

The model allows deletions, but the algorithm does not know which earlier updates a deletion cancels: it sees only the pair $(i, \Delta)$.

## What it counts

The costs are those of the streaming model: the bits of memory, including the random seeds that the algorithm keeps, the update time, the query time, and the error with its failure probability. Two quantities that are free in the [cash register model](/cash-register-model/) are not free here. The number of updates $m$ says nothing about $\|f\|_1$, since updates can cancel. And a statistic such as the number of distinct items can go down, so a summary must be able to undo an update.

## Relation to other models

- **Generality.** Cash register streams are strict turnstile streams, and strict turnstile streams are general turnstile streams. So each general turnstile algorithm works in the other two models, and each lower bound for the cash register model holds here.
- **Linear sketches.** An algorithm that keeps $Sf$ for a fixed random matrix $S$ works in the general turnstile model: an update $(i, \Delta)$ adds $\Delta$ times column $i$ of $S$. Li, Nguyen and Woodruff (2014) proved a converse. Any one-pass turnstile algorithm that computes a function of $f \in \{-M, \ldots, M\}^n$ with constant probability can be replaced by one that draws a matrix $A$ from a fixed set of $O(n \log M)$ integer matrices with entries of size $\mathrm{poly}(n)$, and keeps $Af$. The proof needs the original algorithm to be correct on streams of any length, also when the counts in the middle of the stream are very large, and the new algorithm is non-uniform. Kallaugher and Price (2020) showed that the converse can fail when the stream length or the counts in the middle are bounded. See [linear sketch](/linear-sketch/).
- **Lower bounds by subtraction.** Communication reductions use deletions directly: Alice inserts $x$, Bob deletes $y$, and the stream ends with $f = x - y$. Then $f = 0$ exactly when $x = y$, and $\|f\|_0$ is the Hamming distance of two bit vectors.
- **Graph streams.** In a dynamic graph stream, edges are inserted and deleted. Linear sketches of the vertex incidence vectors, as in the [AGM sketch](/agm-graph-sketch/), solve connectivity in $O(n\,\mathrm{polylog}\,n)$ bits.

## Known results in the model

**Proved here: testing $f = 0$ with $O(\log(nM/\delta))$ bits.** Let $p$ be a prime with $p > M$ and $p \ge n/\delta$, and pick $z$ uniform in $\{0, \ldots, p-1\}$. Keep $P = \sum_i f_i z^i \bmod p$. An update $(i, \Delta)$ adds $\Delta z^i \bmod p$, with $O(\log i)$ multiplications modulo $p$. The query answers "$f = 0$" when $P = 0$.

*Proof.* If $f = 0$ then $P = 0$. If $f \ne 0$, some $f_i \ne 0$ with $|f_i| \le M < p$, so $f_i \not\equiv 0 \pmod p$, and $Q(z) = \sum_i f_i z^i$ is a nonzero polynomial of degree at most $n$ over the field $\mathbb{Z}_p$. It has at most $n$ roots, so $\Pr[P = 0] \le n/p \le \delta$. The memory is $z$ and $P$, two numbers of $\lceil \log_2 p \rceil = O(\log(nM/\delta))$ bits. $\square$

The test is a linear sketch with one row: $P = \langle s, f \rangle \bmod p$ with $s_i = z^i$. The same idea, applied to the parts of a hashed universe, finds one nonzero entry of $f$ when exactly one exists, which is the base of the [L0 sampler](/l0-sampler/).

**Proved here: the Misra-Gries summary does not carry over.** Take the [Misra-Gries summary](/misra-gries-summary/) with one counter. On the stream $a, b$ it stores $a$ with count 1, then the arrival of $b$ lowers that count to 0, and the summary is empty. On the stream $a, c$ it is empty too. Now append the deletion $(a, -1)$ to both. Both streams are strict turnstile streams, and they end with $f = e_b$ and $f = e_c$, so the only item left, which is the heavy hitter, is $b$ in one case and $c$ in the other. The summary is in the same state before the deletion in both cases, so any deterministic rule for the deletion gives the same answer to both, and it is wrong on one of them. $\square$

The following results are cited here and proved on the linked pages.

| problem | sketch | space | guarantee |
|---|---|---|---|
| point query $f_i$ | [count-min sketch](/count-min-sketch/) | $O(\varepsilon^{-1}\log(1/\delta))$ counters | error $\varepsilon\|f\|_1$; one-sided in the strict model |
| point query $f_i$ | [count sketch](/count-sketch/) | $O(\varepsilon^{-2}\log(1/\delta))$ counters | error $\varepsilon\|f\|_2$ |
| second moment $F_2$ | [AMS sketch](/ams-sketch/) | $O(\varepsilon^{-2}\log(1/\delta))$ counters | relative $\varepsilon$ |
| $\|f\|_p$, $0 < p \le 2$ | [p-stable sketch](/indyk-p-stable-sketch/) | $O(\varepsilon^{-2}\log(1/\delta))$ counters | relative $\varepsilon$ |
| a random nonzero coordinate | [L0 sampler](/l0-sampler/) | $O(\log^2 n\,\log(1/\delta))$ bits | near uniform |
| quantiles | [dyadic intervals](/dyadic-intervals/) with count-min | $O(\varepsilon^{-1}\log^2 n \log(\log n/\delta))$ counters | rank error $\varepsilon\|f\|_1$, strict model |
| dynamic graph connectivity | [AGM sketch](/agm-graph-sketch/) | $O(n \log^3 n)$ bits | with high probability |

## References
