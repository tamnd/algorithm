---
tag: 2X28B6
kind: problem
slug: context-free-language-recognition
name: Parsing context-free grammars
area: automata-and-parsing/context-free-parsing
level: core
summary: Determines whether a string belongs to the language of a context-free grammar and recovers a derivation tree, for example with the CYK algorithm.
prereqs: [context-free-grammar, derivation, parse-tree]
see_also: [cyk-algorithm, earley-parser, valiant-algorithm, cfg-membership-problem, cfg-parsing-problem, glr-parsing, lr-parsing, shared-packed-parse-forest]
sources:
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 3, Introduction to Parsing (3.4.3 Type 2 Grammars, 3.5 An Overview of Context-Free Parsing Methods, 3.10 The Relation between Parsing and Boolean Matrix Multiplication); Section 4.2, The CYK Parsing Method; Chapter 13, Parsing as Intersection
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.4.4, Testing Membership in a CFL
  - paper: doi:10.1016/S0022-0000(75)80046-8
    title: Leslie G. Valiant, General context-free recognition in less than cubic time, Journal of Computer and System Sciences 10(2) (1975)
    locator: pp. 308 to 315
  - paper: doi:10.1145/505241.505242
    title: Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1) (2002)
    locator: pp. 1 to 15
  - paper: doi:10.1137/16M1061771
    title: Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, SIAM Journal on Computing 47(6) (2018)
    locator: pp. 2527 to 2555
  - paper: "Martin Lange and Hans Leiß, To CNF or not to CNF? An efficient yet presentable version of the CYK algorithm, Informatica Didactica 8 (2009)"
    locator: Section 2 (sizes of the normal-form conversions in different orders) and the CYK variant for binary normal form
  - paper: doi:10.1016/0304-3975(76)90068-2
    title: Neil D. Jones and William T. Laaser, Complete problems for deterministic polynomial time, Theoretical Computer Science 3(1) (1976)
    locator: pp. 105 to 117 (P-completeness of context-free grammar problems when the grammar is part of the input)
---

