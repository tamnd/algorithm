---
tag: XAA52M
kind: algorithm
slug: brzozowski-derivatives
name: Derivative-based regex matching
aliases:
- Brzozowski derivative matching
- derivative matcher
area: automata-and-parsing/regular-expressions
level: advanced
summary: Matches a string by taking successive derivatives of the regex and checking nullability at the end.
solves: [regex-matching]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, n: the length of the input string, d: the largest number of nodes of a normalized derivative of the expression by a prefix of the input}
  time: {expected: O(m + n d)}
  space: {extra: O(m + n d)}
properties: {deterministic: true, recursive: false}
history:
  year: 1964
  people: [Janusz A. Brzozowski]
  note: Brzozowski defined the derivative of a regular expression, used it to build deterministic automata, and proved that an expression has only finitely many derivatives up to the rules for union.
prereqs: [regular-expression, regex-derivative]
see_also: [brzozowski-finiteness-theorem, antimirov-derivatives, lazy-dfa-construction, subset-construction, dfa-minimization, hash-consing, parsing-with-derivatives, glushkov-automaton]
sources:
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494 (the derivative rules, the nullability test, and the finiteness of the set of dissimilar derivatives)
  - paper: doi:10.1017/S0956796808007090
    title: Scott Owens, John Reppy and Aaron Turon, Regular-expression derivatives re-examined, Journal of Functional Programming 19(2) (2009)
    locator: pp. 173 to 190 (derivatives for scanner generators, with intersection and complement, and machines smaller than those of the McNaughton and Yamada method)
  - paper: doi:10.1016/0304-3975(95)00182-4
    title: Valentin Antimirov, Partial derivatives of regular expressions and finite automaton constructions, Theoretical Computer Science 155(2) (1996)
    locator: pp. 291 to 319 (partial derivatives, which split a derivative into a set of terms)
  - paper: doi:10.1145/2034773.2034801
    title: Matthew Might, David Darais and Daniel Spiewak, Parsing with derivatives, a functional pearl, ICFP 2011
    locator: pp. 189 to 195 (the derivative extended from regular expressions to context-free grammars)
  - paper: doi:10.1145/3591262
    title: Dan Moseley, Mario Nishio, Jose Perez Rodriguez, Olli Saarikivi, Stephen Toub, Margus Veanes, Tiki Wan and Eric Xu, Derivative based nonbacktracking real-world regex matching with backtracking semantics, Proceedings of the ACM on Programming Languages 7(PLDI) (2023)
    locator: pp. 1026 to 1049 (the derivative-based regex backend of .NET 7, with anchors and counting)
---

Derivative-based matching decides whether a string $w$ is in the language of a [regular expression](/regular-expression/) $r$ by rewriting $r$ once per symbol. The [derivative](/regex-derivative/) of $r$ by a symbol $a$ is an expression for the words $v$ such that $av$ is in $L(r)$, so after reading all of $w$ the expression left over contains the empty string exactly when $w$ matches. Brzozowski (1964) gave the rules and showed that, up to simple rules for union, an expression has only finitely many derivatives, so the same rules also build a [DFA](/deterministic-finite-automaton/) whose states are expressions.

## In plain words

Think of the pattern as a description of what may still come. Reading a letter changes the description: if the pattern was "a, then any number of b's", after reading an a the rest must be "any number of b's", and after reading a c nothing can match any more.

The matcher keeps one description, updates it for each letter of the input, and stops early if the description says that nothing can match. At the end, it asks one question: does the description allow the input to stop here?

The update rules are short. The catch is that descriptions can grow, so the matcher removes obvious waste after each step, such as a choice between a thing and the same thing again. With that cleanup, a pattern has only a limited number of different descriptions, and they can be stored as the states of an automaton.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is a regular expression $r$ with $m$ nodes over an alphabet $\Sigma$, and a string $w = a_1 \cdots a_n$. The output is whether $w \in L(r)$. This is [regex matching](/regex-matching/).

