---
tag: 4RKREQ
kind: definition
slug: kleene-star
name: Kleene star
aliases:
- Kleene closure
- star operator
area: automata-and-parsing/regular-expressions
level: intro
summary: The operator L* giving all finite concatenations of strings from L, including the empty string.
prereqs: [alphabet, monoid]
see_also: [regular-expression, regular-language, arden-lemma, kleene-algebra, kleene-theorem, thompson-construction, closure-properties-of-regular-languages, star-height-problem]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.1.1, The Operators of Regular Expressions (the closure of a language), and Section 3.4, Algebraic Laws for Regular Expressions
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.1, Definition 1.23 (the regular operations union, concatenation and star)
  - paper: "Stephen C. Kleene, Representation of events in nerve nets and finite automata, in Claude E. Shannon and John McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press (1956)"
    title: Stephen C. Kleene, Representation of events in nerve nets and finite automata
    locator: pp. 3 to 41 (the iterate operation on events, later written with a star)
---

The Kleene star of a set of strings $L$, written $L^*$, is the set of all strings that you get by concatenating zero or more strings of $L$, so it always contains the empty string $\varepsilon$. It is one of the three operators of [regular expressions](/regular-expression/), with union and concatenation, and it is the only one that makes a finite language infinite. The [regular languages](/regular-language/) are closed under the star, and the star is the operation behind the loops of finite automata.

## Definition

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. So $ab^*$ means $a(b^*)$, and $a \mid b^*$ means $a \mid (b^*)$.

Let $\Sigma$ be an [alphabet](/alphabet/) and let $L \subseteq \Sigma^*$ be a language. The concatenation of two languages is $LM = \{uv : u \in L, v \in M\}$. The powers of $L$ are

$$L^0 = \{\varepsilon\}, \qquad L^{n+1} = L^n L \quad (n \ge 0).$$

The **Kleene star** (or Kleene closure) of $L$ is

$$L^* = \bigcup_{n \ge 0} L^n = \{w_1 w_2 \cdots w_n : n \ge 0,\ w_1, \ldots, w_n \in L\}.$$

The case $n = 0$ is the empty concatenation, which is $\varepsilon$. So $\varepsilon \in L^*$ for every $L$, even for $L = \emptyset$.

The **positive closure** is $L^+ = \bigcup_{n \ge 1} L^n = L L^*$. In practical syntax it is the operator `+` ([extended regular expressions](/extended-regular-expressions/)).

**In regular expressions.** For a regular expression $r$, the expression $r^*$ denotes $L(r^*) = L(r)^*$.

**As a monoid.** The set $\Sigma^*$ of all strings, with concatenation and $\varepsilon$, is a [monoid](/monoid/): the free monoid on $\Sigma$. The set $L^*$ is the smallest submonoid of $\Sigma^*$ that contains $L$. It contains $\varepsilon$ and $L$, it is closed under concatenation, and every submonoid that contains $L$ contains all products of strings of $L$. This is why $\Sigma^*$, the set of all strings over $\Sigma$, uses the same symbol: it is the star of the language $\Sigma$ of one-letter strings.

**Laws.** For all languages $L$ and $M$ (HMU, Section 3.4):

- $\emptyset^* = \{\varepsilon\}$ and $\{\varepsilon\}^* = \{\varepsilon\}$;
- $(L^*)^* = L^*$ and $L^* L^* = L^*$;
- $L^* = \{\varepsilon\} \cup L L^* = \{\varepsilon\} \cup L^* L$;
- $L^* = (L \setminus \{\varepsilon\})^*$, so the empty string in $L$ does not change $L^*$;
- $L^+ = L^*$ if and only if $\varepsilon \in L$;
- $L^*$ is infinite if and only if $L$ contains a nonempty string;
- $(L \cup M)^* = (L^* M^*)^*$ and $(LM)^* L = L (ML)^*$.

