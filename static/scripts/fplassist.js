    	 var colList = [];
    	 var fullColList = [];
    	 var player_data;
    	 
        function genInfoFilter(divName, filterInfo){
           for(var i=0; i<filterInfo.length; i++){
               var a = $('#'+divName).append("<div></div>")
                       .children("div").not("[id]");
               a.attr("id", filterInfo[i]['name'].toLowerCase()+"-input");
               
               a.append("<div class='filter-name'></div>")
               .children("div.filter-name").text(filterInfo[i]['name']);
               
               var c = a.append("<div class='filter-entry'></div>")
               .children("div.filter-entry");
               
               for(var j=0; j<filterInfo[i]["values"].length; j++){
                   c.append("<input class='info-class'>");
                   c.children("input.info-class").not("[type]").attr({
                        "name" : filterInfo[i]['name'].toLowerCase(),
                        "value" : filterInfo[i]["values"][j],
                        "type" : "checkbox",
                        "checked" : "checked"
                    });
                    
                   c.append("<label class='filter-label'>");
                   c.children("label.filter-label").not("[id]")
                   .attr("id", "label-id").text(filterInfo[i]["values"][j]);
                   
                   c.append("<br>");
               }
           }
           return 1;
        }
        
        function genStatFilter(divName, filterInfo){
            for(var i=0; i<filterInfo.length; i++){
                var a = $('#'+divName).append("<div></div>")
                        .children("div").not("[id]");
                a.attr("id", filterInfo[i]['name'].toLowerCase()+"-input");
                
                a.append("<div class='filter-name'></div>")
                .children("div.filter-name").html(filterInfo[i]['name']+"<br>");

               var c = a.append("<div class='filter-entry'></div>")
               .children("div.filter-entry");
               
               c.append("<input class='stat-class'>");
               c.children("input.stat-class").not("[type]").attr({
                    "name" : filterInfo[i]["name"].toLowerCase()+"_min",
                    "value" : filterInfo[i]["values"]["min"],
                    "min" : filterInfo[i]["values"]["min"],
                    "max" : filterInfo[i]["values"]["max"],
                    "step" : filterInfo[i]["values"]["step"],
                    "type" : "number"
                });
                
               c.append("<input class='stat-class'>");
               c.children("input.stat-class").not("[type]").attr({
                    "name" : filterInfo[i]["name"].toLowerCase()+"_max",
                    "value" : filterInfo[i]["values"]["max"],
                    "min" : filterInfo[i]["values"]["min"],
                    "max" : filterInfo[i]["values"]["max"],
                    "step" : filterInfo[i]["values"]["step"],
                    "type" : "number"
                });
                
                c.append("<br>");
            }
        
        }

        function writePlayerTable(filteredPlayerData){
            $("tr[id^='player_']").hide();
            var resultCount = $("input[name='num-results'").val();
            for(var i=0; i<filteredPlayerData.length; i++){
                if(i<resultCount){
                    $("tr[id='player_"+filteredPlayerData[i]["id"]+"']").show();
                }
                else{
                    break;
                }
            }
        }

        function createPlayerTable(){
            $("#misc_options").find("input.info-class").each(function(){
                if($(this).prop("checked") == false){
                    colList.push($(this).val());
                }
                fullColList.push($(this).val());
            });
            
            var tableBody = $("#table-container").append("<table id='player-table'><thead></thead><tbody></tbody></table>")
                            .find("tbody");
            var tableHead = $("#table-container").find("thead");
                            
            
            $.ajax({
                type: 'GET',
                url: 'get_data/',
                data: {},
                success: function(response){
                    player_data = response;
                    var resultCount = $("input[name='num-results'").val();
                    
                    tableHead.append("<tr id='header-row'><th>Name</th></tr>");
                    var headerRow = tableHead.children("#header-row");
                    for(var i=0; i<fullColList.length; i++){
                        headerRow.append("<th class='col-"+fullColList[i].toLowerCase()+"'>"+fullColList[i]+"</th>");
                    }
                    
                    for(var i=0; i<player_data.length; i++){
                        tableBody.append("<tr id='player_"+player_data[i]["id"]+"'><td>"+player_data[i]["name"]+"</td></tr>");
                        var playerRow = tableBody.children("#player_"+player_data[i]["id"]);
                        
                        for(var j=0; j<fullColList.length; j++){
                            playerRow.append("<td class='col-"+fullColList[j].toLowerCase()+"'>"+player_data[i][fullColList[j].toLowerCase()]+"</td>");
                        }                        
                    }
                    
                    $("#player-table").tablesorter({theme: 'default'});
                    
                    $("tr:gt("+resultCount.toString()+")").hide();
                    
                    for(var i=0; i<colList.length; i++){
                        $("th.col-"+colList[i].toLowerCase()).hide();
                        $("td.col-"+colList[i].toLowerCase()).hide();
                    }
                    $('.loader').hide();
                }
            });
            
                
        }
        
        var checkedFilters=[];
        var filterVals = {};
        var filterListItems = [];
        function isFit(playerObj){
            if(!(checkedFilters.includes(playerObj["position"]))){
                return false;
            }
            else if(!(checkedFilters.includes(playerObj["team"]))){
                return false;
            }
            else if(!(checkedFilters.includes(playerObj["availability"]))){
                return false;
            }
            else if(!(checkedFilters.includes(playerObj["difficulty"]))){
                return false;
            }
            else if(playerObj["points"] < filterVals["points_min"] || playerObj["points"] >= filterVals["points_max"]){
                return false;
            }         

            for(var i=0; i<filterListItems.length; i++){
                var tmpFilterItem = filterListItems[i].toLowerCase();
                if(playerObj[tmpFilterItem] < filterVals[tmpFilterItem+"_min"] || playerObj[tmpFilterItem] >= filterVals[tmpFilterItem+"_max"]){
                    return false;
                }
            }

            return true;

        }
        
        
        function genFilterData(){
            checkedFilters = [];
            $(document).find("#player_info .info-class").each(function(){
               if($(this).prop("checked") == true){
                   checkedFilters.push($(this).val());
               }
            });
            
            filterVals= {};
            $(document).find("#player_base .stat-class").each(function(){
                filterVals[$(this).attr("name")] = $(this).val();
            });

            $(document).find("#player_deep .stat-class").each(function(){
                filterVals[$(this).attr("name")] = $(this).val();
            });
            
            writePlayerTable(player_data.filter(isFit));
        }
        
        
        $(function(){
            var unchecked_default = [];
            $('.loader').fadeIn();
            
            $('#filter-btn').click(function(){
                $('#filter-container').toggle("slide", {direction:"left"}, 300);
            });
            
            $('.filter-header').click(function(){
                $(this).siblings('.filter-categories').toggle(300);
            })
            
            $(document).on("click", '.filter-name', function(){
                $(this).next('.filter-entry').toggle(300);
            });
            
            $(document).on("change", 'input[name="num-results"]', function(){
                $("#player_info .info-class").each(function(){
                    $(this).prop("checked", true); 
                });

                var tmpRsltCount = $(this).val();
                
                if(tmpRsltCount > 100){tmpRsltCount = 100;}
                
                $("tr:lt("+tmpRsltCount.toString()+")").show(300);
                $("tr:gt("+tmpRsltCount.toString()+")").hide(300);
            });
            
            $(document).on("change", ".info-class[name='columns']", function(){
               var tmpColFilter = $(this).val();
               $("th.col-"+tmpColFilter.toLowerCase()).toggle(500);
               $("td.col-"+tmpColFilter.toLowerCase()).toggle(500); 
            });
            
            $(document).on("change", "#player_info .info-class", genFilterData);
            $(document).on("change", "#player_base .stat-class", genFilterData);
            $(document).on("change", "#player_deep .stat-class", genFilterData);
            
            $.ajax({
                type: 'GET',
                url: 'get_filters/',
                data: {},
                success: function (response) {
                   var statusInfo = genInfoFilter("player_info", response["player_info"]);
                   var statusBaseStat = genStatFilter("player_base", response["player_base"]);
                   var statusDeepStat = genStatFilter("player_deep", response["player_deep"]);
                   var statusInfo = genInfoFilter("misc_options", response["misc_options"]);
                   
                   unchecked_default = response["unchecked_default"];
                   filterListItems = response["misc_options"][0]["values"];
                   
                   var mo = $("#misc_options.filter-categories")
                            .append("<div id='results-input'></div>")
                            .children("#results-input");
                   mo.append("<div class='filter-name'>No-Of-Results<br><div/>")
                   var inp = mo.append("<div class='filter-entry'></div>")
                             .children(".filter-entry");
                   inp.append("<input class='stat-class' name='num-results' value=50 min=0 max=200 step=1><br>")
                   
                   for(var i=0; i<unchecked_default.length; i++){
                       $("#misc_options").find("input[value='"+unchecked_default[i]+"']").prop("checked", false);
                   }
                   
                   var statusCreateTable = createPlayerTable();
                   
                   
                }
            });
        
            
        });