---
tag: F009SS
kind: model
slug: warren-abstract-machine
name: Warren Abstract Machine
aliases:
- WAM
- Warren's Abstract Machine
area: logic-and-constraints/unification-and-resolution
level: research
summary: Warren's 1983 abstract machine for compiled Prolog. A heap, a stack, a trail and registers, with get, put, unify, call and try instructions that run SLD resolution under Prolog's control.
prereqs: [logic-programming, sld-resolution, robinson-unification]
see_also: [answer-substitution, occurs-check, chronological-backtracking, depth-first-search, horn-clause, random-access-machine, mark-and-sweep, cheney-copying-collector]
sources:
  - paper: "David H. D. Warren, An abstract Prolog instruction set, Technical Note 309, SRI International, Menlo Park, California (October 1983)"
    locator: the data areas, the registers, the instruction set and the compiled code examples
  - book: isbn:9780262510585
    title: "Hassan Aït-Kaci, Warren's Abstract Machine: A Tutorial Reconstruction, MIT Press (1991)"
    locator: Chapter 2 (M0, unification), Chapter 3 (M1 and M2, flat resolution and environments), Chapter 4 (M3, choice points), Chapter 5 (optimizations, indexing and cut, Figures 5.8, 5.9 and 5.18) and Appendix B (instructions and memory layout, pp. 97 to 117)
  - paper: "David H. D. Warren, Applied logic, its use and implementation as a programming tool, PhD thesis, University of Edinburgh (1977)"
    locator: the earlier DEC-10 Prolog compiler, which used structure sharing
  - paper: "Peter Van Roy, 1983 to 1993, the wonder years of sequential Prolog implementation, Journal of Logic Programming 19 and 20 (1994)"
    locator: the survey of Prolog systems built on, or departing from, the WAM
---

The Warren Abstract Machine (WAM) is an abstract machine for running Prolog, designed by David H. D. Warren and published in 1983 as an SRI technical note. A compiler translates each Prolog clause into a short sequence of WAM instructions, and an emulator or a native code generator executes them. The WAM implements [SLD resolution](/sld-resolution/) with Prolog's control: the leftmost atom is selected, clauses are tried in program order by [depth-first search](/depth-first-search/), failure undoes work by [chronological backtracking](/chronological-backtracking/), and unification omits the [occurs check](/occurs-check/). It is not a cost model for complexity analysis, as the [random access machine](/random-access-machine/) is; it is a model of how Prolog runs, given by its memory areas, registers and instructions. Aït-Kaci's tutorial (1991), which rebuilds the machine step by step, calls it "the de facto standard for implementing Prolog compilers".

## The machine

This section follows Aït-Kaci's reconstruction, which arrives at Warren's design through the machines M0 (unification of one query term with one program term), M1 (procedures and argument registers), M2 (conjunctions and environments) and M3 (backtracking), followed by optimizations.

**Cells and terms.** Terms are stored on the *heap* as tagged cells. The four tags are:

| cell | meaning |
|---|---|
| $\langle \mathrm{REF}, a \rangle$ | a variable; an unbound variable is a cell that refers to its own address $a$ |
| $\langle \mathrm{STR}, a \rangle$ | a pointer to a structure whose functor cell $f/n$ is at address $a$, followed by its $n$ argument cells |
| $\langle \mathrm{CON}, c \rangle$ | a constant $c$ |
| $\langle \mathrm{LIS}, a \rangle$ | a pointer to a list pair, with the head at $a$ and the tail at $a + 1$ and no functor cell |

For the query term $p(Z, h(Z, W), f(W))$, the compiler of M0 gives the code of Figure 2.3, with registers $X_1 = p(\ldots)$, $X_2 = Z$, $X_3 = h(Z, W)$, $X_4 = f(W)$ and $X_5 = W$:

```text
put_structure h/2, X3
set_variable X2
set_variable X5
put_structure f/1, X4
set_value X5
put_structure p/3, X1
set_value X2
set_value X3
set_value X4
```

The inner terms are built first, so that each `set_value` can refer to a term already on the heap. Running the code builds these 12 heap cells:

| address | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cell | STR 1 | h/2 | REF 2 | REF 3 | STR 5 | f/1 | REF 3 | STR 8 | p/3 | REF 2 | STR 1 | STR 5 |

Cells 2 and 3 are the unbound variables $Z$ and $W$, and the cells 6 and 9 share them.

**Memory areas.** In the final machine (Aït-Kaci, Appendix B), memory is divided, from low to high addresses, into:

