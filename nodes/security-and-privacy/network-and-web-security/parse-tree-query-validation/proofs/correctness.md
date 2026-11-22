---
title: Parse-tree validation accepts exactly the queries whose inputs stay inside their literals
proves: [correctness, complexity]
status: full
---

We use the pseudocode VALIDATE of the page and its toy SQL grammar. The template has static parts $p_0, \ldots, p_k$ and the inputs are $x_1, \ldots, x_k$. Line L1 builds $q = p_0 x_1 p_1 \cdots x_k p_k$ and line L2 builds $q_0$, the same text with each $x_i$ replaced by the one-character placeholder `1`.

**Origins.** Each character of $q$ and of $q_0$ has an origin: $s_m$ for the $m$-th static character, or $h_i$ for a character of input $i$ (in $q_0$, the placeholder of input $i$). Order the origins as they occur in the template: $s_m < h_i$ when the static character $m$ comes before hole $i$, and so on. Along $q$ and along $q_0$ the origins never decrease. Each static origin occurs exactly once in each string, and in $q_0$ each $h_i$ also occurs exactly once, because the placeholder has one character.

**Fact 1.** Let $u$ be a token of $q$ from position $a$ to position $b$, and let $o$ be an origin that occurs exactly once in $q$, at position $p$. Then $p$ is in $u$ if and only if $\mathrm{orig}(a) \le o \le \mathrm{orig}(b)$.

*Proof.* If $a \le p \le b$, monotonicity gives the inequalities. Conversely, if $p < a$ then $o = \mathrm{orig}(p) \le \mathrm{orig}(a)$, and equality would put the unique occurrence of $o$ at $a$, not at $p$; so $o < \mathrm{orig}(a)$. The case $p > b$ is the same. $\square$

The same holds in $q_0$, where all origins are unique.

**The template check.** Lines L3 and L4 require that $q_0$ parses to a tree $A$, and that the placeholder of each input meets exactly one token of $A$, a literal. Call it the literal of input $i$, $\lambda_i$.

**Theorem.** Assume the template passes lines L3 and L4. VALIDATE accepts if and only if (a) $q$ parses to a tree $B$; (b) $B$ and $A$ have the same shape when the text of each literal is erased; and (c) for each $j$, the $j$-th token of $B$ starts and ends at characters whose origins are those of the start and the end of the $j$-th token of $A$. When it accepts:

1. $B$ is $A$ with the text of some literals changed. The structure of the query is the one the programmer planned.
2. Each static character is in the $j$-th token of $q$ if and only if it is in the $j$-th token of $q_0$, and the two tokens have the same kind, and the same text when they are not literals.
3. Each character of $x_i$ that is not a blank is inside the token of $B$ at the position of $\lambda_i$, which is a literal. No character of an input is part of a keyword, a name, an operator or a parenthesis.

*Proof.* Lines L5 and L6 reject when (a) fails, line L7 when (b) fails, and lines L8 and L9 when (c) fails. The leaves of a concrete parse tree are the tokens in order, so (b) gives the same number of tokens and lets line L8 pair them. So VALIDATE accepts exactly when (a), (b) and (c) hold. Claim 1 is (b).

For claim 2, let $s_m$ be a static origin and let $b_j$ and $a_j$ be the $j$-th tokens of $q$ and $q_0$. By Fact 1 in $q$, $s_m$ is in $b_j$ if and only if $\mathrm{orig}(\mathrm{start}\ b_j) \le s_m \le \mathrm{orig}(\mathrm{end}\ b_j)$. By (c) the bounds are those of $a_j$, and by Fact 1 in $q_0$ this holds if and only if $s_m$ is in $a_j$. The kinds and texts agree by (b).

For claim 3, let $c$ be a character of $x_i$ that is not a blank. The lexer puts each character that is not a blank between tokens into a token, so $c$ is in some $b_j$, and by monotonicity $\mathrm{orig}(\mathrm{start}\ b_j) \le h_i \le \mathrm{orig}(\mathrm{end}\ b_j)$. By (c) the same holds for $a_j$, and since $h_i$ occurs once in $q_0$, Fact 1 says that the placeholder is in $a_j$. So $a_j = \lambda_i$, a literal, and by (b) $b_j$ is a literal too. $\square$

**The local form of the condition.** The test of the page checks VALIDATE against a simpler description, input by input. Call hole $i$ *quoted* when $\lambda_i$ is a string literal that starts at the static quote just before the hole and ends at the static quote just after it, and *unquoted* when $\lambda_i$ is the placeholder alone, with a blank, an operator or the end of the text on each side.

**Lemma.** For a template whose holes are all quoted or unquoted, VALIDATE accepts if and only if each quoted input has only runs of quotes of even length, and each unquoted input is blanks, one number or one complete string literal, and blanks.

*Proof.* Only if. Let hole $i$ be quoted. By claim 2, the token of $q$ that holds the static quote before the hole is a string that ends at the static quote after it. The string lexer reads a pair of quotes as one quote and stops at the first quote that is not followed by another. If a quote run of $x_i$ had odd length, its last quote would either end the string inside $x_i$ or pair with the static quote after the hole, and in both cases the string would not end at that static quote. Let hole $i$ be unquoted. By claim 3 the non-blank characters of $x_i$ are all in one literal token $b_j$, and by (c) $b_j$ starts and ends at characters with origin $h_i$, so $b_j$ is inside $x_i$. A literal token is a number or a complete string, and the rest of $x_i$ is blanks.

If. The lexer reads $q$ and $q_0$ the same way up to the first hole. At a quoted hole it is inside the string in both texts; in $q$ it reads the even quote runs of $x_i$ as pairs, so the string does not end inside $x_i$ and continues over the same static text as in $q_0$. At an unquoted hole the character before the hole ends the token before it in both texts, since a blank or an operator is not continued by a digit or a quote; $x_i$ gives exactly one literal token; and the character after the hole starts a new token, since a blank or an operator does not continue a number or a closed string. So the token lists agree in kind, in non-literal text and in the origins of their ends, and the parser, which looks only at kinds and non-literal texts, builds trees of the same shape. $\square$

**Cost.** Let $n = |q| + |q_0|$. The lexer reads each character once, with $O(1)$ work for each, since the operators have at most two characters. The grammar is LL(1), so the recursive descent parser consumes one token per step with no backtracking, in $O(n)$ time. Line L4 looks at each position of $q_0$ once, because the tokens are disjoint. SHAPE and the loop of line L8 visit each node and leaf once. So VALIDATE runs in $\Theta(n)$ time and $O(n)$ space on the word-RAM. $\blacksquare$
