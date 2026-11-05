---
tag: QVTCWG
kind: theorem
slug: determinization-blowup-lower-bound
name: Determinization blow-up lower bound
aliases:
- exponential blow-up of determinization
- 2^n lower bound for subset construction
area: automata-and-parsing/finite-automata
level: advanced
summary: Some n-state NFAs require 2^n states in any equivalent DFA, so subset construction is worst-case optimal.
prereqs: [subset-construction, myhill-nerode-relation, nondeterministic-finite-automaton]
see_also: [rabin-scott-theorem, state-complexity, nfa-determinization, minimal-dfa-uniqueness, regex-dfa-state-blowup, nfa-minimization, closure-properties-of-regular-languages, lazy-dfa-construction]
sources:
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the subset construction and its upper bound of 2^n states)
  - paper: doi:10.1109/t-c.1971.223108
    title: F. R. Moore, On the bounds for state-set size in the proofs of equivalence between deterministic, nondeterministic, and two-way finite automata, IEEE Transactions on Computers C-20(10) (1971)
    locator: pp. 1211 to 1214
  - paper: doi:10.1109/swat.1971.11
    title: Albert R. Meyer and Michael J. Fischer, Economy of description by automata, grammars, and formal systems, 12th Annual Symposium on Switching and Automata Theory (1971)
    locator: pp. 188 to 191
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.6, A Bad Case for the Subset Construction
  - paper: doi:10.1016/0304-3975(86)90142-8
    title: Marek Chrobak, Finite automata and unary languages, Theoretical Computer Science 47 (1986)
    locator: pp. 149 to 158 (the blow-up for a one-letter alphabet)
---

The [subset construction](/subset-construction/) turns an [NFA](/nondeterministic-finite-automaton/) with $n$ states into a DFA with at most $2^n$ states. This theorem shows that the bound cannot be improved: for each $n$ there is an NFA with $n$ states over a two-letter alphabet whose smallest equivalent DFA has exactly $2^n$ states. So no method of determinization can avoid an exponential blow-up in the worst case. A simpler family, "the $n$-th symbol from the end is $a$", has NFAs with $n + 1$ states and minimal DFAs with $2^n$ states.

## Statement

The notation is that of the automata pages. An NFA is $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to 2^Q$ and no $\varepsilon$-moves, and DFAs are complete. For $S \subseteq Q$ and $w \in \Sigma^*$, $\hat\delta(S, w)$ is the set of states that $N$ can be in after reading $w$ from some state of $S$.

**Theorem.** For every $n \ge 1$ let $N_n$ be the NFA with $Q = \{0, 1, \ldots, n-1\}$, $\Sigma = \{a, b\}$, $q_0 = 0$, $F = \{0\}$ and

$$\delta(i, a) = \{ (i + 1) \bmod n \}, \qquad \delta(0, b) = \emptyset, \qquad \delta(i, b) = \{ 0, i \} \text{ for } 1 \le i \le n - 1.$$

Then the minimal complete DFA for $L(N_n)$ has exactly $2^n$ states.

**Corollary.** For $n \ge 1$ let $L_n = \{ w \in \{a, b\}^* : |w| \ge n \text{ and the } n\text{-th symbol from the end of } w \text{ is } a \}$. Then $L_n$ has an NFA with $n + 1$ states, and its minimal complete DFA has exactly $2^n$ states.

## In plain words

A machine that may guess can follow many paths at once. A machine that may not guess must remember, in its single state, the whole set of places where the guessing machine could be. A machine with $n$ places has $2^n$ such sets, so the non-guessing machine never needs more than $2^n$ states.

The theorem says that this many can really be needed. In the example, every set of places can come up, and for any two different sets some continuation of the input is accepted from one and rejected from the other. So the non-guessing machine must keep all the sets apart, and it needs one state for each of them. The simpler example asks whether the letter $n$ places from the end is an $a$. The guessing machine waits and guesses. The other machine must remember the last $n$ letters.

## Proof

The upper bound $2^n$ holds because the subset construction gives a DFA whose states are subsets of $Q$, and it accepts $L(N_n)$. For the lower bound, we show that the subset DFA has all $2^n$ subsets as reachable states and that no two of them are equivalent. Then the subset DFA is minimal by Part 3 of the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/), so the minimal DFA has $2^n$ states.

Write $S + j = \{ (s + j) \bmod n : s \in S \}$. From the definition of $\delta$:

- $\hat\delta(S, a) = S + 1$, since $a$ moves each state one step around the cycle.
- If $S$ contains a state other than 0, then $\hat\delta(S, b) = S \cup \{0\}$: each $i \ge 1$ in $S$ goes to $i$ and to $0$, and 0 goes nowhere. Also $\hat\delta(\{0\}, b) = \emptyset$.

**Every subset is reachable.** By induction on $k = |S|$.