- the *code area*, which holds the compiled program;
- the *heap*, which holds terms (Warren calls it the global stack);
- the *stack*, which holds environments and choice points (Warren calls it the local stack; Aït-Kaci describes it as an AND-stack and an OR-stack merged into one);
- the *trail*, which records the addresses of variables that must be reset to unbound on backtracking;
- the *PDL*, a push-down list that serves as the work stack of unification.

**Registers.**

| register | content |
|---|---|
| P | address of the next instruction |
| CP | continuation: where to go after the current procedure succeeds |
| S | address of the next argument of a structure, during head unification |
| H | top of the heap |
| HB | value of H at the latest choice point |
| E | the current environment |
| B | the latest choice point |
| B0 | the choice point to cut back to |
| TR | top of the trail |
| A1, A2, ... | argument registers, which also serve as temporary registers X1, X2, ... |

**Environments and choice points.** A clause whose body has more than one goal allocates an *environment* on the stack, a frame that holds the previous environment CE, the continuation CP, and the *permanent variables* $Y_1, \ldots, Y_n$. A variable is permanent if it occurs in more than one body goal, where the head counts as part of the first body goal; all other variables are *temporary* and live in the X registers. In M2 and M3 the frame also holds the count $n$; with environment trimming, the final machine reads the size from the second argument of the `call` instruction instead. A procedure with more than one candidate clause pushes a *choice point*, a frame that holds the number $n$ of arguments, the argument registers $A_1, \ldots, A_n$, the values of E and CP, the previous choice point B, the address BP of the next clause to try, the values of TR and H, and, once cut is added, the register B0.

**Instructions.** Each group of instructions does one part of a resolution step.

| group | instructions | role |
|---|---|---|
| put | `put_variable`, `put_value`, `put_unsafe_value`, `put_structure`, `put_list`, `put_constant` | load the arguments of a body goal into A registers |
| get | `get_variable`, `get_value`, `get_structure`, `get_list`, `get_constant` | unify the A registers with the arguments of a clause head |
| set | `set_variable`, `set_value`, `set_local_value`, `set_constant`, `set_void` | build the arguments of a structure on the heap, for body goals |
| unify | `unify_variable`, `unify_value`, `unify_local_value`, `unify_constant`, `unify_void` | match or build the arguments of a structure in a head |
| control | `allocate`, `deallocate`, `call P, N`, `execute P`, `proceed` | create and remove environments, call procedures, return |
| choice | `try_me_else L`, `retry_me_else L`, `trust_me`, `try L`, `retry L`, `trust L` | create, update and remove choice points |
| indexing | `switch_on_term V, C, L, S`, `switch_on_constant N, T`, `switch_on_structure N, T` | select the clauses by the first argument |
| cut | `neck_cut`, `get_level Yn`, `cut Yn` | remove choice points |

**Read and write mode.** A head argument $f(t_1, \ldots, t_n)$ compiles to `get_structure f/n, Ai` followed by $n$ `unify` instructions. If $A_i$ dereferences to an unbound variable, `get_structure` builds a new structure on the heap, binds the variable to it, and sets *write mode*, in which the `unify` instructions build the arguments. If $A_i$ is a structure with functor $f/n$, it sets S to its first argument and sets *read mode*, in which the `unify` instructions match the existing arguments. Otherwise it fails. One code sequence thus serves both a call that supplies the argument and a call that expects it as output. A `get_value` or a `unify_value` in read mode calls the general unification routine, which uses the PDL.

**Binding and trailing.** The `bind` operation makes one cell refer to the other, without the occurs check: in Aït-Kaci's words, "the occurs-check test is omitted in most actual Prolog implementations in order not to impede performance". A binding is recorded on the trail only if the variable is older than the latest choice point, that is, if its address is below HB on the heap or below B on the stack. Younger variables disappear on backtracking anyway.

**Compiled clauses.** For the rule `p(X, Y) :- q(X, Z), r(Z, Y).`, $Y$ and $Z$ are permanent and $X$ is temporary. Figure 5.9 of the tutorial gives:

```text
p/2: allocate 2
     get_variable Y1, A2
     put_variable Y2, A2
     call q/2
     put_value Y2, A1
     put_value Y1, A2
     deallocate
     execute r/2
```

Two optimizations show here. The value of $X$ arrives in $A_1$ and is passed on in $A_1$, so the pair `get_variable X3, A1` and `put_value X3, A1` of the plain M2 code (Figure 3.1) is removed (Figure 5.8). And *last call optimization* replaces `call r/2` followed by `deallocate` with `deallocate` followed by `execute r/2`, so the environment is freed before the last call, which then reuses the continuation of `p`.

For list joining, `conc([], L, L).` and `conc([H | T], L, [H | R]) :- conc(T, L, R).`, Figure 5.18 gives:

```text
conc/3: switch_on_term C1a, C1, C2, fail
C1a:    try_me_else C2a
C1:     get_constant [], A1
        get_value A2, A3
        proceed
C2a:    trust_me
C2:     get_list A1
        unify_variable X4
        unify_variable A1
        get_list A3
        unify_value X4
        unify_variable A3
        execute conc/3
```

`switch_on_term` dispatches on the first argument: a variable goes to `C1a`, which tries both clauses with a choice point; the constant `[]` goes to `C1`; a list goes to `C2`; a structure fails. The second clause needs no environment and no instruction for its second argument, since $L$ is already in $A_2$ for the recursive call, and $T$ and $R$ are unified directly into $A_1$ and $A_3$.

## What it counts

The WAM is used to describe execution, not to state complexity bounds, and neither Warren nor Aït-Kaci defines a cost function. Its natural units are these:

- **Instructions.** Most instructions do a bounded amount of work. The exceptions are dereferencing, which follows a chain of REF cells, and general unification in `get_value` and `unify_value`, which walks both terms with the PDL.
- **Calls.** Each `call` or `execute` is one SLD resolution step. Prolog systems are often compared in logical inferences per second, where one inference is one call.
- **Space.** The heap grows with the terms built, and shrinks only on backtracking, when H is reset from the choice point, or by garbage collection. The stack holds environments and choice points; an environment can be popped at `deallocate` only if no newer choice point still needs it. The trail grows by one entry for each conditional binding.

## Relation to other models

- **SLD resolution.** A run of the WAM is a depth-first walk of the SLD tree of the query under the leftmost computation rule. The current goal list is the code at P together with the chain of continuations in CP and the environments. The choice point stack holds the unexplored branches. On failure, the machine returns to the latest choice point, restores the registers from it, resets H, and unbinds the variables recorded on the trail after TR. The [answer substitution](/answer-substitution/) of a refutation is read from the bindings of the query variables when the query code reaches its end.
- **Random access machine.** Each WAM instruction can be carried out by a [random access machine](/random-access-machine/) program, so the WAM is an intermediate layer between Prolog and real hardware, and native code compilers translate WAM code further.
- **Earlier Prolog implementations.** Warren's DEC-10 Prolog compiler (1977) represented terms by structure sharing, where a term is a skeleton together with a frame of variable values. The WAM represents terms by structure copying: a term built by a goal is copied onto the heap.
- **Garbage collection.** The heap order carries meaning in the WAM: the trail test compares addresses with HB, and backtracking resets H. A collector must keep this order. A plain [copying collector](/cheney-copying-collector/) does not keep it, so WAM-based systems mostly use mark-and-compact collectors in the style of [mark-and-sweep](/mark-and-sweep/) that slide live cells and keep their order.
- **Later machines.** Many Prolog systems start from the WAM and extend it, for example with tabling, constraints or attributed variables, or replace it with other designs. Van Roy (1994) surveys this period.

## Known results in the model

- **Correctness by refinement.** Aït-Kaci derives the full WAM in stages, from M0, which only unifies one query term with one program term, to M3, which runs pure Prolog with backtracking, and then adds the optimizations one by one. Each stage adds one feature to the previous one, and the tutorial explains why the new code keeps the old behaviour. Machine-checked and mathematical correctness proofs of WAM compilers were given later, among them by Russinoff (1992) and by Börger and Rosenzweig (1995).
- **Constant stack space for deterministic tail recursion.** With last call optimization, a clause frees its environment before its last call, so a recursion whose last goal is the recursive call does not grow the stack. With first-argument indexing, `conc/3` called with a list as first argument creates no choice point, since `switch_on_term` jumps directly to the matching clause. Together, these make the loop run in constant stack space; only the heap grows, by the output list. Aït-Kaci notes that last call optimization generalizes tail recursion optimization, because it applies to the last call of every clause, not only to a recursive one.
- **Unsoundness without the occurs check.** Since `bind` omits the occurs check, the program `eq(Y, Y).` with the query `?- eq(X, f(X)).` succeeds and binds $X$ to a cyclic term, although $X = f(X)$ has no solution among finite terms. This is the standard behaviour of Prolog, and it is what the occurs check pages discuss.
- **Cut.** `neck_cut` removes the choice points created since the procedure was called, using B0; `get_level Yn` saves B0 in a permanent variable and `cut Yn` later restores B from it, for a cut deeper in the body.
- **Differences in Warren's original.** Warren's 1983 note has the extra instructions `put_nil`, `get_nil` and `unify_nil` for the empty list, does not store the arity in choice points, and uses the `unify` instructions in both the query and the head, with no separate `set` instructions. Aït-Kaci's Section 5.3, a note on set instructions, explains the last of these choices.

## References
