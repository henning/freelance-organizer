# Next things to do

## Features

* upgrade to latest Django and libs

* add import
  * from CSV or TSV file
  * from text lines (e.g. current spreadsheet...)
    * Click the menu link to the import view in the admin
    * Paste text from a spreadsheet app into a form and click import
    * be redirected to the admin timeslices list with a filter for imported 
      and unchecked Timeslices to veryfy them
    * have a "toggle import checked state" option in actions for the chosen 
      slices (similar to invoiced state already works)

## Operations

* add config to run on external IP / add proxy to docker setup
* ensure regular/on demand backups into filesystem -> docker compose config?!
  * as sql dump
  * as django dump
* use "proper" DB -> postgres

* Run app as non-root in container:
  RUN useradd -m appuser
  RUN chown appuser:appuser /opt/freelance-organizer
  USER appuser
  * Requires using a proper db first
