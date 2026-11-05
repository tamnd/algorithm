---
tag: Y6M4HN
kind: theorem
slug: krohn-rhodes-theorem
name: Krohn-Rhodes theorem
aliases:
- Krohn-Rhodes decomposition theorem
area: automata-and-parsing/finite-automata
level: research
summary: Every finite automaton's transition monoid decomposes into a cascade of simple groups and aperiodic monoids.
prereqs: [deterministic-finite-automaton, monoid]
see_also: [syntactic-monoid, schutzenberger-theorem, star-free-language, mealy-machine, minimal-dfa-uniqueness, lagranges-theorem-group-theory]
sources:
  - paper: doi:10.1090/s0002-9947-1965-0188316-1
    title: Kenneth Krohn and John Rhodes, Algebraic theory of machines. I. Prime decomposition theorem for finite semigroups and machines, Transactions of the American Mathematical Society 116 (1965)
    locator: pp. 450 to 464
  - paper: doi:10.1016/s0019-9958(67)90228-8
    title: H. Paul Zeiger, Cascade synthesis of finite-state machines, Information and Control 10(4) (1967)
    locator: pp. 419 to 433 (the holonomy decomposition)
  - paper: doi:10.1007/978-3-642-13754-9_12
    title: Oded Maler, On the Krohn-Rhodes cascaded decomposition theorem, Time for Verification, Lecture Notes in Computer Science 6200 (2010)
    locator: pp. 260 to 278 (an automata-theoretic account of the holonomy proof)
  - paper: doi:10.1016/s0019-9958(65)90108-7
    title: Marcel-Paul Schützenberger, On finite monoids having only trivial subgroups, Information and Control 8(2) (1965)
    locator: pp. 190 to 194
  - book: doi:10.1007/b104443
    title: John Rhodes and Benjamin Steinberg, The q-theory of Finite Semigroups, Springer Monographs in Mathematics (2009)
    locator: the chapters on the prime decomposition theorem and on complexity
  - book: doi:10.1007/978-1-4612-0289-9
    title: Howard Straubing, Finite Automata, Formal Logic, and Circuit Complexity, Birkhäuser (1994)
    locator: the chapters on the wreath product and on the decomposition theorem
---

The Krohn-Rhodes theorem says that every finite automaton can be built by connecting very simple automata in a chain, where each automaton in the chain reads the input and the states of the automata before it. Two kinds of building block suffice: the *flip-flop*, a one-bit memory that can be set, reset or left alone, and the automata of finite *simple groups*, which permute their states reversibly. Moreover, the simple groups that are needed are exactly those that already occur, as divisors, in the transition monoid of the automaton. The theorem is the analogue for finite automata and semigroups of the decomposition of a finite group into simple factors, and it explains the role of the [syntactic monoid](/syntactic-monoid/) in the classification of regular languages: for example, the automata without nontrivial groups are exactly those built from flip-flops alone.

## Statement

The automata here are *semiautomata*: a semiautomaton $A = (Q, \Sigma, \delta)$ is a complete DFA without start and accepting states, with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves. Each word $w$ acts on $Q$ by $q \mapsto \delta^*(q, w)$, and the *transition monoid* $M(A)$ is the set of these maps, with composition. A monoid $S$ *divides* $T$ if $S$ is a homomorphic image of a submonoid of $T$.

**Covering.** $A = (Q, \Sigma, \delta)$ is *covered* by $B = (P, \Gamma, \eta)$ if there are a partial map $\varphi$ from $P$ onto $Q$ and a map $\psi : \Sigma \to \Gamma$ such that, whenever $\varphi(p)$ is defined, $\varphi(\eta(p, \psi(a)))$ is defined and equals $\delta(\varphi(p), a)$. Then $B$ can simulate $A$: run $B$ on $\psi(w)$ from any $p$ with $\varphi(p) = q$, and read off the state of $A$ by $\varphi$. So every language that $A$ recognizes with some start and accepting states is recognized by $B$.

**Cascade product.** For $A_1 = (Q_1, \Sigma, \delta_1)$ and $A_2 = (Q_2, Q_1 \times \Sigma, \delta_2)$, the cascade $A_1 \circ A_2 = (Q_1 \times Q_2, \Sigma, \delta)$ has

$$\delta((q_1, q_2), a) = (\delta_1(q_1, a), \delta_2(q_2, (q_1, a))).$$

So the second automaton reads the input symbol together with the current state of the first. Longer cascades $A_1 \circ A_2 \circ \cdots \circ A_k$ are defined in the same way: $A_i$ reads the symbol and the states of $A_1, \ldots, A_{i-1}$. Information flows only forward.

**Building blocks.**

- The *flip-flop* $U$ has the states $\{0, 1\}$ and three input symbols: $r_0$ and $r_1$ set the state to 0 and to 1, and $e$ leaves it unchanged. Its transition monoid $\{1, r_0, r_1\}$ is called $U_2$.
- For a finite group $G$, the *group automaton* $A_G$ has the states $G$ and the input symbols $G$, with $\delta(g, h) = gh$.

