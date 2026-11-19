---
tag: BT4KA7
kind: model
slug: combinatory-categorial-grammar
name: Combinatory categorial grammar
aliases:
- CCG
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "A lexicalized grammar whose words have functor categories such as (S\\NP)/NP, combined by application, composition and type raising."
prereqs: [context-free-grammar, lambda-calculus]
see_also: [tree-adjoining-grammar, supertagging, combinatory-logic, simply-typed-lambda-calculus, semantic-parsing, cyk-algorithm, feature-structure-unification, a-star-parsing]
sources:
  - book: isbn:9780262194204
    title: "Mark Steedman, The Syntactic Process, MIT Press, 2000"
    locator: "the combinatory rules of application, composition, type raising and substitution, and their use for coordination and extraction"
  - paper: "K. Vijay-Shanker and David J. Weir, The equivalence of four extensions of context-free grammars, Mathematical Systems Theory 27(6), 511-546, 1994"
    title: "K. Vijay-Shanker and David J. Weir, The equivalence of four extensions of context-free grammars"
    locator: "the weak equivalence of CCG, tree-adjoining grammar, linear indexed grammar and head grammar"
  - paper: "K. Vijay-Shanker and David J. Weir, Parsing some constrained grammar formalisms, Computational Linguistics 19(4), 591-636, 1993"
    title: "K. Vijay-Shanker and David J. Weir, Parsing some constrained grammar formalisms"
    locator: "the polynomial recognition algorithm for CCG"
  - paper: doi:10.1162/coli_a_00324
    title: "Marco Kuhlmann, Giorgio Satta and Peter Jonsson, On the complexity of CCG parsing, Computational Linguistics 44(3), 447-482, 2018"
    locator: "the universal recognition problem for CCG: EXPTIME-complete in general and NP-complete without empty categories"
  - paper: "Stephen Clark and James R. Curran, Wide-coverage efficient statistical parsing with CCG and log-linear models, Computational Linguistics 33(4), 493-552, 2007"
    title: "Stephen Clark and James R. Curran, Wide-coverage efficient statistical parsing with CCG and log-linear models"
    locator: "Section 8 (the supertagger and its 425 categories), Section 9 (adaptive supertagging and CKY parsing) and the evaluation on DepBank"
  - paper: "Luke S. Zettlemoyer and Michael Collins, Learning to map sentences to logical form: structured classification with probabilistic categorial grammars, UAI 2005, 658-666"
    title: "Luke S. Zettlemoyer and Michael Collins, Learning to map sentences to logical form"
    locator: "the CCG lexicon with lambda-calculus semantics and the log-linear model over derivations"
---

Combinatory categorial grammar (CCG) puts almost all of the grammar in the lexicon: each word gets a category such as $(S\backslash NP)/NP$, which says "give me a noun phrase on the right, then a noun phrase on the left, and I make a sentence". A small fixed set of rules then combines neighboring categories by function application, function composition and type raising. The rules are the combinators B, T and S of [combinatory logic](/combinatory-logic/), and each rule builds a term of the [lambda calculus](/lambda-calculus/) for the meaning in step with the syntax: the lambda calculus is the language of the meanings, while CCG is the grammar that decides which terms to build and in what order, without variables of its own. CCG is the formalism behind many [supertagging](/supertagging/) parsers and [semantic parsers](/semantic-parsing/), and it is weakly equivalent to [tree-adjoining grammar](/tree-adjoining-grammar/).

## The machine

**Categories.** Fix a finite set $N$ of atomic categories, such as $S$, $NP$, $N$ and $PP$. Every atomic category is a category, and if $X$ and $Y$ are categories then so are $X/Y$ and $X\backslash Y$. The category $X/Y$ is a function that takes an argument $Y$ on its right and gives $X$; $X\backslash Y$ takes $Y$ on its left. Slashes associate to the left, so $(S\backslash NP)/NP$ is a transitive verb: it takes the object on the right first, then the subject on the left.

**Grammar.** We write the grammar as $G = (N, \Sigma, R, S)$, where $\Sigma$ is the set of words, $R$ is the lexicon, a finite set of pairs of a word and a category, together with the rule schemata the grammar allows, and $S \in N$ is the start category. The size $g$ is the total length of the lexical entries. Each lexical entry also carries a lambda term for its meaning.

