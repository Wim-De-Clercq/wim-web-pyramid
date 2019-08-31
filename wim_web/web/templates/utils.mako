<%def name="form_field(form, field_name, label_class='label',
                       input_class='input', left_icon=None, right_icon=None)">

  <% field = getattr(form, field_name) %>

  <div class="field">
    ${field.label(class_=label_class)}
    <div class="control ${'has-icons-left' if left_icon else ''}
                ${'has-icons-right' if right_icon else ''}">
      ${field(class_=input_class + (' is-danger' if field.errors else ''),
              placeholder=field.label.text)}
      % if left_icon:
        <span class="icon is-small is-left">
          <i class="material-icons">${left_icon}</i>
        </span>
      % endif
      % if right_icon:
        <span class="icon is-small is-right">
          <i class="material-icons">${right_icon}</i>
        </span>
      % endif
    </div>
    % for error in field.errors:
    <p class="help is-danger">${error}</p>
    % endfor
  </div>

</%def>

<%def name="trim100(text)">
    ${text[:97] + (text[97:] and '..')}
</%def>