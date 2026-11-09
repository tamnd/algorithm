---
tag: FPPA26
kind: theorem
slug: shannon-expansion
name: Shannon expansion
aliases:
- Shannon decomposition
- Boole's expansion theorem
- Boole-Shannon expansion
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Every boolean function f equals x·f|x=1 + x'·f|x=0, the recursion behind BDDs.
prereqs: [boolean-function, cofactor]
see_also: [binary-decision-diagram, ite-operator, bdd-apply, bdd-quantification, bdd-compose, kronecker-functional-decision-diagram, bdd-satisfy-count]
sources:
  - paper: doi:10.1109/T-AIEE.1938.5057767
    title: Claude E. Shannon, A symbolic analysis of relay and switching circuits, Transactions of the American Institute of Electrical Engineers 57(12), 1938, pages 713 to 723
    locator: the expansion of a switching function about one variable, and its use to design two-terminal networks
  - book: "George Boole, An Investigation of the Laws of Thought, Walton and Maberly, London, 1854"
    title: An Investigation of the Laws of Thought
    locator: Chapter V, the development (expansion) of logical functions, f(x) = f(1)x + f(0)(1 - x)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 1.1, equation (1) (the Shannon expansion), and Sections 4.3 and 4.5 (Apply and Compose derived from it)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 8, Decision diagrams based on other decomposition rules (the Davio expansions)
---

The Shannon expansion says that each [Boolean function](/boolean-function/) splits on any one variable into its two [cofactors](/cofactor/): $f = (\neg x_i \wedge f|_{x_i=0}) \vee (x_i \wedge f|_{x_i=1})$. It is the step that every algorithm on [binary decision diagrams](/binary-decision-diagram/) takes: a BDD node is this identity drawn as a graph, and [APPLY](/bdd-apply/), [ITE](/ite-operator/), [quantification](/bdd-quantification/) and [composition](/bdd-compose/) all recurse on it. Boole wrote the identity in 1854, and Shannon used it in 1938 to analyse relay circuits.

## Statement

**Theorem.** Let $n \ge 1$, $f \in B_n$ and $1 \le i \le n$. Write $f_0 = f|_{x_i=0}$ and $f_1 = f|_{x_i=1}$. Then, as functions on $\{0,1\}^n$:

1. (Shannon expansion, sum form) $f = (\neg x_i \wedge f_0) \vee (x_i \wedge f_1)$.
2. (product form) $f = (x_i \vee f_0) \wedge (\neg x_i \vee f_1)$.
3. (positive Davio expansion) $f = f_0 \oplus (x_i \wedge (f_0 \oplus f_1))$.
4. (negative Davio expansion) $f = f_1 \oplus (\neg x_i \wedge (f_0 \oplus f_1))$.
5. (uniqueness) If $g_0, g_1 \in B_n$ do not depend on $x_i$ and $f = (\neg x_i \wedge g_0) \vee (x_i \wedge g_1)$, then $g_0 = f_0$ and $g_1 = f_1$.

In the notation of the [ITE operator](/ite-operator/), part 1 says $f = \mathrm{ITE}(x_i, f_1, f_0)$.

## In plain words

Pick one input of a yes or no question. Either that input is off, or it is on. If it is off, the answer is what the question gives with that input fixed to off. If it is on, the answer is what the question gives with that input fixed to on. So the question is the same as "look at this one input, then answer one of two smaller questions". The two smaller questions no longer look at that input. Do the same to each smaller question, and you get a tree of tests. A binary decision diagram is this tree with equal parts shared.

## Proof

Fix an input $x \in \{0,1\}^n$. Let $x^{(b)}$ be $x$ with its $i$-th entry replaced by $b$. By the definition of the cofactor, $f_0(x) = f(x^{(0)})$ and $f_1(x) = f(x^{(1)})$.

*Case $x_i = 0$.* Then $x^{(0)} = x$, so $f_0(x) = f(x)$. In part 1, the term $x_i \wedge f_1$ is 0 and the term $\neg x_i \wedge f_0$ is $f_0(x) = f(x)$. In part 2, the factor $\neg x_i \vee f_1$ is 1 and the factor $x_i \vee f_0$ is $f(x)$. In part 3, the right side is $f_0(x) \oplus 0 = f(x)$. In part 4, the right side is $f_1(x) \oplus (f_0(x) \oplus f_1(x)) = f_0(x) = f(x)$, since $a \oplus a = 0$.

*Case $x_i = 1$.* Then $x^{(1)} = x$, so $f_1(x) = f(x)$. In part 1, only the term $x_i \wedge f_1 = f(x)$ is left. In part 2, only the factor $\neg x_i \vee f_1 = f(x)$ is left. In part 3, the right side is $f_0(x) \oplus f_0(x) \oplus f_1(x) = f(x)$. In part 4, the right side is $f_1(x) \oplus 0 = f(x)$.

