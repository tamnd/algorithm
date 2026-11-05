---
tag: 1G6BSV
kind: problem
slug: backreference-matching
name: Matching with backreferences
aliases:
- regex matching with backreferences
area: automata-and-parsing/regular-expressions
level: advanced
summary: Decide membership for patterns with backreferences, which is NP-complete in general.
prereqs: [backreference, np-complete, 3-sat]
see_also: [backtracking-regex-matching, regex-matching, polynomial-time-reduction, string-constraint-satisfiability, redos, extended-regular-expressions, posix-regex-semantics, cook-levin-theorem]
sources:
  - book: isbn:9780444880710
    title: Alfred V. Aho, Algorithms for finding patterns in strings, in Jan van Leeuwen (ed.), Handbook of Theoretical Computer Science, Volume A, Elsevier and MIT Press (1990)
    locator: Chapter 5, pp. 255 to 300, Section 6 (regular expressions with back referencing, Theorem 6.2, NP-completeness of their membership problem)
  - paper: doi:10.1142/S012905410300214X
    title: Cezar Câmpeanu, Kai Salomaa and Sheng Yu, A formal study of practical regular expressions, International Journal of Foundations of Computer Science 14(6) (2003)
    locator: pp. 1007 to 1018 (the formal semantics of regex with backreferences)
  - paper: "Dana Angluin, Finding patterns common to a set of strings, Journal of Computer and System Sciences 21(1) (1980)"
    title: Dana Angluin, Finding patterns common to a set of strings
    locator: pp. 46 to 62 (pattern languages and the NP-completeness of their membership problem)
  - paper: doi:10.4230/LIPIcs.STACS.2011.507
    title: Dominik D. Freydenberger, Extended regular expressions, succinctness and decidability, STACS 2011, Leibniz International Proceedings in Informatics 9
    locator: pp. 507 to 518 (membership is NP-complete, and polynomial when the number of variables is bounded)
  - url: "https://arxiv.org/abs/1903.05896"
    title: Markus L. Schmid, Regular expressions with backreferences, polynomial-time matching techniques (2019)
    locator: the active variable degree and memory-deterministic regex, two classes with polynomial-time matching
  - url: "https://www.gnu.org/software/grep/manual/grep.html"
    title: GNU grep manual
    locator: Section 5, Performance (a slower matcher for back-references, and the exponential example)
---

Matching with backreferences is the problem of deciding whether a string matches a pattern that may contain [backreferences](/backreference/), such as `(a*)b\1`. Aho (1990) showed that it is [NP-complete](/np-complete/) when the pattern and the string are both part of the input, so no algorithm handles every pattern in polynomial time unless P = NP. For a fixed pattern, or a bounded number of capture groups, it can be solved in polynomial time, and most of the cost in practice comes from engines that use [backtracking](/backtracking-regex-matching/) for every pattern.

## In plain words

A backreference says "here, the same text that an earlier group took". To check a string, an engine must decide what each group takes, and a choice made early can make a later part fail.

With ordinary regular expressions, the engine can follow all choices at once with a small set of states. With backreferences, the remembered text is part of the state, and there can be very many different remembered texts.

There is a simple way to turn any puzzle of true and false variables into such a match: one group per value of each variable, and one part of the pattern per condition. A fast matcher for all patterns would then solve all those puzzles fast, which is believed to be impossible.

## Definition

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Patterns in the syntax of practical engines are in `code font`, where `E?` is $E \mid \varepsilon$.

A *regex with backreferences* is a regular expression with two more forms: a capture group $(r)_k$, and a backreference $\backslash k$ for a group number $k$. Its semantics is the one on the [backreference](/backreference/) page, after Câmpeanu, Salomaa and Yu (2003): a match runs through the pattern from left to right, a group stores the substring it matched, a group inside a star stores the substring of its last iteration, and $\backslash k$ must match exactly the stored substring of group $k$. We fix two details: a backreference to a group that is not set fails, and an iteration of a star must read at least one symbol, as in the [backtracking](/backtracking-regex-matching/) matcher.

