---
tag: M1RXRV
kind: problem
slug: nfa-universality
name: NFA universality
aliases:
- universality problem for NFAs
- NFA non-universality
area: automata-and-parsing/finite-automata
level: advanced
summary: Decide whether an NFA accepts every string over its alphabet; PSPACE-complete.
model: word-ram
complexity:
  vars: {n: the number of NFA states, m: the number of NFA transitions, σ: the alphabet size}
  time: {worst: O(2^n σ(n + m))}
prereqs: [nondeterministic-finite-automaton, subset-construction, pspace]
see_also: [nfa-equivalence, regex-universality, regex-equivalence-pspace-completeness, savitch-theorem, dfa-emptiness, unambiguous-nfa, nfa-determinization, state-complexity]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the reduction from Turing machines with bounded space, which shows that the universality of regular expressions and NFAs is PSPACE-hard)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (the problems for regular expressions over a one-letter alphabet are NP-complete or coNP-complete)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Space Complexity (Example 8.4, a nondeterministic linear space algorithm for the complement of the universality problem of NFAs)
  - paper: "Martin De Wulf, Laurent Doyen, Thomas A. Henzinger and Jean-Francois Raskin, Antichains: a new algorithm for checking universality of finite automata, Computer Aided Verification (CAV 2006), Lecture Notes in Computer Science 4144"
    locator: pp. 17 to 30 (the search over antichains of subsets)
  - paper: "Marek Chrobak, Finite automata and unary languages, Theoretical Computer Science 47 (1986)"
    locator: pp. 149 to 158 (the size of DFAs for unary NFAs)
---

NFA universality is the problem of deciding, for a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) $N$ over an alphabet $\Sigma$, whether $L(N) = \Sigma^*$. For a [DFA](/deterministic-finite-automaton/) it takes linear time, but for an NFA it is [PSPACE](/pspace/)-complete (Meyer and Stockmeyer, 1972), and coNP-complete over a one-letter alphabet. The standard algorithm searches the reachable sets of the [subset construction](/subset-construction/) for a set with no accepting state, and the shortest string that the NFA rejects can be exponentially long.

## In plain words

A machine reads strings and says yes or no. The question is whether it says yes to every string. For a deterministic machine this is easy: look at every state that some input can reach, and check that each of them says yes.

For a nondeterministic machine, a string is accepted when at least one of its possible paths ends well, so a single state tells you little. You must follow the set of states that are possible after each input, and these sets can be very many. The first string that the machine rejects can be extremely long, even for a small machine. No known method avoids this in all cases, and most researchers believe that none exists.

## Definition

**Input.** An NFA $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, one start state, and no $\varepsilon$-moves. $N$ need not be complete. Let $n = |Q|$, $m = \sum_{q, a} |\delta(q, a)|$ and $\sigma = |\Sigma|$, with $\sigma \ge 1$. An [epsilon-NFA](/epsilon-nfa/) is first turned into an NFA with the same states by the [epsilon-closure](/epsilon-closure/).

**Question.** Is $L(N) = \Sigma^*$?

A *counterexample* is a string $w \in \Sigma^* \setminus L(N)$. The complement problem, *non-universality*, asks whether a counterexample exists.

For $X \subseteq Q$ and $a \in \Sigma$, write $\mathrm{post}_a(X) = \bigcup_{q \in X} \delta(q, a)$. Then $w$ is a counterexample if and only if the set $\delta^*(\{q_0\}, w)$ has no state in $F$; call such a set *rejecting*.

## Variants

- **DFAs.** For a complete DFA, $L(M) = \Sigma^*$ if and only if every reachable state is accepting. A [breadth-first search](/breadth-first-search/) decides this in $O(n \sigma)$ time. For a partial DFA, a missing transition from a reachable state also gives a counterexample.
- **Regular expressions.** Is $L(r) = \Sigma^*$ for a [regular expression](/regular-expression/) $r$? This is [regex universality](/regex-universality/). It is PSPACE-complete too, since an expression of length $k$ becomes an NFA with $O(k)$ states, and the hardness proof below also works for expressions.
- **One-letter alphabet.** For $\Sigma = \{a\}$, the problem is coNP-complete (Stockmeyer and Meyer, 1973).
- **Unambiguous NFAs.** For an [unambiguous NFA](/unambiguous-nfa/) the problem is in polynomial time, by counting the accepted strings of each length.
- **Inclusion and equivalence.** Is $L(N_1) \subseteq L(N_2)$, or $L(N_1) = L(N_2)$? Universality is the special case where $N_1$ accepts $\Sigma^*$, so both are PSPACE-hard; see [NFA equivalence](/nfa-equivalence/).
- **Infinite words.** For [Büchi automata](/buchi-automaton/), universality is also PSPACE-complete, and it is a core step of model checking.

