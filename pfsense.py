#!/usr/bin/env python3
from datetime import datetime, timezone
from pprint import pformat

from util import DataNode


class PfSenseNode(DataNode):
    def __init__(self, parent=None):
        self._parent = parent

    def __getattr__(self, name):
        # This trick hides PyLint error messages...
        raise AttributeError

    def __call__(self, content):
        pass # discard content

    def __repr__(self):
        return pformat(self.data)

    def __str__(self):
        return str(self.data)

    @property
    def parents(self):
        obj = self
        while obj._parent:
            yield obj._parent
            obj = obj._parent

    @property
    def rootdoc(self):
        return list(self.parents)[-1]

class PfSenseString(PfSenseNode):
    string = None

    def __call__(self, content):
        self.string = str(content)

    @property
    def data(self):
        return self.string


class PfSenseInteger(PfSenseNode):
    integer = None

    def __call__(self, content):
        self.integer = int(content)

    @property
    def data(self):
        return self.integer

class PfSenseTimestamp(PfSenseNode):
    datetime = None

    def __call__(self, content):
        self.datetime = datetime.fromtimestamp(int(content), timezone.utc)

    @property
    def data(self):
        return self.datetime

class PfSenseFlag(PfSenseNode):
    @property
    def data(self):
        return True

class PfSenseChange(PfSenseNode):
    _time = PfSenseTimestamp
    _username = PfSenseString

class PfSenseRuleAlias(PfSenseString):
    @property
    def data(self):
        data = super().data
        for interface_name, interface_data in self.rootdoc.pfsense.interfaces.data.items():
            alias_name = data
            if alias_name.endswith('ip'):
                alias_name = alias_name[:-2]
            if interface_name == alias_name:
                interface_data['name'] = data
                return {'interface': interface_data}
        for alias in self.rootdoc.pfsense.aliases.alias:
            if alias.name.string == data:
                return {'alias': alias.data}
        return data

class PfSenseRuleInterface(PfSenseString):
    @property
    def data(self):
        data = super().data
        data_list = []
        for iface_name in data.split(','):
            found = False
            for interface_name, interface_data in self.rootdoc.pfsense.interfaces.data.items():
                if interface_name == iface_name:
                    interface_data['name'] = iface_name
                    data_list.append({'interface': interface_data})
                    found = True
                    break
            if not found:
                data_list.append(iface_name)
        return data_list

class PfSenseRuleLocation(PfSenseNode):
    _any = PfSenseNode
    _network = PfSenseRuleAlias
    _address = PfSenseRuleAlias
    _port = PfSenseInteger

class PfSenseFilterRule(PfSenseNode):
    _id = PfSenseString
    _tracker = PfSenseString
    _type = PfSenseString
    _interface = PfSenseRuleInterface
    _ipprotocol = PfSenseString
    _tag = PfSenseString
    _tagged = PfSenseString
    _max = PfSenseString
    _max_src_nodes = PfSenseString
    _max_src_conn = PfSenseString
    _max_src_states = PfSenseString
    _statetimeout = PfSenseString
    _statetype = PfSenseString
    _os = PfSenseString
    _protocol = PfSenseString
    _source = PfSenseRuleLocation
    _destination = PfSenseRuleLocation
    _descr = PfSenseString
    _created = PfSenseChange
    _updated = PfSenseChange
    _disabled = PfSenseFlag

class PfSenseFilter(PfSenseNode):
    _rule = [PfSenseFilterRule]

class PfSenseNatOutboundRule(PfSenseNode):
    _interface = PfSenseRuleInterface
    _source = PfSenseRuleLocation
    _dstport = PfSenseInteger
    _target = PfSenseString
    _targetip = PfSenseString
    _targetip_subnet = PfSenseString
    _destination = PfSenseRuleLocation
    _natport = PfSenseInteger
    _staticnatport = PfSenseInteger
    _descr = PfSenseString
    _created = PfSenseChange
    _updated = PfSenseChange
    _disabled = PfSenseFlag

class PfSenseNatOutbound(PfSenseNode):
    _mode = PfSenseString
    _rule = [PfSenseNatOutboundRule]

class PfSenseNat(PfSenseNode):
    _outbound = PfSenseNatOutbound

class PfSenseAlias(PfSenseNode):
    _name = PfSenseString
    _type = PfSenseString
    _address = PfSenseString
    _descr = PfSenseString
    _detail = PfSenseString

class PfSenseAliases(PfSenseNode):
    _alias = [PfSenseAlias]

class PfSenseInterface(PfSenseNode):
    _if = PfSenseString
    _descr = PfSenseString
    _ipaddr = PfSenseString
    _subnet = PfSenseString
    _enable = PfSenseFlag

class PfSenseInterfaces(PfSenseNode):
    _wan = PfSenseInterface
    _lan = PfSenseInterface
    _opt = PfSenseInterface

    def __getattr__(self, name):
        if name.startswith('_opt'):
            return self._opt
        raise AttributeError

class PfSenseSystem(PfSenseNode):
    _optimization = PfSenseString
    _hostname = PfSenseString
    _domain = PfSenseString
    _timeservers = PfSenseString
    _timezone = PfSenseString
    _language = PfSenseString
    _dnsserver = PfSenseString

class PfSenseConfig(PfSenseNode):
    _version = PfSenseString
    _system = PfSenseSystem
    _interfaces = PfSenseInterfaces
    _aliases = PfSenseAliases
    _nat = PfSenseNat
    _filter = PfSenseFilter

class PfSenseDocument(PfSenseNode):
    _pfsense = PfSenseConfig
