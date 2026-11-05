---
tag: WW3YEB
kind: concept
slug: unambiguous-nfa
name: Unambiguous NFA
aliases:
- unambiguous finite automaton
- UFA
area: automata-and-parsing/finite-automata
level: advanced
summary: NFA in which every accepted string has exactly one accepting run.
prereqs: [nondeterministic-finite-automaton, deterministic-finite-automaton]
see_also: [ambiguity, nfa-equivalence, nfa-universality, nfa-minimization, weighted-automaton, regex-ambiguity-detection, unambiguous-polynomial-time, one-unambiguous-regular-expression]
sources:
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611 (equivalence and containment of unambiguous automata in polynomial time, by counting)
  - paper: "Andreas Weber and Helmut Seidl, On the degree of ambiguity of finite automata, Theoretical Computer Science 88(2) (1991)"
    locator: pp. 325 to 349 (finite, polynomial and exponential ambiguity, and the criteria for each)
  - paper: "Mikhail A. Raskin, A superpolynomial lower bound for the size of non-deterministic complement of an unambiguous automaton, 45th International Colloquium on Automata, Languages, and Programming (ICALP 2018), LIPIcs 107"
    locator: the main theorem (the complement of an unambiguous automaton can need superpolynomially many NFA states)
  - paper: "Tao Jiang and B. Ravikumar, Minimal NFA problems are hard, SIAM Journal on Computing 22(6) (1993)"
    locator: pp. 1117 to 1141 (minimization of unambiguous automata given a DFA is NP-complete)
---

An unambiguous NFA (UFA) is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) in which every accepted string has exactly one accepting run. Every [DFA](/deterministic-finite-automaton/) is unambiguous, and a UFA can be exponentially smaller than any DFA for its language. Unambiguity keeps much of what makes DFAs easy: the number of accepted strings of each length is the number of accepting paths, so [equivalence](/nfa-equivalence/) and [universality](/nfa-universality/) of UFAs are in polynomial time (Stearns and Hunt, 1985), while for general NFAs they are PSPACE-complete.

## In plain words

A nondeterministic machine may have many ways to read a string. It accepts when at least one way ends well. An unambiguous machine is one where an accepted string never has two different successful ways: it may try many paths, but at most one of them succeeds.

This helps when you want to count. In a general machine, counting the successful paths overcounts the strings, because one string can have many of them. In an unambiguous machine, the two counts are equal, and counting paths is easy with a table of numbers. With such counts you can check whether two machines accept the same strings, which is very hard for general machines.

## The idea

**Definition.** Let $N = (Q, \Sigma, \delta, q_0, F)$ be an NFA with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, one start state and no $\varepsilon$-moves; $N$ need not be complete. A *run* of $N$ on $w = a_1 \cdots a_\ell$ is a sequence of states $r_0, r_1, \ldots, r_\ell$ with $r_0 = q_0$ and $r_i \in \delta(r_{i-1}, a_i)$; it is accepting if $r_\ell \in F$. Let $\mathrm{runs}_N(w)$ be the number of accepting runs. $N$ is *unambiguous* if $\mathrm{runs}_N(w) \le 1$ for all $w \in \Sigma^*$. The *degree of ambiguity* of $N$ is $\sup_w \mathrm{runs}_N(w)$.

**Testing unambiguity.** Build the self-product $N \times N$, with states $(p, q)$, start state $(q_0, q_0)$, and $(p, q) \xrightarrow{a} (p', q')$ when $p' \in \delta(p, a)$ and $q' \in \delta(q, a)$. Then $N$ is ambiguous if and only if some pair $(p, q)$ with $p \ne q$ is reachable from $(q_0, q_0)$ and can reach $F \times F$. *Proof.* If two accepting runs on $w$ differ, they form one path of $N \times N$ from $(q_0, q_0)$ to $F \times F$ on $w$, and at a position where they differ the path is in a pair $(p, q)$ with $p \ne q$. Conversely, a path from $(q_0, q_0)$ through such a pair to $F \times F$ on a string $w$ gives two accepting runs on $w$ that differ at that position. Two graph searches on $N \times N$ decide this in $O(n^2 + m^2)$ time, where $n = |Q|$ and $m = \sum_{q, a} |\delta(q, a)|$. Both conditions are needed: a pair $p \ne q$ that is reachable but cannot reach $F \times F$ does not make $N$ ambiguous.

**Counting.** Let $M = \sum_{a \in \Sigma} M_a$, where $M_a$ is the $n \times n$ integer matrix with $(M_a)_{pq} = 1$ if $q \in \delta(p, a)$. Let $u$ be the indicator vector of $q_0$ and $v$ that of $F$. Then $u^{\mathsf T} M^\ell v$ is the number of accepting runs on strings of length $\ell$. If $N$ is unambiguous, it equals the number $c_N(\ell)$ of strings of length $\ell$ in $L(N)$. So $c_N(\ell)$ is computed with $O(\ell)$ matrix-vector products, or with $O(\log \ell)$ [matrix powers](/matrix-power/).

**Linear recurrences.** By the Cayley-Hamilton theorem, $M$ satisfies its characteristic polynomial $x^n + c_{n-1} x^{n-1} + \cdots + c_0$, so $M^{\ell + n} = -\sum_{i < n} c_i M^{\ell + i}$, and the sequence $c_N(\ell)$ satisfies a [linear recurrence](/linear-recurrences-with-constant-coefficients/) of order $n$. A sum or difference of two sequences that satisfy recurrences of orders $r$ and $s$ satisfies one of order $r + s$ (use the block diagonal matrix). A sequence that satisfies a recurrence of order $r$ and is zero for $\ell = 0, \ldots, r - 1$ is zero everywhere, by induction on $\ell$.

