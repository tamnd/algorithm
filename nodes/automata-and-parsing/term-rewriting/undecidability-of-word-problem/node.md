---
tag: 6DJ4FQ
kind: theorem
slug: undecidability-of-word-problem
name: Undecidability of the word problem
aliases:
- Post-Markov theorem
area: automata-and-parsing/term-rewriting
level: advanced
summary: There is no algorithm deciding equivalence for arbitrary finite string-rewriting systems.
prereqs: [word-problem, string-rewriting-system, halting-problem]
see_also: [turing-machine, word-problem-for-groups, post-canonical-system, post-correspondence-problem, undecidability-of-termination, confluence-decision-problem, knuth-bendix-completion]
sources:
  - paper: doi:10.2307/2267170
    title: Emil L. Post, Recursive unsolvability of a problem of Thue, Journal of Symbolic Logic 12(1) (1947)
    locator: pp. 1 to 11
  - book: isbn:9780387979656
    title: Ronald V. Book and Friedrich Otto, String-Rewriting Systems, Springer, 1993
    locator: the chapter on decision problems for Thue systems (undecidability of the word problem, Thue's question of 1914, and the results of Post and Markov)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.1, Deciding ≈E (the word problem is undecidable in general)
---

The **undecidability of the word problem**, proved by Post and by Markov in 1947, says that there is a finite Thue system, a set of string equations $u_i = v_i$, for which no algorithm decides whether two given strings are equal. Equivalently, there is a finitely presented semigroup with an undecidable word problem. The proof encodes a Turing machine as string rewrite rules, so that an initial configuration is equal to a fixed halting word iff the machine halts. Since strings are terms over unary symbols, the equational [word problem](/word-problem/) for terms is undecidable too.

## Statement

We use the notation of the term rewriting pages, specialized to strings as on the [string rewriting system](/string-rewriting-system/) page: an alphabet $A$, words $A^*$, rules $l \to r$ with $l, r \in A^*$, a step $x l y \to_T x r y$, and $\to_T^*$ for the reflexive transitive closure. A **Thue system** uses its rules in both directions: $\leftrightarrow_T^*$ is the reflexive, symmetric and transitive closure of $\to_T$, the **Thue congruence**. Two words are equal in the monoid presented by $\langle A \mid T \rangle$ iff they are $\leftrightarrow_T^*$-related.

**Theorem (Post 1947, Markov 1947).**

1. (Uniform version.) There is no algorithm that, given a finite Thue system $T$ over $A$ and words $u, v \in A^*$, decides whether $u \leftrightarrow_T^* v$.
2. (Fixed system.) There is a fixed finite Thue system $T$ for which no algorithm decides, given $u, v$, whether $u \leftrightarrow_T^* v$.

Since no rule below has an empty side, the same holds for finitely presented semigroups.

## In plain words

Take a fixed list of allowed swaps between short strings, each usable forwards or backwards. Given two long strings, can one be turned into the other by a sequence of such swaps? The theorem says that for some lists no computer program can answer this question for every pair of strings.

The reason is that the swaps can imitate a computer. A string records the whole state of a running machine, and one swap performs one step of the machine. Asking whether the starting string can be turned into the string "the machine has stopped" asks whether the machine stops, and no program can answer that for every machine.

The catch is that swaps can run backwards, which a machine cannot do. The proof shows that going backwards never helps, because the machine has only one possible next step.

## Proof

**The machine.** Let $M$ be a deterministic [Turing machine](/turing-machine/) with states $Q$, tape alphabet $\Gamma$ with blank $\square$, start state $q_0$, and one halting state $h$ with no transitions. The tape is infinite to the right, and $M$ never moves left from the first cell. A configuration with tape contents $x y$ (followed by blanks), state $q$ and the head on the first letter of $y$ is written as the word $x\, q\, y\, \rhd$ over $A = \Gamma \cup Q \cup \{\rhd\}$; an empty $y$ means the head is on a blank to the right of the written part.

**The rules.** $T_M$ has the following rules:

1. $q\, a \to b\, q'$ for each move $\delta(q, a) = (q', b, \mathrm{R})$;
2. $c\, q\, a \to q'\, c\, b$ for each move $\delta(q, a) = (q', b, \mathrm{L})$ and each $c \in \Gamma$;
3. $q\, \rhd \to q\, \square\, \rhd$ for each $q \ne h$ (the head reaches fresh tape);
4. $h\, a \to h$ for each $a \in \Gamma$ (erase to the right of the head after halting);
5. $c\, h\, \rhd \to h\, \rhd$ for each $c \in \Gamma$ (then erase to the left).

