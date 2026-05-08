# Sync Music Assistant Files
## Running
powershell:
```powershell
$ . ./run.ps1 -Source '[SOURCE_DIRECTORY]' -Target '[TARGET_DIRECTORY]'q
```

bash:
```bash
# Enable devenv
$ devenv shell

# run script
$ uv run main.py --source '[SOURCE_DIRECTORY]' --target '[TARGET_DIRECTORY]'
```


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

