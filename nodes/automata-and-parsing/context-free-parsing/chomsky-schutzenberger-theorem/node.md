---
tag: GK5A6Y
kind: theorem
slug: chomsky-schutzenberger-theorem
name: Chomsky-Schützenberger representation theorem
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Every context-free language is a homomorphic image of the intersection of a Dyck language with a regular language.
prereqs: [dyck-language, chomsky-normal-form, cfl-closure-properties]
see_also: [context-free-language, regular-language, parse-tree, pushdown-automaton, deterministic-context-free-language, cfl-reachability, context-free-grammar]
sources:
  - paper: doi:10.1016/S0049-237X(08)72023-8
    title: Noam Chomsky and Marcel-Paul Schützenberger, The algebraic theory of context-free languages, in Computer Programming and Formal Systems, Studies in Logic and the Foundations of Mathematics 35, North-Holland (1963)
    locator: pp. 118 to 161
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Supplementary Lecture G, The Chomsky-Schützenberger Theorem
  - paper: doi:10.1007/978-3-642-59136-5_3
    title: Jean-Michel Autebert, Jean Berstel and Luc Boasson, Context-free languages and pushdown automata, in Handbook of Formal Languages, Volume 1, Springer (1997)
    locator: pp. 111 to 174
  - paper: doi:10.1007/978-3-642-31653-1_12
    title: Alexander Okhotin, Non-erasing variants of the Chomsky-Schützenberger theorem, Developments in Language Theory, LNCS 7410 (2012)
    locator: pp. 121 to 129
---

The Chomsky-Schützenberger theorem says that every [context-free language](/context-free-language/) is obtained from a [Dyck language](/dyck-language/) of balanced brackets in two simple steps: intersect it with a [regular language](/regular-language/), then rename or erase the brackets with a homomorphism. The converse also holds, so this is an exact description of the class. It shows that nesting, as in balanced brackets, is the only thing that context-free languages add to regular languages.

## Statement

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$. For $k \ge 0$, $D_k$ is the Dyck language over $k$ pairs of brackets $[_1, ]_1, \ldots, [_k, ]_k$: the strings in which the brackets match. A homomorphism $h : \Delta^* \to \Sigma^*$ is given by a string $h(c) \in \Sigma^*$ for each letter $c$, and $h(c_1 \cdots c_m) = h(c_1) \cdots h(c_m)$; it may map a letter to $\varepsilon$.

**Theorem (Chomsky and Schützenberger).** A language $L \subseteq \Sigma^*$ is context-free if and only if there are a number $k$, a regular language $R$ over the $2k$ brackets of $D_k$, and a homomorphism $h$ from the brackets to $\Sigma^*$ such that

$$L = h(D_k \cap R).$$

The proof below gives more: $R$ can be a *local* language, defined only by its allowed first letters, its allowed last letters and its allowed pairs of adjacent letters, and for a grammar $G$ in [Chomsky normal form](/chomsky-normal-form/) one can take $k = 2|P|$, two pairs of brackets for each production.

**Small examples.** With one pair $[\,]$ and $h([) = a$, $h(]) = b$, we have $D_1 \cap [^* ]^* = \{[^m ]^m : m \ge 0\}$, so $\{a^m b^m : m \ge 0\} = h(D_1 \cap [^* ]^*)$. With two pairs $[\,]$ and $(\,)$, a word of $D_2$ in which all left brackets come first is a string $u$ of left brackets followed by the mirror image of $u$ with each bracket closed, so with $h([) = h(]) = a$ and $h(() = h()) = b$ the even palindromes are $\{w w^R : w \in \{a, b\}^*\} = h(D_2 \cap \{[, (\}^* \{], )\}^*)$.

## In plain words

Write a parse tree as a string of brackets: open a bracket when you enter a node and close it when you leave. The result is always balanced, and a few simple rules about which bracket may follow which make sure that the brackets come from real grammar rules. A finite automaton can check those rules, because each rule looks at only two neighbouring brackets. Then erase all brackets except the ones that stand for the letters at the leaves, and what remains is the word that the tree derives. So every context-free language is "balanced brackets, filtered by a finite automaton, then relabelled".