Parsing a context-free grammar is the problem of deciding whether a string belongs to the language of a given [context-free grammar](/context-free-grammar/) and, when it does, producing a [parse tree](/parse-tree/) that shows how the grammar generates it. The decision part alone is recognition, also called the [membership problem](/cfg-membership-problem/). For every grammar the problem is solvable in cubic time in the input length, by the [CYK algorithm](/cyk-algorithm/) or the [Earley parser](/earley-parser/), and in $O(n^\omega)$ time by [Valiant's algorithm](/valiant-algorithm/). Compilers avoid the general problem by restricting the grammar to a class such as LL(1) or LALR(1), for which a deterministic parser runs in linear time.

## In plain words

A grammar is a finite list of replacement rules that describes a set of sentences, for example the valid programs of a language. Given the rules and one sentence, the question is whether the rules can produce that sentence. If they can, we also want the proof: a tree that shows which rule built each part of the sentence. A compiler needs that tree to know what the program means.

The difficulty is that the rules can be used in many orders and many ways, and a sentence can have more than one tree. A general method must find a tree among all these choices without trying them one by one. The classic methods fill a table that records, for each piece of the sentence, which placeholders can produce that piece.

## Definition

We use the notation of the [context-free grammar](/context-free-grammar/) page: $G = (V, \Sigma, P, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $|G|$ for the total length of the productions, and an input $w = a_1 a_2 \cdots a_n \in \Sigma^*$ of length $n$.

A **parse tree** of $w$ for $G$ is an ordered rooted tree whose root is labelled $S$, whose leaves read from left to right spell $w$ (leaves labelled $\varepsilon$ contribute nothing), and in which each internal node labelled $A$ with children labelled $X_1, \ldots, X_k$ satisfies $A \to X_1 \cdots X_k \in P$ (a single child $\varepsilon$ when the production is $A \to \varepsilon$).

- **Recognition.** Input: $G$ and $w$. Output: yes if $w \in L(G)$, that is, if $S \Rightarrow^* w$, and no otherwise.
- **Parsing.** Input: $G$ and $w$. Output: a parse tree of $w$ for $G$ if $w \in L(G)$, and no otherwise.

A parse tree of $w$ exists if and only if $S \Rightarrow^* w$ (see [derivation](/derivation/)), so the parsing output is a certificate for the recognition answer, and it can be checked in time linear in its size.

## Variants

- **Fixed grammar or uniform.** In the *fixed-grammar* version, $G$ is a constant and only $n$ grows; most bounds below are stated this way. In the *uniform* version, $G$ is part of the input and the cost depends on $|G|$ too.
- **All parses.** Output every parse tree. The number of trees can grow exponentially in $n$, and is infinite when the grammar has a cycle $A \Rightarrow^+ A$ or, for the empty input, a nullable loop. A [shared packed parse forest](/shared-packed-parse-forest/) represents all trees in polynomial space, $O(n^3)$ nodes for a grammar whose right sides have length at most 2.
- **Counting.** Output the number of parse trees, which detects whether this string is ambiguous. Deciding whether the grammar is ambiguous for *some* string is undecidable ([CFG ambiguity](/cfg-ambiguity-undecidable/)).
- **Best parse.** With a [probabilistic context-free grammar](/probabilistic-context-free-grammar/), output the [most probable parse](/most-probable-parse/), for example by [probabilistic CKY](/probabilistic-cky/).
- **Restricted grammars.** For [LL(k)](/ll-k-parsing/), [LR(k)](/lr-parsing/), [LALR(1)](/lalr-parsing/) and [SLR(1)](/slr-parsing/) grammars, a deterministic parser decides membership and builds the tree in $O(n)$ time.
- **Incremental and error-correcting.** Re-parse after an edit ([incremental parsing](/incremental-parsing/)), or find the least number of edits that makes $w$ a member.

## Examples

Take the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid a$.

- $w = a + a * a$: yes. The only parse tree has root $E \to E + T$, with left child deriving $a$ through $E \to T \to F \to a$, and right child $T \to T * F$, with its own children deriving $a$ and $a$.
- $w = a + {*}\,a$: no. No production can place $*$ right after $+$.
- $w = \varepsilon$: no, because no nonterminal of this grammar derives $\varepsilon$.

Take the ambiguous grammar $E \to E + E \mid a$.

- $w = a + a + a$: yes, with 2 parse trees. In general, the string with $k$ operators has $C_k = \frac{1}{k+1}\binom{2k}{k}$ parse trees, the [Catalan numbers](/catalan-numbers/) 1, 1, 2, 5, 14, 42 for $k = 0, \ldots, 5$.

Take $S \to SS \mid (\,S\,) \mid \varepsilon$.

- $w = \varepsilon$: yes, and $w$ has infinitely many parse trees, since $S \Rightarrow SS \Rightarrow S$ can repeat. A parser that enumerates trees must stop this, and a recognizer must not loop on it.

## Known algorithms

- [CYK algorithm](/cyk-algorithm/): dynamic programming over substrings, for a grammar in [Chomsky normal form](/chomsky-normal-form/). $\Theta(n^3 |G|)$ time and $\Theta(n^2 |V|)$ space.
- [Earley parser](/earley-parser/): works on any grammar without conversion. $O(n^3)$ time for a fixed grammar, $O(n^2)$ for an unambiguous one, $O(n)$ for many deterministic grammars; Leo's change makes it linear for every LR(k) grammar.
- [Valiant's algorithm](/valiant-algorithm/): reduces recognition to [Boolean matrix multiplication](/boolean-matrix-multiplication/), $O(n^\omega)$ for a fixed grammar, with $\omega < 2.372$.
- [GLR parsing](/glr-parsing/) with a [graph-structured stack](/graph-structured-stack/): an LR parser that forks on conflicts; linear on deterministic grammars and polynomial in general in its later forms.
- [Chart parsing](/chart-parsing/) and [left-corner parsing](/left-corner-parsing/): agenda-driven and hybrid variants of the same tabulation.
- Deterministic parsers for subclasses: [LL(1)](/ll1-parsing/), [LR(0)](/lr0-parsing/), [SLR(1)](/slr-parsing/), [LALR(1)](/lalr-parsing/), [canonical LR(1)](/canonical-lr-parsing/), all $\Theta(n)$ time.
- [Backtracking parsing](/backtracking-parsing/) and naive [recursive descent](/recursive-descent-parsing/): simple, but exponential time in the worst case, and they loop on [left recursion](/left-recursion/).

## Bounds

- **Upper bound, fixed grammar.** $O(n^\omega)$ time on the [word RAM](/word-ram/) by Valiant (1975), where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). Without fast matrix multiplication the best known combinatorial algorithms take $O(n^3 / \log^3 n)$ time, according to Abboud, Backurs and Vassilevska Williams.
- **Upper bound, uniform.** CYK takes $O(n^3 |G'|)$ time on a grammar $G'$ in Chomsky normal form. Converting $G$ in the order: split long right sides, remove $\varepsilon$-productions, remove unit productions, gives $|G'| = O(|G|^2)$, while other orders can be exponential. Lange and Leiß (2009) give a CYK variant that accepts unit and $\varepsilon$-productions in a binarized grammar of size $O(|G|)$ and runs in $O(n^3 |G|)$ time.
- **Unconditional lower bound.** $\Omega(n)$, since a recognizer must read each input symbol. No better unconditional bound is known for a fixed grammar.
- **Conditional lower bounds.** Lee (2002) showed that a parser for a general grammar that runs in $O(|G|\, n^{3 - \epsilon})$ time gives Boolean matrix multiplication of $m \times m$ matrices in $O(m^{3 - \epsilon/3})$ time. Abboud, Backurs and Vassilevska Williams showed that recognition in $O(n^{\omega - \epsilon})$ time for one fixed constant-size grammar, or a combinatorial algorithm in $O(n^{3 - \epsilon})$, would give a faster algorithm for $k$-clique than any known.
- **Uniform version.** When the grammar is part of the input, membership is P-complete under log-space reductions (Jones and Laaser, 1976), so it is unlikely to have a fast parallel algorithm in the size of the grammar.

## Reductions

- **To Boolean matrix multiplication.** Valiant's algorithm computes the CYK table as a transitive closure of an upper-triangular matrix over a nonassociative "product" defined by the grammar, using fast matrix multiplication.
- **From Boolean matrix multiplication.** Lee's reduction builds, from two $m \times m$ Boolean matrices, a grammar and a string whose parse information gives the product.
- **To emptiness.** $w \in L(G)$ if and only if $L(G) \cap \{w\} \neq \emptyset$. The intersection of a grammar with a finite automaton for $\{w\}$ is a grammar with nonterminals $[i, A, j]$, the Bar-Hillel construction, and testing its [emptiness](/cfg-emptiness-problem/) decides membership. Its useful part is exactly the [parse chart](/parse-chart/), which is why parsing is sometimes called intersection.
- **To graph problems.** [CFL reachability](/cfl-reachability/) generalizes recognition from a path (the string) to a graph, and contains the problem as the special case of a path graph.

## Applications

- **Compilers and interpreters.** Each front end parses the program text, almost always with a deterministic subclass ([LALR parsing](/lalr-parsing/) in yacc and Bison, [LL(1)](/ll1-parsing/) or [recursive descent](/recursive-descent-parsing/) in hand-written parsers), and with [GLR](/glr-parsing/) for languages like C++ whose grammars are not deterministic.
- **Natural language.** Grammars of human languages are highly ambiguous, so chart parsers such as [CYK](/cyk-algorithm/) and [Earley](/earley-parser/), with probabilities ([probabilistic CKY](/probabilistic-cky/), the [inside-outside algorithm](/inside-outside-algorithm/)), find the likely trees.
- **Biology.** Stochastic context-free grammars model RNA secondary structure, where paired bases nest like brackets; folding algorithms are CYK-like dynamic programs.
- **Program analysis.** Interprocedural analyses phrased as [CFL reachability](/cfl-reachability/) match calls to returns with a [Dyck language](/dyck-language/).

## References
