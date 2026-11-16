---
tag: KAXFCE
kind: definition
slug: computable-function
name: Computable function
aliases:
- recursive function
- effectively computable function
area: complexity/computability
level: intro
summary: A partial function whose value some Turing machine computes on every input in its domain, and on whose other inputs the machine runs forever. A total computable function is defined everywhere.
prereqs: [turing-machine, church-turing-thesis]
see_also: [partial-recursive-function, primitive-recursive-function, uncomputable-function, godel-numbering, universal-turing-machine, decidable-language, busy-beaver-function, s-m-n-theorem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 5.3, Mapping reducibility (computable functions)
  - book: isbn:9780262680523
    title: Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)
    locator: Chapter 1 (partial recursive functions, the indexing and the enumeration theorem)
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 1, Defining Computability (partial computable functions, the notation for indices)
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265 (computable sequences and numbers)
---

A computable function is a function whose values a [Turing machine](/turing-machine/) can compute. In computability the word means a *partial* function by default: the machine halts with the value on each input where the function is defined, and runs forever on the other inputs. A *total* computable function is a computable function that is defined on every input. By the [Church-Turing thesis](/church-turing-thesis/), these are the functions that any mechanical method can compute, and the same class arises from the [partial recursive functions](/partial-recursive-function/), the [lambda calculus](/lambda-calculus/) and every other general model.

## Definition

Fix a finite alphabet $\Sigma$. A *partial function* $f : \Sigma^* \rightharpoonup \Sigma^*$ has a domain $\mathrm{dom}(f) \subseteq \Sigma^*$ and a value $f(x)$ for each $x \in \mathrm{dom}(f)$. We write $f(x)\!\downarrow$ when $x \in \mathrm{dom}(f)$ and $f(x)\!\uparrow$ otherwise.

A Turing machine $M$ *computes* $f$ if, for every $x \in \Sigma^*$:

- if $f(x)\!\downarrow$, then $M$ on input $x$ halts in the state accept, and the tape then holds $f(x)$ followed by blanks;
- if $f(x)\!\uparrow$, then $M$ on input $x$ never halts.

The partial function $f$ is *computable* (also *partial computable*, or *partial recursive*) if some Turing machine computes it. It is *total computable* if, in addition, $\mathrm{dom}(f) = \Sigma^*$. Functions on $\mathbb{N}$ are coded by words, for example in binary or in unary ($n \mapsto 1^n$); functions of several arguments take a coded tuple, for example $1^x 0 1^y$ or a [pairing function](/godel-numbering/). The choice of a computable coding does not change the class.

**Total or partial.** This page means partial functions unless it says total. Older texts use the word "recursive" alone for the *total* functions of the class and "partial recursive" for the partial ones; see the [partial recursive function](/partial-recursive-function/) page for the definition by recursion and minimization. Many modern texts use "computable" for both and say "total" when they mean it. This page uses *computable* for partial functions and *total computable* for total ones.

**Indices.** With the [Gödel numbering](/godel-numbering/) of machines, $\varphi_e$ is the partial function that the machine with index $e$ computes, and $W_e = \mathrm{dom}(\varphi_e)$. Every computable function equals $\varphi_e$ for infinitely many $e$. The *enumeration theorem* says that the function $(e, x) \mapsto \varphi_e(x)$ is itself computable; a [universal Turing machine](/universal-turing-machine/) computes it.

**Equivalent forms.** For a partial function $f : \mathbb{N} \rightharpoonup \mathbb{N}$ the following are equivalent:

1. $f$ is Turing computable;
2. $f$ is partial recursive (built from the basic functions by composition, primitive recursion and the minimization operator $\mu$);
3. $f$ is lambda-definable;
4. the graph $\{(x, y) : f(x) = y\}$ is a [computably enumerable](/recursively-enumerable-language/) set.

Items 1 to 3 are classical theorems of Kleene and Turing. For 1 and 4: from a machine for $f$, a machine that on $(x, y)$ runs $f(x)$ and accepts if the result is $y$ recognizes the graph. Conversely, from a machine $G$ for the graph, a machine for $f$ on input $x$ runs $G$ on all pairs $(x, 0), (x, 1), \ldots$ by dovetailing (round $r$ runs $r$ steps on each of the first $r$ pairs) and outputs the first $y$ that $G$ accepts. Since the graph has at most one $y$ for each $x$, the output is $f(x)$, and if $f(x)\!\uparrow$ the search never ends.

## Examples and non-examples

