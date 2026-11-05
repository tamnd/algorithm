---
tag: G0N1RW
kind: theorem
slug: brzozowski-finiteness-theorem
name: Brzozowski finiteness theorem
aliases:
- finiteness of dissimilar derivatives
area: automata-and-parsing/regular-expressions
level: advanced
summary: Modulo associativity, commutativity and idempotence of union, a regex has finitely many distinct derivatives.
prereqs: [regex-derivative, regular-expression]
see_also: [brzozowski-derivatives, antimirov-derivatives, myhill-nerode-theorem, kleene-theorem, regex-equivalence, deterministic-finite-automaton, extended-regular-expressions]
sources:
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494 (similarity of expressions, the theorem that every expression has only finitely many dissimilar derivatives, and the automaton whose states are the derivatives)
  - paper: doi:10.1017/S0956796808007090
    title: Scott Owens, John Reppy and Aaron Turon, Regular-expression derivatives re-examined, Journal of Functional Programming 19(2) (2009)
    locator: pp. 173 to 190 (derivatives with more simplification rules than similarity, used to build DFAs for scanner generators)
  - paper: doi:10.1016/0304-3975(95)00182-4
    title: Valentin Antimirov, Partial derivatives of regular expressions and finite automaton constructions, Theoretical Computer Science 155(2) (1996)
    locator: pp. 291 to 319 (an expression with k symbol occurrences has at most k + 1 partial derivatives)
---

Brzozowski's finiteness theorem says that the [derivatives](/regex-derivative/) of a regular expression by all words, which are infinitely many expressions, fall into finitely many classes once union is treated as associative, commutative and idempotent. Two expressions in the same class denote the same language, so the classes can be the states of a [DFA](/deterministic-finite-automaton/) for the expression. The theorem is what makes the [derivative method](/brzozowski-derivatives/) terminate, and idempotence cannot be dropped from it.

## Statement

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

**Derivatives.** The test $\nu(r)$ is false for $\emptyset$ and for a symbol, true for $\varepsilon$ and for a star, $\nu(s) \lor \nu(t)$ for $s \mid t$, and $\nu(s) \land \nu(t)$ for $st$; it is true exactly when $\varepsilon \in L(r)$. For a symbol $a$, the derivative $\partial_a r$ is defined by
$$\partial_a \emptyset = \partial_a \varepsilon = \emptyset, \qquad \partial_a b = \begin{cases} \varepsilon & b = a \\ \emptyset & b \ne a \end{cases}, \qquad \partial_a (s \mid t) = \partial_a s \mid \partial_a t,$$
$$\partial_a (st) = \begin{cases} (\partial_a s)\, t \mid \partial_a t & \nu(s) \\ (\partial_a s)\, t & \text{otherwise} \end{cases}, \qquad \partial_a (s^*) = (\partial_a s)\, s^*,$$
and for words, $\partial_\varepsilon r = r$ and $\partial_{ua} r = \partial_a (\partial_u r)$. These are syntactic rules: they apply no simplification, so $\partial_a(ab)$ is the expression $\varepsilon b$, not $b$. They satisfy $L(\partial_u r) = \{v : uv \in L(r)\}$.

**Similarity.** Let $\sim$ be the smallest equivalence relation on expressions that contains
$$(x \mid y) \mid z \sim x \mid (y \mid z), \qquad x \mid y \sim y \mid x, \qquad x \mid x \sim x$$
and is a congruence: $x \sim x'$ implies $x \mid y \sim x' \mid y$, $y \mid x \sim y \mid x'$, $xy \sim x'y$, $yx \sim yx'$ and $x^* \sim x'^*$. Expressions with $x \sim y$ are *similar*.

**Theorem (Brzozowski, 1964).** For every regular expression $r$ over a finite alphabet $\Sigma$, the set $\{\partial_u r : u \in \Sigma^*\}$ meets only finitely many classes of $\sim$. If $N(r)$ is the number of these classes, then
$$N(\emptyset) = 1, \quad N(\varepsilon) = 2, \quad N(a) = 3, \quad N(s \mid t) \le N(s)\, N(t), \quad N(st) \le N(s)\, 2^{N(t)}, \quad N(s^*) \le 2^{N(s)}.$$

## In plain words

