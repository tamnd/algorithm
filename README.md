# Algorithm

[![CI](https://github.com/tamnd/algorithm/actions/workflows/ci.yml/badge.svg)](https://github.com/tamnd/algorithm/actions/workflows/ci.yml)
[![Site](https://img.shields.io/badge/site-algorithm.tamnd.com-2b59c3)](https://algorithm.tamnd.com)
[![REUSE](https://img.shields.io/badge/REUSE-3.3-green)](https://reuse.software)

This repository is the content of [algorithm.tamnd.com](https://algorithm.tamnd.com). The site is a reference for algorithms and data structures. Each page gives the idea in plain words, a precise statement, pseudocode, a proof, tested code in ten languages and a visualization that you can step through.

The toolchain `algo` is in [tamnd/algorithm-agent](https://github.com/tamnd/algorithm-agent). The plan of the project is the [specification](https://algorithm.tamnd.com/spec/).

## What a node is

Each page comes from one directory under `nodes/`:

```text
nodes/sorting/comparison-sorts/merge-sort/
  node.md                 front matter and prose
  proofs/correctness.md   the proof for people
  impl/<language>/        the code and its tests
  viz/scene.ts            the visualization
  viz/presets.yaml        the inputs of the visualization
```

The kinds of node are algorithm, data structure, problem, technique, concept, definition, model, theorem and some more. The kind sets the sections of the page.

## Work on the content

1. Install the toolchain: `go install github.com/tamnd/algorithm-agent/cmd/algo@latest`.
2. Make a node: `algo new algorithm heap-sort -area sorting/comparison-sorts`.
3. Check your work: `algo check -changed origin/main`.
4. Run the tests of the code: `algo test -unsafe-local heap-sort`. Read the code first, because this runs it on your computer.
5. Check the scene: `algo viz check heap-sort`.
6. Look at the page: `algo site serve`, then open http://localhost:8150/heap-sort/.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you open a pull request.

## How the site is built

Each push to `main` runs the CI workflow. It runs the audit, the scene checks and the native tests of each language in its own job. Then it renders the site and deploys it to Cloudflare Pages. A pull request from this repository gets a preview site.

## Roadmap

The work is in six milestones, M0 to M5, from November 2026 to December 2028. [Spec 19](https://algorithm.tamnd.com/spec/19-milestones/) gives the goal and the exit criteria of each one. The [milestones](https://github.com/tamnd/algorithm/milestones) list the open issues. Issues with the label `good first issue` are small and clear.

## Licence

| Part | Licence |
| --- | --- |
| Prose | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Code, tests and scenes | [MIT](LICENSES/MIT.txt) |
| Lean proofs | [Apache 2.0](LICENSES/Apache-2.0.txt) |
| Metadata | [CC0 1.0](LICENSES/CC0-1.0.txt) |

[REUSE.toml](REUSE.toml) gives the licence of each path.
