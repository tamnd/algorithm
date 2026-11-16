---
tag: DCGQW0
kind: definition
slug: godel-numbering
name: Gödel numbering
aliases:
- Gödel coding
area: complexity/computability
level: core
summary: A computable, injective coding of formulas, programs or strings by natural numbers, with a computable decoding. It lets machines and formulas talk about machines and formulas.
prereqs: [turing-machine, countability]
see_also: [universal-turing-machine, computable-function, s-m-n-theorem, kleene-recursion-theorem, godel-incompleteness-theorem, countability, kolmogorov-complexity, halting-problem]
sources:
  - paper: doi:10.1007/BF01700692
    title: Kurt Gödel, Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I, Monatshefte für Mathematik und Physik 38 (1931)
    locator: pp. 173 to 198, Section 2 (the numbering of the basic signs and the prime-power codes of formulas and proofs)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.1 (enumerating the binary strings, and codes for Turing machines)
  - paper: doi:10.2307/2964290
    title: Richard M. Friedberg, Three theorems on recursive enumeration, Journal of Symbolic Logic 23(3) (1958)
    locator: pp. 309 to 316, part III (enumeration of the partial recursive functions without repetition)
  - title: Hartley Rogers Jr., Gödel numberings of partial recursive functions, Journal of Symbolic Logic 23(3) (1958)
    locator: pp. 331 to 341 (acceptable numberings and the isomorphism theorem)
  - book: isbn:9780262680523
    title: Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)
    locator: Chapter 1 (the indexing of the partial recursive functions)
---

A Gödel numbering is a coding of the objects of a formal system, such as formulas, proofs, strings or machines, by natural numbers, so that a machine can compute the code of an object and recover the object from its code. Gödel introduced it in 1931 to let arithmetic make statements about its own formulas. In computability it is the step that makes a program into an input: once each [Turing machine](/turing-machine/) $M$ has a number, a machine can read that number, simulate $M$, or build new machines from it. The exact choice of numbering does not matter, as long as coding and decoding are computable.

## Definition

Let $X$ be a set of finite objects that are given as words over a finite alphabet (for example the words of $\Sigma^*$, the formulas of a logic, or the transition tables of Turing machines). A *Gödel numbering* of $X$ is a map $g : X \to \mathbb{N}$ such that:

1. $g$ is injective;
2. $g$ is computable: a machine computes $g(x)$ from $x$;
3. the image $g(X)$ is a [decidable](/decidable-language/) set, and the inverse $g^{-1} : g(X) \to X$ is computable.

Condition 3 says that a machine can tell whether a number is a code and, if it is, decode it. Many authors also allow $g$ to be a bijection onto $\mathbb{N}$, which makes condition 3 automatic for the image.

**Codes of machines.** This area fixes one computable encoding $M \mapsto \langle M \rangle \in \{0,1\}^*$ of Turing machines by binary words, and writes $\langle M, w \rangle$ for a pair of a machine and an input. A standard choice numbers the states $q_1, q_2, \ldots$, the tape symbols $X_1, X_2, \ldots$ and the moves $D_1 = L$, $D_2 = R$, and codes the rule $\delta(q_i, X_j) = (q_k, X_l, D_m)$ as the word $0^i 1 0^j 1 0^k 1 0^l 1 0^m$. The codes of the rules are joined with the separator $11$. Since each block of zeros is nonempty, $11$ never occurs inside the code of one rule, and the decoding is unique.

**Indices.** Turn the binary word into a number by the shortlex order of $\{0,1\}^*$: the word $u$ has index $2^{|u|} - 1 + \mathrm{val}(u)$, and the number $n$ is the word obtained by writing $n + 1$ in binary and deleting its leading $1$. Let $M_e$ be the machine whose code is the word with index $e$; if that word is not a valid code, let $M_e$ be a fixed machine that loops on every input. Then:

- $\varphi_e$ is the partial function that $M_e$ computes, and $W_e = \mathrm{dom}(\varphi_e)$ is its domain;
- every Turing machine is some $M_e$, so the list $\varphi_0, \varphi_1, \ldots$ contains every partial [computable function](/computable-function/);
- each function occurs infinitely often in the list, because unused states can be added to a machine without changing what it computes (the *padding lemma*).

The number $e$ is an *index* or *program number* of $\varphi_e$.

**Acceptable numberings.** A numbering $\psi_0, \psi_1, \ldots$ of all partial computable functions is *acceptable* if (a) the function $(e, x) \mapsto \psi_e(x)$ is partial computable, and (b) for every other numbering $\theta$ that satisfies (a), there is a total computable $t$ with $\theta_e = \psi_{t(e)}$ for all $e$. The numbering by Turing machine codes above is acceptable; condition (a) is the [universal Turing machine](/universal-turing-machine/), and (b) follows from the [s-m-n theorem](/s-m-n-theorem/). Rogers (1958) proved that any two acceptable numberings differ by a computable permutation of $\mathbb{N}$. So results such as the [recursion theorem](/kleene-recursion-theorem/) do not depend on which acceptable numbering is used.

