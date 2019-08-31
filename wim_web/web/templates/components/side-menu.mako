<aside class="menu is-hidden-touch">
  <a class="navbar-item" style="padding: 0; padding-bottom: 1em;"
      href="${request.relative_url('/')}">
    <figure class="image" style="width: 100px;">
      <img src="${request.static_url('wim_web:web/static/WimLogo.png')}">
    </figure>
  </a>
  <div class="buttons">
    % if not request.authenticated_userid:
    <ul class="menu-list">
      <li>
        <a class="button is-dark" href="${request.relative_url('/login')}">
          Log in
        </a>
      </li>
      <li>
        <a class="button is-primary" href="${request.relative_url('/register')}">
          Sign up
        </a>
      </li>
    </ul>
    % else:
    <ul class="menu-list">
      <p class="menu-label">
        ${request.user.name}
      </p>
      <li>
        <a class="button is-dark"
           href="${request.relative_url('/logout')}">
          Logout
        </a>
      </li>
      <li>
        <a class="button is-primary"
           href="${request.relative_url('/users/') + str(request.authenticated_userid)}">
          Profile
        </a>
      </li>
    </ul>
    % endif
  </div>
  <p class="menu-label">
    Administration
  </p>
  <ul class="menu-list">
    % if request.has_path_permission('view-users', '/users'):
    <li>
      <a href="${request.relative_url('/users')}">Users</a>
    </li>
    % endif
    % if request.has_path_permission('view-items', '/items'):
    <li>
      <a href="${request.relative_url('/items')}">Items</a>
    </li>
    % endif
  </ul>
</aside>