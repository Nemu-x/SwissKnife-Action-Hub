# Contributing a pack

1. Add a folder `packs/<name>/` with a `manifest.yaml` (the folder is named like
   the pack). Give it `title`, `summary` and a `category`:
   `security`, `exchange`, `hr`, `teams`, `intune`, `reports` or `other`.
2. Prefer a **workflow** (built-in actions, no code). Add PowerShell only for
   what no built-in action does, and keep scripts short and readable.
3. Test it in the app: copy the folder into **Settings → Action packs → Open
   folder**, trust it, run the preview against a test tenant.
4. Rebuild the index and commit both:

   ```
   pip install pyyaml
   python tools/build_index.py
   ```

5. Open a pull request. Reviewers read every line: what it changes, which
   permissions it needs, and that a plan step never writes.

Rules: no obfuscated code, no downloads or external calls from scripts, no
secrets in files, English labels required (Russian welcome). Files are stored
byte-exact (`.gitattributes`), so do not let an editor rewrite line endings
after building the index.
