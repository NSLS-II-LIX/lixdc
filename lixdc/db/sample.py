import collections
import pandas
import amostra.client.commands as acc

container_ref = acc.ContainerReference()
sample_ref = acc.SampleReference()


def insert_plate(plate_info):
    plate = container_ref.create(**plate_info)
    return plate


def insert_sample_list(samples):
    result = collections.deque()
    for s in samples:
        result.append(sample_ref.create(**s))

    return result


def find_plate_by_barcode(owner, project, beamline_id, barcode, fill=True):
    samples = collections.deque()
    try:
        plate_info = list(container_ref.find(owner=owner, project=project, beamline_id=beamline_id, barcode=barcode))[0]
    except IndexError:
        return None

    if fill:
        for s_uid in plate_info['content']:
            samples.append(next(sample_ref.find(uid=s_uid)))

        plate_info['content'] = list(samples)

    return plate_info


def import_plate_from_excel(fname, owner, project, beamline_id, plate_kind):
    samples = collections.deque()
    excel_data = pandas.read_excel(fname,header=1)
    barcode = ""

    for line in excel_data.iterrows():
        if line[0] == 0:
            name = line[1][0]
            barcode = str(int(line[1][1])).zfill(13)
            plate_info = {
                "owner": owner,
                "project": project,
                "beamline_id": beamline_id,
                "kind": plate_kind,
                "name": name,
                "barcode": barcode,
            }
        s_y = line[1][2]
        s_x = line[1][3]
        s_name = line[1][4]
        s_shortname = line[1][5]
        s_conc = line[1][6]
        s_volume = line[1][7]
        s_temperature = line[1][8]
        sample_info = {
                "project": project,
                "beamline_id": beamline_id,
                "owner": owner,
                "name": s_name,
                "short_name": s_shortname,
                "position": {"x": s_x, "y": s_y},
                "concentration": s_conc,
                "volume": s_volume,
                "temperature": s_temperature
            }
        samples.append(sample_info)

    # Add the samples to the database
    samples_uid = sample_ref.create_sample_list(samples)

    # Add the Samples uid list to the plate data
    plate_info["content"] = samples_uid
    # Add the plate to the database
    container_ref.create(**plate_info)

    # Return the plate data filled with the sample data
    return find_plate_by_barcode(owner, project, beamline_id, barcode)
