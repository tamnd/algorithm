---
tag: AW94RC
kind: definition
slug: straight-line-program-grammar
name: Straight-line program for strings
aliases:
- straight-line grammar
- string straight-line program
area: compression-and-coding/dictionary-compression
level: advanced
summary: A grammar in which each nonterminal has exactly one rule and the rules are acyclic, so it derives one string.
prereqs: [context-free-grammar, chomsky-normal-form]
see_also: [grammar-based-compression, smallest-grammar-problem, straight-line-program, re-pair, pattern-matching-in-compressed-text, compressed-indexing, lempel-ziv-factorization, fibonacci-word]
sources:
  - paper: doi:10.1515/gcc-2012-0016
    title: Markus Lohrey, Algorithmics on SLP-compressed strings, a survey, Groups Complexity Cryptology 4(2), 2012, pages 241 to 299
    locator: Section 3 (the definition of SLPs in Chomsky normal form, the size as the number of rules, and the length computation); the later sections on compressed equality and pattern matching
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005
    locator: Section II (grammars that generate one string, the size as the total length of the right-hand sides, and the example a rose is a rose is a rose)
  - paper: doi:10.1145/3457389
    title: Moses Ganardi, Artur Jeż and Markus Lohrey, Balancing straight-line programs, Journal of the ACM 68(4), 2021, Article 27
    locator: the main theorem (an SLP of size g for a string of length n can be made into an equivalent SLP of size O(g) and depth O(log n) in linear time); conference version FOCS 2019
  - paper: doi:10.1137/130936889
    title: Philip Bille, Gad M. Landau, Rajeev Raman, Kunihiko Sadakane, Srinivasa Rao Satti and Oren Weimann, Random access to grammar-compressed strings and trees, SIAM Journal on Computing 44(3), 2015
    locator: the main theorem (random access in O(log n) time with a structure of size O(g) on the word RAM); conference version SODA 2011
  - paper: doi:10.1016/S0304-3975(02)00777-6
    title: Wojciech Rytter, Application of Lempel-Ziv factorization to the approximation of grammar-based compression, Theoretical Computer Science 302(1-3), 2003
    locator: the AVL grammars and the conversion of an LZ77 factorization with k factors into a grammar of size O(k log n)
---

A straight-line program (SLP) is a [context-free grammar](/context-free-grammar/) in which each nonterminal has exactly one rule and no nonterminal can derive itself, so the grammar derives exactly one string. SLPs are the standard model of [grammar-based compression](/grammar-based-compression/): a string of length $n$ with many repeats has an SLP of size much smaller than $n$, sometimes $O(\log n)$. Many operations, such as finding the length, reading one symbol, and [pattern matching](/pattern-matching-in-compressed-text/), run on the SLP without expanding it. The name is shared with the [arithmetic straight-line program](/straight-line-program/) of computer algebra, which is a different object (see below).

## Definition

Fix a finite alphabet $\Sigma$ of size $\sigma$. A **straight-line program** is a tuple $G = (V, \Sigma, R, S)$ where $V = \{X_1, \ldots, X_m\}$ is a set of nonterminals disjoint from $\Sigma$, $S = X_m$ is the start symbol, and $R$ has exactly one rule $X_i \to \alpha_i$ for each $i$, with

$$\alpha_i \in (\Sigma \cup \{X_1, \ldots, X_{i-1}\})^{+}.$$

So the right-hand side of $X_i$ uses only terminals and nonterminals with a smaller index. This order makes the rules acyclic. The **value** of a symbol is defined by induction on the index: $\mathrm{val}(a) = a$ for $a \in \Sigma$, and $\mathrm{val}(X_i) = \mathrm{val}(\beta_1) \cdots \mathrm{val}(\beta_k)$ when $\alpha_i = \beta_1 \cdots \beta_k$. The SLP **derives** the string $\mathrm{val}(G) = \mathrm{val}(S)$, and its language is $\{\mathrm{val}(G)\}$.

An SLP is in **Chomsky normal form** (CNF) if each rule has one of two forms: $X_i \to a$ with $a \in \Sigma$, or $X_i \to X_j X_k$ with $j, k < i$. This matches the [Chomsky normal form](/chomsky-normal-form/) of general grammars, without the empty string. Many papers on algorithms use only CNF SLPs.

Two size measures are in use, and a statement about "the size" must say which:

- **Total length**, $|G| = \sum_{i=1}^{m} |\alpha_i|$. This is the measure of the [smallest grammar problem](/smallest-grammar-problem/) in Charikar et al. (2005).
- **Number of rules**, $m$. This is the usual measure for CNF SLPs, as in Lohrey's survey.

For a CNF SLP with $t$ terminal rules and $m - t$ binary rules, $|G| = t + 2(m - t)$, so $m \le |G| \le 2m$. A general SLP of total length $g$ becomes a CNF SLP with at most $g + \sigma$ rules: a rule of length $k \ge 2$ becomes $k - 1$ binary rules, a rule of length 1 is removed by substitution, and each terminal gets one rule $X_a \to a$. So the two measures agree up to a constant factor whenever each letter of $\Sigma$ occurs in the string.

The **height** $h$ of a CNF SLP is the largest number of binary rules on a path from $S$ to a terminal rule in the derivation tree. The derivation tree has $n = |\mathrm{val}(G)|$ leaves, and each binary rule at most doubles the length, so $n \le 2^h$ and $h \ge \lceil \lg n \rceil$. In the same way, an SLP with $m$ rules in CNF derives a string of length at most $2^{m-1}$, so each SLP for a string of length $n$ has at least $\lg n + 1$ rules.

