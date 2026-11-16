---
tag: 4SQQ4V
kind: concept
slug: decision-tree-complexity
name: Decision tree complexity
aliases:
- D(f)
- deterministic query complexity
area: complexity/communication-and-query-complexity
level: advanced
summary: "The depth D^dt(f) of the shallowest deterministic decision tree that computes a Boolean function f, that is, its worst-case number of queries. For total f it is at most C_0(f) C_1(f)."
prereqs: [query-model, decision-tree-model]
see_also: [query-complexity, certificate-complexity, block-sensitivity, randomized-query-complexity, sensitivity-theorem, adversary-argument, decision-tree-method, deterministic-communication-complexity]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 5.1 (D(f) at most C_0(f) C_1(f), D(f) at most C_1(f) bs(f), D(f) at most bs(f)^3)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees (decision tree complexity, certificate complexity and the bound D at most C_0 C_1)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (the bound D(f) at most C_1(f) bs(f) for total f)
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (C(f) at most s(f) bs(f))
  - paper: "Gábor Tardos, Query complexity, or why is it difficult to separate NP^A ∩ coNP^A from P^A by random oracles A?, Combinatorica 9(4), 385 to 392, 1989"
    locator: the bound on deterministic query complexity by the product of the two certificate complexities
  - paper: "Manuel Blum and Russell Impagliazzo, Generic oracles and oracle classes, 28th IEEE Symposium on Foundations of Computer Science (FOCS 1987), 118 to 126"
    locator: the bound D at most C_0 C_1, as credited in Buhrman and de Wolf, Section 5.1
  - paper: "Juris Hartmanis and Lane A. Hemachandra, One-way functions, robustness and non-isomorphism of NP-complete sets, 2nd Structure in Complexity Theory Conference (1987), 160 to 174"
    locator: the bound D at most C_0 C_1, as credited in Buhrman and de Wolf, Section 5.1
---

Decision tree complexity is the deterministic measure of [query complexity](/query-complexity/). For a Boolean function $f$, it is the depth of the shallowest decision tree that computes $f$, which is the number of input bits that the best deterministic algorithm reads on its worst input. We write it $D^{dt}(f)$, with the superscript that keeps it apart from the communication measure $D^{cc}$. The [decision tree model](/decision-tree-model/) page defines the trees and the model in general, with any kind of query; the [query model](/query-model/) page fixes the queries to single input bits; this page defines the measure and proves the main bounds on it.

## In plain words

You must find out a yes or no fact about a hidden row of bits. You may look at one bit at a time, and you may choose the next bit from what you saw. Your plan is a tree: the first bit to look at, then a next bit for each answer, and so on, with an answer at each end. Decision tree complexity is the length of the longest path in the best plan, that is, the number of looks that the best plan needs in its worst case. Some facts need every bit. Others need only a few looks whatever the row is. A good way to find the cost is to ask how short a proof of each answer can be: if both answers always have short proofs, then a plan with few looks exists.

## The idea

**Definition.** Let $f : \{0,1\}^n \to \{0,1\}$ be total. A decision tree with bit queries **computes** $f$ when the leaf that each input $x$ reaches is labeled $f(x)$. Then

$$D^{dt}(f) = \min \{ \operatorname{depth}(T) : T \text{ computes } f \}.$$

The depth is the largest number of queries on a root-to-leaf path. The same number arises from a recursion on restrictions. A **restriction** fixes some of the bits; $f|_{x_i = b}$ is $f$ with bit $i$ fixed to $b$. Then $D^{dt}(f) = 0$ if $f$ is constant, and otherwise

$$D^{dt}(f) = 1 + \min_{i} \max_{b \in \{0,1\}} D^{dt}(f|_{x_i = b}).$$

The root of a best tree queries the best $i$, and the two subtrees are best trees for the two restrictions. A function on $n$ bits has $3^n$ restrictions (each bit is 0, 1 or free), so dynamic programming over them computes $D^{dt}(f)$ exactly in time $3^n$ times a factor polynomial in $2^n$. This is fast enough for $n$ up to about 10, and it gave the exact values in the examples below.

