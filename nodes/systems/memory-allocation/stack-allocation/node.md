---
tag: 2NC7TG
kind: technique
slug: stack-allocation
name: Stack allocation
aliases:
- stack discipline allocation
- LIFO allocation
- mark-release allocation
area: systems/memory-allocation
level: intro
summary: "Allocate by a bump of the top pointer and free in last-in-first-out order, as call frames do. Freeing moves top back. alloca and escape analysis put more data on the stack."
prereqs: [stack, allocator]
see_also: [bump-pointer-allocation, arena-allocation, region-based-memory-management, recursion, memory-pool, copying-collection, reference-counting, free-list]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 7.2, Stack allocation of space (activation trees, activation records, calling sequences and variable-length data on the stack)
  - paper: "Jong-Deok Choi, Manish Gupta, Mauricio Serrano, Vugranam C. Sreedhar and Samuel Midkiff, Escape analysis for Java, OOPSLA 1999"
    locator: the connection graph, and the use of escape analysis to allocate objects that do not escape a method on its stack frame
  - paper: "Edsger W. Dijkstra, Recursive programming, Numerische Mathematik 2, 1960, 312-318"
    locator: the stack of activation data for recursive procedures in ALGOL 60
  - paper: doi:10.1016/0020-0190(87)90175-X
    title: Andrew W. Appel, Garbage collection can be faster than stack allocation, Information Processing Letters 25(4), 1987, 275-279
    locator: the comparison of the cost of popping stack frames with the cost of copying collection
---

*Stack allocation* is allocation with a [stack](/stack/) discipline: the block that was allocated last is freed first. One pointer, *top*, divides the used part of a range from the free part. To allocate, move top up by the size, as in [bump-pointer allocation](/bump-pointer-allocation/). To free, move top back. Both steps take $O(1)$ time, and there is no free list and no fragmentation. Call frames are the main use: each call of a procedure gets a frame for its locals on the *call stack*, and the return frees it. The rule is strict: a block can live no longer than every block above it. Compilers put more data on the stack in two ways: with `alloca` and variable-length arrays, and with *escape analysis*, which proves that an object never outlives the call that makes it.

## In plain words

Think of a stack of trays in a canteen. You put a tray on top and you take a tray from the top. You never pull one out of the middle.

Memory can work the same way. When a function starts, it takes a piece of memory on top of the pile for its own data. When it ends, it gives back that piece, which is always the top one, because any function it called has already ended. So giving back is just moving a pointer down. Nothing needs to be searched, and no gaps are left behind.

## When it applies

- Lifetimes nest: each block dies before every block that was made before it. Procedure calls give this order, because a call returns before its caller does.
- The size of each block is known when it is made, and the total stays under a known bound, the size of the stack.
- No pointer to a block is used after the block is freed. For locals this means that the address of a local must not escape its procedure.
- The program has phases that can be undone, such as the temporary data of a search, which a *mark* and a *release* free in one step.

## The template

The range is $[base, limit)$, and top starts at $base$. BLOCKS is a stack of the starts of the live blocks; a real call stack keeps it implicit in the frames, but it lets the allocator check the LIFO rule.

```pseudo id=main
STACK-ALLOC(n)
L1  if top + n > limit then return FAIL                ▷ stack overflow
L2  push top on BLOCKS; p ← top; top ← top + n; return p

STACK-FREE(p)
L3  if BLOCKS is empty or the top of BLOCKS ≠ p then error: not last in, first out
L4  pop BLOCKS; top ← p

MARK()
L5  return (top, the size of BLOCKS)

RELEASE((t, k))                                        ▷ free all blocks made after the mark
L6  pop BLOCKS down to k entries; top ← t
```

A call frame is a mark followed by an allocation for the fixed locals. `alloca(n)` is STACK-ALLOC in the current frame, and the return of the procedure is RELEASE of the frame's mark, which also frees every `alloca` block of the frame. The live blocks are always packed from $base$ to top in the order of their allocation, so a free that follows the rule leaves no hole.

## Classic examples

**A worked run.** A stack of 100 bytes from address 0. A procedure f has 16 bytes of locals and calls g, which has 24.

