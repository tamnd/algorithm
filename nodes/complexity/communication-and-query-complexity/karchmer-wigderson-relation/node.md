---
tag: MRHENN
kind: concept
slug: karchmer-wigderson-relation
name: Karchmer-Wigderson relation
aliases:
- KW game
area: complexity/communication-and-query-complexity
level: research
summary: "For a Boolean function f, Alice gets x with f(x) = 1, Bob gets y with f(y) = 0, and they must find a position i with x_i different from y_i. Its communication cost equals the formula depth of f."
prereqs: [deterministic-communication-complexity, boolean-circuit]
see_also: [karchmer-wigderson-theorem, circuit-complexity, nc, boolean-circuit, parity-problem, majority-problem, graph-reachability, perfect-matching]
sources:
  - paper: doi:10.1137/0403021
    title: "Mauricio Karchmer and Avi Wigderson, Monotone circuits for connectivity require super-logarithmic depth, SIAM Journal on Discrete Mathematics 3(2), 1990, pages 255-265"
    locator: the relation, the monotone relation, the equality of depth and communication, and the Omega(log^2 n) bound for monotone st-connectivity
  - paper: doi:10.1145/146637.146684
    title: "Ran Raz and Avi Wigderson, Monotone circuits for matching require linear depth, Journal of the ACM 39(3), 1992, pages 736-744"
    locator: the Omega(n) bound on the monotone depth of perfect matching, by a reduction from disjointness to the monotone relation
  - paper: doi:10.1007/BF01206317
    title: "Mauricio Karchmer, Ran Raz and Avi Wigderson, Super-logarithmic depth lower bounds via the direct sum in communication complexity, Computational Complexity 5(3/4), 1995, pages 191-204"
    locator: the conjecture on the depth of composed functions and why it would give a function in P that is not in NC1
  - paper: doi:10.1007/s004930050062
    title: "Ran Raz and Pierre McKenzie, Separation of the monotone NC hierarchy, Combinatorica 19(3), 1999, pages 403-435"
    locator: the separation of monotone NC^i from monotone NC^(i+1), by a lifting theorem for the monotone relation
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press (1997)
    locator: Chapter 5, The communication complexity of relations; Chapter 10, Boolean circuit depth (Section 10.2, the connection to communication complexity)
  - book: isbn:9783642245077
    title: Stasys Jukna, Boolean Function Complexity, Advances and Frontiers, Springer (2012)
    locator: Chapter 3, Games on relations (Section 3.3, games and circuit depth); Chapter 6, Formulas (Section 6.7, formulas and rectangles; Section 6.8, Khrapchenko's theorem)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press (2020)
    locator: Chapter 9, Circuits and Proofs
---

The Karchmer-Wigderson relation of a Boolean function $f$ is a communication problem that captures the formula depth of $f$. Alice gets an input $x$ with $f(x) = 1$, Bob gets an input $y$ with $f(y) = 0$, and they must agree on a position $i$ where $x_i \ne y_i$. Such a position always exists, because $x \ne y$. The problem is a **relation**, not a function: there can be many correct answers, and any one of them is fine. Karchmer and Wigderson proved that the deterministic communication cost of this relation equals the least depth of a fan-in-2 AND/OR formula for $f$, and that the least number of leaves of a protocol equals the least formula size. This is the [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/); this page defines the relation and shows how it is used.

## In plain words

Alice holds a string that makes a test say yes. Bob holds a string that makes the same test say no. So the two strings differ somewhere, and the players must find one place where they differ. They pay one unit for each bit they send. This game is tied to circuits. A circuit made of AND and OR gates that computes the test gives a strategy: start at the top gate and walk down to an input. At an OR gate Alice says which branch is true for her string; at an AND gate Bob says which branch is false for his. They end at a place where the strings differ. The number of bits is the depth of the circuit. The other direction also holds, so to show that a test needs deep circuits it is enough to show that this game needs many bits.

## The idea

Let $f : \{0,1\}^n \to \{0,1\}$ be non-constant. The **Karchmer-Wigderson relation** of $f$ is

$$\mathrm{KW}_f = \{ (x, y, i) : f(x) = 1, \; f(y) = 0, \; x_i \ne y_i \} .$$

A protocol for $\mathrm{KW}_f$ is a protocol tree in the two-party [communication model](/communication-model/) whose leaves are labelled with positions. It is correct if, for every $x \in f^{-1}(1)$ and $y \in f^{-1}(0)$, the leaf that $(x, y)$ reaches holds a position $i$ with $x_i \ne y_i$. Write $D^{cc}(\mathrm{KW}_f)$ for the least depth of a correct protocol, as for [deterministic communication complexity](/deterministic-communication-complexity/) of functions.

For a **monotone** $f$, that is, $x \le y$ coordinatewise implies $f(x) \le f(y)$, the monotone relation asks for more:

$$\mathrm{KW}^{+}_f = \{ (x, y, i) : f(x) = 1, \; f(y) = 0, \; x_i = 1, \; y_i = 0 \} .$$

Such an $i$ exists: if there were none, then $x \le y$, and monotonicity would give $f(x) \le f(y)$. The cost $D^{cc}(\mathrm{KW}^{+}_f)$ equals the least depth of a monotone formula, with no negations, for $f$.

**Rectangles.** As for functions, the inputs that reach one leaf form a rectangle $A \times B$ with $A \subseteq f^{-1}(1)$ and $B \subseteq f^{-1}(0)$. The leaf can answer $i$ only if $x_i \ne y_i$ for all $x \in A$ and $y \in B$, which forces $x_i$ to be one constant $c$ on all of $A$ and $y_i = 1 - c$ on all of $B$. So a protocol with $L$ leaves splits $f^{-1}(1) \times f^{-1}(0)$ into $L$ rectangles of this kind, and lower bounds on the number of such rectangles are lower bounds on formula size. Khrapchenko's bound is of this type: if $E$ is the set of pairs $(x, y) \in A \times B$ at Hamming distance 1, then every formula that is 1 on $A$ and 0 on $B$ has at least $|E|^2/(|A||B|)$ leaves.

**Formula depth and circuit depth.** For fan-in 2, a circuit of depth $d$ unfolds into a formula of the same depth, with at most $2^d$ leaves. So the relation measures circuit depth, and $D^{cc}(\mathrm{KW}_f) = O(\log n)$ for a family $f$ exactly when $f$ is in non-uniform [NC1](/nc/).

## Examples

**Parity by binary search.** Let $f$ be the parity of $n$ bits. Alice's $x$ has odd weight and Bob's $y$ has even weight, so the parities of $x$ and $y$ differ on the whole interval $[1, n]$. Keep an interval on which the parities differ. Alice sends the parity of $x$ on the left half and Bob sends the parity of $y$ on the left half. If these differ, keep the left half; if not, the right half must differ, so keep it. Each round costs 2 bits and halves the interval. For $n = 8$, $x = 10110101$ (weight 5) and $y = 10011100$ (weight 4):

| Interval | Alice's left parity | Bob's left parity | Next |
|---|---|---|---|
| positions 1 to 8 | 1 | 0 | left half, 1 to 4 |
| positions 1 to 4 | 1 | 1 | right half, 3 to 4 |
| positions 3 to 4 | 1 | 0 | left half, 3 |

The answer is $i = 3$, with $x_3 = 1$ and $y_3 = 0$, after $6 = 2\log_2 8$ bits. In general this protocol has $2\log_2 n$ bits and $n^2$ leaves, so parity has a formula of depth $2\log_2 n$ and size $n^2$. Khrapchenko's bound, with $A$ the odd strings and $B$ the even strings, gives $|E| = n 2^{n-1}$ and $|A| = |B| = 2^{n-1}$, so size at least $n^2$; for $n$ a power of 2, this protocol is optimal.

**Majority of three bits from a formula.** Take the formula $F = (x_1 \wedge x_2) \vee (x_3 \wedge (x_1 \vee x_2))$ for $\mathrm{MAJ}_3$, and let $x = 011$ and $y = 100$. At the top OR gate, Alice says which child is 1 on $x$: the left child is $0 \wedge 1 = 0$ and the right child is $1 \wedge 1 = 1$, so she says "right". At the AND gate $x_3 \wedge (x_1 \vee x_2)$, Bob says which child is 0 on $y$: $y_3 = 0$, so he says "left". The leaf is $x_3$, and indeed $x_3 = 1$ and $y_3 = 0$. This run used 2 bits; the worst case is the depth of $F$, which is 3.

**All functions on three variables.** A search over all protocols and all formulas for $n = 3$ gives the following values, with formula size counted in leaves:

| $f$ | least depth | $D^{cc}(\mathrm{KW}_f)$ | least size | least protocol leaves |
|---|---|---|---|---|
| $x_1 \wedge x_2 \wedge x_3$ | 2 | 2 | 3 | 3 |
| $x_1 \oplus x_2$ | 2 | 2 | 4 | 4 |
| $\mathrm{MAJ}_3$ | 3 | 3 | 5 | 5 |
| $x_1 \oplus x_2 \oplus x_3$ | 4 | 4 | 10 | 10 |
| $[x_1 = x_2]$ | 2 | 2 | 4 | 4 |

The two columns of each pair agree for all 254 non-constant functions on three variables, and the monotone versions agree for all 18 non-constant monotone functions, as the theorem says.

**st-connectivity.** Let $f$ say whether a graph on $n$ vertices has a path from $s$ to $t$; it is monotone in the edges. In $\mathrm{KW}^{+}_f$, Alice can take a minimal 1-input, a simple path from $s$ to $t$, and Bob a maximal 0-input, a split of the vertices into a side with $s$ and a side with $t$ with all edges inside the sides present and no edges across. They must find an edge of the path that crosses the split. Binary search over the path finds it: Alice names the middle vertex of the current part of the path ($\lceil \log_2 n \rceil$ bits), and Bob says which side it is on (1 bit). This gives $O(\log^2 n)$ bits, and Karchmer and Wigderson proved that $\Omega(\log^2 n)$ bits are needed, so monotone formulas for [graph reachability](/graph-reachability/) need depth $\Theta(\log^2 n)$.

**Perfect matching.** Raz and Wigderson reduced two-party set disjointness to $\mathrm{KW}^{+}_f$ for $f$ = "the graph has a [perfect matching](/perfect-matching/)" and proved that monotone circuits for it need depth $\Omega(n)$.

## Where it is used

- **Depth lower bounds.** The relation turns a question about circuits into a question about two players, where rectangles, information and other communication tools apply. It gives the $\Omega(\log^2 n)$ bound for monotone st-connectivity and the $\Omega(n)$ bound for monotone matching.
- **Formula size.** Khrapchenko's bound and its later forms are rectangle bounds for the relation.
- **The KRW conjecture.** Karchmer, Raz and Wigderson asked whether the relation of a composed function $f \circ g$ costs about the cost for $f$ plus the cost for $g$. A positive answer would give a function in $\mathsf{P}$ that is not in $\mathsf{NC^1}$; see the [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/).
- **Lifting.** Raz and McKenzie separated the levels of the monotone $\mathsf{NC}$ hierarchy with relations of this kind, by a method that turns query lower bounds into communication lower bounds.

## References