Reading a word letter by letter turns a pattern into a new pattern for the rest of the input. There are infinitely many words, so a priori there could be infinitely many such patterns.

The theorem says that there are not, as long as you do not tell apart patterns that differ only in the order of their choices, in how the choices are grouped, or in a choice that is listed twice. Up to that, a pattern has only a limited number of leftover patterns.

So these leftover patterns can be the states of a finite machine: each letter moves from one leftover pattern to the next, and a state accepts when its pattern allows the empty input. Without the rule that a choice listed twice counts once, the leftovers can keep growing forever, even for a pattern as simple as "any number of a's".

## Proof

Throughout, $\partial_a$ and $\nu$ are as in the statement.

**Lemma 1.** If $x \sim y$, then $\nu(x) = \nu(y)$ and $\partial_a x \sim \partial_a y$ for every symbol $a$.

*Proof.* Let $R$ be the set of pairs $(x, y)$ with $\nu(x) = \nu(y)$ and $\partial_a x \sim \partial_a y$ for all $a$. It is enough to show that $R$ is an equivalence relation that contains the three axioms and is a congruence, since $\sim$ is the smallest such relation. $R$ is an equivalence relation because $=$ and $\sim$ are. The axioms: $\nu$ is unchanged, because $\lor$ is associative, commutative and idempotent; and $\partial_a((x \mid y) \mid z) = (\partial_a x \mid \partial_a y) \mid \partial_a z \sim \partial_a x \mid (\partial_a y \mid \partial_a z) = \partial_a(x \mid (y \mid z))$, and the same for the other two axioms. Congruence: let $(x, x') \in R$. For $x \mid y$ against $x' \mid y$, $\nu$ agrees and $\partial_a x \mid \partial_a y \sim \partial_a x' \mid \partial_a y$. For $xy$ against $x'y$: $\nu(x) = \nu(x')$, so the same case of the rule applies, and $(\partial_a x)\, y \sim (\partial_a x')\, y$, with the same added term $\partial_a y$ if any. For $yx$ against $yx'$: the case depends on $\nu(y)$ only, $(\partial_a y)\, x \sim (\partial_a y)\, x'$, and the added terms are $\partial_a x \sim \partial_a x'$; also $\nu(y) \land \nu(x) = \nu(y) \land \nu(x')$. For $x^*$ against $x'^*$: $(\partial_a x)\, x^* \sim (\partial_a x')\, x'^*$. The cases with the arguments of $\mid$ swapped are the same. $\square$

By induction on $u$, Lemma 1 extends to words: $x \sim y$ implies $\partial_u x \sim \partial_u y$.

**Sums.** For a finite nonempty set $S$ of expressions, write $\Sigma S$ for the union of its members, in some order and grouping. By the axioms, all choices of order and grouping are similar, and if every member of $S$ is similar to a member of $S'$ and every member of $S'$ to a member of $S$, then $\Sigma S \sim \Sigma S'$: replace each member by a similar one, using the congruence, and then remove repeats with $x \mid x \sim x$. So the class of $\Sigma S$ depends only on the set of classes of the members of $S$. Also, $\partial_a(\Sigma S) = \Sigma \{\partial_a x : x \in S\}$, grouped the same way, by the rule for union.

**Lemma 2 (shape of the derivatives).** Let $u$ be a word.

1. $\partial_u(s \mid t) = \partial_u s \mid \partial_u t$.
2. There is a set $Y_u$ of words with $\partial_u(st) \sim \Sigma\big(\{(\partial_u s)\, t\} \cup \{\partial_y t : y \in Y_u\}\big)$.
3. If $u \ne \varepsilon$, there is a nonempty set $Y_u$ of words with $\partial_u(s^*) \sim \Sigma\{(\partial_y s)\, s^* : y \in Y_u\}$.

*Proof.* Each part is by induction on the length of $u$.

