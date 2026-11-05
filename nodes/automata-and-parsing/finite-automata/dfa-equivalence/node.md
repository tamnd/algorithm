---
tag: NWWAHD
kind: problem
slug: dfa-equivalence
name: DFA equivalence
aliases:
- language equivalence of DFAs
area: automata-and-parsing/finite-automata
level: core
summary: Decide whether two DFAs recognize the same language.
model: word-ram
complexity:
  vars: {n: the total number of states of the two DFAs, σ: the alphabet size}
  time: {worst: O(σ n α(n))}
prereqs: [deterministic-finite-automaton, product-construction, dfa-emptiness]
see_also: [hopcroft-karp-equivalence, dfa-minimization, minimal-dfa-uniqueness, nfa-equivalence, regex-equivalence, language-containment, disjoint-set, bisimulation]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.1, Decidable Languages (Theorem 4.5, equivalence of DFAs by emptiness of the symmetric difference)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4.2, Testing Equivalence of Regular Languages
  - paper: "John E. Hopcroft and Richard M. Karp, A linear algorithm for testing equivalence of finite automata, Technical Report 71-114, Department of Computer Science, Cornell University, 1971"
    locator: the whole report (the union-find algorithm for equivalence)
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (experiments that distinguish the states of a machine)
  - paper: doi:10.1145/2429069.2429124
    title: Filippo Bonchi and Damien Pous, Checking NFA equivalence with bisimulations up to congruence, 40th ACM Symposium on Principles of Programming Languages (POPL 2013)
    locator: pp. 457 to 468 (Hopcroft and Karp's algorithm as a bisimulation up to equivalence, and its extension to NFAs)
---

DFA equivalence asks whether two [deterministic finite automata](/deterministic-finite-automaton/) accept the same language. The two languages differ exactly when the [product](/product-construction/) of the DFAs can reach a pair of states in which one accepts and the other rejects, so the problem reduces to [DFA emptiness](/dfa-emptiness/) of the symmetric difference. A search of the product takes $O(\sigma n_1 n_2)$ time, and the [Hopcroft-Karp algorithm](/hopcroft-karp-equivalence/) with a [disjoint-set](/disjoint-set/) structure takes almost linear time, $O(\sigma n \alpha(n))$. When the answer is "no", both methods return a short string that one DFA accepts and the other rejects.

## In plain words

Two machines read words over the same letters and say yes or no. We want to know if they agree on every word, and there are infinitely many words.

Run the two machines side by side. At each moment the pair of their current states is all that matters for the future, and there are only finitely many pairs. So explore all pairs that the two machines can reach together from their start states. If some reachable pair has one machine saying yes and the other saying no, the letters that led there form a word on which they disagree. If no such pair exists, they agree on every word. A faster method also merges pairs that must agree, so it looks at far fewer pairs.

## Definition

**Input.** Two complete DFAs $M_i = (Q_i, \Sigma, \delta_i, q_i, F_i)$ for $i = 1, 2$ over the same alphabet, with $\delta_i : Q_i \times \Sigma \to Q_i$ and no $\varepsilon$-moves. Let $n_i = |Q_i|$, $n = n_1 + n_2$ and $\sigma = |\Sigma|$.

**Output.** "Equivalent" if $L(M_1) = L(M_2)$, and otherwise "not equivalent" with a *counterexample*, a string $w$ in the symmetric difference $L(M_1) \triangle L(M_2)$.

**The characterization.** Call a pair $(p, r) \in Q_1 \times Q_2$ *bad* if exactly one of $p \in F_1$ and $r \in F_2$ holds. Then $L(M_1) \neq L(M_2)$ if and only if a bad pair is reachable from $(q_1, q_2)$ in the product DFA, whose transitions are $(p, r) \xrightarrow{a} (\delta_1(p, a), \delta_2(r, a))$.

*Proof.* The product reaches $(\delta_1^*(q_1, w), \delta_2^*(q_2, w))$ on $w$, by induction on $|w|$ (Lemma 1 of the [closure properties](/closure-properties-of-regular-languages/)). This pair is bad if and only if $w$ is in exactly one of the two languages. $\square$

**Short counterexamples.** If $L(M_1) \neq L(M_2)$, a counterexample of length at most $n_1 + n_2 - 2$ exists. Put $M_1$ and $M_2$ side by side as one DFA with $N = n_1 + n_2$ states and accepting set $F_1 \cup F_2$. Its states $q_1$ and $q_2$ are not equivalent. As shown for [Moore's algorithm](/moore-minimization/), the partitions by "agree on all words of length at most $i$" refine strictly until they stabilize, starting from 2 blocks and ending with at most $N$ blocks. So they stabilize by $i = N - 2$, and two inequivalent states disagree on some word of length at most $N - 2$. The bound is reached: the cycle of $m$ states that accepts $a^k$ for $k \equiv m - 1 \pmod m$, and the chain $0 \to 1 \to \cdots \to m$ with a loop at $m$ that agrees with it up to $a^{m-1}$ and then rejects, have $2m - 1 = n_1 + n_2 - 2$ as the length of their shortest counterexample. A script checked this for $m = 2, \ldots, 8$, and an exhaustive search over all pairs of DFAs with at most 3 states each over 1 and 2 symbols found no longer shortest counterexample than $n_1 + n_2 - 2$.

## Variants

- **Inclusion.** Decide $L(M_1) \subseteq L(M_2)$: the bad pairs are $F_1 \times (Q_2 \setminus F_2)$. Union-find does not apply here, because inclusion is not symmetric. See [language containment](/language-containment/).
- **Equivalence of states.** Decide whether two states of one DFA are equivalent. This is the same problem with $M_1 = M_2$, and computing all equivalent pairs at once is [DFA minimization](/dfa-minimization/).
- **NFA equivalence.** For [NFAs](/nondeterministic-finite-automaton/) the problem is PSPACE-complete. See [NFA equivalence](/nfa-equivalence/). Determinizing on the fly and checking equivalence of the subset DFAs with Hopcroft-Karp, possibly with congruence closure (Bonchi and Pous, 2013), works well in practice.
- **Regular expressions.** See [regex equivalence](/regex-equivalence/): PSPACE-complete in general, decided by converting to automata or with [Brzozowski derivatives](/brzozowski-derivatives/).
- **Equivalence of Moore and Mealy machines.** The same search, with "bad" meaning different outputs. See [Moore machine](/moore-machine/).

## Examples

Over $\{a, b\}$, let $M_1$ count the $a$s modulo 2 (states 0, 1, $F_1 = \{0\}$), and let $M_2$ count the $a$s modulo 3 (states 0, 1, 2, $F_2 = \{0\}$). Both ignore $b$. A breadth-first search of the product from $(0, 0)$:

| pair | bad? | on $a$ | on $b$ |
|---|---|---|---|
| $(0, 0)$ | no | $(1, 1)$ | $(0, 0)$ |
| $(1, 1)$ | no | $(0, 2)$ | $(1, 1)$ |
| $(0, 2)$ | yes | | |

The pair $(0, 2)$ is reached by $aa$, which $M_1$ accepts and $M_2$ rejects. So the DFAs are not equivalent, with the shortest counterexample $aa$.

Now let $M_3$ count the $a$s modulo 4 with $F_3 = \{0, 2\}$. The product of $M_1$ and $M_3$ reaches only the pairs $(0, 0)$, $(1, 1)$, $(0, 2)$ and $(1, 3)$, none of them bad, so $L(M_1) = L(M_3)$. Both checks were run by a script.

## Known algorithms

| algorithm | time | counterexample |
|---|---|---|
| search of the product | $O(\sigma n_1 n_2)$ | shortest, with breadth-first search |
| [Hopcroft-Karp](/hopcroft-karp-equivalence/) | $O(\sigma n \alpha(n))$ | yes, not always shortest |
| minimize both, compare canonical forms | $O(\sigma n \log n)$ | not directly |
| minimize the disjoint union, test $[q_1] = [q_2]$ | $O(\sigma n \log n)$ | not directly |

The product search is the method of the textbooks: it decides emptiness of $L(M_1) \triangle L(M_2)$. The Hopcroft-Karp algorithm keeps a [disjoint-set](/disjoint-set/) partition of $Q_1 \cup Q_2$. It starts by merging $q_1$ and $q_2$, and for each merged pair $(p, r)$ and each symbol it merges $\delta_1(p, a)$ and $\delta_2(r, a)$. It answers "not equivalent" when it would merge an accepting with a rejecting state. Each merge reduces the number of sets by one, so it processes at most $n - 1$ pairs. Minimization works because the minimal DFA is unique ([uniqueness theorem](/minimal-dfa-uniqueness/)): with the states numbered in breadth-first order, two DFAs are equivalent exactly when their minimal DFAs are equal.

## Bounds

**Upper bound.** $O(\sigma n \alpha(n))$ time on the [word RAM](/word-ram/), where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).

**Lower bound.** $\Omega(\sigma n)$ table entries must be read on some inputs, because DFA emptiness reduces to equivalence with a one-state DFA that accepts nothing, and emptiness needs this many reads. No algorithm with $O(\sigma n)$ worst-case time is known for the general problem.

**Space.** DFA equivalence is NL-complete. Non-equivalence is in NL: guess a counterexample one symbol at a time while tracking the two current states. Equivalence is then in NL because NL is closed under complement ([Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/)). Hardness follows from emptiness, which is NL-complete.

## Reductions

- **To emptiness.** $L(M_1) = L(M_2)$ if and only if the product DFA with the bad pairs as accepting states is empty.
- **From emptiness.** $L(M) = \emptyset$ if and only if $M$ is equivalent to a one-state DFA with no accepting state.
- **To minimization.** Compare the canonical minimal DFAs.
- **From regex and NFA equivalence**, by the [subset construction](/subset-construction/), with an exponential blow-up in the worst case.

## Applications

- **Testing compilers of regular expressions**: check that an optimized automaton accepts the same language as a reference one, and print a counterexample when it does not.
- **Learning.** The equivalence queries of the [L* algorithm](/lstar-algorithm/) are answered in tests by an equivalence check against the target DFA, and the counterexample drives the next step.
- **Verification.** Equivalence of finite-state models, of protocol specifications, and of hardware state machines after optimization.
- **Teaching tools** that grade an automaton by checking it against a model solution and show a counterexample.

## References
