#!/usr/bin/env python3
import re
from datetime import datetime, timezone
from pprint import pformat

from util import DataNode


class PfSenseNode(DataNode):
    def __init__(self, parent=None):
        self._parent = parent

    def __getattr__(self, name):
        # This trick hides PyLint error messages...
        return super().__getattribute__(name)

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

class PfSenseInterfacesNode(PfSenseNode):
    def __getattr__(self, name):
        if name.startswith('_opt'):
            return self._opt
        return super().__getattribute__(name)

class PfSenseFlag(PfSenseNode):
    @property
    def data(self):
        return True

class PfSenseAliasString(PfSenseString):
    @property
    def data(self):
        data = super().data
        for alias in self.rootdoc.pfsense.aliases.alias:
            if alias.name.string == data:
                return {'alias': alias.data}
        return data

class PfSensePortString(PfSenseAliasString):
    PORT_STRING = re.compile(r'(\d+((:|-)(\d+))?|[a-zA-Z0-9_]+)')

    def __call__(self, content):
        super().__call__(content)
        if self.PORT_STRING.fullmatch(self.string) is None:
            raise RuntimeError("Invalid port string: {}".format(self.string))

class PfSenseChange(PfSenseNode):
    _time = PfSenseTimestamp
    _username = PfSenseString

class PfSenseRange(PfSenseNode):
    _from = PfSenseString
    _to = PfSenseString

class PfSenseSysCtlItem(PfSenseNode):
    _tunable = PfSenseString
    _value = PfSenseString
    _descr = PfSenseString

class PfSenseSysCtl(PfSenseNode):
    _item = [PfSenseSysCtlItem]

class PfSenseStaticMap(PfSenseNode):
    _mac = PfSenseString
    _ipaddr = PfSenseString
    _hostname = PfSenseString

class PfSenseDhcpdItem(PfSenseNode):
    _range = [PfSenseRange]
    _staticmap = [PfSenseStaticMap]
    _defaultleasetime = PfSenseInteger
    _maxleasetime = PfSenseInteger
    _enable = PfSenseFlag

class PfSenseDhcpd(PfSenseInterfacesNode):
    _wan = PfSenseDhcpdItem
    _lan = PfSenseDhcpdItem
    _opt = PfSenseDhcpdItem

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
        if data is None:
            return data
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
    _port = PfSensePortString
    _not = PfSenseFlag

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
    _associated_rule_id = PfSenseString
    _created = PfSenseChange
    _updated = PfSenseChange
    _disabled = PfSenseFlag

class PfSenseFilter(PfSenseNode):
    _rule = [PfSenseFilterRule]

class PfSenseNatOutboundRule(PfSenseNode):
    _interface = PfSenseRuleInterface
    _source = PfSenseRuleLocation
    _dstport = PfSensePortString
    _target = PfSenseString
    _targetip = PfSenseString
    _targetip_subnet = PfSenseString
    _destination = PfSenseRuleLocation
    _natport = PfSensePortString
    _staticnatport = PfSensePortString
    _descr = PfSenseString
    _created = PfSenseChange
    _updated = PfSenseChange
    _disabled = PfSenseFlag

class PfSenseNatOutbound(PfSenseNode):
    _mode = PfSenseString
    _rule = [PfSenseNatOutboundRule]

class PfSenseNatRule(PfSenseNode):
    _source = PfSenseRuleLocation
    _destination = PfSenseRuleLocation
    _protocol = PfSenseString
    _target = PfSenseRuleAlias
    _local_port = PfSenseInteger
    _interface = PfSenseRuleInterface
    _descr = PfSenseString
    _associated_rule_id = PfSenseString
    _created = PfSenseChange
    _updated = PfSenseChange
    _disabled = PfSenseFlag

class PfSenseNat(PfSenseNode):
    _outbound = PfSenseNatOutbound
    _rule = [PfSenseNatRule]

class PfSenseAlias(PfSenseNode):
    _name = PfSenseString
    _type = PfSenseString
    _address = PfSenseString
    _descr = PfSenseString
    _detail = PfSenseString

class PfSenseAliases(PfSenseNode):
    _alias = [PfSenseAlias]

class PfSenseDnsMasqDomainOverride(PfSenseNode):
    _domain = PfSenseString
    _ip = PfSenseString
    _idx = PfSenseInteger
    _descr = PfSenseString

class PfSenseDnsMasqHostAliasItem(PfSenseNode):
    _host = PfSenseString
    _domain = PfSenseString
    _description = PfSenseString

class PfSenseDnsMasqHostAliases(PfSenseNode):
    _item = [PfSenseDnsMasqHostAliasItem]