**Derivatives.** For a language $L$ and a symbol $a$, the *left quotient* is $a^{-1}L = \{v : av \in L\}$. For a word $u$, $u^{-1}L = \{v : uv \in L\}$, so $(ua)^{-1}L = a^{-1}(u^{-1}L)$ and $w \in L$ if and only if $\varepsilon \in w^{-1}L$. The derivative $\partial_a r$ is an expression with $L(\partial_a r) = a^{-1}L(r)$, computed by structural rules (lines L5 to L9 below). The test $\nu(r)$, true if and only if $\varepsilon \in L(r)$, is: false for $\emptyset$ and for a symbol, true for $\varepsilon$ and for a star, $\nu(s) \lor \nu(t)$ for $s \mid t$, and $\nu(s) \land \nu(t)$ for $st$.

## The algorithm

```pseudo id=main
DERIV-MATCH(r, w)                  ▷ r normalized, w = a1 ... an
L1  for i ← 1 to n do
L2      r ← D(r, ai)
L3      if r = ∅ then return false
L4  return NULLABLE(r)

D(r, a)                            ▷ memoized on the pair (r, a)
L5  if r = ∅ or r = ε then return ∅
L6  if r is a symbol b then return ε if b = a, else ∅
L7  if r = s1 | ... | sj then return ALT(D(s1, a), ..., D(sj, a))
L8  if r = s t then return CAT(D(s, a), t) if not NULLABLE(s), else ALT(CAT(D(s, a), t), D(t, a))
L9  if r = s* then return CAT(D(s, a), s*)

L10 CAT(x, y): ∅ if x = ∅ or y = ∅; y if x = ε; x if y = ε; otherwise the node x y
L11 ALT(x1, ..., xj): the set of the alternatives of all xi, with nested unions flattened and ∅ removed; ∅ if the set is empty, its member if it has one, otherwise the union node of the set
L12 STAR(x): ε if x = ∅ or x = ε; x if x is already a star; otherwise the node x*
```

Every expression is built through the constructors at lines L10 to L12, and every node is *hash-consed*: equal nodes get the same identifier, so the test at line L3 and the memo table of `D` cost $O(1)$ per lookup. A union is stored as a set of alternatives, which makes it associative, commutative and idempotent; this is what keeps the number of different derivatives finite. Each node stores its NULLABLE bit, computed by the constructor from the bits of its children, so line L4 takes $O(1)$.

The implementation computes `D` with an explicit stack in postorder, and it visits the right side $t$ of a concatenation only when NULLABLE(s) holds.

## Example

**A run.** Let $r = (a \mid b)^* ab$, the words that end in $ab$, parsed as $((a \mid b)^* a)\, b$. On $w = bab$:

| prefix read | derivative | nullable |
|---|---|---|
| $\varepsilon$ | $(a \mid b)^* ab$ | no |
| $b$ | $(a \mid b)^* ab$ | no |
| $ba$ | $(\varepsilon \mid (a \mid b)^* a)\, b$ | no |
| $bab$ | $\varepsilon \mid (a \mid b)^* ab$ | yes |

The first step: by line L8, $\partial_b(((a \mid b)^* a)\, b) = \mathrm{CAT}(\partial_b((a \mid b)^* a), b)$, and $\partial_b((a \mid b)^* a) = \mathrm{ALT}(\mathrm{CAT}(\partial_b (a \mid b)^*, a), \partial_b a)$. By line L9, $\partial_b (a \mid b)^* = \mathrm{CAT}(\varepsilon, (a \mid b)^*) = (a \mid b)^*$, and $\partial_b a = \emptyset$, which ALT drops. So the derivative is $r$ again. The last derivative is nullable, so $bab$ matches. Reading one more $a$ gives $(\varepsilon \mid (a \mid b)^* a)\, b$ again.

**The DFA of derivatives.** Starting from $r$ and taking derivatives by $a$ and $b$ until no new expression appears gives three states:

| state | expression | accepting | on $a$ | on $b$ |
|---|---|---|---|---|
| 0 | $(a \mid b)^* ab$ | no | 1 | 0 |
| 1 | $(\varepsilon \mid (a \mid b)^* a)\, b$ | no | 1 | 2 |
| 2 | $\varepsilon \mid (a \mid b)^* ab$ | yes | 1 | 0 |

This is the minimal DFA for the language. For $(a \mid b)^* a (a \mid b)(a \mid b)$ the same method gives 8 states, also minimal.

