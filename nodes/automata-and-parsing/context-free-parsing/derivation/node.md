---
tag: 0FM3NA
kind: concept
slug: derivation
name: Derivation
aliases:
- production sequence
area: automata-and-parsing/context-free-parsing
level: intro
summary: A sequence of production applications that rewrites the start symbol into a string.
prereqs: [context-free-grammar]
see_also: [leftmost-derivation, sentential-form, parse-tree, handle, ambiguity, top-down-parsing, bottom-up-parsing]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.1.3, Derivations Using a Grammar; Section 5.1.4, Leftmost and Rightmost Derivations; Section 5.2, Parse Trees (the equivalence of trees, leftmost derivations and rightmost derivations)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.2.3, Derivations; Section 4.2.4, Parse Trees and Derivations
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 2.2.2, Generating Sentences from a Formal Grammar; Section 3.1, The Parse Tree; Section 3.2, Two Ways to Parse a Sentence
---

A derivation is a finite sequence of rewriting steps of a [context-free grammar](/context-free-grammar/), each of which replaces one nonterminal by the right side of one of its productions. A derivation from the start symbol to a string of terminals is a proof that the string is in the language of the grammar. Parsers are programs that find derivations: a top-down parser builds a leftmost derivation from the start symbol, and a bottom-up parser builds a rightmost derivation backwards from the input.

## In plain words

A grammar is a set of replacement rules. A rule says that a placeholder may be replaced by a given sequence of words and placeholders. You start with one placeholder, the start symbol. At each step you pick one placeholder in your current line and replace it by one of its rules. When no placeholder is left, you have a sentence of the language, and the list of lines you wrote is a derivation of it.

Many derivations can lead to the same sentence, because you can often choose which placeholder to replace first. Two fixed habits remove that freedom: always replace the leftmost placeholder, or always the rightmost one. A derivation also has a tree shape that ignores the order of the steps, and parsers work with that tree.

## The idea

Let $G = (V, \Sigma, P, S)$ be a context-free grammar, written in the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the length of the derived terminal string.

**Steps and derivations.** For $\beta, \gamma \in (V \cup \Sigma)^*$ and a production $A \to \alpha$, the pair $\beta A \gamma \Rightarrow \beta \alpha \gamma$ is a **derivation step**. A **derivation** of length $m \ge 0$ is a sequence

$$\alpha_0 \Rightarrow \alpha_1 \Rightarrow \cdots \Rightarrow \alpha_m,$$

and we write $\alpha_0 \Rightarrow^m \alpha_m$, $\alpha_0 \Rightarrow^* \alpha_m$ for some $m \ge 0$, and $\alpha_0 \Rightarrow^+ \alpha_m$ for some $m \ge 1$. Each $\alpha_i$ in a derivation from $S$ is a [sentential form](/sentential-form/). A string $w \in \Sigma^*$ is in $L(G)$ exactly when there is a derivation $S \Rightarrow^* w$.

**Leftmost and rightmost.** A step $\beta A \gamma \Rightarrow \beta \alpha \gamma$ is **leftmost** if $\beta \in \Sigma^*$, so $A$ is the leftmost nonterminal, and **rightmost** if $\gamma \in \Sigma^*$. A [leftmost derivation](/leftmost-derivation/) uses only leftmost steps, written $\Rightarrow_{lm}$; a rightmost derivation uses only rightmost steps, written $\Rightarrow_{rm}$.

**Derivations and parse trees.** Each derivation $S \Rightarrow^* w$ defines a [parse tree](/parse-tree/): the root is $S$, and the step that rewrites an occurrence of $A$ by $X_1 \cdots X_k$ gives that occurrence the children $X_1, \ldots, X_k$ (one child $\varepsilon$ when $k = 0$). The tree forgets the order of the steps. Conversely, each order of the internal nodes of a tree in which every parent comes before its children is a derivation. Two facts tie the three objects together:

- Each parse tree of $w$ comes from exactly one leftmost derivation and exactly one rightmost derivation. Expanding the internal nodes in preorder gives the leftmost one, and expanding them in the preorder that visits children from right to left gives the rightmost one.
- So the number of parse trees of $w$, the number of leftmost derivations of $w$ and the number of rightmost derivations of $w$ are equal. A grammar is [ambiguous](/ambiguity/) when this number exceeds 1 for some $w$.

**The splitting lemma.** The fact that makes context-free parsing work by dynamic programming is this one.

> **Lemma.** If $X_1 X_2 \cdots X_k \Rightarrow^m w$ with each $X_i \in V \cup \Sigma$ and $w \in \Sigma^*$, then $w = w_1 w_2 \cdots w_k$ with $X_i \Rightarrow^{m_i} w_i$ for each $i$ and $m_1 + \cdots + m_k = m$.

