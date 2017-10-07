
var x = 0;
var y = 0;
var start_point = '000000';
var end_point = '000000';
var blocks = [];
    	 
function cell_select(e){
	var cell = ("000" + e.currentTarget.parentNode.rowIndex).slice(-3) + ("000" + e.currentTarget.cellIndex).slice(-3);
	//window.alert(blocks)
	if(e.ctrlKey){
     	if(cell==end_point){
        	return;
        	}
     	if(blocks.includes(cell)){
        	 blocks.splice(blocks.indexOf(cell), 1);
        	 }
    	document.getElementById("draw_table").rows[parseInt(start_point.slice(0,3))].cells[parseInt(start_point.slice(3,6))].style.backgroundColor = "#FFFFFF";
    	start_point = cell;
    	document.getElementById("draw_table").rows[e.currentTarget.parentNode.rowIndex].cells[e.currentTarget.cellIndex].style.backgroundColor = "#F06251";
    	return;
	 }
	 else if(e.altKey){
    	if(cell==start_point){
        	return;
        	}
       if(blocks.includes(cell)){
        	blocks.splice(blocks.indexOf(cell), 1);
        	}
    	document.getElementById("draw_table").rows[parseInt(end_point.slice(0,3))].cells[parseInt(end_point.slice(3,6))].style.backgroundColor = "#FFFFFF";
    	end_point = cell;
    	document.getElementById("draw_table").rows[e.currentTarget.parentNode.rowIndex].cells[e.currentTarget.cellIndex].style.backgroundColor = "#92F051";
    	return;
	 }
	 
	 if(blocks.includes(cell)){
    	 blocks.splice(blocks.indexOf(cell), 1);
    	 document.getElementById("draw_table").rows[e.currentTarget.parentNode.rowIndex].cells[e.currentTarget.cellIndex].style.backgroundColor = "#FFFFFF";
	 }
	 else{
    	 if(cell==start_point || cell==end_point){
        	 return;
        	 }
    	 blocks.push(cell);
    	 document.getElementById("draw_table").rows[e.currentTarget.parentNode.rowIndex].cells[e.currentTarget.cellIndex].style.backgroundColor = "#38003C";
	 }
	 //window.alert(cell + " - " + start_point + " - " + end_point);
	 }
    	 
function generate_table(){
	 x = parseInt(document.getElementById('value_x').value);
	 y = parseInt(document.getElementById('value_y').value);	 
   
   if(!check_input()){
       return;
   }
	     	 var modal = document.getElementById('entryModal')
	 modal.style.display = 'none';

	     	 var main = document.getElementById('main-container')
	 main.style.display = 'block';
	 
	 var table = document.getElementById('draw_table');
	 for(var i=0; i<x; i++){
    	 var row = table.insertRow(i);
    	 for(var j=0; j<y; j++){
        	 cell = row.insertCell(j)
        	 cell.innerHTML = ""
        	 cell.setAttribute("onclick", "cell_select(event);")
    	 }
	 }
	 start_point = "000000";
	 end_point = ("000" + (x-1)).slice(-3) + ("000" + (y-1)).slice(-3);
	 document.getElementById("draw_table").rows[0].cells[0].style.backgroundColor = "#F06251";
	 document.getElementById("draw_table").rows[x-1].cells[y-1].style.backgroundColor = "#92F051";
	 
	 }
    	 
	 function check_input() {
    	 x = parseInt(document.getElementById('value_x').value);
    	 y = parseInt(document.getElementById('value_y').value);
    	 
    	 if(x < 1 || x > 99){
        	 window.alert("Enter a value within  0-100");
        	 return false;
    	 }
        else if(y < 1 || y > 99){
            window.alert("Enter a value within 0-100");
            return false;
       	 }
        else{
            return true;
            }
    };

    	 
function showOnLoad(){
	 var modal = document.getElementById('entryModal')
	 modal.style.display = 'block';
	 }
    	 	
if (window.addEventListener)
	window.addEventListener("load", showOnLoad, false);
else if (window.attachEvent)
	window.attachEvent("onload", showOnLoad);
else window.onload = showOnLoad;