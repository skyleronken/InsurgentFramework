
function activaTab(tab){
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
};

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
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-danger btn-sm removeNode'><span class='glyphicon glyphicon-minus' aria-hidden='true'></button></td>";
    newRow += "</tr>"
    $('#nodesTable tr:last').after(newRow);
    
    $('#nodesTable tr:last button.removeNode').click(function() {
       var $this = $(this);
       $this.parents('tr').remove();
    });
}

function addToCommandsTable(cmd){
    
    var cmd_name = cmd['name']
    var cmd_module = cmd['module']
    
    var newRow = "<tr>"
    newRow += "<td class='col-md-2'>" + cmd_name + "</td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-primary btn-sm editCommand'><span class='glyphicon glyphicon-pencil' aria-hidden='true'></span></button></td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-danger btn-sm removeCommand'><span class='glyphicon glyphicon-minus' aria-hidden='true'></button></td>";
    newRow += "</tr>"
    $('#commandsTable tr:last').after(newRow);
    
    $('#commandsTable tr:last button.removeCommand').click(function() {
       var $this = $(this);
       $this.parents('tr').remove();
       $('#'+cmd_module+'_li').show()
    });
    
}

function addToEncodersTable(encoder, table){
    
    var encoder_name = encoder['name']
    var encoder_module = encoder['module']
    
    var newRow = "<tr>"
    newRow += "<td class='col-md-2'>" + encoder_name + "</td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-primary btn-sm editEncoder'><span class='glyphicon glyphicon-pencil' aria-hidden='true'></span></button></td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-danger btn-sm removeEncoder'><span class='glyphicon glyphicon-minus' aria-hidden='true'></button></td>";
    newRow += "</tr>"
    table.children().last().after(newRow);
    
    table.children().last().find('button.removeEncoder').click(function() {
       var $this = $(this);
       $this.parents('tr').remove();
    });
    
}

function buildNodesTable(nodes){
    
    $('#nodesTable').html("<tr><th class='col-md-2'>Type</th><th class='col-md-4'>Host/IP</th><th class='col-md-2'>Port</th><th class='col-md-1'>Parameters</th><th class='col-md-1'>Remove</th></tr>");
    if (nodes != null) {
        for (var i = 0; i < nodes.length; i++){
            addToNodesTable(nodes[i]);
        }
    }
    
}

function buildCommandsTable(commands){
    
    $('#commandsTable').html("<tr><th class='col-md-2'>Command</th><th class='col-md-1'>Config</th><th class='col-md-1'>Remove</th></tr>");
    if (commands != null) {
        for (var i = 0; i < commands.length; i++){
            addToCommandsTable(commands[i]);
        }
    }
    
}

function buildEncodersTable(encoders, table){
    
    table.html("<tr><th class='col-md-2'>Encoder</th><th class='col-md-1'>Config</th><th class='col-md-1'>Remove</th></tr>");
    if (encoders != null) {
        for (var i = 0; i < encoders.length; i++){
            addToEncodersTable(encoders[i],table);
        }
    }
    
}

$(document).ready(function(){

    // Setup
    buildNodesTable(null);
    buildCommandsTable(null);
    buildEncodersTable(null,$('#encodingTable'));
    buildEncodersTable(null,$('#respEncodingTable'));

    $('#respEncodingSelect').hide();
    $('#respEncodingTable').hide();
    
    //Handlers
    $('#addNodeButton').click(function(){
       var $this = $(this);
       var node = {}
       node['name'] = $('#inputNodeTypeSelect').text()
       node['type'] = $('#inputNodeTypeSelect').val();
       node['host'] = $('#inputNodeHost').val();
       node['port'] = $('#inputNodePort').val();
       node['params'] = null;
       addToNodesTable(node);
       
       $('#inputNodeHost').val('');
       $('#inputNodePort').val('');
    });
    
    $('#cmdList button').click(function() {
       
       var $this = $(this);
       var parent = $this.parent('li');
       
       var cmd = {}
       cmd['name'] = parent.text()
       cmd['module'] = $this.val()
       
       addToCommandsTable(cmd);
       
       parent.hide()
        
    });
    
    $('#respEncodingToggle').click(function() {
        var $this = $('#respEncodingSelect');

        if ($('#respEncodingToggle').is(':checked')) {
          $this.show();
          $('#respEncodingTable').show()
          $this.prop("disabled", false);
        } else {
          $this.hide();
          $('#respEncodingTable').hide()
          $this.prop("disabled", true);
        }
    });
    
    $('#encodingSelect').change(function() {
        
        var $this = $(this);
        
        if ($this.val() != null) {
            var encoder = {};
            encoder['name'] = $this.children('option:selected').text();
            encoder['module'] = $this.val();
            
            addToEncodersTable(encoder,$('#encodingTable'));
            $this.prop('selectedIndex', 0);
        }
        
    });
    
    $('#respEncodingSelect').change(function() {
        
        var $this = $(this);
        
        if ($this.val() != null) {

            var encoder = {};
            encoder['name'] = $this.children('option:selected').text()
            encoder['module'] = $this.val();
        
            addToEncodersTable(encoder,$('#respEncodingTable'));
            $this.prop('selectedIndex', 0);
        }
    });
    
});