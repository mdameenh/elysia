    	var player_data;
    	var colSort = {};

       var modal;
              
       function close_modal(){
           modal.style.display = "none";
       }
           	
		function expand_filter(filtername){
             if(document.getElementById(filtername).style.display == "block"){
                 document.getElementById(filtername).style.display = "none";
             }
             else if(document.getElementById(filtername).style.display == "none"){
                 document.getElementById(filtername).style.display = "block";
             }
         }
         

        $(document).ready(function() {
            $('#updateForm').on('submit', function (e) {
                e.preventDefault();
                var player_table = document.getElementById('player_table');
                player_table.style.display = "none";
                document.getElementById('table_spinner').style.display = "block";
                $.ajax({
                    type: 'POST',
                    url: 'update_table/',
                    data: $("#updateForm").serialize(),
                    success: function (response) {
                        player_data = response;
                        player_table.style.display = "table";
                        document.getElementById('table_spinner').style.display = "none";
                        updateSortMap(3, null);
                        sortTable(player_table.rows[0].cells[3]);
                    }
                }); 
                
                return false;               
            });
        });
        
        function getPlayerDetail(rowSelect){
            modal.style.display = "block";
            document.getElementById("detail_spinner").style.display = "block";
            document.getElementById("player_detail").style.display = "none";
            document.getElementById("pl_img").setAttribute("src", "");
            document.getElementById("team_logo").setAttribute("src", "");
            player_id = rowSelect.id.split("_")[1];
            $.ajax({
                type: 'GET',
                url: 'player_details/',
                data: {"req_player_id" : player_id},
                success: function (response) {
                    img_src = "https://platform-static-files.s3.amazonaws.com/premierleague/photos/players/110x140/p" + response["player_photo"]+ ".png"
            		   team_src = "../static/images/logos/" + response["team_id"] + ".png"
                    document.getElementById("pl_img").setAttribute("src", img_src);
		    document.getElementById("team_logo").setAttribute("src", team_src)
                    document.getElementById("pl_name").innerHTML = response["player_name"];
                    document.getElementById("pl_pos_team").innerHTML = response["pos_long"] + " - " + "Man - City";
                    document.getElementById("pl_news").innerHTML = response["news"];
                    if (response["availability"] == "a"){
                        document.getElementById("pl_news").style.backgroundColor = "78F260";
                    }
                    else if(response["availability"] == "d"){
                        document.getElementById("pl_news").style.backgroundColor = "#EFB129";
                    }
                    else{
                        document.getElementById("pl_news").style.backgroundColor = "#F5572E";
                    }
                    
                    player_stats = ["points", "cost", "minutes", "tsb", "ppg",
                                    "goals", "assists", "cleansheet", "transfer_in", 
                                    "transfer_out", "ict_index", "open_play_crosses", 
                                    "big_chances_created", "clearances_blocks_interceptions", 
                                    "recoveries", "key_passes", "tackles", "winning_goals", 
                                    "attempted_passes", "completed_passes", "penalties_conceded", 
                                    "big_chances_missed", "tackled", "offside", 
                                    "target_missed", "fouls", "dribbles"]
                    
                    for(var i = 0; i<player_stats.length; i++){
                        document.getElementById(player_stats[i]+"_ph").innerHTML = response[player_stats[i]];
                    }

                    document.getElementById("detail_spinner").style.display = "none";
                    document.getElementById("player_detail").style.display = "block";
                    
                }
            });             
            
        }
        
        function printTable(inputTable, tableEle){
            var rowCount = tableEle.rows.length;
            for (var i = rowCount - 1; i > 0; i--) {
                tableEle.deleteRow(i);
            }
            
            rowCount = (player_data.length > 50)? 50 : player_data.length;
            for(var count=0; count<rowCount; count++){
                player = inputTable[count];
                var row = tableEle.insertRow(count+1);
                row.setAttribute("id", "player_"+ player[player.length-1].toString());
                row.setAttribute("onclick", "getPlayerDetail(this)");
                for(var cell_count=0; cell_count<(player.length)-1; cell_count++){
                    row.insertCell(cell_count).innerHTML = player[cell_count]
                }
            }            
        }

        
        function sortTable(cellSelect){
            var tableEle = cellSelect.parentElement.parentElement;
            var col = cellSelect.cellIndex;

            if(colSort[col.toString()] == "a"){
                if([0,1,2].includes(col)){
                    sortedTable = player_data.sort(function(a, b) {
                                                          var nameA = a[col]; // ignore upper and lowercase
                                                          var nameB = b[col]; // ignore upper and lowercase
                                                          if (nameA < nameB) {
                                                            return -1;
                                                          }
                                                          if (nameA > nameB) {
                                                            return 1;
                                                          }
                                                        
                                                          return 0;
                                                        });
                }
                else{
                    sortedTable = player_data.sort(function(a,b){return b[col]-a[col];});
                }
                
                updateSortMap(col, "d")
            }
            else if(colSort[col.toString()] == "d"){
                if([0,1,2].includes(col)){
                    sortedTable = player_data.sort(function(a, b) {
                                                          var nameA = a[col]; // ignore upper and lowercase
                                                          var nameB = b[col]; // ignore upper and lowercase
                                                          if (nameA < nameB) {
                                                            return -1;
                                                          }
                                                          if (nameA > nameB) {
                                                            return 1;
                                                          }
                                                        
                                                          return 0;
                                                        });
                    sortedTable.reverse();
                }
                else{
                    sortedTable = player_data.sort(function(a,b){return a[col]-b[col];});
                }
                updateSortMap(col, "a")
            }
            else{
                if([0,1,2].includes(col)){
                    sortedTable = player_data.sort(function(a, b) {
                                                          var nameA = a[col];
                                                          var nameB = b[col];
                                                          if (nameA < nameB) {
                                                            return -1;
                                                          }
                                                          if (nameA > nameB) {
                                                            return 1;
                                                          }
                                                        
                                                          return 0;
                                                        });
                }
                else{
                    sortedTable = player_data.sort(function(a,b){return b[col]-a[col];});
                }
                updateSortMap(col, "d")
            }
            
            printTable(sortedTable, tableEle);
        }
        
        function updateSortMap(sortKey, sortOrder){
            cellLength = document.getElementById("header_row").cells.length;
            for(var i=0; i<cellLength; i++){
                if(i!=sortKey){
                    colSort[i.toString()] = null;
                }
                else{
                    colSort[i.toString()] = sortOrder;
                }
            }
        }