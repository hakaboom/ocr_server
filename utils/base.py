# -*- coding: utf-8 -*-
import json
import re
import numpy as np


class auto_increment(object):
    def __init__(self):
        self._val = 0

    def __call__(self):
        self._val += 1
        return self._val


import pybase64
from cv.base_image import image as base_image


def load_image(image):
    img_data = pybase64.b64decode(image)
    img = base_image(img_data).imread()
    return img


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def listToJson(lst):
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False, cls=jsonEncoder)  # json转为string
    return str_json


def ocr_result(ocr, lang, time):
    ret = dict(ocr=ocr, lang=lang, time=time)
    return ret


def get_type(value):
    s = re.findall(r'<class \'(.+?)\'>', str(type(value)))
    if s:
        return s[0]
    else:
        raise ValueError('unknown error,can not get type: value={}, type={}'.format(value, type(value)))


def get_space(SpaceNum=1):
    return '\t'*SpaceNum


def pprint(*args):
    _str = []
    for index, value in enumerate(args):
        if isinstance(value, (dict, tuple, list)):
            _str.append('[{index}]({type}) = {value}\n'.format(index=index, value=_print(value),
                                                                     type=get_type(value)))
        else:
            _str.append('[{index}]({type}) = {value}\n'.format(index=index, value=value,
                                                                   type=get_type(value)))
    print(''.join(_str))


def _print(args, SpaceNum=1):
    _str = []
    SpaceNum += 1
    if isinstance(args, (tuple, list)):
        _str.append('')
        for index, value in enumerate(args):
            _str.append('{space}[{index}]({type}) = {value}'.format(index=index, value=_print(value, SpaceNum),
                                                                    type=get_type(value), space=get_space(SpaceNum)))
    elif isinstance(args, dict):
        _str.append('')
        for key, value in args.items():
            _str.append('{space}[{key}]({type}) = {value}'.format(key=key, value=_print(value,SpaceNum),
                                                                  type=get_type(value), space=get_space(SpaceNum)))
    else:
        _str.append(str(args))

    return '\n'.join(_str)