---
tag: ACGS5S
kind: problem
slug: set-reconciliation
name: Set reconciliation
aliases:
- reconciling sets
- set difference synchronization
area: distributed/replication-and-crdts
level: advanced
summary: Two hosts hold sets that differ in d elements. Each must learn the elements it lacks, with communication close to d log u bits, independent of the size of the sets.
prereqs: [polynomial-interpolation, bloom-filter, hash-function]
see_also: [anti-entropy, merkle-tree, peeling-decoding, counting-bloom-filter, polynomial-factorization-over-finite-fields, scuttlebutt-reconciliation, k-core, universal-hashing]
sources:
  - paper: doi:10.1109/TIT.2003.815784
    title: Yaron Minsky, Ari Trachtenberg and Richard Zippel, Set reconciliation with nearly optimal communication complexity, IEEE Transactions on Information Theory 49(9), 2213-2218, 2003
    locator: the characteristic polynomial, the reconciliation by rational function interpolation from evaluations at m ≥ d points, the check at extra points, and the comparison with the information-theoretic lower bound
  - paper: doi:10.1109/ISIT.2001.936095
    title: Yaron Minsky, Ari Trachtenberg and Richard Zippel, Set reconciliation with nearly optimal communication complexity, Proceedings of the IEEE International Symposium on Information Theory (ISIT), 232, 2001
    locator: the conference version of the characteristic polynomial method
  - paper: doi:10.1145/2018436.2018462
    title: David Eppstein, Michael T. Goodrich, Frank Uyeda and George Varghese, What's the difference? Efficient set reconciliation without prior context, Proceedings of the ACM SIGCOMM 2011 Conference, 218-229, 2011
    locator: the Difference Digest, built from an invertible Bloom filter with count, idSum and hashSum fields, subtraction and peeling, and the Strata Estimator for the size of the difference
  - url: https://arxiv.org/abs/1101.2245
    title: Michael T. Goodrich and Michael Mitzenmacher, Invertible Bloom lookup tables, 49th Allerton Conference on Communication, Control, and Computing, 2011
    locator: the IBLT, listing by peeling, and the table of thresholds on the number of cells per item below which listing fails, about 1.222 for k = 3
---

Set reconciliation is the problem of making two sets equal by sending only what differs. Alice holds a set $A$ and Bob a set $B$, both drawn from a universe of $u$ possible elements, and the sets differ in $d$ elements, that is, $|A \triangle B| = d$. The goal is for each side to learn the elements it lacks, $A \setminus B$ for Bob and $B \setminus A$ for Alice, while the communication depends on $d$ and $\log u$ and not on $|A|$ or $|B|$. Sending one set whole costs $|A| \log_2 u$ bits, which is wasteful when the sets are large and almost equal, as replicas of a database usually are. Minsky, Trachtenberg and Zippel (2003) showed that about $d \log_2 u$ bits in one message are enough, by sending values of a polynomial whose roots are the elements; the invertible Bloom lookup table (IBLT) of Eppstein et al. (2011) and Goodrich and Mitzenmacher (2011) uses $O(d)$ cells of $O(\log u)$ bits and decodes in linear time.

## In plain words

Two people each have a big box of numbered cards. The boxes are almost the same, but a few cards are in one box and not the other. They want both boxes to end up with all the cards, and they want to talk as little as possible.

Reading out every card number takes very long. A smarter way lets one person send a short message whose length depends only on how many cards differ. From this message and their own box, the other person can work out exactly which cards are missing on each side. The trick is that the cards both people have cancel out of the message, and only the different ones are left to find.

## Definition

**Input.** A universe $U$ with $|U| = u$, for example the integers $1, \dots, u$. Alice holds $A \subseteq U$ and Bob holds $B \subseteq U$. Often a bound $\bar m \ge d = |A \triangle B|$ is known; otherwise it must be estimated.

**Output.** Bob learns $A \setminus B$ and $B \setminus A$, so that both can compute $A \cup B$, or so that Bob can send Alice what she lacks.

**Cost.** The number of bits exchanged, the number of messages (rounds), the computation at each side, and, for randomized protocols, the probability $\varepsilon$ of a wrong or missing answer.

**Model.** Two parties exchange messages over a reliable channel; there are no failures and no time limits. Both may use shared random hash functions. In a replicated store, two replicas run one such exchange in each [anti-entropy](/anti-entropy/) session, in the [asynchronous model](/asynchronous-model/).

## Variants

