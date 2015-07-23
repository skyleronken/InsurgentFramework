%def nodesform():
<div class="container">
    <div class="row">
        <div class="col-md-6">
            <h2>Define Nodes</h2>
        </div>
        <div class="col-md-6">
            <nav>
              <ul class="pager">
                <!--<li><button onclick="activaTab('bbb');" class="btn btn-default">Previous</button></li>-->
                <li><button onclick="activaTab('encoding');" class="btn btn-default">Next</button></li>
              </ul>
            </nav>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <form class="form-horizontal">
              <div class="form-group">
                <label for="inputNodeType" class="col-sm-2 control-label">Type</label>
                <div class="col-sm-3" id="inputNodeType">
                    <select class="form-control" id="inputNodeTypeSelect">
                        % for node in node_modules:
                          <option value="{{node.__module__.split('.')[-1]}}">{{node.display_name}}</option>
                        % end
                    </select>
                </div>
              </div>
              <div class="form-group">
                <label for="inputNodeHost" class="col-sm-2 control-label">Host/IP</label>
                <div class="col-sm-6">
                  <input type="input" class="form-control" id="inputNodeHost" placeholder="Host/IP">
                </div>
              </div>
              <div class="form-group">
                <label for="inputNodePort" class="col-sm-2 control-label">Port</label>
                <div class="col-sm-2">
                  <input type="input" class="form-control" id="inputNodePort" placeholder="Port">
                </div>
              </div>
              <div class="form-group">
                <label for="inputNodeParams" class="col-sm-2 control-label">Parameters*</label>
                <div class="col-sm-6">
                  <textarea class="form-control" id="inputNodeParams" rows="3"></textarea>
                  <br>
                  <small class="col-sm-offset-3">* line separated 'key=value' format</small>
                </div>
              </div>
              <div class="form-group">
                <div class="col-sm-offset-2 col-sm-10">
                  <button id="addNodeButton" type="button" class="btn btn-default">Add Node</button>
                </div>
              </div>
            </form>
        </div>
        <div class="col-md-6">
            <table class="table table-condensed table-bordered" id="nodesTable">
            </table>
        </div>
    </div>
</div>
%end

%def commandsform():
<div class="container">
    <div class="row">
        <div class="col-md-6">
            <h2>Select Commands</h2>
        </div>
        <div class="col-md-6">
            <nav>
              <ul class="pager">
                <li><button onclick="activaTab('encoding');" class="btn btn-default">Previous</button></li>
                <li><button onclick="activaTab('build');" class="btn btn-default">Next</button></li>
              </ul>
            </nav>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <ul class="list-group" id="cmdList">
              % for cmd in command_modules:
                <li class="list-group-item" id="{{cmd.__module__.split('.')[-1]}}_li">
                  <button type="button" class="btn btn-primary btn-sm" value="{{cmd.__module__.split('.')[-1]}}"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
                  {{cmd.display_name}}
                </li>
              %end
            </ul>
        </div>
        <div class="col-md-6">
            <table class="table table-condensed table-bordered" id="commandsTable">
            </table>
        </div>
    </div>
</div>
%end

%def encodingsform():
<div class="container">
    <div class="row">
        <div class="col-md-6">
            <h2>Select Encoding</h2>
        </div>
        <div class="col-md-6">
            <nav>
              <ul class="pager">
                <li><button onclick="activaTab('nodes');" class="btn btn-default">Previous</button></li>
                <li><button onclick="activaTab('commands');" class="btn btn-default">Next</button></li>
              </ul>
            </nav>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <ul class="list-group">
              <select class="form-control" id="encodingSelect">
                  <option value=null>Select...</option>
                % for codec in encoding_modules:
                  <option value="{{codec.__module__.split('.')[-1]}}">{{codec.display_name}}</option>
                % end
              </select>
            </ul>
        </div>
      <div class="col-md-6">
            <table class="table table-condensed table-bordered" id="encodingTable">
            </table>
        </div>
    </div>
    <div class="row">
        <input type="checkbox" name="respEncoding" id="respEncodingToggle" value="true">Use different encoding for responses.</br>
    </div>
    <div class="row">
        <div class="col-md-6">
          <select class="form-control" id='respEncodingSelect' disabled>
              <option value=null>Select...</option>
            % for codec in encoding_modules:
              <option value="{{codec.__module__.split('.')[-1]}}">{{codec.display_name}}</option>
            % end
          </select>
        </div>
      <div class="col-md-6">
            <table class="table table-condensed table-bordered" id="respEncodingTable">
            </table>
        </div>
    </div>
</div>
%end

%def buildform():
<div class="jumbotron">
  <div class="center-block">
    <button type="button" class="btn btn-danger btn-lg"><span class="glyphicon glyphicon-wrench" aria-hidden="true"></span> Build</button>
  </div>
</div>
%end

%rebase('settings_form.tpl', nodesform=nodesform, commandsform=commandsform, encodingsform=encodingsform, buildform=buildform)