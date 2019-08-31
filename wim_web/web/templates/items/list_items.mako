<%namespace name="utils" file="../utils.mako"/>
<%inherit file="/base.mako"/>

<%!
    def trim100(text):
        return utils.trim(100, text)
%>

<%block name="title">
  Items
</%block>

<h1 class="title">
  Items
  <a class="button is-primary" href="${request.relative_url('/items/create')}">
    Create
  </a>
</h1>
<div class="columns is-multiline">
  % for index, item in enumerate(items):
  <div class="column is-one-quarter-fullhd is-one-third-desktop is-half-tablet is-full-mobile">
    <div class="card" style="min-width: 250px;">
      <header class="card-header">
        <p class="card-header-title">
          ${item.title}
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          ${item.description | utils.trim100}
        </div>
      </div>
      <footer class="card-footer">
        <a href="${request.relative_url('/items')}/${item.id}" class="card-footer-item">
          <i class="material-icons size-24">remove_red_eye</i>Open
        </a>
        <a href="${request.relative_url('/items')}/${item.id}/edit" class="card-footer-item">
          <i class="material-icons size-24 ">create</i>Edit
        </a>
        <a class="card-footer-item confirm-delete has-text-dark is-tooltip-active
                  is-tooltip-top"
           href="${request.relative_url('/items')}/${item.id}"
           data-tooltip="Click again to confirm.">
          <i class="material-icons size-24 ">delete</i>Delete
        </a>
      </footer>
    </div>
  </div>
  % endfor
</div>

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
                card = anchor.closest('div.column');
                card.parentNode.removeChild(card);
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