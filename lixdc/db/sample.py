import os
import collections
import pandas
import amostra.client.commands as acc
import lixdc
from lixdc.conf import load_configuration

path = os.path.dirname(lixdc.__file__)+"/"

CONTAINER_TYPES = { "96 Well Plate": {"id": "96wp",
                                      "cols": 12,
                                      "rows": 8,
                                      "cols_letters": False,
                                      "rows_letters": True,
                                      "image": "{}96wp.png".format(path)},
                   "12 Cells": {"id": "12cells",
                                "cols": 6,
                                "rows": 2,
                                "cols_letters": False,
                                "rows_letters": False,
                                "image": "{}12cells.png".format(path)}
                   }

config_params = {k: v for k, v in load_configuration('lixdc', 'LIXDC',
                                                     [
                                                      'amostra_host',
                                                      'amostra_port',
                                                      ]
                                                     ).items() if v is not None}

host, port = config_params['amostra_host'], config_params['amostra_port']
container_ref = acc.ContainerReference(host=host, port=port)
sample_ref = acc.SampleReference(host=host, port=port)


def get_container_type_by_id(cont_id):
    for k, v in CONTAINER_TYPES.items():
        if v['id'] == cont_id:
            return v
    return None

def upsert_container(cont_info):
    if 'uid' in cont_info:
        cont = cont_info['uid']
        q = {'uid': cont_info.pop('uid', '')}
        container_ref.update(q, cont_info)
    else:
        cont = container_ref.create(**cont_info)
    return cont


def upsert_sample_list(samples):
    result = []
    for s in samples:
        if 'uid' in s and s['uid'] != "":
            q = {'uid': s['uid']}
            s.pop('uid', '')
            sample_ref.update(q, s)  # TODO: Check if this can fail this way
            result.append(q['uid'])
        else:
            s.pop('uid', '')
            result.append(sample_ref.create(**s))

    return result


def find_containers(**kwargs):
    return list(container_ref.find(**kwargs))


def find_container_by_barcode(owner, proposal_id, beamline_id, barcode, fill=True):

    try:
        cont_info = list(container_ref.find(owner=owner, proposal_id=proposal_id,
                                             beamline_id=beamline_id,
                                             barcode=barcode))[0]
    except IndexError:
        return None

    if fill:
        fill_container(cont_info)

    return plate_info


def fill_container(cont_info):
    samples = collections.deque()

    for s_uid in cont_info['content']:
        samples.append(next(sample_ref.find(uid=s_uid)))

    cont_info['content'] = list(samples)

def validate_sample(sample):
    if sample['name'] is None or sample['name'] == "":
        return False, "Sample Name is required."
    if sample['concentration'] is None or sample['concentration'] < 0:
        return False, "Sample Concentration needs to be > 0 mg/ml."
    if sample['volume'] is None or sample['volume'] < 0:
        return False, "Sample Volume needs to be > 0 ul."
    if sample['temperature'] is None:
        return False, "Sample Temperature is required."

    return True, ""
