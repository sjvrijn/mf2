# Contributing

## Bugs
If you've found a problem of some sort, please open an issue on
[GitHub][new-issue] with your code, the resulting output and expected output.

## Additions
Suggestions for new functions are welcome too. When suggesting a function,
please include the DOI of the source paper.

When submitting a PR to add new functions to this package, you can roughly
follow the following steps:

 1. Implement the function in a new file in the appropriate (sub)folder
 2. Add it to the tests:
    * Add the function in the `tests/property_test.py` and
    `tests/regression_test.py` files
    * Run the tests: `pytest tests`. It will fail the first time while the
    [`pytest-regressions`][pytest-regressions] package automatically creates
    the new output files.
    * Run the tests again to confirm that all tests now pass.
 3. Make sure to commit all new and updated files to git (Travis-CI will
    complain otherwise ;)
 4. Create a pull-request!

If you need any help with this process, please get in touch as specified in the
README under **Contact**.

[new-issue]:          https://github.com/sjvrijn/mf2/issues/new
[pytest-regressions]: https://github.com/ESSS/pytest-regressions