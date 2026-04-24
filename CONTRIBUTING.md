# Contributing

Thank you for the interest in contributing to the TU Cookbook initiative! We accept contributions in the following areas:

- Reporting a bug
- Discussing the current state of notebooks and code
- Submitting a fix
- Proposing new notebooks
- Proposing adaptations and new features to existing notebooks

# Development on TU Wien GitLab

All development takes place on the TU Wien's GitLab repository: https://gitlab.tuwien.ac.at/cookbooks. Here we track issues and feature/notebook requests.

# Propose New Cookbooks

To propose new cookbooks contact ...

# Propose Changes with Merge Requests to Existing Cookbooks

GitLab's Merge Request (equivalent of GitHub's Pull Request) are at the core of proposing new changes to the existing TU Cookbook collection. For a successful merge request check the following:

1. Make sure that you follow the instructions for development as outlined belows
2. Use the pre-commit hooks
3. Check whether the GitLab CI checks pass

# Contribution License

Any contribution to an existing Cookbook will under the same license that covers the current Cookbook, ....

# Report Bugs using GitLab Issues

We use GitLab to track public bugs. If you want to report a bug, please open a new issue on the relevant TU Cookbook on https://gitlab.tuwien.ac.at/cookbooks.

## How to write issues

A bug should be reported with details, back and sample code as well as data. The goals is to create a [minimal reproducible example](https://stackoverflow.com/help/minimal-reproducible-example). Ideally this should contain:

- A quick summary and/or background
- Steps to reproduce; minimal reproducible example
- What you expect to happen
- What actually happens
- Notes (e.g. possible workarounds and/or things you tried to solve the bug)

# Reference

This section was adapted from [this guideline](https://gist.github.com/briandk/3d2e8b3ec8daf5a27a62).

# Development

## Environment

To be determined... (conda, uv, etc.)

## Testing

To ensure that the cookbook webpage can be deployed and the notebooks run on the dataLAB JupyterHub follow the next steps.

1. Start Jupyter Lab from a Docker container:

   ```bash
   docker compose up
   ```
2. Copy Jupyter Lab URL to web browser. Run all notebooks once to check if you added all dependencies to the `pyproject.toml` and whether external data can be accessed.

If the following steps are completed successfully then one can stop and remove the container.

1. Stop Docker container with `CTRL + C`

2. Remove container:

   ```bash
   docker compose down
   ```

## Code Quality

### Why Code Quality Matters

As a public showcase of the university research, the code must:

- **Teach by Example:** Demonstrate best practices to readers
- **Ensure FAIR Compliance:** Clear, well-documented code supports Findable, Accessible, Interoperable and Reuseable data
- **Establish Credibility** High-quality code reflects the university's technical excellence and aids reproducability

### Enforcing Quality

> [!important]
> The following sections assumes that you have [uv] installed on your system, as [uv] provides a lot of helpful features, e.g. through it's toolrunner `uvx`. In order to install it follow the steps on their website.

We use automated tools to maintain standards. Follow these steps:

1. **Install pre-commit hooks**

Run this command to enable automatic checks on every commit:

```bash
uvx pre-commit install
```

2. **Run Checks Manually**

Use the [uv] toolrunner to execute tools:

```bash
# Format the code (ruff)
uvx ruff format

# Lint the code (ruff)
uvx ruff check  --fix

# Type check (ty)
uvx ty check
```

### Key Tools

- **Pre-Commit:** Run the pre-commit hooks. Find out more at the [pre-commit] documentation
- **Ruff:** The Linter and Formatter. Can be configured in the `pyproject.toml` file. Find out more at the [ruff] documenation
- **TY:** The Typechecker. Can be configured in the `pyproject.toml` file. Find out more at the [ty] documenation
- **UV:** The package and project manager. Find out more at the [uv] documentation

### Best Practices for Academic Code

- **Type Hints:** Annotate function arguments and returns as defined in [PEP 484]. This can help to find issues in your code early. A helpful cheatsheet is available [here](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
- **Consistent Formatting:** Function signatures and classes should have a uniform interface. Follow the [PEP 8] guidelines.
- **Pre-Commit Checks:** To ensure properly formatted code.
- **Documentation:** Add Docstrings to public functions and classes. Follow the [NumPy Docstring] convention (there are tools for automated docstring documentation like [this VSCode Extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)).

[uv]: https://docs.astral.sh/uv/
[ruff]: https://docs.astral.sh/ruff/
[ty]: https://docs.astral.sh/ty/
[pre-commit]: https://pre-commit.com/
[PEP 484]: https://peps.python.org/pep-0484/
[PEP 8]: https://peps.python.org/pep-0008/
[NumPy Docstring]: https://numpydoc.readthedocs.io/en/latest/format.html
