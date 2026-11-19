---
tag: XZYMCK
kind: definition
slug: synchronous-context-free-grammar
name: Synchronous context-free grammar
aliases:
- SCFG
- syntax-directed transduction grammar
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: A grammar whose rules rewrite a nonterminal into a pair of strings with linked nonterminals, deriving a source and target sentence together.
history:
  year: 1968
  people: [Philip M. Lewis, Richard E. Stearns]
  note: Lewis and Stearns (1968) defined syntax-directed transductions for compilers, and Aho and Ullman (1969) studied the general syntax-directed translation schemata and their relation to pushdown transducers. Wu (1997) brought a binary form to translation, and Chiang (2005, 2007) made the general form, under the name synchronous context-free grammar, the basis of hierarchical and syntax-based translation.
prereqs: [context-free-grammar]
see_also: [inversion-transduction-grammar, hierarchical-phrase-based-translation, ghkm-rule-extraction, syntax-directed-translation, cyk-algorithm, pushdown-automaton, finite-state-transducer, hypergraph]
sources:
  - paper: "Philip M. Lewis and Richard E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3), 1968, pages 465 to 488"
    title: Lewis and Stearns 1968
    locator: the definition of syntax-directed transduction, with rules that rewrite a nonterminal on the input and the output side together
  - paper: doi:10.1016/s0022-0000(69)80006-1
    title: Alfred V. Aho and Jeffrey D. Ullman, Syntax directed translations and the pushdown assembler, Journal of Computer and System Sciences 3(1), 1969, pages 37 to 56
    locator: syntax-directed translation schemata, their simple (order-preserving) form, and their relation to pushdown transducers
  - paper: "David Chiang, Hierarchical phrase-based translation, Computational Linguistics 33(2), 2007, pages 201 to 228, ACL Anthology J07-2003"
    title: Chiang 2007
    locator: the definition of synchronous context-free grammars with linked nonterminals and their derivations, used for translation
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 11 (tree-based models: synchronous grammars)"
---

A synchronous context-free grammar (SCFG) is a [context-free grammar](/context-free-grammar/) whose rules produce two strings at once. Each rule rewrites one nonterminal into a source string and a target string, and every nonterminal on the source side is linked to one nonterminal with the same label on the target side. A derivation rewrites linked nonterminals together, so it builds a source sentence and its translation from one shared tree, while the order of the subtrees can differ between the two sides. SCFGs are the formal basis of [inversion transduction grammars](/inversion-transduction-grammar/), [hierarchical phrase-based translation](/hierarchical-phrase-based-translation/) and syntax-based translation with [GHKM rules](/ghkm-rule-extraction/).

## Definition

An SCFG is a tuple $G = (N, \Sigma, \Delta, R, S)$ with a finite set $N$ of nonterminals, a source alphabet $\Sigma$, a target alphabet $\Delta$, a start symbol $S \in N$, and a finite set $R$ of rules of the form

$$X \to \langle \alpha, \beta, \sim \rangle,$$

where $X \in N$, $\alpha \in (N \cup \Sigma)^*$, $\beta \in (N \cup \Delta)^*$, and $\sim$ is a one-to-one map between the nonterminal occurrences in $\alpha$ and those in $\beta$ that links only occurrences with the same label. The links are written as indices: $\mathrm{VP} \to \langle \mathrm{NP}_{1} \; \mathrm{V}_{2}, \; \mathrm{V}_{2} \; \mathrm{NP}_{1} \rangle$. The *rank* of a rule is its number of linked pairs, and the rank of $G$ is the largest rank of its rules.

A *sentential form* is a pair $\langle \gamma, \delta \rangle$ with a link map between its nonterminals. A derivation step picks a linked pair $\langle X_i, X_i \rangle$ and a rule $X \to \langle \alpha, \beta, \sim \rangle$, replaces $X_i$ by $\alpha$ on the source side and by $\beta$ on the target side, and gives the new linked pairs fresh indices. The *translation* of $G$ is the relation

$$T(G) = \{ (f, e) \in \Sigma^* \times \Delta^* : \langle S_1, S_1 \rangle \Rightarrow^* \langle f, e \rangle \}.$$

In translation, the source is $f = f_1 \ldots f_m$ and the target is $e = e_1 \ldots e_l$; the grammar itself is symmetric, and swapping the two sides of every rule gives a grammar for the inverse relation. A *weighted* SCFG gives each rule a weight, and a derivation the product (or, in log space with natural logs, the sum) of the weights of its rules. A derivation has one tree, whose nodes are rule applications; the source tree and the target tree are the same tree with the children of each node in two orders.

## Examples and non-examples

**Example (SOV to SVO).** Japanese puts the verb after the object, English before it. The grammar