**Total computable functions.** The successor $x + 1$, addition, multiplication, $x \bmod y$ with a fixed value at $y = 0$, the $n$-th prime, the [Ackermann function](/ackermann-function/), and every function with a [primitive recursive](/primitive-recursive-function/) definition. The Ackermann function is total computable but not primitive recursive, so the primitive recursive functions are a proper subclass.

**A machine for addition.** On the input $1^x 0 1^y$, the machine has the rules: in $q_0$ move right over $1$; in $q_0$ on $0$ write $1$ and go to $q_1$; in $q_1$ move right over $1$; in $q_1$ on a blank move left to $q_2$; in $q_2$ on $1$ write a blank and accept. It halts after $x + y + 3$ steps with $1^{x+y}$ on the tape:

| $(x, y)$ | $(0, 0)$ | $(2, 3)$ | $(3, 0)$ | $(0, 4)$ | $(5, 7)$ |
|---|---|---|---|---|---|
| steps | 3 | 8 | 6 | 7 | 15 |
| output | empty | $1^5$ | $1^3$ | $1^4$ | $1^{12}$ |

**Partial computable functions.** The everywhere undefined function, computed by a machine that loops on every input. The function $h(x) = x / 2$ for even $x$, undefined for odd $x$. The function that, on input $e$, runs $\varphi_e(e)$ and outputs $\varphi_e(e) + 1$ if that halts; it is undefined exactly on the $e$ with $\varphi_e(e)\!\uparrow$.

**A partial computable function with no total computable extension.** Let $\psi(e) = \varphi_e(e) + 1$ where defined. If a total computable $g$ agreed with $\psi$ on $\mathrm{dom}(\psi)$, then $g = \varphi_i$ for some $i$, and $\varphi_i(i) = g(i)$ is defined, so $g(i) = \psi(i) = \varphi_i(i) + 1 = g(i) + 1$, which is false. So the partial functions cannot simply be "completed" to total ones.

**Computable, but we do not know the program.** Let $g(n) = 1$ if the decimal expansion of $\pi$ contains a run of at least $n$ consecutive digits $7$, and $g(n) = 0$ otherwise. If runs of every length occur, $g$ is the constant $1$. If not, there is a largest length $k$, and $g(n) = 1$ exactly for $n \le k$. In each case $g$ is computed by a very simple machine. So $g$ is computable, though we do not know which of these machines computes it. Computability asks for the existence of a machine, not for a way to find it.

**Non-examples.**

- The halting function: $\mathrm{halt}(e) = 1$ if $\varphi_e(e)\!\downarrow$ and $0$ otherwise. It is total but not computable, because the [halting problem](/halting-problem/) is undecidable.
- The [busy beaver function](/busy-beaver-function/) $\Sigma(n)$, the largest number of $1$s that a halting $n$-state machine leaves on a blank tape. It eventually exceeds every total computable function.
- A total function that bounds the running time of every halting machine: if $t$ were total computable and every machine that halts on the empty input halted within $t(|\langle M \rangle|)$ steps, the halting problem on the empty input would be decidable by simulation.
- See the [uncomputable function](/uncomputable-function/) page for more, and [countability](/countability/) for the count: there are uncountably many functions $\mathbb{N} \to \mathbb{N}$ and only countably many computable ones.

**Partial is not a defect.** The class of partial computable functions has a universal member $(e, x) \mapsto \varphi_e(x)$. The class of total computable functions has none: if $u(e, x)$ were a total computable function that listed all total computable functions as $u(e, \cdot)$, then $d(x) = u(x, x) + 1$ would be total computable and differ from each $u(e, \cdot)$ at $x = e$. This [diagonal argument](/diagonalization-argument/) is why the theory works with partial functions.

## Related definitions

- [Partial recursive function](/partial-recursive-function/) and [primitive recursive function](/primitive-recursive-function/): the definitions by recursion; the first class equals the computable functions.
- [Uncomputable function](/uncomputable-function/): the functions outside the class.
- [Decidable language](/decidable-language/): a language whose characteristic function is total computable. A [computably enumerable language](/recursively-enumerable-language/) is the domain of a computable function.
- [Many-one reducibility](/many-one-reducibility/): uses total computable functions as reductions.
- [Gödel numbering](/godel-numbering/), [s-m-n theorem](/s-m-n-theorem/) and [Kleene's recursion theorem](/kleene-recursion-theorem/): the theory of the indices $e$ of $\varphi_e$.
- [Turing completeness](/turing-completeness/): a system is Turing complete if it computes every computable function.
- [Computable real numbers](/computable-real-numbers/): reals whose digits, or rational approximations, a total computable function produces.

## References
