% if request.path and request.path != '/':
<nav class="breadcrumb" aria-label="breadcrumbs">
  <ul>
    <li><a href="/">Home</a></li>
    <%
    path = ''
    crumbs = []
    for crumb in request.path.split('/')[1:]:
      if not crumb:
        continue
      path += '/' + crumb
      crumbs.append((request.relative_url(path), crumb))
    %>
    % for href, label in crumbs[:-1]:
    <li>
      <a href="${href}">${label}</a>
    </li>
    % endfor
    <li class="is-active">
      <a href="${crumbs[-1][0]}" aria-current="page">
        ${crumbs[-1][1]}
      </a>
    </li>
  </ul>
</nav>
% endif