**Why normalization matters.** Without the constructors, applying the rules of lines L5 to L9 literally, the derivatives of $(a^* b^*)^*$ by $a, aa, aaa, \ldots, a^8$ have 19, 49, 109, 229, 469, 949, 1909 and 3829 nodes, about twice as many at each step. With the constructors, every one of them is $a^* b^* (a^* b^*)^*$.

**Not always minimal.** The derivatives of $(a^* b^*)^*$ are $(a^* b^*)^*$, $a^* b^* (a^* b^*)^*$ and $b^* (a^* b^*)^*$, so the DFA has 3 states, while the language is $\{a, b\}^*$, whose minimal DFA has 1 state. Similarly, $a^* \mid a$ gives 4 states for a language with 2 (the words in $a^*$, and the rest). The rules see only the syntax, so two expressions with the same language can stay apart; [DFA minimization](/dfa-minimization/) merges them.

**Small derivatives, large DFA.** For $L_n = (a \mid b)^* a (a \mid b)^{n-1}$, with $m = 4n + 2$ nodes, the derivative DFA has $2^n$ states for $n = 1, \ldots, 8$, the size of the minimal DFA, but every derivative has at most $6n + 2$ nodes. The matcher never builds the DFA, so on this family its work per symbol stays linear in $m$.

## Correctness

Two facts carry the proof. First, $L(\partial_a r) = a^{-1}L(r)$, by induction on $r$. For a concatenation, a word $av$ is in $L(st)$ either because $a$ starts the part from $s$, which gives $\partial_a(s)\, t$, or because the part from $s$ is empty and $a$ starts the part from $t$, which is possible only when $\nu(s)$ holds. For a star, $av \in L(s^*)$ means that the first nonempty iteration starts with $a$, which gives $\partial_a(s)\, s^*$. The constructors at lines L10 to L12 only apply language identities such as $\emptyset x = \emptyset$, $\varepsilon x = x$ and $x \mid x = x$, so they do not change the language. Second, $\nu(r)$ is true exactly when $\varepsilon \in L(r)$, by the same induction.

By induction on $i$, after $i$ rounds of the loop, $L(r) = (a_1 \cdots a_i)^{-1} L(r_0)$, where $r_0$ is the input expression. If line L3 returns, the quotient is empty, so no extension of the prefix matches. Otherwise line L4 returns $\nu(r)$, which is true if and only if $\varepsilon \in w^{-1}L(r_0)$, that is, $w \in L(r_0)$. The loop runs $n$ times, and each call of `D` is a postorder over the finitely many nodes below $r$, so the algorithm stops. The full proof is below.

## Complexity

- **Per symbol.** A call $D(r, a)$ visits each node of $r$ at most once, and does $O(1)$ hash operations per child, so the first call on a pair $(r, a)$ costs $O(|r|) \le O(d)$ expected time. A later call on the same pair is one lookup. The total is $O(m + n d)$ expected time, where $O(m)$ builds the input expression.
- **Space.** Each call adds at most $O(d)$ new nodes and memo entries, so the table holds $O(m + n d)$ entries. Since there are finitely many different derivatives, the table stops growing once all derivatives reached by the input have been seen.
- **The size $d$.** Brzozowski's [finiteness theorem](/brzozowski-finiteness-theorem/) bounds the number of different derivatives, so $d$ is finite for every $r$. No bound polynomial in $m$ is claimed here for the size of one derivative. In the examples above, $d$ is at most $2m$.
- **The DFA.** Building all derivatives, as in the example, costs $O(D \cdot |\Sigma| \cdot d)$ expected time for $D$ states. $D$ can be $2^n$ for an expression with $O(n)$ nodes, as for $L_n$ above.

## Properties