Both cases give $f(x)$ on the right side of each part, for each $x$, so parts 1 to 4 hold.

*Part 5.* Take the cofactor by $x_i = 0$ of both sides of $f = (\neg x_i \wedge g_0) \vee (x_i \wedge g_1)$. The cofactor commutes with $\wedge$, $\vee$ and $\neg$ (property 2 on the [cofactor](/cofactor/) page), $x_i|_{x_i=0} = 0$, and $g_0|_{x_i=0} = g_0$ because $g_0$ does not depend on $x_i$. So $f_0 = (1 \wedge g_0) \vee (0 \wedge g_1|_{x_i=0}) = g_0$. The cofactor by $x_i = 1$ gives $f_1 = g_1$ in the same way. $\blacksquare$

**Corollary (full expansion).** Expanding on $x_1$, then on $x_2$ in each cofactor, and so on to $x_n$, gives

$$f = \bigvee_{a \in S_f} \; \bigwedge_{j=1}^{n} \ell_j(a), \qquad \ell_j(a) = x_j \text{ if } a_j = 1, \quad \ell_j(a) = \neg x_j \text{ if } a_j = 0,$$

the sum of minterms of $f$. The proof is by induction on $n$ with part 1: the cofactor $f|_{x_1 = b}$ has the minterms $a$ of $f$ with $a_1 = b$, with the literal of $x_1$ removed.

## Consequences

- **The meaning of a BDD node.** A node that tests $x_i$ and has the children $u_0$ and $u_1$ stands for $(\neg x_i \wedge f_{u_0}) \vee (x_i \wedge f_{u_1})$. When the order puts $x_i$ above all variables of $u_0$ and $u_1$, part 5 shows that $f_{u_0}$ and $f_{u_1}$ are the cofactors. This is the base of the proof of [canonicity](/bdd-canonicity/).
- **Recursive operations.** Since cofactors commute with each pointwise operator, $f \circ g = \mathrm{ITE}(x_i, f_1 \circ g_1, f_0 \circ g_0)$. [APPLY](/bdd-apply/) and [ITE](/ite-operator/) use this with $x_i$ the top variable of the arguments.
- **Quantification and composition.** $\exists x_i\, f = f_0 \vee f_1$ and $\forall x_i\, f = f_0 \wedge f_1$ ([BDD quantification](/bdd-quantification/)). Replacing $x_i$ by $g$ in part 1 gives $f|_{x_i=g} = (\neg g \wedge f_0) \vee (g \wedge f_1)$ ([BDD compose](/bdd-compose/)).
- **Counting.** Since the two terms of part 1 are disjoint, $|S_f| = |S_{f_0}| / 2 + |S_{f_1}| / 2$ when both cofactors are seen as functions of all $n$ variables. [Counting satisfying assignments on BDDs](/bdd-satisfy-count/) applies this at each node.
- **Other decision diagrams.** A node may use a Davio expansion (parts 3 and 4) in place of part 1. Diagrams that mix the three rules per variable are the [Kronecker functional decision diagrams](/kronecker-functional-decision-diagram/).
- **Circuits.** Part 1 is a 2-to-1 multiplexer with select input $x_i$. Iterating it builds any function from multiplexers, and a [Boolean circuit](/boolean-circuit/) of this form is a BDD.

## Tightness

Part 5 needs the hypothesis that $g_0$ and $g_1$ do not depend on $x_i$. Without it, the pair is not unique: for $f = x_1$, both $(g_0, g_1) = (0, 1)$ and $(g_0, g_1) = (0, x_1)$ satisfy $f = (\neg x_1 \wedge g_0) \vee (x_1 \wedge g_1)$. This is why an [ordered BDD](/ordered-binary-decision-diagram/) forbids a test of $x_i$ below a test of $x_i$: the children of a node must not depend on the variable of the node.

The full expansion can be as large as $2^{n-1}$ minterms, and for parity no shorter sum of products exists. Each product term of a sum-of-products form of $x_1 \oplus \cdots \oplus x_n$ must contain all $n$ variables: if a term $t$ misses $x_j$, take an input that makes $t$ true, flip $x_j$, and $t$ stays true while the parity changes, so the form is 1 at an input where parity is 0. A term with all $n$ variables covers one input, and parity has $2^{n-1}$ inputs with value 1. The BDD of parity, which shares the subfunctions, has only $2n + 1$ nodes.

## History

Boole gave the expansion $f(x) = f(1)\,x + f(0)\,(1 - x)$ of a logical function about one symbol in An Investigation of the Laws of Thought (1854). Shannon used the same identity in 1938, in his analysis of relay and switching circuits, to expand a switching function about one variable and to build a two-terminal network for it. The name Shannon expansion comes from this use. Bryant (1986) states it as equation (1) of his paper and derives his Apply and Compose procedures from it. The Davio expansions are the basis of the functional decision diagrams that Wegener (2000, Chapter 8) surveys.

## References
