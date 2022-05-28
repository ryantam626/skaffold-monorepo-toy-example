# Devtools

This is a set of tooling that work alongside (or instead of skaffold) for manipulating local k8s resources.

To use this, include the various Taskfile.*.yml in your main Taskfile.yml within a new directory and then use `task`, `task --list-all` shows you what you can do.

## Expectation

- Assumes the follow scripts exists in container
  ```bash
  /scripts/test.sh
  /scripts/format.sh
  /scripts/lint.sh
  ```
