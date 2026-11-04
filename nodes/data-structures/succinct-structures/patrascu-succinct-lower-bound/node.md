---
tag: 5MWV2R
kind: theorem
slug: patrascu-succinct-lower-bound
name: Pătraşcu's lower bounds for succinct data structures
aliases:
- succincter lower bounds
area: data-structures/succinct-structures
level: research
summary: Lower bounds showing that rank and select structures with little extra space must pay a matching query-time cost.
prereqs: [cell-probe-model, rank-select-problem, rank-select-dictionary, source-coding-theorem]
see_also: [bit-probe-model, succinct-data-structures, rrr-bitvector, fully-indexable-dictionary, jacobson-rank, kraft-inequality, binomial-coefficient, succinct-permutation]
sources:
  - paper: doi:10.1137/1.9781611973075.11
    title: Mihai Pătraşcu and Emanuele Viola, Cell-probe lower bounds for succinct partial sums, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA 2010), 117-122
    locator: the main theorem, redundancy n / w^{O(t)} for rank with t probes, and its extension to select and to sparse arrays
  - paper: doi:10.1109/FOCS.2008.83
    title: Mihai Pătraşcu, Succincter, 49th Annual Symposium on Foundations of Computer Science (FOCS 2008), 305-313
    locator: the upper bound n + n / (w / t)^t + O(n^{3/4}) bits for rank and select in O(t) time, by recursive spillover representations
  - paper: doi:10.1016/j.tcs.2007.07.041
    title: Alexander Golynski, Optimal lower bounds for rank and select indexes, Theoretical Computer Science 387(3), 2007, 348-359
    locator: the systematic lower bound, an index of Omega(n lg t / t) bits when a query reads t bits of the plain bit vector
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4 (Bitvectors), the bibliographic notes on lower bounds for rank and select
---

Pătraşcu's lower bounds say how much extra space a [rank and select](/rank-select-problem/) structure must use for a given query time. A bit vector of $n$ bits needs $n$ bits; a structure that uses $n + r$ bits has *redundancy* $r$. Pătraşcu showed in "Succincter" (FOCS 2008) that rank and select can be answered in $O(t)$ time with redundancy $n / (w / t)^t$, plus a lower-order term, on words of $w$ bits. Pătraşcu and Viola proved in 2010 that this is essentially the best possible in the [cell-probe model](/cell-probe-model/): any structure that answers rank with $t$ probes must have redundancy $n / w^{O(t)}$. So the redundancy can fall exponentially in $t$ but no faster, and constant time forces redundancy $n / \text{polylog}\, n$. This page states both results, and proves in full a simpler bound of the same form for structures that keep the bit vector in plain form.

## Statement

Let $A \in \{0, 1\}^n$ and $\text{rank}(i) = A[0] + \cdots + A[i-1]$. A *cell-probe structure* stores $A$ in cells of $w$ bits, for a total of $n + r$ bits, and answers a query by reading (probing) cells, each choice depending on the query and the contents read so far; only probes are counted.

**Theorem 1 (Pătraşcu and Viola, 2010).** If a cell-probe structure with cells of $w$ bits stores every $A \in \{0,1\}^n$ in $n + r$ bits and answers every rank query with at most $t$ probes, then

$$r \ge \frac{n}{w^{O(t)}}.$$

The same holds for select queries.

**Theorem 2 (Pătraşcu, 2008).** On the word RAM with $w = \Theta(\lg n)$, for any $t$, there is a structure for rank and select on $A$ with $O(t)$ query time in

$$n + \frac{n}{(w / t)^{t}} + \tilde{O}(n^{3/4}) \text{ bits.}$$

**Proposition 3 (a systematic version, proved below).** Suppose $A$ is stored verbatim, next to an index of $r$ bits, and $\text{rank}(i)$ is computed by reading the whole index for free and at most $t$ bits of $A$, chosen adaptively. Then, for every $n$,

$$r \ge 2 \left\lfloor \frac{n}{2^{2t+4}} \right\rfloor.$$

