---
tag: FKACGJ
kind: concept
slug: deterministic-communication-complexity
name: Deterministic communication complexity
aliases:
- D(f)
- "D^cc(f)"
area: complexity/communication-and-query-complexity
level: core
summary: "D^cc(f) is the least worst-case number of bits that a deterministic two-party protocol sends to compute f(x, y), with both players knowing the answer. It is at most n + 1 for n-bit inputs."
prereqs: [communication-model, communication-matrix]
see_also: [communication-complexity, fooling-set-method, log-rank-lower-bound, log-rank-conjecture, nondeterministic-communication-complexity, randomized-communication-complexity, decision-tree-complexity, equality-problem]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics, and Chapter 2, More on Covers (Section 2.2, Communication Complexity Versus Protocol Cover, and Section 2.3, Determinism Versus Nondeterminism)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols (sections Rectangles, Balancing Protocols, From Rectangles to Protocols and Lower Bounds)
  - paper: doi:10.1145/800135.804414
    title: "Andrew Chi-Chih Yao, Some complexity questions related to distributive computing (preliminary report), Proceedings of the 11th Annual ACM Symposium on Theory of Computing (STOC 1979), pages 209-213"
    locator: the definition of the measure and the first lower bounds
  - paper: doi:10.1145/800061.808742
    title: "Alfred V. Aho, Jeffrey D. Ullman and Mihalis Yannakakis, On notions of information transfer in VLSI circuits, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), pages 133-139"
    locator: the comparison of the lower bound methods and the bound of the deterministic cost by the two cover numbers
  - paper: doi:10.1137/16M1059369
    title: "Mika Göös, Toniann Pitassi and Thomas Watson, Deterministic communication vs. partition number, SIAM Journal on Computing 47(6) (2018), pages 2435-2450 (FOCS 2015)"
    locator: Theorem 1 (a function whose deterministic cost is about the 1.5th power of the log of its partition number)
---

The deterministic communication complexity $D^{cc}(f)$ of a function $f : X \times Y \to Z$ is the least number of bits that a deterministic protocol in the two-party [communication model](/communication-model/) must send, on its worst input, so that both Alice and Bob know $f(x, y)$ at the end. It is the basic measure of [communication complexity](/communication-complexity/): every Boolean function of two $n$-bit inputs has $D^{cc}(f) \le n + 1$, and most lower bounds for it count the monochromatic rectangles of the [communication matrix](/communication-matrix/). The superscript separates it from $D^{dt}(f)$, the depth of the best decision tree in the [query model](/query-model/); this site never writes $D(f)$ alone.

## In plain words

Alice and Bob follow a fixed plan to find an answer that depends on both of their inputs. The plan says who speaks and what they say, based only on their own input and on what was said before. Nothing is left to chance and the answer must always be right.

The measure is the length of the longest talk that the best plan ever needs. One plan always works: Alice says her whole input, and Bob says the answer. So the measure is never more than the length of Alice's input plus one.

The hard part is to show that no plan can be shorter. The usual proof looks at what a short talk can tell apart. A short talk has few possible endings, and inputs that end the same way must all have the same answer. If the inputs need many different endings, the talk must be long.

## The idea

**Definition.** A deterministic protocol $P$ is a binary tree whose inner nodes belong to Alice or Bob and send a bit that depends only on the owner's input, and whose leaves hold outputs. Its cost is its depth. The protocol computes $f$ if every input pair $(x, y)$ reaches a leaf with output $f(x, y)$. Then

$$D^{cc}(f) = \min \{ \operatorname{depth}(P) : P \text{ computes } f \}.$$

Both players know the output, because both see the whole transcript. If only Bob must know it, the cost can drop by at most $\lceil \log_2 |Z| \rceil$ bits, which is one bit for Boolean $f$.

**Upper bound.** Alice sends $x$ in $\lceil \log_2 |X| \rceil$ bits, and Bob sends $f(x, y)$ in $\lceil \log_2 |Z| \rceil$ bits. For Boolean $f$ on $\{0,1\}^n \times \{0,1\}^n$ this gives $D^{cc}(f) \le n + 1$. A random 0-1 matrix of size $2^n \times 2^n$ has full rank with probability that tends to 1, so by the rank bound below most Boolean functions need at least $n$ bits. The trivial bound is close to tight for a typical function.

**Rectangles.** The inputs that reach a node form a combinatorial rectangle $A \times B$. The leaves of a protocol of cost $c$ cut $X \times Y$ into at most $2^c$ monochromatic rectangles. If $\chi(f)$ is the least number of monochromatic rectangles in a partition of $X \times Y$, the partition number, then

$$D^{cc}(f) \ge \log_2 \chi(f).$$

Each lower bound method finds a reason why $\chi(f)$ is large.

