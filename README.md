# munin2graphite

Simple python script that writes munin node data to graphite

Idea for this script came from my collage.

Script cycles munin plugins symlinks, executes script using munin-run and writes result to graphite

## What you need:

-installed munin node with some plugins

## Configuration

-change parameters on top to suit your needs

-optionally add to crontab to be executed (e.g.:every minute)
