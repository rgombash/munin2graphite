# munin2graphite

Simple python script that writes munin node data to graphite.

Script cycles munin plugin symlinks, executes scripts using munin-run and writes result to graphite.

Idea for this script came from my collage.

## What you need:

- installed munin node with some plugins

## Configuration

- change config parameters to suit your needs
- optionally add to crontab to be executed (e.g.:every minute)
