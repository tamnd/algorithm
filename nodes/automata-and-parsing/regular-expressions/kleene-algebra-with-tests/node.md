---
tag: N3QB1H
kind: concept
slug: kleene-algebra-with-tests
name: Kleene algebra with tests
aliases:
- KAT
area: automata-and-parsing/regular-expressions
level: research
summary: Kleene algebra extended with Boolean tests, used to reason about program equivalence.
prereqs: [kleene-algebra]
see_also: [hoare-logic, regex-equivalence, regex-equivalence-pspace-completeness, relational-algebra, kleene-star, arden-lemma]
sources:
  - paper: doi:10.1145/256167.256195
    title: Dexter Kozen, Kleene algebra with tests, ACM Transactions on Programming Languages and Systems 19(3) (1997)
    locator: pp. 427 to 443 (the definition, the encoding of conditionals and while loops, and an equational proof that every while program can be simulated by one with at most one while loop)
  - paper: doi:10.1007/3-540-63172-0_43
    title: Dexter Kozen and Frederick Smith, Kleene algebra with tests, completeness and decidability, Computer Science Logic 1996, Lecture Notes in Computer Science 1258 (1997)
    locator: pp. 244 to 259 (completeness for the language model of guarded strings and for relational models, and decidability)
  - paper: doi:10.1145/343369.343378
    title: Dexter Kozen, On Hoare logic and Kleene algebra with tests, ACM Transactions on Computational Logic 1(1) (2000)
    locator: pp. 60 to 76 (KAT subsumes propositional Hoare logic, and deciding the relational validity of its inference rules is PSPACE-complete)
  - paper: doi:10.1007/3-540-44957-4_38
    title: Dexter Kozen and Maria-Cristina Patron, Certification of compiler optimizations using Kleene algebra with tests, Computational Logic 2000, Lecture Notes in Computer Science 1861 (2000)
    locator: pp. 568 to 582
  - paper: doi:10.1145/2535838.2535862
    title: Carolyn Jane Anderson, Nate Foster, Arjun Guha, Jean-Baptiste Jeannin, Dexter Kozen, Cole Schlesinger and David Walker, NetKAT, semantic foundations for networks, POPL 2014
    locator: pp. 113 to 126
---

A Kleene algebra with tests, or KAT, is a [Kleene algebra](/kleene-algebra/) that contains a Boolean algebra of special elements called tests. Kozen introduced it in 1997 to reason about while programs with the same algebra that describes [regular expressions](/regular-expression/): actions are letters, tests are guards, and conditionals and loops become sums, products and stars. Its equational theory is complete for a model of guarded strings and is decidable, so program equivalences of this kind can be checked by automata.

## In plain words

A program does things and asks questions. "Add one to x" is a thing it does; "is x less than 3?" is a question. In a Kleene algebra with tests both are elements of one algebra. Doing one step after another is a product, choosing between two branches is a sum, and repeating is a star.

A question is a filter: it lets the run go on if the answer is yes. Questions obey the laws of logic, so "ask b, then ask not b" is a run that never goes through, and "ask b or ask not b" lets every run through.

With these two kinds of elements, "if b then p else q" and "while b do p" are short formulas, and facts about programs, such as "running the same loop twice is the same as running it once", become equations that can be proved by algebra.

## The idea

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. As on the [Kleene algebra](/kleene-algebra/) page, the algebra writes the union as $+$, the empty language as $0$ and the empty string as $1$.

**Definition.** A Kleene algebra with tests is a structure $(K, B, +, \cdot, {}^*, 0, 1, \bar{\ })$ such that $(K, +, \cdot, {}^*, 0, 1)$ is a Kleene algebra, $B \subseteq K$, and $(B, +, \cdot, \bar{\ }, 0, 1)$ is a Boolean algebra. The elements of $B$ are *tests*. On tests, $+$ is "or", $\cdot$ is "and", $\bar b$ is "not b", $0$ is "false" and $1$ is "true". The complement $\bar{\ }$ is defined only on tests. So, for tests $b$ and $c$, the laws $bb = b$, $bc = cb$, $b \bar b = 0$ and $b + \bar b = 1$ hold, while for general elements $p$ and $q$ neither $pp = p$ nor $pq = qp$ is required.

**Programs.** With actions $p, q$ and a test $b$:

| program | KAT term |
|---|---|
| $p$; $q$ | $pq$ |
| if $b$ then $p$ else $q$ | $bp + \bar b q$ |
| while $b$ do $p$ | $(bp)^* \bar b$ |
| assert $b$ | $b$ |
| skip, and the program that never ends normally | $1$ and $0$ |

The loop term reads: some number of times, check that $b$ holds and run $p$; then check that $b$ fails.

