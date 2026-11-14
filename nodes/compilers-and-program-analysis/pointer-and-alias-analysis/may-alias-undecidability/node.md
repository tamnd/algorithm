---
tag: QGWZHP
kind: theorem
slug: may-alias-undecidability
name: Undecidability of may-alias analysis
aliases:
- Landi's theorem
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Precise intraprocedural may-alias analysis is undecidable for languages with recursive data structures and pointers.
prereqs: [alias-analysis, post-correspondence-problem, undecidability]
see_also: [flow-insensitive-alias-np-hardness, rice-theorem, halting-problem, points-to-analysis, shape-analysis, separation-logic, flow-sensitivity, andersen-analysis]
sources:
  - paper: "William Landi, Undecidability of static analysis, ACM Letters on Programming Languages and Systems 1(4), 323 to 337 (1992)"
    locator: the main theorems (intraprocedural may-alias is not recursive and must-alias is not recursively enumerable, for languages with dynamic storage and recursive data structures)
  - paper: doi:10.1145/186025.186041
    title: G. Ramalingam, The undecidability of aliasing, ACM Transactions on Programming Languages and Systems 16(5), 1467 to 1471 (1994)
    locator: whole paper (the reduction from the Post correspondence problem)
  - paper: "Emil L. Post, A variant of a recursively unsolvable problem, Bulletin of the American Mathematical Society 52(4), 264 to 268 (1946)"
    locator: the correspondence problem and the proof that it is unsolvable
  - paper: doi:10.1145/604131.604142
    title: Venkatesan T. Chakaravarthy, New results on the computability and complexity of points-to analysis, Proceedings of the 30th ACM Symposium on Principles of Programming Languages (POPL 2003), 115 to 125
    locator: the undecidability of points-to analysis with dynamic memory when all variables are scalars
  - paper: doi:10.1145/1353445.1353447
    title: Noam Rinetzky, G. Ramalingam, Mooly Sagiv and Eran Yahav, On the complexity of partially-flow-sensitive alias analysis, ACM Transactions on Programming Languages and Systems 30(3), Article 13 (2008)
    locator: the summary of earlier results (flow-sensitive may-alias without dynamic allocation is PSPACE-complete)
---

Precise may-alias analysis is [undecidable](/undecidability/) as soon as a program can allocate cells and link them into data structures of any size. No algorithm takes every program, a point in it and two pointer expressions, and always answers correctly whether some execution makes the two expressions name the same cell at that point. Landi proved this in 1992, together with the stronger fact that precise must-alias is not even recursively enumerable. Ramalingam gave a short proof in 1994 by a reduction from the [Post correspondence problem](/post-correspondence-problem/). The result holds even when every path through the control flow graph counts as executable, so it does not come from branch conditions. It comes from the heap.

## Statement

**Programs.** A program has pointer variables and one kind of cell with two pointer fields, `left` and `right`. Its statements are

- `p = new`, which makes a new cell with both fields null and stores its address in `p`;
- `p = q`, `p = null`, `p = q.f` and `q.f = p`, where `f` is `left` or `right`.

The control flow graph has no branch conditions: at a branch, any successor may follow. So every path from the entry is executable, except that a statement that reads or writes a field through a null pointer stops the run, and such a path reaches no later point. At the start every variable is null.

**Aliases.** Two pointer expressions $e_1$ and $e_2$ *alias* in a state when both hold the address of the same cell. Two null values do not alias.

- *May-alias:* given a program, a point $X$ and two expressions, does some path from the entry to $X$ end in a state where they alias?
- *Must-alias:* do they alias at the end of every path from the entry to $X$?

**Theorem (Landi 1992; Ramalingam 1994).**

1. May-alias is recursively enumerable but not decidable.
2. Must-alias is not recursively enumerable.

Both hold for intraprocedural programs in the language above.

## In plain words

A compiler often wants to know whether two pointers can ever point to the same memory cell at some point of a program. This theorem says that no algorithm can always answer this exactly. The proof turns a famous unsolvable puzzle into a program. The program builds a chain of cells of any length. Then two pointers walk down the chain, each guided by one half of the puzzle. The two pointers can meet at the same cell only if the puzzle has a solution. So an exact alias checker would solve the puzzle, which is impossible. This is why every practical alias analysis gives an approximate answer that is safe, not an exact one.

## Proof

**The source problem.** An instance of the Post correspondence problem (PCP) is a list of pairs of non-empty words $(w_1, z_1), \ldots, (w_k, z_k)$. A *solution* is a sequence $i_1, \ldots, i_m$ with $m \ge 1$ and $w_{i_1} \cdots w_{i_m} = z_{i_1} \cdots z_{i_m}$. Post (1946) proved that no algorithm decides whether a solution exists. The problem stays undecidable over the two letters `L` and `R`, since each letter of a larger alphabet can be written as a block of `L` and `R` of a fixed length. Whether a solution exists is recursively enumerable: try all sequences, shortest first.

**The program.** For a PCP instance over `L` and `R`, build the program below. To *walk* `p` along a word means to run `p = p.left` for each `L` and `p = p.right` for each `R`, in order. Each `choose` line is a branch to any of the listed blocks.

```
start:  root = new
        c = root
        choose grow_l grow_r walk
grow_l: n = new
        c.left = n
        c = n
        choose grow_l grow_r walk
grow_r: n = new
        c.right = n
        c = n
        choose grow_l grow_r walk
walk:   p = root
        q = root
pick:   choose pair_1 ... pair_k
pair_i: walk p along w_i
        walk q along z_i
        choose pick X
X:      (the question point)
```