**Least solution of an equation.** The language $X = L^* M$ is the smallest language with $X = LX \cup M$, and it is the only solution when $\varepsilon \notin L$. This is [Arden's lemma](/arden-lemma/). In particular, $L^*$ is the smallest $X$ with $\{\varepsilon\} \cup LX \subseteq X$, which is the form of the star axiom of [Kleene algebra](/kleene-algebra/).

**History.** Kleene (1956) defined the operation, as the iterate of an event, in the paper that proved the equivalence of regular expressions and finite automata ([Kleene's theorem](/kleene-theorem/)).

## Examples and non-examples

**Basic cases.** Over $\Sigma = \{a, b\}$:

| language $L$ | $L^*$ |
|---|---|
| $\emptyset$ | $\{\varepsilon\}$ |
| $\{\varepsilon\}$ | $\{\varepsilon\}$ |
| $\{a\}$ | $\{\varepsilon, a, aa, aaa, \ldots\}$, the strings $a^n$ with $n \ge 0$ |
| $\{a, b\}$ | all strings over $\{a, b\}$ |
| $\{ab\}$ | $\{\varepsilon, ab, abab, \ldots\}$ |
| $\{aa, aaa\}$ | all $a^n$ with $n \ne 1$ |

In the last row, every $n \ge 2$ is a sum of 2s and 3s, but $1$ is not.

**Counting.** The strings of $\{a, bb\}^*$ of length $n$ are $1, 1, 2, 3, 5, 8, 13, 21$ for $n = 0, 1, \ldots, 7$, the Fibonacci numbers. A string of length $n \ge 2$ in this language ends with $a$ (after a string of length $n - 1$) or with $bb$ (after a string of length $n - 2$), and each string has only one factorization into $a$ and $bb$.

**Factorizations need not be unique.** With $L = \{a, ab, ba\}$, the string $aba$ is in $L^*$ in two ways: $a \cdot ba$ and $ab \cdot a$. A language in which every string of $L^*$ has exactly one factorization is a [variable-length code](/variable-length-code/), and every [prefix code](/prefix-code/) is one. $\{a, bb\}$ is a code; $\{a, ab, ba\}$ is not.

**Membership.** A string $w = w_1 \cdots w_n$ is in $L^*$ if and only if there are positions $0 = i_0 < i_1 < \cdots < i_k = n$ such that each piece $w_{i_{j-1}+1} \cdots w_{i_j}$ is in $L$. A table $t[0..n]$ with $t[0]$ true and $t[i]$ true if and only if $t[j]$ is true and $w_{j+1} \cdots w_i \in L$ for some $j < i$ decides this. For $L = \{a, ab, ba\}$ and $w = abba$, the table is true, true, true, false, true: $ab$ is in $L$, $abb$ is not in $L^*$, and $abba = ab \cdot ba$ is.

**Star of a regular expression.** $(a \mid b)^* a$ denotes the strings that end with $a$. $(ab \mid b)^*$ denotes the strings over $\{a, b\}$ in which each $a$ is followed at once by $b$; its strings of length at most 3 are $\varepsilon$, $b$, $ab$, $bb$, $abb$, $bab$ and $bbb$.

**Non-examples.**

- $\{a^n b^n : n \ge 0\}$ is not the star of any language. If it were $L^*$, then $L$ would contain $ab$ (the shortest nonempty string of the set must be in $L$), so $abab$ would be in $L^*$, but $abab$ is not of the form $a^n b^n$.
- $L^*$ is not "the strings of $L$ repeated": $\{a, b\}^*$ contains $ab$, which is not a repetition of a single string of $\{a, b\}$. The set of repetitions $\{w^n : w \in L, n \ge 0\}$ is a different language.
- The star is not the same as the set of strings over the letters of $L$. With $L = \{ab\}$, the string $ba$ uses only letters of $L$ but is not in $L^*$.

## Related definitions

- **[Regular expression](/regular-expression/).** The syntax built from $\emptyset$, $\varepsilon$, letters, union, concatenation and the star.
- **[Regular language](/regular-language/).** The languages that regular expressions denote. The class is closed under the star ([closure properties](/closure-properties-of-regular-languages/)): from an automaton for $L$, the [Thompson construction](/thompson-construction/) builds one for $L^*$ with a loop and an $\varepsilon$-move.
- **[Kleene algebra](/kleene-algebra/).** The algebraic structure that axiomatizes union, concatenation and the star.
- **[Arden's lemma](/arden-lemma/).** The equation $X = LX \cup M$ and its least solution $L^* M$.
- **[Star height](/star-height-problem/).** The largest nesting depth of stars that an expression for a language needs.
- **[Extended regular expressions](/extended-regular-expressions/).** Practical syntax, where `E*` is the star, `E+` the positive closure and `E{m,}` is $E^m E^*$.
- **[Greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/).** In regex engines, the star is also a choice that the engine makes in a fixed order; this changes the reported match but not the language.

## References
