---
tag: 4HDSNQ
kind: concept
slug: nondeterministic-communication-complexity
name: Nondeterministic communication complexity
aliases:
- N(f)
- "N^1(f)"
area: complexity/communication-and-query-complexity
level: advanced
summary: "N^1(f) is the cost of checking a certificate, sent by a prover who sees both inputs, that f(x, y) = 1. Up to 2 bits, it is log2 of the least number of 1-rectangles that cover the 1-entries of M_f."
prereqs: [deterministic-communication-complexity, communication-matrix, np]
see_also: [deterministic-communication-complexity, fooling-set-method, log-rank-lower-bound, equality-problem, disjointness-problem, certificate, co-np, nonnegative-matrix-factorization]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 2, More on Covers (Section 2.1, Covers and Nondeterminism; Section 2.3, Determinism Versus Nondeterminism; Section 2.5, On Rank and Covers)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols (section Rectangle Covers)
  - paper: doi:10.1145/800061.808742
    title: "Alfred V. Aho, Jeffrey D. Ullman and Mihalis Yannakakis, On notions of information transfer in VLSI circuits, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), pages 133-139"
    locator: the bound of the deterministic cost by the product of the two nondeterministic costs
---

Nondeterministic communication complexity measures how many bits two players need to check a proof that $f(x, y) = 1$, when the proof comes from a prover who sees both inputs. The measure $N^1(f)$ is the least cost of such a protocol, and $N^0(f) = N^1(1 - f)$ is the cost of proving $f(x, y) = 0$; both equal, up to rounding, $\log_2$ of the least number of monochromatic rectangles that cover the 1-entries or the 0-entries of the [communication matrix](/communication-matrix/). Nondeterminism can be much cheaper than determinism on one side, as for non-equality, but Aho, Ullman and Yannakakis (1983) showed that the [deterministic cost](/deterministic-communication-complexity/) is at most $O(N^0(f) N^1(f))$.

## In plain words

A helper who can see both inputs wants to convince Alice and Bob that the answer is yes. The helper writes a short note that both of them can read. Then Alice and Bob check the note against their own inputs, with a short talk. If the answer is yes, some note must pass the check. If the answer is no, every note must fail.

The cost is the length of the note plus the talk. For some questions the note is very short. To show that two long rows are different, the helper only names one place where they differ, and each person checks their own digit there.

For the opposite question, that the rows are the same, no short note works. So the cost of a yes proof and the cost of a no proof can be very different.

## The idea

**Definition.** A nondeterministic protocol for $f : X \times Y \to \{0,1\}$ is a deterministic protocol $P$ that gets, besides $x$ and $y$, a certificate $z \in \{0,1\}^k$ that both players see. It must satisfy:

- if $f(x, y) = 1$, then $P(x, y, z) = 1$ for some $z$;
- if $f(x, y) = 0$, then $P(x, y, z) = 0$ for every $z$.

The cost is $k$ plus the worst-case number of bits that $P$ sends. $N^1(f)$ is the least cost, and $N^0(f) = N^1(1 - f)$. The analogy is with the class [NP](/np/), where a polynomial-time verifier checks a [certificate](/certificate/); $N^0$ plays the role of [coNP](/co-np/). This site writes $N^1(f)$ and $N^0(f)$, not $N(f)$ alone, so that the side is clear.

**Covers.** A **1-cover** of $f$ is a set of 1-rectangles $A_i \times B_i$, which may overlap, whose union is the set of 1-entries of $M_f$. Let $C^1(f)$ be the least size of a 1-cover, and $C^0(f)$ the same for the 0-entries. Then

$$\log_2 C^1(f) \le N^1(f) \le \lceil \log_2 C^1(f) \rceil + 2.$$

For the upper bound, the prover names a rectangle $i$ of an optimal cover that holds $(x, y)$; Alice sends 1 if $x \in A_i$, and Bob sends 1 if $y \in B_i$. For the lower bound, fix a protocol of cost $c$ and, for each certificate $z$, take the leaves of $P(\cdot, \cdot, z)$ that accept; these leaf rectangles are 1-rectangles, there are at most $2^c$ of them in all, and they cover every 1-entry. Kushilevitz and Nisan define $N^1(f) = \log_2 C^1(f)$, which differs from the protocol cost by at most 2 bits.

**Lower bounds.** A 1-[fooling set](/fooling-set-method/) of size $s$ gives $C^1(f) \ge s$, since its proof never uses that the rectangles are disjoint. The rectangle size method also works: if every 1-rectangle holds at most a fraction $\delta$ of the 1-entries under some distribution, then $C^1(f) \ge 1/\delta$. The [log-rank lower bound](/log-rank-lower-bound/) does not apply, because a cover may overlap: non-equality has rank $2^n$ but a 1-cover of size $2n$.

