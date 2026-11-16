---
tag: 489076
kind: concept
slug: certificate-complexity
name: Certificate complexity
aliases:
- C(f)
area: complexity/communication-and-query-complexity
level: advanced
summary: "C(f) is the largest, over inputs x, of the fewest bits of x that fix the value f(x). It is the nondeterministic query complexity, and it lies between bs(f) and D^dt(f)."
prereqs: [decision-tree-complexity, certificate]
see_also: [certificate, decision-tree-complexity, block-sensitivity, sensitivity, query-complexity, np, nondeterministic-communication-complexity, adversary-argument]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.1 (certificate complexity), Section 5.1 (D(f) at most C_0(f) C_1(f)), Section 6.2 (monotone functions have C(f) = s(f) = bs(f))
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (minimal sensitive blocks have size at most s(f); C(f) at most s(f) bs(f))
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees (certificate complexity and the bound D at most C_0 C_1)
---

Certificate complexity measures how many bits of an input are enough to prove the value of a Boolean function on it. A certificate for $x$ is a set of positions such that every input that agrees with $x$ there has the same value as $x$. $C(f)$ is the size of the smallest certificate on the worst input. It is the nondeterministic [query complexity](/query-complexity/) of $f$: a prover shows the bits, and a verifier reads only them. This is a different object from a [certificate](/certificate/) in the sense of NP, which is a string checked by a polynomial-time machine; here the certificate is a set of input positions, and only its size counts.

## In plain words

Someone knows a hidden row of bits and wants to convince you of a yes or no fact about it. They may uncover some of the bits for you, and you then check that the fact must hold whatever the other bits are. The fewest bits that they must uncover, on the hardest row, is the certificate complexity. For the fact "some bit is 1", a yes answer needs one bit: the 1. A no answer needs all the bits, because any hidden bit could be a 1. So the two answers can need very different numbers of bits. A plan that must find the answer itself, with no helper, needs at least this many looks, and it never needs more than the product of the two numbers.

## The idea

**Definitions.** Let $f : \{0,1\}^n \to \{0,1\}$ be total, and let $x$ be an input. A set $S \subseteq \{1, \ldots, n\}$ is a **certificate** for $x$ when every $y$ with $y_i = x_i$ for all $i \in S$ has $f(y) = f(x)$. Equivalently, the partial assignment $x|_S$ forces the value of $f$. Then

- $C(f, x)$ is the least size of a certificate for $x$,
- $C_b(f) = \max \{ C(f, x) : f(x) = b \}$ for $b \in \{0, 1\}$, the **0-certificate complexity** and the **1-certificate complexity**,
- $C(f) = \max_x C(f, x) = \max(C_0(f), C_1(f))$.

**Nondeterministic queries.** Consider a verifier that receives a set $S$ from an untrusted prover, queries the bits in $S$, and accepts if the answers force $f = 1$. On a 1-input, an honest prover shows a certificate of size at most $C_1(f)$. On a 0-input, no set of answers forces $f = 1$, so no prover can make the verifier accept. So $C_1(f)$ is the nondeterministic query complexity of $f$, and $C_0(f)$ is that of $1 - f$. In this sense, $C_1$ and $C_0$ are the query analogs of NP and coNP.

**Conflict property.** A 0-certificate and a 1-certificate always fix some common position to different values. Otherwise one input would satisfy both, and it would have both values. All upper bounds on $D^{dt}$ in terms of certificates use this fact.

**Relations.** For every total $f$:

1. $\mathrm{bs}(f) \le C(f) \le D^{dt}(f)$. Each sensitive block of $x$ meets every certificate of $x$, and the bits queried on the path of $x$ in a decision tree form a certificate. See [query complexity](/query-complexity/).
2. $D^{dt}(f) \le C_0(f) \, C_1(f)$. The algorithm queries a consistent 1-certificate in each round, and each round queries a new bit of every 0-certificate that is still consistent. The proof is on the [decision tree complexity](/decision-tree-complexity/) page. This is the query analog of $\mathsf{P} = \mathsf{NP} \cap \mathsf{coNP}$. It is true for queries, and it is open for Turing machines.
3. $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f)$ (Nisan 1991). The proof follows.