## Examples

**Cycles of prime lengths.** Let $p_1, \ldots, p_k$ be distinct primes and $P = p_1 p_2 \cdots p_k$. Build a unary NFA $C$ with a start state $s$ and, for each $i$, a cycle of $p_i$ states $(i, 0), \ldots, (i, p_i - 1)$ with $(i, j) \xrightarrow{a} (i, j + 1 \bmod p_i)$. Add $s \xrightarrow{a} (i, 1 \bmod p_i)$ for each $i$. The accepting states are $s$ and all $(i, j)$ with $j \ne p_i - 1$. After $a^\ell$ with $\ell \ge 1$ the NFA is in $\{(i, \ell \bmod p_i) : 1 \le i \le k\}$, so it rejects $a^\ell$ if and only if $\ell \equiv -1 \pmod{p_i}$ for all $i$. By the Chinese remainder theorem, the shortest counterexample is $a^{P - 1}$. For the primes 2 and 3, the NFA has 6 states and the search meets these sets:

| $\ell$ | set after $a^\ell$ | rejecting |
|---|---|---|
| 0 | $\{s\}$ | no |
| 1 | $\{(1, 1), (2, 1)\}$ | no |
| 2 | $\{(1, 0), (2, 2)\}$ | no |
| 3 | $\{(1, 1), (2, 0)\}$ | no |
| 4 | $\{(1, 0), (2, 1)\}$ | no |
| 5 | $\{(1, 1), (2, 2)\}$ | yes |

With more primes, the counterexample grows much faster than the NFA:

| primes | 2, 3 | 2, 3, 5 | 2, 3, 5, 7 | 2 to 11 | 2 to 13 |
|---|---|---|---|---|---|
| NFA states $1 + \sum p_i$ | 6 | 11 | 18 | 29 | 42 |
| shortest counterexample $P - 1$ | 5 | 29 | 209 | 2,309 | 30,029 |

With the first $k$ primes, $n = 1 + \sum p_i$ grows as $\Theta(k^2 \log k)$ and $P$ as $e^{(1 + o(1)) k \ln k}$, so the shortest counterexample has length $e^{\Theta(\sqrt{n \log n})}$.

**A universal NFA.** Let $N$ over $\{a, b\}$ have states 0 and 1, start 0, $F = \{0\}$, and $\delta(0, a) = \{0\}$, $\delta(0, b) = \{0, 1\}$, $\delta(1, a) = \delta(1, b) = \emptyset$. The search meets only the sets $\{0\}$ and $\{0, 1\}$, and both contain the accepting state 0, so $L(N) = \{a, b\}^*$. Removing $0 \in \delta(0, b)$ gives the counterexample $b$.

## Known algorithms

