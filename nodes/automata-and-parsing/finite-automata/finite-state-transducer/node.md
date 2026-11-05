---
tag: P3SZXV
kind: model
slug: finite-state-transducer
name: Finite-state transducer
aliases:
- finite transducer
- sequential transducer
area: automata-and-parsing/finite-automata
level: core
summary: Finite automaton that emits output symbols on transitions, defining a relation between strings.
prereqs: [nondeterministic-finite-automaton, epsilon-nfa, mealy-machine]
see_also:
- mealy-machine
- moore-machine
- weighted-automaton
- levenshtein-automaton
- string-morphism
- closure-properties-of-regular-languages
- regular-language
- two-way-finite-automaton
sources:
  - paper: doi:10.1147/rd.91.0047
    title: Calvin C. Elgot and Jorge E. Mezei, On relations defined by generalized finite automata, IBM Journal of Research and Development 9(1) (1965)
    locator: pp. 47 to 68 (rational relations and their closure under composition)
  - paper: doi:10.1145/321466.321473
    title: Timothy V. Griffiths, The unsolvability of the equivalence problem for Λ-free nondeterministic generalized machines, Journal of the ACM 15(3) (1968)
    locator: pp. 409 to 413
  - paper: doi:10.1016/0304-3975(77)90049-4
    title: Christian Choffrut, Une caractérisation des fonctions séquentielles et des fonctions sous-séquentielles en tant que relations rationnelles, Theoretical Computer Science 5(3) (1977)
    locator: pp. 325 to 337 (the twinning property)
  - paper: doi:10.1016/0304-3975(77)90055-x
    title: Marcel-Paul Schützenberger, Sur une variante des fonctions séquentielles, Theoretical Computer Science 4(1) (1977)
    locator: pp. 47 to 57 (subsequential functions)
  - paper: doi:10.1016/s0304-3975(01)00214-6
    title: Marie-Pierre Béal, Olivier Carton, Christophe Prieur and Jacques Sakarovitch, Squaring transducers, an efficient procedure for deciding functionality and sequentiality, Theoretical Computer Science 292(1) (2003)
    locator: pp. 45 to 63
  - paper: "Mehryar Mohri, Finite-state transducers in language and speech processing, Computational Linguistics 23(2) (1997)"
    locator: pp. 269 to 311 (sequential and subsequential transducers, determinization and minimization)
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1) (2002)
    locator: pp. 69 to 88
  - book: isbn:9783519023401
    title: Jean Berstel, Transductions and Context-Free Languages, Teubner, 1979
    locator: Chapter III, Rational transductions, and Chapter IV, Rational functions
---

A finite-state transducer is a finite automaton whose transitions read input and write output. A run from the start state to a final state reads an input string $x$ and writes an output string $y$, and the transducer *relates* $x$ to $y$. Because it can be nondeterministic, one input may have several outputs, or none. The relations defined this way are the *rational relations*. They are closed under composition and their domains and images of regular languages are regular, but their equivalence is undecidable. Transducers that are deterministic on the input, the *sequential* and *subsequential* transducers, run in linear time and are used for morphology, speech recognition, text normalization and lexical analysis.

## The machine

A finite-state transducer is a tuple $T = (Q, \Sigma, \Delta, E, q_0, F)$, where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is the input [alphabet](/alphabet/) and $\Delta$ the output alphabet,
- $E \subseteq Q \times (\Sigma \cup \{\varepsilon\}) \times \Delta^* \times Q$ is a finite set of transitions,
- $q_0 \in Q$ is the start state, and
- $F \subseteq Q$ is the set of final states.

A transition $(p, a, u, q)$, written $p \xrightarrow{a : u} q$, reads $a$ (one symbol, or nothing if $a = \varepsilon$) and writes the string $u$. So $\varepsilon$-moves on the input are allowed, and a move may write nothing. The model is nondeterministic and need not be complete. With the outputs removed, $T$ is an [epsilon-NFA](/epsilon-nfa/), its *input automaton*.