## In plain words

You can store a long row of bits with extra notes that let you count the 1s before any position quickly. The question is how small the notes can be. If you may read more pieces of memory per question, the notes can be smaller; Pătraşcu found a way where each extra read divides the size of the notes by a large factor.

The lower bound says nothing better is possible. Counting 1s really does require information beyond the bits themselves, and each read of memory can only buy a limited amount of it. So the notes can shrink fast as reads grow, but never to nothing.

## Proof

**Proof of Proposition 3, in full.** The proof is an encoding argument: a structure with a small index would let us write every bit vector in fewer than $n$ bits each, which is impossible.

Let $b = 2^{2t+4}$, which is even, and $k = \lfloor n / b \rfloor$; if $k = 0$ there is nothing to prove. Cut $A$ into blocks $A_1, \ldots, A_k$ of $b$ bits, followed by a tail of $n - kb$ bits. Let $c_j$ be the number of 1s in $A_j$, and $R_j = \text{rank}(jb) = c_1 + \cdots + c_j$, with $R_0 = 0$.

*The code.* Encode $A$ as the concatenation of:

1. the $r$ bits of the index $I$ built for $A$;
2. for $j = 1, \ldots, k$ in order, the values of the at most $t$ bits of $A$ that the query $\text{rank}(jb)$ reads, in the order it reads them;
3. for $j = 1, \ldots, k$, the index of $A_j$ among the $\binom{b}{c_j}$ strings of length $b$ with $c_j$ ones, in $\lceil \lg \binom{b}{c_j} \rceil$ bits;
4. the tail, verbatim.

*Decoding.* Read $I$, of known length $r$. For $j = 1, \ldots, k$, run the query algorithm for $\text{rank}(jb)$ with index $I$; each time it asks for a bit of $A$, take the next bit of part 2. The algorithm makes the same requests as on $A$, because it sees the same index and the same answers, so it outputs $R_j$, and it also tells when its requests end. Then $c_j = R_j - R_{j-1}$ is known, so the length $\lceil \lg \binom{b}{c_j} \rceil$ of the next field of part 3 is known, and $A_j$ is recovered. The tail has known length $n - kb$. So the decoder recovers $A$ and also finds where the code ends: the code is injective and *prefix-free*.

*Length.* Write $b = 2m$, so $m = 2^{2t+3}$. Every binomial coefficient $\binom{b}{c}$ is at most $\binom{2m}{m}$, and $\binom{2m}{m} \le 4^m / \sqrt{3m + 1}$ by induction on $m$. It holds for $m = 0$. For the step, $\binom{2m+2}{m+1} = \binom{2m}{m} \cdot 2(2m+1)/(m+1)$, so it suffices that $(2(2m+1)/(m+1))^2 \le 16(3m+1)/(3m+4)$, that is, $(2m+1)^2 (3m+4) \le 4(m+1)^2(3m+1)$. Expanding, the left side is $12m^3 + 28m^2 + 19m + 4$ and the right side is $12m^3 + 28m^2 + 20m + 4$.

Since $3m + 1 > 2m = b$, this gives $\lg \binom{b}{c_j} < b - \frac12 \lg b = b - t - 2$. The right side is an integer, so $\lceil \lg \binom{b}{c_j} \rceil \le b - t - 2$. Each block thus costs at most $t$ bits in part 2 and $b - t - 2$ bits in part 3, and the code of every $A$ has length

$$L(A) \le r + k(b - 2) + (n - kb) = r + n - 2k.$$

*Contradiction unless $r$ is large.* The code is prefix-free, so by the [Kraft inequality](/kraft-inequality/) $\sum_A 2^{-L(A)} \le 1$. If every $L(A)$ were at most $n - 1$, the sum over the $2^n$ vectors would be at least $2^n \cdot 2^{-(n-1)} = 2$. So some $A$ has $L(A) \ge n$, and then $r + n - 2k \ge n$, that is, $r \ge 2k = 2\lfloor n / 2^{2t+4} \rfloor$. $\blacksquare$

