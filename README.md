# git-learn

Hands-on Git sandbox. Work in this repo. Do the tasks in order. Each task: edit a file, run commands, check the result.

## Setup (once)

1. Configure Git:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
2. Point Git at the repo hooks:
   ```
   git config core.hooksPath .githooks
   ```
3. Confirm tests pass:
   ```
   python3 test_app.py
   ```
   Expected output: `ok`.

---

## Task 1: Your first commit (edit code first)

1. Open `app.py`. Add a new function at the bottom:
   ```python
   def multiply(a, b):
       return a * b
   ```
2. See what changed (nothing staged yet):
   ```
   git status
   git diff
   ```
3. Stage the file:
   ```
   git add app.py
   ```
4. Now `git diff` shows nothing. See staged changes instead:
   ```
   git diff --staged
   ```
5. Commit:
   ```
   git commit -m "add multiply()"
   ```
6. Check history:
   ```
   git log --oneline
   ```

---

## Task 2: Stage individual hunks

1. Open `app.py`. Make two separate edits:
   - Change `add` to:
     ```python
     def add(a, b):
         return a + b  # addition
     ```
   - Add at the bottom:
     ```python
     def divide(a, b):
         return a / b
     ```
2. Stage only one hunk interactively:
   ```
   git add -p
   ```
   Answer `y` to one hunk, `n` to the other.
3. Verify split state:
   ```
   git diff          # the unstaged hunk
   git diff --staged # the staged hunk
   ```
4. (Optional) Finish staging everything and commit:
   ```
   git add app.py
   git commit -m "annotate add and add divide"
   ```

---

## Task 3: Amend the last commit

1. You forgot a file or want a better message. Run:
   ```
   git commit --amend -m "better message"
   ```
2. Check history:
   ```
   git log --oneline
   ```
   The previous commit hash is replaced, not duplicated.

---

## Task 4: Branch, merge, and resolve a conflict

1. Create and switch to a branch:
   ```
   git switch -c feature
   ```
2. Edit `app.py`: change `add` to return `a + b + 0`. Commit:
   ```
   git add app.py
   git commit -m "tweak add on feature"
   ```
3. Switch back and make a conflicting edit on `main`:
   ```
   git switch main
   ```
   Edit `app.py`: change `add` to return `a + b + 1`. Commit:
   ```
   git add app.py
   git commit -m "tweak add on main"
   ```
4. Merge (conflict expected):
   ```
   git merge feature
   ```
5. Open `app.py`, resolve the `<<<<<<<` conflict markers, keep one version. Then:
   ```
   git add app.py
   git commit
   ```
6. Verify:
   ```
   git log --oneline --graph --all
   ```

---

## Task 5: Rebase (replay commits onto a new base)

Rebase takes the commits unique to your branch and replays them on top of another commit.
It does not create a merge commit; it recreates each commit (new hashes) and leaves a
straight, linear history. Use it to keep a feature branch current with `main` and to clean
up local commits before sharing them.

### Part A — Rebase a branch onto updated `main`

1. Start from a clean state on `main`:
   ```
   git switch main
   git status
   git log --oneline --graph --all
   ```
2. Create a demo branch from an older commit so it diverges from `main`:
   ```
   git switch -c rebase-demo <hash>
   ```
   (`<hash>` should be the hash of a past commit.)
3. Add two commits on the demo branch:
   - Edit `app.py`, add:
     ```python
     def subtract(a, b):
         return a - b
     ```
     then:
     ```
     git add app.py
     git commit -m "add subtract"
     ```
   - Edit `app.py`, add:
     ```python
     def power(a, b):
         return a ** b
     ```
     then:
     ```
     git add app.py
     git commit -m "add power"
     ```
4. Inspect the fork:
   ```
   git log --oneline --graph --all
   ```
   `rebase-demo` sits two commits ahead of the old base while `main` went a different way.
5. Replay the demo commits onto current `main`:
   ```
   git rebase main
   ```
   Git rewinds to the common ancestor, then applies "add subtract" and "add power" on top
   of `main`.
6. Verify the result:
   ```
   git log --oneline --graph --all
   ```
   The demo commits now sit directly on top of `main` with new hashes; no merge commit was
   created. `app.py` contains both new functions plus everything from `main`.
   ```
   python3 test_app.py
   ```

If a commit conflicts with changes on `main`:
- Git stops and prints `CONFLICT`. Run `git status` to see the file.
- Open the file, resolve the `<<<<<<<` / `=======` / `>>>>>>>` markers, keep the intended code.
- Stage: `git add app.py`
- Continue: `git rebase --continue` (an editor opens for the commit message; save and close).
- Abandon and restore the branch to before the rebase: `git rebase --abort`.
- Skip the current commit entirely: `git rebase --skip`.