**Rules.** The common schemata, with the meaning each one builds:

| rule | name | syntax | meaning |
|---|---|---|---|
| $>$ | forward application | $X/Y \quad Y \Rightarrow X$ | $f\,a$ |
| $<$ | backward application | $Y \quad X\backslash Y \Rightarrow X$ | $f\,a$ |
| $>\mathbf{B}$ | forward composition | $X/Y \quad Y/Z \Rightarrow X/Z$ | $\lambda z.\, f\,(g\,z)$ |
| $<\mathbf{B}$ | backward composition | $Y\backslash Z \quad X\backslash Y \Rightarrow X\backslash Z$ | $\lambda z.\, f\,(g\,z)$ |
| $>\mathbf{B}_\times$ | forward crossed composition | $X/Y \quad Y\backslash Z \Rightarrow X\backslash Z$ | $\lambda z.\, f\,(g\,z)$ |
| $>\mathbf{T}$ | forward type raising | $X \Rightarrow T/(T\backslash X)$ | $\lambda f.\, f\,a$ |
| $<\mathbf{T}$ | backward type raising | $X \Rightarrow T\backslash(T/X)$ | $\lambda f.\, f\,a$ |
| $>\mathbf{S}$ | forward substitution | $(X/Y)/Z \quad Y/Z \Rightarrow X/Z$ | $\lambda z.\, f\,z\,(g\,z)$ |

Generalized composition $>\mathbf{B}^k$ lets the second category have $k$ arguments, $X/Y \quad (\ldots(Y/Z_1)\ldots)/Z_k \Rightarrow (\ldots(X/Z_1)\ldots)/Z_k$, for $k$ up to a fixed bound. Coordination uses the category $(X\backslash X)/X$ for "and", with the meaning of a conjunction at the type of $X$. Composition is Curry's combinator $\mathbf{B}$, type raising is $\mathbf{T}$ and substitution is $\mathbf{S}$, which gives the grammar its name. A string of words is in the language if some choice of lexical categories, combined by the rules, gives $S$.

**An example.** Take the lexicon `Kim`, `Sandy`, `broccoli` $\vdash NP$, `likes` $\vdash (S\backslash NP)/NP : \lambda x.\lambda y.\,\mathit{like}(y, x)$, `hates` the same with $\mathit{hate}$, and `and` $\vdash (X\backslash X)/X$. The sentence "Kim likes and Sandy hates broccoli" coordinates two strings that are not constituents in a [context-free grammar](/context-free-grammar/):

1. `Kim` $\Rightarrow S/(S\backslash NP) : \lambda f.\, f\,\mathit{kim}$ by $>\mathbf{T}$.
2. `Kim likes` $\Rightarrow S/NP : \lambda x.\,\mathit{like}(\mathit{kim}, x)$ by $>\mathbf{B}$.
3. `Sandy hates` $\Rightarrow S/NP : \lambda x.\,\mathit{hate}(\mathit{sandy}, x)$ in the same way.
4. `and Sandy hates` $\Rightarrow (S/NP)\backslash(S/NP)$ by $>$, and then `Kim likes and Sandy hates` $\Rightarrow S/NP : \lambda x.\,\mathit{like}(\mathit{kim}, x) \wedge \mathit{hate}(\mathit{sandy}, x)$ by $<$.
5. Adding `broccoli` by $>$ gives $S : \mathit{like}(\mathit{kim}, \mathit{broccoli}) \wedge \mathit{hate}(\mathit{sandy}, \mathit{broccoli})$.

The meaning comes out by [beta reduction](/beta-reduction/) of the terms the rules build. The same rules give extraction, as in "the broccoli that Kim likes", where `Kim likes` is again $S/NP$.

## What it counts

