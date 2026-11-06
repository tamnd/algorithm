---
tag: QHNBWP
kind: concept
slug: leftmost-derivation
name: Leftmost derivation
aliases:
- left derivation
area: automata-and-parsing/context-free-parsing
level: intro
summary: A derivation that always expands the leftmost nonterminal, matching top-down parsing.
prereqs: [context-free-grammar, derivation]
see_also: [parse-tree, sentential-form, top-down-parsing, ll1-parsing, recursive-descent-parsing, ambiguity, bottom-up-parsing, handle]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.1.4, Leftmost and Rightmost Derivations; Section 5.2.6, From Trees to Derivations; Section 5.4.3, Leftmost Derivations as a Way to Express Ambiguity
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Context-Free Grammars, the part on ambiguity (the definition of a leftmost derivation)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.2.3, Derivations; Section 4.4, Top-Down Parsing
---

A leftmost derivation is a [derivation](/derivation/) of a [context-free grammar](/context-free-grammar/) in which each step rewrites the leftmost nonterminal of the current string. Each [parse tree](/parse-tree/) has exactly one leftmost derivation, so leftmost derivations are a linear way to write parse trees, and a grammar is [ambiguous](/ambiguity/) exactly when some string has two of them. A [top-down parser](/top-down-parsing/) builds the leftmost derivation of its input step by step, from left to right.

## In plain words

A grammar rewrites placeholders into words. When the current line has several placeholders, you can choose which one to rewrite next. A leftmost derivation always picks the first placeholder from the left.

This habit has two effects. First, the order of the steps is no longer a choice: only the choice of rule is left. So two different leftmost derivations of the same sentence mean two really different structures. Second, the words to the left of the first placeholder never change again. A parser that reads the input from left to right can check these words against the input as soon as they appear. This is what a top-down parser does.

## The idea

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. Lowercase letters $u, v, w$ are strings of terminals, and Greek letters are strings over $V \cup \Sigma$. These are the conventions of all pages of this area.

**Leftmost step.** A step $u A \gamma \Rightarrow u \alpha \gamma$ by a production $A \to \alpha$ is a *leftmost step* when $u \in \Sigma^*$, that is, when $A$ is the leftmost nonterminal of $uA\gamma$. We write it $u A \gamma \Rightarrow_{lm} u \alpha \gamma$. A *leftmost derivation* is a sequence of leftmost steps, and $\Rightarrow_{lm}^*$ is the reflexive and transitive closure of $\Rightarrow_{lm}$. A string $\alpha$ with $S \Rightarrow_{lm}^* \alpha$ is a *left-sentential form*. A rightmost derivation $\Rightarrow_{rm}$ is the mirror image: the step rewrites the rightmost nonterminal.

**Only the rule is a choice.** In a string with at least one nonterminal, the leftmost nonterminal is fixed. So a leftmost derivation from $S$ is fully given by its sequence of productions $p_1, p_2, \ldots, p_m$: step $i$ applies $p_i$ to the leftmost nonterminal, and it is a legal step only when the left side of $p_i$ is that nonterminal. This sequence is the *left parse* of the string, the output of an LL parser.

**Trees and leftmost derivations.** Let $w \in \Sigma^*$.

> **Proposition.** The map that sends a leftmost derivation $S \Rightarrow_{lm}^* w$ to its parse tree is a bijection between the leftmost derivations of $w$ and the parse trees of $w$ with root $S$. The derivation and its tree have the same number of steps and inner nodes.

*Proof.* (Tree from derivation.) Build the tree step by step. Start with one node $S$. A step that rewrites an occurrence of $A$ by $X_1 \cdots X_k$ gives the leaf of that occurrence the children $X_1, \ldots, X_k$, or one child $\varepsilon$ when $k = 0$. The leaves of the tree, read from left to right, always spell the current string, so at the end the tree is a parse tree of $w$, with one inner node for each step.

(Derivation from tree.) Given a parse tree $t$ of $w$, list its inner nodes in preorder (a node before its children, the children from left to right), and apply their productions in this order. We show by induction on $i$ that after $i$ steps the current string is the frontier of the tree made of the first $i$ inner nodes in preorder, and that the leftmost nonterminal of this frontier is the $(i+1)$-th inner node in preorder. In the frontier, every leaf to the left of node $x_{i+1}$ is either a terminal, $\varepsilon$, or an inner node that comes before $x_{i+1}$ in preorder, and all of these have been expanded; so the leaves to its left are terminals. Hence step $i+1$ is a leftmost step. After all inner nodes, the frontier is $w$.

(The two maps are inverse.) The tree of the preorder derivation is $t$, because each step adds exactly the children that $t$ gives that node. Conversely, take a leftmost derivation $D$ and its tree $t$. The node that $D$ expands at step $i+1$ is the leftmost unexpanded nonterminal leaf of the partial tree. In the preorder of $t$, that node is the first inner node not yet expanded, because a node to its left is already fully expanded down to terminals, and a node to its right comes later in preorder. So $D$ expands the nodes of $t$ in preorder, and $D$ is the preorder derivation of $t$. $\blacksquare$

The same argument with the mirror preorder (children from right to left) gives the same bijection for rightmost derivations. Two consequences follow.

