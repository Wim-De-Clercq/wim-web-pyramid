<%namespace name="util" file="../utils.mako"/>
<%inherit file="/base.mako"/>

<%block name="title">
  Edit user <i>${user.name}
</%block>

<h1 class="title">Edit user <i>${user.name}</i></h1>

<div class="columns">
  <div class="column is-half">

    <form method="post" class="form">
      % for error in form.errors.get('', []):
      <p class="help is-danger is-size-5">${error}</p>
      % endfor
      <div class="field">
        <label class="label">Id</label>
        <div class="control">
          <p>${user.id}</p>
        </div>
      </div>
      ${util.form_field(form, 'name', left_icon='person')}
      ${util.form_field(form, 'email', left_icon='alternate_email')}
      <div class="control">
        <input type="submit" class="button is-primary" value="Edit"/>
      </div>
      <input type="hidden" id="formtarget" name="target" />
    </form>
  </div>
  <div class="column is-half">
  </div>
</div>

<%block name="script">
  ${parent.script()}

  function addReferrer() {
    field = document.getElementById('formtarget');
    field.value = document.referrer;
  }

  document.addEventListener('DOMContentLoaded', () => {
    addReferrer();
  });

</%block>