- **Subset search.** Run the [subset construction](/subset-construction/) from $\{q_0\}$ in breadth-first order and stop at the first rejecting set. The parent links give a shortest counterexample. Time $O(N' \sigma (n + m))$ for $N' \le 2^n$ reachable sets, in the worst case $O(2^n \sigma (n + m))$, and space $O(N' n)$.
- **Polynomial space.** Guess a counterexample one symbol at a time and keep only the current set, $n$ cells of memory, plus a counter up to $2^n$. This nondeterministic algorithm uses $O(n)$ space, so non-universality is in NSPACE($n$), and by [Savitch's theorem](/savitch-theorem/) universality is in DSPACE($n^2$).
- **Antichains.** If $X \subseteq Y$ then $\mathrm{post}_a(X) \subseteq \mathrm{post}_a(Y)$, and a subset of a rejecting set is rejecting. So if $Y$ reaches a rejecting set on a string $w$, then $X$ does too, on the same $w$. The search can drop each set that contains a set already found, and keep only an antichain of the $\subseteq$-minimal sets (De Wulf, Doyen, Henzinger and Raskin, 2006). The worst case stays exponential, but the antichain is often far smaller than the set of reachable sets.
- **Bisimulation up to congruence.** This method for [NFA equivalence](/nfa-equivalence/) also decides universality, as equivalence with a one-state NFA for $\Sigma^*$.
- **One-letter alphabet.** For $\Sigma = \{a\}$, compute the set reached by $a^\ell$ with the $\ell$-th power of the $n \times n$ Boolean transition matrix, by repeated squaring, in $O(n^3 \log \ell)$ time. A counterexample, if one exists, has $\ell$ below the number of states of the DFA, which is $e^{O(\sqrt{n \log n})}$ (Chrobak, 1986), so $\ell$ has $O(n)$ binary digits and can be guessed. This puts non-universality in NP.

## Bounds

**Upper bound.** NFA universality is in PSPACE, by the polynomial space algorithm above.

**Lower bound.** NFA universality is PSPACE-hard (Meyer and Stockmeyer, 1972). Here is the reduction. Let $A$ be a language in PSPACE, decided by a deterministic [Turing machine](/turing-machine/) $T$ in space $s(|x|)$ for a polynomial $s$; let $T$ stay in its halting configuration once it reaches it. For an input $x$, a configuration is a string of length $s = s(|x|)$ over $\Gamma' = \Gamma \cup (Q_T \times \Gamma)$, where one cell holds the state. An accepting history is a string $\# C_0 \# C_1 \# \cdots \# C_t \#$ where $C_0$ is the start configuration on $x$, $C_{i+1}$ follows from $C_i$ by one step, and $C_t$ holds the accepting state. The NFA $N_x$ accepts a string over $\Gamma' \cup \{\#\}$ if and only if at least one of these holds:

1. the string is not in $(\# (\Gamma')^s)^+ \#$, which an NFA with $O(s)$ states checks;
2. the string does not start with $\# C_0 \#$, which an NFA with $O(s)$ states checks;
3. the string contains no accepting state symbol, which a 2-state NFA checks;
4. some cell is wrong: the NFA guesses a position, reads the symbols at the positions $j - 1$, $j$ and $j + 1$ of one configuration, skips to position $j$ of the next configuration, $s + 1$ symbols on, and checks that this symbol is not the one that the transition function of $T$ gives for that window. This needs $O(s \cdot |\Gamma'|^3)$ states.

The union of the four NFAs has $O(s \cdot |\Gamma'|^3)$ states, and a log-space machine writes it. A string that none of the four accepts is an accepting history, since its first configuration is $C_0$ and every next configuration is the step of $T$ from the one before. Such a string exists if and only if $T$ accepts $x$. So $x \in A$ if and only if $N_x$ is not universal. This reduces each language in PSPACE to non-universality, and since PSPACE is closed under complement, universality is PSPACE-hard as well.

**Exponential time.** So, unless P = PSPACE, no algorithm decides universality in time polynomial in $n$. The subset search takes $O(2^n \sigma(n + m))$ in the worst case on the [word RAM](/word-ram/).

**Length of a shortest counterexample.** A shortest counterexample $w$ visits distinct sets $\delta^*(\{q_0\}, u)$ for its prefixes $u$, since a repeated set would give a shorter counterexample. So $|w| < 2^n$. For one letter, the prime-cycle example gives a length of $e^{\Theta(\sqrt{n \log n})}$, which matches the upper bound for this case from Chrobak's bound on the DFA size.

**One letter.** Unary NFA universality is coNP-complete (Stockmeyer and Meyer, 1973): it is in coNP by the guessed power above, and coNP-hard by a reduction from 3-SAT in which each variable is coded by residues modulo a distinct prime, in the style of the example.

## Reductions

- **Universality to equivalence and inclusion.** $L(N) = \Sigma^*$ if and only if $L(N)$ equals, or contains, the language of a one-state NFA with a loop on each symbol. So [NFA equivalence](/nfa-equivalence/) and NFA inclusion are PSPACE-hard.
- **Universality to emptiness.** $L(N) = \Sigma^*$ if and only if the complement of $L(N)$ is empty. Complementing an NFA needs [determinization](/nfa-determinization/), and [DFA emptiness](/dfa-emptiness/) of the result is a search, so this is the subset search above.
- **From regular expressions.** Regex universality reduces to NFA universality by the [Thompson construction](/thompson-construction/). The reverse also holds: the four checks in the hardness proof are written as regular expressions of polynomial length, so [regex universality](/regex-universality/) is PSPACE-complete, and so is regex equivalence ([regex equivalence](/regex-equivalence-pspace-completeness/)).

## Applications

- **Verification.** "Every behavior of the system satisfies the specification" is an inclusion $L(S) \subseteq L(P)$, and universality is its base case. Antichain tools decide such inclusions for NFAs and Büchi automata.
- **Checking patterns.** A tool can test whether a regular expression, or a set of lexer rules, matches every input, and report a shortest unmatched string.
- **Complexity theory.** Universality is a standard PSPACE-complete problem to reduce from, for example in proofs about games and planning on finite automata.

## References