- **One-way or interactive.** In the one-way version, Alice sends one message and Bob decodes. Interactive protocols, such as a top-down comparison of [Merkle trees](/merkle-tree/), use more rounds and can have simpler messages.
- **Known or unknown d.** With a bound $\bar m \ge d$, one message suffices. Without it, the sides estimate $d$ first, or start with a small $\bar m$ and double it until the check passes.
- **Multisets and key-value maps.** A key-value map becomes a set of pairs (key, hash of value); a changed value shows up as two differing pairs.
- **Sets of sets.** Each party holds a collection of sets, and the goal is to reconcile each child set with its counterpart, as in documents made of lines.
- **Many parties.** Each of $n$ hosts holds a set, and all must learn the union. Gossip runs pairwise reconciliation between random pairs, as in [anti-entropy](/anti-entropy/).

## Examples

**Characteristic polynomials over GF(97).** The method works in a field $\mathbb{F}_p$ with $p$ larger than every element; here $p = 97$. The characteristic polynomial of a set $S$ is $\chi_S(z) = \prod_{x \in S} (z - x)$. Let $A = \{1, 2, 9, 12, 33\}$ and $B = \{1, 2, 9, 10, 12, 28\}$, so $d = 3$, and Bob knows $\bar m = 3$.

1. Alice sends $|A| = 5$ and $\chi_A$ at the points $96, 95, 94$, and at the extra point $93$: the values are $58, 19, 89, 77$.
2. Bob computes $\chi_B$ at the same points, $15, 54, 68, 77$, and divides: $f(z) = \chi_A(z) / \chi_B(z)$ gives $75, 74, 17, 1$. The common factor $\chi_{A \cap B}$ cancels, so $f = P/Q$ with $P = \chi_{A \setminus B}$ and $Q = \chi_{B \setminus A}$.
3. Bob knows $\deg P + \deg Q \le 3$ and $\deg P - \deg Q = |A| - |B| = -1$, so $P = z + p_0$ and $Q = z^2 + q_1 z + q_0$. The three equations $P(z) = f(z) Q(z)$ at $z = 96, 95, 94$ are linear in $p_0, q_1, q_0$, and give $p_0 = 64$, $q_1 = 59$, $q_0 = 86$.
4. At the extra point, $P(93)/Q(93) = 60/60 = 1 = f(93)$, so Bob accepts.
5. The roots are $P = z - 33$ and $Q = z^2 - 38z + 280 = (z - 10)(z - 28)$, so $A \setminus B = \{33\}$ and $B \setminus A = \{10, 28\}$.

Alice sent five numbers below 97. The common elements $1, 2, 9, 12$ never had to be named.

**An invertible Bloom lookup table.** Each cell of the table has a count, a keySum and a hashSum. To insert $x$, each of three hash functions picks a cell, and in each one the count goes up by 1, and $x$ and a check hash $g(x)$ are XORed into keySum and hashSum. Alice sends her table. Bob subtracts his own table cell by cell: counts subtract, sums XOR. An element in both sets cancels out of all its cells. What is left holds the elements of $A \setminus B$ with count $+1$ and those of $B \setminus A$ with count $-1$. A cell with count $\pm 1$ whose hashSum equals $g$(keySum) holds a single element, which can be read off and removed from its other cells; this may make other cells pure, and so on. This is [peeling decoding](/peeling-decoding/). It succeeds when every element is eventually alone in some cell.

**The size of the table.** For $d = 200$ differing elements and three hash functions, in 200 random trials of the code, peeling failed in all trials with $d$ cells, in about 55% with $1.25d$ cells, about 4% with $1.4d$, about 1.5% with $1.6d$ and about 0.5% with $2d$. For $d = 30$, the rates were higher: about 19% with $1.6d$ cells and 6% with $2d$. A table that is too small fails rather than giving a wrong answer, apart from a rare false pure cell, which the check hash makes unlikely.

## Known algorithms

| Method | Messages | Bits | Bob's work | Failure |
|---|---|---|---|---|
| Send the whole set | 1 | $\lvert A \rvert \log_2 u$ | $O(\lvert A \rvert + \lvert B \rvert)$ | none |
| Merkle tree comparison | $O(\log n)$ rounds | $O(d \log n \cdot \log u)$ | $O(d \log n)$ after building the trees | hash collisions |
| Characteristic polynomials | 1 | $(\bar m + k)\lceil\log_2 p\rceil$ | $O(\lvert B \rvert \bar m + \bar m^3)$, plus root finding | $\approx (\bar m/p)^k$ for $k$ check points |
| IBLT (difference digest) | 1 | $c\, d\, (\log_2 u + O(\log d))$, $c > 1.222$ | $O(\lvert B \rvert + d)$ | falls with $c$ and $d$ |

Here $n = \max(|A|, |B|)$.

