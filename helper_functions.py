import math


s = 86164.09  # one sidereal day
R = 6367444.5  # radius of the earth


# Takes in fixed spherical coordinates in DMS format and converts to cartesian position.
# NS and EW are either 1 or -1, 1 for North and East, -1 for South and West
def polar_to_cart(lat_deg, lat_min, lat_sec, NS, long_deg, long_min, long_sec, EW, altitude):
    lat_rads = NS * rads(lat_deg, lat_min, lat_sec)
    long_rads = EW * rads(long_deg, long_min, long_sec)
    r = R + altitude
    return r * math.sin(lat_rads) * math.cos(long_rads), r * math.sin(lat_rads) * math.sin(long_rads), r * math.cos(
        lat_rads)


# Converts cartesian coordinates to polar coordinates and returns in DMS format.
# If z < 0, theta is negative
def cart_to_polar(x, y, z):
    NS = z / abs(z)
    EW = y / abs(y)
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    if x != 0:
        theta = math.arctan(y / x)
    else:
        theta = math.pi / 2

    if x >= 0:
        theta = abs(theta)
    elif x < 0 <= y:
        theta = abs(theta + math.pi)
    elif x < 0 and y < 0:
        theta = abs(theta - math.pi)

    phi = math.arccos(abs(z) / r)
    altitude = r - R
    (lat_deg, lat_min, lat_sec) = dms(math.pi / 2 - phi)
    (long_deg, long_min, long_sec) = dms(theta)

    return lat_deg, lat_min, lat_sec, NS, long_deg, long_min, long_sec, EW, altitude


# Takes in radians and returns a vector of (degrees, minutes, seconds).
# Both degrees and minutes are integers, while seconds is a float
def dms(radians):
    # get seconds first
    temp = radians * 180 * 3600 / math.pi
    seconds = temp % 60
    # get minutes next
    temp = int(math.floor(temp / 60))
    minutes = temp % 60
    # get degrees last
    degrees = int(math.floor(temp / 60))
    return degrees, minutes, seconds


# Takes in degrees, minutes, seconds and returns radians
def rads(degrees, minutes, seconds):
    # convert to seconds first
    temp = degrees * 3600 + minutes * 60 + seconds
    return temp * math.pi / (3600 * 180)
