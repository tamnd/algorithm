---
tag: 8ND4RM
kind: definition
slug: expspace
name: EXPSPACE
aliases:
- exponential space
area: complexity/complexity-classes
level: advanced
summary: The decision problems that a deterministic Turing machine solves with 2^p(n) cells of work tape for a polynomial p. It strictly contains PSPACE.
prereqs: [pspace, exptime, space-hierarchy-theorem]
see_also: [savitch-theorem, nexptime, alternating-turing-machine, regex-equivalence-pspace-completeness, regular-expression, petri-net, qsat, time-hierarchy-theorem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 9.1, Hierarchy Theorems (exponential space completeness and regular expressions with exponentiation)
  - paper: doi:10.1109/SWAT.1972.29
    title: Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory, 125 to 129 (1972)
    locator: the main theorem, EXPSPACE-completeness of regular expressions with squaring
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 177 to 192 (1970)
    locator: NSPACE(s) in DSPACE(s^2)
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 114 to 133 (1981)
    locator: alternating time and deterministic space
  - paper: doi:10.1109/FOCS.1965.11
    title: Richard E. Stearns, Juris Hartmanis and Philip M. Lewis II, Hierarchies of memory limited computations, 6th Annual Symposium on Switching Circuit Theory and Logical Design, 179 to 190 (1965)
    locator: the space hierarchy
---

EXPSPACE is the class of decision problems that a deterministic Turing machine decides with $2^{p(n)}$ cells of work tape on inputs of length $n$, for some polynomial $p$. It is to exponential space what [PSPACE](/pspace/) is to polynomial space. By Savitch's theorem, nondeterminism adds nothing, and by the space hierarchy theorem, EXPSPACE strictly contains PSPACE. So an EXPSPACE-complete problem is provably not in PSPACE. The first natural problem of this kind was found by Meyer and Stockmeyer in 1972: deciding whether two regular expressions with a squaring operator describe the same language. Whether EXPSPACE equals [EXPTIME](/exptime/) is open.

## Definition

**Model.** The machine is a deterministic [multitape Turing machine](/multitape-turing-machine/) with a read-only input tape, and only the work tapes count. $\mathsf{DSPACE}(s(n))$ is the class of languages decided by such a machine that halts on every input and uses $O(s(n))$ work cells on inputs of length $n$.

**Definition.**

$$\mathsf{EXPSPACE} = \bigcup_{k \ge 1} \mathsf{DSPACE}\left(2^{n^k}\right).$$

**Nondeterminism.** $\mathsf{NEXPSPACE} = \bigcup_k \mathsf{NSPACE}(2^{n^k})$ is equal to EXPSPACE. By [Savitch's theorem](/savitch-theorem/), $\mathsf{NSPACE}(2^{n^k}) \subseteq \mathsf{DSPACE}(2^{2 n^k})$, and $2^{2 n^k} \le 2^{n^{k+1}}$ for $n \ge 2$.

**Alternation.** Chandra, Kozen and Stockmeyer (1981) proved $\mathsf{ATIME}(t) \subseteq \mathsf{DSPACE}(t) \subseteq \mathsf{ATIME}(t^2)$ for $t(n) \ge n$. So EXPSPACE is also the class of problems that an [alternating Turing machine](/alternating-turing-machine/) decides in time $2^{n^{O(1)}}$, just as PSPACE is alternating polynomial time.

**Completeness.** A language $B$ is EXPSPACE-complete if $B \in \mathsf{EXPSPACE}$ and every language in EXPSPACE reduces to $B$ by a polynomial-time many-one reduction; see [polynomial-time reduction](/polynomial-time-reduction/).

**Inclusions.**

$$\mathsf{PSPACE} \subseteq \mathsf{EXP} \subseteq \mathsf{NEXP} \subseteq \mathsf{EXPSPACE} \subseteq \mathsf{2EXP}.$$

- $\mathsf{NEXP} \subseteq \mathsf{EXPSPACE}$: a deterministic machine tries all branches of a nondeterministic machine with time $2^{n^k}$ one after another, and it stores only the current branch, which has $2^{n^k}$ choices. See [NEXPTIME](/nexptime/).
- $\mathsf{EXPSPACE} \subseteq \mathsf{2EXP} = \bigcup_k \mathsf{DTIME}(2^{2^{n^k}})$, because a machine with space $2^{n^k}$ that halts has at most $2^{2^{O(n^k)}}$ configurations.
- $\mathsf{PSPACE} \subsetneq \mathsf{EXPSPACE}$ by the [space hierarchy theorem](/space-hierarchy-theorem/): $\mathsf{PSPACE} \subseteq \mathsf{DSPACE}(2^n) \subsetneq \mathsf{DSPACE}(2^{2n}) \subseteq \mathsf{EXPSPACE}$.
- $\mathsf{EXP} \subsetneq \mathsf{2EXP}$ by the [time hierarchy theorem](/time-hierarchy-theorem/), so at least one of the inclusions $\mathsf{EXP} \subseteq \mathsf{EXPSPACE}$ and $\mathsf{EXPSPACE} \subseteq \mathsf{2EXP}$ is strict. Which one is open.
- By padding, $\mathsf{P} = \mathsf{PSPACE}$ would imply $\mathsf{EXP} = \mathsf{EXPSPACE}$. So a proof of $\mathsf{EXP} \ne \mathsf{EXPSPACE}$ would separate P from PSPACE.

## Examples and non-examples

**Regular expressions with squaring.** Extend [regular expressions](/regular-expression/) over $\{0, 1\}$ by the operator $E^2$, which means $EE$. Meyer and Stockmeyer (1972) proved that deciding whether such an expression describes all strings over its alphabet, and with it the equivalence of two such expressions, is EXPSPACE-complete. The reason is the compression that squaring allows. Let $E_0 = (0+1)$ and $E_{j+1} = (E_j)^2$. Then $E_k$ describes exactly the strings of length $2^k$; for $k = 0, 1, 2, 3$ it describes 2, 4, 16 and 256 strings. Written with squaring, $E_k$ has $5 + 4k$ symbols, because each squaring adds "(", ")", "^" and "2". Written out without squaring, it is $(0+1)$ repeated $2^k$ times, with $5 \cdot 2^k$ symbols. For $k = 10$ that is 45 symbols against 5120, and for $k = 20$ it is 85 against 5242880.

So an expression with squaring can count to $2^n$ with $O(n)$ symbols. The hardness proof uses this to describe the rows of an exponential-space computation: each row has $2^{n^k}$ cells, and an expression of polynomial size can check that two symbols lie exactly one row apart. The upper bound writes the expression out, which costs a factor of at most $2^{O(n)}$ in size, and runs the polynomial-space algorithm for ordinary expressions on the result; see [regular expression equivalence](/regex-equivalence-pspace-completeness/). Without squaring, the same problem is PSPACE-complete.

**Vector addition systems and Petri nets.** In a [Petri net](/petri-net/), the coverability problem asks whether some reachable marking has at least a given number of tokens in each place. Lipton (1976) proved that it needs exponential space, and Rackoff (1978) proved that it can be solved in exponential space, so it is EXPSPACE-complete. The reachability problem for Petri nets is much harder: it is decidable, but recent work shows that it is not even elementary.

**Commutative semigroups.** Mayr and Meyer (1982) proved exponential-space lower bounds for the word problem of finitely presented commutative semigroups and for the membership problem of polynomial ideals.

**PSPACE problems (in EXPSPACE, but not complete).** Every problem in PSPACE, such as [QSAT](/qsat/), is in EXPSPACE. No PSPACE problem is EXPSPACE-complete, since $\mathsf{PSPACE} \ne \mathsf{EXPSPACE}$.

**Problems beyond EXPSPACE.** The [halting problem](/undecidability/) is not in any space class. Among decidable problems, Petri net reachability, above, is outside EXPSPACE.

## Related definitions

- **PSPACE** is the polynomial version and a proper subset. See [PSPACE](/pspace/).
- **EXPTIME** is contained in EXPSPACE. Whether they are equal is open. See [EXPTIME](/exptime/).
- **NEXPTIME** is contained in EXPSPACE. See [NEXPTIME](/nexptime/).
- **NEXPSPACE** equals EXPSPACE by Savitch's theorem.
- **AEXPTIME**, alternating exponential time, equals EXPSPACE by Chandra, Kozen and Stockmeyer.
- **2EXP**, doubly exponential time, contains EXPSPACE, and it equals alternating exponential space.

## References