## Proof

**If.** $D_k$ is context-free; it has the grammar $S \to [_1 S ]_1 S \mid \cdots \mid [_k S ]_k S \mid \varepsilon$. The intersection of a context-free language with a regular language is context-free, and the image of a context-free language under a homomorphism is context-free ([closure properties](/cfl-closure-properties/)). So $h(D_k \cap R)$ is context-free.

**Only if.** Let $L$ be context-free. If $L \subseteq \{\varepsilon\}$, take $k = 0$ and $R = L$. Otherwise take a grammar $G = (V, \Sigma, P, S)$ for $L$ in [Chomsky normal form](/chomsky-normal-form/): every production is $A \to B C$ with $B, C \in V$ or $A \to a$ with $a \in \Sigma$, except that $S \to \varepsilon$ is allowed when $S$ is on no right side. Let $P'$ be the set of productions other than $S \to \varepsilon$. For each $\pi \in P'$ take two new pairs of brackets $[^1_\pi, ]^1_\pi$ and $[^2_\pi, ]^2_\pi$; so $k = 2|P'|$. Let $D$ be the Dyck language over these pairs.

*The homomorphism.* $h([^1_\pi) = a$ if $\pi$ is $A \to a$, and $h$ maps every other bracket to $\varepsilon$.

*The bracketed grammar.* Let $G'$ have the nonterminals of $G$ and, for each $\pi \in P'$, the production

$$A \to [^1_\pi\, B\, ]^1_\pi\, [^2_\pi\, C\, ]^2_\pi \ \text{ if } \pi = A \to B C, \qquad A \to [^1_\pi\, ]^1_\pi\, [^2_\pi\, ]^2_\pi \ \text{ if } \pi = A \to a.$$

Let $G_0 = (V, \Sigma, P', S)$, and write $L_{G_0}(A)$ and $L_{G'}(A)$ for the terminal strings that $A$ derives in $G_0$ and in $G'$. A derivation tree of $G'$ becomes a derivation tree of $G_0$ when we delete the brackets, and conversely; by induction on the height of the tree, the tree of $G'$ with frontier $x$ corresponds to a tree of $G_0$ with frontier $h(x)$, because $h([^1_\pi\, ]^1_\pi\, [^2_\pi\, ]^2_\pi) = a$ for $\pi = A \to a$, and $h$ erases the four brackets of $A \to B C$. So

$$h(L_{G'}(A)) = L_{G_0}(A) \quad \text{for every } A \in V. \tag{1}$$

*The regular language.* For a nonterminal $A$ let $R_A$ be the set of nonempty strings over the brackets that satisfy:

- **(F)** the first letter is $[^1_\pi$ for some $\pi \in P'$ with left side $A$;
- **(E)** the last letter is $]^2_\pi$ for some $\pi$;
- **(N)** each letter $u$ that is not the last one is followed by a letter $v$ as follows:
  - if $u = [^1_\pi$ with $\pi = A' \to B C$, then $v = [^1_\sigma$ for some $\sigma$ with left side $B$; if $u = [^2_\pi$ with $\pi = A' \to B C$, then $v = [^1_\sigma$ for some $\sigma$ with left side $C$;
  - if $u = [^j_\pi$ with $\pi = A' \to a$, then $v = ]^j_\pi$, for $j = 1, 2$;
  - if $u = ]^1_\pi$, then $v = [^2_\pi$;
  - if $u = ]^2_\pi$, then $v$ is a right bracket.

These conditions look only at the first letter, the last letter and pairs of adjacent letters, so a finite automaton that remembers the last letter read accepts $R_A$, and $R_A$ is regular. Let $R = R_S \cup \{\varepsilon\}$ if $\varepsilon \in L$, and $R = R_S$ otherwise.

**Claim.** $D \cap R_A = L_{G'}(A)$ for every nonterminal $A$.

($\supseteq$) By induction on the derivation. Let $x \in L_{G'}(A)$ come from the production for $\pi \in P'$. If $\pi = A \to a$, then $x = [^1_\pi\, ]^1_\pi\, [^2_\pi\, ]^2_\pi$, which is balanced and satisfies (F), (E) and (N). If $\pi = A \to B C$, then $x = [^1_\pi\, y\, ]^1_\pi\, [^2_\pi\, z\, ]^2_\pi$ with $y \in L_{G'}(B)$ and $z \in L_{G'}(C)$, and by induction $y \in D \cap R_B$ and $z \in D \cap R_C$. Then $x$ is balanced. (F) and (E) hold for $x$. The pairs of adjacent letters inside $y$ and inside $z$ satisfy (N). The other pairs are: $[^1_\pi$ and the first letter of $y$, which is $[^1_\sigma$ with left side $B$ by (F) for $y$; the last letter of $y$, which is some $]^2_\rho$ by (E), and $]^1_\pi$, a right bracket; $]^1_\pi$ and $[^2_\pi$; $[^2_\pi$ and the first letter of $z$, which has left side $C$; the last letter of $z$, a $]^2_\rho$, and $]^2_\pi$. All of them satisfy (N), so $x \in D \cap R_A$.

($\subseteq$) By induction on the length of $x \in D \cap R_A$. By (F), $x$ starts with $[^1_\pi$, where $\pi$ has left side $A$. As $x$ is balanced, this bracket is closed by a $]^1_\pi$, so $x = [^1_\pi\, y\, ]^1_\pi\, x'$ with $y$ balanced. By (E), $]^1_\pi$ is not the last letter, and by (N) the next letter is $[^2_\pi$; it is closed in turn, so $x' = [^2_\pi\, z\, ]^2_\pi\, x''$ with $z$ balanced. Then $x''$ is balanced too. If $x''$ were not empty, it would begin with a left bracket, but by (N) the letter after $]^2_\pi$ is a right bracket. So $x'' = \varepsilon$ and $x = [^1_\pi\, y\, ]^1_\pi\, [^2_\pi\, z\, ]^2_\pi$.

- If $\pi = A \to a$, then by (N) $[^1_\pi$ is followed by $]^1_\pi$ and $[^2_\pi$ by $]^2_\pi$, so $y = z = \varepsilon$ and $x$ is the right side of the production of $G'$ for $\pi$.
- If $\pi = A \to B C$, then by (N) the letter after $[^1_\pi$ is a left bracket $[^1_\sigma$ with $\sigma$ a production of $B$, so $y$ is not empty and satisfies (F) for $B$. The last letter of $y$ is a right bracket, since $y$ is balanced and nonempty, and it is followed by $]^1_\pi$; by (N) a $]^1_\rho$ is followed by $[^2_\rho$, so the last letter of $y$ is a $]^2_\rho$, and $y$ satisfies (E). The pairs inside $y$ are pairs of $x$, so $y$ satisfies (N). Hence $y \in D \cap R_B$, and in the same way $z \in D \cap R_C$. Both are shorter than $x$, so by induction $y \in L_{G'}(B)$ and $z \in L_{G'}(C)$, and $x \in L_{G'}(A)$. $\square$

**End of the proof.** Every nonempty string of $R$ is in $R_S$, and $\varepsilon \in D$, so

$$D \cap R = (D \cap R_S) \cup (\{\varepsilon\} \text{ if } \varepsilon \in L) = L_{G'}(S) \cup (\{\varepsilon\} \text{ if } \varepsilon \in L).$$

By (1), $h(D \cap R) = L_{G_0}(S) \cup (\{\varepsilon\} \text{ if } \varepsilon \in L)$. The production $S \to \varepsilon$ can only be used at the root, because $S$ is on no right side, so $L_{G_0}(S) = L \setminus \{\varepsilon\}$ and $h(D \cap R) = L$. $\blacksquare$

**Example.** For $G$ with $\pi_1 = S \to A B$, $\pi_2 = A \to a$, $\pi_3 = B \to b$, the only string of $D \cap R$ is

$$[^1_1\ [^1_2\, ]^1_2\, [^2_2\, ]^2_2\ ]^1_1\ [^2_1\ [^1_3\, ]^1_3\, [^2_3\, ]^2_3\ ]^2_1,$$

which is the parse tree of $ab$ written with brackets. The homomorphism keeps $h([^1_2) = a$ and $h([^1_3) = b$ and erases the rest, which gives $ab$.

## Consequences

- **One generator for the whole class.** Two pairs of brackets are enough if inverse homomorphisms are allowed. Let $g([_i) = a\, b^i$ and $g(]_i) = \bar b^i\, \bar a$, where $a, \bar a$ and $b, \bar b$ are the two pairs of $D_2$. Then $D_k = g^{-1}(D_2)$. If $x \in D_k$, then clearly $g(x) \in D_2$. For the converse, let $g(x) \in D_2$ with $x$ not empty, and check $g(x)$ with a stack. The word $x$ starts with a left bracket, so it has a factor $[_i\, ]_j$. When the stack check reads $\bar b^j \bar a$ after $a\, b^i$, the top of the stack is $b^i$ above $a$; if $j > i$, a $\bar b$ meets the $a$, and if $j < i$, the $\bar a$ meets a $b$, and both fail. So $j = i$, and after the factor the stack is the same as before it, so $g(x)$ with the factor removed is also balanced. By induction on $|x|$ the shorter word is in $D_k$, and so is $x$. Hence every context-free language is $h(g^{-1}(D_2) \cap R)$: the context-free languages are the smallest class that contains $D_2$ and is closed under homomorphism, inverse homomorphism and intersection with regular languages.
- **Every context-free language is an image of a deterministic one.** $D_k \cap R$ is a [deterministic context-free language](/deterministic-context-free-language/): a deterministic pushdown automaton checks the brackets with its stack and runs a finite automaton for $R$ in its state. So every context-free language is a homomorphic image of a deterministic one. Since some context-free languages are not deterministic, the deterministic context-free languages are not closed under homomorphism.
- **Parse trees as strings.** The proof shows that the parse trees of a grammar, written with brackets, form the set $D \cap R$. The same view of nesting as matched brackets is used in [CFL reachability](/cfl-reachability/), where paths in a graph must spell words of a context-free language, often a Dyck language of matching calls and returns.

## Tightness

- **The regular language is needed.** $D_k$ contains $\varepsilon$ and is closed under concatenation, so $h(D_k)$ also contains $\varepsilon$ and is closed under concatenation. So the language $\{a\}$ is not $h(D_k)$ for any $k$ and $h$.
- **The Dyck language is needed.** If $D_k$ is replaced by a regular language, $h(R)$ is regular, since regular languages are closed under intersection and homomorphism. So $\{a^m b^m : m \ge 0\}$ is not obtained.
- **Erasing.** Every nonempty word of $D_k$ has length at least 2, so if no letter is mapped to $\varepsilon$, then $h(D_k \cap R)$ contains no word of length 1, and $\{a\}$ cannot be obtained. Okhotin showed in 2012 that this is the only obstacle: every context-free language with no words of length 1 has a representation in which $h$ maps no letter to $\varepsilon$.
- **The number of pairs.** In the construction, $k = 2|P'|$ depends on the grammar. With the encoding $g$ above, two pairs suffice when an inverse homomorphism is allowed.

## History

Chomsky and Schützenberger published the theorem in 1963, in their paper on the algebraic theory of context-free languages, which studies context-free grammars with formal power series. Kozen's textbook gives a proof in one of its supplementary lectures. Autebert, Berstel and Boasson survey the theorem and its variants in the Handbook of Formal Languages. Okhotin studied in 2012 when the homomorphism can be taken to be non-erasing.

## References
