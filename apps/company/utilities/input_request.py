from ctypes.wintypes import PINT


def get_building_information(request):
    building_information_list = []

    site_name = request.POST['site_name']
    building_information_list.append(site_name[0:50])

    address = request.POST['address_b']
    building_information_list.append(address[0:100])

    contact_email = request.POST['contact_email']
    building_information_list.append(contact_email[0:40])

    contact_mobile_number = request.POST['contact_mobile_number']
    building_information_list.append(contact_mobile_number[0:15])

    lat = request.POST['lat']
    building_information_list.append(lat)

    lon = request.POST['lon']
    building_information_list.append(lon)

    return building_information_list

def get_information(request):
    building_information_list = []

    site_name = request.POST['site_name']
    building_information_list.append(site_name[0:50])

    contact_email = request.POST['contact_email']
    building_information_list.append(contact_email[0:40])

    contact_mobile_number = request.POST['contact_mobile_number']
    building_information_list.append(contact_mobile_number[0:15])

    return building_information_list