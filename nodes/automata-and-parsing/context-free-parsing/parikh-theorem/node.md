---
tag: D3PW71
kind: theorem
slug: parikh-theorem
name: Parikh's theorem
area: automata-and-parsing/context-free-parsing
level: advanced
summary: The Parikh image of a context-free language is a semilinear set.
prereqs: [context-free-language, parse-tree, parikh-vector, regular-language]
see_also: [cfl-pumping-lemma, presburger-arithmetic, inherent-ambiguity, chomsky-schutzenberger-theorem, cfl-closure-properties, petri-net, nondeterministic-finite-automaton, context-free-grammar]
sources:
  - paper: doi:10.1145/321356.321364
    title: Rohit J. Parikh, On context-free languages, Journal of the ACM 13(4) (1966)
    locator: pp. 570 to 581
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Supplementary Lecture H, Parikh's Theorem
  - paper: doi:10.2140/pjm.1966.16.285
    title: Seymour Ginsburg and Edwin H. Spanier, Semigroups, Presburger formulas, and languages, Pacific Journal of Mathematics 16(2) (1966)
    locator: pp. 285 to 296 (the semilinear sets are exactly the sets definable in Presburger arithmetic)
  - paper: doi:10.1016/j.ipl.2011.03.019
    title: Javier Esparza, Pierre Ganty, Stefan Kiefer and Michael Luttenberger, Parikh's theorem, a simple and direct automaton construction, Information Processing Letters 111(12) (2011)
    locator: pp. 614 to 619
---

Parikh's theorem says that if one forgets the order of the letters, every [context-free language](/context-free-language/) looks like a [regular language](/regular-language/). Precisely, the set of [Parikh vectors](/parikh-vector/) of a context-free language, the vectors that count how often each letter occurs in each word, is a semilinear set: a finite union of sets of the form "a base vector plus any combination of finitely many period vectors". The theorem gives a test for non-context-freeness that the [pumping lemma](/cfl-pumping-lemma/) cannot always give, shows that every context-free language over one letter is regular, and connects context-free grammars to [Presburger arithmetic](/presburger-arithmetic/).

## Statement

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

Let $\Sigma = \{a_1, \ldots, a_d\}$. The **Parikh map** $\psi : \Sigma^* \to \mathbb{N}^d$ sends a word $w$ to $(|w|_{a_1}, \ldots, |w|_{a_d})$, where $|w|_a$ is the number of occurrences of $a$ in $w$. For a language $L$, $\psi(L) = \{ \psi(w) : w \in L \}$. Two languages are **letter-equivalent** when they have the same Parikh image.

A set $X \subseteq \mathbb{N}^d$ is **linear** if there are vectors $b, p_1, \ldots, p_m \in \mathbb{N}^d$, with $m \ge 0$, such that

$$X = b + \{p_1, \ldots, p_m\}^* = \{ b + c_1 p_1 + \cdots + c_m p_m : c_1, \ldots, c_m \in \mathbb{N} \}.$$

It is **semilinear** if it is a finite union of linear sets.

> **Theorem (Parikh, 1966).** For every context-free grammar $G$, the set $\psi(L(G))$ is semilinear. Equivalently, every context-free language is letter-equivalent to a regular language.

The two forms are equivalent because the Parikh images of regular languages are exactly the semilinear sets. If $X = b + \{p_1, \ldots, p_m\}^*$, pick words $u, v_1, \ldots, v_m$ with $\psi(u) = b$ and $\psi(v_i) = p_i$; then $\psi(u (v_1 + \cdots + v_m)^*) = X$, and a finite union of linear sets is the image of the union of these regular languages. Conversely a regular language is context-free, so its image is semilinear by the theorem.

## In plain words

Take a grammar and, for each word it generates, keep only how many of each letter the word has. Parikh's theorem says that the counts that can occur have a very plain shape. There are finitely many starting points, and from each starting point you may add any number of copies of a few fixed bundles of letters.

The reason is the same as for the pumping lemma. In a large parse tree some rule repeats along a branch, and the part between the two repetitions can be cut out or copied. Each such part adds a fixed bundle of letters. Cutting them all out leaves one of finitely many small trees. The only care needed is to cut pieces that leave at least one copy of every grammar symbol of the tree, so that bundles can later be put back.

## Proof

Fix $G$ and let $k = |V|$. A *tree* below means a [parse tree](/parse-tree/) of $G$ whose leaves are terminals or $\varepsilon$, except in the case of a pump, which has one more leaf. For $U \subseteq V$, let $T_U$ be the set of complete parse trees with root $S$ whose set of nonterminal labels is exactly $U$. Then $L(G)$ is the union over the finitely many $U$ of the yields of $T_U$, so it suffices to prove that $\psi(\mathrm{yield}(T_U))$ is semilinear for each $U$. Write $\psi(t)$ for the Parikh vector of the yield of a tree $t$.