**Two basic computations.** Both run on the SLP and take time polynomial in its size, not in $n$.

- *Length.* Compute $\ell(X_i) = |\mathrm{val}(X_i)|$ for $i = 1, \ldots, m$: $\ell(X_i) = 1$ for $X_i \to a$, and $\ell(X_i) = \ell(X_j) + \ell(X_k)$ for $X_i \to X_j X_k$. This takes $m$ additions. The numbers have up to $m$ binary digits, because $n \le 2^{m-1}$. On the [word RAM](/word-ram/) with words of $\Theta(\log n)$ binary digits, each addition takes $O(1)$ time.
- *Random access.* To read the symbol at position $p$ (from 0), start at $S$. At a rule $X \to Y Z$, go to $Y$ if $p < \ell(Y)$; else set $p \leftarrow p - \ell(Y)$ and go to $Z$. At a terminal rule $X \to a$, return $a$. This visits one rule on each level, so it takes $O(h)$ time after the lengths are known.

The time $O(h)$ can be as bad as $\Theta(m)$, because an SLP can be a long chain. Two results remove this cost. Bille et al. (2015) give a structure of size $O(m)$ that answers random access in $O(\log n)$ time on any SLP. Ganardi, Jeż and Lohrey (2021) show that each SLP of size $g$ for a string of length $n$ can be changed, in linear time, into an SLP for the same string of size $O(g)$ and height $O(\log n)$. After this balancing, the walk above takes $O(\log n)$ time.

## Examples and non-examples

**Fibonacci words.** The SLP with the rules $X_1 \to b$, $X_2 \to a$, $X_i \to X_{i-1} X_{i-2}$ for $3 \le i \le m$ derives the [Fibonacci word](/fibonacci-word/) $f_m$. With $m = 6$:

| rule | value | length |
|---|---|---|
| $X_1 \to b$ | b | 1 |
| $X_2 \to a$ | a | 1 |
| $X_3 \to X_2 X_1$ | ab | 2 |
| $X_4 \to X_3 X_2$ | aba | 3 |
| $X_5 \to X_4 X_3$ | abaab | 5 |
| $X_6 \to X_5 X_4$ | abaababa | 8 |

It has 6 rules and total length 10, for a string of length 8. With $m$ rules the length is the Fibonacci number $F_m$, which grows like $1.618^m$, so the SLP has size $O(\log n)$. To read position $p = 5$ of abaababa: at $X_6$, $5 \ge \ell(X_5) = 5$, so go to $X_4$ with $p = 0$. At $X_4$, $0 < \ell(X_3) = 2$, so go to $X_3$. At $X_3$, $0 < \ell(X_2) = 1$, so go to $X_2$, which gives a. Position 5 of abaababa is a.

**Powers of a letter.** The rules $X_1 \to a$ and $X_{i} \to X_{i-1} X_{i-1}$ for $2 \le i \le m$ derive $a^{2^{m-1}}$. This shows that the bound $n \le 2^{m-1}$ is tight.

**A non-CNF SLP.** Charikar et al. open their paper with the string "a rose is a rose is a rose", 26 characters including the spaces. Their SLP is $S \to B B A$, $A \to$ "a rose", $B \to A$ " is ", where each character and each space is one terminal. Its total length is $3 + 6 + 5 = 14$, and they state that no grammar for this string is smaller. In CNF the same string needs more rules, because each rule of length $k$ becomes $k - 1$ binary rules.

**Non-examples.**

- $S \to a S \mid b$ has two rules for $S$, and $S$ derives itself. It generates the infinite language $a^{*} b$, not one string.
- $S \to A b$, $A \to S a$ has one rule for each nonterminal, but the rules have a cycle. No string is derived, because the derivation never ends.
- $S \to ab \mid ba$ generates a finite language, but $S$ has two rules, so the grammar is not an SLP. An SLP never has a choice during a derivation.
- $S \to A$, $A \to \varepsilon$ is not an SLP in the sense above, because right-hand sides must not be empty. With this rule every SLP derives a non-empty string, and the empty string needs a special case.

## Related definitions

- **Arithmetic straight-line program.** In [computer algebra](/straight-line-program/), a straight-line program is a sequence of instructions $x_i \leftarrow x_j \circ x_k$ with $\circ \in \{+, -, \times\}$, and it computes a polynomial or a number. A string SLP is the same shape over the free monoid: the only operation is concatenation. The two pages share a name and the alias SLP, but the questions are different. On strings, the size relates to compression; on polynomials, the length relates to the cost of evaluation.
- **Grammar compression.** [Grammar-based compression](/grammar-based-compression/) stores an SLP in place of the string. The [smallest grammar problem](/smallest-grammar-problem/) asks for the SLP of minimum total length.
- **Collage systems and run-length SLPs.** Some papers add rules $X \to Y^k$ (run-length SLPs) or truncation rules. These describe some strings more compactly. They are not SLPs in the sense above.
- **LZ77.** A [Lempel-Ziv factorization](/lempel-ziv-factorization/) without self-reference, of $z$ factors, is never larger than the smallest grammar, and Rytter (2003) turns it into an SLP of size $O(z \log n)$. So the two measures are within a factor of $O(\log n)$.
- **Compressed indexes.** SLPs are the base of several [compressed indexes](/compressed-indexing/) for repetitive text, and of measures of repetitiveness such as the [string attractor](/string-attractor/).

## References
