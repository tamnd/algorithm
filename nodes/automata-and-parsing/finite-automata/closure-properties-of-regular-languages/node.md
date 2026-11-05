---
tag: 9JCFF5
kind: theorem
slug: closure-properties-of-regular-languages
name: Closure properties of regular languages
aliases:
- Boolean closure of regular languages
area: automata-and-parsing/finite-automata
level: core
summary: Regular languages are closed under union, intersection, complement, concatenation, star, reversal and homomorphism.
prereqs: [kleene-theorem, deterministic-finite-automaton, epsilon-nfa]
see_also: [product-construction, regular-language, regular-language-intersection, state-complexity, pumping-lemma-for-regular-languages, string-morphism, dfa-equivalence, kleene-star]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.2, Closure Properties of Regular Languages (Boolean operations, reversal, homomorphisms and inverse homomorphisms)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.1 (Theorem 1.25, union by a product of DFAs) and Section 1.2 (Theorems 1.45, 1.47 and 1.49, union, concatenation and star by NFAs)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lectures 4 and 10 (the product construction and closure under homomorphic images and preimages)
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (closure of the sets defined by automata under the Boolean operations, concatenation, star and reflection)
  - paper: "Sheng Yu, Qingyu Zhuang and Kai Salomaa, The state complexities of some basic operations on regular languages, Theoretical Computer Science 125(2) (1994)"
    locator: pp. 315 to 328 (the exact number of DFA states that each operation needs)
---

The [regular languages](/regular-language/) are closed under many operations: when the inputs are regular, so is the result. This holds for union, intersection, complement and difference, for concatenation and the [Kleene star](/kleene-star/), for reversal, and for homomorphisms and their inverses. Each proof is a construction on automata, so the theorem also gives algorithms, and their state counts are the subject of [state complexity](/state-complexity/). Closure properties are the main tool for showing that a language is regular, and, together with the [pumping lemma](/pumping-lemma-for-regular-languages/), for showing that it is not.

## Statement

Let $\Sigma$ and $\Delta$ be finite alphabets. For languages $A, B \subseteq \Sigma^*$ write $AB = \{xy : x \in A, y \in B\}$, $A^* = \bigcup_{k \ge 0} A^k$, $A^R = \{ w^R : w \in A \}$ for the reversal, and $A / B = \{ x : xy \in A \text{ for some } y \in B \}$ for the right quotient. A homomorphism $h : \Sigma^* \to \Delta^*$ satisfies $h(xy) = h(x)h(y)$, and so is fixed by the strings $h(a)$, $a \in \Sigma$, which may be empty.

**Theorem.** Let $L_1, L_2 \subseteq \Sigma^*$ and $L \subseteq \Delta^*$ be regular, and let $h : \Sigma^* \to \Delta^*$ be a homomorphism. Then the following languages are regular:

1. the complement $\Sigma^* \setminus L_1$;
2. the union $L_1 \cup L_2$, the intersection $L_1 \cap L_2$, the difference $L_1 \setminus L_2$ and the symmetric difference $L_1 \triangle L_2$;
3. the concatenation $L_1 L_2$;
4. the star $L_1^*$;
5. the reversal $L_1^R$;
6. the image $h(L_1) \subseteq \Delta^*$;
7. the inverse image $h^{-1}(L) = \{ w \in \Sigma^* : h(w) \in L \} \subseteq \Sigma^*$;
8. the right quotient $L_1 / K$, for every language $K \subseteq \Sigma^*$.

All the constructions are effective, except that item 8 needs a way to test $K$; for a regular $K$ it is effective too. In the constructions, automata are complete DFAs $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves, or [epsilon-NFAs](/epsilon-nfa/) with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$, which need not be complete.

## In plain words

Suppose a machine with finitely many states can check whether a word has some property, and another machine can check a second property. Then a machine with finitely many states can also check "both", "either", "not the first", "a word with the first property followed by a word with the second", "any number of words with the first property in a row", and "the first property, read backwards".