**Pumps.** A *$U$-pump* is a tree $p$ whose root has a label $A \in U$, whose nonterminal labels all lie in $U$, and which has exactly one leaf labelled by a nonterminal, the *foot*, with the label $A$; its other leaves are terminals or $\varepsilon$. Let $\psi(p)$ count the terminal leaves of $p$. Set $N_0 = (k + 1)^2 + k$ and define the finite sets

$$B_U = \{ \psi(t) : t \in T_U, \ \mathrm{height}(t) < N_0 \}, \qquad P_U = \{ \psi(p) : p \text{ a } U\text{-pump}, \ \mathrm{height}(p) \le N_0 \}.$$

They are finite because there are finitely many trees of bounded height: each inner node has at most $r$ children, where $r$ is the length of the longest right side. We prove

$$\psi(\mathrm{yield}(T_U)) = B_U + P_U^*,$$

where $B_U + P_U^*$ is the union over $b \in B_U$ of the linear sets $b + P_U^*$. This proves the theorem.

**Inserting pumps ($\supseteq$).** Let $t \in T_U$ and let $p$ be a $U$-pump with root label $A$. Since $A \in U$, the tree $t$ has a node $v$ labelled $A$. Replace the subtree of $v$ by a copy of $p$ and put the old subtree of $v$ in place of the foot. The result is a complete tree with root $S$ (if $v$ is the root, $A = S$), its labels are those of $t$ together with those of $p$, which is still exactly $U$, and its Parikh vector is $\psi(t) + \psi(p)$. Repeating this for any finite list of pumps shows that $b + c_1 p_1 + \cdots + c_m p_m$ is in $\psi(\mathrm{yield}(T_U))$ for every $b \in B_U$, every list of vectors $p_i \in P_U$ and every $c_i \in \mathbb{N}$.

**Removing pumps ($\subseteq$).** We show by induction on the number of nodes that $\psi(t) \in B_U + P_U^*$ for every $t \in T_U$. If $\mathrm{height}(t) < N_0$, then $\psi(t) \in B_U$. Otherwise let $h = \mathrm{height}(t) \ge N_0$ and let $P$ be a path from the root to a leaf $z$ at depth $h$. All nodes of $P$ except $z$ are inner nodes.

For each $A \in U$ choose one node of $t$ labelled $A$ and call it *marked*; there are at most $k$ marked nodes. For a marked node $m$, let $\beta(m)$ be the deepest node of $P$ that is an ancestor of $m$ or equal to it. Call the nodes $\beta(m)$ *special*; there are at most $k$ of them. For nodes $x$ above $y$ on $P$, write $[x, y)$ for the nodes of $P$ from $x$ down to the parent of $y$.

*Claim.* Cutting out the part between $x$ and $y$, that is, replacing the subtree of $x$ by the subtree of $y$, keeps every marked node if $[x, y)$ contains no special node. Indeed, a marked node $m$ is in the subtree of $x$ exactly when $x$ is at or above $\beta(m)$, and in the subtree of $y$ exactly when $y$ is at or above $\beta(m)$; so $m$ is removed exactly when $\beta(m) \in [x, y)$.

Now look at the $N_0$ lowest inner nodes of $P$, at the depths $h - N_0, \ldots, h - 1$. At most $k$ of them are special, so at least $N_0 - k = (k + 1)^2$ are not, and they fall into at most $k + 1$ maximal runs of consecutive nonspecial nodes. Some run has at least $k + 1$ nodes, and since there are only $k$ nonterminals, two of them, $x$ above $y$, have the same label $A$. All of $[x, y)$ lies in the run, so it has no special node.

Let $t'$ be $t$ with the subtree of $x$ replaced by the subtree of $y$, and let $p$ be the subtree of $x$ with the subtree of $y$ replaced by a foot labelled $A$. Then:

- $t'$ is a complete tree with root $S$, its labels are a subset of $U$, and by the claim it keeps all marked nodes, so its label set is exactly $U$ and $t' \in T_U$;
- $p$ is a $U$-pump, and its height is at most the height of the subtree of $x$, which is $h - \mathrm{depth}(x) \le N_0$, because $z$ is a deepest leaf of $t$ and lies below $x$; so $\psi(p) \in P_U$;
- $\psi(t) = \psi(t') + \psi(p)$, since the terminal leaves of $t$ are those of $t'$ and those of $p$;
- $t'$ has fewer nodes than $t$, because $x \ne y$.

By the induction hypothesis $\psi(t') \in B_U + P_U^*$, so $\psi(t) \in B_U + P_U^*$. $\blacksquare$

The proof works for any grammar, with $\varepsilon$-productions and unit productions, and it is constructive: it computes a semilinear representation from $G$, though $B_U$ and $P_U$ can be exponentially large.

## Consequences

**Context-free languages over one letter are regular.** For $\Sigma = \{a\}$, $\psi$ is a bijection between $a^*$ and $\mathbb{N}$. A linear set $b + \{p_1, \ldots, p_m\}^* \subseteq \mathbb{N}$ is ultimately periodic: the multiples of $g = \gcd(p_1, \ldots, p_m)$ that are large enough are all sums of the $p_i$, so from some point on the set is $b$ plus all multiples of $g$. A finite union of ultimately periodic sets is ultimately periodic, and the unary languages with an ultimately periodic set of lengths are exactly the regular ones. So $\{a^m : m \text{ prime}\}$, $\{a^{m^2} : m \ge 0\}$ and $\{a^{2^m} : m \ge 0\}$ are not context-free.

**A test for non-context-freeness.** If $\psi(L)$ is not semilinear, $L$ is not context-free. For example $\{a^m b^{m^2} : m \ge 0\}$ has the image $\{(m, m^2)\}$; a linear set contained in it can have no nonzero period, because adding a period $(c, e)$ twice would need $(m + 2c)^2 - (m + c)^2 = (m + c)^2 - m^2$, so $c = 0$ and then $e = 0$; so a semilinear subset of it is finite. The test works also with closure properties: intersecting with a regular language or applying a homomorphism keeps a language context-free, and so keeps its image semilinear.

**Examples of images.**

| language | grammar | Parikh image | letter-equivalent regular language |
|---|---|---|---|
| $\{a^i b^j c^i\}$ | $S \to a S c \mid B$, $B \to b B \mid \varepsilon$ | $(0,0,0) + \{(1,0,1), (0,1,0)\}^*$ | $(a c)^* b^*$ |
| [Dyck words](/dyck-language/), $a$ opening and $b$ closing | $S \to a S b S \mid \varepsilon$ | $(0, 0) + \{(1, 1)\}^*$ | $(a b)^*$ |
| $\{a^i b^j c^k : i = j \text{ or } j = k\}$ | | $\{(1,1,0), (0,0,1)\}^* \cup \{(1,0,0), (0,1,1)\}^*$ | $(a b)^* c^* + a^* (b c)^*$ |

In the first row the pumps of the proof are the bundles $(1, 0, 1)$ from $S \to a S c$ and $(0, 1, 0)$ from $B \to b B$, and the only base vector is $(0, 0, 0)$, from $S \to B \to \varepsilon$. The third language is [inherently ambiguous](/inherent-ambiguity/), while its letter-equivalent regular language has an unambiguous grammar: the Parikh image cannot see ambiguity.

**Presburger arithmetic.** Ginsburg and Spanier (1966) showed that the semilinear sets are exactly the sets definable in [Presburger arithmetic](/presburger-arithmetic/), the first-order theory of $(\mathbb{N}, +)$. With Parikh's theorem, the letter counts of a context-free language are described by a Presburger formula, which can be computed from the grammar. Questions such as "does the language contain a word with as many $a$'s as $b$'s and at least one $c$" become decidable, since Presburger arithmetic is decidable.

**Verification.** Programs with recursion are modelled by context-free grammars or pushdown systems, and their counts of events by Parikh images. Reachability in communication-free [Petri nets](/petri-net/), the analysis of procedural programs with counters, and the checking of properties of message counts all use existential Presburger formulas for Parikh images. Verma, Seidl and Schwentick (2005) showed that such a formula can be built in linear time from the grammar, which places many of these problems in NP.

## Tightness

- **The converse fails.** A semilinear image does not make a language context-free. $\{a^m b^m c^m\}$ has the linear image $\{(1,1,1)\}^*$, and is not context-free. Parikh's theorem only constrains the counts, never the order.
- **Larger classes.** The theorem fails just above the context-free languages. $\{a^{2^m} : m \ge 0\}$ is generated by an indexed grammar and by a context-sensitive grammar, and its image $\{2^m\}$ is not semilinear.
- **Size of the regular language.** The grammar $A_0 \to a$, $A_i \to A_{i-1} A_{i-1}$ for $1 \le i \le k$, with start symbol $A_k$, has $k + 1$ nonterminals and generates the single word $a^{2^k}$. A [nondeterministic finite automaton](/nondeterministic-finite-automaton/) with the same unary language has at least $2^k + 1$ states, since an accepting path of length $2^k$ through fewer states repeats a state and its loop would give infinitely many words. So the letter-equivalent regular language can need an automaton exponentially larger than the grammar. Esparza, Ganty, Kiefer and Luttenberger (2011) give a direct construction of an automaton whose size is exponential only in the number of nonterminals.
- **The bounds of the proof.** The height bound $N_0 = (k + 1)^2 + k$ is not optimal; any bound that forces a cuttable repetition works, and sharper ones give smaller sets $B_U$ and $P_U$. For a fixed alphabet, Kopczyński and To (2010) showed that a semilinear representation of polynomial size in $|G|$ exists.

## History

Rohit Parikh proved the theorem in a 1961 MIT report, published in the Journal of the ACM in 1966 as "On context-free languages". The same paper shows that some context-free languages are inherently ambiguous, using the map $\psi$. Ginsburg and Spanier characterized the semilinear sets as the Presburger-definable sets in the same year. Later proofs replaced Parikh's induction by algebraic arguments, by fixed points in commutative semirings (Pilling's equations), and by the direct automaton construction of Esparza, Ganty, Kiefer and Luttenberger (2011). Verma, Seidl and Schwentick's linear-size existential Presburger formula (2005) made the theorem a practical tool in verification.

## References
