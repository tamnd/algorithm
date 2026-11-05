---
tag: FCD9T8
kind: concept
slug: star-free-expressions
name: Star-free expressions
aliases:
- star-free regular expressions
- star-free languages
area: automata-and-parsing/regular-expressions
level: advanced
summary: Regular expressions without the star operator, equal in power to aperiodic automata by Schützenberger's theorem.
prereqs: [regular-expression, star-free-language, syntactic-monoid]
see_also: [schutzenberger-theorem, star-free-language, syntactic-monoid, extended-regular-expressions, star-height-problem, linear-temporal-logic, krohn-rhodes-theorem, regex-derivative]
sources:
  - paper: doi:10.1016/S0019-9958(65)90108-7
    title: Marcel-Paul Schützenberger, On finite monoids having only trivial subgroups, Information and Control 8(2) (1965)
    locator: pp. 190 to 194 (a regular language is star-free if and only if its syntactic monoid is aperiodic)
  - book: "Robert McNaughton and Seymour Papert, Counter-Free Automata, MIT Press, 1971"
    locator: the chapters on star-free sets, counter-free automata and first-order definable sets
  - book: "Larry J. Stockmeyer, The complexity of decision problems in automata theory and logic, PhD thesis, MIT, 1974 (Project MAC Technical Report 133)"
    locator: the chapter on star-free expressions with complement (their equivalence problem is not elementary recursive)
  - paper: doi:10.1016/S0022-0000(71)80003-X
    title: Rina S. Cohen and Janusz A. Brzozowski, Dot-depth of star-free events, Journal of Computer and System Sciences 5(1) (1971)
    locator: pp. 1 to 16 (the dot-depth of a star-free expression)
  - paper: doi:10.1016/0022-0000(78)90049-1
    title: Janusz A. Brzozowski and Robert Knast, The dot-depth hierarchy of star-free languages is infinite, Journal of Computer and System Sciences 16(1) (1978)
    locator: pp. 37 to 55
  - paper: doi:10.1016/0304-3975(91)90075-D
    title: Sang Cho and Dung T. Huynh, Finite-automaton aperiodicity is PSPACE-complete, Theoretical Computer Science 88(1) (1991)
    locator: pp. 99 to 116
  - book: "Volker Diekert and Paul Gastin, First-order definable languages, in Logic and Automata: History and Perspectives, Texts in Logic and Games 2, Amsterdam University Press, 2008"
    locator: pp. 261 to 306 (a survey of the equivalence of star-free expressions, aperiodic monoids, first-order logic and temporal logic)
---