**Problem.** Input: a regex with backreferences $p$ and a string $w$. Output: yes if $w \in L(p)$, no otherwise. The size of the input is $|p| + |w|$.

## Variants

- **Fixed pattern.** The pattern is fixed and only $w$ is the input. Every fixed pattern can be matched in polynomial time, since the degree of the polynomial depends only on the number of groups (see Known algorithms).
- **Bounded number of groups.** The pattern is part of the input but has at most $k$ groups, for a constant $k$. Freydenberger (2011) notes that the problem is then polynomial.
- **Pattern languages.** A pattern is a string of letters and variables, such as $x\,a\,x\,y$, where each variable stands for a nonempty string and equal variables stand for equal strings. Angluin (1980) showed that membership in a pattern language is NP-complete. A pattern is a regex in which each variable is a group $(\Sigma\Sigma^*)_k$ at its first use and a backreference $\backslash k$ after it.
- **Search.** Decide whether some substring of $w$ matches. This is matching with the pattern $\Sigma^* p\, \Sigma^*$, and has the same complexity.
- **Engine semantics.** Real engines differ: in JavaScript a reference to an unset group matches the empty string, and some engines allow a group to refer to itself or to a later group. The hardness proof below uses none of these details, so it holds for all of them.

## Examples

**The reduction on one formula.** Take $\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor \lnot x_2 \lor x_3)$. The reduction below gives, in Python syntax, the pattern and the text

```
pattern: (x?)(x?);(x?)(x?);(x?)(x?);\1\3\6x?x?;\2\4\5x?x?;
text:    x;x;x;xxx;xxx;
```

Groups 1 and 2 belong to $x_1$, groups 3 and 4 to $x_2$, and groups 5 and 6 to $x_3$; the odd group of a variable holds `x` when the variable is true. Python's `re.fullmatch` finds a match with the groups `x`, empty, `x`, empty, `x`, empty, which is the assignment with $x_1$, $x_2$ and $x_3$ all true. In the first clause segment, `\1\3\6` reads `xx`, and `x?x?` reads the third `x`. In the second, `\2\4\5` reads `x`, and `x?x?` reads the other two.

**An unsatisfiable formula.** The 8 clauses on $x_1, x_2, x_3$ with all sign patterns have no satisfying assignment. The reduction gives a pattern of 115 characters and a text of 38 characters, and `re.fullmatch` returns no match.

**Agreement on random formulas.** For 600 random 3-CNF formulas with 1 to 5 variables and 1 to 12 clauses, Python's `re.fullmatch` on the reduced pair matched exactly when a search over all assignments found the formula satisfiable.

**Patterns that are easy.** The pattern `(a*)b\1` has one group, so the fixed-pattern algorithm takes polynomial time; here a direct check works in linear time: find the `b`, and compare the two sides. The pattern `((a|b)*)\1` for the squares $ww$ has one group as well.

## Known algorithms

- **Backtracking.** Try the choices of the pattern depth-first, and carry the stored substrings along the current path. This is what Perl, PCRE, Python, Java and JavaScript do. It is exponential in the worst case, even for patterns without backreferences.
- **Guess the groups.** If no group lies under a star, each group is set at most once, and its stored substring is a substring $w_{s+1} \cdots w_e$ of $w$. Try all $O(n^2)$ pairs $(s, e)$ for each of the $k$ groups, with $n = |w|$. For a fixed choice, each backreference becomes a fixed string, and the check that a run exists in which each group spans exactly its chosen positions is an NFA simulation over the pattern with the positions as extra constraints, in time polynomial in $|p|$ and $n$. The total is $n^{2k}$ times a polynomial. Groups under a star need more care, because their last iteration must be chosen too, but the bound stays $n^{O(k)}$ for a fixed number $k$ of groups.
- **Restricted classes.** Schmid (2019) defines a parameter of the pattern, the active variable degree, and shows polynomial-time matching when it is bounded, and a class of memory-deterministic patterns that can be matched in time linear in $|w|$ times a polynomial in $|p|$.
- **Practical engines without backreferences.** RE2, Go and Rust reject backreferences, so that they can match all patterns with automata in time linear in $|w|$.