**Hoare triples.** The partial correctness assertion $\{b\}\, p\, \{c\}$, "if $b$ holds before $p$ and $p$ ends, then $c$ holds after", is the equation $b p \bar c = 0$: no run starts in $b$, runs $p$ and ends in $\bar c$. Kozen (2000) shows that the rules of propositional Hoare logic become theorems of KAT under this encoding, so its special proof system can be replaced by equational reasoning.

**Models.** Two kinds of models matter most.

- *Relational models.* $K$ is a set of binary relations on a set of states, with union, composition and reflexive transitive closure, and $B$ is a set of subsets of the identity relation, a test being the identity on the states where it holds. This is the meaning of a program as an input-output relation.
- *Guarded strings.* Fix finite sets of primitive actions and primitive tests. An *atom* is a full truth assignment to the primitive tests. A guarded string is $\alpha_0 p_1 \alpha_1 p_2 \cdots p_n \alpha_n$, with atoms $\alpha_i$ and actions $p_i$. A KAT term denotes a set of guarded strings: a test denotes the atoms that satisfy it, an action $p$ denotes all strings $\alpha p \beta$, and the product joins $x \alpha$ and $\alpha y$ into $x \alpha y$ when the atoms agree.

**Completeness and decidability.** Kozen and Smith (1996) proved that an equation between KAT terms holds in all KATs if and only if the two terms denote the same set of guarded strings, and that it then holds in all relational models too. Sets of guarded strings are regular, so equivalence can be decided with automata, as for [regular expressions](/regex-equivalence/). For plain Kleene algebra the problem is [PSPACE-complete](/regex-equivalence-pspace-completeness/), and Kozen (2000) shows that deciding the relational validity of Hoare-style inference rules in KAT is PSPACE-complete too.

## Examples

**The guarded strings of a loop.** With one primitive test $b$, the atoms are $b$ and $\bar b$. The loop $(bp)^* \bar b$ denotes

$$\bar b, \quad b\, p\, \bar b, \quad b\, p\, b\, p\, \bar b, \quad b\, p\, b\, p\, b\, p\, \bar b, \quad \dots$$

that is, every run in which $b$ holds before each step and fails at the end. The conditional $bp + \bar b q$ denotes the four strings $b p b$, $b p \bar b$, $\bar b q b$ and $\bar b q \bar b$.

**Running a loop twice is the same as once.** Let $W = (bp)^* \bar b$. In every Kleene algebra $x^* = 1 + x x^*$. Then

$$\bar b W = \bar b (1 + bp (bp)^*) \bar b = \bar b \bar b + \bar b b \, p (bp)^* \bar b = \bar b + 0 = \bar b,$$

using $\bar b \bar b = \bar b$ and $\bar b b = 0$. So $W W = (bp)^* (\bar b W) = (bp)^* \bar b = W$. The Boolean laws are needed: if $b$ and $\bar b$ are read as two unrelated letters, the language of $WW$ contains $bpbp\bar b\bar b$, which is not in the language of $W$.

**Tests do not commute with actions.** In the guarded-string model $pb$ denotes $\{b p b, \bar b p b\}$, and $bp$ denotes $\{b p b, b p \bar b\}$. They differ, as they should: "run p, then check b" is not "check b, then run p". Facts such as $bp = pb$, "p does not change b", are added as hypotheses when they hold for a particular program, which is how Kozen's proof of the one-loop theorem uses commutativity conditions.

**A relational model.** Let the states be $x \in \{0, 1, 2, 3\}$, let $b$ be the test $x < 3$, and let $p$ be $x := \min(x + 1, 3)$. The relation of $(bp)^* \bar b$ is $\{(0, 3), (1, 3), (2, 3), (3, 3)\}$: from every state the loop ends at 3.

**A Hoare triple.** With $e$ the test "x is even" and $p$ the action $x := (x + 2) \bmod 4$ on the same states, $e\, p\, \bar e = 0$, so $\{e\}\, p\, \{e\}$ holds. For $x := (x + 1) \bmod 4$ instead, $e\, p\, \bar e$ is the relation $\{(0, 1), (2, 3)\}$, which is not $0$, so the triple fails.

## Where it is used

- **Program equivalence.** Kozen (1997) gives an equational proof, in KAT with commutativity conditions, that every while program can be simulated by a while program with at most one while loop.
- **Hoare logic.** KAT subsumes propositional [Hoare logic](/hoare-logic/), and gives a decision procedure for the propositional part of correctness proofs.
- **Compiler optimizations.** Kozen and Patron (2000) use KAT to certify standard optimizations of compilers as equations between program terms.
- **Networks.** NetKAT (Anderson and others, 2014) extends KAT with tests and assignments on the fields of packets, so that the forwarding behaviour of a network is a KAT term and questions about it become equations.
- **Automata.** Because the guarded-string sets are regular, the tools for [regular expression equivalence](/regex-equivalence/), such as derivatives and bisimulation of automata, carry over to programs.

## References