Let $H = h \rhd$. No rule applies to $H$: rules 1 to 3 need a state other than $h$, rule 4 needs a letter after $h$, and rule 5 a letter before it.

**Claim.** $M$ halts on input $w \in \Gamma^*$ iff $q_0\, w \rhd \leftrightarrow_{T_M}^* H$.

**Step 1 (configuration words are closed).** Call a word a configuration word if it has the form $x\, q\, y\, \rhd$ with $x, y \in \Gamma^*$ and $q \in Q$. Each side of each rule has exactly one state symbol, and the symbol $\rhd$ appears either at the end of both sides or in neither. So a step in either direction turns a configuration word into a configuration word, and every word on a chain $q_0 w \rhd = u_0 \leftrightarrow u_1 \leftrightarrow \cdots$ is one.

**Step 2 (determinism).** A configuration word $x\, q\, y\, \rhd$ has at most one successor under $\to_{T_M}$. Every left side contains the state symbol, so a redex must contain $q$, and it is fixed by $q$ and its neighbours. If $q \ne h$ and $y = a y'$, only the rule of type 1 or 2 for $\delta(q, a)$ can apply, and for type 2 the letter $c$ is the last letter of $x$. If $q \ne h$ and $y$ is empty, only rule 3 applies. If $q = h$, rule 4 applies iff $y$ is nonempty, and rule 5 iff $y$ is empty and $x$ is not. In each case there is at most one rule at one position.

**Step 3 (forward simulation).** If $M$ moves from configuration $C$ to $C'$, then the word of $C$ rewrites to the word of $C'$ in one step, or in two steps when rule 3 first adds a blank. Rules 4 and 5 then reduce any word $x\, h\, y \rhd$ to $H$. So if $M$ halts on $w$, then $q_0 w \rhd \to_{T_M}^* H$. Conversely, rules 1 to 3 introduce $h$ only when $M$ enters $h$, and by Step 2 the forward reduction from $q_0 w \rhd$ is the unique one that simulates $M$. So $q_0 w \rhd \to_{T_M}^* H$ implies that $M$ halts on $w$.

**Step 4 (backward steps do not help).** Suppose $q_0 w \rhd = u_0 \leftrightarrow u_1 \leftrightarrow \cdots \leftrightarrow u_n = H$, with $n$ as small as possible. Call step $i$ forward if $u_{i-1} \to u_i$ and backward if $u_i \to u_{i-1}$. If a backward step $i$ is followed by a forward step $i + 1$, then $u_{i-1} \leftarrow u_i \to u_{i+1}$, and by Step 2, $u_{i-1} = u_{i+1}$; deleting $u_i$ and $u_{i+1}$ gives a shorter chain, a contradiction. So all forward steps come before all backward steps. If $n \ge 1$ and the last step is backward, then $H \to u_{n-1}$, which is impossible since $H$ is irreducible. Hence there are no backward steps, and $q_0 w \rhd \to_{T_M}^* H$. By Step 3, $M$ halts on $w$. This proves the claim.