A star-free expression is a regular expression that may use complement, and intersection, but not the star. Without the star, complement does the work of describing infinite languages: $\neg \emptyset$ is the set of all strings, and $(ab)^*$ turns out to have a star-free expression, while $(aa)^*$ does not. The languages described, the [star-free languages](/star-free-language/), are exactly those whose [syntactic monoid](/syntactic-monoid/) has no non-trivial group, by [Schützenberger's theorem](/schutzenberger-theorem/), and also exactly those that first-order logic and [linear temporal logic](/linear-temporal-logic/) can define on strings. The price of complement is succinctness that no algorithm can afford: deciding whether two star-free expressions are equivalent is not elementary.

## In plain words

An ordinary pattern uses "or", "followed by" and "repeat any number of times". A star-free pattern gives up "repeat", and gets "not" in exchange: it can describe every string that does not fit some other pattern.

"Not" turns out to replace much of what repetition did. "Anything at all" is "not nothing". "Strings with no two equal letters in a row" is "not anything, then a double letter, then anything". Many repeating patterns can be rebuilt this way.

What "not" cannot rebuild is counting modulo a number. "An even number of letters" has no star-free pattern, because a star-free pattern cannot tell a very long run of a letter from a run that is one letter longer. This is the whole difference: a regular language has a star-free pattern exactly when it never needs to count around a cycle.

## The idea

The core syntax of the [regular expression](/regular-expression/) page has union $\mid$, concatenation, star $^*$, $\varepsilon$ and $\emptyset$. Star-free expressions drop the star and add complement $\neg r$, which denotes $\Sigma^* \setminus L(r)$, and intersection $r \mathbin{\&} s$, which is $\neg(\neg r \mid \neg s)$ and so adds no power. They are the star-free fragment of regular expressions with Boolean operators, which automata theory also calls [extended regular expressions](/extended-regular-expressions/). Practical engines do not have a complement operator; their [lookahead](/regex-lookaround/) assertions give some of its effect, and features such as backreferences go beyond regular languages altogether.

**Complement is essential.** With only $\emptyset$, $\varepsilon$, symbols, union, concatenation and intersection, every expression denotes a finite language, by induction on the expression. Complement is what makes infinite languages reachable. The basic building blocks are:

- $\Sigma^* = \neg \emptyset$, written $\Sigma^*$ below as a shorthand, not as a star;
- $\Sigma^* w \Sigma^*$, the strings that contain $w$, and $\neg(\Sigma^* w \Sigma^*)$, those that avoid it;
- $w \Sigma^*$ and $\Sigma^* w$, the strings that start or end with $w$;
- $B^*$ for a set of letters $B$, the intersection of $\neg(\Sigma^* c \Sigma^*)$ over the letters $c \notin B$;
- $\{\varepsilon\} = \neg \big( \bigcup_{a \in \Sigma} a \Sigma^* \big)$, so $\varepsilon$ need not be a primitive.

**The alphabet matters.** Complement is taken in $\Sigma^*$, so the same expression can denote different languages over different alphabets: $\neg \emptyset$ is $\{a, b\}^*$ over $\{a, b\}$ and $\{a, b, c\}^*$ over $\{a, b, c\}$. Whether a language is star-free does not depend on the alphabet, but its expressions do.

**What star-free expressions cannot say.** Every star-free language $L$ has a number $k$ such that for all strings $x, u, y$ and all $n \ge k$,
$$x u^n y \in L \iff x u^{n + 1} y \in L.$$
The proof is an induction on the expression. For $\emptyset$, $k = 0$ works; for $\varepsilon$ and a symbol, $k = 2$, since $x u^n y$ is then too long to be in the language for $n \ge 2$ and $u \ne \varepsilon$. Complement keeps the same $k$, and union takes the larger of the two. For a concatenation $L_1 L_2$ with numbers $k_1$ and $k_2$, take $k = k_1 + k_2 + 1$: if $x u^n y = st$ with $s \in L_1$ and $t \in L_2$, the cut between $s$ and $t$ leaves at least $k_1$ whole copies of $u$ in $s$ or at least $k_2$ in $t$, and on that side one copy can be added or removed without leaving $L_1$ or $L_2$. So the property says that a star-free language cannot count beyond a fixed threshold. The language $(aa)^*$ fails it with $x = y = \varepsilon$ and $u = a$, since $a^n$ and $a^{n + 1}$ always differ in parity.

**Schützenberger's theorem.** The property above says that the [syntactic monoid](/syntactic-monoid/) of $L$ is *aperiodic*: every element $m$ satisfies $m^k = m^{k + 1}$, which is the same as having no non-trivial group inside. Schützenberger (1965) proved the converse: every regular language with an aperiodic syntactic monoid has a star-free expression, and his proof constructs it. For a DFA the test reads: the minimal DFA is *counter-free*, meaning that no string $u$ moves a cycle of two or more different states around. Deciding this from a DFA is PSPACE-complete (Cho and Huynh, 1991).

**Logic.** McNaughton and Papert (1971) showed that the star-free languages are exactly the languages defined by sentences of first-order logic over the positions of a string, with the order $<$ and a predicate for each letter. A concatenation $L_1 L_2$ becomes "there is a position where the string splits into a part in $L_1$ and a part in $L_2$", and complement becomes negation. By Kamp's theorem (1968), first-order logic on strings has the same power as [linear temporal logic](/linear-temporal-logic/), so star-free expressions, aperiodic monoids, counter-free automata, first-order logic and LTL all describe one class. Diekert and Gastin (2008) survey the proofs.

**Size and complexity.** A star-free expression of size $m$ is matched against a string of length $n$ in polynomial time, by computing for every subexpression the set of substrings it matches. Translating it into an automaton is far more expensive. Each complement needs a DFA, and each concatenation of complements makes a nondeterministic choice that the next complement must determinize again, so the number of states can grow by one exponential per level of nesting. Stockmeyer (1974) showed that this cannot be avoided: emptiness and equivalence of star-free expressions with complement are decidable but not elementary, that is, no algorithm runs within a tower of exponentials of fixed height. With only union and concatenation, the languages are finite and equivalence is coNP-complete ([regex equivalence](/regex-equivalence/)).

**Dot-depth.** Cohen and Brzozowski (1971) measured a star-free expression by its *dot-depth*, the number of alternations between concatenation and Boolean operations. Brzozowski and Knast (1978) proved that the levels form an infinite hierarchy. Deciding the dot-depth of a given star-free language is an old open problem, solved only for the lowest levels.

**Star height.** The star height of an expression is the nesting depth of its stars. With complement allowed, the star-free languages are those of generalized star height 0. No regular language is known to need generalized star height 2 or more, and whether one exists is open ([star height problem](/star-height-problem/)).

## Examples

All expressions below are over $\Sigma = \{a, b\}$ unless stated otherwise. A script built the minimal DFA of each one by product and subset constructions, compared its language with the given regular expression on all strings of length at most 10, and checked that its transition monoid is aperiodic. It did the same for 3000 random star-free expressions over two and three letters, including $\emptyset$, $\varepsilon$ and nested complements, comparing each DFA with the language computed directly from the definition.

| star-free expression | ordinary expression | minimal DFA states |
|---|---|---|
| $\neg(a \Sigma^* \mid b \Sigma^*)$ | $\varepsilon$ | 2 |
| $\Sigma^* abb$ | $(a \mid b)^* abb$ | 4 |
| $\neg(\Sigma^* ab \Sigma^*)$ | $b^* a^*$ | 3 |
| $\neg(b \Sigma^* \mid \Sigma^* a \mid \Sigma^* aa \Sigma^* \mid \Sigma^* bb \Sigma^*)$ | $(ab)^*$ | 3 |
| $\neg(\Sigma^* a\, \neg(\Sigma^* b \Sigma^*))$ | $\varepsilon \mid (a \mid b)^* b$ | 2 |

- **$(ab)^*$.** A string is in $(ab)^*$ if and only if it does not start with $b$, does not end with $a$, and contains neither $aa$ nor $bb$: a non-empty string with these properties alternates its letters, starts with $a$ and ends with $b$. Over $\{a, b, c\}$ the same expression also admits strings with $c$, such as $c$ itself, and one must intersect with $\neg(\Sigma^* c \Sigma^*)$; the script confirmed both facts on strings of length at most 7.
- **Nested complement.** The last row says "no $a$ is followed only by letters other than $b$", that is, every $a$ is eventually followed by a $b$. It is the temporal formula $\mathbf{G}(a \to \mathbf{F} b)$ written as an expression, and the inner complement is the "eventually" part.
- **C comments.** Over the characters `/`, `*` and others, a C comment is `/*`, then a string that does not contain `*/`, then `*/`:
  $$\texttt{/*}\ \neg(\Sigma^*\, \texttt{*/}\, \Sigma^*)\ \texttt{*/}.$$
  The usual expression without complement, in practical syntax, is `/\*([^*]|\*+[^*/])*\*+/`. A script checked that the two agree on all strings of length at most 9 over the three characters `/`, `*` and `x`. Lexer generators that support complement, such as those built on [derivatives](/regex-derivative/), can accept the first form.
