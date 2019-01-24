# tiny-invoicer

**Work-in-Progress**

A super simple Python script for generating HTML invoices.

## Example

```sh
$ venv/bin/python invoicer.py meta.example.yaml invoice.example.yaml > example-invoice.html
```

You can see a preview of the generated invoice [here][example]

## Installation

```sh
$ python3 -m venv venv
$ venv/bin/pip install -r requirements.txt
```

## Usage

```sh
$ venv/bin/python tiny-invoicer.py meta.yaml invoice.yaml > invoice.html
```

[example]: https://htmlpreview.github.io/?https://raw.githubusercontent.com/klingtnet/tiny-invoicer/master/example-invoice.html
