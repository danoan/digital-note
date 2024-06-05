#! /usr/bin/env bash

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${SCRIPT_PATH%digital-note*}digital-note"

pushd "${PROJECT_PATH}" >/dev/null
python -m doctest docs/*.md -o NORMALIZE_WHITESPACE
popd >/dev/null
