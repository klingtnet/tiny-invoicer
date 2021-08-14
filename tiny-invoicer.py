import argparse
from dataclasses import dataclass
from typing import List
from datetime import date, datetime

import strictyaml
from jinja2 import Template
from babel.dates import format_date

parser = argparse.ArgumentParser(description='A tiny invoice generator')
parser.add_argument(
    'company',
    type=argparse.FileType('r'),
    help='path to the company.yaml that contains details about the company')
parser.add_argument(
    'invoice',
    type=argparse.FileType('r'),
    help='path to invoice.yaml that contains invoice details')
args = parser.parse_args()


def to_html_addr(addr: str) -> str:
    return addr.replace('\n', '<br>\n')


@dataclass
class BankDetails:
    owner: str
    name: str
    iban: str
    bic: str


@dataclass
class Company:
    address: str
    name: str
    logo: str
    phone: str
    website: str
    tax_number: str
    bank_details: BankDetails

    def addr(self) -> str:
        return to_html_addr('\n'.join([self.name, self.address]))


@dataclass
class Service:
    descr: str
    qty: float
    unit: str
    price: float
    net: float


@dataclass
class Invoice:
    address: str
    _date: datetime
    services: List[Service]
    message: str

    def date(self, locale="en_US") -> str:
        return format_date(self._date, locale=locale)

    def number(self) -> str:
        return self._date.isoformat()

    def net_total(self) -> float:
        total = 0.0
        for service in self.services:
            total += service.net
        return total

    def addr(self) -> str:
        return to_html_addr(self.address)


with args.company as f:
    yml = strictyaml.load(f.read())
    bd = yml.get('bank_details')
    bank_details = BankDetails(
        bd.get('owner').data,
        bd.get('name').data,
        bd.get('iban').data,
        bd.get('bic').data)
    company = Company(
        yml.get('address').data,
        yml.get('name').data,
        yml.get('logo').data,
        yml.get('phone').data,
        yml.get('website').data,
        yml.get('tax_number').data, bank_details)

with args.invoice as f:
    yml = strictyaml.load(f.read())
    date = date.fromisoformat(yml.get('date').data)
    services = []
    for service in yml.get('services'):
        qty = float(service.get('qty').data)
        price = float(service.get('price').data)
        net = price * qty
        services.append(
            Service(
                service.get('descr').data, qty,
                service.get('unit').data, price, net))
    invoice = Invoice(yml.get('address').data, date, services, yml.get('message', default='').__str__())

with open('invoice.html.jinja') as f:
    template = Template(f.read())
    print(template.render(company=company, invoice=invoice))