The same argument says more: by the [source coding theorem](/source-coding-theorem/), the *average* of $L(A)$ over uniform $A$ is at least $n$, so the bound holds even if only the expected index length is counted.

**Outline of Theorem 1.** The cell-probe bound is much harder, because a structure that is not systematic can store $A$ in any form, and each probe returns $w$ bits rather than one. Pătraşcu and Viola take $A$ uniformly random and consider rank queries at well-spaced positions. Because the space exceeds the entropy of $A$ by only $r$ bits, the contents of the memory are close to uniform, and the cells read by one query reveal little about most of the input. On the other hand, a rank answer at the end of a stretch of $\ell$ random bits has about $\frac12 \lg \ell$ bits of entropy given everything before the stretch, much like the binomial bound above. An inductive argument over the $t$ probes, in which each probe can gain at most a factor of about $w$ in the relevant advantage, shows that unless $r \ge n / w^{O(t)}$, some query cannot output the correct answer. We do not reproduce the details; see their paper.

**Outline of Theorem 2.** Pătraşcu's construction stores $A$ by recursive "spillover" representations: each block of the input is encoded into a number of whole words plus a small *spill* in a range that is not a power of two, and the spills of $B$ neighbours are combined, with an index, into the next level. Each of the $t$ levels of recursion reduces the redundancy by a factor of about $w / t$, and a query decodes one path of length $O(t)$.

## Consequences

- **Constant time costs $n / \text{polylog}\, n$ bits.** With $t = O(1)$ and $w = \Theta(\lg n)$, Theorem 1 gives $r \ge n / \lg^{O(1)} n$, and Theorem 2 achieves $n / \lg^c n$ for any constant $c$. So the $o(n)$ redundancy of [Jacobson](/jacobson-rank/) and of the [rank/select dictionary](/rank-select-dictionary/) can be made $n / \lg^c n$, and no $O(1)$-time structure gets, say, $\sqrt{n}$ redundancy.
- **The trade-off is exponential.** Each extra probe can divide the redundancy by a factor polynomial in $w$, no more and, by Theorem 2, also no less.
- **Systematic structures are weaker.** For structures that keep $A$ verbatim, Golynski proved that the index needs $\Omega(n \lg t / t)$ bits when $t$ bits of $A$ are read, which for $t = O(\lg n)$ is $\Omega(n \lg \lg n / \lg n)$. This matches the classical indexes, and it shows that the much smaller redundancies of Theorem 2 need $A$ to be encoded, not stored plainly.
- **Compressed structures.** The bounds extend to sparse arrays, so the redundancy over $\lg \binom{n}{m}$ of [RRR](/rrr-bitvector/)-type and [fully indexable dictionaries](/fully-indexable-dictionary/) is also subject to an exponential trade-off.
- **Trees and sequences.** Since rank reduces to many succinct tree and sequence operations, their redundancies face the same limit.

## Tightness

Theorems 1 and 2 match up to the constant in the exponent: the upper bound is $n / (w / t)^{t}$ and the lower bound $n / w^{O(t)}$, which coincide in form for $t \le w^{1 - \varepsilon}$. Proposition 3 is weaker than Golynski's systematic bound, $\Omega(n \lg t / t)$, by an exponential factor in $t$; it is included because its proof is short and complete, and it already shows that no systematic structure can have redundancy $o(n / 2^{2t})$. For rank in $O(1)$ time, the remaining gap is in the constant of the exponent of $\lg n$.

## History

Jacobson (1989) and Clark (1996) gave the first $o(n)$-redundancy rank and select structures. Miltersen (2005) and Golynski (2007) proved lower bounds for systematic indexes, the latter optimal. Gál and Miltersen (2003) proved the first cell-probe lower bounds on the redundancy of succinct structures, for polynomial evaluation. Pătraşcu's "Succincter" at FOCS 2008, which won the best student paper award, gave the exponential trade-off as an upper bound, and Pătraşcu and Viola proved the matching cell-probe lower bound at SODA 2010.

## References