**Recognition and parsing time.** A chart parser fills items $(X, i, j)$, which say that the category $X$ derives the words of the span $(i, j)$. Spans are fenceposts: $(i, j)$ covers the words $i + 1$ to $j$ of a sentence of $n$ words. If the categories that can appear in a derivation form a finite set, which holds when composition and type raising are bounded so that no category grows with $n$, the grammar is context-free in effect and the [CKY algorithm](/cyk-algorithm/) recognizes it in $O(n^3)$ time for a fixed grammar (theorem). With generalized composition the categories in a derivation can grow with $n$, and Vijay-Shanker and Weir (1993) gave a polynomial algorithm that shares the stack-like tails of categories, with the same $O(n^6)$ time as for tree-adjoining grammar (theorem).

**Grammar size.** When the grammar is part of the input, the problem is much harder. Kuhlmann, Satta and Jonsson (2018) showed that universal recognition for CCG in the Vijay-Shanker and Weir style is EXPTIME-complete, and NP-complete when lexical entries for the empty string are not allowed (theorem). So the polynomial bounds above hide a factor that is exponential in $g$.

**Spurious ambiguity.** One reading can have many derivations. "Kim likes broccoli" can be derived by $>$ then $<$, or by $>\mathbf{T}$, $>\mathbf{B}$ and $>$; composition is associative, so both give the same term (theorem). A parser that does not restrict derivations spends time on these copies. Eisner (1996) gave a normal form that keeps one derivation for each reading in a restricted CCG, by forbidding the output of a composition to be the function of a later composition or application (theorem).

**Ambiguity in practice.** With a wide-coverage lexicon each word has many categories; in Clark and Curran's tag dictionary the word "is" has 45. The number of lexical choices is the main cost of parsing, which is why parsers first prune the categories with a supertagger (heuristic, with the measurements below).

## Relation to other models

- **Context-free grammar.** Categorial grammar with only application, the AB grammar of Ajdukiewicz and Bar-Hillel, is weakly equivalent to context-free grammar (theorem, Bar-Hillel, Gaifman and Shamir 1960). Composition and type raising are what take CCG beyond it.
- **Tree-adjoining grammar.** CCG, [tree-adjoining grammar](/tree-adjoining-grammar/), linear indexed grammar and head grammar generate the same class of string languages (theorem, Vijay-Shanker and Weir 1994). All four are mildly context-sensitive: they generate $\{a^m b^m c^m d^m\}$ and cross-serial dependencies, yet parse in polynomial time. The structures they assign differ: TAG builds trees by adjunction, CCG builds derivations of categories.
- **Lambda calculus and combinatory logic.** Each rule is a combinator, and a derivation builds a term of the [simply typed lambda calculus](/simply-typed-lambda-calculus/) whose types follow the categories, for example $NP \mapsto e$ and $S\backslash NP \mapsto e \to t$. The lambda calculus has variables and abstraction; CCG has neither in its syntax, and builds the same terms by combinators.
- **Dependency grammar.** The function-argument pairs of a derivation give word-to-word dependencies, which is how CCG parsers are often evaluated.
- **Feature structures.** Atomic categories often carry features such as $S[\mathit{dcl}]$ or $NP[\mathit{nb}]$, which match by a light form of [feature structure unification](/feature-structure-unification/).

## Known results in the model

- **CCGbank.** Hockenmaier and Steedman converted the Penn Treebank into CCG derivations, which gave a corpus for training wide-coverage CCG parsers.
- **Wide-coverage parsing (measurement).** Clark and Curran (2007) kept the 425 categories that occur at least 10 times in sections 02 to 21 of CCGbank. Their log-linear supertagger reached 92.6% per-word accuracy on section 00 with gold part-of-speech tags, and 91.5% with automatic tags. Their CKY parser over the pruned categories reached more than 81% F-score on the DepBank evaluation.
- **Semantic parsing (measurement and method).** Zettlemoyer and Collins (2005) learned a CCG lexicon with lambda-calculus meanings from sentences labeled only with logical forms, and trained a log-linear model over derivations. Many later [semantic parsers](/semantic-parsing/) use CCG in the same way.
- **A\* parsing.** Because a supertag-factored model scores a derivation by its lexical categories, [A\* parsing](/a-star-parsing/) with an estimate built from the supertag scores finds the best derivation while building few chart items (heuristic, with measurements in the work of Lewis and Steedman).

## References
