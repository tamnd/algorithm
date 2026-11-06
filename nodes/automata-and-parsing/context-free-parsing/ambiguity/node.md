---
tag: RMZ192
kind: concept
slug: ambiguity
name: Grammar ambiguity
aliases:
- ambiguous grammar
area: automata-and-parsing/context-free-parsing
level: intro
summary: A grammar is ambiguous if some string has two distinct parse trees or leftmost derivations.
prereqs: [context-free-grammar, parse-tree, leftmost-derivation]
see_also: [inherent-ambiguity, cfg-ambiguity-problem, cfg-ambiguity-undecidable, shift-reduce-conflict, glr-parsing, most-probable-parse, abstract-syntax-tree, catalan-numbers]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.4, Ambiguity in Grammars and Languages (5.4.1 to 5.4.4, with leftmost derivations as a way to express ambiguity and the inherently ambiguous language of 5.4.4)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Context-Free Grammars, the part Ambiguity (the definition by leftmost derivations)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.2.5, Ambiguity, Section 4.3.2, Eliminating Ambiguity (the dangling else), and Section 4.8, Using Ambiguous Grammars
  - paper: doi:10.1145/321312.321318
    title: Seymour Ginsburg and Joseph Ullian, Ambiguity in context free languages, Journal of the ACM 13(1) (1966)
    locator: pp. 62 to 89 (inherently ambiguous languages, and the undecidability of inherent ambiguity)
---

A [context-free grammar](/context-free-grammar/) is ambiguous when some string of its language has two different [parse trees](/parse-tree/), or, equivalently, two different [leftmost derivations](/leftmost-derivation/). An ambiguous grammar gives a string two structures, for example two orders of evaluation for `1 - 2 - 3`, so a compiler cannot use it without extra rules. Ambiguity is a property of the grammar, not of the language: most ambiguous grammars have an unambiguous equivalent, but some [languages](/context-free-language/) have only ambiguous grammars. No algorithm can decide whether a grammar is ambiguous.

## In plain words

A grammar is a set of rules that build strings. When you read a string with a grammar, you find out which rules built it, and in what nesting. This nesting is a tree, and the tree is the meaning: it says what is grouped with what.

A grammar is ambiguous when one string can be built in two different ways, with two different trees. For a calculator this is bad: "one minus two minus three" can mean "(one minus two) minus three" or "one minus (two minus three)", and these give different answers.

Two derivations that differ only in which rule is applied first do not count. Only a different tree counts. Grammar writers remove ambiguity by adding rules for precedence and grouping, or by telling the parser which choice to prefer.

## The idea

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$ and the start symbol $S$; $n$ is the length of the input and $|G|$ is the size of the grammar. These are the conventions of all pages of this area.

**Definition.** A string $w \in \Sigma^*$ is *derived ambiguously* by $G$ if there are two different parse trees with root $S$ and yield $w$. The grammar $G$ is *ambiguous* if it derives some string ambiguously, and *unambiguous* otherwise. The *degree of ambiguity* of $w$ is its number of parse trees, which can be any natural number or infinite.

**Trees, leftmost and rightmost derivations.** For each $A \in V$ and $w \in \Sigma^*$, the parse trees with root $A$ and yield $w$, the leftmost derivations $A \Rightarrow^*_{lm} w$ and the rightmost derivations $A \Rightarrow^*_{rm} w$ are in bijection. A leftmost derivation always rewrites the leftmost nonterminal. So it is fixed by the list of productions it uses, in order. From a tree, list the productions at its inner nodes in preorder (a node, then its subtrees from left to right). This list gives a leftmost derivation, because preorder expands the leftmost unexpanded node first. Conversely, a leftmost derivation builds a unique tree: each step expands the leftmost leaf labeled by a nonterminal with the production of the step. The two maps are inverse to each other. Rightmost derivations work the same way with the mirror order. So "two parse trees", "two leftmost derivations" and "two rightmost derivations" give the same definition of ambiguity.

Two arbitrary derivations are not enough. With $S \to AB$, $A \to a$, $B \to b$, the string $ab$ has two derivations, $S \Rightarrow AB \Rightarrow aB \Rightarrow ab$ and $S \Rightarrow AB \Rightarrow Ab \Rightarrow ab$, but one tree. The grammar is unambiguous.

**Inherent ambiguity.** A context-free language $L$ is [inherently ambiguous](/inherent-ambiguity/) if every grammar $G$ with $L(G) = L$ is ambiguous. Such languages exist. Hopcroft, Motwani and Ullman (Section 5.4.4) prove it for

$$L = \{ a^n b^n c^m d^m : n, m \ge 1 \} \cup \{ a^n b^m c^m d^n : n, m \ge 1 \}.$$

Each grammar for $L$ gives two parse trees to $a^n b^n c^n d^n$ for some $n$, because such a string belongs to both parts and no grammar can tell which part made it.

