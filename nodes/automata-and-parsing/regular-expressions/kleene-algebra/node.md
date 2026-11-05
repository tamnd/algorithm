---
tag: Y3W6S7
kind: concept
slug: kleene-algebra
name: Kleene algebra
aliases:
- KA
area: automata-and-parsing/regular-expressions
level: advanced
summary: An algebraic structure of choice, sequence and star axiomatizing the equational theory of regular expressions.
prereqs: [regular-expression, kleene-star, arden-lemma]
see_also: [kleene-algebra-with-tests, regex-equivalence, regex-equivalence-pspace-completeness, kleene-theorem, transitive-closure, floyd-warshall, warshall-algorithm, dfa-to-regex-conversion]
sources:
  - paper: doi:10.1006/inco.1994.1037
    title: Dexter Kozen, A completeness theorem for Kleene algebras and the algebra of regular events, Information and Computation 110(2) (1994)
    locator: pp. 366 to 390 (the axioms of Kleene algebra, the Kleene algebra of matrices, and the completeness theorem)
  - paper: doi:10.1016/0304-3975(91)90395-I
    title: Daniel Krob, Complete systems of B-rational identities, Theoretical Computer Science 89(2) (1991)
    locator: pp. 207 to 343 (complete axiomatizations of the equations between regular expressions by infinitely many equations)
  - paper: doi:10.1145/321312.321326
    title: Arto Salomaa, Two complete axiom systems for the algebra of regular events, Journal of the ACM 13(1) (1966)
    locator: pp. 158 to 169 (a complete system whose star rule has the side condition that the empty word is not in the coefficient)
  - paper: "V. N. Redko, On defining relations for the algebra of regular events, Ukrainskii Matematicheskii Zhurnal 16 (1964)"
    title: V. N. Redko, On defining relations for the algebra of regular events
    locator: pp. 120 to 126 (no finite set of equations axiomatizes the equations between regular expressions)
  - paper: doi:10.1016/0304-3975(77)90056-1
    title: Daniel J. Lehmann, Algebraic structures for transitive closure, Theoretical Computer Science 4(1) (1977)
    locator: pp. 59 to 76 (the star of matrices over semirings with a star, and its use for path problems)
  - paper: "doi:10.2168/LMCS-8(1:16)2012"
    title: Thomas Braibant and Damien Pous, Deciding Kleene algebras in Coq, Logical Methods in Computer Science 8(1) (2012)
    locator: paper 16 (a verified decision procedure for the equational theory of Kleene algebra, used as a proof tactic)
---

A Kleene algebra is a set with a choice operation $+$, a sequencing operation $\cdot$, constants $0$ and $1$, and a star, satisfying the axioms of an idempotent semiring and four axioms that make $a^*$ the least solution of a linear inequality. Kozen (1994) proved that these finitely many axioms derive exactly the equations between [regular expressions](/regular-expression/) that hold for their languages, so equational reasoning about regular expressions can be done by algebra. The same axioms also hold for binary relations, where the star is the reflexive transitive closure, and for shortest-path distances, so one theorem covers automata, programs and path problems.

## In plain words

Regular expressions obey many laws: choosing between $x$ and $x$ is the same as $x$, repeating "any number of times" twice is the same as doing it once, and so on. A Kleene algebra is any system in which a short, fixed list of such laws holds.

The surprise is that the short list is enough. Every law that is true for all regular expressions can be derived from it by ordinary algebra, by replacing equals by equals and by one extra rule that says that "repeat" is the smallest thing closed under one more step.

Other systems obey the same list. Relations between states, where "repeat" means "reach in any number of steps", and travel costs, where "choose" means "take the cheaper", are examples. So proofs done once in the algebra apply to all of them.

## The idea

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. In a Kleene algebra the union is written $+$, the empty language $0$ and the empty string $1$, as is usual in algebra; a regular expression is a term with $|$ read as $+$, $\emptyset$ as $0$ and $\varepsilon$ as $1$.

**Axioms.** A Kleene algebra $(K, +, \cdot, 0, 1, {}^*)$ satisfies, for all $a, b, c, x \in K$:

- $+$ is associative and commutative, $a + 0 = a$, and $a + a = a$;
- $\cdot$ is associative, $1 \cdot a = a \cdot 1 = a$, and $0 \cdot a = a \cdot 0 = 0$;
- $a(b + c) = ab + ac$ and $(a + b)c = ac + bc$;
- $1 + a a^* \le a^*$ and $1 + a^* a \le a^*$ (unfolding);
- if $b + a x \le x$ then $a^* b \le x$, and if $b + x a \le x$ then $b a^* \le x$ (induction).

Here $a \le b$ means $a + b = b$; it is a partial order because $+$ is idempotent, and all operations are monotone for it. The first three groups say that $K$ is an *idempotent semiring*. The induction axioms are Horn clauses, not equations: they make $a^* b$ the least solution of $b + ax \le x$, which is [Arden's lemma](/arden-lemma/) in algebraic form.

**Some derived laws.** All of the following hold in every Kleene algebra.

- $1 \le a^*$ and $a \le a^*$, by unfolding.
- $a^* a^* = a^*$. For $\le$, use the first induction axiom with $b = x = a^*$: $a^* + a a^* \le a^*$ holds by unfolding, so $a^* a^* \le a^*$. For $\ge$, $a^* = a^* \cdot 1 \le a^* a^*$.
- $(a^*)^* = a^*$. By induction with $b = 1$ and $x = a^*$: $1 + a^* a^* \le a^*$ by the previous law, so $(a^*)^* \le a^*$. Also $a^* \le (a^*)^*$, since $y \le y^*$ for every $y$.
- Monotonicity: if $a \le b$ then $a^* \le b^*$. Indeed $1 + a b^* \le 1 + b b^* \le b^*$, so $a^* \le b^*$ by induction.
- Sliding: $(ab)^* a = a (ba)^*$. For $\le$, take $x = a(ba)^*$: then $a \le x$ since $1 \le (ba)^*$, and $ab \cdot a (ba)^* = a\,(ba)(ba)^* \le a (ba)^*$, so $a + ab\,x \le x$ and induction gives $(ab)^* a \le x$. The other direction is the mirror image, with the second induction axiom.
- Denesting: $(a + b)^* = a^* (b a^*)^*$. Its proof from the axioms is longer.

**Completeness.** For regular expressions $r$ and $s$, write $\mathrm{KA} \vdash r = s$ if the equation follows from the axioms. Kozen (1994) proved:
$$\mathrm{KA} \vdash r = s \iff L(r) = L(s).$$
The direction from left to right holds because the languages over an alphabet form a Kleene algebra. The other direction is the hard part; the proof encodes automata as matrices, shows that the $n \times n$ matrices over a Kleene algebra form a Kleene algebra, and carries out determinization and minimization of automata as algebraic steps. In algebraic terms, the regular languages over $\Sigma$ form the free Kleene algebra on the generators $\Sigma$.

**Why the Horn clauses are needed.** Redko (1964) showed that no finite set of equations derives all the equations true for regular languages. So a finite complete system must use something other than equations. Salomaa (1966) used the rule "from $x = xa + b$ infer $x = b a^*$", valid only when $\varepsilon \notin L(a)$, a side condition that is not algebraic, since it is not preserved when $a$ is replaced by another term. Krob (1991) gave complete systems of equations, which are infinite. Kozen's axioms are finite, and all of them are preserved by substitution.

**Matrices.** If $K$ is a Kleene algebra, so are the $n \times n$ matrices over $K$, with the usual sum and product and with the star defined by blocks. For $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$ with square blocks $A$ and $D$, and $F = A + B D^* C$,
$$M^* = \begin{pmatrix} F^* & F^* B D^* \\ D^* C F^* & D^* + D^* C F^* B D^* \end{pmatrix}.$$
A finite automaton is a triple $(u, M, v)$, where $M_{ij}$ is the sum of the symbols on the moves from state $i$ to state $j$, $u$ marks the start state and $v$ the accepting states; it accepts $u M^* v$. Computing $M^*$ by blocks is the state elimination method of [DFA to regex conversion](/dfa-to-regex-conversion/), and over other Kleene algebras it is the [Floyd-Warshall](/floyd-warshall/) and [Warshall](/warshall-algorithm/) algorithms. Lehmann (1977) treated these path problems in this algebraic way.

**Complexity.** By completeness, deciding $\mathrm{KA} \vdash r = s$ is deciding [regex equivalence](/regex-equivalence/), which is [PSPACE-complete](/regex-equivalence-pspace-completeness/). Practical decision procedures build automata or derivatives for $r$ and $s$ and compare them.

## Examples

**Regular languages.** The subsets of $\Sigma^*$, or the regular ones only, with union, concatenation, $\emptyset$, $\{\varepsilon\}$ and the Kleene star. Every law above was checked here by comparing the words of length at most 8 over $\{a, b\}$: $a^* a^* = a^*$, $(a^*)^* = a^*$, $(ab)^* a = a (ba)^*$, $(a \mid b)^* = a^* (b a^*)^*$ and $(a \mid b)^* = (a^* b^*)^*$ hold, while $(ab)^* = a^* b^*$ fails, for instance on $aab$.

**Binary relations.** The relations on a set $X$, with union, composition, the empty relation, the identity relation, and the reflexive transitive closure as the star. Here $a^* b \le x$ says that if $x$ contains $b$ and is closed under a step of $a$ in front, it contains everything reachable. On a set of 3 points, all 512 relations satisfy the unfolding axioms, and 20000 random triples $(a, b, x)$ satisfy the induction axioms. Program semantics uses this model: a program denotes a relation between states, $+$ is nondeterministic choice, $\cdot$ is sequencing, and the star is a loop that runs any number of times.

**Shortest distances.** The numbers $[0, \infty]$ with $\min$ as $+$, ordinary addition as $\cdot$, $\infty$ as $0$, the number $0$ as $1$, and $a^* = 0$ for every $a$. The order $a \le b$ means $\min(a, b) = b$, so it is the reverse of the order of numbers. For a matrix of edge lengths, $M^*$ is the matrix of shortest distances, and computing it by blocks is the Floyd-Warshall algorithm. The axioms were checked on the values $0, 1, 2, 3, 5, \infty$.

**Booleans.** $\{0, 1\}$ with $\lor$, $\land$ and $0^* = 1^* = 1$. Matrices over it are relations on a finite set, and their star is the [transitive closure](/transitive-closure/) with the identity added.

**An automaton as a matrix.** The DFA with states 0 and 1 that switches state on $b$ and stays on $a$ has $M = \begin{pmatrix} a & b \\ b & a \end{pmatrix}$. The block formula gives $(M^*)_{00} = (a + b a^* b)^*$, so the words with an even number of $b$ are $(a \mid b a^* b)^*$; this agrees with a direct count on all words of length at most 8.

**A non-example.** Take the languages over $\Sigma$ with the usual $+$ and $\cdot$, but define $a^* = \Sigma^*$ for every $a$. Union and concatenation still form an idempotent semiring, and the unfolding axioms hold, since $\Sigma^*$ contains everything. The induction axiom fails: with $a = \emptyset$ and $b = x = \{\varepsilon\}$, $b + a x = \{\varepsilon\} \le x$, but $a^* b = \Sigma^* \not\le x$. Unfolding alone only says that $a^*$ is *some* solution of $1 + a x \le x$; the induction axioms make it the least one.

## Where it is used

- **Equivalence of regular expressions.** Algebraic proofs of identities such as sliding and denesting, and verified decision procedures: Braibant and Pous (2012) built one in Coq that decides the equational theory of Kleene algebra and is used as a proof tactic.
- **Program verification.** Programs with choice, sequence and loops form a Kleene algebra of relations; adding Boolean tests gives [Kleene algebra with tests](/kleene-algebra-with-tests/), which can express conditionals, while loops and [Hoare logic](/hoare-logic/) assertions.
- **Path problems.** Shortest paths, reachability and the regular expression of all paths are the star of a matrix in different Kleene algebras, and one algorithm, Gaussian elimination by blocks, computes all of them.
- **Automata theory.** The matrix view gives an algebraic proof of [Kleene's theorem](/kleene-theorem/), and the conversions between automata and expressions become algebraic identities.

## References
