---
tag: VRYA87
kind: algorithm
slug: brzozowski-minimization
name: Brzozowski's minimization algorithm
aliases:
- reverse-determinize-reverse-determinize
area: automata-and-parsing/finite-automata
level: advanced
summary: Minimizes an automaton by reversing, determinizing, reversing and determinizing again.
solves: [dfa-minimization]
model: word-ram
complexity:
  vars: {n: the number of states of the input automaton, σ: the alphabet size}
  time: {worst: O(σ 4^n)}
  space: {extra: O(4^n + σ 2^n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1962
  people: [Janusz A. Brzozowski]
  note: Brzozowski observed that determinizing the reverse of an automaton whose states are all reachable gives a minimal DFA, in his work on definite events.
prereqs: [subset-construction, dfa-minimization, minimal-dfa-uniqueness, nondeterministic-finite-automaton]
see_also: [moore-minimization, hopcroft-minimization, determinization-blowup-lower-bound, closure-properties-of-regular-languages, nfa-determinization, brzozowski-derivatives, state-complexity]
sources:
  - paper: "Janusz A. Brzozowski, Canonical regular expressions and minimal state graphs for definite events, in Proceedings of the Symposium on Mathematical Theory of Automata, MRI Symposia Series 12, Polytechnic Press of the Polytechnic Institute of Brooklyn, 1962"
    locator: pp. 529 to 561
  - paper: doi:10.1016/j.tcs.2014.04.016
    title: Janusz A. Brzozowski and Hellis Tamm, Theory of átomata, Theoretical Computer Science 539 (2014)
    locator: pp. 13 to 27 (a characterization of the automata whose determinized reverse is minimal)
  - paper: doi:10.1007/978-3-642-38771-5_17
    title: Sven De Felice and Cyril Nicaud, Brzozowski algorithm is generically super-polynomial for deterministic automata, Developments in Language Theory (DLT 2013), Lecture Notes in Computer Science 7907
    locator: pp. 179 to 190
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 6, The Subset Construction, and Lectures 13 to 16 on minimization and the Myhill-Nerode theorem
---

Brzozowski's algorithm [minimizes](/dfa-minimization/) an automaton with four simple steps: reverse all transitions, apply the [subset construction](/subset-construction/), reverse again, and apply the subset construction again. The result is the minimal complete DFA. The key fact is that determinizing the reverse of a DFA whose states are all reachable always gives a minimal DFA. The algorithm works on [NFAs](/nondeterministic-finite-automaton/) as well as DFAs, and it removes unreachable states by itself. Its worst-case time is exponential, even for a DFA input whose minimal DFA is small, but it is short to write and often fast in practice on NFAs.

## In plain words

Turn every arrow of the machine around and swap the start and the accepting states. The new machine reads words backwards. Make it deterministic in the usual way, by letting each new state stand for a set of old states.

Each new state now stands for a set of old states from which the same backward words lead to acceptance. Two different sets of this kind always behave differently, so the deterministic machine has no two states that do the same job. It is the smallest machine for the reversed words. Doing all of this a second time turns the words around again, and so it gives the smallest machine for the original words.

## The problem

The input is an NFA $N = (Q, \Sigma, \delta, I, F)$ with $\delta : Q \times \Sigma \to 2^Q$, no $\varepsilon$-moves, $n = |Q|$ and $\sigma = |\Sigma|$. It has a set $I$ of start states, because reversal turns the accepting states into start states; the NFAs and DFAs of the other pages are the case $I = \{q_0\}$. A complete DFA is the case where each $\delta(q, a)$ has one element. The output is the minimal complete DFA for $L(N)$. See [DFA minimization](/dfa-minimization/).

The *reverse* of $N$ is $\mathrm{rev}(N) = (Q, \Sigma, \delta^R, F, I)$ with $\delta^R(q, a) = \{ p : q \in \delta(p, a) \}$. It accepts $L(N)^R = \{ w^R : w \in L(N) \}$, as shown on the [closure properties](/closure-properties-of-regular-languages/) page. The subset construction $\det$ keeps only the subsets that are reachable from the start subset, and it keeps the empty set when it is reached, so its output is a complete DFA with all states reachable.

## The algorithm

```pseudo id=main
BRZOZOWSKI-MINIMIZE(Q, Σ, δ, I, F)
L1  N1 ← rev(N): the transitions reversed, start states F, accepting states I
L2  D1 ← DETERMINIZE(N1)                      ▷ a DFA for L(N)^R
L3  N2 ← rev(D1)
L4  D2 ← DETERMINIZE(N2)                      ▷ the minimal DFA for L(N)
L5  return D2

DETERMINIZE(Q, Σ, δ, I, F)
L6  S0 ← I; give S0 the number 0; queue ← [S0]
L7  while queue is not empty
L8      S ← remove the first subset of queue
L9      for a in Σ: T ← the union of δ(q, a) over q ∈ S
L10         if T has no number: give T the next number, append T to queue
L11         δ'(S, a) ← T
L12 F' ← the subsets S with S ∩ F ≠ ∅
L13 return the DFA with the numbered subsets, δ', start S0 and F'
```

Line L1 builds the reverse NFA, and line L2 determinizes it. Line L2 is a breadth-first search over subsets, lines L6 to L13. Line L9 computes the successor subset, line L10 numbers the subsets in the order of discovery, and line L12 makes a subset accepting when it contains an accepting state. The DFA $D_1$ accepts $L(N)^R$, and all its states are reachable. Line L3 reverses $D_1$, which gives an NFA whose reverse is deterministic, and line L4 determinizes it. Line L5 returns the result, which accepts $(L(N)^R)^R = L(N)$ and is minimal by the theorem in the correctness section.

## Example

Let $\Sigma = \{a, b\}$ and let $N$ be the NFA for the strings that end with $ab$: states 0, 1, 2, $I = \{0\}$, $F = \{2\}$, a loop at 0 on $a$ and $b$, $0 \xrightarrow{a} 1$ and $1 \xrightarrow{b} 2$.

**Lines L1 and L2.** The reverse has start set $\{2\}$, accepting set $\{0\}$ and the moves $2 \xrightarrow{b} 1$, $1 \xrightarrow{a} 0$ and $0 \xrightarrow{a, b} 0$. The subset construction finds four subsets, numbered in the order of discovery:

| $D_1$ state | subset | on $a$ | on $b$ | accepting |
|---|---|---|---|---|
| 0 | $\{2\}$ | 1 | 2 | no |
| 1 | $\emptyset$ | 1 | 1 | no |
| 2 | $\{1\}$ | 3 | 1 | no |
| 3 | $\{0\}$ | 3 | 3 | yes |

$D_1$ accepts the strings that start with $ba$, which is $L(N)^R$. Its state 1 is a dead state.

**Lines L3 and L4.** Reversing $D_1$ gives the start set $\{3\}$, the accepting set $\{0\}$ and, for example, the moves into 3 reversed: $3 \xrightarrow{a} 2$ and $3 \xrightarrow{a, b} 3$. The subset construction now finds three subsets:

| $D_2$ state | subset of $D_1$ states | on $a$ | on $b$ | accepting |
|---|---|---|---|---|
| 0 | $\{3\}$ | 1 | 0 | no |
| 1 | $\{2, 3\}$ | 1 | 2 | no |
| 2 | $\{0, 3\}$ | 1 | 0 | yes |

This is the minimal DFA for the strings that end with $ab$: state 0 means "no progress", state 1 "just read $a$", and state 2 "just read $ab$". The dead state 1 of $D_1$ never appears, because it reaches no accepting state of $D_1$. The test file checks both tables.

## Correctness

The proof rests on one theorem. Let $D = (P, \Sigma, \eta, p_0, G)$ be a deterministic automaton, complete or partial, in which every state is reachable from $p_0$. Then $\det(\mathrm{rev}(D))$ is the minimal complete DFA for $L(D)^R$.

The subset that $\det(\mathrm{rev}(D))$ reaches on a string $w$ is $S_w = \{ p \in P : \eta^*(p, w^R) \in G \}$, the set of states from which $D$ accepts $w^R$; this follows by induction on $|w|$ from the definition of $\delta^R$. The subset $S_w$ is accepting when it contains $p_0$, that is, when $w^R \in L(D)$, so the automaton accepts $L(D)^R$. To show that two different subsets $S_u \neq S_v$ are not equivalent, take $p$ in one of them and not in the other, say $p \in S_u \setminus S_v$. Since $p$ is reachable, $p = \eta^*(p_0, x)$ for some $x$. Then $S_{u x^R}$ contains $p_0$ if and only if $\eta^*(p_0, x u^R) = \eta^*(p, u^R) \in G$, that is, if and only if $p \in S_u$. So $x^R$ is accepted from $S_u$ and rejected from $S_v$. All states are reachable and pairwise inequivalent, so the DFA is minimal by the [uniqueness theorem](/minimal-dfa-uniqueness/). Determinism of $D$ is used in the step $\eta^*(p_0, x u^R) = \eta^*(p, u^R)$.

Line L2 gives a DFA $D_1$ for $L(N)^R$ with all states reachable, so the theorem applied to $D_1$ shows that line L4 returns the minimal DFA for $L(N)$. The full proof is in the correctness file.

## Complexity

Let $d_1$ and $d_2$ be the numbers of states of $D_1$ and $D_2$, with $d_1 \le 2^n$, and $d_2 \le 2^n$ because $D_2$ is the minimal DFA of a language with an $n$-state NFA.

- **Line L2.** Each of the $\sigma d_1$ subset transitions takes a union over up to $n$ states with up to $n$ successors each, $O(n^2)$ time, plus a hash lookup of a set of size up to $n$. Total $O(\sigma n^2 d_1)$ time.
- **Line L4.** $\mathrm{rev}(D_1)$ has $d_1$ states and $d_1$ transitions per symbol in all, so a subset transition takes $O(d_1)$ time, and the total is $O(\sigma d_1 d_2)$.
- **Total.** $O(\sigma (n^2 d_1 + d_1 d_2))$ time, which is $O(\sigma 4^n)$ in the worst case. The space is $O(n d_1 + d_1 d_2)$ for the stored subsets and $O(\sigma (d_1 + d_2))$ for the tables.
- **The blow-up is real, even for DFAs.** Let $D$ be the DFA with $n + 2$ states for "the $n$-th symbol is $a$". Line L2 builds a DFA for "the $n$-th symbol from the end is $a$", which has $2^n$ states by the [determinization blow-up lower bound](/determinization-blowup-lower-bound/), and line L4 returns $n + 2$ states again. A script checked this for $n = 1, \ldots, 6$. De Felice and Nicaud (2013) showed that for random DFAs the expected running time is super-polynomial.

## Properties

- **Works on NFAs.** It minimizes the language of an NFA without a separate determinization step, and it can start from several start states.
- **Removes unreachable states automatically,** because the subset construction explores only reachable subsets.
- **Canonical output.** With the breadth-first numbering of line L10, the output depends only on the language and the order of $\Sigma$.
- **Half of it is useful alone.** If the input is a DFA with all states reachable, lines L3 and L4 alone, applied to it, give the minimal DFA of the reverse language.
- **Deterministic and not recursive.**

## Variants and improvements

- **One determinization suffices for some inputs.** If $\mathrm{rev}(N)$ is already deterministic with all states reachable, then $\det(N)$ is minimal by the theorem, applied to $\mathrm{rev}(N)$. Brzozowski and Tamm (2014) characterized all NFAs whose determinization is minimal, in terms of the *atoms* of the language, the non-empty intersections of the quotients and their complements.
- **Partial DFAs.** Dropping the empty subset in both determinizations gives the minimal partial DFA, which has one state fewer when the language has a dead state.
- **Weighted and other settings.** The reverse-determinize idea extends to weighted automata over some semirings and has a category-theoretic explanation by duality, but the subset construction for weighted automata need not terminate.

## When to use it

Use Brzozowski's algorithm when the input is an NFA, such as the [Thompson](/thompson-construction/) or [Glushkov](/glushkov-automaton/) automaton of a regular expression, and the minimal DFA is wanted in one step, or when a short and obviously correct implementation matters more than worst-case time. For a DFA input, use [Hopcroft's algorithm](/hopcroft-minimization/), which takes $O(\sigma n \log n)$ time, or [Moore's algorithm](/moore-minimization/).

## Pitfalls

- **Exponential intermediate result.** $D_1$ can have $2^n$ states even when the input and the output are small DFAs, as in the complexity section.
- **Dropping the empty subset in only one step.** Each determinization must either keep the empty set as a dead state or drop it consistently. Keeping it in line L2 is harmless, because the dead state of $D_1$ never enters a subset of line L4.
- **One start state.** The reverse of an automaton has a start state for each old accepting state. An implementation that assumes one start state must add a new start state with $\varepsilon$-moves, and then the subset construction must use [epsilon closures](/epsilon-closure/).
- **Reachability is needed.** The theorem needs all states of $D_1$ to be reachable. A determinization that lists all $2^n$ subsets instead of the reachable ones gives a correct but non-minimal result in line L4.

## Implementations

## History

Brzozowski stated the method in 1962, in a paper on definite events, and it became known as a folklore algorithm in the following decades. Its elegance made it a common teaching example, and comparisons by Watson and others found it competitive on NFAs from regular expressions. Brzozowski and Tamm (2014) explained it, and its generalizations, through the atoms of a regular language. De Felice and Nicaud (2013) showed that its average behavior on random DFAs is super-polynomial.

## References