The same holds when each letter is replaced by a fixed word. The checks are all built from the given machines. For "both" or "either", run the two machines side by side. For "not", swap the yes and no answers. For the joins and the repeats, let a machine guess where one word ends and the next one starts.

## Proof

The full proof is in [the proof of the closure properties](proofs/main.md). Its parts:

- **Complement.** Keep the complete DFA and replace $F$ by $Q \setminus F$. Each string has exactly one run, which ends outside $F$ exactly when the string is not in $L$.
- **Boolean operations.** The [product construction](/product-construction/) runs $M_1$ and $M_2$ in parallel on the states $Q_1 \times Q_2$, with $\delta((p, r), a) = (\delta_1(p, a), \delta_2(r, a))$. By induction on $|w|$, the product reaches $(\delta_1^*(q_1, w), \delta_2^*(q_2, w))$. The accepting pairs $F_1 \times F_2$ give the intersection, $(F_1 \times Q_2) \cup (Q_1 \times F_2)$ the union, and $F_1 \times (Q_2 \setminus F_2)$ the difference.
- **Concatenation.** Put $M_1$ and $M_2$ side by side and add an $\varepsilon$-move from each state of $F_1$ to $q_2$. An accepting path must cross from $M_1$ to $M_2$ exactly once, along one of these moves, so it splits into a run of $M_1$ that accepts and a run of $M_2$ that accepts.
- **Star.** Add a new start state $s$, which is the only accepting state, an $\varepsilon$-move $s \to q_1$, and an $\varepsilon$-move from each state of $F_1$ back to $s$. A path from $s$ to $s$ splits at its visits to $s$ into accepting runs of $M_1$.
- **Reversal.** Reverse every transition, start in $F_1$ through a new state with $\varepsilon$-moves, and accept in $q_1$. A path of $M_1$ read backwards is a path of the reversed machine with the reversed label.
- **Homomorphism.** Write $L_1 = L(E)$ by [Kleene's theorem](/kleene-theorem/) and replace each symbol $a$ in $E$ by the string $h(a)$. Since $h$ commutes with union, concatenation and star, a structural induction shows that the new expression denotes $h(L_1)$.
- **Inverse homomorphism.** Given a DFA for $L$, let $\delta'(q, a) = \delta^*(q, h(a))$. By induction on $|w|$, $\delta'^*(q, w) = \delta^*(q, h(w))$, so the new DFA accepts $w$ exactly when $h(w) \in L$.
- **Quotient.** Keep the DFA for $L_1$ and make $q$ accepting when some $y \in K$ leads from $q$ into $F_1$.

**Example.** Let $\Sigma = \{a, b\}$. The DFA $M_1$ with the states $E, O$ accepts the strings with an even number of $a$s, and the DFA $M_2$ with the states $0, 1$ accepts the strings that end in $b$ (state 1 means "the last symbol was $b$"). The product has 4 states. With $F = \{(E, 1)\}$ it accepts $L_1 \cap L_2$, whose strings of length at most 3 are $b$, $bb$, $aab$ and $bbb$. The product is not minimal: the pairs $(O, 0)$ and $(O, 1)$ both reject and go to the same pairs on $a$ and on $b$, so they are equivalent, and the minimal DFA for $L_1 \cap L_2$ has 3 states. The same holds for the union and the difference.

For an inverse image, let $L = (ab)^*$ over $\Delta = \{a, b\}$, with the DFA $0 \xrightarrow{a} 1 \xrightarrow{b} 0$, all other moves to a dead state 2, and $F = \{0\}$. Let $\Sigma = \{x, y\}$ with $h(x) = ab$ and $h(y) = ba$. Then $\delta'(0, x) = \delta^*(0, ab) = 0$ and $\delta'(0, y) = \delta^*(0, ba) = 2$, so $h^{-1}(L) = x^*$. A script checked these languages on all strings of length at most 10.

## Consequences

- **Proving regularity.** A language built from regular languages by these operations is regular. For example, the set of binary strings with an even number of 1s that do not contain $00$ is the difference of two regular languages.
- **Proving non-regularity.** If $L$ were regular, so would be $L \cap R$ for a regular $R$, or $h^{-1}(L)$. For example, the set of strings over $\{a, b\}$ with equally many $a$s and $b$s meets $a^* b^*$ in $\{ a^n b^n : n \ge 0 \}$, which is not regular by the [pumping lemma](/pumping-lemma-for-regular-languages/). So the first set is not regular either.
- **Decision procedures.** With complement and intersection, [DFA equivalence](/dfa-equivalence/) and inclusion reduce to [DFA emptiness](/dfa-emptiness/): $L_1 = L_2$ if and only if $L_1 \triangle L_2 = \emptyset$.
- **Algebra.** The regular languages over $\Sigma$ form a Boolean algebra of sets, and with concatenation and star they form a model of [Kleene algebra](/kleene-algebra/). Closure under homomorphisms and inverse homomorphisms makes them a *full trio*, a notion of the theory of language families. The [context-free languages](/context-free-language/) are closed under union, concatenation, star and homomorphisms, but not under intersection or complement.

## Tightness

**State complexity.** Let $L_1$ and $L_2$ have minimal complete DFAs with $m$ and $n$ states. The worst-case number of states of the minimal complete DFA for the result is known exactly for each basic operation:

| operation | worst-case DFA states | construction above |
|---|---|---|
| complement | $n$ | same DFA |
| union, intersection | $mn$ | product |
| concatenation | $m 2^n - 2^{n-1}$ | NFA, then subsets |
| star | $2^{n-1} + 2^{n-2}$ (for $n \ge 2$) | NFA, then subsets |
| reversal | $2^n$ | NFA, then subsets |

The bounds for concatenation and star are from Yu, Zhuang and Salomaa (1994), and each row has witness languages that reach the bound. For intersection the witness is easy: if $L_1$ counts the $a$s modulo $m$ and $L_2$ counts the $b$s modulo $n$, then each pair $(i, j)$ of counters needs its own state, and a script confirmed that the minimal DFA for $L_1 \cap L_2$ has $mn$ states for $1 \le m, n \le 4$. See [state complexity](/state-complexity/).

**The NFA constructions are small.** For NFAs, union, concatenation and star need only $O(1)$ new states and reversal none, and the cost of these operations moves into the later [subset construction](/subset-construction/). Complement is the expensive operation for NFAs: it can need $2^n$ states.

**Operations that do not preserve regularity.**

- An infinite union: $\{ a^n b^n \} = \bigcup_n \{ a^n b^n \}$ is a union of finite, hence regular, languages, and it is not regular.
- A subset: $\{ a^n b^n \}$ is a subset of the regular $\Sigma^*$.
- An image under a map that is not a homomorphism: the map $w \mapsto w w$ sends $\Sigma^*$ to $\{ ww : w \in \Sigma^* \}$, which is not regular for $|\Sigma| \ge 2$.

### Pitfalls

- **Complementing an NFA by swapping the accepting states fails.** The NFA with $\delta(0, a) = \{0, 1\}$, $\delta(0, b) = \{0\}$ and $F = \{1\}$ accepts the strings that end in $a$. With $F = \{0\}$ it accepts every string, because state 0 is always reachable. Determinize first.
- **Complementing a partial DFA by swapping fails.** A string whose run falls off the table is rejected by both machines. Add a dead state first.
- **Star without a new start state fails.** For $L_1 = a^* b$ with the DFA $0 \xrightarrow{a} 0$, $0 \xrightarrow{b} 1$ and $F = \{1\}$, making 0 accepting and adding $1 \xrightarrow{\varepsilon} 0$ accepts $a$, which is not in $(a^* b)^*$.

## History

Rabin and Scott (1959) proved closure under the Boolean operations and other operations with automata, and introduced nondeterministic automata partly for this purpose. Closure under union, concatenation and star is built into Kleene's regular expressions (1956). Ginsburg and his coauthors studied homomorphisms, inverse homomorphisms and quotients in the 1960s as part of the theory of abstract families of languages. The exact state complexities were found by Maslov (1970) and, in a systematic study, by Yu, Zhuang and Salomaa (1994).

## References