1. For $u = \varepsilon$ both sides are $s \mid t$, and $\partial_a(\partial_u s \mid \partial_u t) = \partial_{ua} s \mid \partial_{ua} t$ by the rule for union.
2. For $u = \varepsilon$, take $Y_\varepsilon = \emptyset$. For the step from $u$ to $ua$, apply $\partial_a$ to both sides; by Lemma 1 the results are similar. The left side becomes $\partial_{ua}(st)$. On the right, $\partial_a$ goes into each member of the sum. The member $(\partial_u s)\, t$ gives $(\partial_{ua} s)\, t$, together with $\partial_a t$ if $\nu(\partial_u s)$ holds. Each member $\partial_y t$ gives $\partial_{ya} t$. So the claim holds with $Y_{ua} = \{ya : y \in Y_u\}$, plus the word $a$ if $\nu(\partial_u s)$ holds.
3. For $u = a$, $\partial_a(s^*) = (\partial_a s)\, s^*$, so $Y_a = \{a\}$. For the step from $u$ to $ub$, each member $(\partial_y s)\, s^*$ gives $(\partial_{yb} s)\, s^*$, together with $\partial_b(s^*) = (\partial_b s)\, s^*$ if $\nu(\partial_y s)$ holds. So $Y_{ub} = \{yb : y \in Y_u\}$, plus the word $b$ if $\nu(\partial_y s)$ holds for some $y \in Y_u$; it is nonempty because $Y_u$ is. $\square$

**Proof of the theorem.** By induction on the structure of $r$.

- $r = \emptyset$: every derivative is $\emptyset$, so $N(\emptyset) = 1$.
- $r = \varepsilon$: the derivatives are $\varepsilon$ and, for $u \ne \varepsilon$, $\emptyset$. So $N(\varepsilon) = 2$.
- $r = a$: the derivatives are $a$, then $\varepsilon$ by $a$, and $\emptyset$ by every other word. So $N(a) = 3$.
- $r = s \mid t$: by Lemma 2.1 and the congruence, the class of $\partial_u r$ depends only on the classes of $\partial_u s$ and $\partial_u t$. There are at most $N(s) N(t)$ such pairs.
- $r = st$: by Lemma 2.2, the class of $\partial_u r$ depends only on the class of $\partial_u s$, which fixes the class of $(\partial_u s)\, t$ by the congruence, and on the set of classes of the $\partial_y t$ with $y \in Y_u$, which is a subset of the $N(t)$ classes of derivatives of $t$. So $N(st) \le N(s) \cdot 2^{N(t)}$.
- $r = s^*$: the word $\varepsilon$ gives $r$ itself. For $u \ne \varepsilon$, by Lemma 2.3, the class of $\partial_u r$ depends only on a nonempty set of classes of derivatives of $s$, and there are at most $2^{N(s)} - 1$ such sets. So $N(s^*) \le 2^{N(s)}$.

In every case $N(r)$ is finite. $\blacksquare$

**The same proof for normalized derivatives.** The [derivative matcher](/brzozowski-derivatives/) stores each union as a set of alternatives and also applies $\emptyset x = x \emptyset = \emptyset$, $\varepsilon x = x \varepsilon = x$, $x \mid \emptyset = x$, $\emptyset^* = \varepsilon^* = \varepsilon$ and $(x^*)^* = x^*$ when it builds a node, so that two unions with the same set of alternatives are the same object. The proof above uses the rules for union, concatenation and star only through Lemma 2, and Lemma 2 still holds with $=$ in place of $\sim$. The one case to check is that the derivative of the normalized product of $x$ and $t$ is still the normalized form of $(\partial_a x)\, t$, joined with $\partial_a t$ when $\nu(x)$ holds. If $x = \emptyset$ or $t = \emptyset$, both sides are $\emptyset$. If $x = \varepsilon$ the product is $t$, and the formula gives $\emptyset \mid \partial_a t = \partial_a t$. If $t = \varepsilon$ the product is $x$, and the formula gives $\partial_a x \mid \emptyset = \partial_a x$. So the matcher, too, meets only finitely many different expressions.

## Consequences