### Part B — Interactive rebase (clean up local commits)

Only use on commits that have not been pushed/shared.

1. Make sure you are on `rebase-demo` (after Part A) and add one more commit:
   - Edit `app.py`, add:
     ```python
     def clamp(x, lo, hi):
         return max(lo, min(hi, x))
     ```
   - Then:
     ```
     git add app.py
     git commit -m "add clamp"
     ```
2. Start an interactive rebase over the commits after `main`:
   ```
   git rebase -i main
   ```
   Your editor opens a todo list like:
   ```
   pick <hash> add subtract
   pick <hash> add power
   pick <hash> add clamp
   ```
3. Change commands to reshape history, for example combine the last two and rename the first:
   ```
   reword <hash> add subtract
   squash <hash> add power
   fixup  <hash> add clamp
   ```
   Commands:
   - `pick` = keep the commit as-is
   - `reword` = keep the commit, edit its message
   - `edit` = pause to amend the commit
   - `squash` = combine into the previous commit, edit the combined message
   - `fixup` = combine into the previous commit, discard this message
   - `drop` = remove the commit
   - `exec <cmd>` = run a command between commits
4. Save and close. Git applies the plan; editors may open for reword/squash messages.
   Save each one.
5. Verify:
   ```
   git log --oneline
   git diff main..rebase-demo
   ```
   Fewer commits, but the final code is unchanged.

### Part C — Transplant a range (`--onto`)

Move commits that are on `oldbase..branch` onto a different base:
```
git rebase --onto <new-base> <old-base> <branch>
```
Example: take only the demo commits and replay them onto `origin/main` instead of local `main`.

### Safety rules

- Never rebase commits that have been pushed to a shared branch; rewriting public history
  forces collaborators to recover.
- Create a backup first if unsure: `git branch backup-rebase-demo`.
- Recovery after a bad rebase: `git reflog`, then `git reset --hard <hash>` (see Task 8).

---

## Task 6: Cherry-pick

1. Find a commit hash:
   ```
   git log --oneline
   ```
2. Copy that commit onto current branch:
   ```
   git cherry-pick <hash>
   ```

---

## Task 7: Stash

1. Edit `app.py` but do not commit.
2. Shelve changes:
   ```
   git stash
   git stash list
   ```
3. Restore:
   ```
   git stash pop
   ```

---

## Task 8: Undo safely

Shared/pushed branches (safe, keeps history):
```
git revert <hash>
```

Local, unpushed only:
```
git reset --soft HEAD~1   # keep changes staged
git reset --mixed HEAD~1  # keep changes unstaged (default)
git reset --hard HEAD~1   # discard changes
```

Recover after a bad reset/rebase:
```
git reflog
git reset --hard <hash>
```

---

## Task 9: Inspection

```
git diff
git log --oneline --graph --all
git blame app.py
```

---

## Task 10: Bug hunting with bisect

1. Edit `app.py`: introduce a bug in `add` (e.g. `return a - b`). Commit:
   ```
   git add app.py
   git commit -m "break add"
   ```
2. Start bisect:
   ```
   git bisect start
   git bisect bad            # current commit is broken
   git bisect good <hash>    # a known good commit
   git bisect run python3 test_app.py
   git bisect reset
   ```

---

## Task 11: Remote sync and publishing

Sync:
```
git remote -v
git fetch                 # download updates, don't merge
git pull                  # fetch + merge
git pull --rebase         # fetch + replay local commits on top
git push
```

Publish to GitHub (instructions only):
1. Create an empty repo on github.com (no README).
2. Then:
   ```
   git remote add origin https://github.com/<user>/git-learn.git
   git branch -M main
   git push -u origin main
   ```

---

## Task 12: Hooks and ignore rules

`.gitignore` already keeps build artifacts/secrets out.

Hooks run scripts on events. This repo uses `.githooks/pre-commit` (runs tests).

1. Make sure hooks are enabled:
   ```
   git config core.hooksPath .githooks
   ```
2. Edit `.githooks/pre-commit` to add linters/tests. It must stay executable:
   ```
   chmod +x .githooks/pre-commit
   ```
3. Now a commit that breaks tests is blocked automatically.

---

## Quick reference

```
git status | git add -p | git commit -m "msg" | git push
git switch -c x | git merge x | git rebase main
git stash | git stash pop
git log --oneline | git diff | git blame file
git reflog
```