class PfSenseDnsMasqHost(PfSenseNode):
    _host = PfSenseString
    _domain = PfSenseString
    _ip = PfSenseString
    _descr = PfSenseString
    _aliases = PfSenseDnsMasqHostAliases

class PfSenseDnsMasq(PfSenseNode):
    _enable = PfSenseFlag
    _reqdhcp = PfSenseFlag
    _reqdhcpstatic = PfSenseFlag
    _strict_order = PfSenseFlag
    _custom_options = PfSenseString
    _interface = PfSenseRuleInterface
    _hosts = [PfSenseDnsMasqHost]
    _domainoverrides = [PfSenseDnsMasqDomainOverride]

class PfSenseOpenVpnClient(PfSenseNode):
    _vpnid = PfSenseInteger
    _auth_user = PfSenseString
    _mode = PfSenseString
    _protocol = PfSenseString
    _dev_mode = PfSenseString
    _interface = PfSenseRuleInterface
    _ipaddr = PfSenseString
    _local_port = PfSenseInteger
    _server_addr = PfSenseString
    _server_port = PfSenseInteger
    _crypto = PfSenseString
    _digest = PfSenseString
    _tunnel_network = PfSenseString
    _remote_network = PfSenseString
    _local_network = PfSenseString
    _topology = PfSenseString
    _description = PfSenseString
    _custom_options = PfSenseString

class PfSenseOpenVpnServer(PfSenseNode):
    _vpnid = PfSenseInteger
    _mode = PfSenseString
    _authmode = PfSenseString
    _protocol = PfSenseString
    _dev_mode = PfSenseString
    _interface = PfSenseRuleInterface
    _ipaddr = PfSenseString
    _local_port = PfSenseInteger
    _crypto = PfSenseString
    _digest = PfSenseString
    _tunnel_network = PfSenseString
    _remote_network = PfSenseString
    _local_network = PfSenseString
    _dynamic_ip = PfSenseString
    _pool_enable = PfSenseString
    _topology = PfSenseString
    _description = PfSenseString
    _custom_options = PfSenseString

class PfSenseOpenVpn(PfSenseNode):
    _openvpn_server = [PfSenseOpenVpnServer]
    _openvpn_client = [PfSenseOpenVpnClient]

class PfSenseRoute(PfSenseNode):
    _network = PfSenseString
    _gateway = PfSenseString
    _descr = PfSenseString

class PfSenseStaticRoutes(PfSenseNode):
    _route = [PfSenseRoute]

class PfSenseGatewayItem(PfSenseNode):
    _interface = PfSenseRuleInterface
    _gateway = PfSenseString
    _name = PfSenseString
    _weight = PfSenseInteger
    _ipprotocol = PfSenseString
    _interval = PfSenseInteger
    _alert_interval = PfSenseInteger
    _descr = PfSenseString
    _defaultgw = PfSenseFlag

class PfSenseGateways(PfSenseNode):
    _gateway_item = [PfSenseGatewayItem]

class PfSenseVlan(PfSenseNode):
    _vlanif = PfSenseString
    _tag = PfSenseInteger
    _if = PfSenseString
    _descr = PfSenseString

class PfSenseVlans(PfSenseNode):
    _vlan = [PfSenseVlan]

class PfSenseBridged(PfSenseNode):
    _bridgeif = PfSenseString
    _members = PfSenseRuleInterface
    _descr = PfSenseString

class PfSenseBridges(PfSenseNode):
    _bridged = [PfSenseBridged]

class PfSenseInterface(PfSenseNode):
    _if = PfSenseString
    _descr = PfSenseString
    _ipaddr = PfSenseString
    _subnet = PfSenseString
    _enable = PfSenseFlag

class PfSenseInterfaces(PfSenseInterfacesNode):
    _wan = PfSenseInterface
    _lan = PfSenseInterface
    _opt = PfSenseInterface

class PfSenseSyslog(PfSenseNode):
    _nentries = PfSenseInteger
    _logfilesize = PfSenseInteger
    _remoteserver = PfSenseString
    _remoteserver2 = PfSenseString
    _remoteserver3 = PfSenseString
    _sourceip = PfSenseRuleInterface
    _ipproto = PfSenseString
    _logall = PfSenseFlag
    _enable = PfSenseFlag

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
    _vlans = PfSenseVlans
    _bridges = PfSenseBridges
    _gateways = PfSenseGateways
    _staticroutes = PfSenseStaticRoutes
    _aliases = PfSenseAliases
    _nat = PfSenseNat
    _filter = PfSenseFilter
    _dnsmasq = PfSenseDnsMasq
    _dhcpd = PfSenseDhcpd
    _openvpn = PfSenseOpenVpn
    _syslog = PfSenseSyslog
    _sysctl = PfSenseSysCtl

class PfSenseDocument(PfSenseNode):
    _pfsense = PfSenseConfig
