---
tag: TT8H7B
kind: definition
slug: probabilistic-context-free-grammar
name: Probabilistic context-free grammar
aliases:
- PCFG
- stochastic context-free grammar
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A context-free grammar whose productions carry probabilities summing to one per nonterminal.
prereqs: [context-free-grammar, parse-tree, ambiguity]
see_also: [probabilistic-cky, most-probable-parse, inside-outside-algorithm, cyk-algorithm, chomsky-normal-form, parse-chart, earley-parser, cfg-emptiness-problem]
sources:
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 11, Probabilistic Context Free Grammars (the definition, the astronomers example, inside and outside probabilities, and consistency)
  - paper: doi:10.1109/T-C.1973.223746
    title: Taylor L. Booth and Richard A. Thompson, Applying probability measures to abstract languages, IEEE Transactions on Computers C-22(5) (1973)
    locator: pp. 442 to 450 (when the probabilities of the finite derivations sum to one, by the first-moment matrix)
  - url: https://aclanthology.org/J98-2005/
    title: Zhiyi Chi and Stuart Geman, Estimation of probabilistic context-free grammars, Computational Linguistics 24(2) (1998)
    locator: pp. 299 to 305 (maximum-likelihood estimates give consistent grammars)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 9, Transformational grammars, and Chapter 10, RNA structure analysis (stochastic context-free grammars for RNA)
---

A probabilistic context-free grammar (PCFG) is a [context-free grammar](/context-free-grammar/) with a probability on each production, such that the productions of each nonterminal have probabilities that sum to 1. The probability of a [parse tree](/parse-tree/) is the product of the probabilities of the productions it uses, and the probability of a string is the sum over its parse trees. A PCFG turns the [ambiguity](/ambiguity/) of a grammar into a ranking: among the trees of a sentence, the most probable one is the preferred reading. PCFGs are the base of statistical parsing of natural language and of models of RNA secondary structure. [Probabilistic CKY](/probabilistic-cky/) finds the [most probable parse](/most-probable-parse/) in cubic time, and the [inside-outside algorithm](/inside-outside-algorithm/) estimates the probabilities from unparsed text.

## Definition

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. A production with probability $p$ is written $A \to \alpha\ [p]$.

**Definition.** A **probabilistic context-free grammar** is a tuple $(V, \Sigma, P, S, q)$, where $(V, \Sigma, P, S)$ is a context-free grammar and $q : P \to [0, 1]$ satisfies, for every nonterminal $A$,

$$\sum_{A \to \alpha \in P} q(A \to \alpha) = 1.$$

A grammar with this property is called **proper**. The number $q(A \to \alpha)$ is read as the probability that a node labeled $A$ is expanded by $A \to \alpha$, independently of everything else in the tree.

**Probabilities of trees and strings.** For a parse tree $t$ with root $S$, let $c(r, t)$ be the number of nodes of $t$ that use the production $r$. Then

$$P(t) = \prod_{r \in P} q(r)^{c(r, t)}, \qquad P(w) = \sum_{t \,:\, \mathrm{yield}(t) = w} P(t), \qquad P(t \mid w) = \frac{P(t)}{P(w)}.$$

The sum for $P(w)$ can have infinitely many terms, for example with cycles of unit productions, but it always converges, since the trees with root $S$ have total probability at most 1. A leftmost derivation corresponds to a unique tree and has the same probability.

**Consistency.** A PCFG is **consistent**, or tight, if $\sum_t P(t) = 1$ over all finite parse trees with root $S$. Then $P$ is a probability distribution on the trees, and $P(w)$ is a distribution on $L(G)$. A proper grammar need not be consistent: the missing mass belongs to the event that the random expansion never stops. Booth and Thompson gave the test. Let $M$ be the $|V| \times |V|$ matrix with

$$M_{A B} = \sum_{A \to \alpha \in P} q(A \to \alpha) \cdot (\text{number of occurrences of } B \text{ in } \alpha),$$

the expected number of $B$ children of an $A$ node. If the spectral radius of $M$ is less than 1, the grammar is consistent and the expected size of a tree is finite; if it is greater than 1 (and every nonterminal is useful), it is not consistent. The tree is a multi-type branching process, and the total probability of the finite trees is its probability of extinction, the least nonnegative solution of a system of polynomial equations, one per nonterminal.

## Examples and non-examples

The probabilities below were computed with exact fractions by a script.

**Prepositional phrase attachment.** The grammar of Manning and Schütze

| production | $q$ | production | $q$ |
|---|---|---|---|
| $S \to NP\ VP$ | 1.0 | $NP \to NP\ PP$ | 0.4 |
| $PP \to P\ NP$ | 1.0 | $NP \to \text{astronomers}$ | 0.1 |
| $VP \to V\ NP$ | 0.7 | $NP \to \text{ears}$ | 0.18 |
| $VP \to VP\ PP$ | 0.3 | $NP \to \text{saw}$ | 0.04 |
| $P \to \text{with}$ | 1.0 | $NP \to \text{stars}$ | 0.18 |
| $V \to \text{saw}$ | 1.0 | $NP \to \text{telescopes}$ | 0.1 |