A component of a cascade may use any map from its input alphabet $Q_1 \times \cdots \times Q_{i-1} \times \Sigma$ to the symbols of $U$ or of $A_G$.

**Theorem (Krohn and Rhodes, 1965).** Every finite semiautomaton $A$ is covered by a cascade $A_1 \circ \cdots \circ A_k$ in which each $A_i$ is a flip-flop or the group automaton $A_G$ of a finite simple group $G$ that divides $M(A)$.

In semigroup terms: every finite semigroup $S$ divides an iterated wreath product of copies of $U_2$ and of finite simple groups that divide $S$.

## In plain words

Any machine with finitely many states can be rebuilt from two kinds of part. One part is a switch that can be turned on, turned off, or left alone. The other part turns its state in a reversible way, like the hand of a clock that moves by fixed steps, and it cannot be split into smaller reversible parts.

The parts sit in a line. Each part sees the input and the states of the parts before it, never the parts after it. The reversible parts that the rebuilt machine needs are only those that are already hidden in the original machine. A machine that never counts in a cycle can be built from switches alone.

## Proof

The proof has a part that concerns groups, which is short and given in full, and a general part, which is long. For the general part we give a proof sketch, marked as such, and refer to Krohn and Rhodes (1965), Zeiger (1967), Maler (2010) and the book of Rhodes and Steinberg (2009).

**Lemma 1 (one normal subgroup).** Let $G$ be a finite group and $N$ a normal subgroup. Then $A_G$ is isomorphic to a cascade $A_{G/N} \circ A_N$, with a suitable map from $(G/N) \times G$ to the symbols of $A_N$.

*Proof.* Choose a transversal: for each coset $c \in G/N$ an element $t(c) \in c$, with $t(N) = 1$. Each $g \in G$ is uniquely $g = n \, t(c)$ with $c = Ng$ and $n = g \, t(c)^{-1} \in N$. Map the state $g$ to $(c, n)$; this is a bijection between $G$ and $(G/N) \times N$.

Now read a symbol $h \in G$. Then $gh = n \, t(c) h$. The coset of $gh$ is $ch$, so $t(c) h \, t(ch)^{-1}$ lies in $N$; call it $\kappa(c, h)$. Then

$$gh = \big(n \, \kappa(c, h)\big) \, t(ch).$$

So the new pair is $(ch, \, n \, \kappa(c, h))$. The first component moves by $h$ in $A_{G/N}$, using only $c$ and $h$. The second moves by the symbol $\kappa(c, h) \in N$ of $A_N$, which depends only on the first component and on $h$. This is the cascade $A_{G/N} \circ A_N$ with the input map $(c, h) \mapsto \kappa(c, h)$, and the bijection respects the transitions. $\square$

For example, the counter modulo 4, the group automaton of $\mathbb{Z}_4$ with the symbol $+1$, splits along $N = \{0, 2\}$ with $t(0) = 0$ and $t(1) = 1$. Then $\kappa(0, +1) = 0$ and $\kappa(1, +1) = 2$: the first component is the low bit, and the second flips exactly when the low bit is 1. This is the binary counter with a carry. A script checked Lemma 1 on $\mathbb{Z}_4$ and on the symmetric group $S_3$ with $N = A_3$.

**Lemma 2 (group automata).** For a finite group $G$ with a composition series $G = G_0 \rhd G_1 \rhd \cdots \rhd G_r = 1$, the automaton $A_G$ is isomorphic to a cascade of the automata of the composition factors $G_{i-1}/G_i$, which are simple groups that divide $G$.

*Proof.* By induction on $|G|$. If $G$ is simple or trivial, there is nothing to show. Otherwise apply Lemma 1 to $N = G_1$. The first component $A_{G/G_1}$ is simple. The second, $A_{G_1}$, is a cascade of the automata of its composition factors by induction, and a cascade whose last component is replaced by a cascade is again a cascade, since each component may read the states of all earlier ones. Each factor $G_{i-1}/G_i$ is a quotient of the subgroup $G_{i-1}$, so it divides $G$. $\square$

**Lemma 3 (covering passes to monoids).** If $A$ is covered by $B$, then $M(A)$ divides $M(B)$.

*Proof.* Let $D \subseteq P$ be the domain of $\varphi$. By induction on $|w|$, the action of $\psi(w)$ maps $D$ into $D$ and satisfies $\varphi(\eta^*(p, \psi(w))) = \delta^*(\varphi(p), w)$ for $p \in D$. The actions of the words $\psi(w)$ form a submonoid $T$ of $M(B)$. Map the action of $\psi(w)$ to the action of $w$ on $Q$. This is well defined: if $\psi(w)$ and $\psi(v)$ act alike, then for each $q \in Q$ pick $p \in D$ with $\varphi(p) = q$, and $\delta^*(q, w) = \varphi(\eta^*(p, \psi(w))) = \varphi(\eta^*(p, \psi(v))) = \delta^*(q, v)$. It is a homomorphism onto $M(A)$. $\square$

