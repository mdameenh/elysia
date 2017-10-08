async function pathfinder_djikstra(e){

    var unvisited_nodes = [];
    var current_node = {'index':start_point, 'distance':0};
    var neighbour_nodes = {};
    var destination_node = end_point;
    var all_nodes = [];
    
    for(var i=0; i<x; i++){
        for(var j=0; j<y; j++){
            t_cell = getCellString(i,j)
            if(!(blocks.includes(t_cell))){
                unvisited_nodes.push(t_cell);
                all_nodes[t_cell] = x*y;
                }
            }
    }
    
    neighbour_nodes[x*y] = find_neighbours(current_node['index']);
    unvisited_nodes.splice(unvisited_nodes.indexOf(current_node['index']), 1);
    
    while(unvisited_nodes.includes(destination_node)){
        if(neighbour_nodes[x*y].length == 0){
            break;
        }
        
        neighbour_distances = Object.keys(neighbour_nodes).sort(function(a, b){return a - b});
        closest_neighbours = neighbour_nodes[neighbour_distances[0]];
        current_distance = current_node['distance'];
        
        for(neighbour in closest_neighbours){
            if(closest_neighbours[neighbour]!=end_point){
                document.getElementById("draw_table").rows[parseInt(closest_neighbours[neighbour].slice(0,3))].cells[parseInt(closest_neighbours[neighbour].slice(3,6))].style.backgroundColor = "#7e7f7d";
                await sleep(1);
            }
            current_node = {'index':closest_neighbours[neighbour], 'distance':current_distance+1};
            if(unvisited_nodes.includes(current_node['index'])){
                unvisited_nodes.splice(unvisited_nodes.indexOf(current_node['index']), 1);
                t_neighbours = find_neighbours(current_node['index']);
                for(t_neighbour in t_neighbours){
                    if(!(neighbour_nodes[x*y].includes(t_neighbours[t_neighbour]) || t_neighbours[t_neighbour]==start_point)){
                        if(unvisited_nodes.includes(t_neighbours[t_neighbour])){
                            neighbour_nodes[x*y].push(t_neighbours[t_neighbour])
                        }
                    }
                }
            }
            neighbour_nodes[neighbour_distances[0]].splice(neighbour, 1);
        }
    }
    
    //out of loop. do post processing here...
    if(unvisited_nodes.includes(destination_node)){
        window.alert("No path found! Try again with a different map.")
    }
    
    window.alert("Djikstra!");
}

function find_neighbours(t_cell){
    var neighbours = [];
    t_x = parseInt(t_cell.slice(0,3));
    t_y = parseInt(t_cell.slice(3,6));
    
    lower_bound = [t_x-1 > 0 ? t_x-1 : 0, t_y-1 > 0 ? t_y-1 : 0];
    upper_bound = [t_x+1 < x ? t_x+1 : x-1, t_y+1 < y ? t_y+1 : y-1];
    
    for(var i=lower_bound[0]; i<=upper_bound[0]; i++){
        for(var j=lower_bound[1]; j<=upper_bound[1]; j++){
            if(!(blocks.includes(t_cell))){
                if(i==t_x && j==t_y){
                //do nothing
                }
                else{
                    neighbours.push(getCellString(i,j));
                }
                }
            }
        }
        
    return neighbours;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