- **Characteristic polynomial interpolation** (Minsky, Trachtenberg and Zippel 2003). Alice sends $|A|$ and $\chi_A$ at $\bar m + k$ points that cannot be elements. Bob forms $f = \chi_A / \chi_B$ at those points, solves the linear system of the example for monic $P$ and $Q$ with $\deg P + \deg Q = \bar m$ and $\deg P - \deg Q = |A| - |B|$, by [Gaussian elimination](/gaussian-elimination/) modulo $p$, divides both by their [greatest common divisor](/polynomial-gcd/), checks the result at the $k$ extra points, and finds the roots of $P$ and $Q$ by [factorization over a finite field](/polynomial-factorization-over-finite-fields/), such as the Cantor-Zassenhaus method. If $\bar m \ge d$, any solution of the system equals $P \cdot G$ and $Q \cdot G$ for a common $G$, so the gcd step recovers $P$ and $Q$ exactly. If $\bar m < d$, the system has no solution or the check fails, except with small probability, and the parties retry with a larger $\bar m$. The code uses $p = 2^{61} - 1$.
- **Difference digest** (Eppstein, Goodrich, Uyeda and Varghese 2011). Each side builds an invertible Bloom filter over hashes of its elements, Alice sends hers, and Bob subtracts and peels. The size of the table needs an estimate of $d$, which the Strata Estimator gives in one more short message.
- **Invertible Bloom lookup tables** (Goodrich and Mitzenmacher 2011). The general structure, with insert, delete and listing by peeling. Listing succeeds with high probability when the number of cells exceeds a threshold times the number of items, about $1.222$ for three hash functions, which is the threshold for a random 3-uniform hypergraph to have an empty 2-[core](/k-core/).
- **Merkle tree comparison.** Both sides build a hash tree over a fixed split of the universe and compare it top down, as in [anti-entropy](/anti-entropy/); simple, but it needs one round per tree level.

## Bounds

**Lower bound.** Fix Bob's set $B$. Alice's set can be any set within distance $d$ of $B$, and there are $\sum_{i=0}^{d} \binom{u}{i}$ of them. A one-way protocol that always succeeds must give each of them a different message, so it sends at least
$$\log_2 \sum_{i=0}^{d} \binom{u}{i} \;\ge\; \log_2 \binom{u}{d} \;\ge\; d \log_2 \frac{u}{d}$$
bits in the worst case. For $u = 2^{32}$ and $d = 10$, this is about 298 bits, and $d \log_2(u/d) \approx 287$.

**Upper bounds.** Characteristic polynomials send $\bar m + k$ elements of $\mathbb{F}_p$ and the size $|A|$. With $p$ just above $u$ and $\bar m = d$, this is $(d + k) \log_2 u + O(\log u)$ bits, so within an additive $O(d \log d + k \log u)$ of the lower bound when $d \ll u$. With $p = 2^{61} - 1$, $u = 2^{32}$, $d = 10$ and $k = 2$, it is $12 \cdot 61 + 32 = 764$ bits. An IBLT sends a constant factor more, since each of its $c\,d$ cells holds a count and a check field besides the keySum, but it decodes in linear time.

**Computation.** Bob's work for characteristic polynomials is dominated by solving an $\bar m \times \bar m$ system, $O(\bar m^3)$ field operations with Gaussian elimination, and by root finding, which takes expected time polynomial in $\bar m$ and $\log p$. IBLT decoding takes $O(d)$ hash computations after building the tables.

## Reductions

- **To syndrome decoding.** Write $A$ and $B$ as characteristic vectors in $\{0, 1\}^u$. Their Hamming distance is $d$. If Alice sends the syndrome $H \chi_A$ of a linear code that corrects $d$ errors, Bob computes $H \chi_A - H \chi_B = H(\chi_A - \chi_B)$, the syndrome of an error pattern of weight $d$, and decodes it to find $A \triangle B$. Characteristic polynomial evaluation is such a syndrome for a Reed-Solomon-like code, and the message has $d$ symbols, as for any code that corrects $d$ errors with $d$ check symbols over a large alphabet.
- **To rational function interpolation.** The characteristic polynomial method reduces reconciliation to finding the rational function $P/Q$ of known degree bounds from its values, a form of [polynomial interpolation](/polynomial-interpolation/), followed by root finding.
- **From key-value reconciliation.** Hash each (key, value) pair to an element; reconciling the sets of pairs finds the keys whose values differ. This is what an anti-entropy session needs.

## Applications

- **Replica repair.** [Anti-entropy](/anti-entropy/) in replicated stores, where two replicas are usually almost equal, and the cost of a session should depend on how much they differ.
- **Device synchronization.** Minsky, Trachtenberg and Zippel motivated the problem by synchronizing handheld devices with a desktop over a slow link.
- **Peer-to-peer systems and deduplication.** Eppstein et al. name finding the blocks that two hosts both have before a transfer, and synchronizing routing tables and databases.
- **Gossip.** Pairwise reconciliation between random peers spreads updates to all peers in $O(\log n)$ rounds; see [Scuttlebutt reconciliation](/scuttlebutt-reconciliation/) for a version that exchanges version summaries.

## References
