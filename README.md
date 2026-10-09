# SwissKnife Action Hub

Community **action packs** for [SwissKnife](https://github.com/Nemu-x/SwissKnife-for-MS-Graph) —
the cross-platform Microsoft 365 administration runtime.

Browse and install them from the app: **Settings → Action packs → Action Hub**.

| Pack | Kind | What it does |
| --- | --- | --- |
| [security-basics](packs/security-basics) | Workflow | Compromised account response, shared-mailbox conversion, quick offboarding |
| [litigation-hold](packs/litigation-hold) | PowerShell | List mailboxes on litigation hold, turn the hold on or off |

## Two kinds of packs

- **Workflows** chain the app's own actions — no code. Each step is previewed,
  confirmed once and journaled like any built-in action. Prefer these.
- **PowerShell packs** add actions the app does not have. Scripts are full
  PowerShell running with the operator's admin connection, in their own process.

Either way, an installed pack runs only when it is **signed** by a key the
operator trusts, or after the operator **reviewed and trusted** its exact files.
Installing checks every file against the digest in [`index.json`](index.json).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The pack format is documented in the
[app repository](https://github.com/Nemu-x/SwissKnife-for-MS-Graph/tree/main/packs).
