<%namespace name="util" file="../utils.mako"/>
<%inherit file="/base.mako"/>

<%block name="title">
  Create item
</%block>

<h1 class="title">Create Item</h1>

<div class="columns">
  <div class="column is-half">

    <form method="post" class="form">
      % for error in form.errors.get('', []):
      <p class="help is-danger is-size-5">${error}</p>
      % endfor
      ${util.form_field(form, 'title', left_icon='title')}
      ${util.form_field(form, 'description', input_class='textarea')}
      <div class="control">
        <input type="submit" class="button is-primary" value="Create"/>
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