- **Non-example: $(aa)^*$.** The parity of a run of $a$s is a cycle of length 2 in the DFA, which the letter $a$ moves around, so the monoid contains the group of order 2. The same holds for $b^* (a b^* a b^*)^*$, an even number of $a$s, and for $(a \mid bb)^*$, where every maximal run of $b$s has even length.
- **A star does not mean "not star-free".** $(ab)^*$ and $(a \mid b)^* abb$ use a star but are star-free; $(aa)^*$ has the same size as $(ab)^*$ and is not. Whether a language is star-free is a property of the language, not of a given expression.

## Where it is used

- **Verification.** Properties of finite traces stated in [linear temporal logic](/linear-temporal-logic/) or first-order logic describe star-free languages, and translations between formulas, star-free expressions and counter-free automata underlie runtime monitors and model checkers for finite traces.
- **Specification and lexing.** Complement states "a string that does not contain $w$" directly, as in the C comment above. Tools based on [derivatives](/regex-derivative/), which handle complement without building an automaton first, support it in lexer specifications.
- **Algebraic classification.** Star-free languages are the first example of a class of regular languages described by a class of finite monoids. Their subclasses, such as the piecewise testable and the locally testable languages, and the dot-depth hierarchy are studied with the same methods, and the [Krohn-Rhodes theorem](/krohn-rhodes-theorem/) relates aperiodic monoids to cascades of reset automata.
- **Circuit complexity.** First-order logic with order can be evaluated by constant-depth circuits of polynomial size, so every star-free language lies in the circuit class AC0. The strings over $\{a, b\}$ with an even number of $a$s, which are not star-free, are not in AC0 (Furst, Saxe and Sipser; Ajtai).
- **Lower bounds.** Star-free expressions with complement are the standard example of a natural decidable problem that is not elementary, and the reductions behind it are reused for the logics above.

## References