**The general case (proof sketch).** If every symbol acts on $Q$ as a permutation, then $M(A)$ is a group $G$, and $A$ is covered by $A_G$ on each orbit; a few flip-flops that hold the orbit, which never changes, combine the orbits, and Lemma 2 finishes. In general, some symbols collapse states. The *holonomy* proof of Zeiger (1967), in the form of Eilenberg and of Maler (2010), considers the family of sets $Q \cdot w = \{\delta^*(q, w) : q \in Q\}$ together with $Q$ and the singletons, ordered by inclusion. It sorts these sets into levels by height. For each set it takes its *holonomy group*, the group of permutations of its maximal subsets that are induced by words mapping the set onto itself. The cascade has one component per level, from the top down. The component of a level holds, for the current state, which maximal subset at that level it lies in, and it changes either by a permutation of the holonomy group or by a reset to a fixed subset. Such a *permutation-reset* automaton is covered by a cascade of its group automaton with flip-flops, and the group automaton is decomposed by Lemma 2. Each holonomy group divides $M(A)$, so the simple groups that occur divide $M(A)$. The details, in particular that the levels together determine the state and that each level's input depends only on the levels above, are in the cited works. $\square$

## Consequences

- **Counter-free automata.** If $M(A)$ is *aperiodic*, that is, it contains no nontrivial group, then no nontrivial simple group divides it, and $A$ is covered by a cascade of flip-flops alone. Conversely, every cascade of flip-flops has an aperiodic transition monoid; a script checked this on 300 random cascades of up to 3 flip-flops. With [Schützenberger's theorem](/schutzenberger-theorem/) on [star-free languages](/star-free-language/) (Schützenberger, 1965), this gives: a regular language is star-free if and only if its minimal DFA is covered by a cascade of flip-flops.
- **Counting needs groups.** The counter modulo $p$ for a prime $p$ is the automaton of the simple group $\mathbb{Z}_p$. Every cascade that covers it contains a component whose group $\mathbb{Z}_p$ divides (see Tightness). So no cascade of flip-flops and counters modulo other primes can count modulo $p$.
- **Solvable monoids.** If every group that divides $M(A)$ is solvable, then all the simple factors are cyclic of prime order, and $A$ is covered by a cascade of flip-flops and counters modulo primes. Non-solvable groups such as $A_5$ give automata of a different kind; they are the source of the power of bounded-width branching programs in circuit complexity (Straubing, 1994).
- **Complexity of semigroups.** The *Krohn-Rhodes complexity* of a semigroup is the least number of group components that must alternate with aperiodic parts in such a decomposition. Its decidability for finite semigroups has been a central open problem of the theory (Rhodes and Steinberg, 2009).
- **Design of sequential circuits.** The theorem says that a sequential machine can be realized as a loop-free network of simple parts. This was a motivation of the original work and of Zeiger's cascade synthesis.

## Tightness

- **Flip-flops are needed unless the monoid is a group.** In a cascade of group automata, each symbol acts on the first component by a permutation, and, for fixed earlier states, on each later component by a permutation, so it acts injectively on the product. Hence the transition monoid of the cascade is a finite monoid of permutations, which is a group. Every divisor of a finite group is a group, because a submonoid of a finite group is a subgroup and a homomorphic image of a group is a group. The flip-flop monoid $U_2$ has three idempotents, $1$, $r_0$ and $r_1$, while a group has one. So by Lemma 3, no cascade of group automata covers a flip-flop, nor any automaton whose transition monoid has $U_2$ as a divisor, which is every automaton whose monoid is not a group.
- **The simple groups are needed.** Krohn and Rhodes (1965) also proved that the finite simple groups are *prime* for this decomposition: if a simple group $G$ divides the transition monoid of a cascade, then $G$ divides the transition monoid of one of its components. So every simple group that divides $M(A)$ must divide some component of every cascade that covers $A$, and the list of groups in the theorem cannot be shortened. This is the sense in which the decomposition is a "prime decomposition". By Lemma 2 and the Jordan-Hölder theorem, for a group automaton the needed simple groups are exactly the composition factors.
- **The components cannot be split further.** The flip-flop and the automata of simple groups cannot themselves be covered by cascades of smaller automata of the two kinds; for the simple groups this is the primality above, and for the flip-flop it follows from the corresponding result for $U_2$.
- **Size.** The theorem bounds the kinds of components, not their number. Constructive versions, such as the holonomy decomposition, can produce cascades with many more states than $A$.

## History

Krohn and Rhodes published the prime decomposition theorem for finite semigroups and machines in 1965. Zeiger (1967) gave the holonomy decomposition, a proof that works directly with the automaton, which Eilenberg's treatise later presented. In the same year as the published theorem, Schützenberger (1965) characterized the star-free languages by aperiodic monoids, and McNaughton and Papert linked them to first-order logic; together with the theorem, these results made aperiodic monoids and flip-flop cascades three views of one class. Maler (2010) gave an account of the holonomy proof in the language of automata, and Rhodes and Steinberg (2009) developed the theory of complexity that grew from the theorem.

## References
