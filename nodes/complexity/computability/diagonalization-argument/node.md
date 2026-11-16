---
tag: 6Y3CF2
kind: technique
slug: diagonalization-argument
name: Diagonalization argument
aliases:
- Cantor's diagonal argument
- diagonal argument
area: complexity/computability
level: intro
summary: Build an object that differs from the i-th member of a list in the i-th place, so it is not in the list. It proves uncountability, undecidability and the hierarchy theorems.
prereqs: [countability]
see_also: [countability, halting-problem, acceptance-problem, undecidability, time-hierarchy-theorem, kleene-recursion-theorem, relativization, ladner-theorem]
sources:
  - title: Georg Cantor, Über eine elementare Frage der Mannigfaltigkeitslehre, Jahresbericht der Deutschen Mathematiker-Vereinigung 1 (1891)
    locator: pp. 75 to 78
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 8, Application of the diagonal process
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.2, Undecidability (the diagonalization method)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.1 (the diagonalization language)
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117 (1965)
    locator: pp. 285 to 306 (time hierarchy by diagonalization)
---

The diagonalization argument builds an object that is not in a given list. Take a list of objects $x_0, x_1, x_2, \ldots$, each with coordinates $0, 1, 2, \ldots$, and build $d$ so that its $i$-th coordinate differs from the $i$-th coordinate of $x_i$. Then $d \ne x_i$ for every $i$. Cantor used it in 1891 to show that the infinite binary sequences cannot be listed. Turing used it in 1936 against the list of all machines, and it is still the main way to show that a problem is [undecidable](/undecidability/), that a language is not [computably enumerable](/recursively-enumerable-language/), or that more time lets machines decide more languages.

## In plain words

Suppose someone claims to list every infinite row of zeros and ones. Write the rows one below the other. Walk down the diagonal: the first entry of the first row, the second entry of the second row, and so on. Flip each of these entries and write the results as a new row.

The new row differs from the first row in the first place, from the second row in the second place, and from every row somewhere. So it is not in the list, and the claim was false.

The same trick works on a list of programs. Each program gives an answer on each input, and the inputs can be the programs themselves. A new program that, on each program, does the opposite of what that program does on itself, is not in the list. If the list holds all programs, the new program cannot exist.

## When it applies

- The objects can be seen as rows of a table: each object $x_i$ has an entry $x_i(j)$ for each column $j$, and the columns can be indexed by the same set as the rows.
- You want to show that some list, or every list of a certain kind, misses an object: no surjection onto a set, no machine for a language, no algorithm within a resource bound.
- For results about computation, the list is a list of machines or programs, given by a [Gödel numbering](/godel-numbering/), and the column $i$ is the input $i$ or the code of machine $i$ itself.
- To show that the new object is itself computable, or computable within a bound, the entries of the diagonal must be computable within that bound. This usually needs a [universal Turing machine](/universal-turing-machine/).

## The template

Let LIST be a list $x_0, x_1, x_2, \ldots$ of objects. ENTRY$(x, i)$ is the $i$-th coordinate of $x$, and FLIP is a map on the values of the coordinates with $\mathrm{FLIP}(a) \ne a$ for every value $a$.

```pseudo id=template
DIAGONAL(LIST)                 ▷ LIST(i) is the object x_i, for i = 0, 1, 2, ...
L1  for each index i = 0, 1, 2, ...
L2      a ← ENTRY(LIST(i), i)      ▷ the i-th coordinate of the i-th object
L3      d(i) ← FLIP(a)             ▷ FLIP(a) ≠ a for every value a
L4  return d                       ▷ the object with coordinates d(0), d(1), ...
```

**Lemma.** For every $i$, the object $d$ returned at L4 differs from $x_i$.

*Proof.* At L3, $d(i) = \mathrm{FLIP}(x_i(i)) \ne x_i(i)$, so $d$ and $x_i$ differ in coordinate $i$. $\square$

**Effective form.** If LIST, ENTRY and FLIP are computable, then $d$ is computable: to find $d(i)$, run L2 and L3 for this $i$. So a computable list of total computable objects of this kind cannot contain all of them. In the results about machines, the argument goes the other way: one assumes that some machine exists, puts $d$ together from that machine and a universal machine, and finds that $d$ would be on the list of all machines, which the lemma forbids.

## Classic examples

