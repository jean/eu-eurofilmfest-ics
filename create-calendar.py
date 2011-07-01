from lxml.html.soupparser import fromstring

# Grabbed from http://s3.amazonaws.com/statichtmlplus/page_tab3/160579703997119.html
html = fromstring(open('eurofilmfest.html').read().decode('utf-8'))

trs = html.findall('.//tr')
trs = trs[4:]
trs = trs[:-1]
movies = []
for i in range(len(trs))[::2]:
    movies.append( (trs[i], trs[i+1]) )

#
# Grab text content
#
def do_kids(node, tt=[]):
  for n in node.getchildren():
    text = n.text and n.text.strip() or ''
    tail = n.tail and n.tail.strip() or ''
    if text:
      tt.append(text.strip())
    if tail:
      tt.append(tail.strip())
    if n.getchildren():
      tt = do_kids(n, tt)
  return tt

#
# Give the text some structure
#
movies_d = {}
for m in movies:
  ll = do_kids(m[0], [])
  country = ll[0]
  movie = ll[1]
  showtimes = [t for t in ll[2:] if not t.startswith('Sorry')]
  showtimes_d = {}
  for t in showtimes:
    if t == 'Showtime in Bangkok:':
      city = 'Bangkok Art and Culture Centre'
      print 'Bangkok'
      continue
    if t == 'Showtime in Chiangmai:':
      city = 'Chiangmai Vista Kadsuankaew'
      print 'Chiangmai'
      continue
    times = showtimes_d.get(city, [])
    times.append(t)
    showtimes_d[city] = times
  ll = do_kids(m[1], [])
  eng_desc = ll[0]
  thai_desc = ll[1]
  movies_d[movie] = {
        'city': city,
        'country': country,
        'showtimes': showtimes_d,
        'en': eng_desc,
        'th': thai_desc, 
        }

#
# Write an ICS file
#
from icalendar import Calendar, Event
cal = Calendar()
from datetime import datetime
from icalendar import LocalTimezone
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

# I'm running this in Bangkok
lt = LocalTimezone()

for movie, props in movies_d.items():
  for city, shows in props['showtimes'].items():
    for show in shows:
      try:
        dt = datetime.strptime(show+" 2011", "%a, %d %B, %H:%M %Y")
      except ValueError:
        dt = datetime.strptime(show+" 2011", "%a, %d %B at %H:%M %Y")
      dt = dt.replace(tzinfo=lt)
      event = Event()
      event.add('summary', movie)
      event.add('location', city)
      event.add('description', '\n'.join(
            [props['country'], props['en'], props['th']]))
      event.add('dtstart', dt)
      event.add('dtstamp', datetime.now())
      cal.add_component(event)

f = open('eurofilmfest.ics', 'wb')
# Google calendar doesn't like DTSTART;VALUE=DATE:20110716T072000Z
f.write(cal.as_string().replace(';VALUE=DATE', ''))
f.close()
