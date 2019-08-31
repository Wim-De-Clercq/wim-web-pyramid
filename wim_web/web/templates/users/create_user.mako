<%namespace name="util" file="../utils.mako"/>
<%inherit file="/base.mako"/>

<%block name="title">
  Register
</%block>

<h1 class="title">Register</h1>

<div class="columns">
  <div class="column is-half">

    <form method="post" class="form">
      % for error in form.errors.get('', []):
      <p class="help is-danger is-size-5">${error}</p>
      % endfor
      ${util.form_field(form, 'name', left_icon='person')}
      ${util.form_field(form, 'email', left_icon='alternate_email')}
      ${util.form_field(form, 'password', left_icon='lock')}
      <div class="control">
        <input type="submit" class="button is-primary" value="Register"/>
      </div>
    </form>
  </div>

  <div class="column is-half">
  </div>

</div>