**The relation.** A path $q_0 \xrightarrow{a_1 : u_1} q_1 \cdots \xrightarrow{a_m : u_m} q_m$ with $q_m \in F$ is *accepting*, and it relates $x = a_1 \cdots a_m$ to $y = u_1 \cdots u_m$ (with $\varepsilon$ dropped). The relation of $T$ is

$$R(T) = \{ (x, y) \in \Sigma^* \times \Delta^* : \text{some accepting path relates } x \text{ to } y \}.$$

For $x \in \Sigma^*$ let $T(x) = \{ y : (x, y) \in R(T) \}$, and for $L \subseteq \Sigma^*$ let $T(L) = \bigcup_{x \in L} T(x)$. The *domain* is $\mathrm{dom}(T) = \{ x : T(x) \neq \emptyset \}$. $T$ is *functional* if $|T(x)| \le 1$ for every $x$.

**Normal form.** A transition $p \xrightarrow{a : b_1 \cdots b_k} q$ with $k \ge 2$ can be replaced by a chain through $k - 1$ new states, $p \xrightarrow{a : b_1} \cdot \xrightarrow{\varepsilon : b_2} \cdots \xrightarrow{\varepsilon : b_k} q$. After this step every transition reads at most one symbol and writes at most one symbol, and $R(T)$ does not change.

**Deterministic classes.** A *sequential* transducer has no $\varepsilon$-moves, at most one transition for each state and input symbol, and all states final. It computes a partial function in one pass. A *subsequential* transducer adds a final output $\rho : F \to \Delta^*$, written after the last symbol (Schützenberger, 1977). A [Mealy machine](/mealy-machine/) is a complete sequential transducer whose transitions all write exactly one symbol. The names vary between authors: some call the subsequential transducers "sequential", and others call any finite-state transducer a "generalized sequential machine".

**Example.** Over $\Sigma = \Delta = \{a, b\}$, let $f(x) = a^{|x|}$ if $x$ ends with $a$, and $f(x) = b^{|x|}$ otherwise. A transducer for $f$ has the states 0 to 4, $q_0 = 0$, $F = \{0, 2, 4\}$, and the transitions

- $0 \xrightarrow{\varepsilon : \varepsilon} 1$ and $0 \xrightarrow{\varepsilon : \varepsilon} 3$, a guess of the last symbol,
- $1 \xrightarrow{a : a} 1$, $1 \xrightarrow{b : a} 1$ and $1 \xrightarrow{a : a} 2$,
- $3 \xrightarrow{a : b} 3$, $3 \xrightarrow{b : b} 3$ and $3 \xrightarrow{b : b} 4$.

On $abba$ the only accepting path is $0, 1, 1, 1, 1, 2$, with the output $aaaa$; the branch through 3 cannot end, because its last move must read $b$. So $T$ is functional, although it is not deterministic. A script checked that $T(x) = \{ f(x) \}$ for all $x$ of length at most 8.

## What it counts

The cost of running a transducer depends on the class.

- **Sequential and subsequential transducers** make one step per input symbol, as a DFA does, and write the output as they go. On an input of length $n$ the time is $O(n + |y|)$ with $y$ the output.
- **General transducers** are simulated like an NFA. To test $(x, y) \in R(T)$, search the graph whose vertices are the triples $(q, i, j)$, a state with $i$ symbols of $x$ read and $j$ symbols of $y$ written, and whose edges follow the transitions that match $x$ and $y$. With $T$ in normal form this takes $O(|E| (|x| + 1)(|y| + 1))$ time. Computing all of $T(x)$ can take exponential time when $T(x)$ is large, and $T(x)$ is infinite if a cycle of $\varepsilon$-input moves writes output; a common way out is to compute $T(x)$ as an automaton, the image of the one-string language $\{x\}$.

The size of a transducer is its number of states, or its number of transitions together with the total length of their outputs.

## Relation to other models