### Binary sequences and real numbers (Cantor 1891)

The list is any sequence $x_0, x_1, \ldots$ of infinite binary sequences, ENTRY is the $i$-th bit, and FLIP exchanges $0$ and $1$. So no list contains all binary sequences, and $\{0, 1\}^{\mathbb{N}}$ is uncountable. With the rows $0110$, $1010$, $0001$, $1111$ as the first bits of $x_0$ to $x_3$, the diagonal is $0, 0, 0, 1$ and $d$ starts with $1110$. For real numbers, use decimal digits and let FLIP map $5$ to $6$ and every other digit to $5$. Then $d$ has no digit $0$ or $9$, so it has only one decimal expansion, and it is not any $x_i$.

### Power sets

For any set $S$ and any map $f : S \to \mathcal{P}(S)$, the set $D = \{ s \in S : s \notin f(s) \}$ is not a value of $f$. Here the rows are the sets $f(s)$, the columns are the elements of $S$, and FLIP is negation. This is Cantor's theorem; see [countability](/countability/).

### A language that is not computably enumerable

Let $w_0, w_1, \ldots$ be the binary words in shortlex order and $M_0, M_1, \ldots$ the Turing machines, where $M_i$ has code $w_i$. Let
$$L_d = \{ w_i : M_i \text{ does not accept } w_i \}.$$
If $L_d = L(M_j)$ for some $j$, then $w_j \in L_d$ if and only if $M_j$ does not accept $w_j$, if and only if $w_j \notin L(M_j) = L_d$. So $L_d$ is the language of no machine: it is not c.e. Here the rows are the languages $L(M_i)$, the columns are the words $w_j$, and FLIP is negation.

### The acceptance problem and the halting problem (Turing 1936)

Suppose a machine $H$ decides $A_{\mathrm{TM}} = \{ \langle M, w \rangle : M \text{ accepts } w \}$. Let $D$ be the machine that on input $\langle M \rangle$ runs $H$ on $\langle M, \langle M \rangle \rangle$ and outputs the opposite: it accepts if $H$ rejects, and rejects if $H$ accepts. Then $D$ halts on every input, and $D$ accepts $\langle D \rangle$ if and only if $H$ rejects $\langle D, \langle D \rangle \rangle$, if and only if $D$ does not accept $\langle D \rangle$. This is a contradiction, so $H$ does not exist, and the [acceptance problem](/acceptance-problem/) is undecidable. The same proof, with "halts" for "accepts" and a machine $D$ that runs forever where $H$ says "halts", works for the [halting problem](/halting-problem/). Turing's own proof, in Section 8 of his paper, is about machines that print infinitely many digits ("circle-free" machines), and diagonalizes against the sequences they print.

### A total computable function that is not primitive recursive

The [primitive recursive](/primitive-recursive-function/) definitions are words, so a machine can list them, and each one defines a total function. Let $f_0, f_1, \ldots$ be the unary functions they define, in this order, and let $d(n) = f_n(n) + 1$. Then $d$ is total computable: find the $n$-th definition and evaluate it at $n$. And $d$ differs from each $f_n$ at $n$, so it is not primitive recursive. If the list starts with $n$, $2n$, $n^2$ and $2^n$, then $d(0), \ldots, d(3)$ are $1, 3, 5, 9$. The [Ackermann function](/ackermann-function/) is a natural function with the same property.

### The time hierarchy (Hartmanis and Stearns 1965)

Let $t$ be time-constructible. The machine $D$ takes an input $x$ of the form $\langle M \rangle$ followed by padding $1 0^k$, with $n = |x|$. It simulates $M$ on $x$ with the efficient universal machine and stops after $t(n)$ of its own steps. It accepts if the simulation finished within this time and $M$ did not accept, and rejects otherwise. So $D$ runs in time $O(t(n))$. Let $M$ run in time $g(n)$ with $g(n) \log g(n) = o(t(n))$. The simulation costs $O(c_M\, g(n) \log g(n))$ steps of $D$, so on inputs with enough padding it finishes, and $D$ disagrees with $M$ on them. So $L(D)$ is decidable in time $O(t(n))$ and not in time $g(n)$. This is the [time hierarchy theorem](/time-hierarchy-theorem/); the [space hierarchy theorem](/space-hierarchy-theorem/) is proved in the same way.

## Variations

