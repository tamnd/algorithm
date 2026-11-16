---
tag: KSGQYF
kind: theorem
slug: karchmer-wigderson-theorem
name: Karchmer-Wigderson theorem
aliases:
- KW theorem
area: complexity/communication-and-query-complexity
level: research
summary: "The least depth of a fan-in-2 AND/OR formula for f equals the deterministic communication cost of the Karchmer-Wigderson relation of f. Formula size equals the least number of protocol leaves."
prereqs: [karchmer-wigderson-relation, boolean-circuit, circuit-complexity]
see_also: [nc, deterministic-communication-complexity, communication-model, parity-problem, graph-reachability, perfect-matching, p, boolean-function]
sources:
  - paper: doi:10.1137/0403021
    title: "Mauricio Karchmer and Avi Wigderson, Monotone circuits for connectivity require super-logarithmic depth, SIAM Journal on Discrete Mathematics 3(2), 1990, pages 255-265"
    locator: the theorem for general and monotone circuits, and the Omega(log^2 n) bound for monotone st-connectivity
  - paper: doi:10.1145/62212.62265
    title: "Mauricio Karchmer and Avi Wigderson, Monotone circuits for connectivity require super-logarithmic depth, 20th ACM Symposium on Theory of Computing (STOC 1988), pages 539-550"
    locator: the conference version
  - paper: doi:10.1145/146637.146684
    title: "Ran Raz and Avi Wigderson, Monotone circuits for matching require linear depth, Journal of the ACM 39(3), 1992, pages 736-744"
    locator: the Omega(n) bound on the monotone depth of perfect matching
  - paper: doi:10.1007/BF01206317
    title: "Mauricio Karchmer, Ran Raz and Avi Wigderson, Super-logarithmic depth lower bounds via the direct sum in communication complexity, Computational Complexity 5(3/4), 1995, pages 191-204"
    locator: the KRW conjecture on composed functions and its consequence that P is not contained in NC1
  - paper: doi:10.1007/s004930050062
    title: "Ran Raz and Pierre McKenzie, Separation of the monotone NC hierarchy, Combinatorica 19(3), 1999, pages 403-435"
    locator: monotone NC^i is different from monotone NC^(i+1) for every i
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press (1997)
    locator: Chapter 10, Boolean circuit depth (Section 10.2, the connection to communication complexity)
  - book: isbn:9783642245077
    title: Stasys Jukna, Boolean Function Complexity, Advances and Frontiers, Springer (2012)
    locator: Chapter 3, Games on relations (Section 3.3, games and circuit depth); Chapter 6, Formulas (formula balancing, Section 6.8, Khrapchenko's theorem)
---

The Karchmer-Wigderson theorem says that the depth of a Boolean function is a communication cost. For a non-constant $f : \{0,1\}^n \to \{0,1\}$, the least depth of a fan-in-2 AND/OR formula for $f$ equals the deterministic communication complexity of the [Karchmer-Wigderson relation](/karchmer-wigderson-relation/) $\mathrm{KW}_f$, in which Alice holds $x \in f^{-1}(1)$, Bob holds $y \in f^{-1}(0)$, and they must find $i$ with $x_i \ne y_i$. The same proof shows that formula size equals the least number of leaves of a protocol, and that the monotone versions match. The theorem lets communication methods prove depth lower bounds, and it gave the first super-logarithmic lower bounds on monotone depth.

## Statement

Formulas here are trees of AND and OR gates of fan-in 2 whose leaves are literals $x_i$ or $\neg x_i$ (De Morgan formulas). The depth is the length of the longest path from the output to a leaf, and the size $L(f)$ is the least number of leaves. A monotone formula has only positive literals.

**Theorem (Karchmer and Wigderson).** For every non-constant $f : \{0,1\}^n \to \{0,1\}$,

$$\mathrm{depth}(f) = D^{cc}(\mathrm{KW}_f) \quad \text{and} \quad L(f) = \min_P \mathrm{leaves}(P) ,$$

where the minimum is over protocols $P$ for $\mathrm{KW}_f$. For every non-constant monotone $f$, the same holds for monotone depth, monotone size, and the monotone relation $\mathrm{KW}^{+}_f$, in which the answer $i$ must have $x_i = 1$ and $y_i = 0$.

Since a fan-in-2 circuit of depth $d$ unfolds into a formula of depth $d$ (with at most $2^d$ leaves), and negations can be pushed to the leaves without increasing the depth, $\mathrm{depth}(f)$ is also the least depth of a fan-in-2 circuit over AND, OR and NOT.

## In plain words

To see why a circuit says yes on one input and no on another, walk down from the top. At an OR gate, the yes input must make some branch true, so its holder names that branch. At an AND gate, the no input must make some branch false, so its holder names that branch. At the bottom is an input bit on which the two inputs differ. Each step costs one bit, so a shallow circuit gives a short conversation. The theorem says that the other direction also works: any short conversation that always finds a differing bit can be turned back into a shallow circuit. The two numbers are exactly equal. So to show that a function needs deep circuits, it is enough to show that two people need to talk a lot to find a place where a yes input and a no input differ.

## Proof

Prove a stronger claim for every pair of disjoint nonempty sets $A, B \subseteq \{0,1\}^n$. Let $\mathrm{KW}(A, B)$ be the game in which Alice gets $x \in A$, Bob gets $y \in B$, and they must find $i$ with $x_i \ne y_i$. Say that a formula $F$ **separates** $A$ from $B$ if $F(x) = 1$ for all $x \in A$ and $F(y) = 0$ for all $y \in B$.

**Claim.** The least depth of a formula that separates $A$ from $B$ equals $D^{cc}(\mathrm{KW}(A, B))$, and the least size equals the least number of leaves of a protocol for $\mathrm{KW}(A, B)$.

The theorem is the case $A = f^{-1}(1)$, $B = f^{-1}(0)$, since a formula separates these two sets exactly when it computes $f$.

**From formulas to protocols.** Let $F$ separate $A$ from $B$. Build a protocol by induction on $F$.

1. If $F$ is a literal $x_i$, then $x_i = 1$ on $A$ and $x_i = 0$ on $B$, so the protocol outputs $i$ with no communication. A literal $\neg x_i$ is the same with the values swapped.
2. If $F = F_1 \vee F_2$, let $A_j = \{x \in A : F_j(x) = 1\}$. Each $x \in A$ is in $A_1$ or $A_2$, and $F_j(y) = 0$ for all $y \in B$ because $F(y) = 0$. So $F_j$ separates $A_j$ from $B$. Alice sends one bit $j$ with $x \in A_j$, and the players continue with the protocol for $F_j$ on $(A_j, B)$. If some $A_j$ is empty, Alice never sends $j$ and that branch is not needed.
3. If $F = F_1 \wedge F_2$, let $B_j = \{y \in B : F_j(y) = 0\}$. Then $F_j$ separates $A$ from $B_j$, Bob sends $j$ with $y \in B_j$, and the players continue with $F_j$.

The protocol tree has the same shape as $F$: OR gates become Alice nodes, AND gates become Bob nodes, and leaves become leaves. So its depth is the depth of $F$ and its number of leaves is the size of $F$. If $F$ is monotone, each leaf is a positive literal $x_i$, and the answer has $x_i = 1$ and $y_i = 0$, as $\mathrm{KW}^{+}$ requires.

**From protocols to formulas.** Let $P$ be a protocol for $\mathrm{KW}(A, B)$. Build a formula by induction on the depth of $P$.

1. If $P$ is a single leaf with answer $i$, then $x_i \ne y_i$ for all $x \in A$ and $y \in B$. Fix any $y \in B$. Every $x \in A$ has $x_i = 1 - y_i$, so $x_i$ takes one value $c$ on all of $A$, and by the same argument with a fixed $x$, $y_i = 1 - c$ on all of $B$. The literal $x_i$ (if $c = 1$) or $\neg x_i$ (if $c = 0$) separates $A$ from $B$. In the monotone relation $c = 1$, so the literal is positive.
2. If Alice speaks first, her bit splits $A$ into $A_0$ and $A_1$, and the two subtrees are protocols for $\mathrm{KW}(A_0, B)$ and $\mathrm{KW}(A_1, B)$. By induction there are formulas $F_0$ and $F_1$ that separate them, with the depths and sizes of the subtrees. Then $F_0 \vee F_1$ is 1 on all of $A = A_0 \cup A_1$ and 0 on all of $B$. If one part is empty, use the formula of the other part.
3. If Bob speaks first, his bit splits $B$ into $B_0$ and $B_1$, and $F_0 \wedge F_1$ separates $A$ from $B$ in the same way.

The formula has the shape of $P$, so its depth is the depth of $P$ and its size is the number of leaves of $P$.

The two constructions prove both inequalities of the claim, for depth and for size, and for the monotone versions. $\blacksquare$

## Consequences

- **Formula size and depth.** A formula of depth $d$ has at most $2^d$ leaves, so $\mathrm{depth}(f) \ge \log_2 L(f)$. Spira proved that every formula of size $s$ has an equivalent formula of depth $O(\log s)$. So $D^{cc}(\mathrm{KW}_f) = \Theta(\log L(f))$, and a family of functions is in non-uniform $\mathsf{NC^1}$ exactly when it has formulas of polynomial size, and exactly when its relations cost $O(\log n)$ bits. See [NC](/nc/).
- **Parity.** A binary search protocol solves $\mathrm{KW}$ of the parity of $n$ bits with $2\log_2 n$ bits and $n^2$ leaves, and Khrapchenko's bound shows $L \ge n^2$. So for $n$ a power of 2 the [parity function](/parity-problem/) has De Morgan depth exactly $2\log_2 n$ and size exactly $n^2$.
- **Monotone st-connectivity.** Karchmer and Wigderson proved that the monotone relation for [graph reachability](/graph-reachability/) on $n$ vertices needs $\Omega(\log^2 n)$ bits. So monotone circuits for st-connectivity need depth $\Omega(\log^2 n)$, which matches the $O(\log^2 n)$ depth from repeated squaring. It was the first super-logarithmic lower bound on monotone depth for a function with small monotone circuits, and it separates monotone $\mathsf{NC^1}$ from monotone $\mathsf{NC^2}$.
- **Monotone matching.** Raz and Wigderson reduced set disjointness to the monotone relation for [perfect matching](/perfect-matching/) and proved that monotone circuits for it on graphs with $n$ vertices need depth $\Omega(n)$, linear in the number of vertices.
- **The monotone NC hierarchy.** Raz and McKenzie proved that monotone $\mathsf{NC^i}$ is different from monotone $\mathsf{NC^{i+1}}$ for every $i$, and that monotone $\mathsf{NC}$ is different from monotone $\mathsf{P}$, with a lifting theorem for monotone relations.
- **The KRW conjecture.** Karchmer, Raz and Wigderson conjectured that $D^{cc}(\mathrm{KW}_{f \circ g})$ is close to $D^{cc}(\mathrm{KW}_f) + D^{cc}(\mathrm{KW}_g)$ for the block composition $f \circ g$. They showed that the conjecture would give a function in [P](/p/) that is not in $\mathsf{NC^1}$. It is still open.

## Tightness

The theorem is an exact equality, with no constant lost in either direction, for depth and for size. A search over all protocols and all formulas for $n = 3$ confirms it on all 254 non-constant functions and on all 18 non-constant monotone functions. For example, $\mathrm{MAJ}_3$ has depth 3 and size 5, and the parity of 3 bits has depth 4 and size 10, and the relations have the same costs and leaf counts.

The equality needs the De Morgan basis with fan-in 2. With other gates it fails. With XOR gates of fan-in 2, the parity of $n$ bits has depth $\lceil \log_2 n \rceil$, but $D^{cc}(\mathrm{KW})$ for parity is $2\log_2 n$ for $n$ a power of 2. With unbounded fan-in, a single OR gate of fan-in $n$ has depth 1, while the relation for OR needs Alice to name a position, about $\log_2 n$ bits.

The relation between depth and size is not an equality. The bound $\mathrm{depth}(f) \ge \log_2 L(f)$ is exact for parity with $n$ a power of 2, but not in general: the AND of three bits has size 3 and depth 2, and $\log_2 3 < 2$. Spira's balancing gives depth $O(\log s)$ with a constant factor greater than 1.

## History

Karchmer and Wigderson presented the theorem and the monotone st-connectivity bound at STOC 1988, and the journal version appeared in the SIAM Journal on Discrete Mathematics in 1990. Earlier, Khrapchenko's 1971 lower bound of $n^2$ on the formula size of parity had been proved by a counting argument over neighbouring pairs of inputs; in the language of the theorem it is a bound on the number of rectangles in a protocol. Raz and Wigderson proved the linear bound for monotone matching in 1992. Karchmer, Raz and Wigderson stated their conjecture on composition in 1991, in the conference version of their 1995 paper. Raz and McKenzie separated the monotone NC hierarchy in 1997, in work that started the method of lifting query lower bounds to communication lower bounds.

## References
