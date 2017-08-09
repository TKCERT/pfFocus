#!/usr/bin/env python3
from pfsense import PfSenseFilterAlias, PfSenseFilterLocation
from util import dict_to_list, obj_to_dict, obj_to_list


def format_filter_alias(filter_alias):
    if isinstance(filter_alias, dict):
        if 'alias' in filter_alias:
            filter_alias = '[{name}](#aliases "{address}")'.format(**filter_alias['alias'])
        elif 'interface' in filter_alias:
            filter_alias = '[{name}](#interfaces "{descr}")'.format(**filter_alias['interface'])
    return filter_alias

def format_filter_location(filter_location):
    if isinstance(filter_location, PfSenseFilterAlias):
        filter_location = format_filter_alias(filter_location.data)
    return str(filter_location)

def format_markdown_cell(cell):
    if isinstance(cell, PfSenseFilterLocation):
        data = ''
        if hasattr(cell, 'any'):
            data += 'any'
        elif hasattr(cell, 'address'):
            data += format_filter_location(cell.address)
        elif hasattr(cell, 'network'):
            data += format_filter_location(cell.network)
        if hasattr(cell, 'port'):
            data += ':'
            data += str(cell.port)
        cell = data
    return str(cell).replace('|', '\\|')

def output_markdown_table(stream, header, rows):
    # Header
    stream.write("| ")
    stream.write(" | ".join(header))
    stream.write(" |\n")
    # Seperator
    stream.write("| ")
    stream.write(" | ".join(map(lambda x: '-'*len(x), header)))
    stream.write(" |\n")
    # Rows
    for row in rows:
        stream.write("| ")
        stream.write(" | ".join(map(format_markdown_cell, row)))
        stream.write(" |\n")

def output_markdown(doc, stream):
    stream.write("# pfSense\n")
    stream.write("Version {}\n".format(doc.pfsense.version))
    stream.write("\n")

    stream.write("## System\n")
    info = obj_to_dict(doc.pfsense.system, ('hostname', 'domain', 'timeservers', 'timezone', 'language', 'dnsserver'))
    output_markdown_table(stream, ('Option', 'Value'), info.items())
    stream.write("\n")

    stream.write("## Interfaces\n")
    interfaces = sorted(doc.pfsense.interfaces.data.items(), key=lambda interface: interface[0])
    interfaces = [[interface_name]+dict_to_list(interface_data, ('descr', 'if', 'ipaddr', 'subnet')) for interface_name, interface_data in interfaces]
    output_markdown_table(stream, ('Name', 'Description', 'Interface', 'Address', 'Subnet'), interfaces)
    stream.write("\n")

    stream.write("## Aliases\n")
    aliases = [obj_to_list(alias, ('name', 'type', 'address', 'descr', 'detail')) for alias in doc.pfsense.aliases.alias]
    output_markdown_table(stream, ('Name', 'Type', 'Address', 'Description', 'Detail'), aliases)
    stream.write("\n")

    stream.write("## Filter rules\n")
    rules = [obj_to_list(rule, ('interface', 'type', 'ipprotocol', 'protocol', 'source', 'destination', 'descr')) for rule in doc.pfsense.filter.rule]
    output_markdown_table(stream, ('Interface', 'Type', 'IP', 'Protocol', 'Source', 'Destination', 'Description'), rules)
    stream.write("\n")
