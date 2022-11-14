# blogpost-db-application

This application supports some basic commands for a blogpost application. 
The commands are as follows: 
 - post
 - comment
 - delete
 - show
 - find


Command structure and sample commands for reference:
All strings except the command name in the first will be between double inverted commas

 - post blogName userName title postBody tags timestamp
   post "Poem" "Yash Srivastava" "Last Leaf" "one last leaf is like life" "life,poetry" "14/11/2022 1:31pm" 

 - comment blogname permalink userName commentBody timestamp
   comment "Poem" "Poem.Last_Leaf" "Neel Gandhi" "good poem" "14/11/2022 2:01pm" 

 - delete blogname permalink userName timestamp
   delete "Poem" "Poem.Last_Leaf" "Neel Gandhi" "14/11/2022 3:34pm"

 - show blogName
   show "Poem"

 - find blogName searchString
   find "Poem" "leaf" 