- $k = 0$: $\emptyset = \hat\delta(\{0\}, b)$.
- $k = 1$: $\{j\} = \hat\delta(\{0\}, a^j)$ for $0 \le j \le n - 1$.
- $k \ge 2$: let $S$ have $k$ elements and pick $t \in S$. The set $S' = S + (n - t)$ contains 0 and has $k$ elements. The set $S'' = S' \setminus \{0\}$ has $k - 1 \ge 1$ elements, none of them 0, so it is reachable by the induction hypothesis, say $S'' = \hat\delta(\{0\}, u)$. Then $\hat\delta(S'', b) = S'' \cup \{0\} = S'$, and $\hat\delta(S', a^t) = S' + t = S$. So $S = \hat\delta(\{0\}, u b a^t)$.

**No two subsets are equivalent.** In the subset DFA, a set $S$ accepts $z$ when $\hat\delta(S, z) \cap F \neq \emptyset$. For $q \in Q$ let $m = (n - q) \bmod n$. Then $\hat\delta(S, a^m) = S + m$, and $0 \in S + m$ if and only if $q \in S$. So $a^m$ is accepted from $S$ if and only if $q \in S$. If $S \neq S'$, some $q$ lies in one of them and not in the other, and $a^{(n - q) \bmod n}$ separates them.

Hence the subset DFA has $2^n$ reachable, pairwise inequivalent states, and the minimal DFA has $2^n$ states. $\square$

**Proof of the corollary.** The NFA has the states $0, 1, \ldots, n$, start 0, final state $n$, a loop at 0 on $a$ and $b$, a move $0 \xrightarrow{a} 1$, and moves $i \xrightarrow{a, b} i + 1$ for $1 \le i \le n - 1$. It guesses the position of the $a$ and then checks that exactly $n - 1$ symbols follow. A DFA whose states are the last $n$ symbols read, padded on the left with $b$s, accepts $L_n$ with $2^n$ states, since padding with $b$ does not change whether a string of length less than $n$ is accepted. For the lower bound, take two different strings $x, y$ of length $n$. They differ at some position $i$, say $x_i = a$ and $y_i = b$. Then $x b^{i-1} \in L_n$ and $y b^{i-1} \notin L_n$, since in both strings the symbol at position $i$ is the $n$-th from the end. So the $2^n$ strings of length $n$ are pairwise distinguishable, and every DFA for $L_n$ has at least $2^n$ states by the [Myhill-Nerode relation](/myhill-nerode-relation/). $\square$

A script built the subset DFA of $N_n$ and minimized it for $n = 1, \ldots, 10$, and found $2^n$ states each time. It found $2^n$ states for $L_n$ as well.

## Consequences

- **The subset construction is optimal.** No algorithm can turn every NFA with $n$ states into a DFA with fewer than $2^n$ states, so the worst-case time of [NFA determinization](/nfa-determinization/) is $\Omega(2^n)$ even when the output is minimal.
- **Regular expressions.** The language $L_n$ has the regular expression $(a + b)^* a (a + b)^{n-1}$ of size $O(n)$, so converting regular expressions to DFAs also has an exponential worst case. See [regex DFA state blow-up](/regex-dfa-state-blowup/). This is why regex engines simulate the NFA, or build the DFA [lazily](/lazy-dfa-construction/) as the input asks for states.
- **Reversal.** The reverse of $L_n$, "the $n$-th symbol is $a$", has a DFA with $n + 2$ states: a counter, an accepting sink and a dead sink. Reversing it gives $L_n$, whose minimal DFA has $2^n$ states. So the [state complexity](/state-complexity/) of reversal is exponential, and this is also why [Brzozowski's algorithm](/brzozowski-minimization/) can take exponential time.
- **Complement and other operations on NFAs.** Complementing an NFA by determinizing it costs up to $2^n$ states on these examples. The operations whose standard proofs pass through determinization inherit this cost.
- **Succinctness.** NFAs can be exponentially more succinct than DFAs. [Alternating finite automata](/alternating-finite-automaton/) are exponentially more succinct than NFAs, and doubly exponentially more succinct than DFAs.

## Tightness

- **The bound $2^n$ is exact.** The subset construction gives at most $2^n$ states, and the theorem reaches it. With the empty set as the dead state, the count $2^n$ is for complete DFAs; the minimal partial DFA of $L(N_n)$ has $2^n - 1$ states.
- **Two letters are enough, one is not.** Over a one-letter alphabet, an NFA with $n$ states has an equivalent DFA with $e^{(1 + o(1)) \sqrt{n \ln n}}$ states, and this is the worst case (Chrobak, 1986). So the full $2^n$ needs at least two letters.
- **The corollary is off by one state.** The family $L_n$ uses $n + 1$ NFA states for $2^n$ DFA states. The family $N_n$ removes this gap.
- **Unambiguous NFAs.** The lower bound does not need ambiguity: the NFA for $L_n$ has at most one accepting run on each string, so even [unambiguous NFAs](/unambiguous-nfa/) can be exponentially smaller than DFAs.

## History

Rabin and Scott (1959) introduced the subset construction and the bound of $2^n$ states. Lupanov (1963) gave the first NFAs that reach it. F. R. Moore (1971) and Meyer and Fischer (1971) gave further families, the latter as part of a study of the succinctness of automata, grammars and formal systems. The family of the "$n$-th symbol from the end" is the standard textbook example, for instance in the book of Hopcroft, Motwani and Ullman. Chrobak (1986) settled the unary case.

## References
