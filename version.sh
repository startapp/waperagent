#!/bin/bash

cat README.RU | grep -o "waperagent [0-9.]*" | grep -o "[0-9.]*"
