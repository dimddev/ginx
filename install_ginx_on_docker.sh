#!/usr/bin/env bash
doc=$(which docker)
if [[ -x "$doc" ]]; then
    $doc build -t ginx .
else
    echo "Docker cli is not located on this system"
fi
