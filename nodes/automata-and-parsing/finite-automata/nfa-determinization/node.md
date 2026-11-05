---
tag: 31A4G4
kind: problem
slug: nfa-determinization
name: NFA determinization
aliases:
- NFA to DFA conversion
- determinization of finite automata
area: automata-and-parsing/finite-automata
level: core
summary: Given an NFA, construct an equivalent DFA.
model: word-ram
complexity:
  vars: {n: the number of NFA states, m: the number of NFA transitions, σ: the alphabet size}
  time: {worst: O(2^n σ(n + m))}
prereqs: [nondeterministic-finite-automaton, deterministic-finite-automaton]
see_also: [subset-construction, rabin-scott-theorem, determinization-blowup-lower-bound, brzozowski-minimization, dfa-minimization, nfa-simulation, state-complexity, unambiguous-nfa]
sources:
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the equivalence of nondeterministic and deterministic automata)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.5, Equivalence of Deterministic and Nondeterministic Finite Automata, and Section 2.3.6, A Bad Case for the Subset Construction
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7, From Regular Expressions to Automata (the conversion of an NFA to a DFA and the simulation of an NFA), and Section 3.9, Optimization of DFA-Based Pattern Matchers (the direct conversion of a regular expression to a DFA with followpos)
  - paper: doi:10.1109/T-C.1971.223108
    title: Frank R. Moore, On the bounds for state-set size in the proofs of equivalence between deterministic, nondeterministic, and two-way finite automata, IEEE Transactions on Computers C-20(10) (1971)
    locator: pp. 1211 to 1214
  - paper: "Marek Chrobak, Finite automata and unary languages, Theoretical Computer Science 47 (1986)"
    locator: pp. 149 to 158 (the conversion of unary NFAs to DFAs)
---

NFA determinization is the problem of building a [deterministic finite automaton](/deterministic-finite-automaton/) that accepts the same language as a given [nondeterministic finite automaton](/nondeterministic-finite-automaton/). The [Rabin-Scott theorem](/rabin-scott-theorem/) shows that a solution always exists with at most $2^n$ states for an NFA with $n$ states, and the [subset construction](/subset-construction/) builds it. The output can be exponentially larger than the input, and for some NFAs it must be, so no algorithm runs in polynomial time in the worst case. Lexer generators, regular expression engines and model checkers solve this problem, often only on the part of the DFA that they need.

## In plain words

An NFA may have several moves for one letter, so after some input it can be in several states at once. A DFA has exactly one move for each letter, so it is easy to run and easy to complement. The task is to turn the first kind of machine into the second kind without a change in the set of accepted strings.

The standard method gives each DFA state the meaning "the set of NFA states that are possible now". This always works. The cost is that there can be very many such sets: with $n$ NFA states there are $2^n$ of them, and some NFAs reach all of them, each one needed.

## Definition

**Input.** An NFA $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, one start state, and no $\varepsilon$-moves, as on the [NFA](/nondeterministic-finite-automaton/) page; or an [epsilon-NFA](/epsilon-nfa/) with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$. The NFA need not be complete. Its size is $n = |Q|$, $m = \sum_{q, a} |\delta(q, a)|$ and $\sigma = |\Sigma|$.

**Output.** A complete DFA $M = (Q', \Sigma, \delta', q_0', F')$ with $\delta' : Q' \times \Sigma \to Q'$, no $\varepsilon$-moves, and $L(M) = L(N)$.

The definition does not ask for a small DFA, only for a correct one. The output size is the main cost measure, because each correct method must at least write its output.

## Variants

