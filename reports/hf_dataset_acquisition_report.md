# Hugging Face Dataset Acquisition Report

## Result

- Date: 2026-10-09 (Asia/Shanghai session)
- WP scope: WP1 candidate data acquisition only
- Hugging Face repository: `HuggingFaceH4/tau2-bench-data`
- Pinned Hugging Face revision: `ec3f3dbee04ce793378e0eb48b6dc258b01fdc69`
- Local destination: `datasets/huggingface/HuggingFaceH4/tau2-bench-data/ec3f3dbee04ce793378e0eb48b6dc258b01fdc69/`
- Cache destination: `.workspace_cache/huggingface/` plus repository-local HF metadata
- Download status: completed
- Model/Agent/Embedding API calls: 0

## Source selection and limitations

The Hugging Face connector's dataset-search operation was disabled by its server configuration. Discovery therefore fell back to Hugging Face Hub pages and the Dataset Viewer workflow described by the installed Hugging Face skill.

`HuggingFaceH4/tau2-bench-data` was selected because its dataset card states that it contains domain data from `sierra-research/tau2-bench`, covers the required task files, declares an MIT license, and is small enough for a guarded workspace-local download. It is nevertheless a Hugging Face H4 mirror, not the official Sierra code checkout.

The Dataset Viewer cannot fully build this repository because heterogeneous JSON files have incompatible columns. The pinned raw repository files were therefore downloaded directly rather than using generated Viewer Parquet files.

The dataset card declares `license: mit`, but the downloaded revision contains no standalone `LICENSE` file. License evidence is therefore limited to the repository metadata/card and must be reconciled against the official upstream checkout before final WP1 publication.

## Workspace and network controls

- Free space before acquisition: 107.63 GiB on `D:`.
- All Hugging Face, XDG, Python, and temporary paths were redirected beneath the effective project root.
- The first sandboxed CLI request timed out connecting to `huggingface.co` and produced no payload.
- After explicit network approval, the identical pinned-revision command succeeded.
- No floating `main` revision was used for the download.
- Post-download reparse-point scan found no symbolic links or junctions in the dataset snapshot.

## Downloaded payload validation

- Payload files excluding HF local metadata: 34
- Payload bytes: 26,252,336 (approximately 25.04 MiB)
- HF metadata files: 34
- Distinct revision values in local HF metadata: only `ec3f3dbee04ce793378e0eb48b6dc258b01fdc69`
- Revision consistency check: passed

Static task-file validation:

| Domain | Rows | Unique IDs | Blank IDs | Task-file SHA256 |
|---|---:|---:|---:|---|
| airline | 50 | 50 | 0 | `40d692b3fca780f46b56d48b447fd8db79a653f216667b8ed7c1a88380544532` |
| retail | 114 | 114 | 0 | `76e1fa649a359bef2d2fd30eae834b99d261d84e2e5d364856f6632fdf778dfd` |
| telecom | 114 | 114 | 0 | `192a2c143b3b512c37c3775fdf6c5040c33717388620c38b140c731dc6153cd7` |

The complete 34-file SHA256 inventory is stored in:

`datasets/huggingface/manifests/HuggingFaceH4_tau2-bench-data_ec3f3dbee04ce793378e0eb48b6dc258b01fdc69.json`

Manifest SHA256 at creation: `ea73572980826249723553ca19f590583dc644bd1b9897c1faadca6d465492c6`.

## WP1 decision

Status: `CANDIDATE_SOURCE_ONLY`.

This snapshot is suitable for static schema exploration, content hashing, and adapter development. It is not sufficient for final `CuratedTaskRegistry-v1` because it does not establish the official upstream benchmark commit and does not include the executable runner, tools, evaluator/grader implementation, reset machinery, or prefix-replay environment required by WP1.

WP2 remains out of scope.