**Deciding ambiguity.** Ambiguity is semi-decidable: list the strings of $\Sigma^*$ and count the parse trees of each one up to two. But the [CFG ambiguity problem](/cfg-ambiguity-problem/) is undecidable ([theorem](/cfg-ambiguity-undecidable/)), and so is the question whether the language of a grammar is inherently ambiguous (Ginsburg and Ullian, 1966). Some sufficient tests exist: each [LL(k)](/ll-grammar/) and each [LR(k)](/lr-grammar/) grammar is unambiguous, so a parser generator that builds a table without conflicts has also proved that the grammar is unambiguous.

**Removing ambiguity.** There are two standard methods.

- Rewrite the grammar. Add one nonterminal for each level of precedence, and make the recursion left or right to fix the associativity. The grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to a$ gives each string one tree, with $*$ binding tighter than $+$ and both operators grouping to the left.
- Keep the ambiguous grammar and resolve the conflicts of the parser with rules. A yacc grammar declares `%left '+'` and gives `*` a higher precedence. The parse table then drops one action of each [shift-reduce conflict](/shift-reduce-conflict/).

## Examples

**Arithmetic.** The grammar $E \to E + E \mid E * E \mid a$ is ambiguous. The string $a + a * a$ has two trees, one for $a + (a * a)$ and one for $(a + a) * a$. A sum of $k + 1$ copies of $a$ with $k$ plus signs has $C_k = \frac{1}{k+1}\binom{2k}{k}$ trees, the [Catalan number](/catalan-numbers/), because a tree is a full binary bracketing of the $k + 1$ operands:

| plus signs $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| parse trees | 1 | 1 | 2 | 5 | 14 | 42 | 132 |

The layered grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to a$ generates the same language and gives each of $a + a * a$, $a * a + a$ and $a + a + a$ exactly one tree.

**Dangling else.** Write $i$ for "if $b$ then", $e$ for "else" and $a$ for another statement. The grammar $S \to i S \mid i S e S \mid a$ is ambiguous: $i\,i\,a\,e\,a$ has two trees, one where the $e$ belongs to the inner $i$ and one where it belongs to the outer $i$, and $i\,i\,i\,a\,e\,a$ has three. The grammar

$$S \to M \mid U, \qquad M \to i M e M \mid a, \qquad U \to i S \mid i M e U$$

generates the same strings and gives each one tree (Aho, Lam, Sethi and Ullman, Section 4.3.2), in which each $e$ matches the nearest unmatched $i$. Most languages use this rule, and yacc gets it by preferring shift in the conflict.

**Infinite degree.** The grammar $S \to S S \mid (S) \mid \varepsilon$ of balanced parentheses gives the string $()$ infinitely many trees, because $S \Rightarrow SS$ followed by $S \Rightarrow \varepsilon$ can be inserted any number of times. The grammar $S \to (S) S \mid \varepsilon$ generates the same language and is unambiguous. More generally, if a useful nonterminal $A$ has $A \Rightarrow^+ A$, the grammar is ambiguous.

**An inherently ambiguous language.** The grammar

$$S \to AB \mid C, \quad A \to aAb \mid ab, \quad B \to cBd \mid cd, \quad C \to aCd \mid aDd, \quad D \to bDc \mid bc$$

generates the language $L$ of the previous section. The strings $aabbcd$ and $abbccd$ have one tree each, and $a^n b^n c^n d^n$ has two trees for each $n \ge 1$, one through $AB$ and one through $C$. By the theorem cited above, no other grammar for $L$ avoids this.

## Where it is used

- **Parser construction.** An LR or LL parser generator reports an ambiguous grammar as a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/). [Yacc](/yacc/) and its successors resolve such conflicts by precedence declarations, as in Section 4.8 of Aho, Lam, Sethi and Ullman.
- **Abstract syntax.** The [abstract syntax tree](/abstract-syntax-tree/) is built from the parse tree, so an ambiguous grammar makes the meaning of a program depend on the parser.
- **General parsers.** [GLR parsing](/glr-parsing/), the [Earley parser](/earley-parser/) and the [CYK algorithm](/cyk-algorithm/) accept ambiguous grammars and return all trees in a [shared packed parse forest](/shared-packed-parse-forest/), whose size stays polynomial even when the number of trees is exponential.
- **Natural language.** Sentences such as "I saw the man with the telescope" are ambiguous in every reasonable grammar of English. A [probabilistic grammar](/probabilistic-context-free-grammar/) ranks the trees and returns the [most probable parse](/most-probable-parse/).
- **Decision problems.** The [CFG ambiguity problem](/cfg-ambiguity-problem/) and its [undecidability](/cfg-ambiguity-undecidable/), and [ambiguity detection for regular expressions](/regex-ambiguity-detection/), which is decidable.

## References