*Proof.* Induction on $m$. If $m = 0$ then $X_1 \cdots X_k = w$, so each $X_i$ is a terminal; take $w_i = X_i$ and $m_i = 0$. If $m \ge 1$, the first step rewrites some $X_j = A$ by a production $A \to \alpha$, so $X_1 \cdots X_{j-1}\, \alpha\, X_{j+1} \cdots X_k \Rightarrow^{m-1} w$. By the induction hypothesis applied to the symbols of this string, $w$ splits into pieces, one for each symbol, with step counts that sum to $m - 1$. Let $w_j$ be the concatenation of the pieces of the symbols of $\alpha$, with $m_j - 1$ the sum of their counts. Then $\alpha \Rightarrow^{m_j - 1} w_j$ by doing the derivations of the pieces one after the other, so $A \Rightarrow^{m_j} w_j$, and the other pieces keep their counts. The counts sum to $(m - 1) + 1 = m$. $\blacksquare$

So whether $A$ derives a substring $w[i..j]$ depends only on that substring and on which productions of $A$ split it into derivable parts. The [CYK algorithm](/cyk-algorithm/) and the [Earley parser](/earley-parser/) are tables of exactly these facts.

**Length of a derivation in Chomsky normal form.** If every production has the form $A \to BC$ or $A \to a$ ([Chomsky normal form](/chomsky-normal-form/)), every derivation $S \Rightarrow^* w$ with $|w| = n \ge 1$ has exactly $2n - 1$ steps. Each terminal of $w$ comes from one step $A \to a$, which gives $n$ steps. The steps $A \to BC$ are the internal nodes of a full binary tree whose $n$ leaves are the nodes rewritten by $A \to a$, and such a tree has $n - 1$ internal nodes. Without this form, a derivation of a short string can be arbitrarily long, for example by unit cycles $A \Rightarrow B \Rightarrow A$.

## Examples

**One string, many derivations.** Take the expression grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to (\,E\,) \mid a.$$

The leftmost derivation of $a + a * a$ is

$$E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow a + T \Rightarrow a + T * F \Rightarrow a + F * F \Rightarrow a + a * F \Rightarrow a + a * a,$$

and the rightmost derivation is

$$E \Rightarrow E + T \Rightarrow E + T * F \Rightarrow E + T * a \Rightarrow E + F * a \Rightarrow E + a * a \Rightarrow T + a * a \Rightarrow F + a * a \Rightarrow a + a * a.$$

Both have 8 steps and give the same parse tree. That tree has 8 internal nodes: the root $E$, the left subtree $E, T, F$, and the right subtree $T, T, F, F$. Every order of these 8 nodes with parents before children is a derivation. For a tree, the count of such orders is $8!$ divided by the product of the subtree sizes, $8 \cdot 3 \cdot 2 \cdot 1 \cdot 4 \cdot 2 \cdot 1 \cdot 1 = 384$. So $a + a * a$ has $40320 / 384 = 105$ derivations in all, exactly one of them leftmost and one rightmost.

**Two leftmost derivations mean ambiguity.** With $E \to E + E \mid a$, the string $a + a + a$ has two leftmost derivations:

$$E \Rightarrow E + E \Rightarrow a + E \Rightarrow a + E + E \Rightarrow a + a + E \Rightarrow a + a + a,$$

$$E \Rightarrow E + E \Rightarrow E + E + E \Rightarrow a + E + E \Rightarrow a + a + E \Rightarrow a + a + a.$$

The first groups the input as $a + (a + a)$ and the second as $(a + a) + a$. So this grammar is ambiguous.

**A derivation that never ends in a string.** With $S \to aS \mid b$, the derivation $S \Rightarrow aS \Rightarrow aaS$ is a valid derivation of the sentential form $aaS$, and one more step $S \to b$ gives $aab$. With only $S \to aS$, every derivation keeps one $S$, so the language is empty although derivations of every length exist.

## Where it is used

- A [top-down parser](/top-down-parsing/) such as [recursive descent](/recursive-descent-parsing/) or an [LL(1) parser](/ll1-parsing/) builds the leftmost derivation of the input from left to right.
- A [bottom-up parser](/bottom-up-parsing/) such as an [LR parser](/lr-parsing/) builds the rightmost derivation in reverse. At each step it finds the [handle](/handle/) of the current right sentential form and replaces it by a nonterminal.
- The [CYK algorithm](/cyk-algorithm/), the [Earley parser](/earley-parser/) and [chart parsing](/chart-parsing/) tabulate the splitting lemma over all substrings.
- The equivalence of grammars and [pushdown automata](/pushdown-automaton/) ([CFG to PDA conversion](/cfg-to-pda-conversion/)) lets the stack hold the unexpanded suffix of a leftmost sentential form.
- Proofs about grammars, such as the [pumping lemma for context-free languages](/cfl-pumping-lemma/), argue on derivations or on their trees.

## References
