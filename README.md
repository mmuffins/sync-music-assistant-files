# Sync Music Assistant Files
## Running
Windows:
```powershell
$ uv run main.py --source '[SOURCE_DIRECTORY]' --target '[TARGET_DIRECTORY]'
```

Linux:
```bash
# Enable devenv
$ devenv shell

# run script
$ uv run main.py --source '[SOURCE_DIRECTORY]' --target '[TARGET_DIRECTORY]'
```
A runner script is available for nixos that automatically activates the devshell and runs the main script.

## Updating
- Manually update the python version in `devenv.nix`
- Manually update the python version in `pyproject.toml`
- Update devenv:
```bash
devenv update
```

- Update uv:
```bash
# Get outdated packages
$ uv tree --outdated --depth 1

# Update package
$ uvpkg=mutagen && uv remove $uvpkg && uv add $uvpkg

# or
$ uv add "mutagen>=1.47.0"
```

uv automatically upgrades versions matching the constraint, and will do so silently, they will not be listed in the outdated packages. `uv tree --outdated` only highlights packages that need to be upgraded manually.