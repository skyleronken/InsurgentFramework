%def nodesform():
<div class="container">
    <div class="row">
        <div class="col-md-6">
            <h2>Define Nodes</h2>
        </div>
        <div class="col-md-6">
            <nav>
              <ul class="pager">
                <li><a href="/#info">Previous</a></li>
                <li><a href="/#behaviors">Next</a></li>
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
                    <select class="form-control">
                        % for node in node_modules:
                          <option>{{node.display_name}}</option>
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
                  <button type="submit" class="btn btn-default">Add Node</button>
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
                <li><a href="/#info">Previous</a></li>
                <li><a href="/#behaviors">Next</a></li>
              </ul>
            </nav>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <ul class="list-group">
              % for cmd in command_modules:
                <li class="list-group-item">
                  <button type="button" class="btn btn-primary btn-sm"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
                  {{cmd.display_name}}
                </li>
              %end
            </ul>
        </div>
        <div class="col-md-6">
            <table class="table table-condensed table-bordered" id="nodesTable">
            </table>
        </div>
    </div>
</div>
%end

%rebase('settings_form.tpl', nodesform=nodesform, commandsform=commandsform)