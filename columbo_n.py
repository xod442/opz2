#!/usr/bin/env python
#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    columbo_n.py.py
#                    Rick Kauffman a.k.a. Chewie
#
#
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#   
#
##--------------------------------------------------------------------------
#  Initial release - uses supplied comma seperated MAC address list
#                    builds a return page with found items.
#
#==========================================================================
# Wookieware Web Update
# Complete rewrite of macfind with xmltodict 
# Version 1.0.0
# Last Update 04/01/2015................Chewie@wookieware.com
#==========================================================================

import sys
import cgi
import cgitb; cgitb.enable()
import xmltodict
import requests
from requests.auth import HTTPDigestAuth

#========================Testing VARS


def getform():
  """ Get the values from the calling web form """
  form = cgi.FieldStorage()
  host = form.getvalue('host')
  user = form.getvalue('user')
  passwd = form.getvalue('passwd')
  macz = form.getvalue('macz')
  return (host, user, passwd, macz)

def printhead(pagevar1, pagevar2, pagevar3, host):
  """
  pagevar1 = Header/Title
  pagevar2 = Subtitle
  pagevar3 = Description text
  host = target text
  """
  print ("Content-type:text/html\r\n\r\n")
  print ("<!DOCTYPE html>")
  print ("<html>")
  print ("<head>")
  print ("<title>Columbo</title>")
  print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/tasks.css\"/>")
  print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
  print ("</head>")
  print ("<body>")
  print ("<header>")
  print ("<span>  {} </span>".format(pagevar1)) 
  print ("</header>")
  print ("<main>")
  print ('<section id="mainDisplay">')
  print ("<h3> {} </h3>".format(pagevar2))
  print ("<p> {} {} </p>".format(pagevar3, host))
  print ("<hr>")
  print ('<table id="tblTasks class=.even">')
  print ("<colgroup>")
  print ('<col width="10%">')
  print ('<col width="15%">')
  print ('<col width="15%">')
  print ('<col width="15%">')
  print ('<col width="15%">')
  print ('<col width="20%">')
  print ('<col width="10%">')
  print ("</colgroup>")
  print ("<thead>")
  print ("<tr>")
  print ("<thead>")
  print ("<th>MAC</th>")
  print ("<th>IP Address</th>")
  print ("<th>Interface</th>")
  print ("<th>Device Name</th>")
  print ("<th>Location</th>")
  print ("<th>Contact</th>")
  print ("</tr>")
  print ("</thead>")  

def printfoot(): 
  print ("</table>")
  print ("<nav>") 
  print ('<a href=\"/columbo.html\" id="button">Home</a>')
  print ("</nav>") 
  print ("<footer>")
  print ("API Connected Solutions From WookieWare 2015")
  print ("</footer")
  print ("</body>")
  print ("<script>")
  print ("$(document).ready(function() {")
  print ("$('tbody tr:even').addClass('even');")
  print ("$('tbody tr').click(function(evt) {")
  print ("$(evt.target).closest('td').siblings().andSelf().toggleClass('rowHighlight');")
  print ("});")
  print ("$('#tblTasks tbody').on('click', '.deleteRow', function(evt) {") 
  print ("evt.preventDefault();")
  print ("$(evt.target).parents('tr').remove();") 
  print ("});")
  print ("});")
  print ("</script>")
  print ("</main>")
  print ("</section>")
  print ("</html>")
  
def printpage(pagevar1, pagevar2, user, passwd):
  # Genic return page
  print ("Content-type:text/html\r\n\r\n")
  print ("<!DOCTYPE html>")
  print ("<html>")
  print ("<head>")
  print ("<title> Columbo</title>")
  print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/tasks.css\"/>")
  print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
  print ("</head>")
  print ("<body>")
  print ("<header>")
  print ("<span>  {} </span>".format(pagevar1)) 
  print ("</header>")
  print ("<main>")
  print ('<section id="mainDisplay">')
  print ("<h3> {} </h3>".format(pagevar2))
  print ("<p> {} </p>".format(user))
  print ("<p> {} </p>".format(passwd))
  print ("<nav>") 
  print ('<a href=\"/columbo.html\" id="button">Home</a>')
  print ("</nav>") 
  print ("<footer>")
  print ("API Connected Solutions From WookieWare 2015")
  print ("</footer")
  print ("</body>")
  print ("</script>")
  print ("</main>")
  print ("</section>")
  print ("</html>")

    

def main():
  counter = 0
  host, user, passwd, macz = getform()  
  
  # Split input mac address(es) on the comma
  macz = macz.split(",")
  
  # Print begining of page back to web client
  pagevar1 = "MacFind"
  pagevar2 = "MAC address(es)"
  pagevar3 = "This is the requested information from the IMC server"
  printhead(pagevar1, pagevar2, pagevar3, host)

  for item in macz:
    macAdd = macz[counter].strip()
    api_url='http://{}/imcrs/res/access/realtimeLocate?type=1&value={}'.format(host,macAdd)
    
    try:
      auth=HTTPDigestAuth(user,passwd)
      r = requests.get(api_url, auth=auth)
      my_dict = xmltodict.parse(r.text)
  
    except:
      pagevar1 = "Connection Alert"
      pagevar2 = "System Connection failure"
      pagevar3 = "There has been an error connecting to the IMC target"
      pagevar4 = "Check supplied credentials and try again"
      printpage(pagevar1, pagevar2, user, passwd)
      sys.exit()
    
    # Assign variables from locate API call    
    devIp = my_dict['list']['realtimeLocation']['deviceIp']
    devInt = my_dict['list']['realtimeLocation']['ifDesc']
    deviceId = my_dict['list']['realtimeLocation']['deviceId']
    
    # Get device location information
    
    ip_url='http://{}/imcrs/plat/res/device/{}'.format(host,deviceId)
    
    try:
      auth=HTTPDigestAuth(user,passwd)
      r = requests.get(ip_url, auth=auth)
      my_dev = xmltodict.parse(r.text)
  
    except:
      pagevar1 = "Connection Alert"
      pagevar2 = "System Connection failure"
      pagevar3 = "There has been an error connecting to the IMC target"
      pagevar4 = "Check supplied credentials and try again"
      printpage(pagevar1, pagevar2, user, passwd)
      sys.exit()
    
    devName = my_dev['device']['sysName']
    contact = my_dev['device']['contact']
    devLoc = my_dev['device']['location']
    
    
    #Print table row
    print ("<tr>")
    print ("<td> {} </td>".format(macAdd))
    print ("<td> {} </td>".format(devIp))
    print ("<td> {} </td>".format(devInt))
    print ("<td> {} </td>".format(devName))
    print ("<td> {} </td>".format(devLoc))
    print ("<td> {} </td>".format(contact))
    print ("</tr>")
     
    counter = counter + 1
  printfoot()


# Start program
if __name__ == "__main__":
   main()