- **Finite automata.** The input automaton of $T$ accepts $\mathrm{dom}(T)$, and the output automaton, with the inputs removed and the outputs split into single symbols, accepts the image $T(\Sigma^*)$. A finite automaton for $L$ is the transducer of the identity relation on $L$.
- **Mealy and Moore machines.** These are the deterministic, length-preserving transducers. See [Mealy machine](/mealy-machine/) and [Moore machine](/moore-machine/).
- **Morphisms.** A [string morphism](/string-morphism/) $h$ is computed by a one-state transducer with the transitions $q \xrightarrow{a : h(a)} q$. The inverse of $h$ is computed by the same transducer with input and output swapped. The [closure properties](/closure-properties-of-regular-languages/) under homomorphism and inverse homomorphism are special cases of the image theorem below.
- **Weighted automata.** A [weighted automaton](/weighted-automaton/) over a semiring gives each string a weight. Weighted transducers combine both and are the main tool of the speech-recognition systems of Mohri, Pereira and Riley (2002).
- **Two-way transducers.** A transducer with a [two-way](/two-way-finite-automaton/) input head can reverse or copy its input, which no one-way transducer can do as a function. Deterministic two-way transducers define the *regular functions*, a strictly larger class than the rational functions.
- **Edit distance.** For a fixed $k$, the relation $\{ (x, y) : x \text{ and } y \text{ have edit distance at most } k \}$ is rational, by a transducer whose state counts the edits used. Its image of one word $x$ is the language of the [Levenshtein automaton](/levenshtein-automaton/) of $x$.

## Known results in the model

### Closure and images

