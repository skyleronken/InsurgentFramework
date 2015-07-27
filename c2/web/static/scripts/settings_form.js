
var _nodes = [];
var _beacons = [];
var _encoders = [];
var _commands = [];
var _decoders = [];
var _responders = [];

function activaTab(tab){
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
};

function generateNodesXML(){

    var xml = "<nodes>";

    for (var i = 0; i < _nodes.length; i++){
        
        xml = xml + "<node type='" + _nodes[i]['type'] + "'>";
        xml = xml + "<host>" + _nodes[i]['host'] + "</host>";
        xml = xml + "<port>" + _nodes[i]['port'] + "</port>";
        //Do parameters here
        
        xml = xml + "</node>";
    }
    
    xml = xml + "</nodes>";
    
    return xml;
    
}

function generateBehaviorsXML(){
    
    var xml = "<behaviors>";
    
    xml = xml + "</behaviors>";
    
    return xml;
    
}

function generateNodeModulesXML(tag,mod_array){
    
    var xml = "<" + tag + ">";
    
    for (var i = 0; i < mod_array.length; i++){
    
        xml = xml + "<module>";
        xml = xml + "<type>";
        xml = xml + mod_array[i]['type'];
        xml = xml + "</type>";
        xml = xml + "</module>";
        
    }
    
    xml = xml + "</" + tag + ">";
    
    return xml;
    
}

function generateCommandsXML(){
    
    var xml = "<commands>";
    
    for (var i = 0; i < _commands.length; i++){
    
        xml = xml + "<module>";
        xml = xml + "<type>";
        xml = xml + _commands[i]['module'];
        xml = xml + "</type>";
        xml = xml + "</module>";
        
    }
    
    xml = xml + "</commands>";
    
    return xml;
    
}

function generateCodecXML(tag,mod_array){
    
    var xml = "<" + tag + ">";
    
    for (var i = 0; i < mod_array.length; i++){
    
        xml = xml + "<module order='"+ (parseInt(i)+1) +"'>";
        xml = xml + "<type>";
        xml = xml + mod_array[i]['module'];
        xml = xml + "</type>";
        xml = xml + "</module>";
        
    }
    
    xml = xml + "</" + tag + ">";
    
    return xml;
    
}

function generateModulesXML(){
    
    var xml = "<modules>";
    
    xml = xml + generateNodeModulesXML("beacons",_beacons);
    xml = xml + generateCommandsXML();
    xml = xml + generateCodecXML("decoders",_decoders);
    xml = xml + generateCodecXML("encoders",_encoders);
    xml = xml + generateNodeModulesXML("responders",_responders);
    
    xml = xml + "</modules>"; 
    
    return xml;
    
}

function GenerateXML(){

    var xml = ""
    xml = xml + "<root>";
    
    xml = xml + generateNodesXML();
    xml = xml + generateBehaviorsXML();
    xml = xml + generateModulesXML();
    
    xml = xml + "</root>";

    return xml;

}

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
    
    _nodes.push(node);
    
    $('#nodesTable tr:last button.removeNode').click(function() {
       var $this = $(this);
       $this.parents('tr').remove();
    });
}

function addToCommandsTable(cmd){
    
    var cmd_name = cmd['name']
    var cmd_module = cmd['module']
    
    var newRow = "<tr>";
    newRow += "<td class='col-md-2'>" + cmd_name + "</td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-primary btn-sm editCommand'><span class='glyphicon glyphicon-pencil' aria-hidden='true'></span></button></td>";
    newRow += "<td class='col-md-1'><button type='button' class='btn btn-danger btn-sm removeCommand'><span class='glyphicon glyphicon-minus' aria-hidden='true'></button></td>";
    newRow += "</tr>"
    $('#commandsTable tr:last').after(newRow);
    
    _commands.push(cmd);
    
    $('#commandsTable tr:last button.removeCommand').click(function() {
       var $this = $(this);
       
       var index = $('#commandsTable tr').index($this.parents('tr')) - 1;
       _commands.splice(index,1);
       
       $this.parents('tr').remove();
       $('#'+cmd_module+'_li').show();
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
    
    var id = table[0].id;
    if (id == "encodingTable"){
       _decoders.push(encoder);
    } else if (id == "respEncodingTable"){
       _encoders.push(encoder);
    }

    table.children().last().find('button.removeEncoder').click(function() {
       var $this = $(this);
       
       var index = table.children('tr').index($this.parents('tr'));

       var id = table[0].id;
       if (id == "encodingTable"){
           _decoders.splice(index,1);
       } else if (id == "respEncodingTable"){
           _encoders.splice(index,1);
       }
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
    
    table.html("<tr><th class='col-md-2'>Codec</th><th class='col-md-1'>Config</th><th class='col-md-1'>Remove</th></tr>");
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
    
    
    $('#buildButton').click(function(){
       
        var xml = GenerateXML();
        
        $.getScript('/src/scripts/Blob.js', function()
        {
            $.getScript('/src/scripts/FileSaver.js', function()
            {
                var blob = new Blob([xml], {type: "text/plain;charset=utf-8"});
                saveAs(blob, "settings.xml");
            });
        });
        
    });
    
});