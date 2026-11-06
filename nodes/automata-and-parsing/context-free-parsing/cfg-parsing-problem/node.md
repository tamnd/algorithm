---
tag: 3G12K0
kind: problem
slug: cfg-parsing-problem
name: CFG parsing problem
aliases:
- parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Given a grammar and a string in its language, produce a parse tree or derivation.
model: word-ram
complexity:
  vars: {n: the input length, g: the grammar size}
  time: {worst: O(n^3 g)}
prereqs: [cfg-membership-problem, parse-tree, derivation]
see_also: [context-free-language-recognition, shared-packed-parse-forest, earley-parser, cyk-algorithm, glr-parsing, lr-parsing, ll1-parsing, ambiguity]
sources:
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 3, Introduction to Parsing (parse trees, parse forests, and the classes of parsing methods), and Chapter 4, General Non-Directional Parsing (CYK)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.1, Introduction (the role of the parser), Section 4.4, Top-Down Parsing, and Section 4.5, Bottom-Up Parsing
  - paper: doi:10.1145/505241.505242
    title: Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1) (2002)
    locator: pp. 1 to 15 (the definition of c-parsing and the reduction from Boolean matrix multiplication)
  - paper: doi:10.3115/981623.981641
    title: Sylvie Billot and Bernard Lang, The structure of shared forests in ambiguous parsing, 27th Annual Meeting of the Association for Computational Linguistics (1989)
    locator: pp. 143 to 151 (all parse trees in a shared forest of polynomial size)
  - paper: doi:10.1016/j.scico.2009.07.001
    title: Elizabeth Scott and Adrian Johnstone, Recognition is not parsing, SPPF-style parsing from cubic recognisers, Science of Computer Programming 75(1-2) (2010)
    locator: pp. 55 to 70 (building a binarized shared packed parse forest in cubic time)
---

The CFG parsing problem asks, for a [context-free grammar](/context-free-grammar/) $G$ and a string $w$, for a [parse tree](/parse-tree/) of $w$, or a report that $w \notin L(G)$. It extends the [membership problem](/cfg-membership-problem/), which asks only for yes or no, and every general recognizer, such as [CYK](/cyk-algorithm/) or [Earley](/earley-parser/), can be extended to output a tree in the same $O(n^3 |G|)$ time. When the grammar is [ambiguous](/ambiguity/) a string can have exponentially many or infinitely many trees, so the problem has variants that ask for one tree, for a compact representation of all trees, or for the best tree under some weight.

## In plain words

Knowing that a sentence is grammatical is not enough for a compiler. It needs to know the structure: which part is the condition of an "if", which numbers an operator adds. A parse tree shows that structure, with the whole string at the root and the letters at the leaves.

A parser finds such a tree. Some parsers work from the top, guessing which rule the whole string came from. Others work from the bottom, gluing letters into larger and larger pieces. Fast parsers make no wrong guesses, but they work only for grammars of a special kind. General parsers accept any grammar and fill a table of all pieces that each rule can build, then read a tree out of the table.

If the string has several trees, a parser must choose one or return all of them in a shared form.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $n$ is the length of the input $w = w_1 \cdots w_n$, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

**Input.** A context-free grammar $G$ and a string $w \in \Sigma^*$.

**Output.** A parse tree with root $S$ and yield $w$, or "no" if $w \notin L(G)$.

A parse tree can be given in several equivalent ways: as a tree, as a [leftmost derivation](/leftmost-derivation/), which is the preorder list of its productions, or as a rightmost derivation in reverse, which is the postorder list and the order in which a [bottom-up parser](/bottom-up-parsing/) finds them.

**The size of a tree.** If $G$ has no cycle $A \Rightarrow^+ A$, every parse tree of $w$ has $O(n)$ nodes for a fixed grammar: a path that repeats a label over the same span, or inside a subtree with empty yield, would give such a cycle. If $G$ has a cycle through a useful nonterminal, some strings have infinitely many trees, but cutting out the repeated parts always leaves a tree with $O(n)$ nodes. So the output of the basic problem is small.

## Variants

- **All trees.** Output every parse tree. Their number can be exponential in $n$ or infinite, so the usual output is a [shared packed parse forest](/shared-packed-parse-forest/), a graph whose nodes are triples $(A, i, j)$ meaning $A \Rightarrow^* w_{i+1} \cdots w_j$, with packed nodes for the alternatives. For a binarized grammar it has $O(n^3 |G|)$ size (Billot and Lang; Scott and Johnstone).
- **Counting.** Compute the number of parse trees, or detect that it is infinite. Dynamic programming over the forest gives it with $O(n^3 |G|)$ arithmetic operations.
- **Best tree.** For a [probabilistic grammar](/probabilistic-context-free-grammar/), output the [most probable parse](/most-probable-parse/), by the Viterbi variant of CYK.
- **c-parsing.** Lee's form: output, for each pair $i < j$ and nonterminal $A$, whether $A$ derives $w_{i+1} \cdots w_j$ and that span is consistent with a full parse. Every general tabular parser computes this.
- **Deterministic parsing.** Restrict $G$ to a class where a parser makes no guesses, such as [LL(1)](/ll1-parsing/) or [LR(1)](/lr-parsing/), and get the tree in $O(n)$ time. The parser must also report an error at the first symbol that cannot continue a sentence.
- **Error recovery and partial parsing.** Output a tree of a nearby string in $L(G)$, or trees of the longest parsable pieces, when $w \notin L(G)$.
- **Incremental parsing.** After an edit of $w$, update the tree by reparsing only the changed region.