- The [fooling set method](/fooling-set-method/): a set $S$ of inputs with the same value, no two of which fit in one monochromatic rectangle, gives $D^{cc}(f) \ge \log_2 |S|$.
- The [log-rank lower bound](/log-rank-lower-bound/): each 1-rectangle is a matrix of rank 1, so $\chi(f) \ge \operatorname{rank}(M_f)$ over the reals and $D^{cc}(f) \ge \log_2 \operatorname{rank}(M_f)$.
- The rectangle size bound: if every monochromatic rectangle holds at most a fraction $\delta$ of the input pairs, under some distribution, then $\chi(f) \ge 1/\delta$.

**Partitions against protocols.** Not every partition into rectangles comes from a protocol, but partitions and protocols are close. Aho, Ullman and Yannakakis (1983) showed that $D^{cc}(f) = O(\log^2 \chi(f))$, and in fact $D^{cc}(f) = O(N^0(f) N^1(f))$, where $N^1(f)$ and $N^0(f)$ are the [nondeterministic costs](/nondeterministic-communication-complexity/) of $f$ and of its negation. Göös, Pitassi and Watson (2018) found functions with $D^{cc}(f) \ge \tilde{\Omega}(\log^{1.5} \chi(f))$, so the gap between the partition bound and the cost is real.

**Balancing.** A protocol tree with $\ell$ leaves can be changed into a protocol of depth $O(\log \ell)$ that computes the same function. So the cost is controlled by the number of leaves, not by the shape of the tree.

**Relation to other measures.** For every Boolean $f$,

$$\log_2 \operatorname{rank}(M_f) \le D^{cc}(f) \le O(N^0(f) N^1(f)), \qquad R(f) \le D^{cc}(f),$$

where $R(f)$ is the [randomized communication complexity](/randomized-communication-complexity/). With private coins, $R(f) = \Omega(\log D^{cc}(f))$, so randomness can save at most an exponential factor. For a function of the form $g(x \oplus y)$, each query of a decision tree for $g$ costs two bits, so $D^{cc}(f) \le 2 D^{dt}(g)$.

## Examples

All examples have $X = Y = \{0,1\}^n$ and Boolean output.

- **Parity of all bits.** $f(x, y) = x_1 \oplus \cdots \oplus x_n \oplus y_1 \oplus \cdots \oplus y_n$. Alice sends the parity of $x$, and Bob sends the answer. $D^{cc}(f) = 2$ for $n \ge 1$. One bit is not enough, because $f$ depends on both inputs and both players must learn the answer.
- **Weight threshold.** $f(x, y) = 1$ exactly when $x$ and $y$ have at least $n$ ones together. Alice sends the number of ones in $x$, in $\lceil \log_2(n+1) \rceil$ bits, and Bob sends the answer. So $D^{cc}(f) \le \lceil \log_2(n+1) \rceil + 1$.
- **Equality.** $D^{cc}(\mathrm{EQ}) = n + 1$. The $2^n$ diagonal pairs $(x, x)$ form a fooling set, so the 1-entries need $2^n$ leaves, and the 0-entries need at least one more leaf. A protocol tree with at least $2^n + 1$ leaves has depth at least $n + 1$. See the [equality problem](/equality-problem/).
- **Greater-than, disjointness, inner product.** Each has $D^{cc} = n + 1$, by a fooling set or by rank. See the [greater-than problem](/greater-than-problem/), the [disjointness problem](/disjointness-problem/) and the [inner product problem](/inner-product-problem/).

For $n = 1, 2, 3$, an exhaustive search over all protocol trees, where each node splits the current set of rows or columns in two, gives $D^{cc} = 2, 3, 4$ for each of equality, greater-than, disjointness and inner product. This agrees with $n + 1$.

The worked case $\mathrm{EQ}$ with $n = 2$: $M_{\mathrm{EQ}} = I_4$. Any 1-rectangle holds one diagonal entry, so 4 leaves output 1. At least one leaf outputs 0. A binary tree with 5 leaves has depth at least 3, and the trivial protocol has cost 3, so $D^{cc}(\mathrm{EQ}) = 3$.

## Where it is used

- **Circuit depth.** The depth of the best fan-in 2 circuit for $f$ equals the deterministic cost of its [Karchmer-Wigderson relation](/karchmer-wigderson-relation/). This is the [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/), and deterministic lower bounds for relations give monotone depth lower bounds.
- **VLSI.** Yao's first motive: the bits that must cross the middle of a chip bound its area and time.
- **Lower bounds for randomized protocols.** Since $R(f) = \Omega(\log D^{cc}(f))$ with private coins, a deterministic lower bound of $n$ gives a private-coin lower bound of $\Omega(\log n)$. This is how the private-coin cost of equality is shown to be $\Theta(\log n)$.
- **Query complexity.** Lifting theorems compare $D^{cc}$ of a composed function with the decision tree depth $D^{dt}$ of the outer function, and turn query lower bounds into communication lower bounds. See [decision tree complexity](/decision-tree-complexity/).
- **The log-rank conjecture.** The [log-rank conjecture](/log-rank-conjecture/) asks whether $D^{cc}(f)$ is at most a polynomial in $\log_2 \operatorname{rank}(M_f)$, which would make the rank bound tight up to a polynomial.

## References
