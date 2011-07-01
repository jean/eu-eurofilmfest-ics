Calendar for the European Film Festival, Thailand, 2011
=======================================================

I like to be able to set reminders for the films I'm interested in, 
and the HTML version of the program doesn't allow this. 

So I wrote a script to convert the HTML page to an ICS file.

The HTML is wildly inconsistent. More or less the only consistent thing 
is the order in which the information is presented. So I used that. 

Usage
-----

* Grab the schedule from
  http://s3.amazonaws.com/statichtmlplus/page_tab3/160579703997119.html
  and save it as `eurofilmfest.html`.
* Run the script. 
* Create a Google calendar.
* Import the generated `eurofilmfest.ics` file.

The imported calendar can be found at 
https://www.google.com/calendar/embed?src=jp0qve10ohl5s09ponb34h6sds%40group.calendar.google.com&ctz=Asia/Bangkok

Dependencies
------------

* http://pypi.python.org/pypi/ElementSoup
* http://pypi.python.org/pypi/icalendar

Improvements
------------

Come on, lazyweb.

It would be cool to run this on Google App Engine, pulling the programme
from the origin URL and serving the conversion as ICS.  That way, the
calendar will stay up to date if the programme changes, *if* the format
stays the same. That's a big "if". 

Problems
--------

1. The encoding gets screwed up when the string is written to a file. As
   a result, the Thai descriptions are scrambled.
2. It may have been better to create seperate calendars for Bangkok and 
   Chiang Mai.
