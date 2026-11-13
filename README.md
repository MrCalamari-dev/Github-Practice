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

## Task 5: Rebase

1. Switch to feature branch:
   ```
   git switch feature
   ```
2. Replay it on latest main:
   ```
   git rebase main
   ```
   Resolve any conflicts as in Task 4 (edit, `git add`, `git rebase --continue`).
3. Interactive rebase last 3 commits:
   ```
   git rebase -i HEAD~3
   ```
   Change `pick` to `squash`/`reword` to combine or rename commits.

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