- **Every derivation can be made leftmost.** If $S \Rightarrow^* w$ by any derivation, its tree gives a leftmost derivation $S \Rightarrow_{lm}^* w$ with the same productions, each used the same number of times. So $L(G) = \{ w \in \Sigma^* : S \Rightarrow_{lm}^* w \}$.
- **Ambiguity.** A grammar is ambiguous if and only if some string $w$ has two different leftmost derivations, because these are counted by the parse trees.

The proposition is about terminal strings $w$. For a string with nonterminals it fails: if $S \to AB$, $A \to a$ and $B \to b$, then $S \Rightarrow AB \Rightarrow Ab$ is a derivation, but $Ab$ is not a left-sentential form. After the step $S \Rightarrow_{lm} AB$ the next leftmost step must rewrite $A$.

**Why top-down parsers produce it.** Each left-sentential form is $u A \gamma$ with $u \in \Sigma^*$. If it leads to the input $w$, then $u$ is a prefix of $w$, because no later leftmost step changes $u$. A top-down parser keeps exactly this shape: $u$ is the part of the input that it has read, and $A\gamma$ is its stack of symbols that remain to be matched. Its decision at each step is which production of $A$ to apply, and [lookahead](/lookahead-parsing/) at the next tokens of $w$ after $u$ is what an [LL(1) parser](/ll1-parsing/) uses to make it. A bottom-up parser builds a rightmost derivation instead, in reverse order, by finding a [handle](/handle/) at each step.

## Examples

**One tree, one leftmost derivation.** Take the expression grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to ( E ) \mid a.$$

The string $a + a * a$ has one parse tree and so exactly one leftmost derivation, with 8 steps:

$$E \Rightarrow_{lm} E + T \Rightarrow_{lm} T + T \Rightarrow_{lm} F + T \Rightarrow_{lm} a + T \Rightarrow_{lm} a + T * F \Rightarrow_{lm} a + F * F \Rightarrow_{lm} a + a * F \Rightarrow_{lm} a + a * a.$$

Its left parse is the production sequence $E \to E + T$, $E \to T$, $T \to F$, $F \to a$, $T \to T * F$, $T \to F$, $F \to a$, $F \to a$. The rightmost derivation of the same tree uses the same 8 productions in another order:

$$E \Rightarrow_{rm} E + T \Rightarrow_{rm} E + T * F \Rightarrow_{rm} E + T * a \Rightarrow_{rm} E + F * a \Rightarrow_{rm} E + a * a \Rightarrow_{rm} T + a * a \Rightarrow_{rm} F + a * a \Rightarrow_{rm} a + a * a.$$

**Two leftmost derivations.** In the grammar $E \to E + E \mid E * E \mid a$ the same string has two leftmost derivations, one for each tree:

$$E \Rightarrow_{lm} E + E \Rightarrow_{lm} a + E \Rightarrow_{lm} a + E * E \Rightarrow_{lm} a + a * E \Rightarrow_{lm} a + a * a,$$

$$E \Rightarrow_{lm} E * E \Rightarrow_{lm} E + E * E \Rightarrow_{lm} a + E * E \Rightarrow_{lm} a + a * E \Rightarrow_{lm} a + a * a.$$

The first groups the string as $a + (a * a)$ and the second as $(a + a) * a$. So this grammar is ambiguous. In the grammar $E \to E + E \mid a$, the string $a + a + \cdots + a$ with $k$ plus signs has $C_k = \frac{1}{k+1}\binom{2k}{k}$ leftmost derivations, one for each binary tree with $k$ inner nodes: 1, 2, 5, 14 and 42 for $k = 1, \ldots, 5$.

**A non-example.** With $S \to AB$, $A \to a$, $B \to b$, the derivation $S \Rightarrow AB \Rightarrow Ab \Rightarrow ab$ is not leftmost: its second step rewrites $B$ while $A$ is to its left. Its tree has the leftmost derivation $S \Rightarrow_{lm} AB \Rightarrow_{lm} aB \Rightarrow_{lm} ab$, with the same two productions after the first step in the other order.

**Empty right sides.** With $S \to A S b \mid \varepsilon$ and $A \to a \mid \varepsilon$, the string $b$ has the leftmost derivation $S \Rightarrow_{lm} ASb \Rightarrow_{lm} Sb \Rightarrow_{lm} b$. The step $A \to \varepsilon$ removes the leftmost nonterminal, and the next step rewrites the new leftmost one.

## Where it is used

- [Top-down parsing](/top-down-parsing/), [recursive descent parsing](/recursive-descent-parsing/), [LL(1) parsing](/ll1-parsing/) and [LL(k) parsing](/ll-k-parsing/) produce the leftmost derivation of the input. Their stack holds the part $A\gamma$ of the current left-sentential form.
- An [LL(k) grammar](/ll-grammar/) is defined by a condition on two leftmost derivations that agree on the next $k$ input symbols.
- [Left recursion](/left-recursion/) ($A \Rightarrow^+ A \alpha$) makes a leftmost derivation able to grow without reading input, which is why top-down parsers need [left recursion elimination](/left-recursion-elimination/).
- [Ambiguity](/ambiguity/) is counted with leftmost derivations, and the [pushdown automaton](/pushdown-automaton/) made by the [CFG to PDA conversion](/cfg-to-pda-conversion/) simulates leftmost derivations.

## References