| step | call | result | top after | live blocks |
|---|---|---|---|---|
| 1 | enter f (16) | 0 | 16 | 0 |
| 2 | alloca(10) in f | 16 | 26 | 0, 16 |
| 3 | enter g (24) | 26 | 50 | 0, 16, 26 |
| 4 | alloca(30) in g | 50 | 80 | 0, 16, 26, 50 |
| 5 | free(16) | error | 80 | 16 is not the last block |
| 6 | leave g | | 26 | 0, 16 |
| 7 | alloc(80) | FAIL | 26 | $26 + 80 > 100$: overflow |
| 8 | alloc(20) | 26 | 46 | 0, 16, 26 |
| 9 | free(26), leave f | | 0 | none |

Step 6 frees the frame of g and its `alloca` block in one step. Step 8 reuses the same addresses for new data. The page's tests check the allocator against a plain list model on seeded random runs, including frees out of order, which must raise an error.

**Call stacks.** Since ALGOL 60, compilers keep the activation records of procedures on a stack, which makes recursion work: each call of a recursive procedure has its own frame. Dijkstra described this run-time stack for ALGOL 60 in 1960. The [recursion](/recursion/) of most programming languages still rests on it.

**alloca and variable-length arrays.** The C function `alloca(n)`, found in many C libraries but in no C standard, allocates $n$ bytes in the caller's frame. C99 variable-length arrays do the same with a size known only at run time. Both are freed when the function returns.

**Escape analysis.** A compiler for a language with a heap can prove that an object does not *escape*: no pointer to it is stored in the heap, in a global or in the return value. Then the object can live in the frame of the procedure that makes it. Choi, Gupta, Serrano, Sreedhar and Midkiff (1999) built a *connection graph* for each Java method to find such objects, and used the same analysis to remove locks on objects that only one thread can reach. The Go compiler uses escape analysis to decide which values can live on the stack, and the HotSpot Java compiler uses it to replace objects that do not escape by their fields and to remove locks.

**Mark and release.** Some Pascal systems offered `mark` and `release` on the heap, and GNU obstacks free back to a saved object. Backtracking search can save a mark before each choice and release it when it undoes the choice.

## Variations

- **Downward stacks.** Most hardware stacks grow toward lower addresses: allocation subtracts from the stack pointer and the return adds back.
- **Segmented stacks.** A stack can be a list of chunks, so that it grows past one chunk, at the cost of a check on each call. Some language runtimes do this for their threads.
- **Regions as a stack.** [Region-based memory management](/region-based-memory-management/) keeps a stack of regions instead of a stack of blocks. Each region can grow while it is open, and it is freed when its scope ends.
- **Arenas with a mark.** An [arena](/arena-allocation/) that supports mark and release is a stack of objects over a list of chunks.
- **Stacks of frames on the heap.** For closures and coroutines whose frames must outlive a call, some systems put frames on the heap and let a garbage collector free them. Appel (1987) argued that with a copying collector and enough memory this can cost less than popping stack frames.

## Pitfalls

- **Returning the address of a local.** A pointer to a local of a procedure is invalid after it returns, and the next call reuses the memory. This is the classic dangling-pointer bug of C.
- **Stack overflow.** Deep recursion or a large `alloca` passes the limit. Many systems put an unmapped guard page below the stack, which a single large allocation can jump over.
- **alloca in a loop.** Each `alloca` lives until the function returns, not until the end of the loop body, so a loop can use up the stack.
- **Freeing out of order.** A stack allocator that does not check the order frees the wrong memory without any sign. Check it in debug builds.
- **Unsound escape analysis.** If the analysis misses one way an object escapes, such as a store by native code or by reflection, a frame object can be used after its frame is gone.

## Exercises

1. Show that the live blocks of a stack allocator are always packed from base to top, so that it has no external fragmentation.
2. A procedure allocates an object, stores it in a field of another object made in the same call, and returns neither. Can both objects live on the stack?
3. Write a recursive tree walk and its frames as calls of STACK-ALLOC and RELEASE. How many bytes of stack does a tree of height $h$ need?
4. Why must `alloca` be freed only at the return of its function, and not at the end of the block that calls it, in C?
5. Give a sequence of allocations and frees whose lifetimes do not nest. Which allocator would you use for it?

## References
