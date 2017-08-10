#!/usr/bin/env python3
from collections import OrderedDict


class DataNode(object):
    @property
    def data(self):
        attr_filter = lambda x: not x[0].startswith('_')
        data_items = filter(attr_filter, self.__dict__.items())
        data = {}
        for key, value in data_items:
            if isinstance(value, DataNode):
                data[key] = value.data
            else:
                data[key] = value
        return data

class DataList(list, DataNode):
    @property
    def data(self):
        data = []
        for value in self:
            if isinstance(value, DataNode):
                data.append(value.data)
            else:
                data.append(value)
        return data


def dict_to_dict(data, attributes):
    data_items = [(attribute, data.get(attribute, '')) for attribute in attributes]
    return OrderedDict(data_items)

def dict_to_list(data, attributes):
    data_values = [data.get(attribute, '') for attribute in attributes]
    return list(data_values)

def obj_to_dict(obj, attributes):
    return dict_to_dict(obj.__dict__, attributes)

def obj_to_list(obj, attributes):
    return dict_to_list(obj.__dict__, attributes)

def hasattr_r(obj, attribute):
    for attr in attribute.split('.'):
        if not hasattr(obj, attr):
            return False
        obj = getattr(obj, attr)
    return True