**Simple bounds.** Always $D^{dt}(f) \le n$. A tree of depth $d$ has at most $2^d - 1$ inner nodes, so it reads at most $2^d - 1$ different bits. If $f$ depends on all $n$ bits, every bit must appear in the tree, so $D^{dt}(f) \ge \log_2 (n + 1)$. The address function below shows that this can be close to the truth.

**Lower bounds.** Each of these is at most $D^{dt}(f)$: the [certificate complexity](/certificate-complexity/) $C(f)$, the [block sensitivity](/block-sensitivity/) $\mathrm{bs}(f)$, the [sensitivity](/sensitivity/) $\mathrm{s}(f)$ and the degree $\deg(f)$ of $f$ as a real polynomial. The proofs are on the [query complexity](/query-complexity/) page. The direct method is an [adversary argument](/adversary-argument/): an adversary answers each query so that the value of $f$ stays open as long as possible. If it stays open for $k$ queries, then $D^{dt}(f) > k$. A function with $D^{dt}(f) = n$ is called **evasive**. OR, AND, PARITY and MAJORITY are evasive; the [decision tree model](/decision-tree-model/) page discusses evasive graph properties.

**Theorem 1 (certificates).** For every total $f$, $D^{dt}(f) \le C_0(f) \, C_1(f)$. Here $C_1(f)$ is the largest size of a smallest certificate of a 1-input, and $C_0(f)$ the same for 0-inputs.

*Proof.* A 0-certificate (a partial assignment that forces $f = 0$) and a 1-certificate cannot both hold for one input. So any 0-certificate and any 1-certificate fix some common bit to different values. The algorithm works in rounds. At the start of a round, if $f$ is constant on all inputs that agree with the answers so far, it outputs that constant. Otherwise some 1-input agrees with the answers, and its smallest certificate $A$ agrees with the answers too. The algorithm queries all bits of $A$ that are not yet queried, at most $C_1(f)$ bits.

Take any 0-input $x$ that agrees with all answers after a round, and let $S$ be its smallest certificate, with at most $C_0(f)$ bits. $S$ and the certificate $A$ of this round conflict on some bit $v$. Bit $v$ was not queried before this round, because both $S$ and $A$ agreed with the answers before it. So $v$ is queried in this round, and the answer agrees with $x$, because $x$ agrees with all answers. So each round queries at least one new bit of $S$, for as long as $x$ stays consistent. After $C_0(f)$ rounds, either no 0-input is consistent, so $f = 1$ on the consistent inputs, or some consistent 0-input $x$ has all bits of its certificate $S$ queried, and then every consistent input agrees with $x$ on $S$ and has value 0. In both cases the algorithm stops, after at most $C_0(f) \, C_1(f)$ queries. $\square$

**Theorem 2 (block sensitivity).** For every total $f$, $D^{dt}(f) \le C_1(f) \, \mathrm{bs}(f)$. With $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f) \le \mathrm{bs}(f)^2$ (Nisan 1991), this gives $D^{dt}(f) \le \mathrm{bs}(f)^3$.

*Proof.* Use the same rounds as in Theorem 1. Suppose that the algorithm starts round $k + 1$. Then $f$ is not constant on the consistent inputs, so there is a consistent 0-input $x$ and a consistent 1-input $z$. For each earlier round $i \le k$ with certificate $A_i$, let $B_i$ be the set of bits of $A_i$ where $x$ differs from $A_i$. The set $B_i$ is not empty: if $x$ agreed with all of $A_i$, then $f(x) = 1$. Also $B_i$ contains only bits first queried in round $i$, because $A_i$ and $x$ both agree with the answers before round $i$. So $B_1, \ldots, B_k$ are disjoint, and $f(x^{B_i}) = 1$ because $x^{B_i}$ agrees with $A_i$. Let $B$ be the set of bits where $z$ differs from $x$. These bits are all unqueried, so $B$ is disjoint from every $B_i$, and $f(x^B) = f(z) = 1$. So $x$ has $k + 1$ disjoint sensitive blocks, and $k + 1 \le \mathrm{bs}(f)$. The algorithm thus runs at most $\mathrm{bs}(f)$ rounds of at most $C_1(f)$ queries each. $\square$

