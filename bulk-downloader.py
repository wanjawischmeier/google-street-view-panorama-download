import streetview
import keys
from routing import GeoapifyRouter
from matplotlib.pyplot import imsave
from os.path import exists
from os import makedirs

waypoints = [(50.783946, 4.453791), (50.798266, 4.463265)]

router = GeoapifyRouter(keys.geoapify)
coords = router(waypoints)
name = "R0, 1160 Auderghem, Belgien"
quality = 1

for coord in coords:
    panoinfos = streetview.panoids(lat=coord[1], lon=coord[0])

    if len(panoinfos) > 0:
        panoinfo = panoinfos[0]
        panoid = panoinfo['panoid']
        if "year" in panoinfo:
            year = panoinfo['year']
        else:
            year = "date_unknown"
        pano_path = f"imgs/{name}/{year}/quality_{quality}"
        pano_file = f"{pano_path}/color ({panoinfo['lat']},{panoinfo['lon']}).jpg"

        if not exists(pano_path):
            makedirs(pano_path)
        
        if not exists(pano_file):
            panorama = streetview.download_panorama(panoid, zoom=quality)
            imsave(pano_file, panorama)
        else:
            print("Panorama already downloaded")
    else:
        print("No panoramas found")