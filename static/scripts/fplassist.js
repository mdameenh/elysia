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
    team_map = {1:'Arsenal', 2:'Bournemouth', 3:'Brighton', 4:'Burnley', 5:'Chelsea', 
                6:'Crystal Palace', 7:'Everton', 8:'Huddersfield', 9:'Leicester', 10:'Liverpool', 
                11:'Manchester City', 12:'Manchester United', 13:'Newcastle', 14:'Southampton', 15:'Stoke City', 
                16:'Swansea', 17:'Tottenham Spurs', 18:'Watford', 19:'West Brom', 20:'West-Ham', }
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
            document.getElementById("pl_pos_team").innerHTML = response["pos_long"] + " - " + team_map[response["team_id"]];
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

            var ctx = document.getElementById("canvas").getContext("2d");
            config = getChartData(response["points_history"], response["ict_history"])
            window.myLine = new Chart(ctx, config);
            
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

function getChartData(points_hist, ict_hist){
    var _list = [];
    for(var i = 1; i<=points_hist.length; i++){
        _list.push(i);
    }
    window.chartColors = {
        	red: 'rgb(255, 99, 132)',
        	orange: 'rgb(255, 159, 64)',
        	yellow: 'rgb(255, 205, 86)',
        	green: 'rgb(75, 192, 192)',
        	blue: 'rgb(54, 162, 235)',
        	purple: 'rgb(153, 102, 255)',
        	grey: 'rgb(231,233,237)'
        };
    var config = {
        type: 'line',
        data: {
            labels: _list,
            datasets: [{
                label: "Points",
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: points_hist,
                fill: false,
            }, {
                label: "ICT Index",
                fill: false,
                backgroundColor: window.chartColors.blue,
                borderColor: window.chartColors.blue,
                data: ict_hist,
            }]
        },
        options: {
            responsive: true,
            title:{
                display:true,
                text:'Chart.js Line Chart'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };
    return config
}