- **Kleene's theorem, from expressions to automata.** Take one state for each class, the class of $r$ as the start state, $\partial_a$ as the move on $a$, which is well defined on classes by Lemma 1, and the classes with $\nu$ true as the accepting states. By $L(\partial_u r) = u^{-1}L(r)$, this DFA accepts $L(r)$. So every regular expression has a DFA, without an NFA in between; see [Kleene's theorem](/kleene-theorem/).
- **Termination of derivative algorithms.** The DFA construction of the [derivative method](/brzozowski-derivatives/) explores derivatives until no new one appears, and the theorem says that this happens. A lazy derivative matcher keeps a cache that is bounded by $N(r)$ times the alphabet size.
- **Boolean operators.** With $\partial_a(s \,\&\, t) = \partial_a s \,\&\, \partial_a t$ and $\partial_a(\lnot s) = \lnot \partial_a s$, the same proof gives $N(s \,\&\, t) \le N(s)\, N(t)$ and $N(\lnot s) \le N(s)$. So expressions with intersection and complement, the [extended regular expressions](/extended-regular-expressions/) of language theory, still denote regular languages, and their DFAs can be built in the same way. These operators go beyond the notation of this site.
- **Deciding equivalence.** $L(r) = L(s)$ if and only if $\nu(\partial_u r) = \nu(\partial_u s)$ for every word $u$. Exploring the pairs $(\partial_u r, \partial_u s)$ up to similarity visits at most $N(r) N(s)$ pairs, so the search ends, and it finds a word in exactly one of the languages if there is one; see [regex equivalence](/regex-equivalence/).
- **A syntactic Myhill-Nerode bound.** Similar expressions denote the same language, so the number of different quotients $u^{-1}L(r)$, which is the number of states of the minimal complete DFA by the [Myhill-Nerode theorem](/myhill-nerode-theorem/), is at most $N(r)$.

## Tightness

**Idempotence is needed.** Keep associativity and commutativity of union but drop $x \mid x \sim x$. Then the derivatives of $a^*$ by $a, aa, aaa, \ldots$ are $\varepsilon a^*$, then $\emptyset a^* \mid \varepsilon a^*$, then $\emptyset a^* \mid \emptyset a^* \mid \varepsilon a^*$, and in general $i - 1$ copies of $\emptyset a^*$ and one copy of $\varepsilon a^*$ after $a^i$. These are pairwise different for $i = 1, 2, \ldots$, so there are infinitely many classes. With idempotence, the derivatives of $a^*$ fall into 4 classes: $a^*$, $\varepsilon a^*$, $\emptyset a^* \mid \varepsilon a^*$, and $\emptyset a^*$ (by any word with a $b$, over $\{a, b\}$).

**Exponentially many classes are unavoidable.** Let $L_n = (a \mid b)^* a (a \mid b)^{n-1}$, the words over $\{a, b\}$ whose $n$-th symbol from the end is $a$. The expression has $4n + 2$ nodes, and its minimal complete DFA has $2^n$ states, since a DFA must remember the last $n$ symbols. By the last consequence above, $N(L_n) \ge 2^n$. The counts of classes for the rules of the statement, and for the normalized rules of the derivative matcher, over the alphabet $\{a, b\}$, are:

| expression | classes of $\sim$ | normalized derivatives | minimal DFA states |
|---|---|---|---|
| $a^*$ | 4 | 2 | 2 |
| $(a^* b^*)^*$ | 8 | 3 | 1 |
| $(a \mid b)^* ab$ | 9 | 3 | 3 |
| $L_1$ | 5 | 2 | 2 |
| $L_2$ | 9 | 4 | 4 |
| $L_3$ | 15 | 8 | 8 |
| $L_4$ | 27 | 16 | 16 |
| $L_5$ | 51 | 32 | 32 |

**The gap to the language count.** $(a^* b^*)^*$ denotes $\{a, b\}^*$, which has one quotient, but its derivatives fall into 8 classes of $\sim$, and 3 even after normalization. Similarity is a syntactic test: it does not identify all expressions with the same language, and minimization is a separate step.

**The bound of the proof.** The recurrences give a tower of exponentials for nested stars and concatenations. The theorem only needs finiteness, and this page makes no claim about how close the worst case comes to these recurrences. For the nondeterministic version, Antimirov (1996) showed that an expression with $k$ symbol occurrences has at most $k + 1$ partial derivatives, so the derivatives, as sets of partial derivatives, are at most $2^{k+1}$ different languages.

## History

Brzozowski (1964) introduced derivatives of regular expressions, with intersection, complement and other Boolean operations included, defined similarity by the associativity, commutativity and idempotence of union, and proved that every expression has only finitely many dissimilar derivatives. He used the result to build a deterministic automaton directly from an expression. Antimirov (1996) split each derivative into partial derivatives and obtained the linear bound for them. Owens, Reppy and Turon (2009) used derivatives with more simplification rules than similarity to generate scanners, and reported smaller DFAs than those of the McNaughton and Yamada method.

## References
