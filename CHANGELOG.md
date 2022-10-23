# django-sans-db changelog

## Unreleased

## [1.2.0] - 2022-10-23

- Remove upper limit on Python version.
  This should prevent issues when installing for new versions of Python.
- Add Django 4.1 to text matrix.
- Add tests for using `block_db` as a decorator.
  This was working before, but not officially supported.

## [1.1.0] - 2022-06-11

- Add `{% sansdb %}` template tag.

## [1.0.0] - 2022-06-08

- Add support for configs with multiple databases.
- Dropped Python 3.6 from test matrix.
- Dropped Django 2.0 and 2.1 from test matrix.

## [0.1.0] - 2021-12-17

- Initial release.
- Tested with PostgreSQL, MySQL, and SQLite DB backends.
- Tested with sensible combinations of:
  - Django 2.0, 2.1, 2.2, 3.0, 3.1, 3.2, 4.0
  - Python 3.6, 3.7, 3.8, 3.9, 3.10