**Polynomial time universality and equivalence.** A UFA $N$ is universal if and only if $c_N(\ell) = \sigma^\ell$ for all $\ell$, where $\sigma = |\Sigma|$. The sequence $\sigma^\ell$ satisfies a recurrence of order 1, so it is enough to compare $\ell = 0, \ldots, n$. For two UFAs $N_1$ and $N_2$ with $n_1$ and $n_2$ states, the product NFA for $L(N_1) \cap L(N_2)$ is again unambiguous, and $L(N_1) \subseteq L(N_2)$ if and only if $c_{N_1}(\ell) = c_{N_1 \times N_2}(\ell)$ for all $\ell$, which needs only $\ell < n_1 + n_1 n_2$. Two inclusions give equivalence. All numbers have $O(\ell \log(n\sigma))$ digits, so the tests run in polynomial time (Stearns and Hunt, 1985).

**Degrees of ambiguity.** For an NFA in which every state is reachable and co-reachable, the number of accepting runs is either bounded by a constant, or bounded by a polynomial in the length of the string but not by a constant, or exponential: for infinitely many $\ell$, some string of length $\ell$ has $2^{\Omega(\ell)}$ accepting runs. Weber and Seidl (1991) gave the criteria. $N$ has exponential ambiguity if and only if some state $p$ and string $v$ admit two different paths from $p$ to $p$ on $v$. $N$ has polynomial but unbounded ambiguity if and only if this fails and there are states $p \ne q$ and a string $v$ with paths $p \to p$, $p \to q$ and $q \to q$, all on $v$.

**Succinctness.** UFAs lie between DFAs and NFAs. The gap to DFAs can be $2^n$ against $n + 1$ (the example below), and the gap to NFAs can also be exponential. The complement of a UFA with $n$ states can need superpolynomially many NFA states (Raskin, 2018), although the complement of a DFA has a DFA of the same size. Finding a minimal UFA for a language given by a DFA is NP-complete (Jiang and Ravikumar, 1993).

## Examples

**The $n$-th symbol from the end.** The NFA for "the $n$-th symbol from the end is $a$", with states $0, 1, \ldots, n$, a loop on 0, $0 \xrightarrow{a} 1$, and $i \xrightarrow{a, b} i + 1$ for $1 \le i < n$, is unambiguous: in an accepting run the move from 0 to 1 must happen exactly $n$ symbols before the end. It has $n + 1$ states, and the minimal DFA has $2^n$. For $n = 2$ the counts are $c(\ell) = 2^{\ell - 1}$ for $\ell \ge 2$, since the second symbol from the end is fixed and the others are free, and the numbers of accepting paths are the same: 2, 4, 8, 16 for $\ell = 2, 3, 4, 5$.

**An ambiguous NFA for "contains an $a$".** States 0 (start) and 1 (accepting), with loops $0 \xrightarrow{a, b} 0$ and $1 \xrightarrow{a, b} 1$, and $0 \xrightarrow{a} 1$. An accepted string has one accepting run for each $a$ in it, since the run may jump at any $a$. For $\ell = 1$ to 6, the strings of length $\ell$ in the language number $2^\ell - 1$: 1, 3, 7, 15, 31, 63, but the accepting paths number $\ell \cdot 2^{\ell - 1}$: 1, 4, 12, 32, 80, 192. The ambiguity is polynomial (linear): take $p = 0$, $q = 1$ and $v = a$ in the criterion above. Removing the loop $0 \xrightarrow{a} 0$ makes the NFA unambiguous, since then the run must jump at the first $a$.

**Exponential ambiguity.** Over $\{a\}$, let $0 \xrightarrow{a} 0$, $0 \xrightarrow{a} 1$, $1 \xrightarrow{a} 0$, with 0 the start and the only accepting state. The string $aa$ has the two paths $0, 0, 0$ and $0, 1, 0$ from 0 to 0, and $a^\ell$ has $F_{\ell + 1}$ accepting runs, the Fibonacci numbers 1, 1, 2, 3, 5, 8 for $\ell = 0, \ldots, 5$.

**A non-example.** A DFA is always unambiguous, since it has one run on each string. The converse fails: the first example is unambiguous but not deterministic.

## Where it is used

- **Counting and sampling.** The number of strings of length $\ell$ in a regular language, and a uniform random string of that length, are computed from a UFA by dynamic programming on paths.
- **Equivalence and inclusion checks** in polynomial time when the automata are known to be unambiguous, for example automata from unambiguous grammars.
- **Regular expressions.** Ambiguous expressions cause many matches of the same string and slow backtracking; [regex ambiguity detection](/regex-ambiguity-detection/) can run the self-product test on the [Glushkov automaton](/glushkov-automaton/) of the expression.
- **Weighted automata.** On an unambiguous [weighted automaton](/weighted-automaton/), the weight of a string is the weight of its one accepting run, so it does not depend on the sum operation of the semiring.
- **Complexity theory.** UFAs are the finite-state analogue of the class [UP](/unambiguous-polynomial-time/) of problems with unique witnesses.

## References
