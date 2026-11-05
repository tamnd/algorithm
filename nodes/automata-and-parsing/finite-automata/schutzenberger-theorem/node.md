---
tag: SR3FQW
kind: theorem
slug: schutzenberger-theorem
name: Schützenberger's theorem
aliases:
- Schützenberger theorem on star-free languages
- star-free aperiodic theorem
area: automata-and-parsing/finite-automata
level: research
summary: A regular language is star-free iff its syntactic monoid is aperiodic.
prereqs: [star-free-language, syntactic-monoid, regular-language]
see_also: [krohn-rhodes-theorem, star-free-expressions, linear-temporal-logic, myhill-nerode-theorem, dfa-minimization, cyclic-group, finite-group, pspace]
sources:
  - paper: "Marcel-Paul Schützenberger, On finite monoids having only trivial subgroups, Information and Control 8(2) (1965)"
    locator: pp. 190 to 194 (the theorem, in both directions)
  - book: "Jean-Éric Pin, Varieties of Formal Languages, North Oxford Academic, 1986"
    locator: the chapter on star-free languages and aperiodic monoids (the proof by induction on ideals followed here)
  - book: "Robert McNaughton and Seymour Papert, Counter-Free Automata, MIT Press, 1971"
    locator: the chapters on counter-free automata, star-free sets and first-order definability
  - paper: "Sang Cho and Dung T. Huynh, Finite-automaton aperiodicity is PSPACE-complete, Theoretical Computer Science 88(1) (1991)"
    locator: pp. 99 to 116 (the decision problem for a language given by a DFA)
---

Schützenberger's theorem says that a [regular language](/regular-language/) is [star-free](/star-free-language/), that is, built from letters with union, concatenation and complement but no star, if and only if its [syntactic monoid](/syntactic-monoid/) is aperiodic, that is, contains no non-trivial group. It turns a question about all possible expressions into a finite test on one monoid, so star-freeness is decidable. It was the first of many results that match a class of regular languages with a class of finite monoids, and with the theorem of McNaughton and Papert it also characterizes the languages definable in first-order logic.

## Statement

Let $\Sigma$ be a finite alphabet, $L \subseteq \Sigma^*$ a regular language, and $M(L)$ its syntactic monoid, the quotient of $\Sigma^*$ by $u \equiv_L v \iff (\forall x, y : xuy \in L \Leftrightarrow xvy \in L)$. A finite monoid $M$ is *aperiodic* if there is $N \ge 0$ with $m^N = m^{N + 1}$ for all $m \in M$.

**Theorem (Schützenberger, 1965).** $L$ is star-free if and only if $M(L)$ is aperiodic.

Equivalent forms of the right side:

1. $M(L)$ has no subgroup with more than one element.
2. There is $N$ such that $x u^N y \in L \Leftrightarrow x u^{N + 1} y \in L$ for all strings $x, u, y$.
3. The minimal complete DFA $(Q, \Sigma, \delta, q_0, F)$ of $L$ is *counter-free*: no string $u$ permutes a set of two or more states in a cycle, that is, $\delta^*(p_i, u) = p_{i + 1 \bmod j}$ for different states $p_0, \ldots, p_{j - 1}$ with $j \ge 2$ never happens.

## In plain words

Some patterns of text can be described without saying "repeat this any number of times", using only "or", "followed by" and "not". For example, "the text alternates $a$ and $b$, starts with $a$ and ends with $b$" needs no repetition: it says that the text does not start with $b$, does not end with $a$, and never has two equal letters in a row.

Other patterns need repetition, like "the text has an even length". The theorem gives a test that tells the two kinds apart. Take the smallest machine for the pattern and look at what each piece of text does to its states. The pattern needs no repetition exactly when no piece of text sends some states around a cycle of length two or more. In other words, the machine can never be used to count modulo a number.

## Proof

The full proof is in [the proof](proofs/main.md). Its parts are as follows.

**The forms are equivalent.** Form 2 is the same statement as aperiodicity, since $\eta_L(u)^N = \eta_L(u^N)$ and every element of $M(L)$ is some $\eta_L(u)$. For form 1: if $m^N = m^{N + 1}$ for all $m$ and $H$ is a subgroup with identity $e$, then for $h \in H$, multiplying $h^N = h^{N + 1}$ by the inverse of $h^N$ in $H$ gives $e = h$. Conversely, if $M$ is not aperiodic, some $m$ has $m^k \ne m^{k + 1}$ for all $k$; its powers are eventually periodic with a period $p \ge 2$, and the elements $m^i, \ldots, m^{i + p - 1}$ of the periodic part, for $i$ a multiple of $p$ past the start of the period, form a cyclic group of order $p$. For form 3, $M(L)$ is the transition monoid of the minimal DFA, and a map $f : Q \to Q$ satisfies $f^N = f^{N + 1}$ for some $N$ if and only if it has no cycle of length 2 or more.

