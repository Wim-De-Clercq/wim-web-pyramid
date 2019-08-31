<%inherit file="/base.mako"/>

<%block name="title">
  Users
</%block>

<h1 class="title">Users</h1>
<table class="table is-fullwidth is-striped is-hoverable">
  <thead>
    <tr>
      <th>ID</th>
      <th>name</th>
      <th>email</th>
      <th class="limit3">actions</th>
    </tr>
  </thead>
    % for user in users:
    <tr>
      <th>${user.id}</th>
      <td>
        <a href="${request.relative_url('/users')}/${user.id}">
          ${user.name}
        </a>
      </td>
      <td>${user.email}</td>
      <td class="limit3">
        <a class="has-text-dark material-icons size-24"
           href="${request.relative_url('/users')}/${user.id}/edit">
          create
        </a>
        <a class="confirm-delete has-text-dark is-tooltip-active
                  is-tooltip-right"
           href="${request.relative_url('/users')}/${user.id}"
           data-tooltip="Click again to confirm.">
          <i class="material-icons size-24 ">delete</i>
        </a>
      </td>
    </tr>
    % endfor
  </tbody>
</table>

<%block name="script">
  ${parent.script()}

  function addConfirmDeleteEvent() {
    (document.querySelectorAll('.confirm-delete') || []).forEach(
      (anchor) => {
        anchor.addEventListener('click', (event) => {
          event.preventDefault();
          if (anchor.classList.contains('tooltip')) {
            var req = new XMLHttpRequest();
            req.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 204) {
                tr = anchor.closest('tr');
                tr.parentNode.removeChild(tr);
              }
            };
            req.open("DELETE", anchor.href, true);
            req.setRequestHeader("Accept", "application/json");
            req.send();
            return true;
          } else {
            anchor.classList.toggle('tooltip');
            anchor.classList.toggle('has-text-dark');
            anchor.classList.toggle('has-text-danger');
          }
        });
        anchor.addEventListener("focusout", () => {
          anchor.classList.toggle('tooltip');
          anchor.classList.toggle('has-text-dark');
          anchor.classList.toggle('has-text-danger');
        });
      }
    );
  }

  document.addEventListener('DOMContentLoaded', () => {
    addConfirmDeleteEvent();
  });

</%block>