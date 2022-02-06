# http://stjarnhimlen.se/comp/ppcomp.html
# http://www.stjarnhimlen.se/comp/tutorial.html


from numpy import pi, sin, cos, sqrt, arctan2, arcsin
from orbital_elements import *


def day(y, m, D, UT):
    d = 367*y - 7 * ( y + (m+9)//12 ) // 4 + 275*m//9 + D - 730530
    d = d + UT/24.0
    return d

def floor(x):
    if x<0:
        return int(x)-1
    else:
        return int(x)

    
def obl_ecl(d):
    """obliquity of the ecliptic (tilt of the Earth's axis of rotation)"""
    ecl = 23.4393 - 3.563E-7 * d
    return ecl


def getE(ec, m, dp=5):
    # http://www.jgiesen.de/kepler/kepler.html
    K = pi/180
    maxIter=30
    i=0
    delta = 10**-dp
    m = m/360.0
    m = 2 * pi * (m-floor(m))
    if ec<0.8:
        E=m
    else:
        E=pi
    F = E - ec*sin(m) - m
    while ((abs(F)>delta) and (i<maxIter)):
        E = E - F/(1-ec*cos(E))
        F = E - ec*sin(E) - m
        i = i + 1
    E = E/K
    return round(E*(10**dp)) / (10**dp)


def get_sun(d, lon_corr):
    N,i,w,a,e,M = sun_oe(d)
    E = M + e*(180/pi) * sin(M*(pi/180)) * ( 1.0 + e * cos(M*(pi/180)) )
    xv = cos(E*(pi/180)) - e
    yv = sqrt(1 - e**2) * sin(E*(pi/180))
    r = sqrt(xv**2 + yv**2)
    v = arctan2(yv, xv) *(180/pi)
    lonsun = v + w
    # kh: not sure if I should add this:
    #lonsun = lonsun + lon_corr 

    xs = r * cos(lonsun*(pi/180))
    ys = r * sin(lonsun*(pi/180))
    #zs = 0
    return xs, ys

def helio(N,i,w,a,e,M):
    """heliocentric position of planet"""
    E = getE(e,M)
    
    xv = a * (cos(E*(pi/180)) - e)
    yv = a * (sqrt(1 - e**2) * sin(E*(pi/180)))

    r = sqrt(xv**2 + yv**2)
    v = arctan2(yv, xv) *(180/pi)

    xh = r * ( cos(N*(pi/180)) * cos((v+w)*(pi/180)) - sin(N*(pi/180)) * sin((v+w)*(pi/180)) * cos(i*(pi/180)) )
    yh = r * ( sin(N*(pi/180)) * cos((v+w)*(pi/180)) + cos(N*(pi/180)) * sin((v+w)*(pi/180)) * cos(i*(pi/180)) )
    zh = r * ( sin((v+w)*(pi/180)) * sin(i*(pi/180)) )
    return xh, yh, zh, r

def helio_to_geoeq(xh, yh, zh, d, r):
    # ecliptic longitude and latitude
    lonecl = arctan2(yh, xh)*(180/pi)
    latecl = arctan2(zh, sqrt(xh**2+yh**2))*(180/pi)

    Epoch = 2000
    lon_corr = 3.82394E-5 * ( 365.2422 * ( Epoch - 2000.0 ) - d )
    # Not sure if i should add it:
    #lonecl = lonecl + lon_corr

    xh = r * cos(lonecl*(pi/180)) * cos(latecl*(pi/180))
    yh = r * sin(lonecl*(pi/180)) * cos(latecl*(pi/180))
    zh = r                        * sin(latecl*(pi/180))

    xs, ys = get_sun(d, lon_corr)

    xg = xh + xs
    yg = yh + ys
    zg = zh

    # convert rectangular, ecliptic coordinates to rectangular, equatorial coordinates
    ecl = obl_ecl(d)
    
    xe = xg
    ye = yg * cos(ecl*(pi/180)) - zg * sin(ecl*(pi/180))
    ze = yg * sin(ecl*(pi/180)) + zg * cos(ecl*(pi/180))
    return xe, ye, ze

def geoeq_to_radec(xe, ye, ze):
    ra  = arctan2(ye, xe)*(180/pi)
    dec = arctan2(ze, sqrt(xe**2 + ye**2))*(180/pi)
    rg = sqrt(xe**2 + ye**2 + ze**2)
    return ra, dec, rg
    

d = day(1990, 4, 19, 0)
N,i,w,a,e,M = mercury_oe(d)
#print(N,i,w,a,e,M)
xh, yh, zh, r = helio(N,i,w,a,e,M)
#print(xh, yh, zh)
xe, ye, ze = helio_to_geoeq(xh, yh, zh, d, r)
#print(xe, ye, ze)
ra, dec, rg = geoeq_to_radec(xe, ye, ze)
print(ra, dec, rg)
