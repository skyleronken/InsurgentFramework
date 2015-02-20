<html>
<head>
  <title>{{title or 'No title'}}</title>
  <link href="/src/styles/default.css" rel="stylesheet" media="screen">
  <link href="/src/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
  <script src="/src/scripts/jquery-1.11.2.min.js"></script>
  <script src="/src/bootstrap/js/bootstrap.min.js"></script>
  <script src="/src/scripts/settings_form.js"></script>  
</head>
<body>
  <div class="container-fluid">
    <div class="row">
      %include('header.tpl')
    </div>
    <div class="row">
      <div class="col-md-1"></div>
      <div class="col-md-10">
        %include
      </div>
      <div class="col-md-1"></div>
    </div>
    <div class="row">
    </div>
  </div>
</body>
</html>