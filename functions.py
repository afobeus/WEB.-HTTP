def get_size(geo_object):
    upper_corner = geo_object["boundedBy"]["Envelope"]["upperCorner"]
    upper_corner_x, upper_corner_y = map(float, upper_corner.split())
    lower_corner = geo_object["boundedBy"]["Envelope"]["lowerCorner"]
    lower_corner_x, lower_corner_y = map(float, lower_corner.split())
    return upper_corner_x - lower_corner_x, upper_corner_y - lower_corner_y
