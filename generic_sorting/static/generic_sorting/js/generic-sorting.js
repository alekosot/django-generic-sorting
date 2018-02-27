// TODO: This is useless, since it has been copied/pasted into
// generic_sorting_base.html
(function() {
'use strict';

document.addEventListener('DOMContentLoaded', function() {
  var forms = document.querySelectorAll('.generic-sorting-form');
  var dragZone = forms[0].parentNode;
  var form = null;
  var orderApplied = false; // check before submit

  // Find the form
  if (dragZone.tagName == 'form') {
    form = dragZone;
  } else {
    if (typeof dragZone.closest !== 'undefined') {
      form = dragZone.closest('form');
    } else {
      form = dragZone.parentNode;
      while (form.tagName !== 'form') {
        form = form.parentNode;
      }
    }
  }

  dragula([dragZone]);

  form.addEventListener('submit', function(e) {
    if (!orderApplied) {
      e.preventDefault();

      [].forEach.call(document.querySelectorAll('.generic-sorting-form'), function(form, index) {
        form.querySelector('input[id^="id_form-"][id$="-{{ order_by_field }}"]').value = index;
      });

      orderApplied = true;

      form.submit();
    }
  })
});

}());
