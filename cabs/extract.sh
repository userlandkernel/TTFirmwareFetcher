#!/usr/bin/env bash

for file in $(find . -type f | grep ".cab");do
	mkdir -p "../firmware/$(echo $file | sed -e 's/\.cab//g')"
	cabextract "$file" -d "../firmware/$(echo $file | sed -e 's/\.cab//g')"
done
