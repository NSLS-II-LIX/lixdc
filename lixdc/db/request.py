import collections
import pandas
import amostra.client.commands as acc

request_ref = acc.RequestReference()

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

def find_request_by_barcode(owner, project, beamline_id, barcode):
    try:
        req_info = list(container_ref.find(owner=owner, project=project,
                                             beamline_id=beamline_id,
                                             container_barcode=barcode))[0]
    except IndexError:
        return None

    return req_info
