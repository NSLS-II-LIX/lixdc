import collections
import pandas
import amostra.client.commands as acc
from lixdc.conf import load_configuration

config_params = {k: v for k, v in load_configuration('lixdc', 'LIXDC',
                                                     [
                                                      'amostra_host',
                                                      'amostra_port',
                                                     ]
                                                     ).items() if v is not None}

host, port = config_params['amostra_host'], config_params['amostra_port']
request_ref = acc.RequestReference(host=host, port=port)


def upsert_request(req_info):
    if 'uid' in req_info:
        req = req_info['uid']
        q = {'uid': req_info.pop('uid', '')}
        request_ref.update(q, cont_info)
    else:
        req = request_ref.create(**req_info)
    return req

def find_requests(**kwargs):
    return list(request_ref.find(**kwargs))

def find_request_by_barcode(owner, proposal_id, beamline_id, barcode):
    try:
        req_info = list(container_ref.find(owner=owner, proposal_id=proposal_id,
                                             beamline_id=beamline_id,
                                             container_barcode=barcode))[0]
    except IndexError:
        return None

    return req_info
