#!/bin/sh

buildpath=.

interval=600
cfgpath=/app/config.yml

nixpacks build $buildpath --name lunchbot --start-cmd "python -m lunchbot -c $cfgpath -i $interval"
