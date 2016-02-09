import geojson
import random
from bokeh import plotting as plt


def load_geojson(filename):
    """
    Returns a geojson object for the given file.
    """
    with open(filename) as f:
        dat = f.read()
        obj = geojson.loads(dat)
    return obj

# manhattan_simple.geojson is a simple approximation of Manhattan.
# manhattan_complex.geojson is a complex approximation of Manhattan.
# The former has no issues.
# The latter has major ones.
# To switch between the two, switch them here.
def load_coordinates(name, filename="manhattan_simple.geojson"):
    """
    Loads Manhattan.
    What else?
    Are you surprised?

    Later on it ought to be able to load some named city region.
    For now the paramter is quietly ignored.
    """
    obj = load_geojson(filename)
    return list(geojson.utils.coords(obj))


# Borrowed from: http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x,y,poly):
    """
    Checks if a point is inside a polygon.
    Used to validate points as being inside of Manahttan.
    Borrowed from: http://www.ariel.com.au/a/python-point-int-poly.html

    The shapely library provides features for this and other things besides, but is too much to deal with at the moment.
    """

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


def generate_sample_points(coordinate_list, n=1000):
    """
    Generates n uniformly distributed sample points within the given coordinate list.

    When the geometry is sufficiently complex and the list of points large this query can take a while to process.
    """
    lats, longs = list(map(lambda coords: coords[0], coordinate_list)), list(map(lambda coords: coords[1], coordinate_list))
    max_lat = max(lats)
    min_lat = min(lats)
    max_long = max(longs)
    min_long = min(longs)
    ret = []
    while True:
        p_lat = random.uniform(min_lat, max_lat)
        p_long = random.uniform(min_long, max_long)
        if point_inside_polygon(p_lat, p_long, coordinate_list):
            ret.append((p_lat, p_long))
            if len(ret) > n:
                break
        else:
            continue
    return ret


def sample_points(search_location, n=10000):
    """
    Given the name of the location being search, returns n uniformally distributed points within that location.

    Wraps the above.
    """
    return generate_sample_points(load_coordinates(search_location), n)


if __name__ == "__main__":
    manhattan_point_cloud = sample_points("Manhattan", n=1000)
    p = plt.figure(height=500,
                    width=960,
                    title="Manhattan Point Cloud",
                    x_axis_label="Latitude",
                    y_axis_label="Longitude"
                   )

    p.scatter(
        [coord[0] for coord in manhattan_point_cloud],
        [coord[1] for coord in manhattan_point_cloud]
    )

    plt.output_file(filename="manhattan_point_cloud.html")
    plt.show(p)