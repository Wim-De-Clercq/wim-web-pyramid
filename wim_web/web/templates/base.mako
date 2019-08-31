<%namespace name="top_menu" file="components/top-menu.mako"/>
<%namespace name="notifications" file="components/notifications.mako"/>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title><%block name="title"/></title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="${request.static_url('wim_web:web/static/favicon.ico')}?v=0.1">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
        rel="stylesheet">
  <link rel="stylesheet"
        href="${request.static_url('wim_web:web/static/style.css')}">
  <script type="text/javascript">
    <%block name="script">
    ${top_menu.script()}
    ${notifications.script()}
    </%block>
  </script>
</head>
<body>
  ${top_menu.body()}
  <div class="parent is-flex">
    <%include file="components/side-menu.mako"/>
    <div class="main-wrapper">
      <main class="container">
        ${notifications.body()}
        <%include file="components/breadcrumb.mako"/>
        ${self.body()}
      </main>
    </div>
  </div>
</body>
</html>