
function addToNodesTable(node){
    
    var type = node['type']
    var host = node['host']
    var port = node['port']
    var params = node['params']
    
    var newRow = "<tr>"
    newRow += "<td class='col-md-2'>" + type + "</td>"
    newRow += "<td class='col-md-4'>" + host + "</td>"
    newRow += "<td class='col-md-2'>" + port + "</td>"
    newRow += "<td class='col-md-6'>" + params + "</td>"
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-danger btn-xs'></button></td>"
    newRow += "</tr>"
    $('#nodesTable tr:last').after(newRow);
}

function buildNodesTable(nodes){
    
    $('#nodesTable').html("<tr><th class='col-md-2'>Type</th><th class='col-md-4'>Host/IP</th><th class='col-md-2'>Port</th><th  class='col-md-6'>Parameters</th><th class='col-md-1'>  </th></tr>")
    for (var i = 0; i < nodes.lenth; i++){
        addToNodesTable(nodes[i])
    }
    
}

$(document).ready(function(){
    
    buildNodesTable()
    
});