**Conclusion.** The map $(M, w) \mapsto (T_M, q_0 w \rhd, H)$ is computable. A decision procedure for the uniform word problem would decide the [halting problem](/halting-problem/), which proves part 1. For part 2, fix a machine $M$ whose halting set $\{ w : M \text{ halts on } w \}$ is undecidable, such as a universal machine. Then $T_M$ is one fixed finite Thue system, and deciding $q_0 w \rhd \leftrightarrow_{T_M}^* H$ for all $w$ would decide that set. $\blacksquare$

**Example.** Let $M_1$ scan right over $\Gamma = \{0, 1, \square\}$, halting at the first $1$: $\delta(q_0, 0) = (q_0, 0, \mathrm{R})$, $\delta(q_0, \square) = (q_0, \square, \mathrm{R})$, $\delta(q_0, 1) = (h, 1, \mathrm{R})$. On input $01$:
$$q_0\, 0\, 1 \rhd \;\to\; 0\, q_0\, 1 \rhd \;\to\; 0\, 1\, h \rhd \;\to\; 0\, h \rhd \;\to\; h \rhd.$$
On input $0$ the machine runs forever and the class of $q_0\, 0 \rhd$ is infinite: $0\, q_0 \rhd$, $0\, q_0\, \square \rhd$, $0\, \square\, q_0 \rhd, \ldots$ never reach $H$. A program built $T_{M_1}$ and $T_{M_2}$ for a binary increment machine $M_2$ with left moves, and checked on all inputs of length at most 4 that each configuration word has at most one successor, that the forward reduction reaches $H$ exactly when the machine halts, and that a bounded search of the Thue class in both directions finds $H$ only in those cases.

## Consequences

- **Equational logic.** Read each letter $a$ as a unary function symbol and each word $a_1 \cdots a_k$ as the term $a_k(\cdots a_1(x) \cdots)$. Then $T_M$ becomes a finite set $E$ of equations between terms with one variable, and $u \leftrightarrow_T^* v$ iff $u \approx_E v$. So the [word problem](/word-problem/) for equational theories is undecidable, already for a fixed finite $E$ over unary symbols.
- **Rewriting tools.** No complete procedure can decide $\approx_E$ for every finite $E$. In particular [Knuth-Bendix completion](/knuth-bendix-completion/) cannot succeed on every input: when it ends with a finite convergent system, the word problem of that system is decidable, so for $E = T_M$ it must fail or run forever.
- **Other properties.** Reachability $u \to_T^* v$ for semi-Thue systems is undecidable by Step 3 alone. The same encoding idea gives the undecidability of [termination](/undecidability-of-termination/) and of [confluence](/confluence-decision-problem/). The [Post correspondence problem](/post-correspondence-problem/) is another problem about pairs of words whose undecidability is proved by simulating a machine.
- **Groups.** The [word problem for groups](/word-problem-for-groups/) is undecidable too, by the Novikov-Boone theorem, but the proof is much harder, since inverses allow far more equalities than a Thue system has.

## Tightness

- **Determinism matters.** Without Step 2, a Thue congruence can relate words that no forward reduction connects. In the semi-Thue system $\{a \to b,\ a \to c\}$, $b \leftarrow a \to c$ gives $b \leftrightarrow^* c$, but neither $b \to^* c$ nor $c \to^* b$. This is why the proof straightens chains only for a deterministic machine.
- **Decidable special cases.** The word problem is decidable for every finite Thue system that has an equivalent finite [convergent](/confluence/) system, for ground term equations by congruence closure, and for commutative semigroups, where it is EXPSPACE-complete; see [word problem](/word-problem/). So the undecidable systems are not convergent and not commutative.
- **Fixed system, varying words.** Part 2 needs only the words to vary. For any single pair $u, v$ the question has a fixed answer, so the undecidability is about a uniform method for all pairs.

## History

Axel Thue posed the problem of deciding equality of words under a finite set of substitutions in 1914, and the systems are named after him (Book and Otto). Post (1947) and Markov (1947) independently proved that it is undecidable, Post by a reduction from Turing machines close to the one above.

## References
