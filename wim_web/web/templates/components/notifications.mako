% for notification in request.session.pop_flash('success-notifications'):
<div class="notification is-success">
  <button class="delete"></button>
  ${notification}
</div>
% endfor

% for notification in request.session.pop_flash('failure-notifications'):
<div class="notification is-danger">
  <button class="delete"></button>
  ${notification}
</div>
% endfor

<%def name="script()">
  function addCloseNotificationEvent() {
    (document.querySelectorAll('.notification .delete') || []).forEach(
      (deleteButton) => {
        notification = deleteButton.parentNode;
        deleteButton.addEventListener('click', () => {
          notification.parentNode.removeChild(notification);
        });
      }
    );
  }

  document.addEventListener('DOMContentLoaded', () => {
    addCloseNotificationEvent();
  });

</%def>