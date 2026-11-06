---
tag: S37P6R
kind: concept
slug: inherent-ambiguity
name: Inherent ambiguity
aliases:
- inherently ambiguous language
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A context-free language for which every grammar generating it is ambiguous.
prereqs: [ambiguity, context-free-language, cfl-pumping-lemma]
see_also: [cfg-ambiguity-undecidable, cfg-ambiguity-problem, deterministic-context-free-language, knuth-lr-theorem, parikh-theorem, generating-functions, glr-parsing, shared-packed-parse-forest]
sources:
  - paper: doi:10.1145/321356.321364
    title: Rohit J. Parikh, On context-free languages, Journal of the ACM 13(4) (1966)
    locator: pp. 570 to 581
  - paper: doi:10.1007/BF01694004
    title: William Ogden, A helpful result for proving inherent ambiguity, Mathematical Systems Theory 2(3) (1968)
    locator: pp. 191 to 194
  - paper: doi:10.1145/321312.321318
    title: Seymour Ginsburg and Joseph Ullian, Ambiguity in context free languages, Journal of the ACM 13(1) (1966)
    locator: pp. 62 to 89
  - paper: doi:10.1016/0304-3975(87)90011-9
    title: Philippe Flajolet, Analytic models and ambiguity of context-free languages, Theoretical Computer Science 49(2-3) (1987)
    locator: pp. 283 to 309
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, Addison-Wesley, 1979
    locator: Section 4.7, The existence of inherently ambiguous context-free languages
  - paper: doi:10.1016/S0049-237X(08)72023-8
    title: Noam Chomsky and Marcel-Paul Schützenberger, The algebraic theory of context-free languages, in Computer Programming and Formal Systems, North-Holland (1963)
    locator: pp. 118 to 161
---

A [context-free language](/context-free-language/) is inherently ambiguous if every [context-free grammar](/context-free-grammar/) for it is [ambiguous](/ambiguity/), so that no grammar gives each word a single parse tree. Ambiguity is usually a defect of one grammar that a better grammar removes; inherent ambiguity is a property of the language itself. Parikh proved in 1961 that such languages exist, and the standard example is $\{a^i b^j c^k : i = j \text{ or } j = k\}$.

## In plain words

A grammar is ambiguous when some sentence can be built in two different ways. Often we can rewrite the grammar so that every sentence has only one structure, as compilers do for arithmetic expressions. For some languages this is impossible. Take the strings of a's, then b's, then c's, where the a's and b's match in number, or the b's and c's do. A grammar must pair the a's with the b's to produce the first kind of string, and the b's with the c's for the second kind. A string where all three numbers are equal is of both kinds, and every grammar for the language builds some such strings in both ways. No clever grammar can avoid this, so the ambiguity belongs to the language and not to the grammar.

## The idea

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

**Definitions.** A grammar $G$ is *ambiguous* if some word of $L(G)$ has two different [parse trees](/parse-tree/), or equivalently two different leftmost derivations. A context-free language $L$ is *inherently ambiguous* if every context-free grammar $G$ with $L(G) = L$ is ambiguous. Otherwise $L$ is *unambiguous*: some grammar for it gives every word exactly one parse tree.