## Bounds

**Theorem.** Matching with backreferences is NP-complete. It stays NP-hard for patterns without a star and with only the letters `x` and `;`.

**In NP.** A certificate is a run of the pattern: the sequence of choices for each union and the number of iterations of each star. Each iteration of a star reads at least one symbol, so there are at most $|w|$ iterations for each entry into a star, and the run has size polynomial in $|p| + |w|$. Checking the run, with the stored substrings, takes polynomial time.

**NP-hard, by a reduction from [3-SAT](/3-sat/).** Let $\varphi$ have variables $x_1, \ldots, x_n$ and clauses $C_1, \ldots, C_m$, each with three literals. Give $x_i$ the groups $T_i = 2i - 1$ and $F_i = 2i$, and let the group of a literal be $T_i$ for $x_i$ and $F_i$ for $\lnot x_i$. Build

$$p = \prod_{i=1}^{n} \big((x?)_{T_i} (x?)_{F_i}\, ;\big) \prod_{j=1}^{m} \big(\backslash g_{j1}\, \backslash g_{j2}\, \backslash g_{j3}\; x?\, x?\, ;\big), \qquad w = (x;)^n (xxx;)^m,$$

where $g_{j1}, g_{j2}, g_{j3}$ are the groups of the literals of $C_j$. Both have size $O(n + m)$.

*Alignment.* Each segment of $p$ ends with `;` and has no other `;`, and $w$ has exactly $n + m$ symbols `;`, so in any match the $t$-th segment of $p$ matches the $t$-th segment of $w$.

*Variables.* The segment of $x_i$ matches `x;` exactly when one of $T_i$, $F_i$ stores `x` and the other stores the empty string. Read this as $x_i$ true when $T_i$ stores `x`. Every assignment arises from exactly one way to match the variable segments.

*Clauses.* Each backreference in the segment of $C_j$ reads `x` if its literal is true and nothing if it is false, so the three read $t_j \in \{0, 1, 2, 3\}$ symbols, where $t_j$ is the number of true literals of $C_j$. Then `x?x?` reads between 0 and 2 more, and the segment matches `xxx;` if and only if $t_j \ge 1$.

So $w \in L(p)$ if and only if some assignment makes every clause true, that is, if and only if $\varphi$ is satisfiable. The pattern has no star and uses only `x` and `;`. $\blacksquare$

**Fine-grained consequence.** The reduction is linear in size. With the sparsification lemma of Impagliazzo, Paturi and Zane, which allows $m = O(n)$, the Exponential Time Hypothesis implies that no algorithm decides the problem in time $2^{o(|p| + |w|)}$.

**Upper bound.** Backtracking, or trying all certificates, takes $2^{O(|p| \cdot |w| \log |w|)}$ time at most, since a certificate has polynomial size.

## Reductions

- **From 3-SAT,** as above, and so from every problem in NP by the [Cook-Levin theorem](/cook-levin-theorem/).
- **From pattern-language membership.** A pattern with variables is a regex with backreferences, so Angluin's NP-hardness for patterns carries over.
- **To SAT.** Being in NP, the problem reduces to SAT; a solver can then decide hard instances that backtracking cannot.
- **Related string problems.** Word equations and [string constraint satisfiability](/string-constraint-satisfiability/) also ask for strings that repeat the same unknown text, and they have backreference-like constraints.

## Applications

- **Engine design.** The NP-completeness is the reason RE2, Go and Rust leave out backreferences, and the reason engines that keep them cannot promise polynomial time ([ReDoS](/redos/)).
- **POSIX tools.** POSIX basic regular expressions, used by `grep` and `sed`, have backreferences `\1` to `\9`; the bound of 9 groups keeps each fixed pattern polynomial in principle. The GNU grep manual says that patterns with back-references go to a slower matcher, and that `^(.*)\1{14}(.*)\2{13}$` takes exponential time.
- **Text processing.** Typical uses are finding doubled words, as with `\b(\w+) \1\b`, or matching tags with the same name, as with `<(\w+)>.*?</\1>`.

## References