- **Minimal output.** Output the [minimal DFA](/minimal-dfa-uniqueness/) of $L(N)$. Determinize, then apply [DFA minimization](/dfa-minimization/), or use [Brzozowski's method](/brzozowski-minimization/), which determinizes twice with a reversal before each step.
- **Partial output.** Allow a DFA with undefined transitions. This saves at most one state, the empty set of NFA states, which acts as the dead state.
- **Lazy output.** Build only the DFA states that a given input reaches, as in [NFA simulation](/nfa-simulation/) with a cache of subsets.
- **Size question.** Given $N$ and $k$, decide whether the minimal DFA of $L(N)$ has at most $k$ states. This is a decision version; determinize and minimize answer it in exponential time.
- **Other kinds of automata.** For a [Büchi automaton](/buchi-automaton/) on infinite words, the subset construction fails, and a deterministic automaton needs a stronger acceptance condition. For a [weighted automaton](/weighted-automaton/) over some semirings, no equivalent deterministic weighted automaton exists at all.

## Examples

**Second symbol from the end.** Let $N_2$ accept the strings over $\{a, b\}$ whose second symbol from the end is $a$: $Q = \{0, 1, 2\}$, $q_0 = 0$, $F = \{2\}$, $\delta(0, a) = \{0, 1\}$, $\delta(0, b) = \{0\}$, $\delta(1, a) = \delta(1, b) = \{2\}$, and $\delta(2, \cdot) = \emptyset$. The subset construction reaches four sets.

| DFA state | on $a$ | on $b$ | accepting |
|---|---|---|---|
| $\{0\}$ (start) | $\{0, 1\}$ | $\{0\}$ | no |
| $\{0, 1\}$ | $\{0, 1, 2\}$ | $\{0, 2\}$ | no |
| $\{0, 1, 2\}$ | $\{0, 1, 2\}$ | $\{0, 2\}$ | yes |
| $\{0, 2\}$ | $\{0, 1\}$ | $\{0\}$ | yes |

Each state records the last two symbols: $\{0, 1, 2\}$ means $aa$, $\{0, 2\}$ means $ab$, $\{0, 1\}$ means $ba$ or the single string $a$, and $\{0\}$ means $bb$ or a shorter string with no $a$ in the last two places. The four states are pairwise distinguishable, so this DFA is minimal.

**Growth with $n$.** For the same language with "the $n$-th symbol from the end", the NFA $N_n$ has $n + 1$ states and the minimal DFA has $2^n$ states, one for each window of the last $n$ symbols.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 10 | 20 |
|---|---|---|---|---|---|---|---|---|
| NFA states | 2 | 3 | 4 | 5 | 6 | 7 | 11 | 21 |
| minimal DFA states | 2 | 4 | 8 | 16 | 32 | 64 | 1,024 | 1,048,576 |

$N_n$ is an [unambiguous NFA](/unambiguous-nfa/): an accepted string has exactly one accepting run, the one that leaves state 0 at the $n$-th symbol from the end. So the exponential blowup is not a matter of ambiguity.

**A DFA as input.** If $N$ is already a DFA, seen as an NFA with $|\delta(q, a)| = 1$, the construction reaches only singleton sets, and its output is a copy of the reachable part of $N$.

## Known algorithms

- [Subset construction](/subset-construction/) (Rabin and Scott, 1959): search the sets $S \subseteq Q$ that are reachable from the closure of $\{q_0\}$, with $\delta'(S, a)$ the closure of $\bigcup_{q \in S} \delta(q, a)$. Time $O(N' \sigma (n + m))$ and space $O(N' (n + \sigma))$, where $N' \le 2^n$ is the number of reachable sets. This is output sensitive.
- **Determinize, then minimize.** Subset construction followed by [Hopcroft's algorithm](/hopcroft-minimization/) gives the minimal DFA in $O(N' \sigma \log N')$ extra time.
- [Brzozowski's algorithm](/brzozowski-minimization/): reverse, determinize, reverse, determinize. The result is the minimal DFA, and it can be small even when the subset construction of $N$ itself is large.
- **Lazy determinization.** Keep a cache of the subsets that a run has met, and build a new one only when the input needs it. Regular expression engines that use DFAs work this way, and fall back to [NFA simulation](/nfa-simulation/) when the cache grows too large.
- **Direct construction from a regular expression.** From the positions of the expression, as in the [Glushkov automaton](/glushkov-automaton/), the subsets are sets of positions, and the DFA can be built without an explicit NFA. Aho, Lam, Sethi and Ullman describe this as the construction with the followpos function.

## Bounds

**Upper bound.** At most $2^n$ DFA states, by the Rabin-Scott theorem, and $2^n - 1$ if the output may be partial and the empty set is dropped.

**The upper bound is reached.** For each $n \ge 1$ there are $n$-state NFAs over a two-letter alphabet whose minimal DFAs have $2^n$ states (Lupanov, 1963; Moore, 1971). A binary witness with a full proof is on the [Rabin-Scott theorem](/rabin-scott-theorem/) page, and more are on the [determinization blowup](/determinization-blowup-lower-bound/) page. So the worst case time of each algorithm is $\Omega(2^n)$, since it must write the output.

**Unary alphabets.** For NFAs over one letter, the minimal DFA has at most $e^{O(\sqrt{n \ln n})}$ states, and this order of growth is reached (Chrobak, 1986). So the blowup is smaller than $2^n$, but still more than polynomial.

**Time.** The subset construction runs in $O(2^n \sigma (n + m))$ time in the worst case on the [word RAM](/word-ram/), with hashing of the sets. Since the output can have $2^n$ states and $2^n \sigma$ transitions, this is optimal up to the factor $n + m$.

## Reductions

- **Complement of an NFA** reduces to determinization: determinize to a complete DFA, then swap $F'$ with $Q' \setminus F'$.
- **[NFA universality](/nfa-universality/), inclusion and [NFA equivalence](/nfa-equivalence/)** reduce to determinization plus a graph search on the DFA, or on a product of DFAs. These problems are PSPACE-complete, so a polynomial-size output is impossible in general unless P = PSPACE.
- **From regular expressions.** A regular expression of length $k$ becomes an NFA with $O(k)$ states by the [Thompson construction](/thompson-construction/), so determinization of NFAs also turns regular expressions into DFAs.
- **To NFA simulation.** Running the DFA on one string of length $\ell$ costs $O(\ell)$, after a construction of up to $2^n$ states. [NFA simulation](/nfa-simulation/) computes the same sequence of subsets on demand in $O(\ell (n + m))$ time.

## Applications

- **Lexical analysis.** Lexer generators build one NFA for all token patterns, determinize it and minimize the result, so that the scanner reads each input character with one table lookup.
- **Regular expression search.** Tools such as [grep](/grep/) build a DFA for the pattern, in full or lazily.
- **Model checking and verification.** To check that a system, given as an automaton, satisfies a property given as an NFA, the property is complemented, which needs determinization or an algorithm that avoids it.
- **Complementation and Boolean operations** on regular languages in libraries of automata.

## References