**Other upper bounds.** In terms of the other measures, $D^{dt}(f) \le 27 R(f)^3$ (see [randomized query complexity](/randomized-query-complexity/)) and $D^{dt}(f) = O(Q(f)^4)$ (Aaronson, Ben-David, Kothari, Rao and Tal 2021). All these hold only for total functions. For a partial function, the promise can remove the inputs that make certificates large.

## Examples

**Majority of 3 bits.** Query $x_1$ and $x_2$. If they are equal, output their value; otherwise query $x_3$ and output it. The depth is 3. An adversary that answers 0 and then 1 keeps the value open until the third query, so $D^{dt}(\mathrm{MAJ}_3) = 3$. In general $D^{dt}(\mathrm{MAJ}_n) = n$, while $C(\mathrm{MAJ}_n) = (n + 1)/2$ for odd $n$: a certificate shows $(n+1)/2$ equal bits.

**OR of ANDs.** Let $f$ be the OR of $k$ ANDs, each on its own $k$ bits, so $n = k^2$. A 1-certificate is one AND block of all ones, so $C_1(f) = k$. A 0-certificate is one zero in each block, so $C_0(f) = k$. Theorem 1 gives $D^{dt}(f) \le k^2 = n$, and the exact search gives $D^{dt}(f) = 4$ for $k = 2$ and $D^{dt}(f) = 9$ for $k = 3$. So Theorem 1 is tight, and $D^{dt}$ can be the square of $C$.

**Address function.** Take $k$ address bits $a$ and $2^k$ data bits $y_0, \ldots, y_{2^k - 1}$, and let $f(a, y) = y_a$. A tree reads the $k$ address bits, then one data bit, so $D^{dt}(f) \le k + 1$, while $n = k + 2^k$. Here $f$ depends on every bit, and $D^{dt}$ is close to the lower bound $\log_2(n + 1)$. For $k = 2$, $n = 6$, and the exact search gives $D^{dt}(f) = C(f) = \mathrm{bs}(f) = \mathrm{s}(f) = 3$.

**Exact values.** The dynamic program gives these depths. Each row also lists $C_0$ and $C_1$, to compare with Theorem 1.

| function | $n$ | $C_0$ | $C_1$ | $\mathrm{bs}$ | $D^{dt}$ |
|---|---|---|---|---|---|
| OR | 5 | 5 | 1 | 5 | 5 |
| PARITY | 5 | 5 | 5 | 5 | 5 |
| MAJORITY | 7 | 4 | 4 | 4 | 7 |
| OR of 2 ANDs of 2 | 4 | 2 | 2 | 2 | 4 |
| OR of 3 ANDs of 3 | 9 | 3 | 3 | 3 | 9 |
| address, $k = 2$ | 6 | 3 | 3 | 3 | 3 |

For MAJORITY on 7 bits, $C_0 C_1 = 16$ and $C_1 \, \mathrm{bs} = 16$, far above the true value 7. The bounds are tight only for some functions.

## Where it is used

- It is the base measure of [query complexity](/query-complexity/). The other measures are compared with it, and the [sensitivity theorem](/sensitivity-theorem/) is a statement about how far below $D^{dt}$ the sensitivity can be.
- Evasiveness of graph properties asks whether $D^{dt}(f) = n$ for every nontrivial monotone graph property on $n$ vertex pairs; see the [decision tree model](/decision-tree-model/).
- Oracle separations often reduce to a bound on $D^{dt}$. Theorem 1 was found in this setting: it shows that if an oracle problem has short certificates for both answers, then a deterministic machine can solve it with polynomially many queries.
- A tree of depth $d$ gives a two-party protocol with about $2d$ bits for some composed functions; see [deterministic communication complexity](/deterministic-communication-complexity/).
- The [decision tree method](/decision-tree-method/) uses the depth of comparison trees, not bit trees, to bound sorting and searching. The ideas are the same, but the numbers are not comparable, because a comparison reads two whole keys.

## References