## Examples and non-examples

**Gödel's prime-power code.** Let $p_1 = 2, p_2 = 3, p_3 = 5, \ldots$ be the primes. A finite sequence $(a_1, \ldots, a_k)$ of *positive* integers gets the code
$$\ulcorner a_1, \ldots, a_k \urcorner = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}.$$
By unique factorization the code determines the sequence. Gödel gave each basic sign a positive number, coded a formula as the sequence of its signs, and coded a proof as the sequence of the codes of its formulas.

- The sequence $(1, 2, 1)$ has the code $2^1 \cdot 3^2 \cdot 5^1 = 90$.
- With $a \mapsto 1$ and $b \mapsto 2$, the word $abba$ has the code $2^1 \cdot 3^2 \cdot 5^2 \cdot 7^1 = 3150$.
- The number $600 = 2^3 \cdot 3^1 \cdot 5^2$ decodes to the sequence $(3, 1, 2)$, that is, the word $cab$ if $c \mapsto 3$.
- The code is computable, and so is the decoding: divide by $2, 3, 5, \ldots$ in turn. The image is decidable: a number $n \ge 1$ is a code exactly when the primes that divide it are $p_1, \ldots, p_k$ for some $k$, with no gap.

**Non-example: exponent zero.** If the entries may be $0$, the code is not injective: $(1)$ and $(1, 0)$ both get $2^1 = 2$. Gödel avoided this by giving every sign a positive number. Another fix is to code $(a_1, \ldots, a_k)$ as $p_1^{a_1 + 1} \cdots p_k^{a_k + 1}$.

**The Cantor pairing function.** The map $\pi(x, y) = \tfrac{1}{2}(x + y)(x + y + 1) + y$ is a computable bijection $\mathbb{N}^2 \to \mathbb{N}$ with a computable inverse; for example $\pi(3, 5) = 41$. Nested pairs code tuples, and with a length in front, finite sequences. Any computable bijection with a computable inverse serves as well as the prime-power code; the prime-power code is the one Gödel used because its decoding is easy to define by arithmetic formulas.

**The code of a machine.** The machine of the [Turing machine](/turing-machine/) page that decides $\{0^n 1^n : n \ge 0\}$ has 11 rules. Number its states $q_0, q_1, q_2, q_3, \text{accept}, \text{reject}$ as $1$ to $6$ and its tape symbols $0, 1, \sqcup, X, Y$ as $1$ to $5$. The rule $\delta(q_0, 0) = (q_1, X, R)$ becomes $0\,1\,0\,1\,00\,1\,0000\,1\,00$, a word of 14 bits, and the whole code $\langle M \rangle$ has 219 bits. A program that splits the code at $11$ and counts the zeros in each block gets back the 11 rules and runs the machine: it accepts $0011$ after 13 steps and rejects $001$ after 8 steps, as the machine itself does.

**Non-example: a non-computable listing.** Give the machines that halt on the empty input the even numbers, and the other machines the odd numbers, each part in the shortlex order of the codes. This map is injective, but it is not computable: the last bit of the number of $M$ would tell whether $M$ halts on the empty input, which is an undecidable question (see the [halting problem](/halting-problem/)). Such a map is not a Gödel numbering.

**A numbering without repetition.** Friedberg (1958) built a numbering of all partial computable functions in which each function occurs exactly once. It satisfies condition (a) above, but it is not acceptable, since an acceptable numbering repeats each function infinitely often by the padding lemma. So the numbering used in practice is the machine-code one, with repetitions.

## Related definitions

- [Countability](/countability/): a Gödel numbering is a computable witness that a set of finite objects is countable.
- [Universal Turing machine](/universal-turing-machine/): a machine that takes $\langle M, w \rangle$ and simulates $M$ on $w$. It exists because the decoding is computable.
- [Computable function](/computable-function/): the notation $\varphi_e$ and $W_e$ comes from the numbering above.
- [s-m-n theorem](/s-m-n-theorem/) and [Kleene's recursion theorem](/kleene-recursion-theorem/): statements about the indices of a numbering, which hold for every acceptable numbering.
- [Gödel's incompleteness theorem](/godel-incompleteness-theorem/): the numbering of formulas and proofs is the first step of its proof.
- [Kolmogorov complexity](/kolmogorov-complexity/): the length of the shortest code of a program that prints a string; it depends on the coding only up to an additive constant.

## References
