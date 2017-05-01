
html_str = """
<table border=1>
     <tr>
       <th>Number</th>
       <th>Square</th>
     </tr>
     <indent>
     <% for i in range(10): %>
       <tr>
         <td><%= i %></td>
         <td><%= i**2 %></td>
       </tr>
     </indent>
</table>
"""

for i in range(5):
    file_name = 'htmlfile' + str(i)
    Html_file = open(file_name, "w")
    Html_file.write(html_str)
    Html_file.close()
