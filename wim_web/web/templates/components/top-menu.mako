<nav id="top-menu" class="navbar is-hidden-desktop" role="navigation"
     aria-label="main navigation">
  <div class="container">
    <div class="navbar-brand">
      <a class="navbar-item" href="${request.relative_url('/')}">
        <figure class="image" style="width: 100px">
          <img src="${request.static_url('wim_web:web/static/WimLogo.png')}">
        </figure>
      </a>

      <a role="button" class="navbar-burger burger" aria-label="menu"
         aria-expanded="false" data-target="horizontal-menu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div id="horizontal-menu" class="navbar-menu">
      <div class="navbar-start">
        <a class="navbar-item" href="${request.relative_url('/')}">
          Home
        </a>

        % if request.has_path_permission('view-users', '/users'):
        <a class="navbar-item" href="${request.relative_url('/users')}">
          Users
        </a>
        % endif
        % if request.has_path_permission('view-items', '/items'):
        <a class="navbar-item" href="${request.relative_url('/items')}">
          Items
        </a>
        % endif

        <a class="navbar-item">
          Files
        </a>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            % if not request.authenticated_userid:
            <a class="button is-dark" href="${request.relative_url('/login')}">
              Log in
            </a>
            <a class="button is-primary" href="${request.relative_url('/register')}">
              Sign up
            </a>
            % else:
            <div class="navbar-item">
              ${request.user.name}
            </div>
            <a class="button is-dark"
               href="${request.relative_url('/logout')}">
              Logout
            </a>
            <a class="button is-primary"
               href="${request.relative_url('/users/') + str(request.authenticated_userid)}">
              Profile
            </a>
            % endif
          </div>
        </div>
      </div>
    </div>
  </div>
</nav>

<%def name="script()">
function addMenuBurgerClickEvent() {
  (document.querySelectorAll('.navbar-burger') || []).forEach(
    (el) => {
      el.addEventListener('click', () => {
        const targetStr = el.dataset.target;
        const target = document.getElementById(targetStr);
        el.classList.toggle('is-active');
        target.classList.toggle('is-active');
      });
    }
  );
}

document.addEventListener('DOMContentLoaded', () => {
  addMenuBurgerClickEvent();
});

console.log('log example 1');
</%def>