is proper: the probabilities of the productions of each nonterminal sum to 1. The sentence *astronomers saw stars with ears* has two trees:

- $t_1$, with the phrase *with ears* attached to *stars* by $NP \to NP\ PP$: $P(t_1) = 1.0 \cdot 0.1 \cdot 0.7 \cdot 1.0 \cdot 0.4 \cdot 0.18 \cdot 1.0 \cdot 1.0 \cdot 0.18 = 0.0009072$;
- $t_2$, with *with ears* attached to the verb phrase by $VP \to VP\ PP$: $P(t_2) = 1.0 \cdot 0.1 \cdot 0.3 \cdot 0.7 \cdot 1.0 \cdot 0.18 \cdot 1.0 \cdot 1.0 \cdot 0.18 = 0.0006804$.

So $P(w) = 0.0015876$, and $t_1$ is the most probable parse, with $P(t_1 \mid w) = 4/7$. Here the attachment to the noun wins only because $0.4 \cdot 0.7 > 0.3 \cdot 0.7$; the words themselves play no role, which is the main weakness of plain PCFGs as language models.

**Hidden Markov models.** A right-linear PCFG, with productions $A \to b\, B\ [p]$ and $A \to b\ [p]$, is a hidden Markov model whose states are the nonterminals: $p$ is the product of the probability of emitting $b$ and the probability of moving to $B$. PCFGs extend HMMs as context-free grammars extend [regular grammars](/regular-language/).

**Proper but not consistent.** $S \to S\, S\ [p] \mid a\ [1 - p]$. The total probability $x$ of the finite trees is the least nonnegative solution of $x = p\, x^2 + (1 - p)$, whose roots are $1$ and $(1 - p)/p$. For $p \le 1/2$, $x = 1$ and the grammar is consistent. For $p = 2/3$, $x = 1/2$: half of the probability is on infinite expansions. The matrix $M$ is the single number $2p$, and $2p > 1$ exactly when $p > 1/2$.

**Not proper.** $S \to a\, S\ [0.9] \mid b\ [0.3]$ has weights that sum to 1.2. It is a weighted grammar, not a PCFG. Its weights still define a ranking of trees, and dividing by the total weight $\sum_k 0.9^k \cdot 0.3 = 3$ gives the distribution $P(a^k b) = 0.9^k \cdot 0.1$, which is that of the PCFG $S \to a\, S\ [0.9] \mid b\ [0.1]$. Dividing the weights of each nonterminal by their local sum instead gives $S \to a\, S\ [0.75] \mid b\ [0.25]$, a different distribution.

**Unambiguous grammars.** If the underlying grammar is unambiguous, each string has one tree and $P(w) = P(t)$. The probabilities then only rank strings, not readings.

## Related definitions

- **Inside and outside probabilities.** For a grammar in [Chomsky normal form](/chomsky-normal-form/), the inside probability $\beta_A(i, j)$ is the probability that $A$ derives $w_{i+1} \cdots w_j$, and the outside probability $\alpha_A(i, j)$ is the probability of deriving $w_1 \cdots w_i\, A\, w_{j+1} \cdots w_n$ from $S$. The inside probabilities are the [CYK](/cyk-algorithm/) chart with sums and products in place of "or" and "and", and $P(w) = \beta_S(0, n)$.
- **Most probable parse.** Replacing the sum by a maximum gives the [most probable parse](/most-probable-parse/), computed by [probabilistic CKY](/probabilistic-cky/) in $O(n^3 |G|)$ time. The [Earley parser](/earley-parser/) has a probabilistic version for grammars not in normal form.
- **Estimation.** From a treebank, the maximum-likelihood estimate is the relative frequency $q(A \to \alpha) = c(A \to \alpha) / c(A)$, the number of uses of the production over the number of $A$ nodes. From plain sentences, the [inside-outside algorithm](/inside-outside-algorithm/) is the expectation-maximization method. Chi and Geman (1998) proved that both estimates always give consistent grammars.
- **Weighted grammars.** Replacing probabilities by elements of a semiring gives weighted context-free grammars, used for the number of trees, the best tree, or the sum over trees with one algorithm. A proper and consistent PCFG is the special case of the probability semiring with normalized weights.
- **Emptiness.** A nonterminal that derives no terminal string, as found by the [emptiness test](/cfg-emptiness-problem/), takes probability mass that no finite tree receives. If such a nonterminal is reached from $S$ with positive probability, the grammar is proper but not consistent.

## References
