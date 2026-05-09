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
devenv:
```bash
devenv update
```
uv:
```bash
# Get outdated packages
$ uv tree --outdated --depth 1

# Update package
$ uvpkg=mutagen && uv remove $uvpkg && uv add $uvpkg

# or
$ uv add "mutagen>=1.47.0"
```

