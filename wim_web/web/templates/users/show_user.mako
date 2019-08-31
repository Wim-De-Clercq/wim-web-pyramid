<%namespace name="util" file="../utils.mako"/>
<%inherit file="/base.mako"/>

<%block name="title">
  User ${user.name}
</%block>

<h1 class="title">User <i>${user.name}</i></h1>

<div class="columns">
  <div class="column is-half">
    <div class="field">
      <label class="label">Id</label>
      <div class="control">
        <p>${user.id}</p>
      </div>
    </div>
    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <p>${user.name}</p>
      </div>
    </div>
    <div class="field">
      <label class="label">Email</label>
      <div class="control">
        <p>${user.email}</p>
      </div>
    </div>
  </div>

  <div class="column is-half">
    <a class="button is-primary"
       href="${request.relative_url('/users')}/${user.id}/edit">
      <span class="icon">
        <i class="material-icons">create</i>
      </span>
      <span>Edit</span>
    </a>

    <a id="delete" type="submit" class="button is-dark is-tooltip-active
                                        is-tooltip-bottom"
       href="${request.relative_url('/users')}/${user.id}"
       data-tooltip="Click again to confirm.">
      <span class="icon">
        <i class="material-icons">delete</i>
      </span>
      <span>Delete</span>
    </a>
  </div>
</div>

<%block name="script">
  ${parent.script()}

  function addConfirmDeleteEvent() {
    anchor = document.querySelectorAll('#delete')[0]
    anchor.addEventListener(
      'click',
      (event) => {
          event.preventDefault();
          if (anchor.classList.contains('tooltip')) {
            var req = new XMLHttpRequest();
            req.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 204) {
                if (document.referrer) {
                  window.location = document.referrer;
                } else {
                  window.location = "${request.relative_url('/')}";
                }
              }
            };
            req.open("DELETE", anchor.href, true);
            req.send();
            return true;
          } else {
            anchor.classList.toggle('tooltip');
            anchor.classList.toggle('is-danger');
            anchor.classList.toggle('is-dark');
          }
        });
    anchor.addEventListener("focusout", () => {
      anchor.classList.toggle('tooltip');
      anchor.classList.toggle('is-danger');
      anchor.classList.toggle('is-dark');
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    addConfirmDeleteEvent();
  });

</%block>