- **Fixed points.** If every map on the values has a fixed point, the argument cannot work, and turning it around gives fixed-point theorems. [Kleene's recursion theorem](/kleene-recursion-theorem/) says that for every total computable $f$ there is an $e$ with $\varphi_e = \varphi_{f(e)}$. Gödel's diagonal lemma, behind [Gödel's incompleteness theorem](/godel-incompleteness-theorem/), builds a sentence that says of itself that it is not provable.
- **Delayed diagonalization.** Instead of differing from $x_i$ at a fixed place $i$, the new object waits until it has enough time to find a place where it differs, and then moves on to $x_{i+1}$. [Ladner's theorem](/ladner-theorem/) builds a language in NP that is neither in P nor NP-complete (if P is not NP) this way.
- **Priority arguments.** Several diagonal requirements, against several lists at once, may conflict. The priority method orders the requirements and lets a requirement of higher priority injure one of lower priority a finite number of times. It solves [Post's problem](/post-problem/) on c.e. sets strictly between the decidable sets and the halting problem.
- **Lazy diagonalization.** For nondeterministic machines, the flip "accept if $M$ rejects" is not cheap, since a nondeterministic machine cannot complement itself quickly. Lazy diagonalization only flips the answer on rare long inputs, where it has time for a deterministic simulation, and is used for the nondeterministic time hierarchy.
- **Counting instead of diagonalization.** The non-constructive form of the argument compares sizes: there are more languages than machines ([countability](/countability/)), and more Boolean functions than small circuits ([counting argument](/counting-argument/)). It shows existence without naming the object.

## Pitfalls

- **Duplicate representations.** Real numbers have two decimal expansions when one ends in $0$s and the other in $9$s, for example $0.1999\ldots = 0.2000\ldots$. A FLIP that can produce such an expansion can produce a number that is in the list after all. Use digits away from $0$ and $9$.
- **The list must be all of them.** The argument shows that $d$ is not in *this* list. To prove uncountability, it must work for *every* list. To prove undecidability, the list must contain *every* machine, so that $d$, if it were computable, would be in it.
- **Partial functions.** For a list $\varphi_0, \varphi_1, \ldots$ of all partial computable functions, $d(i) = \varphi_i(i) + 1$ is partial computable and is undefined where $\varphi_i(i)$ is undefined. Then $d = \varphi_j$ for some $j$ with $\varphi_j(j)$ undefined, and there is no contradiction. FLIP must change every value, and "undefined" is a value that no machine can detect and flip. This is why the partial computable functions have a universal function, and the total ones do not.
- **The diagonal must be computable within the claimed bound.** In a hierarchy proof, $D$ must itself run within the larger time bound, including the cost of simulating $M$ and of counting to $t(n)$. A diagonal that is too expensive proves nothing about the larger class.
- **Diagonalization relativizes.** A pure simulation and diagonalization argument works the same way for machines with any oracle. Since there are oracles $A$ with $\mathrm{P}^A = \mathrm{NP}^A$ and oracles $B$ with $\mathrm{P}^B \ne \mathrm{NP}^B$ ([Baker, Gill and Solovay](/baker-gill-solovay-theorem/)), such an argument cannot settle P against NP. See [relativization](/relativization/).

## Exercises

1. Let $E$ be the set of binary sequences that have only finitely many $1$s. Show that $E$ is countable, and explain where the diagonal argument fails for a list of $E$.
2. Apply the template to a list that starts with $n + 1$, $3n$, $n^3$ and $n!$, with FLIP$(a) = a + 1$. Compute $d(0)$ to $d(3)$.
3. Prove that no machine lists exactly the codes of the machines that halt on every input. Hint: from such a list $e_0, e_1, \ldots$, build $d(n) = \varphi_{e_n}(n) + 1$.
4. Let $\psi(e) = \varphi_e(e) + 1$ where defined. Show that $\psi$ is partial computable, and that no total computable function agrees with $\psi$ on the domain of $\psi$.
5. List the deterministic finite automata over $\{0, 1\}$ as $B_0, B_1, \ldots$. Show that $\{ w_i : B_i \text{ does not accept } w_i \}$ is decidable but not regular.
6. Write out the halting-problem form of the proof above: given a decider $H$ for HALT, build $D$ and derive the contradiction. Where does the proof need $D$ to run forever, rather than reject?

## References