**Where the unambiguous languages are.** Every regular language is unambiguous: a deterministic finite automaton with states $q$ gives the grammar with productions $q \to a\, q'$ for each move $q \xrightarrow{a} q'$ and $q \to \varepsilon$ for each accepting $q$, and a word has one derivation because it has one run. Every [deterministic context-free language](/deterministic-context-free-language/) is unambiguous, because it has an [LR(1) grammar](/lr-grammar/) ([Knuth's LR theorem](/knuth-lr-theorem/)) and an LR($k$) grammar is never ambiguous. The even palindromes $\{w w^R\}$ are unambiguous, with the grammar $S \to a S a \mid b S b \mid \varepsilon$, but they are not deterministic. So

$$\text{regular} \subsetneq \text{deterministic} \subsetneq \text{unambiguous} \subsetneq \text{context-free}.$$

**Why $L = \{a^i b^j c^k : i = j \text{ or } j = k\}$ is inherently ambiguous.** The language has the ambiguous grammar

$$S \to X C \mid A Y, \quad X \to a X b \mid \varepsilon, \quad C \to c C \mid \varepsilon, \quad A \to a A \mid \varepsilon, \quad Y \to b Y c \mid \varepsilon,$$

in which a word has two parse trees exactly when $i = j = k$. The proof that every grammar for $L$ is ambiguous uses Ogden's lemma, a stronger form of the [pumping lemma](/cfl-pumping-lemma/) in which some positions of the word are *marked*. For every grammar $G$ there is a number $p$ such that every word $z \in L(G)$ with at least $p$ marked positions can be written $z = u v w x y$ where $v x$ has at least one marked position, $v w x$ has at most $p$ marked positions, and the parse tree of $z$ has a node labelled $A$ with $A \Rightarrow^* v A x$ below it, so that $u v^m w x^m y \in L(G)$ for all $m \ge 0$, with a parse tree that repeats this part.

Let $G$ be any grammar for $L$, let $p$ be its constant, and let $N = p!$, so that $N \ge p$ and every $s \le p$ divides $N$. Take $z = a^N b^N c^{2N}$ and mark the $a$'s. Then $v x$ has an $a$. If $x$ had an $a$, then $v$ and $x$ would both lie in the block of $a$'s, pumping would change only the number of $a$'s, and the words would leave $L$. So $v = a^s$ with $1 \le s \le p$, and $x$ lies in one block. If $x \in c^*$, then for $m = 2$ the word has $i = N + s \ne N = j$ and $k \ge 2N > j$, so it is not in $L$. So $x = b^t$. If $t \ne s$, then $i \ne j$ for every $m \ne 1$, while $j = k$ holds for at most one $m$, so some pumped word is not in $L$. Hence $t = s$. Pump with $m = N/s + 1$: the result is $a^{2N} b^{2N} c^{2N}$, and its parse tree $T_1$ has a node whose subtree yields $v^m w x^m$, a word with no $c$ and more than $N$ $b$'s. In the same way, from $a^{2N} b^N c^N$ with the $c$'s marked, we get a parse tree $T_2$ of the same word $a^{2N} b^{2N} c^{2N}$ with a node whose subtree yields a word with no $a$ and more than $N$ $b$'s.

If $T_1 = T_2$, this one tree has both nodes. Their yields are not nested, because one yield has an $a$ and no $c$, and the other has a $c$ and no $a$. So the two yields are disjoint, and together they contain more than $2N$ $b$'s, but the word has only $2N$. So $T_1 \ne T_2$, and $G$ is ambiguous. Ogden introduced his lemma for proofs of this kind, and Hopcroft and Ullman use it in the same way for the similar language $\{a^m b^m c^l d^l\} \cup \{a^m b^l c^l d^m\}$.

## Examples

- **$\{a^i b^j c^k : i = j \text{ or } j = k\}$.** Inherently ambiguous, by the argument above. The words with $i = j = k$ are the ones that cause the ambiguity.
- **$\{a^m b^m c^l d^l : m, l \ge 1\} \cup \{a^m b^l c^l d^m : m, l \ge 1\}$.** Inherently ambiguous; the words $a^m b^m c^m d^m$ are in both parts.
- **Ambiguous grammars of unambiguous languages.** The grammar $E \to E + E \mid E * E \mid a$ is ambiguous, but its language $a ((+ \mid *)\, a)^*$ is regular, and the grammar $E \to E + T \mid T$, $T \to T * a \mid a$ is unambiguous. The "dangling else" grammar of many programming languages is ambiguous, but the language also has an unambiguous grammar.
- **Unambiguous but not deterministic.** The even palindromes, and $\{a^m b^m\} \cup \{a^m b^{2m}\}$ with the grammar $S \to A \mid B$, $A \to a A b \mid a b$, $B \to a B b b \mid a b b$, are unambiguous but not deterministic, as the [deterministic context-free language](/deterministic-context-free-language/) page proves.
- **A union of two unambiguous languages.** $\{a^i b^i c^k\}$ and $\{a^i b^j c^j\}$ are both deterministic, but their union is the inherently ambiguous language above. So the unambiguous languages are not closed under union.

## Where it is used

- **Grammar design.** For a parser that builds one tree per input, as in a compiler, the grammar must be unambiguous, or the parser must break ties by rules such as operator precedence and associativity ([operator-precedence parsing](/operator-precedence-parsing/)). Inherent ambiguity marks the limit of this: for an inherently ambiguous language, every grammar has words with two trees, and a parser must either pick one by an outside rule or return all of them.
- **General parsing.** Parsers for any grammar, such as the [Earley parser](/earley-parser/) and [GLR parsing](/glr-parsing/), return all parse trees in a [shared packed parse forest](/shared-packed-parse-forest/). Natural languages are full of ambiguity, and their grammars are used with such parsers and with probabilities that rank the trees.
- **Decision problems.** It is undecidable whether a context-free grammar is ambiguous ([undecidability of ambiguity](/cfg-ambiguity-undecidable/)). Ginsburg and Ullian showed in 1966 that it is also undecidable whether the language of a grammar is inherently ambiguous.
- **Counting words.** Chomsky and Schützenberger showed that an unambiguous grammar gives a system of polynomial equations for the [generating function](/generating-functions/) that counts the words of each length, so the generating function of an unambiguous language is algebraic. Flajolet used this in 1987 in the other direction: if the generating function of a language is not algebraic, the language is inherently ambiguous. This proves inherent ambiguity for some languages where pumping arguments are hard to apply.
- **Language classes.** Inherent ambiguity separates the unambiguous languages from the context-free languages. With the even palindromes, which separate the deterministic languages from the unambiguous ones, it shows that each class in the chain above is strictly larger than the one before it.

## References