**Star-free implies aperiodic.** By induction on a star-free expression, every star-free language satisfies form 2 for some $N$. The empty set needs $N = 0$, a letter $N = 2$, complement keeps $N$, union takes the maximum, and a concatenation $KL$ needs $N_K + N_L + 1$: in a factorization of $x u^{N + 1} y = vz$, one of the two parts contains at least $N_K + 1$ or $N_L + 1$ whole copies of $u$, and one copy can be removed there without leaving $K$ or $L$; adding a copy works the same way.

**Aperiodic implies star-free.** Let $\varphi : \Sigma^* \to M$ be the syntactic morphism. It is enough to write each $\varphi^{-1}(m)$ as a star-free language, by induction on the size of the ideal $MmM$, from large to small. Two facts about aperiodic monoids drive the induction: if $s \in mM \cap Mm$ and $m \in MsM$ then $s = m$; and if $s \in MstM$ then $sM = stM$. For $m = 1$, $\varphi^{-1}(1) = B^*$ for the set $B$ of letters with $\varphi(a) = 1$. For $m \ne 1$, a string maps to $m$ if and only if a prefix of it reaches the right ideal $mM$ by a last letter, a suffix reaches the left ideal $Mm$ by a first letter, and no factor falls out of the two-sided ideal $MmM$:

$$\varphi^{-1}(m) = \bigl( U \Sigma^* \cap \Sigma^* V \bigr) \setminus \Sigma^* (C \cup W) \Sigma^*,$$

where $U$, $V$ and $W$ are finite unions of languages $\varphi^{-1}(n) a$, $a \varphi^{-1}(n)$ and $a \varphi^{-1}(n) b$ with $MnM \supsetneq MmM$, which are star-free by induction, and $C$ is a set of letters.

## Consequences

- **Star-freeness is decidable.** Compute the minimal DFA, then its transition monoid, and test $f^n = f^{n + 1}$ for each element, where $n = |Q|$. Equivalently, test whether the minimal DFA is counter-free. The monoid can have up to $n^n$ elements; the problem is PSPACE-complete for a language given by a DFA (Cho and Huynh, 1991).
- **A star-free expression can be computed.** The proof is constructive: it builds an expression for each $\varphi^{-1}(m)$ from the expressions for elements higher in the monoid.
- **Logic.** McNaughton and Papert (1971) proved that the star-free languages are exactly the languages definable in first-order logic over the positions of a string with $<$ and letter predicates. With this theorem, first-order definability of a regular language is decidable. Through Kamp's theorem the same class is the class of [linear temporal logic](/linear-temporal-logic/) on finite strings.
- **Closure properties that are not clear from expressions.** If $\psi : \Gamma^* \to \Sigma^*$ is a morphism and $L$ is star-free, then $\psi^{-1}(L)$ is star-free, since it is recognized by $\eta_L \circ \psi$, whose image is a submonoid of the aperiodic $M(L)$. Quotients $u^{-1} L$ and $L u^{-1}$ are star-free for the same reason.
- **Group languages.** If $M(L)$ is a group and $L$ is star-free, then $M(L)$ is trivial and $L$ is $\emptyset$ or $\Sigma^*$. So no non-trivial language recognized by a permutation automaton, such as "the number of $a$s is divisible by 3", is star-free.

## Tightness

- **The syntactic monoid cannot be replaced by any recognizing monoid.** A DFA that is not minimal can have a counter for a star-free language: over $\{a\}$, two accepting states that swap on $a$ accept $a^* = \overline{\emptyset}$, and the transition monoid is the group of order 2. What is true is that $L$ is star-free if and only if *some* aperiodic monoid recognizes $L$, since $M(L)$ is a quotient of a submonoid of every recognizing monoid, and these operations keep aperiodicity.
- **The constant $N$ is not bounded by the alphabet.** For $L = \{a^j\}$ over $\{a\}$, the least $N$ in form 2 is $j + 1$: $a^j \in L$ and $a^{j + 1} \notin L$. If the minimal DFA has $n$ states, the least $N$ is at most $n - 1$, since under a map without cycles of length 2 or more every state reaches a fixed point within $n - 1$ steps; here $n = j + 2$, so the bound is reached.
- **Groups are the only obstruction.** Every regular language that is not star-free has a group of order at least 2 in $M(L)$. The smallest example, $(aa)^*$ over $\{a\}$, has $M(L)$ equal to that group.

## History

Schützenberger proved the theorem in 1965, in a paper on finite monoids with only trivial subgroups. McNaughton and Papert (1971) connected star-free languages with counter-free automata and first-order logic. Eilenberg (1976) placed the theorem in his variety theory, where classes of finite monoids correspond to classes of regular languages; Simon's theorem on piecewise testable languages (1975) is another case. Cho and Huynh (1991) settled the complexity of the decision problem. The proof here, by induction on ideals, follows Pin (1986).

## References