The first part builds a chain of cells. Let $b$ be the word of the turns it took, `L` for `grow_l` and `R` for `grow_r`. The chain has one cell for each prefix $u$ of $b$, the root for the empty prefix, and the cell for $u$ links by its field $\ell$ to the cell for $u\ell$ when $u\ell$ is a prefix of $b$. Every other field is null. The second part picks a sequence $i_1, \ldots, i_m$ with $m \ge 1$, one index each time it passes through `pick`.

**Lemma.** On a path that reaches `X`, `p` holds the cell for the word $W = w_{i_1} \cdots w_{i_m}$ if $W$ is a prefix of $b$, and null if $W = u\ell$ for a prefix $u$ of $b$ and a letter $\ell$ such that $u\ell$ is not a prefix of $b$. No other case reaches `X`.

*Proof.* Walking from the cell for $u$ by the letter $\ell$ gives the cell for $u\ell$ if $u\ell$ is a prefix of $b$, and null otherwise. The next step from null reads a field through null and stops the run. The same holds for `q` with $Z = z_{i_1} \cdots z_{i_m}$. $\square$

**May-alias is undecidable.** Ask whether `p` and `q` may alias at `X`.

*If the instance has a solution* $i_1, \ldots, i_m$, let $u = w_{i_1} \cdots w_{i_m} = z_{i_1} \cdots z_{i_m}$. Take the path that grows the chain along $u$, so $b = u$, and then picks $i_1, \ldots, i_m$. Every position of `p` and `q` on the way is the cell of a prefix of $u$, so no step reads through null, and at `X` both hold the cell for $u$. They alias.

*If `p` and `q` alias at `X`* at the end of some path, both hold the same cell. By the lemma that cell is the one for $W$ and also the one for $Z$. Different prefixes of $b$ have different cells, so $W = Z$, and the indices picked on the path are a solution.

So the program and the question can be built from the instance by an algorithm, and the answer is yes exactly when the instance has a solution. A decision procedure for may-alias would decide PCP, which is impossible.

**May-alias is recursively enumerable.** Each path determines the run completely, because the language has no input and no conditions. List all paths from the entry to $X$, shortest first, run each one and answer yes when one ends with the two expressions aliased. This answers yes on every yes instance and runs forever on the others. A recursively enumerable problem whose complement is also recursively enumerable is decidable, so the complement, "the two expressions never alias at $X$", is not recursively enumerable. $\square$

**Must-alias is not recursively enumerable.** Extend the program after `X`:

```
X:      x = new
        y = new
        p.left = x
        q.left = y
        t = p.left
Y:      (the question point)
```

A path reaches `Y` only if `p` and `q` are not null at `X`, since the stores through them would stop the run. After the stores, `t` holds `y` if `p` and `q` alias, and `x` otherwise. So `t` and `x` alias at the end of every path to `Y` exactly when no path makes `p` and `q` alias at `X`, which by the proof above is exactly when the PCP instance has no solution. "No solution" is the complement of a recursively enumerable problem that is not decidable, so it is not recursively enumerable, and must-alias is not either. $\square$

## Consequences

**Every practical alias analysis approximates.** A sound may-alias analysis answers yes on every pair that may alias and on some pairs that never do. A sound must-alias analysis answers yes only on pairs that must alias and misses some. The usual approximations drop exactly what the proof uses. An allocation-site abstraction keeps one abstract cell for each `new` statement, so the chain of the proof becomes one cell that points to itself, and [Andersen's analysis](/andersen-analysis/) then says that `p` and `q` may alias, which is sound but not precise. A flow-insensitive analysis drops the order of the statements. A $k$-limited analysis keeps access paths up to length $k$ only. [Shape analysis](/shape-analysis/) and [separation logic](/separation-logic/) keep more of the heap structure, but they too must approximate.

**Points-to analysis inherits the result.** Two pointers alias exactly when they point to the same cell, so precise points-to questions about concrete cells are undecidable too. Chakaravarthy (2003) showed that the points-to question stays undecidable with dynamic memory even when all variables are scalars, without records.

**Rice's theorem is a different reason.** If branch conditions are evaluated, then even the question whether a point is reached is the [halting problem](/halting-problem/), and [Rice's theorem](/rice-theorem/) makes every nontrivial question about runs undecidable. The theorem here is stronger: it holds when every path is executable, which is the usual assumption of data-flow analysis.

## Tightness

**Without dynamic allocation the problem is decidable.** If the program cannot allocate, the set of states is finite, and a search over states answers both questions. Flow-sensitive may-alias is then PSPACE-complete (Landi 1992 and Muth and Debray 2000, as summarized by Rinetzky et al. 2008).

**Without order, it is still hard.** If the order of statements is ignored and there is no dynamic memory, the precise question is decidable but [NP-hard](/flow-insensitive-alias-np-hardness/).

**The degree of undecidability is exact.** May-alias is recursively enumerable, so it is not harder than the halting problem. Must-alias is co-recursively-enumerable: a path that ends with the two expressions not aliased is a finite witness that the answer is no.

## History

Landi's 1992 paper in LOPLAS studied static analysis for languages with pointers and showed that precise intraprocedural may-alias with recursive data structures is not recursive, and that must-alias is not recursively enumerable. Ramalingam's short note of 1994 gave the short reduction from PCP that this page follows, for programs where all paths are executable. The program on this page is written for this page in Ramalingam's style. Chakaravarthy (2003) removed the need for records, and later work, such as Rinetzky, Ramalingam, Sagiv and Yahav (2008), mapped the complexity of restricted cases.

## References