## Examples

For the unambiguous expression grammar
$$E \to E + T \mid T, \quad T \to T * F \mid F, \quad F \to ( E ) \mid a,$$
the input $a + a * a$ has exactly one tree,
$$[E\ [E\ [T\ [F\ a]]]\ +\ [T\ [T\ [F\ a]]\ *\ [F\ a]]],$$
in which $*$ binds tighter than $+$. Its leftmost derivation is
$$E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow a + T \Rightarrow a + T * F \Rightarrow a + F * F \Rightarrow a + a * F \Rightarrow a + a * a.$$
The input $a * ( a$ has no tree, and a parser reports the error at the end of the input, where a $)$ is missing.

For the ambiguous grammar $E \to E + E \mid E * E \mid ( E ) \mid a$, a script counts 2 trees for $a + a * a$, 5 trees for $a + a + a + a$ and 14 trees for $a * a * a * a * a$: the Catalan number $C_k$ for $k$ operators. A parser must choose, and the usual choice uses precedence and associativity rules outside the grammar. For $S \to a S b \mid S S \mid \varepsilon$ the input $ab$ has infinitely many trees, since $S \Rightarrow S S$ with an empty $S$ can repeat.

## Known algorithms

- **General, tabular.** [CYK](/cyk-algorithm/) in $O(n^3 |G|)$ for a grammar in [Chomsky normal form](/chomsky-normal-form/) or a binary form; [Earley](/earley-parser/) in $O(n^3 |G|)$ for every grammar, $O(n^2 |G|)$ for unambiguous ones; [chart parsing](/chart-parsing/) as the common framework. A tree is read from the table by following back pointers.
- **General, by matrix multiplication.** [Valiant's algorithm](/valiant-algorithm/) in $O(|G| n^\omega)$.
- **Generalized LR.** [GLR](/glr-parsing/) runs an LR automaton with a graph-structured stack and builds a shared forest; it is linear on deterministic grammars.
- **Deterministic top-down.** [LL(1)](/ll1-parsing/) table parsing and [recursive descent](/recursive-descent-parsing/), $O(n)$, for LL grammars.
- **Deterministic bottom-up.** [Shift-reduce](/shift-reduce-parsing/) parsing with [LR(0)](/lr0-parsing/), [SLR](/slr-parsing/), [LALR(1)](/lalr-parsing/) or [canonical LR(1)](/canonical-lr-parsing/) tables, $O(n)$, and [operator precedence](/operator-precedence-parsing/) parsing.
- **Backtracking.** [Backtracking parsers](/backtracking-parsing/) try the alternatives in order; they are simple and can take exponential time.

## Bounds

**Upper bounds.** $O(n^3 |G|)$ for one tree or the whole forest, $O(|G| n^\omega)$ for one tree with Valiant's method, and $O(n)$ for the deterministic classes.

**Lower bounds.** A tree has $\Omega(n)$ nodes, so $\Omega(n)$ time is needed, and no better unconditional bound is known. Lee showed that c-parsing in $O(|G| n^{3 - \epsilon})$ time gives Boolean matrix multiplication of $m \times m$ matrices in $O(m^{3 - \epsilon/3})$ time, so a fast practical parser for all grammars would give a fast practical matrix product. The bounds for [membership](/cfg-membership-problem/) apply as well, since a parser decides membership.

**Output size.** Listing all trees takes time proportional to their number, which can be $C_k \approx 4^k / k^{3/2}$ for a string with $k$ operators, so the forest is the only polynomial output for all trees.

## Reductions

- **From membership.** A parser decides membership: it outputs a tree exactly when $w \in L(G)$.
- **To membership, with tables.** The table of CYK or Earley answers membership for every nonterminal and span, and a tree is read from it top-down in $O(n^2 |G|)$ further time by choosing, for $(A, i, j)$, a production and a split point that the table confirms.
- **From Boolean matrix multiplication**, by Lee, for c-parsing.
- **Of a pushdown automaton.** A sequence of moves of a [pushdown automaton](/pushdown-automaton/) built from $G$ by the [standard conversion](/cfg-to-pda-conversion/) is a leftmost derivation of $G$, so a run that accepts $w$ is a parse.

## Applications

- **Compilers and interpreters**, which build a parse tree or an [abstract syntax tree](/abstract-syntax-tree/) for each source file, usually with an LR or LL parser.
- **Natural language processing**, where chart parsers and probabilistic grammars find the structure of sentences.
- **Data formats and protocols**, such as JSON, XML and network messages, which are parsed into trees before use.
- **Bioinformatics**, where a parse of an RNA sequence under a grammar is a [secondary structure](/rna-secondary-structure/).
- **Editors and tools**, where incremental parsers keep a tree up to date for syntax highlighting and refactoring.

## References
