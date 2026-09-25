# Personal Homebrew tap

Personal macOS casks downloaded directly from their upstream publishers.

## Install and upgrade

```sh
brew tap jaredwad/personal
brew trust --tap jaredwad/personal
brew install --cask jaredwad/personal/alacritty
```

`brew trust` permits Homebrew to load this tap's Ruby recipes. It does not approve
apps in macOS Gatekeeper. Review a tap's code before trusting it.

If Alacritty is already installed from another tap, switch it with
`brew reinstall --cask jaredwad/personal/alacritty` (do not use `--zap`).

Once installed from this tap, normal updates work:

```sh
brew update
brew outdated --cask
brew upgrade --cask
```

For a single app, use `brew upgrade --cask jaredwad/personal/alacritty`.
An unqualified `brew upgrade alacritty` resolves the disabled official cask,
even though the installed copy belongs to this tap. Bulk upgrades use the
installed tap correctly.

Alacritty is not Apple-notarized. If macOS blocks it, approve this specific app
using System Settings > Privacy & Security > Open Anyway after attempting to
launch it, provided you trust its source. This tap does not remove quarantine or
disable Gatekeeper. Configuration files are not changed by installation/upgrades.

## Optional shell wrapper for short names

To make `brew info alacritty` and `brew upgrade alacritty` use this tap, add this
function to `~/.zshrc` (or your interactive bash startup file):

```sh
# Resolve personal-tap casks before their official Homebrew names.
brew() {
  local arg
  local -a args=()

  for arg in "$@"; do
    case "$arg" in
      alacritty)
        args+=("jaredwad/personal/alacritty")
        ;;
      *)
        args+=("$arg")
        ;;
    esac
  done

  command brew "${args[@]}"
}
```

Open a new terminal, or run `source ~/.zshrc` in an existing zsh session. Verify:

```sh
whence -w brew
brew info --cask alacritty
brew upgrade --cask --dry-run alacritty
```

`whence` should report `brew: function`, and the info output should identify
`jaredwad/personal/alacritty` without the official cask's disabled warning.

The wrapper replaces only arguments exactly equal to `alacritty`, preserves
argument boundaries, and uses `command brew` to call the real executable without
recursion. Fully qualified names and commands without that argument are unchanged.
It applies to **every subcommand**, including `brew search alacritty`; it does not
interpret the argument's role. It affects only shells loading this function, not
GitHub Actions or programs invoking Homebrew directly.

Bypass it for a single command with `command brew info alacritty`, or explicitly
select the official cask with `brew info homebrew/cask/alacritty`.

For another app, add an exact-name `case` branch mapping its short name to
`jaredwad/personal/<app>` before the `*` branch. If your shell configuration is
managed by chezmoi, keep the function in its source file too. To remove the
wrapper, delete it from the startup file and managed source, then run
`unset -f brew` in existing sessions.

## Automatic release checks

The **Update casks** GitHub Actions workflow runs daily at 09:23 UTC (GitHub may
delay scheduled runs) and can also be dispatched manually from the Actions tab.
It uses `brew livecheck` across every cask in this tap, then
`brew bump-cask-pr --write-only` to download releases and update versions and
checksums. After a style check it commits changed casks directly to `main`.
It uses the repository's built-in `GITHUB_TOKEN`; no personal token is required.

This updates the tap, not apps on your Mac. Run `brew update` and `brew upgrade`
to install available versions. Check Actions for failures; a broken download,
release check, or cask prevents the batch from being published. GitHub may disable
scheduled workflows in public repositories after 60 days without repository
activity; re-enable the workflow in Actions if needed.

Run the same updater locally from the tapped repository:

```sh
brew livecheck --tap=jaredwad/personal --cask
python3 scripts/update-casks.py
brew style Casks
```

Local updates must be committed and pushed to publish them.

## Add another app

1. Add `Casks/<app>.rb` using Homebrew's cask DSL, with a version, SHA-256,
   official download URL, and installation artifacts.
2. Add a working `livecheck` rule when automatic detection is insufficient.
   Use stable releases; avoid unversioned downloads where possible.
3. Run `brew livecheck --cask jaredwad/personal/<app>` and `brew style Casks`.
4. Commit and push, then install using `brew install --cask jaredwad/personal/<app>`.

The workflow discovers added casks automatically; no app list needs updating.
Apps with unusual version/architecture schemes may need updater changes. Casks
without a usable livecheck result are reported and not automatically bumped.

## Attribution

The Alacritty cask is adapted from
[Homebrew/homebrew-cask](https://github.com/Homebrew/homebrew-cask/blob/99ad3f93362061501fa275b3313f76fe13e47324/Casks/a/alacritty.rb),
without the official tap's Gatekeeper-based disabling directive. Its BSD 2-Clause
license is retained in `LICENSE`.
