# Git Common Operations Guide

## Scenario 1: Syncing After Remote File Removal

When you've removed a file on GitHub and need to sync/commit your local changes:

1. Fetch the latest changes from GitHub:
   ```bash
   git fetch origin
   ```

2. Check your status:
   ```bash
   git status
   ```

3. Choose one of these sync methods:

   **Method A - Using Rebase (Recommended for cleaner history)**
   ```bash
   git rebase origin/main
   ```

   **Method B - Using Merge**
   ```bash
   git merge origin/main
   ```

4. Push your changes:
   ```bash
   git push origin main
   ```

## Handling Conflicts

If you get conflicts during rebase or merge:

1. Check conflicted files:
   ```bash
   git status
   ```

2. Open each conflicted file and look for:
   ```
   <<<<<<< HEAD
   your changes
   =======
   remote changes
   >>>>>>> branch-name
   ```

3. Edit files to resolve conflicts by choosing which changes to keep

4. After fixing conflicts:
   ```bash
   # If using rebase:
   git add .
   git rebase --continue

   # If using merge:
   git add .
   git merge --continue
   ```

5. Push your changes:
   ```bash
   git push origin main
   ```

## Emergency Abort Commands

If you need to start over:

```bash
git rebase --abort   # abort a rebase
git merge --abort    # abort a merge
```

## Best Practices

1. Always commit local changes before pulling or rebasing
2. Use `git status` frequently to check your state
3. Create branches for new features:
   ```bash
   git checkout -b feature-name
   ```
4. Keep commits atomic and well-described:
   ```bash
   git commit -m "clear description of changes"
   ```

## Common Git Commands

```bash
# Check current status
git status

# Stage all changes
git add .

# Stage specific file
git add filename

# Commit changes
git commit -m "commit message"

# Push to remote
git push origin branch-name

# Pull from remote
git pull origin branch-name

# Check commit history
git log

# Switch branches
git checkout branch-name

# Create and switch to new branch
git checkout -b new-branch-name

# Discard local changes to a file
git checkout -- filename

# See difference in files
git diff
```

## Need Help?

- Check official Git documentation: https://git-scm.com/doc
- Use `git --help` for command list
- Use `git command --help` for specific command help 