**Relation to determinism.** Every deterministic protocol is a nondeterministic one with an empty certificate, and its leaves give a 1-cover and a 0-cover, so $N^1(f), N^0(f) \le D^{cc}(f)$. In the other direction:

- **Aho, Ullman and Yannakakis (1983).** $D^{cc}(f) = O(N^0(f) \cdot N^1(f))$. The protocol uses the fact that a 1-rectangle and a 0-rectangle have no common entry, so they share no row or share no column. In each round, the players use $O(N^1(f))$ bits to name a rectangle of the 1-cover that removes at least half of the 0-rectangles that can still hold the input, or to stop. After $O(N^0(f))$ rounds, the answer is known.
- **Yannakakis (1991).** $D^{cc}(f) = O(\log^2 \chi_1(f))$, where $\chi_1(f)$ is the least number of disjoint 1-rectangles that partition the 1-entries. Göös, Pitassi and Watson (FOCS 2015) showed that this bound is tight up to polylogarithmic factors.
- So, with the communication classes of Babai, Frankl and Simon, where efficient means a cost polylogarithmic in $n$, $\mathrm{P}^{cc} = \mathrm{NP}^{cc} \cap \mathrm{coNP}^{cc}$. The analogous statement for Turing machines is open.

## Examples

All inputs have $n$ bits.

| Problem | $N^1$ | $N^0$ | $D^{cc}$ |
|---|---|---|---|
| [Equality](/equality-problem/) | $n$ | $\log_2 n + O(1)$ | $n + 1$ |
| [Disjointness](/disjointness-problem/) (1 = disjoint) | $n$ | $\log_2 n + O(1)$ | $n + 1$ |
| [Greater-than](/greater-than-problem/) | $n$ | $n$ | $n + 1$ |
| [Inner product](/inner-product-problem/) | $n - O(1)$ | $n - O(1)$ | $n + 1$ |

**Equality.** The diagonal is a 1-fooling set of size $2^n$, so $C^1(\mathrm{EQ}) = 2^n$ and $N^1(\mathrm{EQ}) = n$. For the 0-entries, the $2n$ rectangles $R_{i,b} = \{x : x_i = b\} \times \{y : y_i \ne b\}$, for $1 \le i \le n$ and $b \in \{0,1\}$, cover every pair with $x \ne y$: take an $i$ where they differ and $b = x_i$. So $C^0(\mathrm{EQ}) \le 2n$. The certificate is $(i, b)$, and the players check $x_i = b$ and $y_i \ne b$. A cover of the 0-entries also needs at least $n$ rectangles, so $N^0(\mathrm{EQ}) = \log_2 n + O(1)$. This is the standard example where $N^0$ is exponentially smaller than $N^1$.

**Disjointness.** To prove that $x$ and $y$ intersect, the prover names an element $i$ with $x_i = y_i = 1$, and both players check their bit: $N^0(\mathrm{DISJ}) \le \lceil \log_2 n \rceil + 2$. To prove that they are disjoint, no short certificate works: the pairs $(A, \bar{A})$ form a 1-fooling set of size $2^n$, so $N^1(\mathrm{DISJ}) = n$.

**Inner product.** Every monochromatic rectangle of $M_{\mathrm{IP}}$ has at most $2^n$ entries, by the bound of Lindsey's lemma on the bias of rectangles of a Hadamard matrix. The 1-entries and the 0-entries each number about $2^{2n-1}$, so each cover needs about $2^{n-1}$ rectangles, and both $N^1$ and $N^0$ are $n - O(1)$.

## Where it is used

- **Bounds on deterministic cost.** The bound $D^{cc}(f) = O(N^0 N^1)$ relates the deterministic cost to two cover problems. The same idea, with rank in place of one of the covers, gives the known upper bounds toward the [log-rank conjecture](/log-rank-conjecture/).
- **Extended formulations.** A nonnegative factorization of a matrix into $r$ nonnegative rank-1 terms gives a cover of its nonzero entries by $r$ rectangles. So $\log_2$ of the nonnegative rank is at least $N^1$ of the support of the matrix, and Yannakakis used this to bound the size of linear programs for polytopes. See [nonnegative matrix factorization](/nonnegative-matrix-factorization/).
- **Circuit complexity.** In the [Karchmer-Wigderson relation](/karchmer-wigderson-relation/), the players search for a coordinate where their inputs differ, as in the certificate for non-equality.
- **Communication classes.** $\mathrm{NP}^{cc}$ and $\mathrm{coNP}^{cc}$, with $\mathrm{P}^{cc} = \mathrm{NP}^{cc} \cap \mathrm{coNP}^{cc}$, are the base of the hierarchy of communication complexity classes.

## References