- **Images of regular languages.** If $L$ is regular, then $T(L)$ is regular. *Proof.* Put $T$ in normal form, and take a DFA $D = (P, \Sigma, \eta, p_0, G)$ for $L$. Build the epsilon-NFA with states $Q \times P$, start $(q_0, p_0)$, final states $F \times G$, and a move $(q, p) \xrightarrow{b} (q', \eta(p, a))$ for each transition $q \xrightarrow{a : b} q'$ with $a \in \Sigma$, and $(q, p) \xrightarrow{b} (q', p)$ for each $q \xrightarrow{\varepsilon : b} q'$, where $b \in \Delta \cup \{\varepsilon\}$. Its accepting paths are exactly the pairs of an accepting path of $T$ that relates some $x$ to $y$ and the run of $D$ on $x$ ending in $G$, and the path spells $y$. So it accepts $T(L)$. $\square$ With $L = \Sigma^*$ this shows that the image is regular, and swapping input and output shows that $\mathrm{dom}(T)$ and the preimages $T^{-1}(K)$ of regular $K$ are regular.
- **Composition.** If $R_1 \subseteq \Sigma^* \times \Gamma^*$ and $R_2 \subseteq \Gamma^* \times \Delta^*$ are rational, so is $R_2 \circ R_1 = \{ (x, z) : (x, y) \in R_1, (y, z) \in R_2 \text{ for some } y \}$ (Elgot and Mezei, 1965). *Proof.* Put $T_1$ and $T_2$ in normal form. The composed transducer has the states $Q_1 \times Q_2$, start $(q_1, q_2)$, final states $F_1 \times F_2$, and three kinds of moves: $(p, q) \xrightarrow{a : \varepsilon} (p', q)$ for each $p \xrightarrow{a : \varepsilon} p'$ in $T_1$, where $T_1$ moves and writes nothing; $(p, q) \xrightarrow{\varepsilon : c} (p, q')$ for each $q \xrightarrow{\varepsilon : c} q'$ in $T_2$, where $T_2$ moves and reads nothing; and $(p, q) \xrightarrow{a : c} (p', q')$ for each pair $p \xrightarrow{a : b} p'$ and $q \xrightarrow{b : c} q'$ with $b \in \Gamma$, where the symbol $b$ that $T_1$ writes is read by $T_2$ at once. Given accepting paths of $T_1$ on $(x, y)$ and of $T_2$ on $(y, z)$, walk along both; each move of $T_1$ that writes nothing and each move of $T_2$ that reads nothing is a move of the first or second kind, and each symbol of $y$ pairs one move of $T_1$ with one move of $T_2$ in a move of the third kind. This gives an accepting path of the composed transducer on $(x, z)$. Conversely, an accepting path of the composed transducer projects to an accepting path of $T_1$ and one of $T_2$, and the symbols $b$ of its moves of the third kind spell a common middle string $y$. $\square$
- **Union, concatenation and star.** Rational relations are closed under these operations, by the constructions for NFAs. They are also closed under inverse, by swapping input and output.
- **No intersection or complement.** $R_1 = \{ (a^n b^m, c^n) : n, m \ge 0 \}$ and $R_2 = \{ (a^n b^m, c^m) : n, m \ge 0 \}$ are rational, but $R_1 \cap R_2 = \{ (a^n b^n, c^n) : n \ge 0 \}$ has the domain $\{ a^n b^n \}$, which is not regular, so $R_1 \cap R_2$ is not rational. Since rational relations are closed under union, the De Morgan law shows that they are not closed under complement either.
- **Nivat's theorem.** A relation $R$ is rational if and only if $R = \{ (g(w), h(w)) : w \in K \}$ for a regular language $K$ and two [string morphisms](/string-morphism/) $g$ and $h$.

### Decision problems

- **Emptiness and membership** are decidable in polynomial time by graph search, as above.
- **Equivalence is undecidable.** Deciding $R(T_1) = R(T_2)$ is undecidable, even for transducers without $\varepsilon$-input moves (Griffiths, 1968). So is inclusion.
- **Functionality is decidable.** Whether $T$ is functional can be decided in polynomial time, by a search of the product of $T$ with itself that tracks the delay between the two outputs (Béal, Carton, Prieur and Sakarovitch, 2003).
- **Equivalence of functional transducers is decidable.** If $T_1$ and $T_2$ are functional, then $R(T_1) = R(T_2)$ if and only if $\mathrm{dom}(T_1) = \mathrm{dom}(T_2)$ and the union transducer $T_1 \cup T_2$ is functional. The first test is the equivalence of two regular languages and the second is the test above.

### Sequential functions

A rational function, the relation of a functional transducer, is not always subsequential. The example $f$ above is not. *Proof.* Suppose a subsequential transducer computes $f$. After reading $a^n$ with $n \ge 1$, it has written some string $p_n$ in a state $s_n$. Both $f(a^n a) = a^{n+1}$ and $f(a^n b) = b^{n+1}$ start with $p_n$, so $p_n = \varepsilon$. There are finitely many states, so $s_n = s_m$ for some $n < m$. Then $f(a^n) = p_n \rho(s_n) = \rho(s_n)$ and $f(a^m) = \rho(s_m) = \rho(s_n)$, but $f(a^n) = a^n \neq a^m = f(a^m)$. $\square$

Choffrut (1977) characterized the subsequential functions among the rational ones by the *twinning property*: two states reached by the same input, each with a loop on a common input, must write outputs on these loops that keep the delay between the two outputs bounded. The property is decidable in polynomial time (Béal and others, 2003). When it holds, a transducer can be determinized by a subset construction on pairs (state, pending output), and a subsequential transducer can be minimized by moving outputs as early as possible and then minimizing it as a DFA whose symbols are (input, output) pairs (Mohri, 1997).

### Applications

- **Morphology.** Rules that rewrite strings in a context, such as phonological rules, compile into transducers, and a lexicon composed with the rules maps surface word forms to their analyses.
- **Speech and text processing.** Weighted transducers for the lexicon, the pronunciation and the language model are composed and optimized into one search network (Mohri, Pereira and Riley, 2002).
- **Text normalization and transliteration.** Case folding and many transliteration schemes are sequential transducers, and others are rational functions that need a bounded look-ahead.

### Pitfalls

- **Intersection.** Unlike regular languages, rational relations are not closed under intersection, so the product construction for automata does not work on two transducers that write strings. It works for transducers that read and write exactly one symbol on every move.
- **Cycles of $\varepsilon$-input moves.** A cycle that reads nothing and writes something makes $T(x)$ infinite. Simulations that list $T(x)$ must detect it.
- **Functional is not deterministic.** A functional transducer can need to guess and check, as in the example, so a one-pass algorithm that writes output as it reads can fail on it. Use the twinning test before determinizing, since the determinization does not stop when the property fails.
- **Composition with $\varepsilon$.** When $T_1$ writes nothing and $T_2$ reads nothing on the same step, the construction above can produce several paths for one pair of paths. This does not change the relation, but it does change the result of weighted composition, which needs a filter that keeps one path.

## References