**Lemma (Nisan).** Let $B$ be a minimal sensitive block of $x$: $f(x^B) \ne f(x)$, and $f(x^{B'}) = f(x)$ for every proper subset $B' \subset B$. Then $|B| \le \mathrm{s}(f)$.

*Proof.* Let $y = x^B$. For each $i \in B$, the input $y^i$ equals $x^{B \setminus \{i\}}$, so $f(y^i) = f(x) \ne f(y)$ by minimality. So $y$ is sensitive to every $i \in B$, and $|B| \le \mathrm{s}(f, y) \le \mathrm{s}(f)$. $\square$

**Theorem (Nisan).** $C(f, x) \le \mathrm{s}(f) \, \mathrm{bs}(f, x)$ for every $x$, so $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f)$.

*Proof.* Choose minimal sensitive blocks $B_1, \ldots, B_k$ of $x$ that are pairwise disjoint, with $k$ as large as possible. Then $k \le \mathrm{bs}(f, x)$. Let $U = B_1 \cup \cdots \cup B_k$. We show that $U$ is a certificate for $x$. Suppose $y$ agrees with $x$ on $U$ and $f(y) \ne f(x)$. Let $B$ be the set of positions where $y$ and $x$ differ. Then $B$ is sensitive for $x$ and disjoint from $U$. Among the sensitive subsets of $B$, take one that is minimal by inclusion. It is a minimal sensitive block disjoint from $B_1, \ldots, B_k$, which contradicts the choice of $k$. So $U$ is a certificate, and by the lemma $|U| \le k \, \mathrm{s}(f) \le \mathrm{bs}(f, x) \, \mathrm{s}(f)$. $\square$

With $D^{dt}(f) \le C_1(f) \, \mathrm{bs}(f)$ (Beals, Buhrman, Cleve, Mosca and de Wolf), this gives $D^{dt}(f) \le \mathrm{bs}(f)^3$.

**Monotone functions.** If $f$ is monotone (flipping a 0 to 1 never lowers the value), then $C(f) = \mathrm{s}(f) = \mathrm{bs}(f)$. The reason: let $S$ be a smallest certificate of a 1-input $x$. If $S$ fixed some $x_i = 0$, we could drop $i$ from $S$, because raising bits never lowers $f$; so $S$ fixes only ones. Let $z$ have ones exactly on $S$. If flipping some $z_i$ with $i \in S$ kept the value 1, then $S \setminus \{i\}$ would be a smaller certificate of $x$, again by monotonicity. So $z$ is sensitive at every position of $S$, and $\mathrm{s}(f) \ge C_1(f)$. The 0-side is the same with zeros. Together with $\mathrm{s} \le \mathrm{bs} \le C$ this gives equality.

## Examples

**OR on $n$ bits.** A 1-input is certified by one position that holds a 1, so $C_1(\mathrm{OR}) = 1$. The all-zero input needs all $n$ positions, because any unread bit could be 1, so $C_0(\mathrm{OR}) = n$. Here $C_0 C_1 = n = D^{dt}$.

**OR of $k$ ANDs of $k$ bits.** A 1-certificate is one block of $k$ ones, and a 0-certificate is one zero in each of the $k$ blocks. So $C_0 = C_1 = k$, while $D^{dt} = k^2$. A brute-force search for $k = 3$ gives $C = 3$ and $D^{dt} = 9$. This function shows that the bound $D^{dt} \le C_0 C_1$ is tight.

**Graph connectivity.** The input lists which of the $\binom{v}{2}$ possible edges on $v$ vertices are present, and $f = 1$ when the graph is connected. A 1-certificate is a spanning tree, with $v - 1$ edges. A 0-certificate is a cut: a set $X$ of vertices with all edges between $X$ and the rest absent, with $|X| (v - |X|)$ edges. The worst disconnected graph is two equal halves, so $C_0 = \lfloor v/2 \rfloor \lceil v/2 \rceil$. A brute-force count over all graphs agrees:

| $v$ | edges $n$ | $C_0$ | $C_1$ | $\mathrm{s}$ | $D^{dt}$ |
|---|---|---|---|---|---|
| 3 | 3 | 2 | 2 | 2 | 3 |
| 4 | 6 | 4 | 3 | 4 | 6 |
| 5 | 10 | 6 | 4 | 6 | not computed |

Connectivity is monotone, so $C = \mathrm{s}$ in every row, as the theorem on monotone functions says. Here $C_0 C_1$ is larger than $n$, so the product bound says nothing; the exact search shows that connectivity on 3 and 4 vertices is evasive.

**A function with $C_1 < C_0$.** Let $f(x) = 1$ when exactly one or two of three bits are 1. At $x = 100$, the set $\{1, 2\}$ is a certificate: the inputs that agree with $x$ there are $100$ and $101$, and both have value 1. One position is not enough: with only $x_1 = 1$ fixed, the input $111$ has value 0. At the 0-inputs $000$ and $111$, all three bits are needed, because each single flip changes the value. A brute-force search confirms $C_1(f) = 2$ and $C_0(f) = 3$.

## Where it is used

- **Upper bounds on $D^{dt}$.** The bounds $D^{dt} \le C_0 C_1$ and $D^{dt} \le C_1 \, \mathrm{bs}$ turn short proofs into short deterministic algorithms; see [decision tree complexity](/decision-tree-complexity/).
- **Lower bounds.** Since $C \le D^{dt}$, a large certificate on one input gives a lower bound on $D^{dt}$. It does not bound $R$ or $Q$ directly: OR has $C = n$ but $Q(\mathrm{OR}) = \Theta(\sqrt n)$.
- **The sensitivity theorem.** Nisan's bound $C \le \mathrm{s} \, \mathrm{bs}$ is one link in the chain that the [sensitivity theorem](/sensitivity-theorem/) completes.
- **Communication complexity.** The same idea in the two-party setting gives covers by monochromatic rectangles and [nondeterministic communication complexity](/nondeterministic-communication-complexity/). There too, short proofs for both answers give a short deterministic protocol.
- **Oracle results.** The bound $D^{dt} \le C_0 C_1$ was found while studying relativized versions of $\mathsf{P}$ versus $\mathsf{NP} \cap \mathsf{coNP}$; see [NP](/np/).

## References
