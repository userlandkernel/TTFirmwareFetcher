#!/usr/bin/env bash

if ! [ -x "$(command -v cabextract)" ]; then
  echo 'Error: cabextract is not installed.' >&2
  exit 1
fi

for file in $(find . -type f | grep ".cab");do
	mkdir -p "firmware/$(echo $file | sed -e 's/\.cab//g')"
	cabextract "$file" -d "firmware/$(echo $file | sed -e 's/\.cab//g')"
done