- **Deterministic.** The state after each prefix is one expression, not a set of states; the method is a [subset construction](/subset-construction/) in which the subsets are written as expressions.
- **Lazy.** The matcher computes only the derivatives that the input reaches, and memoization turns it into a [lazy DFA](/lazy-dfa-construction/) whose states are expressions.
- **Early failure.** Once the derivative is $\emptyset$, no extension of the prefix can match, and the matcher stops.
- **Boolean operators for free.** The rules extend to intersection, $\partial_a(r \,\&\, s) = \partial_a r \,\&\, \partial_a s$, and to complement, $\partial_a(\lnot r) = \lnot \partial_a r$, with $\nu(r \,\&\, s) = \nu(r) \land \nu(s)$ and $\nu(\lnot r) = \lnot \nu(r)$. Owens, Reppy and Turon (2009) name this as a main advantage over automaton constructions, where complement needs a determinization. These operators go beyond the notation of this site, but they keep the languages regular.
- **Not minimal.** The DFA of derivatives can be larger than the minimal DFA, as the example $(a^* b^*)^*$ shows; Owens, Reppy and Turon (2009) report that it is usually smaller than the DFA of the McNaughton and Yamada method.

## Variants and improvements

- **Derivative DFA.** Compute all derivatives in advance, as in the example, and match with a table; this is how scanner generators such as the one of Owens, Reppy and Turon (2009) use the method.
- **Partial derivatives.** [Antimirov derivatives](/antimirov-derivatives/) split a derivative into a set of terms whose union is the derivative. The sets of terms form an NFA with at most $k + 1$ states for $k$ symbol occurrences, which avoids the exponential number of states.
- **Character classes.** For large alphabets such as Unicode, compute derivatives by classes of symbols that behave the same way, instead of one symbol at a time.
- **Extended features.** Moseley and others (2023) built a derivative-based backend for .NET 7 that supports anchors and counted repetition, and reports the same matches as a backtracking engine without backtracking.
- **Grammars.** [Parsing with derivatives](/parsing-with-derivatives/) applies the same rules to context-free grammars, with laziness and memoization to handle recursion (Might, Darais and Spiewak, 2011).

## When to use it

Use derivatives when the expression has intersection or complement, when a small and readable implementation matters, as in functional languages and in proof assistants, or when a DFA must be built from an expression without an intermediate NFA. For plain matching of long texts with fixed expressions, a precomputed DFA or a [lazy DFA](/lazy-dfa-construction/) over a [Thompson NFA](/thompson-construction/) has a smaller constant per symbol, since each step is one table lookup instead of a hash lookup on expressions.

Derivatives cannot handle backreferences. The language of `(a*)b\1` is $\{a^i b a^i : i \ge 0\}$; its quotients by $a^0, a^1, a^2, \ldots$ are all different, since $b a^i$ is in the $i$-th quotient only. A language with infinitely many quotients is not regular, so no finite set of derivatives can describe it. Engines with backreferences use [backtracking](/backtracking-regex-matching/).

## Pitfalls

- **No normalization.** Without the constructors, the derivatives grow without bound, as in the example $(a^* b^*)^*$, and the DFA construction does not terminate. At least associativity, commutativity and idempotence of union are needed for termination.
- **Normalization that is not consistent.** If union is stored as a list, $x \mid y$ and $y \mid x$ are two states. Sort the alternatives or store them as a set, and hash-cons the nodes so that equal expressions are equal objects.
- **The nullable side of a concatenation.** Line L8 must add $\partial_a t$ when $\nu(s)$ holds; in $a^* b$ the derivative by $b$ is $\varepsilon$, which comes only from that branch.
- **Star of a nullable body.** $\partial_a(s^*) = \partial_a(s)\, s^*$ is correct even when $\varepsilon \in L(s)$. Defining it through the unfolding $\varepsilon \mid s s^*$ instead makes the rule for $s s^*$ call itself on $s^*$ when $\nu(s)$ holds, and the computation does not stop.
- **Recursion depth.** The derivative rules are recursive, and a recursive implementation overflows the call stack on deep expressions, for example a long concatenation. Use an explicit stack.
- **Cost of hashing.** Each new node is hashed, and a union with many alternatives hashes a large set. Cache the hash in the node.

## Implementations

## History

Brzozowski (1964) defined the derivative of a regular expression, including expressions with intersection and complement, proved that an expression has only finitely many dissimilar derivatives up to associativity, commutativity and idempotence of union, and used the derivatives as the states of a deterministic automaton. Antimirov (1996) introduced partial derivatives, which give nondeterministic automata. Owens, Reppy and Turon (2009) revived the method for scanner generators in functional languages, and Might, Darais and Spiewak (2011) extended it to context-free parsing. Moseley and others (2023) describe the derivative-based backend that .NET 7 shipped.

## References