$$\begin{aligned} \mathrm{S} &\to \langle \mathrm{NP}_1 \; \mathrm{VP}_2, \; \mathrm{NP}_1 \; \mathrm{VP}_2 \rangle & \mathrm{NP} &\to \langle \text{kare wa}, \; \text{he} \rangle \\ \mathrm{VP} &\to \langle \mathrm{NP}_1 \; \mathrm{V}_2, \; \mathrm{V}_2 \; \mathrm{NP}_1 \rangle & \mathrm{NP} &\to \langle \text{hon o}, \; \text{books} \rangle \\ & & \mathrm{V} &\to \langle \text{yomu}, \; \text{reads} \rangle \end{aligned}$$

derives

$$\langle \mathrm{S}_1, \mathrm{S}_1 \rangle \Rightarrow \langle \mathrm{NP}_2 \, \mathrm{VP}_3, \mathrm{NP}_2 \, \mathrm{VP}_3 \rangle \Rightarrow \langle \text{kare wa} \; \mathrm{VP}_3, \text{he} \; \mathrm{VP}_3 \rangle \Rightarrow \langle \text{kare wa} \; \mathrm{NP}_4 \, \mathrm{V}_5, \text{he} \; \mathrm{V}_5 \, \mathrm{NP}_4 \rangle \Rightarrow^* \langle \text{kare wa hon o yomu}, \text{he reads books} \rangle.$$

The VP rule reorders its two children, and the words of each child stay together on both sides.

**Example (reversal).** The rank 1 grammar $S \to \langle a \, S_1, S_1 \, a \rangle$, $S \to \langle b \, S_1, S_1 \, b \rangle$, $S \to \langle \varepsilon, \varepsilon \rangle$ translates every string over $\{a, b\}$ into its reverse.

**Example (Hiero rule).** $X \to \langle X_1 \text{ de } X_2, \; X_2 \text{ of } X_1 \rangle$ has one nonterminal label and mixes words with linked gaps; it swaps the two noun phrases around a Chinese possessive marker.

**Non-example (unequal labels).** $X \to \langle A_1 \, B_2, B_1 \, A_2 \rangle$ links $A$ to $B$. Links must join equal labels, because both sides of a link are rewritten by the same rule.

**Non-example (deletion or copying).** $X \to \langle A_1 \, B_2, A_1 \rangle$ has an unlinked $B$, and $X \to \langle A_1, A_1 \, A_1 \rangle$ uses one source nonterminal twice. Neither is an SCFG rule, because the link map must be one to one. Copying rules belong to tree transducers.

**Non-example (copy relation).** The relation $\{(w, w w) : w \in \{a, b\}^*\}$ is not the translation of any SCFG, because the target side of an SCFG translation is a [context-free language](/context-free-language/) (see below), and $\{w w\}$ is not context-free.

**Non-example (two independent grammars).** Two CFGs, one for each language, with no links between their nonterminals generate pairs of unrelated sentences, not translations.

## Related definitions

- **Projections (theorem).** Dropping the target side of every rule gives a CFG for $\{f : (f, e) \in T(G)\}$, and dropping the source side a CFG for the targets. So both projections are context-free languages, and parsing the source with the source CFG, for example by the [CYK algorithm](/cyk-algorithm/) after binarizing the source sides, takes $O(m^3 |G|)$ time and gives a packed forest, a [hypergraph](/hypergraph/), from which the target side is read.
- **Rank and binarization (theorem).** A rule can be split into rank 2 rules with new nonterminals exactly when its nonterminal order can be built by repeatedly joining adjacent blocks, in the same or in the opposite order. The order 2 4 1 3 cannot: no two of its nonterminals are adjacent on both sides. Aho and Ullman showed that rank 3 grammars give no more translations than rank 2 grammars, while for higher ranks each rank adds new translations.
- **Inversion transduction grammar.** An [ITG](/inversion-transduction-grammar/) is an SCFG of rank 2 in a normal form, with straight and inverted binary rules. Every SCFG of rank 2 or 3 has an equivalent ITG.
- **Biparsing.** Deciding whether $(f, e) \in T(G)$ takes $O(m^3 l^3)$ time for an ITG. Satta and Peserico (2005) showed that it is NP-hard when the grammar is part of the input and its rank is not bounded.
- **Syntax-directed translation.** In compilers, [syntax-directed translation](/syntax-directed-translation/) attaches arbitrary actions to the rules of one grammar. An SCFG is the special case where the action of each rule writes out fixed words and the translations of the children in some order, and nothing else.
- **Simple SCFGs and pushdown transducers.** If every rule keeps its nonterminals in the same order on both sides, the grammar is *simple*, and Aho and Ullman (1969) relate these translations to the ones computed by [pushdown](/pushdown-automaton/) transducers.
- **Finite-state transducers.** A rank 1 SCFG whose nonterminal is always at the right end of both sides defines a rational relation, the kind computed by a [finite-state transducer](/finite-state-transducer/).
- **Tree-based rules.** Synchronous tree substitution grammars, such as the [GHKM](/ghkm-rule-extraction/) rules, let one side of a rule be a tree fragment of several levels. Flattening each fragment to its root and its frontier gives an SCFG rule, so the translation relation is the same, but the tree that the rules build differs.

## References
