<%inherit file="/base.mako"/>

<%block name="title">
Page not found.
</%block>

<section class="hero">
  <div class="hero-body">
    <div class="container">
      <article class="message is-warning">
        <div class="message-header">
          <p>
            <i class="material-icons">error_outline</i>
            Not found
          </p>
        </div>
        <div class="message-body">
          ${msg}
        </div>
      </article>
    </div>
  </div>
</section>